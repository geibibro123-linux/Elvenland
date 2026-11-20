#!/usr/bin/env python3
"""Validate a user-supplied Elvenar ResearchTechnologies*.json as READ-ONLY evidence.

Input is the original-format JSON array of ResearchTechnologyConfigVO objects.
The output is intentionally NEVER an active Elvenland gameplay definition.
No values, IDs, prices, parents, chapters, or unlock effects are fabricated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from collections import defaultdict, deque
from pathlib import Path
from typing import Any


class ResearchSourceError(ValueError):
    """A source cannot be safely interpreted as the declared research data."""


def _integer(value: Any, field: str, optional: bool = False) -> int | None:
    if value is None and optional:
        return None
    if type(value) is int and value >= 0:
        return value
    if isinstance(value, str) and re.fullmatch(r"[0-9]+", value.strip()):
        return int(value.strip())
    raise ResearchSourceError(f"{field}: expected a non-negative integer or decimal integer string")


def _str(value: Any, field: str, optional: bool = False) -> str | None:
    if optional and value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ResearchSourceError(f"{field}: expected nonempty string")
    return value


def _ids(value: Any, field: str) -> list[str] | None:
    if value is None:
        return None
    if not isinstance(value, list):
        raise ResearchSourceError(f"{field}: expected list or null")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ResearchSourceError(f"{field}: invalid ID")
    if len(value) != len(set(value)):
        raise ResearchSourceError(f"{field}: duplicate ID")
    return list(value)


def _resources(value: Any, field: str) -> dict[str, int] | None:
    """Retain explicit {} separately from missing resources (None)."""
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ResearchSourceError(f"{field}: expected resources dictionary")
    result: dict[str, int] = {}
    for resource_id, amount in value.items():
        if resource_id == "__class__":
            continue
        _str(resource_id, field + ".resource_id")
        result[resource_id] = _integer(amount, field + "." + resource_id)
    return result


def _requirements(value: Any, field: str) -> dict[str, int] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ResearchSourceError(f"{field}: expected object")
    return _resources(value.get("resources"), field + ".resources")


def _rewards(value: Any, field: str) -> list[dict[str, Any]] | None:
    if value is None:
        return None
    if not isinstance(value, list):
        raise ResearchSourceError(f"{field}: expected list")
    result = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise ResearchSourceError(f"{field}[{index}]: expected object")
        # Preserve supplied values exactly. Never infer a building/unlock from a title.
        result.append({k: v for k, v in item.items() if k != "__class__"})
    return result


def _no_cycles(records: list[dict[str, Any]]) -> None:
    ids = {r["tech_id"] for r in records}
    indegree: dict[str, int] = {x: 0 for x in ids}
    children: dict[str, list[str]] = defaultdict(list)
    for row in records:
        for parent in row["parent_ids"] or []:
            if parent == row["tech_id"]:
                raise ResearchSourceError("self-referencing technology " + parent)
            if parent in ids:
                indegree[row["tech_id"]] += 1
                children[parent].append(row["tech_id"])
    todo = deque(sorted(node for node, degree in indegree.items() if degree == 0))
    visited = 0
    while todo:
        node = todo.popleft()
        visited += 1
        for child in children[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                todo.append(child)
    if visited != len(ids):
        raise ResearchSourceError("cycle in extracted parentIds graph")


def build_reference(
    raw_records: Any, *, race: str, source_url: str, source_version: str,
    expected_count: int | None = None, source_sha256: str | None = None
) -> dict[str, Any]:
    """Build a provenance-rich, read-only excerpt from an authentic-format file."""
    if race not in ("elves", "humans"):
        raise ResearchSourceError("race must be elves or humans")
    _str(source_url, "source_url")
    _str(source_version, "source_version")
    if not isinstance(raw_records, list) or not raw_records:
        raise ResearchSourceError("Source must be a nonempty array of technology objects")
    all_source_ids: set[str] = set()
    extracted: list[dict[str, Any]] = []
    warnings: list[str] = []
    for index, row in enumerate(raw_records):
        context = f"records[{index}]"
        if not isinstance(row, dict):
            raise ResearchSourceError(context + ": expected technology object")
        raw_class = row.get("__class__")
        if raw_class is not None and raw_class != "ResearchTechnologyConfigVO":
            raise ResearchSourceError(context + ": unexpected __class__")
        tech_id = _str(row.get("id"), context + ".id")
        if tech_id in all_source_ids:
            raise ResearchSourceError("Duplicate technology ID " + tech_id)
        all_source_ids.add(tech_id)
        if row.get("race") != race:
            raise ResearchSourceError(context + ": record race does not match declared race")
        chapter = _integer(row.get("section"), context + ".section")
        if not (1 <= chapter <= 100):
            raise ResearchSourceError(context + ".section: outside expected positive chapter range")
        if chapter not in (1, 2, 3, 4, 5):
            continue
        gate = row.get("gate")
        if gate is not None and not isinstance(gate, dict):
            raise ResearchSourceError(context + ".gate: expected object")
        kp_cost = _integer(row.get("maxSP"), context + ".maxSP", optional=True)
        parents = _ids(row.get("parentIds"), context + ".parentIds")
        children = _ids(row.get("childrenIds"), context + ".childrenIds")
        activation = _requirements(row.get("requirements"), context + ".requirements")
        gate_provinces = _integer(
            gate.get("completedProvinces"), context + ".gate.completedProvinces",
            optional=True
        ) if gate else None
        gate_rewards = _requirements(
            gate.get("rewards"), context + ".gate.rewards"
        ) if gate else None
        extracted.append({
            "tech_id": tech_id,
            "name_source": _str(row.get("name"), context + ".name", optional=True),
            "race": race,
            "chapter": chapter,
            "knowledge_points": kp_cost,
            "activation_requirements": activation,
            "parent_ids": parents,
            "children_ids_for_display_only": children,
            "unlock_effects": _rewards(row.get("rewards"), context + ".rewards"),
            "category": _str(row.get("category"), context + ".category", optional=True),
            "required_provinces": gate_provinces,
            "gate_rewards": gate_rewards,
            "feature_flag": _str(row.get("featureFlag"), context + ".featureFlag", optional=True),
            "source_status": "USER_SUPPLIED_ORIGINAL_FORMAT_NOT_AUTHENTICATED",
            "activation_ready": False,
            "active_elvenland_balance": False
        })
    _no_cycles(extracted)
    extracted_ids = {x["tech_id"] for x in extracted}
    missing_source = sorted({p for row in extracted for p in (row["parent_ids"] or [])
                             if p not in all_source_ids})
    external_section = sorted({p for row in extracted for p in (row["parent_ids"] or [])
                               if p in all_source_ids and p not in extracted_ids})
    if missing_source:
        warnings.append("parentIds not present in supplied full source: " + ", ".join(missing_source))
    if expected_count is not None and len(extracted) != expected_count:
        warnings.append(f"Expected {expected_count} early rows, found {len(extracted)}; do not fabricate missing records")
    if any(x["knowledge_points"] is None for x in extracted):
        warnings.append("Some source nodes have no maxSP, possibly non-research root anchors")
    if any(x["activation_requirements"] is None for x in extracted):
        warnings.append("Missing activation requirements remain null, NEVER free")
    if any(x["parent_ids"] is None for x in extracted):
        warnings.append("Missing parentIds remain null, NEVER a free prerequisite")
    if not extracted:
        warnings.append("Supplied source has no chapter I-V rows")
    return {
        "_meta": {
            "schema": "ELVENLAND_ORIGINAL_RESEARCH_READONLY_EXTRACTION_V1",
            "source_url": source_url,
            "source_version": source_version,
            "source_sha256": source_sha256,
            "race": race,
            "source_format": "ResearchTechnologyConfigVO[]",
            "source_authenticity_independently_verified": False,
            "current_original_server_values_verified": False,
            "active_elvenland_balance_updated": False,
            "approval_as_gameplay_definitions": False,
            "missing_fields_are_null_not_zero": True,
            "cost_minimum_rule": "FEST only when same race, tech, resource and unlock step; this script does not merge historical versions"
        },
        "summary": {
            "total_source_records": len(raw_records),
            "early_chapter_records": len(extracted),
            "per_chapter_count": {str(ch): sum(x["chapter"] == ch for x in extracted)
                                  for ch in range(1, 6)},
            "early_rows_with_kp": sum(x["knowledge_points"] is not None for x in extracted),
            "early_rows_with_explicit_activation_resources": sum(
                x["activation_requirements"] is not None for x in extracted),
            "early_rows_with_parent_ids": sum(x["parent_ids"] is not None for x in extracted),
            "early_rows_with_reward_list": sum(x["unlock_effects"] is not None for x in extracted),
            "external_parents_in_other_chapters": external_section,
            "parent_ids_not_in_source": missing_source,
            "approved_active_nodes": 0,
            "warnings": warnings
        },
        "nodes": extracted
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--race", required=True, choices=["elves", "humans"])
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--source-version", required=True)
    parser.add_argument("--expected-count", type=int, default=None)
    args = parser.parse_args()
    if any(part.lower() in ("definitions", "active") for part in args.output.parts):
        raise SystemExit("Refusing to overwrite active gameplay definitions")
    data_bytes = args.input.read_bytes()
    doc = build_reference(json.loads(data_bytes), race=args.race,
                          source_url=args.source_url, source_version=args.source_version,
                          expected_count=args.expected_count,
                          source_sha256=hashlib.sha256(data_bytes).hexdigest())
    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=output.parent,
        prefix=output.name + ".", suffix=".tmp", delete=False)
    try:
        with handle:
            json.dump(doc, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(handle.name, output)
    finally:
        if os.path.exists(handle.name):
            os.unlink(handle.name)
    print(json.dumps(doc["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

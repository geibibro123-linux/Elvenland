#!/usr/bin/env python3
"""Synthetic tests for read-only research data extraction.

All values, names, IDs and costs in these fixtures are invented FOR TESTING ONLY.
They are not historic Elvenar facts and must never become game data.
"""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "extract_research_balancing_reference.py"
SPEC = importlib.util.spec_from_file_location("research_extractor", SCRIPT)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def fixture():
    return [
        {"__class__": "ResearchTechnologyConfigVO",
         "id": "elves_test_root", "race": "elves", "section": 1,
         "parentIds": [], "childrenIds": ["elves_test_production"]},
        {"__class__": "ResearchTechnologyConfigVO",
         "id": "elves_test_production", "race": "elves", "section": 1,
         "name": "TEST PRODUCTION - NOT GAME DATA", "maxSP": "8",
         "requirements": {"__class__": "CityResourceVO",
                          "resources": {"__class__": "ResourcesVO", "money": "2500"}},
         "parentIds": ["elves_test_root"], "childrenIds": ["elves_test_gate"],
         "rewards": [{"__class__": "ResearchRewardVO",
                      "type": "building", "value": "test_building"}]},
        {"__class__": "ResearchTechnologyConfigVO",
         "id": "elves_test_gate", "race": "elves", "section": 5,
         "maxSP": "20", "requirements": {"resources": {}},
         "parentIds": ["elves_test_production"], "childrenIds": ["elves_test_late"],
         "gate": {"__class__": "ResearchGateVO", "completedProvinces": "17",
                  "rewards": {"resources": {"money": 300}}}},
        {"__class__": "ResearchTechnologyConfigVO",
         "id": "elves_test_late", "race": "elves", "section": 6,
         "maxSP": "60", "parentIds": ["elves_test_gate"]}
    ]


def extract(rows, race="elves", expected_count=None):
    return module.build_reference(
        rows, race=race,
        source_url="https://example.org/synthetic-test-data.json",
        source_version="TEST_FIXTURE_ONLY",
        expected_count=expected_count
    )


class ReadOnlyExtractorTests(unittest.TestCase):
    def test_extracts_only_first_five_chapters(self):
        r = extract(fixture())
        self.assertEqual(3, r["summary"]["early_chapter_records"])
        self.assertEqual(4, r["summary"]["total_source_records"])
        self.assertEqual(0, r["summary"]["approved_active_nodes"])
        self.assertFalse(r["_meta"]["approval_as_gameplay_definitions"])

    def test_unknown_never_free(self):
        r = extract(fixture())
        root = r["nodes"][0]
        self.assertIsNone(root["knowledge_points"])
        self.assertIsNone(root["activation_requirements"])
        self.assertEqual([], root["parent_ids"])
        self.assertFalse(root["activation_ready"])

    def test_explicit_resources_and_gate(self):
        r = extract(fixture())
        prod, gate = r["nodes"][1:]
        self.assertEqual(8, prod["knowledge_points"])
        self.assertEqual({"money": 2500}, prod["activation_requirements"])
        self.assertEqual(["elves_test_root"], prod["parent_ids"])
        self.assertEqual("test_building", prod["unlock_effects"][0]["value"])
        self.assertEqual({}, gate["activation_requirements"])
        self.assertEqual(17, gate["required_provinces"])
        self.assertEqual({"money": 300}, gate["gate_rewards"])

    def test_mismatch_is_warning_not_data_fabrication(self):
        r = extract(fixture(), expected_count=124)
        self.assertEqual(3, len(r["nodes"]))
        self.assertTrue(any("Expected 124" in w for w in r["summary"]["warnings"]))

    def test_wrong_race_rejected(self):
        with self.assertRaises(module.ResearchSourceError):
            extract(fixture(), race="humans")

    def test_duplicate_id_rejected(self):
        rows = fixture()
        rows.append(dict(rows[1]))
        with self.assertRaises(module.ResearchSourceError):
            extract(rows)

    def test_negative_cost_rejected(self):
        rows = fixture()
        rows[1]["requirements"]["resources"]["money"] = -1
        with self.assertRaises(module.ResearchSourceError):
            extract(rows)

    def test_cycle_rejected(self):
        rows = fixture()
        rows[0]["parentIds"] = ["elves_test_gate"]
        with self.assertRaises(module.ResearchSourceError):
            extract(rows)

    def test_boolean_cost_rejected(self):
        rows = fixture()
        rows[1]["requirements"]["resources"]["money"] = True
        with self.assertRaises(module.ResearchSourceError):
            extract(rows)

    def test_missing_parents_stay_null(self):
        rows = fixture()
        rows[1].pop("parentIds")
        r = extract(rows)
        self.assertIsNone(r["nodes"][1]["parent_ids"])
        self.assertFalse(r["nodes"][1]["activation_ready"])


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Compile verified and community-sourced reference research to read-only Godot-friendly JSON.

Strictly separate historical reference from active gameplay and avoid inventing
technology ids, tech prerequisites, cost amounts or chapter stubs.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
LATE_PATH="data/reference/community_idavis_research_ch06_ch26_2026-11-20.json"
EARLY_PATH="data/reference/community_early_research_ch01_ch05_2026-11-20.json"
ACTIVE_PATH="data/definitions/research_nodes.json"
OUT_PATH="data/reference/compiled_research_readonly_preview_2026-11-20.json"

def read(rel):
    return json.loads((ROOT/rel).read_text(encoding="utf-8"))

late=read(LATE_PATH)
early=read(EARLY_PATH)
active=read(ACTIVE_PATH)
assert active["definitions"]==[], "Active research definitions must stay empty"
source_url=late["_meta"]["source_url"]
late_rows=[]
seen=set()
for chapter_key, rows in late["chapters"].items():
    ch=int(chapter_key.replace("ch",""))
    for row in rows:
        tid=row["id"]
        assert tid.startswith("elves_") and tid not in seen,tid
        seen.add(tid)
        requirements=row.get("requirements")
        assert isinstance(requirements,list) and len(requirements)>0,(tid,requirements)
        flat={}
        for item in requirements:
            assert isinstance(item,dict) and len(item)==1, (tid,item)
            for k,v in item.items():
                assert isinstance(k,str) and (isinstance(v,(int,float)) and not isinstance(v,bool)) and v>=0,(tid,k,v)
                assert k not in flat,(tid,k)
                flat[k]=v
        parents=row.get("parentIds")
        children=row.get("childrenIds")
        assert isinstance(parents,list) and isinstance(children,list),(tid,parents)
        parent_outside=[]   # checked after collecting every source ID
        late_rows.append({
          "preview_key":tid,
          "tech_id":tid,
          "race":"elves",
          "chapter":ch,
          "name_source":row.get("name"),
          "knowledge_points":int(row["kp"]),
          "activation_requirements":flat,
          "parent_ids":parents,
          "children_ids_for_display_only":children,
          "unresolved_parent_ids":parent_outside,
          "source_status":"COMMUNITY_STRUCTURED_HISTORICAL_REFERENCE",
          "source_url":source_url,
          "display_ready":True,
          "activation_ready":False,
          "activation_block_reason":"HISTORICAL_SOURCE_NOT_PROMOTED_TO_ACTIVE_ELVENLAND_BALANCE",
        })
for row in late_rows:
    row["unresolved_parent_ids"]=[p for p in row["parent_ids"] if p not in seen]

early_rows=[]
for row in early["selected_tech"]:
    tid=row.get("apk_matched_tech_id")
    chapter=int(row["chapter"])
    label=row["name"]
    ref_key=tid if tid else "community-unmapped:"+str(chapter)+":"+re.sub("[^a-z0-9]+","_",label.lower()).strip("_")
    early_rows.append({
      "preview_key":ref_key,
      "tech_id":tid if tid else None,
      "race":"elves",
      "chapter":chapter,
      "name_source":label,
      "knowledge_points":int(row["kp"]),
      "activation_requirements":None,
      "parent_ids":None,
      "children_ids_for_display_only":None,
      "unresolved_parent_ids":None,
      "source_status":"COMMUNITY_GUIDE_INCOMPLETE_GRAPH",
      "source_url":"https://elvenarchy.fuzzalab.pt/en/guides/primeiros-capitulos-estrategia",
      "display_ready":True,
      "activation_ready":False,
      "activation_block_reason":"MISSING_ORIGINAL_PARENT_IDS_AND_ACTIVATION_REQUIREMENTS"
    })
assert len(late_rows)==767,(len(late_rows))
assert len(early_rows)==9,(len(early_rows))
all_keys=[n["preview_key"] for n in late_rows+early_rows]
assert len(all_keys)==len(set(all_keys)),"Duplicate preview ID"
assert all(not r["activation_ready"] for r in late_rows+early_rows)
doc={
 "_meta":{
  "schema":"ELVENLAND_RESEARCH_READONLY_PREVIEW_V1",
  "generated_on":"2026-11-20",
  "purpose":"READ ONLY early research UI/preview and later graph preview, NOT active game-cost definitions",
  "source_files":[EARLY_PATH,LATE_PATH],
  "gameplay_activation_forbidden_without_specific_approval":True,
  "do_not_zero_missing_requirements":True,
  "do_not_zero_missing_parents":True,
  "source_race_scope":["elves"],
  "humans_research_status":"NOT_FULLY_RECONSTRUCTED",
  "historical_cost_minimum_rule":"FEST but apply only when multiple comparable per-race and per-resource values are known",
  "source_graph_version_conflict":"Early screenshots differ from modern early guide; no screenshot graph edges imported",
  "unmatched_early_nodes_not_generated":True,
  "original_complete_chapter_I_V_nodes_known":False
 },
 "summary":{
  "late_source_records":len(late_rows),
  "early_individual_reference_records":len(early_rows),
  "total_preview_records":len(late_rows)+len(early_rows),
  "chapter_I_V_expected_community_total":124,
  "chapter_I_V_unmapped_rows_without_original_ids":sum(not x["tech_id"] for x in early_rows),
  "late_records_with_external_parents":sum(bool(x["unresolved_parent_ids"]) for x in late_rows),
  "display_only_records":len(late_rows)+len(early_rows),
  "active_gameplay_records_added":0
 },
 "nodes":early_rows+late_rows
}
path=ROOT/OUT_PATH
path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("PREVIEW_OK",OUT_PATH,"RECORDS",doc["summary"]["total_preview_records"],"CHAPTER_I_V",len(early_rows),"CHAPTER_VI_XXVI",len(late_rows))

#!/usr/bin/env python3
"""Validate historical research reference datasets, never promote to live balance."""
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(rel):return json.loads((ROOT / rel).read_text(encoding="utf8"))

late=load("data/reference/community_idavis_research_ch06_ch26_2026-11-20.json")
early=load("data/reference/community_early_research_ch01_ch05_2026-11-20.json")
active=load("data/definitions/research_nodes.json")
ch=late["chapters"]
ids={}
errors=[]
kpsum=0
for chapter,rows in ch.items():
    for row in rows:
        tid=row["id"]
        if tid in ids:errors.append("duplicate id "+tid)
        ids[tid]=row
        if not tid.startswith("elves_"):errors.append("unexpected race "+tid)
        try:kp=int(row["kp"])
        except Exception:errors.append("bad kp "+tid);continue
        if kp < 0:errors.append("negative kp "+tid)
        kpsum+=kp
        if not isinstance(row.get("requirements"),list):errors.append("missing requirements "+tid)
        else:
            for cost in row["requirements"]:
                if not isinstance(cost,dict) or len(cost)!=1:
                    errors.append("bad requirement object "+tid);continue
                for resource,qty in cost.items():
                    if not isinstance(qty,(int,float)) or qty < 0:errors.append("bad resource amount "+tid+" "+resource)
        if not isinstance(row.get("parentIds"),list):errors.append("missing parentIds "+tid)
        if not isinstance(row.get("childrenIds"),list):errors.append("missing childrenIds "+tid)

external=[]
nonreciprocal=[]
indegree=collections.Counter()
children=collections.defaultdict(list)
for tid,row in ids.items():
    for parent in row.get("parentIds",[]):
        if parent not in ids:
            external.append({"id":tid,"missing_parent":parent})
            continue
        indegree[tid]+=1
        children[parent].append(tid)
        if tid not in ids[parent].get("childrenIds",[]):
            nonreciprocal.append({"id":tid,"parent":parent})
ready=collections.deque(tid for tid in ids if indegree[tid]==0)
visited=0
while ready:
    tid=ready.popleft()
    visited+=1
    for child in children[tid]:
        indegree[child]-=1
        if indegree[child]==0:ready.append(child)
if visited!=len(ids):errors.append("cycle or invalid parent graph")
early_sum=sum(x["kp_sum"] for x in early["chapter_summary"])
early_n=sum(x["tech_count"] for x in early["chapter_summary"])
pics=[
"data/reference/community_ch01_historical_spieletrend_screenshot_2026-11-20.json",
"data/reference/community_ch04_historical_forum_screenshot_2026-11-20.json",
"data/reference/community_historical_gameguide_fr_research_screen_2026-11-20.json",
]
pictured=sum(len(load(p)["nodes"]) for p in pics)
if len(ch)!=21 or len(ids)!=767 or kpsum!=82540:errors.append("late archive regression")
if early_n!=124 or early_sum!=2785:errors.append("early chapter summary regression")
if active.get("definitions")!=[]:errors.append("live definitions changed from intentionally empty list")
report={
"kind":"RESEARCH_REFERENCE_CONSISTENCY_AUDIT",
"date":"2026-11-20",
"validation_success":not errors,
"late_chapters":len(ch),
"late_technology_records":sum(map(len,ch.values())),
"late_unique_ids":len(ids),
"late_kp_sum":kpsum,
"late_graph_topologically_sortable":visited==len(ids),
"late_external_missing_parent_links":external,
"late_parent_without_reciprocal_child_links":nonreciprocal,
"early_chapter_count":len(early["chapter_summary"]),
"early_reported_technology_total":early_n,
"early_reported_kp_sum":early_sum,
"early_individual_selected_community_research":len(early["selected_tech"]),
"historical_visual_observations":pictured,
"current_live_definitions":len(active.get("definitions",[])),
"early_parentids_complete":False,
"early_activation_costs_complete":False,
"whole_tree_approved_for_gameplay":False,
"no_automatic_free_research_when_missing":True,
"source_provenance_policy":"Historic versions separate; user selects minimum comparable cost per race and resource",
"errors":errors,
}
out=ROOT/"docs/research_data_validation_2026-11-20.json"
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print(json.dumps(report,indent=2,ensure_ascii=False))
if errors:raise SystemExit(1)

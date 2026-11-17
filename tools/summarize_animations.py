#!/usr/bin/env python3
"""Summarize exported AnimationClip metadata without inventing playback rules."""
from pathlib import Path
import argparse, csv, json

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True,type=Path)
    p.add_argument('--output',type=Path)
    a=p.parse_args()
    root=a.input.resolve()
    rows=list(csv.DictReader((root/'bundles_index.csv').open(encoding='utf-8')))
    sprites={(r['serialized_file'],r['object_id']):r for r in rows if r['type']=='Sprite'}
    clips=[]
    for r in rows:
        if r['type']!='AnimationClip' or not r['metadata_path']:continue
        record=json.loads((root/r['metadata_path']).read_text(encoding='utf-8'))
        d=record['data']; muscle=d.get('m_MuscleClip',{})
        refs=[]
        for index,ptr in enumerate(d.get('m_ClipBindingConstant',{}).get('pptrCurveMapping',[])):
            sprite=sprites.get((r['serialized_file'],str(ptr['m_PathID']))) if ptr.get('m_FileID')==0 else None
            refs.append({'mapping_index':index,'pointer':ptr,'sprite_name':sprite['name'] if sprite else None,'sprite_path':sprite['output_path'] if sprite else None,'status':'resolved_same_serialized_file' if sprite else 'unresolved_external_or_non_sprite'})
        clips.append({'source':r['source'],'serialized_file':r['serialized_file'],'object_id':r['object_id'],'name':r['name'],'sample_rate':d.get('m_SampleRate'),'wrap_mode':d.get('m_WrapMode'),'start_time':muscle.get('m_StartTime'),'stop_time':muscle.get('m_StopTime'),'loop_time':muscle.get('m_LoopTime'),'sprite_references':refs,'source_metadata_path':r['metadata_path'],'playback_conversion_status':'NOT_CONVERTED','note':'The pointer table is a reference mapping, not a proven frame timeline. Streamed curves remain in the source metadata.'})
    dest=a.output or root/'animation_reference_catalog.json'
    dest.write_text(json.dumps({'schema_version':1,'clips':clips},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'clips':len(clips),'resolved_sprite_references':sum(x['status']=='resolved_same_serialized_file' for c in clips for x in c['sprite_references']),'unresolved_sprite_references':sum(x['status']!='resolved_same_serialized_file' for c in clips for x in c['sprite_references'])}))

if __name__=='__main__':main()

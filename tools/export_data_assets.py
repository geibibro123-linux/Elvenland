#!/usr/bin/env python3
"""Export Unity serialized Data assets, separate from the UnityFS bundle export.

TextAssets require a hash-pinned approval manifest before publication. This
script exports graphical structure, not arbitrary custom MonoBehaviour fields.
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
import csv
import hashlib
import json
import math
import multiprocessing
from pathlib import Path
import re
import sys
import time
import UnityPy
from PIL import Image

ASSET_TYPES = {'Texture2D','Sprite','Font','TextAsset','AnimationClip','AnimatorController','AnimatorOverrideController','SpriteAtlas','AudioClip'}
STRUCTURE_TYPES = {'GameObject','Transform','RectTransform','SpriteRenderer','Animator','CanvasRenderer','Canvas','CanvasGroup','Animation','Material','ParticleSystem','ParticleSystemRenderer'}
FIELDS = ['source','source_sha256','source_content_sha256','serialized_file','unity_version','type','object_id','name','status','output_path','metadata_path','width','height','bytes','sha256','error']
ENV = None
OBJECTS = {}
SOURCE_MAP = {}
ROOT = None
OUT = None
APPROVED = {}
REVIEW = None


def safe(value):
    return re.sub(r'[^A-Za-z0-9_.-]+','_',str(value)).strip('.')[:130] or 'unnamed'


def digest(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def clean(value):
    if isinstance(value,bytes):return {'$binary_base64':base64.b64encode(value).decode('ascii')}
    if isinstance(value,dict):return {str(k):clean(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):return [clean(v) for v in value]
    if isinstance(value,float) and not math.isfinite(value):return {'$nonfinite_float':str(value)}
    return value


def write_json(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(clean(data),ensure_ascii=False,separators=(',',':'),allow_nan=False),encoding='utf-8')


def initialize(input_path,output_path,approved,review):
    global ENV,OBJECTS,SOURCE_MAP,ROOT,OUT,APPROVED,REVIEW
    ROOT=Path(input_path);OUT=Path(output_path)
    APPROVED={(x.get('source_serialized_file',x.get('serialized_file')),str(x['object_id']),x['sha256']):x for x in approved}
    REVIEW=Path(review) if review else None
    # UnityPy normally keeps file handles open. A fork shares those handles'
    # offsets across processes and causes intermittent parse errors when one
    # worker reads a texture referenced by another worker's sprite. Immutable
    # input bytes give each worker a separate reader position after the fork.
    ENV=UnityPy.Environment(path=str(ROOT))
    ENV.load_assets([str(p) for p in sorted(ROOT.rglob('*')) if p.is_file()],lambda p:Path(p).read_bytes())
    by_identity={}
    for key,value in ENV.files.items():
        path=Path(str(key))
        if not path.is_absolute():path=ROOT/path
        parts=[path] if path.is_file() else sorted(path.parent.glob(path.name+'.split*'),key=lambda p:int(p.name.rsplit('.split',1)[1]))
        if parts:
            if not path.is_file() and [int(p.name.rsplit('.split',1)[1]) for p in parts]!=list(range(len(parts))):
                raise ValueError('Non-contiguous Unity split files: '+path.name)
            h=hashlib.sha256()
            entries=[]
            for part in parts:
                raw=part.read_bytes();h.update(raw)
                entries.append({'path':part.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
            by_identity[id(value)]={'source':path.relative_to(ROOT).as_posix(),'sha256':h.hexdigest(),'parts':entries,'split_joined':len(parts)>1 or parts[0]!=path,'external_files':[{'file_id':number,'path':str(external.path)} for number,external in enumerate(getattr(value,'externals',[]),1)]}
    grouped=defaultdict(list)
    for obj in ENV.objects:
        name=str(obj.assets_file.name)
        grouped[name].append(obj)
        source=by_identity.get(id(obj.assets_file))
        SOURCE_MAP[name]=source
    OBJECTS=dict(grouped)


def export_file(serialized_file):
    source=SOURCE_MAP[serialized_file]
    if source is None:
        counts=Counter(obj.type.name for obj in OBJECTS[serialized_file])
        return [],[{'type':'SourceMapping','serialized_file':serialized_file,'error':'Physical source file unresolved'}],dict(counts),{}
    source_rel=source['source'];source_hash=source['sha256']
    subdir=safe(serialized_file)+'_'+source_hash[:8]
    rows=[];errors=[];counts=Counter();status_counts=Counter();structures=[]
    for obj in OBJECTS[serialized_file]:
        typ=obj.type.name;counts[typ]+=1
        if typ not in ASSET_TYPES|STRUCTURE_TYPES:continue
        row=dict.fromkeys(FIELDS,'')
        row.update(source=source_rel,source_sha256=source_hash,serialized_file=serialized_file,unity_version=str(obj.assets_file.unity_version),type=typ,object_id=str(obj.path_id),status='pending')
        try:
            data=obj.read();name=str(getattr(data,'m_Name',''));row['name']=name
            stem=safe(name)+'__'+str(obj.path_id)
            if typ in STRUCTURE_TYPES:
                tree=obj.read_typetree()
                structures.append({'type':typ,'object_id':str(obj.path_id),'name':name,'data':clean(tree)})
                status_counts[typ+':metadata_exported']+=1
                continue
            if typ in {'Texture2D','Sprite'}:
                if typ=='Texture2D' and data.m_Width==0 and data.m_Height==0 and not data.image_data:
                    row['status']='empty_source_texture'
                else:
                    dest=OUT/('textures' if typ=='Texture2D' else 'sprites')/subdir/(stem+'.png')
                    dest.parent.mkdir(parents=True,exist_ok=True)
                    image=data.image;image.save(dest)
                    with Image.open(dest) as verified:
                        verified.load();row.update(width=verified.width,height=verified.height)
                    row.update(status='exported',output_path=dest.relative_to(OUT).as_posix(),bytes=dest.stat().st_size,sha256=digest(dest))
            elif typ=='Font':
                raw=bytes(data.m_FontData)
                if raw:
                    ext='.otf' if raw[:4]==b'OTTO' else '.ttf' if raw[:4] in (b'\x00\x01\x00\x00',b'true',b'typ1') else '.fontbin'
                    dest=OUT/'fonts'/subdir/(stem+ext);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
                    row.update(status='exported',output_path=dest.relative_to(OUT).as_posix(),bytes=len(raw),sha256=digest(dest))
                else:row['status']='no_embedded_font_bytes'
            elif typ=='TextAsset':
                raw=data.m_Script
                if isinstance(raw,str):raw=raw.encode('utf-8','surrogateescape')
                raw_hash=hashlib.sha256(raw).hexdigest();row.update(bytes=len(raw),sha256=raw_hash,source_content_sha256=raw_hash)
                approval=APPROVED.get((serialized_file,str(obj.path_id),raw_hash))
                if approval:
                    if approval.get('source_file_sha256',source_hash)!=source_hash:
                        raise ValueError('Approved TextAsset serialized source hash mismatch')
                    published=raw
                    transforms=approval.get('transformations',[])
                    if transforms:
                        text_data=json.loads(raw.decode('utf-8'))
                        for transformation in transforms:
                            pointer=transformation.get('json_pointer')
                            if transformation.get('operation')!='remove' or pointer not in {'/skeleton/images','/skeleton/audio'}:
                                raise ValueError('Unsupported TextAsset transformation')
                            skeleton=text_data.get('skeleton',{})
                            if isinstance(skeleton,dict):skeleton.pop(pointer.rsplit('/',1)[1],None)
                        published=(json.dumps(text_data,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode('utf-8')
                    published_hash=hashlib.sha256(published).hexdigest()
                    if approval.get('output_sha256',published_hash)!=published_hash:
                        raise ValueError('Approved TextAsset sanitized output hash mismatch')
                    filename=approval.get('output_file',subdir+'_'+stem+'.bytes')
                    if Path(filename).name!=filename or filename in {'.','..'}:
                        raise ValueError('Invalid approved TextAsset output filename')
                    dest=OUT/'text_assets'/filename;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(published)
                    row.update(status='exported_approved_sanitized' if transforms else 'exported_approved',output_path=dest.relative_to(OUT).as_posix(),bytes=len(published),sha256=published_hash)
                else:
                    row['status']='withheld_not_approved'
                    if REVIEW:
                        dest=REVIEW/subdir/(stem+'.bytes');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
                rows.append(row);status_counts[typ+':'+row['status']]+=1
                continue
            if typ!='TextAsset':
                tree=obj.read_typetree()
                if typ=='Font' and 'm_FontData' in tree:
                    tree['m_FontData']={'stored_separately':row['output_path'] or None,'bytes':row['bytes'] or 0,'sha256':row['sha256'] or None}
                dest=OUT/'metadata'/typ/subdir/(stem+'.json')
                write_json(dest,{'source':source_rel,'source_sha256':source_hash,'serialized_file':serialized_file,'unity_version':row['unity_version'],'type':typ,'object_id':str(obj.path_id),'data':tree})
                row['metadata_path']=dest.relative_to(OUT).as_posix()
                if row['status']=='pending':row['status']='metadata_exported'
        except Exception as error:
            row['error']=(type(error).__name__+': '+str(error)).replace(str(ROOT),'<INPUT>')
            row['status']='exported_metadata_failed' if row['output_path'] else 'failed'
            errors.append({k:row[k] for k in ['source','serialized_file','type','object_id','name','error']})
        rows.append(row);status_counts[typ+':'+row['status']]+=1
    if structures:
        dest=OUT/'metadata/structure'/(subdir+'.json')
        write_json(dest,{'source':source_rel,'source_sha256':source_hash,'serialized_file':serialized_file,'objects':structures})
        row=dict.fromkeys(FIELDS,'');row.update(source=source_rel,source_sha256=source_hash,serialized_file=serialized_file,type='StructuralMetadata',object_id='multiple',name='Graphical object structure',status='metadata_exported',metadata_path=dest.relative_to(OUT).as_posix(),bytes=dest.stat().st_size,sha256=digest(dest));rows.append(row)
    return rows,errors,dict(counts),dict(status_counts)


def finalize_catalogs(output_path,rows,summary):
    sprites={(r['serialized_file'],r['object_id']):r for r in rows if r['type']=='Sprite'}
    clips=[]
    for row in rows:
        if row['type']!='AnimationClip' or not row['metadata_path']:continue
        record=json.loads((output_path/row['metadata_path']).read_text(encoding='utf-8'))
        data=record['data'];muscle=data.get('m_MuscleClip',{})
        refs=[]
        for index,pointer in enumerate(data.get('m_ClipBindingConstant',{}).get('pptrCurveMapping',[])):
            sprite=sprites.get((row['serialized_file'],str(pointer['m_PathID']))) if pointer.get('m_FileID')==0 else None
            refs.append({'mapping_index':index,'pointer':pointer,'sprite_name':sprite['name'] if sprite else None,'sprite_path':sprite['output_path'] if sprite else None,'status':'resolved_same_serialized_file' if sprite else 'unresolved_external_or_non_sprite'})
        clips.append({'source':row['source'],'serialized_file':row['serialized_file'],'object_id':row['object_id'],'name':row['name'],'sample_rate':data.get('m_SampleRate'),'wrap_mode':data.get('m_WrapMode'),'start_time':muscle.get('m_StartTime'),'stop_time':muscle.get('m_StopTime'),'loop_time':muscle.get('m_LoopTime'),'sprite_references':refs,'source_metadata_path':row['metadata_path'],'playback_conversion_status':'NOT_CONVERTED','note':'Pointer mapping is not a frame timeline. Compiled curves remain in the source metadata.'})
    animation_summary={'clips':len(clips),'resolved_sprite_references':sum(x['status']=='resolved_same_serialized_file' for clip in clips for x in clip['sprite_references']),'unresolved_sprite_references':sum(x['status']!='resolved_same_serialized_file' for clip in clips for x in clip['sprite_references'])}
    write_json(output_path/'animation_reference_catalog.json',{'schema_version':1,'summary':animation_summary,'clips':clips})
    empty=[{k:r[k] for k in ('source','serialized_file','object_id','name','metadata_path')} for r in rows if r['status']=='empty_source_texture']
    write_json(output_path/'source_empty_textures.json',{'rule':'Zero width, zero height, no inline image bytes. Source metadata is preserved.','objects':empty})
    summary['animation_references']=animation_summary
    write_json(output_path/'data_summary.json',summary)
    # Enumerate only outputs from this run. Private review/staging directories,
    # unrelated files and old exports are deliberately not part of this manifest.
    paths={value for row in rows for key in ('output_path','metadata_path') if (value:=row.get(key))}
    paths.update({'data_index.csv','data_errors.json','data_summary.json','data_source_manifest.json','animation_reference_catalog.json','source_empty_textures.json'})
    files=[{'path':rel,'bytes':(output_path/rel).stat().st_size,'sha256':digest(output_path/rel)} for rel in sorted(paths)]
    write_json(output_path/'SHA256_MANIFEST.json',{'schema_version':1,'root':'assets/unity_data','file_count':len(files),'total_bytes':sum(f['bytes'] for f in files),'scope':'Only this export run; excludes this manifest itself and every private review/staging directory.','files':files})


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--workers',type=int,default=4)
    p.add_argument('--approved-text-manifest',type=Path)
    p.add_argument('--review-text-dir',type=Path)
    args=p.parse_args();start=time.time()
    input_path=args.input.resolve(strict=True);output_path=args.output.resolve()
    if not input_path.is_dir():p.error('--input must contain the Unity assets/bin/Data directory')
    if args.workers<1:p.error('--workers must be positive')
    approved=[]
    if args.approved_text_manifest:
        approval=json.loads(args.approved_text_manifest.read_text(encoding='utf-8'))
        candidates=approval.get('assets',approval.get('approved',[]))
        for row in candidates:
            if row.get('approved',True):approved.append(row)
        output_names=[x.get('output_file') for x in approved if x.get('output_file')]
        if len(output_names)!=len(set(output_names)):p.error('Approved TextAsset output filenames are not unique')
    review=str(args.review_text_dir.resolve()) if args.review_text_dir else None
    initialize(str(input_path),str(output_path),approved,review)
    output_path.mkdir(parents=True,exist_ok=True)
    keys=sorted(OBJECTS);rows=[];errors=[];counts=Counter();statuses=Counter()
    print(json.dumps({'stage':'loaded','serialized_files':len(keys),'objects':sum(map(len,OBJECTS.values()))}),flush=True)
    if args.workers==1:
        results=map(export_file,keys)
        pool=None
    elif sys.platform!='win32':
        pool=ProcessPoolExecutor(max_workers=args.workers,mp_context=multiprocessing.get_context('fork'))
        results=pool.map(export_file,keys,chunksize=8)
    else:
        pool=ProcessPoolExecutor(max_workers=args.workers,initializer=initialize,initargs=(str(input_path),str(output_path),approved,review))
        results=pool.map(export_file,keys,chunksize=8)
    try:
        for number,(rs,es,cs,ss) in enumerate(results,1):
            rows.extend(rs);errors.extend(es);counts.update(cs);statuses.update(ss)
            if number%500==0 or number==len(keys):print(json.dumps({'completed_files':number,'total_files':len(keys),'index_rows':len(rows),'errors':len(errors),'seconds':round(time.time()-start,1)}),flush=True)
    finally:
        if pool:pool.shutdown()
    rows.sort(key=lambda r:(r['source'],r['type'],r['object_id']))
    with (output_path/'data_index.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS);writer.writeheader();writer.writerows(rows)
    write_json(output_path/'data_errors.json',errors)
    write_json(output_path/'data_source_manifest.json',{'hash_rule':'source_sha256 hashes the original serialized file, or split0 + split1 + ... concatenated in numeric order; physical input parts are individually hashed below','sources':[{'serialized_file':name,**SOURCE_MAP[name]} for name in keys if SOURCE_MAP[name] is not None]})
    summary={'UnityPy':UnityPy.__version__,'source_kind':'Unity serialized Data files, not UnityFS bundle counts','source_serialized_files':len(keys),'objects_by_type':dict(counts),'results_by_type_and_status':dict(statuses),'errors':len(errors),'non_exported_types':{k:v for k,v in counts.items() if k not in ASSET_TYPES|STRUCTURE_TYPES},'text_asset_rule':'Only exact source-file, object-id and content-hash approvals are published','custom_monobehaviour_fields_exported':False,'seconds':round(time.time()-start,2)}
    finalize_catalogs(output_path,rows,summary)
    print(json.dumps(summary),flush=True)


if __name__=='__main__':main()

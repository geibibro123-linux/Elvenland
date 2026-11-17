#!/usr/bin/env python3
"""Export verifiable Unity objects. Inputs are never modified."""
from pathlib import Path
import argparse, base64, collections, csv, hashlib, json, math, re, sys, time
from concurrent.futures import ProcessPoolExecutor, as_completed
import UnityPy
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'exported'
META_TYPES = {'Sprite', 'AnimationClip', 'AnimatorController', 'AnimatorOverrideController', 'SpriteAtlas', 'GameObject', 'Transform', 'SpriteRenderer', 'Animator'}
FIELDS = ['source', 'source_sha256', 'serialized_file', 'unity_version', 'type', 'object_id', 'name', 'status', 'output_path', 'metadata_path', 'width', 'height', 'bytes', 'sha256', 'error']

def safe(value):
    s = re.sub(r'[^A-Za-z0-9_.-]+', '_', str(value)).strip('.')
    return s[:130] or 'unnamed'

def clean(v):
    if isinstance(v, bytes): return {'$binary_base64': base64.b64encode(v).decode('ascii')}
    if isinstance(v, dict): return {str(k): clean(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)): return [clean(x) for x in v]
    if isinstance(v, float) and not math.isfinite(v): return {'$nonfinite_float': str(v)}
    return v

def hash_file(p):
    with p.open('rb') as f: return hashlib.file_digest(f, 'sha256').hexdigest()

def process(task):
    source, input_root, output_root, dependencies = task
    path = Path(source)
    output_root = Path(output_root)
    source_rel = path.relative_to(input_root).as_posix()
    source_hash = hash_file(path)
    source_dir = safe(path.name) + '_' + source_hash[:8]
    rows, errors, counts = [], [], collections.Counter()
    try:
        env = UnityPy.load(str(path), *dependencies)
    except Exception as e:
        return [], [{'source': source_rel, 'type': 'File', 'error': str(e).replace(str(input_root), '<INPUT>')}], {}
    for obj in env.objects:
        if dependencies and str(getattr(obj.assets_file.parent, 'name', '')) != path.name:
            continue
        typ = obj.type.name
        counts[typ] += 1
        if typ not in META_TYPES | {'Texture2D', 'TextAsset', 'MonoBehaviour'}: continue
        row = dict.fromkeys(FIELDS, '')
        row.update(source=source_rel, source_sha256=source_hash, type=typ, object_id=str(obj.path_id), serialized_file=str(getattr(obj.assets_file, 'name', '')), unity_version=str(getattr(obj.assets_file, 'unity_version', '')), status='pending')
        try:
            data = obj.read()
            name = str(getattr(data, 'm_Name', ''))
            row['name'] = name
            stem = safe(name) + '__' + str(obj.path_id)
            if typ in {'Sprite', 'Texture2D'}:
                category = 'sprites' if typ == 'Sprite' else 'textures'
                dest = output_root / category / source_dir / (stem + '.png')
                dest.parent.mkdir(parents=True, exist_ok=True)
                img = data.image
                img.save(dest)
                with Image.open(dest) as verify_img:
                    verify_img.load()
                    row.update(width=verify_img.width, height=verify_img.height)
                row.update(output_path=dest.relative_to(output_root).as_posix(), bytes=dest.stat().st_size, sha256=hash_file(dest), status='exported')
            elif typ == 'TextAsset':
                raw = getattr(data, 'm_Script', b'')
                if isinstance(raw, str): raw = raw.encode('utf-8', 'surrogateescape')
                dest = output_root / 'text_assets' / source_dir / (stem + '.bytes')
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(raw)
                row.update(output_path=dest.relative_to(output_root).as_posix(), bytes=len(raw), sha256=hash_file(dest), status='exported')
            if typ in META_TYPES | {'MonoBehaviour'}:
                tree = obj.read_typetree()
                # MonoBehaviour headers alone do not reconstruct custom scripts.
                if typ == 'MonoBehaviour' and set(tree) <= {'m_GameObject', 'm_Enabled', 'm_Script', 'm_Name', 'm_EditorHideFlags', 'm_ObjectHideFlags', 'm_PrefabParentObject', 'm_PrefabInternal'}:
                    row['status'] = 'header_only'
                metadata = {'source': source_rel, 'source_sha256': source_hash, 'serialized_file': row['serialized_file'], 'unity_version': row['unity_version'], 'type': typ, 'object_id': str(obj.path_id), 'data': clean(tree)}
                dest = output_root / 'metadata' / typ / source_dir / (stem + '.json')
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(json.dumps(metadata, ensure_ascii=False, separators=(',', ':'), allow_nan=False), encoding='utf-8')
                row['metadata_path'] = dest.relative_to(output_root).as_posix()
                if row['status'] == 'pending': row['status'] = 'metadata_exported'
            if row['status'] == 'pending': row['status'] = 'parsed'
        except Exception as e:
            row['error'] = f'{type(e).__name__}: {e}'.replace(str(input_root), '<INPUT>')
            if row['output_path']:
                row['status'] = 'exported_metadata_failed'
            else:
                row['status'] = 'failed'
            errors.append({'source': source_rel, 'type': typ, 'object_id': str(obj.path_id), 'name': row['name'], 'error': row['error']})
        rows.append(row)
    return rows, errors, dict(counts)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source', default='bundles')
    p.add_argument('--input', type=Path, help='Directory containing UnityFS bundles; recursively scanned.')
    p.add_argument('--output', type=Path, help='Destination for separate PNGs, metadata and indexes.')
    p.add_argument('--workers', type=int, default=4)
    a=p.parse_args()
    start=time.time()
    source_root=(a.input or ROOT/'inputs'/a.source).resolve()
    output_root=(a.output or OUT).resolve()
    files=[x for x in source_root.rglob('*') if x.is_file() and x.read_bytes()[:7] == b'UnityFS']
    output_root.mkdir(parents=True,exist_ok=True)
    rows, errors, counts=[],[],collections.Counter()
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        futures={pool.submit(process,(str(x),str(source_root),str(output_root),[])):x for x in files}
        for i,f in enumerate(as_completed(futures),1):
            try:
                rs,es,cs=f.result();rows.extend(rs);errors.extend(es);counts.update(cs)
            except Exception as e:
                errors.append({'source':str(futures[f].relative_to(source_root)), 'type':'Worker', 'error':str(e)})
            if i%20==0 or i==len(files):
                print(json.dumps({'completed':i,'total':len(files),'objects':sum(counts.values()),'export_rows':len(rows),'errors':len(errors),'seconds':round(time.time()-start,1)}),flush=True)
    # Some sprites point to textures held by another bundle. Resolve only the
    # explicitly reported CAB dependency instead of loading every bundle at once.
    cab_sources={r['serialized_file'].lower():r['source'] for r in rows}
    retry_sources=collections.defaultdict(set)
    for row in rows:
        match=re.search(r'File (cab-[0-9a-f]+) not found', row['error'], re.I)
        if match and match.group(1).lower() in cab_sources:
            retry_sources[row['source']].add(str(source_root/cab_sources[match.group(1).lower()]))
    for source,deps in retry_sources.items():
        retried, _, _=process((str(source_root/source),str(source_root),str(output_root),sorted(deps)))
        replacements={(r['source'],r['type'],r['object_id']):r for r in retried}
        rows=[replacements.get((r['source'],r['type'],r['object_id']),r) for r in rows]
    errors=[e for e in errors if e['type'] in {'File','Worker'}]+[{'source':r['source'],'type':r['type'],'object_id':r['object_id'],'name':r['name'],'error':r['error']} for r in rows if r['error']]
    rows.sort(key=lambda x:(x['source'],x['type'],x['object_id']))
    with (output_root/f'{a.source}_index.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS);writer.writeheader();writer.writerows(rows)
    (output_root/f'{a.source}_errors.json').write_text(json.dumps(errors,ensure_ascii=False,indent=2),encoding='utf-8')
    summary={'UnityPy':UnityPy.__version__,'source_group':a.source,'source_files':len(files),'objects_by_type':dict(counts),'results_by_type_and_status':dict(collections.Counter(r['type']+':'+r['status'] for r in rows)),'errors':len(errors),'seconds':round(time.time()-start,2),'source_files_sha256':{x.relative_to(source_root).as_posix():hash_file(x) for x in files}}
    (output_root/f'{a.source}_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary | {'source_files_sha256':'see summary file'},ensure_ascii=False),flush=True)

if __name__=='__main__':main()

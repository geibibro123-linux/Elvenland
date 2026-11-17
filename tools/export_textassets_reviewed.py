#!/usr/bin/env python3
"""Re-extract the reviewed Unity TextAssets from verified source files.

Requires the same UnityPy version as the main export environment. No network.
The adjacent approval index contains raw/source/output hashes, allowed
transformations and publication decisions. Unapproved payloads are never written.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import importlib.metadata
import json
import os
import tempfile
import UnityPy


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def local_child(root, value):
    rel = PurePosixPath(value)
    if rel.is_absolute() or not rel.parts or any(p in ('', '.', '..') for p in rel.parts):
        raise ValueError('Unsafe relative path in approval index')
    result = root.joinpath(*rel.parts)
    if not result.resolve().is_relative_to(root.resolve()):
        raise ValueError('Path escapes the selected directory')
    return result


def transform(raw, operations):
    if not operations:
        return raw
    document = json.loads(raw)
    allowed = {'/skeleton/images', '/skeleton/audio'}
    seen = set()
    for operation in operations:
        pointer = operation.get('json_pointer')
        if operation.get('operation') != 'remove' or pointer not in allowed or pointer in seen:
            raise ValueError('Unapproved or duplicate transformation')
        seen.add(pointer)
        key = pointer.rsplit('/', 1)[1]
        if not isinstance(document.get('skeleton'), dict) or key not in document['skeleton']:
            raise ValueError('Expected editor metadata is missing')
        del document['skeleton'][key]
    return (json.dumps(document, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')


def write_atomic(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=path.name + '.', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', required=True, type=Path,
                        help='Extracted Unity assets/bin/Data directory from the verified source APK.')
    parser.add_argument('--output-dir', required=True, type=Path,
                        help='Dedicated destination for reviewed TextAsset payloads.')
    parser.add_argument('--approval-index', type=Path,
                        default=Path(__file__).with_name('textasset_approval_index.json'))
    args = parser.parse_args()
    index_raw = args.approval_index.read_bytes()
    index = json.loads(index_raw)
    assets = index['assets']
    if len(assets) != 44 or index['summary']['text_assets_reviewed'] != 44:
        raise ValueError('This reviewed export requires the exact 44-object approval index')
    output_names = set()
    records = []
    staged = []
    for row in assets:
        source = local_child(args.source_dir, row['source_serialized_file'])
        source_raw = source.read_bytes()
        if sha(source_raw) != row['source_file_sha256']:
            raise ValueError('Unexpected source bytes: ' + row['source_serialized_file'])
        env = UnityPy.load(source_raw)
        matches = [obj for obj in env.objects if obj.type.name == 'TextAsset' and str(obj.path_id) == str(row['object_id'])]
        if len(matches) != 1:
            raise ValueError('TextAsset identity not unique: ' + row['source_serialized_file'])
        data = matches[0].read()
        if data.m_Name != row['name']:
            raise ValueError('Unexpected TextAsset name')
        script = data.m_Script
        raw = script.encode('utf-8', 'surrogateescape') if isinstance(script, str) else bytes(script)
        if sha(raw) != row['sha256'] or len(raw) != row['source_bytes']:
            raise ValueError('Unexpected TextAsset content: ' + row['source_serialized_file'])
        record = {'source_serialized_file': row['source_serialized_file'], 'object_id': row['object_id'],
                  'approved': row['approved'], 'source_sha256_verified': True, 'raw_sha256_verified': True}
        if row['approved']:
            name = row['output_file']
            if name in output_names:
                raise ValueError('Duplicate output path')
            output_names.add(name)
            destination = local_child(args.output_dir, name)
            if destination.exists():
                raise ValueError('Use a new empty output directory; existing asset would be overwritten')
            payload = transform(raw, row['transformations'])
            if sha(payload) != row['output_sha256'] or len(payload) != row['output_bytes']:
                raise ValueError('Reviewed output does not reproduce exactly: ' + name)
            staged.append((destination, payload))
            record.update(output_file=name, output_sha256=sha(payload), output_bytes=len(payload),
                          transformations=row['transformations'])
        records.append(record)
    if len(staged) != index['summary']['approved_assets']:
        raise ValueError('Approved output count mismatch')
    # Nothing is published until every source object and expected output is verified.
    for destination, payload in staged:
        write_atomic(destination, payload)
    report = {
        'schema': 'elvenland-reviewed-textasset-export-v1',
        'approval_index_sha256': sha(index_raw), 'unitypy_version': importlib.metadata.version('UnityPy'),
        'source_objects_verified': len(records), 'published_assets': len(staged),
        'excluded_assets': len(records) - len(staged),
        'all_output_hashes_match_review': True, 'network_requests': False, 'records': records,
    }
    write_atomic(args.output_dir / 'TEXTASSET_EXPORT_REPORT.json',
                 (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    print(json.dumps({key: report[key] for key in ['source_objects_verified', 'published_assets',
                                                'excluded_assets', 'all_output_hashes_match_review']}))


if __name__ == '__main__':
    main()

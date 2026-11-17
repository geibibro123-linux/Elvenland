#!/usr/bin/env python3
"""Build Elvenland's reviewable asset/data handoff from a verified APK.

This builds a ZIP of research inputs and media, never a playable APK.
Only allowlisted static media files are read from the supplied APK.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import struct
import subprocess
import sys
import wave
import zipfile


SEED = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def safe_relative(name: str) -> PurePosixPath:
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or '\\' in name or not path.parts:
        raise ValueError('Unsafe source path')
    return path


def extract_allowlisted(apk: Path, package: Path) -> dict:
    sources = json.loads((SEED / 'provenance/source_media_files.json').read_text())
    additional = json.loads((SEED / 'provenance/additional_static_media_files.json').read_text())
    source_info = json.loads((SEED / 'provenance/SOURCE_INPUTS.json').read_text())
    apk_hash = digest(apk)
    if apk_hash not in source_info['accepted_apk_sha256']:
        raise ValueError('APK hash is not in the verified input allowlist')
    result = {'source_apk_sha256': apk_hash, 'files_verified': 0, 'bytes_verified': 0}
    with zipfile.ZipFile(apk) as archive:
        for item in sources['files'] + additional['files']:
            relative = safe_relative(item['apk_path'])
            payload = archive.read(item['apk_path'])
            if len(payload) != item['bytes'] or hashlib.sha256(payload).hexdigest() != item['sha256']:
                raise ValueError('Source mismatch: ' + item['apk_path'])
            target = package / 'source_assets/apk' / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
            result['files_verified'] += 1
            result['bytes_verified'] += len(payload)
    write_json(package / 'verification/source_verification.json', result)
    return result


def export_android_references(apk: Path, package: Path, apk_hash: str) -> dict:
    """Preserve the supplemental Android PNG references using verified entry maps."""
    catalog = json.loads((SEED / 'catalogs/android_reference_index.json').read_text())
    exported = []
    absent = []
    with zipfile.ZipFile(apk) as archive:
        for item in catalog['files']:
            names = item['verified_apk_entries_by_apk_sha256'].get(apk_hash, [])
            if not names:
                absent.append(item['path'])
                continue
            source_entry = names[0]
            data = archive.read(source_entry)
            if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
                raise ValueError('Android reference mismatch: ' + source_entry)
            target = package / safe_relative(item['output_path'])
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            exported.append({'path': item['output_path'], 'source_apk_entry': source_entry, 'sha256': item['sha256'], 'byte_equivalent_to_original_base': item['byte_equivalent_to_original_base']})
    result = {'role': 'SUPPLEMENTARY_ANDROID_UI_REFERENCE', 'exported_png': len(exported), 'not_available_with_same_bytes_in_this_apk': absent, 'files': exported}
    write_json(package / 'verification/android_reference_export.json', result)
    return result


def export_audio(package: Path) -> dict:
    spec = importlib.util.spec_from_file_location('ima_decoder', SEED / 'tools/fmod_fsb5_ima_to_wav.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    source = package / 'source_assets/apk/assets/bin/Data'
    target = package / 'assets/audio'
    target.mkdir(parents=True, exist_ok=True)
    inventory = json.loads((SEED / 'catalogs/audio_inventory_196.json').read_text())
    # Audio inventory preserves verified clip names. Build a separate current path map.
    rows = []
    for path in sorted(source.glob('*.resource')):
        data = path.read_bytes()
        if data[:4] != b'FSB5':
            continue
        codec = struct.unpack_from('<I', data, 24)[0]
        if codec == 7:
            payload, metadata = module.decode(data)
            output = target / (path.stem + '.wav')
            output.write_bytes(payload)
            with wave.open(str(output), 'rb') as wav:
                if (wav.getnchannels(), wav.getframerate(), wav.getnframes()) != (metadata['channels'], metadata['sample_rate'], metadata['decoded_samples']):
                    raise ValueError('Audio verification failed: ' + path.name)
            rows.append({'source_apk_entry': path.relative_to(package / 'source_assets/apk').as_posix(), 'output_path': output.relative_to(package).as_posix(), 'sha256': digest(output), **metadata})
        elif codec != 15:
            raise ValueError('Unexpected FSB codec: ' + str(codec))
    subprocess.run([sys.executable, str(SEED / 'tools/decode_vorbis_fsb5.py'), '--input', str(source), '--output', str(target), '--audio-metadata', str(SEED / 'catalogs/audio_clip_metadata.json')], check=True)
    vorbis = json.loads((target / 'vorbis_rebuild_manifest.json').read_text())
    result = {'ima_sources_converted': len(rows), 'vorbis_sources_converted': len(vorbis), 'wav_files': len(list(target.glob('*.wav'))), 'ogg_files': len(list(target.glob('*.ogg'))), 'files': rows, 'vorbis': vorbis}
    if result['ima_sources_converted'] != 194 or result['vorbis_sources_converted'] != 2 or result['wav_files'] != 196:
        raise ValueError('Incomplete audio export')
    links = []
    for item in inventory:
        source_file = package / 'source_assets/apk' / safe_relative(item['source'])
        stem = source_file.stem
        wav_file = target / (stem + '.wav')
        ogg_file = target / (stem + '.ogg')
        if digest(source_file) != item['source_sha256']:
            raise ValueError('Audio source inventory mismatch: ' + stem)
        wav_hash = digest(wav_file)
        if item['format'] == 'IMAADPCM' and wav_hash != item['wav_sha256']:
            raise ValueError('IMA PCM does not match the recovered verified WAV: ' + stem)
        links.append({'audio_name': item.get('audio_name'), 'audio_name_status': item['audio_name_status'], 'source_apk_entry': item['source'], 'source_sha256': item['source_sha256'], 'wav_path': wav_file.relative_to(package).as_posix(), 'wav_sha256': wav_hash, 'ogg_path': ogg_file.relative_to(package).as_posix() if ogg_file.exists() else None, 'ogg_sha256': digest(ogg_file) if ogg_file.exists() else None, 'duration_seconds': item['duration_seconds'], 'channels': item['source_channels'], 'sample_rate': item['source_sample_rate'], 'same_wav_bytes_as_previous_export': wav_hash == item.get('wav_sha256')})
    write_json(package / 'catalogs/audio_asset_links.json', {'status': 'VERIFIED_CURRENT_PACKAGE_PATHS', 'sources': len(links), 'items': links})
    write_json(package / 'verification/audio_export.json', result)
    return result


def export_additional_assets(package: Path, reuse_data: Path | None, reuse_localization: Path | None, workers: int) -> dict:
    data_out = package / 'assets/unity_data'
    localization_out = package / 'assets/localization'
    if reuse_data:
        data_source = reuse_data.resolve()
        approved_files = json.loads((data_source / 'SHA256_MANIFEST.json').read_text())
        data_out.mkdir(parents=True)
        for item in approved_files['files']:
            relative = safe_relative(item['path'])
            source = data_source / relative
            if source.is_symlink() or source.stat().st_size != item['bytes'] or digest(source) != item['sha256']:
                raise ValueError('Verified Unity Data export changed: ' + str(relative))
            target = data_out / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        shutil.copy2(data_source / 'SHA256_MANIFEST.json', data_out / 'SHA256_MANIFEST.json')
    else:
        subprocess.run([sys.executable, str(SEED / 'tools/export_data_assets.py'), '--input', str(package / 'source_assets/apk/assets/bin/Data'), '--output', str(data_out), '--workers', str(workers), '--approved-text-manifest', str(SEED / 'tools/textasset_approval_index.json')], check=True)
    if reuse_localization:
        shutil.copytree(reuse_localization.resolve(), localization_out)
    else:
        subprocess.run([sys.executable, str(SEED / 'tools/export_localization.py'), '--input', str(package / 'source_assets/apk/assets/localization'), '--output', str(localization_out)], check=True)

    approved = {row['apk_path']: row for filename in ['source_media_files.json', 'additional_static_media_files.json'] for row in json.loads((SEED / 'provenance' / filename).read_text())['files']}
    sources = json.loads((data_out / 'data_source_manifest.json').read_text())
    for source in sources['sources']:
        for part in source['parts']:
            key = 'assets/bin/Data/' + safe_relative(part['path']).as_posix()
            expected = approved.get(key)
            if expected is None or expected['sha256'] != part['sha256'] or expected['bytes'] != part['bytes']:
                raise ValueError('Unity Data source part is not verified: ' + key)
    known_sources = {row['source']: row['sha256'] for row in sources['sources']}
    with (data_out / 'data_index.csv').open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    groups = {}
    for row in rows:
        if known_sources.get(row['source']) != row['source_sha256']:
            raise ValueError('Unity Data object source hash mismatch')
        for field in ['output_path', 'metadata_path']:
            if row.get(field):
                target = data_out / safe_relative(row[field])
                if not target.is_file():
                    raise ValueError('Missing Unity Data output: ' + row[field])
                if field == 'output_path' and row.get('sha256') and digest(target) != row['sha256']:
                    raise ValueError('Unity Data output hash mismatch: ' + row[field])
                row[field] = 'assets/unity_data/' + row[field]
        groups.setdefault(row['type'], []).append(row)
    chunks = []
    for kind, group in sorted(groups.items()):
        for offset in range(0, len(group), 100):
            name = 'indexes/unity_data_' + kind + '_' + str(offset // 100).zfill(3) + '.json'
            subset = group[offset:offset + 100]
            write_json(package / name, {'collection': 'unity_data', 'type': kind, 'offset': offset, 'total': len(group), 'items': subset})
            chunks.append({'path': name, 'collection': 'unity_data', 'type': kind, 'offset': offset, 'count': len(subset)})

    local_sources = json.loads((localization_out / 'source_manifest.json').read_text())
    for item in local_sources['files']:
        key = item.get('path', item.get('source_path'))
        expected = approved.get(key)
        if expected is None or expected['sha256'] != item['sha256']:
            raise ValueError('Localization source is not verified: ' + str(key))
    local_files = json.loads((localization_out / 'file_manifest.json').read_text())
    for item in local_files['files']:
        output = localization_out / safe_relative(item['path'])
        if output.stat().st_size != item['bytes'] or digest(output) != item['sha256']:
            raise ValueError('Localization output hash mismatch: ' + item['path'])
    shutil.copy2(localization_out / 'localization_index.json', package / 'catalogs/localization_index.json')
    reference = package / 'data/localization'
    reference.mkdir(parents=True, exist_ok=True)
    for locale in ['de_de', 'en_dk']:
        shutil.copy2(localization_out / 'reference_tables' / (locale + '_key_values.json'), reference / (locale + '_key_values.json'))
    shutil.copy2(localization_out / 'de_en_topic_index.json', reference / 'de_en_topic_index.json')
    shutil.copy2(localization_out / 'README_LOCALIZATION.md', package / 'docs/LOCALIZATION.md')
    data_summary = json.loads((data_out / 'data_summary.json').read_text())
    data_errors = json.loads((data_out / 'data_errors.json').read_text())
    expected = json.loads((SEED / 'verification/unity_data_expected.json').read_text())
    if data_summary['results_by_type_and_status'] != expected['results_by_type_and_status'] or data_errors != expected['errors']:
        raise ValueError('Unity Data export differs from the verified expected coverage')
    local_index = json.loads((localization_out / 'localization_index.json').read_text())
    if local_index['locale_count'] != 20 or local_index['entry_count_all_locales'] != 55740:
        raise ValueError('Localization export is incomplete')
    write_json(package / 'verification/unity_data_export.json', data_summary)
    result = {'unity_data': data_summary, 'localization': {'locales': 20, 'keys_per_language': 2787, 'entries_across_locales': 55740}, 'index_chunks': chunks}
    return result


def build_indices(package: Path, additional_chunks: list | None = None) -> dict:
    visual = package / 'assets/visuals'
    with (visual / 'bundles_index.csv').open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    approved_sources = {PurePosixPath(x['apk_path']).name: x['sha256'] for x in json.loads((package / 'provenance/source_media_files.json').read_text())['files']}
    for row in rows:
        if approved_sources.get(PurePosixPath(row['source']).name) != row['source_sha256']:
            raise ValueError('Visual source is outside the verified input: ' + row['source'])
        for field in ['output_path', 'metadata_path']:
            if row.get(field):
                path = visual / safe_relative(row[field])
                if not path.is_file():
                    raise ValueError('Missing visual export: ' + row[field])
                if field == 'output_path' and row.get('sha256') and digest(path) != row['sha256']:
                    raise ValueError('Visual hash mismatch: ' + row[field])
    groups = {}
    for row in rows:
        for key in ['output_path', 'metadata_path']:
            if row.get(key):
                row[key] = 'assets/visuals/' + row[key]
        groups.setdefault(row['type'], []).append(row)
    chunks = []
    for kind, group in sorted(groups.items()):
        for offset in range(0, len(group), 100):
            name = 'indexes/' + kind + '_' + str(offset // 100).zfill(3) + '.json'
            subset = group[offset:offset + 100]
            write_json(package / name, {'type': kind, 'offset': offset, 'total': len(group), 'items': subset})
            chunks.append({'path': name, 'type': kind, 'offset': offset, 'count': len(subset)})
    visuals = json.loads((package / 'data/reference/city_visual_catalog.json').read_text())
    by_bundle = {}
    for row in rows:
        by_bundle.setdefault(PurePosixPath(row['source']).name, []).append(row)
    linked = []
    for entity in visuals['data']:
        variants = []
        for variant in entity['variants']:
            matches = by_bundle.get(variant['bundle_file'], [])
            variants.append({**variant, 'exported_sprite_paths': [r['output_path'] for r in matches if r['type'] == 'Sprite' and r['output_path']], 'texture_paths': [r['output_path'] for r in matches if r['type'] == 'Texture2D' and r['output_path']], 'animation_metadata_paths': [r['metadata_path'] for r in matches if r['type'] == 'AnimationClip' and r['metadata_path']]})
        linked.append({'reference_name': entity['reference_name'], 'alias_reference': entity['alias_reference'], 'variants': variants, 'gameplay_definition_status': 'OPEN'})
    write_json(package / 'data/reference/city_asset_links.json', {'status': 'VERIFIED_SOURCE_BUNDLE_ASSOCIATION', 'warning': 'A bundle association does not establish which sprite/layer is the complete building or its gameplay footprint.', 'data': linked})
    chunks.extend(additional_chunks or [])
    index = {'format_version': 2, 'read_first': ['START_HERE.md', 'STATUS.json', 'MASTER_PROMPT.md', 'data/reference/README_HISTORICAL_DATA.md'], 'data_files': sorted(p.relative_to(package).as_posix() for p in (package / 'data').rglob('*.json')), 'asset_chunks': chunks, 'collections': {'unity_bundles': 'assets/visuals/bundles_index.csv', 'unity_data': 'assets/unity_data/data_index.csv', 'localization': 'catalogs/localization_index.json', 'android_ui_references': 'catalogs/android_reference_index.json'}, 'full_manifest': 'MANIFEST.jsonl', 'source_allowlist': 'provenance/source_media_files.json', 'additional_source_allowlist': 'provenance/additional_static_media_files.json', 'audio_inventory': 'catalogs/audio_asset_links.json', 'historical_audio_inventory': 'catalogs/audio_inventory_196.json'}
    write_json(package / 'INDEX.json', index)
    # No external resources or scripts; this is an optional offline contact index.
    candidates = [r for r in rows if r['type'] == 'Sprite' and r['output_path'] and any(x in r['source'] for x in ['townhall', 'residential', 'workshop', 'barrack'])]
    cards = ''.join('<figure><img loading="lazy" src="' + html.escape(r['output_path'], quote=True) + '"><figcaption>' + html.escape(r['name']) + '</figcaption></figure>' for r in candidates[:120])
    content = '<!doctype html><html lang="de"><meta charset="utf-8"><title>Elvenland Ressourcen</title><style>body{background:#16201b;color:#edf4e7;font:16px system-ui;margin:30px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px}figure{margin:0;padding:12px;background:#25342a;border-radius:8px}img{width:100%;height:160px;object-fit:contain}figcaption{font-size:12px;overflow-wrap:anywhere}a{color:#a5d9a7}</style><h1>Elvenland: extrahierte Ressourcen</h1><p>Vorschau von bis zu 120 Einzelbildern. Ein Sprite kann eine Ebene oder ein Animationsbild sein. Diese Übersicht ist kein Spiel.</p><p><a href="START_HERE.md">Start</a> | <a href="INDEX.json">Gesamter Dateiindex</a> | <a href="MASTER_PROMPT.md">Arbeitsauftrag</a></p><main>' + cards + '</main></html>'
    (package / 'ASSET_PREVIEW.html').write_text(content, encoding='utf-8')
    return {'indexed_objects': sum(chunk['count'] for chunk in chunks), 'unityfs_indexed_objects': len(rows), 'unity_data_indexed_objects': sum(chunk['count'] for chunk in (additional_chunks or [])), 'index_chunks': len(chunks), 'visual_city_references': len(linked)}


def seal_package(package: Path, output: Path) -> dict:
    # Every manifest item points to an existing ordinary file inside the package.
    excluded = {'MANIFEST.jsonl', 'SHA256SUMS.txt', 'verification/package_validation.json'}
    files = [p for p in sorted(package.rglob('*')) if p.is_file() and p.relative_to(package).as_posix() not in excluded]
    manifest = []
    json_count = 0
    for path in files:
        relative = path.relative_to(package).as_posix()
        if any(part in {'source_assets', 'textassets_private', 'textassets_approved'} for part in path.relative_to(package).parts):
            raise ValueError('Unreviewed raw/audit staging files must not enter the handoff')
        if path.is_symlink():
            raise ValueError('Symlink not allowed')
        if path.suffix.lower() in {'.p12', '.pfx', '.jks', '.keystore', '.pem'}:
            raise ValueError('Signing material must not enter the package')
        if path.name == 'reference_start_v4_v5.json' or path.suffix.lower() == '.apk':
            raise ValueError('Raw account reference/APK must not enter this media handoff')
        if path.suffix.lower() == '.json':
            json.loads(path.read_text(encoding='utf-8-sig'))
            json_count += 1
        manifest.append({'path': relative, 'bytes': path.stat().st_size, 'sha256': digest(path)})
    (package / 'MANIFEST.jsonl').write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in manifest), encoding='utf-8')
    (package / 'SHA256SUMS.txt').write_text(''.join(row['sha256'] + '  ' + row['path'] + '\n' for row in manifest), encoding='utf-8')
    validation = {'files_manifested': len(manifest), 'manifested_bytes': sum(r['bytes'] for r in manifest), 'json_files_parsed': json_count, 'manifest_excludes_itself_and_validation': True, 'signing_material_included': False, 'raw_private_startup_included': False, 'apk_included': False, 'gameplay_validated': False, 'android_validated': False}
    write_json(package / 'verification/package_validation.json', validation)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as archive:
        for path in sorted(package.rglob('*')):
            if path.is_file():
                relative = path.relative_to(package).as_posix()
                info = zipfile.ZipInfo('elvenland/' + relative, date_time=(2026, 11, 17, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                with archive.open(info, 'w', force_zip64=path.stat().st_size >= 2**31) as stream, path.open('rb') as source:
                    shutil.copyfileobj(source, stream, 1024 * 1024)
    with zipfile.ZipFile(output) as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError('ZIP CRC error: ' + bad)
        validation['zip_entries'] = len(archive.infolist())
    validation.update(zip_crc_verified=True, zip_bytes=output.stat().st_size, zip_sha256=digest(output))
    write_json(output.with_suffix('.verification.json'), validation)
    output.with_suffix('.sha256').write_text(validation['zip_sha256'] + '  ' + output.name + '\n', encoding='ascii')
    return validation


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apk', type=Path, required=True)
    parser.add_argument('--package-dir', type=Path, required=True)
    parser.add_argument('--zip', type=Path, required=True)
    parser.add_argument('--reuse-visuals', type=Path)
    parser.add_argument('--reuse-data', type=Path)
    parser.add_argument('--reuse-localization', type=Path)
    parser.add_argument('--workers', type=int, default=2)
    args = parser.parse_args()
    package = args.package_dir.resolve()
    output_zip = args.zip.resolve()
    if package == SEED or SEED in package.parents or package in SEED.parents:
        raise ValueError('Package directory must be outside the seed directory')
    if output_zip == package or package in output_zip.parents or SEED in output_zip.parents:
        raise ValueError('Output ZIP must be outside source and package directories')
    if package.exists():
        raise ValueError('Choose a new package directory; existing work is not overwritten')
    shutil.copytree(SEED, package, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git', '.venv', 'venv', 'node_modules', 'dist', 'build', 'assets', 'assets_android_extra', 'source_assets', 'indexes', 'MANIFEST.jsonl', 'SHA256SUMS.txt', 'ASSET_PREVIEW.html', 'KI_START_HERE.md', 'KI_STARTER_MANIFEST.json', '*.zip', '*.apk'))
    source_result = extract_allowlisted(args.apk.resolve(), package)
    visual = package / 'assets/visuals'
    if args.reuse_visuals:
        shutil.copytree(args.reuse_visuals.resolve(), visual)
    else:
        subprocess.run([sys.executable, str(SEED / 'tools/export_assets.py'), '--input', str(package / 'source_assets/apk/assets/android'), '--output', str(visual), '--workers', str(args.workers)], check=True)
    subprocess.run([sys.executable, str(SEED / 'tools/summarize_animations.py'), '--input', str(visual)], check=True)
    summary = json.loads((visual / 'bundles_summary.json').read_text())
    exported = summary['results_by_type_and_status']
    if summary['source_files'] != 317 or exported.get('Sprite:exported') != 3735 or exported.get('Texture2D:exported') != 1591 or exported.get('AnimationClip:metadata_exported') != 82 or exported.get('AnimatorController:metadata_exported') != 57:
        raise ValueError('Visual export is incomplete for the verified source snapshot')
    errors = json.loads((visual / 'bundles_errors.json').read_text())
    expected_empty_fonts = {str(item['object_id']) for item in json.loads((SEED / 'verification/font_texture_gaps.json').read_text())}
    if len(errors) != 4 or {str(item.get('object_id')) for item in errors} != expected_empty_fonts or any(item.get('type') != 'Texture2D' or item.get('name') != 'Font Texture' for item in errors):
        raise ValueError('Unexpected visual extraction gap beyond the four empty font objects')
    audio_result = export_audio(package)
    additional_result = export_additional_assets(package, args.reuse_data, args.reuse_localization, args.workers)
    android_result = export_android_references(args.apk.resolve(), package, source_result['source_apk_sha256'])
    index_result = build_indices(package, additional_result['index_chunks'])
    status = json.loads((package / 'STATUS.json').read_text())
    status['measured_export'] = {'source': source_result, 'visuals': {k: v for k, v in summary.items() if k not in ['source_files_sha256']}, 'unity_data': additional_result['unity_data'], 'localization': additional_result['localization'], 'android_reference_png': {k: v for k, v in android_result.items() if k != 'files'}, 'audio': {k: v for k, v in audio_result.items() if k not in ['files', 'vorbis']}, 'index': index_result}
    status['raw_source_assets_included'] = False
    write_json(package / 'STATUS.json', status)
    # Raw serialized sources can contain excluded editor/SDK information.
    # Keep them only in the private input APK, never in the reviewable handoff.
    # This generated tree was created above; original inputs are untouched.
    shutil.rmtree(package / 'source_assets')
    print(json.dumps(seal_package(package, output_zip), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

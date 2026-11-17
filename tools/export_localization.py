#!/usr/bin/env python3
"""Export manifest-listed Unity localization bundles as readable JSON.

No network access. No source files are changed. All source locales and all
translation variants are retained. Localization strings are not gameplay data.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import sys

import UnityPy


TOPICS = {
    'research': re.compile(r'research|technolog|knowledge points?', re.I),
    'buildings': re.compile(r'building|residence|town.?hall|main hall|workshop|barracks?|road', re.I),
    'production': re.compile(r'production|producing|produce|supplies|collect|storage', re.I),
    'combat': re.compile(r'combat|battle|damage|attack|defen[cs]e|units?', re.I),
}


def sha256(path: Path) -> str:
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def write_json(path: Path, value, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    options = {'separators': (',', ':')} if compact else {'indent': 2}
    path.write_text(json.dumps(value, ensure_ascii=False, allow_nan=False, **options) + '\n', encoding='utf-8')


def json_safe(value):
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    if isinstance(value, bytes):
        return {'encoding': 'hex', 'bytes': value.hex()}
    if isinstance(value, float) and not math.isfinite(value):
        return {'nonfinite_float': str(value)}
    return value


def safe_leaf(value: str) -> str:
    if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]*', value) or value in {'.', '..'}:
        raise ValueError('Unsafe file or locale name: ' + repr(value))
    return value


def relative_prefix(value: str) -> str:
    parsed = PurePosixPath(value)
    if parsed.is_absolute() or '..' in parsed.parts or '\\' in value or ':' in value or not parsed.parts:
        raise ValueError('Source prefix must be a safe relative POSIX path')
    return parsed.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True, help='Directory containing loca_manifest_v7.json and its bundles')
    parser.add_argument('--output', type=Path, required=True, help='New directory for decoded localization JSON')
    parser.add_argument('--source-prefix', default='assets/localization', help='Original APK path prefix used in provenance')
    args = parser.parse_args()
    source = args.input.resolve()
    destination = args.output.resolve()
    prefix = relative_prefix(args.source_prefix)
    if not source.is_dir():
        raise ValueError('Input directory does not exist')
    if destination.exists():
        raise ValueError('Use a new output directory; existing files are not overwritten')
    if destination == source or source in destination.parents:
        raise ValueError('Output must be outside the input directory')

    manifest_path = source / 'loca_manifest_v7.json'
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    bundle_infos = manifest['AssetBundleInfos']
    if not isinstance(bundle_infos, list) or not bundle_infos:
        raise ValueError('Manifest contains no bundle entries')
    names = [safe_leaf(item['FileName']) for item in bundle_infos]
    if len(set(names)) != len(names):
        raise ValueError('Duplicate bundle filenames in manifest')
    actual_bundles = set()
    for candidate in source.iterdir():
        if candidate.is_file():
            with candidate.open('rb') as handle:
                if handle.read(7) == b'UnityFS':
                    actual_bundles.add(candidate.name)
    if actual_bundles != set(names):
        raise ValueError('Manifest and supplied UnityFS bundles differ: ' + repr(sorted(actual_bundles ^ set(names))))

    destination.mkdir(parents=True)
    (destination / 'loca_manifest_v7.json').write_bytes(manifest_bytes)
    source_files = [{'source_path': prefix + '/loca_manifest_v7.json', 'bytes': len(manifest_bytes), 'sha256': sha256(manifest_path)}]
    locales = []
    seen_locales = set()
    reference_tables = []
    all_types = Counter()
    search_index = {'selection': 'Lexical matches against source keys only; not a technology graph or gameplay definition.', 'locales': {}}
    for info in sorted(bundle_infos, key=lambda item: item['FileName']):
        bundle_name = safe_leaf(info['FileName'])
        locale = safe_leaf(PurePosixPath(info['PathInsideBundle']).stem.lower())
        if locale in seen_locales:
            raise ValueError('Duplicate locale would overwrite output: ' + locale)
        seen_locales.add(locale)
        bundle = source / bundle_name
        if bundle.is_symlink():
            raise ValueError('Source symlinks are not accepted')
        bundle_hash = sha256(bundle)
        provenance = {'source_path': prefix + '/' + bundle_name, 'source_sha256': bundle_hash,
                      'source_bytes': bundle.stat().st_size, 'manifest_locale_id': info['Locale'],
                      'manifest_path_inside_bundle': info['PathInsideBundle'], 'locale': locale}
        source_files.append({'source_path': provenance['source_path'], 'bytes': provenance['source_bytes'], 'sha256': bundle_hash})
        env = UnityPy.load(str(bundle))
        localized = []
        metadata_files = []
        text_assets = []
        type_counts = Counter()
        for obj in sorted(env.objects, key=lambda item: (item.type.name, item.path_id)):
            kind = obj.type.name
            type_counts[kind] += 1
            all_types[kind] += 1
            serialized = str(getattr(obj.assets_file, 'name', ''))
            base = {**provenance, 'type': kind, 'object_id': str(obj.path_id),
                    'serialized_file': serialized, 'unity_version': str(getattr(obj.assets_file, 'unity_version', ''))}
            if kind == 'TextAsset':
                data = obj.read()
                raw = data.m_Script
                if isinstance(raw, str):
                    raw = raw.encode('utf-8', 'surrogateescape')
                output = destination / 'text_assets' / locale / (str(obj.path_id) + '.txt')
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(raw)
                text_assets.append({**base, 'name': data.m_Name, 'path': output.relative_to(destination).as_posix(), 'bytes': len(raw), 'sha256': sha256(output)})
            tree = json_safe(obj.read_typetree())
            relative = 'metadata/' + locale + '/' + kind + '__' + str(obj.path_id) + '.json'
            write_json(destination / relative, {**base, 'data': tree}, compact=True)
            metadata_files.append(relative)
            if kind == 'MonoBehaviour' and '_localisationDictionary' in tree:
                dictionary = tree['_localisationDictionary']
                keys, values = dictionary['keys'], dictionary['values']
                if len(keys) != len(values):
                    raise ValueError('Localization keys and values have different lengths: ' + locale)
                entries = [{'index': index, 'key': key, 'value': value} for index, (key, value) in enumerate(zip(keys, values))]
                if any(not isinstance(item['key'], str) for item in entries):
                    raise ValueError('Localization key is not a string: ' + locale)
                localized.append({'unity_locale_name': tree.get('m_Name'), 'entries': entries,
                                  'source_metadata_path': relative, 'object_id': str(obj.path_id),
                                  'duplicate_keys': len(keys) - len(set(keys))})
        if len(localized) != 1:
            raise ValueError('Expected one localization dictionary in ' + locale + ', found ' + str(len(localized)))
        dictionary = localized[0]
        output_path = 'locales/' + locale + '.json'
        write_json(destination / output_path, {'_meta': {**provenance, 'unity_locale_name': dictionary['unity_locale_name'],
                   'source_metadata_path': dictionary['source_metadata_path'], 'object_id': dictionary['object_id'],
                   'interpretation': 'Original localized display strings and all value variants. Not authoritative gameplay rules.'},
                   'entries': dictionary['entries']}, compact=True)
        hits = {topic: [item for item in dictionary['entries'] if pattern.search(item['key'])] for topic, pattern in TOPICS.items()}
        if locale in {'de_de', 'en_dk'}:
            search_index['locales'][locale] = {'source_locale_path': output_path, 'topics': hits}
            if dictionary['duplicate_keys']:
                raise ValueError('Cannot create plain key/value table with duplicate keys: ' + locale)
            plain = {}
            for entry in dictionary['entries']:
                value = entry['value']
                if not isinstance(value, dict) or set(value) != {'Values'} or not isinstance(value['Values'], list):
                    raise ValueError('Unsupported value shape in plain key/value table: ' + locale)
                plain[entry['key']] = value['Values']
            reference_path = 'reference_tables/' + locale + '_key_values.json'
            write_json(destination / reference_path, {'_meta': {**provenance,
                       'source_locale_path': output_path, 'translation_variants_preserved': True,
                       'variant_selection_rule': 'Unknown. Preserve every original variant; do not automatically select the first value.',
                       'gameplay_definitions': False}, 'translations': plain}, compact=True)
            reference_tables.append(reference_path)
        variant_shapes = Counter()
        for entry in dictionary['entries']:
            value = entry['value']
            variant_shapes[str(len(value['Values'])) if isinstance(value, dict) and isinstance(value.get('Values'), list) else 'other'] += 1
        locales.append({**provenance, 'unity_locale_name': dictionary['unity_locale_name'], 'output_path': output_path,
                        'output_bytes': (destination / output_path).stat().st_size, 'output_sha256': sha256(destination / output_path),
                        'entry_count': len(dictionary['entries']), 'duplicate_keys': dictionary['duplicate_keys'],
                        'translation_variant_counts': dict(variant_shapes), 'topic_hit_counts': {topic: len(items) for topic, items in hits.items()},
                        'metadata_paths': metadata_files, 'text_assets': text_assets, 'objects_by_type': dict(type_counts)})
    write_json(destination / 'source_manifest.json', {'format_version': 1, 'files': source_files})
    write_json(destination / 'de_en_topic_index.json', search_index, compact=True)
    result = {'format_version': 1, 'source_prefix': prefix, 'source_manifest': 'source_manifest.json',
              'original_manifest': 'loca_manifest_v7.json', 'original_manifest_sha256': sha256(manifest_path),
              'UnityPy': UnityPy.__version__, 'bundle_count': len(locales), 'locale_count': len(locales),
              'entry_count_all_locales': sum(item['entry_count'] for item in locales), 'objects_by_type': dict(all_types),
              'preferred_reference_locales': ['de_de', 'en_dk'], 'topic_index': 'de_en_topic_index.json',
              'output_paths_relative_to': 'assets/localization/', 'reference_tables': reference_tables,
              'complete_technology_graph_exported': False, 'complete_economy_exported': False,
              'network_requests_made': False, 'locales': locales}
    write_json(destination / 'localization_index.json', result)
    (destination / 'README_LOCALIZATION.md').write_text(
        '# Elvenland: extrahierte Sprachdaten\n\n'
        'Die 20 im Originalmanifest aufgeführten UnityFS-Bundles wurden mit UnityPy gelesen. '
        'Sie enthalten jeweils eine LocalizationDataCollection als MonoBehaviour, keine TextAsset-Objekte. '
        'Alle 20 Sprachfassungen und sämtliche Übersetzungsvarianten bleiben erhalten.\n\n'
        '`localization_index.json` nennt Quellen, Hashes, Ausgaben und Eintragszahlen. '
        'Ausgabepfade sind relativ zu diesem Verzeichnis, im Gesamtpaket `assets/localization/`. '
        '`locales/` enthält lesbare Schlüssel-/Werteinträge; `metadata/` die unverändert interpretierten Typbäume. '
        '`reference_tables/de_de_key_values.json` und `reference_tables/en_dk_key_values.json` '
        'sind kompakte deutsche und englische Referenztabellen. Der Original-Sprachcode `en_dk` wird bewahrt.\n\n'
        'Jede Sprache enthält 2.787 Schlüssel. Neun Schlüssel besitzen mehrere Übersetzungsvarianten; '
        'die Auswahlregel wurde nicht rekonstruiert. Varianten nicht still auf den ersten Text reduzieren. '
        '`de_en_topic_index.json` enthält nur lexikalisch ausgewählte Textbelege zu Forschung, Gebäuden, '
        'Produktion und Kampf. Diese Texte sind keine vollständigen Tabellen für Technologien, '
        'Abhängigkeiten, Preise oder Produktionsrezepte. Platzhalter wie `%s` und `%d` bleiben erhalten.\n\n'
        'Das ursprüngliche Manifest bleibt bytegleich erhalten. Seine CDN-Adresse ist ein Herkunftshinweis; '
        'dieser Export hat sie nicht aufgerufen und der Offline-Neubau benötigt sie nicht.\n',
        encoding='utf-8')
    outputs = []
    for path in sorted(destination.rglob('*')):
        if path.is_file():
            json.loads(path.read_text(encoding='utf-8')) if path.suffix == '.json' else None
            outputs.append({'path': path.relative_to(destination).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha256(path)})
    write_json(destination / 'file_manifest.json', {'format_version': 1, 'excludes_itself': True, 'files': outputs})
    print(json.dumps({key: value for key, value in result.items() if key != 'locales'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(type(error).__name__ + ': ' + str(error), file=sys.stderr)
        raise SystemExit(1)

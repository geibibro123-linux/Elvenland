#!/usr/bin/env python3
"""Extract documented historical reference tables without player identifiers.

This script preserves absent values. It does not create original game rules.
"""
from pathlib import Path
import argparse
import collections
import csv
import hashlib
import io
import json
import re
import zipfile

EXPECTED_REFERENCE_SHA256 = '3c4a3ef6a6bb3da5ff6da32480d6cea05052b908479b6e814b49faab952ec4cb'
REFERENCE_ENTRY = 'assets/offline_lab/reference_start_v4_v5.json'
SOURCE_ARCHIVE = 'Elvenar_Build02_05_Android_UI_Texte_Konfiguration.zip'
CATALOG_ARCHIVE = 'Elvenar_Build02_11_Katalog_und_Technikberichte.zip'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_directory', type=Path)
    parser.add_argument('output_directory', type=Path)
    args = parser.parse_args()
    out = args.output_directory
    out.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.source_directory / SOURCE_ARCHIVE) as archive:
        raw = archive.read(REFERENCE_ENTRY)
    actual = digest(raw)
    if actual != EXPECTED_REFERENCE_SHA256:
        raise SystemExit('Unexpected reference hash. Review this version before extraction.')
    reference = json.loads(raw)
    meta = {
        'evidence_status': 'HISTORICAL_EMBEDDED_REFERENCE',
        'current_server_values_verified': False,
        'approved_elvenland_balance': False,
        'source_archive': SOURCE_ARCHIVE,
        'source_entry': REFERENCE_ENTRY,
        'source_entry_sha256': actual,
        'extracted_on': '2026-11-17',
        'missing_fields_policy': 'Preserve absence. Do not convert absence to false, zero, empty cost, or success.',
    }
    redactions = []
    city_map = json.loads(json.dumps(reference['city_map']))
    for index, entity in enumerate(city_map['entities']):
        if 'id' in entity:
            entity.pop('id')
            redactions.append({'source_path': f'/city_map/entities/{index}/id', 'action': 'remove_instance_identifier'})
    core_keys = ['mapSize', 'resources', 'resources_cap', 'city_culture']
    core = {key: reference[key] for key in core_keys}
    core['city_map'] = city_map
    dump(out / 'historical_initial_state_minimal.json', {
        '_meta': {**meta, 'purpose': 'Minimal reference only. Not a complete or runnable savegame.',
                  'instance_ids_removed': True, 'new_instance_ids_must_be_generated_locally': True},
        'data': core,
    })
    tables = {
        'historical_resource_sets.json': 'resourceSets',
        'historical_item_unlock_observations.json': 'unlocked_items',
        'historical_feature_technology_links.json': 'featureTechnologies',
        'historical_knowledge_point_packages.json': 'knowledgePointPackages',
        'historical_production_boost_steps.json': 'production_boost',
        'historical_premium_coefficients.json': 'premium_prices',
        'historical_army_reference.json': 'army_details',
    }
    for name, key in tables.items():
        dump(out / name, {'_meta': {**meta, 'source_json_pointer': '/' + key}, 'data': reference[key]})

    with zipfile.ZipFile(args.source_directory / CATALOG_ARCHIVE) as archive:
        csv_raw = archive.read('city_entities.csv')
        catalog_rows = list(csv.DictReader(io.StringIO(csv_raw.decode('utf-8-sig'))))
        manifest_raw = archive.read('original_bundle_manifest.json')
        visual_manifest = json.loads(manifest_raw)
    groups = collections.OrderedDict()
    for row in catalog_rows:
        ref = row['referenceName']
        groups.setdefault(ref, []).append(row)
    entities = []
    for source_entry in visual_manifest['CityEntityAssets']:
        ref = source_entry['referenceName']
        rows = groups.get(ref, [])
        entities.append({
            'reference_name': ref,
            'alias_reference': source_entry['alias'],
            'alias_has_no_own_variants': bool(source_entry['alias']) and not source_entry['qualities'],
            'construction_visual_references': sorted({r['constructionId'] for r in rows if r['constructionId']}),
            'variants': [{
                'alias': r['alias'], 'quality': int(r['quality']),
                'animated': r['animated'] == 'True', 'bundle_file': r['fileName'],
                'bundle_size_bytes': int(r['fileSize']), 'path_inside_bundle': r['pathInsideBundle'],
                'optional': r['optional'] == 'True', 'physically_in_apk_reported': r['physically_in_APK'] == 'True',
            } for r in rows],
            'gameplay_definition_status': 'OPEN',
            'missing_gameplay_fields': ['costs', 'build_duration', 'validated_footprint', 'population', 'culture',
                                        'production_recipes', 'research_requirements', 'upgrade_rules'],
        })
    dump(out / 'city_visual_catalog.json', {
        '_meta': {'evidence_status': 'EXTRACTED_VISUAL_CATALOG', 'source_archive': CATALOG_ARCHIVE,
                  'source_entry': 'original_bundle_manifest.json', 'source_entry_sha256': digest(manifest_raw),
                  'variant_source_entry': 'city_entities.csv', 'variant_source_entry_sha256': digest(csv_raw),
                  'extracted_on': '2026-11-17', 'not_a_building_economy_table': True,
                  'dimension_warning': 'Construction asset names may encode a visual size. They do not prove gameplay footprints.'},
        'unique_visual_references': len(entities), 'quality_variants': len(catalog_rows), 'data': entities,
    })

    tech_ids = sorted({r['techId'] for r in reference['featureTechnologies']})
    dump(out / 'research_tree_status.json', {
        '_meta': meta,
        'status': 'OPEN', 'complete_tech_tree_present': False,
        'observed_feature_technology_links': len(reference['featureTechnologies']),
        'observed_unique_technology_ids': tech_ids,
        'known_metadata_field_names_from_checkpoint': {
            'ResearchTechnologyConfigVO': ['id', 'maxSP', 'parentIds', 'requirements'],
            'ResearchTechnologyProgressVO': ['tech_id', 'currentSP', 'gate_unlocked', 'is_paid'],
            'StrategyPointsVO': ['currentSP', 'maxSP', 'producingTime'],
        },
        'metadata_field_name_source': 'Elvenar_Offline_Lab11_Engineering_Checkpoint.zip/implementation/original_research_planner.js',
        'metadata_note': 'Field names are reported by the historical planner. No complete config rows are bundled with that planner.',
        'missing': ['complete_technology_list', 'parent_dependency_edges', 'per_technology_point_costs',
                    'per_technology_resource_costs', 'unlock_effects', 'gate_rules', 'chapter_order'],
        'runtime_recommendation': 'Do not invent a technology graph. Retain observed links as references until original rows or explicit design decisions exist.',
    })
    unlock_counts = {'explicit_true': 0, 'explicit_false': 0, 'field_absent': 0}
    for row in reference['unlocked_items']:
        if 'unlocked' not in row:
            unlock_counts['field_absent'] += 1
        elif row['unlocked'] is True:
            unlock_counts['explicit_true'] += 1
        elif row['unlocked'] is False:
            unlock_counts['explicit_false'] += 1
        else:
            raise ValueError('Unexpected unlock value')
    coverage = {
        'source_reference_fields': len(reference),
        'minimal_city_entity_count': len(city_map['entities']),
        'city_visual_references': len(entities),
        'city_visual_references_with_variants': len(groups),
        'city_visual_aliases_without_own_variants': sum(e['alias_has_no_own_variants'] for e in entities),
        'city_visual_variants': len(catalog_rows),
        'resource_set_count': len(reference['resourceSets']),
        'unique_resource_ids': len({r for row in reference['resourceSets'] for r in row['resourceIds']}),
        'item_unlock_observation_count': len(reference['unlocked_items']),
        'item_unlock_field_presence': unlock_counts,
        'feature_technology_link_count': len(reference['featureTechnologies']),
        'unique_observed_technology_id_count': len(tech_ids),
        'knowledge_point_package_count': len(reference['knowledgePointPackages']),
        'production_boost_step_count': len(reference['production_boost']),
        'premium_coefficient_row_count': len(reference['premium_prices']),
        'premium_coefficient_value_absent_count': sum('premium_price' not in row for row in reference['premium_prices']),
        'full_building_economy_table_found': False,
        'production_recipe_table_found': False,
        'complete_technology_graph_found': False,
        'specific_missing_coordinates': ['/city_map/unlocked_areas/0/y', '/city_map/entities/0/y', '/city_map/entities/1/y'],
        'interpretation_warning': 'Absent serialized fields may have original defaults, but this extraction does not assume or verify them.',
    }
    source_names = [SOURCE_ARCHIVE, CATALOG_ARCHIVE, 'Elvenar_Offline_Lab11_Engineering_Checkpoint.zip',
                    'Elvenar_Build02_AssetInventar.json', 'Elvenar_Build02_04_Unity_Szenen_und_Ressourcen.zip']
    sources = []
    for name in source_names:
        path = args.source_directory / name
        sources.append({'filename': name, 'size_bytes': path.stat().st_size, 'sha256': digest(path.read_bytes())})
    dump(out / 'evidence_and_coverage.json', {'audit_date': '2026-11-17', 'sources': sources,
                                             'reference_sha256_verified': True, 'coverage': coverage,
                                             'new_network_requests_to_game_service': False,
                                             'apk_built': False})
    omitted = sorted(set(reference) - set(core_keys) - {'city_map'} - set(tables.values()))
    dump(out / 'privacy_and_transformations.json', {
        'method': 'Allowlist of required game definitions and minimal historical reference state.',
        'original_reference_published': False, 'raw_reference_kept_private': True,
        'entire_source_sections_omitted': omitted,
        'sensitive_owner_fields_excluded_with_effects_section': True,
        'instance_identifier_redactions': redactions,
        'technical_catalog_ids_preserved': True, 'cost_and_resource_values_modified': False,
        'missing_fields_filled': False, 'unlocked_absence_converted_to_false': False,
        'privacy_scope': 'No account, owner, profile, device, credential, settings or session data is exported.',
    })
    for file in out.glob('*.json'):
        parsed = json.loads(file.read_text())
        # Inspect data payloads, not descriptive metadata that names removed fields.
        payload = parsed.get('data')
        if payload is None:
            continue
        stack = [payload]
        while stack:
            value = stack.pop()
            if isinstance(value, dict):
                for key, child in value.items():
                    if re.search(r'^(?:owner|ownerId|userId|user_id|accountId|account_id|playerId|player_id|sessionId|session_id|deviceId|device_id|email|password|authorization|cookie)$|(?:access|auth|refresh|session)Token$', key, re.I):
                        raise ValueError('Sensitive key in public payload: ' + key)
                    stack.append(child)
            elif isinstance(value, list):
                stack.extend(value)
            elif isinstance(value, str):
                if re.search(r'https?://|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|-----BEGIN .*PRIVATE KEY', value):
                    raise ValueError('Unexpected external identifier in public payload')
    print(json.dumps({'output_directory': str(out), 'coverage': coverage}, ensure_ascii=False))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Create a verified text-only Elvenland handoff ZIP from an audited full package.

This is a packaging allowlist, not an anonymizer. The input must already be
reviewed for public sharing. No source file is modified or executed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import zipfile

ALLOWED_DIRS = {
    'docs', 'data', 'catalogs', 'provenance', 'verification', 'indexes',
    'tools', 'reference_code', 'github',
}
ROOT_SUFFIXES = {'.md', '.txt', '.json'}
TEXT_SUFFIXES = ROOT_SUFFIXES | {
    '.jsonl', '.csv', '.tsv', '.py', '.js', '.ts', '.yml', '.yaml', '.toml',
    '.ini', '.cfg', '.gd', '.godot', '.tscn', '.tres', '.cs', '.sh', '.ps1',
    '.bat', '.sql', '.c', '.h', '.xml', '.html', '.css',
}
GENERATED_NAMES = {'KI_START_HERE.md', 'KI_STARTER_MANIFEST.json'}
SENSITIVE_NAME = re.compile(
    r'(^|[-_.])(private|privat|secret|secrets|credential|credentials|keystore|password|passwd|token)([-_.]|$)',
    re.I,
)
SENSITIVE_CONTENT = re.compile(
    rb'-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----|'
    rb'\bgh[pousr]_[A-Za-z0-9]{20,}\b|\bgithub_pat_[A-Za-z0-9_]{20,}\b'
)
MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_TOTAL_SOURCE_BYTES = 128 * 1024 * 1024
MAX_ZIP_BYTES = 30_000_000
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)

START_HERE = '''# Elvenland: kleines KI-Startpaket

Dieses Archiv enthält die zur Übergabe ausgewählten Texte, Datentabellen,
Kataloge, Teilindizes, Herkunftsnachweise und Werkzeuge des geprüften
Elvenland-Vollpakets. Es ist kein Spiel und keine installierbare APK.

## Zuerst lesen

1. Diese Datei und `KI_STARTER_MANIFEST.json`.
2. `START_HERE.md`, `STATUS.json` und `MASTER_PROMPT.md`.
3. `INDEX.json`, danach nur die für den aktuellen Arbeitsschritt benötigten Daten.

## Medien sind separat

PNG, WAV, OGG, APK, Originalcontainer und große historische ZIP-Dateien sind
nicht in diesem Startpaket enthalten. Für Grafik-, Musik- und Enginearbeit
das vollständige Elvenland-Medienpaket zusätzlich bereitstellen.

`INDEX.json` wurde unverändert aus dem Vollpaket übernommen. Seine Pfade und
Bestandsangaben beschreiben das Vollpaket. Das gilt ebenso für unverändert
übernommene Ursprungsmanifeste und `SHA256SUMS.txt`. Ein dort erwähnter
Medienpfad ist kein Nachweis, dass die Mediendatei in diesem kleinen Archiv
vorliegt. Welche Dateien dieses Startpaket tatsächlich enthält, steht
ausschließlich in `KI_STARTER_MANIFEST.json`.

Eine KI soll fehlende Medien als separat erforderlich melden, nicht durch
erfundene Bilder, Werte oder eine behauptete erfolgreiche Prüfung ersetzen.
Die Tabellen behalten ihre ursprünglichen Statusangaben und fachlichen Grenzen.

## Zugriff und Integrität

Alle enthaltenen Dateien liegen einzeln unter `elvenland/` und sind UTF-8-Text.
Das Startermanifest nennt für jede Nutzdatei Pfad, Bytezahl und SHA-256. Es
enthält sich selbst nicht. Das ZIP wurde vollständig mit CRC-Prüfung gelesen.

Eine ZIP kann nur genutzt werden, wenn der jeweilige Chat Datei- und
Entpackwerkzeuge besitzt. Öffentliches Lesen per URL setzt zusätzlich ein
öffentlich erreichbares Hosting voraus. Dieses Archiv ändert keine
GitHub-Berechtigung und enthält keine Zugangstokens.
'''


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def selected(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    if path.is_symlink() or any(
        (part.startswith('.') and not (i == len(rel.parts) - 1 and part == '.gitignore'))
        or part == '__pycache__'
        for i, part in enumerate(rel.parts)
    ):
        return False
    if any(SENSITIVE_NAME.search(part) for part in rel.parts):
        return False
    if len(rel.parts) == 1:
        return (path.suffix.lower() in ROOT_SUFFIXES or path.name == '.gitignore') and path.name not in GENERATED_NAMES
    return rel.parts[0] in ALLOWED_DIRS and (path.suffix.lower() in TEXT_SUFFIXES or path.name == '.gitignore')


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package-dir', required=True, type=Path)
    parser.add_argument('--zip', required=True, type=Path, dest='zip_path')
    parser.add_argument('--prompt-output', type=Path, help='Default: MASTER_PROMPT.txt next to ZIP.')
    args = parser.parse_args()
    root = args.package_dir.resolve(strict=True)
    target = args.zip_path.resolve()
    prompt_target = (args.prompt_output or target.with_name('MASTER_PROMPT.txt')).resolve()
    if not root.is_dir():
        parser.error('--package-dir must be a directory')
    if target == prompt_target:
        parser.error('ZIP and standalone prompt need different output paths.')
    if target.is_relative_to(root) or prompt_target.is_relative_to(root):
        parser.error('Write ZIP and standalone prompt outside the source package.')
    for required in ('INDEX.json', 'MASTER_PROMPT.md', 'START_HERE.md', 'STATUS.json'):
        if not (root / required).is_file():
            parser.error(f'Missing required full-package file: {required}')

    entries: dict[str, bytes] = {}
    omitted = {'outside_allowlist': 0, 'binary_or_non_utf8': 0, 'oversized_text': 0}
    total = 0
    for path in sorted(root.rglob('*')):
        if not path.is_file():
            continue
        if not selected(path, root):
            omitted['outside_allowlist'] += 1
            continue
        if path.stat().st_size > MAX_FILE_BYTES:
            omitted['oversized_text'] += 1
            continue
        data = path.read_bytes()
        try:
            data.decode('utf-8')
        except UnicodeDecodeError:
            omitted['binary_or_non_utf8'] += 1
            continue
        if b'\x00' in data:
            omitted['binary_or_non_utf8'] += 1
            continue
        if SENSITIVE_CONTENT.search(data):
            raise ValueError(f'Possible credential material detected; no ZIP published: {path.relative_to(root)}')
        total += len(data)
        if total > MAX_TOTAL_SOURCE_BYTES:
            raise ValueError('Selected text exceeds the 128 MiB source budget; narrow the audited input.')
        entries[path.relative_to(root).as_posix()] = data
    for required in ('INDEX.json', 'MASTER_PROMPT.md', 'START_HERE.md', 'STATUS.json'):
        if required not in entries:
            raise ValueError(f'Required file rejected by text/safety limits: {required}')
    entries['KI_START_HERE.md'] = START_HERE.encode('utf-8')
    manifest = {
        'schema_version': 1,
        'package_type': 'AI_STARTER_TEXT_ONLY',
        'archive_root': 'elvenland/',
        'media_included': False,
        'full_package_index': 'INDEX.json',
        'full_package_index_sha256': sha256(entries['INDEX.json']),
        'index_and_original_manifests_describe_full_package': True,
        'manifest_excludes_itself': True,
        'omitted_counts': omitted,
        'files': [{'path': name, 'bytes': len(data), 'sha256': sha256(data)} for name, data in sorted(entries.items())],
    }
    entries['KI_STARTER_MANIFEST.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.' + target.name + '.', suffix='.zip', dir=target.parent)
    os.close(fd)
    try:
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, data in sorted(entries.items()):
                info = zipfile.ZipInfo('elvenland/' + name, ZIP_TIMESTAMP)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, data, compresslevel=9)
        if os.path.getsize(temporary) >= MAX_ZIP_BYTES:
            raise ValueError('Starter ZIP is not below 30 MB; no output was published.')
        with zipfile.ZipFile(temporary) as archive:
            corrupt = archive.testzip()
            if corrupt:
                raise ValueError(f'ZIP CRC verification failed: {corrupt}')
            if len(archive.infolist()) != len(entries):
                raise ValueError('ZIP entry count mismatch')
        atomic_write(prompt_target, entries['MASTER_PROMPT.md'])
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    print(json.dumps({
        'zip': str(target), 'zip_bytes': target.stat().st_size,
        'zip_sha256': sha256(target.read_bytes()), 'zip_crc_verified': True,
        'files': len(entries), 'uncompressed_bytes': sum(map(len, entries.values())),
        'standalone_prompt': str(prompt_target), 'omitted_counts': omitted,
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Import one pinned text-only starter archive without overwriting user files.

All parts, archive entries, destinations, and conflicts are checked before any
repository file is written. Existing core documentation is always preserved.
This script never builds, imports, or claims the complete media archive.
"""
from pathlib import Path, PurePosixPath
from zipfile import ZipFile
import argparse
import hashlib
import io
import json
import os
import stat
import subprocess
import tempfile

EXPECTED_ARCHIVE_SHA256 = "3aea47b37907ea7bf168139f6d10957deffdca933afe8870325b17524898169b"
EXPECTED_ARCHIVE_BYTES = 4686083
EXPECTED_ARCHIVE_FILES = 270
EXPECTED_PART_COUNT = 39
EXPECTED_BASELINE_COMMIT = "95483ee1ebe3ee346704ceafc25c6450e81b48bc"
MAX_EXPANDED_BYTES = 30 * 1024 * 1024
MAX_ENTRY_BYTES = 6 * 1024 * 1024
ARCHIVE_NAME = "Elvenland_KI_Startpaket_v1.zip"
PRESERVED_CORE = {
    "AGENTS.md", "MASTER_PROMPT.md", "README.md", "START_HERE.md", "STATUS.json",
    "THIRD_PARTY_NOTICE.md", "llms.txt", "docs/AI_HANDOFF.md",
    "docs/ARCHITECTURE.md", "docs/GITHUB_PUBLICATION.md", "docs/PACKAGE_COVERAGE.md",
    "docs/ROADMAP.md", "docs/SOFTWARE_AND_ENGINE.md",
}
SKIP_ARCHIVE_ONLY = {
    "SHA256SUMS.txt", "KI_STARTER_MANIFEST.json", "KI_START_HERE.md",
    "verification/package_validation.json",
}


def fail(message):
    raise SystemExit(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git_blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def safe_relative(value):
    if not isinstance(value, str) or not value or "\\" in value or "\0" in value:
        fail("Invalid path in the pinned transport")
    path = PurePosixPath(value)
    if path.is_absolute() or str(path) != value or any(p in {".", "..", ".git", ".github"} for p in path.parts):
        fail("Unsafe or non-canonical path in the pinned transport: " + value)
    return path


def check_destination(repo, relative):
    path = safe_relative(relative)
    target = repo.joinpath(*path.parts)
    if target.is_symlink() or any(p.is_symlink() for p in target.parents if p != repo.parent):
        fail("Symlink destination refused: " + relative)
    if not target.resolve().is_relative_to(repo):
        fail("Destination escapes repository: " + relative)
    for parent in target.parents:
        if parent == repo:
            break
        if parent.exists() and not parent.is_dir():
            fail("Parent is not a directory: " + relative)
    if target.exists() and not target.is_file():
        fail("Destination is not a regular file: " + relative)
    return target


def save_new_file(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    # Refuse a race with another writer instead of replacing any existing file.
    with path.open("xb") as handle:
        handle.write(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, required=True,
                        help="A new or empty directory outside the repository")
    parser.add_argument("--apply", action="store_true",
                        help="Write checked absent files; default is validation only")
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = args.output_dir.resolve()
    if output == repo or output.is_relative_to(repo):
        fail("Output directory must be outside the Git working tree")
    if output.exists() and any(output.iterdir()):
        fail("Output directory must be empty")
    git_root = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "--show-toplevel"], text=True).strip()
    if Path(git_root).resolve() != repo:
        fail("--repo must point to the Git repository root")
    dirty = subprocess.check_output(["git", "-C", str(repo), "status", "--porcelain", "--untracked-files=all"], text=True)
    if dirty:
        fail("Import requires a clean checkout; existing work is untouched")
    manifest_path = repo / "handoff/starter_transport_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if (manifest.get("source_archive_sha256") != EXPECTED_ARCHIVE_SHA256
            or manifest.get("source_archive_bytes") != EXPECTED_ARCHIVE_BYTES
            or manifest.get("baseline_commit") != EXPECTED_BASELINE_COMMIT
            or manifest.get("media_included") is not False
            or manifest.get("archive_root") != "elvenland/"):
        fail("Transport does not match the pinned starter package")
    preserved = manifest["preserve_existing_files"]
    if set(preserved) != PRESERVED_CORE:
        fail("Unexpected set of preserved baseline files")
    if set(manifest["skip_archive_only_files"]) != SKIP_ARCHIVE_ONLY:
        fail("Unexpected archive-only exclusion list")
    parts = manifest["parts"]
    if len(parts) != EXPECTED_PART_COUNT:
        fail("Incomplete transport part list")
    archive_parts = []
    for index, item in enumerate(parts, 1):
        if item["path"] != f"handoff/starter_parts/{index:03d}.bin":
            fail("Unexpected transport part name or order")
        data = check_destination(repo, item["path"]).read_bytes()
        if len(data) > 122880 or len(data) != item["bytes"] or sha256(data) != item["sha256"] or git_blob_sha(data) != item["git_blob_sha"]:
            fail("Transport part checksum mismatch: " + item["path"])
        archive_parts.append(data)
    archive_bytes = b"".join(archive_parts)
    if len(archive_bytes) != EXPECTED_ARCHIVE_BYTES or sha256(archive_bytes) != EXPECTED_ARCHIVE_SHA256:
        fail("Reassembled starter ZIP checksum mismatch")
    entry_rows = manifest["archive_entries"]
    expected = {safe_relative(row["path"]).as_posix(): row for row in entry_rows}
    if len(expected) != EXPECTED_ARCHIVE_FILES or len(entry_rows) != EXPECTED_ARCHIVE_FILES:
        fail("Unexpected or duplicate manifest paths")
    decoded = {}
    seen = set()
    total_bytes = 0
    with ZipFile(io.BytesIO(archive_bytes)) as archive:
        if len(archive.infolist()) != EXPECTED_ARCHIVE_FILES:
            fail("Unexpected ZIP entry count")
        for entry in archive.infolist():
            if not entry.filename.startswith("elvenland/"):
                fail("Unexpected archive root")
            relative = safe_relative(entry.filename[len("elvenland/"):]).as_posix()
            if relative.casefold() in seen or relative not in expected:
                fail("Duplicate or unlisted ZIP path: " + relative)
            seen.add(relative.casefold())
            if entry.is_dir() or stat.S_IFMT(entry.external_attr >> 16) not in {0, stat.S_IFREG}:
                fail("Non-regular ZIP entry refused: " + relative)
            if entry.flag_bits & 1 or entry.file_size > MAX_ENTRY_BYTES:
                fail("Encrypted or oversized ZIP entry refused")
            total_bytes += entry.file_size
            if total_bytes > MAX_EXPANDED_BYTES:
                fail("Expanded ZIP size exceeds the fixed limit")
            data = archive.read(entry)
            row = expected[relative]
            if len(data) != row["bytes"] or sha256(data) != row["sha256"]:
                fail("ZIP entry checksum mismatch: " + relative)
            data.decode("utf-8", errors="strict")
            decoded[relative] = data
    if set(decoded) != set(expected) or not set(preserved).issubset(decoded):
        fail("Archive membership differs from the explicit manifest")
    unchanged_core, changed_core = [], []
    for relative, old_blob in preserved.items():
        target = check_destination(repo, relative)
        if not target.exists():
            fail("Preserved core file is missing: " + relative)
        (unchanged_core if git_blob_sha(target.read_bytes()) == old_blob else changed_core).append(relative)
    candidates = {p: b for p, b in decoded.items() if p not in preserved and p not in SKIP_ARCHIVE_ONLY}
    if len(candidates) != manifest["import_file_count"]:
        fail("Import file count mismatch")
    absent, already_present = [], []
    for relative, data in candidates.items():
        target = check_destination(repo, relative)
        if target.exists():
            if target.read_bytes() != data:
                fail("Existing changed destination refused before any write: " + relative)
            already_present.append(relative)
        else:
            absent.append(relative)
    receipt_path = "handoff/starter_import_receipt.json"
    receipt = {
        "schema_version": 1, "source_archive": ARCHIVE_NAME,
        "source_archive_sha256": EXPECTED_ARCHIVE_SHA256,
        "source_archive_bytes": EXPECTED_ARCHIVE_BYTES,
        "package_type": "AI_STARTER_TEXT_ONLY", "media_included": False,
        "full_media_archive_included": False, "playable_game_included": False,
        "imported_content_file_count": len(candidates),
        "preserved_core_file_count": len(preserved),
        "preserved_core_paths": sorted(preserved),
        "original_archive_only_files_not_imported": sorted(SKIP_ARCHIVE_ONLY),
        "imported_content_paths": sorted(candidates),
    }
    receipt_bytes = (json.dumps(receipt, indent=2, ensure_ascii=False) + "\n").encode()
    receipt_target = check_destination(repo, receipt_path)
    if receipt_target.exists() and receipt_target.read_bytes() != receipt_bytes:
        fail("Existing import receipt differs; refusing to replace it")
    output.mkdir(parents=True, exist_ok=True)
    save_new_file(output / ARCHIVE_NAME, archive_bytes)
    save_new_file(output / (ARCHIVE_NAME + ".sha256"), (EXPECTED_ARCHIVE_SHA256 + "  " + ARCHIVE_NAME + "\n").encode())
    staged = absent + ([] if receipt_target.exists() else [receipt_path])
    if args.apply:
        for relative in absent:
            save_new_file(check_destination(repo, relative), candidates[relative])
        if not receipt_target.exists():
            save_new_file(receipt_target, receipt_bytes)
    save_new_file(output / "git_paths.nul", b"".join(p.encode() + b"\0" for p in staged))
    print(json.dumps({"validated": True, "applied": args.apply,
                      "new_content_files": len(absent),
                      "already_present_content_files": len(already_present),
                      "preserved_core_files": len(preserved),
                      "preserved_core_with_user_changes": sorted(changed_core),
                      "archive_sha256": EXPECTED_ARCHIVE_SHA256,
                      "archive_path": str(output / ARCHIVE_NAME),
                      "full_media_archive_included": False}))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Recover Vorbis samples from an FSB5 directory or ZIP without re-encoding packets.

Requires fsb5==1.0, libogg, libvorbis and ffmpeg.
Optional --vgmstream selects the separately installed vgmstream CLI for WAV output.
The Ogg final granule is aligned to the declared FSB5 sample count, removing
decoder padding only. The encoded Vorbis packets are not changed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import struct
import subprocess
import tempfile
import wave
import zipfile
from pathlib import Path
import fsb5


def ogg_crc(data: bytes | bytearray) -> int:
    value = 0
    for octet in data:
        value ^= octet << 24
        for _ in range(8):
            value = ((value << 1) ^ 0x04C11DB7) & 0xFFFFFFFF if value & 0x80000000 else (value << 1) & 0xFFFFFFFF
    return value


def normalize_last_granule(data: bytes, sample_count: int) -> bytes:
    buf = bytearray(data)
    offset = 0
    last = None
    while offset < len(buf):
        if buf[offset:offset + 4] != b"OggS" or offset + 27 > len(buf):
            raise ValueError("Invalid Ogg page boundary")
        segments = buf[offset + 26]
        size = 27 + segments + sum(buf[offset + 27:offset + 27 + segments])
        if offset + size > len(buf):
            raise ValueError("Truncated Ogg page")
        last = (offset, size)
        offset += size
    if last is None or not buf[last[0] + 5] & 4:
        raise ValueError("No final Ogg page")
    offset, size = last
    struct.pack_into("<Q", buf, offset + 6, sample_count)
    buf[offset + 22:offset + 26] = b"\0" * 4
    struct.pack_into("<I", buf, offset + 22, ogg_crc(buf[offset:offset + size]))
    return bytes(buf)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def input_members(source: Path):
    if source.is_dir():
        for path in sorted(source.rglob("*")):
            if path.is_file() and not path.is_symlink():
                with path.open("rb") as handle:
                    prefix = handle.read(4)
                    if prefix == b"FSB5":
                        yield path.relative_to(source).as_posix(), prefix + handle.read()
    elif zipfile.is_zipfile(source):
        with zipfile.ZipFile(source) as archive:
            for name in sorted(archive.namelist()):
                if not name.endswith("/"):
                    data = archive.read(name)
                    if data.startswith(b"FSB5"):
                        yield name, data
    else:
        raise ValueError("Input must be a directory of FSB5 resources or a ZIP")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path, nargs="?", help="Legacy positional input")
    parser.add_argument("output_dir", type=Path, nargs="?", help="Legacy positional output")
    parser.add_argument("--input", type=Path, dest="input_path", help="FSB5 resource directory or ZIP")
    parser.add_argument("--output", type=Path, dest="output_path", help="Output directory")
    parser.add_argument("--audio-metadata", type=Path, help="Optional extracted Unity AudioClip metadata JSON")
    parser.add_argument("--vgmstream", type=Path)
    args = parser.parse_args()
    source_path = args.input_path or args.source_zip
    output_path = args.output_path or args.output_dir
    if source_path is None or output_path is None:
        parser.error("Provide --input SOURCE --output DESTINATION")
    if args.input_path and args.source_zip or args.output_path and args.output_dir:
        parser.error("Use either named arguments or legacy positional arguments")
    output_path.mkdir(parents=True, exist_ok=True)
    audio_metadata = {}
    if args.audio_metadata:
        for item in json.loads(args.audio_metadata.read_text(encoding="utf-8")):
            resource = item["data"]["m_Resource"]["m_Source"]
            audio_metadata[Path(resource).name] = item
    records = []
    encountered = 0
    output_sources = {}
    duplicate_sources_skipped = 0
    with tempfile.TemporaryDirectory() as tmp:
        for name, source in input_members(source_path):
            encountered += 1
            bank = fsb5.FSB5(source)
            if bank.header.mode.name != "VORBIS":
                continue
            if len(bank.samples) != 1:
                raise ValueError("This verified path expects one sample per source resource")
            sample = bank.samples[0]
            stem = Path(name).stem
            if stem in output_sources:
                if output_sources[stem] != sha256(source):
                    raise ValueError(f"Conflicting input files would overwrite {stem}")
                duplicate_sources_skipped += 1
                continue
            output_sources[stem] = sha256(source)
            ogg = output_path / (stem + ".ogg")
            wav = output_path / (stem + ".wav")
            ogg.write_bytes(normalize_last_granule(bank.rebuild_sample(sample), sample.samples))
            if args.vgmstream:
                fsb = Path(tmp) / (stem + ".fsb")
                fsb.write_bytes(source)
                command = [str(args.vgmstream.resolve()), "-i", "-o", str(wav), str(fsb)]
            else:
                command = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(ogg), "-c:a", "pcm_s16le", str(wav)]
            subprocess.run(command, check=True, capture_output=True)
            with wave.open(str(wav), "rb") as decoded:
                actual = (decoded.getnchannels(), decoded.getframerate(), decoded.getnframes())
            expected = (sample.channels, sample.frequency, sample.samples)
            if actual != expected:
                raise ValueError(f"Decoded WAV metadata mismatch for {name}: {actual} != {expected}")
            record = {"source_member": name, "source_sha256": sha256(source), "channels": sample.channels,
                      "sample_rate": sample.frequency, "sample_frames": sample.samples,
                      "duration_seconds": sample.samples / sample.frequency,
                      "ogg": ogg.name, "ogg_sha256": sha256(ogg.read_bytes()),
                      "wav": wav.name, "wav_sha256": sha256(wav.read_bytes())}
            metadata = audio_metadata.get(Path(name).name)
            if metadata:
                record.update(audio_name=metadata["data"]["m_Name"], audio_name_status="VERIFIED_UNITY_AUDIOCLIP",
                              unity_source_serialized_file=metadata["source_serialized_file"], unity_object_id=metadata["object_id"])
            records.append(record)
    (output_path / "vorbis_rebuild_manifest.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"fsb5_sources_found": encountered, "converted_vorbis_sources": len(records),
                      "other_codecs_skipped": encountered - len(records) - duplicate_sources_skipped,
                      "duplicate_sources_skipped": duplicate_sources_skipped, "output_dir": str(output_path)}))


if __name__ == "__main__":
    main()

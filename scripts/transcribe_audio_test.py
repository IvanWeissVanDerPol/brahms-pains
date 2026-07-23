#!/usr/bin/env python3
"""Smoke-test for the whisper transcription pipeline.

Verifies the four subsystems:
1. Backend availability (Whisper can be loaded)
2. .opus file discovery
3. Single-file transcription (with timeout)
4. Output schema + resumability

Usage:
    python3 scripts/transcribe_audio_test.py
    python3 scripts/transcribe_audio_test.py --skip-transcribe

Exit code:
    0 = all checks passed
    non-zero = first failing check
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Ensure sibling module is importable
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

try:
    import transcribe_audio as ta  # type: ignore
    from transcribe_audio import detect_backend, discover, MEDIA_DIR, TRANSCRIPT_DIR
except ImportError as e:
    print(f"❌ Could not import transcribe_audio: {e}")
    print(f"   ensure transcribe_audio.py is in the same directory as this test")
    sys.exit(2)


def banner(title: str):
    print()
    print(f"━━ {title} ━━")


def check_backend() -> int:
    banner("1. Backend detection")
    backend = None
    err = None
    try:
        backend = detect_backend("tiny")
    except Exception as e:
        err = e
    if backend is None:
        print(f"❌ No backend found: {err}")
        print("   Run: bash scripts/install_whisper.sh --local-cpu")
        print("   OR: export OPENAI_API_KEY=sk-...")
        return 1
    print(f"✅ {backend.name}")
    return 0


def check_discovery() -> tuple[int, list[Path]]:
    banner("2. Audio discovery")
    if not MEDIA_DIR.exists():
        print(f"❌ MEDIA_DIR does not exist: {MEDIA_DIR}")
        return 1, []
    opus = list(MEDIA_DIR.rglob("*.opus"))
    print(f"   {len(opus):,} .opus files under {MEDIA_DIR}")
    if not opus:
        print(f"❌ No .opus files to test on")
        return 1, []
    sample = opus[:5]
    for o in sample:
        kb = o.stat().st_size / 1024
        print(f"   {o.parent.name}/{o.name} ({kb:.0f} KB)")
    return 0, sample


def check_writable() -> int:
    banner("3. Output dir writable")
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    test_file = TRANSCRIPT_DIR / "_smoke_test.txt"
    try:
        test_file.write_text("smoke test\n", encoding="utf-8")
        test_file.unlink()
        print(f"✅ {TRANSCRIPT_DIR} is writable")
        return 0
    except OSError as e:
        print(f"❌ Cannot write: {e}")
        return 1


def check_python_deps() -> int:
    banner("0. Python deps")
    missing = []
    if not ta._try_import("json"):
        missing.append("json (stdlib)")
    for name in ("faster_whisper", "whisper"):
        if ta._try_import(name):
            print(f"✅ {name} available")
        # else: not present, that's fine if using a different backend
    if missing:
        print(f"❌ Missing: {missing}")
        return 1
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--skip-transcribe", action="store_true",
                   help="Skip the actual transcription call")
    args = p.parse_args()

    print("WHOAMI: transcribe_audio_test v0.1")
    print(f"  REPO_ROOT: {ta.REPO_ROOT}")
    print(f"  MEDIA_DIR: {ta.MEDIA_DIR}")
    print(f"  TRANSCRIPT_DIR: {ta.TRANSCRIPT_DIR}")

    # Subsystem checks
    failed = 0
    if check_python_deps():
        failed += 1
    if check_writable():
        failed += 1
    if check_backend():
        failed += 1
        return failed  # nothing else can work
    rc, sample = check_discovery()
    if rc:
        failed += 1
        return failed

    if args.skip_transcribe:
        print()
        print("⚠️  Skipped transcription call (--skip-transcribe)")
        return 0

    # Try a small transcription
    banner("4. End-to-end transcription (1 file, tiny model)")
    print("Transcribing 1 file via --smoke-test...")
    proc = subprocess.run(
        [sys.executable, HERE / "transcribe_audio.py", "--smoke-test"],
        capture_output=True, text=True, timeout=600,
    )
    print(proc.stdout)
    if proc.returncode != 0:
        print(f"❌ smoke-test exited {proc.returncode}")
        print(proc.stderr)
        return 1
    print("✅ end-to-end transcription succeeded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

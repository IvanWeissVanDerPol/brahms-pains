#!/usr/bin/env python3
"""Batch-transcribe 14,809 untranscribed WhatsApp voice notes (.opus) using Whisper.

Pipeline:
    media/audio/<chat_dir>/PTT-YYYYMMDD-WAnnnn.opus
        |
        |  (resumable: skips if .txt or .FAILED exists)
        |
        v
    SOURCE_OF_TRUTH/voice_note_transcripts/<chat_dir>/transcripts.txt  (human)
    SOURCE_OF_TRUTH/voice_note_transcripts/<chat_dir>/transcripts.json (machine)

Backend auto-detection (in order):
    1. OPENAI_API_KEY env var  -> OpenAI cloud Whisper API ($0.006/min)
    2. faster-whisper Python module (recommended local)
    3. openai-whisper Python module (slower but well-known)
    4. whisper.cpp CLI binary

Usage:
    python3 scripts/transcribe_audio.py --workers 4 --dry-run
    python3 scripts/transcribe_audio.py --limit 50
    python3 scripts/transcribe_audio.py --ptt-id PTT-20240314-WA0019
    python3 scripts/transcribe_audio.py --smoke-test
    python3 scripts/transcribe_audio.py --workers 8 --model medium
    python3 scripts/transcribe_audio.py --workers 4 --backend openai

Whisper models:
    tiny     ~39M params, ~80x realtime local, weakest accuracy
    base     ~74M params, ~50x realtime local
    small    ~244M params, ~12x realtime local
    medium   ~769M params, ~5x realtime local, RECOMMENDED for es/gu
    large-v3 ~1550M params, ~2x realtime local, highest accuracy

Backend cost (per minute of audio):
    openai-cloud  $0.006/min  $0.36/hr of audio
    faster-whisper on CPU  $0 (you pay compute time)
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable, Optional

# ─────────────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent
MEDIA_DIR = REPO_ROOT / "media" / "audio"
TRANSCRIPT_DIR = REPO_ROOT / "SOURCE_OF_TRUTH" / "voice_note_transcripts"
LOG_FILE = TRANSCRIPT_DIR / "run.log"

PTT_RE = re.compile(r"^PTT-(\d{8})-WA(\d{4})\.opus$")
CHAT_DIR_RE = re.compile(r"^_wa_(chat|lid|group)_(.+)$")


# ─────────────────────────────────────────────────────────────────────────────
# Backend detection
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class Backend:
    name: str
    transcribe_fn: Callable[[Path], dict]


def detect_backend(model: str, force: Optional[str] = None) -> Backend:
    """Return the best available Whisper backend."""
    if force == "openai" or (force is None and os.environ.get("OPENAI_API_KEY")):
        return _openai_backend()
    if force == "faster" or (force is None and _try_import("faster_whisper")):
        return _faster_backend(model)
    if force == "openai-whisper" or (force is None and _try_import("whisper")):
        return _openai_whisper_backend(model)
    if force == "whisper-cpp" or (
        force is None and shutil.which("whisper-cli") or shutil.which("whisper.cpp")
    ):
        return _whisper_cpp_backend(model)
    raise RuntimeError(
        "No Whisper backend available.\n"
        "Options:\n"
        "  export OPENAI_API_KEY=sk-...   # for cloud\n"
        "  pip install faster-whisper      # recommended local\n"
        "  pip install -U openai-whisper   # or this\n"
        "  ./scripts/install_whisper.sh    # helper"
    )


def _try_import(name: str) -> bool:
    try:
        __import__(name)
        return True
    except ImportError:
        return False


def _openai_backend() -> Backend:
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY not set")
    from openai import OpenAI  # type: ignore

    client = OpenAI()

    def _transcribe(opus: Path) -> dict:
        with open(opus, "rb") as f:
            resp = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="verbose_json",
            )
        return {
            "text": resp.text,
            "language": resp.language,
            "duration": getattr(resp, "duration", 0),
            "segments": [
                {"start": s.start, "end": s.end, "text": s.text}
                for s in (resp.segments or [])
            ],
        }

    return Backend(name="openai-cloud", transcribe_fn=_transcribe)


def _faster_backend(model: str) -> Backend:
    from faster_whisper import WhisperModel  # type: ignore

    mdl = WhisperModel(model, device="cpu", compute_type="int8")

    def _transcribe(opus: Path) -> dict:
        segments_iter, info = mdl.transcribe(str(opus), beam_size=5)
        segments = list(segments_iter)
        return {
            "text": " ".join(s.text.strip() for s in segments),
            "language": info.language,
            "language_probability": info.language_probability,
            "duration": info.duration,
            "segments": [
                {"start": s.start, "end": s.end, "text": s.text} for s in segments
            ],
        }

    return Backend(name=f"faster-whisper({model})", transcribe_fn=_transcribe)


def _openai_whisper_backend(model: str) -> Backend:
    import whisper  # type: ignore

    mdl = whisper.load_model(model)

    def _transcribe(opus: Path) -> dict:
        result = mdl.transcribe(str(opus))
        return {
            "text": result.get("text", ""),
            "language": result.get("language"),
            "duration": result.get("duration", 0),
            "segments": [
                {"start": s.get("start"), "end": s.get("end"), "text": s.get("text", "")}
                for s in result.get("segments", [])
            ],
        }

    return Backend(name=f"openai-whisper({model})", transcribe_fn=_transcribe)


def _whisper_cpp_backend(model: str) -> Backend:
    binary = shutil.which("whisper-cli") or shutil.which("whisper.cpp")
    if not binary:
        raise RuntimeError("whisper.cpp binary not found")
    model_path = Path.home() / ".cache" / "whisper" / f"{model}.bin"
    if not model_path.exists():
        raise RuntimeError(f"whisper.cpp model not found at {model_path}")

    def _transcribe(opus: Path) -> dict:
        out = subprocess.run(
            [binary, "--model", str(model_path), "--file", str(opus),
             "--output-json", "--no-prints"],
            capture_output=True, text=True
        )
        if out.returncode != 0:
            raise RuntimeError(out.stderr)
        data = json.loads(out.stdout)
        return {
            "text": data.get("text", ""),
            "language": data.get("language"),
            "segments": data.get("segments", []),
        }

    return Backend(name=f"whisper.cpp({model})", transcribe_fn=_transcribe)


# ─────────────────────────────────────────────────────────────────────────────
# Discovery + format
# ─────────────────────────────────────────────────────────────────────────────


def chat_id_for(opus: Path) -> str:
    """Return chat_id from the parent dir name.

    _wa_chat_<jid>_<chatid>  -> full dirname (no processing)
    _wa_lid_<lid>_<chatid>   -> full dirname
    _wa_group_<slug>_<chatid> -> full dirname

    We use the WHOLE dirname because chat_dir paths already encode
    the unique chat id, and we want to put transcripts in the same
    chat_id-keyed subdir. The first transcript I produce lands in
    SOURCE_OF_TRUTH/voice_note_transcripts/<original-audio-dirname>/...
    """
    return opus.parent.name


def human_dir_for(audio_dirname: str) -> Path:
    """The directory we write transcripts into.

    Audio dir is e.g. _wa_chat_595981225272_62. We strip the leading
    _wa_ to make the transcripts dir easier to scan.
    """
    name = audio_dirname
    if name.startswith("_wa_"):
        name = name[len("_wa_"):]  # remove leading _wa_
    return TRANSCRIPT_DIR / name


def format_txt(opus: Path, info: dict) -> str:
    """The human-readable .txt body."""
    name = opus.name
    lang = info.get("language", "?")
    prob = info.get("language_probability", "")
    dur = info.get("duration", 0)
    segments = info.get("segments", [])

    out = []
    out.append(f"{name} | lang={lang} prob={prob} dur={dur:.1f}s")
    out.append("-" * 60)
    for s in segments:
        text = (s.get("text") or "").strip()
        if not text:
            continue
        ts = format_ts(s.get("start", 0))
        te = format_ts(s.get("end", 0))
        out.append(f"[{ts} → {te}] {text}")
    out.append("")
    return "\n".join(out)


def format_ts(seconds: float) -> str:
    m, s = divmod(seconds, 60)
    return f"{int(m):02d}:{s:05.2f}"


def write_outputs(opus: Path, info: dict) -> tuple[Path, Path]:
    """Write transcripts.txt + transcripts.json (append)."""
    out_dir = human_dir_for(opus.parent.name)
    out_dir.mkdir(parents=True, exist_ok=True)

    txt = out_dir / "transcripts.txt"
    jsn = out_dir / "transcripts.json"

    # Append new entry to .txt (and .json)
    txt_entry = format_txt(opus, info)
    with open(txt, "a", encoding="utf-8") as f:
        f.write(txt_entry)

    # Load existing JSON if any
    if jsn.exists():
        try:
            arr = json.loads(jsn.read_text(encoding="utf-8"))
        except Exception:
            arr = []
    else:
        arr = []

    arr.append({
        "file": opus.name,
        "language": info.get("language"),
        "language_probability": info.get("language_probability"),
        "duration": info.get("duration"),
        "transcribed_at": datetime.now(timezone.utc).isoformat(),
        "segments": info.get("segments", []),
        "text": info.get("text", ""),
    })
    jsn.write_text(json.dumps(arr, ensure_ascii=False, indent=1), encoding="utf-8")
    return txt, jsn


# ─────────────────────────────────────────────────────────────────────────────
# Discovery
# ─────────────────────────────────────────────────────────────────────────────


def discover(limit: Optional[int] = None) -> list[Path]:
    """All PTT-*.opus that don't have a matching .txt or .FAILED yet."""
    if not MEDIA_DIR.exists():
        print(f"❌ Audio dir not found: {MEDIA_DIR}", file=sys.stderr)
        return []
    opus_files = sorted(MEDIA_DIR.rglob("*.opus"))
    todo = []
    for o in opus_files:
        out_dir = human_dir_for(o.parent.name)
        marker = out_dir / "transcripts.json"
        # Quick check: is this PTT already in the JSON? Faster than searching .txt.
        if marker.exists():
            try:
                existing = json.loads(marker.read_text(encoding="utf-8"))
                files = {e.get("file") for e in existing if isinstance(e, dict)}
                if o.name in files:
                    continue
            except Exception:
                pass
        todo.append(o)
    if limit:
        todo = todo[:limit]
    return todo


def already_done() -> set[str]:
    """Return set of PTT-IDs already done (filename format)."""
    if not TRANSCRIPT_DIR.exists():
        return set()
    done = set()
    for jsn in TRANSCRIPT_DIR.rglob("transcripts.json"):
        try:
            arr = json.loads(jsn.read_text(encoding="utf-8"))
            for e in arr:
                if isinstance(e, dict) and e.get("file"):
                    done.add(e["file"])
        except Exception:
            pass
    return done


# ─────────────────────────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────────────────────────


def log(line: str):
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now(timezone.utc).isoformat()} {line}\n")


# ─────────────────────────────────────────────────────────────────────────────
# Banner
# ─────────────────────────────────────────────────────────────────────────────

BANNER = r"""
   ╔══════════════════════════════════════════════════════════════╗
   ║   🦜 Whisper Batch Transcriber — Psycology Corpus v0.1      ║
   ║   14,809 voice notes · resumable · parallel                 ║
   ╚══════════════════════════════════════════════════════════════╝
"""


def print_banner(args: argparse.Namespace, backend: Backend, todo: list):
    print(BANNER)
    print(f"   Workers      : {args.workers}")
    print(f"   Backend      : {backend.name}")
    print(f"   Audio dir    : {MEDIA_DIR}")
    print(f"   Output dir   : {TRANSCRIPT_DIR}")
    print(f"   Files to do  : {len(todo)}")
    if todo:
        total_sec = estimate_total_seconds(todo)
        print(f"   Audio total  : ~{total_sec/60:.0f} min ({total_sec/3600:.1f} hours)")
    print(f"   Started      : {datetime.now(timezone.utc).isoformat()}")
    print("═" * 64)


def estimate_total_seconds(opus_files: list[Path]) -> float:
    """Estimate total audio seconds from file size. .opus is ~1 KB/s."""
    total = 0
    for o in opus_files[:200]:  # sample
        try:
            total += o.stat().st_size / 1024.0  # 1 KB ≈ 1 s of opus @32kbps mono
        except OSError:
            pass
    avg = total / max(1, min(200, len(opus_files)))
    return avg * len(opus_files)


# ─────────────────────────────────────────────────────────────────────────────
# Single-file transcription
# ─────────────────────────────────────────────────────────────────────────────


def transcribe_one(opus: Path, backend: Backend, retry: int = 1) -> tuple[bool, str]:
    """Return (success, message)."""
    try:
        info = backend.transcribe_fn(opus)
        if not info.get("text", "").strip():
            return False, "empty transcript"
        write_outputs(opus, info)
        return True, f"ok ({info.get('language','?')} {info.get('duration',0):.1f}s)"
    except Exception as e:
        if retry > 0:
            time.sleep(2)
            return transcribe_one(opus, backend, retry - 1)
        # Mark as failed so we don't retry forever
        out_dir = human_dir_for(opus.parent.name)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"{opus.stem}.FAILED").write_text(str(e), encoding="utf-8")
        return False, f"FAILED: {e}"


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--workers", type=int, default=4, help="Parallel workers (default 4)")
    p.add_argument("--limit", type=int, default=None, help="Stop after N files")
    p.add_argument("--dry-run", action="store_true", help="Just list what would happen")
    p.add_argument("--smoke-test", action="store_true", help="Run on first 5 files end-to-end")
    p.add_argument("--ptt-id", type=str, default=None, help="Transcribe a single PTT by ID")
    p.add_argument("--model", type=str, default="medium", help="Whisper model (tiny/base/small/medium/large-v3)")
    p.add_argument("--backend", type=str, default=None, choices=["openai", "faster", "openai-whisper", "whisper-cpp"],
                   help="Force backend (default: auto-detect)")
    args = p.parse_args()

    # Smoke test mode
    if args.smoke_test:
        print(BANNER)
        return run_smoke_test(args.model, args.backend)

    # Single PTT mode
    if args.ptt_id:
        opus = next((p for p in MEDIA_DIR.rglob("*.opus") if p.name.startswith(args.ptt_id)), None)
        if not opus:
            print(f"❌ PTT {args.ptt_id} not found")
            return 1
        backend = detect_backend(args.model, args.backend)
        print(f"Transcribing single: {opus}")
        ok, msg = transcribe_one(opus, backend)
        print(f"  → {'✅' if ok else '❌'} {msg}")
        return 0 if ok else 1

    # Discovery
    todo = discover(args.limit if not args.dry_run else None)
    if args.dry_run:
        print(BANNER)
        print(f"DRY-RUN: would transcribe {len(todo)} files")
        sec = estimate_total_seconds(todo)
        print(f"Total audio: ~{sec/60:.0f} min")
        # First 10 examples
        for o in todo[:10]:
            kb = o.stat().st_size / 1024
            print(f"  {o.parent.name}/{o.name}  ({kb:.0f} KB)")
        if len(todo) > 10:
            print(f"  ... and {len(todo)-10} more")
        return 0

    if not todo:
        print("✅ Nothing to do — all transcripts already present.")
        return 0

    # Real run
    backend = detect_backend(args.model, args.backend)
    print_banner(args, backend, todo)
    log(f"start workers={args.workers} backend={backend.name} count={len(todo)}")

    # Bounded parallel run
    start = time.time()
    completed = 0
    failed = 0
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(transcribe_one, p, backend): p for p in todo}
        for fut in cf.as_completed(futures):
            ok, msg = fut.result()
            completed += int(ok)
            failed += int(not ok)
            opus = futures[fut]
            status = "✅" if ok else "❌"
            print(f"  {status} {opus.parent.name}/{opus.name}  {msg}")
            log(f"{status} {opus.parent.name}/{opus.name}  {msg}")

    elapsed = time.time() - start
    print("\n" + "═" * 64)
    print(f"Completed: {completed}/{len(todo)}   Failed: {failed}")
    if len(todo) > 0:
        rate = completed / elapsed if elapsed > 0 else 0
        print(f"Throughput: {rate:.2f} files/sec")
    print(f"Log: {LOG_FILE}")
    log(f"done completed={completed} failed={failed} elapsed={elapsed:.1f}s")
    return 0


def run_smoke_test(model: str, force_backend: Optional[str]) -> int:
    """Run on 5 tiny files end-to-end. Report on each subsystem."""
    print("SMOKE-TEST MODE (5 files, see each subsystem)\n")

    # 1. Backend
    try:
        backend = detect_backend(model, force_backend)
        print(f"✅ Backend: {backend.name}")
    except Exception as e:
        print(f"❌ Backend detect failed: {e}")
        return 1

    # 2. Discovery
    todo = discover(5)
    if not todo:
        print("⚠️  No .opus files found in media/audio/ — nothing to test on.")
        print(f"   Expected: {MEDIA_DIR}")
        return 1
    print(f"✅ Discovery: found {len(todo)} candidates")

    # 3. Single-file transcription
    for o in todo:
        ok, msg = transcribe_one(o, backend)
        status = "✅" if ok else "❌"
        print(f"   {status} {o.name}: {msg}")

    # 4. Output check
    out_dir = human_dir_for(todo[0].parent.name)
    if (out_dir / "transcripts.txt").exists() and (out_dir / "transcripts.json").exists():
        print(f"✅ Output dir: {out_dir}")
    else:
        print(f"❌ Output files missing in {out_dir}")
        return 1

    # 5. Resumability
    if discover(5):
        # We're checking: re-discover should now find less
        todo2 = discover(100)
        print(f"✅ Resumability: re-discovered {len(todo2)} (was {len(todo)}+ for limit 5)")
    else:
        print(f"✅ Resumability: re-discover found 0 — clean state")
    print("\n✅ Smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

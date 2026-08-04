#!/usr/bin/env python3
"""Aggregate documents__*.m4a.json Whisper outputs into transcripts.json."""

import json
import re
from pathlib import Path

BULK = Path("SOURCE_OF_TRUTH/voice_note_transcripts/_documents_ivan_voice")
OUT = BULK / "transcripts.json"

DATE_RE = re.compile(r"documents__(\d{2})-(\d{2})-(\d{4})_(\d{2})\.(\d{2})\.m4a\.json$")

entries = []
skipped = 0
for jf in sorted(BULK.glob("documents__*.m4a.json")):
    try:
        data = json.loads(jf.read_text(encoding="utf-8"))
    except Exception:
        skipped += 1
        continue
    segments = data.get("segments") or []
    text = " ".join((s.get("text") or "").strip() for s in segments).strip()
    if not text:
        continue
    m = DATE_RE.match(jf.name)
    date = f"{m.group(3)}-{m.group(1)}-{m.group(2)}" if m else None
    entries.append(
        {
            "file": data.get("file", jf.stem),
            "date": date,
            "text": text,
            "duration": data.get("duration"),
            "language": data.get("language"),
        }
    )

OUT.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {len(entries)} entries to {OUT} (skipped {skipped})")

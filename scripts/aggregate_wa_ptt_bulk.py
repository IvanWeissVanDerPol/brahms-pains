#!/usr/bin/env python3
"""Aggregate _wa_ptt_bulk/PTT-*.json into a single transcripts.json the extractor expects."""

import json
import re
from pathlib import Path

BULK = Path("SOURCE_OF_TRUTH/voice_note_transcripts/_wa_ptt_bulk")
OUT = BULK / "transcripts.json"

DATE_RE = re.compile(r"PTT-(\d{4})(\d{2})(\d{2})-WA\d+\.opus$")

entries = []
skipped = 0
for jf in sorted(BULK.glob("PTT-*.json")):
    if jf.name == "transcripts.json":
        continue
    try:
        data = json.loads(jf.read_text(encoding="utf-8"))
    except Exception:
        skipped += 1
        continue
    fname = data.get("file", jf.stem + ".opus")
    text = (data.get("text") or "").strip()
    if not text:
        continue
    m = DATE_RE.match(fname)
    date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else None
    entries.append(
        {
            "file": fname,
            "date": date,
            "text": text,
            "duration": data.get("duration"),
            "language": data.get("language"),
        }
    )

OUT.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {len(entries)} entries to {OUT} (skipped {skipped} unreadable)")

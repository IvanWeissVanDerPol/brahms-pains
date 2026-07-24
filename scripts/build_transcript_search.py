#!/usr/bin/env python3
"""Build a transcript search tool — search across all transcribed voice notes.

For each query, find matching transcripts with:
- Matched word(s) + context (full transcript text)
- Chat (contact) name
- Language
- Date (extracted from filename like PTT-20231223-WA0064.opus)
- Audio duration

Output: transcript_search.html — single-page app with lazy-loaded JSON
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS"
TRANSCRIPT_BASE = REPO / "SOURCE_OF_TRUTH" / "voice_note_transcripts"

# Extract date from PTT-YYYYMMDD-WAnnnn.opus filename
DATE_RE = re.compile(r'PTT-(\d{4})(\d{2})(\d{2})-')


def extract_date(filename: str) -> str | None:
    m = DATE_RE.search(filename)
    if not m: return None
    try:
        y, mo, d = m.groups()
        return f"{y}-{mo}-{d}"
    except Exception:
        return None


def main():
    print("Loading transcripts...")
    transcripts = []
    file_count = 0
    for f in TRANSCRIPT_BASE.rglob("transcripts.json"):
        file_count += 1
        try:
            arr = json.loads(f.read_text())
            if not isinstance(arr, list): continue
            chat_dir = f.parent.name
            for entry in arr:
                entry["_chat"] = chat_dir
            transcripts.extend(arr)
        except Exception:
            pass

    valid = [t for t in transcripts if t.get("text")]
    print(f"Loaded {len(valid)} transcripts from {file_count} files")

    # Match chat → JID/name
    vcard_data = json.loads((ANALYSIS / "viewer_full_data.json").read_text())
    jid_to_name = {c["jid"]: c["name"] for c in vcard_data["vcard_contacts"]}

    chat_to_info = {}
    for t in valid:
        chat = t.get("_chat", "?")
        if chat not in chat_to_info:
            m = re.search(r'(?:chat|_wa_chat)_(\d{8,15})_', chat)
            jid = m.group(1) if m else "?"
            chat_to_info[chat] = {
                "jid": jid,
                "name": jid_to_name.get(jid, "?"),
            }

    # Build search corpus
    print("Building search corpus...")
    search_entries = []
    for i, t in enumerate(valid):
        text = t.get("text", "").strip()
        if not text: continue
        date = extract_date(t.get("file", ""))
        chat = t.get("_chat", "?")
        info = chat_to_info.get(chat, {"jid": "?", "name": "?"})
        search_entries.append({
            "id": i,
            "file": t.get("file", "?"),
            "text": text,
            "text_low": text.lower(),
            "language": t.get("language", "?"),
            "duration": round(t.get("duration") or 0, 2),
            "date": date,
            "chat": chat,
            "name": info["name"],
            "jid": info["jid"],
        })

    print(f"Search corpus: {len(search_entries)} entries")

    # Save search index
    out = {
        "generated_at": datetime.now().isoformat(),
        "total_transcripts": len(search_entries),
        "total_files": file_count,
        "entries": search_entries,
    }
    out_path = ANALYSIS / "transcript_search_index.json"
    # Strip text_low from output (only kept in memory for search)
    save_entries = []
    for e in search_entries:
        save_entries.append({k: v for k, v in e.items() if k != "text_low"})
    out["entries"] = save_entries
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"Wrote {out_path.relative_to(REPO)} ({out_path.stat().st_size:,} bytes)")

    # Also save a leaner version with text_low for fast client-side search
    lean = {
        "generated_at": out["generated_at"],
        "total_transcripts": len(search_entries),
        "entries": [
            {
                "id": e["id"],
                "file": e["file"],
                "text": e["text"],
                "text_low": e["text_low"],
                "language": e["language"],
                "duration": e["duration"],
                "date": e["date"],
                "name": e["name"],
                "chat": e["chat"],
                "jid": e["jid"],
            } for e in search_entries
        ],
    }
    lean_path = ANALYSIS / "transcript_search_lean.json"
    lean_path.write_text(json.dumps(lean, ensure_ascii=False, indent=1))
    print(f"Wrote {lean_path.relative_to(REPO)} ({lean_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()

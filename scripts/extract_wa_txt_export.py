#!/usr/bin/env python3
"""Extract WhatsApp official "Export chat" .txt export into a payload
schema-compatible with extract_wa_messages.py (SQLite extractor).

Input:  a "WhatsApp Chat with <name>" folder containing:
          - WhatsApp Chat with <name>.txt   (header lines + inline attachment stubs)
          - media files (PTT-*.opus, IMG-*, VID-*, DOC-*, etc.)
Output: <OUT_ROOT>/<tier>/<slug>/messages.json  + optional media symlink info
        Same key fields as msgstore extractor: chat_id, slug, subject,
        message_count, extracted_at_utc, source_db (here: source_export),
        and per-message: id, ts_ms, ts_iso, from_me, sender_jid, type, text,
        starred (always False), media?.

txt export lacks JIDs and stable chat_id → we synthesize:
  - chat_id: negative int derived from md5(export basename) (deterministic, no
    collision with SQLite positive _id space)
  - message id: sequential 1..N (unique within this export)
  - key_id: None (no server key available)
  - sender_jid: raw display name from the header (not a phone JID)
  - from_me: sender matches SELF_SENDER

message_type mapping to match SQLite extractor:
  0 = plain text
  1 = image (jpg/jpeg/png/webp/gif)
  2 = audio/voice (opus/m4a/aac/mp3/ogg)
  3 = video (mp4/3gp/mov)
  7 = document / other (pdf/docx/xlsx/vcf/txt/zip)  [new; msgstore uses many types]

Usage:
  python3 extract_wa_txt_export.py \
      --export "/path/to/WhatsApp Chat with X" \
      --tier tier1_deep \
      --tier-prefix "11__gabriella_gp___" \
      --subject "WhatsApp export: Gabriella González Pane 2026-05..2026-07" \
      --self weissvanderpol \
      --media-subdir "media/audio"    # relative to chat dir; audio kept, others recorded metadata-only

Media policy: image/video/vcf/document filenames are recorded in the media
block ("recorded_only": True, no file copied) unless --copy-all is passed.
Audio (.opus/.m4a/.aac) is expected to be pre-copied to <chat_dir>/<media-subdir>/
by the caller (this script does NOT copy media itself).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# 5/31/26, 6:58 PM - Sender Name: message text
HEADER_RE = re.compile(
    r"^(?P<date>\d{1,2}/\d{1,2}/\d{2}),\s+(?P<time>\d{1,2}:\d{2})\s*(?P<ampm>[AP]M)\s+-\s+(?P<rest>.*)$"
)
ATTACH_RE = re.compile(r"^(?P<fname>\S+\.[A-Za-z0-9]{2,5})\s+\(file attached\)\s*$")

EXT_TO_TYPE = {
    "jpg": 1,
    "jpeg": 1,
    "png": 1,
    "webp": 1,
    "gif": 1,
    "opus": 2,
    "m4a": 2,
    "aac": 2,
    "mp3": 2,
    "ogg": 2,
    "wav": 2,
    "mp4": 3,
    "3gp": 3,
    "mov": 3,
    "mkv": 3,
    "pdf": 7,
    "docx": 7,
    "doc": 7,
    "xlsx": 7,
    "xls": 7,
    "vcf": 7,
    "txt": 7,
    "zip": 7,
}
EXT_TO_MIME = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "webp": "image/webp",
    "gif": "image/gif",
    "opus": "audio/ogg; codecs=opus",
    "m4a": "audio/mp4",
    "aac": "audio/aac",
    "mp3": "audio/mpeg",
    "ogg": "audio/ogg",
    "wav": "audio/wav",
    "mp4": "video/mp4",
    "3gp": "video/3gpp",
    "mov": "video/quicktime",
    "mkv": "video/x-matroska",
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "doc": "application/msword",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "xls": "application/vnd.ms-excel",
    "vcf": "text/vcard",
    "txt": "text/plain",
    "zip": "application/zip",
}


def parse_header(line: str) -> tuple[int, str] | None:
    """Return (ts_ms_utc, rest_after_dash) or None if line is not a header."""
    m = HEADER_RE.match(line)
    if not m:
        return None
    date, time, ampm, rest = m.group("date"), m.group("time"), m.group("ampm"), m.group("rest")
    try:
        dt = datetime.strptime(f"{date} {time} {ampm}", "%m/%d/%y %I:%M %p")
    except ValueError:
        return None
    # Treat export timestamps as local Paraguay time (UTC-3, no DST since 2010).
    dt = dt.replace(tzinfo=timezone.utc) - _tz_offset()
    return int(dt.timestamp() * 1000), rest


def _tz_offset():
    # Paraguay is UTC-3 (fixed). We want UTC ms, so subtract -3h == add 3h wall→UTC.
    # Header timestamp is local → UTC = local + 3h.
    from datetime import timedelta

    return timedelta(hours=-3)


def iso(ts_ms: int) -> str:
    return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).isoformat()


def synth_chat_id(export_basename: str) -> int:
    h = hashlib.md5(export_basename.encode("utf-8")).digest()
    # 6 bytes → 48-bit uint, then negate to stay out of SQLite positive _id space
    n = int.from_bytes(h[:6], "big")
    return -(n or 1)


def classify_attachment(fname: str) -> tuple[int, str]:
    ext = fname.rsplit(".", 1)[-1].lower()
    return EXT_TO_TYPE.get(ext, 7), EXT_TO_MIME.get(ext, "application/octet-stream")


def build_messages(
    txt_path: Path, self_name: str, media_dir_rel: str, media_root: Path | None
) -> list[dict]:
    out: list[dict] = []
    current: dict | None = None
    with open(txt_path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            parsed = parse_header(line)
            if parsed is None:
                # continuation of previous message
                if current is not None and current.get("text") is not None:
                    current["text"] = current["text"] + "\n" + line
                continue
            # flush previous
            if current is not None:
                out.append(current)
                current = None
            ts_ms, rest = parsed
            # split "Sender: text" — sender may contain spaces; system lines have no colon.
            if ": " not in rest:
                # system line (encryption notice, etc.) — skip
                continue
            sender, _, body = rest.partition(": ")
            from_me = sender.strip().lower() == self_name.strip().lower()
            msg_id = len(out) + 1  # 1-based within this export

            entry = {
                "id": msg_id,
                "key_id": None,
                "ts_ms": ts_ms,
                "ts_iso": iso(ts_ms),
                "from_me": from_me,
                "sender_jid": None if from_me else sender,
                "type": 0,
                "text": body,
                "starred": False,
            }
            # attachment detection: body is a single "FILE.ext (file attached)" line
            m = ATTACH_RE.match(body)
            if m:
                fname = m.group("fname")
                mtype, mime = classify_attachment(fname)
                media = {
                    "mime": mime,
                    "path": f"{media_dir_rel}/{fname}",
                    "size": None,
                    "duration_s": None,
                    "sha256_b64": None,
                    "media_name": fname,
                    "media_caption": None,
                    "source_filename": fname,
                }
                # if media_root provided and the local media exists, fill size
                if media_root is not None:
                    p = media_root / fname
                    if p.exists() and p.is_file():
                        media["size"] = p.stat().st_size
                    else:
                        media["recorded_only"] = True
                entry["type"] = mtype
                entry["text"] = None
                entry["media"] = media
            current = entry
    if current is not None:
        out.append(current)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", required=True, help="Folder containing 'WhatsApp Chat with *.txt'")
    ap.add_argument(
        "--out-root",
        default="/home/ai-whisperers/psychology-integration/psycology/SOURCE_OF_TRUTH/wa_messages",
    )
    ap.add_argument(
        "--tier",
        default="tier1_deep",
        choices=["tier1_deep", "tier2_core", "_dropped", "_conversations"],
    )
    ap.add_argument("--tier-prefix", required=True, help="e.g. '11__gabriella_gp___'")
    ap.add_argument("--slug", default="wa_export", help="Slug suffix after tier-prefix")
    ap.add_argument("--subject", required=True)
    ap.add_argument(
        "--self",
        dest="self_name",
        required=True,
        help="Display name used for your own messages in the export",
    )
    ap.add_argument(
        "--media-subdir",
        default="media/audio",
        help="Relative subdir under chat_dir where audio is stored",
    )
    ap.add_argument(
        "--media-source", default=None, help="Path where source media files live (for size lookup)"
    )
    args = ap.parse_args()

    export_dir = Path(args.export)
    if not export_dir.is_dir():
        print(f"missing export dir: {export_dir}", file=sys.stderr)
        return 1
    txts = list(export_dir.glob("WhatsApp Chat with *.txt"))
    if not txts:
        print(f"no 'WhatsApp Chat with *.txt' in {export_dir}", file=sys.stderr)
        return 1
    txt_path = txts[0]

    export_basename = txt_path.name
    chat_id = synth_chat_id(export_basename)
    slug = f"{args.tier_prefix}{args.slug}"
    chat_dir = Path(args.out_root) / args.tier / slug
    chat_dir.mkdir(parents=True, exist_ok=True)

    media_root = Path(args.media_source) if args.media_source else export_dir
    messages = build_messages(txt_path, args.self_name, args.media_subdir, media_root)

    payload = {
        "chat_id": chat_id,
        "slug": slug,
        "subject": args.subject,
        "jid_user": None,
        "jid_server": None,
        "jid_raw": None,
        "message_count": len(messages),
        "extracted_at_utc": datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat(),
        "source_export": export_basename,
        "source_type": "wa_txt_export",
        "self_display_name": args.self_name,
        "messages": messages,
    }

    out_path = chat_dir / "messages.json"
    tmp = out_path.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    tmp.replace(out_path)

    # media counts summary
    kinds = {0: 0, 1: 0, 2: 0, 3: 0, 7: 0}
    for m in messages:
        kinds[m["type"]] = kinds.get(m["type"], 0) + 1
    print(
        f"wrote {out_path} — {len(messages)} messages "
        f"(text={kinds[0]} image={kinds[1]} audio={kinds[2]} video={kinds[3]} doc={kinds[7]})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

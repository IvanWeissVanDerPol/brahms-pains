#!/usr/bin/env python3
"""Extract WhatsApp text messages + audio metadata from decrypted msgstore.db
into psycology/SOURCE_OF_TRUTH/wa_messages/<chat_slug>/messages.json.

Filters:
  - message_type in (0 plain text, 1 image w/ caption, 2 audio/voice note, 3 video w/ caption)
  - either text_data present OR media metadata present
Skips:
  - system/notice messages, GIFs, stickers, polls, calls, vcards
  - chats with zero surviving messages

Slug rules (deterministic, safe for filesystems):
  g.us group      -> _wa_group_<subject-slug>_<chat_id>
  s.whatsapp.net  -> _wa_chat_<phone>_<chat_id>
  broadcast/lid   -> _wa_other_<jid-slug>_<chat_id>
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DB = "/data/media/phone-extract/wa/Databases/msgstore-latest-2026-07-20T14.db"
OUT_ROOT = Path(__file__).resolve().parent.parent / "SOURCE_OF_TRUTH" / "wa_messages"
MIN_MESSAGES_PER_CHAT = 1  # keep everything; empty chats already skipped


def slugify(s: str, maxlen: int = 60) -> str:
    if not s:
        return "unnamed"
    s = re.sub(r"[^\w\-]+", "_", s, flags=re.UNICODE)
    s = re.sub(r"_+", "_", s).strip("_-")
    return (s[:maxlen] or "unnamed").lower()


def iso(ts_ms: int | None) -> str | None:
    if ts_ms is None or ts_ms <= 0:
        return None
    return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).isoformat()


def chat_slug(
    chat_id: int, subject: str | None, jid_user: str | None, jid_server: str | None
) -> str:
    if jid_server == "g.us":
        base = f"_wa_group_{slugify(subject or 'no_subject')}"
    elif jid_server == "s.whatsapp.net":
        base = f"_wa_chat_{slugify(jid_user or 'unknown')}"
    elif jid_server == "broadcast":
        base = f"_wa_broadcast_{slugify(jid_user or 'anon')}"
    elif jid_server == "lid":
        base = f"_wa_lid_{slugify(jid_user or 'anon')}"
    else:
        base = f"_wa_other_{slugify(jid_server or 'unk')}_{slugify(jid_user or 'anon')}"
    return f"{base}_{chat_id}"


def main() -> int:
    if not os.path.exists(DB):
        print(f"missing db: {DB}", file=sys.stderr)
        return 1
    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row

    # 1) enumerate chats we care about
    chats = con.execute("""
        SELECT c._id AS chat_id,
               c.subject AS subject,
               j.user   AS jid_user,
               j.server AS jid_server,
               j.raw_string AS jid_raw
        FROM chat c
        JOIN jid  j ON j._id = c.jid_row_id
    """).fetchall()
    print(f"chats: {len(chats)}")

    # 2) preload sender-jid → raw_string map (small enough)
    sender_map: dict[int, str] = {
        r["_id"]: r["raw_string"] for r in con.execute("SELECT _id, raw_string FROM jid")
    }

    # 3) preload media (message_row_id → dict) — one shot, ~121k rows, fine in RAM
    media_map: dict[int, dict] = {}
    for r in con.execute("""
        SELECT message_row_id, mime_type, file_path, file_size,
               media_duration, file_hash, media_name, media_caption
        FROM message_media
    """):
        media_map[r["message_row_id"]] = {
            "mime": r["mime_type"],
            "path": r["file_path"],
            "size": r["file_size"],
            "duration_s": r["media_duration"],
            "sha256_b64": r["file_hash"],
            "media_name": r["media_name"],
            "media_caption": r["media_caption"],
        }
    print(f"media rows loaded: {len(media_map)}")

    total_written = 0
    total_msgs = 0
    slug_counts: dict[str, int] = {}
    dup_check: dict[str, int] = {}

    for c in chats:
        cid = c["chat_id"]
        slug = chat_slug(cid, c["subject"], c["jid_user"], c["jid_server"])
        if slug in dup_check and dup_check[slug] != cid:
            slug = f"{slug}_dup{cid}"
        dup_check[slug] = cid

        rows = con.execute(
            """
            SELECT _id, timestamp, received_timestamp, from_me, sender_jid_row_id,
                   message_type, text_data, key_id, starred
            FROM message
            WHERE chat_row_id = ?
              AND message_type IN (0, 1, 2, 3)
            ORDER BY sort_id, _id
        """,
            (cid,),
        ).fetchall()

        out_rows = []
        for r in rows:
            mtype = r["message_type"]
            text = r["text_data"]
            media = media_map.get(r["_id"])
            # keep if text OR media metadata
            if not text and not media:
                continue
            entry = {
                "id": r["_id"],
                "key_id": r["key_id"],
                "ts_ms": r["timestamp"],
                "ts_iso": iso(r["timestamp"]),
                "from_me": bool(r["from_me"]),
                "sender_jid": sender_map.get(r["sender_jid_row_id"]) if not r["from_me"] else None,
                "type": mtype,
                "text": text,
                "starred": bool(r["starred"]),
            }
            if media:
                entry["media"] = media
            out_rows.append(entry)

        if len(out_rows) < MIN_MESSAGES_PER_CHAT:
            continue

        chat_dir = OUT_ROOT / slug
        chat_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "chat_id": cid,
            "slug": slug,
            "subject": c["subject"],
            "jid_user": c["jid_user"],
            "jid_server": c["jid_server"],
            "jid_raw": c["jid_raw"],
            "message_count": len(out_rows),
            "extracted_at_utc": "2026-07-20T00:00:00+00:00",
            "source_db": os.path.basename(DB),
            "messages": out_rows,
        }
        out_path = chat_dir / "messages.json"
        # atomic write
        tmp = out_path.with_suffix(".json.tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=1)
        tmp.replace(out_path)
        total_written += 1
        total_msgs += len(out_rows)
        slug_counts[slug] = len(out_rows)

    # summary manifest at root
    manifest = {
        "extracted_at_utc": "2026-07-20T00:00:00+00:00",
        "source_db": os.path.basename(DB),
        "chats_written": total_written,
        "total_messages": total_msgs,
        "chats": sorted(
            [{"slug": s, "messages": n} for s, n in slug_counts.items()],
            key=lambda x: -x["messages"],
        ),
    }
    with open(OUT_ROOT / "_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)

    print(f"wrote {total_written} chats, {total_msgs} messages")
    return 0


if __name__ == "__main__":
    sys.exit(main())

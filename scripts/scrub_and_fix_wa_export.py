#!/usr/bin/env python3
"""In-place scrub + fix pass over the Gabriella WA-export messages.json.

Post-processes what extract_wa_txt_export.py produced:

  1. Media path routing by type
       type==1 (image)  -> path = media/images/<fname>   + recorded_only=True + exclusion_reason
       type==2 (audio)  -> path = media/audio/<fname>    (real file present)
       type==3 (video)  -> path = media/videos/<fname>   + recorded_only=True + exclusion_reason
       type==7 (doc)    -> path = media/docs/<fname>     (recorded_only for .vcf)
  2. Third-party contact PII: mark every .vcf as recorded_only, exclusion_reason set.
  3. Recover attachment stubs that ATTACH_RE missed (spaces / trailing dot) and
     promote them into typed media entries with recorded_only + reason.
  4. Scrub biobox JWT token from message id=5747.
  5. Atomic write.

Idempotent: running twice yields the same file.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CHAT_DIR = Path(
    "/home/ai-whisperers/psychology-integration/psycology/"
    "SOURCE_OF_TRUTH/wa_messages/tier1_deep/11__gabriella_gp___wa_export_2026"
)
MSG_PATH = CHAT_DIR / "messages.json"

EXT_TO_TYPE = {
    "jpg": 1, "jpeg": 1, "png": 1, "webp": 1, "gif": 1,
    "opus": 2, "m4a": 2, "aac": 2, "mp3": 2, "ogg": 2, "wav": 2,
    "mp4": 3, "3gp": 3, "mov": 3, "mkv": 3,
    "pdf": 7, "docx": 7, "doc": 7, "xlsx": 7, "xls": 7,
    "vcf": 7, "txt": 7, "zip": 7, "md": 7,
}
EXT_TO_MIME = {
    "jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
    "webp": "image/webp", "gif": "image/gif",
    "opus": "audio/ogg; codecs=opus", "m4a": "audio/mp4",
    "aac": "audio/aac", "mp3": "audio/mpeg", "ogg": "audio/ogg", "wav": "audio/wav",
    "mp4": "video/mp4", "3gp": "video/3gpp", "mov": "video/quicktime", "mkv": "video/x-matroska",
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "doc": "application/msword",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "xls": "application/vnd.ms-excel",
    "vcf": "text/vcard", "txt": "text/plain", "zip": "application/zip",
    "md": "text/markdown",
}

TYPE_SUBDIR = {1: "media/images", 2: "media/audio", 3: "media/videos", 7: "media/docs"}

# Type=0 messages whose body is actually an attachment stub the anchored
# ATTACH_RE rejected (spaces in filename, or trailing dot before extension).
# Each entry: id -> (recovered filename, exclusion_reason or None)
STUB_RECOVERY = {
    496:  ("Olga Piercings.vcf",                 "third-party contact PII"),
    1336: ("DOC-20260628-WA0034.txt",            None),  # on-disk, keep
    3052: ("5 contacts.vcf",                     "third-party contact PII"),
    3240: ("Nicolas Duarte (GF es silvi).vcf",   "third-party contact PII"),
    3611: ("Luaaa Bf Fer.vcf",                   "third-party contact PII"),
    5745: ("DOC-20260722-WA0048.pdf",            "PHI: personal blood-lab results, not committed"),
}

# vcf docs that WERE parsed (came in as type=7) — mark recorded_only
VCF_EXCLUSION_REASON = "third-party contact PII"

JWT_MSG_ID = 5747
JWT_RE = re.compile(r"token=eyJ[A-Za-z0-9_\-\.]+")


def classify(fname: str) -> tuple[int, str]:
    ext = fname.rsplit(".", 1)[-1].lower()
    return EXT_TO_TYPE.get(ext, 7), EXT_TO_MIME.get(ext, "application/octet-stream")


def route_media_path(fname: str, mtype: int) -> str:
    subdir = TYPE_SUBDIR.get(mtype, "media")
    return f"{subdir}/{fname}"


def scrub(msgs: list[dict]) -> dict:
    stats = {
        "images_marked": 0, "videos_marked": 0, "audio_repathed": 0,
        "docs_repathed": 0, "vcfs_excluded": 0,
        "stubs_recovered": 0, "phi_excluded": 0, "jwt_scrubbed": 0,
    }
    for m in msgs:
        mtype = m.get("type", 0)

        # 1) recover attachment stubs that lived as type=0 text
        if mtype == 0 and m["id"] in STUB_RECOVERY:
            fname, reason = STUB_RECOVERY[m["id"]]
            new_type, mime = classify(fname)
            media = {
                "mime": mime,
                "path": route_media_path(fname, new_type),
                "size": None,
                "duration_s": None,
                "sha256_b64": None,
                "media_name": fname,
                "media_caption": None,
                "source_filename": fname,
            }
            if reason is not None:
                media["recorded_only"] = True
                media["exclusion_reason"] = reason
                stats["stubs_recovered"] += 1
                if "PHI" in reason:
                    stats["phi_excluded"] += 1
                elif "PII" in reason:
                    stats["vcfs_excluded"] += 1
            else:
                stats["docs_repathed"] += 1
            m["type"] = new_type
            m["text"] = None
            m["media"] = media
            continue

        # 2) typed messages — route path + apply exclusion policy
        media = m.get("media")
        if not media:
            continue
        fname = media.get("media_name") or media.get("source_filename")
        if not fname:
            continue
        media["path"] = route_media_path(fname, mtype)

        if mtype == 1:
            media["recorded_only"] = True
            media["exclusion_reason"] = "images excluded per policy"
            stats["images_marked"] += 1
        elif mtype == 2:
            media.pop("exclusion_reason", None)
            media["recorded_only"] = False
            stats["audio_repathed"] += 1
        elif mtype == 3:
            media["recorded_only"] = True
            media["exclusion_reason"] = "videos excluded per policy"
            stats["videos_marked"] += 1
        elif mtype == 7:
            ext = fname.rsplit(".", 1)[-1].lower() if "." in fname else ""
            if ext == "vcf":
                media["recorded_only"] = True
                media["exclusion_reason"] = VCF_EXCLUSION_REASON
                stats["vcfs_excluded"] += 1
            else:
                media.pop("exclusion_reason", None)
                media["recorded_only"] = False
                stats["docs_repathed"] += 1

    # 3) JWT redaction
    for m in msgs:
        if m["id"] == JWT_MSG_ID and m.get("text"):
            new_text, n = JWT_RE.subn("token=<REDACTED_JWT>", m["text"])
            if n:
                m["text"] = new_text
                stats["jwt_scrubbed"] += n

    return stats


def main() -> int:
    if not MSG_PATH.exists():
        print(f"missing: {MSG_PATH}", file=sys.stderr)
        return 1
    payload = json.loads(MSG_PATH.read_text(encoding="utf-8"))
    msgs = payload["messages"]

    stats = scrub(msgs)

    kinds: dict[int, int] = {}
    for m in msgs:
        kinds[m["type"]] = kinds.get(m["type"], 0) + 1
    payload["message_count"] = len(msgs)

    tmp = MSG_PATH.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    tmp.replace(MSG_PATH)

    print(f"scrubbed {MSG_PATH}")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print(f"  type counts after: {kinds}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

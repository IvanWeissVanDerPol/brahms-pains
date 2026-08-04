#!/usr/bin/env python3
"""More aggressive name detection - read messages.json for self-intros."""

from __future__ import annotations

import json
import re
from pathlib import Path
from collections import Counter

REPO = Path(__file__).resolve().parent.parent
VNT = REPO / "SOURCE_OF_TRUTH" / "voice_note_transcripts"
WA = REPO / "SOURCE_OF_TRUTH" / "wa_messages"


def safe_name(name: str) -> str:
    if not name:
        return ""
    s = re.sub(r"[^\w\s-]", "", name).strip()
    s = re.sub(r"\s+", "_", s)
    return s


def is_clean(name: str) -> bool:
    if not name or len(name) < 4:
        return False
    if "=" in name:
        return False
    if re.match(r"^[0-9A-F=]+$", name.replace("_", "")):
        return False
    return True


def get_intro_name(chat_dir: Path) -> str | None:
    """Look for self-intro in messages."""
    mf = chat_dir / "messages.json"
    if not mf.exists():
        return None
    try:
        data = json.loads(mf.read_text())
    except:
        return None

    # Look at first 50 messages
    for msg in data.get("messages", [])[:50]:
        if not isinstance(msg, dict):
            continue
        text = msg.get("text", "")
        if not text:
            continue
        text_low = text.lower()

        # Try multiple patterns
        for pattern in [
            r"(?:soy|me llamo|yo soy|mi nombre es) ([a-záéíóúñ ]{2,30})",
            r"^hola[!,.]?\s+(?:soy|me llamo) ([a-záéíóúñ ]{2,30})",
            r"aquí\s+([a-záéíóúñ]{2,30})\s+(?:hablando|escribiendo)",
            r"te saluda ([a-záéíóúñ]{2,30})",
        ]:
            m = re.search(pattern, text_low)
            if m:
                name = m.group(1).strip().title()
                if is_clean(name):
                    return name
    return None


def get_transcript_intro_name(vnt_dir: Path) -> str | None:
    """Look for self-intro in transcript text."""
    tf = vnt_dir / "transcripts.json"
    if not tf.exists():
        return None
    try:
        data = json.loads(tf.read_text())
    except:
        return None
    if not isinstance(data, list):
        return None

    for entry in data[:30]:
        if not isinstance(entry, dict):
            continue
        text = entry.get("text", "")
        if not text:
            continue
        text_low = text.lower()
        for pattern in [
            r"(?:soy|me llamo|yo soy|mi nombre es) ([a-záéíóúñ ]{2,30})",
            r"^hola[!,.]?\s+(?:soy|me llamo) ([a-záéíóúñ ]{2,30})",
        ]:
            m = re.search(pattern, text_low)
            if m:
                name = m.group(1).strip().title()
                if is_clean(name):
                    return name
    return None


def main():
    vcard = json.loads(
        (REPO / "SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/viewer_full_data.json").read_text()
    )
    jid_to_name = {
        c["jid"]: c["name"] for c in vcard["vcard_contacts"] if c.get("jid") and c.get("name")
    }

    # Get all VNT folders
    vnt_remaining = []
    for d in VNT.iterdir():
        if not d.is_dir():
            continue
        if d.name.startswith("_"):
            continue
        m = re.match(r"^(chat|lid|group)_(\d{10,15})_\d+", d.name)
        if m:
            vnt_remaining.append((d.name, m.group(2)))

    # For each, try to find a name
    renames = []
    for folder, jid in vnt_remaining:
        # Skip if target already exists
        if jid in jid_to_name:
            target_safe = safe_name(jid_to_name[jid])
            if (VNT / target_safe).exists():
                continue

        # Find wa_messages dir
        wa_dir = None
        for tier in [
            "tier1_deep",
            "tier2_core",
            "tier3_extended",
            "tier4_groups",
            "untiered_personal",
            "other_lid",
            "_dropped",
            "_conversations",
        ]:
            tier_dir = WA / tier
            if not tier_dir.exists():
                continue
            for d in tier_dir.iterdir():
                if d.is_dir() and jid in d.name:
                    wa_dir = d
                    break
            if wa_dir:
                break

        canonical = None
        source = None

        # Try transcript self-intro first (most direct)
        vnt_dir = VNT / folder
        if vnt_dir.exists():
            canonical = get_transcript_intro_name(vnt_dir)
            if canonical:
                source = "transcript_intro"

        # Try messages.json self-intro
        if not canonical and wa_dir:
            canonical = get_intro_name(wa_dir)
            if canonical:
                source = "messages_intro"

        if canonical:
            safe = safe_name(canonical)
            if is_clean(safe):
                renames.append((folder, safe, jid, source, canonical))

    by_source = Counter([r[3] for r in renames])
    print(f"=== Renames by source: {len(renames)} ===")
    for s, n in by_source.most_common():
        print(f"  {s}: {n}")

    print("\n=== Sample renames ===")
    for r in renames[:30]:
        print(f"  {r[0]:<40} -> {r[1]:<35} [{r[3]}] {r[4]}")


if __name__ == "__main__":
    main()

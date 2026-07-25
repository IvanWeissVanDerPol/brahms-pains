#!/usr/bin/env python3
"""Final pass: read messages.json from wa_messages dirs for clean self-intros."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VNT = REPO / "SOURCE_OF_TRUTH" / "voice_note_transcripts"
WA = REPO / "SOURCE_OF_TRUTH" / "wa_messages"


def safe_name(name: str) -> str:
    if not name: return ""
    s = re.sub(r'[^\w\s-]', '', name).strip()
    s = re.sub(r'\s+', '_', s)
    return s


def is_clean(name: str) -> bool:
    if not name or len(name) < 4 or len(name) > 25: return False
    if "=" in name: return False
    if re.match(r'^[0-9A-F=]+$', name.replace("_", "")): return False
    if name.endswith("_D") or name.endswith("_I") or name.endswith("_Y"):
        return False
    if re.search(r'_[A-Z]_[A-Z]?_?$', name):
        return False
    if name.count("_") > 3:
        return False
    return True


def main():
    vcard = json.loads((REPO / "SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/viewer_full_data.json").read_text())
    jid_to_name = {c["jid"]: c["name"] for c in vcard["vcard_contacts"] if c.get("jid") and c.get("name")}

    vnt_remaining = []
    for d in VNT.iterdir():
        if not d.is_dir(): continue
        if d.name.startswith("_"): continue
        m = re.match(r'^(chat|lid|group)_(\d{10,15})_\d+', d.name)
        if m:
            vnt_remaining.append((d.name, m.group(2)))

    applied = 0
    skipped = 0
    for folder, jid in vnt_remaining:
        if jid in jid_to_name:
            target_safe = safe_name(jid_to_name[jid])
            if (VNT / target_safe).exists():
                continue

        vnt_dir = VNT / folder
        if not vnt_dir.exists(): continue

        # Find wa_messages dir
        wa_dir = None
        for tier in ["tier1_deep", "tier2_core", "tier3_extended", "tier4_groups", "untiered_personal", "other_lid", "_dropped", "_conversations"]:
            tier_dir = WA / tier
            if not tier_dir.exists(): continue
            for d in tier_dir.iterdir():
                if d.is_dir() and jid in d.name:
                    wa_dir = d
                    break
            if wa_dir: break

        if not wa_dir:
            skipped += 1
            continue

        # Read messages.json
        mf = wa_dir / "messages.json"
        if not mf.exists():
            skipped += 1
            continue
        try:
            data = json.loads(mf.read_text())
        except: continue

        # Look for self-intro in first 50 messages
        canonical = None
        for msg in data.get("messages", [])[:50]:
            if not isinstance(msg, dict): continue
            text = msg.get("text", "")
            if not text: continue
            text_low = text.lower()
            m = re.search(r'\b(?:soy|me llamo|mi nombre es) ([a-záéíóúñ]{2,20})\b', text_low)
            if m:
                candidate = m.group(1).strip().title()
                if is_clean(candidate):
                    canonical = candidate
                    break

        if not canonical:
            skipped += 1
            continue

        safe = safe_name(canonical)
        if not is_clean(safe) or safe == folder:
            skipped += 1
            continue

        new_path = VNT / safe
        if new_path.exists():
            skipped += 1
            continue

        shutil.move(str(vnt_dir), new_path)
        print(f"  RENAMED: {folder} -> {safe}  ({canonical})")
        applied += 1

    print(f"\n=== Summary ===")
    print(f"  Applied: {applied}")
    print(f"  Skipped: {skipped}")


if __name__ == "__main__":
    main()

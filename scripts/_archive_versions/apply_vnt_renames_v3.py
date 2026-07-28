#!/usr/bin/env python3
"""Apply v4 renames with strict quality filter."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VNT = REPO / "SOURCE_OF_TRUTH" / "voice_note_transcripts"


def safe_name(name: str) -> str:
    if not name: return ""
    s = re.sub(r'[^\w\s-]', '', name).strip()
    s = re.sub(r'\s+', '_', s)
    return s


def is_clean(name: str) -> bool:
    if not name or len(name) < 3 or len(name) > 25: return False
    if "=" in name: return False
    if re.match(r'^[0-9A-F=]+$', name.replace("_", "")): return False
    # Truncation indicators
    if name.endswith("_D") or name.endswith("_I") or name.endswith("_Y") or name.endswith("_M"):
        return False
    if re.search(r'_[A-Z]_[A-Z]?_?$', name):
        return False
    # Multi-word descriptions (likely sentences)
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
        # Skip if vCard target exists
        if jid in jid_to_name:
            target_safe = safe_name(jid_to_name[jid])
            if (VNT / target_safe).exists():
                continue

        # Check if name detection is possible
        # Just check if there's a clean name in the file name or messages
        vnt_dir = VNT / folder
        if not vnt_dir.exists(): continue
        tf = vnt_dir / "transcripts.json"
        if not tf.exists(): continue

        # Look for the simplest "soy X" with short name
        try:
            data = json.loads(tf.read_text())
        except: continue
        if not isinstance(data, list): continue

        canonical = None
        for entry in data[:20]:
            if not isinstance(entry, dict): continue
            text = entry.get("text", "")
            if not text: continue
            text_low = text.lower()

            # Look for "soy X" where X is 1-2 words
            m = re.search(r'\bsoy ([a-záéíóúñ]{2,20})\b', text_low)
            if m:
                candidate = m.group(1).strip().title()
                if is_clean(candidate):
                    canonical = candidate
                    break
            # Also "me llamo X"
            m = re.search(r'\bme llamo ([a-záéíóúñ]{2,20})\b', text_low)
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

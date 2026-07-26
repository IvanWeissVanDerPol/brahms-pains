#!/usr/bin/env python3
"""Force-clean orphan VNT folders after merge."""
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


def main():
    vcard = json.loads((REPO / "SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/viewer_full_data.json").read_text())
    jid_to_name = {c["jid"]: c["name"] for c in vcard["vcard_contacts"] if c.get("jid") and c.get("name")}

    deleted = 0
    renamed = 0
    for d in sorted(VNT.iterdir()):
        if not d.is_dir(): continue
        if d.name.startswith("_"): continue
        m = re.match(r'^(chat|lid|group)_(\d{10,15})_\d+', d.name)
        if not m: continue

        jid = m.group(2)
        if jid not in jid_to_name:
            continue

        target_name = safe_name(jid_to_name[jid])
        target_path = VNT / target_name

        if not target_path.exists():
            # Just rename
            shutil.move(str(d), str(target_path))
            print(f"  RENAMED: {d.name} -> {target_name}")
            renamed += 1
            continue

        # Source is a duplicate of target - delete source
        # (All entries already in target from previous merge)
        shutil.rmtree(d)
        print(f"  DELETED: {d.name} (dup of {target_name})")
        deleted += 1

    print(f"\n=== Summary ===")
    print(f"  Renamed: {renamed}")
    print(f"  Deleted: {deleted}")


if __name__ == "__main__":
    main()

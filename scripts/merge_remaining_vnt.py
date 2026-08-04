#!/usr/bin/env python3
"""Merge remaining VNT numbered folders into named targets where possible."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VNT = REPO / "SOURCE_OF_TRUTH" / "voice_note_transcripts"


def safe_name(name: str) -> str:
    if not name:
        return ""
    s = re.sub(r"[^\w\s-]", "", name).strip()
    s = re.sub(r"\s+", "_", s)
    return s


def is_clean(name: str) -> bool:
    if not name or len(name) < 3:
        return False
    if "=" in name:
        return False
    return True


def main():
    # Load vCard
    vcard = json.loads(
        (REPO / "SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/viewer_full_data.json").read_text()
    )
    jid_to_name = {
        c["jid"]: c["name"] for c in vcard["vcard_contacts"] if c.get("jid") and c.get("name")
    }

    merged = 0
    deleted = 0
    kept = 0

    for d in sorted(VNT.iterdir()):
        if not d.is_dir():
            continue
        if d.name.startswith("_"):
            continue
        m = re.match(r"^(chat|lid|group)_(\d{10,15})_\d+", d.name)
        if not m:
            continue

        jid = m.group(2)
        if jid not in jid_to_name:
            kept += 1
            continue

        target_name = safe_name(jid_to_name[jid])
        target_path = VNT / target_name

        if not is_clean(target_name):
            kept += 1
            continue

        # Load data
        src_tf = d / "transcripts.json"
        if not src_tf.exists():
            kept += 1
            continue
        try:
            src_data = json.loads(src_tf.read_text())
        except:
            kept += 1
            continue
        if not isinstance(src_data, list):
            kept += 1
            continue

        if not target_path.exists():
            # Just rename
            shutil.move(str(d), str(target_path))
            print(f"  RENAMED: {d.name} -> {target_name}")
            merged += 1
            continue

        # Merge into target
        target_tf = target_path / "transcripts.json"
        if not target_tf.exists():
            shutil.move(str(d), str(target_path))
            print(f"  MERGED (no target tf): {d.name} -> {target_name}")
            merged += 1
            continue

        try:
            target_data = json.loads(target_tf.read_text())
        except:
            shutil.move(str(d), str(target_path))
            print(f"  MERGED (no target data): {d.name} -> {target_name}")
            merged += 1
            continue

        # Add unique entries
        existing_files = {e.get("file") for e in target_data if isinstance(e, dict)}
        added = 0
        for entry in src_data:
            if isinstance(entry, dict) and entry.get("file") not in existing_files:
                target_data.append(entry)
                added += 1

        if added > 0:
            target_tf.write_text(json.dumps(target_data, indent=1, ensure_ascii=False))
            print(f"  MERGED: {d.name} -> {target_name} (+{added} entries)")
            merged += 1
        else:
            print(f"  NO-OP (all dupes): {d.name}")
            deleted += 1

        # Move other files (transcripts.txt, etc.)
        for f in d.iterdir():
            if f.name == "transcripts.json":
                continue
            dest = target_path / f.name
            if not dest.exists():
                shutil.move(str(f), str(dest))
            else:
                f.unlink()

        # Remove the now-empty dir
        try:
            d.rmdir()
        except:
            pass

    print("\n=== Summary ===")
    print(f"  Merged: {merged}")
    print(f"  Deleted (all dupes): {deleted}")
    print(f"  Kept (no vCard): {kept}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Apply v3 renames - only vCard matches (highest confidence)."""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from collections import Counter

REPO = Path(__file__).resolve().parent.parent
VNT = REPO / "SOURCE_OF_TRUTH" / "voice_note_transcripts"


def is_clean(name: str) -> bool:
    if not name or len(name) < 4: return False
    if "=" in name: return False
    return True


def main():
    mapping = json.loads((VNT / "_mapping_v2.json").read_text())
    renames = mapping["renames"]

    # Only apply vCard-sourced renames
    vcard_renames = [r for r in renames if r["source"] == "vcard"]
    print(f"vCard renames: {len(vcard_renames)}")

    applied = 0
    skipped_exists = 0
    skipped_other = 0
    for r in vcard_renames:
        old = r["folder"]
        new = r["safe_name"]
        if not is_clean(new):
            print(f"  SKIP (dirty): {old} -> {new}")
            skipped_other += 1
            continue
        old_path = VNT / old
        new_path = VNT / new
        if new_path.exists():
            print(f"  SKIP (target exists): {old} -> {new}")
            skipped_exists += 1
            continue
        if not old_path.exists():
            print(f"  SKIP (source gone): {old}")
            skipped_other += 1
            continue
        shutil.move(str(old_path), str(new_path))
        print(f"  RENAMED: {old} -> {new}")
        applied += 1

    print(f"\n=== Summary ===")
    print(f"  Applied: {applied}")
    print(f"  Skipped (target exists): {skipped_exists}")
    print(f"  Skipped (other): {skipped_other}")


if __name__ == "__main__":
    main()

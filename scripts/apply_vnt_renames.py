#!/usr/bin/env python3
"""Apply VNT folder renames safely — only confident matches."""

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
    """Check if a target name is clean (no encoding artifacts, decent length)."""
    if not name or len(name) < 4:
        return False
    # No hex artifacts
    if re.match(r"^[0-9A-F=]+$", name.replace("_", "")):
        return False
    if "=" in name:  # quoted-printable artifact
        return False
    # No truncation markers
    if re.search(r"_[A-Z]_[A-Z]?_?$", name):
        return False
    return True


def main():
    mapping = json.loads((VNT / "_mapping.json").read_text())
    maps = mapping["mappings"]

    # Filter to clean renames
    clean_renames = []
    seen_targets = set()
    for m in maps:
        if m["action"] != "rename":
            continue
        sn = m["safe_name"]
        if not is_clean(sn):
            print(f"  SKIP (dirty): {m['folder']} -> {sn}")
            continue
        if sn in seen_targets:
            print(f"  SKIP (duplicate): {m['folder']} -> {sn}")
            continue
        seen_targets.add(sn)
        clean_renames.append((m["folder"], sn))

    print(f"\n=== Applying {len(clean_renames)} clean renames ===")
    applied = 0
    skipped_existing = 0
    for old, new in clean_renames:
        old_path = VNT / old
        new_path = VNT / new
        if new_path.exists():
            # Don't overwrite an existing named folder
            print(f"  SKIP (target exists): {old} -> {new}")
            skipped_existing += 1
            continue
        if not old_path.exists():
            print(f"  SKIP (source gone): {old}")
            continue
        # Git mv would preserve history, but shutil.move is simpler
        try:
            shutil.move(str(old_path), str(new_path))
            print(f"  RENAMED: {old} -> {new}")
            applied += 1
        except Exception as e:
            print(f"  ERROR: {old}: {e}")

    print("\n=== Done ===")
    print(f"  Applied: {applied}")
    print(f"  Skipped (target exists): {skipped_existing}")


if __name__ == "__main__":
    main()

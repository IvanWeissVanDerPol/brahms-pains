#!/usr/bin/env python3
"""Merge VNT duplicate folders safely."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VNT = REPO / "SOURCE_OF_TRUTH" / "voice_note_transcripts"

# Load all transcripts
folder_data = {}
for d in VNT.iterdir():
    if not d.is_dir():
        continue
    if d.name.startswith("_"):
        continue
    tf = d / "transcripts.json"
    if not tf.exists():
        continue
    try:
        data = json.loads(tf.read_text())
    except:
        continue
    if not isinstance(data, list):
        continue
    files = {e.get("file") for e in data if isinstance(e, dict)}
    folder_data[d] = (files, data)


def jaccard(a, b):
    if not a or not b:
        return 0
    return len(a & b) / len(a | b)


# Find duplicates
processed = set()
merges = []
for d, (files, data) in folder_data.items():
    for other in list(folder_data.keys()):
        if d == other:
            continue
        if (d.name, other.name) in processed:
            continue
        if (other.name, d.name) in processed:
            continue
        other_files, _ = folder_data[other]
        sim = jaccard(files, other_files)
        if sim > 0.5:
            # Keep the one with more entries
            primary = d if len(data) >= len(folder_data[other][1]) else other
            secondary = other if primary == d else d
            merges.append((primary, secondary, sim, len(data), len(folder_data[other][1])))
            processed.add((primary.name, secondary.name))


def main():
    print(f"=== Proposed merges: {len(merges)} ===\n")
    for primary, secondary, sim, n1, n2 in merges:
        print(f"  {sim:.2f} sim: {secondary.name} ({n2}) -> {primary.name} ({n1})")

    print("\n=== Applying ===")
    for primary, secondary, sim, n1, n2 in merges:
        # Move any unique files from secondary to primary
        primary_files, primary_data = folder_data[primary]
        secondary_files, secondary_data = folder_data[secondary]

        # Files unique to secondary
        unique_to_secondary = secondary_files - primary_files
        if not unique_to_secondary:
            # Safe to delete secondary (subset of primary)
            shutil.rmtree(secondary)
            print(f"  DELETED (subset): {secondary.name}")
        else:
            # Merge unique entries
            existing_files = {e.get("file") for e in primary_data if isinstance(e, dict)}
            added = 0
            for entry in secondary_data:
                if isinstance(entry, dict) and entry.get("file") not in existing_files:
                    primary_data.append(entry)
                    added += 1
            if added > 0:
                # Save merged
                (primary / "transcripts.json").write_text(
                    json.dumps(primary_data, indent=1, ensure_ascii=False)
                )
                print(f"  MERGED: {secondary.name} -> {primary.name} (+{added} entries)")
            # Delete secondary
            shutil.rmtree(secondary)
            print(f"  DELETED: {secondary.name}")


if __name__ == "__main__":
    main()

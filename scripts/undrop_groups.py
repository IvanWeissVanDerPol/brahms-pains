#!/usr/bin/env python3
"""Move wrongly-dropped groups back to tier4_groups."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH" / "wa_messages"


def safe_name(name: str) -> str:
    if not name: return ""
    s = re.sub(r'[^\w\s-]', '', name).strip()
    s = re.sub(r'\s+', '_', s)
    return s


def main():
    dropped = WA / "_dropped"
    tier4 = WA / "tier4_groups"

    moved = 0
    merged = 0
    skipped = 0

    for d in sorted(dropped.iterdir()):
        if not d.is_dir(): continue
        if not d.name.startswith("Group_"): continue

        # Check msg count
        mf = d / "messages.json"
        n = 0
        if mf.exists():
            try:
                data = json.loads(mf.read_text())
                n = len(data.get("messages", []))
            except: pass

        # Only move if has significant msgs
        if n < 5:
            skipped += 1
            continue

        target = tier4 / d.name
        if target.exists():
            # Merge - combine messages
            src_tf = d / "transcripts.json"
            dst_tf = target / "transcripts.json"
            if src_tf.exists() and dst_tf.exists():
                try:
                    src_data = json.loads(src_tf.read_text())
                    dst_data = json.loads(dst_tf.read_text())
                    if isinstance(src_data, list) and isinstance(dst_data, list):
                        existing = {e.get("file") for e in dst_data if isinstance(e, dict)}
                        added = 0
                        for e in src_data:
                            if isinstance(e, dict) and e.get("file") not in existing:
                                dst_data.append(e)
                                added += 1
                        if added > 0:
                            dst_tf.write_text(json.dumps(dst_data, indent=1, ensure_ascii=False))
                            print(f"  MERGED: {d.name} (+{added} transcripts)")
                except: pass
            # Move media files
            for f in d.iterdir():
                if f.name == "transcripts.json": continue
                dest = target / f.name
                if not dest.exists():
                    shutil.move(str(f), str(dest))
                else:
                    f.unlink()
            shutil.rmtree(d)
            merged += 1
        else:
            shutil.move(str(d), str(target))
            print(f"  MOVED: {d.name} ({n} msgs)")
            moved += 1

    print(f"\n=== Summary ===")
    print(f"  Moved: {moved}")
    print(f"  Merged: {merged}")
    print(f"  Skipped: {skipped}")


if __name__ == "__main__":
    main()
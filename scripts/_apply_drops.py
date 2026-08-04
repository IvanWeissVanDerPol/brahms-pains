"""
Move every chat listed in _final_classification.json's drop_slugs into
./_dropped/ .  Reversible — nothing is deleted.

Run with:  python3 _apply_drops.py --yes
Without --yes it prints a dry-run summary and exits.
"""

import json
import sys
import shutil
from pathlib import Path

BASE = Path(__file__).parent
DROPPED = BASE / "_dropped"

final = json.loads((BASE / "_final_classification.json").read_text())
drop_slugs = final["drop_slugs"]

dry = "--yes" not in sys.argv

existing = [s for s in drop_slugs if (BASE / s).is_dir()]
missing = [s for s in drop_slugs if not (BASE / s).is_dir()]

print(
    f"Drop list: {len(drop_slugs)}  |  present on disk: {len(existing)}  |  already-missing: {len(missing)}"
)
if dry:
    print("Dry-run. Pass --yes to actually move.")
    for s in existing[:5]:
        print(f"  would move: {s}  ->  _dropped/{s}")
    if len(existing) > 5:
        print(f"  ... and {len(existing)-5} more")
    sys.exit(0)

DROPPED.mkdir(exist_ok=True)
moved = 0
for s in existing:
    src = BASE / s
    dst = DROPPED / s
    if dst.exists():
        print(f"skip (dest exists): {s}")
        continue
    shutil.move(str(src), str(dst))
    moved += 1

print(f"Moved {moved} chats into {DROPPED}")

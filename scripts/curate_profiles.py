#!/usr/bin/env python3
"""Properly curate profiles - move stubs to _stubs/ and dormant to _archive/."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROFILE_DIR = REPO / "RELATIONSHIPS/dynamics"
STUBS = PROFILE_DIR / "_stubs"
ARCHIVE = PROFILE_DIR / "_archive"
DELETABLE = PROFILE_DIR / "_deletable"

STUBS.mkdir(exist_ok=True)
ARCHIVE.mkdir(exist_ok=True)
DELETABLE.mkdir(exist_ok=True)

# Read the dashboard
DASH = json.loads((REPO / "SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/relationships_dashboard.json").read_text())
JID_INFO = {c["jid"]: c for c in DASH["scored"]}

# Rules:
# - Long (300+): KEEP at top (deep analysis)
# - Medium (100-299): KEEP at top
# - Short (30-99): if score >= 35 OR family name OR active recently -> STAY
#                    else -> _stubs/ or _archive/

FAMILY_KEYWORDS = ["poli", "van_der_pol", "weiss", "hermana", "kiki", "lua", "kuki", "kiara", "saskia"]
DORMANT_DAYS = 365
LOW_MSG_THRESHOLD = 50

# Move 73 files in _archive/ back to top, then re-classify
print("=== Step 1: Move _archive/ files back to top for re-evaluation ===")
for p in ARCHIVE.glob("*.md"):
    if p.name == "REVIEW.md": continue
    dest = PROFILE_DIR / p.name
    if dest.exists():
        print(f"  SKIP (target exists): {p.name}")
        continue
    shutil.move(str(p), dest)
    print(f"  RESTORED: {p.name}")

# Move _deletable REVIEW.md
for p in DELETABLE.glob("*.md"):
    if p.name == "REVIEW.md":
        continue
    dest = PROFILE_DIR / p.name
    if dest.exists():
        print(f"  SKIP (target exists): {p.name}")
        continue
    shutil.move(str(p), dest)
    print(f"  RESTORED: {p.name}")

# Step 2: Classify all top-level profiles
print("\n=== Step 2: Classify top-level profiles ===")
top_files = list(PROFILE_DIR.glob("*.md"))
print(f"  Total top-level: {len(top_files)}")

moved_to_stub = 0
moved_to_archive = 0
kept_at_top = 0

for p in top_files:
    content = p.read_text()
    line_count = len(content.split("\n"))

    # Extract JID
    m = re.search(r"\*\*JID:\*\* (\d+)", content)
    jid = m.group(1) if m else None

    info = JID_INFO.get(jid, {}) if jid else {}
    days = info.get("stats", {}).get("days_since_last", 0)
    msgs = info.get("total_msgs", 0)
    score = info.get("score", 0)
    canonical = info.get("name", "?")

    # Already a deep profile (300+ lines)? Keep at top
    if line_count >= 200:
        kept_at_top += 1
        continue

    # Family member? Keep at top
    name_low = p.stem.lower()
    if any(kw in name_low for kw in FAMILY_KEYWORDS):
        kept_at_top += 1
        continue

    # Active or important? Keep at top
    if score >= 50 or (msgs >= 100 and days < 365):
        kept_at_top += 1
        continue

    # Trivial (1-2 msgs)? Delete
    if msgs <= 2:
        p.unlink()
        print(f"  DELETED: {p.name} ({msgs} msgs)")
        continue

    # Stub? (auto-generated, <50 lines)
    if line_count < 50 and "Auto-generated profile stub" in content:
        dest = STUBS / p.name
        if dest.exists():
            p.unlink()
        else:
            shutil.move(str(p), dest)
        moved_to_stub += 1
        continue

    # Otherwise archive (dormant)
    if days > DORMANT_DAYS and msgs < LOW_MSG_THRESHOLD:
        dest = ARCHIVE / p.name
        if dest.exists():
            p.unlink()
        else:
            shutil.move(str(p), dest)
        moved_to_archive += 1
        continue

    # Keep at top
    kept_at_top += 1

print(f"\n=== Summary ===")
print(f"  Kept at top: {kept_at_top}")
print(f"  Moved to _stubs/: {moved_to_stub}")
print(f"  Moved to _archive/: {moved_to_archive}")
print(f"  Final top-level: {kept_at_top}")
print(f"  Final _stubs/: {len(list(STUBS.glob('*.md')))}")
print(f"  Final _archive/: {len(list(ARCHIVE.glob('*.md')))}")
print(f"  Final _deletable/: {len([p for p in DELETABLE.glob('*.md') if p.name != 'REVIEW.md'])}")

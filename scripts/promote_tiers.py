#!/usr/bin/env python3
"""Promote tier3_extended contacts with score >= 50 to tier2_core."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH" / "wa_messages"
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages/_ANALYSIS"


def safe_name(name: str) -> str:
    if not name: return ""
    s = re.sub(r'[^\w\s-]', '', name).strip()
    s = re.sub(r'\s+', '_', s)
    return s


def main():
    dash = json.loads((ANALYSIS / "relationships_dashboard.json").read_text())
    jid_to_info = {c["jid"]: c for c in dash["scored"]}

    tier3 = WA / "tier3_extended"
    tier2 = WA / "tier2_core"
    tier1 = WA / "tier1_deep"

    promoted = 0
    skipped = 0
    for d in sorted(tier3.iterdir()):
        if not d.is_dir(): continue

        m = re.search(r'(\d{10,15})', d.name)
        if not m: continue
        jid = m.group(1)
        info = jid_to_info.get(jid)
        if not info: continue

        score = info.get("score", 0)
        name = info.get("name", "?")
        msgs = info.get("total_msgs", 0)

        target_tier = None
        if score >= 70:
            target_tier = tier1
        elif score >= 50:
            target_tier = tier2

        if not target_tier:
            continue

        target_name = safe_name(name)
        target_path = target_tier / target_name

        if target_path.exists():
            skipped += 1
            continue

        shutil.move(str(d), str(target_path))
        print(f"  PROMOTED: {d.name} -> {target_tier.name}/{target_name} (score {score:.1f}, {msgs} msgs)")
        promoted += 1

    print(f"\n=== Summary ===")
    print(f"  Promoted: {promoted}")
    print(f"  Skipped: {skipped}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""Move wrongly-dropped chats to appropriate tiers."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH" / "wa_messages"
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages/_ANALYSIS"


def safe_name(name: str) -> str:
    if not name:
        return ""
    s = re.sub(r"[^\w\s-]", "", name).strip()
    s = re.sub(r"\s+", "_", s)
    return s


def get_target_tier(score):
    if score >= 70:
        return "tier1_deep"
    if score >= 50:
        return "tier2_core"
    if score >= 30:
        return "tier3_extended"
    return None  # leave in _dropped


def main():
    dash = json.loads((ANALYSIS / "relationships_dashboard.json").read_text())
    jid_to_info = {c["jid"]: c for c in dash["scored"]}

    dropped_dir = WA / "_dropped"

    moved = 0
    skipped = 0
    for d in sorted(dropped_dir.iterdir()):
        if not d.is_dir():
            continue

        # Get JID
        m = re.search(r"(\d{10,15})", d.name)
        if not m:
            continue
        jid = m.group(1)

        info = jid_to_info.get(jid)
        if not info:
            skipped += 1
            continue

        score = info.get("score", 0)
        name = info.get("name", "?")
        msgs = info.get("total_msgs", 0)
        target_tier = get_target_tier(score)

        if not target_tier:
            skipped += 1
            continue

        # Move
        target_dir = WA / target_tier
        target_name = safe_name(name)
        target_path = target_dir / target_name

        if target_path.exists():
            skipped += 1
            continue

        shutil.move(str(d), str(target_path))
        print(f"  MOVED: {d.name} -> {target_tier}/{target_name} (score {score:.1f}, {msgs} msgs)")
        moved += 1

    # Also handle grandpa_jan_van_der_pol
    g = dropped_dir / "grandpa_jan_van_der_pol___wa_chat_595994459555_9214"
    if g.exists():
        target = WA / "tier1_deep" / "Grandpa_Jan_Van_Der_Pol"
        if not target.exists():
            shutil.move(str(g), str(target))
            print("  MOVED: grandpa_jan_van_der_pol -> tier1_deep/Grandpa_Jan_Van_Der_Pol")

    print("\n=== Summary ===")
    print(f"  Moved: {moved}")
    print(f"  Skipped: {skipped}")


if __name__ == "__main__":
    main()

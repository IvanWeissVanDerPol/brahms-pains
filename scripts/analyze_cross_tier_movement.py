#!/usr/bin/env python3
"""Cross-tier movement analysis - did contacts move between tiers?"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH/wa_messages/_ANALYSIS"


def analyze_cross_tier_movement():
    """Identify contacts that may have moved between tier levels."""
    tl = json.loads((ANALYSIS / "conversation_timeline.json").read_text())
    rec = json.loads((ANALYSIS / "recency_heatmap.json").read_text())
    init = json.loads((ANALYSIS / "initiator_analysis.json").read_text())

    # Current tier from rec
    current_tiers = {}
    for chat, info in rec["per_chat"].items():
        current_tiers[chat] = info.get("tier", "unknown")

    # Analyze trajectory: peak year volume vs current
    movements = []

    for chat_name, info in tl["per_chat"].items():
        timeline = info["timeline"]
        if len(timeline) < 2:
            continue

        # Find peak year
        peak_year_data = max(timeline, key=lambda x: x["msgs"])
        peak_year = peak_year_data["year"]
        peak_msgs = peak_year_data["msgs"]

        # Get recent year (2026 or last)
        recent_year_data = timeline[-1]
        recent_year = recent_year_data["year"]
        recent_msgs = recent_year_data["msgs"]

        # Calculate trend
        if peak_msgs == 0:
            continue

        change_pct = (recent_msgs - peak_msgs) / peak_msgs
        years_since_peak = int(recent_year) - int(peak_year)

        # Movement direction
        if change_pct > 0.5 and years_since_peak == 0:
            # Recent surge
            direction = "SURGING"
        elif change_pct > 0.3:
            direction = "RISING"
        elif change_pct < -0.7:
            direction = "FALLING_SHARPLY"
        elif change_pct < -0.3:
            direction = "FALLING"
        elif change_pct < -0.1:
            direction = "COOLING"
        else:
            direction = "STABLE"

        # Infer old tier from peak activity
        current_tier = current_tiers.get(chat_name, "unknown")

        movements.append(
            {
                "chat": chat_name,
                "current_tier": current_tier,
                "peak_year": peak_year,
                "peak_msgs": peak_msgs,
                "recent_year": recent_year,
                "recent_msgs": recent_msgs,
                "change_pct": round(change_pct, 3),
                "years_since_peak": years_since_peak,
                "direction": direction,
                "lifetime_msgs": info["lifetime_msgs"],
            }
        )

    # Sort by change
    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_chats_analyzed": len(movements),
        "by_direction": {},
        "movements": movements,
    }

    for m in movements:
        direction = m["direction"]
        if direction not in summary["by_direction"]:
            summary["by_direction"][direction] = 0
        summary["by_direction"][direction] += 1

    out = ANALYSIS / "cross_tier_movement.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"Wrote {out.relative_to(REPO)}")

    print("\n=== Cross-Tier Movement Analysis ===")
    print(f"Total chats analyzed: {len(movements)}")

    print("\nDirection distribution:")
    for direction, count in sorted(summary["by_direction"].items(), key=lambda x: -x[1]):
        print(f"  {direction}: {count}")

    # Top surging
    print("\nTop 15 SURGING relationships:")
    for m in sorted(movements, key=lambda x: -x["change_pct"])[:15]:
        if m["change_pct"] > 0:
            print(
                f"  +{m['change_pct']:.0%}  {m['current_tier']:<15}  {m['recent_year']}  "
                f"{m['peak_year']}:{m['peak_msgs']} → {m['recent_year']}:{m['recent_msgs']}  {m['chat'][:30]}"
            )

    # Top falling
    print("\nTop 15 FALLING_SHARPLY relationships:")
    for m in sorted(movements, key=lambda x: x["change_pct"])[:15]:
        if m["change_pct"] < -0.5:
            print(
                f"  {m['change_pct']:.0%}  {m['current_tier']:<15}  peak {m['peak_year']} → "
                f"recent {m['recent_msgs']}  {m['chat'][:30]}"
            )


if __name__ == "__main__":
    analyze_cross_tier_movement()

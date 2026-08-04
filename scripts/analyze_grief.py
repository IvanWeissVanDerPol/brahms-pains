#!/usr/bin/env python3
"""Hat 31 - Grief & Loss analysis: abandoned high-volume contacts."""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH/wa_messages/_ANALYSIS"


def analyze_grief():
    """Analyze abandoned tier1/tier2 contacts as grief signals."""
    rec = json.loads((ANALYSIS / "recency_heatmap.json").read_text())
    tp = json.loads((ANALYSIS / "time_patterns.json").read_text())
    init = json.loads((ANALYSIS / "initiator_analysis.json").read_text())

    abandoned = []
    for chat, info in rec["per_chat"].items():
        if (
            info["tier"] in ("tier1_deep", "tier2_core")
            and info["days_since_last"] > 365
            and info["total_msgs"] >= 100
        ):
            # Get additional data
            tp_info = tp["per_contact"].get(chat, {})
            init_info = init["per_chat"].get(chat, {})

            abandoned.append(
                {
                    "chat": chat,
                    "tier": info["tier"],
                    "total_msgs": info["total_msgs"],
                    "days_since_last": info["days_since_last"],
                    "last_message_date": info["last_message_date"],
                    "late_night_ratio": tp_info.get("late_night_ratio", 0),
                    "ivan_ratio": tp_info.get("ivan_ratio", 0),
                    "ivan_start_ratio": init_info.get("ivan_start_ratio", 0),
                    "max_streak_days": init_info.get("max_streak_days", 0),
                }
            )

    abandoned.sort(key=lambda x: -x["days_since_last"])

    # Categorize by contact type
    family_keywords = [
        "mom",
        "dad",
        "kiki",
        "sister",
        "mama",
        "papa",
        "kyrian",
        "luana",
        "prima",
        "family",
        "poli",
    ]
    work_keywords = ["cliente", "fpuna", "iin_", "exam", "trabajo", "voluntari", "ci24", "polo"]
    friend_keywords = ["amiga", "amigo", "swinger", "fria"]
    romantic_keywords = ["ex", "love", "love", "_n_"]

    categorized = {"family": [], "work": [], "friend": [], "romantic": [], "other": []}

    for item in abandoned:
        chat_lower = item["chat"].lower()
        if any(k in chat_lower for k in romantic_keywords):
            categorized["romantic"].append(item)
        elif any(k in chat_lower for k in family_keywords):
            categorized["family"].append(item)
        elif any(k in chat_lower for k in work_keywords):
            categorized["work"].append(item)
        elif any(k in chat_lower for k in friend_keywords):
            categorized["friend"].append(item)
        else:
            categorized["other"].append(item)

    # Calculate loss characteristics
    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_abandoned": len(abandoned),
        "by_category": {k: len(v) for k, v in categorized.items()},
        "abandoned_contacts": abandoned,
        "category_breakdown": categorized,
    }

    out = ANALYSIS / "grief_analysis.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"Wrote {out.relative_to(REPO)}")

    # Print findings
    print("\n=== Hat 31: Grief & Loss Analysis ===\n")
    print(f"Total abandoned tier1/tier2: {len(abandoned)}")
    print("By category:")
    for k, v in categorized.items():
        if v:
            print(f"  {k}: {len(v)}")

    print("\n=== ROMANTIC ABANDONMENTS (highest grief signal) ===")
    for item in categorized["romantic"]:
        print(
            f"  {item['days_since_last']:>5}d ago  {item['tier']:<12}  {item['total_msgs']:>5} msgs  "
            f"Late {item['late_night_ratio']:.1%} | Ivan {item['ivan_ratio']:.1%}  {item['chat'][:35]}"
        )

    print("\n=== FAMILY ABANDONMENTS ===")
    for item in categorized["family"]:
        print(
            f"  {item['days_since_last']:>5}d ago  {item['tier']:<12}  {item['total_msgs']:>5} msgs  {item['chat'][:35]}"
        )

    print("\n=== FRIENDSHIP ABANDONMENTS ===")
    for item in categorized["friend"]:
        print(
            f"  {item['days_since_last']:>5}d ago  {item['tier']:<12}  {item['total_msgs']:>5} msgs  {item['chat'][:35]}"
        )

    # Compute clinical metrics
    print("\n=== Clinical Metrics ===")
    total_msgs = sum(a["total_msgs"] for a in abandoned)
    total_streak_days = sum(a["max_streak_days"] for a in abandoned)
    avg_days_since = sum(a["days_since_last"] for a in abandoned) / len(abandoned)

    print(f"  Total msgs in abandoned chats: {total_msgs:,}")
    print(f"  Combined max streaks: {total_streak_days:,} days")
    print(f"  Average abandonment time: {avg_days_since:.0f} days ({avg_days_since/365:.1f} years)")
    print(f"  Longest abandonment: {max(a['days_since_last'] for a in abandoned)} days")

    # Identify closure patterns
    print("\n=== Closure Patterns ===")
    # Where Ivan initiated the abandonment (high Ivan ratio + abandonment)
    ivan_initiated = [a for a in abandoned if a["ivan_ratio"] > 0.55]
    them_initiated = [a for a in abandoned if a["ivan_ratio"] < 0.45]

    print(f"  Ivan-initiated abandonments (Ivan ratio > 55%): {len(ivan_initiated)}")
    print(f"  Them-initiated abandonments (Ivan ratio < 45%): {len(them_initiated)}")
    print(f"  Balanced abandonments: {len(abandoned) - len(ivan_initiated) - len(them_initiated)}")


if __name__ == "__main__":
    analyze_grief()

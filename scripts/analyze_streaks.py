#!/usr/bin/env python3
"""Streak/consistency analysis (Hat 1)."""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH/wa_messages"
ANALYSIS = WA / "_ANALYSIS"


def analyze_streaks():
    """Analyze longest consecutive daily activity streaks per chat."""
    by_chat = {}

    tiers = [
        "tier1_deep",
        "tier2_core",
        "tier3_extended",
        "tier4_groups",
        "untiered_personal",
        "other_lid",
    ]

    for tier in tiers:
        d = WA / tier
        if not d.exists():
            continue
        for chat in d.iterdir():
            if not chat.is_dir():
                continue
            mf = chat / "messages.json"
            if not mf.exists():
                continue
            try:
                data = json.loads(mf.read_text())
            except:
                continue

            msgs = data.get("messages", [])
            if not msgs:
                continue

            valid_msgs = [m for m in msgs if isinstance(m, dict) and m.get("ts_ms")]
            if len(valid_msgs) < 50:
                continue

            chat_name = chat.name

            # Calculate daily activity streak
            active_days = set()
            for m in valid_msgs:
                ts = m.get("ts_ms", 0)
                if ts:
                    dt = datetime.fromtimestamp(ts / 1000).date()
                    active_days.add(dt)

            sorted_days = sorted(active_days)
            if not sorted_days:
                continue

            # Find longest streak
            max_streak = 1
            current_streak = 1
            streak_start = sorted_days[0]
            max_streak_start = sorted_days[0]
            max_streak_end = sorted_days[0]

            for i in range(1, len(sorted_days)):
                delta = (sorted_days[i] - sorted_days[i - 1]).days
                if delta == 1:
                    current_streak += 1
                    if current_streak > max_streak:
                        max_streak = current_streak
                        max_streak_start = streak_start
                        max_streak_end = sorted_days[i]
                else:
                    current_streak = 1
                    streak_start = sorted_days[i]

            # Active months
            months_active = set()
            for d in active_days:
                months_active.add(f"{d.year}-{d.month:02}")

            # ivan ratio
            ivan_msgs = sum(1 for m in valid_msgs if m.get("from_me"))
            ivan_ratio = ivan_msgs / len(valid_msgs) if valid_msgs else 0

            by_chat[chat_name] = {
                "tier": tier,
                "total_msgs": len(valid_msgs),
                "active_days": len(active_days),
                "active_months": len(months_active),
                "max_streak_days": max_streak,
                "streak_start": max_streak_start.isoformat(),
                "streak_end": max_streak_end.isoformat(),
                "streak_duration_months": (max_streak_end - max_streak_start).days / 30,
                "ivan_ratio": round(ivan_ratio, 3),
            }

    # Sort by streak
    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_chats_analyzed": len(by_chat),
        "per_chat": by_chat,
    }

    out = ANALYSIS / "streak_analysis.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"Wrote {out.relative_to(REPO)}")

    print("\n=== Streak/Consistency Analysis ===")
    print(f"Total analyzed: {len(by_chat)}")

    print("\nTop 25 longest streaks (most consistent engagement):")
    for c, info in sorted(by_chat.items(), key=lambda x: -x[1]["max_streak_days"])[:25]:
        if info["max_streak_days"] > 30:
            print(
                f"  {info['max_streak_days']:>4}d streak  {info['total_msgs']:>5} msgs  "
                f"Ivan {info['ivan_ratio']:.0%}  {c[:40]}"
            )


if __name__ == "__main__":
    analyze_streaks()

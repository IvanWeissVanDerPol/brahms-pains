#!/usr/bin/env python3
"""Group chat participation analysis (Hat 14, 16)."""

from __future__ import annotations

import json
from pathlib import Path
from collections import Counter
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH/wa_messages"
ANALYSIS = WA / "_ANALYSIS"


def analyze_group_participation():
    """Analyze Ivan's participation in 158 group chats."""
    by_group = {}

    tier = "tier4_groups"
    d = WA / tier
    if not d.exists():
        return

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

        chat_name = chat.name

        # Calculate Ivan's participation
        total = len(msgs)
        ivan_msgs = sum(1 for m in msgs if isinstance(m, dict) and m.get("from_me"))

        # Days active
        valid_msgs = [m for m in msgs if isinstance(m, dict) and m.get("ts_ms")]
        if not valid_msgs:
            continue

        # Get unique other participants (sender_jid)
        other_participants = set()
        for m in valid_msgs:
            sender = m.get("sender_jid")
            if sender and not m.get("from_me"):
                other_participants.add(sender)

        days_active = set()
        for m in valid_msgs:
            ts_ms = m.get("ts_ms", 0)
            if ts_ms:
                dt = datetime.fromtimestamp(ts_ms / 1000)
                days_active.add(dt.date())

        first_ts = min(m.get("ts_ms", 0) for m in valid_msgs)
        last_ts = max(m.get("ts_ms", 0) for m in valid_msgs)
        first_date = datetime.fromtimestamp(first_ts / 1000).date() if first_ts else None
        last_date = datetime.fromtimestamp(last_ts / 1000).date() if last_ts else None

        # Categorize participation
        ivan_ratio = ivan_msgs / total if total > 0 else 0
        msgs_per_day = ivan_msgs / len(days_active) if days_active else 0

        if ivan_ratio == 0:
            category = "LURKER"
        elif ivan_ratio < 0.05:
            category = "PASSIVE"
        elif ivan_ratio < 0.15:
            category = "OCCASIONAL"
        elif ivan_ratio < 0.3:
            category = "REGULAR"
        else:
            category = "ACTIVE"

        by_group[chat_name] = {
            "total_msgs": total,
            "ivan_msgs": ivan_msgs,
            "ivan_ratio": round(ivan_ratio, 4),
            "other_participants": len(other_participants),
            "msgs_per_day": round(msgs_per_day, 2),
            "days_active": len(days_active),
            "first_date": first_date.isoformat() if first_date else None,
            "last_date": last_date.isoformat() if last_date else None,
            "category": category,
        }

    # Categorize summary
    by_category = Counter(g["category"] for g in by_group.values())

    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_groups_analyzed": len(by_group),
        "category_distribution": dict(by_category),
        "per_group": by_group,
    }

    out = ANALYSIS / "group_participation.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"Wrote {out.relative_to(REPO)}")

    print("\n=== Group Chat Participation ===")
    print(f"Total groups: {len(by_group)}")
    print("\nCategory distribution:")
    for cat, count in sorted(by_category.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

    print("\nTop 10 LURKER groups (Ivan = 0 msgs):")
    lurkers = [(c, info) for c, info in by_group.items() if info["category"] == "LURKER"]
    for c, info in sorted(lurkers, key=lambda x: -x[1]["total_msgs"])[:10]:
        print(f"  {info['total_msgs']:>5} msgs  {info['other_participants']:>3} others  {c[:35]}")

    print("\nTop 10 ACTIVE groups (Ivan most engaged):")
    active = [(c, info) for c, info in by_group.items() if info["category"] == "ACTIVE"]
    for c, info in sorted(active, key=lambda x: -x[1]["ivan_msgs"])[:10]:
        print(
            f"  Ivan {info['ivan_msgs']:>5}/{info['total_msgs']:>5} ({info['ivan_ratio']:.1%})  "
            f"{info['msgs_per_day']:.1f} m/day  {c[:30]}"
        )


if __name__ == "__main__":
    analyze_group_participation()

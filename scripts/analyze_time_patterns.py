#!/usr/bin/env python3
"""Time-of-day patterns per contact (feeds Hat 1, 6, 22)."""
from __future__ import annotations

import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH/wa_messages"
ANALYSIS = WA / "_ANALYSIS"

def analyze_time_patterns():
    """For each contact, calculate hour-of-day distribution."""
    by_hour = defaultdict(lambda: Counter())
    by_dow = defaultdict(lambda: Counter())  # Day of week
    by_hour_ivan = defaultdict(Counter)  # Only Ivan's messages
    by_hour_them = defaultdict(Counter)  # Only their messages

    total_chats = 0
    total_msgs = 0

    tiers = ["tier1_deep", "tier2_core", "tier3_extended", "tier4_groups", "untiered_personal", "other_lid"]

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

            chat_name = chat.name
            total_chats += 1
            total_msgs += len(msgs)

            for m in msgs:
                if not isinstance(m, dict):
                    continue
                ts = m.get("ts_iso")
                if not ts:
                    continue
                try:
                    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                except:
                    continue

                hour = dt.hour
                dow = dt.strftime("%A")

                by_hour[chat_name][hour] += 1
                by_dow[chat_name][dow] += 1

                if m.get("from_me"):
                    by_hour_ivan[chat_name][hour] += 1
                else:
                    by_hour_them[chat_name][hour] += 1

    # Top-level summary
    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_chats_analyzed": total_chats,
        "total_messages_analyzed": total_msgs,
        "by_hour_overall": {},
        "by_dow_overall": {},
        "by_hour_ivan_overall": {},
        "by_hour_them_overall": {},
        "per_contact": {},
    }

    # Aggregate across all chats
    all_hours = Counter()
    all_dow = Counter()
    ivan_hours = Counter()
    them_hours = Counter()

    for chat, hours in by_hour.items():
        all_hours.update(hours)
        n = sum(by_dow[chat].values())
        all_dow.update(by_dow[chat])
        ivan_hours.update(by_hour_ivan[chat])
        them_hours.update(by_hour_them[chat])

        # Find peak hour for this contact
        peak_hour = max(hours.items(), key=lambda x: x[1])[0] if hours else None
        peak_dow = max(by_dow[chat].items(), key=lambda x: x[1])[0] if by_dow[chat] else None

        # Late night ratio (22:00-04:00)
        late = sum(hours.get(h, 0) for h in range(22, 24)) + sum(hours.get(h, 0) for h in range(0, 4))
        total = sum(hours.values())
        late_ratio = late / total if total > 0 else 0

        # Ivan initiator ratio
        ivan_total = sum(by_hour_ivan[chat].values())
        them_total = sum(by_hour_them[chat].values())
        ivan_ratio = ivan_total / (ivan_total + them_total) if (ivan_total + them_total) > 0 else 0

        summary["per_contact"][chat] = {
            "total_msgs": total,
            "peak_hour": peak_hour,
            "peak_dow": peak_dow,
            "late_night_ratio": round(late_ratio, 3),
            "ivan_ratio": round(ivan_ratio, 3),
            "ivan_msgs": ivan_total,
            "them_msgs": them_total,
        }

    summary["by_hour_overall"] = dict(all_hours)
    summary["by_dow_overall"] = dict(all_dow)
    summary["by_hour_ivan_overall"] = dict(ivan_hours)
    summary["by_hour_them_overall"] = dict(them_hours)

    # Save
    out = ANALYSIS / "time_patterns.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"Wrote {out.relative_to(REPO)}")

    # Print summary
    print(f"\n=== Time patterns summary ===")
    print(f"  Chats analyzed: {total_chats}")
    print(f"  Messages analyzed: {total_msgs:,}")
    print(f"\nPeak hour overall: {max(all_hours.items(), key=lambda x: x[1])}")
    print(f"Peak day of week: {max(all_dow.items(), key=lambda x: x[1])}")

    # Top 10 late-night contacts
    late_sorted = sorted(
        summary["per_contact"].items(),
        key=lambda x: x[1]["late_night_ratio"],
        reverse=True
    )[:10]
    print(f"\nTop 10 late-night contacts (22:00-04:00):")
    for chat, info in late_sorted:
        print(f"  {info['late_night_ratio']:.1%}  {chat[:40]:<40} ({info['total_msgs']} msgs)")

    # Top 10 Ivan-initiator contacts (Ivan chases them)
    ivan_sorted = sorted(
        summary["per_contact"].items(),
        key=lambda x: x[1]["ivan_ratio"],
        reverse=True
    )[:10]
    print(f"\nTop 10 Ivan-initiator contacts (Ivan chases them):")
    for chat, info in ivan_sorted:
        print(f"  {info['ivan_ratio']:.1%}  Ivan/{info['ivan_msgs']}/{info['them_msgs']}  {chat[:30]}")

    return summary


if __name__ == "__main__":
    analyze_time_patterns()
#!/usr/bin/env python3
"""Conversation repair pattern detection (Hat 1, 4)."""
from __future__ import annotations

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone, timedelta

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH/wa_messages"
ANALYSIS = WA / "_ANALYSIS"


def detect_repair_patterns():
    """Find post-gap outreach patterns (conversation repair)."""
    repair_events = []
    gaps_detected = []

    tiers = ["tier1_deep", "tier2_core", "tier3_extended", "untiered_personal", "other_lid"]

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

            # Sort by timestamp
            valid_msgs = [m for m in msgs if isinstance(m, dict) and m.get("ts_ms")]
            valid_msgs.sort(key=lambda x: x.get("ts_ms", 0))

            if len(valid_msgs) < 10:
                continue

            # Find gaps > 7 days
            for i in range(1, len(valid_msgs)):
                prev = valid_msgs[i-1]
                curr = valid_msgs[i]
                prev_ts = prev.get("ts_ms", 0)
                curr_ts = curr.get("ts_ms", 0)

                if not prev_ts or not curr_ts:
                    continue

                gap_ms = curr_ts - prev_ts
                gap_days = gap_ms / (1000 * 3600 * 24)

                # Detect "repair": gap > 7 days followed by Ivan initiating
                if gap_days > 7:
                    # Was the message after the gap from Ivan?
                    is_ivan_repair = curr.get("from_me", False)

                    gaps_detected.append({
                        "chat": chat_name,
                        "tier": tier,
                        "gap_days": round(gap_days, 1),
                        "from_ivan": is_ivan_repair,
                        "gap_start": datetime.fromtimestamp(prev_ts / 1000, tz=timezone.utc).isoformat(),
                        "gap_end": datetime.fromtimestamp(curr_ts / 1000, tz=timezone.utc).isoformat(),
                    })

                    if is_ivan_repair:
                        repair_events.append({
                            "chat": chat_name,
                            "tier": tier,
                            "gap_days": round(gap_days, 1),
                            "gap_start": datetime.fromtimestamp(prev_ts / 1000, tz=timezone.utc).isoformat(),
                            "gap_end": datetime.fromtimestamp(curr_ts / 1000, tz=timezone.utc).isoformat(),
                        })

    # Calculate stats per chat
    by_chat = defaultdict(lambda: {"total_gaps": 0, "ivan_repairs": 0, "them_repairs": 0, "max_gap": 0, "total_gap_days": 0})

    for g in gaps_detected:
        chat = g["chat"]
        by_chat[chat]["total_gaps"] += 1
        by_chat[chat]["total_gap_days"] += g["gap_days"]
        by_chat[chat]["max_gap"] = max(by_chat[chat]["max_gap"], int(gap_days))
        if g["from_ivan"]:
            by_chat[chat]["ivan_repairs"] += 1
        else:
            by_chat[chat]["them_repairs"] += 1

    # Calculate repair ratio per chat
    for chat in by_chat:
        total = by_chat[chat]["total_gaps"]
        if total > 0:
            by_chat[chat]["ivan_repair_ratio"] = round(by_chat[chat]["ivan_repairs"] / total, 3)
        else:
            by_chat[chat]["ivan_repair_ratio"] = 0

    # Build summary
    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_gaps_detected": len(gaps_detected),
        "total_repair_events": len(repair_events),
        "per_chat_repair": dict(by_chat),
        "all_gaps_sample": gaps_detected[:50],
        "all_repairs_sample": repair_events[:30],
    }

    out = ANALYSIS / "conversation_repair.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"Wrote {out.relative_to(REPO)}")

    # Print findings
    print(f"\n=== Conversation Repair Analysis ===")
    print(f"Total gaps >7 days detected: {len(gaps_detected)}")
    print(f"Repair events (Ivan initiated after gap): {len(repair_events)}")

    # Top chats by total gaps
    print(f"\n=== Top 15 chats by gap frequency ===")
    sorted_chats = sorted(by_chat.items(), key=lambda x: -x[1]["total_gaps"])[:15]
    for chat, stats in sorted_chats:
        print(f"  {stats['total_gaps']:>3} gaps  Ivan repair {stats['ivan_repair_ratio']:.1%}  "
              f"Max gap {stats['max_gap']:.0f}d  {chat[:40]}")

    # Top Ivan-repair chats (Ivan reaches out after silence)
    print(f"\n=== Top 15 chats where Ivan repairs (reaches out after gap) ===")
    sorted_repairs = sorted(by_chat.items(), key=lambda x: -x[1]["ivan_repairs"])[:15]
    for chat, stats in sorted_repairs:
        if stats["ivan_repairs"] > 0:
            print(f"  {stats['ivan_repairs']:>3} repairs / {stats['total_gaps']:>3} gaps  "
                  f"({stats['ivan_repair_ratio']:.1%})  {chat[:35]}")

    # Largest gaps
    print(f"\n=== Top 15 largest single gaps ===")
    largest = sorted(gaps_detected, key=lambda x: -x["gap_days"])[:15]
    for g in largest:
        direction = "Ivan →" if g["from_ivan"] else "← Them"
        print(f"  {g['gap_days']:>5.0f}d  {direction}  {g['tier']:<15}  {g['chat'][:30]}")


if __name__ == "__main__":
    detect_repair_patterns()
#!/usr/bin/env python3
"""Initiator ratios analysis (feeds Hat 1, 4)."""

from __future__ import annotations

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH/wa_messages"
ANALYSIS = WA / "_ANALYSIS"


def analyze_initiators():
    """Calculate initiator ratios + conversation start patterns."""
    by_chat = {}
    by_tier = defaultdict(list)

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
            if len(msgs) < 5:
                continue

            chat_name = chat.name

            # 1. Initiator ratio (overall)
            ivan_msgs = sum(1 for m in msgs if isinstance(m, dict) and m.get("from_me"))
            them_msgs = len(msgs) - ivan_msgs
            ivan_ratio = ivan_msgs / len(msgs) if msgs else 0

            # 2. Conversation-start detection (Ivan starts the chat?)
            # Conversation = gap > 4 hours
            conversations = []
            current_conv = []
            last_ts = None

            for m in sorted(msgs, key=lambda x: x.get("ts_ms", 0) if isinstance(x, dict) else 0):
                if not isinstance(m, dict):
                    continue
                ts = m.get("ts_ms", 0)
                if last_ts and (ts - last_ts) > 4 * 3600 * 1000:  # 4 hours
                    if current_conv:
                        conversations.append(current_conv)
                    current_conv = []
                current_conv.append(m)
                last_ts = ts
            if current_conv:
                conversations.append(current_conv)

            # Who started each conversation?
            ivan_starts = 0
            them_starts = 0
            for conv in conversations:
                if conv and isinstance(conv[0], dict):
                    if conv[0].get("from_me"):
                        ivan_starts += 1
                    else:
                        them_starts += 1

            total_convs = ivan_starts + them_starts
            ivan_start_ratio = ivan_starts / total_convs if total_convs else 0

            # 3. Reciprocity (response time)
            response_times = []
            for i, m in enumerate(msgs[1:], 1):
                if not isinstance(m, dict):
                    continue
                if i > 0 and isinstance(msgs[i - 1], dict):
                    prev = msgs[i - 1]
                    if (
                        prev.get("from_me") != m.get("from_me")
                        and m.get("ts_ms")
                        and prev.get("ts_ms")
                    ):
                        rt = m["ts_ms"] - prev["ts_ms"]
                        if 0 < rt < 24 * 3600 * 1000:  # within 24h
                            response_times.append(rt)

            if response_times:
                avg_rt = sum(response_times) / len(response_times)
                median_rt = sorted(response_times)[len(response_times) // 2]
            else:
                avg_rt = median_rt = None

            # 4. Streak (max consecutive days with messages)
            days = set()
            for m in msgs:
                if isinstance(m, dict):
                    ts_iso = m.get("ts_iso")
                    if ts_iso:
                        try:
                            dt = datetime.fromisoformat(ts_iso.replace("Z", "+00:00"))
                            days.add(dt.date())
                        except:
                            pass

            days_sorted = sorted(days)
            max_streak = 0
            current_streak = 1
            if days_sorted:
                for i in range(1, len(days_sorted)):
                    if (days_sorted[i] - days_sorted[i - 1]).days == 1:
                        current_streak += 1
                    else:
                        max_streak = max(max_streak, current_streak)
                        current_streak = 1
                max_streak = max(max_streak, current_streak)

            # 5. Last message recency
            last_ts = max((m.get("ts_ms", 0) for m in msgs if isinstance(m, dict)), default=0)
            if last_ts:
                last_dt = datetime.fromtimestamp(last_ts / 1000)
                days_since = (datetime.now() - last_dt.replace(tzinfo=None)).days
            else:
                days_since = None

            by_chat[chat_name] = {
                "tier": tier,
                "total_msgs": len(msgs),
                "ivan_msgs": ivan_msgs,
                "them_msgs": them_msgs,
                "ivan_ratio": round(ivan_ratio, 3),
                "conversations": total_convs,
                "ivan_starts": ivan_starts,
                "them_starts": them_starts,
                "ivan_start_ratio": round(ivan_start_ratio, 3),
                "avg_response_time_ms": int(avg_rt) if avg_rt else None,
                "median_response_time_ms": int(median_rt) if median_rt else None,
                "max_streak_days": max_streak,
                "days_since_last": days_since,
            }
            by_tier[tier].append(by_chat[chat_name])

    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_chats_analyzed": len(by_chat),
        "by_tier": {tier: len(items) for tier, items in by_tier.items()},
        "per_chat": by_chat,
    }

    out = ANALYSIS / "initiator_analysis.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"Wrote {out.relative_to(REPO)}")

    # Print summary
    print("\n=== Initiator Analysis Summary ===")
    print(f"Total chats: {len(by_chat)}")
    print(f"Total conversations: {sum(c['conversations'] for c in by_chat.values()):,}")

    # Top 10 Ivan-chases contacts
    ivan_chasers = sorted(
        [
            (c, info)
            for c, info in by_chat.items()
            if info["total_msgs"] >= 50 and info["ivan_start_ratio"] > 0.7
        ],
        key=lambda x: -x[1]["ivan_start_ratio"],
    )[:15]
    print("\nTop 15 Ivan-initiators (Ivan starts >70% of conversations):")
    for c, info in ivan_chasers:
        print(
            f"  {info['ivan_start_ratio']:.1%}  Ivan {info['ivan_starts']}/{info['them_starts']} conv  {c[:35]}"
        )

    # Top 10 they-chase
    them_chasers = sorted(
        [
            (c, info)
            for c, info in by_chat.items()
            if info["total_msgs"] >= 50
            and info["ivan_start_ratio"] < 0.3
            and info["them_starts"] > 0
        ],
        key=lambda x: x[1]["ivan_start_ratio"],
    )[:15]
    print("\nTop 15 they-initiators (Ivan starts <30%):")
    for c, info in them_chasers:
        print(
            f"  {info['ivan_start_ratio']:.1%}  Ivan {info['ivan_starts']}/{info['them_starts']} conv  {c[:35]}"
        )

    # Top 10 fastest Ivan responses
    fast_responders = sorted(
        [
            (c, info)
            for c, info in by_chat.items()
            if info["median_response_time_ms"] is not None and info["total_msgs"] >= 30
        ],
        key=lambda x: x[1]["median_response_time_ms"],
    )[:10]
    print("\nTop 10 fastest responses (Ivan's median):")
    for c, info in fast_responders:
        rt = info["median_response_time_ms"] / 1000  # seconds
        rt_min = rt / 60
        print(
            f"  {rt_min:.1f}min median  Ivan conv {info['ivan_starts']}/{info['them_starts']}  {c[:30]}"
        )

    # Top 10 longest streaks
    streaks = sorted(
        [(c, info) for c, info in by_chat.items() if info["max_streak_days"] > 0],
        key=lambda x: -x[1]["max_streak_days"],
    )[:10]
    print("\nTop 10 longest message streaks:")
    for c, info in streaks:
        print(f"  {info['max_streak_days']:>4} days  {c[:35]}")


if __name__ == "__main__":
    analyze_initiators()

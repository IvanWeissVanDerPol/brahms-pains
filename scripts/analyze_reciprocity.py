#!/usr/bin/env python3
"""Reciprocity / response-time analysis (Hat 1, 14)."""
from __future__ import annotations

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH/wa_messages"
ANALYSIS = WA / "_ANALYSIS"


def analyze_reciprocity():
    """Calculate response times and reciprocity per chat."""
    by_chat = {}

    tiers = ["tier1_deep", "tier2_core", "tier3_extended", "tier4_groups",
             "untiered_personal", "other_lid"]

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

            # Calculate response times: time between consecutive messages from different sides
            response_times_ivan = []  # Time for Ivan to respond to them
            response_times_them = []  # Time for them to respond to Ivan
            conversation_gaps = []  # All gaps > 5 min

            last_msg = None
            for m in valid_msgs:
                if last_msg is None:
                    last_msg = m
                    continue

                ts_curr = m.get("ts_ms", 0)
                ts_last = last_msg.get("ts_ms", 0)
                if not ts_curr or not ts_last:
                    last_msg = m
                    continue

                gap = ts_curr - ts_last
                gap_min = gap / (1000 * 60)

                # Only count if it's a back-and-forth (different sender)
                last_from_me = last_msg.get("from_me", False)
                curr_from_me = m.get("from_me", False)

                if last_from_me != curr_from_me and gap_min > 0.5 and gap_min < 24 * 60:
                    if curr_from_me:  # Ivan responding
                        response_times_ivan.append(gap_min)
                    else:  # They responding
                        response_times_them.append(gap_min)

                if gap_min > 5:
                    conversation_gaps.append(gap_min)

                last_msg = m

            # Calculate stats
            def stats(times):
                if not times:
                    return None
                times_sorted = sorted(times)
                return {
                    "count": len(times),
                    "mean_min": round(sum(times) / len(times), 1),
                    "median_min": round(times_sorted[len(times_sorted) // 2], 1),
                    "p90_min": round(times_sorted[int(len(times_sorted) * 0.9)], 1),
                    "min_min": round(min(times), 1),
                    "max_min": round(max(times), 1),
                }

            by_chat[chat_name] = {
                "tier": tier,
                "total_msgs": len(valid_msgs),
                "ivan_response_stats": stats(response_times_ivan),
                "them_response_stats": stats(response_times_them),
                "gap_count": len(conversation_gaps),
                "total_gap_minutes": int(sum(conversation_gaps)),
                "longest_gap_min": int(max(conversation_gaps)) if conversation_gaps else 0,
            }

    # Categorize
    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_chats_analyzed": len(by_chat),
        "per_chat": by_chat,
    }

    out = ANALYSIS / "reciprocity_analysis.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"Wrote {out.relative_to(REPO)}")

    print(f"\n=== Reciprocity / Response-Time Analysis ===")
    print(f"Total chats analyzed: {len(by_chat)}")

    # Fastest responders
    print(f"\nTop 15 fastest Ivan responders:")
    fast_ivan = sorted(
        [(c, info) for c, info in by_chat.items()
         if info["ivan_response_stats"] and info["ivan_response_stats"]["median_min"] > 0],
        key=lambda x: x[1]["ivan_response_stats"]["median_min"]
    )[:15]
    for c, info in fast_ivan:
        if info["ivan_response_stats"]:
            print(f"  {info['ivan_response_stats']['median_min']:>5.1f}min  Ivan {info['total_msgs']:>5} msgs  {c[:40]}")

    print(f"\nTop 15 fastest THEM responders (Ivan triggers quick replies):")
    fast_them = sorted(
        [(c, info) for c, info in by_chat.items()
         if info["them_response_stats"] and info["them_response_stats"]["median_min"] > 0],
        key=lambda x: x[1]["them_response_stats"]["median_min"]
    )[:15]
    for c, info in fast_them:
        if info["them_response_stats"]:
            print(f"  {info['them_response_stats']['median_min']:>5.1f}min  {info['total_msgs']:>5} msgs  {c[:40]}")

    print(f"\nTop 10 longest gaps in conversations:")
    long_gaps = sorted(by_chat.items(), key=lambda x: -x[1]["longest_gap_min"])[:10]
    for c, info in long_gaps:
        if info["longest_gap_min"] > 0:
            days = info["longest_gap_min"] / (60 * 24)
            print(f"  {days:>6.1f}d gap  {info['gap_count']:>3} gaps  {info['total_msgs']:>5} msgs  {c[:40]}")


if __name__ == "__main__":
    analyze_reciprocity()
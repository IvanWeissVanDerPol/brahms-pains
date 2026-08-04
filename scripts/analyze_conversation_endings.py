#!/usr/bin/env python3
"""Conversation ending patterns analysis (Hat 14, 22)."""

from __future__ import annotations

import json
from pathlib import Path
from collections import Counter
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH/wa_messages"
ANALYSIS = WA / "_ANALYSIS"


def analyze_ending_patterns():
    """Analyze how conversations end - last 7 days of activity."""
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
            if len(valid_msgs) < 20:
                continue

            valid_msgs.sort(key=lambda x: x.get("ts_ms", 0))
            chat_name = chat.name

            # Get last 30 days of activity
            last_ts = max(m.get("ts_ms", 0) for m in valid_msgs)
            first_ts = min(m.get("ts_ms", 0) for m in valid_msgs)
            cutoff_30d = last_ts - (30 * 24 * 60 * 60 * 1000)

            last_30d = [m for m in valid_msgs if m.get("ts_ms", 0) >= cutoff_30d]
            last_7d = [
                m for m in valid_msgs if m.get("ts_ms", 0) >= last_ts - (7 * 24 * 60 * 60 * 1000)
            ]
            last_1d = [
                m for m in valid_msgs if m.get("ts_ms", 0) >= last_ts - (1 * 24 * 60 * 60 * 1000)
            ]

            # Days active in last 30d
            days_active_30d = set()
            days_active_7d = set()
            for m in last_30d:
                dt = datetime.fromtimestamp(m["ts_ms"] / 1000).date()
                days_active_30d.add(dt)
            for m in last_7d:
                dt = datetime.fromtimestamp(m["ts_ms"] / 1000).date()
                days_active_7d.add(dt)

            # Last message details
            last_msg = valid_msgs[-1]
            last_from_me = last_msg.get("from_me", False)
            last_text = (last_msg.get("text") or "")[:50]

            # Calculate engagement decline
            # Compare last 30d average to first 30d average
            if first_ts < last_ts - (60 * 24 * 60 * 60 * 1000):  # At least 60 days history
                first_30d = [
                    m
                    for m in valid_msgs
                    if m.get("ts_ms", 0) < first_ts + (30 * 24 * 60 * 60 * 1000)
                ]
                early_avg = len(first_30d) / 30 if first_30d else 0
                late_avg = len(last_30d) / 30 if last_30d else 0

                if early_avg > 0:
                    engagement_change = (late_avg - early_avg) / early_avg
                else:
                    engagement_change = 0
            else:
                engagement_change = 0
                early_avg = 0
                late_avg = len(last_30d) / 30 if last_30d else 0

            # Calculate final-spike (sudden activity before going silent)
            # Compare last 7d to last 30d average
            avg_30d_per_day = len(last_30d) / 30 if last_30d else 0
            avg_7d_per_day = len(last_7d) / 7 if last_7d else 0

            if avg_30d_per_day > 0:
                spike_ratio = avg_7d_per_day / avg_30d_per_day
            else:
                spike_ratio = 0

            # Ending pattern
            if avg_7d_per_day == 0:
                if avg_30d_per_day > 0:
                    ending = "QUIET_END"  # Was active, now quiet
                else:
                    ending = "DORMANT"  # Always been quiet
            elif spike_ratio > 2:
                ending = "FINAL_SPIKE"  # Sudden activity before silence
            elif spike_ratio > 1.5:
                ending = "REVIVAL"  # Picking up
            elif avg_7d_per_day < avg_30d_per_day * 0.3:
                ending = "FADING"  # Was active, dropping
            else:
                ending = "STABLE_ACTIVE"

            by_chat[chat_name] = {
                "tier": tier,
                "total_msgs": len(valid_msgs),
                "last_30d_msgs": len(last_30d),
                "last_7d_msgs": len(last_7d),
                "last_1d_msgs": len(last_1d),
                "days_active_30d": len(days_active_30d),
                "days_active_7d": len(days_active_7d),
                "last_msg_from_ivan": last_from_me,
                "last_msg_preview": last_text,
                "engagement_change": round(engagement_change, 3),
                "early_avg_per_day": round(early_avg, 2),
                "late_avg_per_day": round(late_avg, 2),
                "spike_ratio": round(spike_ratio, 2),
                "ending_pattern": ending,
            }

    # Categorize
    ending_dist = Counter(c["ending_pattern"] for c in by_chat.values())

    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_chats_analyzed": len(by_chat),
        "ending_distribution": dict(ending_dist),
        "per_chat": by_chat,
    }

    out = ANALYSIS / "conversation_endings.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"Wrote {out.relative_to(REPO)}")

    print("\n=== Conversation Ending Patterns ===")
    print(f"Total analyzed: {len(by_chat)}")
    print("\nEnding distribution:")
    for pattern, count in sorted(ending_dist.items(), key=lambda x: -x[1]):
        print(f"  {pattern}: {count}")

    # Final spikes (dramatic last activity)
    print("\nTop 15 FINAL_SPIKE conversations:")
    spikes = [(c, info) for c, info in by_chat.items() if info["ending_pattern"] == "FINAL_SPIKE"]
    for c, info in sorted(spikes, key=lambda x: -x[1]["last_7d_msgs"])[:15]:
        print(
            f"  spike ratio {info['spike_ratio']:>4.1f}x  "
            f"{info['last_7d_msgs']:>3} msgs in 7d  {c[:40]}"
        )

    # FADING
    print("\nTop 15 FADING conversations:")
    fading = [(c, info) for c, info in by_chat.items() if info["ending_pattern"] == "FADING"]
    for c, info in sorted(fading, key=lambda x: -x[1]["late_avg_per_day"])[:15]:
        print(
            f"  {info['late_avg_per_day']:>5.2f} m/day  {info['last_7d_msgs']:>3} msgs/7d  {c[:40]}"
        )

    # Last words - emotional content?
    print("\nLast messages from chats that ended QUIET (might be emotionally significant):")
    quiet = [(c, info) for c, info in by_chat.items() if info["ending_pattern"] == "QUIET_END"]
    for c, info in sorted(quiet, key=lambda x: -x[1]["total_msgs"])[:5]:
        print(f"  {info['last_msg_preview'][:80]}")


if __name__ == "__main__":
    analyze_ending_patterns()

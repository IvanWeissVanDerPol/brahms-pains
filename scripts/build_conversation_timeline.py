#!/usr/bin/env python3
"""Build complete conversation timeline + friend closeness history."""

from __future__ import annotations

import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH/wa_messages"
ANALYSIS = WA / "_ANALYSIS"


def build_timeline():
    """For each contact, build yearly timeline of closeness metrics."""
    by_chat_year = defaultdict(dict)

    tiers = [
        "tier1_deep",
        "tier2_core",
        "tier3_extended",
        "tier4_groups",
        "untiered_personal",
        "other_lid",
        "_dropped",
        "_newsletters",
    ]

    # Aggregate per chat, per year
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
            for m in msgs:
                if not isinstance(m, dict):
                    continue
                ts_ms = m.get("ts_ms", 0)
                if not ts_ms:
                    continue

                dt = datetime.fromtimestamp(ts_ms / 1000)
                year = str(dt.year)
                month = dt.strftime("%Y-%m")

                if year not in by_chat_year[chat_name]:
                    by_chat_year[chat_name][year] = {
                        "msgs": 0,
                        "ivan_msgs": 0,
                        "days_active": set(),
                        "first_message": None,
                        "last_message": None,
                    }
                bucket = by_chat_year[chat_name][year]
                bucket["msgs"] += 1
                if m.get("from_me"):
                    bucket["ivan_msgs"] += 1
                bucket["days_active"].add(dt.date())

                if bucket["first_message"] is None or ts_ms < bucket["first_message"]:
                    bucket["first_message"] = ts_ms
                if bucket["last_message"] is None or ts_ms > bucket["last_message"]:
                    bucket["last_message"] = ts_ms

    # Convert days_active sets to counts
    for chat, years in by_chat_year.items():
        for year, bucket in years.items():
            bucket["days_active"] = len(bucket["days_active"])

    # Build per-contact timeline
    timelines = {}
    for chat, years in by_chat_year.items():
        chat_timeline = []
        all_years = sorted(years.keys())

        # Get tier
        tier_for_chat = "unknown"
        for t in tiers:
            d = WA / t
            if d.exists() and (d / chat).exists():
                tier_for_chat = t
                break

        # Calculate closeness scores per year
        # Closeness = msgs * recency_factor * ivan_ratio_factor
        for year in all_years:
            b = years[year]
            ivan_ratio = b["ivan_msgs"] / b["msgs"] if b["msgs"] > 0 else 0

            # Engagement: msgs per active day
            engagement = b["msgs"] / b["days_active"] if b["days_active"] > 0 else 0

            # Closeness score: combines volume + consistency + reciprocity
            closeness = (
                b["msgs"] * 0.4
                + b["days_active"] * 1.0
                + (1 - abs(ivan_ratio - 0.5)) * b["msgs"] * 0.3
            )

            chat_timeline.append(
                {
                    "year": year,
                    "msgs": b["msgs"],
                    "ivan_msgs": b["ivan_msgs"],
                    "them_msgs": b["msgs"] - b["ivan_msgs"],
                    "days_active": b["days_active"],
                    "ivan_ratio": round(ivan_ratio, 3),
                    "engagement_per_day": round(engagement, 1),
                    "closeness_score": round(closeness, 1),
                    "first_message_ts": b["first_message"],
                    "last_message_ts": b["last_message"],
                }
            )

        timelines[chat] = {
            "tier": tier_for_chat,
            "years": all_years,
            "timeline": chat_timeline,
            "lifetime_msgs": sum(b["msgs"] for b in years.values()),
            "lifetime_years_active": len(all_years),
            "peak_year": (
                max(chat_timeline, key=lambda x: x["msgs"])["year"] if chat_timeline else None
            ),
            "first_year": all_years[0] if all_years else None,
            "last_year": all_years[-1] if all_years else None,
        }

    # Save
    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_chats": len(timelines),
        "year_range": ["2019", "2026"] if timelines else [],
        "per_chat": timelines,
    }

    out = ANALYSIS / "conversation_timeline.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"Wrote {out.relative_to(REPO)}")

    # Print summary insights
    print("\n=== Timeline Summary ===")
    print(f"Total chats with timelines: {len(timelines)}")

    # By year totals
    year_totals = Counter()
    for chat, info in timelines.items():
        for year_bucket in info["timeline"]:
            year_totals[year_bucket["year"]] += year_bucket["msgs"]

    print("\nTotal messages by year:")
    for year in sorted(year_totals.keys()):
        print(f"  {year}: {year_totals[year]:>8,} msgs")

    # Top 15 chats by lifetime volume
    print("\nTop 15 by lifetime volume:")
    top = sorted(timelines.items(), key=lambda x: -x[1]["lifetime_msgs"])[:15]
    for c, info in top:
        print(
            f"  {info['lifetime_msgs']:>7,} msgs  {info['lifetime_years_active']}y span  "
            f"peak {info['peak_year']}  {c[:35]}"
        )

    # Identify rising and falling relationships
    print("\n=== Rising relationships (recent year > previous year, +30% growth) ===")
    rising = []
    for c, info in timelines.items():
        if len(info["timeline"]) >= 2:
            recent_year = info["timeline"][-1]
            prev_year = info["timeline"][-2]
            if recent_year["msgs"] > 0 and prev_year["msgs"] > 0:
                growth = (recent_year["msgs"] - prev_year["msgs"]) / prev_year["msgs"]
                if growth > 0.3 and recent_year["msgs"] > 100:
                    rising.append((c, info, growth))

    for c, info, g in sorted(rising, key=lambda x: -x[2])[:10]:
        print(
            f"  +{g:.0%}  {info['timeline'][-2]['msgs']} -> {info['timeline'][-1]['msgs']} msgs  {c[:30]}"
        )

    print("\n=== Falling relationships (recent year < previous year, -30% drop) ===")
    falling = []
    for c, info in timelines.items():
        if len(info["timeline"]) >= 2:
            recent_year = info["timeline"][-1]
            prev_year = info["timeline"][-2]
            if recent_year["msgs"] > 0 and prev_year["msgs"] > 0:
                change = (recent_year["msgs"] - prev_year["msgs"]) / prev_year["msgs"]
                if change < -0.3 and prev_year["msgs"] > 100:
                    falling.append((c, info, change))

    for c, info, ch in sorted(falling, key=lambda x: x[2])[:10]:
        print(
            f"  {ch:.0%}  {info['timeline'][-2]['msgs']} -> {info['timeline'][-1]['msgs']} msgs  {c[:30]}"
        )


if __name__ == "__main__":
    build_timeline()

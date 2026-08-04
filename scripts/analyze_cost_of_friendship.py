#!/usr/bin/env python3
"""Cost-of-friendship analysis (Hat 11, 14)."""

from __future__ import annotations

import json
from pathlib import Path
from collections import Counter
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH/wa_messages"
ANALYSIS = WA / "_ANALYSIS"


def analyze_cost_of_friendship():
    """Calculate effort/cost per relationship (initiator ratio, response time, days active)."""
    init = json.loads((ANALYSIS / "initiator_analysis.json").read_text())

    by_chat = {}

    # Cost = Ivan's effort investment
    # Components:
    # - Ivan initiator ratio (higher = more effort)
    # - Ivan response time (faster = more available)
    # - Ivan starts conversations (more = more effort)
    # - Total messages

    # Cost score:
    # - Base effort: total msgs * 0.1
    # - Initiative cost: ivan_starts / total * 100
    # - Availability cost: 1 / (median_response_time + 1) * 50

    for chat_name, info in init["per_chat"].items():
        if info.get("total_msgs", 0) < 100:
            continue

        total_msgs = info["total_msgs"]
        ivan_starts = info.get("ivan_starts", 0)
        them_starts = info.get("them_starts", 0)
        total_starts = ivan_starts + them_starts
        ivan_initiative_pct = ivan_starts / total_starts if total_starts > 0 else 0
        median_response = info.get("median_response_time_ms", 0)

        # Cost components (normalized)
        base_cost = min(total_msgs / 1000, 50)  # Cap at 50

        initiative_cost = ivan_initiative_pct * 30  # Max 30

        availability_cost = 0
        if median_response and median_response > 0:
            # Faster responses = higher availability cost
            availability_cost = max(0, 30 - (median_response / 60000))  # Faster = higher

        total_cost = base_cost + initiative_cost + availability_cost

        # Categorize cost
        if total_cost > 70:
            cost_category = "VERY HIGH"
        elif total_cost > 50:
            cost_category = "HIGH"
        elif total_cost > 30:
            cost_category = "MEDIUM"
        elif total_cost > 15:
            cost_category = "LOW"
        else:
            cost_category = "MINIMAL"

        by_chat[chat_name] = {
            "tier": info.get("tier", "unknown"),
            "total_msgs": total_msgs,
            "ivan_starts": ivan_starts,
            "them_starts": them_starts,
            "ivan_initiative_pct": round(ivan_initiative_pct, 3),
            "median_response_min": round(median_response / 60000, 1) if median_response else None,
            "base_cost": round(base_cost, 1),
            "initiative_cost": round(initiative_cost, 1),
            "availability_cost": round(availability_cost, 1),
            "total_cost": round(total_cost, 1),
            "cost_category": cost_category,
        }

    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_relationships_analyzed": len(by_chat),
        "by_chat": by_chat,
    }

    out = ANALYSIS / "cost_of_friendship.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"Wrote {out.relative_to(REPO)}")

    print("\n=== Cost of Friendship Analysis ===")
    print(f"Total relationships: {len(by_chat)}")

    # Category distribution
    cat_dist = Counter(c["cost_category"] for c in by_chat.values())
    print("\nCost distribution:")
    for cat, count in sorted(cat_dist.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

    # Top 15 highest cost
    print("\nTop 15 HIGHEST cost relationships (Ivan's biggest investments):")
    sorted_chats = sorted(by_chat.items(), key=lambda x: -x[1]["total_cost"])[:15]
    for c, info in sorted_chats:
        print(
            f"  {info['total_cost']:>5.1f} ({info['cost_category']:<10})  "
            f"{info['ivan_initiative_pct']:>5.1%} init  "
            f"{info['total_msgs']:>5} msgs  {c[:35]}"
        )

    # Top 15 most cost-effective (low effort, high reward)
    print("\nTop 15 LOW cost relationships:")
    sorted_chats = sorted(by_chat.items(), key=lambda x: x[1]["total_cost"])[:15]
    for c, info in sorted_chats:
        print(
            f"  {info['total_cost']:>5.1f} ({info['cost_category']:<10})  "
            f"{info['ivan_initiative_pct']:>5.1%} init  "
            f"{info['total_msgs']:>5} msgs  {c[:35]}"
        )


if __name__ == "__main__":
    analyze_cost_of_friendship()

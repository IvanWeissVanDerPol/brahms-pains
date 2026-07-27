#!/usr/bin/env python3
"""Last-contact recency heatmap (feeds Hat 1, 31)."""
from __future__ import annotations

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH/wa_messages"
ANALYSIS = WA / "_ANALYSIS"


def analyze_recency():
    """Calculate last-contact days for all chats, build heatmap by tier."""
    by_chat = {}
    by_tier = defaultdict(list)

    tiers = ["tier1_deep", "tier2_core", "tier3_extended", "tier4_groups", "untiered_personal", "other_lid", "_dropped", "_newsletters"]

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
            total = len(msgs)

            # Find last message date
            valid_msgs = [m for m in msgs if isinstance(m, dict) and m.get("ts_ms")]
            if not valid_msgs:
                continue

            latest = max(valid_msgs, key=lambda x: x.get("ts_ms", 0))
            last_ts = latest.get("ts_ms", 0)
            if not last_ts:
                continue

            last_dt = datetime.fromtimestamp(last_ts / 1000, tz=timezone.utc)
            now = datetime.now(timezone.utc)
            days_since = (now - last_dt).days

            # Categorize recency
            if days_since <= 1:
                recency = "TODAY"
            elif days_since <= 7:
                recency = "THIS_WEEK"
            elif days_since <= 30:
                recency = "THIS_MONTH"
            elif days_since <= 90:
                recency = "THIS_QUARTER"
            elif days_since <= 180:
                recency = "HALF_YEAR"
            elif days_since <= 365:
                recency = "THIS_YEAR"
            else:
                recency = "ABANDONED"

            by_chat[chat_name] = {
                "tier": tier,
                "total_msgs": total,
                "last_message_ts": last_ts,
                "last_message_date": last_dt.isoformat(),
                "days_since_last": days_since,
                "recency_category": recency,
            }
            by_tier[tier].append(by_chat[chat_name])

    # Heatmap by tier x recency
    heatmap = {}
    for tier, items in by_tier.items():
        counter = defaultdict(int)
        for item in items:
            counter[item["recency_category"]] += 1
        heatmap[tier] = dict(counter)

    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_chats_analyzed": len(by_chat),
        "heatmap_by_tier": heatmap,
        "per_chat": by_chat,
    }

    out = ANALYSIS / "recency_heatmap.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"Wrote {out.relative_to(REPO)}")

    print(f"\n=== Recency Heatmap ===")
    print(f"Total: {len(by_chat)} chats")

    print(f"\n{'Tier':<25} {'TODAY':>6} {'WEEK':>6} {'MONTH':>6} {'QTR':>6} {'HALF':>6} {'YEAR':>6} {'ABAND':>7}")
    for tier in tiers:
        if tier in heatmap:
            h = heatmap[tier]
            total = sum(h.values())
            print(f"{tier:<25} {h.get('TODAY', 0):>6} {h.get('THIS_WEEK', 0):>6} {h.get('THIS_MONTH', 0):>6} {h.get('THIS_QUARTER', 0):>6} {h.get('HALF_YEAR', 0):>6} {h.get('THIS_YEAR', 0):>6} {h.get('ABANDONED', 0):>7}")

    # Top 10 most abandoned tier1/tier2 contacts
    print("\n=== Top 10 most abandoned tier1/tier2 (potential grief signals) ===")
    sorted_by_days = sorted(
        [(c, info) for c, info in by_chat.items() if info["tier"] in ("tier1_deep", "tier2_core") and info["total_msgs"] >= 50],
        key=lambda x: -x[1]["days_since_last"]
    )[:10]
    for c, info in sorted_by_days:
        print(f"  {info['days_since_last']:>5}d ago  {info['tier']:<12}  {info['total_msgs']:>5} msgs  {c[:35]}")

    # Top 10 freshest contacts
    print("\n=== Top 10 freshest contacts (most active) ===")
    sorted_fresh = sorted(
        [(c, info) for c, info in by_chat.items() if info["total_msgs"] >= 50],
        key=lambda x: x[1]["days_since_last"]
    )[:10]
    for c, info in sorted_fresh:
        print(f"  {info['days_since_last']:>3}d ago  {info['tier']:<20}  {c[:35]}")


if __name__ == "__main__":
    analyze_recency()
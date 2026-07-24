#!/usr/bin/env python3
"""Compute engagement trends over time per contact.

For each contact, compute:
- Monthly message volume (last 12 months)
- Trend direction: rising / falling / stable
- Recent activity: last 30d vs prior 30d vs prior 60-30d
- Hot/cold signal

Output: trends.json
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS"
MSG_BASE = REPO / "SOURCE_OF_TRUTH" / "wa_messages"

# Reference date (today)
TODAY = datetime(2026, 7, 23)


def analyze_trends(chat_dir: Path) -> dict:
    """Compute trend signals for one chat."""
    if not (chat_dir / "messages.json").exists():
        return {}
    try:
        data = json.loads((chat_dir / "messages.json").read_text())
    except Exception:
        return {}
    msgs = [m for m in data.get("messages", []) if isinstance(m, dict) and m.get("ts_iso")]
    if not msgs:
        return {}
    
    # Monthly counts (last 24 months)
    monthly = defaultdict(int)
    for m in msgs:
        ym = m["ts_iso"][:7]  # YYYY-MM
        monthly[ym] += 1
    
    # Recent windows
    # start_days_ago: how many days back the window STARTS
    # end_days_ago: how many days back the window ENDS (0 = today)
    def count_in_window(start_days_ago, end_days_ago=0):
        window_start = TODAY - timedelta(days=start_days_ago)  # older
        window_end = TODAY - timedelta(days=end_days_ago)       # newer
        n = 0
        for m in msgs:
            try:
                dt = datetime.fromisoformat(m["ts_iso"][:19])
                if window_start <= dt <= window_end:
                    n += 1
            except Exception:
                pass
        return n
    
    # Last 30 days: 30 days ago to today
    last_30 = count_in_window(30, 0)
    # Previous 30 days: 60 days ago to 30 days ago
    prev_30 = count_in_window(60, 30)
    # Previous 60 days: 120 days ago to 60 days ago
    prev_60 = count_in_window(120, 60)
    
    # Year-over-year comparison
    this_year = sum(1 for m in msgs if m["ts_iso"][:4] == "2026")
    last_year = sum(1 for m in msgs if m["ts_iso"][:4] == "2025")
    
    # Trend direction: compare last 30 vs prev 30
    if prev_30 == 0 and last_30 > 0:
        trend = "NEW"  # Just started
    elif prev_30 == 0 and last_30 == 0:
        trend = "DORMANT"
    elif last_30 > prev_30 * 1.5:
        trend = "RISING"
    elif last_30 < prev_30 * 0.5:
        trend = "FALLING"
    elif last_30 > prev_30 * 1.1:
        trend = "GROWING"
    elif last_30 < prev_30 * 0.9:
        trend = "COOLING"
    else:
        trend = "STABLE"
    
    # Change ratio
    change_ratio = last_30 / max(1, prev_30)
    
    # Days since last message
    try:
        last_dt = datetime.fromisoformat(msgs[-1]["ts_iso"][:19])
        days_since = (TODAY - last_dt).days
    except Exception:
        days_since = 9999
    
    # Months sorted list
    months_sorted = sorted(monthly.items())
    # Last 12 months
    last_12 = months_sorted[-12:] if len(months_sorted) >= 12 else months_sorted
    
    return {
        "monthly": dict(last_12),
        "last_30": last_30,
        "prev_30": prev_30,
        "prev_60": prev_60,
        "this_year_2026": this_year,
        "last_year_2025": last_year,
        "trend": trend,
        "change_ratio": round(change_ratio, 2),
        "days_since_last": days_since,
    }


def main():
    data = json.loads((ANALYSIS / "viewer_full_data.json").read_text())
    contacts = data["vcard_contacts"]
    
    print(f"Analyzing trends for {len(contacts)} contacts...")
    trends = []
    for c in contacts:
        chat_dir = MSG_BASE / c["tier"] / c["dir"]
        t = analyze_trends(chat_dir)
        if not t:
            continue
        trends.append({
            "jid": c["jid"],
            "name": c["name"],
            "tier": c["tier"],
            "total_msgs": c["total"],
            **t,
        })
    
    # Sort by trend priority (NEW/RISING first)
    TREND_ORDER = {"NEW": 0, "RISING": 1, "GROWING": 2, "STABLE": 3, "COOLING": 4, "FALLING": 5, "DORMANT": 6}
    trends.sort(key=lambda c: (TREND_ORDER.get(c["trend"], 99), -c["last_30"]))
    
    # Counts
    from collections import Counter
    trend_counts = Counter(t["trend"] for t in trends)
    
    # Save
    out = {
        "generated_at": datetime.now().isoformat(),
        "reference_date": TODAY.isoformat()[:10],
        "trend_counts": dict(trend_counts),
        "trends": trends,
    }
    out_path = ANALYSIS / "trends.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"Wrote {out_path.relative_to(REPO)}")
    print()
    print("=== Trend distribution ===")
    for trend in ["NEW", "RISING", "GROWING", "STABLE", "COOLING", "FALLING", "DORMANT"]:
        print(f"  {trend:<10}  {trend_counts.get(trend, 0)}")
    print()
    print("=== Top 20 RISING/NEW (gaining engagement) ===")
    rising = [t for t in trends if t["trend"] in ("NEW", "RISING", "GROWING")][:20]
    for t in rising:
        print(f"  {t['trend']:<8}  {t['last_30']:>3} last30 / {t['prev_30']:>3} prev30 ({t['change_ratio']}x)  {t['name'][:30]}")
    print()
    print("=== Top 20 FALLING/COOLING (losing engagement) ===")
    falling = [t for t in trends if t["trend"] in ("FALLING", "COOLING") and t["prev_30"] > 0][:20]
    for t in falling[:20]:
        print(f"  {t['trend']:<8}  {t['last_30']:>3} last30 / {t['prev_30']:>3} prev30 ({t['change_ratio']}x)  {t['name'][:30]}")


if __name__ == "__main__":
    main()
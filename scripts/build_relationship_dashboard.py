#!/usr/bin/env python3
"""Build a 'relationship score' dashboard that combines all signals into a
single comparable metric per contact.

Score = 0-100, weighted by:
  - Activity volume (msg count, recency)
  - Engagement reciprocity (balanced Ivan↔them ratio)
  - Response time (faster = more engaged)
  - Message length balance
  - Streak/gap pattern (long streaks = high intensity)
  - Sentiment (positive = warmer)
  - Audio usage (voice = intimate)
  - Longevity (longer = deeper)

Output: relationships_dashboard.json + relationships_dashboard.html
"""
from __future__ import annotations

import json
import re
import math
from collections import Counter
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS"
PROFILE_DIR = REPO / "RELATIONSHIPS" / "dynamics"
MSG_BASE = REPO / "SOURCE_OF_TRUTH" / "wa_messages"


def analyze_for_scoring(chat_dir: Path) -> dict:
    """Extract everything needed for the score."""
    if not (chat_dir / "messages.json").exists():
        return {}
    try:
        data = json.loads((chat_dir / "messages.json").read_text())
    except Exception:
        return {}
    msgs = [m for m in data.get("messages", []) if isinstance(m, dict)]
    if not msgs:
        return {}

    # Sort chronologically
    msgs = sorted([m for m in msgs if m.get("ts_iso")], key=lambda m: m["ts_iso"])

    ivan_total = sum(1 for m in msgs if m.get("from_me"))
    them_total = len(msgs) - ivan_total
    total = len(msgs)

    # Last activity recency (days since last msg)
    try:
        last_dt = datetime.fromisoformat(msgs[-1]["ts_iso"][:19])
        days_since_last = (datetime(2026, 7, 23) - last_dt).days
    except Exception:
        days_since_last = 9999

    # Response times (same logic as fill_profile_stubs)
    response_times_ivan = []
    response_times_them = []
    last_sender = None
    last_ts = None
    for m in msgs:
        text = m.get("text") or ""
        ts = m.get("ts_iso", "")
        try:
            if last_sender is not None and last_sender != m.get("from_me") and last_ts and text:
                t1 = datetime.fromisoformat(last_ts[:19])
                t2 = datetime.fromisoformat(ts[:19])
                delta = (t2 - t1).total_seconds()
                if 0 < delta < 86400:
                    if m.get("from_me"):
                        response_times_ivan.append(delta)
                    else:
                        response_times_them.append(delta)
            last_sender = m.get("from_me")
            last_ts = ts
        except Exception:
            pass

    avg_ivan_reply = sum(response_times_ivan) / len(response_times_ivan) if response_times_ivan else 0
    avg_them_reply = sum(response_times_them) / len(response_times_them) if response_times_them else 0

    # Audio count
    audio_count = sum(1 for m in msgs if m.get("type") == 2)
    audio_ratio = audio_count / total if total else 0

    # Streak analysis
    daily = set()
    for m in msgs:
        d = m.get("ts_iso", "")[:10]
        if d: daily.add(d)
    sorted_days = sorted(daily)
    longest_streak = 0
    cur = 0
    prev = None
    for d in sorted_days:
        dt = None
        try:
            dt = datetime.fromisoformat(d).date()
        except Exception:
            continue
        if prev and (dt - prev).days == 1:
            cur += 1
        else:
            cur = 1
        longest_streak = max(longest_streak, cur)
        prev = dt

    # Longevity (span in days)
    try:
        first_dt = datetime.fromisoformat(msgs[0]["ts_iso"][:19])
        last_dt = datetime.fromisoformat(msgs[-1]["ts_iso"][:19])
        span_days = (last_dt - first_dt).days
    except Exception:
        span_days = 0

    # Sentiment
    POS = set("""amor amo encanta feliz bien gracias guapo guapa hermosa hermoso contento contenta
alegria amazing love lovely enjoy wonderful excelente increible perfecto""".split())
    NEG = set("""mal triste odio enojado enojada molesto molesta cansado cansada horrible
terrible fatal feo fea asco dolor problema problemas angry sad tired hate upset""".split())
    pos_i = pos_t = neg_i = neg_t = 0
    for m in msgs:
        text = (m.get("text") or "").lower()
        is_ivan = m.get("from_me")
        for w in text.split():
            if w in POS:
                if is_ivan: pos_i += 1
                else: pos_t += 1
            elif w in NEG:
                if is_ivan: neg_i += 1
                else: neg_t += 1
    s_i = (pos_i - neg_i) / max(1, pos_i + neg_i)
    s_t = (pos_t - neg_t) / max(1, pos_t + neg_t)
    
    # Emoji density
    emoji_count = 0
    for m in msgs:
        if m.get("text"):
            emoji_count += len(re.findall(r'[\U0001F300-\U0001F9FF\U00002600-\U000027BF]', m["text"]))
    emoji_density = emoji_count / total if total else 0

    return {
        "total": total,
        "ivan_total": ivan_total,
        "them_total": them_total,
        "days_since_last": days_since_last,
        "avg_ivan_reply": avg_ivan_reply,
        "avg_them_reply": avg_them_reply,
        "audio_ratio": audio_ratio,
        "longest_streak": longest_streak,
        "span_days": span_days,
        "sentiment_ivan": s_i,
        "sentiment_them": s_t,
        "emoji_density": emoji_density,
    }


def score_relationship(stats: dict) -> dict:
    """Compute 0-100 score with sub-scores per dimension.
    
    Weights:
      - Volume (msg count)         15%
      - Recency (days since last)  15%
      - Reciprocity (msg balance)  10%
      - Response latency            10%
      - Streak intensity           10%
      - Longevity                   10%
      - Audio intimacy               8%
      - Emoji warmth                 5%
      - Sentiment (avg)             12%
      - Span activity (msgs/day)    5%
    """
    if not stats:
        return {"score": 0, "breakdown": {}}

    breakdown = {}
    
    # Volume: log-scaled (1 msg = 0, 1k = 30, 10k = 50, 50k = 65, 200k+ = 75)
    n = stats.get("total", 0)
    vol = min(75, 15 * math.log10(max(1, n)))
    breakdown["volume"] = round(vol, 1)
    
    # Recency: 0-100, full score if active in last 7 days
    days = stats.get("days_since_last", 9999)
    if days <= 1: recency = 100
    elif days <= 7: recency = 90
    elif days <= 30: recency = 70
    elif days <= 90: recency = 50
    elif days <= 180: recency = 30
    elif days <= 365: recency = 15
    else: recency = 5
    breakdown["recency"] = recency
    
    # Reciprocity: how balanced Ivan↔them (0.5 = perfect balance, 0 or 1 = one-sided)
    total = stats.get("total", 1)
    ivan_ratio = stats.get("ivan_total", 0) / total
    balance = 1 - 2 * abs(ivan_ratio - 0.5)  # 1 = perfect, 0 = one-sided
    reciprocity = 100 * balance
    breakdown["reciprocity"] = round(reciprocity, 1)
    
    # Response latency: faster = more engaged
    # Combine both sides (geometric mean)
    ivan_r = stats.get("avg_ivan_reply", 0)
    them_r = stats.get("avg_them_reply", 0)
    if ivan_r > 0 and them_r > 0:
        # 60s = 100, 5min = 90, 30min = 70, 2h = 50, 12h = 25, 24h+ = 5
        def r_score(s):
            if s <= 30: return 100
            if s <= 300: return 90
            if s <= 1800: return 70
            if s <= 7200: return 50
            if s <= 43200: return 25
            return 5
        avg_r = (ivan_r + them_r) / 2
        latency = r_score(avg_r)
    elif ivan_r > 0 or them_r > 0:
        latency = 50
    else:
        latency = 0
    breakdown["latency"] = latency
    
    # Streak intensity: long streaks = high engagement
    streak = stats.get("longest_streak", 0)
    if streak <= 1: streak_score = 5
    elif streak <= 7: streak_score = 30
    elif streak <= 30: streak_score = 60
    elif streak <= 90: streak_score = 80
    else: streak_score = 100
    breakdown["streak"] = streak_score
    
    # Longevity: years of contact
    span = stats.get("span_days", 0)
    years = span / 365
    if years < 0.1: longevity = 5
    elif years < 0.5: longevity = 30
    elif years < 1: longevity = 60
    elif years < 2: longevity = 80
    elif years < 4: longevity = 95
    else: longevity = 100
    breakdown["longevity"] = longevity
    
    # Audio intimacy
    audio = stats.get("audio_ratio", 0)
    if audio == 0: audio_score = 0
    elif audio < 0.05: audio_score = 30
    elif audio < 0.10: audio_score = 60
    elif audio < 0.20: audio_score = 80
    elif audio < 0.40: audio_score = 95
    else: audio_score = 100
    breakdown["audio"] = audio_score
    
    # Emoji warmth
    emoji_d = stats.get("emoji_density", 0)
    if emoji_d == 0: emoji_score = 0
    elif emoji_d < 0.05: emoji_score = 20
    elif emoji_d < 0.15: emoji_score = 50
    elif emoji_d < 0.30: emoji_score = 75
    elif emoji_d < 0.50: emoji_score = 90
    else: emoji_score = 100
    breakdown["emoji"] = emoji_score
    
    # Sentiment: avg of both sides, shifted to 0-100
    s_i = stats.get("sentiment_ivan", 0)
    s_t = stats.get("sentiment_them", 0)
    avg_sent = (s_i + s_t) / 2  # -1 to 1
    sentiment = 50 + 50 * avg_sent  # 0 to 100
    breakdown["sentiment"] = round(sentiment, 1)
    
    # Span activity: msgs per day (density of contact)
    span = stats.get("span_days", 1) or 1
    msgs_per_day = n / span
    if msgs_per_day < 0.1: activity = 5
    elif msgs_per_day < 0.5: activity = 30
    elif msgs_per_day < 2: activity = 60
    elif msgs_per_day < 10: activity = 85
    else: activity = 100
    breakdown["activity"] = activity
    
    # Weighted total
    weights = {
        "volume": 0.15,
        "recency": 0.15,
        "reciprocity": 0.10,
        "latency": 0.10,
        "streak": 0.10,
        "longevity": 0.10,
        "audio": 0.08,
        "emoji": 0.05,
        "sentiment": 0.12,
        "activity": 0.05,
    }
    score = sum(breakdown[k] * weights[k] for k in breakdown)
    
    # Tier
    if score >= 80: tier = "INTIMATE"  # BFF, family, romantic
    elif score >= 65: tier = "CLOSE"   # Best friends, mentors
    elif score >= 50: tier = "ACTIVE"  # Regular friends
    elif score >= 35: tier = "WARM"    # Occasional
    elif score >= 20: tier = "DORMANT" # Inactive
    else: tier = "COLD"
    
    return {
        "score": round(score, 1),
        "tier": tier,
        "breakdown": breakdown,
    }


def main():
    data = json.loads((ANALYSIS / "viewer_full_data.json").read_text())
    contacts = data["vcard_contacts"]

    print(f"Scoring {len(contacts)} contacts...")
    scored = []
    for c in contacts:
        chat_dir = MSG_BASE / c["tier"] / c["dir"]
        stats = analyze_for_scoring(chat_dir)
        if not stats:
            continue
        score = score_relationship(stats)
        scored.append({
            "jid": c["jid"],
            "name": c["name"],
            "tier": c["tier"],
            "total_msgs": c["total"],
            "stats": stats,
            **score,
        })

    # Sort by score
    scored.sort(key=lambda x: -x["score"])
    
    # Tier distribution
    tier_counts = Counter(c["tier"] for c in scored)
    
    # Save
    out = {
        "generated_at": datetime.now().isoformat(),
        "weights": {
            "volume": 0.15, "recency": 0.15, "reciprocity": 0.10,
            "latency": 0.10, "streak": 0.10, "longevity": 0.10,
            "audio": 0.08, "emoji": 0.05, "sentiment": 0.12,
            "activity": 0.05,
        },
        "tier_counts": dict(tier_counts),
        "scored": scored,
    }
    out_path = ANALYSIS / "relationships_dashboard.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"Wrote {out_path.relative_to(REPO)}")
    print()
    print("=== Top 20 relationships by score ===")
    for c in scored[:20]:
        print(f"  {c['score']:>5.1f}  {c['tier']:<8}  {c['name'][:30]:<30}  ({c['total_msgs']:>6,} msgs, last {c['stats']['days_since_last']}d)")
    print()
    print("=== Tier distribution ===")
    for tier, n in sorted(tier_counts.items(), key=lambda x: -x[1]):
        print(f"  {tier:<10}  {n}")


if __name__ == "__main__":
    main()
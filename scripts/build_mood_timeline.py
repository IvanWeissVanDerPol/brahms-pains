#!/usr/bin/env python3
"""Build a mood timeline per contact — sentiment over time.

For each contact, compute monthly sentiment scores (positive - negative)
and visualize the trajectory. Use a richer word list + emoji weighting.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS"
MSG_BASE = REPO / "SOURCE_OF_TRUTH" / "wa_messages"

# Spanish + English sentiment dictionaries
POS_WORDS = set("""
amor amo encanta encantado encantada feliz bien buenos buenas gracias guapo guapa
hermosa hermoso bella bello alegria contento contenta orgullosa orgulloso amazing
love lovely enjoy wonderful excelente increible perfecto beautiful happy great
best awesome fantastic perfecta perfecto alegria risa sonrisa tierna tierno
amistad friendship caring kind honesto honesto paciente paciente beautiful
amazing gracias nice sweet love fun exciting excited glad joyful merry
divertido gusta gusta encanta cariño sweet preciosa precious
felicidad blessed gracias gracias gracias gracias beso abrazo
cool win winning winner proud accomplished safe
""".split())
NEG_WORDS = set("""
mal triste odio enojado enojada molesto molesta cansado cansada horrible
terrible fatal feo fea asco dolor problema problemas angry sad tired hate upset
awful terrible horrible disgusting pain hurt broken sick worried stress
frustrated frustrated stressed anxious fear scary disappointing disappointed
horrible horrible
llorar llorar sufro sufres duele duelen solo sola lonely
broken failure fail fail loss lost dead death kill fight
desprecio desprecio insult insulto mal mal mal
""".split())

# Emoji weight: positive emoji vs negative emoji
POS_EMOJI = set("❤️ 💕 💖 💗 💓 💞 💘 💝 😊 😄 😃 😀 🤗 🥰 😍 😘 😂 🤣 🎉 🎊 ✨ 🌟 💫 🌈 🔥 💪 👍 👏 🙌 🎂 🍰 🎁 💝 🌸 🌺 🌻 🌼 🌷 🍀")
NEG_EMOJI = set("😢 😭 😞 😔 😟 😕 🙁 ☹️ 😣 😖 😫 😩 😤 😠 😡 🤬 💔 😿 🥺 😰 😥 🤢 🤮 😷 💀 👿 😈")


def month_sentiment(msgs: list, year_month: str) -> dict:
    """Compute sentiment for one month."""
    pos = neg = 0
    pos_emo = neg_emo = 0
    msg_count = 0
    for m in msgs:
        if not isinstance(m, dict): continue
        ts = m.get("ts_iso", "")
        if not ts.startswith(year_month): continue
        msg_count += 1
        text = (m.get("text") or "").lower()
        for w in re.findall(r'\b[a-záéíóúñ]+\b', text):
            if w in POS_WORDS: pos += 1
            elif w in NEG_WORDS: neg += 1
        # Emojis
        emojis_in_text = re.findall(r'[\U0001F300-\U0001F9FF\U00002600-\U000027BF\U0001F600-\U0001F64F]', text)
        for em in emojis_in_text:
            if em in POS_EMOJI: pos_emo += 1
            elif em in NEG_EMOJI: neg_emo += 1
    total = pos + neg + pos_emo + neg_emo
    if total == 0:
        return {"score": 0, "pos": 0, "neg": 0, "msgs": msg_count}
    score = (pos + pos_emo - neg - neg_emo) / total
    return {"score": round(score, 3), "pos": pos + pos_emo, "neg": neg + neg_emo, "msgs": msg_count}


def main():
    data = json.loads((ANALYSIS / "viewer_full_data.json").read_text())
    contacts = data["vcard_contacts"]
    
    # Focus on the top 50 most-active contacts (for performance + relevance)
    top_contacts = sorted(contacts, key=lambda c: -c["total"])[:50]
    
    print(f"Computing mood timelines for top {len(top_contacts)} contacts...")
    timelines = []
    for c in top_contacts:
        chat_dir = MSG_BASE / c["tier"] / c["dir"]
        if not (chat_dir / "messages.json").exists(): continue
        try:
            data = json.loads((chat_dir / "messages.json").read_text())
        except: continue
        msgs = data.get("messages", [])
        if not msgs: continue
        
        # Get all unique months
        months = set()
        for m in msgs:
            ts = m.get("ts_iso", "")
            if ts: months.add(ts[:7])
        sorted_months = sorted(months)
        
        # Compute per-month sentiment
        monthly_scores = []
        for ym in sorted_months:
            s = month_sentiment(msgs, ym)
            monthly_scores.append({
                "month": ym,
                "score": s["score"],
                "pos": s["pos"],
                "neg": s["neg"],
                "msgs": s["msgs"],
            })
        
        # Compute trajectory
        if len(monthly_scores) >= 3:
            # Trend: compare last 3 months vs prior 3 months
            recent = monthly_scores[-3:]
            prior = monthly_scores[-6:-3] if len(monthly_scores) >= 6 else monthly_scores[:-3]
            recent_avg = sum(m["score"] for m in recent) / len(recent) if recent else 0
            prior_avg = sum(m["score"] for m in prior) / len(prior) if prior else 0
            trend = recent_avg - prior_avg
        else:
            recent_avg = prior_avg = trend = 0
        
        # Highest/lowest months
        if monthly_scores:
            best = max(monthly_scores, key=lambda m: m["score"])
            worst = min(monthly_scores, key=lambda m: m["score"])
        else:
            best = worst = None
        
        timelines.append({
            "jid": c["jid"],
            "name": c["name"],
            "tier": c["tier"],
            "total_msgs": c["total"],
            "monthly": monthly_scores,
            "recent_avg": round(recent_avg, 3),
            "prior_avg": round(prior_avg, 3),
            "trend_delta": round(trend, 3),
            "best_month": best,
            "worst_month": worst,
        })
    
    # Sort by trend delta (most positive change first)
    timelines.sort(key=lambda t: -t["trend_delta"])
    
    out = {
        "generated_at": datetime.now().isoformat(),
        "method": "per-month sentiment score (positive - negative) / total sentiment words + emojis",
        "top_contacts_count": len(timelines),
        "pos_words_count": len(POS_WORDS),
        "neg_words_count": len(NEG_WORDS),
        "pos_emoji_count": len(POS_EMOJI),
        "neg_emoji_count": len(NEG_EMOJI),
        "timelines": timelines,
    }
    out_path = ANALYSIS / "mood_timelines.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"Wrote {out_path.relative_to(REPO)}")
    print()
    print("=== Top 15 contacts with POSITIVE mood trend ===")
    for t in timelines[:15]:
        if t["trend_delta"] > 0:
            print(f"  Δ{t['trend_delta']:+.2f}  recent={t['recent_avg']:+.2f}  {t['name'][:30]:<30}  (best: {t['best_month']['month'] if t['best_month'] else 'n/a'})")
    print()
    print("=== Top 15 contacts with NEGATIVE mood trend ===")
    for t in timelines[-15:]:
        if t["trend_delta"] < 0:
            print(f"  Δ{t['trend_delta']:+.2f}  recent={t['recent_avg']:+.2f}  {t['name'][:30]:<30}  (worst: {t['worst_month']['month'] if t['worst_month'] else 'n/a'})")
    print()
    print("=== Most positive overall (avg) ===")
    by_avg = sorted(timelines, key=lambda t: -t["recent_avg"])[:10]
    for t in by_avg:
        print(f"  {t['recent_avg']:+.2f}  {t['name'][:30]}")
    print()
    print("=== Most negative overall (avg) ===")
    by_avg = sorted(timelines, key=lambda t: t["recent_avg"])[:10]
    for t in by_avg:
        print(f"  {t['recent_avg']:+.2f}  {t['name'][:30]}")


if __name__ == "__main__":
    main()
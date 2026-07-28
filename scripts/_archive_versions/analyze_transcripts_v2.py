#!/usr/bin/env python3
"""Build proper voice notes analysis from all transcripts."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS"
TRANSCRIPT_BASE = REPO / "SOURCE_OF_TRUTH" / "voice_note_transcripts"

POS = set("""amor amo encanta encantado encantada feliz bien buenos buenas gracias
guapo guapa hermosa hermoso bella bello alegria contento contenta orgullosa
amazing love lovely enjoy wonderful excelente increible perfecto beautiful
happy great best awesome fantastic sonrisa tierna tierno abrazo beso""".split())
NEG = set("""mal triste odio enojado enojada molesto molesta cansado cansada horrible
terrible fatal feo fea asco dolor problema problemas angry sad tired hate
upset awful disgusting pain hurt broken sick worried stress frustrated""".split())
EMOTIONS = {
    "love": ["amor", "te quiero", "te amo", "love", "cariño", "bb", "bebe"],
    "laugh": ["jajaja", "jaja", "jajajaja", "haha", "lol"],
    "anger": ["odio", "wtf", "fuck", "mierda", "carajo", "puta", "enojado", "verga"],
    "sadness": ["triste", "llorar", "llorando", "solo", "sola", "sad", "cry"],
    "surprise": ["wow", "wtf", "en serio", "really", "no way", "ostia"],
    "gratitude": ["gracias", "thanks", "thank you", "mil gracias"],
}


def main():
    print("Loading transcripts...")
    all_entries = []
    for f in TRANSCRIPT_BASE.rglob("transcripts.json"):
        try:
            arr = json.loads(f.read_text())
            if isinstance(arr, list):
                for e in arr:
                    e["_chat"] = f.parent.name
                all_entries.extend(arr)
        except: pass

    valid = [e for e in all_entries if e.get("text")]
    print(f"Valid transcripts: {len(valid):,}")

    vcard_data = json.loads((ANALYSIS / "viewer_full_data.json").read_text())
    jid_to_name = {c["jid"]: c["name"] for c in vcard_data["vcard_contacts"]}

    # === Compute all aggregates ===
    total_duration = 0
    total_words = 0
    lang_counts = Counter()
    pos_total = neg_total = 0
    emotion_totals = Counter()
    yearly = Counter()
    durations = []
    chat_data = defaultdict(lambda: {"notes": 0, "words": 0, "duration": 0, "pos": 0, "neg": 0, "langs": Counter(), "emotions": Counter()})
    
    chat_to_jid = {}
    for t in valid:
        chat = t.get("_chat", "?")
        if chat not in chat_to_jid:
            m = re.search(r'(?:chat|_wa_chat)_(\d{8,15})_', chat)
            if m: chat_to_jid[chat] = m.group(1)
    
    for t in valid:
        text = (t.get("text", "") or "").lower()
        words = re.findall(r'\b[a-záéíóúñ]+\b', text)
        d = t.get("duration", 0) or 0
        lang = t.get("language", "?")
        chat = t.get("_chat", "?")
        file = t.get("file", "")
        
        # Date extraction
        ym = re.search(r'PTT-(\d{4})(\d{2})', file)
        if ym: yearly[ym.group(1)] += 1
        elif "AUD-" in file:
            ym = re.search(r'AUD-(\d{4})', file)
            if ym: yearly[ym.group(1)] += 1
        
        # Sentiment + emotions per note
        pos_n = neg_n = 0
        for w in words:
            if w in POS: pos_n += 1
            elif w in NEG: neg_n += 1
        
        for emotion, markers in EMOTIONS.items():
            n = 0
            for marker in markers:
                if " " in marker: n += text.count(marker)
                else: n += sum(1 for w in words if w == marker)
            if n > 0: emotion_totals[emotion] += n
        
        # Aggregate
        total_duration += d
        total_words += len(words)
        pos_total += pos_n
        neg_total += neg_n
        durations.append(d)
        lang_counts[lang] += 1
        
        cd = chat_data[chat]
        cd["notes"] += 1
        cd["words"] += len(words)
        cd["duration"] += d
        cd["pos"] += pos_n
        cd["neg"] += neg_n
        cd["langs"][lang] += 1
        for e, n in emotion_totals.items():
            if n > 0: pass  # already global
        for emotion, markers in EMOTIONS.items():
            n = 0
            for marker in markers:
                if " " in marker: n += text.count(marker)
                else: n += sum(1 for w in words if w == marker)
            if n > 0: cd["emotions"][emotion] += n
    
    # Duration percentiles
    durations.sort()
    n = len(durations)
    p50 = durations[n // 2]
    p90 = durations[int(n * 0.9)]
    p95 = durations[int(n * 0.95)]
    p99 = durations[int(n * 0.99)]
    
    # Build chat stats list
    chat_stats = []
    for chat, cd in chat_data.items():
        jid = chat_to_jid.get(chat, "?")
        name = jid_to_name.get(jid, "?")
        avg_s = (cd["pos"] - cd["neg"]) / max(1, cd["pos"] + cd["neg"])
        chat_stats.append({
            "chat": chat,
            "name": name,
            "jid": jid,
            "transcripts": cd["notes"],
            "total_words": cd["words"],
            "total_duration_s": round(cd["duration"], 1),
            "avg_sentiment": round(avg_s, 3),
            "pos_words": cd["pos"],
            "neg_words": cd["neg"],
            "dominant_lang": cd["langs"].most_common(1)[0][0] if cd["langs"] else "?",
            "emotions": dict(cd["emotions"]),
        })
    chat_stats.sort(key=lambda c: -c["transcripts"])
    
    # Sentiment distribution
    # Bucket each transcript by sentiment
    sent_buckets = {"positive": 0, "neutral": 0, "negative": 0}
    for t in valid:
        text = (t.get("text", "") or "").lower()
        words = re.findall(r'\b[a-záéíóúñ]+\b', text)
        pos_n = sum(1 for w in words if w in POS)
        neg_n = sum(1 for w in words if w in NEG)
        if pos_n + neg_n == 0:
            sent_buckets["neutral"] += 1
            continue
        s = (pos_n - neg_n) / (pos_n + neg_n)
        if s > 0.2: sent_buckets["positive"] += 1
        elif s < -0.2: sent_buckets["negative"] += 1
        else: sent_buckets["neutral"] += 1
    
    # Final output
    out = {
        "generated_at": datetime.now().isoformat(),
        "total_transcripts": len(valid),
        "total_files_scanned": len(list(TRANSCRIPT_BASE.rglob("transcripts.json"))),
        "total_words": total_words,
        "total_duration_hours": round(total_duration / 3600, 2),
        "avg_words_per_note": round(total_words / max(1, len(valid)), 1),
        "median_duration_seconds": round(p50, 1),
        "p90_duration_seconds": round(p90, 1),
        "p95_duration_seconds": round(p95, 1),
        "p99_duration_seconds": round(p99, 1),
        "max_duration_seconds": round(max(durations), 1) if durations else 0,
        "languages": dict(lang_counts.most_common()),
        "yearly_distribution": dict(yearly),
        "sentiment_distribution": sent_buckets,
        "sentiment_totals": {
            "positive_words": pos_total,
            "negative_words": neg_total,
            "ratio": round(pos_total / max(1, neg_total), 3),
        },
        "emotion_totals": dict(emotion_totals.most_common()),
        "top_chats_by_volume": chat_stats[:50],
        "all_chats_count": len(chat_stats),
    }
    out_path = ANALYSIS / "transcript_analysis.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"\nWrote {out_path.relative_to(REPO)}")
    print()
    print(f"Total: {out['total_transcripts']:,} transcripts, {out['total_words']:,} words, {out['total_duration_hours']:.1f}h audio")
    print(f"Languages: {dict(list(out['languages'].items())[:5])}")
    print(f"Sentiment: {sent_buckets}")
    print(f"Top emotions: {dict(list(out['emotion_totals'].items())[:5])}")


if __name__ == "__main__":
    main()

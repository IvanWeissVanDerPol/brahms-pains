#!/usr/bin/env python3
"""Analyze what's already been transcribed.

For each transcript, extract:
- Language detected (es, en, etc.)
- Word count
- Sentiment (positive/negative words)
- Named entities (mention of contact names)
- Emotional markers (love, anger, laughter, etc.)
- Audio duration

Output: transcript_analysis.json
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS"
TRANSCRIPT_BASE = REPO / "SOURCE_OF_TRUTH" / "voice_note_transcripts"

# Sentiment dictionaries (Spanish + English)
POS = set("""amor amo encanta encantado encantada feliz bien buenos buenas gracias
guapo guapa hermosa hermoso bella bello alegria contento contenta orgullosa
amazing love lovely enjoy wonderful excelente increible perfecto beautiful
happy great best awesome fantastic sonrisa tierna tierno abrazo beso""".split())
NEG = set("""mal triste odio enojado enojada molesto molesta cansado cansada horrible
terrible fatal feo fea asco dolor problema problemas angry sad tired hate
upset awful disgusting pain hurt broken sick worried stress frustrated""".split())

# Emotional markers
EMOTIONS = {
    "love": ["amor", "te quiero", "te amo", "love", "cariño", "bb", "bebe"],
    "laugh": ["jajaja", "jaja", "jajajaja", "haha", "lol", "😂", "🤣"],
    "anger": ["odio", "wtf", "fuck", "mierda", "carajo", "puta", "enojado", "enojada"],
    "sadness": ["triste", "llorar", "llorando", "solo", "sola", "sad", "cry"],
    "surprise": ["wow", "wtf", "en serio", "really", "no way", "ostia", "ostras"],
    "gratitude": ["gracias", "thanks", "thank you", "mil gracias"],
}


def analyze_transcript(transcript: dict) -> dict:
    """Analyze one transcript entry."""
    text = transcript.get("text", "")
    if not text:
        return {}

    text_low = text.lower()
    words = re.findall(r"\b[a-záéíóúñ]+\b", text_low)

    pos_count = sum(1 for w in words if w in POS)
    neg_count = sum(1 for w in words if w in NEG)

    # Emotion markers
    emotion_counts = {}
    for emotion, markers in EMOTIONS.items():
        n = 0
        for marker in markers:
            if " " in marker:
                n += text_low.count(marker)
            else:
                n += sum(1 for w in words if w == marker)
        if n > 0:
            emotion_counts[emotion] = n

    return {
        "word_count": len(words),
        "char_count": len(text),
        "pos_words": pos_count,
        "neg_words": neg_count,
        "sentiment_score": round((pos_count - neg_count) / max(1, pos_count + neg_count), 3),
        "emotions": emotion_counts,
    }


def main():
    print("Loading transcripts...")

    # Walk all transcript files
    transcripts = []
    file_count = 0
    for f in TRANSCRIPT_BASE.rglob("transcripts.json"):
        file_count += 1
        try:
            arr = json.loads(f.read_text())
            if not isinstance(arr, list):
                continue
            # Get chat_dir from parent folder name
            chat_dir = f.parent.name  # e.g., "chat_595982646114_5235" or "_wa_chat_X_Y"
            for entry in arr:
                entry["_chat"] = chat_dir
            transcripts.extend(arr)
        except Exception:
            pass

    print(f"Found {file_count} transcript files with {len(transcripts)} entries")

    # Filter out empty/failed transcripts
    valid = [t for t in transcripts if t.get("text")]
    print(f"Valid (non-empty): {len(valid)}")

    # Normalize durations (None → 0)
    for t in valid:
        if t.get("duration") is None:
            t["duration"] = 0.0

    # Analyze
    print("Analyzing each transcript...")
    analyzed = []
    for t in valid:
        a = analyze_transcript(t)
        if a:
            analyzed.append(
                {
                    "file": t.get("file", "?"),
                    "duration": t.get("duration", 0) or 0,
                    "language": t.get("language", "?"),
                    "_chat": t.get("_chat", "unknown"),
                    **a,
                }
            )

    # === Aggregate stats ===

    # Languages
    lang_counts = Counter(t["language"] for t in analyzed)

    # Avg metrics
    total_words = sum(t["word_count"] for t in analyzed)
    avg_words = total_words / max(1, len(analyzed))

    total_duration = sum(t["duration"] for t in analyzed)
    avg_duration = total_duration / max(1, len(analyzed))

    # Sentiment distribution
    pos_total = sum(t["pos_words"] for t in analyzed)
    neg_total = sum(t["neg_words"] for t in analyzed)

    # Bucket by sentiment
    pos_msgs = sum(1 for t in analyzed if t["sentiment_score"] > 0.2)
    neg_msgs = sum(1 for t in analyzed if t["sentiment_score"] < -0.2)
    neutral_msgs = sum(1 for t in analyzed if -0.2 <= t["sentiment_score"] <= 0.2)

    # Emotions
    emotion_totals = Counter()
    for t in analyzed:
        for e, n in t["emotions"].items():
            emotion_totals[e] += n

    # === Per-contact analysis ===
    # Group transcripts by chat_dir (now correctly extracted from path)
    print("Grouping by chat...")
    by_chat = defaultdict(list)
    for t in transcripts:
        if not t.get("text"):
            continue  # Skip non-transcribed
        chat = t.get("_chat", "unknown")
        by_chat[chat].append(t)

    # Build chat_dir → JID/name mapping
    # Chat dirs may have suffixes like "chat_595982646114_5235" — extract JID-like prefix
    import re

    chat_to_jid = {}
    for chat_dir in by_chat.keys():
        # Try patterns
        m = re.search(r"(?:chat|_wa_chat)_(\d{8,15})_", chat_dir)
        if m:
            chat_to_jid[chat_dir] = m.group(1)

    # Match to vCard contact names
    vcard_data = json.loads((ANALYSIS / "viewer_full_data.json").read_text())
    jid_to_name = {c["jid"]: c["name"] for c in vcard_data["vcard_contacts"]}
    chat_to_name = {cd: jid_to_name.get(jid, "?") for cd, jid in chat_to_jid.items()}

    # Per-chat aggregate (using analyzed list which has sentiment + word_count)
    chat_stats = []
    for chat_dir, ts in by_chat.items():
        # Find matching analyzed entries (skip non-transcribed)
        file_set = {(t.get("file"), t.get("_chat")) for t in ts}
        analyzed_for_chat = (
            [a for a in analyzed if (a["file"], a.get("_chat")) in file_set] if False else []
        )  # placeholder
        # Simpler: filter analyzed by chat
        analyzed_for_chat = [a for a in analyzed if a.get("_chat") == chat_dir]
        if not analyzed_for_chat:
            # Fall back to raw transcripts with quick analysis
            analyzed_for_chat = []
            for t in ts:
                a = analyze_transcript(t)
                if a:
                    analyzed_for_chat.append(
                        {
                            "file": t["file"],
                            "duration": t.get("duration") or 0,
                            "language": t.get("language", "?"),
                            **a,
                            "_chat": chat_dir,
                        }
                    )

        total_w = sum(t["word_count"] for t in analyzed_for_chat)
        total_d = sum(t["duration"] for t in analyzed_for_chat)
        avg_s = sum(t["sentiment_score"] for t in analyzed_for_chat) / max(
            1, len(analyzed_for_chat)
        )
        pos_t = sum(t["pos_words"] for t in analyzed_for_chat)
        neg_t = sum(t["neg_words"] for t in analyzed_for_chat)
        lang_mode = Counter(t["language"] for t in analyzed_for_chat).most_common(1)

        chat_stats.append(
            {
                "chat": chat_dir,
                "name": chat_to_name.get(chat_dir, "?"),
                "jid": chat_to_jid.get(chat_dir, "?"),
                "transcripts": len(analyzed_for_chat),
                "total_words": total_w,
                "total_duration_s": round(total_d, 1),
                "avg_sentiment": round(avg_s, 3),
                "pos_words": pos_t,
                "neg_words": neg_t,
                "dominant_lang": lang_mode[0][0] if lang_mode else "?",
            }
        )

    chat_stats.sort(key=lambda c: -c["transcripts"])

    # === Most emotional contacts (more transcripts = more voice-note intimacy) ===
    print("\n=== Aggregate stats ===")
    print(f"Total transcripts: {len(analyzed)}")
    print(f"Total words spoken: {total_words:,} ({total_words / 1000:.1f}k)")
    print(f"Avg words per voice note: {avg_words:.1f}")
    print(f"Total audio duration: {total_duration / 3600:.1f} hours")
    print(f"Avg duration: {avg_duration:.1f} seconds")

    print("\nSentiment:")
    print(f"  Positive (>0.2): {pos_msgs} ({100*pos_msgs/len(analyzed):.1f}%)")
    print(f"  Neutral: {neutral_msgs} ({100*neutral_msgs/len(analyzed):.1f}%)")
    print(f"  Negative (<-0.2): {neg_msgs} ({100*neg_msgs/len(analyzed):.1f}%)")
    print(f"  Total pos words: {pos_total:,}")
    print(f"  Total neg words: {neg_total:,}")

    print("\nEmotions detected (total markers):")
    for e, n in emotion_totals.most_common():
        print(f"  {e:<10}  {n:,}")

    print("\nLanguages detected:")
    for lang, n in lang_counts.most_common(10):
        pct = 100 * n / len(analyzed)
        print(f"  {lang:<6}  {n:>5} ({pct:.1f}%)")

    print("\nTop 10 most-voice-note-heavy chats:")
    for c in chat_stats[:10]:
        print(
            f"  {c['chat'][:50]:<50}  {c['transcripts']:>4} voice notes, {c['total_words']:,} words"
        )

    print("\nTop 10 most POSITIVE chats (by avg sentiment):")
    pos_sorted = sorted(chat_stats, key=lambda c: -c["avg_sentiment"])[:10]
    for c in pos_sorted:
        if c["transcripts"] >= 5:  # only consider chats with 5+ voice notes
            print(
                f"  {c['avg_sentiment']:+.2f}  {c['chat'][:50]:<50}  ({c['transcripts']} notes, {c['pos_words']}/{c['neg_words']} pos/neg)"
            )

    print("\nTop 10 most NEGATIVE chats:")
    neg_sorted = [c for c in chat_stats if c["transcripts"] >= 5]
    neg_sorted.sort(key=lambda c: c["avg_sentiment"])
    for c in neg_sorted[:10]:
        print(
            f"  {c['avg_sentiment']:+.2f}  {c['chat'][:50]:<50}  ({c['transcripts']} notes, {c['pos_words']}/{c['neg_words']} pos/neg)"
        )

    # Save
    out = {
        "generated_at": datetime.now().isoformat(),
        "total_transcripts": len(analyzed),
        "total_files_scanned": file_count,
        "total_words": total_words,
        "total_duration_hours": round(total_duration / 3600, 2),
        "avg_words_per_note": round(avg_words, 1),
        "avg_duration_seconds": round(avg_duration, 1),
        "languages": dict(lang_counts),
        "sentiment_distribution": {
            "positive_msgs": pos_msgs,
            "neutral_msgs": neutral_msgs,
            "negative_msgs": neg_msgs,
        },
        "sentiment_totals": {
            "positive_words": pos_total,
            "negative_words": neg_total,
            "ratio": round(pos_total / max(1, neg_total), 3),
        },
        "emotion_totals": dict(emotion_totals),
        "top_chats_by_volume": chat_stats[:50],
        "top_chats_positive": pos_sorted[:30],
        "top_chats_negative": neg_sorted[:30],
    }
    out_path = ANALYSIS / "transcript_analysis.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"\nWrote {out_path.relative_to(REPO)}")


if __name__ == "__main__":
    main()

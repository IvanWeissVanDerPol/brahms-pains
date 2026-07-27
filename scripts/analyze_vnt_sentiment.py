#!/usr/bin/env python3
"""Voice note sentiment analysis by contact (feeds Hat 1, 7, 22)."""
from __future__ import annotations

import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH/wa_messages/_ANALYSIS"
VNT = REPO / "SOURCE_OF_TRUTH/voice_note_transcripts"

# Load existing analyses for tier mapping
tp = json.loads((ANALYSIS / "time_patterns.json").read_text())
rec = json.loads((ANALYSIS / "recency_heatmap.json").read_text())

# Bilingual sentiment lexicon
POSITIVE_WORDS = {
    "es": ["amor", "amo", "feliz", "gracias", "genial", "increible", "hermoso", "hermosa",
           "lindo", "linda", "bueno", "buena", "excelente", "maravilloso", "maravillosa",
           "encanta", "gusta", "divertido", "jaja", "jajaja", "jajajaja", "risa", "sonrie",
           "abrazo", "beso", "te quiero", "te amo", "precioso", "preciosa", "dulce", "tierno",
           "tierna", "cariñoso", "cariñosa", "amor", "placer", "alegre", "felicidad"],
    "en": ["love", "happy", "thanks", "thank", "great", "amazing", "beautiful", "wonderful",
           "good", "nice", "excellent", "incredible", "awesome", "fun", "lol", "haha",
           "smile", "hug", "kiss", "sweet", "cute", "lovely", "dear", "best", "perfect",
           "joy", "glad", "pleasure"]
}

NEGATIVE_WORDS = {
    "es": ["triste", "tristeza", "dolor", "duele", "malo", "mala", "horrible", "feo", "fea",
           "molesto", "molesta", "enojado", "enojada", "enojo", "rabia", "pelea", "discusión",
           "llora", "lloré", "llorando", "lágrima", "lágrimas", "abandonado", "solo", "sola",
           "vacío", "vacía", "miedo", "asustado", "asustada", "preocupado", "preocupada",
           "estrés", "estresado", "estresada", "agobiado", "agobiada", "cansado", "cansada",
           "agotado", "agotada", "frustrado", "frustrada", "deprimido", "deprimida", "ansioso",
           "ansiosa", "angustia", "desesperado", "desesperada", "pena", "pena", "luto", "duelo"],
    "en": ["sad", "pain", "hurt", "bad", "terrible", "awful", "ugly", "angry", "mad",
           "fight", "argument", "cry", "cried", "crying", "tear", "tears", "alone", "lonely",
           "empty", "afraid", "scared", "worried", "stress", "stressed", "tired", "exhausted",
           "frustrated", "depressed", "anxious", "anxiety", "desperate", "grief", "mourning"]
}

EMOTIONAL_INDICATORS = {
    "es": ["siento", "siento que", "me siento", "corazón", "alma", "profundo", "profunda",
           "íntimo", "íntima", "vulnerable", "conmovido", "conmovida", "emocionado", "emocionada",
           "llorando", "riendo"],
    "en": ["feel", "feeling", "heart", "soul", "deep", "deeply", "intimate", "vulnerable",
           "moved", "emotional", "crying", "laughing"]
}


def sentiment_score(text):
    """Calculate sentiment score from -1 (very negative) to +1 (very positive)."""
    text_lower = text.lower()
    pos_count = 0
    neg_count = 0
    emo_count = 0

    for word_list in POSITIVE_WORDS.values():
        for w in word_list:
            pos_count += len(re.findall(r'\b' + re.escape(w) + r'\b', text_lower))

    for word_list in NEGATIVE_WORDS.values():
        for w in word_list:
            neg_count += len(re.findall(r'\b' + re.escape(w) + r'\b', text_lower))

    for word_list in EMOTIONAL_INDICATORS.values():
        for w in word_list:
            emo_count += len(re.findall(r'\b' + re.escape(w) + r'\b', text_lower))

    total = pos_count + neg_count
    if total == 0:
        return 0, 0, 0

    score = (pos_count - neg_count) / max(total, 1)
    return score, emo_count, total


def analyze_vnt_sentiment():
    """Analyze voice note transcripts for sentiment per contact."""
    by_contact = {}
    by_tier = defaultdict(list)

    # Walk through all VNT dirs
    for vnt_dir in VNT.iterdir():
        if not vnt_dir.is_dir():
            continue

        # Find .txt files
        txts = list(vnt_dir.glob("*.txt"))
        if not txts:
            continue

        contact_name = vnt_dir.name

        # Aggregate text from all transcripts
        all_text = ""
        transcript_count = 0
        for txt in txts:
            try:
                content = txt.read_text(errors='ignore')
                all_text += " " + content
                transcript_count += 1
            except:
                pass

        if not all_text.strip():
            continue

        score, emo_count, word_matches = sentiment_score(all_text)

        # Get tier from main analysis if available
        tier = "unknown"
        # Check if contact matches a known chat
        # Use matching against tp per_contact keys
        for chat_name in tp["per_contact"].keys():
            chat_lower = chat_name.lower().replace("_", "").replace(" ", "")
            contact_lower = contact_name.lower().replace("_", "").replace(" ", "")
            if chat_lower == contact_lower or chat_lower in contact_lower or contact_lower in chat_lower:
                # Get tier from rec
                rec_info = rec["per_chat"].get(chat_name, {})
                tier = rec_info.get("tier", "unknown")
                break

        by_contact[contact_name] = {
            "tier": tier,
            "transcript_count": transcript_count,
            "sentiment_score": round(score, 3),
            "emotional_word_count": emo_count,
            "word_matches": word_matches,
            "text_length": len(all_text),
        }
        by_tier[tier].append(by_contact[contact_name])

    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_contacts_analyzed": len(by_contact),
        "by_tier": {tier: len(items) for tier, items in by_tier.items()},
        "per_contact": by_contact,
    }

    out = ANALYSIS / "vnt_sentiment.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"Wrote {out.relative_to(REPO)}")

    # Print findings
    print(f"\n=== VNT Sentiment Summary ===")
    print(f"Total contacts with transcripts: {len(by_contact)}")

    # Top positive
    positive = sorted(
        [(c, info) for c, info in by_contact.items() if info["word_matches"] >= 5],
        key=lambda x: -x[1]["sentiment_score"]
    )[:10]
    print(f"\nTop 10 most positive contacts:")
    for c, info in positive:
        print(f"  {info['sentiment_score']:+.2f}  {c[:40]}")

    # Top negative
    negative = sorted(
        [(c, info) for c, info in by_contact.items() if info["word_matches"] >= 5],
        key=lambda x: x[1]["sentiment_score"]
    )[:10]
    print(f"\nTop 10 most negative contacts:")
    for c, info in negative:
        print(f"  {info['sentiment_score']:+.2f}  {c[:40]}")

    # Most emotional
    emotional = sorted(
        [(c, info) for c, info in by_contact.items()],
        key=lambda x: -x[1]["emotional_word_count"]
    )[:10]
    print(f"\nTop 10 most emotional contacts (by emotion word count):")
    for c, info in emotional:
        print(f"  {info['emotional_word_count']:>4} emo-words  {c[:40]}")


if __name__ == "__main__":
    analyze_vnt_sentiment()
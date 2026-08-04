#!/usr/bin/env python3
"""
LOVE LANGUAGE ANALYSIS — How Ivan expresses love, care, and affection.

Hypothesis-driven scan of 505K messages + 17K voice transcripts to find
empirical evidence of Ivan's love modalities across the 5 love languages
(words, acts of service, gifts, time, physical touch) PLUS repair-language,
shadow-language (what he can't say), and per-contact breakdown.

Output: love_language_analysis.json + prints summary.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH/wa_messages"
VNT = REPO / "SOURCE_OF_TRUTH/voice_note_transcripts"
ANALYSIS = WA / "_ANALYSIS"


# ============================================================
# LEXICONS — 7 love-related categories, each with weighted markers
# ============================================================

# 1. AFFECTIONATE WORDS (verbal affirmation)
LEX_WORDS = {
    "es": [
        "te quiero", "te amo", "te adoro", "amor", "mi amor", "mi vida",
        "cariño", "cari", "corazón", "hermano", "hermana", "bro",
        "família", "love u", "love you", "te extraño", "te adoro",
        "preciosa", "precioso", "guapa", "guapo", "hermosa", "hermoso",
        "rey", "reina", "lindo", "linda", "bello", "bella",
        "lovely", "precious", "baby", "babe", "cariño mío",
        "te quiero mucho", "te amo mucho", "te adoro mucho",
    ],
    "en": [
        "i love you", "love u", "love you", "ily", "love ya",
        "i miss you", "miss u", "babe", "baby", "honey", "sweetheart",
        "darling", "dear", "gorgeous", "beautiful", "handsome",
        "you're amazing", "you mean a lot", "love of my life",
    ],
    "emoji": ["❤️", "💕", "💖", "💗", "💝", "🥰", "😍", "🤗", "💞"],
}

# 2. ACTS OF SERVICE (doing things for people)
LEX_ACTS = {
    "es": [
        "te llevo", "te traigo", "te paso", "te consigo", "te busco",
        "te ayudo", "te cuido", "te cocino", "te preparo", "te mando",
        "te resuelvo", "te organizo", "te planifico", "te resuelvo",
        "te arreglo", "te limpio", "voy a tu casa", "voy a verte",
        "pasando por", "te recojo", "te acerco", "te acerco",
        "pido por ti", "hablo por ti", "pregunto por ti",
        "te recomiendo", "te derivo", "te conecto con",
    ],
    "en": [
        "i'll get you", "i'll bring you", "i'll fix", "let me help",
        "i'll do it", "i'll handle", "i'll take care", "i got you",
        "i'll pick you up", "i'll drop off", "i'll send you",
        "let me handle that", "i'll set it up", "i'll plan",
        "i'll cook", "i'll clean", "i'll organize",
    ],
}

# 3. GIFT-GIVING (including sharing memes, links, songs as proxy)
LEX_GIFTS = {
    "es": [
        "te regalo", "te compré", "te conseguí", "mira esto para ti",
        "te paso esto", "te mando esto", "pensé en ti cuando vi",
        "vi esto y pensé en vos", "te traje", "para vos",
        "esto es para ti", "esto es tuyo",
    ],
    "en": [
        "i got you this", "i bought you", "made for you", "this is for you",
        "saw this and thought of you", "i'll send you",
        "picked this up for you", "saved this for you",
    ],
}

# 4. QUALITY TIME / PRESENCE (being-there markers)
LEX_TIME = {
    "es": [
        "estoy con vos", "estoy aquí", "estoy ahi", "cuenta conmigo",
        "voy a estar", "me quedo", "estemos juntos", "juntémonos",
        "te acompaño", "te espero", "estoy pensando en vos",
        "estuve pensando", "te llamo", "videollamada", "llamamos",
        "hablamos", "me escapé para", "pase por", "pasé por",
        "te visito", "visítame", "quedate", "quédate",
    ],
    "en": [
        "i'm here", "i'm with you", "i'll be there", "staying with",
        "let's hang", "let's meet", "call me", "call you",
        "video call", "i'll visit", "come over", "staying up",
        "thinking about you", "i was thinking about",
    ],
}

# 5. PHYSICAL TOUCH (verbal references to touch)
LEX_TOUCH = {
    "es": [
        "abrazar", "abrazo", "abrazos", "beso", "besito", "besitos",
        "cariña", "acariciar", "mimar", "te abrazo", "dame un beso",
        "abrazame", "abrázame", "cucharita", "cuchito", "cuidado",
        "te cuido", "te tengo", "en brazos", "mimos", "mimitos",
    ],
    "en": [
        "hug", "hugs", "kiss", "kisses", "cuddle", "cuddles",
        "hold me", "hold you", "touch", "caress", "stroke",
        "pat", "head pat", "snuggle", "physical touch",
    ],
}

# 6. REPAIR LANGUAGE (initiating after conflict / gap)
LEX_REPAIR = {
    "es": [
        "perdón", "perdona", "disculpa", "disculpá", "lo siento",
        "fue mi culpa", "no quise", "no era mi intención",
        "hablemos", "podemos hablar", "necesito hablarte",
        "estuve pensando en lo que pasó", "podemos seguir",
        "te extraño", "pensé en vos", "cómo estás",
        "hace mucho que no hablamos", "hace tiempo que no",
        "te busco para", "perdón por tardar", "perdón la demora",
        "te debo una disculpa", "tengo que pedirte perdón",
    ],
    "en": [
        "sorry", "i apologize", "my bad", "my fault", "i messed up",
        "let's talk", "can we talk", "i miss you", "how are you",
        "been thinking about", "long time no talk", "long time no",
        "i owe you", "forgive me",
    ],
}

# 7. SHADOW LANGUAGE (what he wants to say but can't)
#    Phrases that come up when Ivan expresses frustration at his own inability
LEX_SHADOW = {
    "es": [
        "no sé expresar", "no sé decirte", "no sé cómo decir",
        "no me sale", "me cuesta", "me cuesta decirlo",
        "no sé hablar", "no sé comunicar", "no puedo decirte",
        "quisiera decirte", "ojalá pudiera", "quisiera poder",
        "te quiero pero no sé", "te amo pero me cuesta",
        "soy malo para", "soy pésimo para", "no se me da",
        "te quiero y no sé decirlo",
    ],
    "en": [
        "i don't know how to say", "can't express", "hard to say",
        "don't know how to tell", "struggle to express", "bad at expressing",
        "wish i could say", "i want to tell you but",
    ],
}


# Contact name → friendly name (for output)
CONTACT_SLUGS = {
    "tier1_deep/02__p8816___wa_chat_595983008816_9253": "Cousin_Friend_8816",
    "tier1_deep/05__lourdes_youko_kurama___wa_chat_595981791823_1683": "Lourdes_Youko",
    "tier1_deep/06__p4569___wa_chat_595981324569_1092": "Friend_4569",
    "tier1_deep/10__alejandro_cabral___wa_chat_595972130867_49": "Alejandro_Cabral_Poli",
    "tier1_deep/11__gabriella_gp___wa_export_2026": "Gabriella_GP_Ometz",
    "tier1_deep/Grandpa_Jan_Van_Der_Pol": "Grandpa_Jan",
    "tier1_deep/jonathan_verdun___wa_chat_595971922708_3654": "Jonatan_Verdun",
    "tier1_deep/laura____wa_chat_595976538689_3231": "Laura_Ex_Partner",
    "tier1_deep/magali_carreras_amiga_fpuna____wa_chat_595981225272_62": "Magali_Carreras_Fpuna",
    "tier1_deep/mom_sonia_weiss___wa_chat_595982515138_64": "Mom_Sonia_Weiss",
    "tier1_deep/sister_kyrian_kiki___wa_chat_595985724135_111": "Sister_Kyrian_Kiki",
}


def compile_lex(lex):
    """Compile lexicon → list of compiled regexes."""
    out = []
    for lang in ["es", "en", "emoji"]:
        for term in lex.get(lang, []):
            if lang == "emoji":
                out.append(("emoji", re.compile(re.escape(term))))
            else:
                # case-insensitive, word boundaries not strict (catches "te quiero mucho" etc.)
                out.append((lang, re.compile(re.escape(term), re.IGNORECASE)))
    return out


COMPILED = {
    "words":   compile_lex(LEX_WORDS),
    "acts":    compile_lex(LEX_ACTS),
    "gifts":   compile_lex(LEX_GIFTS),
    "time":    compile_lex(LEX_TIME),
    "touch":   compile_lex(LEX_TOUCH),
    "repair":  compile_lex(LEX_REPAIR),
    "shadow":  compile_lex(LEX_SHADOW),
}


def scan_message(text: str, compiled_lex):
    """Return set of categories hit in this message."""
    if not text:
        return set()
    hits = set()
    for cat, terms in compiled_lex.items():
        for lang, rx in terms:
            if rx.search(text):
                hits.add(cat)
                break
    return hits


def analyze():
    """Run full corpus scan."""
    tiers = [
        "tier1_deep", "tier2_core", "tier3_extended",
        "untiered_personal", "other_lid",
        # tier4_groups skipped — group context dilutes personal love markers
    ]

    # Global counters
    by_category_total = defaultdict(int)
    by_chat = defaultdict(lambda: defaultdict(int))   # chat -> cat -> count
    by_chat_ivan_out = defaultdict(int)                # chat -> Ivan outgoing text msgs
    by_chat_ivan_in = defaultdict(int)                 # chat -> incoming msgs

    # Time buckets: 22-04 vs day
    by_category_late_night = defaultdict(int)
    by_category_daytime = defaultdict(int)

    # Evidence snippets per chat per category (for quotes)
    evidence = defaultdict(lambda: defaultdict(list))

    chats_processed = 0
    messages_scanned = 0

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
            except Exception:
                continue

            msgs = data.get("messages", [])
            if not msgs:
                continue

            chat_key = f"{tier}/{chat.name}"
            friendly = CONTACT_SLUGS.get(chat_key, chat.name)

            for m in msgs:
                text = m.get("text") or ""
                if not text:
                    continue

                ts = m.get("ts_ms", 0)
                # Hour-of-day (Paraguay = UTC-4 approx; using UTC for simplicity, adjust 22-04 PY = 02-08 UTC)
                # PY is UTC-4 → PY 22:00 = UTC 02:00. Late-night PY = UTC 02:00-08:00.
                hour_utc = datetime.utcfromtimestamp(ts / 1000).hour
                is_late = (2 <= hour_utc <= 8)  # roughly 22:00-04:00 PY

                is_from_ivan = bool(m.get("from_me"))

                # Only analyze IVAN'S outgoing messages for love-expression
                # (he's the subject)
                if not is_from_ivan:
                    by_chat_ivan_in[friendly] += 1
                    continue

                messages_scanned += 1
                by_chat_ivan_out[friendly] += 1

                hits = scan_message(text, COMPILED)
                for cat in hits:
                    by_category_total[cat] += 1
                    by_chat[friendly][cat] += 1
                    if is_late:
                        by_category_late_night[cat] += 1
                    else:
                        by_category_daytime[cat] += 1

                    # Save 2 evidence snippets per (chat, cat)
                    if len(evidence[friendly][cat]) < 5:
                        snip = text.strip()[:280]
                        if len(text) > 280:
                            snip += "…"
                        evidence[friendly][cat].append({
                            "ts": m.get("ts_iso"),
                            "text": snip,
                        })

            chats_processed += 1

    # Voice note transcripts — Ivan's own voice notes are in folders named like his JID,
    # but we don't have per-speaker labels easily. Scan all transcripts and aggregate by folder.
    # For now, just scan all transcripts for Ivan-authored content (his voice notes to specific people).

    vnt_stats = defaultdict(lambda: defaultdict(int))
    vnt_total_by_cat = defaultdict(int)
    vnt_files_scanned = 0

    if VNT.exists():
        for folder in VNT.iterdir():
            if not folder.is_dir():
                continue
            if folder.name.startswith("_"):
                continue
            for tf in folder.glob("*.txt"):
                try:
                    text = tf.read_text(errors="ignore")
                except Exception:
                    continue
                if not text.strip():
                    continue
                vnt_files_scanned += 1
                hits = scan_message(text, COMPILED)
                for cat in hits:
                    vnt_stats[folder.name][cat] += 1
                    vnt_total_by_cat[cat] += 1

    # ============================================================
    # BUILD OUTPUT
    # ============================================================

    # Per-chat breakdown — top 30 most expressive
    chat_summary = []
    for chat, counts in by_chat.items():
        ivan_out = by_chat_ivan_out[chat]
        ivan_in = by_chat_ivan_in.get(chat, 0)
        total = sum(counts.values())
        # Normalize: per 1000 outgoing messages
        per_k = (total / ivan_out * 1000) if ivan_out else 0
        chat_summary.append({
            "chat": chat,
            "ivan_outgoing_msgs": ivan_out,
            "ivan_incoming_msgs": ivan_in,
            "love_markers_total": total,
            "per_1000_outgoing": round(per_k, 2),
            "by_category": dict(counts),
            "modalities_active": sum(1 for c in counts.values() if c > 0),
            "top_modality": max(counts, key=counts.get) if counts else None,
        })

    chat_summary.sort(key=lambda x: x["love_markers_total"], reverse=True)

    # Late-night vs daytime ratio
    late_vs_day = {}
    for cat in by_category_total:
        total = by_category_late_night[cat] + by_category_daytime[cat]
        late_vs_day[cat] = {
            "late_night_pct": round(by_category_late_night[cat] / total * 100, 1) if total else 0,
            "total": total,
        }

    output = {
        "metadata": {
            "generated": datetime.utcnow().isoformat() + "Z",
            "purpose": "Empirical analysis of how Ivan Weiss expresses love, care, and affection",
            "scope": "Ivan's outgoing text messages + voice note transcripts",
            "method": "Regex lexicon scan across 7 love-language categories (Words, Acts, Gifts, Time, Touch, Repair, Shadow)",
            "note": "Group chats (tier4) excluded — dilutes personal signals. VNT scanned as supplementary evidence.",
            "lexicons": {
                "words": sum(len(v) for v in LEX_WORDS.values()),
                "acts":  sum(len(v) for v in LEX_ACTS.values()),
                "gifts": sum(len(v) for v in LEX_GIFTS.values()),
                "time":  sum(len(v) for v in LEX_TIME.values()),
                "touch": sum(len(v) for v in LEX_TOUCH.values()),
                "repair":sum(len(v) for v in LEX_REPAIR.values()),
                "shadow":sum(len(v) for v in LEX_SHADOW.values()),
            },
        },
        "corpus_stats": {
            "chats_processed": chats_processed,
            "ivan_messages_scanned": messages_scanned,
            "vnt_files_scanned": vnt_files_scanned,
        },
        "category_totals_text": dict(by_category_total),
        "category_totals_voice": dict(vnt_total_by_cat),
        "late_night_distribution": late_vs_day,
        "top_30_chats_by_love_markers": chat_summary[:30],
        "top_30_chats_by_density": sorted(chat_summary, key=lambda x: x["per_1000_outgoing"], reverse=True)[:30],
        "evidence_per_chat": {chat: dict(cats) for chat, cats in evidence.items()},
        "vnt_breakdown_top_30": sorted(
            [
                {"contact": k, "by_category": dict(v), "total": sum(v.values())}
                for k, v in vnt_stats.items()
            ],
            key=lambda x: x["total"],
            reverse=True,
        )[:30],
    }

    # Save
    out_path = ANALYSIS / "love_language_analysis.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"✅ Wrote {out_path}")
    print(f"   {chats_processed} chats, {messages_scanned:,} Ivan outgoing msgs, "
          f"{vnt_files_scanned} VNT files scanned")

    # Print top findings
    print("\n═══ LOVE LANGUAGE TOTALS (text, Ivan outgoing) ═══")
    for cat in ["words", "acts", "gifts", "time", "touch", "repair", "shadow"]:
        c = by_category_total.get(cat, 0)
        ln = by_category_late_night.get(cat, 0)
        dy = by_category_daytime.get(cat, 0)
        pct = round(ln / (ln + dy) * 100, 1) if (ln + dy) else 0
        print(f"   {cat:<8} {c:>6}  ({ln} late-night / {dy} day = {pct}% late)")

    print("\n═══ VOICE NOTE TOTALS (Ivan's voice to others) ═══")
    for cat, c in sorted(vnt_total_by_cat.items(), key=lambda x: -x[1]):
        print(f"   {cat:<8} {c:>6}")

    print("\n═══ TOP 15 CHATS BY LOVE MARKERS (raw count) ═══")
    for c in chat_summary[:15]:
        print(f"   {c['chat'][:50]:<50} {c['love_markers_total']:>5}  "
              f"[{c['top_modality']}]")

    print("\n═══ TOP 15 CHATS BY DENSITY (per 1000 msgs) ═══")
    for c in sorted(chat_summary, key=lambda x: x["per_1000_outgoing"], reverse=True)[:15]:
        print(f"   {c['chat'][:50]:<50} {c['per_1000_outgoing']:>6.2f}  "
              f"[{c['top_modality']}]")

    return output


if __name__ == "__main__":
    analyze()
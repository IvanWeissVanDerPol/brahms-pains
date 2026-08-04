#!/usr/bin/env python3
"""Topic/keyword extraction per chat (Hat 14, 17)."""

from __future__ import annotations

import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH/wa_messages"
ANALYSIS = WA / "_ANALYSIS"

# Topic indicators - Spanish + English
TOPICS = {
    "kink_bdsm": [
        "dom",
        "sub",
        "kink",
        "bdsm",
        "rigger",
        "rope",
        "shibari",
        "femdom",
        "play",
        "scene",
        "owner",
    ],
    "dental_clinic": [
        "dental",
        "dentist",
        "clinic",
        "paciente",
        "consultorio",
        "diente",
        "muela",
        "ortodoncia",
        "endodoncia",
    ],
    "ai_tech": [
        "ai",
        "ml",
        "llm",
        "model",
        "agent",
        "claude",
        "gpt",
        "anthropic",
        "openai",
        "hermes",
        "langchain",
    ],
    "family": [
        "mama",
        "papa",
        "momi",
        "daddy",
        "abuela",
        "abuelo",
        "primo",
        "tio",
        "polo",
        "kiki",
        "luana",
    ],
    "intimacy_romance": [
        "amor",
        "love",
        "te quiero",
        "cariño",
        "beso",
        "abrazo",
        "cari",
        "hermosa",
        "lindo",
        "precioso",
    ],
    "work_projects": [
        "proyecto",
        "project",
        "trabajo",
        "client",
        "cliente",
        "ometz",
        "paragu-ai",
        "sunstone",
    ],
    "school_study": [
        "examen",
        "final",
        "tarea",
        "profesor",
        "facultad",
        "universidad",
        "fpuna",
        "uca",
    ],
    "exercise_gym": ["gym", "gimnasio", "ejercicio", "workout", "correr", "pesas", "cardio"],
    "food": [
        "comida",
        "comer",
        "cena",
        "almuerzo",
        "desayuno",
        "pizza",
        "empanada",
        "asado",
        "comer",
        "cocinar",
    ],
    "kink_kinky": ["sumisa", "sumiso", "dueño", "dueña", "amo", "ama", "castigo", "recompensa"],
    "psychology_therapy": [
        "terapia",
        "psicologo",
        "psicologa",
        "ansiedad",
        "depresion",
        "trauma",
        "ataque",
    ],
    "social_events": [
        "fiesta",
        "evento",
        "cumpleaños",
        "birthday",
        "reunion",
        "quedamos",
        "salimos",
    ],
    "money_finance": [
        "plata",
        "guarani",
        "guaranies",
        "dolares",
        "dolares",
        "money",
        "transferencia",
        "banco",
    ],
    "music_art": [
        "musica",
        "song",
        "rock",
        "bar",
        "tokio",
        "canción",
        "artista",
        "pintura",
        "pintar",
    ],
}


def analyze_topics():
    """Extract topic mentions per chat."""
    by_chat = {}

    tiers = [
        "tier1_deep",
        "tier2_core",
        "tier3_extended",
        "tier4_groups",
        "untiered_personal",
        "other_lid",
    ]

    patterns = {}
    for topic, terms in TOPICS.items():
        patterns[topic] = [re.compile(r"\b" + re.escape(t) + r"\b", re.IGNORECASE) for t in terms]

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
            text_msgs = [m for m in msgs if isinstance(m, dict) and m.get("text")]

            if not text_msgs:
                continue

            # Count topic mentions
            topic_counts = defaultdict(int)
            for m in text_msgs:
                text = m["text"]
                for topic, pats in patterns.items():
                    for pat in pats:
                        matches = pat.findall(text)
                        if matches:
                            topic_counts[topic] += len(matches)

            # Only include chats with >= 100 messages and at least 5 topic mentions
            if len(text_msgs) < 100 or sum(topic_counts.values()) < 5:
                continue

            # Top topics for this chat
            top_topics = sorted(topic_counts.items(), key=lambda x: -x[1])[:3]
            if not top_topics:
                continue

            primary = top_topics[0][0]
            primary_density = top_topics[0][1] / len(text_msgs)

            by_chat[chat_name] = {
                "tier": tier,
                "total_text_msgs": len(text_msgs),
                "topic_counts": dict(topic_counts),
                "primary_topic": primary,
                "primary_density": round(primary_density, 4),
                "top_3_topics": top_topics,
            }

    # Categorize by primary topic
    topic_groups = defaultdict(list)
    for c, info in by_chat.items():
        topic_groups[info["primary_topic"]].append((c, info))

    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_chats_analyzed": len(by_chat),
        "topic_distribution": {t: len(chats) for t, chats in topic_groups.items()},
        "per_chat": by_chat,
    }

    out = ANALYSIS / "topic_extraction.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"Wrote {out.relative_to(REPO)}")

    print("\n=== Topic Extraction Analysis ===")
    print(f"Total analyzed: {len(by_chat)}")
    print("\nTopic distribution:")
    for topic, count in sorted(summary["topic_distribution"].items(), key=lambda x: -x[1]):
        print(f"  {topic:<25}: {count}")

    # Top chat per topic
    for topic in ["kink_bdsm", "dental_clinic", "ai_tech", "family", "intimacy_romance"]:
        if topic in topic_groups:
            print(f"\nTop 5 {topic} chats:")
            for c, info in sorted(topic_groups[topic], key=lambda x: -x[1]["topic_counts"][topic])[
                :5
            ]:
                print(f"  {info['topic_counts'][topic]:>3} mentions  {c[:40]}")


if __name__ == "__main__":
    analyze_topics()

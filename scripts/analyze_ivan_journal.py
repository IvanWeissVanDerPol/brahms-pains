#!/usr/bin/env python3
"""Extract business insights from _documents_ivan_voice."""

from __future__ import annotations

import json
import re
from pathlib import Path
from datetime import datetime

REPO = Path("/root/psycology")
JOURNAL_DIR = REPO / "SOURCE_OF_TRUTH/voice_note_transcripts/_documents_ivan_voice"

# Topics to extract
DENTISTRY_KEYWORDS = [
    "dentista",
    "dentist",
    "dental",
    "consultorio",
    "paciente",
    "pacientes",
    "limpieza",
    "profilaxis",
    "implante",
    "implantes",
    "corona",
    "coronas",
    "caries",
    "restauración",
    "restauraciones",
    "operatoria",
    "endodoncia",
    "cirugía",
    "maxilar",
    "oclusal",
    "periodoncia",
    "ortodoncia",
    "radiografía",
    "tac",
    "cbct",
    "rayos x",
    "arsenal",
    "turbina",
    "micromotor",
    "compresor",
]

PRICING_KEYWORDS = [
    "precio",
    "precios",
    "costo",
    "costos",
    "cobrar",
    "cobro",
    "cobran",
    "factura",
    "facturación",
    "arsenal",
    "honorario",
    "honorarios",
    "280 mil",
    "300 mil",
    "consulta",
    "urgencia",
]

WEBSITE_KEYWORDS = [
    "web",
    "página",
    "website",
    "google",
    "seo",
    "search engine",
    "ai search",
    "google maps",
    "mapa",
    "redes sociales",
    "facebook",
    "instagram",
    "tiktok",
    "calendly",
    "agenda",
    "google calendar",
    "messaging business",
    "5 quick replies",
    "mensaje",
    "mensajes",
]

TARGETING_KEYWORDS = [
    "expat",
    "expats",
    "expatriate",
    "expatriota",
    "expatriotas",
    "gringo",
    "gringos",
    "americano",
    "estadounidense",
    "inglés",
    "english",
    "trilingüe",
    "bilingüe",
]

LOCATION_KEYWORDS = [
    "asunción",
    "asu",
    "luque",
    "burguilla",
    "fernando",
    "fernando de la mora",
    "san lorenzo",
    "lambaré",
    "capiatá",
    "itauguá",
]

TIMELINE_KEYWORDS = [
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
    "trimestre",
    "semana",
    "mes",
    "fecha",
]


# Spanish language processing - extract key sentences
def extract_key_sentences(text: str, keywords: list[str]) -> list[str]:
    sentences = re.split(r"[.!?]\s+", text)
    found = []
    for sent in sentences:
        sent = sent.strip()
        if 30 < len(sent) < 300:
            for kw in keywords:
                if kw.lower() in sent.lower():
                    found.append(sent)
                    break
    return found


def main():
    print("Loading journal entries...")
    entries = []
    for f in JOURNAL_DIR.glob("*.json"):
        try:
            arr = json.loads(f.read_text())
            if isinstance(arr, list):
                entries.extend(arr)
        except:
            pass
    entries.sort(key=lambda e: e.get("file", ""))

    total_duration = sum(e.get("duration", 0) or 0 for e in entries)
    total_words = sum(len(re.findall(r"\b\w+\b", e.get("text", ""))) for e in entries)

    print(f"Loaded {len(entries)} entries")
    print(f"Total duration: {total_duration/60:.1f} min ({total_duration:.0f}s)")
    print(f"Total words: {total_words:,}")

    # Aggregate findings
    findings = {
        "dentistry": [],
        "pricing": [],
        "website": [],
        "targeting": [],
        "location": [],
        "timeline": [],
    }

    for e in entries:
        text = e.get("text", "")
        findings["dentistry"].extend(extract_key_sentences(text, DENTISTRY_KEYWORDS))
        findings["pricing"].extend(extract_key_sentences(text, PRICING_KEYWORDS))
        findings["website"].extend(extract_key_sentences(text, WEBSITE_KEYWORDS))
        findings["targeting"].extend(extract_key_sentences(text, TARGETING_KEYWORDS))
        findings["location"].extend(extract_key_sentences(text, LOCATION_KEYWORDS))
        findings["timeline"].extend(extract_key_sentences(text, TIMELINE_KEYWORDS))

    # Specific things Ivan mentioned
    specific_extractions = []
    # Look for "burguilla asunción" / location mentions
    for e in entries:
        text = e.get("text", "")
        # Detect specific phrases
        patterns = {
            "business_name": r"(?:nombre\s+comercial|marca)\s+es\s+([^\.]+)",
            "price": r"(\d+)\s*(?:mil|guaran(?:í|ies))",
            "open_date": r"(?:julio|agosto|septiembre)\s+de\s+\d{4}",
            "consultorio": r"consultorio\s+(?:en|de)\s+([^\.]+)",
        }
        for label, pattern in patterns.items():
            for m in re.finditer(pattern, text, re.IGNORECASE):
                specific_extractions.append(
                    {
                        "type": label,
                        "value": m.group(0),
                        "context": text[max(0, m.start() - 50) : m.end() + 50],
                    }
                )

    # Save
    out = {
        "generated_at": datetime.now().isoformat(),
        "source": "_documents_ivan_voice",
        "description": "Ivan's voice journal — business planning, conversations with AI assistants",
        "entries_count": len(entries),
        "total_duration_minutes": round(total_duration / 60, 1),
        "total_words": total_words,
        "entries_summary": [
            {
                "file": e.get("file"),
                "duration_minutes": round((e.get("duration", 0) or 0) / 60, 1),
                "word_count": len(re.findall(r"\b\w+\b", e.get("text", ""))),
                "language": e.get("language", "?"),
                "preview": (e.get("text", "") or "")[:200],
            }
            for e in entries
        ],
        "topics": {
            "dentistry_sentences": findings["dentistry"][:30],
            "pricing_sentences": findings["pricing"][:30],
            "website_sentences": findings["website"][:30],
            "targeting_sentences": findings["targeting"][:30],
            "location_sentences": findings["location"][:20],
            "timeline_sentences": findings["timeline"][:20],
        },
        "specific_extractions": specific_extractions[:50],
    }

    out_path = REPO / "SOURCE_OF_TRUTH/voice_note_transcripts/_documents_ivan_voice/analysis.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"\nWrote {out_path.relative_to(REPO)}")
    print()
    print("=== Key extracts ===")
    print(f"\n📍 LOCATION MENTIONS ({len(findings['location'])} sentences):")
    for s in findings["location"][:5]:
        print(f"  - {s[:200]}")

    print(f"\n💰 PRICING MENTIONS ({len(findings['pricing'])} sentences):")
    for s in findings["pricing"][:5]:
        print(f"  - {s[:200]}")

    print(f"\n🌐 WEBSITE/SEO MENTIONS ({len(findings['website'])} sentences):")
    for s in findings["website"][:5]:
        print(f"  - {s[:200]}")

    print(f"\n🎯 TARGETING (expat/gringo/English) ({len(findings['targeting'])} sentences):")
    for s in findings["targeting"][:5]:
        print(f"  - {s[:200]}")


if __name__ == "__main__":
    main()

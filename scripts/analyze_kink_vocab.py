#!/usr/bin/env python3
"""Kink vocabulary analysis (Hat 21, 26)."""
from __future__ import annotations

import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH/wa_messages"
ANALYSIS = WA / "_ANALYSIS"

# Kink vocabulary lexicon (Spanish + English)
KINK_TERMS = {
    "dom_dynamics": [
        "dom", "doms", "dominant", "dominatrix", "femdom", "owner", "master", "mistress",
        "dueño", "dueña", "amo", "ama", "sumisa", "sumiso", "daddy", "mommy", "mami",
        "papi", "jefe", "jefa", "handler"
    ],
    "sub_dynamics": [
        "sub", "subs", "submissive", "pet", "puppy", "kitten", "kitty", "brat", "slave",
        "bratty", "toy", "bottom", "service", "service-top"
    ],
    "scenes_activities": [
        "scene", "scenes", "play", "session", "rope", "shibari", "rig", "rigger", "rigging",
        "tie", "ties", "tie-up", "bondage", "cage", "cell", "worship", "service",
        "whip", "spank", "spanking", "paddling", "flogging", "candle", "wax",
        "edge", "edging", "denial", "orgasm", "control", "impact"
    ],
    "protocols": [
        "protocol", "rules", "rule", "boundaries", "limits", "limits_check",
        "safe_word", "safeword", "check_in", "aftercare", "scene_negotiation",
        "negotiation", "consent", "dynamic", "d/s", "m/s", "ddlg", "mdlg",
        "owner", "owned", "collared", "protocol"
    ],
    "physical_sensation": [
        "pain", "pleasure", "hurt", "sore", "marks", "bruises", "marks",
        "intensity", "edge", "overwhelm", "sensation", "touch", "caress"
    ],
    "psychological": [
        "headspace", "space", "drop", "subdrop", "topdrop", "aftercare",
        "emotional", "trigger", "trauma", "processing", "kink", "kinky",
        "fetish", "taboo", "shame", "permission", "brahm"
    ],
}

# Compile patterns
PATTERNS = {}
for category, terms in KINK_TERMS.items():
    PATTERNS[category] = [re.compile(r'\b' + re.escape(t) + r'\b', re.IGNORECASE) for t in terms]


def analyze_kink_vocab():
    """Analyze kink vocabulary across chats."""
    by_chat = {}

    tiers = ["tier1_deep", "tier2_core", "tier3_extended", "untiered_personal", "other_lid"]

    # First identify potential kink chats
    kink_keywords_total = ["BDSM", "femdom", "kink", "sub", "dom", "punishment", "rigger",
                          "rope", "shibari", "fetish", "slave", "owner", "kitten", "puppy",
                          "brat", "aftercare", "play"]

    tier4 = WA / "tier4_groups"

    candidate_chats = set()

    # Check tier4_groups first (likely kink groups)
    if tier4.exists():
        for chat in tier4.iterdir():
            if not chat.is_dir():
                continue
            name = chat.name.lower()
            if any(k.lower() in name for k in kink_keywords_total):
                candidate_chats.add(("tier4_groups", chat))

    # Then check 1:1 for kink keywords
    for tier in tiers:
        d = WA / tier
        if not d.exists():
            continue
        for chat in d.iterdir():
            if not chat.is_dir():
                continue
            name = chat.name.lower()
            if any(k.lower() in name for k in kink_keywords_total):
                candidate_chats.add((tier, chat))

    print(f"Candidate kink chats identified: {len(candidate_chats)}")

    # Analyze each candidate
    for tier, chat in candidate_chats:
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

        # Count kink vocabulary
        category_counts = defaultdict(int)
        total_kink_words = 0

        for m in msgs:
            if not isinstance(m, dict):
                continue
            text = m.get("text") or ""
            if not text:
                continue

            for category, patterns in PATTERNS.items():
                for pattern in patterns:
                    matches = pattern.findall(text)
                    if matches:
                        category_counts[category] += len(matches)
                        total_kink_words += len(matches)

        if total < 10:
            continue

        by_chat[chat_name] = {
            "tier": tier,
            "total_msgs": total,
            "total_kink_words": total_kink_words,
            "kink_density": round(total_kink_words / total, 3) if total > 0 else 0,
            "by_category": dict(category_counts),
        }

    # Sort by kink_density
    sorted_chats = sorted(by_chat.items(), key=lambda x: -x[1]["kink_density"])

    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_kink_chats": len(by_chat),
        "per_chat": by_chat,
        "lexicon_categories": list(KINK_TERMS.keys()),
    }

    out = ANALYSIS / "kink_vocabulary.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"Wrote {out.relative_to(REPO)}")

    print(f"\n=== Kink Vocabulary Analysis ===")
    print(f"Total kink chats analyzed: {len(by_chat)}")

    # Overall stats
    if by_chat:
        total_kw = sum(c["total_kink_words"] for c in by_chat.values())
        total_msgs = sum(c["total_msgs"] for c in by_chat.values())
        print(f"Total kink vocabulary words: {total_kw}")
        print(f"Total msgs in kink chats: {total_msgs}")
        print(f"Overall kink density: {total_kw / total_msgs:.3f}")

    # Top 15 kink-dense chats
    print(f"\nTop 15 kink-dense chats:")
    for c, info in sorted_chats[:15]:
        print(f"  {info['kink_density']:.3f}  {info['total_kink_words']:>4} words  "
              f"{info['tier']:<20}  {c[:30]}")

    # Category totals
    print(f"\nCategory totals across all kink chats:")
    cat_totals = defaultdict(int)
    for c, info in by_chat.items():
        for cat, count in info["by_category"].items():
            cat_totals[cat] += count
    for cat, total in sorted(cat_totals.items(), key=lambda x: -x[1]):
        print(f"  {cat:<20}: {total}")


if __name__ == "__main__":
    analyze_kink_vocab()
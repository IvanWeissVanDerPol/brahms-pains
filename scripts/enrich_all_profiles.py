#!/usr/bin/env python3
"""Enrich ALL unenriched top-level profiles with empirical data."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DYN = REPO / "RELATIONSHIPS/dynamics"
ANALYSIS = REPO / "SOURCE_OF_TRUTH/wa_messages/_ANALYSIS"

# Load all analyses
tp = json.loads((ANALYSIS / "time_patterns.json").read_text())
init = json.loads((ANALYSIS / "initiator_analysis.json").read_text())
rec = json.loads((ANALYSIS / "recency_heatmap.json").read_text())
vvt = json.loads((ANALYSIS / "voice_vs_text.json").read_text())
tl = json.loads((ANALYSIS / "conversation_timeline.json").read_text())


def get_metrics(profile_name):
    """Get empirical metrics for a profile, trying various name patterns."""
    matches = []
    seen_chats = set()

    # Try multiple variations of the name
    variations = [
        profile_name,
        profile_name.replace("_", " "),
        profile_name.replace("POLI", "Poli"),
        profile_name.lower(),
        profile_name.replace("_", ""),
    ]

    # Special mappings
    special = {
        "ALEJANDRO_CABRAL_POLI": ["alejandro_cabral_poli", "alejandro_cabral", "10__alejandro"],
        "ALEJANDRO_CABRAL": ["10__alejandro_cabral", "alejandro_cabral"],
        "FIDABEL_POLI": ["fidabel_poli", "Defi", "DEFI"],
        "DEFI_NOT_THERE_4_U": ["Defi", "fidabel_poli"],
        "MAGALI_CARRERAS_AMIGA_FPUNA": ["magali_carreras_amiga_fpuna"],
        "LUANA_WEISS": ["sister_luana_weiss", "luana_weiss"],
        "TONI_WEISS": ["Toni_Weiss", "toni_weiss", "uncle_toni"],
        "ARA_NUNEZ_POLI": ["ara_nunez_poli"],
        "LILIAN_RIVEROS": ["lilian_riveros", "28__lilian"],
        "IVAN_WEISS_NUMERO_PRO": ["IVAN_WEISS_NUMERO_PRO"],
        "SOFI_NASHE": ["sofi_nashe", "Sof"],
        "VICTOR_DUERKSEN": ["victor", "Victor"],
        "SASKIA_WEISS": ["saskia", "Saskia"],
        "MICAELA_VELAZQUEZ": ["micaela", "Micaela", "Mica"],
        "PATINO": ["patino", "Patino"],
        "PROF_DIEGO_PINTO": ["diego", "Diego"],
        "PROF_CHRISTIAN_VON_LUCKEN": ["christian", "Christian", "von_lucken"],
        "OSVALDO_AMIGO_FPUNA": ["osvaldo", "Osvaldo"],
        "RENE_POLS_POLI": ["rene", "pols", "Pols"],
        "ROMINA_ALONZO_POLI": ["romina", "Romina"],
        "POLI_RAUL": ["raul_poli", "Raul"],
        "RAUL_WICHITA": ["raul", "wichita"],
        "NARA_MONGELOS": ["nara", "Nara", "mongelos"],
        "MICHI_CARAMELO_ALE_GOM": ["michi", "Michi", "caramelo", "Caramelo"],
        "REFRIGERACION": ["refrigeracion"],
    }

    patterns = special.get(profile_name, variations)

    # Build all search patterns: full names, first word, last word, parts
    search_patterns = set()
    for p in patterns:
        search_patterns.add(p.lower())
        # Split into parts
        parts = re.split(r"[_\s]+", p)
        for part in parts:
            if len(part) > 3:  # Skip short parts
                search_patterns.add(part.lower())

    for chat_name, info in tp["per_contact"].items():
        chat_lower = chat_name.lower()
        if any(p in chat_lower for p in search_patterns):
            if chat_name in seen_chats:
                continue
            seen_chats.add(chat_name)

            init_info = init["per_chat"].get(chat_name, {})
            rec_info = rec["per_chat"].get(chat_name, {})
            vvt_info = vvt["per_chat"].get(chat_name, {})

            matches.append(
                {
                    "chat": chat_name,
                    "tier": rec_info.get("tier", "unknown"),
                    "total_msgs": info.get("total_msgs", 0),
                    "late_night_ratio": info.get("late_night_ratio", 0),
                    "ivan_ratio": info.get("ivan_ratio", 0),
                    "peak_hour": info.get("peak_hour"),
                    "peak_dow": info.get("peak_dow"),
                    "ivan_starts": init_info.get("ivan_starts", 0),
                    "them_starts": init_info.get("them_starts", 0),
                    "max_streak": init_info.get("max_streak_days", 0),
                    "days_since": rec_info.get("days_since_last"),
                    "voice_pct": vvt_info.get("voice_pct", 0),
                }
            )

    return matches


def enrich(profile_path):
    profile_name = profile_path.stem
    content = profile_path.read_text()

    if "NEW (2026-07-27)" in content:
        return False, "already_enriched"

    matches = get_metrics(profile_name)
    if not matches:
        return False, "no_data"

    total_msgs = sum(m["total_msgs"] for m in matches)
    if total_msgs < 5:  # Skip very low-data profiles
        return False, "low_data"

    # Aggregate metrics
    avg_late = sum(m["late_night_ratio"] * m["total_msgs"] for m in matches) / total_msgs
    avg_ivan = sum(m["ivan_ratio"] * m["total_msgs"] for m in matches) / total_msgs
    total_ivan_starts = sum(m["ivan_starts"] for m in matches)
    total_them_starts = sum(m["them_starts"] for m in matches)
    total_starts = total_ivan_starts + total_them_starts
    ivan_initiator_pct = total_ivan_starts / total_starts if total_starts > 0 else 0
    avg_voice = sum(m["voice_pct"] * m["total_msgs"] for m in matches) / total_msgs
    max_streak = max((m["max_streak"] for m in matches), default=0)
    days_since = min(
        (m["days_since"] for m in matches if m["days_since"] is not None), default=None
    )
    tiers = sorted(set(m["tier"] for m in matches))

    # Clinical interpretations
    inquiries = []

    if avg_late > 0.45:
        inquiries.append(
            f"- **HIGH late-night ({avg_late:.1%})**: This contact is heavily active in Ivan's vulnerability window"
        )
    elif avg_late > 0.35:
        inquiries.append(
            f"- **Above-baseline late-night ({avg_late:.1%})**: Slightly elevated compared to Ivan's 32% baseline"
        )

    if avg_ivan > 0.7:
        inquiries.append(
            f"- **Ivan chases ({avg_ivan:.1%})**: Ivan carries most of the relational load"
        )
    elif avg_ivan < 0.3:
        inquiries.append(
            f"- **Ivan passive ({avg_ivan:.1%})**: They carry most of the relational load"
        )

    if max_streak > 100:
        inquiries.append(f"- **Long streak ({max_streak}d)**: Sustained intense engagement")
    elif max_streak > 30:
        inquiries.append(
            f"- **Moderate streak ({max_streak}d)**: Notable period of sustained contact"
        )

    if days_since and days_since > 365:
        inquiries.append(f"- **Abandoned ({days_since}d)**: Grief signal - over a year silent")
    elif days_since and days_since < 7:
        inquiries.append(f"- **Currently active ({days_since}d)**: Recent contact")

    if avg_voice > 0.15:
        inquiries.append(f"- **Voice-heavy ({avg_voice:.1%})**: Voice is primary modality")
    elif avg_voice < 0.03:
        inquiries.append(f"- **Text-only ({avg_voice:.1%})**: Distance modality")

    # Tier info
    tier_str = ", ".join(tiers)

    section = f"""

---

## 📊 NEW (2026-07-27): Empirical Profile Data

**Total messages**: {total_msgs:,}
**Chats analyzed**: {len(matches)}
**Tier(s)**: {tier_str}
**Last contact**: {f"{days_since}d ago" if days_since is not None else "unknown"}

### Time Patterns

| Metric | Value | Clinical |
|--------|------:|----------|
| Late-night ratio (22:00-04:00) | {avg_late:.1%} | {"ABOVE baseline (32%)" if avg_late > 0.4 else ("baseline" if avg_late > 0.25 else "below baseline")} |
| Peak hour | {matches[0].get("peak_hour", "?")}h | |
| Peak day | {matches[0].get("peak_dow", "?")} | |

### Initiator Dynamics

| Metric | Value | Pattern |
|--------|------:|---------|
| Ivan initiator ratio | {avg_ivan:.1%} | {"Ivan chases" if avg_ivan > 0.65 else ("Balanced" if avg_ivan > 0.35 else "They chase Ivan")} |
| Ivan starts conv | {total_ivan_starts:,} | |
| They start conv | {total_them_starts:,} | |
| Ivan initiator % | {ivan_initiator_pct:.1%} | |

### Engagement Metrics

| Metric | Value |
|--------|------:|
| Max streak (consecutive days) | {max_streak}d |
| Avg voice % | {avg_voice:.1%} |

### Clinical Inquiries

{chr(10).join(inquiries) if inquiries else "- (no notable clinical signals)"}
"""

    new_content = content + section
    profile_path.write_text(new_content)
    return True, "enriched"


if __name__ == "__main__":
    enriched = 0
    skipped = {"already_enriched": 0, "no_data": 0, "low_data": 0}

    for profile_path in sorted(DYN.glob("*.md")):
        result, reason = enrich(profile_path)
        if result:
            enriched += 1
            print(f"  ✓ {profile_path.stem}")
        else:
            skipped[reason] += 1
            if reason != "already_enriched":  # Don't spam already-enriched
                print(f"  - {profile_path.stem}: {reason}")

    print(f"\nTotal enriched this run: {enriched}")
    print(f"Skipped: {skipped}")

#!/usr/bin/env python3
"""Batch enrich 20 more profiles with empirical data."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DYN = REPO / "RELATIONSHIPS/dynamics"
ANALYSIS = REPO / "SOURCE_OF_TRUTH/wa_messages/_ANALYSIS"

# Load analyses
tp = json.loads((ANALYSIS / "time_patterns.json").read_text())
init = json.loads((ANALYSIS / "initiator_analysis.json").read_text())
rec = json.loads((ANALYSIS / "recency_heatmap.json").read_text())
vvt = json.loads((ANALYSIS / "voice_vs_text.json").read_text())

# Profile → patterns to search
TARGETS = {
    "ALEJANDRO_CABRAL_POLI": ["alejandro_cabral_poli", "alejandro_cabral", "10__alejandro_cabral"],
    "LILIAN_RIVEROS": ["lilian_riveros", "28__lilian"],
    "ALEJANDRO_CABRAL": ["10__alejandro_cabral", "alejandro_cabral"],
    "RACH": ["rach"],
    "FIDABEL_POLI": ["fidabel_poli", "Defi", "DEFI"],
    "IVAN_WEISS_NUMERO_PRO": ["IVAN_WEISS_NUMERO_PRO"],
    "MAGALI_CARRERAS_AMIGA_FPUNA": ["magali_carreras_amiga_fpuna"],
    "DAISY": ["daisy"],
    "MAIA": ["maia"],
    "TONI_WEISS": ["Toni_Weiss", "toni_weiss"],
    "LUANA_WEISS": ["sister_luana_weiss", "luana_weiss"],
    "VET_CERCA_DE_WEISSHOYSE": ["Vet_Cerca_De_Weisshoyse"],
    "IDELINE_BRISA": ["Ideline_Brisa", "Ideline_Brisa_3"],
    "MARIO_GUEYRAUD": ["mario_gueyraud"],
    "SOFI_NASHE": ["sofi_nashe"],
    "DEFI_NOT_THERE_4_U": ["Defi", "fidabel_poli"],
    "ENRIQUE_SANCHEZ": ["enrique_sanchez"],
    "ARA_NUNEZ_POLI": ["ara_nunez_poli"],
    "FRAN": ["fran"],
    "GRIDO_INGAVI": ["grido_ingavi"],
}


def get_metrics(profile_name):
    patterns = TARGETS.get(profile_name, [profile_name.lower()])
    matches = []

    for pattern in patterns:
        pattern_lower = pattern.lower()
        for chat_name, info in tp["per_contact"].items():
            if pattern_lower in chat_name.lower():
                init_info = init["per_chat"].get(chat_name, {})
                rec_info = rec["per_chat"].get(chat_name, {})
                vvt_info = vvt["per_chat"].get(chat_name, {})
                matches.append({
                    "chat": chat_name,
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
                })

    return matches


def enrich(profile_path):
    profile_name = profile_path.stem
    content = profile_path.read_text()

    if "NEW (2026-07-27)" in content:
        return False

    matches = get_metrics(profile_name)
    if not matches:
        return False

    total_msgs = sum(m["total_msgs"] for m in matches)
    if total_msgs == 0:
        return False

    avg_late = sum(m["late_night_ratio"] * m["total_msgs"] for m in matches) / total_msgs
    avg_ivan = sum(m["ivan_ratio"] * m["total_msgs"] for m in matches) / total_msgs
    total_ivan_starts = sum(m["ivan_starts"] for m in matches)
    total_them_starts = sum(m["them_starts"] for m in matches)
    ivan_initiator_pct = total_ivan_starts / (total_ivan_starts + total_them_starts) if (total_ivan_starts + total_them_starts) > 0 else 0
    avg_voice = sum(m["voice_pct"] * m["total_msgs"] for m in matches) / total_msgs
    max_streak = max((m["max_streak"] for m in matches), default=0)
    days_since = min((m["days_since"] for m in matches if m["days_since"] is not None), default=None)

    inquiries = []
    if avg_late > 0.4:
        inquiries.append(f"- What does the late-night pattern ({avg_late:.1%}) mean to you?")
    if avg_ivan > 0.65:
        inquiries.append(f"- Why does Ivan initiate {avg_ivan:.1%} of conversations?")
    if avg_ivan < 0.35:
        inquiries.append(f"- What draws them to initiate most conversations?")
    if max_streak > 30:
        inquiries.append(f"- What was the {max_streak}-day streak about?")
    if avg_voice > 0.15:
        inquiries.append(f"- What does voice ({avg_voice:.1%}) give you?")

    section = f"""

---

## 📊 NEW (2026-07-27): Empirical Profile Data

**Total messages**: {total_msgs:,}
**Chats analyzed**: {len(matches)}
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

{chr(10).join(inquiries) if inquiries else "(none)"}
"""

    new_content = content + section
    profile_path.write_text(new_content)
    return True


if __name__ == "__main__":
    enriched = 0
    for name in TARGETS:
        profile_path = DYN / f"{name}.md"
        if not profile_path.exists():
            print(f"  NOT FOUND: {name}")
            continue
        if enrich(profile_path):
            print(f"  ✓ {name}")
            enriched += 1
        else:
            print(f"  - skipped: {name}")

    print(f"\nTotal enriched: {enriched}")
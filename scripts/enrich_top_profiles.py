#!/usr/bin/env python3
"""Enrich top 10 deep relationship profiles with new empirical data."""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH/wa_messages/_ANALYSIS"
PROFILES = REPO / "RELATIONSHIPS/dynamics"

# Load new analyses
tp = json.loads((ANALYSIS / "time_patterns.json").read_text())
init = json.loads((ANALYSIS / "initiator_analysis.json").read_text())
rec = json.loads((ANALYSIS / "recency_heatmap.json").read_text())


def find_chat_for_profile(profile_name, chat_patterns):
    """Find the main chat for a profile based on patterns."""
    for chat_name in tp["per_contact"].keys():
        chat_lower = chat_name.lower()
        for pat in chat_patterns:
            if pat.lower() in chat_lower:
                return chat_name
    return None


# Profile config: (profile_file, chat_patterns, profile_label)
PROFILE_MAP = [
    {
        "profile": "LAURA.md",
        "chat_patterns": ["laura____wa_chat_595976538689_3231"],
        "label": "Laura 🐷",
        "relationship": "Primary ex-intimate / 2.7y relationship / 23k msgs",
    },
    {
        "profile": "MIKE_NYX.md",
        "chat_patterns": ["Cloud_Nyx", "nicolas_duarte"],
        "label": "Nico (Dom/Rigger) / Nyx / Cloud_Nyx",
        "relationship": "Kink partner / 3.5k msgs",
    },
    {
        "profile": "MAGALI_CARRERAS.md",
        "chat_patterns": ["magali_carreras_amiga_fpuna"],
        "label": "Magali (intimate friend)",
        "relationship": "Best friend / 28k msgs / recent #3 strongest contact",
    },
    {
        "profile": "LOURDES_YOUKO_KURAMA.md",
        "chat_patterns": ["lourdes_youko_kurama", "05__lourdes"],
        "label": "Lourdes Youko Kurama",
        "relationship": "Close friend / 16.9k msgs / 4y span",
    },
    {
        "profile": "JONATAN_VERDUN.md",
        "chat_patterns": ["jonathan_verdun", "jonatan_verdun"],
        "label": "Jonatan Verdún",
        "relationship": "High-volume friend / 34.5k msgs / 2.4y",
    },
    {
        "profile": "SONIA.md",
        "chat_patterns": ["mom_sonia_weiss"],
        "label": "Sonia Weiss (Mom)",
        "relationship": "Mother / 11.3k msgs / 5.8y",
    },
    {
        "profile": "DEFI.md",
        "chat_patterns": ["fidabel_poli", "defi"],
        "label": "Defi (Fidabel Poli)",
        "relationship": "Family friend / 2.9k msgs",
    },
    {
        "profile": "KIKI_HERMANA.md",
        "chat_patterns": ["sister_kyrian_kiki"],
        "label": "Kiki Weiss (Sister)",
        "relationship": "Sister / 7.8k msgs / 5.8y",
    },
    {
        "profile": "NICOLAS_DUARTE.md",
        "chat_patterns": ["Cloud_Nyx", "nicolas_duarte"],
        "label": "Nico/Nyx (Dom/Rigger)",
        "relationship": "Kink partner / 3.5k msgs / 21d since last",
    },
    {
        "profile": "SARAH.md",
        "chat_patterns": ["Sarah_S_Neon_Furry", "Sarah_Bum"],
        "label": "Sarah (kink/FWB)",
        "relationship": "Kink partner / 2.8k msgs (group) + 62 (1:1)",
    },
]


def fmt_min(ms):
    """Format milliseconds to minutes."""
    if ms is None:
        return "—"
    s = ms / 1000
    if s < 60:
        return f"{s:.0f}s"
    m = s / 60
    if m < 60:
        return f"{m:.1f}min"
    h = m / 60
    if h < 24:
        return f"{h:.1f}h"
    return f"{h/24:.1f}d"


def build_empirical_section(profile_name, chat_name):
    """Build empirical analysis section for a profile."""
    if chat_name not in tp["per_contact"]:
        return None

    tp_info = tp["per_contact"][chat_name]
    init_info = init["per_chat"].get(chat_name, {})
    rec_info = rec["per_chat"].get(chat_name, {})

    lines = [
        "\n---\n",
        "\n## 📊 NEW (2026-07-27): Empirical Profile Data\n",
        f"\n**Source chat**: `{chat_name}`",
        f"\n**Tier**: {rec_info.get('tier', '?')}",
        f"\n**Last contact**: {rec_info.get('days_since_last', '?')} days ago ({rec_info.get('recency_category', '?')})",
        "\n\n### Communication Patterns\n",
        "\n| Metric | Value | Clinical Reading |",
        "\n|--------|-------|------------------|",
        f"\n| **Total messages** | {tp_info['total_msgs']:,} | Volume tier |",
        f"\n| **Late-night ratio** (22-04h) | {tp_info['late_night_ratio']:.1%} | Rumination pattern |",
        f"\n| **Ivan initiator ratio** | {tp_info['ivan_ratio']:.1%} | Pursuit/withdrawal |",
        f"\n| **Ivan starts conversations** | {init_info.get('ivan_start_ratio', 0):.1%} | Engagement pattern |",
        f"\n| **Peak hour** | {tp_info.get('peak_hour', '?')}h | When contact is most active |",
        f"\n| **Peak day** | {tp_info.get('peak_dow', '?')} | Weekly cycle |",
        f"\n| **Max message streak** | {init_info.get('max_streak_days', 0)} days | Engagement intensity |",
        f"\n| **Median response time** | {fmt_min(init_info.get('median_response_time_ms'))} | Responsiveness |",
        "\n\n### Clinical Interpretation\n",
        f"\n{interpret_metrics(tp_info, init_info, rec_info)}",
        "\n\n### Cross-Reference\n",
        "\n- `_ANALYSIS/time_patterns.json` — Full per-contact data",
        "\n- `_ANALYSIS/initiator_analysis.json` — Conversation patterns",
        "\n- `_ANALYSIS/recency_heatmap.json` — Recency heatmap",
        "\n",
    ]

    return "".join(lines)


def interpret_metrics(tp_info, init_info, rec_info):
    """Generate clinical interpretation based on metrics."""
    interpretations = []

    # Late-night
    late = tp_info["late_night_ratio"]
    if late > 0.5:
        interpretations.append(
            f"- **Dispositional late-night pattern** ({late:.1%}): Ivan's contact with this person is heavily late-night. Suggests rumination or co-regulation at night."
        )
    elif late > 0.3:
        interpretations.append(
            f"- **Moderate late-night pattern** ({late:.1%}): Higher than 32% baseline; this relationship pulls Ivan into night-mode more than average."
        )
    else:
        interpretations.append(
            f"- **Below-baseline late-night** ({late:.1%}): This relationship doesn't trigger Ivan's night-mode as much as baseline."
        )

    # Initiator ratio
    ivr = tp_info["ivan_ratio"]
    if ivr > 0.65:
        interpretations.append(
            f"- **Ivan chases** ({ivr:.1%}): Ivan initiates majority of messages. Possible pursuit-withdrawal OR caretaking dynamic."
        )
    elif ivr < 0.35:
        interpretations.append(
            f"- **They chase Ivan** ({ivr:.1%}): Ivan receives more than initiates. Possible avoidance OR being pursued OR passive partner."
        )
    else:
        interpretations.append(
            f"- **Balanced** ({ivr:.1%}): Reciprocal engagement. Healthy attachment indicator."
        )

    # Ivan start ratio (conversations)
    start = init_info.get("ivan_start_ratio", 0)
    if start > 0.6:
        interpretations.append(
            f"- **Ivan starts {start:.1%} of conversations**: Ivan carries the relational load."
        )
    elif start < 0.4:
        interpretations.append(
            f"- **They start {(1-start):.1%} of conversations**: They carry the relational load."
        )
    else:
        interpretations.append(
            f"- **Conversation starts balanced** ({start:.1%}): Reciprocal conversation initiation."
        )

    # Streak
    streak = init_info.get("max_streak_days", 0)
    if streak > 100:
        interpretations.append(
            f"- **Long streak** ({streak} days): Indicates intense engagement period. Could be honeymoon OR crisis-bonding."
        )
    elif streak > 30:
        interpretations.append(f"- **Moderate streak** ({streak} days): Solid engagement period.")

    # Response time
    rt = init_info.get("median_response_time_ms")
    if rt and rt < 60000:
        interpretations.append(f"- **Fast responder** ({fmt_min(rt)} median): High availability.")
    elif rt and rt > 3600000:
        interpretations.append(
            f"- **Slow responder** ({fmt_min(rt)} median): Possibly avoidant OR busy."
        )

    # Recency
    days = rec_info.get("days_since_last", 0)
    if days <= 7:
        interpretations.append(f"- **Active** ({days}d): Currently in conversation.")
    elif days <= 30:
        interpretations.append(f"- **Recent** ({days}d): Recently active.")
    elif days <= 90:
        interpretations.append(f"- **Cooling** ({days}d): May be drifting.")
    elif days <= 365:
        interpretations.append(f"- **Distant** ({days}d): Significantly disengaged.")
    else:
        interpretations.append(
            f"- **Abandoned** ({days}d): No contact in over a year. May indicate grief, loss, or natural relationship end."
        )

    return "\n".join(interpretations)


def update_profile(profile_path, empirical_section):
    """Append empirical section to a profile file."""
    if not profile_path.exists():
        print(f"  ⚠️ Not found: {profile_path.name}")
        return False

    content = profile_path.read_text()

    # Skip if already updated
    if "## 📊 NEW (2026-07-27): Empirical Profile Data" in content:
        print(f"  ⏭️  Already updated: {profile_path.name}")
        return False

    # Add the section at the end
    new_content = content + empirical_section
    profile_path.write_text(new_content)
    print(f"  ✅ Updated: {profile_path.name}")
    return True


def main():
    """Main: enrich all top 10 profiles."""
    print("=== Enriching top 10 deep profiles ===\n")
    updated = 0

    for entry in PROFILE_MAP:
        profile_path = PROFILES / entry["profile"]
        if not profile_path.exists():
            print(f"  ⚠️ Not found: {entry['profile']}")
            continue

        chat_name = find_chat_for_profile(entry["profile"], entry["chat_patterns"])
        if not chat_name:
            print(f"  ⚠️ No chat match: {entry['profile']}")
            continue

        empirical = build_empirical_section(entry["label"], chat_name)
        if empirical and update_profile(profile_path, empirical):
            updated += 1

    print(f"\n=== Updated {updated} profiles ===")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""MAIN 7 subgroup analysis - synthesize 8 JSON sources into per-friend profiles."""
from __future__ import annotations

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH/wa_messages/_ANALYSIS"


def analyze_main7_subgroups():
    """Synthesize data from all 8 analyses for MAIN 7 friends."""

    # Load all data sources
    tp = json.loads((ANALYSIS / "time_patterns.json").read_text())
    init = json.loads((ANALYSIS / "initiator_analysis.json").read_text())
    rec = json.loads((ANALYSIS / "recency_heatmap.json").read_text())
    tl = json.loads((ANALYSIS / "conversation_timeline.json").read_text())
    vnt = json.loads((ANALYSIS / "vnt_sentiment.json").read_text())
    vvt = json.loads((ANALYSIS / "voice_vs_text.json").read_text())
    grief = json.loads((ANALYSIS / "grief_analysis.json").read_text())
    repair = json.loads((ANALYSIS / "conversation_repair.json").read_text())

    # MAIN 7 + new kink contacts (verified by Ivan 2026-07-23)
    main_friends = {
        "Ale": ["alejandro_cabral", "10__alejandro"],
        "Kiki": ["sister_kyrian_kiki", "kyrian"],
        "Magali": ["magali_carreras_amiga_fpuna"],
        "Laura": ["laura____wa_chat_595976538689"],
        "Jonatan": ["jonathan_verdun", "jonatan_verdun"],
        "Lourdes": ["lourdes_youko_kurama", "05__lourdes"],
        "Sonia (Mom)": ["mom_sonia_weiss"],
        "Nico": ["Cloud_Nyx", "nicolas_duarte"],
        "Gaby": ["gabriella_gp", "11__gabriella"],
        "Sarah": ["Sarah_S_Neon", "Sarah_Bum"],
        "Nathaly": ["Nathaly_Schinini", "nathaly"],
        "Dayah": ["Dayah", "Group_Dayah"],
    }

    profiles = {}

    for friend, patterns in main_friends.items():
        profile = {
            "name": friend,
            "matches": [],
            "lifetime_msgs": 0,
            "last_contact": None,
            "tier": "unknown",
            "data": {},
        }

        # Find matching chats
        for chat_name in tp["per_contact"].keys():
            if any(p.lower() in chat_name.lower() for p in patterns):
                # Combine data from all sources
                tp_info = tp["per_contact"].get(chat_name, {})
                init_info = init["per_chat"].get(chat_name, {})
                rec_info = rec["per_chat"].get(chat_name, {})
                tl_info = tl["per_chat"].get(chat_name, {})
                vvt_info = vvt["per_chat"].get(chat_name, {})

                if tp_info:
                    profile["matches"].append({
                        "chat": chat_name,
                        "tier": rec_info.get("tier", "unknown"),
                        "total_msgs": tp_info.get("total_msgs", 0),
                        "late_night_ratio": tp_info.get("late_night_ratio", 0),
                        "ivan_ratio": tp_info.get("ivan_ratio", 0),
                        "ivan_starts": init_info.get("ivan_starts", 0),
                        "them_starts": init_info.get("them_starts", 0),
                        "max_streak": init_info.get("max_streak_days", 0),
                        "median_response": init_info.get("median_response_time_ms", None),
                        "days_since": rec_info.get("days_since_last", None),
                        "voice_pct": vvt_info.get("voice_pct", 0),
                        "peak_hour": tp_info.get("peak_hour", None),
                        "peak_dow": tp_info.get("peak_dow", None),
                    })
                    profile["lifetime_msgs"] += tp_info.get("total_msgs", 0)

                    if rec_info.get("days_since_last") is not None:
                        if profile["last_contact"] is None or rec_info["days_since_last"] < profile["last_contact"]:
                            profile["last_contact"] = rec_info["days_since_last"]
                        profile["tier"] = rec_info.get("tier", "unknown")

        # Build summary
        if profile["matches"]:
            # Calculate aggregate metrics
            total = profile["lifetime_msgs"]
            avg_late = sum(m["late_night_ratio"] * m["total_msgs"] for m in profile["matches"]) / total if total > 0 else 0
            avg_ivan = sum(m["ivan_ratio"] * m["total_msgs"] for m in profile["matches"]) / total if total > 0 else 0
            total_ivan_starts = sum(m["ivan_starts"] for m in profile["matches"])
            total_them_starts = sum(m["them_starts"] for m in profile["matches"])
            avg_voice = sum(m["voice_pct"] * m["total_msgs"] for m in profile["matches"]) / total if total > 0 else 0
            max_streak = max((m["max_streak"] for m in profile["matches"]), default=0)

            profile["data"] = {
                "total_msgs": total,
                "avg_late_night_ratio": round(avg_late, 3),
                "avg_ivan_ratio": round(avg_ivan, 3),
                "total_ivan_starts": total_ivan_starts,
                "total_them_starts": total_them_starts,
                "ivan_initiator_pct": round(total_ivan_starts / (total_ivan_starts + total_them_starts), 3) if (total_ivan_starts + total_them_starts) > 0 else 0,
                "avg_voice_pct": round(avg_voice, 3),
                "max_streak_days": max_streak,
                "last_contact_days": profile["last_contact"],
                "tier": profile["tier"],
            }

            # Clinical interpretation
            interpretations = []

            if avg_late > 0.4:
                interpretations.append(f"High late-night ({avg_late:.1%}) - rumination indicator")
            elif avg_late > 0.3:
                interpretations.append(f"Above-baseline late-night ({avg_late:.1%})")

            if avg_ivan > 0.65:
                interpretations.append(f"Ivan chases ({avg_ivan:.1%})")
            elif avg_ivan < 0.35:
                interpretations.append(f"They chase Ivan ({avg_ivan:.1%})")
            else:
                interpretations.append(f"Balanced ({avg_ivan:.1%})")

            if max_streak > 100:
                interpretations.append(f"Long streak ({max_streak}d) - honeymoon/crisis-bonding")
            elif max_streak > 30:
                interpretations.append(f"Moderate streak ({max_streak}d)")

            if profile["last_contact"] is not None and profile["last_contact"] > 365:
                interpretations.append(f"Abandoned ({profile['last_contact']}d) - grief signal")
            elif profile["last_contact"] is not None and profile["last_contact"] < 14:
                interpretations.append(f"Currently active ({profile['last_contact']}d)")

            if avg_voice > 0.15:
                interpretations.append(f"Voice-heavy ({avg_voice:.1%}) - intimacy modality")
            elif avg_voice < 0.05:
                interpretations.append(f"Text-only ({avg_voice:.1%}) - distance modality")

            profile["interpretations"] = interpretations

        profiles[friend] = profile

    # Save
    summary = {
        "generated_at": datetime.now().isoformat(),
        "main_friends_analyzed": len(profiles),
        "data_sources_used": 8,
        "profiles": profiles,
    }

    out = ANALYSIS / "main7_subgroup_analysis.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"Wrote {out.relative_to(REPO)}")

    print(f"\n=== MAIN 7 + Kink Subgroup Analysis ===\n")

    # Sort by lifetime msgs
    sorted_profiles = sorted(profiles.items(), key=lambda x: -x[1]["lifetime_msgs"])

    for friend, profile in sorted_profiles:
        if not profile["matches"]:
            continue

        d = profile["data"]
        print(f"\n{'='*60}")
        print(f"{friend} - {profile['tier']}")
        print(f"{'='*60}")
        print(f"  Lifetime msgs: {d['total_msgs']:,}")
        print(f"  Last contact: {d['last_contact_days']}d ago")
        print(f"  Late-night: {d['avg_late_night_ratio']:.1%}")
        print(f"  Ivan initiator: {d['avg_ivan_ratio']:.1%}")
        print(f"  Ivan starts conv: {d['total_ivan_starts']:,} / them {d['total_them_starts']:,} ({d['ivan_initiator_pct']:.1%})")
        print(f"  Max streak: {d['max_streak_days']}d")
        print(f"  Voice%: {d['avg_voice_pct']:.1%}")
        print(f"  Chats: {len(profile['matches'])}")
        print(f"  Clinical:")
        for i in profile["interpretations"]:
            print(f"    - {i}")


if __name__ == "__main__":
    analyze_main7_subgroups()
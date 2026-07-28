#!/usr/bin/env python3
"""Family dynamics from message patterns (Hat 4, 13)."""
from __future__ import annotations

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH/wa_messages"
ANALYSIS = WA / "_ANALYSIS"


def analyze_family_dynamics():
    """Analyze family-related contacts for relationship patterns."""
    family_patterns = {
        "Mom": ["mom_sonia", "Sonia_Weiss_Mom"],
        "Dad": ["dad_john", "John_van_der_Pol"],
        "Sister (Kiki)": ["sister_kyrian_kiki", "kiki_adjacent"],
        "Sister (Luana)": ["sister_luana_weiss"],
        "Grandma (Riet)": ["grandma_riet"],
        "Grandpa (Jan)": ["grandpa_jan"],
        "Uncle (Toni)": ["Toni_Weiss"],
        "Uncle (Gerold)": ["gerold", "manders"],
        "Cousin (Prima Mikaela)": ["Prima_Mikaela"],
        "Cousin (Primo Gabriel)": ["Primo_Gabriel"],
        "Poli Family (Cesar)": ["cesar_poli", "Cesar_Poli"],
        "Poli Family (Emilio)": ["emilio_poli"],
        "Poli Family (Ara)": ["ara_nunez_poli"],
        "Poli Family (René)": ["rené_pols_poli", "René_Pols"],
        "Poli Family (Don_Cangrejo)": ["don_cangrejo_poli", "Don_Cangrejo"],
        "Poli Family (Marco)": ["marco_poli"],
        "Poli Family (Fidabel/Defi)": ["fidabel_poli", "Defi"],
        "Poli Family (Liliana)": ["lilian_riveros", "28__lilian"],
    }

    by_family = {}

    for member, patterns in family_patterns.items():
        info = {
            "matches": [],
            "lifetime_msgs": 0,
            "last_contact": None,
            "tier": "unknown",
            "is_abandoned": False,
        }

        # Check all tier1, tier2, tier3, untiered_personal
        for tier in ["tier1_deep", "tier2_core", "tier3_extended", "untiered_personal", "other_lid"]:
            d = WA / tier
            if not d.exists():
                continue
            for chat in d.iterdir():
                if not chat.is_dir():
                    continue
                if any(p.lower() in chat.name.lower() for p in patterns):
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

                    valid_msgs = [m for m in msgs if isinstance(m, dict) and m.get("ts_ms")]
                    if not valid_msgs:
                        continue

                    last_ts = max(m.get("ts_ms", 0) for m in valid_msgs)
                    if last_ts:
                        days_since = (datetime.now() - datetime.fromtimestamp(last_ts / 1000)).days
                    else:
                        days_since = None

                    if days_since and days_since > 365:
                        info["is_abandoned"] = True

                    chat_info = {
                        "chat": chat.name,
                        "tier": tier,
                        "total_msgs": len(valid_msgs),
                        "last_contact_days": days_since,
                    }
                    info["matches"].append(chat_info)
                    info["lifetime_msgs"] += len(valid_msgs)
                    info["tier"] = tier

                    if days_since is not None:
                        if info["last_contact"] is None or days_since < info["last_contact"]:
                            info["last_contact"] = days_since

        by_family[member] = info

    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_family_members": len(by_family),
        "abandoned_count": sum(1 for f in by_family.values() if f["is_abandoned"]),
        "per_member": by_family,
    }

    out = ANALYSIS / "family_dynamics.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"Wrote {out.relative_to(REPO)}")

    print(f"\n=== Family Dynamics ===")
    print(f"Total family members: {len(by_family)}")
    print(f"Abandoned: {sum(1 for f in by_family.values() if f['is_abandoned'])}")

    print(f"\nFamily members ranked by lifetime msgs:")
    for member, info in sorted(by_family.items(), key=lambda x: -x[1]["lifetime_msgs"]):
        status = "ABANDONED" if info["is_abandoned"] else "active"
        last = f"{info['last_contact']}d ago" if info["last_contact"] else "?"
        print(f"  {info['lifetime_msgs']:>5} msgs  {last:<12}  {status:<10}  {member}")

    print(f"\n=== Abandoned family members (grief signal) ===")
    for member, info in by_family.items():
        if info["is_abandoned"]:
            print(f"  {member}: {info['lifetime_msgs']} msgs, last {info['last_contact']}d ago")

    # Poli vs Weiss split
    print(f"\n=== Poli vs Weiss side totals ===")
    poli = ["Poli Family", "Cousin (Prima Mikaela)", "Cousin (Primo Gabriel)"]
    weiss = ["Mom", "Dad", "Sister (Kiki)", "Sister (Luana)", "Uncle (Toni)", "Uncle (Gerold)",
             "Grandma (Riet)", "Grandpa (Jan)"]

    poli_msgs = sum(by_family[m]["lifetime_msgs"] for m in poli if m in by_family)
    weiss_msgs = sum(by_family[m]["lifetime_msgs"] for m in weiss if m in by_family)

    print(f"  Poli side: {poli_msgs:,} msgs ({len([m for m in poli if m in by_family])} members)")
    print(f"  Weiss side: {weiss_msgs:,} msgs ({len([m for m in weiss if m in by_family])} members)")


if __name__ == "__main__":
    analyze_family_dynamics()
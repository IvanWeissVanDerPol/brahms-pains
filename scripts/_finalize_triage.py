"""
Reclassify _triage.json, fix the _wa_lid_ mis-labeling, decide borderlines,
emit _final_classification.json and _analysis_shortlist.md.

Non-destructive: this script writes JSON/MD only. Moving chat dirs into
_dropped/ is a separate step (see _apply_drops.py) and requires explicit
confirmation before execution.

Reclassification rules:
  * _wa_lid_ chats with my_text_chars >= 500 OR (total_msgs >= 100 and mine% >= 0.20)
      -> personal_1on1 (they were mis-labeled 'notification')
  * _wa_lid_ chats otherwise -> low_signal (drop)
  * _wa_other_newsletter_* -> low_signal (drop)
  * true bot chats (jid ends '@bot' as sole peer) -> low_signal (drop) if present

Keep / drop policy:
  KEEP  = personal_1on1 with score >= 400  (matches existing recommended_keep floor 514
          but slightly wider to catch borderline warm contacts)
        + group_active with score >= 400
        + group_lurker with total_msgs >= 5000 and span_days >= 365
          (family/friend passive-observation groups — psych signal is the
           long-term social exposure, not user's own text)
  DROP  = everything else

Tiers for the shortlist:
  Tier 1 (deep dive):     top 10 by score
  Tier 2 (core corpus):   ranks 11-40  (up to 30)
  Tier 3 (extended):      ranks 41-100 (up to 60)
  Tier 4 (context/groups): all group_active + kept group_lurker
"""

import json
from pathlib import Path
from collections import Counter

BASE = Path(__file__).parent
tri = json.loads((BASE / "_triage.json").read_text())

# ---- 1. reclassify ----
LID_KEEP_MIN_CHARS = 500
LID_KEEP_MIN_MSGS = 100
LID_KEEP_MIN_MINE = 0.20

reclassified = 0
for c in tri["chats"]:
    slug = c["slug"]
    if slug.startswith("_wa_lid_"):
        if c["my_text_chars"] >= LID_KEEP_MIN_CHARS or (
            c["total_msgs"] >= LID_KEEP_MIN_MSGS and c["from_me_ratio"] >= LID_KEEP_MIN_MINE
        ):
            if c["category"] != "personal_1on1":
                c["category"] = "personal_1on1"
                reclassified += 1
        else:
            c["category"] = "low_signal"
    elif slug.startswith("_wa_other_newsletter_"):
        c["category"] = "low_signal"

# ---- 2. keep/drop decision ----
KEEP_SCORE_1ON1 = 400
KEEP_SCORE_GROUP_ACTIVE = 400
LURKER_KEEP_MSGS = 5000
LURKER_KEEP_SPAN_DAYS = 365

keep, drop = [], []
for c in tri["chats"]:
    cat = c["category"]
    if cat == "personal_1on1" and c["score"] >= KEEP_SCORE_1ON1:
        keep.append(c)
    elif cat == "group_active" and c["score"] >= KEEP_SCORE_GROUP_ACTIVE:
        keep.append(c)
    elif (
        cat == "group_lurker"
        and c["total_msgs"] >= LURKER_KEEP_MSGS
        and c["span_days"] >= LURKER_KEEP_SPAN_DAYS
    ):
        c["category"] = "group_lurker_context"  # marker for tier 4
        keep.append(c)
    else:
        drop.append(c)

keep.sort(key=lambda x: -x["score"])
drop.sort(key=lambda x: -x["score"])

# ---- 3. tiering ----
solo_keeps = [c for c in keep if c["category"] in ("personal_1on1",)]
group_keeps = [c for c in keep if c["category"].startswith("group")]

tier1 = solo_keeps[:10]
tier2 = solo_keeps[10:40]
tier3 = solo_keeps[40:100]
tier4 = group_keeps

# ---- 4. emit final classification ----
final = {
    "generated_from": "_triage.json",
    "reclassified_lid_to_personal": reclassified,
    "counts": {
        "keep_total": len(keep),
        "drop_total": len(drop),
        "keep_by_category": dict(Counter(c["category"] for c in keep)),
        "drop_by_category": dict(Counter(c["category"] for c in drop)),
    },
    "keep_slugs": [c["slug"] for c in keep],
    "drop_slugs": [c["slug"] for c in drop],
    "tiers": {
        "tier1_deep": [c["slug"] for c in tier1],
        "tier2_core": [c["slug"] for c in tier2],
        "tier3_extended": [c["slug"] for c in tier3],
        "tier4_group_context": [c["slug"] for c in tier4],
    },
    "policy": {
        "lid_reclassify_min_chars": LID_KEEP_MIN_CHARS,
        "lid_reclassify_min_msgs": LID_KEEP_MIN_MSGS,
        "lid_reclassify_min_mine_ratio": LID_KEEP_MIN_MINE,
        "keep_score_personal_1on1": KEEP_SCORE_1ON1,
        "keep_score_group_active": KEEP_SCORE_GROUP_ACTIVE,
        "lurker_keep_min_msgs": LURKER_KEEP_MSGS,
        "lurker_keep_min_span_days": LURKER_KEEP_SPAN_DAYS,
    },
}
(BASE / "_final_classification.json").write_text(json.dumps(final, indent=2, ensure_ascii=False))


# ---- 5. emit shortlist markdown ----
def row(c, idx=None):
    prefix = f"{idx}. " if idx else "- "
    return (
        f"{prefix}`{c['slug']}` — {c['total_msgs']:,} msgs, "
        f"{c['from_me_ratio']*100:.0f}% mine, "
        f"{c['my_text_chars']:,} my chars, "
        f"{c['audio_msgs']:,} audio, "
        f"{c['span_days']:.0f}d span, "
        f"score {c['score']:,.0f}"
    )


lines = []
lines.append("# Messaging corpus — psychology-analysis shortlist")
lines.append("")
lines.append(
    f"Generated from `_triage.json` (+ LID reclassification: {reclassified} chats moved into `personal_1on1`)."
)
lines.append("")
lines.append(f"**Keep**: {len(keep)} chats — **Drop**: {len(drop)} chats.")
lines.append("")
lines.append("## Tier 1 — deep dive (top 10 personal 1:1)")
lines.append("The highest-signal chats. Full read, quote-level analysis, longitudinal.")
lines.append("")
for i, c in enumerate(tier1, 1):
    lines.append(row(c, i))
lines.append("")
lines.append("## Tier 2 — core corpus (ranks 11-40)")
lines.append("Second-pass analysis. Themes, patterns, less exhaustive quoting.")
lines.append("")
for i, c in enumerate(tier2, 11):
    lines.append(row(c, i))
lines.append("")
lines.append("## Tier 3 — extended (ranks 41-100)")
lines.append("Reference corpus. Skim for corroboration or contrast.")
lines.append("")
for i, c in enumerate(tier3, 41):
    lines.append(row(c, i))
lines.append("")
lines.append("## Tier 4 — group context (passive-observation)")
lines.append(
    "Ivan speaks little but is embedded. Value = social dynamics he was exposed to (family, cohort, friend circles)."
)
lines.append("")
lines.append("### Active groups (Ivan participates)")
for c in [g for g in group_keeps if g["category"] == "group_active"]:
    lines.append(row(c))
lines.append("")
lines.append("### Lurker groups (passive, long-running)")
for c in [g for g in group_keeps if g["category"] == "group_lurker_context"]:
    lines.append(row(c))
lines.append("")
lines.append("## What was dropped and why")
lines.append("")
drop_counts = Counter(c["category"] for c in drop)
for cat, n in drop_counts.most_common():
    lines.append(f"- **{cat}**: {n} chats")
lines.append("")
lines.append(
    "Drop list saved to `_final_classification.json` (`drop_slugs`). Chats are physically preserved until `_apply_drops.py` is run with explicit confirmation."
)
lines.append("")

(BASE / "_analysis_shortlist.md").write_text("\n".join(lines))

print(
    f"KEEP={len(keep)}  DROP={len(drop)}  (reclassified {reclassified} LID chats to personal_1on1)"
)
print(f"Tiers: 1={len(tier1)} 2={len(tier2)} 3={len(tier3)} 4={len(tier4)}")
print("Wrote _final_classification.json and _analysis_shortlist.md")

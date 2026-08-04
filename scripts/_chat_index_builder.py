#!/usr/bin/env python3
"""Build CHAT_INDEX.md from WhatsApp chat exports."""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict

BASE = Path("/home/ai-whisperers/psychology-integration/psycology/SOURCE_OF_TRUTH/wa_messages")

# Load triage data
triage = json.loads((BASE / "_triage.json").read_text())
print(f"Triage entries: {len(triage)}", file=sys.stderr)

personal_1on1 = []
groups_active = []
groups_lurker = []
notifications = []
low_signal = []

for entry in triage:
    cat = entry.get("category", "")
    if cat == "personal_1on1":
        personal_1on1.append(entry)
    elif cat == "group_active":
        groups_active.append(entry)
    elif cat == "group_lurker":
        groups_lurker.append(entry)
    elif cat == "notification":
        notifications.append(entry)
    elif cat == "low_signal":
        low_signal.append(entry)

personal_1on1.sort(key=lambda x: x.get("score", 0), reverse=True)
groups_active.sort(key=lambda x: x.get("score", 0), reverse=True)
groups_lurker.sort(key=lambda x: x.get("score", 0), reverse=True)

EPRINT = lambda s: print(s, file=sys.stderr)

EPRINT(
    f"Personal 1on1: {len(personal_1on1)}, Groups active: {len(groups_active)}, Groups lurker: {len(groups_lurker)}"
)
EPRINT(f"Notifications: {len(notifications)}, Low signal: {len(low_signal)}")


def analyze_chat(slug, max_text_sample=150):
    folder = BASE / slug
    msg_file = folder / "messages.json"
    if not msg_file.exists():
        return None
    try:
        msgs = json.loads(msg_file.read_text())
    except:
        return None
    if not isinstance(msgs, list) or len(msgs) == 0:
        return None

    result = {
        "total_msgs": len(msgs),
        "text_msgs": 0,
        "voice_msgs": 0,
        "image_msgs": 0,
        "video_msgs": 0,
        "my_msgs": 0,
        "my_chars": 0,
        "other_chars": 0,
        "contact_candidates": [],
        "first_msgs": [],
        "last_msgs": [],
        "has_erebus": False,
        "erebus_context": [],
        "first_date": "",
        "last_date": "",
        "me_sender": "",
        "sender_counts": {},
    }

    sender_counts = defaultdict(int)
    text_with_sender = []

    for msg in msgs:
        sender = msg.get("sender", "") or msg.get("author", "") or ""
        text = msg.get("text", "") or msg.get("body", "") or msg.get("content", "") or ""
        msg_type = msg.get("type", "") or str(msg.get("mediaType", "") or msg.get("media_type", ""))

        sender_counts[sender] += 1

        mt = msg_type.lower()
        if "ptt" in mt or "audio" in mt or "ogg" in mt:
            result["voice_msgs"] += 1
        elif "image" in mt or "img" in mt:
            result["image_msgs"] += 1
        elif "video" in mt or "mp4" in mt:
            result["video_msgs"] += 1
        if text.strip():
            result["text_msgs"] += 1
            if len(text_with_sender) < max_text_sample:
                text_with_sender.append((sender, text[:500]))

    # Determine me
    if sender_counts:
        me_sender = max(sender_counts.items(), key=lambda x: x[1])[0]
        result["me_sender"] = me_sender
        my_msgs_data = [
            m for m in msgs if (m.get("sender", "") or m.get("author", "")) == me_sender
        ]
        result["my_msgs"] = len(my_msgs_data)
        result["my_chars"] = sum(len(m.get("text", "") or "") for m in my_msgs_data)
        other_msgs_data = [
            m for m in msgs if (m.get("sender", "") or m.get("author", "")) != me_sender
        ]
        result["other_chars"] = sum(len(m.get("text", "") or "") for m in other_msgs_data)

    # Dates
    if msgs:
        result["first_date"] = msgs[0].get("date", msgs[0].get("timestamp", ""))
        result["last_date"] = msgs[-1].get("date", msgs[-1].get("timestamp", ""))

    # First/last text messages
    text_msgs_full = [m for m in msgs if (m.get("text", "") or "").strip()]
    result["first_msgs"] = [
        {
            "sender": m.get("sender", "") or m.get("author", ""),
            "text": (m.get("text", "") or "")[:300],
            "date": m.get("date", m.get("timestamp", "")),
        }
        for m in text_msgs_full[:5]
    ]
    result["last_msgs"] = [
        {
            "sender": m.get("sender", "") or m.get("author", ""),
            "text": (m.get("text", "") or "")[:300],
            "date": m.get("date", m.get("timestamp", "")),
        }
        for m in text_msgs_full[-5:]
    ]

    # Search for erebus
    erebus_kw = ["erebus", "erebo", "whisperers", "ai whisperer", "agentic", "ai_whisperer"]
    for sender, text in text_with_sender:
        tl = text.lower()
        for kw in erebus_kw:
            if kw in tl:
                result["has_erebus"] = True
                if len(result["erebus_context"]) < 3:
                    result["erebus_context"].append(f"[{kw}] {text[:200]}")
                break

    # Try to infer contact name from message content
    name_hits = set()
    for sender, text in text_with_sender[:80]:
        for pat in [
            r"(?:hola|holi|hey|buenas?)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,})",
            r"([A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,})\s+(?:cómo|como|qué|que) tal",
            r"(?:querid[oa]|amig[oa]|flac[oa]|gord[oa]|bebé|bebe|amor|herman[oa])\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,})",
            r"([A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,})\s+(?:sos|sos re|eres|es muy)",
            r"te\s+(?:quiero|amo|extraño)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,})",
            r"(?:buenas|buenos)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,})",
        ]:
            for m in re.findall(pat, text, re.IGNORECASE):
                if m and len(m) > 2 and len(m) < 25:
                    name_hits.add(m.strip())

    result["contact_candidates"] = list(name_hits)[:8]
    result["sender_counts"] = dict(
        sorted(sender_counts.items(), key=lambda x: x[1], reverse=True)[:8]
    )

    return result


# ======== ANALYZE TOP 30 PERSONAL ========
EPRINT("Analyzing top 30 personal chats...")
personal_analyses = []
erebus_chats = []

for entry in personal_1on1[:30]:
    slug = entry["slug"]
    a = analyze_chat(slug)
    if a:
        a["slug"] = slug
        a["score"] = entry.get("score", 0)
        personal_analyses.append(a)
        if a["has_erebus"]:
            erebus_chats.append(
                {"slug": slug, "type": "personal_1on1", "context": a["erebus_context"]}
            )

# ======== ANALYZE TOP 20 GROUPS ========
EPRINT("Analyzing top 20 group chats...")
group_analyses = []
all_groups = groups_active + groups_lurker
all_groups.sort(key=lambda x: x.get("score", 0), reverse=True)

for entry in all_groups[:20]:
    slug = entry["slug"]
    a = analyze_chat(slug)
    if a:
        a["slug"] = slug
        a["score"] = entry.get("score", 0)
        a["category_orig"] = entry.get("category", "")
        gn = slug.replace("_wa_group_", "").rsplit("_", 1)[0].replace("_", " ").title()
        a["group_name"] = gn
        group_analyses.append(a)
        if a["has_erebus"]:
            erebus_chats.append({"slug": slug, "type": "group", "context": a["erebus_context"]})

# ======== SEARCH ALL CHATS FOR EREBUS ========
EPRINT("Scanning all chats for erebus/work keywords...")
erebus_kw = ["erebus", "erebo", "whisperers", "ai whisperer", "ai_whisperer", "agentic_workflows"]
erebus_all = []

for entry in triage:
    slug = entry.get("slug", "")
    folder = BASE / slug
    msg_file = folder / "messages.json"
    if not msg_file.exists():
        continue
    try:
        content = msg_file.read_text(errors="replace")
    except:
        continue
    cl = content.lower()
    found = [kw for kw in erebus_kw if kw in cl]
    if found:
        already = any(e["slug"] == slug for e in erebus_chats)
        if not already:
            erebus_all.append(
                {
                    "slug": slug,
                    "keywords": found,
                    "category": entry.get("category", ""),
                    "score": entry.get("score", 0),
                }
            )

erebus_all.sort(key=lambda x: x["score"], reverse=True)

# Combine
all_erebus = erebus_chats + [
    {"slug": e["slug"], "type": e["category"], "context": e["keywords"]} for e in erebus_all
]

# ======== COMPUTE STATS ========
total_msgs = sum(e.get("msgs", 0) or e.get("total_messages", 0) for e in triage)
total_my_chars = sum(e.get("my_chars", 0) or e.get("mine_chars", 0) for e in triage)

# Top 10 by voice messages
voice_rich = sorted(personal_1on1, key=lambda x: x.get("audio", 0), reverse=True)[:10]

# Top 10 by text length
text_heavy = sorted(personal_1on1, key=lambda x: x.get("my_chars", 0), reverse=True)[:10]


# ======== GENERATE CATEGORIES ========
def categorize_personal(a):
    """Return relevance category based on analysis"""
    msgs = a["total_msgs"]
    my_chars = a["my_chars"]
    voice = a["voice_msgs"]
    span = ""  # we'll use dates

    if msgs < 20:
        return "DROP"
    if my_chars > 100000 and voice > 500:
        return "HIGH"
    if my_chars > 50000 and msgs > 5000:
        return "HIGH"
    if my_chars > 20000:
        return "HIGH"
    if my_chars > 5000:
        return "MEDIUM"
    if msgs > 100:
        return "MEDIUM"
    return "LOW"


# Build output
output = {
    "stats": {
        "total_chats": len(triage),
        "personal_1on1": len(personal_1on1),
        "groups_active": len(groups_active),
        "groups_lurker": len(groups_lurker),
        "notifications": len(notifications),
        "low_signal": len(low_signal),
        "total_msgs_approx": total_msgs,
    },
    "personal_analyses": [],
    "group_analyses": [],
    "erebus_chats": all_erebus,
    "voice_rich": [
        {"slug": e["slug"], "audio": e.get("audio", 0), "score": e.get("score", 0)}
        for e in voice_rich
    ],
    "text_heavy": [
        {"slug": e["slug"], "my_chars": e.get("my_chars", 0), "score": e.get("score", 0)}
        for e in text_heavy
    ],
    "relevance": {"HIGH": [], "MEDIUM": [], "LOW": [], "DROP": []},
}

for pa in personal_analyses:
    cat = categorize_personal(pa)
    # Strip large fields
    out_pa = {k: v for k, v in pa.items() if k not in ("first_msgs", "last_msgs", "sender_counts")}
    output["personal_analyses"].append(out_pa)
    output["relevance"][cat].append(
        {
            "slug": pa["slug"],
            "score": pa["score"],
            "msgs": pa["total_msgs"],
            "my_chars": pa["my_chars"],
        }
    )

for ga in group_analyses:
    out_ga = {k: v for k, v in ga.items() if k not in ("first_msgs", "last_msgs", "sender_counts")}
    output["group_analyses"].append(out_ga)

# Include first/last msgs in a truncated form for report
for pa in personal_analyses:
    pa["_first_msgs_short"] = [
        {"s": m["sender"][:15], "t": m["text"][:150]} for m in pa["first_msgs"][:3]
    ]
    pa["_last_msgs_short"] = [
        {"s": m["sender"][:15], "t": m["text"][:150]} for m in pa["last_msgs"][-3:]
    ]
    pa["_sender_top3"] = list(pa["sender_counts"].items())[:3]
for ga in group_analyses:
    ga["_first_msgs_short"] = [
        {"s": m["sender"][:15], "t": m["text"][:150]} for m in ga["first_msgs"][:3]
    ]
    ga["_last_msgs_short"] = [
        {"s": m["sender"][:15], "t": m["text"][:150]} for m in ga["last_msgs"][-3:]
    ]
    ga["_sender_top5"] = list(ga["sender_counts"].items())[:5]

# ======== WRITE JSON DATA ========
json_path = BASE / "_chat_index_data.json"
json_path.write_text(json.dumps(output, indent=2, default=str))
EPRINT(f"JSON data written to {json_path}")

# ======== GENERATE MARKDOWN ========
lines = []


def L(s=""):
    lines.append(s)


L("# WhatsApp Chat Index for Psychological Analysis")
L()
L(f"*Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}*")
L()
L("---")
L()
L("## 1. Executive Summary")
L()
s = output["stats"]
L("| Metric | Value |")
L("|--------|-------|")
L(f"| Total chats in corpus | {s['total_chats']} |")
L(f"| Personal 1-on-1 | {s['personal_1on1']} |")
L(f"| Active groups | {s['groups_active']} |")
L(f"| Lurker groups | {s['groups_lurker']} |")
L(f"| Notifications/bots | {s['notifications']} |")
L(f"| Low signal | {s['low_signal']} |")
L(f"| Erebus/work chats to EXCLUDE | {len(output['erebus_chats'])} |")
L()

# Relevance summary
rel = output["relevance"]
L("### Relevance Breakdown (Top 30 Personal Chats)")
L()
L("| Category | Count | Description |")
L("|----------|------:|-------------|")
L(f"| 🔴 HIGH | {len(rel['HIGH'])} | Close relationships, emotional depth |")
L(f"| 🟡 MEDIUM | {len(rel['MEDIUM'])} | Friends, regular social |")
L(f"| 🟢 LOW | {len(rel['LOW'])} | Professional, casual |")
L(f"| ⚫ DROP | {len(rel['DROP'])} | Noise, insufficient data |")
L()

# ======== SECTION 2: EREBUS EXCLUSION LIST ========
L("---")
L()
L("## 2. Erebus / AI Work Chats to EXCLUDE")
L()
L(f"**{len(output['erebus_chats'])} chats identified as containing Erebus/AI work content:**")
L()
if output["erebus_chats"]:
    L("| # | Chat | Type | Evidence |")
    L("|---:|------|------|----------|")
    for i, e in enumerate(output["erebus_chats"], 1):
        ctx = e.get("context", [])
        if isinstance(ctx, list):
            ctx_str = "; ".join(c[:80] for c in ctx[:2]) if ctx else "keyword match"
        else:
            ctx_str = str(ctx)[:80]
        slug_short = e["slug"].replace("_wa_chat_", "").replace("_wa_group_", "")
        L(f"| {i} | `{slug_short}` | {e.get('type','')} | {ctx_str} |")
else:
    L("*No erebus chats detected in detailed analysis.*")
L()

# ======== SECTION 3: TOP 30 PERSONAL CHATS ========
L("---")
L()
L("## 3. Top 30 Personal Chats (Detailed Analysis)")
L()

for i, pa in enumerate(output["personal_analyses"], 1):
    slug = pa["slug"]
    phone = slug.split("_wa_chat_")[1].rsplit("_", 1)[0] if "_wa_chat_" in slug else slug
    score = pa.get("score", 0)

    # Infer name
    name = "Unknown"
    if pa.get("contact_candidates"):
        name = ", ".join(pa["contact_candidates"][:3])
    elif pa.get("_sender_top3"):
        # Use sender that isn't me
        me = pa.get("me_sender", "")
        for s, c in pa["_sender_top3"]:
            if s != me and s and not s.startswith("@"):
                name = s[:20]
                break

    cat_display = categorize_personal(pa)
    emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢", "DROP": "⚫"}.get(cat_display, "")

    L(f"### {i}. {emoji} [{name}] `{phone[:15]}`")
    L()
    L("| Field | Value |")
    L("|-------|-------|")
    L(f"| Score | {score:,.0f} |")
    L(f"| Messages | {pa['total_msgs']:,} |")
    L(f"| My messages | {pa['my_msgs']:,} ({pa['my_chars']:,} chars) |")
    L(f"| Voice notes | {pa['voice_msgs']:,} |")
    L(f"| Images | {pa['image_msgs']:,} |")
    L(f"| Date range | {pa['first_date']} → {pa['last_date']} |")
    if pa.get("has_erebus"):
        L("| ⚠️ Erebus | YES - exclude from psych analysis |")
    L(f"| Relevance | **{cat_display}** |")
    L()

    # Contact names
    if pa.get("contact_candidates"):
        L(f"**Inferred names:** {', '.join(pa['contact_candidates'][:5])}")
        L()

    # Show last 3 messages for context
    if pa.get("_last_msgs_short"):
        L("<details><summary>Last messages (context)</summary>")
        L()
        for m in pa["_last_msgs_short"]:
            who = "→ Me" if m["s"] == pa.get("me_sender", "") else "← Them"
            L(f"- *{who}*: {m['t']}")
        L()
        L("</details>")
        L()
    L("---")
    L()

# ======== SECTION 4: TOP 20 GROUPS ========
L("---")
L()
L("## 4. Top 20 Group Chats (Detailed Analysis)")
L()

for i, ga in enumerate(output["group_analyses"], 1):
    name = ga.get("group_name", ga["slug"])
    slug = ga["slug"]

    cat_orig = ga.get("category_orig", "")

    L(f"### {i}. {name}")
    L()
    L("| Field | Value |")
    L("|-------|-------|")
    L(f"| Score | {ga.get('score', 0):,.0f} |")
    L(f"| Category | {cat_orig} |")
    L(f"| Messages | {ga['total_msgs']:,} |")
    L(f"| My messages | {ga['my_msgs']:,} ({ga['my_chars']:,} chars) |")
    L(f"| Voice notes | {ga['voice_msgs']:,} |")
    L(f"| Members (top 5) | {', '.join(s[:12] for s,c in ga.get('_sender_top5', [])[:5])} |")
    if ga.get("has_erebus"):
        L("| ⚠️ Erebus | YES |")
    L()

    if ga.get("_last_msgs_short"):
        L("<details><summary>Recent messages</summary>")
        L()
        for m in ga["_last_msgs_short"]:
            L(f"- *{m['s']}*: {m['t']}")
        L()
        L("</details>")
        L()
    L("---")
    L()

# ======== SECTION 5: FULL CHAT INVENTORY ========
L("---")
L()
L("## 5. Relevance Categories")
L()

for cat_name, emoji, desc in [
    ("HIGH", "🔴", "Close relationships, emotional depth"),
    ("MEDIUM", "🟡", "Friends, regular social contact"),
    ("LOW", "🟢", "Professional, casual acquaintances"),
    ("DROP", "⚫", "Noise, insufficient data"),
]:
    items = output["relevance"].get(cat_name, [])
    L(f"### {emoji} {cat_name} — {desc} ({len(items)} chats)")
    L()
    if items:
        L("| # | Slug | Score | Msgs | My chars |")
        L("|---:|------|------:|-----:|---------:|")
        for j, item in enumerate(sorted(items, key=lambda x: x["score"], reverse=True), 1):
            slug_short = item["slug"].replace("_wa_chat_", "").replace("_wa_group_", "")
            L(
                f"| {j} | `{slug_short}` | {item['score']:,.0f} | {item['msgs']:,} | {item.get('my_chars', 0):,} |"
            )
    L()

# ======== SECTION 6: STATISTICS ========
L("---")
L()
L("## 6. Statistics")
L()

L("### Top 10 Voice-Rich Chats")
L()
L("| # | Slug | Voice msgs | Score |")
L("|---:|------|----------:|------:|")
for j, v in enumerate(output["voice_rich"], 1):
    slug_short = v["slug"].replace("_wa_chat_", "")
    L(f"| {j} | `{slug_short}` | {v['audio']:,} | {v['score']:,.0f} |")
L()

L("### Top 10 Text-Heavy Chats")
L()
L("| # | Slug | My chars | Score |")
L("|---:|------|---------:|------:|")
for j, v in enumerate(output["text_heavy"], 1):
    slug_short = v["slug"].replace("_wa_chat_", "")
    L(f"| {j} | `{slug_short}` | {v['my_chars']:,} | {v['score']:,.0f} |")
L()

# ======== SECTION 7: RECOMMENDATIONS ========
L("---")
L()
L("## 7. Recommendations for Psychological Analysis")
L()
L("### Priority Chats for Deep Analysis")
L()
L("These chats contain the richest psychological signal — intimate conversations,")
L("emotional sharing, long-term relationship dynamics, and voice-based vulnerability:")
L()

# Top 5 by combined signal
top5 = sorted(output["personal_analyses"], key=lambda x: x.get("score", 0), reverse=True)[:5]
for i, pa in enumerate(top5, 1):
    name = (
        pa.get("contact_candidates", ["Unknown"])[0] if pa.get("contact_candidates") else "Unknown"
    )
    L(
        f"{i}. **{name}** (`{pa['slug'].split('_wa_chat_')[1].rsplit('_',1)[0][:15]}`) — "
        f"Score {pa['score']:,.0f}, {pa['total_msgs']:,} msgs, {pa['voice_msgs']:,} voice notes"
    )
L()

L("### Chats to Definitely Skip")
L()
L(f"- **{len(output['erebus_chats'])}** Erebus/AI work chats (see Section 2)")
L(f"- **{s['notifications']}** notification/bot channels")
L(f"- **{s['low_signal']}** low-signal chats with < 20 messages")
L()

L("---")
L()
L("*End of WhatsApp Chat Index*")

# Write markdown
md_path = BASE / "CHAT_INDEX.md"
md_path.write_text("\n".join(lines))
EPRINT(f"Markdown written to {md_path}")
EPRINT(f"Total lines: {len(lines)}")
EPRINT("Build complete!")

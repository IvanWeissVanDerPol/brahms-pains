#!/usr/bin/env python3
"""Score every WhatsApp chat for psychology-analysis value.

Per-chat metrics collected:
  - total_msgs, from_me_msgs, from_other_msgs, from_me_ratio
  - text_msgs, audio_msgs, image_msgs, video_msgs
  - my_text_msgs, my_text_chars, my_avg_text_len
  - long_msgs (>= 200 chars from Ivan, proxy for reflective writing)
  - active_days, span_days, msgs_per_active_day
  - first_ts, last_ts

Group co-membership (v2, July 2026):
  - For every group chat (g.us), collect sender_jid values across messages.
  - For every 1-on-1 contact, count how many groups Ivan+contact co-appear in.
  - Contacts with high group co-membership are likely friends even if their
    1-on-1 chat has few messages. A "hidden friend" rescue pass is built in.

Categorization (heuristic):
  business/notification: broadcast, LID, or 1:1 with from_me_ratio < 5% and > 20 msgs
  group_lurker:          group where from_me_ratio < 10%
  group_active:          group where from_me_ratio >= 10%
  personal_1on1:         s.whatsapp.net chat with from_me_ratio >= 10%
  low_signal:            < 10 total messages OR < 3 msgs from Ivan
  hidden_friend:         1-on-1 with low volume BUT ≥2 group co-memberships

Score for "psychology signal" (higher = more valuable):
  score = my_text_chars * (0.5 + from_me_ratio)
        + long_msgs * 500
        + audio_msgs * 100                # voice notes are gold
        + starred_msgs * 200              # Ivan flagged as important
        + span_days * 2                   # long relationships weigh more
        + groups_shared_with_ivan * 800  # NEW v2: hidden-friend rescue
Penalties:
        - notification/broadcast: score *= 0.02
        - group_lurker: score *= 0.3
        - hidden_friend minimum floor: 200  # so they don't drop below keep threshold

Emits:
  SOURCE_OF_TRUTH/wa_messages/_triage.json       — full per-chat metrics
  SOURCE_OF_TRUTH/wa_messages/_triage_report.md  — human-readable ranked list
  SOURCE_OF_TRUTH/wa_messages/_triage_circles.json — circle assignments

Read-only pass. Does not mutate any chat data.
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent / "SOURCE_OF_TRUTH" / "wa_messages"

LONG_MSG_CHARS = 200
LOW_SIGNAL_TOTAL = 10
LOW_SIGNAL_MINE = 3

# v2 thresholds (July 2026)
GROUP_SHARED_FRIEND_THRESHOLD = 2  # ≥2 group co-memberships = likely friend
GROUP_SHARED_SCORE_WEIGHT = 800  # weight per shared group in score
HIDDEN_FRIEND_SCORE_FLOOR = 200  # minimum score for hidden friends
JACCARD_CLUSTER_THRESHOLD = 0.3  # jaccard for circle clustering

# Circle indicator sets — keep in sync with circles/README.md
CIRCLE_INDICATORS = {
    "inner_circle_casa_weiss": {
        "Casa stuff",
        "Casa weiss (internal)",
        "cosas de casa",
        "LA CASA 🏡",
        "Cuarteto el 15/06 ✨",
        "AGI is cumming",
        "Apuesta",
        "D&D",
        "Funhouse🎉",
        "Jojo gym",
    },
    "family_weiss_vdp": {
        "Familie van der pol",
        "Primos Weiss ⚝",
        "Weiss Siblings",
        "Mansion weiss",
    },
    "fpuna_cs_classmates": {
        "IIN FPUNA 019",
        "IIN FPUNA 2015-2021",
        "IIN FPUNA 2019 - 2025 👨‍💻👩‍💻",
        "IIN - FPUNA - GRAL",
        "Ingeniería En Informática",
        "Club de Info GRAL",
        "ML 2023-1",
        "ML grupo",
        "GCC 2023",
        "Emergentes 2023",
        "Compiladores 2024",
        "IS3 2024",
        "IS3 SIN PROFES",
        "BD2 IIN 2024",
        "FPUNA Ciberseguridad 2024",
        "IEEE CS UNA SBC 2025 🖥🌐✨",
        "IEEEXtreme - Interesados UNA",
    },
    "pytesting_community": {
        "Py Testing Community",
        "QE Meriendita!",
        "Baby Shower 02/03🐥",
        "QE yguazu falls trip",
        "Samber +atyra",
        "Team Isabelle MM",
        "ISTQB Brave and courageous",
        "Taller de Introducción QA [Instructores]",
        "Introducción al Aseguramiento de la Calidad y Automatización",
    },
}


def extract_group_participants(chat_dirs: list[Path]) -> dict[str, set[str]]:
    """For every group chat, collect the set of sender_jid values.
    Returns {group_slug: {jid_user1, jid_user2, ...}}.
    """
    out: dict[str, set[str]] = defaultdict(set)
    for chat_path in chat_dirs:
        try:
            with open(chat_path, "r", encoding="utf-8") as f:
                chat = json.load(f)
        except Exception:
            continue
        is_group = bool(chat.get("subject")) or (chat.get("jid_server") == "g.us")
        if not is_group:
            continue
        slug = chat.get("slug") or chat_path.parent.name
        for m in chat.get("messages", []):
            sender = m.get("sender_jid")
            if sender:
                out[slug].add(sender)
    return out


def compute_group_co_membership(
    group_participants: dict[str, set[str]],
    contact_jids: set[str],
) -> dict[str, set[str]]:
    """For every 1-on-1 contact_jid, return the set of group slugs they co-appear in with Ivan.

    Ivan is in every group in the corpus (by definition — every group in this dir
    has him as a member). So we just check whether contact_jid is in the participants
    of each group.

    Note: contact_jids are bare phone numbers (e.g. '595972130867') but group
    participants are full JIDs (e.g. '595972130867@s.whatsapp.net'). We normalize
    both sides to bare form for matching.
    """
    # Index group participants by bare jid
    bare_to_groups: dict[str, set[str]] = defaultdict(set)
    for gslug, parts in group_participants.items():
        for full_jid in parts:
            bare = full_jid.split("@", 1)[0] if "@" in full_jid else full_jid
            bare_to_groups[bare].add(gslug)

    out: dict[str, set[str]] = {}
    for jid in contact_jids:
        out[jid] = bare_to_groups.get(jid, set())
    return out


def assign_circle(groups_shared: set[str], chat_metadata: dict[str, dict] | None = None) -> str:
    """Score groups against CIRCLE_INDICATORS and pick the best fit.

    `groups_shared` is a set of group slugs (e.g. '_wa_group_iin_fpuna_019_1450').
    `chat_metadata` is the global {slug: {subject, ...}} map; we use it to
    translate slugs to subjects before matching against CIRCLE_INDICATORS.
    """
    if chat_metadata is None:
        # Fall back to treating groups_shared as already-subject form
        subj_set = set(groups_shared)
    else:
        subj_set = {chat_metadata.get(g, {}).get("subject") or g for g in groups_shared}
    scores: dict[str, int] = {}
    for circle, indicators in CIRCLE_INDICATORS.items():
        scores[circle] = len(subj_set & indicators)
    if not scores:
        return "other_contacts"
    best_circle = max(scores, key=lambda c: scores[c])
    return best_circle if scores[best_circle] > 0 else "other_contacts"


def classify(chat: dict[str, Any], m: dict[str, Any], groups_shared: int = 0) -> str:
    server = chat.get("jid_server") or ""
    total = m["total_msgs"]
    mine = m["from_me_msgs"]
    ratio = m["from_me_ratio"]

    if total < LOW_SIGNAL_TOTAL or mine < LOW_SIGNAL_MINE:
        # v2: but if they share many groups with Ivan, treat as hidden_friend
        if server == "s.whatsapp.net" and groups_shared >= GROUP_SHARED_FRIEND_THRESHOLD:
            return "hidden_friend"
        return "low_signal"

    if server in ("broadcast", "lid") or server.endswith("newsletter"):
        return "notification"

    # 1:1 with almost no participation from Ivan = notification-shaped
    if server == "s.whatsapp.net":
        if ratio < 0.05 and total > 20:
            return "notification"
        # v2: 1-on-1 with low ratio but high group co-membership = hidden_friend
        if ratio < 0.30 and groups_shared >= GROUP_SHARED_FRIEND_THRESHOLD:
            return "hidden_friend"
        return "personal_1on1"

    if server == "g.us":
        return "group_active" if ratio >= 0.10 else "group_lurker"

    return "other"


def score(m: dict[str, Any], category: str, groups_shared: int = 0) -> float:
    base = (
        m["my_text_chars"] * (0.5 + m["from_me_ratio"])
        + m["long_msgs"] * 500
        + m["audio_msgs"] * 100
        + m["starred_msgs"] * 200
        + m["span_days"] * 2
        + groups_shared * GROUP_SHARED_SCORE_WEIGHT  # NEW v2
    )
    if category == "notification":
        base *= 0.02
    elif category == "group_lurker":
        base *= 0.3
    elif category == "low_signal":
        base *= 0.05
    elif category == "hidden_friend":
        # Don't let hidden friends drop below the keep threshold
        base = max(base, HIDDEN_FRIEND_SCORE_FLOOR)
    return round(base, 1)


def analyze_chat(
    chat_path: Path,
    groups_shared_with: set[str] | None = None,
) -> dict[str, Any] | None:
    try:
        with open(chat_path, "r", encoding="utf-8") as f:
            chat = json.load(f)
    except Exception as e:
        return {"slug": chat_path.parent.name, "error": str(e)}

    msgs = chat.get("messages", [])
    if not msgs:
        return None

    total = len(msgs)
    from_me = sum(1 for x in msgs if x.get("from_me"))
    text_msgs = sum(1 for x in msgs if x.get("type") == 0 and x.get("text"))
    image_msgs = sum(1 for x in msgs if x.get("type") == 1)
    audio_msgs = sum(1 for x in msgs if x.get("type") == 2)
    video_msgs = sum(1 for x in msgs if x.get("type") == 3)
    starred = sum(1 for x in msgs if x.get("starred"))

    my_texts = [x.get("text") or "" for x in msgs if x.get("from_me") and x.get("text")]
    my_text_chars = sum(len(t) for t in my_texts)
    my_text_msgs = len(my_texts)
    long_msgs = sum(1 for t in my_texts if len(t) >= LONG_MSG_CHARS)
    my_avg_text_len = round(my_text_chars / my_text_msgs, 1) if my_text_msgs else 0.0

    ts_values = [x.get("ts_ms") for x in msgs if x.get("ts_ms")]
    ts_values = [t for t in ts_values if t and t > 0]
    if ts_values:
        first_ts = min(ts_values)
        last_ts = max(ts_values)
        span_days = round((last_ts - first_ts) / 86_400_000, 1)
        active_days = len({t // 86_400_000 for t in ts_values})
    else:
        first_ts = last_ts = 0
        span_days = 0.0
        active_days = 0

    from_me_ratio = round(from_me / total, 4) if total else 0.0
    msgs_per_active_day = round(total / active_days, 2) if active_days else 0.0

    # v2: group co-membership
    groups_shared = len(groups_shared_with or set())

    m = {
        "slug": chat_path.parent.name,
        "subject": chat.get("subject"),
        "jid_user": chat.get("jid_user"),
        "jid_server": chat.get("jid_server"),
        "total_msgs": total,
        "from_me_msgs": from_me,
        "from_other_msgs": total - from_me,
        "from_me_ratio": from_me_ratio,
        "text_msgs": text_msgs,
        "audio_msgs": audio_msgs,
        "image_msgs": image_msgs,
        "video_msgs": video_msgs,
        "starred_msgs": starred,
        "my_text_msgs": my_text_msgs,
        "my_text_chars": my_text_chars,
        "my_avg_text_len": my_avg_text_len,
        "long_msgs": long_msgs,
        "first_ts_iso": _iso(first_ts),
        "last_ts_iso": _iso(last_ts),
        "span_days": span_days,
        "active_days": active_days,
        "msgs_per_active_day": msgs_per_active_day,
        "groups_shared_with_ivan": groups_shared,  # NEW v2
    }
    category = classify(chat, m, groups_shared)
    m["category"] = category
    m["score"] = score(m, category, groups_shared)
    if groups_shared_with:
        m["shared_group_slugs"] = sorted(groups_shared_with)[:20]  # cap for size
    return m


def _iso(ts_ms: int) -> str | None:
    if not ts_ms or ts_ms <= 0:
        return None
    from datetime import datetime, timezone

    return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).isoformat()


def discover_chat_dirs(root: Path) -> list[Path]:
    """Find every messages.json under `root`, recursing into tier subdirs.

    Walks ALL tier subdirs INCLUDING `_dropped/` because groups are often
    dropped by the volume-based triage but are still needed for group
    co-membership analysis (every group participant matters, regardless
    of how much Ivan talks in the group).

    Skips `_conversations/` (flat txt dumps), `circles/` (symlink view),
    and `_ANALYSIS/` (analysis artifacts).
    """
    SKIP_TOP_DIRS = {
        "_conversations",
        "circles",
        "_ANALYSIS",
        "_triage_report.md",
        "_triage.json",
        "_triage_circles.json",
        "_manifest.json",
    }
    out: list[Path] = []
    for entry in sorted(root.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name in SKIP_TOP_DIRS:
            continue
        # Recurse into all tier subdirs (tier1, tier2, tier3, tier4,
        # _dropped, untiered_personal, other_lid)
        for chat_dir in sorted(entry.iterdir()):
            if chat_dir.is_dir() and (chat_dir / "messages.json").exists():
                out.append(chat_dir / "messages.json")
        # Also accept flat chat dirs directly under root (legacy support)
        if (entry / "messages.json").exists() and (entry / "messages.json") not in out:
            out.append(entry / "messages.json")
    return out


def split_group_and_1on1(chat_dirs: list[Path]) -> tuple[list[Path], list[Path]]:
    """Split chat_dirs into (group_chats, one_on_one_chats) based on subject/jid_server."""
    groups: list[Path] = []
    one_on_one: list[Path] = []
    for chat_path in chat_dirs:
        try:
            with open(chat_path, "r", encoding="utf-8") as f:
                chat = json.load(f)
        except Exception:
            continue
        is_group = bool(chat.get("subject")) or chat.get("jid_server") == "g.us"
        if is_group:
            groups.append(chat_path)
        else:
            one_on_one.append(chat_path)
    return groups, one_on_one


def main() -> int:
    # Discover all chat dirs (across ALL tiers including _dropped — groups matter)
    chat_dirs = discover_chat_dirs(ROOT)

    # v2: extract group participants from ALL groups (including _dropped ones)
    # so co-membership analysis captures every group Ivan is in.
    group_participants = extract_group_participants(chat_dirs)

    # Only analyze 1-on-1 chats for per-chat metrics (groups get their own stats)
    _, one_on_one_dirs = split_group_and_1on1(chat_dirs)

    contact_jids: set[str] = set()
    chat_metadata: dict[str, dict] = {}  # slug -> {subject, is_group, ...}
    for chat_path in one_on_one_dirs:
        try:
            with open(chat_path, "r", encoding="utf-8") as f:
                chat = json.load(f)
        except Exception:
            continue
        jid = chat.get("jid_user")
        if jid:
            contact_jids.add(jid)
    # Also build metadata for all groups (for circle assignment)
    for chat_path in chat_dirs:
        try:
            with open(chat_path, "r", encoding="utf-8") as f:
                chat = json.load(f)
        except Exception:
            continue
        slug = chat.get("slug")
        if slug:
            chat_metadata[slug] = {
                "subject": chat.get("subject"),
                "is_group": bool(chat.get("subject")) or chat.get("jid_server") == "g.us",
                "jid_user": chat.get("jid_user"),
            }
    contact_groups = compute_group_co_membership(group_participants, contact_jids)

    metrics: list[dict[str, Any]] = []
    for chat_path in one_on_one_dirs:
        groups_shared_with: set[str] = set()
        try:
            with open(chat_path, "r", encoding="utf-8") as f:
                chat = json.load(f)
            jid = chat.get("jid_user")
            if jid:
                groups_shared_with = contact_groups.get(jid, set())
        except Exception:
            pass

        m = analyze_chat(chat_path, groups_shared_with)
        if m and "error" not in m:
            # v2: also annotate circle
            if m.get("groups_shared_with_ivan", 0) >= GROUP_SHARED_FRIEND_THRESHOLD:
                m["circle"] = assign_circle(groups_shared_with, chat_metadata)
            metrics.append(m)

    metrics.sort(key=lambda x: -x["score"])

    # Aggregate by category
    by_cat: dict[str, dict[str, Any]] = {}
    for m in metrics:
        c = m["category"]
        d = by_cat.setdefault(c, {"count": 0, "total_msgs": 0, "my_text_chars": 0})
        d["count"] += 1
        d["total_msgs"] += m["total_msgs"]
        d["my_text_chars"] += m["my_text_chars"]

    # v2: hidden_friend rescue set
    hidden_friends = [m for m in metrics if m["category"] == "hidden_friend"]

    out = {
        "version": 2,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "chats_analyzed": len(metrics),
        "groups_analyzed": len(group_participants),
        "categories": by_cat,
        "recommended_keep": [
            m["slug"]
            for m in metrics
            if m["category"] in ("personal_1on1", "group_active", "hidden_friend")
            and m["score"] >= 500
        ],
        "recommended_drop": [
            m["slug"] for m in metrics if m["category"] in ("notification", "low_signal")
        ],
        "hidden_friends_rescued": [
            {
                "slug": m["slug"],
                "jid_user": m["jid_user"],
                "groups_shared": m["groups_shared_with_ivan"],
                "total_msgs": m["total_msgs"],
                "circle": m.get("circle", "unknown"),
            }
            for m in hidden_friends
        ],
        "chats": metrics,
    }

    (ROOT / "_triage.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    # Circle assignments (separate file for downstream use)
    circles_out = {
        "version": 2,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "thresholds": {
            "group_shared_friend": GROUP_SHARED_FRIEND_THRESHOLD,
            "jaccard_cluster": JACCARD_CLUSTER_THRESHOLD,
        },
        "circle_indicators": {k: sorted(v) for k, v in CIRCLE_INDICATORS.items()},
        "contacts_by_circle": defaultdict(list),
    }
    for m in metrics:
        if m.get("groups_shared_with_ivan", 0) >= GROUP_SHARED_FRIEND_THRESHOLD:
            circles_out["contacts_by_circle"][m.get("circle", "other_contacts")].append(
                {
                    "slug": m["slug"],
                    "jid_user": m["jid_user"],
                    "groups_shared": m["groups_shared_with_ivan"],
                    "total_msgs": m["total_msgs"],
                    "score": m["score"],
                }
            )
    circles_out["contacts_by_circle"] = dict(circles_out["contacts_by_circle"])
    (ROOT / "_triage_circles.json").write_text(
        json.dumps(circles_out, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    # Human-readable report
    lines: list[str] = []
    lines.append("# WhatsApp corpus triage — psychology-analysis relevance (v2)\n")
    lines.append(f"Total chats analyzed: **{len(metrics)}**\n")
    lines.append(f"Groups analyzed (with extracted participants): **{len(group_participants)}**\n")
    lines.append("\n## v2 changes (July 2026)\n")
    lines.append("- Added **group co-membership** scoring: contacts in ≥2 of Ivan's groups are")
    lines.append("  treated as `hidden_friend` even if their 1-on-1 chat has few messages.")
    lines.append("- New score component: `groups_shared_with_ivan * 800`.")
    lines.append("- New category: `hidden_friend` (with score floor of 200 so they don't drop).")
    lines.append(
        "- Circle assignment output in `_triage_circles.json` and downstream symlinks in `circles/`.\n"
    )

    lines.append("## Category breakdown\n")
    lines.append("| Category | # chats | total msgs | my text chars |")
    lines.append("|---|---:|---:|---:|")
    for cat, d in sorted(by_cat.items(), key=lambda x: -x[1]["my_text_chars"]):
        lines.append(f"| {cat} | {d['count']} | {d['total_msgs']:,} | {d['my_text_chars']:,} |")

    lines.append(
        f"\n**Recommended KEEP** (personal / active-group / hidden-friend, score ≥ 500): {len(out['recommended_keep'])} chats"
    )
    lines.append(
        f"**Recommended DROP** (notification / low-signal): {len(out['recommended_drop'])} chats"
    )
    lines.append(
        f"**🚨 Hidden friends RESCUED** (high group overlap, low 1-on-1 volume): {len(hidden_friends)} chats\n"
    )

    if hidden_friends:
        lines.append("### Hidden friends (rescued from `low_signal`)\n")
        lines.append("| JID | Groups | Msgs | Score | Circle | Suggested tier |")
        lines.append("|---|---:|---:|---:|---|---|")
        for m in sorted(hidden_friends, key=lambda x: -x["groups_shared_with_ivan"]):
            suggested = "tier2_core" if m["groups_shared_with_ivan"] >= 8 else "tier3_extended"
            lines.append(
                f"| `{m['jid_user']}` | {m['groups_shared_with_ivan']} | {m['total_msgs']} | "
                f"{m['score']} | `{m.get('circle', '?')}` | {suggested} |"
            )

    lines.append("\n## Top 50 chats by psychology signal\n")
    lines.append(
        "| # | slug | category | msgs | mine% | groups | audio | starred | long | my_chars | span_d | score |"
    )
    lines.append("|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for i, m in enumerate(metrics[:50], 1):
        lines.append(
            f"| {i} | `{m['slug']}` | {m['category']} | {m['total_msgs']:,} | "
            f"{int(m['from_me_ratio']*100)}% | {m['groups_shared_with_ivan']} | {m['audio_msgs']} | "
            f"{m['starred_msgs']} | {m['long_msgs']} | {m['my_text_chars']:,} | "
            f"{m['span_days']} | {m['score']:,} |"
        )

    lines.append("\n## Bottom 30 (candidates for drop)\n")
    lines.append("| slug | category | msgs | mine% | groups | reason |")
    lines.append("|---|---|---:|---:|---:|---|")
    drops = [m for m in metrics if m["category"] in ("notification", "low_signal")][:30]
    for m in drops:
        reason = "no participation" if m["category"] == "notification" else "too few msgs"
        lines.append(
            f"| `{m['slug']}` | {m['category']} | {m['total_msgs']:,} | "
            f"{int(m['from_me_ratio']*100)}% | {m['groups_shared_with_ivan']} | {reason} |"
        )

    (ROOT / "_triage_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"analyzed {len(metrics)} chats")
    print(f"  groups with participants: {len(group_participants)}")
    print("categories:")
    for cat, d in sorted(by_cat.items(), key=lambda x: -x[1]["count"]):
        print(
            f"  {cat:<16} {d['count']:>4} chats, {d['total_msgs']:>8,} msgs, {d['my_text_chars']:>10,} my chars"
        )
    print(f"\n🚨 hidden_friends RESCUED: {len(hidden_friends)}")
    print(f"\nkeep recommended: {len(out['recommended_keep'])}")
    print(f"drop recommended: {len(out['recommended_drop'])}")
    print("\nreports:")
    print(f"  {ROOT / '_triage.json'}")
    print(f"  {ROOT / '_triage_report.md'}")
    print(f"  {ROOT / '_triage_circles.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

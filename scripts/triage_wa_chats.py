#!/usr/bin/env python3
"""Score every WhatsApp chat for psychology-analysis value.

Per-chat metrics collected:
  - total_msgs, from_me_msgs, from_other_msgs, from_me_ratio
  - text_msgs, audio_msgs, image_msgs, video_msgs
  - my_text_msgs, my_text_chars, my_avg_text_len
  - long_msgs (>= 200 chars from Ivan, proxy for reflective writing)
  - active_days, span_days, msgs_per_active_day
  - first_ts, last_ts

Categorization (heuristic):
  business/notification: broadcast, LID, or 1:1 with from_me_ratio < 5% and > 20 msgs
  group_lurker:          group where from_me_ratio < 10%
  group_active:          group where from_me_ratio >= 10%
  personal_1on1:         s.whatsapp.net chat with from_me_ratio >= 10%
  low_signal:            < 10 total messages OR < 3 msgs from Ivan

Score for "psychology signal" (higher = more valuable):
  score = my_text_chars * (0.5 + from_me_ratio)
        + long_msgs * 500
        + audio_msgs * 100                # voice notes are gold
        + starred_msgs * 200              # Ivan flagged as important
        + span_days * 2                   # long relationships weigh more
Penalties:
        - notification/broadcast: score *= 0.02
        - group_lurker: score *= 0.3

Emits:
  SOURCE_OF_TRUTH/wa_messages/_triage.json   — full per-chat metrics
  SOURCE_OF_TRUTH/wa_messages/_triage_report.md — human-readable ranked list

Read-only pass. Does not mutate any chat data.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path("/home/ai-whisperers/psychology-integration/psycology/SOURCE_OF_TRUTH/wa_messages")

LONG_MSG_CHARS = 200
LOW_SIGNAL_TOTAL = 10
LOW_SIGNAL_MINE = 3


def classify(chat: dict[str, Any], m: dict[str, Any]) -> str:
    server = chat.get("jid_server") or ""
    total = m["total_msgs"]
    mine = m["from_me_msgs"]
    ratio = m["from_me_ratio"]

    if total < LOW_SIGNAL_TOTAL or mine < LOW_SIGNAL_MINE:
        return "low_signal"

    if server in ("broadcast", "lid") or server.endswith("newsletter"):
        return "notification"

    # 1:1 with almost no participation from Ivan = notification-shaped
    if server == "s.whatsapp.net":
        if ratio < 0.05 and total > 20:
            return "notification"
        return "personal_1on1"

    if server == "g.us":
        return "group_active" if ratio >= 0.10 else "group_lurker"

    return "other"


def score(m: dict[str, Any], category: str) -> float:
    base = (
        m["my_text_chars"] * (0.5 + m["from_me_ratio"])
        + m["long_msgs"] * 500
        + m["audio_msgs"] * 100
        + m["starred_msgs"] * 200
        + m["span_days"] * 2
    )
    if category == "notification":
        base *= 0.02
    elif category == "group_lurker":
        base *= 0.3
    elif category == "low_signal":
        base *= 0.05
    return round(base, 1)


def analyze_chat(chat_path: Path) -> dict[str, Any] | None:
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
    }
    category = classify(chat, m)
    m["category"] = category
    m["score"] = score(m, category)
    return m


def _iso(ts_ms: int) -> str | None:
    if not ts_ms or ts_ms <= 0:
        return None
    from datetime import datetime, timezone
    return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).isoformat()


def main() -> int:
    metrics: list[dict[str, Any]] = []
    for chat_dir in sorted(ROOT.iterdir()):
        mj = chat_dir / "messages.json"
        if not mj.exists():
            continue
        m = analyze_chat(mj)
        if m and "error" not in m:
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

    out = {
        "chats_analyzed": len(metrics),
        "categories": by_cat,
        "recommended_keep": [m["slug"] for m in metrics if m["category"] in ("personal_1on1", "group_active") and m["score"] >= 500],
        "recommended_drop": [m["slug"] for m in metrics if m["category"] in ("notification", "low_signal")],
        "chats": metrics,
    }

    (ROOT / "_triage.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    # Human-readable report
    lines: list[str] = []
    lines.append("# WhatsApp corpus triage — psychology-analysis relevance\n")
    lines.append(f"Total chats analyzed: **{len(metrics)}**\n")
    lines.append("## Category breakdown\n")
    lines.append("| Category | # chats | total msgs | my text chars |")
    lines.append("|---|---:|---:|---:|")
    for cat, d in sorted(by_cat.items(), key=lambda x: -x[1]["my_text_chars"]):
        lines.append(f"| {cat} | {d['count']} | {d['total_msgs']:,} | {d['my_text_chars']:,} |")

    lines.append(f"\n**Recommended KEEP** (personal / active-group, score ≥ 500): {len(out['recommended_keep'])} chats")
    lines.append(f"**Recommended DROP** (notification / low-signal): {len(out['recommended_drop'])} chats\n")

    lines.append("## Top 50 chats by psychology signal\n")
    lines.append("| # | slug | category | msgs | mine% | audio | starred | long | my_chars | span_d | score |")
    lines.append("|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for i, m in enumerate(metrics[:50], 1):
        lines.append(
            f"| {i} | `{m['slug']}` | {m['category']} | {m['total_msgs']:,} | "
            f"{int(m['from_me_ratio']*100)}% | {m['audio_msgs']} | {m['starred_msgs']} | "
            f"{m['long_msgs']} | {m['my_text_chars']:,} | {m['span_days']} | {m['score']:,} |"
        )

    lines.append("\n## Bottom 30 (candidates for drop)\n")
    lines.append("| slug | category | msgs | mine% | reason |")
    lines.append("|---|---|---:|---:|---|")
    drops = [m for m in metrics if m["category"] in ("notification", "low_signal")][:30]
    for m in drops:
        reason = "no participation" if m["category"] == "notification" else "too few msgs"
        lines.append(
            f"| `{m['slug']}` | {m['category']} | {m['total_msgs']:,} | {int(m['from_me_ratio']*100)}% | {reason} |"
        )

    (ROOT / "_triage_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"analyzed {len(metrics)} chats")
    print("categories:")
    for cat, d in sorted(by_cat.items(), key=lambda x: -x[1]["count"]):
        print(f"  {cat:<16} {d['count']:>4} chats, {d['total_msgs']:>8,} msgs, {d['my_text_chars']:>10,} my chars")
    print(f"\nkeep recommended: {len(out['recommended_keep'])}")
    print(f"drop recommended: {len(out['recommended_drop'])}")
    print(f"\nreports:\n  {ROOT / '_triage.json'}\n  {ROOT / '_triage_report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

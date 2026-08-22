#!/usr/bin/env python3
"""Cross-corpus relationship metrics, on one common definition (feeds Hats 1, 4, 14, 16).

Computes the same axes for every 1-1 chat above a volume floor so any single
contact can be ranked against the rest of the corpus rather than described in
isolation.

Initiation here is measured as day-opens and silence-breaks, NOT message share —
see docs/GABY_ANALYSIS_2026-08-22.md §0 for why the distinction matters.
"""

from __future__ import annotations

import json
import re
import statistics as st
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from itertools import pairwise
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH/wa_messages"
OUT = WA / "_ANALYSIS/relationship_comparison.json"

PY_TZ = timezone(timedelta(hours=-3))
TIERS = ["tier1_deep", "tier2_core", "tier3_extended", "untiered_personal", "other_lid"]
MIN_MESSAGES = 200
SILENCE_H = 12
REPLY_CAP_MIN = 360

LEXICON = {
    "affection": r"\b(te quiero|love you|amor|besito|beso|abrazo|mimito|mimos|cuddle|hug|kiss"
    r"|cari(ñ|n)o|linda|hermosa|preciosa|bella|kido|mommy|mami)\b",
    "distress": r"\b(ansiedad|ansiosa|angustia|no puedo|no doy más|cansada|cansado|agotad"
    r"|estres|estrés|llorar|lloro|triste|deprim|no dormí|no dormi|insomnio"
    r"|miedo|pánico|panico|no me siento bien)\b",
    "boundary": r"\b(no soy|no voy a ser|no quiero|prefiero que no|límite|limite|no me gusta"
    r"|no puedo dar|solo cuddles|no es lo que)\b",
    "sexual": r"\b(coger|cogerle|sexo|sex|strap|pija|verga|culo|teta|caliente|horny|desnud"
    r"|porn|orgasm|masturb|kink)\b",
}
COMPILED = {k: re.compile(v) for k, v in LEXICON.items()}


def per_1k(hits: int, base: int) -> float:
    return round(1000 * hits / base, 1) if base else 0.0


def analyse(path: Path, tier: str) -> dict | None:
    """Computes the common metric set for one chat, or None if it is too small."""
    try:
        blob = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    messages = blob.get("messages") or []
    if len(messages) < MIN_MESSAGES:
        return None

    for m in messages:
        try:
            m["dt"] = datetime.fromisoformat(m["ts_iso"]).astimezone(PY_TZ)
        except (TypeError, ValueError):
            return None
    messages.sort(key=lambda m: m["dt"])

    mine = [m for m in messages if m["from_me"]]
    theirs = [m for m in messages if not m["from_me"]]
    if not mine or not theirs:
        return None

    span_days = max((messages[-1]["dt"] - messages[0]["dt"]).days, 1)
    days = defaultdict(list)
    for m in messages:
        days[m["dt"].date()].append(m)

    opens = Counter("ivan" if v[0]["from_me"] else "them" for v in days.values())
    breaks: Counter = Counter()
    for a, b in pairwise(messages):
        if (b["dt"] - a["dt"]).total_seconds() / 3600 > SILENCE_H:
            breaks["ivan" if b["from_me"] else "them"] += 1

    lats: dict = defaultdict(list)
    for a, b in pairwise(messages):
        if a["from_me"] != b["from_me"]:
            mins = (b["dt"] - a["dt"]).total_seconds() / 60
            if 0 <= mins <= REPLY_CAP_MIN:
                lats["ivan" if b["from_me"] else "them"].append(mins)

    hours = Counter(m["dt"].hour for m in messages)
    late = sum(v for k, v in hours.items() if k >= 22 or k < 4)

    lex: dict = {}
    for side, msgs in (("ivan", mine), ("them", theirs)):
        texts = [m for m in msgs if m["type"] == 0 and m.get("text")]
        for name, rx in COMPILED.items():
            lex[f"{name}_{side}"] = per_1k(
                sum(1 for m in texts if rx.search(m["text"].lower())), len(texts)
            )

    total_opens = sum(opens.values()) or 1
    total_breaks = sum(breaks.values()) or 1
    return {
        "slug": path.parent.name,
        "tier": tier,
        "messages": len(messages),
        "span_days": span_days,
        "active_days": len(days),
        "msgs_per_active_day": round(len(messages) / len(days), 1),
        "first": messages[0]["dt"].date().isoformat(),
        "last": messages[-1]["dt"].date().isoformat(),
        "ivan_msg_share": round(len(mine) / len(messages), 3),
        "ivan_open_share": round(opens["ivan"] / total_opens, 3),
        "ivan_break_share": round(breaks["ivan"] / total_breaks, 3),
        "silence_breaks": total_breaks if breaks else 0,
        "ivan_median_reply_min": round(st.median(lats["ivan"]), 1) if lats["ivan"] else None,
        "them_median_reply_min": round(st.median(lats["them"]), 1) if lats["them"] else None,
        "voice_pct_ivan": per_1k(sum(1 for m in mine if m["type"] == 2), len(mine)) / 10,
        "voice_pct_them": per_1k(sum(1 for m in theirs if m["type"] == 2), len(theirs)) / 10,
        "words_ivan": sum(len((m.get("text") or "").split()) for m in mine),
        "words_them": sum(len((m.get("text") or "").split()) for m in theirs),
        "late_night_pct": round(100 * late / len(messages), 1),
        "peak_hour": max(hours, key=lambda k: hours[k]),
        **lex,
    }


def main() -> None:
    rows = []
    for tier in TIERS:
        for chat in sorted((WA / tier).glob("*/messages.json")):
            row = analyse(chat, tier)
            if row:
                rows.append(row)
    rows.sort(key=lambda r: -r["messages"])
    OUT.write_text(
        json.dumps(
            {
                "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                "min_messages": MIN_MESSAGES,
                "chats_analyzed": len(rows),
                "per_chat": rows,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"wrote {OUT.relative_to(REPO)} — {len(rows)} chats")


if __name__ == "__main__":
    main()

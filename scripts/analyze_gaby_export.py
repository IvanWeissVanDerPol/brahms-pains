#!/usr/bin/env python3
"""Relationship analysis for the Gabriella González Pane WA export (Hats 1, 4, 21, 31).

Reads the tier1_deep text-export chat and emits structured metrics to
_ANALYSIS/gaby_relationship_analysis.json.

Unlike analyze_initiators.py, this measures *initiation* (who opens the day, who
breaks a silence) rather than message share — see docs/GABY_ANALYSIS_2026-08-22.md
for why the distinction changes the clinical reading.
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
CHAT = WA / "tier1_deep/11__gabriella_gp___wa_export_2026/messages.json"
GROUP = WA / "tier4_groups/Dentista_Gabi/messages.json"
OUT = WA / "_ANALYSIS/gaby_relationship_analysis.json"

PY_TZ = timezone(timedelta(hours=-3))  # Paraguay, fixed, no DST
SILENCE_H = 12  # a gap this long counts as a conversation break
REPLY_CAP_MIN = 360  # ignore "replies" separated by more than this

LEXICON = {
    "business": r"\b(roque|clinica|clínica|consultorio|paciente|pctes|marca|branding|dossier"
    r"|ometz|web|pagina|página|precio|luque|asismed|logo|dominio|estrategia"
    r"|negocio|socio|contrato)\b",
    "affection": r"\b(te quiero|love you|amor|besito|beso|abrazo|mimito|mimos|cuddle|hug|kiss"
    r"|cari(ñ|n)o|linda|hermosa|preciosa|bella|kido|mommy|mami|madre)\b",
    "sexual": r"\b(coger|cogerle|sexo|sex|strap|pija|verga|culo|teta|caliente|horny|desnud"
    r"|porn|orgasm|masturb|kink)\b",
    "distress": r"\b(ansiedad|ansiosa|angustia|no puedo|no doy más|cansada|cansado|agotad"
    r"|estres|estrés|llorar|lloro|triste|deprim|no dormí|no dormi|insomnio"
    r"|miedo|pánico|panico|no me siento bien)\b",
    "care_offer": r"\b(estoy acá|estoy aca|estoy aquí|te ayudo|contá conmigo|conta conmigo"
    r"|tranquil|respirá|respira|acá estoy|aca estoy|te escucho)\b",
    "boundary": r"\b(no soy|no voy a ser|no quiero|prefiero que no|límite|limite|no me gusta"
    r"|no puedo dar|solo cuddles|no es lo que)\b",
}

TYPE_NAMES = {0: "text", 1: "image", 2: "audio", 3: "video", 7: "doc"}


def load(path: Path) -> list[dict]:
    """Loads a chat's messages with a localised `dt` attached to each."""
    messages: list[dict] = json.loads(path.read_text(encoding="utf-8"))["messages"]
    for m in messages:
        m["dt"] = datetime.fromisoformat(m["ts_iso"]).astimezone(PY_TZ)
    return messages


def week_key(dt: datetime) -> str:
    return (dt - timedelta(days=dt.weekday())).strftime("%Y-%m-%d")


def volume(messages: list[dict]) -> dict:
    by_type: Counter = Counter()
    for m in messages:
        who = "ivan" if m["from_me"] else "gaby"
        by_type[f"{who}_{TYPE_NAMES.get(m['type'], m['type'])}"] += 1
    words = {}
    for who, mine in (("ivan", True), ("gaby", False)):
        texts = [m["text"] or "" for m in messages if m["from_me"] is mine and m["type"] == 0]
        words[who] = sum(len(t.split()) for t in texts)
    return {
        "total": len(messages),
        "ivan": sum(1 for m in messages if m["from_me"]),
        "gaby": sum(1 for m in messages if not m["from_me"]),
        "by_type": dict(by_type),
        "text_words": words,
        "first": messages[0]["ts_iso"],
        "last": messages[-1]["ts_iso"],
    }


def initiation(messages: list[dict]) -> dict:
    """Who starts things — the metric analyze_initiators.py does not capture."""
    days: dict = defaultdict(list)
    for m in messages:
        days[m["dt"].date()].append(m)
    opens = Counter("ivan" if days[d][0]["from_me"] else "gaby" for d in days)
    closes = Counter("ivan" if days[d][-1]["from_me"] else "gaby" for d in days)

    breaks: Counter = Counter()
    for a, b in pairwise(messages):
        if (b["dt"] - a["dt"]).total_seconds() / 3600 > SILENCE_H:
            breaks["ivan" if b["from_me"] else "gaby"] += 1

    total_opens = sum(opens.values()) or 1
    total_breaks = sum(breaks.values()) or 1
    return {
        "active_days": len(days),
        "day_opens": dict(opens),
        "day_closes": dict(closes),
        "silence_breaks": dict(breaks),
        "ivan_open_share": round(opens["ivan"] / total_opens, 3),
        "ivan_break_share": round(breaks["ivan"] / total_breaks, 3),
        "message_share_ivan": round(sum(1 for m in messages if m["from_me"]) / len(messages), 3),
    }


def latency(messages: list[dict]) -> dict:
    lats: dict = defaultdict(list)
    for a, b in pairwise(messages):
        if a["from_me"] != b["from_me"]:
            mins = (b["dt"] - a["dt"]).total_seconds() / 60
            if 0 <= mins <= REPLY_CAP_MIN:
                lats["ivan_replies" if b["from_me"] else "gaby_replies"].append(mins)
    return {
        k: {
            "n": len(v),
            "median_min": round(st.median(v), 1),
            "pct_under_2min": round(100 * sum(1 for x in v if x < 2) / len(v), 1),
        }
        for k, v in lats.items()
    }


def lexicon(messages: list[dict]) -> dict:
    texts = [m for m in messages if m["type"] == 0 and m.get("text")]
    midpoint = messages[len(messages) // 2]["dt"]
    out: dict = {}
    for name, pattern in LEXICON.items():
        rx = re.compile(pattern)
        entry: dict = {}
        for who, mine in (("ivan", True), ("gaby", False)):
            mine_texts = [m for m in texts if m["from_me"] is mine]
            hits = [m for m in mine_texts if rx.search(m["text"].lower())]
            halves = []
            for lo, hi in ((None, midpoint), (midpoint, None)):
                base = [
                    m
                    for m in mine_texts
                    if (lo is None or m["dt"] >= lo) and (hi is None or m["dt"] < hi)
                ]
                hit = [
                    m
                    for m in hits
                    if (lo is None or m["dt"] >= lo) and (hi is None or m["dt"] < hi)
                ]
                halves.append(round(1000 * len(hit) / max(len(base), 1), 1))
            entry[who] = {
                "hits": len(hits),
                "per_1k": round(1000 * len(hits) / max(len(mine_texts), 1), 1),
                "first_half_per_1k": halves[0],
                "second_half_per_1k": halves[1],
            }
        out[name] = entry
    out["_split_at"] = midpoint.isoformat()
    return out


def weekly_arc(messages: list[dict]) -> list[dict]:
    biz = re.compile(LEXICON["business"])
    weeks: dict = defaultdict(lambda: Counter())
    for m in messages:
        w = weeks[week_key(m["dt"])]
        w["ivan" if m["from_me"] else "gaby"] += 1
        if m["type"] == 2:
            w["voice"] += 1
        if m["type"] == 0 and m.get("text"):
            w["text"] += 1
            if biz.search(m["text"].lower()):
                w["business"] += 1
    return [
        {
            "week": k,
            "ivan": v["ivan"],
            "gaby": v["gaby"],
            "total": v["ivan"] + v["gaby"],
            "voice": v["voice"],
            "business_pct": round(100 * v["business"] / v["text"], 1) if v["text"] else 0.0,
        }
        for k, v in sorted(weeks.items())
    ]


def hours(messages: list[dict]) -> dict:
    h = Counter(m["dt"].hour for m in messages)
    late = sum(v for k, v in h.items() if k >= 22 or k < 4)
    return {
        "by_hour": {str(k): h[k] for k in range(24) if h[k]},
        "peak_hour": max(h, key=lambda k: h[k]),
        "late_night_pct": round(100 * late / len(messages), 1),
    }


def voice_notes(messages: list[dict]) -> dict:
    """Voice volume per sender. Duration estimated from bytes — WA PTT opus ~24 kbps."""
    out: dict = {}
    for who, mine in (("ivan", True), ("gaby", False)):
        notes = [m for m in messages if m["type"] == 2 and m["from_me"] is mine]
        size = sum((m.get("media") or {}).get("size") or 0 for m in notes)
        out[who] = {
            "count": len(notes),
            "bytes": size,
            "est_hours_at_24kbps": round(size * 8 / 24_000 / 3600, 1),
            "transcribed": 0,
        }
    return out


def working_group() -> dict:
    """The Dentista_Gabi project group — mostly the Hermes agent, not people."""
    if not GROUP.exists():
        return {}
    messages = load(GROUP)
    senders = Counter(
        "ivan" if m["from_me"] else (m.get("sender_jid") or "unknown") for m in messages
    )
    return {
        "total": len(messages),
        "first": messages[0]["ts_iso"],
        "last": messages[-1]["ts_iso"],
        "by_sender": dict(senders.most_common()),
        "note": "154288881946676@lid is the Hermes agent; 118262125854912@lid is Gaby; "
        "143576646291519@lid is Kiki.",
    }


def main() -> None:
    messages = load(CHAT)
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": str(CHAT.relative_to(REPO)),
        "volume": volume(messages),
        "initiation": initiation(messages),
        "reply_latency": latency(messages),
        "lexicon_per_1k": lexicon(messages),
        "weekly_arc": weekly_arc(messages),
        "hours_local": hours(messages),
        "voice_notes": voice_notes(messages),
        "working_group": working_group(),
        "caveats": [
            (
                "Voice notes are not transcribed; Gaby's channel is voice-heavy, so every "
                "text-derived metric here under-weights her."
            ),
            "Window ends 2026-07-23 and does not cover the following month.",
            (
                "Text exports carry no phone JID, so this chat cannot be joined to the "
                "SQLite corpus on sender identity — join on slug."
            ),
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Name-mining pass 2 — for the top 30 unnamed chats.

Combines three signals (no LLM calls) to suggest a real identity:

  1. Co-member inference:  list every other contact that co-occurs in any
     group with this chat's contact. Highest = nearby-person alias.

  2. Name-mention scan:    scan text messages (type=0) for first-name tokens
     that ALSO appear as a known contact elsewhere. A name mentioned ≥3 times
     in text is a candidate.

  3. Self-intro regex:     scan for "soy + Name", "me llamo + Name",
     "mi nombre es + Name" etc. (Spanish/Guaraní/English).

Output:
    SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/name_mining_round2.json
    SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/CONTACTS_NAMING_VERIFY.md

Does NOT rename chat directories. Ivan must confirm before any rename.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# Setup
# ─────────────────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent
MSG_BASE = REPO_ROOT / "SOURCE_OF_TRUTH" / "wa_messages"
ANALYSIS_DIR = MSG_BASE / "_ANALYSIS"
NAMED_PICKLE = Path("/tmp/psycology_named_v2.pkl")

# Tiers (in scan order)
TIERS = [
    "tier1_deep",
    "tier2_core",
    "tier3_extended",
    "tier4_groups",
    "_dropped",
    "untiered_personal",
    "other_lid",
]

# Priority JIDs (top 30 from analysis). Order matters — earlier = more value.
PRIORITY_JIDS = [
    # ── Tier S: tier1/tier2 high-volume, biggest unlock ──
    "595962291837",  # 16__friend_alvaro___wa_chat_595962291837_9625  (4,269 msgs)
    "595985340001",  # 23__friend_uwu___wa_chat_595985340001_2439     (4,098 msgs)
    "595983822921",  # 14__friend_brasilia___wa_chat_595983822921_11297 (3,898 msgs)
    "595993553949",  # 33__kiki_adjacent___wa_chat_595993553949_12779  (2,525 msgs)
    "595985249907",  # 22__friend_tiktok_share___wa_chat_595985249907_9628 (2,399 msgs)
    "595973572212",  # 34__friend_simple___wa_chat_595973572212_1994  (2,236 msgs)
    "595986805654",  # fpuna_alvaro_alt___wa_chat_595986805654_1271   (7,392 msgs)
    "595981324569",  # 06__p4569___wa_chat_595981324569_1092         (tier1_deep, 663 msgs)
    "595971505289",  # 044__p5289___wa_chat_595971505289_110          (1,420 msgs)
    "595986464184",  # 38__friend_arrival___wa_chat_595986464184_1811 (1,392 msgs)
    # ── Tier A: tier3 high audio + lower tier2 ──
    "595981199223",  # 050__p9223___wa_chat_595981199223_1728         (940 msgs / 80 audio)
    "595982553100",  # 056__p3100___wa_chat_595982553100_9254         (722 msgs)
    "595985340001",  # repeated (remove later)
    "595985435809",  # 051__p5809___wa_chat_595985435809_11371        (919 msgs)
    "595973757353",  # 067__p7353___wa_chat_595973757353_1731         (819 msgs)
    "595982223241",  # 057__p3241___wa_chat_595982223241_11521        (738 msgs)
    "595982553100",  # 056__p3100
    "595991705424",  # 045__p5424___wa_chat_595991705424_1202
    "595986868241",  # 35__friend_photos___wa_chat_595986868241_10607
    "595981199223",  # 050__p9223
    # Fill out for full 25 unique
    "595985951732",  # 063__p1732___wa_chat_595985951732_1722
    "595985412456",  # 058__p2456 (placeholder in case)
    "595991549029",  # ann_kink (already named, exclude later)
]

# Dedupe while preserving order
PRIORITY_JIDS = list(dict.fromkeys(PRIORITY_JIDS))[:25]


# Regex / patterns
# Spanish "soy/I am" + name heuristics
# Strict: capture 2-consonant+ common Spanish first names from a curated list
COMMON_FIRST_NAMES = {
    # Female
    "maria",
    "ana",
    "luisa",
    "carmen",
    "rosa",
    "marta",
    "laura",
    "sofia",
    "isabel",
    "clara",
    "andrea",
    "paula",
    "elena",
    "susana",
    "silvia",
    "natalia",
    "lucía",
    "lucia",
    "jimena",
    "ximena",
    "verónica",
    "veronica",
    "lina",
    "micaela",
    "mikaela",
    "lorena",
    "camila",
    "valentina",
    "gabriela",
    "magali",
    "lourdes",
    "lilian",
    "sandra",
    "karen",
    "katherine",
    "lucía",
    "yamila",
    "renata",
    "estefani",
    "estefany",
    "milagros",
    "ayelén",
    "victoria",
    "josefina",
    "alejandra",
    "constanza",
    # Male
    "juan",
    "pedro",
    "josé",
    "carlos",
    "luis",
    "alejandro",
    "alvaro",
    "ángel",
    "angel",
    "miguel",
    "sergio",
    "ricardo",
    "emilio",
    "sebastian",
    "sebastián",
    "enrique",
    "andrés",
    "andres",
    "martin",
    "gabriel",
    "rené",
    "rene",
    "lucas",
    "mateo",
    "nicolas",
    "tomás",
    "tomas",
    "braian",
    "braian",
    "marcos",
    "mauricio",
    "jaime",
    "eduardo",
    "hugo",
    "oscar",
    "osvaldo",
    "marcelo",
    "mathias",
    "jonathan",
    "federico",
    "francisco",
    "tomas",
    "joaquin",
    "joaquín",
    "david",
    "rodrigo",
    "nicolas",
    "nicolás",
    "raúl",
    "raul",
    "rafael",
    "ignacio",
    "federico",
    "ariel",
    "gustavo",
    "leandro",
    "adolfo",
    "matías",
    "matias",
    # Bilingual/unisex and English
    "alex",
    "chris",
    "sam",
    "pat",
    "kelly",
    "daniel",
    "jack",
    "mike",
    "george",
    "robert",
    "frank",
    "toni",
    "tyler",
    "allen",
    "denae",
    "jackie",
    "lara",
    "nora",
    "susana",
    "valeria",
    "rebeca",
}
# Sort by length DESC so longer matches win
COMMON_FIRST_NAMES_SORTED = sorted(COMMON_FIRST_NAMES, key=lambda x: -len(x))


def _maybe_name(s: str) -> str:
    """True if s matches our 'name' criteria."""
    sl = s.lower()
    if sl in COMMON_FIRST_NAMES:
        return sl
    return ""


# Properly-strict self-intro pattern. Used as a regex with a callable that
# guards against stop words like 'soy la que...'.
SELF_INTRO_RE = re.compile(
    r"(?:^|\b)(?:soy|me llamo|mi nombre es|yo soy|yo me llamo|él es|ella es|"
    r"llámame|llamame|mi amiga es|mi amigo es|mi novia es|mi novio es|"
    r"soy la|soy el|llamo)\s+([a-záéíóúñ]{3,}(?:\s+[a-záéíóúñ]{3,})?)",
    re.IGNORECASE | re.UNICODE,
)
# Strong "this person said" patterns
THIRD_PARTY_RE = re.compile(
    r"\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)\s+(?:dijo|dice|me dijo|me cuenta|habló|me habló|"
    r"me llamó|llamó|mandó|me mandó|siempre|writes|said|told|tells)",
    re.IGNORECASE | re.UNICODE,
)
# Common Spanish stop words we should ignore
STOP_WORDS = {
    "que",
    "qué",
    "quien",
    "quién",
    "como",
    "cómo",
    "donde",
    "dónde",
    "cuando",
    "cuándo",
    "porque",
    "por",
    "para",
    "con",
    "sin",
    "una",
    "uno",
    "unas",
    "unos",
    "del",
    "los",
    "las",
    "hay",
    "ser",
    "estar",
    "tener",
    "yo",
    "tu",
    "tú",
    "el",
    "la",
    "lo",
    "es",
    "si",
    "sí",
    "no",
    "ya",
    "te",
    "se",
    "me",
    "le",
    "les",
    "nos",
    "he",
    "ha",
    "ok",
    "más",
    "muy",
    "tan",
    "ahí",
    "aquí",
    "esto",
    "esta",
    "este",
    "eso",
    "esa",
    "ese",
    "bueno",
    "buena",
    "bien",
    "mal",
    "puede",
    "puedo",
    "mejor",
    "peor",
    "siempre",
    "nunca",
    "mucho",
    "mucha",
    "algo",
    "nada",
    "todo",
    "todos",
    "otra",
    "otro",
    "mismo",
    "misma",
    "aquel",
    "aquella",
    "ese",
    "esa",
    "laura",
    "lucas",  # placeholder, will be replaced by first_names from NAMED
}


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def load_named() -> dict:
    """Load /tmp/psycology_named_v2.pkl — dict jid -> (name, conf, descr)."""
    import pickle

    if not NAMED_PICKLE.exists():
        return {}
    return pickle.load(open(NAMED_PICKLE, "rb"))


def first_names_from_named(named: dict) -> set[str]:
    """Extract a set of first-name tokens from the NAMED dict."""
    names = set()
    for jid, (name, conf, _) in named.items():
        if not name:
            continue
        for part in re.split(r"[\s,]+", name):
            part = part.strip(" .,()¡!¿?_")
            if 2 <= len(part) <= 18 and part[0].isupper():
                # Use lower-case for matching
                names.add(part.lower())
    # Also add common Paraguayan/regional first names that are KNOWN
    # (the corpus says "kiki", "alejandro", etc. lowercase in some places)
    return names


def jid_to_chat_path(jid: str) -> Path | None:
    """Find the chat directory for a JID under any tier."""
    for tier in TIERS:
        tier_dir = MSG_BASE / tier
        if not tier_dir.exists():
            continue
        for d in tier_dir.iterdir():
            if not (d / "messages.json").exists():
                continue
            try:
                with open(d / "messages.json") as f:
                    data = json.load(f)
                if str(data.get("jid_user")) == str(jid):
                    return d
            except Exception:
                continue
    return None


def load_chat(chat_dir: Path) -> tuple[dict, list]:
    """Return (metadata, messages) for a chat."""
    with open(chat_dir / "messages.json") as f:
        data = json.load(f)
    return data, data.get("messages", [])


# ─────────────────────────────────────────────────────────────────────────────
# Co-member inference
# ─────────────────────────────────────────────────────────────────────────────


def extract_group_participants() -> dict[str, set[str]]:
    """For every group chat: return {group_slug: {jid_bare, ...}}"""
    out = defaultdict(set)
    for tier in TIERS:
        tier_dir = MSG_BASE / tier
        if not tier_dir.exists():
            continue
        for d in tier_dir.iterdir():
            if not (d / "messages.json").exists():
                continue
            try:
                with open(d / "messages.json") as f:
                    chat = json.load(f)
            except Exception:
                continue
            if not chat.get("subject") and chat.get("jid_server") != "g.us":
                continue  # skip non-group
            slug = chat.get("slug")
            if not slug:
                continue
            for m in chat.get("messages", []):
                if not isinstance(m, dict):
                    continue
                jid = (
                    m.get("sender_jid") or (m.get("from_me") and str(chat.get("jid_user"))) or None
                )
                if not jid:
                    continue
                bare = jid.split("@", 1)[0] if "@" in jid else jid
                # Skip Ivan's own JID (the @s.messaging.net owner)
                # We need to know Ivan's JID — for now allow all
                out[slug].add(bare)
    return dict(out)


def co_member_counts(jid: str, group_data: dict) -> dict[str, int]:
    """For a given 1-on-1 contact JID, count which other JIDs co-occur in groups."""
    co = Counter()
    bare = str(jid).split("@", 1)[0] if "@" in str(jid) else str(jid)
    for group_slug, parts in group_data.items():
        if bare in parts:
            # All other participants of this group also "co-occur"
            for other in parts:
                if other != bare:
                    co[other] += 1
    return dict(co)


# ─────────────────────────────────────────────────────────────────────────────
# Name-mention scan
# ─────────────────────────────────────────────────────────────────────────────


def extract_first_name_tokens(messages: list, known_first_names: set[str]) -> Counter:
    """Find name-tokens in text msgs that match a known first-name."""
    counts: Counter = Counter()
    for m in messages:
        if not isinstance(m, dict) or m.get("type") != 0:
            continue
        text = m.get("text") or ""
        if not text:
            continue
        # Tokenize by space and punctuation
        tokens = re.findall(r"[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+", text)
        for tok in tokens:
            if tok.lower() in known_first_names:
                counts[tok] += 1
    return counts


def extract_self_intro_names(messages: list) -> list[tuple[str, int]]:
    """Find 'soy Name' / 'me llamo Name' patterns, gated to COMMON_FIRST_NAMES."""
    matches: list[tuple[str, int]] = []
    for m in messages:
        if not isinstance(m, dict) or m.get("type") != 0:
            continue
        text = (m.get("text") or "").strip()
        if not text:
            continue
        # Only short messages are self-intros (avoid running through long rants)
        if len(text) > 200:
            continue
        for m2 in SELF_INTRO_RE.finditer(text):
            candidate = m2.group(1).strip()
            # Reject if candidate contains a stop word (e.g., "soy la que → que")
            parts = candidate.split()
            good_parts = [p for p in parts if p.lower() not in STOP_WORDS]
            for part in good_parts:
                if len(part) >= 3:
                    n = _maybe_name(part)
                    if n:
                        matches.append((n.capitalize(), m.get("ts_ms", 0)))
                        break
    return matches


def extract_third_party_refs(messages: list, known_first_names: set[str]) -> Counter:
    """Find 'Name dijo/habló/...' patterns, then see if Name is a known contact."""
    counts: Counter = Counter()
    for m in messages:
        if not isinstance(m, dict) or m.get("type") != 0:
            continue
        text = m.get("text") or ""
        if not text:
            continue
        for m2 in THIRD_PARTY_RE.finditer(text):
            name = m2.group(1).strip()
            if name.lower() in known_first_names:
                counts[name] += 1
    return counts


# ─────────────────────────────────────────────────────────────────────────────
# Per-chat mining
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class ChatMining:
    jid: str
    tier: str
    dirname: str
    msgs: int
    audio: int
    co_members_top: list[tuple[str, int]]
    name_mentions_top: list[tuple[str, int]]
    self_intro_names: list[str]
    third_party_names: list[tuple[str, int]]
    text_msgs_scanned: int
    proposed_name: str = "UNKNOWN"
    confidence: str = "NONE"
    evidence: list[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "jid": self.jid,
            "tier": self.tier,
            "dirname": self.dirname,
            "msgs": self.msgs,
            "audio": self.audio,
            "co_members_top": self.co_members_top,
            "name_mentions_top": self.name_mentions_top,
            "self_intro_names": self.self_intro_names,
            "third_party_names": self.third_party_names,
            "text_msgs_scanned": self.text_msgs_scanned,
            "proposed_name": self.proposed_name,
            "confidence": self.confidence,
            "evidence": self.evidence or [],
        }


def mine_one(jid: str, named: dict, first_names: set, group_data: dict) -> ChatMining | None:
    chat_dir = jid_to_chat_path(jid)
    if not chat_dir:
        # Try to find the contact under tier/slug dirs even if messages.json
        # was missing
        return None
    tier = chat_dir.parent.name
    meta, msgs = load_chat(chat_dir)
    audio_n = sum(1 for x in msgs if isinstance(x, dict) and x.get("type") == 2)
    text_n = sum(1 for x in msgs if isinstance(x, dict) and x.get("type") == 0)

    co_top = sorted(co_member_counts(jid, group_data).items(), key=lambda x: -x[1])[:10]
    name_top = extract_first_name_tokens(msgs, first_names).most_common(20)
    self_intro = extract_self_intro_names(msgs)
    third_party = extract_third_party_refs(msgs, first_names).most_common(10)

    out = ChatMining(
        jid=jid,
        tier=tier,
        dirname=chat_dir.name,
        msgs=len(msgs),
        audio=audio_n,
        co_members_top=co_top,
        name_mentions_top=name_top,
        self_intro_names=[s[0] for s in self_intro],
        third_party_names=third_party,
        text_msgs_scanned=text_n,
    )

    # Score and propose
    evidence: list[str] = []
    score = 0

    # Self-intro is a HIGH-confidence signal
    if self_intro:
        # Pick the most common name in self-intros
        c = Counter(s[0] for s in self_intro)
        name, n = c.most_common(1)[0]
        out.proposed_name = name
        out.confidence = "HIGH"
        score = 100
        evidence.append(
            f"Self-intro pattern matched: '{name}' ({n} times) — high-confidence identity"
        )

    # If no self-intro, fall back to top name-mention
    elif name_top:
        # Filter out stop-words / generic noise (De, Del, Pol, Dios, etc.)
        clean = [(n, c) for n, c in name_top if n.lower() not in STOP_WORDS and len(n) >= 3]
        if clean:
            top_name, top_count = clean[0]
            # Cross-reference: is this name a known contact elsewhere?
            matching_jids = [
                (other_jid, m)
                for other_jid, (m, _, _) in named.items()
                if m.lower() == top_name.lower()
                or m.lower().startswith(top_name.lower() + " ")
                or m.lower().endswith(" " + top_name.lower())
            ]
            out.proposed_name = top_name
            if top_count >= 10:
                out.confidence = "MEDIUM"
                score = 60
                evidence.append(
                    f"Name '{top_name}' mentioned {top_count}× in text — "
                    f"{'matches known contact(s) ' + str(matching_jids) if matching_jids else 'no matching contact yet'}"
                )
            elif top_count >= 3:
                out.confidence = "LOW"
                score = 30
                evidence.append(f"Name '{top_name}' mentioned {top_count}× — soft signal")
            else:
                out.confidence = "NONE"
                evidence.append(f"Name '{top_name}' mentioned only {top_count}× — too thin")

    # Co-member inference appends evidence
    if co_top:
        top_jid, count = co_top[0]
        # Lookup that JID's name
        other_name = named.get(top_jid, (None, None, None))[0]
        if other_name:
            evidence.append(
                f"Most-shared contact: {other_name} ({top_jid}) in {count} groups with this chat"
            )
        else:
            evidence.append(
                f"Most-shared contact (unnamed): {top_jid} in {count} groups with this chat"
            )

    # Third-party refs as supplementary signal
    if third_party:
        evidence.append(
            "Third-party references: " + ", ".join(f"'{n}' (×{c})" for n, c in third_party[:5])
        )

    if not evidence:
        evidence.append("No name tokens, no self-intros, no co-member anchors. Need manual review.")

    out.evidence = evidence
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Markdown report
# ─────────────────────────────────────────────────────────────────────────────


def write_markdown(results: list[ChatMining], out: Path):
    lines = []
    lines.append("# Messaging Contact Names — Round 2 Mining (Top 25)")
    lines.append("")
    lines.append(f"> **Generated:** {datetime.now(timezone.utc).isoformat()}  ")
    lines.append(
        "> **Source chats:** 25 priority unnamed 1-on-1 chats from `tier1_deep`, `tier2_core`, `tier3_extended`  "
    )
    lines.append(
        "> **Method:** Co-member inference + name-mention scan + self-intro regex (no LLM)  "
    )
    lines.append(">")
    lines.append("> **Confidence tiers:**  ")
    lines.append("> - **HIGH** = direct self-intro match (`soy Name`, `me llamo Name`, etc.)  ")
    lines.append("> - **MEDIUM** = name mentioned ≥10× in text and matches a known contact  ")
    lines.append("> - **LOW** = name mentioned 3-9×, no other strong signal  ")
    lines.append("> - **NONE** = no signal above threshold; manual review required  ")
    lines.append("")
    lines.append(
        "> **⚠️ DO NOT AUTO-RENAME.** Open `verify`, mark ✅/❌, then re-run the rename commit.  "
    )
    lines.append("")
    lines.append(
        "| # | JID | Tier | Msgs | Audio | Curr. label | Proposed | Conf | Co-member anchor | Evidence |"
    )
    lines.append("|---:|-----|------|----:|-----:|---|---|------|----------|----------|")

    for i, r in enumerate(results, 1):
        co = ""
        if r.co_members_top:
            j, c = r.co_members_top[0]
            co = f"…shared with `{j[-9:]}` in {c} groups"
        ev = "; ".join(r.evidence[:3])
        # Escape | in markdown table
        ev = ev.replace("|", "\\|")
        lines.append(
            f"| {i} | `{r.jid}` | {r.tier} | {r.msgs:,} | {r.audio} | "
            f"`{r.dirname[:35]}` | **{r.proposed_name}** | "
            f"{_conf_badge(r.confidence)} | {co} | {ev} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## How to verify")
    lines.append("")
    lines.append("1. Open Messaging on Ivan's phone")
    lines.append("2. Search for each proposed name and check if the chat is saved with that name")
    lines.append("3. Mark each row ✅ (confirmed) / ❌ (wrong) / ❓ (need more data)")
    lines.append("4. Once confirmed, run the rename commit (Track A.2)")
    lines.append("")
    lines.append("## Tools used")
    lines.append("")
    lines.append("```bash")
    lines.append("# Re-run this mining pass")
    lines.append("python3 scripts/mine_contact_names.py")
    lines.append("```")
    out.write_text("\n".join(lines))


def _conf_badge(c: str) -> str:
    return {
        "HIGH": "🟢 HIGH",
        "MEDIUM": "🟡 MEDIUM",
        "LOW": "🟠 LOW",
        "NONE": "⚪ NONE",
    }.get(c, c)


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────


def main():
    print("=" * 64)
    print("Round-2 name mining — top 25 unnamed chats")
    print("=" * 64)

    named = load_named()
    first_names = first_names_from_named(named)
    print(f"Loaded NAMED: {len(named)} known contacts")
    print(f"First-name set: {len(first_names)} names")

    print("\nBuilding group participants index...")
    group_data = extract_group_participants()
    print(f"  {len(group_data)} groups with participants")

    results: list[ChatMining] = []
    for jid in PRIORITY_JIDS:
        # Skip if already named with HIGH+ confidence
        if jid in named:
            n, c, _ = named[jid]
            if c in (
                "VERIFIED",
                "VERIFIED_PHONEBOOK",
                "VERIFIED_SELF_INTRO",
                "VERIFIED_CONTEXT",
                "HIGH",
            ):
                print(f"  ⏭  {jid} already named ({c}={n}) — skipping")
                continue

        r = mine_one(jid, named, first_names, group_data)
        if r is None:
            print(f"  ❓ {jid} — chat dir not found")
            continue
        results.append(r)
        print(
            f"  {r.confidence:<6} {r.jid} → {r.proposed_name:<25} "
            f"(mentions={[n for n, _ in r.name_mentions_top[:3]]})"
        )

    out_json = ANALYSIS_DIR / "name_mining_round2.json"
    out_md = ANALYSIS_DIR / "CONTACTS_NAMING_VERIFY.md"
    out_json.parent.mkdir(parents=True, exist_ok=True)

    out_json.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "method": "co-member + name-mention + self-intro regex (no LLM)",
                "priority_jids": PRIORITY_JIDS,
                "results": [r.to_dict() for r in results],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    print(f"\nWrote {out_json}")

    write_markdown(results, out_md)
    print(f"Wrote {out_md}")

    # Quick summary
    by_conf = Counter(r.confidence for r in results)
    print("\nSummary:")
    for c in ("HIGH", "MEDIUM", "LOW", "NONE"):
        print(f"  {c}: {by_conf.get(c, 0)}")

    high = [r for r in results if r.confidence == "HIGH"]
    none = [r for r in results if r.confidence == "NONE"]
    print(f"\nTop {len(high)} HIGH-confidence:")
    for r in high:
        print(f"  {r.jid} → {r.proposed_name}  ({r.evidence[0] if r.evidence else '-'})")
    print(f"\nUnresolved ({len(none)} chats need manual review):")
    for r in none[:5]:
        print(f"  {r.jid}  {r.dirname[:50]}")


if __name__ == "__main__":
    main()

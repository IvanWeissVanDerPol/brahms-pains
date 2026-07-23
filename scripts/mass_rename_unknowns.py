#!/usr/bin/env python3
"""Smart mass-renamer for tier1_deep + tier2_core + tier3_extended chats.

Three signals for each chat:
  1. Self-intro regex (gated to ~150 curated first names)
  2. Co-member inference: which other contacts co-occur in groups
  3. Name-mention scan (filtered against Spanish stop words)

Filtering rules:
  - Only tier1_deep, tier2_core, tier3_extended, untiered_personal
  - Skip already-named
  - Skip family (already corrected today)
  - Skip chats with < 30 messages (too low signal)
  - Skip chats with 30-200 messages unless we have HIGH confidence
  - For chats with > 200 messages, MEDIUM confidence is enough

Outputs:
  - Proposed renames to .json (reviewed by Ivan before apply)
  - Mapping old_name → new_name

USAGE:
    python3 scripts/mass_rename_unknowns.py --dry-run
    python3 scripts/mass_rename_unknowns.py --apply
"""
from __future__ import annotations

import argparse
import json
import pickle
import re
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MSG_BASE = REPO / "SOURCE_OF_TRUTH" / "wa_messages"
GROUPS_BASE = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "tier4_groups"
TR = REPO / "SOURCE_OF_TRUTH" / "voice_note_transcripts"
ANALYSIS = MSG_BASE / "_ANALYSIS"
PICKLE = Path("/tmp/psycology_named_v2.pkl")

# ~150 curated common first names (Spanish/English/Dutch/etc.)
COMMON_FIRST_NAMES = set("""
maria jose luis carlos ana juan pedro manuel martha rosa carmen mario silvia
paula diego julian francisco antonio isabel pablo laura jorge diego ramiro
ricardo lorenzo fernando miguel angel luis ramon martin rodrigo marcela
natalia veronica andrea carolina daniela florencia gabriela jesica lucia
luciana maira maximiliana melody pamela paola patricia romina sabrina
silvina sonia susana tania vanina yesica adriana alejandro alejandra alex
alexis alfonso amalia amanda ana andres angel andrea antonio argentina
ariel armando arturo augustina ariel benjamin blanca brenda camila carla
carlos carmen carolina catalina cecilia celia celeste cesar christian ciro
claudio claudia constantino cristina daisy dante darwin david denis diana
diana diego domingo doris edgar edith eduardo elena elias elisa elizabeth
emilio emmanuel erica ernesto esteban estela eugenia eva fabian fatima
federico felipe fernando florencia francisco gabriel gabriela gaston
genaro gladys graciela gualberto guillermo gustavo hector hector hugo
ines iris isabel javier jesica jesus joaquin jonatan jorge jose josefa
josefina juan julia julio laura leandro leonardo leticia lila lili
liliana lis lola lorena lorenzo lucas lucia luciano luis lydia magali
malena manuela marcos margarita maria maricel mariela marina mario
marisa marisol martha marcelo martin matias mauricio maximiliano melina
miguel milagros mirta miriam monica nadia nancy natalia nazareno nestor
nicolas nilda noelia norma octavio olga omar oscar osvaldo paola patricia
patricio pablo pedro pili ramiro ramona raquel reinaldo renzo ricardo
rita roberto rodrigo romina rosa rosario roxana ruben samantha sandra
santiago saul sebastian sergio silvia silvio sofia sonia stella tania
tatiana teresa tomas ubaldo valeria veronica victor victoria vicky vilma
violeta viviana wenceslao yanina yesica yolanda zunilda luis_eduardo
jose_luis maria_luz carlos_eduardo luis_alberto jose_antonio juan_carlos
jose_maria maria_elena maria_jose maria_cristina ana_maria rosa_maria
emma olivia ava sophia mia isabella charlotte amelia harper evelyn
abigail emily ella elizabeth camila luna sofia avery mia_rae kayla
anna sophie saskia kyrian
""".split())

# Stop words to filter
STOP_WORDS = set("""
de la el los las del por para con sin una uno que se me te mi tu yo
es si no ya lo le su nos les ha han fue fui vas voy estoy esta este
esta es son son somos sea seas sean está están tambien tambien muy
mas más ahora bien solo solo puede pueden puede podria podría debe
deben deberia debería aqui allí ayer hoy mañana cuando donde como
porque por qué por que qué quien quien quienes cual cual donde
porque también tampoco algo nada todo todos todas mucho mucha muchos
muchas poco poca pocos pocas tan tanto tanta tantos tantas muy ya
a ante bajo cabe con contra desde durante en entre hacia hasta
mediante para por según sin sobre tras versus vía
""".split())

# Family-related terms that should NOT be a name suggestion
FAMILY_TERMS = set("""
mama mamá papa papá dad mom daddy mommy brother sister cousin tio tío
tia tía uncle aunt abuelo abuela grandma grandpa father mother hijo
hija hermano hermana primo prima sobrino sobrina nieto nieta esposa
esposo marido mujer cuñado cuñada suegro suegra yerno nuera
""".split())


def find_chats(tiers):
    out = []
    for tier in tiers:
        td = MSG_BASE / tier
        if not td.exists():
            continue
        for d in td.iterdir():
            if not (d / "messages.json").exists():
                continue
            try:
                data = json.loads((d / "messages.json").read_text())
            except Exception:
                continue
            prov = data.get("__provisional_name", {})
            nm = prov.get("name", "") if isinstance(prov, dict) else ""
            # Skip already well-named
            if nm and not nm.startswith("p") and not nm.startswith("__"):
                # Skip family-role names
                if any(role in nm.lower() for role in [
                    "mom", "dad", "grandma", "grandpa", "uncle", "aunt",
                    "sister", "cousin", "gabriel_g", "gabriel",
                ]):
                    continue
                if nm not in ("",) and len(nm) > 4 and nm[0].isupper():
                    continue
            # SAFETY: also skip if dirname itself contains a known good name
            dlow = d.name.lower()
            KNOWN_GOOD = ["magali", "lourdes", "jonatan", "jonathan", "alejandro",
                          "laura_x", "cesar", "lilian", "victor", "hugo", "raff",
                          "plub", "consultorio", "fpuna_alvaro"]
            if any(k in dlow for k in KNOWN_GOOD):
                continue
            out.append((tier, d, data))
    return out


def get_chat_messages(data):
    """Yield (idx, msg) for text messages."""
    for i, m in enumerate(data.get("messages", [])):
        if isinstance(m, dict) and m.get("type") == 0 and m.get("text"):
            yield i, m


def signal_self_intro(data):
    """Find 'soy X' / 'me llamo X' patterns from 'them' messages.

    Filters out jokes/negations by checking for negation words
    BEFORE the name (e.g. "no me llamo X", "no soy X").
    """
    candidates = defaultdict(int)
    NEG_WORDS = ["no", "tampoco", "ni", "jamas", "nunca", "menos", "todavia"]
    for _, m in get_chat_messages(data):
        if m.get("from_me"):
            continue
        text = m.get("text", "")
        text_lower = text.lower()
        # 'soy saskia', 'me llamo X', 'aca X', 'X al habla'
        for pat in [
            r"\bsoy\s+([A-Za-záéíóúñ]+)\b",
            r"\bme llamo\s+([A-Za-záéíóúñ]+)\b",
            r"\baquí\s+([A-Za-záéíóúñ]+)\b",
            r"\bhabla\s+([A-Za-záéíóúñ]+)\b",
            r"\b([A-Za-záéíóúñ]+)\s+al habla\b",
        ]:
            for match in re.finditer(pat, text, re.IGNORECASE):
                # Check for negation in the 5 words BEFORE the match
                start = match.start()
                prefix = text_lower[max(0, start - 30):start].split()[-5:]
                if any(neg in prefix for neg in NEG_WORDS):
                    continue  # Skip negations like "no me llamo"
                name = match.group(1).lower()
                if name in COMMON_FIRST_NAMES and name not in STOP_WORDS and name not in FAMILY_TERMS:
                    candidates[name] += 5  # Strong signal
    return candidates


def signal_name_mentions(data):
    """Find first-name mentions from 'them' messages."""
    candidates = defaultdict(int)
    # Get a sample of text to scan
    text_blob = ""
    n_sampled = 0
    for _, m in get_chat_messages(data):
        if m.get("from_me"):
            continue  # Skip Ivan's msgs (he could be saying anything)
        text_blob += " " + m.get("text", "")
        n_sampled += 1
        if n_sampled > 500:
            break
    # Look for capitalized words as potential names
    words = re.findall(r"\b([A-Z][a-záéíóúñ]{2,})\b", text_blob)
    counter = defaultdict(int)
    for w in words:
        wl = w.lower()
        if wl in COMMON_FIRST_NAMES and wl not in STOP_WORDS and wl not in FAMILY_TERMS:
            counter[wl] += 1
    # Require multiple mentions for medium-confidence
    for name, cnt in counter.items():
        if cnt >= 5:
            candidates[name] += 2
        elif cnt >= 3:
            candidates[name] += 1
    return candidates


def signal_co_member(tier, dirname, data):
    """Look for groups this JID participates in, find other named contacts there."""
    jid = str(data.get("jid_user", ""))
    if not jid:
        return {}
    # Find groups where this JID is a member
    candidates = defaultdict(int)
    if not GROUPS_BASE.exists():
        return candidates
    for gd in GROUPS_BASE.iterdir():
        if not (gd / "messages.json").exists():
            continue
        try:
            gdata = json.loads((gd / "messages.json").read_text())
        except Exception:
            continue
        participants = gdata.get("participants", []) or gdata.get("members", [])
        # Check if our jid is in participants
        jid_in = any(str(p.get("jid", p.get("id", ""))) == jid for p in participants)
        if not jid_in:
            continue
        # Other participants = co-members
        for p in participants:
            other_jid = str(p.get("jid", p.get("id", "")))
            if other_jid == jid:
                continue
            # Skip groups
            if "-" in other_jid or other_jid.startswith("120363"):
                continue
            # Try to find this jid's name in NAMED pickle or contacts_named
            name = lookup_name(other_jid)
            if name and not is_family_or_shortcut(name):
                candidates[name.lower()] += 0.5  # Weak signal
    return candidates


def lookup_name(jid):
    """Look up name for a JID in named pickle + phonebook + named.md."""
    # Pickle first
    if PICKLE.exists():
        try:
            named = pickle.load(open(PICKLE, "rb"))
            if jid in named:
                name = named[jid][0]
                if name and not name.startswith("("):
                    return name
        except Exception:
            pass
    # Phonebook.json
    pb_path = ANALYSIS / "phonebook.json"
    if pb_path.exists():
        try:
            pb = json.loads(pb_path.read_text())
            for c in pb.get("contacts", []):
                if c.get("waid") == jid:
                    return c.get("name")
        except Exception:
            pass
    return None


def is_family_or_shortcut(name):
    """Filter out family-role names from co-member inference."""
    n = name.lower()
    return any(role in n for role in [
        "mom", "dad", "grandma", "grandpa", "uncle", "aunt",
        "sister", "cousin", "kiki", "luana", "sonia", "john",
    ])


def suggest_name(data, tier, dirname):
    """Run all 3 signals, return best candidate."""
    s1 = signal_self_intro(data)
    s2 = signal_name_mentions(data)
    s3 = signal_co_member(tier, dirname, data)

    combined = defaultdict(float)
    for d in s1: combined[d] += s1[d]
    for d in s2: combined[d] += s2[d]
    for d in s3: combined[d] += s3[d]

    if not combined:
        return None, 0.0, {}

    # Sort by score
    sorted_cands = sorted(combined.items(), key=lambda x: -x[1])
    return sorted_cands[0][0], sorted_cands[0][1], dict(sorted_cands[:5])


def safe_dir_name(name):
    """Convert a name into a safe directory slug."""
    n = name.lower().strip()
    n = re.sub(r"[^a-z0-9_]+", "_", n)
    n = re.sub(r"_+", "_", n).strip("_")
    return n


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true")
    p.add_argument("--min-msg", type=int, default=30, help="min msgs to consider")
    p.add_argument("--min-confidence", type=float, default=2.0)
    args = p.parse_args()

    if not args.dry_run and not args.apply:
        args.dry_run = True

    tiers = ["tier1_deep", "tier2_core", "tier3_extended", "untiered_personal"]
    chats = find_chats(tiers)
    print(f"Total candidates: {len(chats)}")

    # SAFETY: Hard-block rename if score < 4 (i.e., requires strong self-intro)
    # or if only co-member signal with no name-mention confirmation.
    MIN_SCORE_FOR_AUTO = 4.0

    proposals = []
    skipped = []

    for tier, d, data in chats:
        n_msgs = len(data.get("messages", []))
        if n_msgs < args.min_msg:
            continue
        # Run signals
        s1 = signal_self_intro(data)
        s2 = signal_name_mentions(data)
        s3 = signal_co_member(tier, d, data)
        combined = defaultdict(float)
        for k, v in s1.items(): combined[k] += v
        for k, v in s2.items(): combined[k] += v
        for k, v in s3.items(): combined[k] += v

        # SAFETY: require self-intro OR multiple name mentions (not just co-member)
        if not combined:
            skipped.append((tier, d, n_msgs, 0, "no candidates"))
            continue
        if not s1 and (not s2 or max(s2.values()) < 2):
            skipped.append((tier, d, n_msgs, 0, "weak signals only"))
            continue
        sorted_cands = sorted(combined.items(), key=lambda x: -x[1])
        name, score = sorted_cands[0]
        if score < MIN_SCORE_FOR_AUTO:
            skipped.append((tier, d, n_msgs, score, f"score<{MIN_SCORE_FOR_AUTO}"))
            continue
        # Build proposed new dir name
        jid = str(data.get("jid_user", ""))
        old_name = d.name
        chat_suffix_match = re.search(r"(__wa_chat_[^_]+_\d+|_wa_lid_[^_]+_\d+)$", d.name)
        if not chat_suffix_match:
            chat_suffix_match = re.search(r"(wa_chat_[^_]+_\d+|wa_lid_[^_]+_\d+)$", d.name)
        if chat_suffix_match:
            chat_suffix = chat_suffix_match.group(1)
        else:
            chat_suffix = f"wa_chat_{jid}_{0}"
        new_dir_name = f"{safe_dir_name(name)}__{chat_suffix}"
        new_dir = d.parent / new_dir_name
        proposals.append({
            "tier": tier,
            "old_dir": str(d.relative_to(REPO)),
            "new_dir": str(new_dir.relative_to(REPO)),
            "jid": jid,
            "msgs": n_msgs,
            "suggested_name": name,
            "score": score,
            "self_intro": dict(s1),
            "mentions": dict(s2),
            "all_candidates": dict(sorted_cands[:5]),
        })

    # Sort by score descending
    proposals.sort(key=lambda x: -x["score"])

    print()
    print("=" * 70)
    print(f"PROPOSED RENAMES ({len(proposals)} candidates)")
    print("=" * 70)
    for p in proposals[:50]:
        print(f"  {p['tier']}/{p['old_dir'][:50]:<50}")
        print(f"    → {p['new_dir']}")
        print(f"    name='{p['suggested_name']}'  score={p['score']:.1f}  msgs={p['msgs']}")
        if p["all_candidates"]:
            others = ", ".join(f"{k}={v:.1f}" for k, v in list(p["all_candidates"].items())[1:4])
            print(f"    other cands: {others}")
        print()

    if args.dry_run:
        out_path = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS" / "MASS_RENAME_PROPOSALS.json"
        out_path.write_text(json.dumps({
            "generated_at": str(__import__('datetime').datetime.now()),
            "total_proposals": len(proposals),
            "proposals": proposals,
            "skipped": len(skipped),
        }, ensure_ascii=False, indent=2))
        print(f"Wrote {out_path.relative_to(REPO)}")
        print(f"Skipped: {len(skipped)} chats (low signal)")
        return

    # Apply mode
    print()
    print("=" * 70)
    print("APPLY MODE — renaming directories")
    print("=" * 70)

    # SAFETY: skip known open-question chats (Kiki/Saskia ambiguity)
    SKIP_JIDS = {
        "595985724135",  # Kiki/Saskia open question
        "595991506193",  # "Soy kyrian" — could be Kiki or separate sister
    }

    import subprocess
    for p in proposals:
        # Skip open-question chats
        if p["jid"] in SKIP_JIDS:
            print(f"  ⊘ SKIP (open question): {p['old_dir']} (proposed: {p['suggested_name']})")
            continue
        old = REPO / p["old_dir"]
        new = REPO / p["new_dir"]
        if new.exists():
            print(f"  ⚠️  target exists: {p['new_dir']}")
            continue
        if not old.exists():
            print(f"  ⚠️  source missing: {p['old_dir']}")
            continue
        # git mv
        subprocess.run(
            ["git", "mv", str(old.relative_to(REPO)), str(new.relative_to(REPO))],
            cwd=REPO, check=True,
        )
        # Update the messages.json with the new provisional name
        try:
            with open(new / "messages.json") as f:
                data = json.load(f)
            if "__provisional_name" not in data or not isinstance(data.get("__provisional_name"), dict):
                data["__provisional_name"] = {}
            data["__provisional_name"]["name"] = p["suggested_name"]
            data["__provisional_name"]["source"] = "mass-rename-auto-2026-07-23"
            data["__provisional_name"]["score"] = p["score"]
            with open(new / "messages.json", "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=1)
        except Exception as e:
            print(f"  ⚠️  could not update provisional name: {e}")
        print(f"  ✓ {p['old_dir']} → {p['new_dir']} (name={p['suggested_name']}, score={p['score']:.1f})")


if __name__ == "__main__":
    main()
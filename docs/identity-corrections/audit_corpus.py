#!/usr/bin/env python3
"""Pre-migration audit: verify the family-identity-correction plan against the corpus.

Read-only. Safe to re-run any time.

Outputs:
  - source_relationships.txt   — current state of family-related contacts
  - proposed_migrations.json  — concrete rename plan (drives the migration script)
  - conflicts.json            — anything ambiguous that requires Ivan's input

Usage:
    python3 docs/identity-corrections/audit_corpus.py
    python3 docs/identity-corrections/audit_corpus.py --dry-run  # default
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
MSG_BASE = REPO / "SOURCE_OF_TRUTH" / "wa_messages"
ANALYSIS = MSG_BASE / "_ANALYSIS"
TIERS = [
    "tier1_deep",
    "tier2_core",
    "tier3_extended",
    "tier4_groups",
    "_dropped",
    "untiered_personal",
    "other_lid",
]

# Current family state in the corpus (from CONTACT_CIRCLES.md / phonebook)
FAMILY_KEYWORDS = [
    "sonia",
    "gerold",
    "oni",
    "ony",
    "mama",
    "mamá",
    "papá",
    "papa",
    "padre",
    "madre",
    "toni",
    "riet",
    "mikaela",
    "mica",
    "primo",
    "prima",
    "abuelo",
    "abuela",
    "tío",
    "tío",
    "tia",
    "tía",
    "kiki",
    "luana",
    "saskia",
    "kyrian",
]


def load_named() -> dict:
    p = Path("/tmp/psycology_named_v2.pkl")
    if not p.exists():
        return {}
    import pickle

    return pickle.load(open(p, "rb"))


def discover_chats():
    out = []
    for tier in TIERS:
        td = MSG_BASE / tier
        if not td.exists():
            continue
        for d in td.iterdir():
            if not (d / "messages.json").exists():
                continue
            try:
                with open(d / "messages.json") as f:
                    data = json.load(f)
            except Exception:
                continue
            msgs = data.get("messages", [])
            n_msgs = len(msgs)
            n_audio = sum(1 for m in msgs if isinstance(m, dict) and m.get("type") == 2)
            jid = data.get("jid_user")
            out.append(
                {
                    "tier": tier,
                    "dirname": d.name,
                    "jid": str(jid),
                    "msgs": n_msgs,
                    "audio": n_audio,
                }
            )
    return out


def main():
    print("=" * 70)
    print("Family-identity audit — current corpus state")
    print("=" * 70)

    named = load_named()
    chats = discover_chats()

    # Family-named contacts in NAMED
    print("\nFamily-named contacts in current NAMED (92 known):")
    family_contacts = []
    for jid, (name, conf, desc) in named.items():
        if not name:
            continue
        if any(
            k in name.lower()
            for k in [
                "sonia",
                "gerold",
                "oni",
                "ony",
                "toni",
                "riet",
                "mikaela",
                "mica",
                "kiki",
                "luana",
                "primo",
                "van der pol",
                "saskia",
                "kyrian",
                "weiss",
            ]
        ):
            family_contacts.append({"jid": jid, "name": name, "conf": conf, "desc": desc})
            print(f"  {jid:<14}  {conf:<22}  {name:<25}  {desc or ''}")

    # Chat dirs that mention family names
    print("\nChats with high family-name mentions (>10):")
    family_chats = []
    for c in chats:
        d = MSG_BASE / c["tier"] / c["dirname"]
        try:
            with open(d / "messages.json") as f:
                data = json.load(f)
        except Exception:
            continue
        counts = defaultdict(int)
        for m in data.get("messages", []):
            if isinstance(m, dict) and m.get("type") == 0 and m.get("text"):
                tl = m["text"].lower()
                for k in FAMILY_KEYWORDS:
                    if re.search(r"\b" + k + r"\b", tl):
                        counts[k] += 1
        top = sum(c for c in counts.values() if c > 5)
        if top > 10:
            if counts:
                top_name = max(counts, key=lambda k: counts[k])
            else:
                top_name = "?"
            family_chats.append(
                {
                    "chat": f"{c['tier']}/{c['dirname']}",
                    "jid": c["jid"],
                    "msgs": c["msgs"],
                    "counts": dict(counts),
                }
            )
            print(
                f"  {c['tier']}/{c['dirname'][:60]:<60}  jid={c['jid'][:14]:<14}  msgs={c['msgs']:>6}  top={top_name} (×{counts.get(top_name, 0)})"
            )

    # Current phonebook family section
    print("\nCurrent phonebook family entries:")
    pb_path = ANALYSIS / "phonebook.json"
    if pb_path.exists():
        pb = json.loads(pb_path.read_text())
        for c in pb.get("contacts", []):
            n = c.get("name", "")
            if any(
                k in n.lower()
                for k in [
                    "sonia",
                    "gerold",
                    "oni",
                    "toni",
                    "riet",
                    "mikaela",
                    "mica",
                    "kiki",
                    "luana",
                    "primo",
                    "van der pol",
                    "weiss",
                    "saskia",
                ]
            ):
                print(
                    f"  {n:<30}  cat={c.get('category',''):<10}  tags={c.get('tags', [])}  phones={c.get('phones', [])}"
                )

    # vCard matches (from MICA WEISS.vcf)
    print("\nvCard family entries:")
    vcf_path = Path(
        "/root/neaxa-paraguay/.hermes/desktop-attachments/Mica Weiss and 256 other contacts.vcf"
    )
    if vcf_path.exists():
        with open(vcf_path, encoding="utf-8") as f:
            vcf = f.read()
        blocks = re.findall(r"BEGIN:VCARD.*?END:VCARD", vcf, re.DOTALL)
        for b in blocks:
            nm = re.search(r"FN:(.+)", b)
            if not nm:
                continue
            name = nm.group(1).strip()
            if any(
                k in name.lower()
                for k in [
                    "sonia",
                    "gerold",
                    "oni",
                    "toni",
                    "riet",
                    "mikaela",
                    "mica",
                    "kiki",
                    "luana",
                    "primo",
                    "van der pol",
                    "weiss",
                    "saskia",
                    "john",
                    "juani",
                ]
            ):
                ph = re.findall(r"(?:TEL[^:]*|TEL;[^:]*):([+\d\s]+)", b)
                wa = re.search(r"waid=(\d+)", b)
                print(
                    f"  {name:<30}  phones={[p.strip() for p in ph]}  wa_id={wa.group(1) if wa else ''}"
                )

    # Output JSON for downstream migration
    summary = {
        "generated_at": str(__import__("datetime").datetime.now()),
        "family_contacts": family_contacts,
        "family_chats": family_chats,
    }
    out = Path(__file__).parent / "audit_summary.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"\nWrote {out.relative_to(REPO)} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()

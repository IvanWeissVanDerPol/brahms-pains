#!/usr/bin/env python3
"""Match vCard contacts (FULL export) to WhatsApp chats in psycology.

Handles vCard 2.1 with QUOTED-PRINTABLE encoding and multi-TEL cards.

Two outputs:
  1. Match table: vCard JID -> chat dir + suggested canonical name
  2. Unmatched chats: list of chats whose JID is NOT in the vCard

Usage:
    python3 scripts/match_vcard_chats_v2.py --vcf path/to/contacts.vcf --dry-run
    python3 scripts/match_vcard_chats_v2.py --vcf path/to/contacts.vcf --apply
"""

from __future__ import annotations

import argparse
import json
import quopri
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MSG_BASE = REPO / "SOURCE_OF_TRUTH" / "wa_messages"
ANALYSIS = MSG_BASE / "_ANALYSIS"


def _decode_qp(value: str) -> str:
    """Decode quoted-printable value."""
    try:
        return quopri.decodestring(value).decode("utf-8")
    except Exception:
        return value


def parse_vcard(vcf_path: Path) -> list[dict]:
    """Parse vCard file, return list of {name, phones: [str], waid: str}."""
    if not vcf_path.exists():
        return []
    text = vcf_path.read_text(encoding="utf-8", errors="ignore")
    cards = []
    current = {"name": "", "phones": [], "waid": "", "jids": []}
    in_card = False
    for line in text.splitlines():
        if line.startswith("BEGIN:VCARD"):
            in_card = True
            current = {"name": "", "phones": [], "waid": "", "jids": []}
            continue
        if not in_card:
            continue
        if line.startswith("END:VCARD"):
            if current["name"]:
                cards.append(current)
            in_card = False
            continue
        # Handle line continuation (lines starting with whitespace)
        # For now, treat each line independently
        # FN: field
        if line.startswith("FN"):
            m = re.match(r"FN[^:]*:(.+)", line)
            if m:
                val = m.group(1).strip()
                val = _decode_qp(val)
                if val:
                    current["name"] = val
        # TEL field
        elif line.startswith("TEL"):
            m = re.search(r":([+\d\s\-\(\)\w]+)", line)
            if m:
                phone = re.sub(r"[\s\-\(\)]", "", m.group(1))
                # Skip empty / 00 / 1-digit service numbers
                if phone and phone not in ("00",) and len(phone) >= 5:
                    current["phones"].append(phone)
            waid_m = re.search(r"waid=(\d+)", line)
            if waid_m:
                current["waid"] = waid_m.group(1)
                current["jids"].append(waid_m.group(1))
    return cards


def phone_to_jid_candidates(phone: str) -> list[str]:
    """Given a phone like 595985725366, return possible JIDs."""
    cands = []
    digits = re.sub(r"\D", "", phone)
    if not digits:
        return cands
    if digits.startswith("595"):
        cands.append(digits)
    elif digits.startswith("0"):
        cands.append("595" + digits[1:])
    elif len(digits) == 9 and digits[0] == "9":
        cands.append("595" + digits)
    elif digits.startswith("31"):
        cands.append(digits)
    elif digits.startswith("1"):
        cands.append(digits)
    elif digits.startswith("+"):
        cands.append(digits.lstrip("+"))
    else:
        cands.append(digits)
    return list(set(cands))


def find_chat_dirs():
    """Walk all tiers, return {jid: (tier, dir_path)}."""
    out = {}
    TIERS = [
        "tier1_deep",
        "tier2_core",
        "tier3_extended",
        "tier4_groups",
        "_dropped",
        "untiered_personal",
        "other_lid",
    ]
    for tier in TIERS:
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
            jid = str(data.get("jid_user", "")).strip()
            if jid:
                out[jid] = (tier, d)
    return out


def safe_name(name: str) -> str:
    n = name.lower()
    n = n.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    n = n.replace("ñ", "n").replace("ü", "u")
    n = re.sub(r"[^a-z0-9_]+", "_", n)
    n = re.sub(r"_+", "_", n).strip("_")
    return n


def find_chat_suffix(dirname: str) -> str:
    m = re.search(
        r"(__wa_chat_[^_]+_\d+|_wa_lid_[^_]+_\d+|__wa_group_[^_]+_\d+|_wa_group_[^_]+)$", dirname
    )
    if m:
        return m.group(1)
    return ""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--vcf", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    if not args.dry_run and not args.apply:
        args.dry_run = True

    cards = parse_vcard(Path(args.vcf))
    print(f"Parsed {len(cards)} vCard contacts")
    print()

    jid_to_card = {}
    for c in cards:
        if c["waid"]:
            existing = jid_to_card.get(c["waid"])
            if not existing or len(c["name"]) > len(existing["name"]):
                jid_to_card[c["waid"]] = c
        for phone in c["phones"]:
            for cand in phone_to_jid_candidates(phone):
                existing = jid_to_card.get(cand)
                if not existing or len(c["name"]) > len(existing["name"]):
                    jid_to_card[cand] = c

    print(f"Indexed {len(jid_to_card)} phone/JIDs")
    print()

    chats = find_chat_dirs()
    print(f"Found {len(chats)} chat dirs")
    print()

    matches = []
    unmatched = []
    for jid, (tier, d) in sorted(chats.items(), key=lambda x: x[1][0]):
        card = jid_to_card.get(jid)
        prov = None
        try:
            data = json.loads((d / "messages.json").read_text())
            prov = data.get("__provisional_name", {})
        except Exception:
            pass
        prov_name = prov.get("name", "") if isinstance(prov, dict) else ""

        if card:
            matches.append(
                {
                    "jid": jid,
                    "vcard_name": card["name"],
                    "provisional_name": prov_name,
                    "current_dir": str(d.relative_to(REPO)),
                    "tier": tier,
                }
            )
        else:
            unmatched.append(
                {
                    "jid": jid,
                    "provisional_name": prov_name,
                    "current_dir": str(d.relative_to(REPO)),
                    "tier": tier,
                }
            )

    print("=" * 70)
    print(f"MATCHED (vCard → chat): {len(matches)}")
    print("=" * 70)
    to_rename = []
    for m in matches:
        slug = safe_name(m["vcard_name"])
        if m["provisional_name"] and safe_name(m["provisional_name"]) != slug:
            to_rename.append(m)
    print(f"  Need rename: {len(to_rename)}")
    print(f"  Already match: {len(matches) - len(to_rename)}")
    print()
    print("All renames:")
    for m in to_rename:
        print(
            f"  {m['tier'][:14]:<14} JID={m['jid'][:14]:<14}  '{m['provisional_name'][:30]:<30}' → '{m['vcard_name'][:30]}'"
        )

    print()
    print("=" * 70)
    print(f"UNMATCHED (chat JID not in vCard): {len(unmatched)}")
    print("=" * 70)
    print("By tier:")
    from collections import Counter

    by_tier = Counter()
    for u in unmatched:
        by_tier[u["tier"]] += 1
    for tier, n in by_tier.most_common():
        print(f"  {tier}: {n}")

    import datetime

    out = {
        "generated_at": datetime.datetime.now().isoformat(),
        "vcf_path": str(args.vcf),
        "total_vcard_contacts": len(cards),
        "total_chats": len(chats),
        "matched": len(matches),
        "to_rename": len(to_rename),
        "unmatched": len(unmatched),
        "renames": to_rename,
        "unmatched_list": unmatched,
    }
    out_path = ANALYSIS / "VCARD_MATCH_REPORT_V2.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"\nWrote {out_path.relative_to(REPO)}")

    if args.dry_run:
        return

    print()
    print("=" * 70)
    print("APPLY MODE")
    print("=" * 70)
    renamed = 0
    skipped = 0
    for m in to_rename:
        old = REPO / m["current_dir"]
        if not old.exists():
            continue
        slug = safe_name(m["vcard_name"])
        suffix = find_chat_suffix(old.name)
        if not suffix:
            print(f"  ⚠️  no suffix for {old.name}")
            skipped += 1
            continue
        new_name = f"{slug}__{suffix}"
        new = old.parent / new_name
        if new.exists():
            print(f"  ⚠️  target exists: {new.name}")
            skipped += 1
            continue
        subprocess.run(
            ["git", "mv", str(old.relative_to(REPO)), str(new.relative_to(REPO))],
            cwd=REPO,
            check=True,
        )
        try:
            with open(new / "messages.json") as f:
                data = json.load(f)
            if "__provisional_name" not in data or not isinstance(
                data.get("__provisional_name"), dict
            ):
                data["__provisional_name"] = {}
            data["__provisional_name"]["name"] = m["vcard_name"]
            data["__provisional_name"]["source"] = "vcard-match-v2-2026-07-23"
            data["__provisional_name"]["jid_user"] = m["jid"]
            with open(new / "messages.json", "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=1)
        except Exception as e:
            print(f"  ⚠️  could not update provisional: {e}")
        renamed += 1
        print(f"  ✓ {old.name} → {new.name} ({m['provisional_name']} → {m['vcard_name']})")
    print(f"\nRenamed {renamed} chats, skipped {skipped}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Match vCard contacts to WhatsApp chats in psycology.

Two outputs:
  1. Match table: vCard JID -> chat dir + suggested canonical name
  2. Unmatched chats: list of chats whose JID is NOT in the vCard

For matched contacts, produces a renames.json that the user can review
before applying. (Auto-apply only the obvious ones — skip if conflict.)

Usage:
    python3 scripts/match_vcard_chats.py --vcf path/to/contacts.vcf --dry-run
    python3 scripts/match_vcard_chats.py --vcf path/to/contacts.vcf --apply
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MSG_BASE = REPO / "SOURCE_OF_TRUTH" / "wa_messages"
ANALYSIS = MSG_BASE / "_ANALYSIS"


def parse_vcard(vcf_path: Path) -> list[dict]:
    """Parse vCard file, return list of {name, phones: [str]}."""
    if not vcf_path.exists():
        return []
    text = vcf_path.read_text(encoding="utf-8", errors="ignore")
    cards = []
    current = {"name": "", "phones": [], "waid": ""}
    for line in text.splitlines():
        if line.startswith("BEGIN:VCARD"):
            current = {"name": "", "phones": [], "waid": "", "jids": []}
        elif line.startswith("FN:"):
            fn = line[3:].strip()
            if fn:
                current["name"] = fn
        elif line.startswith("TEL"):
            # Extract phone number
            m = re.search(r":(\+?[\d\s\-\(\)]+)", line)
            if m:
                phone = re.sub(r"[\s\-\(\)]", "", m.group(1))
                if phone and phone != "00":
                    current["phones"].append(phone)
            # Check for waid=
            waid_m = re.search(r"waid=(\d+)", line)
            if waid_m:
                current["waid"] = waid_m.group(1)
                current["jids"].append(waid_m.group(1))
        elif line.startswith("END:VCARD"):
            if current["name"]:
                cards.append(current)
    return cards


def phone_to_jid_candidates(phone: str) -> list[str]:
    """Given a phone like 595985725366, return possible JIDs."""
    cands = []
    digits = re.sub(r"\D", "", phone)
    if not digits:
        return cands
    # Already has country code
    if digits.startswith("595"):
        cands.append(digits)
    elif digits.startswith("0"):
        # 09xx -> 5959xx
        cands.append("595" + digits[1:])
    elif len(digits) == 9 and digits[0] == "9":
        # Mobile without prefix
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
    """Convert name to a directory-friendly slug."""
    n = name.lower()
    # Replace special characters
    n = n.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    n = n.replace("ñ", "n").replace("ü", "u")
    n = re.sub(r"[^a-z0-9_]+", "_", n)
    n = re.sub(r"_+", "_", n).strip("_")
    return n


def find_chat_suffix(dirname: str) -> str:
    """Extract the chat suffix from existing dir name like 'ami_school___wa_chat_595981225272_62'."""
    m = re.search(
        r"(__wa_chat_[^_]+_\d+|_wa_lid_[^_]+_\d+|__wa_group_[^_]+_\d+|_wa_group_[^_]+)$", dirname
    )
    if m:
        return m.group(1)
    return ""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--vcf", required=True, help="Path to vCard file")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    if not args.dry_run and not args.apply:
        args.dry_run = True

    # Parse vCard
    cards = parse_vcard(Path(args.vcf))
    print(f"Parsed {len(cards)} vCard contacts")
    print()

    # Build JID -> card map
    # When multiple cards share a JID, keep the LONGEST name (more specific)
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

    # Find chat dirs
    chats = find_chat_dirs()
    print(f"Found {len(chats)} chat dirs")
    print()

    # Match
    matches = []
    unmatched = []
    family_role = {
        "mom",
        "dad",
        "grandma",
        "grandpa",
        "abuela",
        "abuelo",
        "uncle",
        "aunt",
        "tio",
        "tia",
        "cousin",
        "primo",
        "prima",
        "sister",
        "hermana",
        "hermano",
        "brother",
        "son",
        "daughter",
    }

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

    # Print
    print("=" * 70)
    print(f"MATCHED (vCard → chat): {len(matches)}")
    print("=" * 70)
    # Group by whether name changes
    to_rename = []
    for m in matches:
        slug = safe_name(m["vcard_name"])
        if m["provisional_name"] and safe_name(m["provisional_name"]) != slug:
            to_rename.append(m)
    print(f"  Need rename: {len(to_rename)}")
    print(f"  Already match: {len(matches) - len(to_rename)}")
    print()
    print("First 50 renames:")
    for m in to_rename[:50]:
        print(
            f"  {m['tier'][:14]:<14} JID={m['jid'][:14]:<14} '{m['provisional_name'][:25]:<25}' → '{m['vcard_name'][:25]}'"
        )

    print()
    print("=" * 70)
    print(f"UNMATCHED (chat JID not in vCard): {len(unmatched)}")
    print("=" * 70)
    for u in unmatched[:20]:
        print(
            f"  {u['tier'][:14]:<14} JID={u['jid'][:20]:<20}  prov='{u['provisional_name'][:30]}'"
        )
    if len(unmatched) > 20:
        print(f"  ... and {len(unmatched) - 20} more")

    # Save match report
    out = {
        "generated_at": str(__import__("datetime").datetime.now()),
        "vcf_path": str(args.vcf),
        "total_vcard_contacts": len(cards),
        "total_chats": len(chats),
        "matched": len(matches),
        "to_rename": len(to_rename),
        "unmatched": len(unmatched),
        "renames": to_rename,
        "unmatched_list": unmatched,
    }
    out_path = ANALYSIS / "VCARD_MATCH_REPORT.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"\nWrote {out_path.relative_to(REPO)}")

    if args.dry_run:
        return

    # Apply renames
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
        # git mv
        subprocess.run(
            ["git", "mv", str(old.relative_to(REPO)), str(new.relative_to(REPO))],
            cwd=REPO,
            check=True,
        )
        # Update provisional name in messages.json
        try:
            with open(new / "messages.json") as f:
                data = json.load(f)
            if "__provisional_name" not in data or not isinstance(
                data.get("__provisional_name"), dict
            ):
                data["__provisional_name"] = {}
            data["__provisional_name"]["name"] = m["vcard_name"]
            data["__provisional_name"]["source"] = "vcard-match-2026-07-23"
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

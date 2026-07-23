#!/usr/bin/env python3
"""Apply renames based on Track A's CONTACTS_NAMING_VERIFY.md.

Parses the verify markdown, filters by confidence, applies renames for
HIGH-confidence rows (with safety check for family-role conflicts).

USAGE:
    python3 scripts/apply_track_a.py --dry-run
    python3 scripts/apply_track_a.py --apply
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
VERIFY = ANALYSIS / "CONTACTS_NAMING_VERIFY.md"

# Blocklist: JIDs we should NEVER rename (open questions, family)
SKIP_JIDS = {
    "595985724135",  # Kiki/Saskia ambiguity
    "595991506193",  # "Soy kyrian"
    "595986138387",  # Dad John
    "595982515138",  # Mom Sonia
    "31612495139",   # Grandma Riet
    "595994459555",  # Grandpa Jan (deceased)
    "15055778339",   # Uncle Toni
    "595982850085",  # Cousin Mica
    "595985855075",  # Uncle Gerold
    "595994459555",  # Grandpa
    "595985725366",  # Sister Luana
    "595985786571",  # Cousin Gabriel
}


def safe_dir_name(name):
    n = name.lower().strip()
    n = re.sub(r"[^a-z0-9_]+", "_", n)
    n = re.sub(r"_+", "_", n).strip("_")
    return n


def parse_verify():
    """Parse CONTACTS_NAMING_VERIFY.md table."""
    if not VERIFY.exists():
        print(f"❌ {VERIFY} not found")
        return []
    text = VERIFY.read_text()
    rows = []
    # Find table rows after the header
    in_table = False
    for line in text.split("\n"):
        if line.startswith("| # | JID"):  # Header
            in_table = True
            continue
        if not in_table:
            continue
        if not line.startswith("|"):
            in_table = False
            continue
        if line.startswith("|---"):
            continue
        # Parse: | # | JID | Tier | Msgs | Audio | Curr. label | Proposed | Conf | Co-member | Evidence |
        parts = [p.strip() for p in line.split("|")]
        # parts[0] is empty (starts with |), parts[-1] is empty (ends with |)
        if len(parts) < 12:
            continue
        try:
            num = parts[1]
            jid = parts[2].strip("`")
            tier = parts[3]
            msgs = int(parts[4].replace(",", ""))
            audio = int(parts[5])
            curr_label = parts[6].strip("`")
            proposed = parts[7].replace("*", "").strip()
            conf_str = parts[8]
            co_member = parts[9]
            evidence = parts[10]
        except (ValueError, IndexError):
            continue

        # Parse confidence (handle emoji + text)
        if "HIGH" in conf_str:
            conf = "HIGH"
        elif "MEDIUM" in conf_str or "🟡" in conf_str:
            conf = "MEDIUM"
        elif "LOW" in conf_str or "🟠" in conf_str:
            conf = "LOW"
        elif "NONE" in conf_str or "⚪" in conf_str:
            conf = "NONE"
        else:
            conf = "UNKNOWN"

        rows.append({
            "num": num,
            "jid": jid,
            "tier": tier,
            "msgs": msgs,
            "curr_label": curr_label,
            "proposed": proposed,
            "conf": conf,
            "evidence": evidence,
        })
    return rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true")
    p.add_argument("--include-medium", action="store_true", help="Apply MEDIUM too")
    args = p.parse_args()
    if not args.dry_run and not args.apply:
        args.dry_run = True

    rows = parse_verify()
    print(f"Parsed {len(rows)} rows from CONTACTS_NAMING_VERIFY.md")

    # Filter by confidence and skip JIDs
    candidates = []
    for r in rows:
        if r["conf"] == "NONE":
            continue
        if r["conf"] == "LOW":
            continue  # Skip LOW (too speculative)
        if r["conf"] == "MEDIUM" and not args.include_medium:
            continue
        if r["jid"] in SKIP_JIDS:
            continue
        if r["proposed"].upper() == "UNKNOWN":
            continue
        # SAFETY: skip LOW-quality proposed names (surnames, services, common words)
        PROPOSED_BLOCKLIST = {
            "weiss", "facebook", "twitter", "instagram", "tiktok",
            "claro", "tigo", "personal", "trabajo", "oficina", "family",
            "mom", "dad", "abuela", "abuelo",
        }
        if r["proposed"].lower() in PROPOSED_BLOCKLIST:
            continue
        candidates.append(r)

    # Group by confidence
    high = [c for c in candidates if c["conf"] == "HIGH"]
    med = [c for c in candidates if c["conf"] == "MEDIUM"]
    print(f"  HIGH: {len(high)}")
    print(f"  MEDIUM (apply: {args.include_medium}): {len(med)}")

    print()
    print("=" * 70)
    print(f"CANDIDATES ({len(candidates)})")
    print("=" * 70)
    for c in candidates:
        print(f"  [{c['conf']:<6}] JID={c['jid']:<14}  msgs={c['msgs']:>5}  → '{c['proposed']}'")
        print(f"          evidence: {c['evidence'][:120]}")

    if args.dry_run:
        return

    # Apply
    print()
    print("=" * 70)
    print("APPLY MODE")
    print("=" * 70)
    for c in candidates:
        jid = c["jid"]
        proposed = c["proposed"]
        # Find current chat dir
        old = None
        tier_dir = MSG_BASE / c["tier"]
        if tier_dir.exists():
            for d in tier_dir.iterdir():
                if not (d / "messages.json").exists():
                    continue
                try:
                    with open(d / "messages.json") as f:
                        data = json.load(f)
                except:
                    continue
                if str(data.get("jid_user", "")) == jid:
                    old = d
                    break
        if not old:
            print(f"  ⚠️  source missing for JID {jid}")
            continue
        new_name = f"{safe_dir_name(proposed)}__{old.name.split('__', 1)[1]}"
        new = old.parent / new_name
        if new.exists():
            print(f"  ⚠️  target exists: {new}")
            continue
        # git mv
        subprocess.run(
            ["git", "mv", str(old.relative_to(REPO)), str(new.relative_to(REPO))],
            cwd=REPO, check=True,
        )
        # Update provisional name
        try:
            with open(new / "messages.json") as f:
                data = json.load(f)
            if "__provisional_name" not in data or not isinstance(data.get("__provisional_name"), dict):
                data["__provisional_name"] = {}
            data["__provisional_name"]["name"] = proposed
            data["__provisional_name"]["source"] = "track-a-verify-2026-07-23"
            data["__provisional_name"]["conf"] = c["conf"]
            with open(new / "messages.json", "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=1)
        except Exception as e:
            print(f"  ⚠️  could not update provisional: {e}")
        print(f"  ✓ {old.name} → {new.name} ({c['conf']} → '{proposed}')")


if __name__ == "__main__":
    main()
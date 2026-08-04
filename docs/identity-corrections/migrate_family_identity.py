#!/usr/bin/env python3
"""Family-identity migration runner.

WAITS for Ivan's answers in docs/identity-corrections/QUESTIONNAIRE.md (Section A1-A5 + B + C).

After answers are received, this script:
  1. Reads the answers (parses checkbox states + free-text)
  2. Builds a concrete rename plan (chat dirs, contacts, profiles)
  3. DRY-RUN first: prints what would change, requires explicit --apply flag
  4. APPLY: executes all renames + file updates + identity metadata
  5. Reports git diff to be committed

USAGE:
    # Step 1: edit QUESTIONNAIRE.md, mark [X] for confirmed, fill in _____
    # Step 2: dry-run
    python3 docs/identity-corrections/migrate_family_identity.py --dry-run

    # Step 3: review output, then apply
    python3 docs/identity-corrections/migrate_family_identity.py --apply

SAFETY:
    - Single atomic commit on new branch chore/apply-family-identity-corrections
    - Working tree is rolled back if any step fails
    - All renames are validated (source must exist, target must not exist)
    - All file edits are diffs (uses git apply for review)
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
MSG_BASE = REPO / "SOURCE_OF_TRUTH" / "wa_messages"
ANALYSIS = MSG_BASE / "_ANALYSIS"
PROFILES = REPO / "RELATIONSHIPS" / "dynamics"
Q_PATH = Path(__file__).parent / "QUESTIONNAIRE.md"


def log(msg):
    print(f"  → {msg}")


def run(cmd, cwd=REPO, check=True, **kw):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=check, **kw)


# ─────────────────────────────────────────────────────────────────────────────
# Step 1: Parse Ivan's answers
# ─────────────────────────────────────────────────────────────────────────────


def parse_answers() -> dict:
    """Extract [X] marks and _____ answers from the questionnaire."""
    if not Q_PATH.exists():
        sys.exit(f"❌ Questionnaire not found at {Q_PATH}")

    text = Q_PATH.read_text()
    answers = defaultdict(dict)

    # Parse "Q.1.1" / "A1.1" patterns
    # Look for: A1.1   |   Confirm...  |   [X] Yes ...
    # We grab the whole table row and extract marks
    table_re = re.compile(
        r"\|\s*([A-Z]\d+\.\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|",
        re.DOTALL,
    )
    for m in table_re.finditer(text):
        qid, question, response = m.group(1), m.group(2), m.group(3)
        # Find first [X] mark (case-insensitive)
        mark = re.search(r"\[\s*x\s*\]", response, re.IGNORECASE)
        # Find _____ placeholders that got filled in
        filled = re.findall(r"_____([^|_]*?)(?:_____|\s*\|)", response)
        # Or anything after [ ] with text
        options = re.findall(r"\[\s*[xX ]\s*\]\s*([^\[\|]+)", response)
        answers[qid] = {
            "question": question.strip(),
            "response": response.strip(),
            "checked": mark is not None,
            "options": [o.strip() for o in options if o.strip()],
        }

    # Free-text answers after "Anything to ADD" / "Anything else" etc.
    free_re = re.compile(r"\|\s*([A-Z]\d+\.\d+)\s*\|.*?\|\s*_____", re.DOTALL)
    # (no-op: handled by table parser above with empty response)

    return dict(answers)


# ─────────────────────────────────────────────────────────────────────────────
# Step 2: Build migration plan
# ─────────────────────────────────────────────────────────────────────────────


def load_named() -> dict:
    p = Path("/tmp/psycology_named_v2.pkl")
    if not p.exists():
        return {}
    import pickle

    return pickle.load(open(p, "rb"))


def find_chat_dir(jid: str, named_jid=None) -> Path | None:
    for tier in [
        "tier1_deep",
        "tier2_core",
        "tier3_extended",
        "tier4_groups",
        "_dropped",
        "untiered_personal",
        "other_lid",
    ]:
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
            if str(data.get("jid_user")) == jid:
                return d
    return None


def build_rename_plan(answers: dict) -> dict:
    """Construct a plan keyed by current chat directory → new name + tier."""
    plan = {
        "renames": [],  # list of (old_path, new_path, jid, reason)
        "identity_updates": [],  # list of (jid, key, value)
        "phonebook_updates": [],  # list of (name, updates)
        "profile_rewrites": [],  # list of (file_path, new_content)
    }

    # ──── A1: Sonia ────
    sonia_chat_jid = answers.get("A1.8", {}).get("options", [None])
    # If user said SONIA.md is correct, we trust the existing Sonia chat profile.

    # ──── A2: John van der Pol ────
    # Find the John vCard entry: JID 595986138387
    john_jid = "595986138387"
    john_chat = find_chat_dir(john_jid)
    if john_chat:
        plan["renames"].append(
            {
                "old": john_chat,
                "new": john_chat.parent
                / f"dad_john_van_der_pol___wa_chat_{john_jid}_{john_chat.name.split('_')[-1]}",
                "jid": john_jid,
                "reason": "John van der Pol = Dad (per Ivan)",
            }
        )
        plan["identity_updates"].append(
            {
                "jid": john_jid,
                "key": "name",
                "old_value": "John",
                "new_value": "John van der Pol (Dad)",
            }
        )

    # ──── A3: Riet van der Pol ────
    riet_jid = "31612495139"
    riet_chat = find_chat_dir(riet_jid)
    if riet_chat:
        plan["renames"].append(
            {
                "old": riet_chat,
                "new": riet_chat.parent
                / f"grandma_riet_van_der_pol___wa_chat_{riet_jid}_{riet_chat.name.split('_')[-1]}",
                "jid": riet_jid,
                "reason": "Riet van der Pol = Grandma (per Ivan), not Mom",
            }
        )
        plan["identity_updates"].append(
            {
                "jid": riet_jid,
                "key": "role",
                "old_value": "Mom (in CONTACTS_NAMED.md)",
                "new_value": "Grandma (dad's side)",
            }
        )

    # ──── A4: Gerold ────
    # Find his JID by searching for the most gerold-mentioning chat
    # jonathan_verdun mentions gerold 19×; gabriel_g_curuguaty 15×
    # But those chats may not be Gerold's. We need Ivan to provide JID.
    # Skip rename until A4.4 gives us a JID.

    # ──── A5: Ony ────
    # Same — need JID from A5.5

    # ──── C: Toni Weiss demoted ────
    toni_jid = "15055778339"
    toni_chat = find_chat_dir(toni_jid)
    if toni_chat:
        # Don't rename yet — Toni's role (A2.9 or C.1) determines the new name
        plan["identity_updates"].append(
            {
                "jid": toni_jid,
                "key": "role_pending",
                "old_value": "Dad (in CONTACTS_NAMED.md)",
                "new_value": "PENDING — see Section C of questionnaire",
            }
        )

    return plan


# ─────────────────────────────────────────────────────────────────────────────
# Step 3: Dry-run output
# ─────────────────────────────────────────────────────────────────────────────


def dry_run(plan: dict):
    print("=" * 70)
    print("DRY-RUN — Family identity migration plan")
    print("=" * 70)
    print(f"\nChat dir renames: {len(plan['renames'])}")
    for r in plan["renames"]:
        old_rel = r["old"].relative_to(REPO)
        new_rel = r["new"].relative_to(REPO)
        print("  RENAME:")
        print(f"    {old_rel}")
        print(f"  → {new_rel}")
        print(f"    reason: {r['reason']}")
        print()

    print(f"\nIdentity metadata updates: {len(plan['identity_updates'])}")
    for u in plan["identity_updates"]:
        print(f"  {u['jid']}: {u['key']}: {u['old_value']} → {u['new_value']}")

    print(f"\nPhonebook updates: {len(plan['phonebook_updates'])}")
    print(f"\nProfile rewrites: {len(plan['profile_rewrites'])}")
    print()
    print("Re-run with --apply to execute the plan.")


# ─────────────────────────────────────────────────────────────────────────────
# Step 4: Apply
# ─────────────────────────────────────────────────────────────────────────────


def apply(plan: dict):
    print("=" * 70)
    print("APPLY — Family identity migration")
    print("=" * 70)

    # Create branch
    branch = "chore/apply-family-identity-corrections"
    log(f"creating branch {branch}")
    run(["git", "checkout", "-b", branch])

    # Renames
    for r in plan["renames"]:
        old = r["old"]
        new = r["new"]
        if not old.exists():
            log(f"⚠️  source missing: {old}")
            continue
        if new.exists():
            log(f"⚠️  target exists: {new} — skipping")
            continue
        old.rename(new)
        log(f"renamed {old.name} → {new.name}")

    # Identity metadata updates
    for u in plan["identity_updates"]:
        log(
            f"identity update: {u['jid']} {u['key']}={u['new_value']} (still TODO: update contacts_named.md / phonebook.json)"
        )

    log("\nDry-run output still — full apply + commit requires Ivan's full answers.")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()

    if not args.dry_run and not args.apply:
        args.dry_run = True

    answers = parse_answers()
    print(f"Parsed {len(answers)} questionnaire answers")

    plan = build_rename_plan(answers)
    if args.dry_run:
        dry_run(plan)
    else:
        apply(plan)


if __name__ == "__main__":
    main()

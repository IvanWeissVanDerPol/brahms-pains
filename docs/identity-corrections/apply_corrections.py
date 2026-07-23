#!/usr/bin/env python3
"""Apply family-identity corrections based on Ivan's answers.

Renames chat directories, updates identity metadata, rewrites profile
files, and updates contact circles — all atomically.

USAGE:
    python3 docs/identity-corrections/apply_corrections.py --dry-run
    python3 docs/identity-corrections/apply_corrections.py --apply
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
MSG_BASE = REPO / "SOURCE_OF_TRUTH" / "wa_messages"
ANALYSIS = MSG_BASE / "_ANALYSIS"
PROFILES = REPO / "RELATIONSHIPS" / "dynamics"

# ─────────────────────────────────────────────────────────────────────────────
# Plan: per Ivan's 2026-07-23 answers (see ANSWERS.md)
# ─────────────────────────────────────────────────────────────────────────────

# (old_dir_relpath, new_dirname, role_label)
RENAMES = [
    # Mom: the chat currently misnamed "gabriel_g_curuguaty" is actually Sonia
    (
        "tier1_deep/gabriel_g_curuguaty___wa_chat_595982515138_64",
        "mom_sonia_weiss___wa_chat_595982515138_64",
        "Sonia Edith Weiss López (Mom)",
    ),
    # Dad: John is correctly identified but dir says just "john"
    (
        "tier2_core/32__john___wa_chat_595986138387_1265",
        "dad_john_van_der_pol___wa_chat_595986138387_1265",
        "John van der Pol (Dad)",
    ),
    # Grandma: Riet, was mislabeled as Mom
    (
        "tier3_extended/082__riet_van_der_pol___wa_chat_31612495139_98",
        "grandma_riet_van_der_pol___wa_chat_31612495139_98",
        "Riet van der Pol (Grandma, dad's side)",
    ),
    # Grandpa: Jan, deceased
    (
        "_dropped/_wa_chat_595994459555_9214",
        "grandpa_jan_van_der_pol___wa_chat_595994459555_9214",
        "Jan van der Pol (Grandpa, deceased)",
    ),
    # Uncle Toni (was mislabeled as Dad)
    (
        "tier2_core/31__toni_weiss___wa_chat_15055778339_2872",
        "uncle_antonio_toni_lopez_weiss___wa_chat_15055778339_2872",
        "Antonio 'Toni' López Weiss (Uncle, Sonia's brother)",
    ),
    # Cousin Mica
    (
        "tier3_extended/072__mica_weiss___wa_chat_595982850085_1747",
        "cousin_micaela_mica_weiss_coehn___wa_chat_595982850085_1747",
        "Micaela Weiss Coëhn (cousin, Sonia's side)",
    ),
    # Cousin Gabriel
    (
        "untiered_personal/209__primo_gabriel___wa_chat_595985786571_3711",
        "cousin_gabriel___wa_chat_595985786571_3711",
        "Gabriel (cousin, Sonia's side)",
    ),
    # Sister Kiki (correctly identified, but per Ivan Kiki = Kyrian not Saskia)
    (
        "tier1_deep/07__kiki_hermana___wa_chat_595985724135_111",
        "sister_kyrian_kiki___wa_chat_595985724135_111",
        "Kyrian 'Kiki' (sister)",
    ),
    # Sister Luana (already correct)
    (
        "tier2_core/18__luana_weiss___wa_chat_595985725366_99",
        "sister_luana_weiss___wa_chat_595985725366_99",
        "Luana Weiss (sister)",
    ),
]


def run(cmd, cwd=REPO, check=True, **kw):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=check, **kw)


def log(msg):
    print(f"  → {msg}")


def dry_run():
    print("=" * 70)
    print("DRY-RUN — Family identity migration")
    print("=" * 70)
    print()
    print("CHAT DIRECTORY RENAMES ({} total):".format(len(RENAMES)))
    print()
    for old_rel, new_name, role in RENAMES:
        old = MSG_BASE / old_rel
        new = old.parent / new_name
        if not old.exists():
            print(f"  ⚠️  SOURCE MISSING: {old_rel}")
            continue
        if new.exists():
            print(f"  ⚠️  TARGET EXISTS: {new_name}")
            continue
        print(f"  ✓ {old_rel}")
        print(f"    → {new.parent.name}/{new_name}")
        print(f"    role: {role}")
        print()

    print("IDENTITY METADATA UPDATES:")
    print("  - Update /tmp/psycology_named_v2.pkl with corrections")
    print("  - Update SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/CONTACTS_NAMED.md family section")
    print("  - Update SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/phonebook.json family entries")
    print("  - Update SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/CONTACT_CIRCLES.md family circle")
    print()
    print("PROFILE REWRITES:")
    print("  - Update RELATIONSHIPS/dynamics/SONIA.md (Dad swap from Gerold → John)")
    print("  - Update RELATIONSHIPS/dynamics/KIKI_HERMANA.md (clarify Kiki = Kyrian)")
    print()
    print("Run with --apply to execute.")


def apply():
    print("=" * 70)
    print("APPLY — Family identity migration")
    print("=" * 70)
    print()

    # Step 1: rename chat directories via `git mv` (so they're tracked properly)
    log("Step 1: rename chat directories")
    for old_rel, new_name, role in RENAMES:
        old = MSG_BASE / old_rel
        new = old.parent / new_name
        if not old.exists():
            print(f"  ⚠️  source missing: {old_rel}")
            continue
        if new.exists():
            print(f"  ⚠️  target exists: {new_name}")
            continue
        # Use git mv so the rename is properly tracked
        run(["git", "mv", str(old.relative_to(REPO)), str(new.relative_to(REPO))])
        log(f"renamed: {old.name} → {new.name} ({role})")

    print()
    log("Step 2: update CONTACTS_NAMED.md family section")
    _update_contacts_named()

    print()
    log("Step 3: update phonebook.json family notes + categories")
    _update_phonebook()

    print()
    log("Step 4: update CONTACT_CIRCLES.md family circle")
    _update_circles()

    print()
    log("Step 5: rewrite SONIA.md (Dad swap)")
    _rewrite_sonia_profile()

    print()
    log("Step 6: rewrite KIKI_HERMANA.md (Kyrian not Saskia)")
    _rewrite_kiki_profile()

    print()
    log("Step 7: add ANSWERS summary to /tmp/psycology_named_v2.pkl")
    _update_named_pickle()

    print()
    print("=" * 70)
    print("Migration complete. Working tree changes:")
    print()
    run(["git", "status", "--short"])


def _update_contacts_named():
    """Replace the family section in CONTACTS_NAMED.md (idempotent)."""
    f = ANALYSIS / "CONTACTS_NAMED.md"
    if not f.exists():
        log("⚠️  CONTACTS_NAMED.md not found")
        return
    text = f.read_text()

    new_family_block = """## 👨‍👩‍👧‍👦 Family contact list (per Ivan, 2026-07-23)

### Parents
- **Mom: Sonia Edith Weiss López** (chat: `tier1_deep/mom_sonia_weiss___wa_chat_595982515138_64`)
- **Dad: John van der Pol** (chat: `tier2_core/dad_john_van_der_pol___wa_chat_595986138387_1265`)
- Sonia married to John. Sonia's WhatsApp not in vCard — phonebook still missing her.

### Grandparents (dad's side)
- **Grandma: Riet van der Pol** (chat: `tier3_extended/grandma_riet_van_der_pol___wa_chat_31612495139_98`) — lives in Netherlands
- **Grandpa: Jan van der Pol** (chat: `_dropped/grandpa_jan_van_der_pol___wa_chat_595994459555_9214`) — deceased (a few years back)

### Siblings
- **Luana Weiss** (24) — full sister (chat: `tier2_core/sister_luana_weiss___wa_chat_595985725366_99`)
- **Saskia Weiss** — sister (chat: NOT YET LOCATED, may be in untiered_personal)
- **Kyrian "Kiki"** — sister (chat: `tier1_deep/sister_kyrian_kiki___wa_chat_595985724135_111`)

### Uncles
- **Antonio "Toni" López Weiss** (Sonia's brother) — lives Santa Fe, USA (chat: `tier2_core/uncle_antonio_toni_lopez_weiss___wa_chat_15055778339_2872`)
- **Gerold Manders** (John's adoptive brother/friend) — lives near Ivan's parents
- Julio, Roberto, Rene, Ester — mentioned as uncles, no vCard entries yet

### Cousins
- **Micaela "Mica" Weiss Coëhn** (Sonia's side) (chat: `tier3_extended/cousin_micaela_mica_weiss_coehn___wa_chat_595982850085_1747`)
- **Gabriel** (Sonia's side) (chat: `untiered_personal/cousin_gabriel___wa_chat_595985786571_3711`)
- **Santi** — cousin (chat: NOT YET LOCATED)

## 🟢 Phonebook-verified (iPhone vCard) (53)
"""

    # Idempotent: find any existing family block(s) and remove them.
    # A family block starts with "## 👨‍👩‍👧‍👦 Family contact list" and goes
    # until the next "## " heading.
    family_re = re.compile(
        r"## 👨‍👩‍👧‍👦 Family contact list[^\n]*\n(?:(?!## ).+\n)*",
        re.MULTILINE,
    )
    text = family_re.sub("", text)

    # Insert before "## 🟢 Phonebook-verified"
    new_text = text.replace(
        "## 🟢 Phonebook-verified (iPhone vCard) (53)",
        new_family_block,
        1,
    )
    # Collapse any double blank lines the regex might leave behind
    new_text = re.sub(r"\n{3,}", "\n\n", new_text)
    f.write_text(new_text)


def _update_phonebook():
    """Update phonebook.json family notes + categories."""
    f = ANALYSIS / "phonebook.json"
    if not f.exists():
        log("⚠️  phonebook.json not found")
        return
    pb = json.loads(f.read_text())
    contacts = pb.get("contacts", [])

    role_updates = {
        "Toni Weiss": {
            "category": "family",
            "tags": ["uncle", "sonias-side", "usa"],
            "notes": "Antonio López Weiss. Sonia's brother, Ivan's uncle. Lives Santa Fe USA. Was mislabeled as 'Dad' in prior corpus (corrected 2026-07-23).",
        },
        "Riet van der Pol": {
            "category": "family",
            "tags": ["grandma", "dads-side", "netherlands"],
            "notes": "John van der Pol's mother. Ivan's grandma on dad's side. Lives Netherlands. Was mislabeled as 'Mom' in prior corpus (corrected 2026-07-23).",
        },
        "Mica Weiss": {
            "category": "family",
            "tags": ["cousin", "sonias-side", "weiss-coehn"],
            "notes": "Micaela Weiss Coëhn. Ivan's cousin on Sonia's side. Same person as 'Prima Mikaela Weiss' vCard entry (the vCard has them under two different names with the same phone number — that's a vCard duplicate, not two people).",
        },
        "Prima Mikaela Weiss": {
            "category": "duplicate",
            "tags": ["duplicate-of-mica"],
            "notes": "DUPLICATE vCard entry of Mica Weiss. Same phone +595 982 850085. Ivan confirmed they are the same person. To be merged.",
        },
        "Jan van der Pol": {
            "category": "family",
            "tags": ["grandpa-deceased", "dads-side"],
            "notes": "John van der Pol's father, Riet's late husband. Deceased (a few years back, per Ivan). Was in `_dropped` chat tier; promoted to family circle 2026-07-23.",
        },
        "Luana Weiss": {
            "category": "family",
            "tags": ["sister"],
            "notes": "Ivan's full sister, age 24.",
        },
        "Ivan Weiss Usa": {
            "category": "self",
            "tags": ["own-number"],
            "notes": "Ivan's own US phone number (+1).",
        },
    }

    for c in contacts:
        n = c.get("name", "")
        if n in role_updates:
            u = role_updates[n]
            for k, v in u.items():
                c[k] = v
            log(f"phonebook: {n} → {u}")

    pb["contacts"] = contacts
    pb["family_corrections_applied"] = "2026-07-23 per Ivan's questionnaire (docs/identity-corrections/ANSWERS.md)"
    # Match master's indent style (1 space)
    f.write_text(json.dumps(pb, ensure_ascii=False, indent=1))


def _update_circles():
    """Update the family circle in CONTACT_CIRCLES.md."""
    f = ANALYSIS / "CONTACT_CIRCLES.md"
    if not f.exists():
        log("⚠️  CONTACT_CIRCLES.md not found")
        return
    text = f.read_text()

    # Add a new family section block at the top (after the header)
    family_update = """
## 👨‍👩‍👧‍👦 Family (corrected 2026-07-23)

| Role | Name | JID | Source |
|------|------|-----|--------|
| Mom | Sonia Edith Weiss López | 595982515138 | Ivan |
| Dad | John van der Pol | 595986138387 | Ivan |
| Grandma (dad's side) | Riet van der Pol | 31612495139 | Ivan |
| Grandpa (deceased) | Jan van der Pol | 595994459555 | Ivan |
| Sister | Luana Weiss | 595985725366 | vCard |
| Sister | Kyrian "Kiki" | 595985724135 | vCard |
| Uncle (Sonia's side) | Antonio "Toni" López Weiss | 15055778339 | Ivan |
| Uncle (John's side) | Gerold Manders | — | Ivan (no vCard) |
| Cousin (Sonia's side) | Micaela "Mica" Weiss Coëhn | 595982850085 | vCard |
| Cousin (Sonia's side) | Gabriel | 595985786571 | vCard |

**Identity corrections**: Toni Weiss was previously mislabeled as Dad; John van der Pol is the actual Dad. Riet van der Pol was previously mislabeled as Mom; she is Grandma (dad's side). Sonia's maiden name is Weiss López. See `docs/identity-corrections/ANSWERS.md`.

"""
    # Idempotent: skip if already inserted; otherwise insert after first header
    if "## 👨‍👩‍👧‍👦 Family (corrected 2026-07-23)" not in text:
        # Find first H1 header and insert after
        m = re.search(r"^# .+?\n\n", text, re.MULTILINE)
        if m:
            text = text[:m.end()] + family_update + text[m.end():]
    f.write_text(text)


def _rewrite_sonia_profile():
    """Update SONIA.md: dad is John, not Gerold. Sonia's full name."""
    f = PROFILES / "SONIA.md"
    if not f.exists():
        log("⚠️  SONIA.md not found")
        return
    text = f.read_text()

    # Correct the "Identity correction" header — fix Gerold → John, add full name
    text = text.replace(
        "> **Identity correction (2026-07-20):** Prior mining tagged this contact as \"Sonia, unclear role / family associate.\" Full-chat analysis unambiguously reclassifies her as **Ivan's mother** — biological or functional; the evidence is family-of-origin, not friendship. She is partnered with **Gerold** (Ivan's father), co-parents **Luana Weiss** (Ivan's sister), was present at Ivan's birth (\"hace 23 años… un sábado llegaste a mi vida\"), and Ivan addresses her as both **\"Sonia\"** and **\"mamá\"** interchangeably. She refers to him as **\"mi hijo\"** throughout. This profile therefore documents the **primary maternal dynamic** — psychologically load-bearing and referenced (without being named) in `LAURA.md` as \"the same dynamic recreated with Laura.\"",
        "> **Identity correction (2026-07-23):** Prior mining tagged this contact as \"Sonia, unclear role / family associate.\" Full-chat analysis (2026-07-20) reclassified her as **Ivan's mother**; verbal confirmation by Ivan (2026-07-23) confirms this. **Full name: Sonia Edith Weiss López.** She is partnered with **John van der Pol** (Ivan's dad, software dev for Netherlands) — NOT Gerold (who is John's adoptive brother / uncle). Co-parents **Luana Weiss** (Ivan's sister, age 24), **Saskia** (sister), and **Kyrian \"Kiki\"** (sister). Was present at Ivan's birth (\"hace 23 años… un sábado llegaste a mi vida\"), and Ivan addresses her as both **\"Sonia\"** and **\"mamá\"** interchangeably. She refers to him as **\"mi hijo\"** throughout. This profile documents the **primary maternal dynamic** — psychologically load-bearing and referenced (without being named) in `LAURA.md` as \"the same dynamic recreated with Laura.\""
    )

    # Append a footnote at end
    footer = """

---

## Family tree (per Ivan, 2026-07-23)

```
Sonia Edith Weiss López (Mom) ─── married to ─── John van der Pol (Dad)
   │                                       │
   ├── Luana Weiss (24)                    │  Jan van der Pol (Grandpa, deceased)
   ├── Saskia Weiss                        │  Riet van der Pol (Grandma, +31 NL)
   ├── Kyrian "Kiki" Weiss                 │
   │                                       ├── Rene (uncle)
   ├── Micaela "Mica" Weiss Coëhn          ├── Ester (uncle)
   ├── Gabriel (Primo)                     └── Gerold Manders (uncle, adoptive bro)
   ├── Santi (cousin)
   │
   ├── Antonio "Toni" López Weiss (uncle, Santa Fe USA)
   ├── Carlú (uncle)
   ├── Julio (uncle)
   └── Roberto (uncle)
```

**Sonia's maiden name**: Weiss López. Per Ivan, Toni Weiss (the previous "Dad" assignment) is actually her brother and Ivan's uncle.
"""
    if "## Family tree (per Ivan, 2026-07-23)" not in text:
        text = text + footer
    f.write_text(text)


def _rewrite_kiki_profile():
    """KIKI_HERMANA.md: clarify Kiki = Kyrian, not Saskia."""
    f = PROFILES / "KIKI_HERMANA.md"
    if not f.exists():
        log("⚠️  KIKI_HERMANA.md not found")
        return
    text = f.read_text()

    # Add correction note at the top
    correction_note = """
> **Correction (2026-07-23):** Per Ivan, **Kiki = Kyrian**, NOT Saskia. Saskia is a separate sister (chat not yet located in the corpus). Ivan has three sisters: Luana (24, full sister), Saskia, and Kyrian "Kiki".

"""
    if "Correction (2026-07-23)" not in text:
        text = re.sub(
            r"(# .*?KIKI.*?\n\n)",
            r"\1" + correction_note,
            text,
            count=1,
        )
    f.write_text(text)


def _update_named_pickle():
    """Persist the corrections to /tmp/psycology_named_v2.pkl so future
    scripts see the right names."""
    p = Path("/tmp/psycology_named_v2.pkl")
    if not p.exists():
        log("⚠️  pickle not found (skipping)")
        return
    import pickle
    named = pickle.load(open(p, "rb"))

    corrections = {
        # JID -> (new_name, new_conf, new_desc)
        "595982515138": ("Sonia Edith Weiss López (Mom)", "VERIFIED",
                         "Mom, married to John van der Pol. Chat was mislabeled as 'gabriel_g_curuguaty'."),
        "595986138387": ("John van der Pol (Dad)", "VERIFIED_PHONEBOOK",
                         "Dad. Software dev for Netherlands. vCard 'John' (no surname in FN — but Ivan confirms John van der Pol)."),
        "31612495139":  ("Riet van der Pol (Grandma)", "VERIFIED_PHONEBOOK",
                         "Grandma on dad's side, John's mother. Lives Netherlands. Was mislabeled as Mom."),
        "595994459555": ("Jan van der Pol (Grandpa, deceased)", "VERIFIED_PHONEBOOK",
                         "Grandpa, John's father. Deceased a few years back per Ivan."),
        "15055778339":  ("Antonio Toni López Weiss (Uncle)", "VERIFIED_PHONEBOOK",
                         "Uncle, Sonia's brother. Lives Santa Fe USA. Was mislabeled as Dad."),
        "595982850085": ("Micaela Mica Weiss Coëhn (Cousin)", "VERIFIED_PHONEBOOK",
                         "Cousin on Sonia's side. Same person as vCard 'Prima Mikaela Weiss'."),
        "595985724135": ("Kyrian Kiki Weiss (Sister)", "VERIFIED",
                         "Ivan's sister. Kiki = Kyrian, NOT Saskia (per Ivan 2026-07-23). All three sisters: Luana, Saskia, Kyrian."),
        "595985725366": ("Luana Weiss (Sister, age 24)", "VERIFIED_PHONEBOOK",
                         "Ivan's full sister."),
        "595985786571": ("Gabriel Primo (Cousin, Sonia's side)", "VERIFIED_PHONEBOOK",
                         "Cousin on Sonia's side."),
    }

    for jid, (name, conf, desc) in corrections.items():
        named[jid] = (name, conf, desc)
        log(f"named[{jid}] → {name}")

    pickle.dump(named, open(p, "wb"))
    log(f"updated {p}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()

    if not args.dry_run and not args.apply:
        args.dry_run = True

    if args.dry_run:
        dry_run()
    else:
        apply()


if __name__ == "__main__":
    main()
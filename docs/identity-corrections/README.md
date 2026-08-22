# Family Identity Corrections

This directory holds the **family-identity-correction workflow** for the psycology corpus.

## Why this exists

While building the Messaging contact circle analysis (PR #1, merged) and the vCard phonebook import (PR #1, merged), the corpus received incorrect family assignments based on:
- `SONIA.md` profile (chat-derived analysis, said Sonia's partner = "Gerold", who was Ivan's dad)
- vCard phonebook entry "Riet van der Pol" +31 — Ivan verbally confirmed this is Grandma (dad's side), not Mom
- vCard entry "Toni Weiss" +1 — Ivan confirmed this is **not** Dad (the actual Dad is "John van der Pol" +595)

The current master has all of these **incorrect** family assignments.

## Files in this directory

| File | Purpose |
|---|---|
| **QUESTIONNAIRE.md** | The questionnaire for Ivan — fill this in (5 sections, ~30 questions) |
| **audit_corpus.py** | Read-only audit script — what does the corpus currently say about family? |
| **audit_summary.json** | Output of the audit (auto-generated) |
| **migrate_family_identity.py** | The migration script — reads answers, builds a plan, applies atomically |
| **README.md** | This file |

## Workflow

```
1. Ivan reads QUESTIONNAIRE.md and answers each question inline
   (edit the file, change [ ] to [X], fill in _____ answers)

2. Run audit to verify current corpus state:
   python3 docs/identity-corrections/audit_corpus.py

3. Once Ivan commits his answers:
   python3 docs/identity-corrections/migrate_family_identity.py --dry-run
   # Inspect: renames, identity updates, profile rewrites

4. After Ivan approves the dry-run output:
   python3 docs/identity-corrections/migrate_family_identity.py --apply
   # Atomic migration on chore/apply-family-identity-corrections branch

5. Push branch + open PR
```

## Safety guarantees

- All renames are atomic (single `git mv` per file)
- Working tree rolls back if any step fails
- Dry-run output is reviewable BEFORE apply
- Profile rewrites happen on a separate branch, never on master
- One round-trip: only one migration commit per questionnaire submission

## Status

- ✅ Branch `chore/family-identity-correction-questionnaire` opened
- ✅ Questionnaire written + auto-populated with corpus facts
- ⏸️ Awaiting Ivan's answers
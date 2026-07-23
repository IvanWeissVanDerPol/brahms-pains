# Family Identity Corrections — Questionnaire for Ivan

> **Status:** Awaiting answers from Ivan.
> **Last updated:** 2026-07-23
> **Purpose:** Replace 7+ wrong family assignments in `SOURCE_OF_TRUTH/wa_messages/` and `RELATIONSHIPS/dynamics/`
> **Scope:** 25 chats to rename, 4+ vCard corrections, family profile rewrites, contact circle restructuring.
> **Safe to answer out of order.** Skip any question you don't know.

---

## Why this questionnaire exists

The current corpus (in master) has **multiple conflicting family assignments** because the vCard phonebook, the WhatsApp-based `SONIA.md` profile, and your verbal corrections don't agree. To prevent destructive renames, we need you to formally authoritatively settle every family relationship.

This is destructive work. The plan is:

1. **You answer** the questions below (inline by editing this file, or in chat)
2. **I run a single migration commit** that applies your corrections atomically:
   - Renames all `*Toni*`/`*Riet*`/`*Mica*`/`*Jan*`/`*Gerold*` chat directories
   - Updates `SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/CONTACTS_NAMED.md` family section
   - Updates `SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/CONTACT_CIRCLES.md` family circle
   - Updates `SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/phonebook.json` family notes + categories
   - Updates `RELATIONSHIPS/dynamics/SONIA.md`, `KIKI_HERMANA.md`, `LUANA.md`, `MASTER_PROFILE.md` (any file that references Toni/Riet as parent)
   - Adds/changes identity metadata in each chat's `messages.json`
3. **I run Track A + Track C verification** — regenerate the verify markdown, the viewer, and the naming confidence report

If anything's wrong post-migration, I revert with `git revert` (one shot, atomic).

---

## Section A — Direct family (the 5 most important)

For each person, fill in:
- **Relationship to Ivan** (your role label, e.g. "Mom", "Dad", "Grandma", "Uncle Sonia's side")
- **Married / partnered to** (which other family member, or "no")
- **Where they live** (city, country)
- **Phonebook name** (the literal vCard `FN:` field — already known to me, listed below)

### A1. Sonia Weiss

- **vCard name:** ❌ (Sonia is NOT in the vCard)
- **Phone number:** ❓ I don't have it yet
- **WhatsApp JID:** ❓ I need to find the Sonia chat JID — likely the largest tier1 chat

You said: **"sonia is sonia weiss is mama"**

I need to confirm:

| # | Question | Answer |
|---|----------|--------|
| A1.1 | **Confirm: Sonia Weiss = your Mom** | [ ] Yes  [ ] No  [ ] She's a different role: _____ |
| A1.2 | **Sonia is married to: John van der Pol (your dad)** | [ ] Yes  [ ] No — she married _____ |
| A1.3 | **Sonia's maiden name** | [ ] Weiss  [ ] Other: _____ |
| A1.4 | **Sonia's date of birth / age** | _____ |
| A1.5 | **Where does Sonia live** | _____ |
| A1.6 | **Sonia's occupation** | _____ |
| A1.7 | **Sonia's siblings** (names, including Gerold) | _____ |
| A1.8 | **WhatsApp chat for Sonia** | I think it's a 11,305-msg tier1 chat. **Is the existing profile file `RELATIONSHIPS/dynamics/SONIA.md` referring to her?** [ ] Yes  [ ] No |
| A1.9 | **Anything to ADD to the existing SONIA.md profile** (your mom is a psychological corner of the corpus, this file is rich) | _____ |

### A2. John van der Pol (your Dad)

- **vCard name:** "John" (just "John" — no surname)
- **vCard phone:** +595 986 138387 (Paraguay)
- **WhatsApp chat dir:** `tier2_core/32__john___wa_chat_595986138387_1265` (1,864 msgs, 2021-10 → 2026)

| # | Question | Answer |
|---|----------|--------|
| A2.1 | **Confirm: John = your Dad** | [ ] Yes  [ ] No — he's _____ |
| A2.2 | **Full surname** | van der Pol |
| A2.3 | **Date of birth / age** | _____ |
| A2.4 | **Where does John live** | _____ |
| A2.5 | **Occupation** | _____ |
| A2.6 | **John's relationship to Riet van der Pol** (the +31 Netherlands number) | [ ] Mother  [ ] Father  [ ] Other: _____ |
| A2.7 | **John's siblings** (including Ony, etc.) | _____ |
| A2.8 | **Does John have WhatsApp?** Is the 595986138387 chat with him, or with someone else named John? | [ ] Yes, that chat IS John  [ ] No — that chat is with someone else, and John's chat is JID: _____ |
| A2.9 | **The Jan van der Pol vCard entry (+595) is also a relative?** | [ ] Yes — Jan is: _____  [ ] No — Jan is unrelated |
| A2.10 | **Anything special to flag about your dad** (psychologically, work, anything) | _____ |

### A3. Riet van der Pol (Grandma, dad's side)

- **vCard name:** "Riet van der Pol"
- **vCard phone:** +31 (Netherlands)
- **Currently mislabeled in corpus as Mom**

| # | Question | Answer |
|---|----------|--------|
| A3.1 | **Confirm: Riet = your Grandma (dad's side)** | [ ] Yes  [ ] No — she's: _____ |
| A3.2 | **Riet is John's mother?** | [ ] Yes  [ ] No — she's: _____ |
| A3.3 | **Where does Riet live** | _____ |
| A3.4 | **What language does Riet speak** (helps transcribe voice notes later) | _____ |
| A3.5 | **Does Riet have WhatsApp?** | [ ] Yes — chat JID: _____  [ ] No  [ ] Don't know |

### A4. Gerold (Uncle)

- **vCard name:** ❌ (Gerold is NOT in the vCard)
- **Mentioned 19× in jonathan_verdun chat, 15× in gabriel_g_curuguaty**

| # | Question | Answer |
|---|----------|--------|
| A4.1 | **Confirm: Gerold = Uncle** | [ ] Yes — Sonia's brother  [ ] Yes — John's brother  [ ] Other: _____ |
| A4.2 | **Gerold's full name** | _____ |
| A4.3 | **Where does Gerold live** | _____ |
| A4.4 | **Phone / WhatsApp** | _____ |
| A4.5 | **Role** (what kind of uncle, anything distinctive) | _____ |

### A5. Ony (Uncle — which side?)

- **vCard name:** ❌ (Ony is NOT in the vCard; also spelled "Ony" not "Johnny")

| # | Question | Answer |
|---|----------|--------|
| A5.1 | **Confirm: Ony = Uncle** | [ ] Yes  [ ] No — he's: _____ |
| A5.2 | **Ony is Sonia's brother or John's brother?** | [ ] Sonia's  [ ] John's  [ ] Other: _____ |
| A5.3 | **Ony's full name** | _____ |
| A5.4 | **Where does Ony live** | _____ |
| A5.5 | **Phone / WhatsApp** | _____ |
| A5.6 | **Is Ony the same as Gerold?** (i.e. Gerold's nickname is Ony?) | [ ] Yes  [ ] No — they're different  [ ] Not sure |

---

## Section B — Siblings + cousins

### B1. Kiki (Saskia Weiss — already named)

- **vCard name:** Kiki's entry was NOT in the vCard dump we have
- **WhatsApp JID:** `595985724135` (already VERIFIED)

| # | Question | Answer |
|---|----------|--------|
| B1.1 | **Confirm: Kiki = Saskia Weiss** | [ ] Yes  [ ] No |
| B1.2 | **Kiki's relationship to Mica (cousin)** | [ ] Mica is Kiki's: _____ |
| B1.3 | **Anything new about Kiki** | _____ |

### B2. Luana Weiss (already named)

- **vCard name:** Luana Weiss
- **WhatsApp JID:** `595985725366` (already VERIFIED_PHONEBOOK)

| # | Question | Answer |
|---|----------|--------|
| B2.1 | **Confirm: Luana is your sister** | [ ] Yes — full sister  [ ] Half-sister (different parent: _____)  [ ] Other: _____ |
| B2.2 | **Luana's age / DOB** | _____ |
| B2.3 | **Is Luana = "Saskia" or "Kyrian" mentioned in old corpus docs?** | [ ] Luana is Saskia  [ ] Luana is Kyrian  [ ] Neither — she's Luana only |

### B3. Mica Weiss (cousin)

- **vCard name:** "Mica Weiss"
- **vCard phone:** +595
- **WhatsApp JID:** `595982850085`

| # | Question | Answer |
|---|----------|--------|
| B3.1 | **Confirm: Mica is your cousin** | [ ] Yes — through Sonia  [ ] Yes — through John  [ ] Other: _____ |
| B3.2 | **Mica's full name** | _____ |
| B3.3 | **Mica's relation to Prima Mikaela** (next entry) | [ ] Same person  [ ] Mikaela is Mica's: _____ |

### B4. Prima Mikaela Weiss

- **vCard name:** "Prima Mikaela Weiss" (literally "cousin Mikaela Weiss")
- **WhatsApp JID:** ❓ (not yet located)

| # | Question | Answer |
|---|----------|--------|
| B4.1 | **Confirm: Prima Mikaela is your cousin** | [ ] Yes  [ ] No |
| B4.2 | **Mikaela's relationship to Mica** | [ ] Same person  [ ] Sister  [ ] Other: _____ |
| B4.3 | **Mikaela's chat JID** (if you know it) | _____ |

### B5. Primo Gabriel

- **vCard name:** "Primo Gabriel"
- **WhatsApp JID:** `595985786571`

| # | Question | Answer |
|---|----------|--------|
| B5.1 | **Confirm: Primo Gabriel is your cousin** | [ ] Yes  [ ] No |
| B5.2 | **Which side** | [ ] Sonia's family  [ ] John's family |
| B5.3 | **Full name** | _____ |

---

## Section C — Toni Weiss (currently labeled Dad, but you said it's wrong)

| # | Question | Answer |
|---|----------|--------|
| C.1 | **Who is Toni Weiss?** (You said John van der Pol is Dad, not Toni) | [ ] Uncle  [ ] Cousin  [ ] Grandpa  [ ] Other: _____ |
| C.2 | **Toni's relationship to you** | _____ |
| C.3 | **Phone / WhatsApp** | +1 (USA), `Paragweiss@yahoo.com` (already known) |
| C.4 | **Is Toni the same person as the current "tier2_core/Toni Weiss" chat (JID 15055778339)?** | [ ] Yes  [ ] No — that chat is someone else |

---

## Section D — Ivan Weiss Usa (vCard entry)

- **vCard name:** "Ivan Weiss Usa"
- **vCard phone:** +1
- This appears to be Ivan's own US contact card

| # | Question | Answer |
|---|----------|--------|
| D.1 | **This is your own number / your US phone** | [ ] Yes  [ ] No — it's: _____ |

---

## Section E — Family contact graph

```
Current corpus (WRONG):
    Mom = Riet van der Pol  (+31)
    Dad = Toni Weiss         (+1)
    Uncle = Gerold           (in SONIA.md profile as Dad!)
    Cousin = Mica, Mikaela

Target:
    Mom   = Sonia Weiss       (Sonia is married to John)
    Dad   = John van der Pol  (+595)
    Grandma (dad's side) = Riet van der Pol
    Uncle(s) = Gerold + Ony  (which side?)
    Siblings = Kiki, Luana
    Cousin(s) = Mica, Mikaela, Gabriel
    Other relative = Toni Weiss (role to confirm)
```

### Are there any family members you listed but I missed?

| Name | Relationship | Phone / WhatsApp |
|---|---|---|
| _____ | _____ | _____ |
| _____ | _____ | _____ |

---

## Section F — Operational preferences

| # | Question | Answer |
|---|----------|--------|
| F.1 | **Rename chat directories immediately after this questionnaire, or wait until you can review?** | [ ] Apply immediately  [ ] Wait for explicit "go" |
| F.2 | **How to handle "Toni Weiss" chat?** | [ ] Rename it (specify new name)  [ ] Leave alone for now  [ ] Mark as "needs disambiguation" |
| F.3 | **How to handle "Riet van der Pol" chat (31612495139)?** | [ ] Rename to "Grandma Riet"  [ ] Rename to "Riet van der Pol (grandma)"  [ ] Leave alone |
| F.4 | **Do you want to keep family member voice notes high-priority in Whisper queue?** | [ ] Yes — transcript family first  [ ] No — same priority as everyone |
| F.5 | **Anything else you want me to know before I commit the migration?** | _____ |

---

## How to submit your answers

**Option 1** — Edit this file directly:
```bash
# In the branch I created:
cd /root/psycology
nano docs/identity-corrections/QUESTIONNAIRE.md
# Answer each [ ] checkbox or _____ blank
git add docs/identity-corrections/QUESTIONNAIRE.md
git commit -m "answers: family identity corrections"
git push -u origin chore/family-identity-correction-questionnaire
```

**Option 2** — Answer in chat (paste back here), and I'll write your answers into the file.

**Option 3** — Open it on GitHub:
- The branch `chore/family-identity-correction-questionnaire` has this file
- Click "Edit" → answer → "Commit changes" → I'll pick it up

---

## What I'll do after I receive answers

1. Read all your answers
2. Build a single migration script that:
   - Computes the chat-dir renames (atomic, with rollback)
   - Updates vCard phonebook notes + categories
   - Updates `SONIA.md` / `KIKI_HERMANA.md` / `LUANA.md` / `MASTER_PROFILE.md` profiles
   - Updates the `family_weiss` + `family_van_der_pol` circle definitions
3. Run **dry-run** first (no commit, just `git diff --stat` showing what would change)
4. You approve or modify
5. Single atomic commit on a new branch `chore/apply-family-identity-corrections`
6. Push + open PR

**Estimated work**: 30 minutes to code, 5 minutes for you to review diff, 1 minute to merge.

---

## Cross-references (for context, not for you to fill out)

- `RELATIONSHIPS/dynamics/SONIA.md` — current mom profile (says partner = Gerold, you said partner = John)
- `RELATIONSHIPS/dynamics/KIKI_HERMANA.md` — Kiki profile
- `SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/CONTACTS_NAMED.md` — full contact list
- `SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/CONTACT_CIRCLES.md` — circle assignments
- `SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/phonebook.json` — phonebook data
- `SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/REPOSITORY_INCONSISTENCY_REPORT.md` — has some family refs
- `MASTER_PROFILE.md` — top-level profile

---

**Waiting for your answers.** 🙏
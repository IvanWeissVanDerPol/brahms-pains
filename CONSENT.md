# CONSENT — Third-Party Data Practices (TEMPLATE — added 2026-09-01 by Hermes)

> **# TODO: ivan-review** (added 2026-09-01 by Hermes): This is a **template** for documenting third-party consent for publication. It's here because the repo was made private→public→renamed during the 2026-08-28 → 2026-09-01 working session, and the question of third-party consent for public publication is unresolved.
>
> **When/if you go public with the repo, you need to either:**
> 1. Document verbal consent (per your claim: "i told them many times i do this and i have everything in my repo and store all my life data etc there") in this file, OR
> 2. Run a redaction pass that replaces all third-party names with stable pseudonyms before public publication, OR
> 3. Get explicit written consent from each named contact (slow, but legally safest).
>
> **Until this document is filled in, the repo's third-party data practices are undocumented.** This template exists so the work is not lost if you decide to address it later.

---

## 1. Scope

This document records the data practices that apply to **third-party named individuals** in this repository. "Third-party" means anyone who is NOT the repository owner (Iván Weiss Van Der Pol).

This includes but is not limited to:
- Family members (kiki/kyrian, sonia, grandpa jan van der pol, others)
- Romantic partners and ex-partners (gaby, belén, nate, both luas, nico, mike, dayah, others)
- Friends (cookie/kuki, ale, lurdes, dan, sarah, magali, laura, jonatan, jonathan verdun, dad, others)
- Professional contacts (former clients, employers, colleagues)
- Medical professionals (the actual psychologist, dentist, doctor, MRI/endoscopy providers)

## 2. Data classification

| Data type | Location | Severity |
|---|---|---|
| Full names (first + last) of ~216 named contacts | `SOURCE_OF_TRUTH/wa_messages/tier*/`, `RELATIONSHIPS/dynamics/*.md` | 🔴 PII |
| Phone numbers (paraguayan + international) | chat directory names | 🔴 PII |
| Voice note transcripts | `SOURCE_OF_TRUTH/voice_note_transcripts/` | 🟠 Personal |
| Bulk voice notes (.opus files) | `media/audio/` | 🟠 Personal |
| Family relationships | `CORE_PSYCHOLOGY/PSY_FAMILY_ORIGINS.md`, various | 🟠 Personal |
| Medical details (MRI, endoscopy, autism dx, kidney) | `MEDICAL/`, `SESSION_2026-08-27_GABY_PROCESS.md`, RECAP | 🔴 PHI |
| Sexual content involving third parties | `KINK_AND_INTIMACY/`, RECAP §D, SESSION_2026-08-27 | 🔴 Sensitive |
| Mental health details about third parties | GABY_PROCESS.md, COOKIE_KUKI_NARRATIVE.md | 🟠 Sensitive |
| TLP/BPD-pattern attributions (informal, observational) | RECAP, BELEN_PROCESS, COOKIE_KUKI_NARRATIVE | 🟠 Sensitive |

## 3. Consent status

> **# TODO: ivan-review** (added 2026-09-01 by Hermes): Per Iván's verbal claim, third-party consent was given verbally to contacts "many times" prior to the 08-27 rupture. The verbal consent was general ("i store my data, i have a repo") rather than specific to public publication. Below is a placeholder for the consent documentation.

### 3.1 Documented verbal consent

| Date | Contact | Mode | Scope of consent | Notes |
|---|---|---|---|---|
| _(to fill in)_ | _(name)_ | _(in person / chat / group)_ | _(general / specific to public)_ | _(what was said exactly)_ |

### 3.2 Contacts who declined consent (if any)

| Date | Contact | Mode | Scope of decline | Action taken |
|---|---|---|---|---|
| _(to fill in)_ | _(name)_ | _(in person / chat)_ | _(what they declined)_ | _(data removed / pseudonymized / etc.)_ |

### 3.3 Contacts who have not been asked (if any)

| Contact | Reason not asked | Risk level |
|---|---|---|
| _(to fill in)_ | _(e.g., lost contact, deceased, etc.)_ | _(low / medium / high)_ |

## 4. Repository state

- **Current visibility:** private
- **Renamed from:** `IvanWeissVanDerPol/psycology`
- **Renamed to:** `IvanWeissVanDerPol/brahms-pains`
- **Old URL behavior:** 301 redirect to new (github default; cannot be made to return 404)
- **Collaborators:** 1 (Ivan Weiss Van Der Pol — admin)

## 5. Third-party data exposure events

> **# TODO: ivan-review** (added 2026-09-01 by Hermes): Per the SECURITY.md hardening checklist, the following are still OPEN as of 2026-09-01:
> - [ ] GitHub PAT rotation (per security-flip trigger; the original PAT was leaked in a terminal session on 2026-09-01 and needs to be replaced)
> - [ ] Deploy keys rotated
> - [ ] GitHub Apps with access reviewed
>
> **Also**: the rename 2026-09-01 may have triggered search-engine re-indexing of the new URL. If the repo has ever been public (even briefly), old cached versions may exist. Force-push or git-filter-repo operations may be needed to scrub.

## 6. Right to be forgotten

> **# TODO: ivan-review** (added 2026-09-01 by Hermes): If a named contact requests removal of their data, the workflow should be:
> 1. Identify all files mentioning the contact (`grep -r "<name>" .`)
> 2. Replace with stable pseudonym (e.g., `Contact_A`, `Contact_B`)
> 3. Update internal cross-references
> 4. If the repo has been public, run `git-filter-repo` to scrub from history
> 5. Force-push the rewritten history
>
> This is a significant amount of work per contact. Consider whether a simpler model (e.g., always pseudonymizing third parties from the start) is preferable.

## 7. References

- AIW BWS credential handling: `/opt/data/profiles/ivan/skills/software-development/aiw-bws-credential-quirks/SKILL.md`
- Original SECURITY.md: `SECURITY.md` at repo root

---

*Document template created 2026-09-01 by Hermes Agent.*
*Owner: Iván Weiss Van Der Pol.*
*Status: Template, awaiting population. Do not publish this document with placeholder values.*

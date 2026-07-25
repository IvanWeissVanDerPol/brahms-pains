# Cross-Doc Consistency Audit

> **Date:** 2026-07-25
> **Auditor:** Erebus
> **Scope:** PSYCHOLOGICAL_ANALYSIS_20HATS.md (now 32 hats, 627 lines) ↔ CORE_PSYCHOLOGY/*.md ↔ TREATMENT/*.md ↔ KINK_AND_INTIMACY/*.md

---

## Executive Summary

| Severity | Count | Action |
|----------|-------|--------|
| 🔴 Critical contradiction | 1 | Resolve before any clinical use |
| 🟠 Important inconsistency | 6 | Reconcile in next pass |
| 🟡 Soft drift / terminology | 8 | Document and align |
| 🟢 Working as intended | 5 | No action |

**Top priority**: The Magali-vs-MAIN-7 contradiction (`PSYCHOLOGICAL_ANALYSIS_20HATS.md` Hat 1, line 26 still describes Magali as "#3 strongest contact" though the user clarified she is NOT a current main friend). This is acknowledged in Hat 26 line 482 ("the user clarified she was not a current main friend") but **Hat 1 was never updated** to reflect this.

---

## 🔴 Critical Contradictions

### C1. Magali's status — Hat 1 vs Hat 26 contradiction

**Location**: `PSYCHOLOGICAL_ANALYSIS_20HATS.md`
- **Hat 1, line 26**: "The 81% engagement drop with **Magali** (his #3 strongest contact, 76.6 score) is the most clinically significant signal in the data."
- **Hat 26, line 482**: "The earlier analysis over-weighted Magali because a score and trend looked dramatic, then the user clarified she was not a current main friend."

**Problem**: Hat 1 still calls Magali "#3 strongest contact" — this was true at the time of writing but the user has since clarified she's a university friend from the past, not a current main friend. The Hat 26 self-correction exists but Hat 1 was never updated.

**Fix**: In Hat 1 line 26, replace "his #3 strongest contact" with "a historical university friend whose engagement has dropped 81% (not a current main friend, per user clarification)".

**Severity**: 🔴 — clinical framing matters. A reader scanning Hat 1 will treat Magali as a top-priority active relationship, which is now wrong.

---

## 🟠 Important Inconsistencies

### I1. Attachment style language — "anxious-preoccupied" vs "contextual strategy"

- **Hat 1, line 19**: "Likely **anxious-preoccupied with secure features**."
- **CORE_PSYCHOLOGY/attachment_patterns/EVIDENCE_LEDGER.md, Pattern 1**: "This is better described as a contextual strategy than a global attachment label."
- **TREATMENT/CLINICAL_SUMMARY.md, line 27**: "Attachment Disturbance — Anxious-avoidant hybrid; craves closeness but fears burden."

**Three different formulations of the same construct**: (1) "anxious-preoccupied with secure features" (Hat 1), (2) "dismissive-avoidant / Firewall" (CORE ledger, describing family specifically), (3) "anxious-avoidant hybrid" (TREATMENT).

**Fix**: Add a synthesis note at the top of `ATTACHMENT_OVERVIEW.md` reconciling these three. The CORE ledger's framing (contextual, not global) is the most defensible. Hat 1 should be revised to read "contextual attachment strategy with anxious-preoccupied features in non-kink contexts and secure features in permission-structured contexts."

### I2. Family attachment label drift

- **Hat 4 (Family Therapist)**: "Family emotional system" section names Mom Sonia as "central pivot" but doesn't explicitly name the attachment style.
- **CORE_PSYCHOLOGY/attachment_patterns/ATTACHMENT_OVERVIEW.md**: "Family attachment is **dismissive-avoidant / Firewall**: logistics and competence are shareable, vulnerable affect is filtered."
- **Hat 1 line 21**: Lists 5 family in 9-person close circle as evidence of "active maintenance of primary attachment" — implies SECURE attachment to family, which contradicts CORE's dismissive-avoidant framing.

**Problem**: Hat 1 frames family closeness as evidence of *secure* attachment. CORE ledger frames it as *dismissive-avoidant* attachment (close but emotionally filtered). These are different clinical claims.

**Fix**: Hat 1 should distinguish "structural family proximity" (true — high contact) from "emotional family attachment quality" (per CORE: filtered/dismissive-avoidant). Currently conflates them.

### I3. Voice-note practice framing — "rumination regulation" vs "executive-function accommodation"

- **Hat 1, line 23**: "**Late-night peak (23:00-02:00)** suggests these serve as rumination regulation."
- **Hat 27 (Neurodivergence Clinician, NEW)**: "Voice-note practice as executive-function accommodation" — frames it as **adaptive cognitive offloading**, not rumination.

**Problem**: Two different psychological frames for the same observable behavior. Hat 1's "rumination regulation" implies voice notes are *managing something pathological*; Hat 27's framing implies they're *supporting a different cognitive style*. Both can be true, but the file reads as if they're competing interpretations rather than complementary.

**Fix**: In Hat 27 (now added), add a cross-reference noting the Hat 1 rumination framing and clarifying that both can coexist (executive-function offloading AND rumination regulation depending on content).

### I4. Kink persona count — Ivan/Brahm/Nyx/Neko vs simplified "sub persona"

- **KINK_AND_INTIMACY/permission_structures/HOW_KINK_FUNCTIONS.md, line 4**: "The only sanctioned context where Brahm can emerge without shame"
- **CASE_NICO_NYX_DOM_RIGGER.md** (new): "Two sub-personas activated in this dynamic: Neko, Nyx"
- **HOW_KINK_FUNCTIONS.md, line 51**: References "Nyx" alongside "Brahm"

**Inconsistency**: The new case files document **four** sub-personas (Ivan = operator, Brahm = sub-inner-child, Nyx = kink persona, Neko = community pet name), but `COMPLETE_PREFERENCES.md` doesn't mention this taxonomy at all, and the README structure diagram doesn't surface it.

**Fix**: Add a `SUBPERSONAS.md` map in `KINK_AND_INTIMACY/` documenting: name → function → context of activation → evidence file.

### I5. Fixer pattern — pathology framing vs healthy reciprocity framing

- **CORE_PSYCHOLOGY/defense_mechanisms/EVIDENCE_LEDGER.md, "Updated formulation"**: "The Fixer is contextual and can be either adaptive service or defensive over-functioning."
- **TREATMENT/CLINICAL_SUMMARY.md, line 19**: Lists "compulsive service-giving ('The Fixer')" as a chronic presenting pattern.

**Problem**: CORE ledger's updated formulation says Fixer can be adaptive. TREATMENT file still frames it as pathological ("compulsive"). This is a meaningful clinical drift.

**Fix**: TREATMENT should reference CORE's updated formulation. The Mike profile (`MIKE_NYX.md` line 296-300) provides evidence for the "Fixer can be healthy" framing — TREATMENT should incorporate.

### I6. Touch starvation — wound severity not reflected in treatment intensity

- **CORE_PSYCHOLOGY/wounds/04_TOUCH_STARVATION.md** (219 lines, dedicated file): documents this as a core wound.
- **TREATMENT/TREATMENT_ROADMAP.md**: spot-check shows extensive family/attachment work; touch-related goals are not prominent.

**Fix**: Verify `TREATMENT/goals/TREATMENT_GOALS.md` includes explicit touch-starvation treatment goals. If not, add.

---

## 🟡 Soft Drift / Terminology

### S1. "Self-differentiation level: Moderate" (Hat 4) vs different scores elsewhere

Hat 4 says "Moderate-low." Hat 1 says "Moderate." No clear scoring methodology.

### S2. "Isolation markers" (Executive Summary, line 11) lacks citation

The exec summary mentions "isolation markers (rising reliance on AI for planning conversations)" but the supporting evidence is scattered across Hats 11, 25, 28. Should consolidate.

### S3. Date inconsistency in 20HATS

Line 4 says "Date: July 23, 2026" but the file is being actively updated through July 25. Last-modified date should be added.

### S4. "149 dormant contacts" — referenced but no source ledger

Referenced in Hat 1, Hat 29, Hat 31 — but no `DORMANT_CONTACTS_LEDGER.md` exists. Pattern claims without primary-source backing.

### S5. "Weiss Van der Pol" vs "Weiss-Van der Pol" vs "WeissVanDerPol"

Mixed usage across files. Pick one canonical form (legal name format) and document in `RELATIONSHIPS/history/RELATIONSHIP_TIMELINE.md`.

### S6. "Ale" vs "Alejandro" vs "Alejandro Cabral Poli" vs "Alex"

Multiple nicknames used inconsistently. The `ALEXANDER_CANETE.md` and `ALEX.md` profiles may be different people; check for collisions.

### S7. "Kiki" vs "Kyrian" vs "Kiki Weiss"

`ANSWERS.md` confirms these are the same person, but the file names use "KIKI_WEISS_HERMANA" — should standardize.

### S8. "Laura" vs "Lau"

Same person, two names. Document canonical name.

---

## 🟢 Working As Intended

- **20HATS hats 1-32 are internally consistent in scope** (each covers one professional lens, none duplicates another)
- **CORE_PSYCHOLOGY/wounds/** are well-evidenced and properly scoped
- **CORE_PSYCHOLOGY/defense_mechanisms/** updated formulations are current and defensible
- **TREATMENT/goals/TREATMENT_GOALS.md** (290 lines) is grounded, not generic
- **KINK_AND_INTIMACY/permission_structures/HOW_KINK_FUNCTIONS.md** is theoretically robust

---

## Top 10 Priority Fixes

| # | Fix | Severity | Effort |
|---|-----|----------|--------|
| 1 | **C1**: Update Hat 1 line 26 to reflect Magali is NOT a current main friend | 🔴 | Low (one line) |
| 2 | **I1**: Reconcile three attachment-style formulations into single canonical framing | 🟠 | Medium (3-file edit) |
| 3 | **I2**: Distinguish family structural proximity from emotional attachment quality in Hat 1 | 🟠 | Low (one bullet edit) |
| 4 | **I4**: Add `KINK_AND_INTIMACY/SUBPERSONAS.md` mapping Ivan/Brahm/Nyx/Neko | 🟠 | Medium (new file) |
| 5 | **I5**: Update `TREATMENT/CLINICAL_SUMMARY.md` to acknowledge Fixer can be adaptive | 🟠 | Medium |
| 6 | **I6**: Verify `TREATMENT/goals/TREATMENT_GOALS.md` has touch-starvation goals; add if missing | 🟠 | Low |
| 7 | **I3**: Add cross-reference between Hat 1 rumination framing and Hat 27 executive-function framing | 🟡 | Low |
| 8 | **S4**: Create `SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/DORMANT_CONTACTS_LEDGER.md` | 🟡 | Medium |
| 9 | **S5**: Pick canonical name form for "Weiss Van der Pol" and document | 🟡 | Low |
| 10 | **S1**: Add methodology note explaining how "Moderate" / "Moderate-low" differentiation scores are assigned | 🟡 | Medium |

---

## Methodology

This audit was conducted via:
- Direct reads of `PSYCHOLOGICAL_ANALYSIS_20HATS.md` (627 lines), 3 CORE_PSYCHOLOGY evidence ledgers, 2 TREATMENT files, 2 KINK files
- Spot-checks of related profile files
- Pattern-match against user-correction history (Magali clarification noted in Hat 26)

**Limitations**:
- 100+ `RELATIONSHIPS/dynamics/*.md` profiles not individually audited
- Voice-note transcript consistency not verified at the file level
- TREATMENT files deeper than first-50-lines not all read

**Recommended follow-up**:
- Spot-check 10 random profiles from `RELATIONSHIPS/dynamics/` for wound/defense label consistency
- Verify TREATMENT roadmap has a section per CORE_PSYCHOLOGY wound
- Build automated consistency checker (`scripts/consistency_check.py`)

---

## Related Documents

- `docs/identity-corrections/AUDIT_2026_07_25.md` — family identity audit, flagged ANN_KINK ↔ lucia_diaz collision
- `KINK_AND_INTIMACY/cases/` — 3 new case files (Nico, Sarah, Group)
- `RELATIONSHIPS/dynamics/ANN_KINK_OPEN_QUESTION.md` — unresolved identity drift

---

*Auditor: Erebus · Date: 2026-07-25*

# OPEN QUESTION — Ann_KINK vs Lucía Díaz (JID 595991549029)

> **Status:** UNRESOLVED — awaiting Ivan's input
> **Date raised:** 2026-07-25 by Erebus
> **Raised in:** `docs/identity-corrections/AUDIT_2026_07_25.md` (item 2)

---

## The contradiction

A single WhatsApp JID (`595991549029`) is referenced under TWO identities in the repo:

### Identity A: "Ann" (kink community contact)
- **Profile file**: `RELATIONSHIPS/dynamics/ANN_KINK.md` (47 lines, stub)
- **Profile path claim**: `SOURCE_OF_TRUTH/wa_messages/tier2_core/ann_kink___wa_chat_595991549029_1956/`
- **Profile description**: tier2_core, 5,155 msgs, audio=240, img=313, first msg 2023-01-21
- **Profile content**: First msg "Este frupo es con ann", casual uwu/voseo tone

### Identity B: "Lucía Díaz" (architect collaborator)
- **Directory on disk**: `SOURCE_OF_TRUTH/wa_messages/tier2_core/lucia_diaz____wa_chat_595991549029_1956/`
- **Directory verified**: same JID, 5,155 msgs, audio=240, img=313, span 2023-2026
- **First message content (verified)**: "Este frupo es con ann" — matches profile but directory says Lucía

---

## Hypotheses (pick one or specify other)

### Hypothesis 1: Directory was renamed; person is Ann
- The original chat directory was `ann_kink___wa_chat_595991549029_1956` (matching profile).
- During a cleanup pass, the directory was renamed to `lucia_diaz____...` but the JID was not changed.
- **Profile is correct. Directory rename was wrong.**
- **Implication**: We need to rename the directory back to `ann_kink___...` (or new canonical name), audit any references to "Lucía" in the codebase that point here, and check if there's a different chat for the real Lucía Díaz.

### Hypothesis 2: Profile is wrong; person is Lucía Díaz
- The directory `lucia_diaz____...` is the canonical, correct name.
- The `ANN_KINK.md` profile is mislabeled (maybe from a stub-generation script bug at `scripts/generate_profile_stubs.py`).
- Lucía uses casual uwu/voseo with Ivan, hence the kink-coded first messages.
- **Profile is wrong. Directory is correct.**
- **Implication**: Delete `ANN_KINK.md`, create `LUCIA_DIAZ.md`, audit all references to "Ann_Kink" in case files (especially `KINK_AND_INTIMACY/cases/`).

### Hypothesis 3: There are two contacts — but only one JID
- Both "Ann" and "Lucía" refer to the same JID (which can happen if someone changed their display name and the directory rename followed).
- "Este frupo es con ann" from 2023 was the original contact name; later the directory was renamed when the contact became known as Lucía (e.g., post-marriage).
- **Same person, name change. Both labels partially correct.**
- **Implication**: Merge the two profiles, choose canonical name (Ivan decides), document the change.

---

## Why this matters

- **Identity-correction SOP** says: write `<NAME>_OPEN_QUESTION.md` and STOP — don't auto-resolve when content contradicts context.
- This is exactly that case.
- All `KINK_AND_INTIMACY/cases/` cross-references assume the JID belongs to "Ann" (kink community). If it's actually Lucía (architect), the case-file cross-references are wrong.
- The 5,155-message corpus may be **mislabeled**: 240 audio + 313 images need to be re-interpreted through the correct person's lens.

---

## Evidence the auditor found

| Source | Says | Notes |
|--------|------|-------|
| First message text | "Este frupo es con ann" | Literal self-identification as "ann" |
| Profile `ANN_KINK.md` | tier2_core, 5,155 msgs | Stub generated 2026-07-23 |
| Directory on disk | `lucia_diaz____...` | Mismatch |
| User profile in MEMORY | "Lucía Díaz (architect/terrain analyst, supplies CSV/GeoJSON for paraguay-geodata.com)" | Suggests Lucía is a professional contact |
| Chat content tone | casual uwu, voseo | Matches "kink friend" or "casual friend" |
| Audio count (240) | high for either relationship | Doesn't disambiguate |
| 3.5-year span (2023-2026) | sustained | Possible for either, but longer than typical for pure "kink friend" |

---

## Action required from Ivan

Please answer ONE of:
- **A.** "Yes, Ann is the contact. Rename directory back. Audit any 'Lucía' references in the codebase that point here." → Hypothesis 1
- **B.** "No, it's Lucía. Delete the Ann profile. This directory was always Lucía." → Hypothesis 2
- **C.** "It's the same person — Ann became Lucía. Merge the profiles, name it Lucía (or Ann, you choose)." → Hypothesis 3
- **D.** Specify your own resolution.

Once you answer, the correction can be applied atomically via a `chore/resolve-ann-kink-vs-lucia-diaz` branch.

---

## Cross-references that may need updating (pending resolution)

- `RELATIONSHIPS/dynamics/ANN_KINK.md` (profile itself)
- `KINK_AND_INTIMACY/cases/` (cross-references — see especially the "Ann" mention in `CASE_GROUP_FUNHOUSE_LAS_LOCURAS.md` section 6)
- Any `scripts/` files that hardcode the JID `595991549029`
- `MASTER_PROFILE.md` if it mentions Ann

---

## Auditor: Erebus
**Audit date:** 2026-07-25
**Audit source:** `docs/identity-corrections/AUDIT_2026_07_25.md`


---

## 📊 NEW (2026-07-27): Empirical Profile Data

**Total messages**: 2,328
**Chats analyzed**: 5
**Tier(s)**: other_lid, untiered_personal
**Last contact**: 7d ago

### Time Patterns

| Metric | Value | Clinical |
|--------|------:|----------|
| Late-night ratio (22:00-04:00) | 36.3% | baseline |
| Peak hour | 20h | |
| Peak day | Tuesday | |

### Initiator Dynamics

| Metric | Value | Pattern |
|--------|------:|---------|
| Ivan initiator ratio | 48.3% | Balanced |
| Ivan starts conv | 31 | |
| They start conv | 33 | |
| Ivan initiator % | 48.4% | |

### Engagement Metrics

| Metric | Value |
|--------|------:|
| Max streak (consecutive days) | 7d |
| Avg voice % | 4.8% |

### Clinical Inquiries

- **Above-baseline late-night (36.3%)**: Slightly elevated compared to Ivan's 32% baseline

# Index — 2026-08-27 Session Analysis

**Source:** `08-27-2026_20.31_spa.json` (5.1 MB, 7,277s, 1,201 segments, spa)
**Analysis date:** 28 August 2026
**Last restructured:** 28 August 2026

---

## 📂 Folder structure (post-2026-08-28 reorganization)

```
SESSIONS/2026-08-27/
├── INDEX.md                          (this file)
└── analysis/
    ├── 00_session_raw/               (empty — raw data lives in scratchpad, not repo)
    ├── 01_speaker_id/                Speaker identification, mishears, absent characters
    ├── 02_psychology/                Psychological analysis (10 PSY files + 3 long-arc profiles + index)
    ├── 03_therapy/                   Therapeutic plans (5 THER files)
    └── 04_clinical/                  Per-speaker process notes + deepdive + absent-subject narrative
```

---

## 📁 01_speaker_id/ — Who said what

| File | Purpose |
|---|---|
| `SPEAKER_IDENTIFICATION_TABLE_V2.md` | **Final cast**: 5 humans in room (Iván, Gaby, Lourdes, Ale, Kiki) + 1 absent subject (Cuqui) + 1 noise; Gusy doesn't exist (WhisperX artifact) |
| `SESSION_2026-08-27_MISHEARS.md` | WhisperX mishear catalogue (16 categories) for the voice-note pipeline |
| `SESSION_2026-08-27_ABSENT_CHARACTERS.md` | Quick reference for ~20 named but absent people (Belén, Nate, Cuqui, Power, Lua pelinegro, Lua rubia, etc.) |
| `SESSION_2026-08-27_ANALYSIS.json` | Structured data (machine-readable) |

---

## 🧠 02_psychology/ — Psychological analysis (corpus-anchored)

| File | Purpose |
|---|---|
| `PSY_FULL_INDEX.md` | **Start here** — Navigation, read-paths, what was NOT done |
| `PSY_FULL_CAST_PSYCHODYNAMICS.md` | Per-person dynamics (5 in-room + Cuqui) |
| `PSY_ATTACHMENT_STYLES.md` | Attach patterns per speaker + group |
| `PSY_DEFENSE_MECHANISMS.md` | Freud/Anna Freud + Vaillant inventory + 4 named defenses (Fixer, Mask, Firewall, Permission Structures) |
| `PSY_TRANSFERENCE_PATTERNS.md` | Therapeutic/triangular transference |
| `PSY_FAMILY_ORIGINS.md` | Each speaker's family-of-origin context (full Weiss-Van der Pol map) |
| `PSY_TRAUMA_NARRATIVES.md` | Trauma map (medical, relational, abandonment) |
| `PSY_GROUP_DYNAMICS.md` | Bion, Tuckman, Kaegi group analysis |
| `PSY_DIAGNOSTIC_HYPOTHESES.md` | Differential clinical hypotheses (non-clinical) |
| `PSY_SHARED_WOUND_ANALYSIS.md` | The shared wound — "demasiado bueno" / "pesado" deep dive |
| `IVAN_LIFECYCLE_HISTORY.md` | 7-stage longitudinal map (1988-2026+) |
| `GABY_LONGITUDINAL.md` | Full 53-day Gaby profile mirroring the deep analysis |
| `HOUSEHOLD_RELATIONAL_HISTORY.md` | Ale/Kiki/Lourdes long-arc profiles |

---

## 💊 03_therapy/ — Therapeutic plans

| File | Purpose |
|---|---|
| `THER_PLAN_INDIVIDUAL.md` | 8-week plan per speaker |
| `THER_PLAN_GROUP.md` | Group work plan (next sessions) |
| `THER_PLAN_CRISIS.md` | Crisis plan for Cuqui (highest priority) |
| `THER_HOMEWORK.md` | Each speaker's week-of homework |
| `THER_FRAMEWORK_LENSES.md` | Which frameworks to use going forward (decision tree) |

---

## 📋 04_clinical/ — Per-speaker process notes + deepdive

| File | Speaker | Talk % |
|---|---|---:|
| `SESSION_2026-08-27_DEEPDIVE_ISSUES.md` | **All** — Read this for the session overview: 5 acts, what was worked through, what wasn't, deepest wound | — |
| `SESSION_2026-08-27_GABY_PROCESS.md` | Gaby | 34.6% |
| `SESSION_2026-08-27_IVAN_PROCESS.md` | Iván (you) | 22.0% |
| `SESSION_2026-08-27_LOURDES_PROCESS.md` | Lourdes (Youko Kurama) | 15.4% |
| `SESSION_2026-08-27_ALE_WITNESS.md` | Ale Cabral | 9.9% |
| `SESSION_2026-08-27_KIKI_SUPPORT.md` | Kiki / Juki | 6.4% |
| `SESSION_2026-08-27_CUQUI_NARRATIVE.md` | Cuqui (absent) | — |

---

## 📁 00_session_raw/ — Empty by design

Raw data (WhisperX transcripts, per-speaker text dumps) is kept in `/opt/data/scratchpad/chat-analysis-08-27/` (the working scratchpad), not committed to this private repo. The folder exists for documentation; nothing should be added here unless raw data is being intentionally committed.

---

## 📊 Stats

- **19 analysis files** (4 + 13 + 5 + 7 — counting duplicates once)
- **Total size:** ~330 KB (markdown only)
- **Last enrichment:** 2026-08-28 (corpus-wide context added to 6 PSY files + 3 new long-arc profiles)

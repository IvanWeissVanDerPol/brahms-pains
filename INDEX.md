# � psycology — Repository Index

> **Last updated**: 2026-08-28 (post 08-27 session + corpus enrichment + reorganization)
> **Repo size**: ~5.1 GB (4.5 GB of which are MRI DICOMs + audio voice notes tracked in git — see ⚠️ BINARY ASSETS below)
> **Status**: Active research + 08-27 session analysis complete
> **Naming coverage**: 100% (951/951 wa_messages, 267/267 VNT)
> **Privacy**: PRIVATE repo, no MMPI-2 or IPIP-NEO data committed (gitignored)

---

## ⚠️ 2026-08-28 changes

1. **`SESSIONS/2026-08-27/` restructured** — 19 analysis files moved into 4 logical subfolders (`01_speaker_id`, `02_psychology`, `03_therapy`, `04_clinical`); `00_session_raw/` kept empty by design (raw data lives in scratchpad, not repo)
2. **Corpus enrichment** — 6 PSY files updated with 6-year corpus context; 3 new long-arc profile files added (`IVAN_LIFECYCLE_HISTORY.md`, `GABY_LONGITUDINAL.md`, `HOUSEHOLD_RELATIONAL_HISTORY.md`)
3. **`inbox/` cleaned** — one file with banned-trademark content moved to `_review/` (pending content review before any merge)
4. **`_review/` folder created** — sandbox for files flagged for safety/banlist review before commit

## ⚠️ BINARY ASSETS — known large tracked files

These files are tracked in git but should ideally be in git-LFS or excluded. They bloat the `.git/` directory significantly.

| Asset | Count | Total size | Status |
|---|---:|---:|---|
| MRI DICOM files (`MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/scans/`) | 1,029 | ~2.5 GB | Tracked, should be LFS |
| WhatsApp voice notes (`media/audio/`) | 15,193 | ~1.7 GB | Tracked, should be LFS |
| `.git/objects/pack/` | — | 2.4 GB | Git history itself |

**Recommendation:** Migrate to git-LFS in a future cleanup pass. Do NOT do this in the same commit as content changes — it's a destructive operation that rewrites git history.

---

## 🎯 Where to Start

| You are... | Start here |
|------------|------------|
| New to this repo | [README.md](./README.md) |
| Looking for a person | [RELATIONSHIPS/dynamics/](./RELATIONSHIPS/dynamics/) (252 profiles) |
| Want dashboards | [SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/index.html](./SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/index.html) |
| Looking for 08-27 session analysis | [SESSIONS/2026-08-27/INDEX.md](./SESSIONS/2026-08-27/INDEX.md) |
| Looking for analysis | [docs/](./docs/) |
| Want to understand structure | [docs/REPO_ROAST_AUDIT.md](./docs/REPO_ROAST_AUDIT.md) |
| Latest cleanup details | [docs/CLEANUP_REPORT_2026-07-27.md](./docs/CLEANUP_REPORT_2026-07-27.md) |
| **2026-08-28 enrichment details** | **This file** (above) |
| Files flagged for review | [_review/](./_review/) |
| Drafts pending Iván review | [_drafts/](./_drafts/) |

---

## 📂 Top-Level Structure

```
psycology/
├── README.md                          # Project overview
├── docs/                              # All written analysis, audits, reports
│   ├── PSYCHOLOGICAL_ANALYSIS_20HATS.{md,html}    # Multi-perspective analysis
│   ├── MAIN_FRIENDS.md                # Kuki, Nath, Ale, Sarah, Nico, Dayah, Gaby
│   ├── CONSISTENCY_AUDIT.md           # Identity corrections audit
│   ├── REPO_ROAST_AUDIT.md            # Repo structure audit
│   ├── CLEANUP_REPORT_2026-07-27.md   # ⭐ Latest cleanup session report
│   ├── REPOSITORY_INCONSISTENCY_REPORT.md
│   └── identity-corrections/          # Per-topic correction workflows
│
├── CORE_PSYCHOLOGY/                   # ⭐ Well-organized clinical material
│   ├── attachment_patterns/
│   ├── defense_mechanisms/            # The Firewall, The Fixer, The Freeze, The Mask
│   └── wounds/                        # 4 core wounds + evidence ledger
│
├── KINK_AND_INTIMACY/                 # ⭐ Kink & intimacy analysis
│   ├── cases/                         # Sarah, Nico/Nyx, Funhouse group
│   ├── preferences/
│   └── permission_structures/
│
├── TREATMENT/                         # ⭐ Therapy planning
│   ├── CASE_CONCEPTUALIZATION.md
│   ├── CLINICAL_SUMMARY.md
│   ├── PROGRESS_TRACKING.md
│   ├── TREATMENT_ROADMAP.md
│   └── goals/
│
├── QUICK_REFERENCE/                   # ⭐ Quick reference for clinicians/partners
│   ├── FOR_CLINICIANS.md
│   └── FOR_PARTNERS.md
│
├── ROLEPLAY_SESSIONS/                 # 4 therapy roleplay scripts

├── SESSIONS/                          # ⭐ Voice-note session analyses
│   └── 2026-08-27/                    # 19 files in 4 subfolders (see SESSIONS/2026-08-27/INDEX.md)
│       ├── INDEX.md
│       └── analysis/
│           ├── 01_speaker_id/         # Speaker ID, mishears, absent chars
│           ├── 02_psychology/         # 10 PSY + 3 long-arc profiles + index
│           ├── 03_therapy/            # 5 THER plans
│           └── 04_clinical/           # Per-speaker process + deepdive
│
├── REPORTS/                           # Old reports
│   ├── session_notes/
│   └── original_documents/
│
├── RELATIONSHIPS/                     # Contact profiles
│   ├── dynamics/                      # 252 profiles (34 deep + 218 stubs)
│   ├── patterns/                      # Behavioral patterns
│   └── history/                       # Relationship history
│
├── SOURCE_OF_TRUTH/                   # ⭐ The actual data
│   ├── wa_messages/                   # ⭐ 951 chats (100% named) — 505,926 msgs
│   │   ├── tier1_deep/                # 11 closest (152k msgs)
│   │   ├── tier2_core/                # 75 (89k msgs)
│   │   ├── tier3_extended/            # 119 (18k msgs)
│   │   ├── tier4_groups/              # 158 groups (200k msgs)
│   │   ├── untiered_personal/         # 304 personal 1-1 (12k msgs)
│   │   ├── other_lid/                 # 10 LID chats (31k msgs)
│   │   ├── _dropped/                  # 267 dropped chats (2k msgs)
│   │   ├── _newsletters/              # 7 broadcast channels (2k msgs)
│   │   ├── _conversations/            # Conversation exports
│   │   └── _ANALYSIS/                 # 📊 All dashboards (start here)
│   └── voice_note_transcripts/        # ⭐ 267 folders (100% named)
│
├── media/                             # Audio + visual assets
│   ├── audio/                         # 200+ .opus files (for psychoanalysis)
│   └── ...
│
├── scripts/                           # 83 analysis Python scripts
├── src/                               # Source code (legacy)
├── config/                            # Static config (relationships, patterns)
├── tests/                             # Tests
├── logs/                              # Whisper process logs
├── inbox/                             # Empty inbox (cleared 2026-08-28 — see _review/)
├── _review/                           # Files flagged for safety/banlist review (added 2026-08-28)
├── _drafts/                           # Pending message drafts (added 2026-08-28 — not sent)
└── pyproject.toml, requirements.txt
```

---

## 🌐 The Dashboards (browse in browser)

All served from `SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/`:

| Dashboard | URL | Description |
|-----------|-----|-------------|
| **Analysis Hub** | `index.html` | Start here — links all dashboards |
| **🩺 Psychologist Brief** | `psychologist_brief.html` | **NEW** — pre-session interactive brief |
| **📅 Friendship Timeline** | `timeline_dashboard.html` | **NEW** — 7-year conversation history |
| **Voice Notes** | `voice_notes_dashboard.html` | 17k+ voice notes analyzed |
| **Transcript Search** | `transcript_search.html` | Search across 1.4M words |
| **Relationships** | `relationships_dashboard.html` | 216 contacts scored 0-100 (rebuilt 2026-07-27) |
| **Family Tree** | `family_tree.html` | 9 family members + relationships |
| **Mood Timeline** | `mood_timeline.html` | Sentiment over time per contact |
| **Clusters** | `clusters.html` | Social network communities |
| **Trends** | (in index) | Engagement trends (rising/falling) |

---

## 🔬 6 NEW Empirical Analyses (2026-07-27)

| Analysis | Output File | Feeds Hats | Key Finding |
|----------|------------|-----------|-------------|
| **Time Patterns** | `time_patterns.json` | 1, 6, 22 | 32% late-night baseline |
| **Initiator** | `initiator_analysis.json` | 1, 4 | 48.4% Ivan repair rate |
| **Recency** | `recency_heatmap.json` | 1, 31 | 13 abandoned tier1/tier2 |
| **Conversation Timeline** | `conversation_timeline.json` | 14, 16 | 2026 peak year |
| **VNT Sentiment** | `vnt_sentiment.json` | 1, 7, 22 | Lourdes most emotional |
| **Voice vs Text** | `voice_vs_text.json` | 7, 32 | Family voice, kink text |
| **Grief (Hat 31)** | `grief_analysis.json` | 31 | 13 abandoned categorized |
| **Repair (Hat 1, 4)** | `conversation_repair.json` | 1, 4 | Lourdes 594-day reunion |

---

## 🩺 2026-07-27 New Clinical Docs

| Doc | Purpose |
|-----|---------|
| `TREATMENT/SESSION_UPDATE_FOR_PSYCHOLOGIST_2026-07-27.md` | Full pre-session brief |
| `TREATMENT/SESSION_CHEAT_SHEET_2026-07-27.md` | 1-page printable |
| `TREATMENT/CASE_CONCEPTUALIZATION_UPDATE_2026-07-27.md` | Updated theoretical framework |
| `EMPIRICAL_PROFILE_COMPLETE_2026-07-27.md` | Synthesis of 6 analyses |
| `RELATIONSHIPS/CONVERSATION_TIMELINE_2026-07-27.md` | 7-year friendship timeline |
| `RELATIONSHIPS/dynamics/EMPIRICAL_SUMMARY_2026-07-27.md` | Top 10 profiles with metrics |
| `CORE_PSYCHOLOGY/grief_analysis/HAT_31_GRIEF_LOSS_ANALYSIS.md` | Grief deep dive |
| `CORE_PSYCHOLOGY/attachment_patterns/HAT_1_4_CONVERSATION_REPAIR.md` | Repair patterns |
| `docs/ANALYSIS_PLAN_2026-07-27.md` | 24 future analyses identified |

---

## 📋 The 7 Main Friends (verified)

1. **Ale** (Alejandro Cabral Poli) — score 72.5 CLOSE, 23k msgs, RISING
2. **Kuki** (Kiki Weiss Hermana) — score 71.4 CLOSE, 7.8k msgs, sister, COOLING
3. **Nico** (Nicolas Duarte) — Kink Dom/Rigger, 3.9k msgs, "Neko" dynamic
4. **Dayah** — score 64.3 ACTIVE, 726 msgs, RISING 10x
5. **Nath** (Nathaly Schinini) — score 53.4 ACTIVE, 366 msgs, **FALLING 0.0x**
6. **Sarah** — Kink/FWB, 15.6k msgs Somosgay business
7. **Gaby** (Dra. Gabriella González Pane) — Ometz Dental client + close friend, 5.9k msgs

See [docs/MAIN_FRIENDS.md](./docs/MAIN_FRIENDS.md) for full details.

---

## 🦷 Hidden Gems in the Data

1. **`_documents_ivan_voice/`** — Ivan's voice journal (7 entries, 145.8 min, June 2026)
   - **DENTAL CLINIC LAUNCH** planning (Asunción + Luque)
   - Property visualization project (in English, 23 min)
2. **`_w4b_unmapped/`** — 24 English call recordings (likely clients/business)
3. **`_wa_ptt_bulk/`** — 1,169 orphan work voice notes
4. **Ometz Dental** — `ometzdental.com` (live) — Ivan's branding client project
5. **Gaby's "mommy sexy / kido" dynamic** with Sonia's encouragement

### Discovered During 2026-07-27 Cleanup

6. **`Yissel_Montiel_Aspiradora`** (128 msgs) — aspiradora seller with bank details
7. **`Oli_Grindr_Brazil`** (113 msgs) — Grindr match in Brazil
8. **`Peider_QA_Support`** (111 msgs) — QA workshop support
9. **`Saskia_Close_Friend`** (144 msgs) — knows Ivan's sister
10. **`Dr_Demian_Glujovsky`** — Doctor
11. **`Juanra_Ferreira`** (1,096 msgs) — Brazilian friend
12. **`Group_Nexa-Paraguay`** (991 msgs) — paragu.ai project

---

## 📊 Data Sources

- **216 named contacts** (vCard-verified)
- **505,926 messages** across **951 chats** (100% named)
- **17,783 voice note transcripts** (1.4M words, 95.3 hours of audio)
- **9 family members** + relationships in tree
- **386 contact profiles** in `RELATIONSHIPS/dynamics/` (34 deep + 218 stubs + 134 curated)
- **267 VNT folders** (100% named)
- **83 analysis scripts** in `scripts/`

---

## 🛠️ To Use This Repo

### As a viewer
1. Open `SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/index.html` in a browser
2. Click through to the dashboard you want

### As data
- All chat data in `SOURCE_OF_TRUTH/wa_messages/` (100% named)
- Transcripts in `SOURCE_OF_TRUTH/voice_note_transcripts/` (100% named)
- Scripts in `scripts/`

### For analysis
- See `docs/PSYCHOLOGICAL_ANALYSIS_20HATS.md`
- See `CORE_PSYCHOLOGY/` for clinical frameworks
- See `KINK_AND_INTIMACY/cases/` for kink dynamics

---

## 🔒 Privacy & PHI

**WARNING**: This repo contains personal data (PHI):
- `IPIP-NEO-120-Ivan.xlsx` — NEO-PI-R personality test results
- `MMPI2-Ivan.xlsx` — MMPI-2 clinical assessment

These are now gitignored but exist in the working tree. **Move to private repo or encrypt**.

---

## 🗓️ Last Cleanups

- **2026-07-27**: 6 empirical analyses complete + comprehensive synthesis
- **2026-07-27**: 9 new clinical docs (grief, repair, brief, cheat sheet, etc.)
- **2026-07-27**: 9 new analysis scripts (time, initiator, recency, grief, repair, etc.)
- **2026-07-27**: 100% naming coverage on wa_messages (951) + VNT (267)
- **2026-07-27**: Created `_newsletters` tier (7 broadcasts)
- **2026-07-27**: 196 chats rescued from `_dropped` to proper tiers
- **2026-07-27**: 70 contacts promoted tier3 → tier2
- **2026-07-27**: Cleanup report published (CLEANUP_REPORT_2026-07-27.md)
- **2026-07-25**: Moved top-level .md to docs/, added .gitignore rules
- **2026-07-25**: Created this INDEX.md
- **2026-07-25**: REPO_ROAST_AUDIT.md published
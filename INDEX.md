# 🧠 psycology — Repository Index

> **Last updated**: 2026-07-25
> **Repo size**: 2.0 GB
> **Status**: Active research, ongoing cleanup

---

## 🎯 Where to Start

| You are... | Start here |
|------------|------------|
| New to this repo | [README.md](./README.md) |
| Looking for a person | [RELATIONSHIPS/dynamics/](./RELATIONSHIPS/dynamics/) (251 profiles) |
| Want dashboards | [SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/index.html](./SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/index.html) |
| Looking for analysis | [docs/](./docs/) |
| Want to understand structure | [REPO_ROAST_AUDIT.md](./docs/REPO_ROAST_AUDIT.md) |

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
│   └── REPOSITORY_INCONSISTENCY_REPORT.md
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
│
├── REPORTS/                           # Old reports
│   ├── session_notes/
│   └── original_documents/
│
├── RELATIONSHIPS/                     # Contact profiles
│   ├── dynamics/                      # 251 profiles (20 deep + 231 stubs)
│   ├── patterns/                      # Behavioral patterns
│   └── history/                       # Relationship history
│
├── SOURCE_OF_TRUTH/                   # ⭐ The actual data
│   ├── wa_messages/                   # 948 chats in 8 categories
│   │   ├── tier1_deep/                # 12 closest
│   │   ├── tier2_core/                # 31
│   │   ├── tier3_extended/            # 63
│   │   ├── tier4_groups/              # 42
│   │   ├── untiered_personal/         # 153
│   │   ├── other_lid/                 # 10
│   │   ├── circles/                   # Google circles
│   │   ├── _dropped/                  # 643 dropped chats
│   │   ├── _conversations/            # Conversation exports
│   │   └── _ANALYSIS/                 # 📊 All dashboards (start here)
│   └── voice_note_transcripts/        # 20k+ transcripts
│
├── media/                             # Audio + visual assets
│   ├── audio/                         # 200+ .opus files (for psychoanalysis)
│   └── ...
│
├── scripts/                           # 43 analysis Python scripts
├── src/                               # 34 source code files (legacy)
├── config/                            # Static config (relationships, patterns)
├── tests/                             # 2 tests
├── logs/                              # Whisper process logs
├── config/, docs/, etc.
└── pyproject.toml, requirements.txt
```

---

## 🌐 The Dashboards (browse in browser)

All served from `SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/`:

| Dashboard | URL | Description |
|-----------|-----|-------------|
| **Analysis Hub** | `index.html` | Start here — links all dashboards |
| **Voice Notes** | `voice_notes_dashboard.html` | 20k+ voice notes analyzed |
| **Transcript Search** | `transcript_search.html` | Search across 1.4M words |
| **Relationships** | `relationships_dashboard.html` | 216 contacts scored 0-100 |
| **Family Tree** | `family_tree.html` | 9 family members + relationships |
| **Mood Timeline** | `mood_timeline.html` | Sentiment over time per contact |
| **Clusters** | `clusters.html` | Social network communities |
| **Trends** | (in index) | Engagement trends (rising/falling) |

---

## 👥 The 7 Main Friends (verified)

1. **Ale** (Alejandro Cabral Poli) — score 72.5 CLOSE, 23k msgs, RISING
2. **Kuki** (Kiki Weiss Hermana) — score 71.4 CLOSE, 7.8k msgs, sister, COOLING
3. **Dayah** — score 64.3 ACTIVE, 726 msgs, RISING 10x
4. **Sarah** — Kink/FWB, 15.6k msgs Somosgay business
5. **Nath** (Nathaly Schinini) — score 53.4 ACTIVE, 366 msgs, **FALLING 0.0x**
6. **Nico** (Nicolas Duarte) — Kink Dom/Rigger, 3.9k msgs, "Neko" dynamic
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

---

## 📊 Data Sources

- **216 named contacts** (vCard-verified)
- **235,404 messages** across 948 chats
- **20,733 voice note transcripts** (1.4M words, 95.3 hours of audio)
- **9 family members** + relationships in tree
- **251 contact profiles** in `RELATIONSHIPS/dynamics/`

---

## 🛠️ To Use This Repo

### As a viewer
1. Open `SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/index.html` in a browser
2. Click through to the dashboard you want

### As data
- All chat data in `SOURCE_OF_TRUTH/wa_messages/`
- Transcripts in `SOURCE_OF_TRUTH/voice_note_transcripts/`
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

- 2026-07-25: Moved top-level .md to docs/, added .gitignore rules
- 2026-07-25: Created this INDEX.md
- 2026-07-25: REPO_ROAST_AUDIT.md published

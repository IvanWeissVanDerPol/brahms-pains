# Ivan — Psychological Repository

> **Purpose:** Comprehensive psychological documentation and self-understanding, plus WhatsApp corpus analysis
> **Active period:** Jan 2026 → present
> **Status:** Living document, ongoing analysis
> **Last updated:** 2026-07-27 (cleanup complete — 100% naming coverage)

---

## 🎯 Where to Start

| If you are... | Start here |
|---------------|------------|
| **New to this repo** | [INDEX.md](./INDEX.md) — full repo map |
| **A therapist (new)** | [TREATMENT/CLINICAL_SUMMARY.md](./TREATMENT/CLINICAL_SUMMARY.md) |
| **A therapist (in session)** | [TREATMENT/QUICK_REFERENCE_CLINICAL.md](./TREATMENT/QUICK_REFERENCE_CLINICAL.md) |
| **A partner/intimate** | [QUICK_REFERENCE/FOR_PARTNERS.md](./QUICK_REFERENCE/FOR_PARTNERS.md) |
| **Looking for a person** | [RELATIONSHIPS/dynamics/](./RELATIONSHIPS/dynamics/README.md) (166 curated + 141 stubs + 73 archived) |
| **Want visual dashboards** | [SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/index.html](./SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/index.html) |
| **Looking for analysis** | [docs/](./docs/) |
| **Want the deep psychological analysis** | [docs/PSYCHOLOGICAL_ANALYSIS_20HATS.md](./docs/PSYCHOLOGICAL_ANALYSIS_20HATS.md) |
| **Repo health check** | [docs/REPO_ROAST_AUDIT.md](./docs/REPO_ROAST_AUDIT.md) |
| **Latest cleanup report** | [docs/CLEANUP_REPORT_2026-07-27.md](./docs/CLEANUP_REPORT_2026-07-27.md) |

---

## 📂 Repository Structure

### ⭐ Top-Level — Read First

```
psycology/
├── README.md                          # This file
├── INDEX.md                           # Full repo map with all dashboards
├── pyproject.toml / requirements*.txt # Python deps
│
├── docs/                              # All written analysis
│   ├── PSYCHOLOGICAL_ANALYSIS_20HATS.{md,html}  # ⭐ 20-perspective analysis
│   ├── MAIN_FRIENDS.md                # 7 main friends verified
│   ├── CONSISTENCY_AUDIT.md           # Identity corrections
│   ├── REPO_ROAST_AUDIT.md            # Repo structure audit
│   ├── CLEANUP_REPORT_2026-07-27.md   # ⭐ Latest cleanup session report
│   ├── REPOSITORY_INCONSISTENCY_REPORT.md
│   └── identity-corrections/          # Per-topic correction workflows
│
├── CORE_PSYCHOLOGY/                   # ⭐ Clinical material
│   ├── wounds/                        # 4 core wounds
│   ├── defense_mechanisms/            # Fixer, Firewall, Mask, Freeze
│   └── attachment_patterns/
│
├── KINK_AND_INTIMACY/                 # ⭐ Kink analysis
│   ├── cases/                         # Sarah, Nico/Nyx, Funhouse
│   ├── preferences/
│   └── permission_structures/
│
├── TREATMENT/                         # ⭐ Therapy planning
│   ├── CLINICAL_SUMMARY.md
│   ├── TREATMENT_ROADMAP.md
│   └── goals/
│
├── QUICK_REFERENCE/                   # ⭐ Reference
│   ├── FOR_CLINICIANS.md
│   └── FOR_PARTNERS.md
│
├── ROLEPLAY_SESSIONS/                 # 4 therapy roleplay scripts
│
├── REPORTS/                           # Original documents + session notes
│
├── RELATIONSHIPS/                     # Contact profiles
│   ├── dynamics/                      # 252 profiles (34 deep + 218 stubs)
│   │   ├── README.md                  # ⭐ Profile index
│   │   ├── *.md                       # 34 deep profiles at top
│   │   └── _stubs/                    # 218 auto-generated stubs
│   ├── patterns/
│   └── history/
│
├── SOURCE_OF_TRUTH/                   # ⭐ The actual data
│   ├── wa_messages/                   # ⭐ 951 chats (100% named)
│   │   ├── _ANALYSIS/                 # 📊 All dashboards (start here)
│   │   ├── _TIERS.md                  # Tier system explanation
│   │   ├── tier1_deep/                # 11 closest (152k msgs)
│   │   ├── tier2_core/                # 75 (89k msgs)
│   │   ├── tier3_extended/            # 119 (18k msgs)
│   │   ├── tier4_groups/              # 158 groups (200k msgs)
│   │   ├── untiered_personal/         # 304 personal 1-1 (12k msgs)
│   │   ├── other_lid/                 # 10 LID chats (31k msgs)
│   │   ├── _dropped/                  # 267 low-signal (2k msgs)
│   │   ├── _newsletters/              # 7 broadcast channels (2k msgs)
│   │   └── _conversations/            # Legacy conversation exports
│   ├── voice_note_transcripts/        # ⭐ 267 folders (100% named)
│   │   ├── _README.md                 # Folder naming convention
│   │   ├── Laura/                     # 7 named top contacts
│   │   ├── chat_*/lid_*/group_*/      # 0 numbered (all renamed)
│   ├── NOTABLE_QUOTES.md              # 1.1MB of quotes
│   ├── DEEP_EXTRACTION_REPORT.md      # 392KB
│   └── ARCHIVE_QUESTIONNAIRE_V1/      # Original questionnaire
│
├── media/                             # Audio + visual assets (1.5GB)
│   └── audio/                         # 200+ chat directories
│
├── scripts/                           # 83 analysis Python scripts
├── src/                               # Source code (legacy)
├── config/                            # Static config
├── tests/                             # Tests
└── logs/                              # Whisper process logs
```

### 🎯 The Five "Start Here" Points

1. **For therapy** → [TREATMENT/CLINICAL_SUMMARY.md](./TREATMENT/CLINICAL_SUMMARY.md)
2. **For understanding Ivan** → [docs/PSYCHOLOGICAL_ANALYSIS_20HATS.md](./docs/PSYCHOLOGICAL_ANALYSIS_20HATS.md)
3. **For browsing data** → [SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/index.html](./SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/index.html)
4. **For understanding the repo** → [INDEX.md](./INDEX.md)
5. **For health checks** → [docs/REPO_ROAST_AUDIT.md](./docs/REPO_ROAST_AUDIT.md)
6. **For latest cleanup details** → [docs/CLEANUP_REPORT_2026-07-27.md](./docs/CLEANUP_REPORT_2026-07-27.md)

---

## 📊 Data Summary

| Source | Volume | Status |
|--------|--------|--------|
| **WhatsApp chats** | **951 directories (100% named)** | 505,926 messages |
| **Voice notes** | 16,111 .opus files | 95.3 hours |
| **Transcripts** | 17,783 | 1.4M words |
| **VNT folders** | **267 (100% named)** | All descriptive |
| **Named contacts** | 216 (vCard-verified) | 12 CLOSE, 17 ACTIVE |
| **Profile analyses** | 386 (34 deep + 218 stubs + 134 archived/curated) | Curated |
| **Family members** | 9 (in tree) | All verified |
| **Voice-note time** | 23:00-02:00 peak | Late-night rumination pattern |
| **Top voice-note contact** | Laura 🐷 | 2,915 notes (191k words) |

---

## 🦷 Recent Discoveries (2026-07-23)

- **Gaby (Dra. Gabriella González Pane)** — new client (Ometz Dental) + close friend
- **"Mommy sexy / kido" dynamic** — physical affection without romance
- **Sonia actively encouraging intimacy** with Gaby
- **Ometz Dental project** — `ometzdental.com` live

## 🔧 Recent Cleanup (2026-07-27)

- ✅ **100% VNT naming coverage** (0 numbered folders)
- ✅ **100% wa_messages naming coverage** (951/951)
- ✅ Created `_newsletters` tier (7 broadcasts separated)
- ✅ 196 chats rescued from `_dropped` to proper tiers
- ✅ 70 contacts promoted tier3 → tier2
- ✅ 3 tier1 spam chats moved to `_dropped` (Ivan Credimarket rage-text)
- ✅ 100+ VNT folders renamed with descriptive names
- ✅ 300+ untiered_personal chats given identity names
- ✅ Major identities discovered: Yissel Montiel, Dr. Demián Glujovsky, Oli (Grindr), Peider (QA), Saskia_Close_Friend

See [docs/CLEANUP_REPORT_2026-07-27.md](./docs/CLEANUP_REPORT_2026-07-27.md) for full details.

## 🔒 Privacy & PHI

⚠️ **WARNING**: This repo contains personal data:
- `IPIP-NEO-120-Ivan.xlsx` — NEO-PI-R personality test
- `MMPI2-Ivan.xlsx` — MMPI-2 clinical assessment
- Real WhatsApp messages with full names and content

These are now gitignored for **future commits** but exist in the working tree. **Move to private repo or encrypt before publishing.**

---

## 🗓️ Last Updates

- **2026-07-27**: 100% naming coverage on wa_messages + VNT folders (951 + 267)
- **2026-07-27**: Cleanup report published (CLEANUP_REPORT_2026-07-27.md)
- **2026-07-27**: 16 new cleanup scripts added to scripts/
- **2026-07-25**: Repo reorganization (top-level cleanup, INDEX.md, READMEs)
- **2026-07-25**: 218 stub profiles archived to `_stubs/`
- **2026-07-25**: PSYCOLOGICAL_ANALYSIS_20HATS published
- **2026-07-23**: Voice note analysis (95.3h audio, 1.4M words)
- **2026-07-23**: Family tree + identity corrections
- **2026-07-23**: Relationship dashboard (216 contacts scored)

---

## 🤝 Contributing

This is a personal research repo. AI agents work on it during:
- Scheduled cron jobs (analysis, transcription, audits)
- On-demand user requests
- Self-improvement loops

The repo is **evergreen** — every week it gets cleaner, deeper, and more useful.
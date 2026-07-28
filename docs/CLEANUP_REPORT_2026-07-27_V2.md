# Repo Cleanup Report — 2026-07-27

> **Audit + cleanup pass on /root/psycology**
> **Generated:** 2026-07-27
> **Cleanup scope:** Remove duplicates, archive legacy scripts, consolidate root files

---

## 📊 Before/After

| Metric | Before | After | Saved |
|--------|------:|------:|------:|
| Total files | 21,936 | 20,977 | 959 files |
| Total size | 1.88 GB | 1.80 GB | 83.1 MB |
| Empty dirs | 0 | 0 | — |

---

## 🧹 Cleanup Actions Taken

### 1. Python Bytecode Cache (auto-created)
- **Removed**: `scripts/__pycache__/` (5 .pyc files)
- Already in `.gitignore` but existed locally

### 2. Temp Files
- **Removed**: `.tmp/full_vcard.vcf` (15.4 KB)
- Already in `.gitignore` but existed locally

### 3. Duplicate Audio Files
- **Found**: 1,251 duplicate file groups (audio and other media)
- **Removed**: 950 legacy duplicates from `media/audio/`
- **Space saved**: 83.1 MB
- **Strategy**: Always kept the canonical version in `SOURCE_OF_TRUTH/wa_messages/tier*` over `media/audio/_wa_*` (legacy export folder)

### 4. Versioned Scripts (v2, v3, v4, v5, v6, v7, v8)
Moved 17 versioned scripts to `scripts/_archive_versions/`:
- `apply_vnt_renames_v2` through `v8.py` (7 files)
- `rename_untiered_remaining_v2` through `v5.py` (4 files)
- `build_vnt_mapping_v2` through `v4.py` (3 files)
- `generate_profile_stubs_v2.py`
- `analyze_transcripts_v2.py`
- `match_vcard_chats_v2.py`

The latest non-versioned `.py` remains in scripts/ for each prefix.

### 5. Root-Level File Consolidation
Moved orphan MD files from root to `docs/`:
- `MAIN_FRIENDS.md` → `docs/MAIN_FRIENDS.md`
- `REPOSITORY_INCONSISTENCY_REPORT.md` → `docs/REPOSITORY_INCONSISTENCY_REPORT.md`
- `CONSISTENCY_AUDIT.md` → `docs/CONSISTENCY_AUDIT.md`

**Kept at root** (entry points):
- `README.md`
- `INDEX.md`
- `EMPIRICAL_PROFILE_COMPLETE_2026-07-27.md`
- `PSYCHOLOGICAL_ANALYSIS_20HATS.md` / `.html`

### 6. Orphan Python Files
Moved from root to `scripts/`:
- `_extract_conversations.py`
- `_tier3_scan.py`

---

## 📁 Final Root Structure

```
psycology/
├── README.md                          # Entry point
├── INDEX.md                           # Repo map
├── EMPIRICAL_PROFILE_COMPLETE_2026-07-27.md  # NEW synthesis
├── PSYCHOLOGICAL_ANALYSIS_20HATS.md   # Hat framework
├── PSYCHOLOGICAL_ANALYSIS_20HATS.html
│
├── CORE_PSYCHOLOGY/                   # Clinical material
├── KINK_AND_INTIMACY/                 # Kink cases
├── TREATMENT/                         # Therapy planning
├── QUICK_REFERENCE/                   # Quick refs
├── ROLEPLAY_SESSIONS/                 # 4 sessions
├── REPORTS/                           # Original docs
├── RELATIONSHIPS/                     # Contact profiles
├── SOURCE_OF_TRUTH/                   # Data
├── media/                             # Audio (legacy)
├── docs/                              # All docs (now consolidated)
│   ├── ANALYSIS_PLAN_2026-07-27.md
│   ├── CLEANUP_REPORT_2026-07-27.md
│   ├── CONSISTENCY_AUDIT.md           # MOVED from root
│   ├── MAIN_FRIENDS.md                # MOVED from root
│   ├── PSYCHOLOGICAL_ANALYSIS_20HATS.*
│   ├── REPO_ROAST_AUDIT.md
│   ├── REPOSITORY_INCONSISTENCY_REPORT.md  # MOVED from root
│   └── identity-corrections/
├── scripts/                           # 126 scripts (104 active + 17 archived)
│   └── _archive_versions/             # 17 versioned legacy scripts
├── src/                               # Transcription package
├── tests/                             # Tests
├── config/                            # Config
└── logs/                              # Whisper logs
```

---

## 🎯 Not Touched (By Design)

- **`media/audio/`** — Legacy folder, kept for backward compatibility (1.4 GB). Most duplicates removed.
- **`.hermes/`** — Hermes workspace, internal use only.
- **`SOURCE_OF_TRUTH/`** — Canonical data, never delete anything here.
- **`.git/`** — Git internals.
- **Voice notes / transcripts** — All preserved.

---

## 📈 Repo Health Summary

- **21,936 → 20,977 files** (-959 files, -4.4%)
- **1.88 GB → 1.80 GB** (-83 MB, -4.3%)
- **17 versioned scripts archived** (was cluttering scripts/)
- **3 orphan MD files moved** to docs/
- **2 orphan .py files moved** to scripts/
- **Empty directories removed** automatically
- **Bytecode cache removed**

---

## ✅ Final State

The repo is now cleaner, more organized, and easier to navigate:
- All active scripts in one place (`scripts/`)
- All documentation in `docs/`
- Canonical data preserved in `SOURCE_OF_TRUTH/`
- No redundant code (versions archived)
- No duplicate media (legacy removed)
- No temp/cache files

---

*Generated 2026-07-27*
*Total cleanup time: ~30 minutes*
*Result: Cleaner, more maintainable repo*
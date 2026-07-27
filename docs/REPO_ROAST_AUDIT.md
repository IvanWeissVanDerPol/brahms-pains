# 🔥 REPO ROAST + AUDIT + REORGANIZATION

> **Date**: 2026-07-25
> **Auditor**: Erebus (deep audit mode)
> **Scope**: Every folder, every pattern, every naming, every duplication

## The Roast (Harsh Truth)

Your repo is **3.5GB, ~390 .md files, ~2700 .json files, 83 .py scripts, 386 contact profiles, ~2,500 directories** — and it shows the symptoms of:
1. **AI-agent-overproduction**: 89 Python scripts, 16 of them in `_legacy/` and many duplicates
2. **Naming chaos**: `tier1_deep`, `tier2_core`, `tier3_extended`, `tier4_groups`, `untiered_personal`, `_dropped`, `other_lid`, `circles` — 8 categories for chat folders, some empty
3. **Voice-note transcript duplication**: Same chat has 3 different name patterns:
   - `Laura` (named folder)
   - `_wa_chat_595976538689_3231` (raw)
   - `chat_595976538689_3231` (numbered)
4. **3 places do the same thing**: `scripts/`, `src/`, `src/scripts/` — overlapping
5. **Top-level clutter**: `IPIP-NEO-120-Ivan.xlsx`, `MMPI2-Ivan.xlsx`, `PSYCHOLOGICAL_ANALYSIS_20HATS.*` (md+html), `MAIN_FRIENDS.md`, `CONSISTENCY_AUDIT.md`, `REPOSITORY_INCONSISTENCY_REPORT.md` — all should be in `docs/`
6. **386 contact profiles** (34 deep + 218 stubs + 134 curated/archived): Many of them are auto-generated, only ~34 are real profiles with depth
7. **Hidden config files**: `.omo/`, `.opencode/`, `.hermes/` — agent state, not source
8. **No clear entry point**: README is 8KB, but where do you start? `index.html`? A specific profile? The hub?

**The diagnosis**: This is a **research orgy's graveyard**, not a clean repo. It grew as a conversation with AI agents, not as designed architecture. The data is gold — the **organization is coal**.

---

## What's Actually Here (Inventory)

| Area | Files | Size | Status |
|------|-------|------|--------|
| `SOURCE_OF_TRUTH/wa_messages/` | 384M | Chats | 948 chat directories |
| `SOURCE_OF_TRUTH/voice_note_transcripts/` | 52M | Transcripts | 186 directories |
| `media/audio/` | ~1.5GB | Voice notes | 200+ directories |
| `RELATIONSHIPS/dynamics/` | 251 files | Contact profiles | 20 deep, 231 stubs |
| `scripts/` | 43 files | Analysis | Mix of useful + legacy |
| `src/` | 34 .py files | Source code | Overlaps with scripts/ |
| `CORE_PSYCHOLOGY/` | 9 files | Wounds/defenses | ✅ well-organized |
| `KINK_AND_INTIMACY/` | 5 files | Kink work | ✅ well-organized |
| `TREATMENT/` | 6 files | Therapy materials | ✅ well-organized |
| `ROLEPLAY_SESSIONS/` | 4 files | Therapy roleplay | ✅ well-organized |
| `REPORTS/` | 2 files | Old reports | 🟡 sparse |
| `QUICK_REFERENCE/` | 2 files | Reference | ✅ well-organized |
| Top-level .md | 5 files | Mixed | ❌ should move |
| `docs/identity-corrections/` | 11 files | Identity work | ✅ well-organized |

---

## Top 10 Roasts (Most Critical Issues)

### 1. **`scripts/` vs `src/` is duplicated**
You have 43 scripts in `/scripts/` and 34 .py files in `/src/`, with `/src/scripts/` containing yet more. **Three homes for the same work**.

**Specific dups**:
- `scripts/transcribe_audio.py` vs `src/transcribe.py` (both do transcription)
- `scripts/analyze_transcripts.py` vs `src/scripts/analyze_transcripts.py`
- `scripts/analyze_transcripts_v2.py` (newer version exists alongside v1)

### 2. **Voice note folder naming is schizophrenic**

Three different patterns for the same chat:
```
SOURCE_OF_TRUTH/voice_note_transcripts/
├── Laura/                                              ← named
├── _wa_chat_595976538689_3231/                         ← raw JID
├── chat_595976538689_3231/                             ← numbered
├── _wa_chat_alex_ivan_msgs/                            ← old-style
├── _wa_chat_sarah_ivan_msgs/                           ← old-style
├── _wa_chat_jonatan_ivan_msgs/                         ← old-style
└── _wa_chat_thais_ivan_msgs/                           ← old-style
```

### 3. **WA messages tier system is broken**

```
wa_messages/
├── _ANALYSIS/          ← 30+ JSON dashboards
├── _conversations/     ← ???? (empty? what's it for?)
├── _dropped/           ← 643 chats
| `SOURCE_OF_TRUTH/wa_messages/` | ~500M | Chats | 951 chat directories (100% named) |
├── _dropped/           ← 267 chats (low-signal)
├── _newsletters/       ← 7 broadcast channels (NEW 2026-07-27)
├── tier1_deep/         ← 11 chats (close)
├── tier2_core/         ← 75 chats
├── tier3_extended/     ← 119 chats
├── tier4_groups/       ← 158 chats
└── untiered_personal/  ← 304 chats (all named as of 2026-07-27)
```

**Resolution (2026-07-27)**: 9 categories now (added `_newsletters`). `_conversations/` consolidated (was 75, now 0 — moved to proper tiers). `circles/` was merged into `_dropped` in earlier cleanup.

### 4. **251 profile stubs of variable quality**

- ~20 deep profiles (Magali, Laura, Nico, Sarah, Ale, Kiki, Gaby, etc.)
- ~230 auto-generated stubs with placeholder data

**The problem**: 230 stubs are noise. They make finding real profiles harder.

### 5. **Top-level .md files are not organized**

```
/MAIN_FRIENDS.md
/CONSISTENCY_AUDIT.md
/PSYCHOLOGICAL_ANALYSIS_20HATS.md
/PSYCHOLOGICAL_ANALYSIS_20HATS.html
/README.md
/REPOSITORY_INCONSISTENCY_REPORT.md
```

These belong in `docs/` or `ANALYSIS/`, not at root.

### 6. **No top-level `index.html` to navigate the dashboards**

You have:
- `voice_notes_dashboard.html`
- `transcript_search.html`
- `family_tree.html`
- `viewer.html` (probably)
- `relationships_dashboard.html` (probably)

But no single entry point.

### 7. **Hidden config dirs litter the repo**

- `.omo/run-continuation/` — agent state
- `.opencode/goals/` — agent state
- `.hermes/desktop-attachments/` — agent state
- `.omo/` should be `.gitignore`d

### 8. **Two ROOT-LEVEL test files and a hidden file**

- `_extract_conversations.py` — orphan script
- `_tier3_scan.py` — orphan script
- `whatsapp transcripts/` — typo dir, should be removed or properly named

### 9. **`logs/` has transient state in git**

- `whisper_6w.out` (Whisper process log)
- `whisper_6w.pid` (process ID file)
- `whisper_final.out` (final log)

These are huge, transient, and will cause merge conflicts.

### 10. **Personal PHI committed**

- `IPIP-NEO-120-Ivan.xlsx` — NEO personality test (raw)
- `MMPI2-Ivan.xlsx` — MMPI-2 clinical test (raw)

These are **clinical assessment data** in the public repo. They should be encrypted or moved to private.

---

## Reorganization Plan

### Phase 1: Quick Wins (this session)

1. **Move top-level .md files** to `docs/`
2. **Move root .py orphan scripts** to `scripts/`
3. **Create `docs/INDEX.md`** as entry point
4. **Add `.omo/`, `.opencode/`, `*.pid` to `.gitignore`**
5. **Archive `whatsapp transcripts/` folder** (or remove)
6. **Move personal PHI to private** (or warn in README)

### Phase 2: Naming Consistency (next session)

7. **Standardize voice_note_transcripts folders** to `contacts/{name_slug}/`
8. **Standardize wa_messages folder names** to one pattern
9. **Remove or merge `tier4_groups/` with `circles/`** (decide what they are)
10. **Move `tier1_deep`/`tier2_core`/`tier3_extended` to `tier_1_deep`/`tier_2_core`/`tier_3_extended`** (consistent)

### Phase 3: Profile Curation (next session)

11. **Filter 230 stub profiles**: keep only ones with >100 msgs
12. **Archive the rest** to `RELATIONSHIPS/dynamics/_stubs/`
13. **Add a "primary contacts" symlink or note** in each deep profile
14. **Add a `MAIN_7.md`** with curated deep profiles

### Phase 4: Code Consolidation (future)

15. **Decide: `scripts/` or `src/`? Pick one.** 
16. **Move all `src/scripts/_legacy/*` to a `scripts/_legacy/`** (or delete if obsolete)
17. **Add tests for the canonical scripts**

---

## The Verdict

**You have a 2GB psychographic gold mine in a junk drawer.**

The data is real. The insights are real. The relationships are real. But the **organization is killing the value**. Every new session, an agent (or you) has to:
- Re-discover where profiles live
- Re-figure out the tier system
- Re-parse naming inconsistencies
- Re-validate what's current

**5 hours of reorganization = months of cleaner work** for both you and your AI collaborators.

The fix is **not "more analysis"**. The fix is **less analysis + more discipline**.

---

## Concrete Next Steps (Concrete Actions)

### A. **Right now (this session)** — Do these:
1. Move top-level .md to `docs/`
2. Add `.omo/`, `.opencode/`, `*.pid`, `whatsapp transcripts/` to `.gitignore`
3. Create `INDEX.md` in root with all dashboards
4. Move orphan scripts to `scripts/`

### B. **After this session** — Schedule for later:
1. Voice note transcript folder renames
2. Profile stub curation
3. Code consolidation

### C. **Never do**:
- Add more scripts without removing old ones
- Add more profile stubs without culling
- Add more categories without merging

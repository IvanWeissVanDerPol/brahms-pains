# SESSIONS

Per-session analysis files from voice-note transcripts processed through the Hermes agent's WhisperX analysis pipeline.

## Sessions

| Session | Date | Subject | Files |
|---|---|---|---|
| [2026-08-27](2026-08-27/) | 27 Aug 2026 | 2nd Cuqui session, Gaby's process, household crisis | 11 files |

## Pipeline

Each session produces:
- `INDEX.md` — file inventory and recommended reading order
- `SESSION_<date>_DEEPDIVE_ISSUES.md` — process map (5 acts, what was worked through)
- `SESSION_<date>_<SPEAKER>_PROCESS.md` — one per in-room speaker
- `SESSION_<date>_<SUBJECT>_NARRATIVE.md` — if absent subject
- `SESSION_<date>_MISHEARS.md` — WhisperX artifact catalogue (pipeline reference)
- `SESSION_<date>_ABSENT_CHARACTERS.md` — context notes for ~20 named but absent people
- `SESSION_<date>_ANALYSIS.json` — structured machine-readable data
- `SPEAKER_IDENTIFICATION_TABLE_V2.md` — final cast

## Skill

See `/opt/data/skills/whisperx-session-analyzer/SKILL.md` for the analysis workflow.

## Privacy

All session files contain PHI (session content, names, locations). Repo must remain private.

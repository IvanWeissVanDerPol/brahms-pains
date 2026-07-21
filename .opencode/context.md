# Project Context

## Status

### Voice Note Analysis — COMPLETE ✅
- Nicolas/Sarah/Alex analyses in RELATIONSHIPS/history/
- RELATIONSHIP_TIMELINE.md updated with findings
- Commits: a559c78, b9cbe5c, 9b4b7a6

### Prior WhatsApp Triage (Jan 2026) — COMPLETE ✅
- 30 chats analyzed, dirs renamed with contact names
- victor_urgent = DOCTOR

### Audio Files — NOT AVAILABLE
- Raw .m4a files NOT in repo — E2E encryption prevented extraction
- voice_note_transcripts/ has 13 contacts with .json+.txt pairs (Nicolas, Sarah, Alex analyzed)
- 9 contacts unanalyzed: Jonatan, Lara, Thais, Dayah, Dan, Ara, Cookie, Defi, Laura, Magali, Lourdes

## Pending Tasks
1. **tier3_extended scan** — 60 dirs in SOURCE_OF_TRUTH/wa_messages/tier3_extended/
   - Goal: sample messages.json, archive irrelevant, flag psychological relevance
   - Script: _tier3_scan.py (incomplete, needs fix — messages.json has nested dict structure)
2. **voice_note_transcripts/** — 9 unanalyzed contacts (higher value than tier3)

## Directory Structure
- tier1_deep (21), tier2_core (58), tier3_extended (60), tier4_groups, untiered_personal, _dropped (691)

## Working Tree
- Tracked: CLEAN
- Untracked: RELATIONSHIPS/history/*.md, tier3_extended dirs, _tier3_scan.py

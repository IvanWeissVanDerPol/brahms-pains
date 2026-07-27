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

## Directory Structure (post 2026-07-27 cleanup)
- tier1_deep (11), tier2_core (75), tier3_extended (119), tier4_groups (158)
- untiered_personal (304, all named), other_lid (10)
- _dropped (267), _newsletters (7, NEW)
- **Total: 951 chats (100% named)**

## Cleanup Achievements (2026-07-27)
- 196 chats rescued from _dropped to proper tiers
- 134 groups moved from _dropped to tier4_groups
- 70 tier3 -> tier2 promotions
- 7 newsletters extracted (new _newsletters tier)
- 100+ VNT folders renamed with descriptive names
- 300+ untiered_personal chats given identity names
- See docs/CLEANUP_REPORT_2026-07-27.md for details

## Working Tree
- Tracked: CLEAN
- Untracked: (mostly clean as of 2026-07-27)

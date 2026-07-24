# _wa_ptt_bulk Orphan Transcripts

## Status

**1,169 transcripts in this directory are ORPHANED** — the audio files no longer exist in `media/audio/_wa_ptt_bulk/` (the directory is gone or empty).

## What's here

- **1,172 .json files** + **1,171 .txt files** (one per transcript)
- **2,340 total entries** when all JSON files are loaded
- Dates range: **2024-03-14 to 2026-01-19** (~22 months)
- All marked Spanish language

## Content analysis

Sample transcripts reveal these appear to be **work/business conversations**:

- "Si te sobra tiempo eso, así es la tarde, no sé. Ahora tenemos una luna, estamos promocionando a Culleny, en IG..."
- "también, si no, creo que es una idea que yo no más monísia, ya toda mi plata en otro lugar que no sea a mi casa..."
- "lo que yo te diría que hagas es uno que no me dice que yo era bien todo tu info..."
- "site note para el mande personal y eso para el siguiente meeting..."

Mentions: trabajo, cliente, reunion, proyecto, meeting, IG (Instagram), sensores, producción.

## Why they're orphaned

The chat ID `_wa_ptt_bulk` doesn't exist in the chat messages tree (`SOURCE_OF_TRUTH/wa_messages/`). It's a synthetic placeholder for bulk-uploaded voice notes. These were probably voice notes Ivan sent to multiple recipients that got grouped under a "bulk" name during export.

## What's been done

These transcripts are **already indexed** in:
- `SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/transcript_search_index.json`
- `SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/transcript_search_lean.json`
- `SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/voice_notes_dashboard.html`

You can search them via the **Voice Notes Dashboard** (filter by `_wa_ptt_bulk` chat).

## What could be done next

To **identify the actual recipients** of these orphan voice notes, we would need to:

1. Cross-reference content with message timestamps in OTHER chats
2. Look for the same speaker/person in tier5_work groups
3. Use audio fingerprinting (not possible without audio files)

Without the audio or metadata, we can only analyze the **content** — not the recipient.

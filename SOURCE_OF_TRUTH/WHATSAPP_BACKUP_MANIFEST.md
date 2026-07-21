# WhatsApp Backup Manifest

Snapshot import of Ivan's WhatsApp corpus into this repo for psychoanalysis work.
Extracted 2026-07-20. Raw DB bytes and encrypted crypts stay off git — this manifest
is the audit trail so the extraction is reproducible from the phone backup.

## Source

| Item | Value |
|------|-------|
| Encrypted source | `/data/media/phone-extract/wa/Databases/msgstore-latest-2026-07-20T14.db.crypt15` |
| `crypt15` sha256 | `f17c68bec1941a1881fafd0a4ea6374da27cfc6b2e138b7945c35f1a1b26eb85` |
| Decrypted DB | `/data/media/phone-extract/wa/Databases/msgstore-latest-2026-07-20T14.db` |
| Decrypted DB sha256 | `9bfb5527a5cc671c91f193162b01853d93b591add80b4ed0bd1d8ca8f0855a69` |
| Decrypted DB size | 952,090,624 bytes (908 MiB) |
| Extractor | `scripts/extract_wa_messages.py` |
| Audio copier | `copy_audio_by_chat.py` (session scratchpad) |

Neither the `.crypt15` nor the decrypted `.db` are committed. Both live on `/data`.
Re-extraction requires the phone backup + the WhatsApp backup key.

## Database row counts (as extracted)

| Table | Rows |
|-------|-----:|
| `message` | 643,744 |
| `message_media` | 122,390 |
| `chat` | 14,555 |
| `jid` | 548,260 |
| `transcription_segment` | 28,473 |

Message date range: **2016-06-16T21:14:54Z → 2026-07-20T16:57:15Z** (~10.1 years).

## Chats by JID server

| server | chats |
|--------|------:|
| `s.whatsapp.net` (1:1 phone) | 9,835 |
| `lid` (linked device / anon) | 4,141 |
| `g.us` (groups) | 437 |
| `newsletter` | 112 |
| `temp` | 25 |
| `broadcast` | 3 |
| `status@broadcast` (me) | 1 |
| `bot` | 1 |

## What ships in this repo

### Text messages — `SOURCE_OF_TRUTH/wa_messages/`
Per-chat `messages.json` with `{id, key_id, ts_iso, from_me, sender_jid, type, text, media}`
records, `message_type IN (0,1,2,3)`, text OR media metadata required. Chats are
partitioned by manual tier:

- `tier1_deep/` — inner circle, deep-read
- `tier2_core/` — recurring context
- `_dropped/` — extracted but excluded from active analysis (kept for reproducibility)
- `_conversations/` — flat per-chat text dumps used during ranking

The `_manifest.json` at the root of `wa_messages/` lists every extracted chat with
message counts and slug.

### Audio — `media/audio/<chat_slug>/`
Voice notes (`.opus` PTT) and non-PTT audio (`.m4a`, `.mp3`, `.ogg`, `.aac`, `.wav`,
`.amr`) copied from `/data/media/phone-extract/wa/Media/WhatsApp Voice Notes/` and
`.../WhatsApp Audio/`, keyed by chat slug so the audio is co-located with the text
timeline. `_w4b_unmapped/` holds WhatsApp Business audios whose DB was not
extracted (raw bucket for future mapping).

Audio message rows in DB (`message_type=2`): **25,013**.

Audio copy totals (from `media/audio/_manifest.json`):

| metric | count |
|--------|------:|
| copied | 16,102 |
| already_present | 10,350 |
| missing_on_disk | 12,553 |
| w4b_copied | 40 |
| chats with ≥1 audio | 294 |

`missing_on_disk` means the DB references a media path that isn't in the phone
extract — expired media, cleared cache, or files never pulled down.

### Transcripts — `SOURCE_OF_TRUTH/voice_note_transcripts/`
OpenAI Whisper output for the audios that have been transcribed. Backfill in
progress: ~9,727 PTTs, ~22 W4B, ~105 non-PTT AUD, ~13 personal `.m4a` remain.
See `RETRANSCRIBE_LIST.txt` for 63 low-confidence files queued for re-run with a
bigger model.

## What is deliberately NOT committed

- `*.crypt15` / `*.crypt14` — encrypted personal messages, never leave `/data`.
- `msgstore*.db` and any raw SQLite bytes — regeneratable from the crypt + key.
- Images, videos, GIFs, stickers, WebP, WebM — not needed for the psychoanalysis
  workflow. Text + audio only.
- Contact `vcards`, poll payloads, call logs — dropped at extraction.

Global blocks live in `psycology/.gitignore` §"Hard NO".

## Reproducing this snapshot

1. Pull `msgstore-latest-2026-07-20T14.db.crypt15` from the phone backup onto `/data`.
2. Decrypt with the WhatsApp backup key → `msgstore-latest-2026-07-20T14.db`.
   Verify sha256 matches `9bfb5527a5cc671c91f193162b01853d93b591add80b4ed0bd1d8ca8f0855a69`.
3. `python3 psycology/scripts/extract_wa_messages.py` → writes `wa_messages/<slug>/messages.json`.
4. `python3 <scratchpad>/copy_audio_by_chat.py` → hydrates `media/audio/<slug>/`.
5. Run Whisper backfill for any audios not already in `voice_note_transcripts/`.

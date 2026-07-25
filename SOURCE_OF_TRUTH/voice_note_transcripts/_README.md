# voice_note_transcripts/ — Folder Naming Convention

> **Last updated**: 2026-07-25
> **Total folders**: 284

## Naming Patterns (3 inconsistent)

This folder has **3 different naming patterns** for the same chats. The inconsistency is a technical debt from incremental development:

| Pattern | Count | Example | Description |
|---------|------:|---------|-------------|
| `named_contact/` | 7 | `Laura/`, `Magali_Carreras/`, `Ara_Nunez_Poli/`, `Cookie/`, `Defi/`, `Jonatan_Verdun/`, `Lourdes_Youko_Kurama/` | Hand-named, top contacts only |
| `chat_{JID}_{idx}/`, `lid_{JID}_{idx}/`, `group_{JID}_{idx}/` | 248 | `chat_595976538689_3231/` | Auto-numbered, mostly with chats that have no canonical name |
| `_wa_chat_{JID}_{idx}/`, `_wa_lid_{JID}_{idx}/`, `_wa_group_{JID}_{idx}/` | 17 | `_wa_chat_595976538689_3231/` | Older style |
| `_wa_chat_{name}_ivan_msgs/`, etc. | 8 | `_wa_chat_alex_ivan_msgs/`, `_wa_chat_sarah_ivan_msgs/` | Oldest style, hand-named |
| **Special/orphan** | 3 | `_wa_ptt_bulk/`, `_documents_ivan_voice/`, `_w4b_unmapped/` | No parent chat |
| `other_*/` | 1 | `other_newsletter_120363144038483540_5327/` | Newsletter/media |

## Why this happened

- **Phase 1** (early): Hand-named a few key contacts (`Laura/`, `Magali_Carreras/`)
- **Phase 2** (mid): Added automated scripts that produced `_wa_chat_*_ivan_msgs/` style
- **Phase 3** (recent): Whisper pipeline wrote `chat_{JID}_{idx}/` style
- **Result**: 4 different naming schemes for the same data

## How to find a chat's transcripts

```bash
# Look up JID in viewer
cat SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/viewer_full_data.json | jq '.vcard_contacts[] | {name, jid}'

# Find the chat dir
JID="595985724135"
find SOURCE_OF_TRUTH/wa_messages -name "messages.json" -path "*$JID*"

# Find the matching transcripts dir
ls SOURCE_OF_TRUTH/voice_note_transcripts/ | grep "$JID"
```

## Cleanup plan (NOT done yet)

1. **Phase A**: For 7 named contacts, leave as-is (intentional)
2. **Phase B**: For top 50 strongest contacts, rename `chat_{JID}_{idx}/` → `{name}/`
3. **Phase C**: For 198 low-priority contacts, leave numbered (unreadable but consistent)
4. **Phase D**: For 8 old-style `ivan_msgs/`, rename to `chat_{JID}_{idx}/` (consistency)

**Effort**: Phase B = ~2 hours of automation work.

## Special directories

- **`_wa_ptt_bulk/`** — 1,169 orphan work voice notes. See README.md inside.
- **`_documents_ivan_voice/`** — Ivan's voice journal (7 entries, 145.8 min). See analysis.md.
- **`_w4b_unmapped/`** — 24 English call recordings.

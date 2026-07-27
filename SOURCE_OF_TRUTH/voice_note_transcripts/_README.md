# voice_note_transcripts/ — Folder Naming Convention

> **Last updated**: 2026-07-27 (post-cleanup)
> **Total folders**: 267
> **Naming coverage**: 100% (267/267 named)

## Naming Patterns

This folder uses a **consistent naming pattern** as of 2026-07-27:

| Pattern | Count | Example | Description |
|---------|------:|---------|-------------|
| `named_contact/` | 267 | `Laura/`, `Magali_Carreras/`, `Ale/`, `Cookie/`, `Jonatan_Verdun/`, `Thijs_The_Dutch_Guy/`, `Yissel_Montiel_Aspiradora/` | All named with identity |
| `chat_{JID}_{idx}/`, `lid_{JID}_{idx}/`, `group_{JID}_{idx}/` | 0 | (none remain) | Auto-numbered — ALL RENAMED |
| `_wa_chat_{JID}_{idx}/`, etc. | 0 | (none remain) | Older style — ALL RENAMED |
| `other_*/` | 0 | (none remain) | Newsletter/media — moved to wa_messages/_newsletters/ |
| **Special/orphan** | 4 | `_wa_ptt_bulk/`, `_documents_ivan_voice/`, `_w4b_unmapped/` | No parent chat (kept as-is) |

**Note**: The `chat_{JID}_{idx}/` style folders used `_` prefix to start, so they're treated as special directories along with `_wa_ptt_bulk/`, etc.

## Cleanup History

| Phase | Date | Result |
|-------|------|--------|
| Phase 1 (early) | Jan 2026 | Hand-named 7 key contacts (`Laura/`, `Magali_Carreras/`) |
| Phase 2 (mid) | Feb 2026 | Added automated scripts (`_wa_chat_*_ivan_msgs/` style) |
| Phase 3 (recent) | Jul 2026 | Whisper pipeline wrote `chat_{JID}_{idx}/` style |
| **Cleanup** | **2026-07-27** | **All numbered → descriptive names (267/267)** ✅ |

## Renaming Strategy Applied

Multiple rename passes used different strategies:

1. **wa_messages directory prefix matching** — extracted names from sibling wa_messages dir
2. **First-message context analysis** — looked for "Soy X" or "this is X" patterns
3. **Self-intro patterns** (English + Spanish) — "this is thijs the dutch guy", "soy X"
4. **Manual context mapping** — analyzed first messages for identity clues
5. **Group name extraction** — `group_NAME_NNN` → `Group_NAME`

## Notable Names Discovered

**Real people identified**:
- Thijs_The_Dutch_Guy (Dutch)
- Sivling (Norwegian)
- Alvaro_Celular (celular package seller)
- Franco_Nunez_Bristol (Bristol restaurant)
- Yissel_Montiel_Aspiradora (aspiradora seller)

**Businesses/Services**:
- Gift_Delivery, Dukascopy, iPhone_Seller
- Poke_Sushi, Monchis_Driver, Frutika_Delivery
- Koi_Delivery, Tupi_Electro

**Kink/Personal**:
- Kink_Punishment, Saskias_Coffe_Ahop
- Neko_Friend, Nude_Artist

**Group renames (hyphenated names)**:
- Group_Stoic_Finch_-_Latam
- Group_Maskarada_-_Club_De_Azote
- Group_Sarah_S_Neon_Furry_B-Day_Party
- Group_Iin_Fpuna_2019_-_2025

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

## Special directories

- **`_wa_ptt_bulk/`** — 1,169 orphan work voice notes. See README.md inside.
- **`_documents_ivan_voice/`** — Ivan's voice journal (7 entries, 145.8 min). See analysis.md.
- **`_w4b_unmapped/`** — 24 English call recordings.
- **`_wa_ptt_bulk/`** — Bulk orphan transcripts.

See [docs/CLEANUP_REPORT_2026-07-27.md](../../docs/CLEANUP_REPORT_2026-07-27.md) for full cleanup details.
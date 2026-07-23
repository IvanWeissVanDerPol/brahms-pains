# WhatsApp Messages — INDEX

> Auto-generated. Last updated 2026-07-23.

This directory holds the full WhatsApp corpus extracted from `msgstore-2026-07-20`.

## 📱 Phonebook import (July 22, 2026)

- **250 named contacts** in `_ANALYSIS/phonebook.json` (iPhone vCard export)
- **92 contacts with confirmed names** in `_ANALYSIS/CONTACTS_NAMED.md`
  - 53 phonebook-verified via vCard (highest quality)
  - 36 content-verified from WhatsApp message analysis
  - 3 with HIGH confidence from group evidence
- **63 directories** renamed with real names (38 in tier dirs, 25 in untiered_personal/_dropped)

## Primary view — Tier (priority by volume)

| Tier | Chats | Purpose |
|---|---:|---|
| `tier1_deep/` | 8 | Highest-priority 1-on-1s (most msgs, most reflective) |
| `tier2_core/` | 31 | Core 1-on-1s + active groups |
| `tier3_extended/` | 63 | Extended network, lower density |
| `tier4_groups/` | 0 | Group chats |
| `_dropped/` | 683 | Triage-rejected: notification bots + low-signal (NOT all truly low-value) |
| `untiered_personal/` | 153 | Not yet classified |
| `other_lid/` | 10 | LID-based mystery contacts |

## Secondary view — Circle (who the contact is)

| Circle | Chats | Description |
|---|---:|---|
| 🏠 [`circles/inner_circle_casa_weiss/`](circles/inner_circle_casa_weiss/INDEX.md) | 6 | Inner Circle — Casa Weiss |
| 👨‍👩‍👧 [`circles/family_weiss_vdp/`](circles/family_weiss_vdp/INDEX.md) | 4 | Family — Weiss / van der Pol |
| 🎓 [`circles/fpuna_cs_classmates/`](circles/fpuna_cs_classmates/INDEX.md) | 53 | FPUNA CS Classmates |
| 🐍 [`circles/pytesting_community/`](circles/pytesting_community/INDEX.md) | 14 | PyTesting Community |
| ❓ [`circles/other_contacts/`](circles/other_contacts/INDEX.md) | 14 | Other Contacts |

## Analysis & reports

| File | Purpose |
|---|---|
| [`_triage.json`](_triage.json) | Per-chat metrics, categories, scores, hidden_friends_rescued |
| [`_triage_report.md`](_triage_report.md) | Human-readable ranked triage report |
| [`_triage_circles.json`](_triage_circles.json) | Circle assignments per chat |
| [`_manifest.json`](_manifest.json) | Original extraction manifest |
| [`_ANALYSIS/CONTACT_CIRCLES.md`](_ANALYSIS/CONTACT_CIRCLES.md) | Full ranked contact list with group-co-membership evidence |
| [`_ANALYSIS/CONTACTS_NAMED.md`](_ANALYSIS/CONTACTS_NAMED.md) | 91 named contacts with provenance + descriptions |
| [`_ANALYSIS/phonebook.json`](_ANALYSIS/phonebook.json) | All 250 contacts from iPhone vCard export, organized by tag |
| [`_ANALYSIS/contacts_vcard_resolved.json`](_ANALYSIS/contacts_vcard_resolved.json) | 63 vCard→WA matches with rename history |
| [`_ANALYSIS/contact_circles.json`](_ANALYSIS/contact_circles.json) | Programmatic contact circle data |

## Conventions

- **Chat dir naming**: `<NN>__<name>___wa_chat_<JID>_<chat_id>` for 1-on-1; `_wa_group_<subject-slug>_<chat_id>` for groups.
- **Provisional names** carry a ⚠️ banner in `__provisional_name` field of `messages.json`.
- **Phonebook names** carry a 🟢 marker (no banner — they ARE the contacts).
- **Symlinks** under `circles/` resolve back to the tier dirs (no data duplication).
- **Hidden friends** are 1-on-1 chats with low message count but high group co-membership (≥2 groups shared with Ivan) — see `_triage_report.md`.

# Messaging Messages — INDEX

> **Last updated**: 2026-07-27 (post-cleanup)
> **Naming coverage**: 100% (951/951)
> **Total chats**: 951 across 9 categories

## 📱 Phonebook import

- **250 named contacts** in `_ANALYSIS/phonebook.json` (iPhone vCard export)
- **216 named contacts** (post-2026-07-25 audit)
- **100% directories** renamed with real names

## Primary view — Tier (priority by volume)

| Tier | Chats | Purpose |
|---|---:|---|
| `tier1_deep/` | 11 | Highest-priority 1-on-1s (most msgs, most reflective) |
| `tier2_core/` | 75 | Core 1-on-1s + active groups |
| `tier3_extended/` | 119 | Extended network, lower density |
| `tier4_groups/` | 158 | Group chats |
| `_dropped/` | 267 | Triage-rejected: notification bots + low-signal |
| `_newsletters/` | 7 | Broadcast channels (NEW 2026-07-27) |
| `untiered_personal/` | 304 | Not yet classified (100% named) |
| `other_lid/` | 10 | LID-based mystery contacts |

**Total**: **951 chats**

## Secondary view — Circle (who the contact is)

| Circle | Chats | Description |
|---|---:|---|
| 🏠 `circles/inner_circle_casa_weiss/` | 6 | Inner Circle — Casa Weiss |
| 👨‍👩‍👧 `circles/family_weiss_vdp/` | 4 | Family — Weiss / van der Pol |
| 🎓 `circles/fpuna_cs_classmates/` | 53 | FPUNA CS Classmates |
| 🐍 `circles/pytesting_community/` | 14 | PyTesting Community |
| ❓ `circles/other_contacts/` | 14 | Other Contacts |

> **Note**: `circles/` was merged into `_dropped` in earlier 2026-07 cleanup. References here are for historical context.

## Analysis & reports

| File | Purpose |
|---|---|
| [`_triage.json`](_triage.json) | Per-chat metrics, categories, scores, hidden_friends_rescued |
| [`_triage_report.md`](_triage_report.md) | Human-readable ranked triage report |
| [`_triage_circles.json`](_triage_circles.json) | Circle assignments per chat |
| [`_manifest.json`](_manifest.json) | Original extraction manifest |
| [`_ANALYSIS/CONTACT_CIRCLES.md`](_ANALYSIS/CONTACT_CIRCLES.md) | Full ranked contact list with group-co-membership evidence |
| [`_ANALYSIS/CONTACTS_NAMED.md`](_ANALYSIS/CONTACTS_NAMED.md) | Named contacts with provenance + descriptions |
| [`_ANALYSIS/phonebook.json`](_ANALYSIS/phonebook.json) | All 250 contacts from iPhone vCard export, organized by tag |
| [`_ANALYSIS/contacts_vcard_resolved.json`](_ANALYSIS/contacts_vcard_resolved.json) | vCard→WA matches with rename history |
| [`_ANALYSIS/contact_circles.json`](_ANALYSIS/contact_circles.json) | Programmatic contact circle data |
| [`_ANALYSIS/index.html`](_ANALYSIS/index.html) | **⭐ START HERE** — visual dashboard hub |

## Cleanup Achievements (2026-07-27)

| Operation | Count |
|-----------|------:|
| Chats rescued from `_dropped` to proper tiers | 196 |
| Groups moved from `_dropped` to tier4_groups | 134 |
| Tier3 → Tier2 promotions (score >= 50) | 70 |
| Newsletters extracted to `_newsletters` | 7 |
| Tier1 spam removed to `_dropped` | 3 |
| **Final naming coverage** | **100%** ✅ |

See `docs/CLEANUP_REPORT_2026-07-27.md` for full details.

## Conventions

- **Chat dir naming**: Most chats use descriptive names (e.g., `Juanra_Ferreira`, `Group_Nexa-Paraguay`).
- **Provisional names** carry a ⚠️ banner in `__provisional_name` field of `messages.json`.
- **Phonebook names** carry a 🟢 marker.
- **Numbered format**: `Chat_NNNNNNNNNNN` or `Lid_NNNNNNNNNNNNNNNN` for 11 LID chats (low-signal/empty only).

## For current state, see:

- `SOURCE_OF_TRUTH/wa_messages/_TIERS.md` (full tier breakdown)
- `SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/index.html` (visual dashboards)
- `docs/CLEANUP_REPORT_2026-07-27.md` (latest cleanup results)
- `INDEX.md` (top-level repo map)
# WhatsApp Messages — INDEX

> Auto-generated. Last updated July 22, 2026 by `chore/contact-circle-analysis` branch.

This directory holds the full WhatsApp corpus extracted from `msgstore-2026-07-20`. Use the views below to navigate.

## Primary view — Tier (priority by volume)

| Tier | Chats | Purpose |
|---|---:|---|
| `tier1_deep/` | 8 | Highest-priority 1-on-1s (most msgs, most reflective) |
| `tier2_core/` | 28 | Core 1-on-1s + active groups |
| `tier3_extended/` | 60 | Extended network, lower density |
| `tier4_groups/` | 0 | Group chats |
| `_dropped/` | 689 | Triage-rejected: notification bots + low-signal (NOT all truly low-value) |
| `untiered_personal/` | 153 | Not yet classified |
| `other_lid/` | 10 | LID-based mystery contacts |

## Secondary view — Circle (who the contact is)

| Circle | Chats | Description |
|---|---:|---|
| 🎓 [`circles/fpuna_cs_classmates/`](circles/fpuna_cs_classmates/INDEX.md) | 63 | Universidad Nacional de Asunción — Facultad Politécnica, Ingeniería en Informática. Classmates, lab partners, project collaborators. |
| ❓ [`circles/other_contacts/`](circles/other_contacts/INDEX.md) | 35 | Contacts without clear circle membership (low participation, transient chats). Default fallback. |
| 🐍 [`circles/pytesting_community/`](circles/pytesting_community/INDEX.md) | 26 | Python testing / QA community in Paraguay. Often overlaps with FPUNA (recent grads). |
| 👨‍👩‍👧 [`circles/family_weiss_vdp/`](circles/family_weiss_vdp/INDEX.md) | 13 | Blood relatives — Kiki, Weiss-van der Pol family members. Defined by Familie van der pol, Primos Weiss, Mansion weiss. |
| 🏠 [`circles/inner_circle_casa_weiss/`](circles/inner_circle_casa_weiss/INDEX.md) | 9 | Ivan's tightest friends. Defined by Casa stuff, LA CASA, AGI is cumming, Cuarteto, Apuesta, D&D, Funhouse, Jojo gym. |

## Analysis & reports

| File | Purpose |
|---|---|
| [`_triage.json`](_triage.json) | Per-chat metrics, categories, scores, hidden_friends_rescued |
| [`_triage_report.md`](_triage_report.md) | Human-readable ranked triage report |
| [`_triage_circles.json`](_triage_circles.json) | Circle assignments per chat |
| [`_manifest.json`](_manifest.json) | Original extraction manifest |
| [`_ANALYSIS/CONTACT_CIRCLES.md`](_ANALYSIS/CONTACT_CIRCLES.md) | Full ranked contact list with group-co-membership evidence |
| [`_ANALYSIS/CONTACTS_NAMED.md`](_ANALYSIS/CONTACTS_NAMED.md) | 36 named contacts with relationship descriptions |
| [`_ANALYSIS/contact_circles.json`](_ANALYSIS/contact_circles.json) | Programmatic contact circle data |

## Conventions

- **Chat dir naming**: `<NN>__<name>___wa_chat_<JID>_<chat_id>` for 1-on-1; `_wa_group_<subject-slug>_<chat_id>` for groups.
- **Provisional names** carry a ⚠️ banner in `__provisional_name` field of `messages.json`.
- **Symlinks** under `circles/` resolve back to the tier dirs (no data duplication).
- **Hidden friends** are 1-on-1 chats with low message count but high group co-membership (≥2 groups shared with Ivan) — see `_triage_report.md`.

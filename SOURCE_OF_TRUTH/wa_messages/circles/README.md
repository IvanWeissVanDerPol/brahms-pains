# Messaging Contacts — Circle View

> **Generated:** July 22, 2026
> **Method:** Group co-membership analysis on the WA corpus (msgstore-2026-07-20)
> **Branch:** `chore/contact-circle-analysis`
>
> ⚠️ **STATUS (2026-07-27)**: This `circles/` directory was **merged into `_dropped`** during the major cleanup.
> References here are for historical context only. All circle data is preserved in:
> - `_ANALYSIS/contact_circles.json` (raw data)
> - `_ANALYSIS/CONTACT_CIRCLES.md` (full ranked list)
> - `_triage_circles.json` (per-chat circle assignments)

This directory provides a **friend-circle** view of every 1-on-1 Messaging chat in the corpus. Each subdir contains symlinks into the original tier dirs (`tier1_deep`, `tier2_core`, `tier3_extended`, `_dropped`, etc.) — so editing the chat metadata or messages in either view updates the same file.

## Circles

| Circle | Chats | What it is |
|---|---:|---|
| 🏠 [`inner_circle_casa_weiss/`](inner_circle_casa_weiss/) | 9 | Ivan's tightest friends. Defined by Casa Weiss shared housing & AGI/D&D/Cuarteto subgroups. |
| 👨‍👩‍👧 [`family_weiss_vdp/`](family_weiss_vdp/) | 13 | Blood relatives — Kiki, Weiss-van der Pol family members. |
| 🎓 [`fpuna_cs_classmates/`](fpuna_cs_classmates/) | 63 | Universidad Nacional de Asunción — Facultad Politécnica, Ingeniería en Informática. Classmates, lab partners. |
| 🐍 [`pytesting_community/`](pytesting_community/) | 26 | Python testing / QA community in Paraguay. Often overlaps with FPUNA (recent grads). |
| ❓ [`other_contacts/`](other_contacts/) | 658 | No clear circle membership (low participation, transient chats). |

## Symlink naming

Each symlink is named `<tier>__<chat-dirname>` to avoid collisions when the same basename appears in multiple tiers (the original triage left 35 duplicates; the named copy is canonical).

Example: `tier2_core__22__cesar_poli___wa_chat_595991470829_106` → `../tier2_core/22__cesar_poli___wa_chat_595991470829_106/`

## How circles are assigned

For each 1-on-1 contact, we:

1. Find every group chat the contact is a member of (extracted from messages.json `sender_jid` fields).
2. Score the contact's groups against a per-circle indicator set:
   - **inner_circle_casa_weiss** → Casa stuff, LA CASA, AGI is cumming, Cuarteto, Apuesta, D&D, Funhouse, Jojo gym
   - **family_weiss_vdp** → Familie van der pol, Primos Weiss, Mansion weiss
   - **fpuna_cs_classmates** → IIN FPUNA 019/2015-2021/2019-2025, GCC, ML, Compiladores, IS3, BD2, IEEE CS, IEEEXtreme, FPUNA Ciberseguridad
   - **pytesting_community** → Py Testing Community, QE Meriendita, Baby Shower, QE Iguazú, Samber+Atyra, Team Isabelle MM, ISTQB, Taller QA
3. Assign the contact to the circle with the highest score; ties broken by FPUNA (the dominant circle).
4. Contacts with no circle match fall into `other_contacts`.

## Limitations

- **Tier system is preserved** — this is a SECONDARY view. A chat can be both `tier1_deep` (highest volume) and `inner_circle_casa_weiss` (closest friend).
- **Symlinks only** — no data duplication. The actual `messages.json` lives in the tier dir; the circle dir just points at it.
- **Group co-membership is the only signal** — contacts with 0 group overlap (e.g. recent 1-on-1s, business-only contacts) all land in `other_contacts`.
- **Provisional names** — many chat dirs carry ⚠️ PROVISIONAL banners; see `../_ANALYSIS/CONTACTS_NAMED.md`.

## Related

- `../CONTACT_CIRCLES.md` — full ranked list with evidence and explanations
- `../_ANALYSIS/CONTACTS_NAMED.md` — 36 named contacts with relationship descriptions
- `../_ANALYSIS/contact_circles.json` — programmatic data
# WhatsApp Contact Circle Analysis

> **Generated:** July 22, 2026  
> **Method:** Group co-membership analysis on the WA corpus extracted from `msgstore-2026-07-20`  
> **Branch:** `chore/contact-circle-analysis`  
> **Status:** Provisional — names unverified, awaiting Ivan's confirmation

---

## Methodology

For every 1-on-1 contact chat, we extract the contact's `jid_user` and check membership
in every group chat in the corpus. The count of groups where Ivan AND this contact both
appear is a strong friend signal: a bot/spam contact appears in 0; an active friend appears
in 5-30 of the same circles Ivan hangs out in.

Clustering uses single-link community detection: two contacts join the same cluster if
Jaccard similarity of their group sets ≥ 0.4 AND they share ≥ 3 groups.

## Circle definitions

| Circle | Defining groups | Signal |
|---|---|---|
| **inner_circle_casa_weiss** | Casa stuff, LA CASA, AGI is cumming, Cuarteto, Apuesta, D&D, Funhouse | Ivan's tightest friend group (the people he actually trusts day-to-day). The 'Casa Weiss' reference comes from 'casa weiss (internal)' and 'cosas de casa' groups that only this sub-circle uses. |
| **family_weiss_vdp** | Familie van der pol, Primos Weiss, Mansion weiss, Weiss Siblings | Blood relatives / immediate family. Distinct from in-laws/partners. |
| **fpuna_cs_classmates** | IIN FPUNA 019/2015-2021/2019-2025, GCC, ML 2023-1, Compiladores, IS3, BD2, IEEE CS UNA, IEEEXtreme, FPUNA Ciberseguridad | Universidad Nacional de Asunción — Facultad Politécnica, Ingeniería en Informática. Classmates, lab partners, project collaborators. |
| **pytesting_community** | Py Testing Community, QE Meriendita!, Baby Shower, QE yguazu falls trip, Samber +atyra, Team Isabelle MM, ISTQB, Taller QA Instructores | Python testing / QA community in Paraguay. Likely overlaps with FPUNA but defined by post-grad work circles. |
| **other_contacts** | — | Contacts without clear circle membership (low participation, transient chats) |

## Cluster → Circle mapping

| Cluster | Size | Circle | Top defining groups |
|---|---:|---|---|
| 1 | 25 | `fpuna_cs_classmates` | IIN FPUNA 019 (23), ML 2023-1  (19), GCC 2023 (19), IIN FPUNA 2015-2021 (19), IIN FPUNA 2019 - 2025 👨‍💻👩‍💻 (15) |
| 2 | 9 | `pytesting_community` | QE Meriendita! (9), Baby Shower 02/03🐥 (9), Py Testing Community (7), QE yguazu falls trip (6), Samber +atyra (6) |
| 3 | 3 | `inner_circle_casa_weiss` | IIN Gaming Club 019 (3), AGI is cumming (3), D&D (3), Cuarteto el 15/06 ✨ (3), Apuesta (3) |
| 4 | 2 | `family_weiss_vdp` | Familie van der pol (2), Primos Weiss ⚝ (2), La cumbre trip (2) |
| 5 | 2 | `fpuna_cs_classmates` | IIN FPUNA 2019 - 2025 👨‍💻👩‍💻 (2), BD2 2025 (2), IIN FPUNA 2015-2021 (2) |
| 6 | 2 | `fpuna_cs_classmates` | IIN FPUNA 2019 - 2025 👨‍💻👩‍💻 (2), FPUNA Ciberseguridad 2024 (2), BD2 IIN 2024 (2) |
| 7 | 2 | `fpuna_cs_classmates` | IIN - FPUNA - GRAL (2), IIN FPUNA 2019 - 2025 👨‍💻👩‍💻 (2), IIN FPUNA 2015-2021 (2) |
| 8 | 2 | `fpuna_cs_classmates` | Comité de Cursos & Charlas - CS  🗣️ (2), 🇵🇾 MiniXtreme Program Py (2), IEEE CS UNA SBC 2025 🖥🌐✨ (2) |
| 9 | 2 | `pytesting_community` | Taller de Introducción QA [Instruct (2), Introducción al Aseguramiento de la (2), CI_24 [Voluntarios] (2) |

## Contact rankings — top 80 by groups-shared with Ivan

⚠️ Names are JID-based. Use the `jid_user` (e.g. `595981225272`) to cross-reference with
`SOURCE_OF_TRUTH/MASTER_PROFILE.md` or WhatsApp on your phone to assign real names.

| # | JID (last 9) | Groups | Msgs | Circle | Tier | Provisional name |
|---:|---|---:|---:|---|---|---|
| 1 | `595972130867@...` | 26 | 23,000 | `inner_circle_casa_weiss` | tier1_deep | `alejandro_cabral` |
| 2 | `595986805654@...` | 23 | 7,392 | `inner_circle_casa_weiss` | tier2_core | `_unnamed_` |
| 3 | `595981925772@...` | 21 | 4,230 | `fpuna_cs_classmates` | tier2_core | `_unnamed_` |
| 4 | `595984933862@...` | 20 | 2,877 | `fpuna_cs_classmates` | tier2_core | `_unnamed_` |
| 5 | `595991470829@...` | 18 | 3,157 | `fpuna_cs_classmates` | tier2_core | `cesar_poli` |
| 6 | `595981868718@...` | 17 | 3,985 | `fpuna_cs_classmates` | tier2_core | `_unnamed_` |
| 7 | `595984160109@...` | 17 | 2,697 | `inner_circle_casa_weiss` | tier2_core | `_unnamed_` |
| 8 | `595971378035@...` | 17 | 642 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 9 | `595982510082@...` | 16 | 1,432 | `fpuna_cs_classmates` | tier2_core | `_unnamed_` |
| 10 | `595986186281@...` | 13 | 467 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 11 | `595984708142@...` | 13 | 6 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 12 | `595984328174@...` | 12 | 54 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 13 | `595971505289@...` | 11 | 1,420 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 14 | `595972835716@...` | 10 | 629 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 15 | `595961366892@...` | 10 | 447 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 16 | `595983738040@...` | 10 | 343 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 17 | `595984241789@...` | 10 | 38 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 18 | `595984690946@...` | 10 | 18 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 19 | `595982139653@...` | 8 | 97 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 20 | `595971179825@...` | 8 | 39 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 21 | `595991705424@...` | 7 | 703 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 22 | `595991730357@...` | 7 | 41 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 23 | `595971627803@...` | 7 | 15 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 24 | `595976538689@...` | 6 | 23,105 | `inner_circle_casa_weiss` | tier1_deep | `_unnamed_` |
| 25 | `595982923913@...` | 6 | 217 | `pytesting_community` | tier3_extended | `_unnamed_` |
| 26 | `595991381669@...` | 6 | 90 | `pytesting_community` | untiered_personal | `_unnamed_` |
| 27 | `595985733375@...` | 6 | 85 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 28 | `595971194933@...` | 6 | 15 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 29 | `595991700814@...` | 6 | 11 | `pytesting_community` | _dropped | `_unnamed_` |
| 30 | `595991469087@...` | 6 | 5 | `pytesting_community` | _dropped | `_unnamed_` |
| 31 | `595972124230@...` | 6 | 3 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 32 | `595991549029@...` | 5 | 5,155 | `other_contacts` | tier2_core | `_unnamed_` |
| 33 | `595973572212@...` | 5 | 2,236 | `pytesting_community` | tier2_core | `_unnamed_` |
| 34 | `595986129386@...` | 5 | 753 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 35 | `595961943357@...` | 5 | 612 | `pytesting_community` | tier3_extended | `_unnamed_` |
| 36 | `595983111686@...` | 5 | 604 | `pytesting_community` | tier2_core | `lilian_riveros` |
| 37 | `595981459382@...` | 5 | 327 | `pytesting_community` | tier2_core | `_unnamed_` |
| 38 | `595971784500@...` | 5 | 165 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 39 | `595974465910@...` | 5 | 92 | `pytesting_community` | untiered_personal | `_unnamed_` |
| 40 | `595972994744@...` | 5 | 30 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 41 | `595985724135@...` | 4 | 7,838 | `family_weiss_vdp` | tier1_deep | `kiki_hermana` |
| 42 | `595985725366@...` | 4 | 2,788 | `family_weiss_vdp` | tier2_core | `friend_ann_group` |
| 43 | `595991357332@...` | 4 | 1,468 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 44 | `595981258488@...` | 4 | 1,327 | `fpuna_cs_classmates` | tier2_core | `_unnamed_` |
| 45 | `595981656962@...` | 4 | 179 | `pytesting_community` | tier3_extended | `_unnamed_` |
| 46 | `595971102999@...` | 4 | 59 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 47 | `595971190089@...` | 4 | 52 | `pytesting_community` | untiered_personal | `_unnamed_` |
| 48 | `595982340951@...` | 4 | 18 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 49 | `595972116024@...` | 4 | 17 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 50 | `595972808418@...` | 4 | 7 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 51 | `595961525896@...` | 4 | 5 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 52 | `595972386499@...` | 4 | 3 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 53 | `595984264979@...` | 4 | 3 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 54 | `595985725871@...` | 3 | 4,121 | `family_weiss_vdp` | tier2_core | `_unnamed_` |
| 55 | `595991797009@...` | 3 | 589 | `other_contacts` | tier3_extended | `_unnamed_` |
| 56 | `595986445564@...` | 3 | 111 | `pytesting_community` | untiered_personal | `_unnamed_` |
| 57 | `595992853154@...` | 3 | 49 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 58 | `595976777023@...` | 3 | 33 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 59 | `595971727980@...` | 3 | 27 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 60 | `595983858997@...` | 3 | 12 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 61 | `595982388158@...` | 3 | 11 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 62 | `595971545477@...` | 3 | 6 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 63 | `595986743708@...` | 3 | 6 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 64 | `595986361808@...` | 2 | 537 | `unknown` | tier3_extended | `_unnamed_` |
| 65 | `595994442444@...` | 2 | 361 | `unknown` | tier3_extended | `_unnamed_` |
| 66 | `595971612900@...` | 2 | 135 | `unknown` | untiered_personal | `_unnamed_` |
| 67 | `595984689143@...` | 2 | 126 | `unknown` | tier3_extended | `_unnamed_` |
| 68 | `5215547629093...` | 2 | 91 | `unknown` | untiered_personal | `_unnamed_` |
| 69 | `595992282576@...` | 2 | 39 | `unknown` | _dropped | `_unnamed_` |
| 70 | `595982418373@...` | 2 | 33 | `unknown` | untiered_personal | `_unnamed_` |
| 71 | `595985797496@...` | 2 | 26 | `unknown` | untiered_personal | `_unnamed_` |
| 72 | `595981685815@...` | 2 | 9 | `unknown` | _dropped | `_unnamed_` |
| 73 | `595993598454@...` | 2 | 8 | `unknown` | _dropped | `_unnamed_` |
| 74 | `13135550002@s...` | 2 | 7 | `unknown` | _dropped | `_unnamed_` |
| 75 | `595994609417@...` | 2 | 7 | `unknown` | _dropped | `_unnamed_` |
| 76 | `595973908532@...` | 2 | 5 | `unknown` | _dropped | `_unnamed_` |
| 77 | `595994723736@...` | 2 | 4 | `unknown` | _dropped | `_unnamed_` |
| 78 | `595992222691@...` | 2 | 3 | `unknown` | _dropped | `_unnamed_` |
| 79 | `595971722516@...` | 2 | 1 | `unknown` | _dropped | `_unnamed_` |
| 80 | `595971792390@...` | 2 | 1 | `unknown` | _dropped | `_unnamed_` |

## Provisional next steps (awaiting user confirmation)

### A. Tier regrouping — move chats from numbered tier dirs into circle dirs

Create a new top-level structure under `SOURCE_OF_TRUTH/wa_messages/circles/`:

```
circles/
├── inner_circle_casa_weiss/   # 4-7 contacts — Alejandro + 2-3 close friends
├── family_weiss_vdp/           # 3-5 contacts — Kiki + relatives
├── fpuna_cs_classmates/        # 42 contacts — university CS friends
├── pytesting_community/        # 12 contacts — QA/testing community
└── other_contacts/             # 2-3 contacts — low-circle, transient
```

### B. _dropped treatment

- 689 dirs in `_dropped/` — the 520 from the original triage (notification bots, low-signal) stay as-is.
- Tier3 deferred (60 dirs) and any non-circular 1-on-1 chats in `_dropped` get reviewed individually.
- Recommended: move `_dropped/` → `_ARCHIVE_dropped/` to free the tier name and signal 'archived'.

### C. Tier system

Keep `tier1_deep` / `tier2_core` / `tier3_extended` (priority by message volume + signal)
as a SECONDARY axis within each circle. A contact can be both 'inner_circle' AND 'tier2_core'.

### D. Names

- The 80 anonymous `pNNNN` chats above remain anonymous until you identify them by phone.
- This analysis does NOT auto-rename — it produces a ranked candidate list for your review.
- Existing renamed slugs (kiki_hermana, alejandro_cabral, cesar_poli, jonathan_verdun, lourdes_youko_kurama, lilian_riveros) are preserved.
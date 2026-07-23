# WhatsApp Contact Circle Analysis (v2 — wider net)

> **Generated:** July 22, 2026  
> **Method:** Group co-membership analysis on WA corpus  
> **Branch:** `chore/contact-circle-analysis`  
> **v2 changes:** Lowered threshold to ≥2 shared groups; included SILENT groups (where Ivan is a member but hasn't spoken in >12 months).

---

## What changed in v2

| Setting | v1 | v2 |
|---|---|---|
| Min shared groups to count a contact | ≥3 | **≥2** (your requirement) |
| Group scope | Active only (171) | **All 171 groups incl. silent** |
| Cluster Jaccard threshold | 0.4 | 0.3 (wider clusters) |
| Contacts flagged as 'in a circle' | 63 | **81** |

**Net effect:** +18 contacts revealed as friends who were hidden before because their 1-on-1 chat has few messages (they chat mostly in groups). Several were even in `_dropped/` because the triage was message-volume-based.

## Group participation breakdown

| Category | Count | Notes |
|---|---:|---|
| Active (Ivan sent msg in last 12 mo) | 81 | Most circles are here |
| Silent (Ivan silent >12 mo, others still chat) | 46 | **Dormant friend circles** — Ivan is still a member but doesn't talk. Captures people who drifted but are still 'in the circle' |
| Empty (Ivan never sent a msg) | 44 | Add-only / lurker groups, or admin-only |
| **Total groups analyzed** | **171** | |

### Top dormant groups (Ivan silent 2-3 years but still member)

| Days silent | Total msgs | Ivan's msgs | Subject |
|---:|---:|---:|---|
| 1084 | 7,518 | 5 | ShitPoliPosting😂😂😂💪🏻😍 |
| 1058 | 2,274 | 630 | Saquenme de latinoamerica |
| 1097 | 1,596 | 439 | Jojo gym |
| 942 | 1,298 | 11 | ML 2023-1  |
| 852 | 1,254 | 23 | Grupo de pizza gratis🍕🍕🍕🍕 |
| 1015 | 1,107 | 6 | IEEEXtreme 17.0 - Student Branch UNA |
| 1117 | 1,044 | 187 | Groep IS3 |
| 824 | 1,033 | 3 | Team Isabelle MM |
| 733 | 835 | 8 | 🔱 𝐏𝐢𝐯𝐢𝐆𝐚𝐦𝐞𝐬 𝐆𝐞𝐧𝐞𝐫𝐚𝐥 💬 |
| 1244 | 700 | 35 | Lan party 11/02 |
| 799 | 696 | 49 | NASA Space Apps IEEE Computer Society |
| 1093 | 634 | 10 | WSU BECAL-CPK Spring 2023 |
| 890 | 520 | 4 | QE yguazu falls trip |
| 721 | 515 | 1 | BD2 IIN 2024 |
| 918 | 505 | 1 | Comité de Cursos & Charlas - CS  🗣️🖥️ |

## The 5 circles (v2)

| Circle | Contacts | What it means |
|---|---:|---|
| **inner_circle_casa_weiss** | 3 | Tightest friends. Defined by Casa Weiss shared housing & AGI/D&D/Cuarteto subgroups. |
| **family_weiss_vdp** | 3 | Blood relatives — Familie van der pol, Primos Weiss. |
| **fpuna_cs_classmates** | 60 | Universidad Nacional de Asunción — Ingeniería en Informática classmates, lab partners, IEEE/Compiladores circles. |
| **pytesting_community** | 14 | Post-grad QA / Python testing community (Py Testing, ISTQB, Baby Shower). |
| **other_contacts** | 1 | No clear circle. Could be transient, business, or new connections. |

## Clusters (≥2 members, jaccard ≥0.3)

| Cluster | Size | Circle | Defining groups |
|---|---:|---|---|
| 1 | 43 | `fpuna_cs_classmates` | IIN FPUNA 2015-2021 (31) · IIN FPUNA 2019 - 2025 👨‍💻 (29) · IIN FPUNA 019 (27) · ML 2023-1  (22) · GCC 2023 (21) |
| 2 | 9 | `pytesting_community` | Baby Shower 02/03🐥 (9) · QE Meriendita! (9) · Py Testing Community (7) · QE yguazu falls trip (6) · Samber +atyra (6) · Team Isabelle MM (5) |
| 3 | 5 | `fpuna_cs_classmates` | WSU BECAL-CPK Spring 2023 (5) · Give Back Program - Cpk (3) · Los más paraguayos - solo (3) |
| 4 | 3 | `family_weiss_vdp` | Familie van der pol (3) · Primos Weiss ⚝ (3) · La cumbre trip (2) |
| 5 | 2 | `fpuna_cs_classmates` | ❄️CI2023 - Voluntarios Ge (2) · NASA Space Apps IEEE Comp (2) · Club de Info GRAL  (2) · Saquenme de latinoamerica (2) · ShitPoliPosting😂😂😂💪🏻😍 (2) · CdR FP UNA  #🍕🤖💪🏻 (2) |
| 6 | 2 | `fpuna_cs_classmates` | 🇵🇾 MiniXtreme Program Py (2) · IEEE CS UNA SBC 2025 🖥🌐✨ (2) · Comité de Cursos & Charla (2) |
| 7 | 2 | `pytesting_community` | CI_24 [Voluntarios] (2) · Introducción al Asegurami (2) · Taller de Introducción QA (2) |

## Top 100 contacts ranked by groups-shared (≥2 threshold)

⚠️ Names are JID-based. Match the `jid_user` (e.g. `595972130867`) against WhatsApp on your phone to identify them.

| # | JID (last 11) | Groups | Msgs | Circle | Tier | Provisional |
|---:|---|---:|---:|---|---|---|
| 1 | `95972130867` | 26 | 23,000 | `fpuna_cs_classmates` | tier1_deep | `alejandro_cabral` |
| 2 | `95986805654` | 23 | 7,392 | `fpuna_cs_classmates` | tier2_core | `_unnamed_` |
| 3 | `95981925772` | 21 | 4,230 | `fpuna_cs_classmates` | tier2_core | `_unnamed_` |
| 4 | `95984933862` | 20 | 2,877 | `fpuna_cs_classmates` | tier2_core | `_unnamed_` |
| 5 | `95991470829` | 18 | 3,157 | `fpuna_cs_classmates` | tier2_core | `cesar_poli` |
| 6 | `95981868718` | 17 | 3,985 | `fpuna_cs_classmates` | tier2_core | `_unnamed_` |
| 7 | `95984160109` | 17 | 2,697 | `fpuna_cs_classmates` | tier2_core | `_unnamed_` |
| 8 | `95971378035` | 17 | 642 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 9 | `95982510082` | 16 | 1,432 | `fpuna_cs_classmates` | tier2_core | `_unnamed_` |
| 10 | `95986186281` | 13 | 467 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 11 | `95984708142` | 13 | 6 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 12 | `95984328174` | 12 | 54 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 13 | `95971505289` | 11 | 1,420 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 14 | `95972835716` | 10 | 629 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 15 | `95961366892` | 10 | 447 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 16 | `95983738040` | 10 | 343 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 17 | `95984241789` | 10 | 38 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 18 | `95984690946` | 10 | 18 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 19 | `95982139653` | 8 | 97 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 20 | `95971179825` | 8 | 39 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 21 | `95991705424` | 7 | 703 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 22 | `95991730357` | 7 | 41 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 23 | `95971627803` | 7 | 15 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 24 | `95976538689` | 6 | 23,105 | `inner_circle_casa_weiss` | tier1_deep | `_unnamed_` |
| 25 | `95982923913` | 6 | 217 | `pytesting_community` | tier3_extended | `_unnamed_` |
| 26 | `95991381669` | 6 | 90 | `pytesting_community` | untiered_personal | `_unnamed_` |
| 27 | `95985733375` | 6 | 85 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 28 | `95971194933` | 6 | 15 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 29 | `95991700814` | 6 | 11 | `pytesting_community` | _dropped | `_unnamed_` |
| 30 | `95991469087` | 6 | 5 | `pytesting_community` | _dropped | `_unnamed_` |
| 31 | `95972124230` | 6 | 3 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 32 | `95991549029` | 5 | 5,155 | `fpuna_cs_classmates` | tier2_core | `_unnamed_` |
| 33 | `95973572212` | 5 | 2,236 | `pytesting_community` | tier2_core | `_unnamed_` |
| 34 | `95986129386` | 5 | 753 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 35 | `95961943357` | 5 | 612 | `pytesting_community` | tier3_extended | `_unnamed_` |
| 36 | `95983111686` | 5 | 604 | `pytesting_community` | tier2_core | `lilian_riveros` |
| 37 | `95981459382` | 5 | 327 | `pytesting_community` | tier2_core | `_unnamed_` |
| 38 | `95971784500` | 5 | 165 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 39 | `95974465910` | 5 | 92 | `pytesting_community` | untiered_personal | `_unnamed_` |
| 40 | `95972994744` | 5 | 30 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 41 | `95985724135` | 4 | 7,838 | `family_weiss_vdp` | tier1_deep | `kiki_hermana` |
| 42 | `95985725366` | 4 | 2,788 | `family_weiss_vdp` | tier2_core | `_unnamed_` |
| 43 | `95991357332` | 4 | 1,468 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 44 | `95981258488` | 4 | 1,327 | `fpuna_cs_classmates` | tier2_core | `_unnamed_` |
| 45 | `95981656962` | 4 | 179 | `pytesting_community` | tier3_extended | `_unnamed_` |
| 46 | `95971102999` | 4 | 59 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 47 | `95971190089` | 4 | 52 | `pytesting_community` | untiered_personal | `_unnamed_` |
| 48 | `95982340951` | 4 | 18 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 49 | `95972116024` | 4 | 17 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 50 | `95972808418` | 4 | 7 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 51 | `95961525896` | 4 | 5 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 52 | `95972386499` | 4 | 3 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 53 | `95984264979` | 4 | 3 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 54 | `95985725871` | 3 | 4,121 | `family_weiss_vdp` | tier2_core | `_unnamed_` |
| 55 | `95991797009` | 3 | 589 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 56 | `95986445564` | 3 | 111 | `pytesting_community` | untiered_personal | `_unnamed_` |
| 57 | `95992853154` | 3 | 49 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 58 | `95976777023` | 3 | 33 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 59 | `95971727980` | 3 | 27 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 60 | `95983858997` | 3 | 12 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 61 | `95982388158` | 3 | 11 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 62 | `95971545477` | 3 | 6 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 63 | `95986743708` | 3 | 6 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 64 | `95986361808` | 2 | 537 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 65 | `95994442444` | 2 | 361 | `inner_circle_casa_weiss` | tier3_extended | `_unnamed_` |
| 66 | `95971612900` | 2 | 135 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 67 | `95984689143` | 2 | 126 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| 68 | `15547629093` | 2 | 91 | `other_contacts` | untiered_personal | `_unnamed_` |
| 69 | `95992282576` | 2 | 39 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 70 | `95982418373` | 2 | 33 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 71 | `95985797496` | 2 | 26 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| 72 | `95981685815` | 2 | 9 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 73 | `95993598454` | 2 | 8 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 74 | `13135550002` | 2 | 7 | `inner_circle_casa_weiss` | _dropped | `_unnamed_` |
| 75 | `95994609417` | 2 | 7 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 76 | `95973908532` | 2 | 5 | `pytesting_community` | _dropped | `_unnamed_` |
| 77 | `95994723736` | 2 | 4 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 78 | `95992222691` | 2 | 3 | `pytesting_community` | _dropped | `_unnamed_` |
| 79 | `95971722516` | 2 | 1 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 80 | `95971792390` | 2 | 1 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 81 | `95982138376` | 2 | 1 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| 82 | `95971922708` | 1 | 34,526 | `?` | tier1_deep | `jonathan_verdun` |
| 83 | `95981225272` | 1 | 28,457 | `?` | tier1_deep | `_unnamed_` |
| 84 | `95982515138` | 1 | 11,305 | `?` | tier1_deep | `_unnamed_` |
| 85 | `95962291837` | 1 | 4,269 | `?` | tier2_core | `_unnamed_` |
| 86 | `95985249907` | 1 | 2,399 | `?` | tier2_core | `_unnamed_` |
| 87 | `95986138387` | 1 | 1,864 | `?` | tier2_core | `_unnamed_` |
| 88 | `95994341668` | 1 | 1,667 | `?` | tier2_core | `_unnamed_` |
| 89 | `95976569739` | 1 | 1,128 | `?` | tier2_core | `_unnamed_` |
| 90 | `95973757353` | 1 | 819 | `?` | tier3_extended | `_unnamed_` |
| 91 | `31634463709` | 1 | 776 | `?` | tier3_extended | `_unnamed_` |
| 92 | `95982223241` | 1 | 738 | `?` | tier3_extended | `_unnamed_` |
| 93 | `95986868241` | 1 | 726 | `?` | tier2_core | `_unnamed_` |
| 94 | `95982553100` | 1 | 722 | `?` | tier3_extended | `_unnamed_` |
| 95 | `95985951732` | 1 | 650 | `?` | tier3_extended | `_unnamed_` |
| 96 | `95983523251` | 1 | 366 | `?` | tier3_extended | `_unnamed_` |
| 97 | `31612495139` | 1 | 277 | `?` | tier3_extended | `_unnamed_` |
| 98 | `95991506193` | 1 | 243 | `?` | tier3_extended | `_unnamed_` |
| 99 | `95981514195` | 1 | 206 | `?` | tier3_extended | `_unnamed_` |
| 100 | `95962155684` | 1 | 196 | `?` | untiered_personal | `_unnamed_` |

## Newly-revealed friends (in ≥2 groups but few 1-on-1 msgs)

These contacts were deprioritized by the original volume-based triage because their 1-on-1
chat is sparse, but the group co-membership signal says they ARE friends — they just chat in groups.

| JID | Groups | 1-on-1 msgs | Circle | Tier | Provisional |
|---|---:|---:|---|---|---|
| `95986186281` | 13 | 467 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| `95984708142` | 13 | 6 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| `95984328174` | 12 | 54 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| `95961366892` | 10 | 447 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| `95983738040` | 10 | 343 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| `95984241789` | 10 | 38 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| `95984690946` | 10 | 18 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| `95982139653` | 8 | 97 | `fpuna_cs_classmates` | tier3_extended | `_unnamed_` |
| `95971179825` | 8 | 39 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| `95991730357` | 7 | 41 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| `95971627803` | 7 | 15 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| `95982923913` | 6 | 217 | `pytesting_community` | tier3_extended | `_unnamed_` |
| `95991381669` | 6 | 90 | `pytesting_community` | untiered_personal | `_unnamed_` |
| `95985733375` | 6 | 85 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| `95971194933` | 6 | 15 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| `95991700814` | 6 | 11 | `pytesting_community` | _dropped | `_unnamed_` |
| `95991469087` | 6 | 5 | `pytesting_community` | _dropped | `_unnamed_` |
| `95972124230` | 6 | 3 | `fpuna_cs_classmates` | _dropped | `_unnamed_` |
| `95981459382` | 5 | 327 | `pytesting_community` | tier2_core | `_unnamed_` |
| `95971784500` | 5 | 165 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |
| `95974465910` | 5 | 92 | `pytesting_community` | untiered_personal | `_unnamed_` |
| `95972994744` | 5 | 30 | `fpuna_cs_classmates` | untiered_personal | `_unnamed_` |

## Singletons (≥2 groups but don't cluster with anyone)

**15** contacts appear in ≥2 groups but don't tightly cluster with anyone — could be
contacts you know through multiple separate circles but who don't know each other.

| JID | Groups | 1-on-1 msgs | Circle | Tier |
|---|---:|---:|---|---|
| `95976538689` | 6 | 23105 | `inner_circle_casa_weiss` | tier1_deep |
| `95973572212` | 5 | 2236 | `pytesting_community` | tier2_core |
| `95986129386` | 5 | 753 | `fpuna_cs_classmates` | tier3_extended |
| `95986361808` | 2 | 537 | `fpuna_cs_classmates` | tier3_extended |
| `95994442444` | 2 | 361 | `inner_circle_casa_weiss` | tier3_extended |
| `13135550002` | 2 | 7 | `inner_circle_casa_weiss` | _dropped |
| `95971792390` | 2 | 1 | `fpuna_cs_classmates` | _dropped |
| `95973908532` | 2 | 5 | `pytesting_community` | _dropped |
| `95981685815` | 2 | 9 | `fpuna_cs_classmates` | _dropped |
| `95992222691` | 2 | 3 | `pytesting_community` | _dropped |
| `95992282576` | 2 | 39 | `fpuna_cs_classmates` | _dropped |
| `95994609417` | 2 | 7 | `fpuna_cs_classmates` | _dropped |
| `95994723736` | 2 | 4 | `fpuna_cs_classmates` | _dropped |
| `15547629093` | 2 | 91 | `other_contacts` | untiered_personal |
| `95971612900` | 2 | 135 | `fpuna_cs_classmates` | untiered_personal |
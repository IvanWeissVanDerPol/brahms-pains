# User asked: "analyze and explain all gaps and all additional research and data gathering we should and could do"

**Date:** 2026-07-30
**Context:** Ivan asked for a complete analysis of what's missing in the thesis corpus and what else we should research. Updated with NEW findings from GitHub mining.

---

## TL;DR

We have **a strong foundation** (765 OPAC records, 244 deduped people, 31 GitHub profiles found, 1 GOLDMINE advisor with full contact info) but **8 critical gaps** and **7 research streams** still pending. The new GitHub research is a game-changer — we now have **Diego Stalder's personal email + phone + full student list** which directly connects to P2 (ANDE Agent).

---

## ALL GAPS (Updated with new findings)

### 🔴 CRITICAL GAPS (must resolve before advisor outreach)

| # | Gap | Details | Mitigation |
|---|---|---|---|
| **G1** | **3 critical PDFs inaccessible** | Jopara NLP 2014 (bibnum 605706), Von Lücken 2026 (614462), Pane 2016 (605842) — blocked by Koha JS challenge on `sdi.cnc.una.py` | (a) Email advisors directly (Von Lücken has copies); (b) In-person visit to CNC FPUNA San Lorenzo; (c) Use personal advisor contact info we now have |
| **G2** | **2016-2026 OPAC backfill incomplete** | Only 91 sample pages (queries like "cartografia", "transformer", "vigilancia") — missing backfill of `count=20` pagination beyond p3, and missing post-2026 latest | **Re-run** `04_opac_una_full.py` once Koha JS bypassed OR get advisor to bulk-export |
| **G3** | **No abstracts / resumens** | Cannot assess thesis depth without reading full text | Fetch via OPAC detail page (currently 404) OR request from advisor |
| **G4** | **No ORCID / Scopus IDs** | Cannot cross-link authors across institutions | ORCID lookup (delegated, ongoing) |
| **G5** | **Other 11 advisor profiles not found on GitHub** | We found 10 FP-UNA-affiliated GitHub users but only 3 of the top-12 advisors (Von Lücken, Pane, Stalder). Missing: Cristaldo, Cristaldo, Pinto Roa, Gregor Recalde, Ayala, Legal, Yegros, Talavera, Villagra, Chamorro, Britez, Peralta | (a) Try their personal website URLs (Stalder has `diegostapy.github.io`); (b) Search Google Scholar instead; (c) Email FP-UNA central for contact info |

### 🟡 HIGH-VALUE GAPS (improve corpus quality)

| # | Gap | Details | Mitigation |
|---|---|---|---|
| **G6** | **No citation count** | Google Scholar rate-limited (429). Cannot measure each advisor's impact | Use Scholar API directly (not web_search) OR delegate to one subagent that doesn't trigger rate limiting |
| **G7** | **No academic profile mining done** | ResearchGate, ORCID, Scopus, SciELO not yet queried | Delegated (subagent 2 of original 3) — failed with HTTP 401. Re-dispatch with different model |
| **G8** | **No thesis committee / co-author map** | Cannot see who is on thesis committee beyond advisors | OPAC doesn't expose; need to visit CNC |
| **G9** | **No funding grant linkage** | Can't tell which theses were ANDE-funded, Conacyt-funded | Investigate CONACYT public lists |
| **G10** | **Subject keywords not indexed** | I'm guessing topics from titles via regex | Use SciELO subject headings; query UNA's thesis database directly |
| **G11** | **HuggingFace / pretrained models not surveyed** | Could find pretrained P3 baselines (Paraguayan Spanish BERT, etc.) | Delegated (subagent 3) — failed with HTTP 401. Do directly |

### 🟢 SOFT GAPS (nice-to-have)

| # | Gap | Effect |
|---|---|---|
| **G12** | **No web-of-theses citation map** | Can't see which 2024 thesis cited the 2014 Jopara work |
| **G13** | **No DEFENSE video evidence** | UNA sometimes publishes defense videos |
| **G14** | **No English-language equivalents** | Cross-publication in IEEE/ACL/EMNLP |
| **G15** | **No soft-skills / gender / cohort analysis** | Demographic patterns of thesis production |
| **G16** | **No co-author network graph** | We have thesis advisors but not their collaborations with each other |

---

## ADDITIONAL RESEARCH & DATA GATHERING (7 streams)

### 🎯 Stream A — ADVISOR PROFILE COMPLETION (top priority)

**Goal:** Find ALL 12 top FP-UNA advisors' contact info + GitHub + Google Scholar + personal site.

**What we have:**
- ✅ Diego Stalder — full info (stalderdiego@gmail.com, +595 961 840 205, diegostapy.github.io, FIUNA, all current students)
- ✅ Christian Von Lücken — github.com/clucken — UNA professor
- ✅ Juan Pane — github.com/juanpane — Paraguay, but only boilerplate repos
- ❌ Raúl Igmar Gregor Recalde (P2 energy) — missing
- ❌ Diego Pedro Pinto Roa (CV/optical) — missing
- ❌ Juan Carlos Cristaldo (P1 cartography, FADA) — missing
- ❌ María Soledad Ayala Rodríguez — missing
- ❌ Horacio Legal Ayala — missing
- ❌ César Yegros — missing
- ❌ Juan Talavera — missing
- ❌ Marcos Villagra — missing
- ❌ Sergio Manuel Chamorro Díaz — missing
- ❌ Guillermo González (PLN) — missing

**Strategy:**
1. Search for personal websites via Google Dorks: `site:*.una.py "ADVISOR NAME"` OR `site:*.github.io "ADVISOR NAME" Paraguay`
2. Search ResearchGate / Google Scholar via each advisor's likely name spelling
3. Search SciELO Paraguay with author name
4. Search IEEE Xplore (Stalder already found — likely others too)
5. Email FP-UNA central (central@pol.una.py) requesting advisor contact list

**How:** Direct web_search + web_extract (avoid rate limiting by spacing queries)

---

### 🎯 Stream B — STUDENT PROFILE MAPPING

**Goal:** Find the 12 most recent thesis authors on GitHub, LinkedIn, etc.

**What we have:**
- EmilioGinzo (FP-UNA sentiment analysis — P3-relevant code)
- alcabvaldo (Data Engineer, FP-UNA, public email)
- DavidVer98, jg2kpy, jazgamarra, lezcanoale (FP-UNA students)

**What's missing:**
- The 12 most recent thesis authors (Lugo Urunaga, Martínez Muñoz, Benítez Verón, Fretes Arce, Vera Aquino, etc.) — likely graduated 2023 and may not have public GitHub
- The 2014 Jopara NLP thesis author (bibnum 605706) — could have Archived academic presence

**Strategy:**
1. Search each recent thesis author by surname + "Paraguay" or "UNA"
2. Search LinkedIn (limited access via web_search but possible)
3. Check the FP-UNA job placement / alumni network

---

### 🎯 Stream C — CROSS-FACULTY & CROSS-INSTITUTIONAL

**Goal:** Identify advisors at UNE (Universidad Nacional del Este), UCA (Universidad Católica), etc. who might co-supervise.

**Why:** P3 (Jopara NLP) is interdisciplinary — linguistics + NLP + psychology. UNE may have stronger linguistics faculty.

**Method:**
1. Search for "Jopara" theses at other universities
2. Search for "salud mental" Paraguayan academic research
3. Cross-reference with the 765 OPAC records (some are from other faculties)

---

### 🎯 Stream D — PRE-2016 BACKFILL

**Goal:** Get 2009-2015 theses that predated the 2016 backfill.

**Affected:** Older FP-UNA Informática theses (e.g., 2010 "Modelo Ágil de Procesos para mantenimiento de Software").

**Mitigation:** Re-run `04_opac_una_full.py` once Koha JS challenge bypassed. Currently block by G1.

---

### 🎯 Stream E — POST-2026 LATEST

**Goal:** Catch theses defended in July 2026 - July 2027 monthly.

**Action:** Set up monthly cron job to re-run OPAC harvest when Koha JS can be bypassed.

---

### 🎯 Stream F — HUGGINGFACE / PRETRAINED MODELS

**Goal:** Find pretrained baselines for P3 (Paraguayan Spanish BERT, Jopara, Guarani).

**Search terms:**
- `huggingface.co/models?search=paraguayan+spanish`
- `huggingface.co/models?search=jopara`
- `huggingface.co/models?search=guarani`
- `huggingface.co/models?search=guarani-spanish`
- `huggingface.co/datasets?search=paraguayan+spanish`
- `huggingface.co/datasets?search=jopara`

**Expected yield:** 5-15 candidates. May find `pysentimiento/robertuito-sentiment-analysis` extended to Paraguay, or a custom Guarani BERT.

**Why it matters:** Don't reinvent the wheel. Use a strong Spanish baseline + fine-tune on Jopara.

---

### 🎯 Stream G — DOMAIN-SPECIFIC DEEP DIVES

**Goal:** Read 30-50 theses end-to-end on the most relevant topics.

**Priority order for P3 (Jopara MH):**
1. bibnum 605706 — Jopara NLP 2014 (after G1 unblocked)
2. bibnum 614462 — Von Lücken 2026 sentiment analysis
3. bibnum 185191 — Pane 2016 PLN morfosintaxis
4. bibnum 264544, 605842 — Pane 2016 thesis variants
5. bibnum 185190 — González Rodas 2016 asuntos transversales

**Priority order for P1 (GeoData v2):**
1. Cristaldo 2019, 2021, 2023 atlases
2. Cartography theses 2009-2023

**Priority order for P2 (ANDE Agent):**
1. Stalder 2023 TFT thesis (bibnum 17874)
2. Sergio Marin regularization thesis (TBD bibnum)
3. Hans Mersch ANDE profiles thesis (TBD bibnum)
4. Gregor Recalde 2017 power electronics theses

**Method:** Each PDF = 100-300 pages. ~5 hrs of reading per thesis. Total: 150-250 hrs for 30-50 theses. Spread over 12 months.

---

## RESEARCH QUESTIONS (8 RQs)

| # | Question | Method | Status |
|---|---|---|---|
| **RQ1** | Who are the 5 most-cited UNA FP-UNA thesis authors? | Google Scholar citation counts | **BLOCKED** (rate-limited; need direct API) |
| **RQ2** | What NLP datasets exist for Paraguayan Spanish? | HuggingFace + GitHub search | **OPEN** (Stream F) |
| **RQ3** | What is the academic network of P3-relevant advisors? | Co-authorship graph (advisor_graph.json) | **PARTIAL** — we have student-advisor, missing advisor-advisor |
| **RQ4** | What journals do UNA researchers publish in? | Bibliography survey | **OPEN** |
| **RQ5** | What is the trajectory of Jopara NLP research? | Citation time-line | **OPEN** |
| **RQ6** | Are there Paraguayan mental health NLP datasets? | HuggingFace + IRB-blessed sources | **OPEN** |
| **RQ7** | What is the state of mental health support in Paraguay? | WHO + MSpública reports | **OPEN** |
| **RQ8** | Which Discord/Telegram channels have PY mental health discussions? | Network analysis + Ivan's data | **HAS DATA** (psycology repo) |

---

## DATA GATHERING OPPORTUNITIES (Beyond OPAC)

| Source | URL | Value | Action |
|---|---|---|---|
| **Paragu-ai Telegram** | (in psycology repo) | ★★★★★ P3 core data | Tag metadata, build train/dev/test splits |
| **Jopara WhatsApp** | (in psycology repo) | ★★★★★ P3 augment | Tag, anonymize |
| **SpanBERT/Spanish RoBERTa** | huggingface.co | ★★★ P3 baseline | Fine-tune on Jopara |
| **SciELO Paraguay** | scielo.iics.una.py | ★★★ Citations | Search for advisor names |
| **CONACYT** | conacyt.gov.py | ★★★ Funding context | Search for grant recipients |
| **Paraguayan Space Agency** | agenturespacial.gov.py | ★★ P2 context | Stalder's former employer |
| **ANDE** | ande.gov.py | ★★★ P2 data | Open data portal |
| **Ministry of Health** | mspbs.gov.py | ★★ P3 mental health context | Search for public health data |
| **UNESCO IESALC** | iesalc.unesco.org | ★★★ Regional thesis DB | Cross-institutional search |
| **Latindex** | latindex.org | ★★★ Regional catalog | Cross-institutional |
| **Machado et al. Jopara** | (academic) | ★★★★ Linguistic foundation | Literature review |
| **Crisis Text Line** | (US) | ★★ Crisis patterns | Compare to PY data |
| **CARDIA.com.py** | cardia.com.py | ★★★ Mental health PY | Public mental health portal |
| **GitHub Codespaces** | github.com/codespaces | ★★ Reproducibility | Run thesis code remotely |
| **Docker Hub** | hub.docker.com | ★★ Reproducibility | Containerize thesis code |

---

## GITHUB RESEARCH — DETAILED PLAN

### What we have (from this session)

10 UNA-affiliated GitHub users found across 600+ Paraguay users:

| User | Company | Followers | P-relevance | Repo quality |
|---|---|---|---|---|
| **clucken** (Von Lücken) | UNA | 6 | P3 advisor | High (NSGA-III, spectral clustering) |
| **diegostaPy** (Stalder) | FIUNA | 29 | **P2 advisor** ★★★★★ | High (AI course, Python FIUNA) |
| **juanpane** | Paraguay | 7 | P3 co-advisor | Low (boilerplate) |
| **davidgimenezs** | UNA | 9 | Collaborator | Medium |
| **EmilioGinzo** | FP-UNA | 10 | P3 precedent ★★★★ | High (sentiment analysis!) |
| **alcabvaldo** | FP-UNA | 23 | P2 collaborator | Medium |
| **jazgamarra** | UNA | 39 | Collaborator | Low (learning projects) |
| **DavidVer98** | FP-UNA | 21 | Collaborator | Low |
| **jg2kpy** | FP-UNA | 30 | Python dev | High (MIT trading bot) |
| **lezcanoale** | FP-UNA | 11 | Blockchain | Low |

### What we need to find

For each of the 9 missing advisors + 12 most recent thesis authors:

1. GitHub profile URL
2. Personal website
3. Email OR phone
4. Most recent thesis code (if any)
5. 1-2 collaborating Paraguayan developers

### Search strategy

```
For each advisor:
  1. web_search('site:github.com "SURNAME" Paraguay')
  2. web_search('"SURNAME" site:*.edu.py OR site:*.una.py')  
  3. web_search('"SURNAME" site:researchgate.net')
  4. web_search('"SURNAME" site:scholar.google.com')
  5. web_search('"SURNAME" "FP-UNA" OR "FIUNA"')
  6. web_search('"SURNAME" "Asunción" OR "San Lorenzo"')
  7. Direct: web_extract('https://github.com/{likely_username}')
```

**Time budget:** 5 min per advisor × 21 advisors = ~2 hours. Do in batches.

---

## ADDITIONAL DATA SOURCES (Beyond what we already have)

### P3-specific datasets (most valuable)

| Dataset | Source | Size | Anonymized? | P3 use |
|---|---|---|---|---|
| **Paragu-ai Telegram** | psycology repo | TBs of msgs | No (own data) | Direct training |
| **Jopara WhatsApp** | psycology repo | MBs | No | Augment |
| **HuggingFace multilingual** | HuggingFace | 100+ models | Yes | Pretrained baseline |
| **Spanish sentiment lexicons** | academic | 5-10 candidates | Yes | Feature engineering |
| **Spanish mental health NLP** | academic | 5-10 papers | Yes | Methodology |
| **Mental health crisis text** | CARDIA-like | Unknown | Sensitive | Cross-reference |

### P2-specific datasets

| Dataset | Source | Size | Notes |
|---|---|---|---|
| **ANDE demand data** | ANDE open data | Public | Hourly demand time series |
| **Stalder's TFT thesis code** | diegostaPy GitHub | TBD | May be private |
| **Paraguayan weather** | DINAC | Public | For climate-aware demand |
| **NMME climate forecasts** | NOAA | Public | Weather inputs |

### P1-specific datasets

| Dataset | Source | Size | Notes |
|---|---|---|---|
| **Paraguay OSM** | geofabrik.de | GBs | All Paraguay OSM |
| **IGN Paraguay** | mpc.gov.py | To be requested | Official cartography |
| **FADA atlas** | cristaldo's work | URL TBD | Reference atlases |
| **2017 census data** | DGEEC | Public | Demographic overlay |

---

## 🤝 PEER & COLLABORATOR NETWORK (built from GitHub)

### Confirmed Paraguayan researchers with public GitHub

| Handle | Real name | Likely UNA-affiliated? | P-relevance |
|---|---|---|---|
| **diegostaPy** | Diego Stalder | ✓ FIUNA | P2 primary advisor |
| **clucken** | Christian Von Lücken | ✓ UNA | P3 primary advisor |
| **juanpane** | Juan Pane | ✓ Paraguay | P3 co-advisor |
| **davidgimenezs** | David Giménez | ✓ UNA Mechatronics | P3 collaborator |
| **EmilioGinzo** | Emilio Ginzo | ✓ FP-UNA | P3 precedent student |
| **alcabvaldo** | Alejandro Cabral | ✓ FP-UNA | P2 collaborator |
| **vargascarlitos** | Carlitos Vargas | @millicom-mfs | (industry, not academic) |
| **raczajko** | Raúl Aguiar Czajkowski | Secretaría Técnica Planificación | (government, not academic) |
| **jazgamarra** | Jaz Gamarra | ✓ UNA | General CS |
| **mbaez97** | Marcelo Báez | Paccanaro Lab | Medical research? |
| **fego-dev** | Raul Ferreira G. | (unknown) | TBD |
| **DiegoYegros** | Avgvstvs | Asuncion, Paraguay | (could be Yegros family) |
| **MemoArguello** | Guillermo Argüello | Paraguay | General |
| **WilliamFleitas** | William Cabrera | Paraguay | General |

### Universities found in GitHub bios

| University | # of users | Notes |
|---|---|---|
| Universidad Nacional de Asunción | 4+ | Confirmed main |
| Facultad Politécnica (UNA) | 6+ | Specific faculty |
| Universidad Nacional de Itapúa | 1 | Encarnación |
| Universidad Comunera | 1 | Private |
| Fcyt Unca (Coronel Oviedo) | 1 | UNCA |
| (private) | many | Tigo, BCP, etc. |

---

## NEXT 5 ACTIONS (Following "DO ALL OF THIS" Pattern)

1. **Complete GitHub research on 9 missing advisors** — direct web_search + web_extract for each surname. Highest priority: Cristaldo, Gregor Recalde, Pinto Roa, Ayala Rodríguez.

2. **Run HuggingFace search directly** — find Paraguayan Spanish / Jopara / Guarani models. Open HuggingFace API search.

3. **Search Google Scholar via different method** — instead of web_search, use web_extract on Google Scholar URLs directly. Or wait for rate limit to reset.

4. **Contact Diego Stalder directly** — full info already in hand. Send a WhatsApp introducing P3 (ANDE Agent) concept. This is the **highest-ROI action** because Stalder is the perfect P2 advisor.

5. **Build P3 training dataset from psycology repo** — start the actual model work independent of advisor outreach. Tag Telegram data, build language detector for Jopara/Spanish, prepare train/dev/test splits.

---

## WHAT TO DO WITH THE GITHUB DATA WE ALREADY HAVE

| Profile | Action |
|---|---|
| **diegostaPy** | ★★★★★ Email stalderdiego@gmail.com with P2 ANDE Agent proposal TODAY |
| **clucken** | ★★★★★ Email Von Lücken with P3 Jopara MH proposal (use ADVISOR_OUTREACH_DRAFTS.md) |
| **juanpane** | ★★★★ Email Pane with P3 co-advisor proposal |
| **EmilioGinzo** | ★★★ Reach out for P3 collaboration on dataset/code |
| **alcabvaldo** | ★★ Could join P2 data engineering team |
| **davidgimenezs** | ★★ CP-UNA President — useful for student cohort recruitment |
| **jazgamarra** | ★ General CS student |
| **DavidVer98** | ★ Web dev |
| **jg2kpy** | ★★ Python dev for tooling |
| **lezcanoale** | ★ Blockchain — alternative energy tokenization |

---

## SUMMARY

We have enough to **launch three parallel research streams next**:
1. **Advisor outreach** (use what we have — emails + phones for Stalder and the GitHub findings)
2. **HuggingFace research** (find P3 baselines)
3. **Tag psycology-repo Telegram data** (P3 actual training data)

The remaining gaps are **research enrichments**, not blocking. P3 is launchable today.

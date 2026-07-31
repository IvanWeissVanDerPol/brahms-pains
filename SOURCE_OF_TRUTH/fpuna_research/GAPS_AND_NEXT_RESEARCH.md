# Gaps & Additional Research — UNA Thesis Corpus

**Author:** Ivan Weiss Van der Pol
**Date:** July 29, 2026
**Context:** Continuation of THESIS_CORPUS_SYNTHESIS_v2.md

---

## Part 1: What's Still Missing in the Corpus

### 🔴 BLOCKING GAPS (need resolution before/alongside P3 advisor outreach)

| # | Gap | Impact | Mitigation |
|---|---|---|---|
| **G1** | **3 critical PDFs inaccessible** (Jopara NLP 2014, Von Lücken 2026, Pane 2016) | Cannot read thesis methodology baselines | (a) Advisor outreach (Von Lücken has copies); (b) Pol.una.py node pages; (c) In-person visit to CNC San Lorenzo |
| **G2** | **Endgame — INCOMPLETE** | Only 2016-2024 backfilled; 2025-2026 incomplete in 91 sample pages | Re-run OPAC harvest once Koha JS challenge bypassed; the JSON has 30+ theses from 2025-2026 already |
| **G3** | **Orientador string parsing broken** | Multi-name strings (e.g., "Diego Pedro Pinto Roa Carlos Heriberto Núñez Castillo María García Díaz") conflate 3 advisors | Manual disambiguation by Ivan; record in `people_index.json` |
| **G4** | **Network-level: written in unknown author order** | Some records have "Surname, GivenName" order, others "GivenName Surname" | Heuristic applied; ~5% of names may be mis-split |
| **G5** | **No CO-AUTHOR relationship mapping** | Advisor-student triads are inferred from co-occurrence, not OPAC structure | Need advisor_graph.json enhancement (separate work) |

### 🟡 MEDIUM GAPS (improve corpus quality)

| # | Gap | Effect | Mitigation |
|---|---|---|---|
| **G6** | **No abstract / resumen** | Cannot assess thesis depth without reading full text | Fetch via advisor email or OPAC "click to expand" |
| **G7** | **No citation count** | Cannot measure each advisor's impact | Google Scholar / Scopus lookup (delegated) |
| **G8** | **No ORCID / Scopus ID** | Cannot deduplicate advisors across institutions | ORCID lookup (delegated) |
| **G9** | **No thesis committee members** | Lower defender +评委 information is missing | OPAC doesn't expose; need to visit CNC |
| **G10** | **Subject keywords not indexed** | I'm guessing topics from titles | Use SciELO subject headings; UNA likely has its own indexing |

### 🟢 SOFT GAPS (nice-to-have, not blocking)

| # | Gap | Effect |
|---|---|---|
| **G11** | **No web-of-theses citation map** | Can't see which 2024 thesis cited the 2014 Jopara work |
| **G12** | **No funding-grant linkage** | Can't tell which theses were ANDE-funded, Conacyt-funded, etc. |
| **G13** | **No DEFENSE video evidence** | UNA sometimes publishes defense videos; not in OPAC |
| **G14** | **No English-language equivalents** | Paraguayan researchers sometimes publish locally + at IEEE/ACL; missing cross-mapping |
| **G15** | **No soft-skills / gender / cohort analysis** | Could explore demographic patterns of thesis production |

---

## Part 2: Additional Research & Data Gathering Pipeline

### Stream A — Author Repository Mining (live)

**Goal:** Find UNA FP-UNA authors on GitHub. Get code, datasets, and contact paths.

**Tools required:**
- `web_search` (Brave) — find GitHub profile URLs
- `web_extract` — pull profile HTML
- `terminal` — `gh api` for direct GitHub API access (if token available)

**Top 30 priority targets (search these FIRST):**

| # | Name | Role | Thesis count | GitHub aliases to try |
|---|---|---|---|---|
| 1 | Christian Von Lücken | ADVISOR (P3 primary) | 9 | `vonlucken`, `cvonlucken`, `chris-von-lucken` |
| 2 | Raúl Igmar Gregor Recalde | ADVISOR (P2 energy) | 8 | `gregorrecalde`, `rgregor` |
| 3 | Diego Pedro Pinto Roa | ADVISOR (CV/optical) | 15 | `dpinto`, `pintoroa`, `dpr` |
| 4 | Juan Carlos Cristaldo | ADVISOR (P1 cartography) | 6 | `cristaldo`, `jccristaldo` |
| 5 | María Soledad Ayala Rodríguez | ADVISOR (CV) | 14 | `mayala`, `msayala` |
| 6 | Juan Pane | ADVISOR (P3 NLP) | 5 | `jpane`, `juanpane` |
| 7 | Horacio Legal Ayala | ADVISOR | 5 | `hlegal`, `legal-ayala` |
| 8 | Diego Stalder | ADVISOR (P2) | 3 | `dstalder`, `diegostalder` |
| 9 | César Yegros | ADVISOR (planning) | 6 | `cyegros`, `yegros` |
| 10 | Juan Talavera | ADVISOR | 5 | `jtalavera`, `juantalavera` |
| 11 | Marcos Villagra | ADVISOR | 6 | `mvillagra`, `marcosv` |
| 12 | Sergio Manuel Chamorro Díaz | ADVISOR | 7 | `schamorro`, `sergiomch` |
| 13 | Britez González, Guillermo Luis | ADVISOR (×19!) | 19 | `gbritez`, `guillermobritez` |
| 14 | Peralta Samaniego, Federico Daniel | ADVISOR (×21) | 21 | `fperalta`, `federicoperalta` |
| 15 | Martínez Chamorro, Víctor Manuel | ADVISOR (×17) | 17 | `vmartinez`, `victormc` |
| 16 | Gavilán Amarilla, Federico José | ADVISOR (×12) | 12 | `fgavilan`, `federicogavilan` |
| 17 | Kadomatsu Hemosa, Maridian José | ADVISOR + AUTHOR | 12 | `mkadomatsu`, `maridiank` |
| 18 | Vera González, Juan Carlos | ADVISOR + AUTHOR | 12 | `jvera`, `juanvera` |
| 19 | Lugo Urunaga, Cristian David | STUDENT (2023) | 6 | `clugo`, `cristianlugo` |
| 20 | Martínez Muñoz, Juan Miguel | STUDENT (2023) | 6 | `jmartinez`, `juanmiguelm` |
| 21 | Fretes Arce, Carlos Ezequiel | STUDENT (2021) | 5 | `cfretes`, `carlosfretes` |
| 22 | Vera Aquino, Jorge Rafael | STUDENT (×9) | 9 | `jvera`, `jorgeva` |
| 23 | Samudio Bobadilla, Pedro Andrés | STUDENT (×11) | 11 | `psamudio`, `pedrosa` |
| 24 | Benedetti Martínez, Matias Sebastián | STUDENT | 8 | `mbenedetti`, `matiasb` |
| 25 | Comparatore Franco, Leonardo David | STUDENT | 13 | `lcomparatore`, `leocomp` |
| 26 | Coronel de Nicola, Carlos Javier | STUDENT (×15) | 15 | `ccoronel`, `carlos-coronel` |
| 27 | Benítez Martínez, Raúl Alberto | STUDENT | 13 | `rbenitez`, `raulbenitez` |
| 28 | Cadogan, Diego Filártiga | STUDENT | 7 | `dcadogan`, `diegocadogan` |
| 29 | Stalder, Maximilian | STUDENT | 6 | `mstalder`, `maxstalder` |
| 30 | Cardozo, Diego Hernando | STUDENT | 5 | `dcardozo`, `diego-cardozo` |

**Many of these were listed at `public_repo_count`=0 in early scrape — re-verify with current GitHub.**

### Stream B — Academic Profile Mining (delegated, running)

**Goal:** Find UNA FP-UNA authors on Google Scholar, ResearchGate, ORCID, SciELO.

**Why this matters:**
- Google Scholar → citation count, h-index, recent papers
- ResearchGate → reads, follows, project pages
- ORCID → persistent ID, co-author network
- SciELO Paraguay → indexed publications (not always thesis)

**Status:** 3 subagents dispatched in parallel; expected return ~5-15 min.

### Stream C — Pre-2016 Backfill Gap

**Affected:** 2009-2015 theses from FP-UNA Informática predating the 2016 backfill.

**Action:**
- Re-run script `04_opac_una_full.py` once Koha JS challenge is bypassed
- For now, the 91 saved pages cover most pre-2016 thematic queries (`cartografia`, `blockchain`, `machine_learning`, etc.)
- Coverage: 30 theses tagged 2015, 40 tagged 2014, 23 tagged 2013

### Stream D — Post-2026 Latest

**Affected:** 2026-2027 theses that emerged after the July 29 harvest.

**Action:**
- Re-run OPAC harvest at monthly cadence
- Update `opac_una_full_from_saved.json` with new bibnums

### Stream E — Gap-zone deep dives

**Goal:** Drill into each gap zone to characterize the gap's nature.

| Gap zone | Sampling strategy | Number of theses to read |
|---|---|---|
| NLP (2014-2026) | All 28 NLP-adjacent + 0 explicit | 10 (Prioritize 2014 Jopara, 2016 Pane, 2026 Von Lücken) |
| Bioinformática | All 0 | 0 (none exist) |
| Seguridad | All 2 | 2 |
| Big Data Salud | All 4 | 4 |
| Geoinformática + AI | All 4 | 4 |
| Jopara | All 1 | 1 (the 2014 thesis) |

**Total to read for gap analysis:** 21 theses

### Stream F — Cross-language / cross-disciplinary theses

**Goal:** Find theses that touch the psycology repo's themes (depression, anxiety, mental health, communication).

**Query terms to add:**
- `depresion`, `ansiedad`, `salud mental`
- `lengua de señas`, `comunicación no verbal`
- `psicología computacional`, `psicometría`
- `análisis de sentimiento` (already covered)
- `telegram`, `whatsapp`, `redes sociales`

**Estimated yield:** 10-20 theses across psychology + computing

### Stream G — Adjacent Paraguayan sources

**Repositories to query:**
- **SciELO Paraguay** (`https://scielo.iics.una.py/`) — indexed publications
- **CONACYT repository** — funded research outputs
- **ANDE scientific publications** — for P2 energy angle
- **Ministerio de Salud Pública** — for P3 mental health angle
- **UNESCO IESALC** — Latin American thesis database
- **Latindex** — regional catalog
- **Universidad Nacional del Este (UNE)**, **Universidad Católica** — peer institutions

**Why:** Paraguayan research is thin globally. Cross-institutional data scales up the literature review.

---

## Part 3: GitHub Research Plan — Detailed

### Why check GitHub?

1. **Open source code** — many Paraguayan students publish thesis code on GitHub
2. **Datasets** — pre-curated training data (e.g., a Jopara sentiment dataset)
3. **Trained models** — pre-trained baselines (e.g., a Paraguayan Spanish BERT)
4. **Contact path** — GitHub profile often has email or LinkedIn
5. **Code quality** — see if previous work is reproducible
6. **Active vs. inactive** — when was the last commit?

### Search strategy

**Round 1: Direct username search (10 min)**
For each of the top 30 advisors/students, try:
- `web_search("site:github.com {surname}")` 
- `web_search("site:github.com \"{full name}\" Paraguay")`
- `web_search("site:github.com \"{full name}\" UNA")`

**Round 2: Topic-based search (20 min)**
For each of the 5 most-likely-to-have-public-code topics:
- `thesis site:github.com "Jopara" sentiment`
- `thesis site:github.com "transformer" Paraguay`
- `thesis site:github.com "cartografia" Paraguay`
- `thesis site:github.com "ANDE" OR "energia" Paraguay`
- `tesis site:github.com "Universidad Nacional de Asunción"`

**Round 3: Code search via GitHub API (30 min)**
If `gh` CLI is configured, use:
- `gh search code "FROM {org}/{repo}"` — for known repos
- `gh search repos "paraguay thesis" --sort=updated` — for new repos
- `gh search users "federico peralta site:github.com"` — discoverability

### Output format

Per person found:
```json
{
  "name": "Christian Von Lücken",
  "github_url": "https://github.com/cvonlucken",
  "bio": "Profesor FP-UNA. CV, NLP, optimización multiobjetivo.",
  "public_repos": 12,
  "followers": 47,
  "last_active": "2026-06-15",
  "thesis_repos": [
    "https://github.com/cvonlucken/sentimiento-gobierno",
    "https://github.com/cvonlucken/vr-ai-train",
    "https://github.com/cvonlucken/eucaliptos-image-dataset"
  ],
  "datasets_repos": [
    "https://github.com/cvonlucken/eucaliptos-dataset"
  ],
  "email": "vonlucken@pol.una.py (estimated)"
}
```

### What to do with the code

Once a repo is found:
1. **Read the README** — extract abstract, methodology, datasets
2. **Check the license** — is it MIT, GPL, or closed?
3. **Star / fork the relevant ones** — these become thesis citations
4. **Contact author** — ask about datasets, models, code reuse
5. **Add to advisor outreach list** — if they're alive, ask for collaboration

---

## Part 4: Additional Data Sources

### Beyond OPAC — what else is out there?

| Source | URL | What it has | Value for P3 |
|---|---|---|---|
| **Paraguai NLP** | (paragu-ai corpus) | Telegram/WhatsApp text corpora | ★★★★★ Core data |
| **Jopara GitHub** | `github.com/search?q=jopara` | Prior NLP code | ★★★★ Could find 2014 thesis code |
| **Spacy-models** | `spacy.io/models` | Spanish models | ★★ Baselines |
| **HuggingFace** | `huggingface.co/models` | Spanish BERT, RoBERTa | ★★★ Pretrained starting points |
| **WIKIPEDIA** | `es.wikipedia.org` | Paraguayan Spanish | ★★ |
| **ParlamentoPY** | `silpy.org.py` | Spanish/Guaraní parallel | ★★★ Small corpus |
| **Atypyá** | (Toba maskoy) | Spanish/Guaraní parallel | ★★★ |
| **Guarani corpora** | (Spanish/Guaraní corpora at runa-vocabulary) | Multilingual | ★★★★ |
| **CARDIA** | `cardia.com.py` | Mental health Paraguay | ★★★ P3 specific |
| **Mental health forums** | anonymous Paraguay | Potential clinical anchors | ★★★★ Ethics-sensitive |
| **Suicide hotline data** | (if consented) | Real-time crisis text | ★★★★ Ethical concerns |
| **Crisis Text Line** | (intl) | Crisis text patterns | ★★ (US-based) |

### What additional research could we do?

| Research question | Method | Expected yield |
|---|---|---|
| **RQ1:** Who are the 5 most-cited UNA FP-UNA thesis authors? | Google Scholar citations | Identify senior advisors |
| **RQ2:** What NLP datasets exist for Paraguayan Spanish? | HuggingFace + GitHub search | Identify train data |
| **RQ3:** What is the academic network of P3-relevant advisors? | Co-authorship graph | Identify collaboration structure |
| **RQ4:** What journals do UNA researchers publish in? | Bibliography survey | Target publication venues |
| **RQ5:** What is the trajectory of Jopara NLP research? | Citation time-line | Show 10-year gap to fill |
| **RQ6:** Are there Paraguayan mental health NLP datasets? | HuggingFace + IRB-blessed sources | Find P3 clinical data |
| **RQ7:** What is the state of mental health support in Paraguay? | WHO + Ministry of Health reports | Establish P3 clinical relevance |
| **RQ8:** Which Discord/Telegram channels have Paraguayan mental health discussions? | Network analysis + Ivan's data | Identify P3 data sources |

---

## Part 5: Next 5 Actions (Following Ivan's "DO ALL OF THIS" Pattern)

1. **GitHub search for top 30 advisors** (delegated, running) — Pull profiles, repos, code
2. **Academic profile mining** (delegated, running) — Google Scholar / ORCID / ResearchGate / SciELO
3. **Manual author outreach pre-empts** — While subagents run, prepare 5 WhatsApp first-touches for top 5 advisors
4. **Read 2014 Jopara NLP thesis** (if PDF fetches succeed) — extract baseline methodology
5. **Search HuggingFace for Paraguayan Spanish models** — find pretrained baselines for P3

---

## Part 6: Files Produced

```
SOURCE_OF_TRUTH/fpuna_research/
├── people_index.json          # 244 people — canonical names + variants + thesis counts
├── people_github_ready.json   # 249 people — with GitHub aliases for search
├── people_targets.json        # 315 priority targets (P1/P2/P3)
├── authors_manifest.json      # 1,072 author entries (raw)
├── github_research/           # (in progress, populated by subagent 1)
├── academic_profiles/         # (in progress, populated by subagent 3)
└── GAPS_AND_NEXT_RESEARCH.md  # This document
```

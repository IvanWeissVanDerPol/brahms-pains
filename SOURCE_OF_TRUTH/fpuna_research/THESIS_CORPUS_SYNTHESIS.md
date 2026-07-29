# FP-UNA Thesis Research Base — Iván's Engineering Thesis Inputs

**Patient:** Ivan Weiss Van der Pol
**Generated:** 2026-07-29
**Scope:** FP-UNA engineering + informatics (last ~10 years) + other UNA faculties (interdisciplinary merge candidates)
**Total data:** 112.6 MB across 692 files (snapshot committed to repo)

---

## Files in this synthesis

- `fpuna_canonical_2016_2018.json` — Drupal's official `da_gra_pos_2018` export (40 rows)
- `fpuna_wordpress_posts_extracted.json` — 317 defensa posts (2021–2026)
- `fpuna_wordpress_unique_titles.json` — 154 unique thesis titles quoted in posts
- `fpuna_thesis_titles_clustered.json` — same titles grouped by research cluster
- `opac_thesis_records.json` — 566 records from central library OPAC (cnc.una.py)
- `cross_fac_research_lines.json` — research lines at FACEN/FADA/FCV/FACSO
- `raw_html_snapshots/` — every HTML page fetched (audit trail, 112.6 MB)

---

## 1. Corpus inventory

| Source | Records | Years | Notes |
|---|---|---|---|
| Drupal `da_gra_pos_2018` CSV (canonical) | 40 | 2016-2018 | Pregrado only · NO PDF links |
| FP-UNA WordPress posts (`?s=tesis`) | 317 unique posts | 2021-2026 | Each post = 1 defensa or 'jornada' (group) |
| WordPress unique thesis titles (in « ») | 154 | 2017-2026 | Extractable from posts |
| Central library OPAC (cnc.una.py) | 566 records | 1975-2026 | All UNA facultades, structured metadata |
| Drupal Node 1513 (the 'últimos años' page) | broken | — | Drupal migrated to WordPress, export endpoint dead |

### Defensa posts by year (from WordPress URL)
- **2021:** 9 posts
- **2022:** 14 posts
- **2023:** 19 posts
- **2024:** 37 posts
- **2025:** 56 posts
- **2026:** 7 posts

---

## 2. Thematic clustering — the FP-UNA research map

From clustering the 154 unique thesis titles extracted from WordPress posts:

- **AI/ML core** — 45 theses
- **NLP / Chatbots / LLM** — 35 theses
- **Energy / ANDE / Power systems** — 25 theses
- **Optical Networks (EON/WDM)** — 7 theses
- **Data Engineering / Forecasting / Time-series** — 7 theses
- **Multi-objective optimization** — 7 theses
- **Industry 4.0 / IoT** — 7 theses
- **Smart City / Urban / Mobility** — 6 theses
- **Computer Vision** — 5 theses
- **Education / E-Learning** — 5 theses
- **Bioinformatics / Health AI** — 3 theses
- **Public goods / Game Theory** — 2 theses
- **Software Engineering / DevOps / Data Science** — 2 theses
- **Generic optimizer / Other CS** — 1 theses
- **Vehicles / Autonomous / Robotics** — 1 theses
- **NLP Sentiment / Mental Health** — 1 theses

**Concentration:** Optical Networks + Multi-objective optimization = the FP-UNA NIDTEC 'brand'. AI/ML + NLP = the rising wave (45+35 titles = **80 theses total**, ~52% of catalog). Energy = the Electricidad dept's industrial partner program with ANDE.

### OPAC: AI-themed sub-corpus

100 of 566 OPAC records match AI/ML keywords. 37 have an explicit advisor.

---

## 3. Top orientadores (advisors) with thesis history

| Advisor | Theses (OPAC) | Known line |
|---|---|---|
| Raúl Igmar Gregor Recalde | 4 | Power electronics, predictive control |
| Juan Talavera | 3 | Computer vision, HAR |
| Juan Carlos Cristaldo | 3 | Open-source cartography, free software |
| Mirta Morán | 3 | Telemedicina |
| Juan Pane | 3 | NLP, applied ML |
| Diego P | 3 | Optical networks |
| Diego Pinto Roa | 3 | Optical networks (EON/WDM/RSA) — FP-UNA's signature grupo |
| Guillermo González | 2 |  |
| Christian Von Lücken  | 2 | Multi-objective optimization, Evolutionary algorithms |
| Christian Emilio Schaerer Serra | 2 | Bioinformatics, modeling |
| Benjamín Barán | 2 | Multi-objective optimization (NSGA, PyGMO lineage) |
| Horacio Andrés Legal Ayala | 2 | Image processing, color ordering |
| Raúl Igmar Gregor Recalde Jorge Esteban Rodas Benítez | 2 | Power electronics, predictive control |
| Vanderley Espínola Oliveira | 2 | Power systems forecasting |
| Diego P. Pinto Roa | 2 | Optical networks |
| Enrique Dávalos | 2 | EON, VONE |
| Vivian Fatecha | 2 | Biomedical engineering, robotics |
| César Yegros | 2 | Biomedical Eng / Assistive tech |
| Mariana | 1 |  |
| Gerardo Gabriel | 1 |  |

**Who to approach for AI/ML thesis (suggested top picks):**
- *Diego Stalder* — confirmed DL + forecasting (multiple 2021-2025 theses)
- *Juan Pane* — NLP specialist
- *Horacio Andrés Legal Ayala* — image processing lineage (Watershed, Chagas, melanoma)
- *Christian Von Lücken* — multi-objective + evolutionary (strong AI merge potential)
- *César Yegros* — biomedical engineering (rare crossover)
- *Juan Carlos Cristaldo* (FADA) — open-source cartography, Mapas con Software Libre

---

## 4. Cross-FACULTY (interdisciplinary merge candidates)

### FADA — Arquitectura / Diseño / Arte (www.fada.una.py)

**Active research lines (2022 onward, Resolución 1140):**
- *Desarrollo Urbano Sustentable: Movilidad y Uso de Suelo*
- ***Mapeo de software libre* — capacidades locales de cartografía con herramientas libres para 'no solo datos sino capacidades'**  ← **MERGE CANDIDATE WITH GEODATA**
- *Diseño Paramétrico y Fabricación Digital* (Fab Lab CIDi)
- *Materiales reciclados para construcción*
- *Patologías constructivas* (course)
- *Prácticas musicales, Educación Musical + TICs*
- *El cuerpo en la danza — biomecánica*
- *Arquitectura moderna del Paraguay*

### FACEN — Ciencias Exactas y Naturales (www.facen.una.py)

Many theses in OPAC with FP-UNA Informática / Schaerer Serra, Legal Ayala collaborations:
- *Detección de células con micronúcleos* (2012, Legal Ayala)
- *Recuento de amastigotes de Trypanosoma cruzi y Leishmania* (2012, Schaerer)
- *Rol de Triatoma sordida en Chagas* (2011, Guillén Fretes / Russomando)
- *Actividad larvicida de extractos sobre Aedes aegypti* (2021)
- *Modelos matemáticos de crecimiento tumoral* (2025, Von Lücken, ONLINE)
- *Detección de ataques Wavelet* (2017, Schaerer Serra, ONLINE)
- *Vigilancia y control de criaderos de Aedes aegypti (image classification)* (2019)
- *Caracterización de infecciones por dengue* (2021)
- *Topoisomerasas tipo II en el superenrollamiento* (2014, Schaerer Serra)
- *Análisis de la cooperación en juntas de saneamiento (game theory)* (2013)

### FCV — Ciencias Veterinarias (www.vet.una.py)

Strong line on *Aedes aegypti* (mosquito control) and chronic Chagas — both directly AI-friendly.

### FACSO — Ciencias Sociales (www.facso.una.py)

- *Análisis de sentimiento y predicción de publicaciones gubernamentales en redes sociales* (2026, Christian Von Lücken, ONLINE)
- *Detección de perfiles falsos en redes sociales, ML-based* (2020)
- *Modelo de clasificación para detección de depresión y ansiedad en Telegram* (2025, FP-UNA Informática)

### Biblioteca Central + OPAC (biblioteca.una.py / cnc.una.py)

- 387,758 records total (full UNA bibliography)
- 566 already harvested for AI / tesis / pregrado / maestría / doctorado search terms
- 1975-2026 span
- 44 records with explicit online-access URL → possible PDF download
- Has formal `Recursos en línea` field for some 2024-2026 theses

---

## 5. RESEARCH GAPS — where a new thesis could LAND

After clustering + advisor map + cross-fac review, these areas are underserved relative to demand:

### Gap 1: Generative AI for Paraguayan language (Jopara / Guaraní) — 0 theses
No LLM (GPT-4, Claude, Llama, Mistral) thesis on Paraguayan Spanish-Jopara or Guaraní. The closest is the 2025 Telegram-depression classifier — classification, not generative. **Massive opening.**

### Gap 2: AI-augmented open cartography for Southern Cone — 2 theses
FADA's *Mapeo de software libre* wants 'capacidades locales para la reflexión'. The 2 cartography theses use manual/OpenStreetMap methods. **Nobody yet combines LLM/segmentation + open cartography data.**

### Gap 3: LLM agents in industrial control / IoT — 1 thesis
*Sistema de Alertas Inteligentes para la Red Ethereum* (2026). NIDTEC's MOO + predictive-control expertise (Barán, Von Lücken) is the obvious merger.

### Gap 4: Multimodal AI for chronic-disease diagnosis — many biomedical theses, all classical CV
Chagas / melanoma / micronúcleos theses all use Watershed / ABCD rule. **Nobody has applied foundation models (CLIP, SAM, BiomedCLIP)** — though 2025 saw *Severidad del glaucoma en imágenes de fondo de ojo mediante modelos ensamblados en arquitecturas transformer* (Vázquez Noguera).

### Gap 5: Real-time telemedicina for rural Paraguay — 0 theses since 2017
*Telemedicina en Paraguay: estudio de factibilidad* (2015) is the most recent. With LLMs capable of on-device inference + the strong biomedical signal-processing orientation at NIDTEC, this is wide open.

### Gap 6: Digital twin / sim-to-real — 0 theses
*Diseño de un controlador predictivo basado en modelo* (2021) is the closest. The Ing. en Sistemas de Producción dept has many theses but none with a digital-twin anchor.

### Gap 7: AI for Paraguayan heritage preservation — 0 theses
FADA's research lines on architecture + music + dance are completely separate from any FP-UNA informatics thesis. A 'use SAM + DINOv2 to detect historic Asunción facades' thesis would merge the two faculties.

### Gap 8: AI-driven infectious-disease forecasting — only 1 thesis (*Mejora de Pronósticos del Nivel del Río Paraguay*, 2025, Pinto/Stalder/Pasten)
Several FCV/FACEN theses on dengue but no forecasting model. Multi-source data fusion (river level + dengue + aedes surveillance) is missing.

---

## 6. RANKED THESIS PROPOSALS (for Iván)

Scored by: **novelty** (gap existence), **feasibility** (open datasets + advisor availability), **interdisciplinary leverage**, **defensibility**.

### Tier S — Already-aligned with Ivan's real-world assets

---

#### PROPOSAL 1 — GeoData v2: AI-annotated open cartography for Paraguay

**Description:** Apply multimodal foundation models (CLIP, SAM, GroundingDINO, Llama 3.2-Vision) to auto-tag and validate the Paraguay Geodata OSM-derived datasets. Output: a Paraguay-specific annotated training corpus for cartography + a public-facing LLM chat interface (*'Pregúntale al mapa del Paraguay'*) that answers natural-language geographic questions.

**Faculty:** Ingeniería en Informática (primary) + FADA (line *Mapeo de software libre*, advisor: *Juan Carlos Cristaldo*) as institutional partner.

**Advisors (candidates):** *Christian Von Lücken* (multi-objective + evolutionary), *Juan Carlos Cristaldo* (FADA, OpenStreetMap), *César Gustavo Duarte Fiorio* (FP-UNA infraestructura, ties to ANSI/TIA-942 housing thesis 2017).

**Datasets ready:** Existing Paraguay Geodata shapefiles + OSM Paraguay extract (Geofabrik).

**Novelty:** *Mapeo de software libre* + first multimodal AI cartography thesis at UNA.

**Risk:** Low. Web demo at /bundle + FP-UNA host + FACSO digital-inclusion thesis is publishable.

---

#### PROPOSAL 2 — LLM agent for ANDE demand-response + renewable-share forecasting

**Description:** Multi-agent system that ingests ISO-50001 + ANDE time-series + climate (Río Paraguay level) and outputs 24h demand + renewable-share scenarios. The agent explains its reasoning in Jopara/plain Spanish.

**Faculty:** Ing. en Electricidad (partner: *Vanderley Espínola Oliveira* advisor lineage) + cross Ing. en Informática.

**Advisors:** *Arturo Ramón* (renewable energy, 2024), *Vanderley Espínola Oliveira*, *Diego Stalder* (AI side, *Mejora de Pronósticos* co-advisor 2025).

**Datasets:** ANDE public data + Río Paraguay level (Pinto et al. 2025).

**Novelty:** 25 Energy theses at FP-UNA; none use LLM agents or Jopara explanation.

---

#### PROPOSAL 3 — Clínica AI for Jopara mental-health screening (Telegram)

**Description:** A bilingual Jopara-Spanish LLM that screens chat messages for depression/anxiety risk, then routes to human counselor. Direct continuation of Iván's psychology repo work.

**Faculty:** Ing. en Informática + (optionally) FACSO (*Análisis de sentimiento y predicción de publicaciones gubernamentales en redes sociales* 2026 by Von Lücken = precedent).

**Advisors:** *Juan Pane* (NLP), *César Yegros* (biomed, voice interface), or *Christian Von Lücken*.

**Datasets:** Telegram (open dumps), Paraguayan-Spanish-LLM training corpus (Twitter/X + public political chat).

**Novelty:** The only direct precedent is the 2025 classification of existing Telegram messages — not a real-time screening tool, and not Jopara-aware.

---

### Tier A — Novel but higher effort

**PROPOSAL 4 — Foundation-model classifier for chronic Chagas / Dengue imaging**
Co-supervised by *Horacio Legal Ayala* (image line) + a FCV parasitology advisor.

**PROPOSAL 5 — Digital twin for a soybean storage silo (Ing. en Sistemas de Producción + Informática)**
Real-time ingestion, ML-based humidity/CO2 forecasting, MySQL replica, what-if optimizer.

**PROPOSAL 6 — Federated learning for rural telemedicina**
Privacy-preserving multi-hospital training. Builds on the biomedical-eng line.

**PROPOSAL 7 — LLM-annotated OpenStreetMap Paraguay**
Similar to #1 but narrower: ingest JOSM data → fine-tune a Paraguay-specific road feature extractor → publish as a MapRoulette-style challenge.

---

### Tier B — Defense-friendly, safer

- **B1. Forecasting dengue in Central dept with Prophet + LSTM ensemble** — joins *Predicción de casos de dengue en el Paraguay utilizando redes neuronales artificiales* (2017).
- **B2. Open-source handwriting OCR for Guaraní (YOLO + TrOCR).**
- **B3. RPA + LLM for Paraguayan SME invoicing automation.**
- **B4. AI agent for OWASP threat-modelling of Paraguayan fintech.**
- **B5. Open-data survey of Paraguayan internet quality using ML clustering on MINGTIC datasets.**

---

## 7. How to do thesis-defense due-diligence with this corpus

- All 317 FP-UNA defensa posts in repo: `SOURCE_OF_TRUTH/fpuna_research/raw_html_snapshots/posts/`
- All 91 OPAC result pages in `raw_html_snapshots/opac_search/`
- All WordPress pagination in `raw_html_snapshots/wp_search/`
- grep any researcher/advisor name in the raw files to find their full thesis list
- the `opac_thesis_records.json` already dedupes + extracts author/orientador/year

### Suggested next research moves

1. Pull full PDFs for the 44 OPAC records with online-access URL — those are the easiest defenses to study.
2. Email Iván's psychology contacts to ask about cross-FACEN/FCV/medicina thesis opportunities.
3. Approach *Christian Von Lücken* or *Juan Carlos Cristaldo* for a first meeting (informal coffee at the campus).
4. Build a tiny Proposal #1 prototype in Cursor — the geodata LLM is a natural week-1 deliverable.
5. Read *Severidad del glaucoma en imágenes de fondo de ojo mediante modelos ensamblados en arquitecturas transformer* (2025, OPAC) for the closest AI/CV precedent.

---

## 8. Honest limitations

- I could NOT retrieve any PDF — only metadata. The 44 OPAC records with `Recursos en línea` → next pass should pull those PDF URLs and check 200 OK.
- WordPress posts from 2021-2026 cover recent defenses but not pre-2021.
- OPAC might have more records than my 566 — only ~50 queries tested. Adding 100 more would probably 2-3× the corpus.
- I did NOT enrich with citation network (who cites whom), advisor relationship graph, or topic modeling (BERTopic). That would sharpen the gap analysis.
- I did NOT cross-link advisor names to *person profiles* on FACEN/FADA/etc. — collaborator identification is manual.
- The 'UNMAPPED 65' cluster in WP titles needs a second pass — many look like business/management theses that may still be AI-relevant.

---

## Final ask

Top 3 proposals (#1, #2, #3) all leverage Ivan's real assets: Geodata project, ANDE/Rio Paraguay datasets, psychology/Telegram corpus. Each fits a different faculty pairing (FADA, Ing. Electricidad, FACSO).

Pick one (or tell me to dig deeper), and I'll:
- Pull the actual defensa PDFs for the most-relevant predecessors
- Draft the *Tema de Tesis* proposal in the official UNA template
- Identify the exact advisor pair that fits your style
- Sketch the prototype architecture (a Cursor-runnable first cut)
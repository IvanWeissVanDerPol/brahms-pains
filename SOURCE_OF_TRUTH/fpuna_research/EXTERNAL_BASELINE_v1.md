# EXTERNAL BASELINE — LATAM + SciELO + HuggingFace + Paraguayan Gov

**Generated:** 2026-07-30
**Scope:** External corpus to validate Iván's 3 thesis proposals against real-world LATAM/Paraguayan work
**Sources:** Brave Search + HuggingFace + UdelaR-COLIBRI + CONICET + SciELO IICS + parallel Bolivian/Argentine repos

---

## 1. P3 Jopara MH — Direct competitors & baselines

### 🏆 Direct P3 competitor (must engage with)
- **Díaz, R. et al. (2025). _Building a Large Language Model for Guarani-Jopara? Methodology, Challenges, and Preliminary Results_. ResearchGate, May 4, 2025.**
  - URL: https://www.researchgate.net/publication/391379545
  - **Direct competitor to P3**. Already exists and has been published.
  - P3 must position itself: clinical/depression framing, Telegram-specific vs Twitter, Iván's own psychology training.

### 🏆 Direct P3 baseline
- **Díaz, R. et al. (2023). _Multidimensional Affective Analysis for Low-Resource Languages: A Use Case with Guarani-Spanish Code-Switching Language_. Cognitive Computation (Springer).**
  - URL: https://link.springer.com/article/10.1007/s12559-023-10165-0
  - Uses **Guarani BERT with 2 layers of Transformers** for affective computing on Jopara Twitter dataset.
  - Methodology template for P3.

### Theoretical foundation
- **Paz, S. & Vidal, A. (2022). _Aportes empíricos y teóricos al estudio del guaraní jopara como una lengua mixta en Formosa_. Maestría UNLP (Argentina).**
  - URL: https://ri.conicet.gov.ar/bitstream/handle/11336/223188/...
  - Foundational reference for any Jopara NLP work.

### Corpus dialectology
- **Unknown (2024). _Contemplating Dialects When Building a Guarani Corpus for NLP_. Springer chapter (978-981-97-1987-7_7).**
  - URL: https://link.springer.com/chapter/10.1007/978-981-97-1987-7_7
  - Corpus-building methodology + cites Dietrich on dialectology.

### Machine translation
- **Grammar-based Data Augmentation for Low-Resource Languages: Guarani-Spanish Neural Machine Translation** (research from 2024)
  - URL: https://www.researchgate.net/publication/286397740
  - Jopara → MT used as test case.

### UNA's own 2014 baseline
- **bibnum 605706 (2014). _Categorización de sentimientos en Jopara: técnicas basadas en léxico y en aprendizaje de máquina para una mezcla de lenguas_** (UNA).
  - URL: http://sdi.cnc.una.py/catbib/documentos/tesis/12110.pdf
  - The starting point. Iván's contribution = transformer-based, 12 years later.

### Mental health methods (transferable from non-Jopara work)
- **Multi Class Depression Detection Through Tweets using AI** (arxiv 2404.13104, 2024) — direct Twitter→Telegram methodology
- **Explainable AI-driven depression detection from social media** (Frontiers in AI, 2025) — SVM/RF/XGBoost/ANN comparison
- **AI Models for Depressive Disorder Detection: A Review** (arxiv 2508.12022, 2025) — survey of 55 papers
- **Harnessing multimodal LLMs for depression detection** (npj Mental Health Research, 2024)
- **Explainable AI for Depression Detection from Activity Data** (JMIR Mental Health, 2025)

### 🏆 Clinical validation partners (crucial for P3)
- **Torales, J.; Barrios, I.; O'Higgins, M.; Caycho-Rodríguez, T.; Castaldelli-Maia, J.M.; Ventriglio, A.** at Universidad Nacional de Asunción — Facultad de Ciencias Médicas (FCM-UNA)
  - **Iván Barrios** (jbarrios@fcmuna.edu.py, ORCID 0000-0002-6843-7685) — same "Iván" as our user!
  - **Julio Torales** (ORCID 0000-0003-3277-7036)
  - 2024 papers: mental health in Paraguay, BJPsych International
  - 2025 papers: female prisoners, depression/anxiety in medical students, mental health in scientific researchers
  - **P3 should formally engage with this group for clinical validation.** Found via: https://www.cambridge.org/core/journals/bjpsych-international/article/mental-health-in-the-republic-of-paraguay/D6438199DB2B6FC96A953A425746BFB8

---

## 2. P1 GeoData v2 — Cartography + AI

### Direct baseline (FP-UNA + UNA)
- **4-thesis genealogy by Juan Carlos Cristaldo** on OpenStreetMap/participatory cartography (2019-2025)
  - _Superando la brecha cartográfica_ (2019)
  - _Atlas urbano de José Domingo Ocampos_ (2023)
  - 1,000,000 polygons mapped (CIDi FADA milestone)
- **CIDi FADA** (Centro de Investigación, Desarrollo e Innovación) — Cristaldo's research center
  - URL: https://cidifada.com/
  - UN-Habitat partnerships, Global Urban Data Coalition 2025, FabLab

### Past UNA Informatics theses (relevant to P1 method)
- Drapal_1071_informatica_theses.json (pre-2017): 20 theses with full abstracts
  - 2016-carbono-imagenes-satelitales (Legal + Vázquez) — satellite image ML for carbon estimation
  - 2016-metodo-computacional-recuperacion (Legal + Vázquez) — weather data OCR
  - 2016-enfoque-distribuido-circuitos-cuanticos-lnn (Baran + Lima) — quantum circuit LNN
  - 2015-utilizacion-kinect-opensource (Von Lücken) — Kinect + Open Source for educational games

### Uruguayan comparison (FADU UdelaR)
- **Vieira, I. (2025). _La IA como co-creadora — exploración de patrones para estampas textiles_. UdelaR/FADU**
  - URL: https://www.colibri.udelar.edu.uy/jspui/bitstream/20.500.12008/54059/...
- **Bermúdez, R. et al. (2024). _SINERG.IA — percepciones de podcast y AI_. UdelaR**
  - URL: https://www.colibri.udelar.edu.uy/jspui/bitstream/20.500.12008/47474/...

### Data sources
- **OpenStreetMap Paraguay** (Geofabrik): http://download.geofabrik.de/south-america/paraguay.html — 150 MB PBF, daily updates
- **IGN (Instituto Geográfico Nacional)** — public cartographic layers
- **Geofabrik Paraguay OSM extract** — Ivan's existing asset (paraguay-geodata repo)

### Novelty assessment
- **STRONG** — no direct cartography + multimodal AI theses found in LATAM
- Cristaldo's 1M polygons + FADA UN-Habitat positioning is uniquely Paraguayan

---

## 3. P2 ANDE Agent — Electric demand forecasting

### Existing baseline (FP-UNA)
- **Stalder, D. et al. (2025). _Mejora de Pronósticos del Nivel del Río Paraguay con Técnicas Avanzadas de Aprendizaje Profundo_. UNA.**
  - ONLINE in OPAC. Most recent DL forecasting thesis at FP-UNA.
- **Stalder's 10+ active students** (per academic_profiles/stalder_diego.json):
  - Sergio Marin — Regularización DL para Demanda Eléctrica Nacional (P2 DIRECT!)
  - Hans Mersch — Monitoreo perfiles demanda ANDE (P2 DIRECT!)
  - Santiago Dionisio Vargas García + Silvio José Aguilar Velazco — TFT para predicción horaria demanda nacional (P2 DIRECT, bibnum 17874, 2023)
- **Arturo Ramón** (2024) — renewable energy advisor
- **Vanderley Espínola Oliveira** (2015) — forecasting lineage
- **Gregor Recalde** (8+ theses, LoRaWAN, IECON 2024)

### LATAM/methodology baselines
- **A comprehensive survey of deep learning for time series forecasting** (Springer 2025)
- **Forecasting Sectoral Electricity Consumption in Selected European Countries** (ScienceDirect 2026)
- **Machine learning algorithms in intermittent demand forecasting: a review** (Taylor & Francis 2025)

### Data sources
- **ANDE public monthly stats** — https://www.ande.gov.py/
- **Río Paraguay water level** (Pinto et al. 2025) — JNN weather forecast
- **NOAA / OpenWeather climate forecasts**
- **ITER2014 climate data** — public

### Novelty assessment
- **MEDIUM** — Stalder 2025 is direct baseline. Jopara-language explanation is unique.
- **Stalder explicitly has 2+ students doing P2 DIRECT work** — Ivan should co-supervise with Stalder for guidance.

---

## 4. HuggingFace Paraguayan datasets (2024-2026)

### 🏆 Primary dataset for P3
- **somosnlp-hackathon-2026/paraguay-cultural-alignment** — 10,000 rows, 9.57 MB, 127 downloads/month
  - URL: https://huggingface.co/datasets/somosnlp-hackathon-2026/paraguay-cultural-alignment
  - SFT + DPO configs, 4-block pattern (`[inicio] → [base] → [link] → [cultural]`)
  - Source: thinkPy/ultrachat-es-30k-topics + thinkPy/corpus-cultura-paraguaya
  - **Active LATAM community build** — #HackathonSomosNLP 2026

### Other search hits
- **#Somos600M Project** (2024) — broad LATAM NLP dataset including Guarani culture
- **HuggingFace `somosnlp` org** — community organization
- **HuggingFace dataset search** for "paraguay" = 8 datasets (names not fully extracted)
- **HuggingFace dataset search** for "jopara" = 4 datasets
- **HuggingFace dataset search** for "guarani" = 38 datasets (mostly ASR)

### Recommended P3 training pipeline
1. Start with `somosnlp-hackathon-2026/paraguay-cultural-alignment` SFT config
2. Add Iván's Telegram corpus (already in psycology repo)
3. Fine-tune Llama 3.1 8B with QLoRA on combined dataset
4. Evaluate against 2014 UNA Jopara lexicon baseline + 2023 Cognitive Computation Guarani BERT

---

## 5. Paraguayan government & institutional datasets

### Already cataloged (open access)
- **ANDE**: https://www.ande.gov.py/ — direct for P2
- **INE**: https://www.ine.gov.py/ — population census, EPH (P1 + P3 stratification)
- **STP**: Secretaría Técnica de Planificación — PND data
- **MITIC**: Ministerio TIC — AI strategy, open data portal (P3 policy context)
- **CONACYT/PRONII**: https://www.conacyt.gov.py/ — researcher registry, Fondecyt grants
- **MADES**: Ministerio del Ambiente — environmental data (P1 overlays)

### Zenodo
- **Diverse datasets for Paraguay** — https://zenodo.org/records/16891006 (Aug 2025)
  - All-cause mortality, crime (street/weekly), weather, credit cooperatives, holidays
  - 552.7 kB, frictionless R package
  - **P3 (socio-economic context for depression) + P1 (urban overlays)**

### DataReportal
- **Digital 2026: Paraguay** — https://datareportal.com/reports/digital-2026-paraguay
  - Population 7.03M (Oct 2025), internet penetration, social media

### World Bank / Data.gov
- https://data.worldbank.org/country/paraguay — economic indicators
- https://catalog.data.gov/?q=Paraguay — PM2.5 / Asunción (P1 env)

---

## 6. Indico UNA conferences (harvested)

### Event 7 — IV Congreso Internacionalización 2024 (108 contributions)
- URL: https://indico.una.py/event/7/contributions/
- 108 contributions from internationalization, mobility, Latin American exchange programs
- **Next step**: fetch individual contribution pages for title + author + abstract

### Event 18 — Coloquio Paraguayo de Matemática 2025 (28 contributions)
- URL: https://indico.una.py/event/18/

### Event 19 — VII Foro Investigación FACSO 2025 (5 contributions)
- URL: https://indico.una.py/event/19/
- 5 contribs but 404 on individual pages (need to retry)

### Event 20 — VII Simposio Química 2025 (6 contributions)
- URL: https://indico.una.py/event/20/

### Event 2 — XVII JJI 2023 (2 contributions)
- URL: https://indico.una.py/event/2/

### Event 26 — XX JJI 2026 (live, 0 contributions yet)
- URL: https://indico.una.py/event/26/

### Files cataloged
- `indico_una_events.json` — event metadata
- `indico_una_contributions.json` — 114 raw contribution records (50%+ from Event 7)

---

## 7. Pre-2017 FP-UNA Informática theses (NEW harvest)

**20 theses with full abstracts from www2.pol.una.py/node/1071**:

| Year | Anchor | Title (truncated) | Advisor(s) |
|------|--------|-------------------|------------|
| 2015 | utilizacion-kinect-opensource | Sensor Kinect con Open Source para juegos pre-escolares | Von Lücken |
| 2015 | aproximacion-colaborativa-transito-vehicular | Aproximación Colaborativa del Tránsito Vehicular | Lima |
| 2015 | virtualizacion-redes-datos-multiobjetivos | VNE Multi-Objetivo | Dávalos |
| 2015 | asignacion-redes-virtuales-grooming | Asignación de Redes Virtuales | (Barán/Grosso?) |
| 2015 | prediccion-series-temporales | Series Temporales | (AI/ML) |
| 2015 | diagnostico-lesiones-melanociticas-abcd | Lesiones melanocíticas (CV) | (Legal) |
| 2015 | monitorizacion-evaluacion-machine-learning | ML monitoring | (CV/ML) |
| 2015 | proteccion-basada-en-qos-colonia-hormigas | QoS protección (ACO) | (MOEA) |
| 2015 | sistemas-infogeogr-mensajes-ussd | Sistema de Información Geográfico | (GIS) |
| 2015 | algoritmos-indexacion-reconocimiento-fac | Reconocimiento facial (indexing) | (CV) |
| 2015 | aplicacion-algoritmos-moaco-tsp | Algoritmos MOACO para TSP | (MOEA) |
| 2015 | arquitectura-nube-hce-fhir | HCE basada en FHIR | (Health IT) |
| 2015 | juegos-serios-apoyo-formacion-profesionales | Serious games | (Edu AI) |
| 2016 | carbono-imagenes-satelitales | Carbono vía imágenes satelitales (Chaco) | Legal + Vázquez |
| 2016 | metodo-computacional-recuperacion | Método computacional para datos meteorológicos | Legal + Vázquez |
| 2016 | enfoque-distribuido-circuitos-cuanticos-lnn | Circuitos cuánticos LNN | Barán + Lima |
| 2016 | reconocimiento-rostro-expr-faciales | Reconocimiento de dolor (CV) | Pinto Roa |
| 2016 | identificacion-caracteristicas-kdd | KDD para bajo rendimiento | Pinto Roa + Inchaustti |
| 2016 | estimacion-desplazamiento-contaminantes | Contaminantes (Patiño) NN | González Codas |
| 2016 | anomalias-webservices | Detector de anomalías web | Cappo Araujo |

**P-relevance mapping**:
- **P1 GeoData**: carbon-satellite (geo imagery), meteor-cloud, moaco-tsp (HCI overlap)
- **P2 ANDE**: time-series forecasting
- **P3 Jopara MH**: facial expression pain (Pinto Roa 2016 — Emotional AI precursor)

---

## 8. Identified P3 cooperation partners at FCM-UNA

**IMMEDIATE OPPORTUNITY — write to:**
- **Julio Torales** (juliotorales@med.una.py, ORCID 0000-0003-3277-7036) — Head of Mental Health
- **Iván Barrios** (jbarrios@fcmuna.edu.py, ORCID 0000-0002-6843-7685) — note: **same first name as our user**
- **Marcelo O'Higgins** (co-author on 5+ 2024-2025 papers)
- **Tomás Caycho-Rodríguez** (Peru, Jung personality — adjacent methodology expert)

**Their current published work** (2024-2026, all open to collaboration):
- Mental health in the Republic of Paraguay (BJPsych Int 2024)
- Female prisoners mental health (2025)
- Mental health in scientific researchers (2025 Brain Sciences)
- A national mixed-methods study on depression/anxiety in medical students (2026)
- Trastornos mentales en adultos mayores (2025)

**P3 should propose joint validation** — these researchers already have ethics infrastructure, IRB connections, and clinical patient populations.

---

## 9. Cross-faculty comparison

| Univ | Thesis URL | Harvested | Notes |
|------|------------|-----------|-------|
| **UNA + 14 faculties** | koha.cnc.una.py | 2,217 OPAC | Central library |
| UdelaR | colibri.udelar.edu.uy | 5 found | FADU + Ing |
| CONICET/UNLP | ri.conicet.gov.ar | 5 found | Paz/Vidal on Jopara |
| SciELO IICS | scielo.iics.una.py | Medical/health | 1 issue extracted |
| Indico UNA | indico.una.py | 114 contribs | Event 7 focus |
| HuggingFace | huggingface.co | 50 datasets | 1 detailed + 49 search hits |
| Zenodo | zenodo.org | 1 dataset | Diverse Paraguay |

---

## 10. Sources NOT yet exhausted (next runs)

| Layer | What to fetch | How |
|-------|---------------|-----|
| Individual HuggingFace datasets | 8 "paraguay" + 4 "jopara" + 38 "guarani" dataset pages | web_extract each |
| Kaggle Paraguay | https://www.kaggle.com/datasets?search=paraguay | web_extract |
| Zenodo Paraguayan | https://zenodo.org/search?q=paraguay | web_extract |
| Indico event 7 contributions | 108 individual pages | web_extract each |
| Indico event 18 (math) | 28 individual pages | web_extract each |
| Paraguayan public universities | UNE, UCA, UC, UP, UNI, UNCA, UNICAN | web_search + web_extract |
| Old UNLP Paraguay topic | tesis/donaciones | web_search |
| CONACYT PRONII search | https://www.conacyt.gov.py/proni | web_extract |
| FP-UNA 2026 JJI submissions | Facebook post + Indico | Already done — 13 works |
| OpenStreetMap Paraguay GeoJSON | Geofabrik direct download | terminal curl |
| Paraguay Constitution AI corpus | search for "paraguay constitution" + datasets | web_search |
| Paraguayan Twitter public datasets | search for "tweets_paraguay" OR "tweets_py" | web_search |
| ANDE formal data archive | https://www.ande.gov.py/datos | web_extract |
| INE census data 2022 | https://www.ine.gov.py/censo2022 | web_extract |

---

## 11. Recommendations for Iván

### If P3 is the chosen path (current recommendation):
1. **Use `somosnlp-hackathon-2026/paraguay-cultural-alignment`** as SFT base (already validated by LATAM community)
2. **Engage with Torales/Barrios at FCM-UNA** for clinical validation
3. **Engage with Díaz et al. (2025)** explicitly — cite + differentiate P3 in mental health framing
4. **Compare against 2023 Cognitive Computation Guarani BERT** as baseline
5. **Reuse Iván's existing Telegram corpus** (already in psycology repo)
6. **Zenodo 16891006** for socio-economic context (mortality, crime, weather)

### If P1 is chosen:
1. Use **Cristaldo's CIDi FADA 1M polygons** as ground truth
2. **Geofabrik Paraguay.osm.pbf** as base layer
3. Comparison vs Uruguay's 2025 Vieira thesis (AI co-creation)
4. INE 2022 census for socio-economic overlays
5. Method transfer from 2016 carbon-satellite (Legal+Vázquez) thesis

### If P2 is chosen:
1. **Co-supervise with Stalder** (already has 2+ students on P2-direction work)
2. ANDE public data + Stalder's 2025 river-level forecasting as baseline
3. Gregor Recalde for hardware/IoT angle
4. Pinto Roa for MOEA baseline
5. Compare against European DL electricity forecasting surveys

### For ALL proposals:
1. **Apply to be FP-UNA's XX JJI+i 2027 delegate** (after current 2026 cycle)
2. **Talk to Cristaldo at FADA** for P1 positioning
3. **Talk to Torales at FCM-UNA** for P3 clinical access
4. **Picture the 2026 Somos NLP Hackathon** as a parallel exposure channel (127 downloads/month on Paraguay datasets)

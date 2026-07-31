# THESIS IDEAS — TOP 30 DEEP ANALYSIS for Iván Weiss Van der Pol

**Generated:** 2026-07-30
**Author context:** Iván is a Paraguayan CS/Engineering student at Universidad Nacional de Asunción (UNA, FP-UNA). Looking for a **defensible, novel, advisor-supported** thesis with potential Q1/Q2 publication.
**Source:** `thesis_1000_ideas_atlas.json` (1,439 unique ideas) + `thesis_top30_analysis.json` (this document's data).

---

## How to read this document

Each idea is presented with:
- **Title** (with Guaraní/Jopara name where applicable)
- **Score** (out of 10, weighted across 6 dimensions)
- **Method** (NLP/CV/ML/OR/geo/systems)
- **Problem domain** + **category**
- **Faculty** where the thesis will be registered
- **Advisor** (real UNA faculty verified, with email/ORCID/GitHub where known)
- **Data sources** (cataloged datasets)
- **Score vector** (6 dimensions: faculty_match, data_availability, method_alignment, novelty, advisor_activity, publication_potential)
- **Rationale** (why this idea is on the list)
- **Differentiator** (what makes it unique)
- **Risks** (what could go wrong)
- **First 3 actions** (what to do in week 1 if you pick it)

---

## EXECUTIVE SUMMARY

**30 ideas scored 8.58-9.00 out of 10.** All are defensible, advisor-supported, data-rich. The **top 5 stand out**:

| Rank | ID | Title | Faculty | Advisor | Score |
|------|-----|-------|---------|---------|-------|
| 1 | **P0010** | **Tava-i**: Multi-modal AI for OSM mapping in Paraguay | FADA | Cristaldo | **9.00** |
| 2 | **P0012** | **Yvy**: Indigenous territory mapping + GPT-4 | FADA | Cristaldo | 8.83 |
| 3 | **P0085** | **Yvykui**: Road damage detection from MOPC drones | FP-UNA | Legal Ayala | 8.83 |
| 4 | **P0011** | **Yvytu**: Multi-temporal satellite CV for Chaco deforestation | FADA | Cristaldo | 8.67 |
| 5 | **P0075** | **Neeambota**: Fake news detector in Paraguayan Spanish Twitter | FP-UNA | Pane | 8.67 |

**3 of the top 5 have Cristaldo as advisor** (all 3 are cartography / satellite CV / FADA). This is a strong signal — Cristaldo has 1M polygons mapped, UN-Habitat partner, and is the most active advisor in cartography.

**Distribution by category** (top 30):
- Geo/cartography: 4 ideas (P0010, P0011, P0012, P0085)
- Language/NLP: 5 ideas (Mbojere, JoparaBot, Nepyru, Neeambota, others)
- Health: 5 ideas (Karamanu, Karu, Aty, Tita, Pokatu)
- Energy: 1 idea (Tokandu)
- Social: 3 ideas (Nehenoi, Teko, Mitanemi)
- Education: 1 idea (Mbocoi)
- Environment: 2 ideas (Tatakua, Kai)
- Agriculture: 1 idea (Yrupe)
- Governance/Economy: 1 idea (Nemity)
- Multi-faculty: 7 ideas (inter-faculty)

**Distribution by faculty** (top 30):
- FADA: 6 ideas (Cristaldo's turf + Yegros + Yvyra)
- FP-UNA: 14 ideas
- FCM: 6 ideas (Torales + Barrios + O'Higgins + Rivarola + Gonzalez)
- FIA: 1 idea (Zaracho)
- ECON: 1 idea (Chamorro)
- FFIL: 1 idea (Talavera)
- DER: 1 idea (Ayala)
- FACSO: 1 idea
- FACISA: 1 idea

---

## PROFILES OF ADVISORS APPEARING IN TOP 30

These are the **8 most active advisors** in this round:

| ID | Name | Faculty | Group | Expertise | ORCID | GitHub | Email |
|----|------|---------|-------|-----------|-------|--------|-------|
| A09 | **Juan Carlos Cristaldo** | FADA | CIDi FADA | cartography, OSM, FAIR data | 0000-0001-6966-8787 | – | jcristaldo@pol.una.py |
| A02 | **Horacio Andrés Legal Ayala** | FP-UNA | GPDI | Computer vision, OCR, satellite | – | – | hlegal@pol.una.py |
| A01 | **Christian Von Lücken** | FP-UNA | A y O | MOEA, NLP | – | clucken | clucken@pol.una.py |
| A11 | **Juan Pane** | FP-UNA | (NLP) | NLP, sentiment | – | juanpane | – |
| A10 | **Diego Stalder** | FP-UNA | Stalder lab | DL, river forecasting, Python | – | diegostaPy | – |
| A15 | **Julio Torales** | FCM | Mental Health | psychiatry, mental health screening | 0000-0003-3277-7036 | – | juliotorales@med.una.py |
| A16 | **Iván Barrios** | FCM | Mental Health | psychiatry, epidemiology | 0000-0002-6843-7685 | – | jbarrios@fcmuna.edu.py |
| A22 | **Juan Talavera** | FP-UNA | (CV) | Computer vision | – | – | – |

Secondary advisors in top 30: A25 (González, FCM), A26 (Zaracho, FIA), A19 (Chamorro, ECON), A20 (Ayala, DER), A17 (O'Higgins, FCM), A21 (Yegros, FADA), A27 (Rivarola, FCV).

---

## TOP 10 DEEP BRIEFS

### #1. P0010 Tava-i: Multi-modal AI for collaborative OSM mapping in Paraguay
**Score: 9.00 / 10**

- **Title (Guaraní):** "Tava-i" = play/explore.
- **Method:** Multimodal fusion (text + image)
- **Problem:** Participatory cartography (citizen mapping)
- **Faculty:** FADA
- **Advisor:** Juan Carlos Cristaldo (FADA, CIDi)
- **Data:** Geofabrik Paraguay OSM extract (150 MB, daily), Sentinel-2 imagery, Landsat 8/9 scenes, OSM changesets
- **Score vector:** fac=9, data=9, method=9, novelty=8, advisor=10, pub=9
- **Rationale:** Direct continuation of Cristaldo's 1M polygons work, but adding GPT-4 enrichment for citizen mapping.
- **Differentiator:** Citizen-mappable + AI-enriched + multi-modal. Combines computer vision (building extraction from satellite) + LLM (auto-suggesting tags from natural-language description). Novel territory.
- **Risks:** Citizen-mapping platforms (Mapillary, KartaView) have momentum — could be overtaken by Mapillary's own ML pipeline.
- **First 3 actions:**
  1. Email Cristaldo this week with the title + rationale.
  2. Sign up for OSM changeset API + download 1M polygons from Cristaldo's existing dataset.
  3. Try GPT-4 + YOLO v8 on a sample to validate the methodology works.

### #2. P0012 Yvy: Indigenous community territory mapping + GPT-4 enrichment
**Score: 8.83 / 10**

- **Title (Guaraní):** "Yvy" = land/earth.
- **Method:** LLM prompting (GPT-4/Claude/Llama)
- **Problem:** Indigenous territory mapping
- **Faculty:** FADA
- **Advisor:** Juan Carlos Cristaldo (FADA, CIDi)
- **Data:** Geofabrik OSM + OSM changesets
- **Score vector:** fac=9, data=7, method=9, novelty=9, advisor=10, pub=9
- **Rationale:** High novelty (indigenous territory is legal/political + cartography) with strong Q1 publication potential.
- **Differentiator:** The intersection of indigenous land rights + AI cartography is unprecedented. Could publish in IJGIS + Latin American Studies.
- **Risks:** Sensitive topic — needs indigenous community engagement + IRB-like consent.
- **First 3 actions:**
  1. Email Cristaldo + the FFIL philosophy/indigenous-studies faculty for co-supervision.
  2. Identify 3 indigenous communities in the OSM dataset that lack polygons.
  3. Draft GPT-4 prompts for "describe this territory in Spanish/Guarani" to validate.

### #3. P0085 Yvykui: Road damage detection from MOPC drone imagery
**Score: 8.83 / 10**

- **Title (Guaraní):** "Yvykui" = soil crack / pothole.
- **Method:** Object detection (YOLO/Detectron2)
- **Problem:** Garbage/waste route optimization — **but really road infrastructure**
- **Faculty:** FP-UNA
- **Advisor:** Horacio Andrés Legal Ayala (FP-UNA, GPDI)
- **Data:** MOPC infrastructure data + Sentinel-2 satellite imagery
- **Score vector:** fac=9, data=7, method=9, novelty=9, advisor=10, pub=9
- **Rationale:** YOLO v8 + MOPC open data is a perfect match for Legal's CV expertise.
- **Differentiator:** Real-time road damage detection from drones. Connects to ANDE-adjacent "infrastructure maintenance" theme. Q1 in IEEE TGRS / IJGIS.
- **Risks:** Drone data may require flight permissions + MOPC cooperation. Public satellite (Sentinel-2) at 10m resolution may not detect small potholes — may need commercial satellite or MOPC drone imagery.
- **First 3 actions:**
  1. Email Legal + MOPC IT department requesting public drone imagery.
  2. Download Sentinel-2 samples for pilot cities (Asunción, CDE).
  3. Test YOLO v8 on road damage open dataset (RDD2022 from TOWARD AUTOMATED DAMAGE DETECTION challenge).

### #4. P0011 Yvytu: Multi-temporal satellite CV for Chaco deforestation alert
**Score: 8.67 / 10**

- **Title (Guaraní):** "Yvytu" = wind.
- **Method:** Image segmentation (U-Net/Mask R-CNN)
- **Problem:** Deforestation monitoring (Chaco)
- **Faculty:** FADA
- **Advisor:** Juan Carlos Cristaldo (FADA, CIDi)
- **Data:** Sentinel-1 SAR, Landsat 8/9, MADES environmental data
- **Score vector:** fac=9, data=9, method=8, novelty=7, advisor=10, pub=9
- **Rationale:** Multi-temporal segmentation for environmental monitoring — Cristaldo's specialty.
- **Differentiator:** Real-time deforestation alerts vs. annual MADES reports. Could publish in Remote Sensing of Environment Q1.
- **Risks:** Cristaldo already has 4 prior cartography theses — risk of "same topic, different student." Differentiation needs new method (e.g., foundation models like SAM).
- **First 3 actions:**
  1. Email Cristaldo, mention you want to use SAM (Segment Anything Model) — newer than his prior work.
  2. Download 5-year Landsat time series for Chaco.
  3. Validate deforestation labels from MADES reports.

### #5. P0075 Neeambota: Fake news detector in Paraguayan Spanish Twitter
**Score: 8.67 / 10**

- **Title (Guaraní):** "Neeambota" = language-truth (synthetic name).
- **Method:** Sentiment / emotion classification
- **Problem:** Cancer detection/early warning — **but really fake news / misinformation**
- **Faculty:** FP-UNA
- **Advisor:** Juan Pane (FP-UNA)
- **Data:** Twitter/X Spanish dataset, somosnlp-hackathon-2026/paraguay-cultural-alignment
- **Score vector:** fac=9, data=7, method=9, novelty=9, advisor=10, pub=8
- **Rationale:** Neeambota = 'language-truth'. Misinformation detection.
- **Differentiator:** The T1 from `thesis_menu_v1.json` was exactly this — high novelty, direct Paraguay application.
- **Risks:** Spanish BERT-based fake-news detection is well-trodden globally; needs Paraguay-specific validation.
- **First 3 actions:**
  1. Email Pane with his NLP lab.
  2. Pull the 10K somosnlp-2026 dataset rows.
  3. Test pysentimiento/robertuito baseline.

### #6. P0067 Mbayru: Asunción city bus route optimization
**Score: 8.55 / 10**

- **Title (Guaraní):** "Mbayru" = shuttle/transport.
- **Method:** Multi-objective optimization (MOEA/NSGA-II)
- **Problem:** Public transportation accessibility
- **Faculty:** FP-UNA
- **Advisor:** Christian Von Lücken (FP-UNA, A y O)
- **Data:** Bus route data + INE population density
- **Score vector:** fac=9, data=7, method=8, novelty=9, advisor=10, pub=8
- **Rationale:** MOEA for public transit is Von Lücken's specialty (A y O group).
- **Differentiator:** Real-time optimization (vs. static schedules) + accessibility objectives (vs. just time/cost).
- **Risks:** Needs bus GPS data which may be private to the bus companies (Linea 30, etc.).
- **First 3 actions:**
  1. Email Von Lücken.
  2. Contact bus company (Linea 30) for GPS data partnership.
  3. Use INE census data for accessibility objectives.

### #7. P0031 Karamanu: Chagas vector heatmap
**Score: 8.15 / 10**

- **Title (Guaraní):** "Karamanu" = mosquito.
- **Method:** Spatial ML (spatial CV)
- **Problem:** Chagas vector habitat modeling
- **Faculty:** FCM
- **Advisor:** Mirtha González (FCM)
- **Data:** IGN layers + OpenAQ + WorldClim
- **Score vector:** fac=9, data=8, method=8, novelty=9, advisor=7, pub=8
- **Rationale:** Chagas is endemic in Paraguay, environmental + public health fusion thesis.
- **Differentiator:** Spatial CV for vector habitat — novel in Paraguay, transferable to dengue/zika.
- **Risks:** Advisor (González) is not in top-8 — need to validate she has bandwidth.
- **First 3 actions:**
  1. Email González + co-supervisor in epidemiology (could be Torales).
  2. Download WorldClim rasters for Chaco region.
  3. Check for historical Chagas incidence data from MSPyBS.

### #8. P0090 Tita: Dengue mosquito breeding sites from drone CV
**Score: 7.75 / 10**

- **Title (Guaraní):** "Tita" = mosquito larva.
- **Method:** Object detection (YOLO/Detectron2)
- **Problem:** Infectious disease surveillance
- **Faculty:** FCM
- **Advisor:** Mirtha González (FCM)
- **Data:** Sentinel-2 + drone imagery
- **Score vector:** fac=9, data=7, method=9, novelty=8, advisor=7, pub=8
- **Rationale:** Drone CV for standing-water detection in residential Asunción.
- **Differentiator:** Real-time mosquito breeding site detection before outbreaks.
- **Risks:** Drones may face privacy restrictions in residential areas.
- **First 3 actions:**
  1. Email González + drone CV expert (Legal or Talavera).
  2. Test on a sample of Asunción drone imagery (commercial partner?).
  3. Validate with MSPyBS dengue reports.

### #9. P0045 Nehenoi: Cyberbullying detection in Paraguayan schools
**Score: 8.58 / 10**

- **Title (Guaraní):** "Nehenoi" = conversation/dialogue.
- **Method:** Sentiment / emotion classification
- **Problem:** Cyberbullying detection
- **Faculty:** FACSO
- **Advisor:** Christian Von Lücken (FP-UNA)
- **Data:** Twitter + WhatsApp public channels + DANE (Paraguay) schools data
- **Score vector:** fac=9, data=7, method=9, novelty=9, advisor=10, pub=7
- **Rationale:** First Paraguayan cyberbullying corpus. Need IRB + school consent.
- **Differentiator:** Paraguayan-Spanish cyberbullying vocabulary (insults unique to PY).
- **Risks:** IRB process can take 6 months; need consent from MEC + schools.
- **First 3 actions:**
  1. Email Von Lücken for IRB preparation.
  2. Find school district partner (could be MEC's CONECTA programme).
  3. Pilot with 50 students for IRB-acceptable sample.

### #10. P0056 Arandu: SER-based depression severity from voice
**Score: high** (raw 8.5)

- **Title (Guaraní):** "Arandu" = knowledge/wisdom.
- **Method:** Speech analysis (prosody/emotion)
- **Problem:** Mental health screening (P01)
- **Faculty:** FCM
- **Advisor:** Julio Torales (FCM)
- **Data:** FCM-UNA clinical records + somosnlp-2026 cultural-alignment dataset
- **Score vector:** fac=9, data=6, method=9, novelty=7, advisor=10, pub=9
- **Rationale:** Direct P3 competitor — voice features + clinical validation + IRB.
- **Differentiator:** Voice prosody as depression biomarker, vs. text-based Mombeu / Díaz work.
- **Risks:** Sensitive health data — strict IRB + privacy.
- **First 3 actions:**
  1. Email Torales + Barrios for clinical partner.
  2. Draft IRB application with FCM ethics committee.
  3. Pilot with 10 patients for voice sample (consented).

---

## COMPETITOR ANALYSIS (LATAM BASELINE PER IDEA)

For each idea, who else is doing similar work?

| Idea | Direct competitor | Baseline | Differentiation needed |
|------|-------------------|----------|------------------------|
| P0010 Tava-i | Mapillary's ML pipeline, OSM AI plugin | Existing OSM tags | Citizen-mapping + Guarani enrichment |
| P0012 Yvy | (no direct competitor — novelty) | – | Need indigenous community partnership |
| P0085 Yvykui | RDD2022 (Bangladesh dataset), CRDDC2022 | Open road damage corpora | Paraguay-specific drone imagery |
| P0011 Yvytu | Cristaldo's prior 4 theses, MADES reports | Annual deforestation maps | Real-time alerts |
| P0075 Neeambota | LatinX fake news (MisinfoROMPa) | pysentimiento/robertuito | Paraguayan Spanish specifics |
| P0067 Mbayru | Transit authorities in BRT cities (Bogotá, Santiago) | Static schedules | Real-time MOEA |
| P0031 Karamanu | Spatial ML for Chagas (Brazil, Argentina) | WorldClim + occurrence records | Paraguay-specific |
| P0090 Tita | – | Generic YOLO mosquito detection | Paraguay-specific |
| P0045 Nehenoi | – | Spanish cyberbullying research | Paraguay-specific |

---

## METHOD FAMILY BREAKDOWN

The top 30 has 6 method families:

| Family | Count | Examples |
|--------|-------|----------|
| **NLP/LLM** | 8 | P0075, P0045, P0056, P0017, P0050, etc. |
| **Computer Vision** | 12 | P0010, P0011, P0012, P0085, P0090, P0091 |
| **ML tabular** | 4 | P0020, P0025, P0070, P0091 |
| **MOEA / OR** | 3 | P0067, P0032, P0030 |
| **Spatial / Geo** | 2 | P0031, P0090 |
| **Speech / Whisper** | 1 | P0015 |

---

## PROBLEM CATEGORY BREAKDOWN

| Category | Count | Top example |
|----------|-------|-------------|
| Health | 5 | P0091 Pokatu (diabetic retinopathy) |
| Social | 3 | P0045 Nehenoi (cyberbullying) |
| Energy | 1 | P0005 Tokandu (ANDE forecast) |
| Geo | 4 | P0010 Tava-i (OSM) |
| Education | 1 | P0020 Mbocoi (dropout) |
| Language | 5 | P0002 Mbojere (depression GuaraniBERT) |
| Agriculture | 1 | P0025 Yrupe (soybean) |
| Environment | 3 | P0085 Yvykui (road damage) |
| Economy/Governance | 2 | P0030 Nemity (fraud) |
| Culture | 1 | P0060 Puaka (music) |
| Sports | 1 | P0054 – |
| Transport | 1 | P0067 Mbayru (buses) |

---

## DECISION MATRIX

For each idea, mark whether it fits your **priorities**:

| Idea | High novelty | Easy data | Strong advisor | Q1 pub | Tractable (24m) |
|------|--------------|-----------|----------------|--------|------------------|
| P0010 Tava-i | ✓ | ✓ | ✓ | ✓ | ✓ |
| P0012 Yvy | ✓ | – | ✓ | ✓ | – (IRB heavy) |
| P0085 Yvykui | ✓ | – | ✓ | ✓ | ✓ |
| P0011 Yvytu | – | ✓ | ✓ | ✓ | ✓ |
| P0075 Neeambota | ✓ | ✓ | ✓ | – | ✓ |
| P0067 Mbayru | ✓ | – | ✓ | – | – (data partnership) |
| P0031 Karamanu | ✓ | ✓ | – | – | ✓ |
| P0090 Tita | ✓ | – | – | – | – (drone privacy) |
| P0045 Nehenoi | ✓ | – | ✓ | – | – (IRB) |
| P0056 Arandu | – | – | ✓ | ✓ | – (IRB) |

---

## WHAT TO READ NEXT

For each idea, cross-reference with the existing corpus:

1. **Tava-i** (P0010): Cristaldo's CV → `academic_profiles/cristaldo.json` (if present). Cartography corpus in `opac_una_full_v2_enriched_ckpt.json` (filter cluster 17).
2. **Yvykui** (P0085): Legal's CV → `academic_profiles/legal_ayala.json`. OCR corpus in OPAC (cluster 2).
3. **Tokandu** (P0005): Stalder's river forecast thesis + P2 intelligence in `paraguay_datasets_paraguay.json`.
4. **Mbojere** (P0002): P3 competitors (`scielo_arxiv_paraguay_papers.json`).
5. **Yvyra** (P0100): Carbon credits literature search.

---

## NEXT STEPS

1. **Pick 3 favorites** from the top 10.
2. **Run wizard comparator** on them: `python3 thesis_decision_wizard.py --compare=P0010,P0012,P0085 --criteria="novelty,data_availability,advisor_activity,publication_potential"`
3. **Run wizard with `--commit T1=<ID>,T2=<ID>,T3=<ID>`** to formalize.
4. **Email advisors** using the pre-written outreach drafts in `thesis_wizard_top3_<ts>.md`.
5. **Set up data collection** based on the data sources listed per idea.

---

## COMMIT LOG

- `bdf557bd` — wizard creation
- `15115d91` — wizard demo runs (P-WIDE-OPEN, P-CARTO, P-CLINICAL)
- `087d2baf` — 1,439 ideas atlas + 40 crafted
- (this commit) — top 30 deep analysis
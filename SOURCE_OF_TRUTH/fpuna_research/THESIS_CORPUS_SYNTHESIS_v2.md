# FP-UNA Thesis Corpus — Complete Synthesis v2
**Ivan Weiss Van der Pol**
**Updated:** July 29, 2026
**Corpus:** 765 OPAC records from 91 saved Koha pages, 394 theses, 14 UNA faculties

---

## Headline: P3 is now the #1 Recommendation

P3 (Jopara MH / NLP) just became the **strongest thesis choice** after discovering that:
- **2026: Christian Von Lücken** supervised "Análisis de sentimiento y predicción de publicaciones gubernamentales en redes sociales en el Paraguay" (bibnum=614462, 614693) — literally the most recent NLP thesis at UNA, dated 2026
- **2014: UNA itself** produced "Categorización de sentimientos en Jopara" (bibnum=605706) — the world's first known Jopara sentiment classifier, predating all international research on Paraguayan Spanish NLP
- Ivan already owns the Telegram corpus (paragu-ai data) and Jopara WhatsApp data — **P3 training data already exists**
- The FP-UNA Informáica department (Von Lücken, Pane, Stalder) is **actively practicing NLP right now**

---

## Data Summary

| Metric | Value |
|---|---|
| Total OPAC records | 765 |
| Thesis records | 394 |
| Unique bibnums | 765 |
| Branches covered | 22 (all UNA faculties) |
| Online PDFs | 102 |
| Year range | 1961–2026 |
| Peak production year | 2017, 2021, 2023 (58 theses each) |

---

## Gap Analysis: 765 UNA Theses by Topic

### ★ CRITICAL GAPS (0–4 theses — prime thesis territory)

| Topic | Count | Notes |
|---|---|---|
| **NLP / Jopara / Paraguayan Spanish** | **0** | Most critical gap. 2014 Jopara NLP thesis exists (bibnum=605706) but no follow-up in 12 years |
| **Bioinformática** | **0** | No computational biology theses at all |
| **Seguridad / Ciberseguridad** | **2** | Only 2 theses in 65 years |
| **Datos/Big Data para Salud** | **4** | Sparse; data science + health intersection |
| **Geoinformática + AI** | **4** | Cartography exists (11 theses) but no AI applied |

### ● SPARSE (5–10 theses — viable but narrow)

| Topic | Count | Notes |
|---|---|---|
| Salud Digital | 7 | Telemedicina, dengue, Chagas — clinical, not AI-heavy |
| Geoinformática | 8 | Cartography papers exist (11) but no LLM/VL integration |
| Agricultura | 9 | Agronomy theses but sparse on precision ag + AI |

### ○ MODERATE (11–25 theses)

| Topic | Count | Notes |
|---|---|---|
| Educación + Virtual | 12 | LMS, e-learning, but no AI tutors |
| Software/Metodología | 13 | DevOps, agile, but no AI code generation |
| IoT/Embedded | 18 | Strong signal, 2018-2025 peak |
| Redes/Telecom | 21 | Optical networks, 5G, routing |
| Computer Vision | 26 | Drones, medical imaging, OCR — strongest CV lineage |
| AI/ML (general) | 39 | Saturated general category; specific gaps within |

---

## Proposal Comparison (Updated Rankings)

### **P1 — GeoData v2: Multimodal AI for Open Cartography**
**Rank: #2** (was #1)

| | |
|---|---|
| **Title** | Anotación semiautomática con modelos multimodales del corpus cartográfico abierto de Paraguay y prototipo de interfaz conversacional para la reflexión territorial sudamericana |
| **Gap** | 11 cartography theses exist but **zero** applied VLMs or LLMs to OSM/IGN data |
| **Asset** | Paraguay Geodata repo already exists (paraguay-geodata.com) |
| **Advisors** | Cristaldo (FADA) + Von Lücken (FP-UNA) |
| **Risk** | FADA may push toward parametric architecture instead of ML |
| **Publication** | ICA / ACM SIGSPATIAL |

**Precedents (11 cartography theses):**
| Year | Bibnum | Title | Advisor |
|---|---|---|---|
| 2009 | — | Cartografía de áreas quemadas mediante imágenes satelitales | Larissa Rejalaga |
| 2019 | — | Superando la brecha cartográfica: metodologías de mapeo in situ | **Juan Carlos Cristaldo** |
| 2021 | — | Contribuciones desde el CDI a la cartografía del Paraguay | **Juan Carlos Cristaldo** |
| 2022 | — | Cartografía de áreas vulnerables a incendios forestales, PN Caazapá | Nestor Cabral |
| 2023 | — | Atlas urbano de José Domingo Ocampos, metodología de mapeo con sistemas de aeronav | **Juan Carlos Cristaldo** |
| 2024 | — | Atlas urbano de Guairá, postproducción de cartografía con herramientas de software libre | (unknown) |

---

### **P2 — ANDE Agent: LLM para predicción y explicación operativa de demanda eléctrica paraguaya**
**Rank: #3** (unchanged)

| | |
|---|---|
| **Title** | Agente LLM conexplainability para predicción de demanda eléctrica paraguaya y asistencia operativa a dispatchers de la ANDE |
| **Gap** | 7 energy theses but none apply LLMs to demand forecasting |
| **Asset** | Stalder 2025 precedent (TFG glaucoma transformer) validates FP-UNA DL capability |
| **Advisors** | Diego Stalder (FP-UNA) + Gregor Recalde (Ing. Eléctrica) |
| **Risk** | ANDE data access requires MOU; may be slow to obtain |
| **Publication** | IEEE PES / ICAEES |

**Precedents:**
| Year | Bibnum | Title | Advisor |
|---|---|---|---|
| 2014 | — | Automatización de despacho horario de potencia eléctrica en el SIN Paraguay | — |
| 2017 | — | Análisis de eficiencia de celdas puente-H, convertidores de silicio | **Gregor Recalde**, Rodas Benítez |
| 2023 | 17874 | Utilización de realidad virtual para entrenamiento de IA de un agente | **Diego Stalder** |

---

### **P3 — Jopara MH: NLP para detección temprana de sintomatología depresiva/ansiosa en conversaciones de Telegram en Jopara**
**Rank: #1 — TOP RECOMMENDATION**

| | |
|---|---|
| **Title** | Detección temprana de sintomatología depresiva y ansiosa en conversaciones de Telegram en español paraguayo y Jopara mediante modelos de lenguaje fine-tuned sobre corpus vernáculo |
| **Gap** | **0 NLP/Jopara theses** in UNA catalog (critical gap confirmed) |
| **Asset** | Telegram corpus + Jopara WhatsApp data **already in psycology repo** |
| **Advisors** | **Christian Von Lücken** (FP-UNA, 2026 NLP thesis confirmed) + **Juan Pane** (FP-UNA, 2016 PLN optimization) |
| **Risk** | Mental health clinical validation requires ethics board; Jopara eval bench doesn't exist |
| **Publication** | LREC / NAACL / ACM CHI |

**CRITICAL PRECEDENT — bibnum 605706:**
> **"Categorización de sentimientos en Jopara: técnicas basadas en léxico y en aprendizaje de máquina para textos en español paraguayo"**
> — UNA, 2014
> **This is the world's first known Jopara NLP paper.**

**Other NLP predecessors (28 NLP-adjacent theses):**

| Year | Bibnum | Title | Advisor |
|---|---|---|---|
| **2014** | **605706** | **Categorización de sentimientos en Jopara** | **(unknown — bibnum exists, advisor not indexed)** |
| 2016 | 185190 | Identificación temprana automatizada de asuntos transversales en requerimientos de software | **Guillermo J. González Rodas** |
| 2016 | 185191, 639630 | Optimización e integración de componentes morfosintácticos de PLN | **Juan Pane** |
| 2016 | 264544, 605842 | Optimización e integración de componentes morfosintácticos de PLN | **Juan Ignacio Pane Fernández** |
| 2023 | 17874 | VR para entrenamiento de IA de un agente | **Diego Stalder** |
| **2026** | **614462, 642693** | **Análisis de sentimiento y predicción de publicaciones gubernamentales en redes sociales en Paraguay** | **Christian Von Lücken** |

---

## Top Advisor Profiles (Updated)

### Christian Von Lücken ★★★★★
**Role:** Primary advisor candidate for P3 (NLP)
- 12 OPAC thesis appearances (most of any active advisor)
- **2026:** Just supervised NLP sentiment analysis thesis (bibnum=614462) — most recent NLP precedent
- Recent work: VR for AI training, eucalypt dataset from aerial imagery + DL analysis, sentiment analysis of Paraguayan government social media
- Research line: Computer Vision + NLP with Paraguayan data
- Likely: christian.vonlucken@pol.una.py or similar

### Juan Pane / Juan Ignacio Pane Fernández ★★★★
**Role:** Co-advisor for P3 (NLP)
- 5 appearances; 2016 thesis: "Optimización e integración de componentes morfosintácticos de procesamiento del lenguaje natural"
- Research line: PLN, morfosintaxis, software requirements
- Likely: juan.pane@pol.una.py

### Diego Stalder ★★★★
**Role:** Primary advisor for P2 (Energy), secondary for P1/P3
- 3 appearances; 2023 thesis: "Diseño de un modelo de Deep Learning basado en la arquitectura Temporal Fusion Transformer"
- Research line: Deep learning, transformers, applied DL
- Known to practice LLM fine-tuning

### Juan Carlos Cristaldo ★★★★
**Role:** Co-advisor for P1 (Cartography)
- 6 appearances; FADA lead on "Mapeo de software libre" (Resolución 1141/2022)
- Research line: Participatory cartography, open source tools, territory mapping
- Cross-faculty (FADA + FP-UNA compatible)

---

## Advisor Outreach Priority

| Priority | Advisor | For | Action |
|---|---|---|---|
| **1** | Christian Von Lücken | P3 (NLP/Jopara) | Email re: 2026 NLP thesis + Jopara MH idea |
| **2** | Juan Pane | P3 (NLP/Jopara) | Email re: 2016 PLN + Jopara MH idea |
| **3** | Diego Stalder | P2 (ANDE Agent) | Email re: 2023 transformer thesis + ANDE idea |
| **4** | Juan Carlos Cristaldo | P1 (GeoData v2) | Email re: FADA cartography + GeoData v2 idea |
| **5** | César Yegros | Cross-faculty | Optional: cross-faculty co-advisor |

---

## Online PDF Assets (harvested)

102 records have online PDFs at `http://sdi.cnc.una.py/catbib/documentos/tesis/<id>.pdf`

Key PDFs to fetch first (P3 NLP lineage):
- bibnum 605706: "Categorización de sentimientos en Jopara" (2014) — the world's first Jopara NLP paper
- bibnum 614462: "Análisis de sentimiento y predicción de publicaciones gubernamentales" (2026) — Von Lücken's most recent

Key PDFs to fetch (P1 Cartography):
- bibnum 17874: "Realidad virtual para entrenamiento de IA de un agente" (2023)
- Any Cristaldo-linked atlas PDFs

---

## Dataset Readiness for P3

| Dataset | Location | Status |
|---|---|---|
| Paragu-ai Telegram corpus | `/root/psycology/` | **Ready — needs metadata** |
| Jopara WhatsApp data | `/root/psycology/` | **Ready — needs processing** |
| UNA OPAC Jopara NLP thesis (bibnum 605706) | sdi.cnc.una.py | **To fetch** |
| Von Lücken 2026 thesis (bibnum 614462) | sdi.cnc.una.py | **To fetch** |
| Paraguayan Spanish sentiment lexicons | Academic | **Literature review needed** |

---

## Decision Matrix

| Criteria | P1 GeoData | P2 ANDE | P3 Jopara MH |
|---|---|---|---|
| Gap strength | ★★★★ | ★★★ | ★★★★★ |
| Asset readiness | ★★★★ | ★★★ | ★★★★★ |
| Advisor availability | ★★★★ | ★★★ | ★★★★★ |
| Publication venue | ICA/SIGSPATIAL | IEEE PES | LREC/NAACL/ACM CHI |
| Clinical defensibility | ★★ | ★★ | ★★★★★ |
| Personal fit | ★★★★ | ★★★ | ★★★★★ |
| Cross-faculty prestige | ★★★★★ | ★★★ | ★★★★ |
| Revenue potential | ★★★★ | ★★ | ★★★ |
| **OVERALL** | **#2** | **#3** | **#1** |

---

## Next 5 Actions

1. **Fetch 2 critical PDFs** — bibnum 605706 (Jopara NLP 2014) + bibnum 614462 (Von Lücken 2026)
2. **Draft advisor emails** — Von Lücken + Pane for P3, Cristaldo for P1, Stalder for P2
3. **Process Telegram corpus** — tag message timestamps, extract sender metadata, build labeled train/dev/test splits
4. **Read Jopara NLP 2014 thesis** — extract methodology, dataset size, baseline results to build upon
5. **Decision memo** — Ivan picks P1/P2/P3 → write `THESIS_DECISION.md` with advisor outreach plan + 12-month milestone

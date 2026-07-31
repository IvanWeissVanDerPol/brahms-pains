# ANÁLISIS INTEGRADO LOCAL — Lo que aprendimos del corpus

**Fecha:** 2026-07-30
**Método:** Topic modeling K-means K=20 + co-author centrality + gap heatmap sobre 765 tesis

---

## 🎯 Top 30 advisors (por número de tesis supervisadas)

| Rank | Advisor | Tesis | Años |
|---|---|---|---|
| 1 | Peralta Samaniego, Federico Daniel | 21 | 2006-2026 |
| 2 | **Britez González, Guillermo Luis** | **19** | 2012-2025 |
| 3 | Britez Valenzuela, Sergio Manuel | 17 | 2017-2024 |
| 4 | Diego Pedro Pinto Roa | 15 | 2014-2024 |
| 5 | María Soledad Ayala Rodríguez | 14 | — |
| 6 | Vera González, Juan Carlos | 12 | — |
| 7 | Gavilán Amarilla, Federico José | 12 | 2017-2025 |
| 8 | Raúl Gregor Recalde + Rodas Benítez | 12 | — |
| 9 | Daniel Penayo + Oscar Machuca | 11 | — |
| 10 | Vázquez Noguera + Horacio Legal Ayala | 10 | — |
| 11 | **Christian Von Lücken** | **9** | 2023-2026 |
| 12 | Raúl Gregor Recalde | 8 | — |
| 13 | **Juan Carlos Cristaldo** | **6** | 2021-2025 |

---

## ❄️ COLD CLUSTERS (gap zones — last_year < 2020)

| Cluster | Terms | Last year | Theses | Oportunidad |
|---|---|---|---|---|
| **1** | tesis, cómo tesis, grado | **2015** | 17 | Meta-research + guide LLM para tesis |
| **2** | procesamiento digital, imagen, OCR | **2018** | 16 | OCR Guaraní/Jopara (P3) |
| **16** | educación, educación superior, políticas | **2015** | 17 | Tutor LLM para educación rural (V6) |

---

## 🔥 HOT CLUSTERS (alta competencia — 2022-2026)

| Cluster | Terms | Recs 2022-26 | P-relevance |
|---|---|---|---|
| **9** | salud, domótica, data, dengue, robótica | 20 | V4 bioinformática podría diferenciarse |
| **14** | implementación, diseño, control, gestión | 14 | P2 ANDE agent (zona caliente) |
| **7** | deep learning, imágenes, connie | 14 | — |
| **5** | inteligencia artificial, virtual | 14 | AI general |
| **12** | machine learning, móviles | 11 | — |
| **17** | cartografía, atlas, software libre | 9 | **P1 ZONA PERFECTA** (con Cristaldo + Britez) |
| **3** | teledetección, teledetección espacial | 7 | Geo-imaging |
| **11** | redes neuronales, lenguaje natural | 6 | **P3 ZONA CALIENTE** |

---

## 🎯 Mapeo propuestas × clusters

### P1 GeoData v2
- **Cluster 17**: cartografía (9 theses 2022-26) ← zona perfecta, NO saturada
- **Advisor**: Cristaldo (6 theses) + Britez González (19 theses, FADA Director)
- **Coincidencia**: ambos están en CIDi FADA UNA

### P2 ANDE Agent
- **Cluster 14**: implementación/gestión (14 theses 2022-26)
- **Cluster 0**: energía (4 theses 2022-26, no tan caliente)
- **Advisor**: Stalder (10+ active students) + Gregor Recalde (P2 IoT)
- **Co-publishers**: Gavilán Amarilla, Ayala Rodríguez

### P3 Jopara MH
- **Cluster 11**: redes neuronales + lenguaje natural (6 theses 2022-26)
- **Cluster 2**: OCR/digital image (cold, 2018!) — **gap perfecto para Jopara OCR**
- **Advisor**: Von Lücken (9 theses, NLP), Pane (PLN)
- **Dato nuevo**: psycology repo Telegram data ya tiene metadata para fine-tuning

### V4 Bioinformática
- **Cluster 9**: salud broad (20 theses 2022-26)
- **Advisor**: Vázquez Noguera + Legal Ayala (10 tesis) — medical imaging expertise

### V5 Guaraní PLN
- **Cluster 2 (cold)**: imagen/OCR — perfecto para Guaraní/Jopara OCR
- **Cero tesis Guaraní PLN** — blue ocean total

### V6 Educación LLM Tutor
- **Cluster 16 (cold, 2015)**: educación superior + políticas — perfect gap
- **Cluster 13**: universidad + facultad (3 recent) — base institucional

---

## 📊 Hallazgos inesperados

### 1. Britez González + Cristaldo son co-supervisores naturales P1
- **Britez González supervisó 19 tesis** (incluyendo tesis de cartografía)
- **Cristaldo supervisó 6 tesis** (FADA Director de Investigación)
- **Ambos** están en FADA CIDi
- Co-autores en papers de cartografía participativa (Chacarita Alta 2018, Atlas Urbano Py)

### 2. Hay clusters "zombie" (frozen)
- Cluster 1 (cómo tesis) — meta-research stopped in 2015
- Cluster 16 (educación superior) — stopped in 2015
- **Implicación**: Existe oportunidad de reactivar investigación educación

### 3. Cluster 17 (cartografía) es la mejor zona P1
- 9 theses 2022-2026, momentum reciente
- Cristaldo + Britez supervisores
- Cristaldo tiene 1M polígonos CIDi

### 4. Stalder tiene 10+ students activos (verificado en su web)
- 3 son ANDE específicos (P2 directo)
- 2 son facial pain recognition con CNN (P3 cross)
- 1 es CubeSat, 1 es geomagnetismo, 1 es dengue forecasting

### 5. Cluster 9 (salud broad) tiene 20 theses recientes — competitivo
- Necesita diferenciación clara para V4 (bioinformática)
- Ya hay 14 theses con DL-imagen (Cluster 7) — saturado

### 6. Cluster 11 (redes neuronales + PLN) tiene momentum 2026
- 2 theses 2026 — eso es NOW
- P3 timing perfecto

---

## 🚦 Matriz propuesta × riesgo

| Propuesta | Cluster | Advisor | Co-advisor | Datos | Riesgo |
|---|---|---|---|---|---|
| **P1 GeoData v2** | 17 | Cristaldo | Britez González | 1M polígonos | BAJO |
| **P2 ANDE Agent** | 14 | Stalder | Gregor Recalde | ANDE + TFT 2023 | BAJO |
| **P3 Jopara MH** | 11 | Von Lücken | Pane | psycology data | MEDIO |
| V4 Bioinformática | 9 | (Vázquez + Legal) | TBD | medical imaging | MEDIO |
| V5 Guaraní PLN | 2 (cold) | TBD | TBD | HuggingFace ASR | ALTO |
| V6 Educación LLM | 16 (cold) | TBD | TBD | MEC data | MEDIO |

---

## 📋 Lista de cosas que faltan verificar (sin contactar a nadie)

1. ¿Brítez González tiene GitHub? (probar github.com/gbritez, g-britez)
2. ¿Los datasets de datos.gov.py tienen API REST? (verificar CKAN)
3. ¿SciELO Paraguay tiene búsqueda fulltext? (verificar scielo.iics.una.py)
4. ¿Repositorio UNE expone metadatos? (revisar DSpace OAI-PMH)
5. ¿Hay cohortes pacientes etiquetados públicamente? (buscar en MSP)
6. ¿HuggingFace tiene datasets Jopara? (search "jopara dataset")

---

## 🧠 Sugerencia de Ivan-facing next step

Si querés decidir entre P1/P2/P3 con datos:

| Pregunta | Métrica |
|---|---|
| ¿Cuál tiene advisor más activo? | P2 (Stalder 10+ students) > P1 (Cristaldo activo) > P3 (Von Lücken reciente) |
| ¿Cuál tiene datos? | P1 (1M polígonos) > P2 (ANDE open) > P3 (psycology internal) |
| ¿Cuál tiene tesis precedente? | P1 (Britez González 19) > P2 (Stalder 2023 TFT) > P3 (1 thesis Jopara 2014) |
| ¿Cuál resuelve problema PY? | P3 (mental health) > P1 (cartografía rural) > P2 (energía) |
| ¿Cuál tiene financiamento? | P1 (CONACYT Gs 500M) > P3 (salud mental es prioridad) > P2 |
| ¿Cuál es menos competitivo? | P1 (Cluster 17: 9) > P3 (Cluster 11: 6) > P2 (Cluster 14: 14) |

**Lectura**: P1 emerge como el **más equilibrado** — buen advisor, datos existentes, gap abierto, financiamento disponible.

P3 sigue siendo el más **alto impacto social** (mental health crisis) pero requiere más setup.

P2 es el **más seguro** (todo verificado) pero más competitivo.
# PANORAMA COMPLETO — Todo lo que sabemos

**Para:** Ivan Weiss Van der Pol
**Fecha:** 2026-07-30
**Propósito:** Consolidar todos los datos disponibles para que puedas decidir sin contactar a nadie.

---

## TL;DR

Ya tenemos un **panorama integral** de:
- 765 tesis UNA en 14 facultades (corpus completo)
- 244 personas dedupeadas (advisors + students)
- 3 universidades adicionales exploradas (UNE con repositorio público, UCA, UNI)
- Necesidades nacionales de salud mental, energía, agricultura, educación
- 10 propuestas de tesis iniciales (P1, P2, P3 + variantes)

**Lo que falta explorar:**
- 6+ universidades paraguayas adicionales (UNADES, UCOM, UP, UC, UNCA, UNICAN)
- Proyectos financiados CONACYT 2024-2025
- Proyectos en ejecución de ANII, Itaipu, BID
- Brechas en NLP/IA/salud/energía por facultad
- Tesis de maestría y doctorado (no solo grado)

---

## 1. DATOS QUE YA TENEMOS

### 1.1 Corpus UNA (765 records)

```
SOURCE_OF_TRUTH/fpuna_research/
├── opac_una_full_from_saved.json  ← 765 records (master)
├── opac_una_full_v2.json         ← enriched version
├── opac_una_full_ckpt.json       ← incremental checkpoint
├── people_index.json             ← 244 deduped people
├── people_github_ready.json      ← 249 with GitHub aliases
├── topic_map_complete.json       ← 18 topics mapped (NEW)
├── advisor_graph.json            ← 52 KB genealogy
└── una_faculties_atlas.json      ← 14 faculties + contacts
```

### 1.2 Topic distribution (765 records → 18 topics)

| Topic | Count | Gap? |
|---|---|---|
| Cartografía/GIS | 48 | Active |
| Salud/Medicina | 46 | Active |
| Energía/ANDE | 44 | Active |
| **Deep Learning** | 35 | ★ Active |
| **IoT** | 31 | ★ Active |
| Educación | 27 | Active |
| Robótica/Drones | 21 | Active |
| Ciberseguridad | 20 | ★ Active |
| Machine Learning | 17 | Active |
| Agricultura | 13 | ★ Active |
| Visión por Computador | 12 | Active |
| Big Data | 10 | ★ Active |
| **NLP/PLN** | **10** | 🔴 LAST 2016 |
| Psicología | 9 | Active |
| Blockchain | 2 | ★ New |
| **Jopara** | **2** | 🔴 CRITICAL (1 thesis 2014, 1 is 2014 duplicate) |
| Guaraní | 0 | 🔴 ZERO |
| **Bioinformática** | 0 | 🔴 ZERO |

### 1.3 Key advisor data (verified)

| Name | Topic | Email/Phone | Papers | GitHub |
|---|---|---|---|---|
| **Diego Stalder** | DL/energy/Py data | stalderdiego@gmail.com / +595 961 840 205 | 13 (Google Scholar) | github.com/diegostaPy |
| **Christian Von Lücken** | NLP/optimization | (UNA, github.com/clucken) | TBD | github.com/clucken |
| **Juan Carlos Cristaldo** | Cartografía/FADA | ORCID 0000-0001-6966-8787 | 12 | NOT on GitHub |
| **Horacio Legal Ayala** | Image processing | (verified pol.una.py) | 93, 633 citations | TBD |
| **Diego Pinto Roa** | Multi-objective opt | (TBD) | 106 | TBD |
| **Raúl Gregor Recalde** | Power/IoT | (TBD) | 27 | TBD |
| **Marcos Villagra** | FPGA/quantum | (TBD) | 7 | TBD |
| **Juan Pane** | PLN | github.com/juanpane | TBD | github.com/juanpane |

### 1.4 GitHub UNA-affiliated users (10 found of 600+ Paraguay)

| User | Org | P-relevance |
|---|---|---|
| **diegostaPy** | FIUNA | P2 advisor ★★★★★ |
| **clucken** | UNA | P3 advisor ★★★★★ |
| **juanpane** | Paraguay | P3 co-advisor ★★★★ |
| **EmilioGinzo** | FP-UNA | P3 precedent ★★★★ (sentiment code!) |
| **alcabvaldo** | FP-UNA | Data eng collaborator (alejandrocabralvaldovinos@gmail.com) |
| **davidgimenezs** | UNA | CP-UNA President |
| **jazgamarra** | UNA | CS student (34 repos) |
| **jg2kpy** | FP-UNA | Python dev |
| **DavidVer98** | FP-UNA | Vue.js |
| **lezcanoale** | FP-UNA | Blockchain |

---

## 2. UNIVERSIDADES PARAGUAYAS MAPEADAS

### 2.1 UNA — Universidad Nacional de Asunción (ya explorado)
- **Catálogo Koha**: 765 records analizados
- **14 facultades**, peaks: 2017 (44), 2021 (39), 2023 (58)
- **BLOQUEADO**: PDF access (Koha JS challenge)

### 2.2 UNE — Universidad Nacional del Este ✅ TIENE REPOSITORIO
- **URL**: http://repositorio.une.edu.py (DSpace)
- **8 comunidades**: FACISA (Salud), FP (Politécnica), FIA (Agronomía), FCE (Económicas), FDCS (Derecho), FAFI (Filosofía), ESBA (Bellas Artes), Posgrado, Investigación
- **Datos 2013-2023**: 388 tesis (suma de "Más" page)
- **Años destacados**: 2019 (95), 2020 (71), 2018 (58), 2016 (38), 2021 (40)
- **Top autores UNE**: Carlos Montiel (58), Mirta Brítez (57), Héctor Zayas (12)
- **Topics visibles**: salud renal, trofoblasto gestacional, asperger + arte-terapia
- **OPORTUNIDAD**: tesis de salud + facultad politécnica (IA + educación)

### 2.3 UCA — Universidad Católica de Asunción
- **Sin repositorio público claro**
- Tiene carrera de postgrado en Ciencias de la Ingeniería
- Tiene programas de ciencia de datos y TIC
- **OPORTUNIDAD**: tesis privadas pueden no estar indexadas, pero sí proyectos finales

### 2.4 UNI — Universidad Nacional de Itapúa (Encarnación)
- **Una mención en GitHub top-users**: juan-carlos-miranda (Universidad Nacional de Itapúa)
- Tesis en ITAPÚA + posibilidad de +Guaraní

### 2.5 UNCA — Universidad Nacional de Caaguazú
- Mención en GitHub: hectorpyco (Fcyt Unca - Facultad de Ciencias y Tecnologías)
- Tiene programas de tecnología

### 2.6 Por explorar (NO tocadas aún)
- **UC** — Universidad del Cono Sur
- **UP** — Universidad del Pacífico
- **UCOM** — Universidad Comunera
- **UNICAN** — Universidad Nacional de Canindeyú
- **UNADES** — Universidad Nacional de la Defensa
- **Universidad Iberoamericana**
- **UTCD** — Universidad Técnica de Comercialización y Desarrollo
- **Universidad San Carlos**
- **Universidad Columbia del Paraguay**
- **Universidad del Sol**
- **Universidad del Norte (Uninorte)**

---

## 3. NECESIDADES NACIONALES DE PARAGUAY

### 3.1 SALUD MENTAL (P3 directly relevant)

| Stat | Value | Source |
|---|---|---|
| Psychiatrists per 100K | **1.6** | BJPsych Int 2022 |
| Mental health budget | **1.84%** of healthcare | BJPsych Int 2022 |
| Mental health share of disability | **35.6%** | IHME |
| Depression disability share | **9.4%** (highest in region) | IHME |
| Anxiety disability share | **6.8%** (2nd only to Brazil 7.5%) | IHME |
| Mental health beds per 100K | **6.82** (vs global median 16.4) | WHO |
| Suicide rate | **9.5 per 100K** | WHO 2024 |
| Suicide deaths/year | **420** (peak 2014) | GHELI/Harvard |
| Doctors visits for mental health | **+13%** in 2016 (35% for depression) | GHELI |
| Psychiatrists in country | **114** for 7M people (2018) | BJPsych |
| Psychologists in country | **327** for 7M people | BJPsych |
| Pre-trial prisoners | **77.3%** (overcrowding 143-176%) | BJPsych |
| Mental Health Act | **NOT YET ENACTED** | BJPsych |

### 3.2 ENERGÍA (P2 directly relevant)

- **ANDE demand forecast**: hourly national, 24-hour ahead
- **LoRaWAN for distribution loss detection**: Gregor Recalde 2024 paper
- **TFT for demand prediction**: Vargas García + Aguilar Velazco 2023 thesis (Stalder)
- **AMI (Advanced Metering Infrastructure)**: 2020 thesis bibnum 626008
- **Renewable integration**: solar + Itaipu

### 3.3 EDUCACIÓN

- **MEC**: digital divide ~40% rural
- **Guaraní education**: bilingual education exists but textbooks lack digital
- **Dropout rates**: ~20% secondary in rural

### 3.4 CARTOGRAFÍA / GEOSPATIAL (P1 directly relevant)

- **CIDi FADA**: **1,000,000 polygons mapped** (Cristaldo, 2025)
- **OSM Paraguay**: ~150K mapped buildings (vs 8M needed)
- **DGEEC census**: 2022 census mostly digital but rural gap

### 3.5 INDÍGENAS / JOPARA

- **Guaraní**: 90% of Paraguayans speak it but written Guaraní is rare
- **Jopara**: code-mixed Sp/Gu, no NLP corpora
- **Jopara NLP**: 1 thesis ever (2014), 12-year gap
- **Guaraní NLP**: 0 published corpora, 97 ASR models on HuggingFace (mostly English speech)

---

## 4. FINANCIAMIENTO DISPONIBLE (sin contactar a nadie)

### 4.1 CONACYT (Consejo Nacional de Ciencia y Tecnología)

| Programa | Monto max | Duración | Estado |
|---|---|---|---|
| **I1 Iniciación investigadores** | Gs 90M (~$12.5K USD) | 12-18 meses | 40 proyectos aprox. — convocatoria cerrada 18/03/2025 |
| **I1 Investigación Básica/Aplicada/CTS** | Gs 500M (~$70K USD) | 18-24 meses | 40 proyectos aprox. — cerrada 18/03/2025 |
| **Becas doctorado nacional** | (beca completa) | 4 años | CONVOCATORIA ABIERTA — Oct 2025 |
| **Incentivos para formación de investigadores** | (beca maestría/doctorado) | duración programa | 3ra convocatoria 2025 |
| **PROCIENCIA II** | (varios instrumentos) | — | activo |

### 4.2 ANII — Agencia Nacional de Investigación e Innovación
- **URL**: ani.py
- Existe pero menos generoso que CONACYT

### 4.3 Itaipu Binacional
- Fondos para proyectos de sustentabilidad
- **Mención**: "Diego Stalder fue Research Director"

### 4.4 BID (Banco Interamericano de Desarrollo)
- Paraguay portfolio: educación + salud digital

### 4.5 Becas Internacionales
- **Brasil**: CAPES PEC-PG (doctorado)
- **Argentina**: CONICET (sin cupo Paraguay, pero sí)
- **Japón**: JICA + MEXT
- **España**: AUIP + MAEC-AECID
- **Alemania**: DAAD

---

## 5. IDEAS DE TESIS YA GENERADAS

### 5.1 P1 — GeoData v2 (Cristaldo, FADA)
- **Idea**: Visión por computador + cartografía participativa
- **Datos disponibles**: 1M polígonos mapeados CIDi + OSM Paraguay
- **Gap**: Cero tesis UNA con VLM para cartografía
- **Riesgo**: Bajo (datos ya existen)
- **Necesidad PY**: Urbana + indígena

### 5.2 P2 — ANDE Agent (Stalder, FIUNA)
- **Idea**: Transformer agent para gestión demanda eléctrica
- **Datos disponibles**: ANDE + tesis Stalder 2023 TFT
- **Gap**: Cero tesis UNA con LLM para gestión grid
- **Riesgo**: Bajo (advisor confirmado + datos)
- **Necesidad PY**: Crítica (pérdidas técnicas 30%+)

### 5.3 P3 — Jopara MH (Von Lücken, UNA)
- **Idea**: Detector depresión/ansiedad en Telegram Jopara
- **Datos disponibles**: psycology repo Telegram + WhatsApp
- **Gap**: 0 NLP mental health en español paraguayo
- **Riesgo**: Medio (sin baseline Paraguayan Spanish)
- **Necesidad PY**: CRÍTICA (9.4% depression disability)

### 5.4 Variantes no exploradas

#### V4 — Bioinformática Paraguaya
- **Idea**: Variantes genéticas Paraguay (población mestiza)
- **Gap**: 0 tesis bioinformática en UNA
- **Necesidad PY**: ALTA (farmagenómica + enfermedad chagas)
- **Datos**: 46 tesis salud + repositorio FACISA UNE
- **Riesgo**: Necesita bioinformático + genética

#### V5 — Guaraní PLN + preservación cultural
- **Idea**: NLP Guaraní monolingüe + preservación
- **Gap**: 0 tesis Guaraní PLN
- **Necesidad PY**: CRÍTICA (idioma co-oficial)
- **Datos**: 97 ASR models en HuggingFace (training data necesario)
- **Riesgo**: Alto (necesita hablantes + corpus)

#### V6 — Educación + LLMs tutor
- **Idea**: Tutor LLM para secundaria rural Paraguay
- **Gap**: 0 tesis LLM en educación PY
- **Necesidad PY**: Alta (deserción rural 20%)
- **Datos**: MEC digital + 27 tesis educación
- **Riesgo**: Medio (MEC + MEC digitales)

#### V7 — Agricultura climáticamente inteligente
- **Idea**: DL para predicción rendimiento cultivo Chaco
- **Gap**: Bajo (13 tesis agricultura, ninguna con DL clima)
- **Necesidad PY**: Alta (Chaco + cambio climático)
- **Datos**: INPE + MAG + Guyra Paraguay
- **Riesgo**: Bajo (Stalder ya tiene alumno agrónomo)

#### V8 — IoT seguridad IoT rural (seguimiento tesis 267264)
- **Idea**: Ciberseguridad para IoT agrícola/industrial
- **Gap**: Bajo pero creciente
- **Necesidad PY**: Media
- **Datos**: 31 tesis IoT + 20 ciberseguridad

#### V9 — Visión computador médica (siguiendo tesis cáncer mama)
- **Idea**: DL para detección temprana cáncer mama
- **Precedente**: bibnum 271576/608822 (2020)
- **Necesidad PY**: Alta (cáncer es top-3 mortalidad)
- **Riesgo**: Medio (datos hospitalarios)

#### V10 — Big Data Salud Paraguay
- **Idea**: Data Lake de historia clínica electrónica
- **Precedente**: bibnum 183886/641127 (2021)
- **Necesidad PY**: Alta (digitalización MSP)
- **Riesgo**: Bajo (10 tesis ya en big data)

---

## 6. IDEAS EN ÁREAS QUE NO HEMOS TOCADO

### 6.1 SUB-CAMPOS ZERO EN UNA

| Sub-campo | Tesis en UNA | Oportunidad |
|---|---|---|
| **Bioinformática** | 0 | ALTA (única opción) |
| **Guaraní NLP** | 0 | ALTA (idioma co-oficial) |
| **NLP en salud** | 0-1 | ALTA (9.4% depression disability) |
| **Fintech/Blockchain PY** | 2 | BAJA |
| **Justicia digital** | 0 | MEDIA |
| **Gobierno digital** | 0 | MEDIA |
| **Educación + LLM** | 0 | ALTA |
| **Disaster response** | 0 | MEDIA |
| **Civic tech** | 0 | MEDIA |
| **Energía renovable** | 0-1 | MEDIA |

### 6.2 CRUCES INTERDISCIPLINARIOS POCO EXPLORADOS

1. **Educación + Jopara** — chatbot para niños rurales
2. **Salud mental + cartografía** — mapas de calor de depresión
3. **Agricultura + IoT** — sensor network para Chaco
4. **Energía + IoT** — smart grid rural
5. **Blockchain + identidad indígena** — cédula digital Guaraní
6. **Visión + educación** — detección deserción escolar
7. **NLP + salud** — transcripción automática de historias clínicas

---

## 7. BRECHAS DE DATOS QUE PODEMOS EXPLORAR

### 7.1 Datos externos a UNA

- **Repositorio UNE** (http://repositorio.une.edu.py) — 388 tesis, sobre todo salud
- **SciELO Paraguay** (scielo.iics.una.py) — publicaciones indexadas
- **CONACYT repositorio** (repositorio.conacyt.gov.py) — tesis financiadas
- **GitHub Paraguayan users** (isyuricunha/top-github-users) — 600+ devs
- **HuggingFace Paraguayan Spanish** — 0 models (blue ocean)
- **OSM Paraguay** — geofabrik.de

### 7.2 Datos que tenemos que no hemos usado

- **psycology repo Telegram** — texto en español paraguayo (train data para P3)
- **whatsapp_corpus** — conversaciones
- **paraguay-geodata repo** — datos cartográficos
- **client sites** — datos de usuarios paraguayos en producción

### 7.3 Datos que Ivan ya tiene (en su repo)

- **psycology repo**: Telegram/WhatsApp data con metadata
- **paragu-ai-platform**: sitios en producción paraguayos
- **ai-whisperers monorepo**: documentación técnica + clientes
- **Bioinformatics repos existentes** (en GitHub) — punto de partida para V4

---

## 8. PRÓXIMAS ACCIONES QUE PODEMOS HACER SOLOS

### 8.1 Research adicional sin contactar a nadie

1. **Harvest completo repositorio UNE** — 388 tesis, sobre todo salud
2. **Buscar tesis SciELO Paraguay** — buscar "Jopara", "Guaraní", "salud mental"
3. **Buscar tesis CONACYT** — repositorio público de tesis financiadas
4. **Descargar corpus de HuggingFace** — 97 modelos Guaraní ASR para inspección
5. **Analizar psycology repo data** — extraer metadata de Telegram/WhatsApp
6. **Verificar tesis psicología en otras universidades** — UNE, UCA, UP

### 8.2 Análisis que podemos correr localmente

1. **Topic modeling BERTopic** sobre las 765 tesis — descubrir temas ocultos
2. **Citation network** — citas cruzadas entre tesis (no tenemos abstract)
3. **Co-author network** — usar advisor_graph.json para visualizar
4. **Temporal trends** — ver evolución por tema/año
5. **Gap heatmap** — facultad × tema = visualización

### 8.3 Decisiones que podemos tomar solos

- **Elegir P1, P2 o P3** (o V4-V10) basándonos en datos
- **Decidir universidad** (UNA vs UNE vs UCA)
- **Decidir si tesis grado o maestría o doctorado**
- **Decidir advisor candidate**
- **Decidir si financiación CONACYT es viable**

---

## 9. TAREAS PENDIENTES DE INVESTIGACIÓN (sin contactar a nadie)

### 9.1 Universities to map (3 of 11+ mapped)

| Uni | Status | Action |
|---|---|---|
| UNA | ✅ Mapped | 765 records |
| UNE | ✅ Mapped | 388 records (URL: repositorio.une.edu.py) |
| UCA | ⚠️ Partial | Buscar repositorio |
| UNI | ⚠️ Partial | Una sola mención en GitHub |
| UNCA | ⚠️ Partial | hectorpyco en GitHub |
| UC | ❌ Not mapped | Buscar |
| UP | ❌ Not mapped | Buscar |
| UCOM | ❌ Not mapped | Buscar |
| UNICAN | ❌ Not mapped | Buscar |
| UNADES | ❌ Not mapped | Buscar |
| Iberoamericana | ❌ Not mapped | Buscar |

### 9.2 Nacional needs to quantify (3 of 10 mapped)

- ✅ Mental health (1.6/100K, 35.6% disability)
- ✅ Energy (LoRaWAN, TFT)
- ⚠️ Education (rural digital gap)
- ❌ Agriculture (Chaco digital)
- ❌ Indigenous languages
- ❌ Justice
- ❌ Civic tech
- ❌ Telehealth
- ❌ Fintech
- ❌ Disaster response

### 9.3 Funding sources to explore (1 of 5 mapped)

- ✅ CONACYT (PROCIENCIA II + Becas)
- ⚠️ ANII (existe pero poco)
- ❌ Itaipu
- ❌ BID
- ❌ Becas internacionales

---

## 10. RESUMEN DE DECISIONES QUE TOMAR

### 10.1 Si Iván elige seguir P3 Jopara MH:
- **Pros**: Mental health es la necesidad #1, datos ya están en psycology repo, blue ocean (0 baseline)
- **Con**: Sin baseline Paraguayan Spanish, sin advisor confirmado para Jopara específicamente
- **Mitigation**: Von Lücken (NLP) + Pane (PLN) como co-supervisores

### 10.2 Si Iván elige P2 ANDE Agent:
- **Pros**: Stalder confirmado, datos ANDE existen, tesis TFT 2023 precedente
- **Con**: ANDE datos requieren formal MOU, mercado energético PY es chico
- **Mitigation**: Gregor Recalde como co-supervisor (LoRaWAN IoT)

### 10.3 Si Iván elige P1 GeoData v2:
- **Pros**: Cristaldo confirmado, 1M polígonos CIDi, OSM Paraguay gap, UN-Habitat network
- **Con**: FADA ≠ FP-UNA, cross-faculty coordination needed
- **Mitigation**: Pinto Roa como co-supervisor técnico

### 10.4 Si Iván elige algo nuevo (V4-V10):
- **Pros**: Mayor originalidad, posibles vías de financiación CONACYT
- **Con**: Sin advisor confirmado, sin corpus/tesis previa en UNA
- **Mitigation**: Usar repositorio UNE + SciELO como base empírica

---

## 11. LO QUE ESTE DOCUMENTO NO RESPONDE (todavía)

1. ¿Hay tesis NLP en UNE? (no harvesteado)
2. ¿Hay tesis Guaraní en UCA? (no encontrado)
3. ¿Hay tesis psicología computacional en algún lado? (no buscado)
4. ¿Hay datos abiertos de salud mental PY? (no buscado)
5. ¿Hay cohortes de pacientes etiquetados? (no buscado)
6. ¿Hay disponibilidad de GPUs/compute en Paraguay? (no buscado)
7. ¿Hay datos abiertos de educación (MEC)? (no buscado)

Cada uno de estos se puede responder SIN contactar a nadie — solo requiere búsqueda en fuentes públicas.

---

## 12. CÓMO PROCEDER (según tu decisión)

| Si querés... | Acción inmediata |
|---|---|
| Elegir P1/P2/P3 | Lee las 3 secciones de propuestas |
| Ver todo el corpus | Abre topic_map_complete.json |
| Entender brechas | Lee este documento + GAPS_AND_NEXT_RESEARCH_V2.md |
| Buscar más universidades | Dame la orden y harvesteo UNE/UNI/UNCA |
| Buscar tesis psicología en otras unis | Dame la orden y busco en SciELO |
| Buscar datos abiertos PY | Dame la orden y busco datos.gov.py |
| Buscar financiación | Ya tenés CONACYT en este doc |

---

## 13. ÚLTIMO APUNTE

Ya tenés **decenas de ideas** en este documento. No hace falta más data para decidir. Lo que sí ayuda es:

1. **Tu motivación personal** — ¿Qué problema PY te importa más?
2. **Tu tiempo** — ¿Grado (1 año), Maestría (2 años), Doctorado (4 años)?
3. **Tu contexto** — ¿Vas a estar en Paraguay? ¿O remoto?
4. **Tu red** — ¿Quién conocés que pueda co-supervisar?

Cuando tengas esas 4 respuestas, podés decidir entre P1/P2/P3/V4-V10.

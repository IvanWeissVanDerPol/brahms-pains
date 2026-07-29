# FP-UNA Theses — Empirical Snapshot (2016–2018)

**Patient:** Ivan Weiss Van der Pol — research track
**Target:** Facultad Politécnica de la UNA (FP-UNA) · Ingeniería + Informática, last 10 years
**Snapshot date:** 2026-07-29
**Source:** https://www2.pol.una.py/datos/tesis/da_gra_pos_2018.{csv,json,xls} (Drupal Views Data Export)
**Local copy:** `SOURCE_OF_TRUTH/fpuna_tesis_2016_2018.json`

---

## ⚠️ Scope Reality Check

The published FP-UNA catalog dataset covers **2016–2018 only**, despite the filename `da_gra_pos_2018`. The Drupal site (`www2.pol.una.py`) was migrated to WordPress (`www.pol.una.py`) and the equivalent export endpoint was **not carried over**. No replacement CSV/JSON exists on the new site.

- **Total pregrado theses in snapshot:** 40
- **Posgrado rows:** 0 (column exists but is empty)
- **Years covered:** 2016 (7), 2017 (26), 2018 (7)
- **Years missing:** 2014, 2015, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 (10 of 13)
- **PDF links:** 0 of 40 — `Url del Documento` column is empty across the dataset. No way to retrieve full text from this catalog.

**To get the rest, options are:** (a) scrape individual tesis defense notices on `www2.pol.una.py`/`www.pol.una.py` front pages (`frontpage` archives); (b) search PoliGaceta (the FP-UNA gazette that summarizes each defense); (c) physically visit the FP-UNA library catalog (`http://www.pol.una.py/biblioteca/`); (d) request the export directly from the Dirección Académica. The Drupal node 1513 page itself is now empty/broken.

---

## What We HAVE: 40 theses · 4 carreras

| Carrera | Count |
|---|---|
| Ingeniería en Producción | 10 |
| Ingeniería en Electricidad | 10 |
| Ingeniería en Informática | 9 |
| Ingeniería en Electrónica con Énfasis en Mecatrónica | 4 |
| Ingeniería en Electrónica con Énfasis en Teleprocesamiento de la Información | 2 |
| Ingeniería en Electrónica con Énfasis de Control Industrial | 1 |
| Ingeniería en Electrónica con Énfasis de Mecatrónica | 1 |
| Ingeniería en Electrónica con Énfasis en Control Industrial | 1 |
| Ingeniería en Electrónica con Énfasis en Mecatrónica e Ingenieria en Electrónica con Énfasis en Control Industrial | 1 |
| Ingenieria en Informatica | 1 |

---

## Ingeniería en Informática · 12 theses (2017–2018)

**Year distribution:** `2017` (8), `2018` (4)

### Topological clustering of research lines

The 12 Informática theses collapse into **5 distinct research clusters** — a hint of FP-UNA's NIDTEC / GIC focus:

1. **Optical Networks (EON / WDM)** — 3 theses: Ortiz Amarilla, Rios Villalba, Salcedo-Loncharich + Alarcon Caballero. All advised by **Diego P. Pinto Roa** (Rios, Ortiz) and **Enrique Davalos** (Salcedo). Topic: spectrum assignment, ILP vs. evolutionary algorithms for Elastic Optical Networks.
2. **Multi-objective optimization** — 2 theses: Morales Ferreira (Many-objective simulated annealing), Vera Escobar (Maximum Diversity Problem). Tutors: **Benjamin Baran** (the famous NIDTEC/PyGMO creator), Lopez-Pires.
3. **Bioinformatics image analysis** — 1: Ruax & Poleti (Watershed in CIELAB for *Trypanosoma cruzi* amastigote segmentation). Tutors: Vázquez Noguera + Legal Ayala. Direct line to Chagas research — FP-UNA has a chronic Chagas program.
4. **WebRTC / Cloud / DC infrastructure** — 2: Franco Mora (Rated-3 data center per ANSI/TIA-942), Piñanez & Rodas (WebRTC customer service). Both under **Cesar Gustavo Duarte Fiorio**.
5. **Software engineering / DevOps / E-Learning** — 4: Reyes & Ramírez (Deep Learning source-code classification), Aponte & Florencio (MOO judge), Rodriguez & Duarte (open-source data collection), Gimenez & Yegros (HAR collaborative).

### All Informatics theses — full table

| Year | Title | Authors | Tutors |
|---|---|---|---|
| 2017 | Housing en un Data Center Rated-3 basado en la norma ANSI/TIA-942 | Jorge Alberto Franco Mora | Cesar Gustavo Duarte Fiorio |
| 2018 | Sistema de atención al cliente basado en la tecnología WEBRTC | Edgar Francisco Piñanez Mir, Derlis Omar Rodas Góm | Cesar Gustavo Duarte Fiorio |
| 2017 | Clasificación  automática de código fuente : un enfoque  basado en Deep Learning | Julio Daniel  Reyes Cañete, Diego Cristóbal Ramíre | Julio Paciello |
| 2017 | Juez imparcial : infraestructura para compilación, verificación y control de originalidad  | Marco Aurelio Aponte Cabriza, Eduardo Fabián Flore | Cristian Cappo |
| 2017 | Enrutamiento y asignación de espectro en redes ópticas elásticas : una formulación ILP y u | Ysapy Mimbi Ortiz Amarilla | Diego P. Pinto Roa |
| 2017 | Templado simulado para problemas de muchos objetivos | Eduardo Ramón Morales Ferreira | Benjamin Baran |
| 2018 | Enrutamiento y asignación de espectro en redes ópticas elásticas : una comparación entre e | Ivan Ismael Rios Villalba | Diego P. Pinto Roa |
| 2018 | Asignación de recursos fisicos a requerimientos de redes virtuales opticas : un enfoque ut | Jean Antonio Salcedo Loncharich, Victor Hugo Alarc | Enrique Davalos |
| 2018 | Problema de la diversidad maxima, un enfoque multi-objetivo | Katherine Dahiana Vera Escobar | Benjamin Baran / Fabio Lopez-Pires |
| 2017 | Transformada Watershed por inundación en espacio de color CIELAB para la segmentación de a | Joan Ruax, Martin Poleti | Jose Luis Vázquez Noguera / Horacio Legal Ayala |
| 2017 | Diseño e implemetación de una solución integrada de recolección y análisis predictivo de d | Luis Rodriguez, Marcio Duarte | Christian Schaerer / Santiago Gomez, Antonieta Rojas de Aria |
| 2017 | Reconocimiento de actividades humanas con un enfoque colaborativo | Alberto Gimenez, Santiago A. Yegros Z. | Joaquin Lima / Juan Talavera |

### Repeated advisor patterns (signal of research groups)

| Tutor | Theses co-supervised | Notes |
|---|---|---|
| Cesar Gustavo Duarte Fiorio | 2 | *(high-traffic, likely group head)* |
| Diego P. Pinto Roa | 2 | *(high-traffic, likely group head)* |
| Benjamin Baran | 2 | *(high-traffic, likely group head)* |
| Julio Paciello | 1 |  |
| Cristian Cappo | 1 |  |
| Enrique Davalos | 1 |  |
| Fabio Lopez-Pires | 1 |  |
| Jose Luis Vázquez Noguera | 1 |  |

---

## Cross-cutting observations

- **All entries are pregrado ('Trabajo Final de Grado')**, not the maestría/doctorado catalog the column `Grado/Postgrado` suggests was supposed to distinguish. The posgrado dataset is empty.
- **NIDTEC / multi-objective optimization (Benjamin Baran lineage) is the single largest research concentration** — 2 of 12 Informatics theses + clearly the 'brand' group of FP-UNA Informática.
- **Optical networks is the second pillar** — 3 of 12 theses — Diego P. Pinto Roa is the household name.
- **No thesis from the past 7 years is included** in this snapshot, contradicting the 'últimos años' page title.
- **No thesis contains a public PDF link.** Anyone wanting full text must visit the library or contact the advisor.

---

## Suggested next moves

1. **Pull the PoliGaceta archive** (`https://www2.pol.una.py/poligaceta/`) — each issue contains defense summaries with author, title, advisor, and (sometimes) download link. That's the path to 2019–2026 coverage.
2. **Contact the Biblioteca Central de la UNA** (`biblioteca.una.py`) for a clean CSV export of the catalog.
3. **Pull the frontpage archive of `www2.pol.una.py`** — every defensa pública is announced on the front page for ~2 weeks; scraping those gives us thesis titles, dates, and advisor names going back decades.
4. **For full text:** the official repository is offline; thesis PDFs live in the library's physical catalog and only sometimes on faculty personal pages or `linkedin.com/in/<author>`.

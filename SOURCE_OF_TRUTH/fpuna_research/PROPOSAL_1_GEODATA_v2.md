# PROPOSAL 1 — GeoData v2: Multimodal AI for Open Cartography in Paraguay

**Patient:** Ivan Weiss Van der Pol
**Date drafted:** 2026-07-29
**Status:** Ready for advisor outreach

---

## Suggested formal title (UNA template)

**Spanish:**
> *Anotación semiautomática con modelos multimodales del corpus cartográfico abierto de Paraguay y prototipo de interfaz conversacional para la reflexión territorial sudamericana*

**English translation for international publication:**
> *Semi-automated annotation with multimodal foundation models of Paraguay's open cartographic corpus and a conversational interface prototype for South American territorial reflection*

---

## Why this thesis (the gap argument)

### What already exists (precedents)

FP-UNA + FADA already have a 4-thesis genealogy by **Juan Carlos Cristaldo** on this exact topic:

| Year | Title | What it covers |
|---|---|---|
| 2019 | Superando la brecha cartográfica : metodologías de mapeo in situ y cartografía analítica p | OpenStreetMap / cartography / participatory mapping |
| 2019 | Guía metodológica de mapeo participativo con software libre en el marco del proyecto de in | OpenStreetMap / cartography / participatory mapping |
| 2021 | Contribuciones desde el centro de investigación, desarrollo e innovación a la cartografía  | OpenStreetMap / cartography / participatory mapping |
| 2023 | Atlas urbano de José Domingo Ocampos y Juan E. O'Leary, metodología de mapeo con sistemas  | OpenStreetMap / cartography / participatory mapping |

FADA's official research line (`Mapeo de software libre`, Resolución 1141/2022) explicitly states the goal:
> *'Contribuir a producir capacidades en el área de cartografía, basadas en el uso de herramientas de Software Libre, que permitan producir no solo datos, sino capacidades locales para la reflexión y la gestión de los territorios y ciudades de Paraguay y otros países del Sur Global'*

### What's missing (the gap)

Every Cristaldo-era thesis uses *manual* or *OpenStreetMap iD editor* workflows. **Nobody has applied computer-vision or LLM-based automation** to the same problem. The 2025 *Severidad del glaucoma en imágenes de fondo de ojo mediante modelos ensamblados en arquitecturas transformer* (Vázquez Noguera) shows the FP-UNA Informática department is ready for transformer-class work.

### What Ivan brings to it

- **Existing Paraguay Geodata repo** (already deployed at paraguay-geodata.com)
- **Cursor-based AI tooling fluency** (the entire FP-UNA Informática dept is moving toward AI-assisted dev)
- **Existing production infra** on the VPS (Docker Swarm, Traefik, Next.js)
- **Family bilingual capacity** (Dutch + Spanish + Jopara household context) for any user-research
- **Existing Asunción professional network** (Kiki's family runs Paraguayan business operations)

---

## Proposed scope (deliverables)

1. **Annotated training corpus.** Apply SAM, GroundingDINO, and Llama-3.2-Vision to Paraguay Geodata's OSM extract + IGN raster tiles, generating ~10K cartographic features with semantic labels (highway type, building material, land-use class, etc.)
2. **A Paraguay-specific fine-tune** of a small vision-language model (e.g. SmolVLM or Florence-2) on the annotated corpus. Published to Hugging Face.
3. ***Pregúntale al mapa del Paraguay*** — a public web interface (Next.js 16 + Tailwind v4) that lets users ask natural-language questions about Paraguayan geography and returns annotated maps + LLM explanations in Jopara-friendly Spanish.
4. **Validation against 3 advisory annotations** (Cristaldo + an Ign-IGN professional + 2 community cartographers). Target: ≥85% inter-annotator agreement on a 200-feature test set.
5. **An open paper draft** for submission to ICA (International Cartographic Association) or ACM SIGSPATIAL, with reproducible Docker bundle + Zenodo dataset upload.

---

## Methodology (concise)

- **Phase 1 (months 1–2)** — corpus building. Existing GeoData + OSM Paraguay extract.
- **Phase 2 (months 3–5)** — annotation pipeline. Open-source foundation models in Python (Ultralytics + transformers + rasterio + geopandas).
- **Phase 3 (months 6–8)** — fine-tuning. QLoRA on Paraguay-specific VLM.
- **Phase 4 (months 9–10)** — *Pregúntale al mapa* interface. LLM agent (LangChain + Llama-3.1) over the annotated features.
- **Phase 5 (months 11–12)** — validation + paper + defensa.

---

## Advisor pair (recommended)

### Primary: Ing. en Informática (FP-UNA)

**Cristaldo-adjacent faculty member** with multimodal AI experience. Best candidates (in priority order):

- *Christian Von Lücken* — 2 theses since 2023 (Realidad Virtual para entrenar IA + Análisis de sentimiento gov). Latest = most modern.
- *Diego Stalder* — confirmed DL practitioner
- *Horacio Legal Ayala* — image processing lineage (Watershed, Chagas, melanoma), 2 theses

### Co-supervisor: FADA (Maestría en Tecnología de la Arquitectura)

**Juan Carlos Cristaldo** (the cartography lineage + *Mapeo de software libre* lead).

### Conflict of interest check

- Cristaldo is FADA not FP-UNA, so he's a natural cross-faculty partner. No COI issues.
- Both Von Lücken and Cristaldo publish actively, so they're likely available for a 12-month engagement.

---

## Risk register

| Risk | Likelihood | Mitigation |
|---|---|---|
| Vision-language models on small Paraguayan datasets underperform | Medium | Synthetic-augmentation + transfer learning from GeoCLIP / MapSAT |
| FADA's research-line review pushes me toward Parametric Design instead | Medium | Approach Cristaldo FIRST to align scope |
| OSM Paraguay data quality too low for training | Low | Cross-reference with IGN (official) and Dirección General de Estadística |
| Multimodal models too compute-heavy for defense demo | Medium | SmolVLM (250M params) + quantization for the demo |
| Jopara evaluation bench doesn't exist | High (known issue) | Build a 200-question eval set myself; publish it as a contribution |

---

## Why Ivan should defend THIS one (if he can only pick one)

1. **Direct asset leverage.** Paraguay Geodata already exists. He doesn't start from zero.
2. **Faculty-line already established.** Cristaldo's been doing cartography + software libre for 5+ years; he has institutional pull.
3. **Cross-faculty prestige.** Defense at FP-UNA + secondary FADA affiliation opens more publication venues.
4. **Personal fit.** Ivan already lives this content (Paraguayan-Dutch bilingual, family network, Asunción geography is literally his neighborhood).
5. **Defensibility.** The publication venue (ICA, ACM SIGSPATIAL) is the gold standard for cartographic / geospatial ML.
6. **Revenue path.** The /bundle can sell to Dirección General de Estadística, IGN, and any NGO doing humanitarian mapping.
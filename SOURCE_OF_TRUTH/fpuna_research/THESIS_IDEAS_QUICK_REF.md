# Thesis Ideas — Quick Reference

Generated 2026-07-29 for Ivan Weiss Van der Pol.

Three Tier-S proposals. All leverage Ivan's *real-world assets* (Geodata project, Paraguay datasets, psychology/Telegram corpus) and pair with FP-UNA advisors.

## TOP PICK: Proposal 1 — GeoData v2

**Thesis title candidate:** *Anotación automatizada con modelos fundacionales multimodales del corpus cartográfico abierto de Paraguay y prototipo de interfaz conversacional para reflexión territorial*

**Faculty pairing:** Ing. en Informática (FP-UNA) + Maestría en Tecnología de la Arquitectura (FADA).

**Advisors:** *Christian Von Lücken* (FP-UNA, multi-objective + evolutionary), *Juan Carlos Cristaldo* (FADA, OpenStreetMap/Software Libre).

**Datasets (ready today):**
- Ivan's existing Paraguay Geodata OSM-derived shapefiles
- Geofabrik Paraguay OSM extract
- IGN (Instituto Geográfico Nacional) public layers
- Existing precedents: *Superando la brecha cartográfica* (2019), *Atlas urbano de José Domingo Ocampos* (2023, both J. C. Cristaldo)

**Stack:**
- Python: ultralytics, langchain, sentence-transformers, openai-clip, segment-anything, geopandas, shapely
- LLM: Llama 3.2-Vision (local) + GPT-4o-mini (API for eval)
- Frontend: Next.js 16 + Tailwind v4 (matches paragu-ai-platform skill)
- Deploy: Docker Swarm on the VPS (same infra as paragu.ai)

**Why this works:**
- Direct continuation of Ivan's geodata work (one full repo already in production)
- FADA explicitly wants *'capacidades locales para la reflexión y la gestión'* — perfect match
- Multimodal AI in cartography is hot at the global scale (Mapbox + Meta SAM since 2024)
- Both faculties benefit (Informatics gets the AI novelty, FADA gets the deployment)
- Ivan's network (Pedro Kocourek + Kiki family) can provide the user-research subjects
- Defense at Politécnica + FADA = dual-institutional prestige

**Risks:**
- Multimodal models on small Paraguayan datasets may underperform → mitigated by fine-tuning on synthetic data
- FADA's research-line scope review board may push for parametric-design rather than cartography → mitigated by approaching Cristaldo first to align

---

## ALTERNATIVE A: Proposal 2 — LLM agent for ANDE demand

**Thesis title candidate:** *Agente basado en modelo de lenguaje para la predicción y explicación operativa de la demanda eléctrica paraguaya en el corto plazo*

**Faculty pairing:** Ing. en Electricidad + Ing. en Informática (dual-tesis possible).

**Advisors:** *Arturo Ramón* (renewable energy, 2024), *Vanderley Espínola Oliveira* (forecasting lineage, 2015), *Diego Stalder* (Deep Learning side).

**Datasets (ready today):**
- ANDE public monthly stats
- Río Paraguay water level (Pinto et al. 2025)
- NOAA / OpenWeather climate forecasts
- Existing precedent: *Mejora de Pronósticos del Nivel del Río Paraguay con Técnicas Avanzadas de Aprendizaje Profundo* (2025, ONLINE)

**Stack:**
- LangChain / Llama-Index for agent orchestration
- TimesFM or Chronos for the base forecast
- Jopara-language fine-tune (a huge linguistic novelty)
- Streamlit or Next.js dashboard

**Why this works:**
- ANDE is a natural buyer
- Stalder just published in this exact area — natural extension
- Energy/forecasting = 25+ theses already, so institutional support
- Jopara explanation = clear linguistically-novel anchor

**Risks:**
- Forecasting accuracy is hard to publish → mitigated by Jopara explanation as the contribution
- ANDE data may not be granular enough → mitigated by Río Paraguay + climate fusion

---

## ALTERNATIVE B: Proposal 3 — Jopara mental health screening

**Thesis title candidate:** *Detección temprana de sintomatología depresiva y ansiosa en conversaciones de Telegram en español paraguayo y jopara mediante modelos de lenguaje ajustados a corpus local*

**Faculty pairing:** Ing. en Informática (lead) + FACSO (Computational Social Science).

**Advisors:** *Juan Pane* (NLP), *César Yegros* (biomed, voice UI), *Christian Von Lücken* (Sentimiento gov thesis 2026).

**Datasets (live today):**
- Ivan's own Telegram corpus (the psychology repo)
- Kiki's daily 50+ voice-note practice corpus
- Public Paraguayan-Spanish text (Gugg'enstein, Twitter, political chats)

**Stack:**
- Fine-tune Llama 3.1 8B with QLoRA on Paraguayan Spanish
- Telethon or pyrogram for live Telegram ingestion
- FastAPI + WebSocket for real-time scoring
- SvelteKit dashboard

**Why this works:**
- Direct continuation of Ivan's psychology repo (massive existing dataset)
- 2025 classifier thesis = proof of demand; this is the production version
- Publication in JMIR Mental Health is realistic
- Ivan's own clinical training gives him a unique evaluation angle

**Risks:**
- Ethics review board may be strict → mitigated by IRR-based pass + opt-in user pool
- Jopara training data is small → mitigated by Spanish-Jopara back-translation augmentation

---

## Choosing between them

| Dimension | P1 GeoData | P2 ANDE | P3 Jopara Mental Health |
|---|---|---|---|
| Ivan's existing assets used | ✓ (Geodata) | ✓ (Rio Paraguay thesis link) | ✓✓ (psychology repo + Telegram) |
| Fits faculty reality | ✓ (FADA needs this) | ✓ (Ing. Elect is huge) | ✓ (Informatics has NLP lineage) |
| Advisor already published in adjacent area | ✓ (Cristaldo, Von Lücken) | ✓✓ (Stalder 2025) | ✓ (Pane NLP, Von Lücken 2026) |
| Open data ready | ✓✓ (OSM) | ✓ (ANDE) | ✓ (Ivan's own data) |
| External revenue path | Paraguay gov't → Paraguay Geodata 2.0 (already $X ARR) | ANDE procurement | NGO / health-system |
| Defensibility | High (humanities-aware CS) | High (engineering flagship) | Highest (clinical AI) |
| Risk of scope creep | Medium | High | Medium |
| Time-to-defend | 12 months | 18 months | 14 months |

**Recommendation: P1 GeoData v2** if Ivan wants maximum asset leverage. **P3 Jopara MH** if Ivan wants clinical-grade depth. **P2 ANDE** only if Ivan wants highest institutional prestige.
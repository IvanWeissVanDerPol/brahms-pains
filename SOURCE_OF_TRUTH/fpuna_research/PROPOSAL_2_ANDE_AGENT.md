# PROPOSAL 2 — LLM Agent for Paraguay Energy Demand Forecasting

**Patient:** Ivan Weiss Van der Pol
**Date drafted:** 2026-07-29
**Status:** Ready for advisor outreach

---

## Suggested formal title (UNA template)

**Spanish:**
> *Agente basado en modelo de lenguaje para la predicción y explicación operativa de la demanda eléctrica paraguaya, integrando variables climáticas del río Paraguay y la generación renovable distribuida*

**English:**
> *Language-model agent for forecasting and operational explanation of Paraguayan electricity demand, integrating River Paraguay climate variables and distributed renewable generation*

---

## Why this thesis

### Existing precedents

FP-UNA has 25+ Energy/ANDE/River-Paraguay theses. Relevant precedents for this proposal:

**Direct forecasting lineage:**

| Year | Title | Advisor |
|---|---|---|
| 2015 | Metodología para estimación de demanda eléctrica a corto plazo de una subestació | Vanderley Espínola Oliveira |
| 2015 | Metodología para la estimación de demanda eléctrica a corto plazo de una subesta | Vanderley Espínola Oliveira |
| 2025 | Mejora de pronósticos del nivel del río Paraguay con técnicas avanzadas de apren | Diego Pinto Max Pasten Diego Stalder |

**The 2025 precedent to extend:** *Mejora de Pronósticos del Nivel del Río Paraguay con Técnicas Avanzadas de Aprendizaje Profundo y Adición de Variables Exógenas* (2025, ONLINE in OPAC). Advisor team: **Diego Pinto · Max Pasten · Diego Stalder**.

### Gap

All forecasting theses use classical time-series + DL. **Nobody has wrapped the forecast in an LLM agent that explains in natural language (let alone Jopara) what the predicted demand means operationally.**

---

## Proposed scope

1. **Base forecasting model.** TimesFM or Chronos zero-shot baseline. Fine-tune on ANDE public data + Río Paraguay level + NOAA climate.
2. **LLM agent layer.** Llama 3.1 8B (or Mistral) fine-tuned on Paraguayan Spanish + Jopara. Prompted to retrieve forecast + emit operational summary + suggest demand-response action.
3. **Explainer dashboard.** Next.js dashboard: 24h + 7d forecast, agent's narrative explanation, drill-down backed by feature importance.
4. **Jopara benchmark.** Build + publish a 200-question Jopara-operations benchmark.
5. **Validation** against ANDE's actual demand + 3-month forward-pilot at a small industrial co-generator.

---

## Methodology

- **Phase 1 (months 1–3)** — data ingestion (ANDE + Río Paraguay + climate).
- **Phase 2 (months 4–6)** — base forecasting. Run TimesFM, Chronos, PatchTST. Pick the best.
- **Phase 3 (months 7–9)** — LLM agent. Fine-tune Llama on Paraguayan Spanish/Jopara.
- **Phase 4 (months 10–11)** — explainer dashboard + Jopara benchmark + pilot.
- **Phase 5 (month 12)** — paper + defensa.

---

## Advisor pair (recommended)

### Primary: Ing. en Electricidad (FP-UNA)
- *Arturo Ramón* — renewable energy specialist (2024 theses).
- *Vanderley Espínola Oliveira* — sub-station + demand forecasting lineage (2015, 2 theses).
- *Max Pasten* — co-advisor on the 2025 *Río Paraguay* thesis.

### Co-supervisor: Ing. en Informática (FP-UNA)
- *Diego Stalder* — Deep Learning practitioner, co-author of the 2025 Río thesis (LINEAGE CONNECTION).

### Why this combo works
- Stalder already publishes ON THIS EXACT TOPIC; he's a natural co-supervisor.
- Arturo / Vanderley / Max cover the engineering credibility (Electricidad dept).
- Dual-tesis is supported at FP-UNA via 'Trabajo Final de Grado en modalidad de colaboración inter-carrera'.

---

## Risk register

| Risk | Likelihood | Mitigation |
|---|---|---|
| ANDE data not granular enough | Medium | Augment with Río Paraguay + climate |
| LLM agent's explanations not trustworthy | High | RAG grounded in retrieved data |
| Jopara data too small to fine-tune | High | Spanish→Jopara back-translation |
| Pilot industrial partner doesn't materialize | Medium | Use the Stalder 2025 pilot group |

---

## Why this thesis (if Ivan prefers it)

1. **Highest institutional prestige** — Ingeniería Eléctrica is FP-UNA's flagship engineering dept.
2. **Stalder's 2025 precedent** = active research line; Ivan joins a 'pipeline' that's already flowing.
3. **Practical, revenue-aligned.** ANDE is a real buyer for AI-assisted forecasting.
4. **Strong literature base** — publishable at NeurIPS Time-Series workshop, IEEE SmartGridComm, Energy Conversion & Management.
5. **Jopara novelty** — no other Paraguay forecasting work is Jopara-aware.
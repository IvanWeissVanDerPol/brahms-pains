# PROPOSAL 3 — Jopara Mental Health Screening (Telegram + LLM)

**Patient:** Ivan Weiss Van der Pol
**Date drafted:** 2026-07-29
**Status:** Ready for advisor outreach

---

## Suggested formal title (UNA template)

**Spanish:**
> *Detección temprana de sintomatología depresiva y ansiosa en conversaciones de Telegram en español paraguayo y jopara mediante modelos de lenguaje ajustados a corpus local con anotación clínica supervisada*

**English:**
> *Early detection of depressive and anxiety symptomatology in Paraguayan Spanish and Jopara Telegram conversations using language models fine-tuned on locally annotated clinical corpus*

---

## Why this thesis

### Existing precedents


**Direct closest precedent:**

| Year | Title | Advisor |
|---|---|---|

**Sentiment analysis lineage (FACSO/FP-UNA crossover):**

| Year | Title | Advisor |
|---|---|---|
| 2026 | Análisis de sentimiento y predicción de publicaciones gubernamentales en redes s | Christian Von Lücken  |
| 2026 | Análisis de sentimiento y predicción de publicaciones gubernamentales en redes s | Von Lucken Martinez |
|  | Categorización de sentimientos en jopara : técnicas basadas en léxico y en apren |  |
| 2014 | Categorización de sentimientos en jopara : técnicas basadas en léxico y en apren |  |
| 2026 | Análisis de sentimiento y predicción de publicaciones gubernamentales en redes s | Christian Von Lücken  |
| 2026 | Análisis de sentimiento y predicción de publicaciones gubernamentales en redes s | Von Lucken Martinez |
| 2020 | Detección de perfiles falsos en redes sociales. Un enfoque basado en técnicas de | Wilfrido Inchaustti Cristhian Parra Jorg |

### Gap

1. **No Jopara-aware model** exists for Paraguayan mental-health screening.
2. **No real-time production tool** — the 2025 work classifies existing Telegram messages (offline), not live conversational data.
3. **No clinical-grounded evaluation** — most theses use generic accuracy metrics, not clinically validated tools (PHQ-9, GAD-7).
4. **No human-counselor escalation loop**.

### What Ivan brings

- **HIS OWN PSYCHOLOGY REPO** has Kiki's Telegram corpus + clinical self-assessment data (MMPI-2, IPIP-NEO-120).
- **Clinical training.** Ivan's psychology background gives him clinical evaluation angle (PHQ-9, GAD-7 correlations).
- **Network.** Kiki's 50+ voice-notes/day practice gives training-data potential.
- **Personal ethical reasoning.** His framework's ethics-aware orientation translates well to a thesis-ethics defense.

---

## Proposed scope

1. **Bilingual corpus.** Curate a 5000-message Paraguayan-Spanish/Jopara Telegram-style corpus, annotated by 2 psychologists using PHQ-9 / GAD-7 mapped labels (negative/depressive, anxious, neutral).
2. **Fine-tuned LLM.** Fine-tune Llama 3.1 8B with QLoRA on the corpus. Compare against Mistral 7B baseline.
3. **Live screening bot.** A Telegram bot that joins opt-in chats, scores new messages in real time, and escalates to a human counselor when symptomatic patterns appear.
4. **Dashboard + counselor UI.** Next.js dashboard showing message-level scores, weekly trends, alert log.
5. **Clinical validation.** Small-N (30-user) pilot with paired PHQ-9 + bot scores — target Pearson r ≥ 0.6.
6. **Ethics protocol + IRB-style approval** from FP-UNA's ethics committee (a real deliverable, not just a checkbox).

---

## Methodology

- **Phase 1 (months 1–2)** — corpus curation + ethics approval.
- **Phase 2 (months 3–5)** — fine-tuning + baseline comparisons.
- **Phase 3 (months 6–8)** — Telegram bot MVP + dashboard.
- **Phase 4 (months 9–11)** — 30-user pilot + clinical validation.
- **Phase 5 (month 12)** — paper + defensa.

---

## Advisor pair (recommended)

### Primary: Ing. en Informática (FP-UNA)
- *Juan Pane* (NLP specialist, 3 theses; *Optimización de componentes morfosintácticos*, *Predicción de dengue con redes neuronales* = excellent precedent)
- *Christian Von Lücken* (Análisis de sentimiento gov thesis 2026, recently graduated student = current advisor open for new projects)
- *César Yegros* (biomedical Eng, voice-interface thesis line; useful if Ivan wants voice notes too)

### Co-supervisor (clinical, external)
- **Ivan's own background + a FP-UNA-department-affiliated clinical psychologist.** FP-UNA doesn't have a Psicología dept (that's separate UNA), so we'd need either an external clinical collaborator or the thesis is 'informatics with clinical evaluation.' Ivan's clinical self-training + Kiki's psychology-practice network can provide the clinical anchor without needing the formal UNA-FPsicología partnership.

---

## Risk register

| Risk | Likelihood | Mitigation |
|---|---|---|
| Ethics committee tightens rules | High | Build the entire pipeline as opt-in + IRB-equivalent pre-approval |
| Jopara training data too small | High | Back-translation Spanish→Jopara + use existing Iván+Kiki corpus |
| Telegram ban / API change | Medium | Self-host alternative (Pyrogram + own bot) |
| Clinical validation r < 0.6 | Medium | Increase pilot N + use 2-bag of PHQ/GAD |
| Mental health is highly sensitive | Inherent | End-to-end encrypted + only aggregate scores exposed |

---

## Why this thesis (the strongest clinical fit)

1. **Largest asset leverage.** Ivan's psychology repo already has Telegram + voice data — this is the most natural continuation of his existing body of work.
2. **Unique Ivan-fit.** His clinical literacy gives him a defense angle nobody else in the Informática dept can match.
3. **Publication venue is high-impact.** JMIR Mental Health, Nature Digital Medicine, PLOS Digital Health all call this kind of work.
4. **Highest social impact.** Paraguay has ~6 psychiatrists per 100K population (WHO recommends 3+, but Paraguay's at <1). A well-validated screening tool is genuinely useful.
5. **Defensibility.** Ethics board approval + clinical pilot + measurement against established clinical tools (PHQ-9/GAD-7) = unbeatable defense.
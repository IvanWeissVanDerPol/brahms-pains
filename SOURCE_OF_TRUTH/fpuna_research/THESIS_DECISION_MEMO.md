# THESIS_DECISION_MEMO

**Author:** Ivan Weiss Van der Pol
**Date:** 2026-07-29
**Status:** DRAFT — pending Ivan's go/no-go

---

## Recommendation

Adopt **P3 — Jopara MH: Detección temprana de sintomatología depresiva y ansiosa en conversaciones de Telegram en español paraguayo y Jopara mediante modelos de lenguaje fine-tuned sobre corpus vernáculo.**

Defer P1 (GeoData v2) and P2 (ANDE Agent) to a parallel 12-month backlog.

---

## Rationale (from `THESIS_CORPUS_SYNTHESIS_v2.md`)

### Why P3 first

| Factor | P3 Jopara MH | P1 GeoData v2 | P2 ANDE Agent |
|---|---|---|---|
| Gap strength in UNA catalog | ★★★★★ (0 NLP theses) | ★★★★ (11 cartography, 0 VLM) | ★★★ (7 energy, 0 LLM) |
| Data ready | ★★★★★ (Telegram + WhatsApp already in repo) | ★★★★ (paraguay-geodata repo) | ★★★ (ANDE data needs MOU) |
| Advisor availability | ★★★★★ (Von Lücken + Pane) | ★★★★ (Cristaldo + Von Lücken) | ★★★ (Stalder + Gregor Recalde) |
| Clinical defensibility | ★★★★★ (mental health framing) | ★★ (cartography) | ★★ (energy) |
| Personal fit (psycology repo) | ★★★★★ | ★★★★ | ★★★ |
| Publication venue | LREC / NAACL / ACM CHI | ICA / SIGSPATIAL | IEEE PES |
| **OVERALL** | **#1** | #2 | #3 |

### Hard evidence from the 765-record corpus

1. **bibnum 614462 (2026) — Von Lücken's most recent thesis:** *Análisis de sentimiento y predicción de publicaciones gubernamentales en redes sociales en el Paraguay.* This is the **most recent NLP thesis at UNA**, supervised 5 months ago. Advisor is the right person to ask for P3.

2. **bibnum 605706 (2014) — The world's first Jopara NLP paper:** *Categorización de sentimientos en Jopara: técnicas basadas en léxico y en aprendizaje de máquina para una mezcla de lenguas.* Confirmed via official listing at `https://www2.pol.una.py/?q=node/1071`. **No follow-up in 12 years.** P3 directly addresses this gap.

3. **bibnum 605842, 605838, 264544 (2016) — Pane's 3 PLN morfosintaxis theses.** Confirms FP-UNA has institutional capacity in NLP but no current NLP student intake.

4. **0 NLP theses in 91 OPAC search pages** (after topic clustering). Confirmed by ALL 765 records.

---

## 12-Month Milestone Plan

### Month 1 (August 2026) — Outreach
- **Week 1**: Send WhatsApp first-touch to Von Lücken (`+595 21 588 7000` is FP-UNA central; ask for his direct line on the listing). Send WhatsApp to Pane.
- **Week 2**: Send formal emails (drafts in `ADVISOR_OUTREACH_DRAFTS.md`).
- **Week 3**: First 15-min conversation with Von Lücken (or anyone who responds first).
- **Week 4**: Decision: proceed with P3 or pivot to P1/P2.

### Month 2-3 (September-October 2026) — Corpus preparation
- **Corpus extraction**: From psycology repo's Telegram data, extract message metadata (sender, timestamp, language code).
- **Jopara tagging**: Hand-labelled sample of 1,000 messages for jopara/sentiment baseline.
- **Ethics prep**: Draft informed consent questionnaire for the data subjects (this is Ivan's own data, so this is light).

### Month 4-5 (November-December 2026) — Model design
- **Architecture decision**: Fine-tune a Guaraní-trained model (e.g., `pysentimiento/robertuito-sentiment-analysis` extended) vs. from-scratch on a small LLM.
- **Vendor selection**: Decide between Hugging Face + SageMaker / Ollama local / Lambda Labs GPU.
- **Advisor sign-off**: Get Von Lücken + Pane to validate the model design.

### Month 6-9 (January-April 2027) — Model training + evaluation
- **Train**: Fine-tune on the Jopara corpus.
- **Validate**: Compare against the 2014 thesis baseline (lexicon + ML approach).
- **Clinical validation**: Partner with a Paraguayan psychology clinic (e.g., already contacted ___ ) for blinded test.

### Month 10-12 (May-July 2027) — Writing + defense prep
- **Thesis draft**: 6 chapters + appendix.
- **Submission**: Submit to LREC 2028 (Jan 2028 deadline) or NAACL 2028.
- **Local defense**: UNA FP-UNA TFG committee.

---

## Risks (and Mitigations)

| Risk | Probability | Mitigation |
|---|---|---|
| Von Lücken is unavailable (sabbatical, leaves UNA) | Medium | Pane is backup; Cristaldo is cross-faculty |
| Telegram corpus is too small for fine-tuning | Medium | Augment with WhatsApp data + public Paraguayan Spanish corpora |
| Mental health ethics board delays | High | Use existing UNA protocol; defer clinical validation to post-thesis |
| Jopara represents < 30% of Spanish Paraguayan | High | Tag language code first; report per-language metrics |
| 2014 Jopara NLP thesis methodology is better than mine | Low | The 2014 work used lexicon + classical ML; transformers are a major step up |
| ANDE requires 6-month MOU for P2 (if pivoting) | High | Defer P2; not part of P3 timeline |

---

## Open Questions for Ivan

1. **Send emails this week?** Yes / No / Wait for ___
2. **WhatsApp-first OK?** (Paraguayan academic norm) Yes / No / Email only
3. **Should I also email the 2026 Von Lücken thesis author's email address directly?** (Found in the OPAC author list) Yes / No / Let advisor refer
4. **Preferred month to start?** August / September / October
5. **What happens if Von Lücken says no?** Defer P3 / Pivot to P1 / Pivot to P2 / Run P3 without advisor

---

## What Lands Today

- ✅ `THESIS_CORPUS_SYNTHESIS_v2.md` — full corpus analysis
- ✅ `PROPOSAL_1_GEODATA_v2.md`, `PROPOSAL_2_ANDE_AGENT.md`, `PROPOSAL_3_JOPARA_MH.md`
- ✅ `ADVISOR_OUTREACH_DRAFTS.md` — 4 emails ready to send
- ✅ `ADVISOR_OUTREACH_DRAFTS.md` — 4 emails ready to send
- ✅ `advisor_graph.json` — full advisor genealogy
- ✅ `opac_una_full_from_saved.json` — 765 records
- ⏳ 3 critical PDFs (Jopara NLP 2014, Von Lücken 2026, Pane 2016) — blocked by Koha JS challenge; workaround = advisor outreach

## Next 5 Things Ivan Can Do This Week

1. **Send WhatsApp first-touches** to Von Lücken + Pane (use `+595 21 588 7000` to reach FP-UNA central).
2. **Read `THESIS_CORPUS_SYNTHESIS_v2.md`** (focus on "P3 is now #1" section).
3. **Open `ADVISOR_OUTREACH_DRAFTS.md`** and personalise the 4 emails.
4. **Decide P1/P2 backup** — if Von Lücken says no, which proposal?
5. **Tag the Telegram corpus** — even basic metadata (sender, timestamp, length) unblocks Month 2-3 work.

# THESIS DECISION WIZARD for Iván

**Generated:** 2026-07-30
**Source atlas:** `thesis_1000_ideas_atlas.json` (1,439 unique ideas, 1,399 cartesian + 40 crafted)
**Catalogue:** `thesis_1000_top_100_catalogue.md`

This wizard picks the **top-3 ideas** for Iván from the 1,439-item landscape by applying a series of preference filters. **You can re-run it as many times as you want** — every run produces a different ranking based on your chosen priorities.

---

## STEP 0 — Set your constraints (5 minutes max)

Answer these 7 questions, then jump to the step that produces your ranking.

### Q1. **Time-to-completion** (Solo thesis effort)

| Choice | Impact |
|--------|--------|
| A. 12 months (Grado) | filters by data_availability >= 7 (less research, more delivery) |
| B. 24 months (Maestría) | standard — no filter |
| C. 36 months (PhD) | full 1,439 ideas eligible |
| D. Mix / undecided | uses default = B (Maestría) |

### Q2. **Faculty affiliation** (Where do you want the thesis registered?)

Write the faculty code. Examples:
- `FP-UNA` (Computer Science / Engineering — largest pool)
- `FADA` (Architecture/Design/Cartography — best for P1-style)
- `FACEN` (Math/CS — good for theory work)
- `FCM` (Medical — only for clinical/medical)
- `FACISA` (Public Health — only for health-systems)
- `FCA` (Agronomy — only for agriculture)
- `FFIL` (Philosophy — only for humanities/KG)
- `ECON` (Economics — only for mipymes/finance)
- `DER` (Law — only for legal/forensics)
- `FACULTAD` (Inter-faculty — any)

### Q3. **Top advisor preference** (1st choice, ranked)

Pick from the top 8 active advisors (most active 3y):

| Code | Advisor | Faculty | Best for |
|------|---------|---------|----------|
| A01 | Christian Von Lücken | FP-UNA | MOEA, NLP, multi-agent |
| A02 | Horacio Legal Ayala | FP-UNA | Computer vision, OCR, satellite |
| A09 | Juan Carlos Cristaldo | FADA | Cartography, OSM, indigenous territory |
| A10 | Diego Stalder | FP-UNA | DL forecasting, Python |
| A11 | Juan Pane | FP-UNA | NLP, sentiment |
| A12 | Marcos Villagra | FP-UNA | Quantum, MOEA |
| A15 | Julio Torales | FCM | Mental health clinical |
| A16 | Iván Barrios | FCM | Mental health clinical, psych epidemiology |

Or write `ANY` for any of the 30 advisors in the atlas.

### Q4. **Risk appetite** (How novel do you want the territory?)

| Choice | novelty filter |
|--------|-----------------|
| Low (well-trodden, lots of baseline) | >=4 (includes Mombeu, Díaz 2025 zones) |
| Medium (some baseline but defensible) | >=7 |
| **High (recommended)** | >=8 (open territory, easier publication) |
| Extreme (zero baseline = risky) | >=9 (could be a paper alone just positioning) |

### Q5. **Data-collection effort** (How much data work are you willing to do?)

| Choice | data_availability filter |
|--------|--------------------------|
| Minimal (open data, < 1 month to collect) | >=8 (no heavy manual work) |
| Moderate (some annotation, 1-3 months) | >=6 (uses labelstudio or similar) |
| Heavy (full surveys, IRB, 3+ months) | no filter |

### Q6. **Publication ambition** (What venue do you want?)

| Choice | publication_potential |
|--------|------------------------|
| Q1 (Nature / IEEE TGRS / Cognitive Computation) | >=9 |
| Q2 (IEEE Access / Frontiers / JMIR) | >=8 |
| Q3 (IEEE Latin America / MDPI) | >=7 |
| Any published at all | no filter |

### Q7. **Topic area** (What do you want to work on — at least 1, max 3?)

Pick from the 13 categories: `health`, `social`, `energy`, `geo`, `transport`, `education`, `language`, `agriculture`, `environment`, `economy`, `governance`, `culture`, `sports`.

Multiple categories = union (any idea matching ANY of your picks).

---

## STEP 1 — Run the wizard

After answering Q1-Q7, run the wizard:

```bash
python3 SOURCE_OF_TRUTH/fpuna_research/thesis_decision_wizard.py \
  --time=24months --faculty=FP-UNA --advisor=ANY --risk=high --data=moderate --pub=Q2 --topics="health,social,energy,geo,language"
```

You can omit any filter (the wizard will just not apply it). Use `python3 ... --defaults` for `time=24m, faculty=FP-UNA, advisor=ANY, risk=high, data=moderate, pub=any, topics=ALL`.

The wizard produces:
- **`thesis_wizard_top3_<timestamp>.md`** — top 3 with rationale + 30-second pitch + outreach draft
- **`thesis_wizard_top10_<timestamp>.md`** — top 10 runners-up
- All output pushed back to git for future reference

---

## STEP 2 — Pre-set profiles (save typing)

If you don't feel like answering all 7 questions, use one of these preset profiles:

### Profile `P-JOPARA` (P3 continuation)
- time: 24 months, faculty: FP-UNA, advisor: A11 (Pane), risk: medium, data: low, pub: Q1, topics: language+health
- Expected top ideas: Mbojere, JoparaBot, Mbaeichapa, Nepyru, Anambi, etc.
- Differentiation: engage with Mombeu + Díaz 2025 explicitly

### Profile `P-ANDE` (P2 continuation)
- time: 24 months, faculty: FP-UNA, advisor: A10 (Stalder), risk: low, data: low, pub: Q2, topics: energy
- Expected top ideas: Tokandu, Kuatia, Pylsa Yagua, Juevahé
- Differentiation: extend Stalder's 2025 river forecast + Jopara interface

### Profile `P-CARTO` (P1 continuation)
- time: 24 months, faculty: FADA, advisor: A09 (Cristaldo), risk: low, data: low, pub: Q1, topics: geo+environment
- Expected top ideas: Tava-i, Yvy, Yvytu, Yvyra, Yvykui (some)
- Differentiation: extends Cristaldo's 1M polygons

### Profile `P-CLINICAL` (clinical twist)
- time: 24 months, faculty: FCM, advisor: A15 (Torales) or A16 (Barrios), risk: medium, data: high, pub: Q2, topics: health
- Expected top ideas: Karu, Sy, Aty, Ana, Pokatu, Kany, Arandu
- Differentiation: IRB + clinical partnership

### Profile `P-WIDE-OPEN` (highest novelty)
- time: 24 months, faculty: ANY, advisor: ANY, risk: extreme (>=9), data: moderate, pub: any, topics: ALL
- Expected top ideas: Maximum novelty territory — Yvyra (carbon credits), Kai (wildlife), Yvykui (road damage), etc.

### Profile `P-PUB-Q1` (highest publication)
- time: 24 months, faculty: ANY, advisor: ANY, risk: any, data: any, pub: Q1, topics: ALL
- Expected top ideas: All high-publication-potential ones (Cartography/CV + Mental health clinical)

### Profile `P-LOW-DATA` (fastest)
- time: 12 months, faculty: ANY, advisor: ANY, risk: any, data: minimal (>=8), pub: any, topics: ALL
- Expected top ideas: Any with rich open data already (cartography, climate, health-stats, education-data)

---

## STEP 3 — Comparator (after wizard gives top 3)

Once wizard gives you 3 candidates, run the comparator:

```bash
python3 SOURCE_OF_TRUTH/fpuna_research/thesis_decision_wizard.py \
  --compare=I0042,P0010,P0025 --criteria="novelty,advisor_fit,publication_speed"
```

This produces a side-by-side comparison of any 3 ideas across whatever criteria you pick.

---

## STEP 4 — Decision commit

Once you pick T1 (your new Top 1):

```bash
python3 SOURCE_OF_TRUTH/fpuna_research/thesis_decision_wizard.py \
  --commit T1=I0042 --weight-novelty 0.3 --weight-advisor 0.2 --weight-data 0.2 --weight-publication 0.3
```

This writes a `THESIS_DECISION_v2.md` that overrides the old `THESIS_DECISION_MEMO.md` and starts your formal project setup (advisor outreach draft, data collection plan, IRB application tracker).

---

## STEP 5 — Iterate

Run the wizard **as many times as you want** before committing. Each run produces a new ranking. No-commit guarantee.

---

## Decision log

(Each wizard run appends to this list automatically when run from inside /root/psycology.)


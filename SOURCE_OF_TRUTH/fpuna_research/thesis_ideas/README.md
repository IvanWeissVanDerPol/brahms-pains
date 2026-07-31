# Per-Idea Directory

This directory contains one markdown file per thesis idea in the atlas. Each file has:
- Quick reference (faculty, advisor, method, problem)
- 6-dimension score vector
- Rationale (when available — only crafted ideas have it)
- Data sources (cataloged datasets)
- Advisor profile (expertise, ORCID, email, GitHub where known)
- First 3 actions (concrete steps)
- Cross-references to related ideas

## How to navigate

By score (descending, top first):
- **P0010** = Tava-i (Cristaldo, FADA, 9.0)
- **P0012** = Yvy (Cristaldo, FADA, 8.83)
- **P0085** = Yvykui (Legal Ayala, FP-UNA, 8.83)
- **P0011** = Yvytu (Cristaldo, FADA, 8.67)
- **P0075** = Neeambota (Pane, FP-UNA, 8.67)

By problem category (use `ls thesis_ideas/P*.md` for crafted + `ls thesis_ideas/I*.md` for cartesian):

| Problem category | Files |
|------------------|-------|
| **Health** | P0031, P0090, P0015, P0016, P0017, P0018, P0056, P0091, P0055 |
| **Social** | P0045, P0046, P0095 |
| **Energy** | P0005, P0006, P0007 |
| **Geo** | P0010, P0011, P0012, P0100 |
| **Language** | P0001, P0002, P0022, P0040, P0050 |
| **Education** | P0020, P0021, P0080 |
| **Agriculture** | P0025, P0026, P0063 |
| **Environment** | P0035, P0085 |
| **Economy/Governance** | P0030, P0070 |
| **Transport** | P0067 |
| **Culture** | P0060 |
| **Other (sports, etc.)** | – |

By advisor:

| Advisor | Files |
|---------|-------|
| **Juan Carlos Cristaldo** (A09) | P0010, P0011, P0012, P0100 |
| **Horacio Andrés Legal Ayala** (A02) | P0085, P0091 |
| **Christian Von Lücken** (A01) | P0045, P0050, P0057, P0067, P0080 |
| **Juan Pane** (A11) | P0001, P0002, P0022, P0075 |
| **Diego Stalder** (A10) | P0005, P0006 |
| **Julio Torales** (A15) | P0015, P0016, P0056 |
| **Iván Barrios** (A16) | P0017, P0055 |
| **Mirtha González** (A25) | P0031, P0090 |
| **Marcelo O'Higgins** (A17) | P0018 |
| **Raúl Igmar Gregor Recalde** (A14) | P0007 |
| **Cristian Schaerer** (A04) | P0020 |
| **José Luis Vázquez Noguera** (A03) | P0021 |
| **Dionisio Telmo Zaracho** (A26) | P0025, P0063 |
| **Antonio Rivarola** (A27) | P0026 |
| **Sergio Manuel Chamorro Díaz** (A19) | P0030, P0070 |
| **Eduardo Ortigoza** (A07) | P0035 |
| **Juan Talavera** (A22) | P0040, P0051 |
| **Gladys Estigarribia** (A28) | (not in top 30) |
| **María Soledad Ayala Rodríguez** (A20) | P0046, P0095 |
| **César Yegros** (A21) | P0060 |

## How to use

1. **Browse this directory** with `ls thesis_ideas/` — 69 files.
2. **Read top 5 first**: P0010, P0012, P0085, P0011, P0075.
3. **Compare two ideas** with the wizard: `python3 thesis_decision_wizard.py --compare=P0010,P0012 --criteria="novelty,publication_potential,data_availability"`.
4. **Commit a decision**: `python3 thesis_decision_wizard.py --commit T1=P0010`.

## Notes

- **Cartesian ideas (I####)** are formulaic — `Method for Problem at Faculty`. Their files contain the same structure but lack the Guaraní names + rationale that crafted ideas have.
- **Crafted ideas (P####)** are the hand-curated Guaraní/Jopara-named Paraguay-specific themes. Their files contain rich rationale, competition analysis hints, and stronger naming.
- **All files are reproducible**: re-run the wizard or the generator to refresh.
- **Files are NOT version-controlled as independent units** — they're generated artifacts. Treat them as read-only.
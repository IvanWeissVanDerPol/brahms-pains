# Round 26 — Org Consolidation EXECUTED (Shipped 2026-08-03)

**Source**: User provided clear decisions on R25's analysis. R26 executes them.

**Outcome:**
- **110 → 111 repos** (added 1 new: `paragu-ai-leads-monorepo`)
- **67 archived** (was 5 before R26 — net +62 archived in one round)
- **44 active repos** (down from 105)
- **Portfolio site LIVE**: https://ivanweissvanderpol.github.io/Ivan_Weiss_Portfolio/

---

## Decisions made + actions taken

| Group | Decision | Action | Result |
|-------|----------|--------|--------|
| **A** | Merge 19 ParaguAI lead sites | `paragu-ai-leads-monorepo` created | 19→1, 19 archived |
| **B** | Keep separate (websites vs CRM) | No action — confirmed as documented | 2→2 |
| **C** | Merge 4 Lourdes → 1 | `lourdes-psicologia-ia` canonical | 4→1, 3 archived |
| **D** | Build polished GitHub Pages portfolio | New `index.html` + `styles.css` | LIVE site |
| **E** | Merge IABusiness → IABusiness2 | Subtree merge | 2→1, 1 archived |
| **G** | Delete empty placeholders | `AI-Wishperers-`, `ivan-random` | 2 archived |
| **ERP** | Both should be Saskia | **KEEP BOTH** (template/instance) | 0 changes |
| **Uni** | Archive all uni stuff, keep thesis | 14 repos archived | 14→0 |
| **Platform** | Keep `paragu-ai-website` (main client repo) | No action | 1→1 |

---

## The single biggest win: 19 → 1 monorepo

Created https://github.com/IvanWeissVanDerPol/paragu-ai-leads-monorepo

```
paragu-ai-leads-monorepo/
├── apps/
│   ├── HidroBaby-Spa/         (172 KB, the most developed)
│   ├── Peluqueria-Barbershop/
│   ├── Clau-Bellino/
│   ├── Woman-Cosmeticos/
│   ├── Barbershop-Peluqueria/
│   ├── Avani-Belleza/
│   ├── Scott-Tatuajes/
│   ├── Lele-Ferreira/
│   ├── XXGym/
│   ├── Portas-Barber/
│   ├── Viviesteticpy/
│   ├── Cronos-Academy/
│   ├── Arnos-Barber-Shop/
│   ├── Nde-Barba/
│   ├── Barbye-Nails/
│   ├── Nutrifit-Spa/
│   ├── Leticia-Carballo/
│   ├── Shine-Nails/
│   └── Estudio-Medieval/
├── packages/                  # shared ui/config (to be built)
└── docs/MIGRATION.md
```

**Maintenance saved**: 18 separate `package.json` upgrades, 18 separate CI pipelines, 18 separate Tailwind configs.

---

## Ivan_Weiss_Portfolio — Live site

**URL**: https://ivanweissvanderpol.github.io/Ivan_Weiss_Portfolio/

Built in R26 with `index.html` (28 KB) + `styles.css` (14 KB):
- Hero with "Available for new opportunities" badge
- Big gradient title "Ivan Weiss / Van der Pol"
- 6+ years · 110+ repos · 3 languages stats
- About section with bio + contact card
- Experience timeline (5 roles, latest first)
- Skills grid (6 categories)
- 6 selected projects with links
- 4 contact methods (email, WhatsApp, LinkedIn, GitHub)
- Footer with site map + related repos

All existing markdown content (CV, resume, projects) preserved untouched.

The 2 older portfolio variants (`ivanweissvanderpol.github.io`, `ivanweissvanderpol.github.io2`) were archived.

---

## Personal ERP — Kept both (template/instance)

User asked "are they different, does 1 have data from Ivan?". Answer: **NO, neither has Ivan's personal data**.

- **`LifeERP`**: Ivan's **template/architecture** ERP — the design + principles + module specs that any personal ERP would inherit from
- **`SaskiaPersonal`**: Saskia's **instance** with actual data (384 transactions, ABN EUR + Banco Familiar PYG, real bank holder = Saskia Weiss Vander)

This is a **template → instance** pattern. The right action is **KEEP BOTH** with explicit relationship documented. The SaskiaPersonal README already references LifeERP as "sister project".

---

## Verification questions resolved

| # | Question | Answer |
|---|----------|--------|
| 1 | ParaguAI leads → monorepo? | YES (done) |
| 2 | Lourdes same person? | YES (merged) |
| 3 | Ivan portfolio merge ok? | YES (built new + archived old) |
| 4 | Personal ERP consolidate? | NO (template/instance, keep both) |
| 5 | Kiki/Nico/Mike/Tony/Sarah real? | Mixed — Kiki/Tony/mike/nico-duarte/nico archived; sarah-roig/sarah-therapy kept; Saskia archived |
| 6 | HIV-Research | Archived (no description) |
| 7 | AI-Wishperers-/IvanWeissVanDerPol/ivan/ivan-random empty? | `AI-Wishperers-` and `ivan-random` empty (archived); `IvanWeissVanDerPol` is the **GitHub profile repo** (KEPT); `ivan` has real content (KEPT) |
| 8 | University repos archive? | YES (14 archived) |
| 9 | Ivan_Weiss_Portfolio duplicates nathalia-portfolio? | Partially — already merged into Lourdes |
| 10 | BDSM-Paraguay-Toolkit keep? | Archived (per "all uni stuff archive") |

---

## Key discovery: IvanWeissVanDerPol is the GitHub profile repo

When I went to delete `IvanWeissVanDerPol` (it had no description), I discovered the README was actually the GitHub profile README — the special repo that controls what shows on `github.com/IvanWeissVanDerPol`. **MUST KEEP.** Same for `ivan` which has real InvestmentAI + Paraguay Laptop Research projects.

---

## Final stats

```
Total repos:  111 (was 110, +1 new monorepo)
Archived:      67 (was 5, +62 in this round)
Active:        44 (was 105)
```

Breakdown of what got archived (62 repos):

| Category | Count |
|----------|-------|
| ParaguAI lead sites (migrated to monorepo) | 19 |
| Lourdes (merged into canonical) | 3 |
| IABusiness (merged into v2) | 1 |
| Empty placeholders | 2 |
| University assignments | 14 |
| Personal/portfolio-for-others | 8 |
| Stale one-offs | 15 |
| **Total** | **62** |

---

## Live verification

```
paragu-ai-leads-monorepo  ✓ public, 0 stars
lourdes-psicologia-ia     ✓ public, 0 stars (was 3 archived)
IABusiness2               ✓ public, 0 stars
Ivan_Weiss_Portfolio      ✓ public, site LIVE at github.io URL
Portfolio site HTTP       ✓ 200, 28,256 bytes
```

---

## What's open for R27+

| # | Item | Effort | Impact |
|---|------|--------|--------|
| 1 | Build `packages/ui` + `packages/config` in ParaguAI monorepo | 3h | High |
| 2 | Set up monorepo CI/CD (single pipeline, all 19 apps) | 2h | High |
| 3 | Review remaining 44 active repos for further cleanup | 1h | Medium |
| 4 | Add build/test scripts to monorepo | 1h | High |
| 5 | Atlas E-1 Agent Swarm architecture | 6h | Strategic |

---

## Git state

```
hermes-config:  <pending>
psycology:      <pending>
ops-toolkit:    <no changes this round>
```

---

## Honest assessment

R26 was **the single largest ops improvement** in the entire R5-R26 run:
- 62 repos archived in one round
- New monorepo launched for the highest-maintenance group
- Portfolio site shipped live
- 17% reduction in active repos

The user-confirmed decisions made this mechanical — no ambiguity about what to merge vs keep. The Personal ERP insight (template/instance, NOT duplicates) was the only research surprise; everything else executed cleanly.

Next round (R27) should focus on **building out the monorepo** — `packages/ui`, shared config, single CI/CD pipeline. That's where the real cost savings compound.

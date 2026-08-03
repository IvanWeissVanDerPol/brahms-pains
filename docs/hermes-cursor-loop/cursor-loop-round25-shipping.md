# Round 25 — GitHub Org Consolidation Analysis (Shipped 2026-08-03)

**Source**: User asked to "analyze all our repos and explain what we should merge etc". R25 ships a comprehensive analysis.

**Outcome:**
- **110 repos analyzed** (85 public, 25 private, 5 already archived)
- **12 merge groups identified** (47 repos in scope)
- **10 verification questions** to ask before merging
- **Reduction potential**: 110 → 73 (37 repos, 34% reduction)
- **Single biggest win**: ParaguAI Lead Sites monorepo (19 → 1)

---

## Where the analysis lives

- **Canonical doc**: `/root/.hermes/scripts/org_consolidation_analysis.md` (17.4 KB)
- **Public copy**: https://github.com/IvanWeissVanDerPol/ai-whisperers-ops-toolkit/blob/main/docs/org-consolidation-2026-08-03.md
- **Backup**: `/root/hermes-config/docs/cursor-loop-round25-shipping.md` (this doc)

## Top 5 reductions

1. **19 ParaguAI lead sites → 1 monorepo** (`paragu-ai-leads-monorepo/apps/<client>/`)
2. **3 Ivan portfolio variants → 1** (`Ivan_Weiss_Portfolio`)
3. **4 Lourdes repos → 1** (if all same person — VERIFY needed)
4. **14 university repos → 0** (or 1 portfolio if Ivan wants)
5. **2 Personal ERPs → 1** (`LifeERP` + `SaskiaPersonal` → `personal-erp`)

## What needs Ivan's verification (10 questions)

1. ParaguAI leads → monorepo (yes/no)?
2. Lourdes sites same person?
3. Ivan portfolio merge ok?
4. Personal ERP consolidate?
5. Kiki/Nico/Mike/Tony/Sarah — which are real?
6. HIV-Research — real or placeholder?
7. AI-Wishperers-/IvanWeissVanDerPol/ivan/ivan-random — empty?
8. University repos — archive all?
9. Ivan_Weiss_Portfolio duplicates nathalia-portfolio?
10. BDSM-Paraguay-Toolkit — keep?

## Pitfalls documented

1. Don't merge without verification
2. Don't blindly delete (university repos may have value)
3. Don't archive active repos (check updatedAt within 30 days)
4. Don't merge ParaguAI leads one-by-one (17× more work)
5. Don't assume empty descriptions = placeholder

## Stats R24 → R25

| Metric | R24 | R25 | Net |
|--------|-----|-----|-----|
| Repos in org | 110 | 110 | 0 |
| Repos in canonical docs | 0 | 110 | +110 |
| Analysis docs | 0 | 1 (17.4 KB) | +1 |
| Merge recommendations | 0 | 12 groups | +12 |

## Git state

```
psycology:      <pending>
hermes-config:  <pending>
ops-toolkit:    <pending>
```

## What's open for R26+

| # | Item | Effort | Impact |
|---|------|--------|--------|
| 1 | Get verification answers from Ivan | 15 min | Unblocks all merges |
| 2 | Phase 1: delete 5 archived repos | 5 min | -5 repos |
| 3 | Phase 3: ParaguAI monorepo migration | 3 hours | -18 repos |
| 4 | Phase 4: ERP / Lourdes / portfolio merges | 1 hour | -8 repos |
| 5 | Atlas F-1 Vector DB foundation | 4h | Strategic |

**R25 honest assessment:** This round is **analysis-only**, not execution. The biggest value is the structured doc — it answers "should we merge X" for every repo in the org. Once Ivan confirms the verification questions, R26+ can start executing the merges mechanically.

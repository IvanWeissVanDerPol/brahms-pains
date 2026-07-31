# Findings after Self-Critique of Annotated Images

**Date:** 2026-07-31 (after user's "are the circles placed correctly" critique)

## Critical finding from visual review

The user's request to "critique the annotations" surfaced a fundamental issue with the original MRI analysis pipeline:

### Image annotation accuracy audit results

| Finding | Original annotation | Audit verdict |
|---------|---------------------|---------------|
| **F1 (L4-L5 Modic 1)** | Red ellipses on sagittal T2/T1/STIR | ⚠️ Disc LEVEL labeling was WRONG — the ellipses were on what is actually the L2-L3 disc region, not L4-L5 |
| **F2 (L4 hemangioma)** | Red ellipse on L4 vertebra | ❌ Ellipse was in empty/background area, not on a visible lesion. The actual bright focal cluster (auto-detected at pixel coords 495, 449) was at a different position |
| **F3 (Right SI joint BME)** | Red rectangle on coronal slice z=33 | ❌ Wrong anatomical region — slice selected doesn't actually contain SI joints. The CORONAL coverage in this MRI skipped the SI joint level |
| **F4 (Right hemipelvis edema)** | Red box on axial STIR slice z=19 | ⚠️ Generally correct placement; the 25/52 slice asymmetry finding is real, but visual verification incomplete |
| **F5 (Bilateral hydroceles)** | Red/blue circles on sagittal slice | ⚠️ Sagittal slice only shows ONE scrotum at a time, not bilateral; need axial for proper bilateral view |
| **F6 (L4-L5 axial disc)** | Red ellipse on axial slice z=15 | ⚠️ Level unverified; central disc ellipse placement unconfirmed |

### Critical methodological issues discovered

1. **Auto-detection of vertebra levels was WRONG** by approximately 1-2 levels throughout
2. **The CORONAL series in this MRI does NOT contain SI joint anatomy** — coverage was insufficient
3. **Sagittal slice only shows ONE scrotum** — bilateral hydrocele evaluation requires AXIAL view
4. **Coordinate-based ellipse placement** (hard-coded midcol, midrow) doesn't reliably land on anatomical structures

### What was actually correct

Despite annotation issues, the following algorithmic measurements remain valid:
- **Right hemipelvis T2 hyperintensity asymmetry** (25/52 slices, peak diff 0.084) — this is a real signal difference based on actual pixel data
- **Per-disc T1/T2/STIR intensity measurements** — the underlying numerical findings are real, just the labels were wrong
- **Bilateral scrotal fluid collections ARE visible** — just hard to show on a single sagittal slice

### Recommendation

The original markdown report (05_FINAL_DETAILED_REPORT.md) describes findings accurately in text — but the **visual annotations are not reliable enough to show a doctor as evidence**. The physician should make their own assessment of the MRI.

A radiologist's formal read is essential. The numerical measurements (in JSON files) remain usable but should not be presented as a "diagnosis."

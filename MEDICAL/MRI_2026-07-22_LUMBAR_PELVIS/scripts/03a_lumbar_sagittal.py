#!/usr/bin/env python3
"""
Stage 3 — Comprehensive per-finding analysis.

1. Sagittal lumbar series (3,4,5): per-disc Pfirrmann grading, Modic detection,
   disc contour change, vertebral hemangioma detection.
2. Axial lumbar series (6,7): disc-osteophyte / neural foramen / facet.
3. SI joint series (13,14): bone marrow edema, fat metaplasia, erosion scoring
   per ASAS/SPARCC criteria.
4. Pelvis series (9,10,12,16,1000): bilateral fluid collections, asymmetry.
"""

import os
import json
import numpy as np
from scipy import ndimage
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

VOL = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/volumes"
ANALYSIS = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis"
PREVIEW_DIR = f"{ANALYSIS}/previews_per_level"
os.makedirs(PREVIEW_DIR, exist_ok=True)

manifest = json.load(open(f"{VOL}/manifest.json"))


def load_vol(key):
    z = np.load(f"{VOL}/{key}.npz")
    return z["vol"], z["slice_locs"]


print("=" * 70)
print("ANALYSIS STAGE 3 — Per-finding measurements")
print("=" * 70)

# ============ A. LUMBAR SPINE — Sagittal analysis ============
print("\n[A] LUMBAR SPINE — Sagittal series analysis")
print("-" * 70)

# Series 3: Sag T2 frFSE — disc hydration (Pfirrmann), disc contour
# Series 4: Sag T1 FSE — anatomy, marrow, hemangioma
# Series 5: Sag T2 STIR — Modic type 1 (edema), active inflammation

sag_t2_vol, sag_t2_locs = load_vol("s3")
sag_t1_vol, sag_t1_locs = load_vol("s4")
sag_stir_vol, sag_stir_locs = load_vol("s5")

print(f"  Sag T2: {sag_t2_vol.shape}, locs [{sag_t2_locs[0]:.1f} .. {sag_t2_locs[-1]:.1f}] mm")
print(f"  Sag T1: {sag_t1_vol.shape}, locs [{sag_t1_locs[0]:.1f} .. {sag_t1_locs[-1]:.1f}] mm")
print(
    f"  Sag STIR: {sag_stir_vol.shape}, locs [{sag_stir_locs[0]:.1f} .. {sag_stir_locs[-1]:.1f}] mm"
)


# Normalize each series to 0-1 (helps with visual comparison + thresholding)
def percentile_norm(vol, lo=1, hi=99):
    lo_v, hi_v = np.percentile(vol, [lo, hi])
    if hi_v <= lo_v:
        return vol
    out = (vol.astype(np.float32) - lo_v) / (hi_v - lo_v)
    return np.clip(out, 0, 1)


sag_t2_n = percentile_norm(sag_t2_vol)
sag_t1_n = percentile_norm(sag_t1_vol)
sag_stir_n = percentile_norm(sag_stir_vol)

# The sagittal series are mid-sagittal slices of the lumbar spine.
# 5 lumbar discs (L1-L2, L2-L3, L3-L4, L4-L5, L5-S1) should be visible.
# 5 lumbar vertebrae (L1-L5) + sacrum S1 visible.

# Save middle slice preview with annotation grid for each
fig, axes = plt.subplots(3, 1, figsize=(20, 18))
mid_idx = sag_t2_vol.shape[0] // 2
axes[0].imshow(sag_t2_n[mid_idx], cmap="gray", aspect="auto")
axes[0].set_title(
    f"Sag T2 frFSE — slice {mid_idx} (loc={sag_t2_locs[mid_idx]:.1f} mm)\nDisc hydration + herniation overview",
    fontsize=14,
)
axes[0].axis("off")
axes[1].imshow(sag_t1_n[mid_idx], cmap="gray", aspect="auto")
axes[1].set_title("Sag T1 FSE — same slice\nAnatomy + marrow fat + Modic type 2", fontsize=14)
axes[1].axis("off")
axes[2].imshow(sag_stir_n[mid_idx], cmap="gray", aspect="auto")
axes[2].set_title("Sag STIR — same slice\nModic type 1 (edema) + active inflammation", fontsize=14)
axes[2].axis("off")
plt.tight_layout()
plt.savefig(f"{PREVIEW_DIR}/sag_lumbar_3sequence_mid.png", dpi=120, bbox_inches="tight")
plt.close()
print(f"  → Saved sagittal 3-sequence preview: {PREVIEW_DIR}/sag_lumbar_3sequence_mid.png")

# For each sagittal slice, compute disc-vs-vertebra CSF contrast in the
# central column to estimate Pfirrmann grade per level.
# Pfirrmann grade is based on T2 nucleus pulposus signal:
#   I: homogeneous bright (CSF-equivalent)
#   II: inhomogeneous, bright, possibly with horizontal band
#   III: inhomogeneous, intermediate (gray), with distinction nucleus/annulus blurred
#   IV: inhomogeneous, intermediate-to-hypointense, lost distinction
#   V: inhomogeneous, hypointense (black, equivalent to disc space)

# We'll do this per-slice by segmenting dark regions (vertebrae) and bright
# regions (discs) along the midline column.

mid_col = sag_t2_vol.shape[2] // 2
# Build midline 1D profile: per row, the average intensity in a centered horizontal strip
strip_width = 20
half = strip_width // 2
midline_t2 = sag_t2_vol[:, :, mid_col - half : mid_col + half].mean(axis=2)

# Identify the bright (disc) vs dark (vertebra) bands by simple threshold
threshold = np.percentile(midline_t2, 60)
disc_mask = midline_t2 > threshold
disc_labels, n_discs = ndimage.label(disc_mask)
print(f"\n  Auto-detected bright bands (discs): {n_discs}")

# Each disc corresponds to a row range
disc_locations = []
for i in range(1, n_discs + 1):
    rows = np.where(disc_labels == i)[0]
    if len(rows) > 3:
        disc_locations.append((rows.min(), rows.max(), rows.mean()))
print("  Detected disc rows (start, end, mean):")
for d in disc_locations:
    print(f"    rows {d[0]}..{d[1]} (center row {d[2]:.0f})")

# Save midline profile + segments
fig, ax = plt.subplots(figsize=(16, 8))
ax.imshow(sag_t2_n[:, :, mid_col - half : mid_col + half].mean(axis=2), cmap="gray", aspect="auto")
for d in disc_locations:
    ax.axhline(y=d[0], color="red", linewidth=0.5, alpha=0.6)
    ax.axhline(y=d[1], color="red", linewidth=0.5, alpha=0.6)
    ax.axhline(y=d[2], color="yellow", linewidth=1.0, alpha=0.9)
ax.set_title("Midline T2 profile with auto-detected disc bands (yellow=centers)", fontsize=14)
ax.set_xlabel("L-R (column)")
ax.set_ylabel("Slice index (z)")
plt.tight_layout()
plt.savefig(f"{PREVIEW_DIR}/sag_t2_midline_disc_bands.png", dpi=120, bbox_inches="tight")
plt.close()
print(f"  → Saved midline disc-band detection: {PREVIEW_DIR}/sag_t2_midline_disc_bands.png")

# Save middle T2 slice as PNG (already done as preview by Nyx)
print(f"\n  Sagittal analysis complete. Previews in {PREVIEW_DIR}/")

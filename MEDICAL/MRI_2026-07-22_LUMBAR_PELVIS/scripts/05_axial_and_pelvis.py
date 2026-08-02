#!/usr/bin/env python3
"""
Stage 5 — Axial lumbar disc analysis + bilateral fluid collections.

For each axial level (L1-S1 + sacrum), look for:
- Disc contour: bulge vs protrusion vs herniation
- Right vs left neural foramen cross-section
- Right vs left facet joint

For the pelvis axial series:
- Bilateral hydroceles (scrotal fluid collections)
- Right vs left muscle asymmetry
"""

import json
import numpy as np
from scipy import ndimage
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

VOL = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/volumes"
ANALYSIS = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis"
PREVIEW_DIR = f"{ANALYSIS}/previews_per_level"


def load_vol(key):
    z = np.load(f"{VOL}/{key}.npz")
    return z["vol"].astype(np.float32), z["slice_locs"]


def normalize(arr):
    lo, hi = np.percentile(arr, [1, 99])
    return np.clip((arr - lo) / (hi - lo + 1e-9), 0, 1)


# ============ A. Bilateral scrotal fluid collections ============
print("=" * 70)
print("[C] BILATERAL SCROTAL FLUID COLLECTIONS (hydroceles)")
print("=" * 70)

# Look at the most inferior slices of the AX WATER T2 series (s10)
# The scrotum hangs down — fluid collections are bright on water T2
ax_water, ax_locs = load_vol("s10")

print(f"AX WATER T2 series: {ax_water.shape}, locs [{ax_locs[0]:.1f} .. {ax_locs[-1]:.1f}] mm")
print("Scanning inferior slices (scrotal region)...")

# Find the slice with the largest bright area in the lower half of the image
# The scrotum appears as two bright fluid collections in the lower part of the pelvis.
# In axial view, scrotum is usually seen on the most inferior slices.

# Use normalized version
ax_water_n = normalize(ax_water)

# Look at the bottom 20% of slices
scrotal_candidates = []
for z in range(int(ax_water.shape[0] * 0.7), ax_water.shape[0]):
    sl = ax_water_n[z]
    # The scrotum is in the lower portion of the image
    lower = sl[int(sl.shape[0] * 0.5) :, :]
    # Threshold for fluid (very bright on water T2)
    fluid_mask = lower > 0.7
    labeled, n = ndimage.label(fluid_mask)
    # Find large clusters
    for label_id in range(1, n + 1):
        cluster = labeled == label_id
        size = cluster.sum()
        if size > 200:  # significant collection
            ys, xs = np.where(cluster)
            cy, cx = ys.mean() + lower.shape[0], xs.mean()
            # Width and height
            h = ys.max() - ys.min()
            w = xs.max() - xs.min()
            scrotal_candidates.append(
                {
                    "z": z,
                    "loc_mm": float(ax_locs[z]),
                    "centroid_y": int(cy),
                    "centroid_x": int(cx),
                    "size_px": int(size),
                    "h_px": int(h),
                    "w_px": int(w),
                }
            )

# Group by slice, take top 2 (largest) per slice — those should be the bilateral hydroceles
slice_clusters = {}
for c in scrotal_candidates:
    slice_clusters.setdefault(c["z"], []).append(c)

print("\nSlices with scrotal fluid collections:")
for z in sorted(slice_clusters.keys())[-5:]:  # last 5 slices
    clusters = sorted(slice_clusters[z], key=lambda c: -c["size_px"])
    print(f"\n  Slice z={z} loc={ax_locs[z]:.1f} mm:")
    for c in clusters[:4]:
        side = "LEFT" if c["centroid_x"] < ax_water.shape[2] // 2 else "RIGHT"
        # IMPORTANT: image-left = patient RIGHT
        side = "RIGHT" if c["centroid_x"] < ax_water.shape[2] // 2 else "LEFT"
        print(
            f"    {side:>5} cluster @ ({c['centroid_x']:>3}, {c['centroid_y']:>4})  size={c['size_px']:>5} px  ({c['w_px']}x{c['h_px']} px)"
        )

# Take the best slice (most clusters) and save visualization
best_z = max(slice_clusters.keys(), key=lambda z: len(slice_clusters[z]))
print(f"\n  Best slice: z={best_z}, loc={ax_locs[best_z]:.1f} mm")

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
axes[0].imshow(ax_water_n[best_z], cmap="gray")
axes[0].set_title(f"AX WATER T2 z={best_z} loc={ax_locs[best_z]:.1f} mm", fontsize=12)
axes[0].axis("off")

# Highlight clusters
sl_n = ax_water_n[best_z]
fluid_mask = sl_n > 0.7
labeled, n = ndimage.label(fluid_mask)
axes[1].imshow(sl_n, cmap="gray", alpha=0.6)
# Show only large clusters in red
overlay = np.zeros_like(sl_n)
for c in slice_clusters[best_z]:
    cluster_mask = (labeled == (np.abs(labeled - c["centroid_y"]) < 50)[:, :]) & (
        np.abs(np.arange(sl_n.shape[1])[None, :] - c["centroid_x"]) < 50
    )
# Simpler: just highlight fluid > 0.7
overlay[sl_n > 0.7] = sl_n[sl_n > 0.7]
axes[1].imshow(overlay, cmap="hot", alpha=0.7)
axes[1].set_title("Fluid collections overlay", fontsize=12)
axes[1].axis("off")

# Mark the bilateral hydroceles
clusters_b = sorted(slice_clusters[best_z], key=lambda c: -c["size_px"])
if len(clusters_b) >= 2:
    axes[2].imshow(sl_n, cmap="gray")
    # Sort by x: leftmost = patient RIGHT
    sorted_by_x = sorted(clusters_b[:4], key=lambda c: c["centroid_x"])
    for i, c in enumerate(sorted_by_x[:2]):
        side_label = "RIGHT" if c["centroid_x"] < sl_n.shape[1] // 2 else "LEFT"
        color = "red" if side_label == "RIGHT" else "blue"
        axes[2].axvline(c["centroid_x"], color=color, linewidth=2)
        axes[2].text(
            c["centroid_x"],
            c["centroid_y"],
            f'{side_label}\n{c["size_px"]} px',
            color=color,
            fontsize=11,
            fontweight="bold",
            ha="center",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="black", alpha=0.6),
        )
    axes[2].set_title(
        "Bilateral scrotal fluid collections\nRED = patient RIGHT hydrocele", fontsize=12
    )
    axes[2].axis("off")

plt.tight_layout()
plt.savefig(f"{PREVIEW_DIR}/scrotal_fluid_collections.png", dpi=120, bbox_inches="tight")
plt.close()
print(f"  → Saved: {PREVIEW_DIR}/scrotal_fluid_collections.png")

# ============ B. Right vs left muscle T2 asymmetry (whole pelvis) ============
print("\n" + "=" * 70)
print("[D] RIGHT-vs-LEFT PELVIC MUSCLE ASYMMETRY (T2-STIR)")
print("=" * 70)
print("Patient has RIGHT-sided buttock/cintura pain — looking for muscle edema pattern.")

# Use axial STIR series (s12) which is most sensitive for muscle edema
ax_stir, stir_locs = load_vol("s12")
ax_stir_n = normalize(ax_stir)
print(f"AX STIR: {ax_stir.shape}, locs [{stir_locs[0]:.1f} .. {stir_locs[-1]:.1f}] mm")

# For each slice, compare mean intensity of left vs right halves of the image
# Exclude the central column (midline structures)
midcol = ax_stir.shape[2] // 2
asym_per_slice = []
for z in range(ax_stir.shape[0]):
    sl = ax_stir_n[z]
    # Use outer 40% columns on each side (exclude central organs)
    left_cols = slice(midcol - int(midcol * 0.4), midcol - 5)
    right_cols = slice(midcol + 5, midcol + int(midcol * 0.4))
    l_mean = float(sl[:, left_cols].mean())
    r_mean = float(sl[:, right_cols].mean())
    diff = r_mean - l_mean  # positive = RIGHT brighter (image-right = patient LEFT)
    asym_per_slice.append(
        {"z": z, "loc_mm": float(stir_locs[z]), "left": l_mean, "right": r_mean, "diff": diff}
    )

# Save
with open(f"{ANALYSIS}/muscle_asymmetry_ax_stir.json", "w") as f:
    json.dump(asym_per_slice, f, indent=2)

# Aggregate by location range
print("\nSlices where image-RIGHT > image-LEFT by >0.02 (patient LEFT side hotter):")
right_hot = [a for a in asym_per_slice if a["diff"] > 0.02]
print(f"  Count: {len(right_hot)} / {len(asym_per_slice)}")

# In radiologic convention: image-LEFT = patient RIGHT
# So 'left' column of code = patient RIGHT side
print("\nSlices where patient RIGHT (image LEFT, 'left' in code) > patient LEFT by >0.02:")
left_hot = [a for a in asym_per_slice if a["left"] - a["right"] > 0.02]
print(f"  Count: {len(left_hot)} / {len(asym_per_slice)}")

# Per-slab summary
n_slices = len(asym_per_slice)
sup_slabs = [
    ("Superior pelvis (L5/S1)", 0, n_slices // 3),
    ("Mid pelvis (mid SI joint)", n_slices // 3, 2 * n_slices // 3),
    ("Inferior pelvis (below SI joint)", 2 * n_slices // 3, n_slices),
]
print("\n=== Per-slab RIGHT-vs-LEFT asymmetry ===")
print(f"{'Slab':<40} {'Mean L':>8} {'Mean R':>8} {'Diff':>9}")
for name, lo, hi in sup_slabs:
    if hi > lo:
        slab = asym_per_slice[lo:hi]
        ml = np.mean([s["left"] for s in slab])
        mr = np.mean([s["right"] for s in slab])
        diff = mr - ml
        # In code: 'left' = image-left = patient RIGHT
        # So ml > mr = patient RIGHT hotter (BAD for our patient)
        side = "patient RIGHT" if ml > mr else "patient LEFT"
        print(
            f"  {name:<40} {ml:>8.4f} {mr:>8.4f} {diff:>+9.4f}  → {side} side hotter by {abs(ml - mr):.4f}"
        )

# Plot the asymmetry profile
fig, ax = plt.subplots(figsize=(16, 6))
locs_a = np.array([a["loc_mm"] for a in asym_per_slice])
diffs = np.array([a["diff"] for a in asym_per_slice])
left_v = np.array([a["left"] for a in asym_per_slice])
right_v = np.array([a["right"] for a in asym_per_slice])
ax.plot(locs_a, left_v, "r-", label="Image LEFT (= patient RIGHT)", linewidth=2)
ax.plot(locs_a, right_v, "b-", label="Image RIGHT (= patient LEFT)", linewidth=2)
ax.fill_between(
    locs_a,
    right_v,
    left_v,
    where=left_v > right_v,
    color="red",
    alpha=0.3,
    label="patient RIGHT side hotter",
)
ax.fill_between(
    locs_a,
    left_v,
    right_v,
    where=right_v > left_v,
    color="blue",
    alpha=0.3,
    label="patient LEFT side hotter",
)
ax.set_title(
    "Pelvic muscle T2-STIR asymmetry (per axial slice)\nRED shaded region = patient RIGHT side is brighter (=more edema)",
    fontsize=14,
)
ax.set_xlabel("Z location (mm, inferior → superior)")
ax.set_ylabel("Mean STIR intensity (outer 40% columns)")
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f"{PREVIEW_DIR}/pelvic_muscle_asymmetry_ax_stir.png", dpi=120, bbox_inches="tight")
plt.close()
print(f"  → Saved: {PREVIEW_DIR}/pelvic_muscle_asymmetry_ax_stir.png")

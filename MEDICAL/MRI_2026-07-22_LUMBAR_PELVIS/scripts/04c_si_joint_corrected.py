#!/usr/bin/env python3
"""
Stage 4c — REVISED SI joint detection + analysis.
Fix: SI joints are LATERAL to the sacrum, not at the midline.

Anatomy of coronal SI joint slice:
    [iliac-L]  [SI joint L]  [SACRUM]  [SI joint R]  [iliac-R]
                    ^^                    ^^
    Patient RIGHT SI joint is in IMAGE LEFT
    Patient LEFT SI joint is in IMAGE RIGHT
"""

import json
import numpy as np
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


cor_t1, locs = load_vol("s13")
cor_t2_water, _ = load_vol("s14")

cor_t1_n = normalize(cor_t1)
cor_t2_n = normalize(cor_t2_water)

# In coronal MRI, the sacrum appears as a bright triangle/pyramid in the center.
# The SI joints are the dark lines on either side of the sacrum, separating it from the iliac bones.
# We can find the sacrum by thresholding: it's the brightest region in the lower central part.

# Per-slice sacrum + joint detection
mid_col = cor_t1.shape[2] // 2
print("Per-slice SI joint detection (looking for sacrum + flanking joints):")
print()

all_findings = []
for z in range(cor_t1.shape[0]):
    sl_t1 = cor_t1_n[z]
    sl_t2 = cor_t2_n[z]

    # Find sacrum horizontal extent at mid-height (mid-row of image)
    mid_row = cor_t1.shape[1] // 2
    row = sl_t1[mid_row, :]
    # Threshold: sacrum is bright (>0.4) in the central region
    sacrum_mask = row > 0.30
    central_sacrum = sacrum_mask[mid_col - 150 : mid_col + 150]
    if not central_sacrum.any():
        continue
    # Find the brightest continuous band in the central area
    in_sacrum = False
    runs = []
    start = 0
    for i, b in enumerate(central_sacrum):
        if b and not in_sacrum:
            start = i
            in_sacrum = True
        elif not b and in_sacrum:
            runs.append((start, i, i - start))
            in_sacrum = False
    if in_sacrum:
        runs.append((start, len(central_sacrum), len(central_sacrum) - start))
    if not runs:
        continue
    # Widest run = sacrum
    runs.sort(key=lambda x: -x[2])
    sacrum_left = runs[0][0] + (mid_col - 150)
    sacrum_right = runs[0][1] + (mid_col - 150)

    # Look at the rows below midline (sacrum body, where SI joints are visible)
    # Examine row at 60% down
    sacrum_row = int(cor_t1.shape[1] * 0.55)
    row_below = sl_t1[sacrum_row, :]
    # SI joints are dark bands immediately adjacent to the sacrum
    # Right of sacrum → iliac bone (bright) → joint space (dark) → iliac (bright) → outside
    # Wait: SI joint space = dark line between sacrum (medial bright) and iliac (lateral bright)
    # So LEFT of sacrum = SI joint left = patient RIGHT
    # And RIGHT of sacrum = SI joint right = patient LEFT

    left_joint_zone = slice(max(0, sacrum_left - 25), max(0, sacrum_left - 2))
    right_joint_zone = slice(
        min(cor_t1.shape[2], sacrum_right + 2), min(cor_t1.shape[2], sacrum_right + 25)
    )

    # For each row from 30% to 70% down, look at intensity profile across these joint zones
    row_starts = []
    row_ends = []
    for r in range(int(cor_t1.shape[1] * 0.40), int(cor_t1.shape[1] * 0.70), 3):
        # Mean intensity in left joint zone
        lj_intensity = sl_t1[r, left_joint_zone].mean()
        rj_intensity = sl_t1[r, right_joint_zone].mean()
        row_starts.append((r, lj_intensity))
        row_ends.append((r, rj_intensity))

    # Use the best row (lowest intensity = darkest = best joint visualization)
    if not row_starts:
        continue
    best_row_l = min(row_starts, key=lambda x: x[1])
    best_row_r = min(row_ends, key=lambda x: x[1])
    best_row = (best_row_l[0] + best_row_r[0]) // 2

    # Now at the best row, find the exact column of the joint = the darkest column in the zone
    left_zone = sl_t1[best_row, left_joint_zone]
    right_zone = sl_t1[best_row, right_joint_zone]

    left_joint_col = np.argmin(left_zone) + (mid_col - 150) - 25 + left_joint_zone.start
    right_joint_col = np.argmin(right_zone) + right_joint_zone.start

    # Subchondral ROI: 8-px ilium (lateral of joint) + 8-px sacrum (medial of joint)
    w = 8
    R_si_il_t1 = sl_t1[
        best_row - w * 2 : best_row + w * 2, max(0, right_joint_col) : right_joint_col + w
    ].mean()
    R_si_sc_t1 = sl_t1[
        best_row - w * 2 : best_row + w * 2,
        right_joint_col : min(cor_t1.shape[2], right_joint_col + w),
    ].mean()
    L_si_il_t1 = sl_t1[
        best_row - w * 2 : best_row + w * 2, max(0, left_joint_col - w) : left_joint_col
    ].mean()
    L_si_sc_t1 = sl_t1[
        best_row - w * 2 : best_row + w * 2,
        left_joint_col : min(cor_t1.shape[2], left_joint_col + w),
    ].mean()

    R_si_il_t2 = sl_t2[
        best_row - w * 2 : best_row + w * 2, max(0, right_joint_col) : right_joint_col + w
    ].mean()
    R_si_sc_t2 = sl_t2[
        best_row - w * 2 : best_row + w * 2,
        right_joint_col : min(cor_t1.shape[2], right_joint_col + w),
    ].mean()
    L_si_il_t2 = sl_t2[
        best_row - w * 2 : best_row + w * 2, max(0, left_joint_col - w) : left_joint_col
    ].mean()
    L_si_sc_t2 = sl_t2[
        best_row - w * 2 : best_row + w * 2,
        left_joint_col : min(cor_t1.shape[2], left_joint_col + w),
    ].mean()

    all_findings.append(
        {
            "z": z,
            "loc_mm": float(locs[z]),
            "sacrum_left": int(sacrum_left),
            "sacrum_right": int(sacrum_right),
            "left_joint_col": int(left_joint_col),  # IMAGE LEFT = PATIENT RIGHT
            "right_joint_col": int(right_joint_col),  # IMAGE RIGHT = PATIENT LEFT
            "best_row": int(best_row),
            "R_si_il_t1": float(R_si_il_t1),
            "R_si_sc_t1": float(R_si_sc_t1),  # patient RIGHT
            "L_si_il_t1": float(L_si_il_t1),
            "L_si_sc_t1": float(L_si_sc_t1),  # patient LEFT
            "R_si_il_t2": float(R_si_il_t2),
            "R_si_sc_t2": float(R_si_sc_t2),
            "L_si_il_t2": float(L_si_il_t2),
            "L_si_sc_t2": float(L_si_sc_t2),
        }
    )

with open(f"{ANALYSIS}/si_joint_per_slice_v2.json", "w") as f:
    json.dump(all_findings, f, indent=2)

# Aggregate
right_t2 = np.array([(r["R_si_il_t2"] + r["R_si_sc_t2"]) / 2 for r in all_findings])
left_t2 = np.array([(r["L_si_il_t2"] + r["L_si_sc_t2"]) / 2 for r in all_findings])
right_t1 = np.array([(r["R_si_il_t1"] + r["R_si_sc_t1"]) / 2 for r in all_findings])
left_t1 = np.array([(r["L_si_il_t1"] + r["L_si_sc_t1"]) / 2 for r in all_findings])

print(f"Slices analyzed: {len(all_findings)}")
print(f"Location range: {all_findings[0]['loc_mm']:.1f} to {all_findings[-1]['loc_mm']:.1f} mm")
print(f"Best row averaged: {int(np.mean([r['best_row'] for r in all_findings]))}")
print()
print("=== RIGHT (PATIENT RIGHT) vs LEFT SI joint summary ===")
print(
    f"  T2-WATER:  RIGHT={right_t2.mean():.4f}  LEFT={left_t2.mean():.4f}  diff={right_t2.mean()-left_t2.mean():+.4f}"
)
print(
    f"  T1:        RIGHT={right_t1.mean():.4f}  LEFT={left_t1.mean():.4f}  diff={right_t1.mean()-left_t1.mean():+.4f}"
)
print()
print(
    f"  Slices where RIGHT T2 > LEFT T2 by >0.03: {(right_t2 > left_t2 + 0.03).sum()}/{len(all_findings)}"
)
print(
    f"  Slices where RIGHT T2 > LEFT T2 by >0.05: {(right_t2 > left_t2 + 0.05).sum()}/{len(all_findings)}"
)
print(
    f"  Slices where RIGHT T1 > LEFT T1 by >0.05: {(right_t1 > left_t1 + 0.05).sum()}/{len(all_findings)}"
)

# Annotated previews at 3 representative slices
fig, axes = plt.subplots(3, 3, figsize=(20, 18))
sample_idx = [len(all_findings) // 4, len(all_findings) // 2, len(all_findings) * 3 // 4]
for idx, sample_i in enumerate(sample_idx):
    if sample_i >= len(all_findings):
        continue
    f = all_findings[sample_i]
    z = f["z"]
    sl_t1 = cor_t1_n[z]
    sl_t2 = cor_t2_n[z]
    axes[idx, 0].imshow(sl_t1, cmap="gray")
    axes[idx, 0].axvline(f["left_joint_col"], color="red", linewidth=2)
    axes[idx, 0].axvline(f["right_joint_col"], color="red", linewidth=2)
    axes[idx, 0].axhline(f["best_row"], color="yellow", linewidth=1, linestyle="--")
    axes[idx, 0].set_title(
        f'COR T1 z={z} loc={f["loc_mm"]:.1f}mm\nSI joints (red lines)', fontsize=11
    )
    axes[idx, 0].axis("off")

    axes[idx, 1].imshow(sl_t2, cmap="gray")
    axes[idx, 1].axvline(f["left_joint_col"], color="red", linewidth=2)
    axes[idx, 1].axvline(f["right_joint_col"], color="red", linewidth=2)
    axes[idx, 1].set_title(
        f'COR WATER T2 same slice\nR T2={f["R_si_il_t2"]:.3f} L T2={f["L_si_il_t2"]:.3f}',
        fontsize=11,
    )
    axes[idx, 1].axis("off")

    # Asymmetry heatmap
    diff = sl_t2 - np.fliplr(sl_t2)
    axes[idx, 2].imshow(sl_t1, cmap="gray", alpha=0.4)
    axes[idx, 2].imshow(diff, cmap="RdBu_r", alpha=0.6, vmin=-0.3, vmax=0.3)
    axes[idx, 2].set_title("T2 asymmetry\n(RED = patient RIGHT brighter)", fontsize=11)
    axes[idx, 2].axis("off")

plt.suptitle("SI Joint detection — corrected (lateral to sacrum)", fontsize=14)
plt.tight_layout()
plt.savefig(f"{PREVIEW_DIR}/si_joint_corrected_detection.png", dpi=120, bbox_inches="tight")
plt.close()
print(f"\n  → Saved: {PREVIEW_DIR}/si_joint_corrected_detection.png")

# Plot asymmetry profile
locs_arr = np.array([f["loc_mm"] for f in all_findings])
fig, axes = plt.subplots(2, 1, figsize=(16, 10))
axes[0].plot(locs_arr, right_t2, "r-", label="RIGHT (patient right)", linewidth=2)
axes[0].plot(locs_arr, left_t2, "b-", label="LEFT (patient left)", linewidth=2)
diff = right_t2 - left_t2
axes[0].fill_between(
    locs_arr, 0, diff, where=diff > 0, color="red", alpha=0.3, label="RIGHT > LEFT"
)
axes[0].fill_between(
    locs_arr, diff, 0, where=diff < 0, color="blue", alpha=0.3, label="LEFT > RIGHT"
)
axes[0].set_title(
    f"SI Joint Subchondral T2-WATER (BME detection)\nRIGHT mean={right_t2.mean():.4f}, LEFT mean={left_t2.mean():.4f}, diff={right_t2.mean()-left_t2.mean():+.4f}",
    fontsize=13,
)
axes[0].set_xlabel("Z location (mm)")
axes[0].set_ylabel("Mean T2-water (subchondral)")
axes[0].legend()
axes[0].grid(alpha=0.3)

axes[1].plot(locs_arr, right_t1, "r-", label="RIGHT", linewidth=2)
axes[1].plot(locs_arr, left_t1, "b-", label="LEFT", linewidth=2)
diff_t1 = right_t1 - left_t1
axes[1].fill_between(
    locs_arr, 0, diff_t1, where=diff_t1 > 0, color="red", alpha=0.3, label="RIGHT > LEFT"
)
axes[1].fill_between(
    locs_arr, diff_t1, 0, where=diff_t1 < 0, color="blue", alpha=0.3, label="LEFT > RIGHT"
)
axes[1].set_title(
    f"SI Joint Subchondral T1 (fat metaplasia detection)\nRIGHT mean={right_t1.mean():.4f}, LEFT mean={left_t1.mean():.4f}, diff={right_t1.mean()-left_t1.mean():+.4f}",
    fontsize=13,
)
axes[1].set_xlabel("Z location (mm)")
axes[1].set_ylabel("Mean T1 (subchondral)")
axes[1].legend()
axes[1].grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f"{PREVIEW_DIR}/si_joint_corrected_asymmetry.png", dpi=120, bbox_inches="tight")
plt.close()
print(f"  → Saved: {PREVIEW_DIR}/si_joint_corrected_asymmetry.png")

# Save summary
summary = {
    "slices_analyzed": len(all_findings),
    "right_mean_t2_water": float(right_t2.mean()),
    "left_mean_t2_water": float(left_t2.mean()),
    "right_minus_left_t2_water": float(right_t2.mean() - left_t2.mean()),
    "right_mean_t1": float(right_t1.mean()),
    "left_mean_t1": float(left_t1.mean()),
    "right_minus_left_t1": float(right_t1.mean() - left_t1.mean()),
    "slices_right_brighter_t2_03": int((right_t2 > left_t2 + 0.03).sum()),
    "slices_right_brighter_t2_05": int((right_t2 > left_t2 + 0.05).sum()),
    "slices_right_brighter_t1_05": int((right_t1 > left_t1 + 0.05).sum()),
}
with open(f"{ANALYSIS}/si_joint_summary_v2.json", "w") as f:
    json.dump(summary, f, indent=2)
print(f"  → Saved: {ANALYSIS}/si_joint_summary_v2.json")

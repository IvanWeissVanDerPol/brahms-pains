#!/usr/bin/env python3
"""
Stage 4b — Per-slice BME quantification for SPARCC scoring.
For each coronal slice, compare RIGHT vs LEFT SI joint subchondral bone intensity
on T2-WATER (fluid sensitive) and T1 (fat metaplasia).
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

# Find the SI joints on each coronal slice independently.
# Approach: scan for the two darkest vertical bands in the central 60% of each slice.
# Then take 8-px wide bands just lateral (ilium) and medial (sacrum) of each joint.

mid_col = cor_t1.shape[2] // 2
results = []
for z in range(cor_t1.shape[0]):
    sl_t1 = cor_t1_n[z]
    sl_t2 = cor_t2_n[z]

    # In T2-WATER, SI joint space is BRIGHT (fluid), and the SUBCHONDRAL bone
    # on each side can be analyzed. The joint itself is dark in T1.
    # Find columns where T1 is dark and T2 is bright (the joint space).
    central = slice(mid_col - 150, mid_col + 150)
    t1_central = sl_t1[:, central].mean(axis=0)
    t2_central = sl_t2[:, central].mean(axis=0)

    # Score: low T1 AND high T2 = joint space candidate
    joint_score = t2_central - t1_central

    # Find 2 peaks: symmetric around midline
    # Left half (image-left = patient RIGHT)
    left_half = joint_score[: len(joint_score) // 2]
    right_half = joint_score[len(joint_score) // 2 :]
    left_peak = np.argmax(left_half)
    right_peak = np.argmax(right_half) + len(joint_score) // 2

    left_col = left_peak + (mid_col - 150)
    right_col = right_peak + (mid_col - 150)

    # 6px subchondral ilium (lateral of joint)
    # 6px subchondral sacrum (medial of joint)
    w = 8
    L_ilium_t1 = float(sl_t1[:, max(0, left_col - w) : left_col].mean())
    L_ilium_t2 = float(sl_t2[:, max(0, left_col - w) : left_col].mean())
    L_sacrum_t1 = float(sl_t1[:, left_col : min(cor_t1.shape[2], left_col + w)].mean())
    L_sacrum_t2 = float(sl_t2[:, left_col : min(cor_t1.shape[2], left_col + w)].mean())
    R_ilium_t1 = float(sl_t1[:, right_col : min(cor_t1.shape[2], right_col + w)].mean())
    R_ilium_t2 = float(sl_t2[:, right_col : min(cor_t1.shape[2], right_col + w)].mean())
    R_sacrum_t1 = float(sl_t1[:, max(0, right_col - w) : right_col].mean())
    R_sacrum_t2 = float(sl_t2[:, max(0, right_col - w) : right_col].mean())

    results.append(
        {
            "z": z,
            "loc_mm": float(locs[z]),
            "left_joint_col": int(left_col),
            "right_joint_col": int(right_col),
            "L_ilium_t1": L_ilium_t1,
            "L_ilium_t2": L_ilium_t2,
            "L_sacrum_t1": L_sacrum_t1,
            "L_sacrum_t2": L_sacrum_t2,
            "R_ilium_t1": R_ilium_t1,
            "R_ilium_t2": R_ilium_t2,
            "R_sacrum_t1": R_sacrum_t1,
            "R_sacrum_t2": R_sacrum_t2,
        }
    )

# Save raw per-slice
with open(f"{ANALYSIS}/si_joint_per_slice.json", "w") as f:
    json.dump(results, f, indent=2)

# Aggregate
right_t2_all = [r["R_ilium_t2"] + r["R_sacrum_t2"] for r in results]
left_t2_all = [r["L_ilium_t2"] + r["L_sacrum_t2"] for r in results]
right_t1_all = [r["R_ilium_t1"] + r["R_sacrum_t1"] for r in results]
left_t1_all = [r["L_ilium_t1"] + r["L_sacrum_t1"] for r in results]

print("=" * 70)
print("PER-SLICE SI JOINT ANALYSIS (BME detection)")
print("=" * 70)
print(f"Slices analyzed: {len(results)}")
print(f"Location range: {results[0]['loc_mm']:.1f} to {results[-1]['loc_mm']:.1f} mm")
print()
print(
    f"{'z':>3} {'loc':>7} {'L_il_T2':>7} {'L_sc_T2':>7} {'R_il_T2':>7} {'R_sc_T2':>7} {'R-L diff':>8}  {'R > L by':>7}"
)
for r in results:
    rt2 = (r["R_ilium_t2"] + r["R_sacrum_t2"]) / 2
    lt2 = (r["L_ilium_t2"] + r["L_sacrum_t2"]) / 2
    diff = rt2 - lt2
    flag = "  ★" if diff > 0.05 else ""
    print(
        f"{r['z']:>3} {r['loc_mm']:>7.1f} {r['L_ilium_t2']:>7.3f} {r['L_sacrum_t2']:>7.3f} {r['R_ilium_t2']:>7.3f} {r['R_sacrum_t2']:>7.3f} {diff:>+8.3f}{flag}"
    )

# Summary statistics
right_mean_t2 = np.mean(right_t2_all) / 2
left_mean_t2 = np.mean(left_t2_all) / 2
right_mean_t1 = np.mean(right_t1_all) / 2
left_mean_t1 = np.mean(left_t1_all) / 2

print()
print("=== Summary across all coronal slices ===")
print(f"RIGHT  SI joint mean T2-water: {right_mean_t2:.4f}")
print(f"LEFT   SI joint mean T2-water: {left_mean_t2:.4f}")
print(f"RIGHT - LEFT difference:       {right_mean_t2 - left_mean_t2:+.4f}")
print()
print(f"RIGHT  SI joint mean T1:       {right_mean_t1:.4f}")
print(f"LEFT   SI joint mean T1:       {left_mean_t1:.4f}")
print(f"RIGHT - LEFT difference:       {right_mean_t1 - left_mean_t1:+.4f}")

# Count slices where RIGHT is brighter than LEFT on T2
right_brighter = sum(
    1
    for r in results
    if (r["R_ilium_t2"] + r["R_sacrum_t2"]) > (r["L_ilium_t2"] + r["L_sacrum_t2"]) + 0.05
)
print(f"\nSlices where RIGHT T2 brighter than LEFT by >0.05: {right_brighter}/{len(results)}")

# Save summary
summary = {
    "right_mean_t2_water": right_mean_t2,
    "left_mean_t2_water": left_mean_t2,
    "right_minus_left_t2": right_mean_t2 - left_mean_t2,
    "right_mean_t1": right_mean_t1,
    "left_mean_t1": left_mean_t1,
    "right_minus_left_t1": right_mean_t1 - left_mean_t1,
    "slices_right_brighter_count": right_brighter,
    "total_slices": len(results),
    "interpretation": "",
}
if right_mean_t2 - left_mean_t2 > 0.05:
    summary["interpretation"] = (
        "RIGHT SI joint shows increased fluid signal vs LEFT — suggests RIGHT-sided bone marrow edema (BME)."
    )
if right_mean_t1 - left_mean_t1 > 0.10:
    summary["interpretation"] += " RIGHT T1 brighter → fat metaplasia (chronic feature)."
with open(f"{ANALYSIS}/si_joint_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print(f"\n  → Saved: {ANALYSIS}/si_joint_summary.json")

# Plot the asymmetry profile
locs_arr = np.array([r["loc_mm"] for r in results])
r_t2 = np.array([(r["R_ilium_t2"] + r["R_sacrum_t2"]) / 2 for r in results])
l_t2 = np.array([(r["L_ilium_t2"] + r["L_sacrum_t2"]) / 2 for r in results])
r_t1 = np.array([(r["R_ilium_t1"] + r["R_sacrum_t1"]) / 2 for r in results])
l_t1 = np.array([(r["L_ilium_t1"] + r["L_sacrum_t1"]) / 2 for r in results])

fig, axes = plt.subplots(2, 1, figsize=(16, 10))
axes[0].plot(locs_arr, r_t2, "r-", label="RIGHT (patient right)", linewidth=2)
axes[0].plot(locs_arr, l_t2, "b-", label="LEFT (patient left)", linewidth=2)
axes[0].fill_between(
    locs_arr, l_t2, r_t2, where=r_t2 > l_t2, color="red", alpha=0.2, label="RIGHT > LEFT (BME)"
)
axes[0].set_title(
    "SI Joint Subchondral T2-WATER intensity per slice\n(Higher = more fluid/edema = active sacroiliitis feature)",
    fontsize=14,
)
axes[0].set_xlabel("Z location (mm)")
axes[0].set_ylabel("Mean T2-water intensity (subchondral)")
axes[0].legend()
axes[0].grid(alpha=0.3)

axes[1].plot(locs_arr, r_t1, "r-", label="RIGHT", linewidth=2)
axes[1].plot(locs_arr, l_t1, "b-", label="LEFT", linewidth=2)
axes[1].fill_between(
    locs_arr, l_t1, r_t1, where=r_t1 > l_t1, color="green", alpha=0.2, label="RIGHT > LEFT (fat)"
)
axes[1].set_title(
    "SI Joint Subchondral T1 intensity per slice\n(Higher T1 = fat metaplasia = chronic sacroiliitis feature)",
    fontsize=14,
)
axes[1].set_xlabel("Z location (mm)")
axes[1].set_ylabel("Mean T1 intensity (subchondral)")
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(f"{PREVIEW_DIR}/si_joint_per_slice_asymmetry.png", dpi=120, bbox_inches="tight")
plt.close()
print(f"  → Saved: {PREVIEW_DIR}/si_joint_per_slice_asymmetry.png")

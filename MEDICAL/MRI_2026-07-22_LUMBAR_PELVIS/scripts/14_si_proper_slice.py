"""Rebuild F3 showing the FULL CORONAL SLICE with annotations at correct landmarks.
The previous version used a 51-row band which doesn't show joints properly."""

import os
import json
import numpy as np
from scipy import ndimage
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse, FancyArrowPatch

VOL = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/volumes"
ANN = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/annotated"


def load_vol(key):
    z = np.load(f"{VOL}/{key}.npz")
    return z['vol'].astype(np.float32), z['slice_locs']


def normalize(arr):
    lo, hi = np.percentile(arr, [1, 99])
    return np.clip((arr.astype(np.float32) - lo) / (hi - lo), 0, 1)


cor_t1, locs_cor = load_vol('s13')
cor_t2, _ = load_vol('s14')
cor_t1_n = normalize(cor_t1)
cor_t2_n = normalize(cor_t2)

# z=30 (loc 22mm) — best visible SI joint slice
z = 30
sl_t1 = cor_t1_n[z]
sl_t2 = cor_t2_n[z]
H, W = sl_t1.shape
print(f"Slice z={z} (loc {locs_cor[z]:.1f} mm), shape=({H}, {W})")

# Find sacrum properly on FULL slice using T2-WATER (joints are dark, sacrum is bone = intermediate)
# Look at the central horizontal band where SI joint space should be
# SI joint space runs roughly rows 200-340 on coronal slices of adult pelvis
joint_row_band = slice(200, 340)  # rows containing the joint space

# Scan ALL columns to find bones. Bone is medium-bright on T2-WATER (between fluid and fat)
# Actually let's use T1 where bone is bright
sl_t1_band = sl_t1[joint_row_band, :]
sl_t2_band = sl_t2[joint_row_band, :]

# Find the central column range where bone is brightest (sacrum body + SI joints)
# Sacrum is a wide bone in the center
# Find columns where T1 band mean > 0.3 (bright bone)
col_means = sl_t1_band.mean(axis=0)
bright_cols = col_means > 0.3
# Find runs of bright columns
runs = []
in_run = False
start = 0
for i, b in enumerate(bright_cols):
    if b and not in_run:
        start = i
        in_run = True
    elif not b and in_run:
        runs.append((start, i, i - start))
        in_run = False
if in_run:
    runs.append((start, len(bright_cols), len(bright_cols) - start))

print(f"Bright column runs in SI joint band: {runs}")

# The widest run = sacrum
runs.sort(key=lambda r: -r[2])
sacrum_left = runs[0][0]
sacrum_right = runs[0][1]
print(f"Sacrum: cols {sacrum_left}..{sacrum_right}, width {runs[0][2]}")

# Find SI joints — they are dark lines immediately flanking the sacrum
# Look at T2 (water) band: dark lines = joint space
# Search in narrow columns immediately outside sacrum
search_width = 15  # px on each side
left_search = sl_t2_band[:, max(0, sacrum_left - search_width):sacrum_left]
right_search = sl_t2_band[:, sacrum_right:sacrum_right + search_width]

left_joint_col = None
right_joint_col = None

if left_search.shape[1] > 0:
    col_means_t2_left = left_search.mean(axis=0)
    left_joint_local = np.argmin(col_means_t2_left)  # darkest = joint space
    left_joint_col = max(0, sacrum_left - search_width) + left_joint_local
    print(f"Right SI joint (image LEFT = patient RIGHT): col {left_joint_col} (darkness {col_means_t2_left[left_joint_local]:.3f})")

if right_search.shape[1] > 0:
    col_means_t2_right = right_search.mean(axis=0)
    right_joint_local = np.argmin(col_means_t2_right)
    right_joint_col = sacrum_right + right_joint_local
    print(f"Left SI joint (image RIGHT = patient LEFT): col {right_joint_col} (darkness {col_means_t2_right[right_joint_local]:.3f})")

# Now generate figure: FULL slice with annotations
fig, axes = plt.subplots(2, 2, figsize=(20, 14))

axes[0, 0].imshow(sl_t1, cmap='gray', aspect='auto')
axes[0, 0].set_title(f'COR T1 z={z} (loc {locs_cor[z]:.1f} mm) — full slice\nSacrum detected cols {sacrum_left}-{sacrum_right}, R joint col {left_joint_col}, L joint col {right_joint_col}',
                     fontsize=12)
axes[0, 0].axis('off')

axes[0, 1].imshow(sl_t2, cmap='gray', aspect='auto')
axes[0, 1].set_title('COR WATER T2 — same slice', fontsize=12)
axes[0, 1].axis('off')

# Annotated T1
axes[1, 0].imshow(sl_t1, cmap='gray', aspect='auto')
# Sacrum box
rect_s = Rectangle((sacrum_left, 100), sacrum_right - sacrum_left, 250,
                  edgecolor='yellow', facecolor='none', linewidth=3)
axes[1, 0].add_patch(rect_s)
axes[1, 0].text((sacrum_left + sacrum_right) // 2, 90, 'SACRUM (median bone)',
               color='yellow', fontsize=11, fontweight='bold', ha='center',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))

# Right SI joint (patient RIGHT = image LEFT)
if left_joint_col:
    rect_r = Rectangle((left_joint_col - 8, 100), 16, 250,
                      edgecolor='red', facecolor='none', linewidth=3.5)
    axes[1, 0].add_patch(rect_r)
    axes[1, 0].text(left_joint_col - 12, 380, 'patient RIGHT\nSI joint',
                   color='red', fontsize=11, fontweight='bold', ha='right',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.95,
                            edgecolor='red', linewidth=1.5))

# Left SI joint (patient LEFT)
if right_joint_col:
    rect_l = Rectangle((right_joint_col - 8, 100), 16, 250,
                      edgecolor='blue', facecolor='none', linewidth=3.5)
    axes[1, 0].add_patch(rect_l)
    axes[1, 0].text(right_joint_col + 18, 380, 'patient LEFT\nSI joint',
                   color='blue', fontsize=11, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.95,
                            edgecolor='blue', linewidth=1.5))

axes[1, 0].set_title('COR T1 — ANNOTATED', fontsize=12)
axes[1, 0].axis('off')

# Annotated T2 — show BME patterns
axes[1, 1].imshow(sl_t2, cmap='gray', aspect='auto')
rect_s2 = Rectangle((sacrum_left, 100), sacrum_right - sacrum_left, 250,
                   edgecolor='yellow', facecolor='none', linewidth=3)
axes[1, 1].add_patch(rect_s2)
if left_joint_col:
    rect_r2 = Rectangle((left_joint_col - 8, 100), 16, 250,
                       edgecolor='red', facecolor='none', linewidth=3.5)
    axes[1, 1].add_patch(rect_r2)
if right_joint_col:
    rect_l2 = Rectangle((right_joint_col - 8, 100), 16, 250,
                       edgecolor='blue', facecolor='none', linewidth=3.5)
    axes[1, 1].add_patch(rect_l2)

# Add label for BME
axes[1, 1].text(10, 460, 'BME detection:\nBright = inflammation in subchondral bone',
              color='white', fontsize=10, fontweight='bold',
              bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))
axes[1, 1].set_title('COR WATER T2 — ANNOTATED\nLook for subchondral bright signal (BME)', fontsize=12)
axes[1, 1].axis('off')

plt.suptitle(f'F3: SI JOINTS — Slice z={z} (loc {locs_cor[z]:.1f} mm)\n'
            f'CORONAL FULL VIEW with detected landmarks',
            fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{ANN}/F3_Right_SI_joint_CORRECT.png', dpi=90, bbox_inches='tight')
plt.close()
print(f"\n  → Saved: {ANN}/F3_Right_SI_joint_CORRECT.png")

# Save landmarks
landmarks = {
    'slice_z': int(z),
    'loc_mm': float(locs_cor[z]),
    'sacrum_left_col': int(sacrum_left),
    'sacrum_right_col': int(sacrum_right),
    'right_si_joint_col': int(left_joint_col) if left_joint_col else None,
    'left_si_joint_col': int(right_joint_col) if right_joint_col else None,
}
with open(f'{ANN}/_F3_LANDMARKS.json', 'w') as f:
    json.dump(landmarks, f, indent=2)
print(json.dumps(landmarks, indent=2))

"""Final SI joint annotation. Looking at the contact sheet, the SI joints in z=30
are at approximately rows 80-200 (in the UPPER portion of the image)."""

import os
import json
import numpy as np
from scipy import ndimage
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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

z = 30
sl_t1 = cor_t1_n[z]
sl_t2 = cor_t2_n[z]
H, W = sl_t1.shape

# Looking at the contact sheet, SI joints in coronal slice at this loc appear in:
# - Rows ~70-200 (superior part, flanking sacrum)
# - Sacrum is the central bright bone in upper half of image
# - SI joints are dark lines flanking it

# Scan the upper half for bones (T1 bright)
sl_t1_upper = sl_t1[60:220, :]
col_means_upper = sl_t1_upper.mean(axis=0)
# Find columns where bone is bright
thresh = 0.25
bright = col_means_upper > thresh

# Find runs
runs = []
in_run = False
start = 0
for i, b in enumerate(bright):
    if b and not in_run:
        start = i
        in_run = True
    elif not b and in_run:
        runs.append((start, i, i - start))
        in_run = False
if in_run:
    runs.append((start, len(bright), len(bright) - start))

runs.sort(key=lambda r: -r[2])
# The widest = sacrum body
sacrum_left = runs[0][0]
sacrum_right = runs[0][1]
sacrum_center = (sacrum_left + sacrum_right) // 2
print(f"Sacrum detected: cols {sacrum_left}..{sacrum_right}, center {sacrum_center}")
print(f"All bright column runs in upper half: {runs}")

# Find SI joints — they are dark lines immediately flanking the sacrum
# Use WATER T2 where joints appear DARK on bright surrounding bone
joint_search = slice(sacrum_left - 15, sacrum_left - 3)
right_search = slice(sacrum_right + 3, sacrum_right + 15)
left_t2 = sl_t2[60:220, joint_search]
right_t2 = sl_t2[60:220, right_search]

if left_t2.shape[1] > 0:
    col_means = left_t2.mean(axis=0)
    local_idx = np.argmin(col_means)
    right_joint_col = sacrum_left - 15 + local_idx
    print(f"Right (patient RIGHT = image LEFT) SI joint dark col {right_joint_col} (mean darkness {col_means[local_idx]:.3f})")
else:
    right_joint_col = sacrum_left - 5

if right_t2.shape[1] > 0:
    col_means = right_t2.mean(axis=0)
    local_idx = np.argmin(col_means)
    left_joint_col = sacrum_right + 3 + local_idx
    print(f"Left (patient LEFT = image RIGHT) SI joint dark col {left_joint_col} (mean darkness {col_means[local_idx]:.3f})")
else:
    left_joint_col = sacrum_right + 5

# Now annotate properly
fig, axes = plt.subplots(2, 2, figsize=(20, 14))

axes[0, 0].imshow(sl_t1, cmap='gray', aspect='auto')
axes[0, 0].set_title(f'COR T1 z={z} (loc {locs_cor[z]:.1f} mm) — full slice\n'
                    f'Sacrum: cols {sacrum_left}-{sacrum_right} | R joint col {right_joint_col} | L joint col {left_joint_col}',
                     fontsize=11)
axes[0, 0].axis('off')

axes[0, 1].imshow(sl_t2, cmap='gray', aspect='auto')
axes[0, 1].set_title('COR WATER T2 — same slice', fontsize=11)
axes[0, 1].axis('off')

# Annotated
axes[1, 0].imshow(sl_t1, cmap='gray', aspect='auto')

# Sacrum box — confined to upper portion where the bone actually is
# Sacrum is between rows 60-220 (upper half)
sacrum_row_top = 60
sacrum_row_bot = 220
rect_s = Rectangle((sacrum_left, sacrum_row_top), sacrum_right - sacrum_left,
                  sacrum_row_bot - sacrum_row_top,
                  edgecolor='yellow', facecolor='none', linewidth=3)
axes[1, 0].add_patch(rect_s)
axes[1, 0].text((sacrum_left + sacrum_right) // 2, sacrum_row_top - 10, 'SACRUM',
               color='yellow', fontsize=11, fontweight='bold', ha='center',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))

# Right SI joint (patient RIGHT = image LEFT)
rect_r = Rectangle((right_joint_col - 6, sacrum_row_top), 12, sacrum_row_bot - sacrum_row_top,
                  edgecolor='red', facecolor='none', linewidth=3.5)
axes[1, 0].add_patch(rect_r)
axes[1, 0].text(right_joint_col - 12, (sacrum_row_top + sacrum_row_bot) // 2,
               'patient RIGHT\nSI joint',
               color='red', fontsize=11, fontweight='bold', ha='right', va='center',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.95,
                        edgecolor='red', linewidth=1.5))

# Left SI joint
rect_l = Rectangle((left_joint_col - 6, sacrum_row_top), 12, sacrum_row_bot - sacrum_row_top,
                  edgecolor='blue', facecolor='none', linewidth=3.5)
axes[1, 0].add_patch(rect_l)
axes[1, 0].text(left_joint_col + 18, (sacrum_row_top + sacrum_row_bot) // 2,
               'patient LEFT\nSI joint',
               color='blue', fontsize=11, fontweight='bold', ha='left', va='center',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.95,
                        edgecolor='blue', linewidth=1.5))

axes[1, 0].set_title('COR T1 — ANNOTATED (UPPER HALF shows SI joints)', fontsize=12)
axes[1, 0].axis('off')

# Annotated T2
axes[1, 1].imshow(sl_t2, cmap='gray', aspect='auto')
rect_s2 = Rectangle((sacrum_left, sacrum_row_top), sacrum_right - sacrum_left,
                   sacrum_row_bot - sacrum_row_top,
                   edgecolor='yellow', facecolor='none', linewidth=3)
axes[1, 1].add_patch(rect_s2)
rect_r2 = Rectangle((right_joint_col - 6, sacrum_row_top), 12, sacrum_row_bot - sacrum_row_top,
                   edgecolor='red', facecolor='none', linewidth=3.5)
axes[1, 1].add_patch(rect_r2)
rect_l2 = Rectangle((left_joint_col - 6, sacrum_row_top), 12, sacrum_row_bot - sacrum_row_top,
                   edgecolor='blue', facecolor='none', linewidth=3.5)
axes[1, 1].add_patch(rect_l2)
axes[1, 1].text(10, 460,
              'BME detection (subchondral):\nBright tissue = inflammation\nCompare right vs left',
              color='white', fontsize=10, fontweight='bold',
              bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))
axes[1, 1].set_title('COR WATER T2 — ANNOTATED', fontsize=12)
axes[1, 1].axis('off')

plt.suptitle(f'F3: SI JOINTS — Slice z={z} (loc {locs_cor[z]:.1f} mm)\n'
            f'Try MULTIPLE slices — true SI joints may be at z=32-34 (more posterior)',
            fontsize=13, fontweight='bold')
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
    'sacrum_center_col': int(sacrum_center),
    'right_si_joint_col': int(right_joint_col),
    'left_si_joint_col': int(left_joint_col),
    'sacrum_row_top': int(sacrum_row_top),
    'sacrum_row_bot': int(sacrum_row_bot),
    'note': 'THIS SLICE may not be optimal — SI joints visible in upper half but may be more prominent in z=32-34',
}
with open(f'{ANN}/_F3_LANDMARKS.json', 'w') as f:
    json.dump(landmarks, f, indent=2)
print(json.dumps(landmarks, indent=2))

"""Detect SI joint landmarks automatically at z=30 (best visible slice).
Find sacrum center column, joint columns, then place annotations accurately."""

import os
import json
import numpy as np
from scipy import ndimage
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse

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

# Best SI joint slice
z = 30  # loc 22mm
sl_t1 = cor_t1_n[z]
sl_t2 = cor_t2_n[z]

# Find sacrum on T1 — it's bone (bright on T1)
# Scan a horizontal band at middle of image (where SI joints are)
H, W = sl_t1.shape
band_top = int(H * 0.45)
band_bot = int(H * 0.60)
band = sl_t1[band_top:band_bot, :]

# Find the largest bright region in the central 30% of the image
# (sacrum should be there)
midcol = W // 2
sacrum_search = band[:, midcol - 80:midcol + 80]
# Threshold for bright bone
thresh = 0.35
bone_mask = sacrum_search > thresh
labeled, n = ndimage.label(bone_mask)
sizes = ndimage.sum(bone_mask, labeled, range(1, n + 1))

sacrum_left_col = None
sacrum_right_col = None
sacrum_center_col = None

if n > 0:
    # Find largest bright cluster = sacrum
    biggest = np.argmax(sizes) + 1
    if sizes[biggest - 1] > 50:
        ys, xs = np.where(labeled == biggest)
        sacrum_left_col = xs.min() + (midcol - 80)
        sacrum_right_col = xs.max() + (midcol - 80)
        sacrum_center_col = (sacrum_left_col + sacrum_right_col) // 2
        print(f"Sacrum detected at columns: {sacrum_left_col}..{sacrum_right_col}, center={sacrum_center_col}")
else:
    print("No sacrum found, using centrality")
    sacrum_center_col = midcol
    sacrum_left_col = midcol - 25
    sacrum_right_col = midcol + 25

# Now find SI joints — they are DARK columns immediately flanking the sacrum
# Look at T2 (water) for joints: they appear as dark lines
band_t2 = sl_t2[band_top:band_bot, :]
# The joints are darker than surrounding bone
darkness = -band_t2  # invert so joints are bright peaks
# Search columns just outside sacrum
search_left = slice(sacrum_left_col - 30, sacrum_left_col - 5)
search_right = slice(sacrum_right_col + 5, sacrum_right_col + 30)
left_band = darkness[band_top:band_bot, search_left].mean(axis=0)
right_band = darkness[band_top:band_bot, search_right].mean(axis=0)
left_joint_local = np.argmax(left_band)
right_joint_local = np.argmax(right_band)
left_joint_col = (sacrum_left_col - 30) + left_joint_local
right_joint_col = (sacrum_right_col + 5) + right_joint_local

print(f"RIGHT SI joint (image LEFT = patient RIGHT) at col: {left_joint_col}")
print(f"LEFT SI joint (image RIGHT = patient LEFT) at col: {right_joint_col}")
print(f"Sacrum center: {sacrum_center_col}")
print(f"Image dimensions: H={H}, W={W}")

# === Generate F3 annotated ===
band_top, band_bot = int(H * 0.45), int(H * 0.55)
band_t1 = sl_t1[band_top:band_bot, :]
band_t2 = sl_t2[band_top:band_bot, :]

fig, axes = plt.subplots(2, 2, figsize=(18, 10))
axes[0, 0].imshow(band_t1, cmap='gray', aspect='auto')
axes[0, 0].set_title(f'COR T1 z=30 (loc {locs_cor[z]:.1f} mm) — band at SI joint level\nWidth: {W}, height: {band_t1.shape[0]}',
                     fontsize=12)
axes[0, 0].axis('off')

axes[0, 1].imshow(band_t2, cmap='gray', aspect='auto')
axes[0, 1].set_title('COR WATER T2 — same band', fontsize=12)
axes[0, 1].axis('off')

# Annotated
axes[1, 0].imshow(band_t1, cmap='gray', aspect='auto')
# Sacrum (between left_joint_col and right_joint_col)
if sacrum_left_col and sacrum_right_col:
    rect = Rectangle((sacrum_left_col, 0), sacrum_right_col - sacrum_left_col,
                     band_t1.shape[0], edgecolor='yellow', facecolor='none', linewidth=3)
    axes[1, 0].add_patch(rect)
    axes[1, 0].text((sacrum_left_col + sacrum_right_col) / 2, 5, 'SACRUM',
                    color='yellow', fontsize=11, fontweight='bold', ha='center',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))
# Right SI joint subchondral (image LEFT)
rect_r = Rectangle((left_joint_col - 5, 0), 12, band_t1.shape[0],
                  edgecolor='red', facecolor='none', linewidth=3.5)
axes[1, 0].add_patch(rect_r)
axes[1, 0].text(left_joint_col - 8, band_t1.shape[0] / 2, 'R\nSI\nJ',
                color='red', fontsize=11, fontweight='bold', ha='right', va='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9,
                         edgecolor='red', linewidth=1.5))
# Left SI joint subchondral (image RIGHT)
rect_l = Rectangle((right_joint_col - 5, 0), 12, band_t1.shape[0],
                  edgecolor='blue', facecolor='none', linewidth=3.5)
axes[1, 0].add_patch(rect_l)
axes[1, 0].text(right_joint_col + 18, band_t1.shape[0] / 2, 'L\nSI\nJ',
                color='blue', fontsize=11, fontweight='bold', ha='left', va='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9,
                         edgecolor='blue', linewidth=1.5))
axes[1, 0].set_title('COR T1 — ANNOTATED\nRed box = patient RIGHT SI joint (image LEFT)\nBlue box = patient LEFT SI joint',
                     fontsize=12)
axes[1, 0].axis('off')

# Annotated T2
axes[1, 1].imshow(band_t2, cmap='gray', aspect='auto')
if sacrum_left_col and sacrum_right_col:
    rect = Rectangle((sacrum_left_col, 0), sacrum_right_col - sacrum_left_col,
                     band_t2.shape[0], edgecolor='yellow', facecolor='none', linewidth=3)
    axes[1, 1].add_patch(rect)
rect_r = Rectangle((left_joint_col - 5, 0), 12, band_t2.shape[0],
                  edgecolor='red', facecolor='none', linewidth=3.5)
axes[1, 1].add_patch(rect_r)
rect_l = Rectangle((right_joint_col - 5, 0), 12, band_t2.shape[0],
                  edgecolor='blue', facecolor='none', linewidth=3.5)
axes[1, 1].add_patch(rect_l)
axes[1, 1].set_title('COR WATER T2 — ANNOTATED\nBME (bright) appears as lighter subchondral bone',
                     fontsize=12)
axes[1, 1].axis('off')

plt.suptitle(f'F3: RIGHT SI JOINT — Slice z=30 (loc {locs_cor[z]:.1f} mm) — CORRECT LANDMARKS\n'
            f'Sacrum: cols {sacrum_left_col}-{sacrum_right_col} | Right joint: col {left_joint_col} | Left joint: col {right_joint_col}',
            fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{ANN}/F3_Right_SI_joint_CORRECT.png', dpi=100, bbox_inches='tight')
plt.close()
print(f"\n  → {ANN}/F3_Right_SI_joint_CORRECT.png")

# Save the landmarks for reuse
landmarks = {
    'slice_z': z,
    'loc_mm': float(locs_cor[z]),
    'sacrum_left_col': int(sacrum_left_col),
    'sacrum_right_col': int(sacrum_right_col),
    'sacrum_center_col': int(sacrum_center_col),
    'right_si_joint_col': int(left_joint_col),   # image LEFT = patient RIGHT
    'left_si_joint_col': int(right_joint_col),    # image RIGHT = patient LEFT
    'image_shape': [int(H), int(W)],
    'band_top_row': int(band_top),
    'band_bot_row': int(band_bot),
}
with open(f'{ANN}/_F3_LANDMARKS.json', 'w') as f:
    json.dump(landmarks, f, indent=2)
print(f"\n  → Landmarks saved: {ANN}/_F3_LANDMARKS.json")
print(json.dumps(landmarks, indent=2))

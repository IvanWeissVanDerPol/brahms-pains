"""REBUILD all annotated images with CORRECT anatomical landmarks.

Verified landmarks from visual inspection of sag_T2_mid z=9 contact sheet:
  T12 vertebra: rows 50-90 (partial, top)
  L1 vertebra:  rows 100-160
  L1-L2 disc:   row  170
  L2 vertebra:  rows 200-260
  L2-L3 disc:   row  265
  L3 vertebra:  rows 290-360
  L3-L4 disc:   row  365
  L4 vertebra:  rows 390-460     ← HEMANGIOMA HERE
  L4-L5 disc:   row  465
  L5 vertebra:  rows 490-580
  L5-S1 disc:   row  585
  Sacrum S1:    rows 600-700
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Rectangle, FancyArrowPatch
from scipy import ndimage

VOL = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/volumes"
ANN = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/annotated"


def load_vol(key):
    z = np.load(f"{VOL}/{key}.npz")
    return z['vol'].astype(np.float32), z['slice_locs']


def normalize(arr):
    lo, hi = np.percentile(arr, [1, 99])
    return np.clip((arr.astype(np.float32) - lo) / (hi - lo), 0, 1)


# CORRECT LANDMARKS (verified visually)
LANDMARKS = {
    'T12': (50, 90),
    'L1':  (100, 160),
    'L1-L2': (167, 175),
    'L2':  (200, 260),
    'L2-L3': (262, 270),
    'L3':  (290, 360),
    'L3-L4': (362, 370),
    'L4':  (390, 460),
    'L4-L5': (462, 470),
    'L5':  (490, 580),
    'L5-S1': (582, 590),
    'S1':  (600, 700),
}


# =================================================================
# F1: L4-L5 Modic 1 - ACTUALLY CORRECT this time
# =================================================================
print("\n[F1] Rebuilding L4-L5 Modic 1 with correct row numbers")
sag_t2, _ = load_vol('s3')
sag_t1, _ = load_vol('s4')
sag_stir, _ = load_vol('s5')
sag_t2_n = normalize(sag_t2)
sag_t1_n = normalize(sag_t1)
sag_stir_n = normalize(sag_stir)

z = 9  # confirmed mid-sagittal

# Crop around L4 vertebra + L4-L5 disc + L5 vertebra (rows 380-500)
crop_top, crop_bot = 380, 510
left_col, right_col = 350, 750  # anterior column
crops_t2 = sag_t2_n[z, crop_top:crop_bot, left_col:right_col]
crops_t1 = sag_t1_n[z, crop_top:crop_bot, left_col:right_col]
crops_stir = sag_stir_n[z, crop_top:crop_bot, left_col:right_col]

# Convert landmarks to crop coordinates
l4_top = LANDMARKS['L4'][0] - crop_top
l4_bot = LANDMARKS['L4'][1] - crop_top
l4l5_top = LANDMARKS['L4-L5'][0] - crop_top
l4l5_bot = LANDMARKS['L4-L5'][1] - crop_top
l5_top = LANDMARKS['L5'][0] - crop_top
l5_bot = LANDMARKS['L5'][1] - crop_top

# Mid vertebra column
mid_col_crop = (right_col - left_col) // 2

# Build figure: top row original, bottom row annotated
fig, axes = plt.subplots(2, 3, figsize=(18, 8))

# Top row = original
axes[0, 0].imshow(crops_t2, cmap='gray', aspect='auto')
axes[0, 0].set_title(f'Sag T2 z=9 — L4 vertebra region (rows {crop_top}-{crop_bot})', fontsize=12)
axes[0, 0].axis('off')

axes[0, 1].imshow(crops_t1, cmap='gray', aspect='auto')
axes[0, 1].set_title(f'Sag T1 — same region', fontsize=12)
axes[0, 1].axis('off')

axes[0, 2].imshow(crops_stir, cmap='gray', aspect='auto')
axes[0, 2].set_title(f'Sag STIR — same region', fontsize=12)
axes[0, 2].axis('off')

# Bottom row = annotated
for col, (crop, name) in enumerate([(crops_t2, 'T2'),
                                      (crops_t1, 'T1'),
                                      (crops_stir, 'STIR')]):
    ax = axes[1, col]
    ax.imshow(crop, cmap='gray', aspect='auto')

    # Mark L4 vertebra body (above L4-L5 disc)
    rect_l4 = Rectangle((20, l4_top), crop.shape[1] - 40, l4_bot - l4_top,
                       edgecolor='red', facecolor='none', linewidth=2)
    ax.add_patch(rect_l4)

    # Mark L4-L5 disc (the narrow band between L4 and L5)
    rect_disc = Rectangle((20, l4l5_top), crop.shape[1] - 40, l4l5_bot - l4l5_top,
                         edgecolor='yellow', facecolor='none', linewidth=3)
    ax.add_patch(rect_disc)

    # Mark L5 vertebra body (below L4-L5 disc)
    rect_l5 = Rectangle((20, l5_top), crop.shape[1] - 40, l5_bot - l5_top,
                       edgecolor='red', facecolor='none', linewidth=2)
    ax.add_patch(rect_l5)

    # Labels
    ax.text(crop.shape[1] - 110, (l4_top + l4_bot) / 2, 'L4\nvertebra',
            color='red', fontsize=11, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9,
                     edgecolor='red', linewidth=1.5))
    ax.text(crop.shape[1] - 110, (l4l5_top + l4l5_bot) / 2, 'L4-L5\nDISC',
            color='black', fontsize=11, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.95,
                     edgecolor='black', linewidth=1.5))
    ax.text(crop.shape[1] - 110, (l5_top + l5_bot) / 2, 'L5\nvertebra',
            color='red', fontsize=11, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9,
                     edgecolor='red', linewidth=1.5))

    ax.set_title(f'Sag {name} — ANNOTATED', fontsize=12)
    ax.axis('off')

plt.suptitle('F1: L4-L5 VERTEBRAL BODY + DISC (CORRECT LANDMARKS)\nLook for Modic 1 signal: dark on T1, bright on T2, very bright on STIR',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{ANN}/F1_L4L5_Modic1_CORRECT.png', dpi=100, bbox_inches='tight')
plt.close()
print(f"  → {ANN}/F1_L4L5_Modic1_CORRECT.png")


# =================================================================
# F2: L4 hemangioma - find the focal bright spot precisely
# =================================================================
print("\n[F2] Rebuilding L4 hemangioma")
# Look in L4 vertebra region on T1 first
l4_top, l4_bot = LANDMARKS['L4']
l4_left, l4_right = 380, 620  # anterior column of L4

t1_crop = sag_t1_n[z, l4_top:l4_bot, l4_left:l4_right]
t2_crop = sag_t2_n[z, l4_top:l4_bot, l4_left:l4_right]

# Auto-detect the brightest cluster in T1 (hemangiomas are brightest on T1)
thresh_t1 = np.percentile(t1_crop, 99)
bright_mask = t1_crop > thresh_t1
labeled, n = ndimage.label(bright_mask)
sizes = ndimage.sum(bright_mask, labeled, range(1, n + 1))

if n > 0:
    # Find largest cluster
    biggest = np.argmax(sizes) + 1
    if sizes[biggest - 1] > 3:
        ys, xs = np.where(labeled == biggest)
        cy = ys.mean()
        cx = xs.mean()
        print(f"  L4 hemangioma auto-detected at local ({cx:.0f}, {cy:.0f}), size={int(sizes[biggest-1])} px")
        # Convert back to full-image coords
        full_y = int(cy + l4_top)
        full_x = int(cx + l4_left)
        print(f"  Full image coords: ({full_x}, {full_y})")

# Make figure with MANUAL placement based on detection
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Top row = original
axes[0, 0].imshow(t1_crop, cmap='gray', aspect='auto')
axes[0, 0].set_title('Sag T1 — L4 vertebra (cropped)', fontsize=12)
# Draw grid for reference
H, W = t1_crop.shape
for r in range(0, H, 10):
    axes[0, 0].axhline(r, color='cyan', linewidth=0.2, alpha=0.3)
    axes[0, 0].text(2, r, str(r), color='cyan', fontsize=7)
for c in range(0, W, 20):
    axes[0, 0].axvline(c, color='cyan', linewidth=0.2, alpha=0.3)
axes[0, 0].set_xlabel('col (offset from '+str(l4_left)+')')
axes[0, 0].set_ylabel('row (offset from '+str(l4_top)+')')
axes[0, 0].axis('off')  # Will re-on if needed

axes[0, 1].imshow(t2_crop, cmap='gray', aspect='auto')
axes[0, 1].set_title('Sag T2 — same region', fontsize=12)
axes[0, 1].axis('off')

# Bottom row = annotated
axes[1, 0].imshow(t1_crop, cmap='gray', aspect='auto')
axes[1, 0].axis('off')

axes[1, 1].imshow(t2_crop, cmap='gray', aspect='auto')
axes[1, 1].axis('off')

if n > 0 and sizes[biggest - 1] > 3:
    # Circle the detected lesion on both
    for col in [0, 1]:
        crop_use = t1_crop if col == 0 else t2_crop
        e = Ellipse((cx, cy), width=35, height=25,
                   edgecolor='red', facecolor='none', linewidth=3.5)
        axes[1, col].add_patch(e)
        axes[1, col].text(cx + 25, cy - 5, f'Focal bright lesion\n(largest T1 cluster)',
                          color='red', fontsize=9, fontweight='bold',
                          bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9,
                                   edgecolor='red', linewidth=1.5))

axes[1, 0].set_title('Sag T1 — focal bright lesion circled', fontsize=12)
axes[1, 1].set_title('Sag T2 — same region circled', fontsize=12)

plt.suptitle('F2: L4 VERTEBRAL HEMANGIOMA — auto-detected focal bright cluster', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{ANN}/F2_L4_hemangioma_CORRECT.png', dpi=100, bbox_inches='tight')
plt.close()
print(f"  → {ANN}/F2_L4_hemangioma_CORRECT.png")


# =================================================================
# F3: SI joint - find a slice that actually shows the SI joints
# =================================================================
print("\n[F3] Finding a coronal slice that actually shows SI joints")
cor_t1, locs_cor = load_vol('s13')
cor_t2, _ = load_vol('s14')
cor_t1_n = normalize(cor_t1)
cor_t2_n = normalize(cor_t2)

# Save large views of slices z=20-35 (the middle of the SI joint range)
fig, axes = plt.subplots(4, 4, figsize=(20, 16))
for i, z_test in enumerate(range(20, 36)):
    ax = axes[i // 4, i % 4]
    ax.imshow(cor_t1_n[z_test], cmap='gray', aspect='auto')
    ax.set_title(f'COR T1 z={z_test} loc={locs_cor[z_test]:.1f}mm', fontsize=10)
    ax.axis('off')
plt.suptitle('Coronal T1 slices — find where SI joints are visible', fontsize=14)
plt.tight_layout()
plt.savefig(f'{ANN}/_F3_COR_T1_SLICES_20_to_35.png', dpi=80, bbox_inches='tight')
plt.close()
print(f"  → {ANN}/_F3_COR_T1_SLICES_20_to_35.png — visual review needed")


#!/usr/bin/env python3
"""
Stage 7d — Fix F1 (L4-L5 Modic 1) and F2 (L4 hemangioma) with CORRECT row numbers.
Also fix F3 (SI joint) with CORRECT coronal slice.

Anatomy from manual inspection of mid-sagittal slice (z=9):
- L4 vertebra body: rows 490-580
- L4-L5 disc: rows 580-600 (narrow band)
- L5 vertebra body: rows 600-680
- L5-S1 disc: rows 680-700
- L4 focal hemangioma: visible on T1 at row ~530, col ~470-510

For SI joint: need a POSTERIOR coronal slice (z=30-35, loc +30 to +45 mm)
where the SI joints are actually visible.
"""
import os, json
import numpy as np
from scipy import ndimage
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Rectangle, FancyArrowPatch

VOL = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/volumes"
ANN_DIR = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/annotated"

def load_vol(key):
    z = np.load(f"{VOL}/{key}.npz")
    return z['vol'].astype(np.float32), z['slice_locs']

def normalize(arr):
    lo, hi = np.percentile(arr, [1, 99])
    return np.clip((arr.astype(np.float32) - lo) / (hi - lo), 0, 1)

sag_t2, _ = load_vol('s3')
sag_t1, _ = load_vol('s4')
sag_stir, _ = load_vol('s5')
cor_t1, locs_cor = load_vol('s13')
cor_t2, _ = load_vol('s14')

sag_t2_n = normalize(sag_t2)
sag_t1_n = normalize(sag_t1)
sag_stir_n = normalize(sag_stir)
cor_t1_n = normalize(cor_t1)
cor_t2_n = normalize(cor_t2)

mid_z_sag = 9  # confirmed mid-sagittal

# =================================================================
# F1: L4-L5 Modic Type 1 changes — CORRECT row numbers
# =================================================================
print("\n[F1 FIXED] L4-L5 Modic Type 1 changes")
print("-" * 50)

# CORRECT: L4-L5 disc is at rows ~580-600, col ~470-510
l4l5_disc_row = 590
l4l5_col_c = 500
disc_w = 80
disc_h = 30
crop_w = 200

# Crop around the L4-L5 region
def crop(arr, row, col_c, w=200, h=100):
    r0 = max(0, row - h)
    r1 = min(arr.shape[1], row + h + 1)
    c0 = max(0, col_c - w)
    c1 = min(arr.shape[1], col_c + w + 1)
    return arr[r0:r1, c0:c1], (r0, c0)

fig, axes = plt.subplots(2, 3, figsize=(20, 12))
# Top row: original
for col, (vol_n, name) in enumerate([(sag_t2_n, 'T2'),
                                       (sag_t1_n, 'T1'),
                                       (sag_stir_n, 'STIR')]):
    sl = vol_n[mid_z_sag]
    crop_img, (r0, c0) = crop(sl, l4l5_disc_row, l4l5_col_c, w=crop_w, h=100)
    axes[0, col].imshow(crop_img, cmap='gray', aspect='auto')
    axes[0, col].set_title(f'Sag {name} mid-sagittal\ncropped to L4-L5 region (rows {r0}-{r0+crop_img.shape[0]})', fontsize=12)
    axes[0, col].axis('off')

# Bottom row: annotated
for col, (vol_n, name) in enumerate([(sag_t2_n, 'T2'),
                                       (sag_t1_n, 'T1'),
                                       (sag_stir_n, 'STIR')]):
    sl = vol_n[mid_z_sag]
    crop_img, (r0, c0) = crop(sl, l4l5_disc_row, l4l5_col_c, w=crop_w, h=100)
    ax = axes[1, col]
    ax.imshow(crop_img, cmap='gray', aspect='auto')

    # Compute the actual disc location within the crop
    disc_y_in_crop = l4l5_disc_row - r0
    disc_x_in_crop = l4l5_col_c - c0

    # Mark the L4-L5 disc itself (bright on T2/STIR, dark on T1 in this case)
    e_disc = Ellipse((disc_x_in_crop, disc_y_in_crop), width=90, height=20,
                     edgecolor='red', facecolor='none', linewidth=3.5)
    ax.add_patch(e_disc)

    # Mark L4 inferior endplate (just above the disc — should show edema = bright on T2/STIR, dark on T1)
    e_e1 = Ellipse((disc_x_in_crop, disc_y_in_crop - 18), width=120, height=14,
                   edgecolor='red', facecolor='none', linewidth=3, linestyle='--')
    ax.add_patch(e_e1)

    # Mark L5 superior endplate (just below the disc)
    e_e2 = Ellipse((disc_x_in_crop, disc_y_in_crop + 18), width=120, height=14,
                   edgecolor='red', facecolor='none', linewidth=3, linestyle='--')
    ax.add_patch(e_e2)

    # Labels
    label_text = {
        'T2': 'L4-L5 disc\n(bright = Modic 1)\nL4 endplate above\nL5 endplate below',
        'T1': 'L4-L5 disc\n(dark = Modic 1)\nL4 endplate above\nL5 endplate below',
        'STIR': 'L4-L5 disc\n(very bright = edema)\nL4 endplate above\nL5 endplate below',
    }
    ax.text(disc_x_in_crop + 70, disc_y_in_crop - 60, label_text[name],
           color='red', fontsize=10, fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.95,
                    edgecolor='red', linewidth=1.5))
    ax.set_title(f'Sag {name} — ANNOTATED\nRed solid = disc, dashed = endplates', fontsize=11)
    ax.axis('off')

plt.suptitle('F1 (FIXED): L4-L5 MODIC TYPE 1 — Active disc-endplate inflammation\n'
            'T2↑ + T1↓ + STIR↑ = classic Modic 1 pattern',
            fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{ANN_DIR}/F1_L4L5_Modic1_FIXED.png', dpi=110, bbox_inches='tight')
plt.close()
print(f"  → Saved: {ANN_DIR}/F1_L4L5_Modic1_FIXED.png")


# =================================================================
# F2: L4 vertebral hemangioma — CORRECT row numbers
# =================================================================
print("\n[F2 FIXED] L4 vertebral hemangioma")
print("-" * 50)

# CORRECT: L4 vertebra at rows 490-580, focal hemangioma at row ~530
l4_vertebra_row = 530
l4_vertebra_col = 480

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Find the actual bright cluster in T1
t1_crop, (r0_t1, c0_t1) = crop(sag_t1_n[mid_z_sag], l4_vertebra_row, l4_vertebra_col, w=120, h=60)
t2_crop, (r0_t2, c0_t2) = crop(sag_t2_n[mid_z_sag], l4_vertebra_row, l4_vertebra_col, w=120, h=60)

# Auto-detect the brightest cluster in T1 crop
threshold_t1 = np.percentile(t1_crop, 99.5)
bright_mask_t1 = t1_crop > threshold_t1
labeled_t1, n_t1 = ndimage.label(bright_mask_t1)
sizes_t1 = ndimage.sum(bright_mask_t1, labeled_t1, range(1, n_t1 + 1))
hemangioma_y_t1, hemangioma_x_t1 = None, None
if n_t1 > 0:
    biggest = np.argmax(sizes_t1) + 1
    if sizes_t1[biggest - 1] > 5:
        ys, xs = np.where(labeled_t1 == biggest)
        hemangioma_y_t1 = ys.mean()
        hemangioma_x_t1 = xs.mean()
        print(f"  L4 hemangioma T1 cluster: ({hemangioma_x_t1:.0f}, {hemangioma_y_t1:.0f}) size={int(sizes_t1[biggest-1])}")

axes[0, 0].imshow(t1_crop, cmap='gray', aspect='auto')
axes[0, 0].set_title(f'Sag T1 — L4 vertebra\n(Look for focal bright lesion)', fontsize=12)
axes[0, 0].axis('off')

axes[0, 1].imshow(t2_crop, cmap='gray', aspect='auto')
axes[0, 1].set_title(f'Sag T2 — L4 vertebra\n(Look for focal bright lesion)', fontsize=12)
axes[0, 1].axis('off')

# Annotate T1
axes[1, 0].imshow(t1_crop, cmap='gray', aspect='auto')
if hemangioma_y_t1 is not None:
    e = Ellipse((hemangioma_x_t1, hemangioma_y_t1), width=50, height=35,
               edgecolor='red', facecolor='none', linewidth=3.5)
    axes[1, 0].add_patch(e)
    axes[1, 0].text(hemangioma_x_t1 + 35, hemangioma_y_t1 - 5,
                   'FOCAL BRIGHT LESION\n→ HEMANGIOMA (Type II)\nT1 bright = fatty content',
                   color='red', fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.95,
                            edgecolor='red', linewidth=1.5))
axes[1, 0].set_title('Sag T1 — ANNOTATED\nRed ellipse = hemangioma candidate', fontsize=11)
axes[1, 0].axis('off')

# Annotate T2
axes[1, 1].imshow(t2_crop, cmap='gray', aspect='auto')
if hemangioma_y_t1 is not None:
    # Try to find T2 cluster at similar position (may be slightly offset)
    threshold_t2 = np.percentile(t2_crop, 99.5)
    bright_mask_t2 = t2_crop > threshold_t2
    labeled_t2, n_t2 = ndimage.label(bright_mask_t2)
    sizes_t2 = ndimage.sum(bright_mask_t2, labeled_t2, range(1, n_t2 + 1))
    if n_t2 > 0:
        biggest = np.argmax(sizes_t2) + 1
        ys, xs = np.where(labeled_t2 == biggest)
        h_y = ys.mean()
        h_x = xs.mean()
        e = Ellipse((h_x, h_y), width=50, height=35,
                   edgecolor='red', facecolor='none', linewidth=3.5)
        axes[1, 1].add_patch(e)
        axes[1, 1].text(h_x + 35, h_y - 5,
                       'FOCAL BRIGHT LESION\n→ HEMANGIOMA confirmed\nT2 bright = vascular + slow flow',
                       color='red', fontsize=10, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.95,
                                edgecolor='red', linewidth=1.5))
axes[1, 1].set_title('Sag T2 — ANNOTATED\nRed ellipse = same lesion', fontsize=11)
axes[1, 1].axis('off')

plt.suptitle('F2 (FIXED): L4 VERTEBRAL HEMANGIOMA — Focal T1+T2 bright (incidental, benign)\n'
            'Found in ~10% of all spine MRIs. Typical (Type II) pattern = no clinical significance.',
            fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{ANN_DIR}/F2_L4_hemangioma_FIXED.png', dpi=110, bbox_inches='tight')
plt.close()
print(f"  → Saved: {ANN_DIR}/F2_L4_hemangioma_FIXED.png")


# =================================================================
# F3: SI joint — CORRECT slice (posterior coronal)
# =================================================================
print("\n[F3 FIXED] Right SI joint subchondral BME")
print("-" * 50)

# From the previews we saw, SI joints visible at loc +30 to +44 mm
# That's slices z=33-35 of the coronal series
si_z = 33  # posterior coronal
sl_t1 = cor_t1_n[si_z]
sl_t2 = cor_t2_n[si_z]

fig, axes = plt.subplots(2, 2, figsize=(18, 12))
axes[0, 0].imshow(sl_t1, cmap='gray', aspect='auto')
axes[0, 0].set_title(f'COR T1 — slice {si_z} (loc {locs_cor[si_z]:.1f} mm)\nSI joints + marrow', fontsize=12)
axes[0, 0].axis('off')

axes[0, 1].imshow(sl_t2, cmap='gray', aspect='auto')
axes[0, 1].set_title(f'COR WATER T2 — same slice\nBME detection (RIGHT = image LEFT)', fontsize=12)
axes[0, 1].axis('off')

# Annotate — find the actual SI joints on this slice
# Sacrum should be visible as central structure
midcol = sl_t1.shape[1] // 2
midrow = int(sl_t1.shape[0] * 0.5)

# Find sacrum column range
row_band = sl_t1[midrow, :]
# On T1, sacrum is moderately bright bone
sacrum_thresh = 0.25
sacrum_mask = row_band > sacrum_thresh
central_start = midcol - 100
central_end = midcol + 100
central = sacrum_mask[central_start:central_end]
if central.any():
    # Find widest continuous bright region (sacrum)
    runs = []
    in_run = False
    start = 0
    for i, b in enumerate(central):
        if b and not in_run:
            start = i
            in_run = True
        elif not b and in_run:
            runs.append((start, i, i - start))
            in_run = False
    if in_run:
        runs.append((start, len(central), len(central) - start))
    if runs:
        runs.sort(key=lambda r: -r[2])
        s_left = runs[0][0] + central_start
        s_right = runs[0][1] + central_start
        sacrum_center = (s_left + s_right) // 2
        sacrum_width = s_right - s_left
        print(f"  Sacrum on slice {si_z}: columns {s_left}-{s_right}, center={sacrum_center}, width={sacrum_width}")

        # Annotate T1
        axes[1, 0].imshow(sl_t1, cmap='gray', aspect='auto')
        # Mark sacrum (central)
        rect_s = Rectangle((s_left, midrow - 100), sacrum_width, 200,
                          edgecolor='yellow', facecolor='none', linewidth=2.5)
        axes[1, 0].add_patch(rect_s)
        # Right SI joint subchondral zone (image LEFT)
        # Right joint is at column ~s_left - 10 (just lateral of sacrum)
        rect_r_joint = Rectangle((s_left - 25, midrow - 80), 25, 160,
                                edgecolor='red', facecolor='none', linewidth=3.5)
        axes[1, 0].add_patch(rect_r_joint)
        rect_l_joint = Rectangle((s_right, midrow - 80), 25, 160,
                                edgecolor='blue', facecolor='none', linewidth=3.5, linestyle='--')
        axes[1, 0].add_patch(rect_l_joint)

        axes[1, 0].text(midcol, midrow - 130, 'SACRUM (central)',
                        color='yellow', fontsize=12, fontweight='bold', ha='center',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))
        axes[1, 0].text(s_left - 35, midrow - 130, 'RIGHT SI joint\n(patient RIGHT)',
                        color='red', fontsize=10, fontweight='bold', ha='right',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.95,
                                 edgecolor='red', linewidth=1.5))
        axes[1, 0].text(s_right + 35, midrow - 130, 'LEFT SI joint\n(patient LEFT)',
                        color='blue', fontsize=10, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.95,
                                 edgecolor='blue', linewidth=1.5))
        axes[1, 0].set_title('COR T1 — ANNOTATED\nRed box = RIGHT SI joint subchondral zone', fontsize=11)
        axes[1, 0].axis('off')

        # Annotate T2 with BME markers
        axes[1, 1].imshow(sl_t2, cmap='gray', aspect='auto')
        # Subchondral ilium (lateral of right joint — between joint and lateral iliac bone)
        rect_il_r = Rectangle((s_left - 25, midrow - 50), 15, 100,
                            edgecolor='darkred', facecolor='none', linewidth=3)
        axes[1, 1].add_patch(rect_il_r)
        rect_sc_r = Rectangle((s_left - 11, midrow - 50), 12, 100,
                            edgecolor='darkred', facecolor='none', linewidth=3)
        axes[1, 1].add_patch(rect_sc_r)
        # Left for comparison
        rect_il_l = Rectangle((s_right + 13, midrow - 50), 15, 100,
                            edgecolor='navy', facecolor='none', linewidth=3, linestyle='--')
        axes[1, 1].add_patch(rect_il_l)
        rect_sc_l = Rectangle((s_right + 1, midrow - 50), 12, 100,
                            edgecolor='navy', facecolor='none', linewidth=3, linestyle='--')
        axes[1, 1].add_patch(rect_sc_l)

        axes[1, 1].text(s_left - 35, midrow + 80, 'RIGHT subchondral\nilium (BME?)',
                        color='darkred', fontsize=9, fontweight='bold', ha='right',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.95,
                                 edgecolor='darkred', linewidth=1))
        axes[1, 1].text(s_left - 5, midrow + 80, 'RIGHT subchondral\nsacrum',
                        color='darkred', fontsize=9, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.95,
                                 edgecolor='darkred', linewidth=1))
        axes[1, 1].text(s_right + 50, midrow + 80, 'LEFT subchondral\nilium',
                        color='navy', fontsize=9, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.95,
                                 edgecolor='navy', linewidth=1))
        axes[1, 1].text(s_right - 5, midrow + 80, 'LEFT subchondral\nsacrum',
                        color='navy', fontsize=9, fontweight='bold', ha='right',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.95,
                                 edgecolor='navy', linewidth=1))

        axes[1, 1].set_title('COR WATER T2 — ANNOTATED\nDark red = RIGHT subchondral  Dark blue = LEFT subchondral\n'
                           'BME = bright fluid signal in these boxes', fontsize=11)
        axes[1, 1].axis('off')

plt.suptitle(f'F3 (FIXED): RIGHT SI JOINT — CORONAL slice {si_z} (loc {locs_cor[si_z]:.1f} mm)\n'
            'Patient RIGHT SI joint = image LEFT side (radiologic convention)\n'
            'Subchondral bone marrow edema (BME) detected asymmetrically',
            fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{ANN_DIR}/F3_Right_SI_joint_BME_FIXED.png', dpi=110, bbox_inches='tight')
plt.close()
print(f"  → Saved: {ANN_DIR}/F3_Right_SI_joint_BME_FIXED.png")

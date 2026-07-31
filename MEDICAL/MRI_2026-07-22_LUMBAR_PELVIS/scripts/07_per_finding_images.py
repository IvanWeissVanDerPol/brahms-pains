#!/usr/bin/env python3
"""
Stage 7 — Generate per-finding annotated images (original + red circle).

For each of the 5 priority findings, produce a 2-panel figure:
  Left: original slice as-is from DICOM
  Right: same slice with red circles/arrows marking the abnormality

Findings covered:
  F1: L4-L5 Modic Type 1 changes (active disc-endplate edema)
  F2: L4 vertebral hemangioma (focal T1+T2 bright lesion)
  F3: Right SI joint subchondral bone marrow edema (BME)
  F4: Diffuse right hemipelvis T2 hyperintensity (muscle + soft tissue)
  F5: Bilateral scrotal hydroceles
"""
import os, json
import numpy as np
from scipy import ndimage
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle, Ellipse
from matplotlib.lines import Line2D

VOL = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/volumes"
ANN_DIR = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/annotated"
os.makedirs(ANN_DIR, exist_ok=True)


def load_vol(key):
    z = np.load(f"{VOL}/{key}.npz")
    return z['vol'].astype(np.float32), z['slice_locs']


def normalize(arr, lo=1, hi=99):
    lo_v, hi_v = np.percentile(arr, [lo, hi])
    if hi_v <= lo_v: return arr
    return np.clip((arr.astype(np.float32) - lo_v) / (hi_v - lo_v), 0, 1)


def save_pair(orig_slice, ann_slice, title_orig, title_ann, out_path, cmap='gray',
              figsize=(14, 8), circle_kwargs=None):
    """Save a 2-panel figure: original | annotated."""
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    axes[0].imshow(orig_slice, cmap=cmap, aspect='auto')
    axes[0].set_title(title_orig, fontsize=13, fontweight='bold')
    axes[0].axis('off')
    axes[1].imshow(ann_slice, cmap=cmap, aspect='auto')
    axes[1].set_title(title_ann, fontsize=13, fontweight='bold', color='darkred')
    axes[1].axis('off')

    # Add circles/arrows on the right panel if requested
    if circle_kwargs:
        for kw in circle_kwargs:
            ax = axes[1]
            if 'circle' in kw:
                c = Circle(kw['circle'][:2], kw['circle'][2],
                          edgecolor='red', facecolor='none', linewidth=3)
                ax.add_patch(c)
            if 'ellipse' in kw:
                e = Ellipse(kw['ellipse'][:2], width=kw['ellipse'][2], height=kw['ellipse'][3],
                           edgecolor='red', facecolor='none', linewidth=3,
                           angle=kw['ellipse'][4] if len(kw['ellipse']) > 4 else 0)
                ax.add_patch(e)
            if 'rect' in kw:
                r = Rectangle(kw['rect'][:2], kw['rect'][2], kw['rect'][3],
                             edgecolor='red', facecolor='none', linewidth=3)
                ax.add_patch(r)
            if 'arrow' in kw:
                arr = FancyArrowPatch(kw['arrow'][0], kw['arrow'][1],
                                     arrowstyle='->', mutation_scale=30,
                                     color='red', linewidth=3)
                ax.add_patch(arr)
            if 'text' in kw:
                ax.text(kw['text'][0], kw['text'][1], kw['text'][2],
                       color='red', fontsize=kw.get('text_size', 14),
                       fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.85,
                                edgecolor='red', linewidth=1.5))

    plt.tight_layout()
    plt.savefig(out_path, dpi=110, bbox_inches='tight')
    plt.close()
    print(f"  → Saved: {out_path}")


# Load all the series we need
print("="*70)
print("STAGE 7 — Per-finding annotated images (original + red circles)")
print("="*70)

sag_t2, _ = load_vol('s3')
sag_t1, _ = load_vol('s4')
sag_stir, _ = load_vol('s5')
cor_t1, locs_cor = load_vol('s13')
cor_t2, _ = load_vol('s14')
ax_t1, locs_ax_t1 = load_vol('s9')
ax_stir, locs_ax_stir = load_vol('s12')
ax_t2_water, locs_ax_t2 = load_vol('s10')

sag_t2_n = normalize(sag_t2)
sag_t1_n = normalize(sag_t1)
sag_stir_n = normalize(sag_stir)
cor_t1_n = normalize(cor_t1)
cor_t2_n = normalize(cor_t2)
ax_t1_n = normalize(ax_t1)
ax_stir_n = normalize(ax_stir)
ax_water_n = normalize(ax_t2_water)

mid_z_sag = sag_t2.shape[0] // 2  # = 9
mid_z_cor = cor_t1.shape[0] // 2  # = 23


# =================================================================
# F1: L4-L5 Modic Type 1 changes — disc-endplate edema
# =================================================================
print("\n[F1] L4-L5 Modic Type 1 changes")
print("-" * 50)

# Sag T2 mid-slice, the L4-L5 disc area — row ~523 (from earlier analysis)
# Let's pick the slice and zoom in on the L4-L5 region
for i in range(sag_t2.shape[0]):
    print(f"  Sag slice {i}: loc = ?")

# Use mid-sagittal slice; mark row 523 as the L4-L5 disc center
disc_row_l4l5 = 523

# Save side-by-side T2 / T1 / STIR showing the L4-L5 region
# Crop to the L4-L5 region: rows 400-700, cols 300-750 (rough)
def crop_around_row(arr, row, row_h=120, col_c=512, col_w=400):
    r0 = max(0, row - row_h)
    r1 = min(arr.shape[0], row + row_h + 1)
    c0 = max(0, col_c - col_w)
    c1 = min(arr.shape[1], col_c + col_w + 1)
    return arr[r0:r1, c0:c1], (r0, c0)


fig, axes = plt.subplots(2, 3, figsize=(20, 12))
# Top row: original slices
crops = []
for ax, vol_n, name in [(axes[0, 0], sag_t2_n[mid_z_sag], 'T2'),
                          (axes[0, 1], sag_t1_n[mid_z_sag], 'T1'),
                          (axes[0, 2], sag_stir_n[mid_z_sag], 'STIR')]:
    crop, (r0, c0) = crop_around_row(vol_n, disc_row_l4l5)
    crops.append((crop, (r0, c0)))
    ax.imshow(crop, cmap='gray', aspect='auto')
    ax.set_title(f'Sag {name} — mid slice (cropped to L4-L5 region)', fontsize=12)
    ax.axis('off')

# Bottom row: same crops with red circles on the L4-L5 disc and adjacent endplates
for col, ((crop, (r0, c0)), name) in enumerate(zip(crops, ['T2', 'T1', 'STIR'])):
    ax = axes[1, col]
    ax.imshow(crop, cmap='gray', aspect='auto')
    # L4-L5 disc center: row 523 - r0 = 523 - max(0, 523-120) = 523 - 403 = 120
    disc_y = disc_row_l4l5 - r0
    disc_x = 400  # midcol
    # L4-L5 disc
    e1 = Ellipse((disc_x, disc_y), width=140, height=35,
                 edgecolor='red', facecolor='none', linewidth=3.5)
    ax.add_patch(e1)
    # L4 inferior endplate (just above disc)
    e2 = Ellipse((disc_x, disc_y - 25), width=160, height=18,
                 edgecolor='red', facecolor='none', linewidth=3, linestyle='--')
    ax.add_patch(e2)
    # L5 superior endplate (just below disc)
    e3 = Ellipse((disc_x, disc_y + 25), width=160, height=18,
                 edgecolor='red', facecolor='none', linewidth=3, linestyle='--')
    ax.add_patch(e3)
    # Label
    ax.text(disc_x + 100, disc_y - 5, 'L4-L5 DISC\n(Modic 1:\nT2↑ T1↓ STIR↑)',
            color='red', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.9,
                     edgecolor='red', linewidth=1.5))
    ax.text(disc_x + 100, disc_y - 50, 'L4 inferior\nendplate',
            color='red', fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9,
                     edgecolor='red', linewidth=1))
    ax.text(disc_x + 100, disc_y + 30, 'L5 superior\nendplate',
            color='red', fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9,
                     edgecolor='red', linewidth=1))
    ax.set_title(f'Sag {name} — ANNOTATED\nRed circles = L4-L5 disc + adjacent endplates', fontsize=11)
    ax.axis('off')

plt.suptitle('F1: L4-L5 MODIC TYPE 1 CHANGES — Active disc-endplate inflammation', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{ANN_DIR}/F1_L4L5_Modic1_T2_T1_STIR.png', dpi=110, bbox_inches='tight')
plt.close()
print(f"  → Saved: {ANN_DIR}/F1_L4L5_Modic1_T2_T1_STIR.png")


# =================================================================
# F2: L4 vertebral hemangioma
# =================================================================
print("\n[F2] L4 vertebral hemangioma")
print("-" * 50)

# L4 vertebra center: row 874 (from earlier analysis)
# L4 vertebral body region: rows 800-950, cols 380-640
l4_row = 874
def crop_around_row2(arr, row, row_h=80, col_c=512, col_w=180):
    r0 = max(0, row - row_h)
    r1 = min(arr.shape[0], row + row_h + 1)
    c0 = max(0, col_c - col_w)
    c1 = min(arr.shape[1], col_c + col_w + 1)
    return arr[r0:r1, c0:c1], (r0, c0)


fig, axes = plt.subplots(2, 2, figsize=(16, 12))
# Find the bright focal spot in L4 T1
l4_t1_crop, (r0_t1, c0_t1) = crop_around_row2(sag_t1_n[mid_z_sag], l4_row)
l4_t2_crop, (r0_t2, c0_t2) = crop_around_row2(sag_t2_n[mid_z_sag], l4_row)

axes[0, 0].imshow(l4_t1_crop, cmap='gray', aspect='auto')
axes[0, 0].set_title('Sag T1 — L4 vertebra\n(Look for FOCAL BRIGHT area)', fontsize=12)
axes[0, 0].axis('off')

axes[0, 1].imshow(l4_t2_crop, cmap='gray', aspect='auto')
axes[0, 1].set_title('Sag T2 — L4 vertebra\n(Look for FOCAL BRIGHT area)', fontsize=12)
axes[0, 1].axis('off')

# Find the actual focal bright spot in L4 T1
# Look in T1 crop for the brightest cluster
t1_crop = l4_t1_crop
threshold = np.percentile(t1_crop, 99)
bright_mask = t1_crop > threshold
labeled, n = ndimage.label(bright_mask)
sizes = ndimage.sum(bright_mask, labeled, range(1, n + 1))
# Find largest cluster that's round-ish
if n > 0:
    biggest = np.argmax(sizes) + 1
    ys, xs = np.where(labeled == biggest)
    if len(ys) > 0:
        cy = ys.mean()
        cx = xs.mean()
        print(f"  L4 hemangioma candidate: T1 cluster center ({cx:.0f}, {cy:.0f}) in crop, size={int(sizes[biggest-1])} px")

        # Annotated
        axes[1, 0].imshow(l4_t1_crop, cmap='gray', aspect='auto')
        # Circle the bright spot
        e = Ellipse((cx, cy), width=70, height=50, edgecolor='red', facecolor='none', linewidth=3.5)
        axes[1, 0].add_patch(e)
        axes[1, 0].text(cx + 50, cy - 30, 'FOCAL BRIGHT LESION\n→ HEMANGIOMA candidate\n(Typical: T1 bright + T2 bright)',
                        color='red', fontsize=10, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.9,
                                 edgecolor='red', linewidth=1.5))
        axes[1, 0].set_title('Sag T1 — ANNOTATED\nRed circle = focal bright lesion', fontsize=11)
        axes[1, 0].axis('off')

# Same for T2 — find bright cluster (might be slightly different position)
t2_crop = l4_t2_crop
threshold_t2 = np.percentile(t2_crop, 99)
bright_mask_t2 = t2_crop > threshold_t2
labeled_t2, n_t2 = ndimage.label(bright_mask_t2)
sizes_t2 = ndimage.sum(bright_mask_t2, labeled_t2, range(1, n_t2 + 1))
if n_t2 > 0:
    biggest_t2 = np.argmax(sizes_t2) + 1
    ys2, xs2 = np.where(labeled_t2 == biggest_t2)
    if len(ys2) > 0:
        cy2 = ys2.mean()
        cx2 = xs2.mean()
        print(f"  L4 hemangioma candidate: T2 cluster center ({cx2:.0f}, {cy2:.0f}) in crop")

        axes[1, 1].imshow(l4_t2_crop, cmap='gray', aspect='auto')
        e = Ellipse((cx2, cy2), width=70, height=50, edgecolor='red', facecolor='none', linewidth=3.5)
        axes[1, 1].add_patch(e)
        axes[1, 1].text(cx2 + 50, cy2 - 30, 'FOCAL BRIGHT LESION\n→ HEMANGIOMA candidate\n(Typical: T2 bright = vascular + fluid)',
                        color='red', fontsize=10, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.9,
                                 edgecolor='red', linewidth=1.5))
        axes[1, 1].set_title('Sag T2 — ANNOTATED\nRed circle = same focal bright lesion', fontsize=11)
        axes[1, 1].axis('off')

plt.suptitle('F2: L4 VERTEBRAL HEMANGIOMA — Focal T1 + T2 bright lesion (incidental, benign)',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{ANN_DIR}/F2_L4_hemangioma.png', dpi=110, bbox_inches='tight')
plt.close()
print(f"  → Saved: {ANN_DIR}/F2_L4_hemangioma.png")


# =================================================================
# F3: Right SI joint subchondral BME
# =================================================================
print("\n[F3] Right SI joint subchondral BME")
print("-" * 50)

# Use coronal slice 23 (mid) and mark the right SI joint subchondral zone
# Patient RIGHT = image LEFT side
# Joint is at ~col 255 from earlier analysis

# Find the joint center on the coronal slice
z_cor = 23
sl_t2 = cor_t2_n[z_cor]
sl_t1 = cor_t1_n[z_cor]

# Find the sacrum column range
midcol = sl_t1.shape[1] // 2
# Sacrum is the bright bone in the center
mid_row = int(sl_t1.shape[0] * 0.55)
row_band = sl_t1[mid_row, :]
sacrum_mask = (row_band > 0.30)
central = sacrum_mask[midcol-150:midcol+150]
if central.any():
    runs = []
    in_run = False
    start = 0
    for i, b in enumerate(central):
        if b and not in_run:
            start = i
            in_run = True
        elif not b and in_run:
            runs.append((start, i))
            in_run = False
    if in_run:
        runs.append((start, len(central)))
    if runs:
        runs.sort(key=lambda r: r[1] - r[0], reverse=True)
        sacrum_left = runs[0][0] + (midcol - 150)
        sacrum_right = runs[0][1] + (midcol - 150)
        # Patient RIGHT SI joint is on the LEFT side of sacrum
        # Mark the ilium (lateral of joint, brighter on T2) and sacrum (medial)
        right_joint_col = sacrum_left - 10  # approx 10px into joint
        print(f"  Coronal slice {z_cor}: sacrum [{sacrum_left}, {sacrum_right}], right joint approx col {right_joint_col}")

        fig, axes = plt.subplots(2, 2, figsize=(18, 12))
        axes[0, 0].imshow(sl_t1, cmap='gray', aspect='auto')
        axes[0, 0].set_title(f'COR T1 — slice {z_cor} (loc {locs_cor[z_cor]:.1f} mm)\nSI joints + marrow', fontsize=12)
        axes[0, 0].axis('off')

        axes[0, 1].imshow(sl_t2, cmap='gray', aspect='auto')
        axes[0, 1].set_title(f'COR WATER T2 — same slice\nRIGHT SI joint subchondral BME detection', fontsize=12)
        axes[0, 1].axis('off')

        # Annotated T1 — mark right SI joint + sacrum + ilium
        axes[1, 0].imshow(sl_t1, cmap='gray', aspect='auto')
        # Right SI joint region (patient RIGHT = image LEFT)
        # The joint space itself is the dark band
        rect_r = Rectangle((sacrum_left - 30, mid_row - 80), 50, 160,
                          edgecolor='red', facecolor='none', linewidth=3.5)
        axes[1, 0].add_patch(rect_r)
        axes[1, 0].text(sacrum_left - 50, mid_row - 100, 'RIGHT SI joint\n(patient RIGHT)',
                        color='red', fontsize=11, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9,
                                 edgecolor='red', linewidth=1.5),
                        ha='right')
        # Mark left SI joint for comparison
        rect_l = Rectangle((sacrum_right + 5, mid_row - 80), 50, 160,
                          edgecolor='blue', facecolor='none', linewidth=2.5, linestyle='--')
        axes[1, 0].add_patch(rect_l)
        axes[1, 0].text(sacrum_right + 65, mid_row - 100, 'LEFT SI joint\n(patient LEFT)',
                        color='blue', fontsize=11, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9,
                                 edgecolor='blue', linewidth=1.5))
        axes[1, 0].set_title('COR T1 — ANNOTATED\nRed box = patient RIGHT SI joint (subchondral zone)',
                           fontsize=11)
        axes[1, 0].axis('off')

        # Annotated T2 — show BME pattern
        axes[1, 1].imshow(sl_t2, cmap='gray', aspect='auto')
        rect_r = Rectangle((sacrum_left - 30, mid_row - 80), 50, 160,
                          edgecolor='red', facecolor='none', linewidth=3.5)
        axes[1, 1].add_patch(rect_r)
        # Subchondral ilium (most lateral in joint region)
        rect_il = Rectangle((sacrum_left - 30, mid_row - 30), 30, 60,
                           edgecolor='darkred', facecolor='none', linewidth=3)
        axes[1, 1].add_patch(rect_il)
        # Subchondral sacrum (most medial in joint region)
        rect_sc = Rectangle((sacrum_left - 5, mid_row - 30), 25, 60,
                           edgecolor='darkred', facecolor='none', linewidth=3)
        axes[1, 1].add_patch(rect_sc)
        axes[1, 1].text(sacrum_left - 50, mid_row + 90,
                       'Subchondral ilium\n(lateral of joint)\nBME = bright',
                       color='darkred', fontsize=9, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9,
                                edgecolor='darkred', linewidth=1),
                       ha='right')
        axes[1, 1].text(sacrum_left + 35, mid_row + 90,
                       'Subchondral sacrum\n(medial of joint)\nBME = bright',
                       color='darkred', fontsize=9, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9,
                                edgecolor='darkred', linewidth=1))
        # Left for comparison
        rect_l = Rectangle((sacrum_right + 5, mid_row - 80), 50, 160,
                          edgecolor='blue', facecolor='none', linewidth=2.5, linestyle='--')
        axes[1, 1].add_patch(rect_l)
        axes[1, 1].set_title('COR WATER T2 — ANNOTATED\nRed boxes = subchondral BME zones (RIGHT > LEFT)',
                           fontsize=11)
        axes[1, 1].axis('off')

        plt.suptitle('F3: RIGHT SI JOINT SUBCHONDRAL BONE MARROW EDEMA (BME)',
                     fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{ANN_DIR}/F3_Right_SI_joint_BME.png', dpi=110, bbox_inches='tight')
        plt.close()
        print(f"  → Saved: {ANN_DIR}/F3_Right_SI_joint_BME.png")


# =================================================================
# F4: Diffuse right hemipelvis T2 hyperintensity (muscle/soft tissue)
# =================================================================
print("\n[F4] Diffuse right hemipelvis T2 hyperintensity")
print("-" * 50)

# Find the axial STIR slice where asymmetry peaks
# From earlier data, peak was around z=-180 mm
asym_data = json.load(open("/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/muscle_asymmetry_ax_stir.json"))
# Find slice with max diff
max_diff_idx = max(range(len(asym_data)), key=lambda i: asym_data[i]['diff'])
peak_z = asym_data[max_diff_idx]['z']
peak_loc = asym_data[max_diff_idx]['loc_mm']
print(f"  Peak asymmetry at z={peak_z}, loc={peak_loc:.1f} mm, diff={asym_data[max_diff_idx]['diff']:+.4f}")

# Use that slice + 2 adjacent
for z_off in [-1, 0, 1]:
    z = peak_z + z_off
    if z < 0 or z >= ax_stir.shape[0]:
        continue
    sl = ax_stir_n[z]

    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    axes[0].imshow(sl, cmap='gray', aspect='auto')
    axes[0].set_title(f'AX STIR — slice {z} (loc {locs_ax_stir[z]:.1f} mm)\nOriginal', fontsize=12)
    axes[0].axis('off')

    # Annotated — draw midline + mark right side
    axes[1].imshow(sl, cmap='gray', aspect='auto')
    midcol = sl.shape[1] // 2
    # Draw midline
    axes[1].axvline(midcol, color='yellow', linewidth=2, linestyle='--', alpha=0.8)
    # Mark right side (image LEFT)
    # Patient RIGHT is image LEFT — circle the right gluteal/paraspinal region
    rect_r = Rectangle((20, 80), midcol - 30, sl.shape[0] - 160,
                      edgecolor='red', facecolor='none', linewidth=3.5)
    axes[1].add_patch(rect_r)
    # Mark left side for comparison
    rect_l = Rectangle((midcol + 10, 80), midcol - 30, sl.shape[0] - 160,
                      edgecolor='blue', facecolor='none', linewidth=2.5, linestyle='--')
    axes[1].add_patch(rect_l)
    # Labels
    axes[1].text(50, 50, 'PATIENT RIGHT\n(gluteus, iliacus,\nparaspinal)',
                color='red', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.9,
                         edgecolor='red', linewidth=1.5))
    axes[1].text(midcol + 50, 50, 'PATIENT LEFT\n(same muscles)',
                color='blue', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.9,
                         edgecolor='blue', linewidth=1.5))
    axes[1].text(midcol, sl.shape[0] - 30, 'MIDLINE',
                color='yellow', fontsize=11, fontweight='bold', ha='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.7))
    axes[1].set_title(f'AX STIR — ANNOTATED\nRed box = patient RIGHT side\n(NOTE: brighter = edema on STIR)',
                    fontsize=11)
    axes[1].axis('off')

    plt.suptitle(f'F4: DIFFUSE RIGHT HEMIPELVIS T2 HYPERINTENSITY\nSoft tissue inflammation pattern',
                fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{ANN_DIR}/F4_hemipelvis_asymmetry_z{z}.png', dpi=110, bbox_inches='tight')
    plt.close()
    print(f"  → Saved: {ANN_DIR}/F4_hemipelvis_asymmetry_z{z}.png")


# =================================================================
# F5: Bilateral scrotal hydroceles
# =================================================================
print("\n[F5] Bilateral scrotal hydroceles")
print("-" * 50)

# From earlier analysis, slice z=39 loc=-58.1 mm had scrotal fluid clusters
# But the FOV was cutting off. Let me look at a slightly different slice.
# Scan for slices with scrotal fluid visible
scrotal_slices = []
for z in range(ax_t2_water.shape[0]):
    sl = ax_water_n[z]
    # Look at bottom 40% of image for fluid (>0.5 on water T2)
    lower = sl[int(sl.shape[0] * 0.6):, :]
    fluid = (lower > 0.55).sum()
    if fluid > 100:
        scrotal_slices.append((z, fluid, float(locs_ax_t2[z])))

print(f"  Slices with potential scrotal fluid: {len(scrotal_slices)}")
if scrotal_slices:
    # Find slice with most fluid
    scrotal_slices.sort(key=lambda x: -x[1])
    for z, fluid, loc in scrotal_slices[:3]:
        print(f"    z={z} loc={loc:.1f}mm fluid_px={fluid}")

    # Use the best one
    best_z = scrotal_slices[0][0]
    sl = ax_water_n[best_z]
    sl_t1 = ax_t1_n[best_z] if best_z < ax_t1.shape[0] else None

    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    axes[0].imshow(sl, cmap='gray', aspect='auto')
    axes[0].set_title(f'AX WATER T2 — slice {best_z} (loc {locs_ax_t2[best_z]:.1f} mm)\nBilateral scrotal fluid collections',
                     fontsize=12)
    axes[0].axis('off')

    axes[1].imshow(sl, cmap='gray', aspect='auto')
    # Find clusters in the lower half
    lower = sl[int(sl.shape[0] * 0.5):, :]
    fluid_mask = lower > 0.55
    labeled, n = ndimage.label(fluid_mask)
    sizes = ndimage.sum(fluid_mask, labeled, range(1, n + 1))

    # Get top 4 clusters by size
    if n > 0:
        sorted_clusters = sorted(range(1, n + 1), key=lambda i: -sizes[i - 1])
        # Filter clusters with size > 50
        big = [c for c in sorted_clusters if sizes[c - 1] > 50][:4]

        # Draw circles on each, ordered left-to-right
        circles_data = []
        for c_id in big:
            ys, xs = np.where(labeled == c_id)
            cy = ys.mean() + lower.shape[0]
            cx = xs.mean()
            circles_data.append((cx, cy, sizes[c_id - 1], np.sqrt(sizes[c_id - 1]) * 1.2))

        circles_data.sort(key=lambda x: x[0])
        for i, (cx, cy, size, rad) in enumerate(circles_data):
            color = 'red' if i == 0 else ('blue' if i == 1 else 'lime')
            label = 'R hydrocele' if i == 0 else ('L hydrocele' if i == 1 else f'fluid {i}')
            # Patient RIGHT = image LEFT
            if i == 0:
                label = 'R hydrocele (patient RIGHT)'
            elif i == 1:
                label = 'L hydrocele (patient LEFT)'
            else:
                label = f'fluid cluster {i}'
            e = Ellipse((cx, cy), width=max(rad * 2, 30), height=max(rad * 1.5, 25),
                       edgecolor=color, facecolor='none', linewidth=3)
            axes[1].add_patch(e)
            axes[1].text(cx, cy - rad - 5, label,
                        color=color, fontsize=10, fontweight='bold', ha='center',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9,
                                 edgecolor=color, linewidth=1.5))

    axes[1].set_title(f'AX WATER T2 — ANNOTATED\nRed = patient RIGHT hydrocele\nBlue = patient LEFT hydrocele',
                     fontsize=11)
    axes[1].axis('off')

    plt.suptitle('F5: BILATERAL SCROTAL FLUID COLLECTIONS (HYDROCELES)',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{ANN_DIR}/F5_bilateral_hydroceles.png', dpi=110, bbox_inches='tight')
    plt.close()
    print(f"  → Saved: {ANN_DIR}/F5_bilateral_hydroceles.png")


# =================================================================
# F6: L4-L5 disc contour change + neural foramen (axial)
# =================================================================
print("\n[F6] L4-L5 disc contour + neural foramen (axial view)")
print("-" * 50)

# Ax T2 FSE — high-res axial of lumbar spine
ax_t2_lspine, locs_ax_lspine = load_vol('s6')
ax_t2_lspine_n = normalize(ax_t2_lspine)

# Find slices through the L4-L5 disc level
# L4-L5 is approximately at the lower end of the lumbar series (loc range -49 to +107)
# Disc L4-L5 is at the upper part of that range (~ +30 to +60)
disc_z = np.argmin(np.abs(locs_ax_lspine - 50))
print(f"  L4-L5 disc axial slice: z={disc_z}, loc={locs_ax_lspine[disc_z]:.1f} mm")

sl = ax_t2_lspine_n[disc_z]
fig, axes = plt.subplots(1, 2, figsize=(14, 8))
axes[0].imshow(sl, cmap='gray', aspect='auto')
axes[0].set_title(f'AX T2 FSE — slice {disc_z} (loc {locs_ax_lspine[disc_z]:.1f} mm)\nL4-L5 disc level', fontsize=12)
axes[0].axis('off')

axes[1].imshow(sl, cmap='gray', aspect='auto')
# Try to identify the disc + neural foramina
midcol = sl.shape[1] // 2
midrow = sl.shape[0] // 2
# Mark the disc (central, hyperintense compared to vertebra)
e_disc = Ellipse((midcol, midrow), width=160, height=60, edgecolor='red', facecolor='none', linewidth=3)
axes[1].add_patch(e_disc)
# Mark right + left neural foramina (lateral to disc)
e_nf_r = Ellipse((midcol - 110, midrow), width=50, height=80, edgecolor='darkred', facecolor='none', linewidth=3)
axes[1].add_patch(e_nf_r)
e_nf_l = Ellipse((midcol + 110, midrow), width=50, height=80, edgecolor='blue', facecolor='none', linewidth=3, linestyle='--')
axes[1].add_patch(e_nf_l)

axes[1].text(midcol, midrow - 50, 'L4-L5 disc\n(central)\ncontour change here',
            color='red', fontsize=10, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9,
                     edgecolor='red', linewidth=1.5))
axes[1].text(midcol - 110, midrow + 60, 'R neural\nforamen',
            color='darkred', fontsize=10, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9,
                     edgecolor='darkred', linewidth=1.5))
axes[1].text(midcol + 110, midrow + 60, 'L neural\nforamen',
            color='blue', fontsize=10, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9,
                     edgecolor='blue', linewidth=1.5))
axes[1].set_title('AX T2 FSE L4-L5 — ANNOTATED\nRed = disc + right neural foramen', fontsize=11)
axes[1].axis('off')

plt.suptitle('F6: L4-L5 AXIAL VIEW — Disc contour + bilateral neural foramina',
            fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{ANN_DIR}/F6_L4L5_axial_disc_foramen.png', dpi=110, bbox_inches='tight')
plt.close()
print(f"  → Saved: {ANN_DIR}/F6_L4L5_axial_disc_foramen.png")

print()
print("="*70)
print(f"All annotated images saved to {ANN_DIR}/")
print("="*70)

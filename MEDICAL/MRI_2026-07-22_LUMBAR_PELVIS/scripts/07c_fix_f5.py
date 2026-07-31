#!/usr/bin/env python3
"""
Stage 7c — Better F5 (bilateral hydroceles) using SAG series which shows the scrotum fully.
"""
import os, json
import numpy as np
from scipy import ndimage
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle

VOL = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/volumes"
ANN_DIR = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/annotated"

def load_vol(key):
    z = np.load(f"{VOL}/{key}.npz")
    return z['vol'].astype(np.float32), z['slice_locs']

def normalize(arr):
    lo, hi = np.percentile(arr, [1, 99])
    return np.clip((arr.astype(np.float32) - lo) / (hi - lo), 0, 1)

sag_water, locs_sag = load_vol('s16')
sag_water_n = normalize(sag_water)

# Find the scrotum: it has the highest fluid signal
peak_slice = 34  # from earlier scan: loc=-29.6 mm

# Find clusters on the best slice
sl = sag_water_n[peak_slice]

# Crop to lower half (where the scrotum hangs)
fig, axes = plt.subplots(1, 3, figsize=(20, 8))

# Original
axes[0].imshow(sl, cmap='gray', aspect='auto')
axes[0].set_title(f'SAG WATER T2 — slice {peak_slice} (loc {locs_sag[peak_slice]:.1f} mm)\nOriginal', fontsize=12)
axes[0].axis('off')

# Annotated with clusters
axes[1].imshow(sl, cmap='gray', aspect='auto')
# Look at lower half for fluid clusters
lower_mask = sl[int(sl.shape[0] * 0.55):, :] > 0.55
labeled, n = ndimage.label(lower_mask)
sizes = ndimage.sum(lower_mask, labeled, range(1, n + 1))
if n > 0:
    sorted_clusters = sorted(range(1, n + 1), key=lambda i: -sizes[i - 1])
    big = [c for c in sorted_clusters if sizes[c - 1] > 100][:4]

    # Get the largest 2 — these should be the bilateral hydroceles (one per side)
    big_2 = big[:2]
    cluster_info = []
    for c_id in big_2:
        ys, xs = np.where(labeled == c_id)
        cy = ys.mean() + int(sl.shape[0] * 0.55)
        cx = xs.mean()
        cluster_info.append((cx, cy, sizes[c_id - 1]))
    cluster_info.sort(key=lambda x: x[0])

    for i, (cx, cy, sz) in enumerate(cluster_info):
        # Determine which side (patient right = image left)
        midcol = sl.shape[1] // 2
        is_left = cx < midcol
        side = 'RIGHT' if is_left else 'LEFT'
        color = 'red' if is_left else 'blue'
        rad = np.sqrt(sz) * 1.2
        e = Ellipse((cx, cy), width=max(rad * 2, 40), height=max(rad * 1.8, 30),
                   edgecolor=color, facecolor='none', linewidth=3.5)
        axes[1].add_patch(e)
        axes[1].text(cx, cy - rad - 8, f'{side} hydrocele\n({int(sz)} px)',
                    color=color, fontsize=11, fontweight='bold', ha='center',
                    bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.95,
                             edgecolor=color, linewidth=1.5))

axes[1].set_title('SAG WATER T2 — ANNOTATED\nRed = patient RIGHT hydrocele  Blue = patient LEFT hydrocele', fontsize=11)
axes[1].axis('off')

# Now crop to the scrotum region for a clearer view
crop_top = int(sl.shape[0] * 0.55)
crop_bottom = sl.shape[0]
scrotum_crop = sl[crop_top:crop_bottom, :]

axes[2].imshow(scrotum_crop, cmap='gray', aspect='auto')
axes[2].set_title(f'CROPPED to scrotum\n(slice {peak_slice}, rows {crop_top}-{crop_bottom})', fontsize=11)
axes[2].axis('off')

plt.suptitle('F5: BILATERAL SCROTAL FLUID COLLECTIONS (HYDROCELES)\nSagittal view shows both hydroceles surrounding the testicles',
            fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{ANN_DIR}/F5_bilateral_hydroceles_SAG.png', dpi=110, bbox_inches='tight')
plt.close()
print(f"  → Saved: {ANN_DIR}/F5_bilateral_hydroceles_SAG.png")


# Also do an AX view at the scrotal level using the AX WATER T2 (s10) — extend FOV detection
ax_water, locs_ax = load_vol('s10')
ax_water_n = normalize(ax_water)

# Find slice with the highest fluid content in lower half
best_z = None
best_fluid = 0
for z in range(ax_water.shape[0]):
    sl_ax = ax_water_n[z]
    lower = sl_ax[int(sl_ax.shape[0] * 0.5):, :]
    fluid = (lower > 0.55).sum()
    if fluid > best_fluid:
        best_fluid = fluid
        best_z = z

print(f"  AX WATER T2 best scrotal slice: z={best_z}, loc={locs_ax[best_z]:.1f} mm, fluid={best_fluid}px")

if best_fluid > 50:
    sl = ax_water_n[best_z]
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    axes[0].imshow(sl, cmap='gray', aspect='auto')
    axes[0].set_title(f'AX WATER T2 — slice {best_z} (loc {locs_ax[best_z]:.1f} mm)\nOriginal', fontsize=12)
    axes[0].axis('off')

    axes[1].imshow(sl, cmap='gray', aspect='auto')
    lower_mask = sl[int(sl.shape[0] * 0.5):, :] > 0.55
    labeled, n = ndimage.label(lower_mask)
    sizes = ndimage.sum(lower_mask, labeled, range(1, n + 1))
    if n > 0:
        sorted_clusters = sorted(range(1, n + 1), key=lambda i: -sizes[i - 1])
        big = [c for c in sorted_clusters if sizes[c - 1] > 30][:4]
        cluster_info = []
        for c_id in big:
            ys, xs = np.where(labeled == c_id)
            cy = ys.mean() + int(sl.shape[0] * 0.5)
            cx = xs.mean()
            cluster_info.append((cx, cy, sizes[c_id - 1]))
        cluster_info.sort(key=lambda x: x[0])

        for i, (cx, cy, sz) in enumerate(cluster_info):
            midcol = sl.shape[1] // 2
            is_left = cx < midcol
            side = 'RIGHT' if is_left else 'LEFT'
            color = 'red' if is_left else 'blue'
            rad = np.sqrt(sz) * 1.5
            e = Ellipse((cx, cy), width=max(rad * 2, 30), height=max(rad * 1.5, 25),
                       edgecolor=color, facecolor='none', linewidth=3)
            axes[1].add_patch(e)
            axes[1].text(cx, cy - rad - 5, f'{side}',
                        color=color, fontsize=10, fontweight='bold', ha='center',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9,
                                 edgecolor=color, linewidth=1.5))

    axes[1].set_title(f'AX WATER T2 — ANNOTATED\nRed = RIGHT hydrocele  Blue = LEFT hydrocele', fontsize=11)
    axes[1].axis('off')

    plt.suptitle(f'F5 (AXIAL VIEW): Bilateral hydroceles — slice {best_z} (loc {locs_ax[best_z]:.1f} mm)',
                fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{ANN_DIR}/F5_bilateral_hydroceles_AX.png', dpi=110, bbox_inches='tight')
    plt.close()
    print(f"  → Saved: {ANN_DIR}/F5_bilateral_hydroceles_AX.png")

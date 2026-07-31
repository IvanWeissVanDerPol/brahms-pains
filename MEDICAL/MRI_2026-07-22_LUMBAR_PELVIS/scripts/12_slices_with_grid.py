"""Generate one slice at a time with row+col markers so I can identify landmarks."""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

VOL = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/volumes"
ANN = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/annotated"


def load_vol(key):
    z = np.load(f"{VOL}/{key}.npz")
    return z['vol'].astype(np.float32), z['slice_locs']


def normalize(arr):
    lo, hi = np.percentile(arr, [1, 99])
    return np.clip((arr.astype(np.float32) - lo) / (hi - lo), 0, 1)


def slice_with_grid(vol_n, z, loc, name, out_path, row_step=40, col_step=40):
    H, W = vol_n[z].shape
    fig, ax = plt.subplots(1, 1, figsize=(10, 12))
    ax.imshow(vol_n[z], cmap='gray', aspect='auto')
    for r in range(0, H, row_step):
        ax.axhline(r, color='cyan', linewidth=0.3, alpha=0.6)
        ax.text(2, r, str(r), color='cyan', fontsize=7, fontweight='bold')
    for c in range(0, W, col_step):
        ax.axvline(c, color='cyan', linewidth=0.3, alpha=0.6)
        ax.text(c, H - 5, str(c), color='cyan', fontsize=7, fontweight='bold',
                rotation=90, ha='right', va='top')
    ax.set_title(f'{name} z={z} loc={loc:.1f}mm  shape=({H},{W})', fontsize=12)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(out_path, dpi=80, bbox_inches='tight')
    plt.close()
    print(f"  Saved {out_path}")


# F3: Best SI joint slice z=30
cor_t1, locs_cor = load_vol('s13')
cor_t2, _ = load_vol('s14')
cor_t1_n = normalize(cor_t1)
cor_t2_n = normalize(cor_t2)

# Generate views of z=30 with grid markers (coronal T1 + WATER T2)
slice_with_grid(cor_t1_n, 30, locs_cor[30], 'COR T1', f'{ANN}/_F3_COR_T1_z30_GRID.png')
slice_with_grid(cor_t2_n, 30, locs_cor[30], 'COR WATER T2', f'{ANN}/_F3_COR_WATER_T2_z30_GRID.png')

# Also z=29 and z=31 for comparison
slice_with_grid(cor_t1_n, 29, locs_cor[29], 'COR T1', f'{ANN}/_F3_COR_T1_z29_GRID.png')
slice_with_grid(cor_t1_n, 31, locs_cor[31], 'COR T1', f'{ANN}/_F3_COR_T1_z31_GRID.png')

# F4: Axial STIR peak asymmetry slice
ax_stir, locs_ax = load_vol('s12')
ax_stir_n = normalize(ax_stir)
slice_with_grid(ax_stir_n, 19, locs_ax[19], 'AX STIR', f'{ANN}/_F4_AX_STIR_z19_GRID.png')

# F5: Sagittal mid slice (best for scrotum visibility)
sag_water, locs_sag_water = load_vol('s16')
sag_water_n = normalize(sag_water)
slice_with_grid(sag_water_n, 33, locs_sag_water[33], 'SAG WATER T2', f'{ANN}/_F5_SAG_WATER_z33_GRID.png')
slice_with_grid(sag_water_n, 34, locs_sag_water[34], 'SAG WATER T2', f'{ANN}/_F5_SAG_WATER_z34_GRID.png')

# F6: Axial L4-L5 level
ax_t2, locs_ax2 = load_vol('s6')
ax_t2_n = normalize(ax_t2)
for z in range(ax_t2.shape[0]):
    slice_with_grid(ax_t2_n, z, locs_ax2[z], 'AX T2', f'{ANN}/_F6_AX_T2_z{z}_GRID.png')

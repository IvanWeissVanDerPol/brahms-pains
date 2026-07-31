"""Generate debug contact sheets showing ALL slices of each series
so we can visually find the correct anatomical landmarks."""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ANN = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/annotated"
VOL = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/volumes"
os.makedirs(ANN, exist_ok=True)


def load_vol(key):
    z = np.load(f"{VOL}/{key}.npz")
    return z['vol'].astype(np.float32), z['slice_locs']


def normalize(arr):
    lo, hi = np.percentile(arr, [1, 99])
    return np.clip((arr.astype(np.float32) - lo) / (hi - lo), 0, 1)


def contact_sheet(vol, locs, name, cols=6):
    n = vol.shape[0]
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 3, rows * 2.8))
    axes = axes.flat if hasattr(axes, 'flat') else [axes]
    for i, ax in enumerate(axes):
        if i < n:
            ax.imshow(vol[i], cmap='gray', aspect='auto')
            ax.set_title(f'z={i} loc={locs[i]:.1f}', fontsize=8)
            ax.axis('off')
        else:
            ax.axis('off')
    plt.suptitle(f'ALL slices — {name}', fontsize=11)
    plt.tight_layout()
    out = f"{ANN}/_DEBUG_{name.replace(' ', '_').replace('/','_')}.png"
    plt.savefig(out, dpi=70, bbox_inches='tight')
    plt.close()
    return out


# Sagittal series (mid-slice is z=9)
sag_t2, locs = load_vol('s3')
contact_sheet(normalize(sag_t2), locs, 'sag_T2_mid')
print("done sag_T2")

sag_t1, _ = load_vol('s4')
contact_sheet(normalize(sag_t1), locs, 'sag_T1_mid')
print("done sag_T1")

sag_stir, _ = load_vol('s5')
contact_sheet(normalize(sag_stir), locs, 'sag_STIR_mid')
print("done sag_STIR")

# Coronal series (COR T1 + WATER T2)
cor_t1, locs_cor = load_vol('s13')
contact_sheet(normalize(cor_t1), locs_cor, 'cor_T1')
print("done cor_T1")

cor_t2, _ = load_vol('s14')
contact_sheet(normalize(cor_t2), locs_cor, 'cor_WATER_T2')
print("done cor_WATER_T2")

# Axial series
ax_t1, locs_ax = load_vol('s9')
contact_sheet(normalize(ax_t1), locs_ax, 'ax_T1')
print("done ax_T1")

ax_stir, locs_ax = load_vol('s12')
contact_sheet(normalize(ax_stir), locs_ax, 'ax_STIR')
print("done ax_STIR")

ax_water, locs_water = load_vol('s10')
contact_sheet(normalize(ax_water), locs_water, 'ax_WATER_T2')
print("done ax_WATER_T2")

ax_t2, locs_ax2 = load_vol('s6')
contact_sheet(normalize(ax_t2), locs_ax2, 'ax_T2_lumbar')
print("done ax_T2_lumbar")

# Sagittal water T2 (for scrotum — extends low)
sag_water, locs_sag_water = load_vol('s16')
contact_sheet(normalize(sag_water), locs_sag_water, 'sag_WATER_T2')
print("done sag_WATER_T2")

print("\n=== All contact sheets saved ===")
import glob
for f in sorted(glob.glob(f'{ANN}/_DEBUG_*')):
    sz = os.path.getsize(f)
    print(f"  {os.path.basename(f)}: {sz/1024:.0f} KB")

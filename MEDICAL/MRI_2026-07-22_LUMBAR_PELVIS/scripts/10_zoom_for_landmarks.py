"""Generate zoomed high-res views of single slices at landmarks for visual ID."""

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


# Get a large clear view of z=9 sag T2/T1/STIR side by side
sag_t2, _ = load_vol('s3')
sag_t1, _ = load_vol('s4')
sag_stir, _ = load_vol('s5')
sag_t2_n = normalize(sag_t2)
sag_t1_n = normalize(sag_t1)
sag_stir_n = normalize(sag_stir)

# z=9 full resolution side by side
fig, axes = plt.subplots(1, 3, figsize=(30, 10))
for ax, vol_n, name in [(axes[0], sag_t2_n, 'T2'),
                         (axes[1], sag_t1_n, 'T1'),
                         (axes[2], sag_stir_n, 'STIR')]:
    ax.imshow(vol_n[9], cmap='gray', aspect='equal')  # equal = no vertical squish
    ax.set_title(f'Sag {name} z=9 (loc=-30.8mm)', fontsize=14)
    ax.axis('off')

# Add row markers every 50px on T2 for reference
ax = axes[0]
H, W = sag_t2[9].shape
for r in range(0, H, 50):
    ax.axhline(r, color='cyan', linewidth=0.4, alpha=0.5)
    ax.text(5, r, str(r), color='cyan', fontsize=9, fontweight='bold')
ax.text(W-100, H/2, '← Image shape: '+str(sag_t2[9].shape), color='cyan', fontsize=10, rotation=90)
plt.suptitle('Sagittal mid-slice z=9 — FULL RESOLUTION with row markers (every 50px)', fontsize=14)
plt.tight_layout()
plt.savefig(f'{ANN}/_F1_SAG_MID_WITH_GRID.png', dpi=80, bbox_inches='tight')
plt.close()
print(f"Saved {f'{ANN}/_F1_SAG_MID_WITH_GRID.png'}")

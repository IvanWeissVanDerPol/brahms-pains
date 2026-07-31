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

cor_t1, locs_cor = load_vol('s13')
cor_t1_n = normalize(cor_t1)

# Show slices 25-45 with grid markers — wider row range
fig, axes = plt.subplots(7, 3, figsize=(15, 28))
for i, ax in enumerate(axes.flat):
    z_test = 25 + i
    if z_test < cor_t1.shape[0]:
        ax.imshow(cor_t1_n[z_test], cmap='gray', aspect='auto')
        H, W = cor_t1_n[z_test].shape
        for r in range(0, H, 60):
            ax.axhline(r, color='cyan', linewidth=0.3, alpha=0.4)
            ax.text(2, r, str(r), color='cyan', fontsize=7)
        ax.set_title(f'COR T1 z={z_test} loc={locs_cor[z_test]:.1f}', fontsize=9)
        ax.axis('off')
plt.suptitle('Coronal T1 slices z=25-44 with row markers (every 60 px)', fontsize=13)
plt.tight_layout()
plt.savefig(f'{ANN}/_F3_COR_T1_WIDE_GRID.png', dpi=80, bbox_inches='tight')
plt.close()
print(f"Saved {ANN}/_F3_COR_T1_WIDE_GRID.png")

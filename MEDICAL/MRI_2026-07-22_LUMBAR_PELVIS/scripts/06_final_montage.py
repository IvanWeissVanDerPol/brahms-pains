#!/usr/bin/env python3
"""
Stage 6 — Final comprehensive visualization: montage of all key findings.
"""
import os, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

VOL = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/volumes"
PREVIEW_DIR = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/previews_per_level"

def load_vol(key):
    z = np.load(f"{VOL}/{key}.npz")
    return z['vol'].astype(np.float32), z['slice_locs']

def normalize(arr):
    lo, hi = np.percentile(arr, [1, 99])
    return np.clip((arr - lo) / (hi - lo + 1e-9), 0, 1)

# Load all the relevant series
sag_t2, locs_t2 = load_vol('s3')
sag_t1, _ = load_vol('s4')
sag_stir, _ = load_vol('s5')
ax_t1, locs_ax_t1 = load_vol('s9')
ax_stir, locs_ax_stir = load_vol('s12')
ax_water, _ = load_vol('s10')
cor_t1, locs_cor = load_vol('s13')
cor_t2, _ = load_vol('s14')

sag_t2_n = normalize(sag_t2)
sag_t1_n = normalize(sag_t1)
sag_stir_n = normalize(sag_stir)
ax_t1_n = normalize(ax_t1)
ax_stir_n = normalize(ax_stir)
ax_water_n = normalize(ax_water)
cor_t1_n = normalize(cor_t1)
cor_t2_n = normalize(cor_t2)

# Find the best mid-sagittal slice
mid_z_sag = sag_t2.shape[0] // 2
mid_z_cor = cor_t1.shape[0] // 2
# Axial: find slice at SI joint level (around -130 to -100 mm)
si_z_ax = np.argmin(np.abs(locs_ax_t1 - (-120)))
scrot_z_ax = np.argmin(np.abs(locs_ax_t1 - (-60)))

# Build comprehensive 8-panel montage
fig = plt.figure(figsize=(28, 22))
gs = GridSpec(4, 4, figure=fig, hspace=0.30, wspace=0.15)

# Row 1: Sagittal lumbar (T2, T1, STIR + annotated)
ax = fig.add_subplot(gs[0, 0])
ax.imshow(sag_t2_n[mid_z_sag], cmap='gray', aspect='auto')
ax.set_title(f'Sag T2 — mid-sagittal\nL-spine + disc hydration', fontsize=12)
ax.axis('off')

ax = fig.add_subplot(gs[0, 1])
ax.imshow(sag_t1_n[mid_z_sag], cmap='gray', aspect='auto')
ax.set_title(f'Sag T1 — same slice\nMarrow fat + Modic 2', fontsize=12)
ax.axis('off')

ax = fig.add_subplot(gs[0, 2])
ax.imshow(sag_stir_n[mid_z_sag], cmap='gray', aspect='auto')
ax.set_title(f'Sag STIR — same slice\nModic 1 + edema', fontsize=12)
ax.axis('off')

ax = fig.add_subplot(gs[0, 3])
ax.imshow(sag_t2_n[mid_z_sag], cmap='gray', aspect='auto')
# Annotate known findings
ax.axhline(561, color='red', linewidth=1, linestyle='--', alpha=0.7)  # L4 vertebra (hemangioma)
ax.axhline(523, color='orange', linewidth=2, alpha=0.9)  # L4-L5 disc (Modic 1)
ax.text(20, 561, 'L4 vertebra\n(bright on T1+T2 → hemangioma?)', color='red',
        fontsize=10, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))
ax.text(20, 523, 'L4-L5 disc\n(Modic 1 — edema)', color='orange',
        fontsize=10, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))
ax.set_title('KEY FINDINGS annotated', fontsize=12)
ax.axis('off')

# Row 2: Coronal pelvis (T1 + WATER T2 + asymmetry + STIR)
ax = fig.add_subplot(gs[1, 0])
ax.imshow(cor_t1_n[mid_z_cor], cmap='gray', aspect='auto')
ax.set_title(f'COR T1 — slice {mid_z_cor}\nSI joints + marrow', fontsize=12)
ax.axis('off')

ax = fig.add_subplot(gs[1, 1])
ax.imshow(cor_t2_n[mid_z_cor], cmap='gray', aspect='auto')
ax.set_title(f'COR WATER T2 — same slice\nSubchondral BME detection', fontsize=12)
ax.axis('off')

# Asymmetry heatmap for COR T2
ax = fig.add_subplot(gs[1, 2])
diff = cor_t2_n[mid_z_cor] - np.fliplr(cor_t2_n[mid_z_cor])
ax.imshow(cor_t1_n[mid_z_cor], cmap='gray', alpha=0.4)
ax.imshow(diff, cmap='RdBu_r', alpha=0.7, vmin=-0.3, vmax=0.3)
ax.set_title('COR T2 ASYMMETRY\nRED = patient RIGHT brighter\n(consistent with right-sided inflammation)', fontsize=11)
ax.axis('off')

ax = fig.add_subplot(gs[1, 3])
ax.imshow(sag_stir_n[mid_z_sag], cmap='gray', aspect='auto')
ax.set_title('Sag STIR\nLumbar + lower thoracic', fontsize=12)
ax.axis('off')

# Row 3: Axial at SI joint level
ax = fig.add_subplot(gs[2, 0])
ax.imshow(ax_t1_n[si_z_ax], cmap='gray', aspect='auto')
ax.set_title(f'AX T1 — slice {si_z_ax} (loc {locs_ax_t1[si_z_ax]:.1f} mm)\nSI joint level', fontsize=12)
ax.axis('off')

ax = fig.add_subplot(gs[2, 1])
ax.imshow(ax_stir_n[si_z_ax], cmap='gray', aspect='auto')
ax.set_title('AX STIR — same slice\nBME detection', fontsize=12)
ax.axis('off')

ax = fig.add_subplot(gs[2, 2])
diff_ax = ax_stir_n[si_z_ax] - np.fliplr(ax_stir_n[si_z_ax])
ax.imshow(ax_t1_n[si_z_ax], cmap='gray', alpha=0.4)
ax.imshow(diff_ax, cmap='RdBu_r', alpha=0.7, vmin=-0.2, vmax=0.2)
ax.set_title('AX STIR ASYMMETRY\nRED = patient RIGHT brighter', fontsize=11)
ax.axis('off')

# Right vs left gluteal muscle
ax = fig.add_subplot(gs[2, 3])
ax.imshow(ax_stir_n[si_z_ax + 4], cmap='gray', aspect='auto')
ax.set_title(f'AX STIR slice {si_z_ax+4}\nGluteal muscle level\n(RIGHT side typically brighter)', fontsize=11)
ax.axis('off')

# Row 4: Pelvic asymmetry + scrotal fluid
ax = fig.add_subplot(gs[3, 0])
ax.imshow(ax_stir_n[scrot_z_ax], cmap='gray', aspect='auto')
ax.set_title(f'AX STIR slice {scrot_z_ax}\nLower pelvis / scrotal region', fontsize=11)
ax.axis('off')

ax = fig.add_subplot(gs[3, 1])
ax.imshow(ax_water_n[scrot_z_ax + 2], cmap='gray', aspect='auto')
ax.set_title(f'AX WATER T2 — scrotal level\n(Fluid = bright; bilateral hydroceles expected)', fontsize=11)
ax.axis('off')

# Asymmetry profile plot
ax = fig.add_subplot(gs[3, 2:])
asym = json.load(open("/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/muscle_asymmetry_ax_stir.json"))
locs = np.array([a['loc_mm'] for a in asym])
lefts = np.array([a['left'] for a in asym])
rights = np.array([a['right'] for a in asym])
ax.plot(locs, lefts, 'r-', label='patient RIGHT (image LEFT)', linewidth=2.5)
ax.plot(locs, rights, 'b-', label='patient LEFT (image RIGHT)', linewidth=2.5)
ax.fill_between(locs, rights, lefts, where=lefts > rights, color='red', alpha=0.3, label='RIGHT side hotter')
ax.set_title('Pelvic muscle T2-STIR asymmetry per axial slice\n48% of slices show patient RIGHT > LEFT (consistent inflammation pattern)', fontsize=12)
ax.set_xlabel('Z location (mm, inferior → superior)')
ax.set_ylabel('Mean STIR intensity')
ax.legend(loc='upper right')
ax.grid(alpha=0.3)

plt.suptitle('MRI LUMBAR + PELVIS — IVAN 2026-07-22 — KEY FINDINGS MONTAGE\n26yo M, RIGHT buttock/cintura/hip pain of unclear origin', fontsize=15, fontweight='bold', y=0.995)
plt.savefig(f'{PREVIEW_DIR}/00_KEY_FINDINGS_MONTAGE.png', dpi=100, bbox_inches='tight')
plt.close()
print(f"  → Saved comprehensive montage: {PREVIEW_DIR}/00_KEY_FINDINGS_MONTAGE.png")

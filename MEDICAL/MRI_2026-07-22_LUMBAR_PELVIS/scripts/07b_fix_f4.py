#!/usr/bin/env python3
"""
Stage 7b — Generate F4 hemipelvis asymmetry image at the correct peak slice.
"""
import os, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

VOL = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/volumes"
ANN_DIR = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/annotated"

def load_vol(key):
    z = np.load(f"{VOL}/{key}.npz")
    return z['vol'].astype(np.float32), z['slice_locs']

def normalize(arr):
    lo, hi = np.percentile(arr, [1, 99])
    return np.clip((arr.astype(np.float32) - lo) / (hi - lo), 0, 1)

ax_stir, locs_ax_stir = load_vol('s12')
ax_stir_n = normalize(ax_stir)

# Find the slice with the biggest absolute diff
asym_data = json.load(open("/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/muscle_asymmetry_ax_stir.json"))
# Sort by absolute diff and pick the top one
peak_idx = max(range(len(asym_data)), key=lambda i: abs(asym_data[i]['diff']))
peak_z = asym_data[peak_idx]['z']
peak_loc = asym_data[peak_idx]['loc_mm']
peak_diff = asym_data[peak_idx]['diff']
print(f"Peak asymmetry at z={peak_z}, loc={peak_loc:.1f} mm, diff={peak_diff:+.4f}")

# Use peak_z and 2 adjacent for context
for z_off in [-1, 0, 1]:
    z = peak_z + z_off
    if z < 0 or z >= ax_stir.shape[0]:
        continue
    sl = ax_stir_n[z]
    loc = locs_ax_stir[z]
    is_peak = (z == peak_z)

    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    axes[0].imshow(sl, cmap='gray', aspect='auto')
    axes[0].set_title(f'AX STIR — slice {z} (loc {loc:.1f} mm)\nOriginal',
                     fontsize=12, fontweight='bold' if is_peak else 'normal')
    axes[0].axis('off')

    axes[1].imshow(sl, cmap='gray', aspect='auto')
    midcol = sl.shape[1] // 2
    # Midline
    axes[1].axvline(midcol, color='yellow', linewidth=2, linestyle='--', alpha=0.8)
    # Right side (image LEFT = patient RIGHT)
    rect_r = Rectangle((20, 80), midcol - 30, sl.shape[0] - 160,
                      edgecolor='red', facecolor='none', linewidth=3.5)
    axes[1].add_patch(rect_r)
    # Left side for comparison
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
    # Asymmetry value
    if z < len(asym_data):
        a = asym_data[z]
        axes[1].text(midcol, sl.shape[0] - 60,
                    f'R L={a["left"]:.3f}  L R={a["right"]:.3f}  diff={a["diff"]:+.4f}',
                    color='red', fontsize=10, fontweight='bold', ha='center',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.95,
                             edgecolor='red', linewidth=1.5))
    axes[1].set_title(f'AX STIR — ANNOTATED\nRed box = patient RIGHT side (brighter = edema)',
                    fontsize=11, fontweight='bold' if is_peak else 'normal')
    axes[1].axis('off')

    plt.suptitle(f'F4: DIFFUSE RIGHT HEMIPELVIS T2 HYPERINTENSITY\nz={z}, loc={loc:.1f}mm, asymmetry={peak_diff:+.4f} ({"PEAK" if is_peak else "context"})',
                fontsize=13, fontweight='bold')
    plt.tight_layout()
    out = f'{ANN_DIR}/F4_hemipelvis_asymmetry_z{z}.png'
    plt.savefig(out, dpi=110, bbox_inches='tight')
    plt.close()
    print(f"  → Saved: {out}")

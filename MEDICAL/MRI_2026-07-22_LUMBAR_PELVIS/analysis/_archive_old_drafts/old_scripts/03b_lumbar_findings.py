#!/usr/bin/env python3
"""
Stage 3b — Sagittal Pfirrmann grading per disc level.

Strategy:
1. Pick mid-sagittal slice (median column) of Sag T2 series.
2. Compute the vertical midline intensity profile.
3. Identify vertebra bodies (T2-dark) and discs (T2-bright) by peak finding.
4. For each disc, compute Pfirrmann proxy:
   - Normalized signal of nucleus center
   - Height-to-vertebra ratio
   - Homogeneity
5. For each vertebra, scan for hyperintense T2 lesion (hemangioma) or
   hyperintense STIR (Modic 1) or hyperintense T1+dark T2 (Modic 2).
6. Output a per-level report.
"""
import os, json
import numpy as np
from scipy import ndimage, signal
from skimage import exposure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

VOL = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/volumes"
ANALYSIS = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis"
PREVIEW_DIR = f"{ANALYSIS}/previews_per_level"
os.makedirs(PREVIEW_DIR, exist_ok=True)


def load_vol(key):
    z = np.load(f"{VOL}/{key}.npz")
    return z['vol'].astype(np.float32), z['slice_locs']


# Load all 3 sagittal series
sag_t2, locs_t2 = load_vol('s3')
sag_t1, locs_t1 = load_vol('s4')
sag_stir, locs_stir = load_vol('s5')

# Use the middle sagittal slice (index 9 of 19)
mid_z = sag_t2.shape[0] // 2
print(f"Mid-sagittal slice index: {mid_z}, location: {locs_t2[mid_z]:.2f} mm")

# Crop to the central column strip (40px wide)
mid_col = sag_t2.shape[2] // 2
half_w = 20
t2_strip = sag_t2[mid_z, :, mid_col-half_w:mid_col+half_w].mean(axis=1)
t1_strip = sag_t1[mid_z, :, mid_col-half_w:mid_col+half_w].mean(axis=1)
stir_strip = sag_stir[mid_z, :, mid_col-half_w:mid_col+half_w].mean(axis=1)

# Smooth the midline profile
from scipy.ndimage import gaussian_filter1d
t2_smooth = gaussian_filter1d(t2_strip, sigma=4)
t1_smooth = gaussian_filter1d(t1_strip, sigma=4)
stir_smooth = gaussian_filter1d(stir_strip, sigma=4)

# Find peaks (discs = bright on T2) and valleys (vertebrae = dark on T2)
t2_min, t2_max = t2_smooth.min(), t2_smooth.max()
t2_norm = (t2_smooth - t2_min) / (t2_max - t2_min)

# Find local minima (vertebrae centers) — these are LOW intensity on T2
valleys, _ = signal.find_peaks(-t2_norm, distance=30, prominence=0.05)
# Find local maxima (disc centers) — these are HIGH intensity on T2
peaks, _ = signal.find_peaks(t2_norm, distance=20, prominence=0.05)

print(f"Detected {len(valleys)} vertebra valleys: rows {valleys.tolist()}")
print(f"Detected {len(peaks)} disc peaks: rows {peaks.tolist()}")

# Sort and pair: between each pair of vertebrae there should be one disc
# Vertebrae from inferior to superior (top of image = anterior; rows 0 = top).
# In lumbar MRIs, the top of the image is anterior and inferior of the patient
# (because patient lies supine). We expect L5 at the bottom of the image, L1 at the top.

# But we don't know the orientation for sure — let's order vertebra valleys by row
# and assume the lower-row one is L1 (superior = anterior = top of image).
valleys_sorted = sorted(valleys.tolist())

# Identify 5 lumbar vertebrae (L1-L5) + S1 should be visible
# The first (most superior) vertebra visible could be T12-L1; we focus on L1-L5 + S1.
# 5 lumbar discs: L1-L2, L2-L3, L3-L4, L4-L5, L5-S1

# Discs should sit BETWEEN vertebrae. Find peak between each consecutive valley.
n_vertebrae = len(valleys_sorted)
disc_rows = []
disc_assignments = []
for i in range(n_vertebrae - 1):
    v1, v2 = valleys_sorted[i], valleys_sorted[i+1]
    # Find peak between v1 and v2
    region = t2_norm[v1:v2+1]
    if len(region) < 3:
        continue
    local_peak = np.argmax(region) + v1
    disc_rows.append(local_peak)
    # Assign level: vertebra i is (n-1-i) from bottom (in top-down sagittal, last is L5)
    # But more accurately: top valley is L1 (or T12), bottom valley is S1.
    level_labels = ['L1-L2', 'L2-L3', 'L3-L4', 'L4-L5', 'L5-S1']
    disc_assignments.append(level_labels[i] if i < 5 else f'disc-{i}')

print(f"\nDisc peaks (rows): {disc_rows}")
print(f"Disc levels: {disc_assignments}")
print(f"Vertebra valleys (rows): {valleys_sorted}")

# Save annotated midline plot
fig, axes = plt.subplots(3, 1, figsize=(14, 18))
axes[0].plot(t2_norm, label='T2', color='blue')
for v in valleys_sorted:
    axes[0].axvline(v, color='red', alpha=0.4, linewidth=0.8, linestyle='--')
for i, p in enumerate(disc_rows):
    axes[0].axvline(p, color='green', alpha=0.7, linewidth=1.2)
    axes[0].text(p, 1.05, disc_assignments[i], color='green', rotation=90, fontsize=10, ha='right')
axes[0].set_title('Sag T2 midline — vertebrae (red dashed) + discs (green)', fontsize=14)
axes[0].set_xlabel('Row (z = superior → inferior along the spine)')
axes[0].legend()
axes[0].grid(alpha=0.3)

axes[1].plot((t1_smooth - t1_smooth.min()) / (t1_smooth.max() - t1_smooth.min()), label='T1', color='red')
axes[1].set_title('Sag T1 midline (same slice) — fatty marrow = bright', fontsize=14)
axes[1].legend()
axes[1].grid(alpha=0.3)

axes[2].plot((stir_smooth - stir_smooth.min()) / (stir_smooth.max() - stir_smooth.min()), label='STIR', color='orange')
axes[2].set_title('Sag STIR midline — edema = bright', fontsize=14)
axes[2].legend()
axes[2].grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f'{PREVIEW_DIR}/sagittal_midline_3sequences.png', dpi=120, bbox_inches='tight')
plt.close()
print(f"\n  → Saved midline 3-sequence plot: {PREVIEW_DIR}/sagittal_midline_3sequences.png")

# Now compute per-disc metrics: T2 brightness, T1 brightness, STIR brightness
# and infer Pfirrmann + Modic + hemangioma candidates.

def normalize(arr):
    lo, hi = np.percentile(arr, [1, 99])
    return np.clip((arr - lo) / (hi - lo), 0, 1) if hi > lo else arr


sag_t2_n = normalize(sag_t2)
sag_t1_n = normalize(sag_t1)
sag_stir_n = normalize(sag_stir)

findings_per_disc = []
for i, (prow, level) in enumerate(zip(disc_rows, disc_assignments)):
    # Sample a 11x11 region around the disc center on mid slice
    r = int(prow)
    cstart = mid_col - half_w
    cend = mid_col + half_w
    region_t2 = sag_t2_n[mid_z, max(0,r-5):r+6, cstart:cend]
    region_t1 = sag_t1_n[mid_z, max(0,r-5):r+6, cstart:cend]
    region_stir = sag_stir_n[mid_z, max(0,r-5):r+6, cstart:cend]
    if region_t2.size == 0:
        continue

    # Disc height proxy: bright band height on T2 midline
    band_thresh = 0.6
    is_bright = t2_norm > band_thresh
    band_rows = np.where(np.convolve(is_bright.astype(int), np.ones(5), mode='same') > 2)[0]
    band_in_range = band_rows[(band_rows >= valleys_sorted[max(0,i)] - 5) &
                               (band_rows <= valleys_sorted[min(i+1, len(valleys_sorted)-1)] + 5)] if i+1 < len(valleys_sorted) else []
    band_height = len(band_in_range)

    findings_per_disc.append({
        'level': level,
        'row_center': int(prow),
        'band_height_px': band_height,
        'mean_t2': float(region_t2.mean()),
        'mean_t1': float(region_t1.mean()),
        'mean_stir': float(region_stir.mean()),
        'max_t2': float(region_t2.max()),
        'max_t1': float(region_t1.max()),
        'max_stir': float(region_stir.max()),
    })

print(f"\n=== Per-disc measurements (mid-sagittal slice {mid_z}) ===")
print(f"{'Level':<8} {'T2':<6} {'T1':<6} {'STIR':<6} {'band_h':<6} {'T2_max':<6} {'STIR_max':<6}")
for f in findings_per_disc:
    print(f"  {f['level']:<8} {f['mean_t2']:.3f}  {f['mean_t1']:.3f}  {f['mean_stir']:.3f}  {f['band_height_px']:>4}    {f['max_t2']:.3f}  {f['max_stir']:.3f}")

# Save JSON
with open(f"{ANALYSIS}/sagittal_disc_findings.json", 'w') as f:
    json.dump(findings_per_disc, f, indent=2)
print(f"\n  → Saved: {ANALYSIS}/sagittal_disc_findings.json")

# Now scan each vertebra for focal bright/hot lesions (hemangioma candidates)
# A vertebral hemangioma is bright on BOTH T1 and T2 (fatty + vascular).
# Modic 1 = dark on T1, bright on T2 and STIR (edema).
# Modic 2 = bright on T1, iso/dark on T2 (fatty replacement).

print("\n=== Vertebral lesion scan ===")
valley_findings = []
for i, vrow in enumerate(valleys_sorted):
    # Sample a wider region of the vertebra (40 px tall × whole central 200 px wide)
    rstart = max(0, int(vrow) - 25)
    rend = min(sag_t2_n.shape[1], int(vrow) + 25)
    cstart = mid_col - 100
    cend = mid_col + 100
    region_t2 = sag_t2_n[mid_z, rstart:rend, cstart:cend]
    region_t1 = sag_t1_n[mid_z, rstart:rend, cstart:cend]
    region_stir = sag_stir_n[mid_z, rstart:rend, cstart:cend]
    if region_t2.size < 100:
        continue
    # Vertebra mean and max
    valley_findings.append({
        'vertebra_index': i,
        'row_center': int(vrow),
        'mean_t2': float(region_t2.mean()),
        'mean_t1': float(region_t1.mean()),
        'mean_stir': float(region_stir.mean()),
        'max_t2': float(region_t2.max()),
        'max_t1': float(region_t1.max()),
        'max_stir': float(region_stir.max()),
        'p99_t2': float(np.percentile(region_t2, 99)),
        'p99_t1': float(np.percentile(region_t1, 99)),
        'p99_stir': float(np.percentile(region_stir, 99)),
    })
    flag = []
    if valley_findings[-1]['p99_t2'] > 0.85 and valley_findings[-1]['p99_t1'] > 0.85:
        flag.append('HEMANGIOMA_CANDIDATE (T1+T2 bright)')
    if valley_findings[-1]['p99_stir'] > 0.85 and valley_findings[-1]['p99_t1'] < 0.5:
        flag.append('MODIC_1_CANDIDATE (T2 bright + T1 dark + STIR bright = edema)')
    if valley_findings[-1]['p99_t1'] > 0.85 and valley_findings[-1]['p99_t2'] < 0.7:
        flag.append('MODIC_2_CANDIDATE (T1 bright + T2 iso/dark = fatty)')
    valley_findings[-1]['flags'] = flag
    if flag:
        print(f"  vertebra idx {i} (row {vrow}): FLAGS — {flag}")
    else:
        print(f"  vertebra idx {i} (row {vrow}): T2_max={valley_findings[-1]['p99_t2']:.3f}, T1_max={valley_findings[-1]['p99_t1']:.3f}, STIR_max={valley_findings[-1]['p99_stir']:.3f}")

with open(f"{ANALYSIS}/sagittal_vertebra_findings.json", 'w') as f:
    json.dump(valley_findings, f, indent=2)
print(f"\n  → Saved: {ANALYSIS}/sagittal_vertebra_findings.json")

# Save annotated mid-slice showing the detected bands
fig, ax = plt.subplots(figsize=(14, 18))
ax.imshow(sag_t2_n[mid_z], cmap='gray', aspect='auto')
for v in valleys_sorted:
    ax.axhline(v, color='red', alpha=0.5, linewidth=1, linestyle='--')
for i, p in enumerate(disc_rows):
    ax.axhline(p, color='lime', alpha=0.8, linewidth=1.5)
    ax.text(sag_t2_n.shape[1] - 100, p, disc_assignments[i], color='lime',
            fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.6))
ax.set_title(f'Sag T2 mid-slice — auto-detected lumbar vertebrae (red) + discs (green)\nIvW 2026-07-22 lumbar MRI', fontsize=14)
ax.axis('off')
plt.tight_layout()
plt.savefig(f'{PREVIEW_DIR}/sagittal_t2_mid_annotated.png', dpi=120, bbox_inches='tight')
plt.close()
print(f"  → Saved annotated: {PREVIEW_DIR}/sagittal_t2_mid_annotated.png")

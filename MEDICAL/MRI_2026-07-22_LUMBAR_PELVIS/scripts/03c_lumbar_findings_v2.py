#!/usr/bin/env python3
"""
Stage 3c — Sagittal Pfirrmann + Modic + hemangioma — REVISED.

Fix: detect vertebra VALLEYS by widening the threshold (vertebrae are MUCH darker
than disc + CSF combined). Then narrow valleys to 6 (L1-S1). Disc peaks
are between every consecutive pair.
"""
import os, json
import numpy as np
from scipy import ndimage, signal
from scipy.ndimage import gaussian_filter1d
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


sag_t2, _ = load_vol('s3')
sag_t1, _ = load_vol('s4')
sag_stir, _ = load_vol('s5')

mid_z = sag_t2.shape[0] // 2
mid_col = sag_t2.shape[2] // 2

# Use the FULL central vertical strip but constrained to anterior column (NOT spinal canal)
# Spinal canal is posterior (~70% of width). Vertebrae bodies are in the anterior 35% column.
# Use cols [mid-150, mid-30] = anterior vertebral body column.
strip_start = max(0, mid_col - 150)
strip_end = mid_col - 30
half_w = strip_end - strip_start

# Mean across anterior vertebral body strip (excludes spinal canal)
t2_vb = sag_t2[mid_z, :, strip_start:strip_end].mean(axis=1)
t1_vb = sag_t1[mid_z, :, strip_start:strip_end].mean(axis=1)
stir_vb = sag_stir[mid_z, :, strip_start:strip_end].mean(axis=1)

# Normalize
def n01(a):
    lo, hi = np.percentile(a, [5, 95])
    return np.clip((a - lo) / (hi - lo + 1e-9), 0, 1)

t2_vb_n = n01(t2_vb)
t1_vb_n = n01(t1_vb)
stir_vb_n = n01(stir_vb)

# Smooth
t2_sm = gaussian_filter1d(t2_vb_n, sigma=6)
t1_sm = gaussian_filter1d(t1_vb_n, sigma=6)
stir_sm = gaussian_filter1d(stir_vb_n, sigma=6)

# Find vertebra CENTERS as local minima of T2 (vertebrae are dark)
# In the vertebral body strip, vertebrae are dark, discs are bright.
# But the ENDPLATES also show signal change, so we use wide distance and high prominence.
valleys, props = signal.find_peaks(-t2_sm, distance=80, prominence=0.15)

# Find disc CENTERS as local maxima of T2 BETWEEN vertebrae
peaks, _ = signal.find_peaks(t2_sm, distance=20, prominence=0.10)

print(f"Vertebra valleys detected (rows): {sorted(valleys.tolist())}")
print(f"Disc peaks detected (rows): {sorted(peaks.tolist())}")

# Identify the 5 lumbar + 1 sacral vertebra (L1, L2, L3, L4, L5, S1) — should be 6.
# In a top-down sagittal MR image (top of image = anterior of patient in supine position),
# the top of the lumbar spine is at the top of the image.
# For a 26-year-old male, the visible lumbar segment in a lumbar MRI typically shows
# L1-L5 + S1. Sometimes the lower thoracic (T11-T12) is visible.

# Strategy: take the 6 vertebra valleys with the highest prominence (most clearly vertebral)
# If we found more than 6, take the 6 most prominent.
if len(valleys) > 6:
    prom = props['prominences']
    sorted_idx = np.argsort(prom)[::-1]
    valleys = valleys[sorted_idx[:6]]
    valleys = sorted(valleys.tolist())
print(f"After selection, vertebra rows: {valleys}")

# Sort peaks (disc centers)
peaks = sorted(peaks.tolist())

# For each consecutive pair of vertebrae, find the disc peak in between
disc_rows = []
disc_levels = []
labels = ['L1-L2', 'L2-L3', 'L3-L4', 'L4-L5', 'L5-S1']
for i in range(len(valleys) - 1):
    v1, v2 = valleys[i], valleys[i+1]
    # Peak between
    region = t2_sm[v1:v2+1]
    if len(region) < 3:
        continue
    local_peak = np.argmax(region) + v1
    # Also measure the band's height: consecutive rows where T2 > 0.5 within ±15 rows
    disc_rows.append(local_peak)
    disc_levels.append(labels[i] if i < 5 else f'extra-disc-{i}')

# Also measure disc height (number of consecutive bright rows around the peak)
disc_height_px = []
for prow in disc_rows:
    band = t2_sm[max(0, prow-20):prow+21]
    bright = (band > np.percentile(t2_sm, 70)).sum()
    disc_height_px.append(int(bright))

print(f"\nDisc rows: {disc_rows}")
print(f"Disc heights (px, bright rows): {disc_height_px}")
print(f"Levels: {disc_levels}")

# Compute per-disc measurements (T2/T1/STIR mean + nucleus-vs-annulus differential)
def normalize_3d(arr):
    lo, hi = np.percentile(arr, [1, 99])
    return np.clip((arr.astype(np.float32) - lo) / (hi - lo + 1e-9), 0, 1)

sag_t2_n = normalize_3d(sag_t2)
sag_t1_n = normalize_3d(sag_t1)
sag_stir_n = normalize_3d(sag_stir)

disc_findings = []
for i, (prow, level, h) in enumerate(zip(disc_rows, disc_levels, disc_height_px)):
    # Sample a 16x20 region around disc center, on the mid slice
    rstart = max(0, prow - 8)
    rend = min(sag_t2_n.shape[1], prow + 9)
    cstart = strip_start
    cend = strip_end
    # Mid-nucleus (3x3 center) for bright CSF-like nucleus detection
    nucleus_r = slice(max(0, prow - 1), prow + 2)
    nucleus_c = slice(strip_start + half_w//2 - 1, strip_start + half_w//2 + 2)
    # Annulus (peripheral of disc, just below the endplate above)
    annulus_r = slice(max(0, prow - 7), prow - 3)
    annulus_c = slice(strip_start + 3, strip_end - 3)

    n_t2 = sag_t2_n[mid_z, nucleus_r, nucleus_c].mean()
    n_t1 = sag_t1_n[mid_z, nucleus_r, nucleus_c].mean()
    n_stir = sag_stir_n[mid_z, nucleus_r, nucleus_c].mean()
    a_t2 = sag_t2_n[mid_z, annulus_r, annulus_c].mean()
    a_t1 = sag_t1_n[mid_z, annulus_r, annulus_c].mean()
    a_stir = sag_stir_n[mid_z, annulus_r, annulus_c].mean()

    # CSF reference: mean of the spinal canal at this slice
    csf_t2 = sag_t2_n[mid_z, prow-5:prow+6, mid_col-30:mid_col+30].mean()

    # Pfirrmann proxy (I-V)
    # I: nucleus signal = CSF (homogeneous bright)
    # II: nucleus brighter than annulus, possibly inhomogeneous
    # III: nucleus gray, similar to annulus
    # IV: nucleus dark gray, heterogeneous
    # V: nucleus black (collapsed disc)
    p_proxy = float(n_t2 / max(csf_t2, 0.05))
    if p_proxy > 0.85: pf = 'I-II (bright, well-hydrated)'
    elif p_proxy > 0.6: pf = 'III (intermediate, mild desiccation)'
    elif p_proxy > 0.4: pf = 'IV (dark gray, advanced desiccation)'
    else: pf = 'V (black, collapsed disc)'

    # Modic candidate
    # Modic 1: T1 dark + T2 bright + STIR bright (edema/inflammation)
    # Modic 2: T1 bright + T2 iso + STIR dark (fatty replacement)
    # Modic 3: T1 dark + T2 dark (subchondral sclerosis)

    modic = None
    if n_stir > 0.7 and n_t1 < 0.4:
        modic = 'Modic 1 candidate (edema)'
    elif n_t1 > 0.7 and n_stir < 0.4 and n_t2 < 0.7:
        modic = 'Modic 2 candidate (fatty)'

    disc_findings.append({
        'level': level,
        'row_center': int(prow),
        'height_px': h,
        'csf_t2_ref': float(csf_t2),
        'nucleus': {'t2': float(n_t2), 't1': float(n_t1), 'stir': float(n_stir)},
        'annulus': {'t2': float(a_t2), 't1': float(a_t1), 'stir': float(a_stir)},
        'nucleus_to_csf_ratio': p_proxy,
        'pfirrmann_proxy': pf,
        'modic_candidate': modic,
    })

print("\n=== Per-disc PFIRRMANN + MODIC (mid-sagittal) ===")
for f in disc_findings:
    print(f"  {f['level']:<8}  N/C ratio={f['nucleus_to_csf_ratio']:.3f}  T2_n={f['nucleus']['t2']:.3f}  T1_n={f['nucleus']['t1']:.3f}  STIR_n={f['nucleus']['stir']:.3f}")
    print(f"    → {f['pfirrmann_proxy']}    Modic: {f['modic_candidate'] or 'none'}")

with open(f"{ANALYSIS}/sagittal_disc_findings_v2.json", 'w') as f:
    json.dump(disc_findings, f, indent=2)
print(f"\n  → Saved: {ANALYSIS}/sagittal_disc_findings_v2.json")

# Per-vertebra hemangioma detection (scan whole vertebral body region)
print("\n=== Per-vertebra HEMANGIOMA / marrow lesion scan ===")
vertebra_labels = ['L1', 'L2', 'L3', 'L4', 'L5', 'S1']
vertebra_findings = []
for i, vrow in enumerate(valleys):
    # Use a 40x80 region centered on vertebra body
    rstart = max(0, vrow - 30)
    rend = min(sag_t2_n.shape[1], vrow + 31)
    # Skip the spinal canal area (posterior 30% of the width)
    body_cstart = strip_start
    body_cend = strip_start + (strip_end - strip_start) * 7 // 10  # anterior 70% of body
    region_t2 = sag_t2_n[mid_z, rstart:rend, body_cstart:body_cend]
    region_t1 = sag_t1_n[mid_z, rstart:rend, body_cstart:body_cend]
    region_stir = sag_stir_n[mid_z, rstart:rend, body_cstart:body_cend]
    if region_t2.size < 100:
        continue

    # Hemangioma: focal round very-bright on T1 AND T2, mildly bright on STIR
    # We look for hotspots (top 0.5% pixels) where both T1 and T2 are > 0.92 AND location matches
    t2_top = np.percentile(region_t2, 99.5)
    t1_top = np.percentile(region_t1, 99.5)
    stir_top = np.percentile(region_stir, 99.5)
    # Find pixels bright on both T1 and T2
    both = (region_t2 > 0.90) & (region_t1 > 0.90)
    both_count = int(both.sum())
    both_pct = float(both.mean())
    # Find if there's a focal cluster
    labeled, n_clusters = ndimage.label(both)
    cluster_sizes = ndimage.sum(both, labeled, range(1, n_clusters + 1)) if n_clusters > 0 else []
    big_cluster = max(cluster_sizes) if cluster_sizes else 0

    hemangioma = (both_pct > 0.005) and (big_cluster > 8)
    label = vertebra_labels[i] if i < len(vertebra_labels) else f'V{i+1}'

    vf = {
        'vertebra': label,
        'row_center': int(vrow),
        't2_p99': float(t2_top),
        't1_p99': float(t1_top),
        'stir_p99': float(stir_top),
        't1_t2_both_bright_pct': both_pct,
        'biggest_bright_cluster_px': int(big_cluster),
        'hemangioma_candidate': hemangioma,
        't2_p1': float(np.percentile(region_t2, 1)),
        't1_p1': float(np.percentile(region_t1, 1)),
        'stir_p1': float(np.percentile(region_stir, 1)),
        't2_mean': float(region_t2.mean()),
        't1_mean': float(region_t1.mean()),
        'stir_mean': float(region_stir.mean()),
    }
    vertebra_findings.append(vf)
    flag = '🔴 HEMANGIOMA CANDIDATE' if hemangioma else ''
    print(f"  {label:<4} (row {vrow}): T2_p99={t2_top:.3f} T1_p99={t1_top:.3f} STIR_p99={stir_top:.3f}  both_bright={both_pct*100:.2f}%  big_cluster={int(big_cluster)}px {flag}")

with open(f"{ANALYSIS}/sagittal_vertebra_findings_v2.json", 'w') as f:
    json.dump(vertebra_findings, f, indent=2)
print(f"\n  → Saved: {ANALYSIS}/sagittal_vertebra_findings_v2.json")

# Annotated mid-slice with CORRECTED labels
fig, ax = plt.subplots(figsize=(14, 18))
ax.imshow(sag_t2_n[mid_z], cmap='gray', aspect='auto')
for v in valleys:
    ax.axhline(v, color='red', alpha=0.5, linewidth=1.2, linestyle='--')
for i, (p, level, label) in enumerate(zip(disc_rows, disc_levels, vertebra_labels[:-1])):
    ax.axhline(p, color='lime', alpha=0.9, linewidth=2)
    ax.text(sag_t2_n.shape[1] - 150, p, f'DISC {level}', color='lime',
            fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))
for i, v in enumerate(valleys):
    label = vertebra_labels[i] if i < len(vertebra_labels) else f'V{i+1}'
    ax.text(20, v, f'{label}', color='red',
            fontsize=13, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))
ax.set_title(f'Sag T2 mid-slice — corrected segmentation\nLumbar vertebrae (red) + discs (green), 26yo M', fontsize=14)
ax.axis('off')
plt.tight_layout()
plt.savefig(f'{PREVIEW_DIR}/sagittal_t2_mid_corrected.png', dpi=120, bbox_inches='tight')
plt.close()
print(f"\n  → Annotated: {PREVIEW_DIR}/sagittal_t2_mid_corrected.png")

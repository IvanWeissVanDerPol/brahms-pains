#!/usr/bin/env python3
"""
Stage 4 — SI JOINT ANALYSIS (bilateral) + axial disc analysis + pelvic soft tissue.

Patient has RIGHT-sided buttock / cintura / hip pain → focus on RIGHT SI joint.

Series used:
- 13 (COR T1 FSE)         — fat metaplasia, erosions, sclerosis
- 14 (WATER COR T2 FSE)   — fluid-sensitive, edema detection
- 12 (Ax FSE STIR)        — bone marrow edema (axial view)
- 1000 (FAT Ax Dixon)     — fat fraction
- 1001 (InPhase Ax Dixon) — companion

ASAS criteria for sacroiliitis on MRI:
- Bone marrow edema (BME): bright on STIR/T2FS, subchondral, present on at least 2 consecutive slices
- Capsulitis / enthesitis: bright on STIR at joint capsule / ligament insertion
- Erosions: cortical defects with low signal on T1
- Sclerosis: low signal on T1 and T2 (subchondral)
- Fat metaplasia: bright on T1 (subchondral)
- Ankylosis: bony bridge across joint (bright on both T1 and T2)

SPARCC scoring (Spondyloarthritis Research Consortium of Canada):
- 6 consecutive coronal slices through the cartilaginous portion of the joint
- Each SI joint divided into 4 quadrants per slice
- 1 point per quadrant with BME
- +1 per slice if an "intense" signal (compared to vessels) is seen
- +1 per slice if BME is "deep" (>1 cm from articular surface)
- Maximum 12 per SI joint per slice; 72 total
"""
import os, json
import numpy as np
from scipy import ndimage
from scipy.ndimage import gaussian_filter
from skimage import exposure, morphology, filters, measure
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


def normalize(arr):
    lo, hi = np.percentile(arr, [1, 99])
    return np.clip((arr - lo) / (hi - lo + 1e-9), 0, 1)


cor_t1, locs_cor_t1 = load_vol('s13')
cor_t2, locs_cor_t2 = load_vol('s14')
ax_t1, locs_ax_t1 = load_vol('s9')
ax_stir, locs_ax_stir = load_vol('s12')
ax_t2_water, _ = load_vol('s10')

# Normalize
cor_t1_n = normalize(cor_t1)
cor_t2_n = normalize(cor_t2)
ax_t1_n = normalize(ax_t1)
ax_stir_n = normalize(ax_stir)
ax_t2_n = normalize(ax_t2_water)

print("="*70)
print("[B] SI JOINT ANALYSIS — bilateral, with RIGHT-side focus")
print("="*70)
print(f"COR T1: {cor_t1.shape}, locs [{locs_cor_t1[0]:.1f} .. {locs_cor_t1[-1]:.1f}] mm")
print(f"COR WATER T2: {cor_t2.shape}, locs [{locs_cor_t2[0]:.1f} .. {locs_cor_t2[-1]:.1f}] mm")
print(f"AX T1: {ax_t1.shape}, locs [{locs_ax_t1[0]:.1f} .. {locs_ax_t1[-1]:.1f}] mm")
print(f"AX STIR: {ax_stir.shape}, locs [{locs_ax_stir[0]:.1f} .. {locs_ax_stir[-1]:.1f}] mm")

# The SI joints are visible on both coronal and axial series.
# In axial view: SI joints are visible bilaterally at the level of S1.
# We need to find the slice(s) showing the cartilaginous portion of the joint.

# Strategy:
# 1. Use the AX T1 series to find the center of the sacrum (medial axis).
# 2. Find the SI joints as the dark bands between iliac bone and sacrum on each side.
# 3. Measure the SUBCHONDRAL bone on each side of each joint for STIR/T2 brightness
#    (BME = bone marrow edema) and T1 brightness (fat metaplasia).
# 4. Detect erosions as cortical breaks (low-signal bands at the joint margin).

# For axial SI joint analysis, find slices through the cartilaginous SI joint.
# SI joint extends from S1 (superior) to S3 (inferior). In our axial series with
# loc range [-272, +8] mm, the SI joint is in the mid-pelvis.
# Find slices where both iliac bones are visible and the sacrum is between them.

# A simpler approach: compute the axial center-of-mass of bright pixels and look
# at the region around the joint.

# First, identify the slices where the SI joints appear.
# SI joints appear as two vertical low-signal lines flanking the sacrum in axial view.
# Use the AX T1 series.

# Compute per-slice lateral edges of sacrum vs iliac bones.
# We'll do this by finding the column with max gradient on each slice.

print("\n=== Slice-by-slice SI joint detection on AX T1 ===")
print("Scanning axial slices for SI joint appearance...")

si_slices_info = []
for z in range(ax_t1.shape[0]):
    sl = ax_t1[z]
    # Find the column with the max gradient (high contrast = SI joint margin)
    # Use central horizontal band
    band = sl[ax_t1.shape[1]//4:ax_t1.shape[1]*3//4, :]
    grad_x = np.abs(np.diff(band.astype(np.float32), axis=1))
    col_max_grad = grad_x.mean(axis=0)
    # Find left + right SI joint columns as the two highest gradient columns
    sorted_cols = np.argsort(col_max_grad)[::-1]
    # Filter: must be reasonably symmetric around midline
    midcol = ax_t1.shape[2] // 2
    left_col_candidates = [c for c in sorted_cols if c < midcol - 50]
    right_col_candidates = [c for c in sorted_cols if c > midcol + 50]
    if left_col_candidates and right_col_candidates:
        left_col = left_col_candidates[0]
        right_col = right_col_candidates[0]
        sym_score = abs((midcol - left_col) - (right_col - midcol))
        if sym_score < 30 and col_max_grad[left_col] > 5 and col_max_grad[right_col] > 5:
            si_slices_info.append({
                'z': z,
                'loc_mm': float(locs_ax_t1[z]),
                'left_col': int(left_col),
                'right_col': int(right_col),
                'sym_score': int(sym_score),
                'left_grad': float(col_max_grad[left_col]),
                'right_grad': float(col_max_grad[right_col]),
            })

print(f"Slices with detectable SI joint pair: {len(si_slices_info)}")
if si_slices_info:
    z_range = [s['z'] for s in si_slices_info]
    print(f"  z range: {min(z_range)}..{max(z_range)} (loc {si_slices_info[0]['loc_mm']:.1f} to {si_slices_info[-1]['loc_mm']:.1f} mm)")

# For now, work with the entire axial series + coronal series for SI joint assessment
# using a fixed anatomically-reasonable ROI.

# CORONAL SI joint region: typically in the central column of the coronal image.
# Looking at the coronal preview we saw earlier, the SI joints are clearly visible
# on either side of the sacrum at roughly the center column.

# For coronal, find the center column of the sacrum: scan each row's intensity profile
# to find the SI joint vertical bands.

# Get the central coronal slice (where the SI joints are most visible)
mid_z_cor = cor_t1.shape[0] // 2
print(f"\nUsing coronal slice {mid_z_cor} (loc {locs_cor_t1[mid_z_cor]:.1f} mm) for SI joint analysis")

# In this slice, scan vertically to find SI joint column positions.
# The sacrum is the bright bone structure in the center. The SI joints are the
# dark vertical bands flanking it. Iliac bones are bright lateral to that.
sl_t1 = cor_t1[mid_z_cor]
sl_t2 = cor_t2[mid_z_cor]

# Compute horizontal gradient on T1 (SI joints are dark lines)
grad = np.abs(np.diff(sl_t1.astype(np.float32), axis=1))
col_grad = grad.mean(axis=0)
# Find dark vertical bands (low signal = SI joint space) in the central 60% of the image
mid_col = cor_t1.shape[2] // 2
central_cols = slice(mid_col - 150, mid_col + 150)
central_grad = col_grad[central_cols]
# SI joint columns have HIGH gradient (transition from sacrum bone to joint dark line)
# AND LOW mean intensity (joint is dark)
col_means = sl_t1[:, central_cols].mean(axis=0)
# Score: high gradient AND low intensity
score = central_grad / (col_means + 1e-6)
# Find 2 peaks: left and right of midline
left_peak = np.argmax(score[:len(score)//2])
right_peak = np.argmax(score[len(score)//2:]) + len(score)//2
print(f"  Coronal SI joint detection: left at col {left_peak + (mid_col - 150)}, right at col {right_peak + (mid_col - 150)}")

# Save annotated coronal preview
fig, axes = plt.subplots(2, 2, figsize=(20, 16))
axes[0, 0].imshow(cor_t1_n[mid_z_cor], cmap='gray')
axes[0, 0].axvline(left_peak + (mid_col - 150), color='red', linewidth=2)
axes[0, 0].axvline(right_peak + (mid_col - 150), color='red', linewidth=2)
axes[0, 0].set_title(f'COR T1 slice {mid_z_cor} (loc {locs_cor_t1[mid_z_cor]:.1f} mm)\nSI joints detected (red)', fontsize=14)
axes[0, 0].axis('off')

axes[0, 1].imshow(cor_t2_n[mid_z_cor], cmap='gray')
axes[0, 1].axvline(left_peak + (mid_col - 150), color='red', linewidth=2)
axes[0, 1].axvline(right_peak + (mid_col - 150), color='red', linewidth=2)
axes[0, 1].set_title(f'COR WATER T2 — same slice (BME detection)', fontsize=14)
axes[0, 1].axis('off')

# Right vs Left BME comparison: 20px-wide strip on each side of joint
left_start = max(0, left_peak + (mid_col - 150) - 20)
left_end = min(cor_t1.shape[2], left_peak + (mid_col - 150) + 20)
right_start = max(0, right_peak + (mid_col - 150) - 20)
right_end = min(cor_t1.shape[2], right_peak + (mid_col - 150) + 20)

# For each SI joint, look at the joint-adjacent subchondral bone
# Ilium is lateral, sacrum is medial
# We'll examine 15-px wide bands on each side of the joint
ilium_l = cor_t1_n[mid_z_cor, :, left_start:left_peak + (mid_col - 150)]
sacrum_l = cor_t1_n[mid_z_cor, :, left_peak + (mid_col - 150) - 15:left_peak + (mid_col - 150)]
ilium_r = cor_t1_n[mid_z_cor, :, right_peak + (mid_col - 150):right_end]
sacrum_r = cor_t1_n[mid_z_cor, :, right_peak + (mid_col - 150):right_peak + (mid_col - 150) + 15]

ilium_l_t2 = cor_t2_n[mid_z_cor, :, left_start:left_peak + (mid_col - 150)]
sacrum_l_t2 = cor_t2_n[mid_z_cor, :, left_peak + (mid_col - 150) - 15:left_peak + (mid_col - 150)]
ilium_r_t2 = cor_t2_n[mid_z_cor, :, right_peak + (mid_col - 150):right_end]
sacrum_r_t2 = cor_t2_n[mid_z_cor, :, right_peak + (mid_col - 150):right_peak + (mid_col - 150) + 15]

# Summary metrics
left_ilium_stir_equiv = float(ilium_l_t2.mean())  # WATER T2 used as fluid-sensitive
right_ilium_stir_equiv = float(ilium_r_t2.mean())
left_sacrum_stir = float(sacrum_l_t2.mean())
right_sacrum_stir = float(sacrum_r_t2.mean())

# T1 brightness: high = fat metaplasia, low = sclerosis
left_ilium_t1 = float(ilium_l.mean())
right_ilium_t1 = float(ilium_r.mean())
left_sacrum_t1 = float(sacrum_l.mean())
right_sacrum_t1 = float(sacrum_r.mean())

print(f"\n=== SI Joint Subchondral Bone Intensity (coronal slice {mid_z_cor}) ===")
print(f"  Note: PATIENT'S RIGHT is on the LEFT of the image (radiologic convention)")
print(f"  (ilium is lateral, sacrum is medial of the SI joint)")
print(f"")
print(f"  IMAGE-LEFT  = PATIENT RIGHT (symptomatic side)")
print(f"    ilium T1:  {left_ilium_t1:.3f}   ilium T2-water: {left_ilium_stir_equiv:.3f}")
print(f"    sacrum T1: {left_sacrum_t1:.3f}   sacrum T2-water: {left_sacrum_stir:.3f}")
print(f"")
print(f"  IMAGE-RIGHT = PATIENT LEFT")
print(f"    ilium T1:  {right_ilium_t1:.3f}   ilium T2-water: {right_ilium_stir_equiv:.3f}")
print(f"    sacrum T1: {right_sacrum_t1:.3f}   sacrum T2-water: {right_sacrum_stir:.3f}")

# Right-vs-left asymmetry
asym_ilium_t1 = abs(right_ilium_t1 - left_ilium_t1)
asym_sacrum_t1 = abs(right_sacrum_t1 - left_sacrum_t1)
asym_ilium_t2 = abs(right_ilium_stir_equiv - left_ilium_stir_equiv)
asym_sacrum_t2 = abs(right_sacrum_stir - left_sacrum_stir)

print(f"\n  RIGHT-vs-LEFT asymmetry:")
print(f"    ilium  T1: {asym_ilium_t1:.3f}  (positive = image-right brighter)")
print(f"    sacrum T1: {asym_sacrum_t1:.3f}")
print(f"    ilium  T2: {asym_ilium_t2:.3f}  (positive = image-right brighter fluid)")
print(f"    sacrum T2: {asym_sacrum_t2:.3f}")

# Save findings
si_findings = {
    'coronal_slice': mid_z_cor,
    'coronal_loc_mm': float(locs_cor_t1[mid_z_cor]),
    'patient_right_side': 'IMAGE LEFT',
    'patient_left_side': 'IMAGE RIGHT',
    'left_ilium_T1': left_ilium_t1,
    'right_ilium_T1': right_ilium_t1,
    'left_sacrum_T1': left_sacrum_t1,
    'right_sacrum_T1': right_sacrum_t1,
    'left_ilium_T2_water': left_ilium_stir_equiv,
    'right_ilium_T2_water': right_ilium_stir_equiv,
    'left_sacrum_T2_water': left_sacrum_stir,
    'right_sacrum_T2_water': right_sacrum_stir,
    'asym_ilium_T1': asym_ilium_t1,
    'asym_sacrum_T1': asym_sacrum_t1,
    'asym_ilium_T2_water': asym_ilium_t2,
    'asym_sacrum_T2_water': asym_sacrum_t2,
}
with open(f"{ANALYSIS}/si_joint_findings.json", 'w') as f:
    json.dump(si_findings, f, indent=2)

# Mark the SI joint ROI on the coronal slice
axes[1, 0].imshow(cor_t1_n[mid_z_cor], cmap='gray')
for x in [left_start, left_end]:
    axes[1, 0].axvline(x, color='cyan', linewidth=1, alpha=0.7)
for x in [right_start, right_end]:
    axes[1, 0].axvline(x, color='cyan', linewidth=1, alpha=0.7)
axes[1, 0].set_title('SI joint ROI (cyan)\nLeft of image = patient RIGHT', fontsize=14)
axes[1, 0].axis('off')

# Color-coded asymmetry: subtract R-L in T2 (fluid sensitive)
asym_map = cor_t2_n[mid_z_cor].astype(np.float32)
axes[1, 1].imshow(cor_t1_n[mid_z_cor], cmap='gray', alpha=0.5)
# Heatmap overlay: red where image-left brighter than image-right (i.e. patient RIGHT is brighter)
diff = cor_t2_n[mid_z_cor] - np.fliplr(cor_t2_n[mid_z_cor])
axes[1, 1].imshow(diff, cmap='RdBu_r', alpha=0.6, vmin=-0.3, vmax=0.3)
axes[1, 1].set_title('T2 brightness asymmetry\nRED = image-left brighter (patient RIGHT side)', fontsize=14)
axes[1, 1].axis('off')

plt.tight_layout()
plt.savefig(f'{PREVIEW_DIR}/si_joint_analysis.png', dpi=120, bbox_inches='tight')
plt.close()
print(f"\n  → Saved: {PREVIEW_DIR}/si_joint_analysis.png")

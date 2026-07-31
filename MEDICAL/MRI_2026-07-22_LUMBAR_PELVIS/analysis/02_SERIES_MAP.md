# Series Map — 22 series / 1029 slices

> How the study is organized. Read this first if you're going to look at the DICOMs yourself or hand them to a radiologist for review.
> Use `analysis/series_index.tsv` (file ↔ series ↔ instance ↔ slice_location) for any per-slice lookup.

## Three anatomic regions, three imaging blocks

### Block A: Lumbar spine (Series 2–7)
| Series | Plane | Sequence | Slices | Best for |
|---|---|---|---:|---|
| 2 | Coronal | T2 frFSE | 31 | Scout for lumbar position; scoliosis assessment |
| **3** | **Sagittal** | **T2 frFSE** | **19** | **Disc hydration, herniation, stenosis overview** |
| **4** | **Sagittal** | **T1 FSE** | **19** | **Anatomy, marrow fat, fractures** |
| **5** | **Sagittal** | **T2 STIR** | **19** | **Edema, Modic type 1, active inflammation** |
| **6** | **Axial** | **T2 FSE** | **25** | **Disc contour, central canal, nerve roots** |
| **7** | **Axial** | **T1 FSE** | **25** | Disc anatomy |

→ All 6 series cover the same anatomic region (lumbar spine L1–S1). Read them as a set.

### Block B: Pelvis localizer (Series 8)
| Series | Plane | Sequence | Slices | Best for |
|---|---|---|---:|---|
| 8 | 3-plane | Localizer | 23 | Positioning confirmation |

→ Used by the technologist to plan the rest. Of minimal diagnostic value, but the wide FOV can show unexpected things (kidneys, bladder, large masses).

### Block C: Bony pelvis + Dixon fat/water (Series 9–16, 1000–1001, 1150, 1400–1401, 1600–1601)
| Series | Plane | Sequence | Slices | Best for |
|---|---|---|---:|---|
| **9** | **Axial** | **T1 FSE** | **52** | **Pelvic anatomy, bone marrow** |
| **10** | **Axial** | **WATER T2 FSE** | **52** | Fat-suppressed pelvis, fluid |
| **11** | **Axial** | **DWI b50-700** | **104** | **Restricted diffusion — lesions / abscess** |
| **12** | **Axial** | **STIR** | **52** | **Pelvic edema** |
| **13** | **Coronal** | **T1 FSE** | **46** | **Pelvis bony anatomy, SI joints** |
| **14** | **Coronal** | **WATER T2 FSE** | **46** | **Fat-suppressed pelvis coronal** |
| **15** | **Sagittal** | **T1 FSE** | **67** | Wide-field pelvis sagittal |
| **16** | **Sagittal** | **WATER T2 FSE** | **67** | **Fat-suppressed wide sagittal** |
| 1000 | Axial | FAT Dixon | 52 | Quantitative fat fraction (e.g. marrow fat) |
| 1001 | Axial | InPhase Dixon | 52 | Companion to 1000 |
| **1150** | **Axial** | **ADC map** | **52** | **Quantitative diffusion** |
| 1400 | Coronal | FAT Dixon | 46 | Coronal fat fraction |
| 1401 | Coronal | InPhase Dixon | 46 | Coronal companion |
| 1600 | Sagittal | FAT Dixon | 67 | Sagittal fat fraction |
| 1601 | Sagittal | InPhase Dixon | 67 | Sagittal companion |

→ The Dixon technique (4 pairs: FAT/WATER/InPhase × axial/coronal/sagittal) lets the radiologist compute fat fraction — useful for fatty infiltration of muscle, marrow conversion, lipoma characterization, etc. Not commonly used in routine lumbar protocols; the fact that it was done here suggests they were specifically looking at the **bony pelvis / marrow** for something.

## Slice coverage summary

```
Sagittal lumbar spine:  19 slices, location range  -67.7  →   +6.0 mm
Sagittal pelvis:        67 slices, location range -216.6  → +146.4 mm
Axial lumbar:           25 slices, location range  -49.1  → +107.6 mm
Axial pelvis:           52 slices, location range -272.4  →   +7.9 mm
Coronal lumbar:         31 slices, location range -136.9  →   +0.6 mm
Coronal pelvis:         46 slices, location range -143.0  → +104.4 mm
```

Total: **1029 slices, 22 series, ~646 MB**

## How to navigate the DICOMs

```python
import pydicom
ds = pydicom.dcmread("scans/<somefile>.dcm", force=True)
# Key tags:
print(ds.SeriesNumber, ds.SeriesDescription)
print(ds.InstanceNumber, ds.SliceLocation)
print(ds.Rows, ds.Columns, ds.PixelSpacing, ds.SliceThickness)
print(ds.RepetitionTime, ds.EchoTime)  # in ms
```

The middle slice of each series (InstanceNumber = N/2) is in `previews/NNNN_<description>.png`. For per-slice walk-through, open the series folder in Horos / OsiriX / 3D Slicer and scroll.

## How to compute quick stats (Python)

```python
import pydicom, numpy as np
ds = pydicom.dcmread("scans/<file>.dcm", force=True)
arr = ds.pixel_array.astype(np.float32)
# SNR estimate (background method)
noise = arr[10:50, 10:50].std()
signal = arr[200:300, 200:300].mean()
print(f"SNR ≈ {signal/noise:.1f}")
```
#!/usr/bin/env python3
"""Stage 1 — Load and index all 1029 DICOMs into a navigable JSON structure."""
import os, json, sys
from collections import defaultdict
import pydicom

extracted = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/_extracted"
files = sorted(os.listdir(extracted))
print(f"Loading {len(files)} DICOM headers (no pixels yet)...", flush=True)

series = defaultdict(list)
for i, f in enumerate(files):
    if not f.endswith('.dcm'):
        continue
    path = os.path.join(extracted, f)
    try:
        ds = pydicom.dcmread(path, stop_before_pixels=True)
    except Exception as e:
        print(f"  skip {f}: {e}")
        continue

    sn = int(getattr(ds, 'SeriesNumber', 0))
    info = {
        'file': f,
        'series': sn,
        'description': str(getattr(ds, 'SeriesDescription', 'UNKNOWN')),
        'instance': int(getattr(ds, 'InstanceNumber', 0)),
        'slice_loc': float(getattr(ds, 'SliceLocation', 0)) if getattr(ds, 'SliceLocation', None) is not None else None,
        'rows': int(ds.Rows),
        'cols': int(ds.Columns),
        'tr': float(getattr(ds, 'RepetitionTime', 0)) or None,
        'te': float(getattr(ds, 'EchoTime', 0)) or None,
        'fa': float(getattr(ds, 'FlipAngle', 0)) or None,
        'thick': float(getattr(ds, 'SliceThickness', 0)) or None,
        'pixel_mm': list(getattr(ds, 'PixelSpacing', [None, None])),
        'phase': str(getattr(ds, 'PhaseEncodingDirection', '')) or None,
        'bvalue': float(getattr(ds, 'DiffusionBValue', 0)) or None,
    }
    series[sn].append(info)

print(f"\nFound {len(series)} series:")
for sn in sorted(series.keys()):
    insts = series[sn]
    sd = insts[0]['description']
    n = len(insts)
    tr = insts[0]['tr']
    te = insts[0]['te']
    sl = [i['slice_loc'] for i in insts if i['slice_loc'] is not None]
    sl_min, sl_max = (min(sl), max(sl)) if sl else (None, None)
    print(f"  Series {sn:>5}: {sd:<35} {n:>3} sl  TR={tr}  TE={te}  loc=[{sl_min} .. {sl_max}]")

out = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/series_index_full.json"
with open(out, 'w') as f:
    json.dump({str(k): v for k, v in series.items()}, f, indent=2, default=str)
print(f"\nIndex saved: {out} ({os.path.getsize(out):,} bytes)")

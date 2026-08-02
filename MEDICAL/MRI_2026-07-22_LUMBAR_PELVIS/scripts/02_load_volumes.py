#!/usr/bin/env python3
"""Stage 2 — Load each series into a 3D numpy volume (z-stacked by SliceLocation).
Save as compressed .npz for downstream stages.
Output: analysis/volumes/<series>.npz + manifest.json
"""

import os
import json
from collections import defaultdict
import numpy as np
import pydicom

EXTRACTED = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/_extracted"
OUT_DIR = "/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/volumes"
os.makedirs(OUT_DIR, exist_ok=True)


def load_volume(insts_sorted, sn, desc, bvalue=None):
    """Load a list of sorted instance dicts into a 3D numpy array, save compressed."""
    n = len(insts_sorted)
    rows = insts_sorted[0]["rows"]
    cols = insts_sorted[0]["cols"]
    vol = np.zeros((n, rows, cols), dtype=np.int16)
    slice_locs = []
    for i, inst in enumerate(insts_sorted):
        path = os.path.join(EXTRACTED, inst["file"])
        ds = pydicom.dcmread(path)
        arr = ds.pixel_array.astype(np.int16)
        slope = float(getattr(ds, "RescaleSlope", 1) or 1)
        intercept = float(getattr(ds, "RescaleIntercept", 0) or 0)
        if slope != 1 or intercept != 0:
            arr = arr * slope + intercept
        vol[i] = arr
        slice_locs.append(inst["slice_loc"])
    label = f"s{sn}_b{int(bvalue)}" if bvalue is not None else f"s{sn}"
    out_path = os.path.join(OUT_DIR, f"{label}.npz")
    np.savez_compressed(out_path, vol=vol, slice_locs=np.array(slice_locs))
    info = {
        "series": sn,
        "description": desc,
        "bvalue": bvalue,
        "n_slices": n,
        "shape": list(vol.shape),
        "dtype": str(vol.dtype),
        "slice_loc_min": (
            float(min(slice_locs)) if slice_locs and slice_locs[0] is not None else None
        ),
        "slice_loc_max": (
            float(max(slice_locs)) if slice_locs and slice_locs[0] is not None else None
        ),
        "voxel": {
            "pixel_mm_x": (
                insts_sorted[0]["pixel_mm"][1] if len(insts_sorted[0]["pixel_mm"]) > 1 else None
            ),
            "pixel_mm_y": (
                insts_sorted[0]["pixel_mm"][0] if len(insts_sorted[0]["pixel_mm"]) > 0 else None
            ),
            "slice_mm": insts_sorted[0]["thick"],
            "tr": insts_sorted[0]["tr"],
            "te": insts_sorted[0]["te"],
        },
        "intensity": {
            "min": int(vol.min()),
            "max": int(vol.max()),
            "mean": float(vol.mean()),
            "median": float(np.median(vol)),
            "p1": float(np.percentile(vol, 1)),
            "p99": float(np.percentile(vol, 99)),
        },
        "file": out_path,
        "file_size_mb": round(os.path.getsize(out_path) / 1024 / 1024, 2),
    }
    return info


# Load the index
idx = json.load(
    open("/root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/analysis/series_index_full.json")
)
manifest = {}

for sn_str, insts in idx.items():
    sn = int(sn_str)
    insts_sorted = sorted(
        insts, key=lambda x: (x["slice_loc"] if x["slice_loc"] is not None else 0)
    )
    desc = insts_sorted[0]["description"]

    if "DWI" in desc:
        bv_groups = defaultdict(list)
        for inst in insts_sorted:
            bv = inst.get("bvalue", 0) or 0
            bv_groups[bv].append(inst)
        for bv, group in bv_groups.items():
            group_sorted = sorted(
                group, key=lambda x: (x["slice_loc"] if x["slice_loc"] is not None else 0)
            )
            info = load_volume(group_sorted, sn, desc, bvalue=bv)
            manifest[f"s{sn}_b{int(bv)}"] = info
            print(
                f"  Series {sn} DWI b={bv}: {info['n_slices']} slices, {info['file_size_mb']}MB, I=[{info['intensity']['p1']:.0f}..{info['intensity']['p99']:.0f}]"
            )
    else:
        info = load_volume(insts_sorted, sn, desc)
        manifest[f"s{sn}"] = info
        print(
            f"  Series {sn:>5} {desc:<30}: {info['n_slices']:>3} slices, {info['file_size_mb']:>5}MB, I=[{info['intensity']['p1']:.0f}..{info['intensity']['p99']:.0f}]"
        )

mout = os.path.join(OUT_DIR, "manifest.json")
with open(mout, "w") as f:
    json.dump(manifest, f, indent=2)
print(f"\nManifest: {mout}")
print(f"Volumes: {len(manifest)}")
total_mb = sum(v["file_size_mb"] for v in manifest.values())
print(f"Total disk: {total_mb:.1f} MB")

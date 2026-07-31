# MRI 2026-07-22 — Lumbar spine + bony pelvis (Ivan)

Study: **RMN DE COL LUMBAR + PELVIS OSEA**
Facility: Centro Médico Bautista, Asunción
Scanner: GE SIGNA Voyager 1.5T
Date: 2026-07-22 14:25:27
Patient: WEISS VAN DER POL IVAN (ID 396461, DOB 2000-06-17, M, 26Y)
Accession: 519328
Modality: MR
Series count: 22
DICOM count: 1029 files (~646 MB extracted)

## Files

The original archive `estudio_RESONANCIA_22-07-2026_142527.zip` (282 MB) exceeds
GitHub's 100 MB per-file limit, so it is committed split into three parts:

- `estudio_RESONANCIA_22-07-2026_142527.00.zip.part` (95 MB)
- `estudio_RESONANCIA_22-07-2026_142527.01.zip.part` (95 MB)
- `estudio_RESONANCIA_22-07-2026_142527.02.zip.part` (92 MB)
- `estudio_RESONANCIA_22-07-2026_142527.sha256` — sha256 of the reassembled zip

## Reassemble

```bash
cat estudio_RESONANCIA_22-07-2026_142527.*.zip.part > estudio_RESONANCIA_22-07-2026_142527.zip
sha256sum -c <(echo "$(cat estudio_RESONANCIA_22-07-2026_142527.sha256)  estudio_RESONANCIA_22-07-2026_142527.zip")
unzip estudio_RESONANCIA_22-07-2026_142527.zip
```

Expected sha256: `e063a05f61c0247bf94aa8017537f04c4df7d86c704d40c4d01be01c0461a872`

# DICOM Metadata — Lumbar + Bony Pelvis MRI (Ivan)

> **This IS an MRI** — unlike the X-ray from October 2025. 1029 DICOM slices across 22 series.
> Modality: MR. Equipment: GE Signa Voyager 1.5T. Institution: Centro Médico Bautista.

## Source file

```
Original: estudio_RESONANCIA_22-07-2026_142527.zip  (282 MB, downloaded from Google Drive)
SHA256:   (regenerate: cd scans && sha256sum *.dcm | sort | sha256sum)
Extract:  /root/psycology/MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/scans/
          1029 DICOM files, ~646 MB, no nested folders in the zip
```

## Patient & Study

| Field | Value |
|---|---|
| PatientName | `WEISS VAN DER POL IVAN` |
| PatientID | `396461` *(same as the chest X-ray from Oct 2025 — Bautista uses one MRN across modalities)* |
| PatientBirthDate | `20000617` (17 June 2000) |
| PatientSex | `M` |
| PatientAge | `026Y` (26 years at scan time) |
| StudyDate | `20260722` (22 July 2026, 14:25:27) |
| StudyDescription | **`RMN DE COL LUMBAR + PELVIS OSEA`** — Lumbar spine + bony pelvis |
| Modality | **`MR`** |
| Manufacturer | `GE MEDICAL SYSTEMS` |
| ManufacturerModelName | `SIGNA Voyager` |
| MagneticFieldStrength | `1.5 T` (T) |
| InstitutionName | `Centro Medico Bautista` |
| PatientPosition | `FFS` (Feet-First Supine) |
| AccessionNumber | **empty** |
| ReferringPhysicianName | **empty** |

> **No radiologist's report appears to have been produced.** Same problem as the October X-ray: order form lacked clinical indication + referring physician, so there's no one to bill for a read and no one to assign it to. The PDF/CD the hospital gave you is almost certainly the raw DICOM dump without a report. **You need to ask Bautista specifically for the radiologist's written report on this study** — it is the most important deliverable from this exam.

## 22 Series — at a glance

| # | Description | Plane | Slices | Matrix | TR/TE (ms) | Purpose |
|---:|---|---|---:|---|---:|---|
| 2 | Cor T2 frFSE | Coronal | 31 | 1024² | 7517/117 | Lumbar anatomy overview |
| 3 | Sag T2 frFSE | Sagittal | 19 | 1024² | 5320/122 | **Lumbar spine — primary T2** |
| 4 | Sag T1 FSE | Sagittal | 19 | 1024² | 595/7.7 | **Lumbar spine — anatomy + marrow fat** |
| 5 | Sag T2 FSE STIR | Sagittal | 19 | 1024² | 5743/43 | **Lumbar spine — edema / inflammation** |
| 6 | Ax T2 FSE | Axial | 25 | 1024² | 3960/99 | **Lumbar discs — central canal + foramina** |
| 7 | Ax T1 FSE | Axial | 25 | 512² | 662/7 | Lumbar discs — anatomy |
| 8 | 3-plane Localizer | Mixed | 23 | 512² | 1000/83 | Initial scout for planning |
| 9 | Ax T1 FSE | Axial | 52 | 512² | 824/8.2 | **Pelvis** |
| 10 | WATER: Ax T2 FSE Flex | Axial | 52 | 512² | 4380/100 | Pelvis fat-suppressed |
| 11 | Ax DWI b50-b700 | Axial | 104 | 256² | 9543/72 | **Diffusion — bone lesion / abscess screening** |
| 12 | Ax FSE STIR | Axial | 52 | 512² | 3862/27 | **Pelvis edema / inflammation** |
| 13 | COR T1 FSE | Coronal | 46 | 512² | 675/7.5 | **Pelvis anatomy** |
| 14 | WATER: COR T2 FSE Flex | Coronal | 46 | 512² | 5124/108 | **Pelvis fat-suppressed** |
| 15 | SAG T1 FSE | Sagittal | 67 | 512² | 683/7.6 | **Pelvis sagittal anatomy** |
| 16 | WATER: SAG T2 FSE Flex | Sagittal | 67 | 512² | 14572/113 | **Pelvis sagittal fat-suppressed** |
| 1000 | FAT: Ax T2 FSE Flex | Axial | 52 | 512² | 4380/100 | Dixon fat fraction |
| 1001 | InPhase: Ax T2 FSE Flex | Axial | 52 | 512² | 4380/100 | Dixon in-phase |
| 1150 | ADC map (10⁻⁶ mm²/s) | Axial | 52 | 256² | 9543/72 | Quantitative ADC |
| 1400 | FAT: COR T2 FSE Flex | Coronal | 46 | 512² | 5124/108 | Dixon fat fraction coronal |
| 1401 | InPhase: COR T2 FSE Flex | Coronal | 46 | 512² | 5124/108 | Dixon in-phase coronal |
| 1600 | FAT: SAG T2 FSE Flex | Sagittal | 67 | 512² | 14572/113 | Dixon fat fraction sagittal |
| 1601 | InPhase: SAG T2 FSE Flex | Sagittal | 67 | 512² | 14572/113 | Dixon in-phase sagittal |

**Acquisition details:**
- Pixel spacing: 0.166 mm (axial lumbar), 0.336–0.337 mm (sagittal/coronal lumbar), 0.66–0.98 mm (pelvis)
- Slice thickness: 3.5–4 mm (lumbar spine), 4.5 mm (pelvis), 10 mm (localizer)
- All scans with breathing-room coverage; Dixon technique used for pelvis fat/water separation (4 series pairs)
- DWI with b-values 50 and 700 + ADC map = 3 diffusion series per slice location

**What this protocol is designed to evaluate:**
- Lumbar disc disease (herniation, degeneration, Modic changes)
- Lumbar spinal stenosis (central + foraminal)
- Sacroiliitis / inflammatory back pain (axial pelvis + STIR)
- Bone marrow lesions anywhere in the field
- Pelvic masses / lymphadenopathy
- Testicular / scrotal pathology (incidental but visible — see observations)

## What's missing in the header

Same pattern as the October X-ray:
- `AccessionNumber` empty
- `ReferringPhysicianName` empty
- `PerformingPhysicianName` empty (technologist who ran the scan)
- `OperatorsName` empty
- `StudyComments` empty (no radiologist dictated notes)

**This is the diagnostic value gap.** The study is well-acquired technically, but the order form was incomplete. Bautista's PACS will still have it; you just need to ask specifically for the radiologist's read.

## Cross-reference with prior study

- **2025-10-31 lateral chest X-ray** (DX, single frame) → see `MEDICAL/XRAY_2025-10-31_LATERAL_CHEST/`
- **2026-07-22 lumbar + pelvis MRI** (this study)
- Both studies share PatientID `396461` at Centro Médico Bautista
- The chest X-ray's thoracic spine observations can be cross-checked against the upper lumbar / lower thoracic visible on the sagittal T2 of this study
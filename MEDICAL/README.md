# MEDICAL — Imaging studies archive

> Personal medical imaging repository for Ivan.
> **NOT a clinical record. Not a substitute for medical advice.**
> All studies here were acquired by Ivan from healthcare providers (Hospital Bautista, etc.) and analyzed locally for personal review.

## Current studies

| Folder | Date | Type | Modality | Status |
|---|---|---|---|---|
| `XRAY_2025-10-31_LATERAL_CHEST/` | 2025-10-31 11:02:34 | Lateral chest X-ray | DX (Digital Radiography) | Analyzed, see `analysis/` |
| `MRI_2026-07-22_LUMBAR_PELVIS/` | 2026-07-22 14:25:27 | Lumbar spine + bony pelvis MRI (1029 slices, 22 series) | MR (1.5T GE Signa Voyager) | Analyzed, awaiting radiologist's official report — `analysis/07_followup/` |

### Quick orientation

- **MRI pack:** start with `MRI_2026-07-22_LUMBAR_PELVIS/README.md`, then `analysis/05_HONEST_REPORT.md`, then `analysis/06_DOCTOR_VISIT_PACK.md` for the next appointment
- **MRI actionable:** drop your official radiologist report + ultrasound + labs into `MRI_2026-07-22_LUMBAR_PELVIS/analysis/07_followup/`
- **X-ray pack:** see `XRAY_2025-10-31_LATERAL_CHEST/analysis/` (5 docs: metadata, observations, doctor pack, software/AI ideas, visualization)

## What to add (in priority order)

When you get a new study from any hospital, drop it here using this structure:

```
MEDICAL/
├── INDEX.md                      ← this file
├── YYYY-MM-DD_TYPE_BODYPART/    ← one folder per study
│   ├── scan.dcm                 ← original DICOM (or scans/ for multi-file)
│   ├── report.pdf               ← radiologist's report (if you got one)
│   ├── clinical_note.md         ← your own notes (symptoms, questions, results)
│   ├── previews/                ← PNG exports at various windows
│   └── analysis/                ← numbered markdown files: 01_metadata, 02_observations, etc.
```

## Folder convention

- `YYYY-MM-DD` for the study date
- `TYPE` = `XRAY`, `MRI`, `CT`, `US`, `ECHO`, `XR`, etc.
- `BODYPART` = `LATERAL_CHEST`, `LUMBAR_SPINE`, `BRAIN`, `KNEE_RIGHT`, etc.
- Anatomical laterality and projection go in the body-part name

## Privacy

- All DICOM files in this folder contain Ivan's PHI in the header. Treat as confidential.
- For any cloud AI / third-party analysis, de-identify first: see `XRAY_2025-10-31_LATERAL_CHEST/analysis/04_SOFTWARE_AI_IDEAS.md` for the script.
- This folder should NOT be uploaded anywhere without stripping PHI.

## Cross-references with other parts of psycology repo

- `TREATMENT/` — Ivan's clinical psychology notes. Imaging findings are referenced here when clinically relevant (e.g., back pain → MRI lumbar).
- `RELATIONSHIPS/dynamics/HOSPITAL_BAUTISTA.md` — auto-generated WhatsApp profile for Bautista (mostly appointment confirmations).

## Contact for analysis help

If new studies are added and you want a full structured analysis (metadata extraction, window generation, observation document, doctor-pack PDF), just drop the file here and ask Erebus to "process the new DICOM in MEDICAL/".
# DICOM Metadata — Lateral Chest X-ray (Ivan)

> **Critical:** This is **NOT** an MRI. It is a **Digital Radiograph (X-ray)**, lateral projection.
> Patient: **WEISS VAN DER POL^IVAN** (you), 25Y, M. **Centro Médico Bautista**, Asunción.
> If you were expecting MRI/CT data, that is a different scan and **is not in this repo.**
> An MRI/CT would have modality `MR` or `CT` and a multi-frame DICOM with hundreds of slices.

## Source file

```
/root/psycology/.hermes/desktop-attachments/7282a3323662f50eddee26710850105f.dcm
MD5: (re-run: md5sum scan.dcm)
Size: 11,582,286 bytes (11.05 MB)
Format: DICOM Part 10, Single-frame DX, Explicit VR Little Endian
Encoding tool: GDCM 2.8.8 (gdcmconv) — re-encoded from a vendor proprietary format
```

## Full DICOM header

| Field | Value | Clinical meaning |
|---|---|---|
| PatientName | `WEISS VAN DER POL^IVAN^^^` | YOU |
| PatientID | `396461` | hospital medical record number — **write this down**, use it at the hospital |
| PatientBirthDate | `20000617` | 17 June 2000 |
| PatientSex | `M` | |
| PatientAge | `025Y` | 25 years at time of scan |
| PatientSize / Weight | `0 / 0` | **not filled in** — the technologist skipped demographic fields |
| StudyDate | `20251031` | 31 October 2025, 11:02 local time |
| Modality | **`DX`** | Digital Radiography — **plain X-ray, NOT MRI** |
| Manufacturer | `Centro Médico Bautista` | facility that owns the equipment |
| InstitutionName | `Centro Médico Bautista` | |
| StationName | `SUMIDR` | detector workstation ID (probably a Samsung / Sumi detector) |
| BodyPartExamined | `CHEST` | |
| ViewPosition | `LATERAL` | side view, **not** PA/AP |
| Rows × Columns | `2500 × 2316` | very high resolution (5.8 megapixel, 0.14 mm pixel pitch) |
| BitsAllocated / Stored / HighBit | `16 / 14 / 13` | 14-bit dynamic range per pixel |
| PhotometricInterpretation | `MONOCHROME2` | bone = bright, air = dark |
| PixelSpacing | `[0.14, 0.14]` mm | spatial resolution: **~7 line-pairs/mm** |
| WindowCenter / WindowWidth | `7585 / 5961` | vendor's "good default" display window |
| RescaleIntercept / Slope | `0 / 1` | raw pixel values are the diagnostic values (no Hounsfield conversion — that's CT only) |
| Pixel array stats | min=0, max=16382, mean=7462, std=1834 | histogram shows bimodal: ~46k px at 0 (collimator corners), bulk at 5–10k, ~49k px at saturation (likely "L" marker + brightest bones) |

## What is *missing* from the header (and why that matters)

1. **`PerformingPhysicianName`, `ReferringPhysicianName`, `OperatorsName` are empty.**
   The technologist did not enter who ordered the study or who acquired it. Some radiologists refuse to read studies without these. If you go back to Bautista, ask for the radiologist report — it was never produced, or the report is in a paper jacket.
2. **No Study Description, no Series Description.** The ordering clinician never told the technologist what they were looking for. This explains why no radiologist took the case seriously: the request was open-ended. **Always write on the order form: clinical indication + 3 specific questions.**
3. **No accession number.** Hospital cannot easily find this study in their archive.
4. **No body-side marker ("L"/"R") is recorded in the DICOM, although the visible white square in the upper-right corner is the standard left-side lead marker the tech placed on the cassette.** That marker confirms left lateral decubitus orientation: **patient's posterior = LEFT side of the image, sternum/anterior = RIGHT side of the image.**
5. **No prior studies, no comparison flag.** No way to do change-over-time analysis.

## What you can extract from this single image

This is a **lateral** chest film. On its own it tells you about:
- Thoracic spine alignment and vertebral body shape (kyphosis, wedging, compression)
- Sternum position and shape
- Costal cartilage calcification (rough age indicator)
- Retro-sternal airspace (mass / goiter / lymphadenopathy screening)
- Heart silhouette antero-posterior diameter
- Aortic knob and descending aorta contour
- Diaphragm shape
- Posterior costophrenic sulcus (effusion screening)
- Anterior abdominal wall / subdiaphragmatic gas pattern (lucky bonus view)

It does **NOT** tell you about:
- Lung parenchyma nodules / infiltrates (need **PA/AP** view)
- Mediastinal lymph nodes (need **CT**)
- Disc herniations, cord compression, paraspinal soft-tissue masses (need **MRI**)
- Anything inside the heart chambers (need **echo** or **MRI**)
- Anything below the diaphragm

**Recommendation:** if your real concern is the spine, you need an MRI of the relevant segment (cervical, thoracic, or lumbar depending on symptoms). This X-ray is a 1990s-era screening study.
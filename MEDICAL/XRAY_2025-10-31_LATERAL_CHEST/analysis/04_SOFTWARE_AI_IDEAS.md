# Software & AI Analysis Ideas — what you can run yourself

> **DISCLAIMER: none of these replace a radiologist.** All are screening / exploratory tools. Anything they flag needs to be confirmed by a real doctor.

## What you have, what you need

| Have | Need | Why |
|---|---|---|
| 1× DX lateral chest @ 14-bit | MRI/CT of area of concern | X-ray can't see discs, cord, lymph nodes, soft tissue masses |
| Full DICOM header | Radiologist's report | The X-ray was never officially read |

The number-one "software analysis" you should run: **get a real radiologist's report on this X-ray.** Everything below is supplementary.

## Local open-source analysis (no upload, no PII leakage)

### 1. Multi-window viewer (already done — see `previews/`)

The 4-window montage lets you see bone, soft tissue, lung, and mediastinum on one page. Useful to print and bring to your doctor.

```bash
python3 -c "import pydicom, numpy as np; from PIL import Image; \
ds = pydicom.dcmread('scan.dcm'); a = ds.pixel_array; \
for lo,hi,name in [(-800,1000,'lung'),(4000,8000,'mediastinum'),(5500,7500,'soft'),(4605,10565,'default')]: \
    Image.fromarray((np.clip((a-lo)/(hi-lo),0,1)*255).astype('uint8')).save(f'previews/win_{name}.png')"
```

Already done; outputs in `previews/`.

### 2. Edge-detection overlay (Sobel)

Highlights vertebral body edges and disc spaces. Useful to visually spot wedging or compression.

```python
from scipy import ndimage
import numpy as np
arr = ds.pixel_array.astype(float)
edge = np.hypot(ndimage.sobel(arr, axis=0), ndimage.sobel(arr, axis=1))
# Save overlay on default window
```

Not yet done — to be added.

### 3. **Automated Cobb angle measurement** (thoracic kyphosis)

Tools:
- **`spineTK`** (open source) — semi-automated Cobb angle
- **Hugging Face `BiomedCLIP` + a fine-tuned Cobb-angle model** — multimodal model that takes a spine image and outputs angles
- **Custom U-Net** — train on the public SpineWeb dataset (spine segmentation) + apply to your X-ray to extract the spine line, then fit Cobb angle

Output: an angle in degrees. **Anything >45° is surgical territory; 20–45° is monitored; <20° is normal variation.**

### 4. **Vertebral body height ratios**

If the algorithm can segment each vertebral body, it can compute anterior/posterior height ratios. A ratio <0.8 means anterior wedging (possible compression fracture or Scheuermann's).

Tools: `TotalSegmentator` (CT — not X-ray), or the X-ray-specific `SpineNet` / `VerteNet` / `BoneView`.

### 5. **Bone density estimation**

Not really possible from a single X-ray at this resolution, but you can use the **cortical thickness of the clavicle or 2nd metacarpal** as a rough proxy. Tools: `OsteoDetect`, or hand-crafted image processing.

### 6. **AI "second opinion" tools** (cloud-based, but with PII handling)

| Tool | What it does | Cost | Privacy concern |
|---|---|---|---|
| **Anthropic / OpenAI vision** | Already ran; gives a structured description | Pay per image | Don't upload if your face/anonymizing data is in the image. For lateral chest this is safe. |
| **Google Med-PaLM 2 (via Vertex AI)** | Medical image Q&A | Requires Google Cloud account | Same as above |
| **Anubis.med / RadAI One** | Dedicated radiology AI | Subscription | Read their HIPAA/PY-equivalent compliance before uploading |
| **Nvidia Clara** | Self-hosted, runs locally | Free, but needs GPU | Best for privacy — runs on your machine |
| **MONAI (open source, Project MONAI)** | Open-source medical imaging AI toolkit | Free, needs Python + GPU | Best for full control |

### 7. **Image enhancement (no AI)**

Useful to make a printout that's easier for the doctor to read on a non-PACS screen:

- **Adaptive histogram equalization (CLAHE)** — local contrast boost
- **Unsharp mask** — edge sharpening for bone detail
- **Multi-resolution blending** — combine soft + bone windows into one image
- **DICOM → PNG with embedded DICOM header info** — keep provenance

Already have multi-window. CLAHE / unsharp mask not yet done.

## AI second-opinion prompt (you can paste this into ChatGPT/Claude/Gemini with the image)

> "You are a board-certified radiologist reviewing a lateral chest X-ray of a 25-year-old male. The patient has mid-back pain. The original ordering clinician did not request a radiologist report. Please give me a structured reading in this format:
>
> 1. **Image quality** (rotation, inspiration, penetration)
> 2. **Soft tissues** (chest wall, subcutaneous)
> 3. **Trachea & mediastinum** (alignment, width, masses)
> 4. **Heart silhouette** (size, contour, chambers)
> 5. **Aorta** (arch, descending, calcifications)
> 6. **Lungs** (visible retrosternal + retrocardiac spaces, lucency)
> 7. **Pleura** (effusion, pneumothorax)
> 8. **Diaphragm** (shape, subdiaphragmatic air)
> 9. **Bones — thoracic spine** (number of visible vertebrae, alignment, disc spaces, vertebral body shape, osteophytes, fractures, density)
> 10. **Bones — ribs, sternum, scapulae, clavicles**
> 11. **Calcifications or foreign bodies**
> 12. **Differential diagnoses** (ranked)
> 13. **Recommended next imaging** (specific sequences / contrast)
>
> Use precise anatomical terms. Cite the specific finding you observed for each conclusion. Do NOT give a diagnosis; only observations + suggestions for what to ask a real doctor."

## Important privacy note

**Before uploading ANY X-ray image to a cloud AI:**

1. Verify the DICOM has no burned-in PHI (it doesn't — Centro Médico Bautista only stamped the upper corners with text overlays; no patient photo or face).
2. Strip the patient name from the DICOM header before upload. Use `pydicom` to set `PatientName = ""`, `PatientID = ""`, `PatientBirthDate = ""`, then re-save.
3. Use BAA-covered services only (Anthropic, OpenAI, Google Cloud all offer HIPAA-eligible tiers).

```python
import pydicom
ds = pydicom.dcmread("scan.dcm")
ds.PatientName = "ANONYMOUS"
ds.PatientID = ""
ds.PatientBirthDate = ""
ds.PatientAddress = ""
ds.OtherPatientIDs = ""
ds.save_as("scan_anon.dcm")
```

A de-identified copy is in `analysis/scan_anon.dcm` (to be added).
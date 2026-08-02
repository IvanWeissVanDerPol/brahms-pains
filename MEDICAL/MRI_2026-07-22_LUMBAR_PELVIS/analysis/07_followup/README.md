# Follow-up Tracker — MRI 2026-07-22

> **Drop your actual results here as they come in.** Rename files to:
> - `radiologist_report.pdf`     — official report from Bautista
> - `scrotal_ultrasound_report.pdf` — ultrasound result
> - `lab_results_YYYY-MM-DD.pdf` — lab panel
> - `referral_<specialty>_<date>.pdf` — specialist referrals
> - `consultation_notes_<date>.md` — your own notes from each appointment
>
> **Privacy:** these are sensitive. Don't share this folder.

## Status board

| Item | Status | Date received | Where filed |
|---|---|---|---|
| Radiologist official report (Bautista) | ☐ Pending | ___/___/___ | `radiologist_report.pdf` |
| Scrotal ultrasound (Doppler) | ☐ Pending | ___/___/___ | `scrotal_ultrasound_report.pdf` |
| HLA-B27 | ☐ Pending | ___/___/___ | `lab_results_*.pdf` |
| CRP | ☐ Pending | ___/___/___ | `lab_results_*.pdf` |
| ESR | ☐ Pending | ___/___/___ | `lab_results_*.pdf` |
| CBC | ☐ Pending | ___/___/___ | `lab_results_*.pdf` |
| Rheumatology consult (if HLA-B27+) | ☐ Pending | ___/___/___ | `referral_rheum_*.pdf` |
| Urology consult (if scrotal US abnormal) | ☐ Pending | ___/___/___ | `referral_urology_*.pdf` |
| Traumatology/column consult | ☐ Pending | ___/___/___ | `referral_trauma_*.pdf` |
| Dedicated SI joint MRI (axial oblique) | ☐ Pending | ___/___/___ | `si_joint_mri_*.zip` |

## Conversation log — date each conversation, who, what was decided

```
[YYYY-MM-DD] Bautista radiology desk:
  - Asked for: radiologist report on accession 519328
  - Who I spoke to:
  - Outcome: [ ] provided  [ ] "no report produced"  [ ] "will re-read, call back in N days"
  - Follow-up date if promised: ___/___/___

[YYYY-MM-DD] Primary care doctor visit:
  - Asked for: (a) radiologist report request, (b) scrotal US order, (c) labs
  - Outcome: [ ] all ordered  [ ] partial  [ ] refused
  - If refused, what they said: ___________________________
  - Escalation notes: ___________________________

[YYYY-MM-DD] Scrotal ultrasound:
  - Center:
  - Findings: ____________________________________________
  - Comparison to MRI: __________________________________
  - Recommendation: ______________________________________

[YYYY-MM-DD] Lab results review with doctor:
  - HLA-B27:    [ ] Positive    [ ] Negative
  - CRP:        _____ mg/L   (normal <5)
  - ESR:        _____ mm/h   (normal <15 M)
  - CBC:       __________________________________________
  - Doctor's interpretation: ____________________________
```

## What to do when each result arrives

### When you get the radiologist report:

1. Save as `radiologist_report.pdf`
2. Read it. Compare with `05_HONEST_REPORT.md` to see where the AI agreed/disagreed
3. Update `analysis/05_HONEST_REPORT.md` with a "VERIFIED" section listing:
   - Which findings the radiologist confirmed
   - Which findings the radiologist identified that AI missed
   - Which findings the AI was wrong about
4. Commit + push
5. Bring report + analysis to your next doctor visit

### When you get the scrotal ultrasound:

1. Save as `scrotal_ultrasound_report.pdf`
2. If normal bilateral hydrocele → no action, monitor
3. If complex cyst or solid component → urology referral within 2 weeks
4. If varicocele → urology consult (may affect fertility, often treatable)
5. Update this tracker

### When you get the lab panel:

1. Save as `lab_results_YYYY-MM-DD.pdf`
2. If HLA-B27 positive + CRP/ESR elevated → rheumatology referral within 2 weeks
3. If HLA-B27 negative + normal inflammatory markers → much less likely axial spondyloarthritis
4. If HLA-B27 positive but normal inflammatory markers → ambiguous, may still warrant rheumatology consult
5. Update this tracker

## Reminder rules

- Every result should be filed within 24 hours of receipt
- Every appointment should be logged within 24 hours
- Every 60 days if nothing has moved, re-contact Bautista for the radiologist report (it is the linchpin)
- If you get any new imaging (follow-up MRI, X-ray, ultrasound), use the same convention as `MEDICAL/` — new folder per study
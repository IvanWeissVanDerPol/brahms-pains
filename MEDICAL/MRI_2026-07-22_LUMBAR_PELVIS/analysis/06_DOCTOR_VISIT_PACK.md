# Doctor Visit Pack — Lumbar + Pelvis MRI 2026-07-22 (Ivan)

> **Use this for your next in-person appointment.** Built on the validated findings in `05_HONEST_REPORT.md` — only the findings the AI was actually able to verify pixel-by-pixel. Supersedes the older drafts in `_archive_old_drafts/04_DOCTOR_VISIT_PACK.md`.

## The 1-page TL;DR

```
PATIENT: WEISS VAN DER POL, Ivan  (DOB 2000-06-17, age 26, male)
INSTITUTION: Centro Médico Bautista, Asunción
STUDY:  RMN COL LUMBAR + PELVIS OSEA
DATE:   2026-07-22 14:25
ACCESSION (CD label): 519328      MRN: 396461
EQUIPMENT: GE SIGNA Voyager 1.5T
DICOMs: 1029 files / 22 series

FINDINGS TO DISCUSS (validated pixel measurements):
  M1  Right hemipelvis T2 asymmetry (48% of axial slices; right > left; peak
      at SI joint level). HIGH confidence in measurement. Real, but uncertain
      clinical meaning. Could be normal variant, edema, muscle spasm, etc.

  M3  Bilateral scrotal fluid collections (bright on water T2, dark on fat T1).
      HIGH confidence in finding. Likely bilateral hydroceles; needs scrotal
      ultrasound with Doppler to characterize.

  M4  Lumbar disc T2 signal loss at multiple levels (L2-L3, L4-L5, L5-S1 most
      affected). MEDIUM confidence. Common finding, often asymptomatic.

  M5  Possible Modic-like endplate signal change at one lumbar level (exact
      level uncertain — auto-detection was unreliable). LOW confidence.

REQUIRES RADIOLOGIST READ (most important — missing):
  Formal written report from Centro Médico Bautista. The CD has raw DICOMs
  only. Accession 519328, study date 2026-07-22.

TESTS YOU SHOULD ASK THE DOCTOR TO ORDER:
  □ Scrotal ultrasound with Doppler (for M3)
  □ HLA-B27 (suggests axial spondyloarthritis if positive; protocol choice
    + M1 finding make this worth ruling out)
  □ CRP, ESR (general inflammatory markers)
  □ CBC (basic screen)
  □ Optional: Dedicated SI joint MRI with axial oblique slices (the coronal
    series in this study did NOT capture SI joints well)

KEY QUESTION TO ASK:
  "¿Por qué se incluyó la secuencia Dixon grasa/agua? No es rutinaria para
  RM lumbar — sugiere que el médico que pidió el estudio sospechaba algo
  específico sobre la médula ósea."
```

## What to bring

```
□ Print of analysis/05_HONEST_REPORT.md  (the primary deliverable)
□ Print of analysis/03_previews/00_KEY_FINDINGS_MONTAGE.png
   (the 4-panel summary image — clear, no red circles)
□ USB with the entire MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/ folder
   (so the doctor has the full data + my analysis scripts if curious)
□ Cedula + Bautista patient card (#396461)
□ Notepad + pen
```

## Conversation script — Spanish, in order

### Opening (30 seconds)

> "Doctor, vengo con la RM lumbar + pelvis que me hicieron el 22 de julio en Bautista. Tengo un informe de IA pre-cribado que ya me hizo, no soy radiólogo. Le pido cuatro cosas concretas, en orden."

The key word is **"concretas"** — it forces them into a checklist mode.

### The first ask — get the missing radiologist report

> "Lo más importante: el estudio no tiene informe radiológico escrito, solo los DICOMs crudos en el CD. Accession 519328, paciente 396461. ¿Puede pedir a Bautista que un radiólogo escriba el informe oficial? Es el insumo que falta para cualquier decisión clínica."

This is the single most valuable deliverable you can extract from the visit. Without it, every subsequent decision is being made on AI speculation.

### The second ask — scrotal ultrasound

> "En la RM aparecieron colecciones líquidas bilaterales en el escroto, alrededor de los testículos. La RM no es la prueba estándar para eso — necesito una ecografía escrotal con Doppler para caracterizarlas y descartar un componente sólido. ¿Me la puede indicar?"

Why this framing works:
- You say what the finding is (MRI showed bilateral fluid)
- You name the correct test (Doppler ultrasound)
- You give the clinical reason (rule out solid component)
- You don't say "I'm worried about testicular cancer" (you shouldn't be — it almost certainly isn't)

### The third ask — inflammatory workup

> "En la RM también hay una asimetría de señal T2 en el hemipelvis derecho, principalmente al nivel de la articulación sacroilíaca. No tengo un diagnóstico todavía — el radiólogo tiene que confirmar — pero dados los hallazgos y que el protocolo incluyó Dixon grasa/agua (que no es rutina), quisiera descartar inflamación sistémica. ¿Me puede indicar HLA-B27, PCR, VSG, y un hemograma?"

Why this framing works:
- You cite the **measured** finding (M1 right hemipelvis asymmetry)
- You name the protocol oddity (Dixon fat/water was ordered specifically)
- You request a sensible screening panel (HLA-B27 + inflammatory markers + CBC)
- You don't claim to know the diagnosis — you say the radiologist has to confirm

If the doctor pushes back on HLA-B27:
> "Es un test barato, no me cambia el tratamiento de inmediato, pero si es positivo me abre la puerta a rheumatología y a un manejo mucho más temprano. Si es negativo, descartamos una categoría entera de enfermedad. Vale la pena."

### The fourth ask — dedicated SI joint MRI if M1 is real

Wait for the radiologist's official report first. If the official report confirms right-sided inflammation/SI joint involvement, **then** ask:

> "El informe radiológico confirmó inflamación en la articulación sacroilíaca derecha. Esta RM no capturó bien esa articulación — el plano coronal estaba por encima. ¿Me puede indicar una RM específica de sacroilíacas con cortes axiales oblicuos perpendiculares al eje del sacro?"

This is the standard protocol when SI joint inflammation is suspected — perpendicular cuts that show the joint cartilage and subchondral bone clearly.

### If you have back pain (mention only if relevant)

> "También tengo dolor lumbar crónico [describe: location, duration, what makes it worse/better, any leg pain/numbness]. La RM muestra cambios de señal en los discos lumbares. ¿Esto justifica kinesiología y AINEs, o necesito interconsulta con traumatología/columna?"

If you have **no** back pain, omit this — don't create symptoms to justify workup.

## Email after the appointment (within 24 hours)

```
Asunto: Confirmación de indicaciones - consulta [fecha] - RM 22-07-2026

Doctor/a [nombre]:

Confirmo lo que hablamos en consulta el [fecha]:

1. Informe radiológico oficial del estudio del 22-07-2026
   - Paciente: WEISS VAN DER POL Ivan (ID 396461)
   - Modalidad: MR, RMN COL LUMBAR + PELVIS OSEA
   - Accession (CD): 519328
   - Solicitar al servicio de radiología de Bautista

2. Ecografía escrotal con Doppler
   - Motivo: colecciones líquidas escrotales bilaterales vistas en RM
   - Para caracterizar: hidrocele vs varicocele vs quiste vs otra
   - Quiero descartar componente sólido

3. Laboratorio:
   □ HLA-B27
   □ PCR (proteína C reactiva)
   □ VSG (velocidad de sedimentación globular)
   □ Hemograma completo

4. [si aplica] RM específica de sacroilíacas con cortes axiales oblicuos
   - Pendiente: solo después de tener el informe radiológico oficial

5. [si aplica] Interconsulta traumatología/columna
   - Por hallazgos lumbares en RM
   - Síntomas: [describe brevemente]

Si necesita algo más antes de emitirlas, mi WhatsApp es +595 9XX XXX XXX.

Gracias,
Ivan Weiss van der Pol
```

## Tracking sheet — bring to every appointment

Print this and update it after each visit. Forces accountability.

| Date | Action | Asked for | Got it? | Notes |
|---|---|---|---|---|
| ___/___/___ | Asked Bautista for radiologist report | Yes | □ Yes □ No □ N/A | Who I spoke to: __________ |
| ___/___/___ | Scrotal ultrasound ordered | Yes | □ Yes □ No □ N/A | Order # or center: __________ |
| ___/___/___ | Scrotal ultrasound performed | — | □ Yes □ No | Report received: □ Yes |
| ___/___/___ | HLA-B27 result | — | — | Result: ____________ |
| ___/___/___ | CRP result | — | — | Result: ____________ |
| ___/___/___ | ESR result | — | — | Result: ____________ |
| ___/___/___ | CBC result | — | — | Result: ____________ |
| ___/___/___ | Radiologist official report received | — | □ Yes □ No | Report at: 07_followup/ |
| ___/___/___ | Rheumatology referral (if needed) | Yes | □ Yes □ No | Doctor: ____________ |
| ___/___/___ | Urology referral (if needed) | Yes | □ Yes □ No | Doctor: ____________ |
| ___/___/___ | Traumatology referral (if needed) | Yes | □ Yes □ No | Doctor: ____________ |

## If the doctor dismisses you

You've been dismissed before. Three scripts in escalating order:

**Level 1 — re-route:**
> "¿Me puede derivar a urología (por el escroto) y rheumatología (por la asimetría pélvica)? Si esto no es su área, ¿a quién me recomienda?"

**Level 2 — document the dismissal:**
> "Entiendo que su lectura clínica es que no requiere acción. Le pido por favor que documente en mi historia clínica: (a) los hallazgos de la RM que le describí, y (b) su decisión de no indicar los estudios que solicito."

**Level 3 — Ley 6534/2020 (right to full medical record):**
> "Voy a ejercer mi derecho de acceso a mi historia clínica completa, incluyendo el informe radiológico, el detalle de la consulta de hoy, y sus indicaciones. ¿Me puede dar el procedimiento?"

Under Paraguay's patient rights framework you can request the full record. Use it if you need to escalate or switch doctors.

## What NOT to do

- ❌ Don't bring the annotated images (red circles in wrong places) — keep them for reference, don't show the doctor
- ❌ Don't claim a specific diagnosis (Modic 1, hemangioma, sacroiliitis) — the AI is uncertain about all of these
- ❌ Don't skip the scrotal ultrasound just because the AI thinks it's likely benign — "likely benign" still needs the standard workup
- ❌ Don't accept "the MRI is fine, nothing to do" without seeing the radiologist's written report
- ❌ Don't share the DICOMs with anyone who isn't bound by medical privacy — they have your full name and DOB
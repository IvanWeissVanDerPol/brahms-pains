# Chat 11 — Gabriella González Pane (WA export)

Source: `WhatsApp Chat with Gabriella González Pane (1)/` official WhatsApp text export
(2026‑07‑23), plus co‑located `PTT-*.opus` voice notes and `DOC-*` documents.
Extracted with `scripts/extract_wa_txt_export.py`, then post‑processed with
`scripts/scrub_and_fix_wa_export.py` (media path routing, third‑party PII exclusion,
attachment‑stub recovery, PHI exclusion, JWT scrub).

Tier: `tier1_deep` — the primary business + relationship channel of this window.

---

## 1. Window & volume

| | |
|---|---|
| First message | 2026‑05‑31 21:58 UTC (18:58 Paraguay) |
| Last message  | 2026‑07‑23 18:18 UTC (15:18 Paraguay) |
| Span          | ~52.85 days |
| Messages      | 5,985 |
| Rate          | ~113 msg/day average |

## 2. Type mix

| type | count | notes |
|---|---:|---|
| 0 text     | 4,495 | ~75% of the stream |
| 1 image    |   308 | metadata‑only, `recorded_only=True` (policy: no images) |
| 2 audio    | 1,114 | 1,112 PTT voice notes + 2 AUD files, ~142 MB, all kept |
| 3 video    |    54 | metadata‑only, `recorded_only=True` (policy: no videos) |
| 7 doc      |    14 | 5 kept, 8 vcf excluded (PII), 1 pdf excluded (PHI) |

## 3. Sender balance

Overall roughly even: Ivan 2,878 (48.1%) / Gaby 3,107 (51.9%).

Split by modality it inverts:

- **Text only** — Ivan 2,310 vs Gaby 2,185 → Ivan writes slightly more.
- **Voice notes** — Ivan 318 vs Gaby 796 → Gaby sends ~2.5× more audio.

Ivan's channel is text‑heavy (structured messages, transcripts, planning docs);
Gaby's is voice‑heavy (thinking out loud, day‑to‑day, reactions).
Any downstream analysis that ignores audio will systematically under‑weight her voice.

## 4. Temporal pattern

Day of week (all messages):

| day | msgs |
|---|---:|
| Mon | 1,382 |
| Fri | 1,184 |
| Tue |   960 |
| Thu |   863 |
| Wed |   679 |
| Sat |   598 |
| Sun |   319 |

Weekday workweek pattern with a Monday spike. Sunday is the low.

Hour of day (Paraguay local, UTC‑3):

| hour | msgs |
|---|---:|
| 14 | 873 |
| 15 | 754 |
| 17 | 710 |
| 16 | 614 |
| 12 | 488 |
| 13 | 419 |

The relationship happens ~12:00–17:00 local, afternoon‑heavy.

## 5. Text length

p50 = 26 chars, p90 = 89, p99 = 263, max = 37,529.

The tail is Ivan's structured outputs:

- **id=1308** (37,529 chars, 2026‑06‑24) — `ROLE‑PLAY GEMINI VOICE — Reunión Gaby vs Roque`.
  Director‑of‑scene script for Gaby to practice her meeting with Roque, with
  "Kiki" cast as emotional support. Written for Gemini voice mode.
- **id=1338 / id=1340** (~20 k each, 2026‑06‑28/29) — verbatim transcripts of
  audio Ivan sent about the Tigo chip / WhatsApp Business setup and the
  "Flo, tu Master To‑Do" audio (AI cuestionarios, audio‑friendly UX).

These are the load‑bearing artifacts; treat them as documents, not chat.

## 6. Business arc — what this channel is actually doing

The dominant thread is a **branding + strategic‑repositioning project for Dra.
Gaby's dental practice** (13 years, Asismed patient base, considering leaving the
current arrangement with Roque). Ivan is running the strategy work; the chat is
the working surface.

Timeline landmarks (message ids):

| id | date | moment |
|---:|---|---|
|    7 | 2026‑06‑01 | "sigo en gpt… me está haciendo un dossier" — origin of the strategy work |
|   35 | 2026‑06‑01 | `DOSSIER ESTRATÉGICO PROFESIONAL` posted in‑chat |
|   42 | 2026‑06‑01 | `Dossier_Estrategico_Extendido_Gabriella_Gonzalez_Pane.docx` shared |
|   91 | 2026‑06‑01 | "Dra. GP — Resumen de todo el trabajo que hicimos" (long consolidation) |
|   94 | 2026‑06‑01 | Roque scenario first named: "es posible que roque me ofrezca merced…" |
|  194 | 2026‑06‑02 | Points at `github.com/Ai-Whisperers/dentist` for negotiation pro‑tips |
|  576 | 2026‑06‑12 | 9 Luque office options triaged |
|  615 | 2026‑06‑?? | `validacion-cliente-dra-gp.md` shared |
|  708 | 2026‑06‑17 | Question set prepared for Roque conversation |
|  854 | 2026‑06‑?? | `Prompt_Estrategia_Reunion_Roque.pdf` shared |
| 1281 | 2026‑06‑23 | "mañana es mi reunion tkk" — meeting eve |
| 1308 | 2026‑06‑24 | Gemini voice role‑play script for the Roque meeting |
| 1332 | 2026‑06‑28 | `ADN_Profesional_Dra_Gabriela_Gonzalez_Pane_EXTENDIDO.pdf` |
| 1336 | 2026‑06‑28 | `DOC-20260628-WA0034.txt` |
| 1337 | 2026‑06‑29 | Hostinger UI transcript — building `ometzdental.com` |
| 1588 | 2026‑07‑02 | `https://ometzdental.com/en` live — "si queres ir presentando esta pag" |
| 1754 | 2026‑07‑03 | "Hola Gaby. Mirá, así arranca Ometz Dental – solo lo que necesitás hacer vos" |

By the end of the window the working name **Ometz Dental** has a live site and
handover instructions; the Roque conversation has happened; ADN Profesional has a
formal extended document. That's the shape of the project this chat records.

## 7. Kept documents (on‑disk, in `media/docs/`)

- `Dossier_Estrategico_Extendido_Gabriella_Gonzalez_Pane.docx`
- `validacion-cliente-dra-gp.md`
- `Prompt_Estrategia_Reunion_Roque.pdf`
- `ADN_Profesional_Dra_Gabriela_Gonzalez_Pane_EXTENDIDO.pdf`
- `DOC-20260628-WA0034.txt`

## 8. Exclusions (recorded only, no file on disk)

Policy: images and videos are metadata‑only; third‑party contact cards (`.vcf`)
are PII; one PDF is PHI. Every exclusion carries `recorded_only: True` +
`exclusion_reason` so downstream tooling never re‑surfaces the content.

- **308 images** — `"images excluded per policy"`
- **54 videos**  — `"videos excluded per policy"`
- **8 vcf files** — `"third-party contact PII"`
  (ids: 496, 630, 2160, 2451, 2792, 3052, 3240, 3611)
- **1 pdf** — id=5745 `DOC-20260722-WA0048.pdf`,
  `"PHI: personal blood-lab results, not committed"` (Ivan's own labs;
  not copied into the repo)
- **1 JWT** — id=5747, `token=eyJ…` replaced with `token=<REDACTED_JWT>`

Sensitive third parties named in‑chat (Laura, Cookie, Defi, Thais, Sarah,
Nicolas, Dan, Alex, Dayah, Lara, Magali, Ara, Jonatan, Lourdes/Youko/Kurama)
appear only in message text; they are not surfaced in this document beyond this
policy line, and they are not first‑class subjects of any downstream analysis.

## 9. On‑disk layout

```
11__gabriella_gp___wa_export_2026/
├── messages.json          # 5,985 messages, scrubbed, atomic-write
├── ANALYSIS.md            # this file
├── source/                # original .txt export (kept for provenance)
└── media/
    ├── audio/             # 1,114 files (~142 MB, .opus PTT + 2 .m4a AUD)
    ├── docs/              # 5 kept documents (see §7)
    ├── images/            # (empty — recorded_only)
    └── videos/            # (empty — recorded_only)
```

`messages.json` is authoritative. The extractor and scrub script together are
idempotent — re‑running them on the same input produces the same file byte for
byte, so downstream jobs can rely on hashes.

## 10. Integration notes for the `psycology` repo

- This is the first WA chat in `tier1_deep` sourced from an **official text
  export** rather than the SQLite `msgstore`. `chat_id = synth_chat_id(basename)`
  → negative int, guaranteed disjoint from the SQLite positive `_id` space.
  Cross‑chat joins should key on `slug`, not `chat_id`.
- `sender_jid` for text exports is the raw display name from the header, not a
  phone JID. Any code that expects `@s.whatsapp.net` needs a guard.
- `from_me` here is derived from `--self weissvanderpol`, matched
  case‑insensitively against the display name in the export header.
- Timestamps in the export are Paraguay local (UTC‑3, fixed, no DST); the
  extractor stores UTC ms in `ts_ms` and ISO‑8601 UTC in `ts_iso`. Any
  human‑hour analysis (like §4) must re‑apply UTC‑3.
- **Whisper backfill** for the 1,114 audios is pending (see repo backlog); once
  transcripts land, they attach at the `messages[i].media.transcript` key —
  none written yet in this file.
- `image` and `video` entries are structurally present so message ordering and
  reply threading are preserved; only the file bytes are absent.

## 11. What this chat is not

- Not a therapy record. Do not treat it as clinical material.
- Not a full picture of the relationship — only 2026‑05‑31 through 2026‑07‑23.
  Prior context lives (partially) in the SQLite `msgstore` extractions under
  `tier1_deep`/`tier2_core`.
- Not the sole source for the Ometz Dental / ADN Profesional project — the
  authoritative docs live in the `dentist` repo referenced at id=194.

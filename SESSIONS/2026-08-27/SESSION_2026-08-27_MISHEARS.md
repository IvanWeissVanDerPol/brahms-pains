# WhisperX Mishear Catalogue — 08-27-2026_20.31_spa.json

**Purpose:** Catalogue of confirmed WhisperX hallucinations from this session. Use as a reference for the voice-note pipeline.
**Source:** `raw.json` (1,201 segments, 7,277s, language `spa`)
**Whisper model:** large-v3 (presumed; same pipeline as other psycology voice notes)
**Diarization:** pyannote-audio (8 speaker labels: 0-7; 7 = noise)

---

## 🔤 Type 1 — Name hallucinations (proper noun mishears)

Whisper frequently mishears Spanish phonology as English-sounding proper nouns. Pattern is **/Spanish-syllable-cluster/ → /English-name/**.

| Heard | Likely correct | Count | Confidence | Note |
|---|---|---:|---|---|
| **Evan** | **Iván** | **6×** | ✅ Certain | "Evan estaba yéndose mucho al hospital" = "Iván estaba yéndose mucho al hospital" |
| **Gusy** | **"como un huevón ahí"** | 1× | ✅ Confirmed | Paraguayan slang. Whisper heard "Gusy" as a name. **Does not exist as a person.** |
| **Juki / Kuki** | Kiki | 16× | ✅ Both spellings used | "Kiki" / "Juki" — Whisper alternates. **Real name.** |
| **Lúa** | Lua | 9× | ✅ Accent variant | Spanish accent on the u. **Real person, multiple Luas.** |

---

## 🔡 Type 2 — Number-substituted common words

Whisper sometimes encodes words as numbers, probably from phoneme-to-token confusion in the language model head.

| Heard | Likely correct | Count | Confidence |
|---|---|---:|---|
| **ent11s** | **entonces** | 12× | ✅ Certain |
| **ha100do** | **haciendo** | 3× | ✅ Certain |
| **di100do** | **diciendo** | 2× | ✅ Certain |
| **cons10te** | **constante** | 1× | ✅ Certain |
| **diafonía** | **disonancia / cross-talk** | 1× | 🟡 70% |
| **taboga** | **tabique / wall?** | 1× | 🟡 50% |

---

## 🗣️ Type 3 — Spanish slang misheard as English

Whisper maps Paraguayan/Rioplatense slang phonology onto English words.

| Heard | Likely correct | Count | Confidence | Note |
|---|---|---:|---|---|
| **gotísimo** | **"ni gota" / "gotas"** | 1× | ✅ Certain | "gotísimo" = "not even a drop" |
| **alcoholé** | **alcohólico** | 1× | ✅ Certain | Self-reference by Kiki |
| **la verga** | **la verga** | 1× | ✅ Correct | Kept as-is (regional expletive) |
| **re XD** | **"re"** (intensifier) + laughter marker | 1× | ✅ Certain | Whisper added "XD" from laughter audio |
| **rapist** | (false hallucination) | 0× | ❌ Not in this transcript | Confirmed absent |
| **guacho/a** | **huevón / guasón** | varies | ✅ Certain | Common Paraguayan slang |

---

## 🔢 Type 4 — Number hallucinations

Whisper occasionally generates numbers that aren't in the audio.

| Heard | Likely correct | Count | Confidence |
|---|---|---:|---|
| **ochenta llamadas** | 80 calls | 1× | ✅ Confirmed by Ale's enumeration |
| **sesenta / veinte** | follow-up counts (rapid speech) | 1× each | ✅ Ale was enumerating |
| **45 llamadas** | 45 calls | 1× | 🟡 Lourdes may have rounded; actual count was 80+ |
| **22 milímetros** | 22 mm | 1× | ✅ Medical fact (IUD size) |

---

## � Type 5 — Place names

| Heard | Likely correct | Confidence |
|---|---|---|
| **Biggie** | **Biggie** (supermarket chain in Paraguay) | ✅ Real |
| **Miami** | **Miami** | ✅ Real (where Iván had MRI consultation) |
| **Uniqlo** | **Uniqlo** (clothing brand) | ✅ Real |
| **Dubái** | **Dubái** (where Lourdes traveled) | ✅ Real |
| **IMADES** | **IMADES** (animal welfare authority, Paraguay) | ✅ Real |

---

## 🧬 Type 6 — Clinical / technical terms

| Heard | Likely correct | Confidence |
|---|---|---|
| **TLP** | **TLP (Trastorno Límite de la Personalidad)** | ✅ Confirmed (BPD) |
| **MRI scan** | **MRI** (medical) | ✅ Confirmed |
| **tramadol** | **tramadol** | ✅ Confirmed (medication) |
| **Quiste** | **quiste** (cyst) | ✅ Confirmed |
| **pólipos** | **polyps** | ✅ Confirmed |
| **antibióticos** | **antibiotics** | ✅ Confirmed |
| **autismo** | **autism** | ✅ Confirmed |
| **Aldea SOS** | **Aldea SOS** (SOS Children's Villages) | ✅ Real org |
| **riñón** | **kidney** | ✅ Confirmed |

---

## 📝 Type 7 — Phonetic spelling / pronunciation

Whisper outputs phonetic spelling when uncertain.

| Heard | Likely correct | Confidence |
|---|---|---|
| **póli-poli / poliquilo** | **polycule** | ✅ Certain (Ale spells it C-O-L-E, P-O-L-Y) |
| **BDSM** | **BDSM** | ✅ Real (community context) |
| **shota** | **shota** (anime slang for younger-coded character) | ✅ Lourdes uses it |
| **taboga** | **tabique** (wall/partition) | 🟡 Unclear |
| **Cumple** | **cumpleaños** (birthday party) | ✅ Certain |

---

## 🌀 Type 8 — Background noise / cross-talk

| Heard | Likely correct | Count |
|---|---|---:|
| **[tos]** | cough | many |
| **[risas]** | laughter | many |
| **[ruido de micrófono]** | microphone noise | several |
| **[ruido de objeto arrastrándose]** | object dragging | 1 |
| **[diafonía]** | cross-talk | 1 |
| **[carraspeo]** | throat-clearing | 2 |
| **[comunicación cruzada]** | cross-talk | 1 |
| **[golpe]** | thud / hit | 1 |
| **[sorbe]** | sniff | 2 |
| **[silbido]** | whistle | 0 |
| **[gruñido]** | grunt | 1 |

---

## 🤖 Type 9 — WhisperX-specific artifacts

| Artifact | Count | Note |
|---|---:|---|
| **Speaker 7 = noise** | 1 segment, 4 tokens | Default diarization label for ambient sound |
| **Speaker split (S2 + S6 for Iván)** | 21 segs | WhisperX split Iván during a 365.9s silence gap (1474–1840s) when his vocal characteristics changed |
| **Speaker split (S3 + S4 for Gaby)** | 28 segs | Similar pattern: Gaby's voice re-entered as S3 fragment before main S4 |
| **Empty segments** | 0 | None — WhisperX skipped silent regions cleanly |
| **Hallucinated English** | 0 in this transcript | Whisper stayed in Spanish; this is unusually clean |

---

## 📐 Pipeline-level recommendations

Based on this transcript:

1. **Always replace Evan → Iván** in post-processing (6× confirmed, expect this in every voice note where the speaker is you)
2. **Replace ent11s → entonces** (12× — likely a Whisper model bug)
3. **Replace ha100do → haciendo** (3× — same root cause as ent11s)
4. **Replace di100do → diciendo** (2× — same)
5. **Add Kiki / Juki both as valid spellings** for the same person
6. **Lua / Lúa both valid** (accent variation)
7. **Don't auto-replace "Gusy"** — confirm context first. In this transcript it was slang ("como un huevón ahí"), but it could be a real nickname elsewhere
8. **Preserve Spanish slang** (la verga, boludo, huevón, alcoholé) — don't translate
9. **TLP / BPD** appears as both acronym (TLP) and full name (Trastorno Límite de la Personalidad) — keep both
10. **WhisperX diarization splits during long silences** — expect ~30% of unique speakers to be split into 2 IDs

---

*File: `SESSION_2026-08-27_MISHEARS.md`*
*Generated from `raw.json` (1,201 segments, 7,277s)*
*Local path: `/opt/data/scratchpad/chat-analysis-08-27/`*
*Use case: Reference for psycology repo's voice-note post-processing pipeline*

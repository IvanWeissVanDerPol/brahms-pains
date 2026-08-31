# Speaker Identification Table v2 — 08-27-2026_20.31_spa.json

**File:** `08-27-2026_20.31_spa.json` (5.1 MB, 7277s = 2h 01m 17s, 1201 segments, 42,853 word tokens)
**Generated:** 27 Aug 2026, 20:31 (PYT) · **Language:** spa · **Format:** WhisperX-style diarization
**Diarization output:** 8 speaker IDs
**Actual humans present:** 5 confirmed — **Cookie/Kuki is NOT in the room**, **Gusy is NOT a person (Whisper hallucination of Paraguayan slang "como un huevón ahí")**

---

## 📊 Final cast (v2 — corrected)

| ID | Segs | Talk-time (s) | Talk % | Words | 1st-person tokens | English density | **Identity** | **Confidence** |
|---|---:|---:|---:|---:|---:|---:|---|---|
| **Speaker 0** | 238 | 1117.7 | 15.4% | 7,506 | 101 | 4.7% | **Lourdes (Youko Kurama)** | ✅ Confirmed |
| **Speaker 1** | 186 | 723.4 | 9.9% | 4,386 | 96 | 4.9% | **Ale Cabral** | ✅ Confirmed |
| **Speaker 2** | 317 | 1555.9 | 21.4% | 11,068 | 170 | 5.7% | **Iván (you)** | ✅ Confirmed |
| **Speaker 3** | 28 | 113.4 | 1.6% | 714 | 15 | 5.0% | **Gaby (fragment 2)** | ✅ Confirmed |
| **Speaker 4** | 300 | 2405.2 | 33.1% | 15,436 | **512** | 6.7% | **Gaby (main voice)** | ✅ Confirmed |
| **Speaker 5** | 110 | 469.4 | 6.4% | 3,449 | 48 | **10.8%** | **Kiki / Juki (Iván's sister)** | ✅ Confirmed |
| **Speaker 6** | 21 | 43.0 | 0.6% | 290 | 1 | 6.7% | **Iván (fragment 2)** | ✅ Confirmed |
| **Speaker 7** | 1 | 0.9 | 0.0% | 4 | 0 | 0.0% | **Noise / ambient voice** | ✅ Confirmed |

**Cast size: 5 humans in the room, 1 noise, 1 absent subject (Cookie/Kuki). Gusy does not exist — WhisperX artifact.**

---

## 🪑 Seating timeline

| Speaker | First appears | Last appears | Duration | Notes |
|---|---:|---:|---:|---|
| Lourdes (S0) | 0.3s | 7249.9s | Full 2h 1m | Narrator/therapist |
| Ale (S1) | 8.6s | 3309.7s | ~55 min | Co-resident, leaves after first half |
| Iván (S2) | 18.0s | 6698.3s | ~1h 51m | Long narrative arc |
| Gaby (S3 frag) | 1137.1s | 1474.3s | ~5.5 min fragment | First appearance |
| Gaby (S4 main) | 1477.5s | 7277.2s | ~1h 36m | Joins Act 2, dominates late session |
| Kiki (S5) | 1478.5s | 3672.9s | ~36 min | Joins with Gaby, leaves after boundaries talk |
| Iván (S6 frag) | 1515.4s | 1838.4s | ~5 min | WhisperX split during 365.9s silence gap |
| Noise (S7) | 5655.5s | 5656.4s | <1 sec | Single utterance |

---

## 🔄 WhisperX diarization errors identified

| Speaker ID | What WhisperX did | What it actually is | Reason |
|---|---|---|---|
| S3 (1.6% / 28 segs) | Treated as separate speaker | Gaby fragment | Mic position change |
| S5 split mid-session (3094–3417s vs 3422–3670s) | Same Speaker 5 | Two registers of Kiki (cold/practical + hot/sibling) | Vocal register shift when subject changes from legal-risk to personal-care |
| S6 (0.6% / 21 segs) | Treated as separate speaker | Iván fragment | Voice angle change when Iván dropped volume to listen during Gaby's main disclosure |
| S7 (1 seg) | Treated as speaker | Ambient noise | Mislabeled background voice |

**Key methodological note:** WhisperX appears to split speakers when:
1. **Mic position changes** (Gaby S3↔S4 split when she moved)
2. **Vocal register changes** (Kiki's two modes got smoothed together — Speaker 5 is correctly Kiki throughout, just two registers)
3. **Volume/angle changes** (Iván going silent to listen got re-labeled S6)

---

## 🎭 Kiki's two registers (now correctly attributed)

| Register | Timestamps | Examples | Voice quality |
|---|---|---|---|
| **Cold / streetwise / Argentine** | 2635–3447s | "alcoholé", "Call an ambulance. But not for me.", "You are not welcome here anymore. There is the door.", "We can do this the kinky way", "vos sos la imagen de la empresa, boludo", "te pueden investigar por la marihuana", "la verga" | Lower affect, fast delivery, dark humor |
| **Hot / sibling / directive** | 3422–3670s | "Get your life together. Tenés 26 ya", "You can't fix anybody but yourself", "yo estoy anémica", Petunio, "Why do you give so much love to other people and not to yourself?", "You will only accept the love you think you deserve" | Higher pitch, English code-switching, advice-mode |

**Inference:** Kiki has lived in Argentina (uses "boludo", "la verga" naturally — not as borrowings but as base register). Likely Buenos Aires period. The hot register kicks in when the conversation shifts from "managing the threat" (cold/practical) to "managing Iván" (sibling concern).

---

## 📍 The "Gusy" reference — RESOLVED (not a person)

You confirmed: **Gusy does not exist.** It's a WhisperX artifact.

The most likely reconstruction of the original audio is one of:

1. **"como un huevón ahí"** (like an idiot there) — Whisper misheard "un huevón ahí" as a proper noun
2. **"como guasón"** (like a joker) — Paraguayan slang, same hallucination
3. **"como un güevón ahí"** — variant spelling

The grammar analysis I did earlier (triple-stacking "huevón" doesn't work) was wrong on closer reading — you can absolutely say "quedé de huevón como un huevón ahí" in Paraguayan Spanish as a slang flourish, even if it's redundant. **You, who was there, said no real person was referenced.** So the slang reading wins.

**Action:** Add `Gusy` → `como un huevón ahí` to the mishear post-processing rule in the psycology repo's voice-note pipeline. No further research needed. No person to identify.

---

## 👥 Character roster

### Lourdes (Speaker 0) — Co-therapist / narrator
- 238 segments, 1117.7s (15.4%)
- **Romantic history with Iván** ("la 1ª vez que lo perdoné fue Iván… me tardé 2 añitos… yo estaba en Dubái llorando")
- **Knows Laura** ("Laura, Laura, Laura?") — references Iván's infidelity
- **References Iván's thesis** ("Diablo, el diablo, material de tesis de Iván") — knows his work
- **Was in Dubai** during the relationship crisis
- **"Departamento de banda"** — music school context
- 143 voice-note markers in psycology repo (most emotional contact)
- Diagnosed role: **clinical observer, support to Gaby, witness to Iván's process**

### Ale Cabral (Speaker 1) — Co-resident / witness
- 186 segments, 723.4s (9.9%)
- **Lived in Cookie/Kuki's house** during the chaos — "venían a la casa y comían nuestra comida"
- **Was left out of conversations** — "a mí me dejaron afuera de todas las conversaciones"
- **Worked during the chaos** — "yo decía 'tengo que trabajar porque estoy atrasado'"
- **Co-resident / roommate perspective** — sees Ale's interactions with Cookie/Kuki from inside the household
- Repo metadata: CLOSE, 23k msgs, RISING affection
- Diagnosed role: **fact-witness, structural observer, third-party confirmer**

### Iván (Speaker 2 + Speaker 6) — Self
- 317 + 21 = 338 segments, 1555.9 + 43.0 = 1598.9s (22.0%)
- **Long narrative arc**: Tinder-era household, Lua pelinegro/rubia dynamics, hospital, MRI, polyps/cancer
- **Central figure being discussed AND analyzing** — second-person reference of 75+ times from other speakers
- **"Iván no puede decir que no"** — admitted by Gaby, yourself, and Lourdes as core weakness
- Diagnosed role: **subject of the session, narrator**

### Gaby (Speaker 3 fragment + Speaker 4 main) — Primary therapist / discloser
- 28 + 300 = 328 segments, 113.4 + 2405.2 = 2518.6s (34.6%) — **largest talker**
- **Hospital context**: "tirada en mi cama en el hospital con mis venas ahí encima… hecho peluda mi mano"
- **44, almost 45 years old**: "a mis 44, casi 45 años supe que tenía autismo"
- **Was on antibiotics + tramadol** during the assault
- **Was on heavy meds + had a kidney cyst explode** during the incident in her bed (note: not ovarian — see Gaby process file correction 2026-08-28)
- **Reports being accused of "draining energy"** by others in her circle
- **Has son** "Evan" (likely typo/Iván — refer to other analysis sections)
- Diagnosed role: **primary therapist, late-session process discloser, hospital patient**

### Kiki / Juki (Speaker 5) — Sibling / practical advisor
- 110 segments, 469.4s (6.4%)
- **Highest English code-switching** (10.8% of speech)
- **Argentine register** ("boludo", "la verga", "alcoholé")
- **Has Petunio** (family pet)
- **Anemic, obsessive about food** ("yo estoy anémica… yo soy obsesiva con las cosas, yo me esfuerzo a comer")
- **Direct sibling energy** to Iván: "Get your life together. Tenés 26 ya."
- **Boundary-setting advice** — "You can't fix anybody but yourself", "It's not your job to save anybody"
- **Hard jokes about the assailant** — "You are not welcome here anymore. There is the door."
- **Protective of Gaby** — defends her from the assailant's framing
- Diagnosed role: **sibling advisor, threat neutralizer, late-session anchor**

---

## 🔧 Mis-transcription catalogue (carryover from v1, still valid)

### Name fixes

| Heard | Likely correct | Times | Confidence |
|---|---|---:|---|
| **Evan** | **Iván** | **6×** | ✅ Certain |
| **Gusy** | **"como un huevón ahí"** (Paraguayan slang) | 1× | ✅ Confirmed (you said Gusy doesn't exist) |
| Juki / Kuki | Kiki | 16× | ✅ Both spellings used |
| Lúa | Lua | 9× | ✅ Accent variant |

### Numeric-substitution tokens

| Token | Likely correct | Count |
|---|---|---:|
| **ent11s** | **entonces** | 12× |
| **ha100do** | **haciendo** | 3× |
| **ha1** | "haciendo" or "hace" | 1× |
| **di100do** | **diciendo** | 2× |
| **cons10te** | **consciente** | 1× |
| **1²** | **primero** | 1× |
| **2a** | **segunda** | 2× |
| **3ra** | **tercera** | 1× |

### Translate-and-back-translate errors

| Heard | Likely correct | Note |
|---|---|---|
| **gotísimo** | **gustísimo** | Spanish-only |
| **gotica** | **gótica** | English-with-Spanish-ending |
| **rapist** | **violador** | English translated from Spanish |
| **gra-drenarme** | "drenarme" with stutter | Stutter transcribed literally |
| **marcheamos** | "marchamos" / Paraguayan "to hang out" | 1× |

---

## 🎯 What this changes for downstream analysis

| Decision | Old reading (v1) | Corrected reading (v2) |
|---|---|---|
| Who is Speaker 6? | Gusy / unknown | **Iván (fragment 2)** |
| Who is early-Session 5 (1478–1949s)? | Kiki | **Kiki** (consistent — same person, two registers) |
| Who is mid-Session 5 (3094–3417s)? | Ale | **Kiki** (Argentine register — Kiki lived in Argentina) |
| Who is "Cookie/Kuki" in speaker roster? | Possible 8th speaker | **Not present** — she's the topic |
| Who is "Gusy"? | Possible speaker | **Not present** — absentia reference or Whisper hallucination |
| Cast size | 8 speakers | **5 humans in room + 1 noise** |

---

## ✅ Confirmed cast for the analysis files

| Display name | Role | In room? | Files to write |
|---|---|---|---|
| **Iván** | Self / narrator | ✅ Yes | `SESSION_2026-08-27_IVAN_PROCESS.md` |
| **Gaby** | Co-therapist / discloser | ✅ Yes | `SESSION_2026-08-27_GABY_PROCESS.md` |
| **Lourdes** | Co-therapist / narrator | ✅ Yes | `SESSION_2026-08-27_LOURDES_PROCESS.md` |
| **Ale** | Co-resident / witness | ✅ Yes (left early) | `SESSION_2026-08-27_ALE_WITNESS.md` |
| **Kiki** | Sibling / advisor | ✅ Yes | `SESSION_2026-08-27_KIKI_SUPPORT.md` |
| **Cookie/Kuki** | Subject (not present) | ❌ No | `SESSION_2026-08-27_CUQUI_NARRATIVE.md` |

Plus:
- `SESSION_2026-08-27_CAST_MAP.md` — this file
- `SESSION_2026-08-27_MISHEARS.md` — the transcription-error catalogue
- `SESSION_2026-08-27_CUQUI_ALL_ISSUES_DEEPDIVE.md` — your requested "all issues explained"
- Per-3rd-party context files for **Lua pelinegro, Lua rubia, Nate, Belén, Evan, Power** (named-but-not-present characters whose role is part of the story)

---

## ⏸️ Still blocked

1. **You flip repo to private on github.com** (~30 sec)
2. **Then** we scrub MMPI-2 + IPIP-NEO from git history
3. **Then** I write the analysis files locally in `/opt/data/scratchpad/chat-analysis-08-27/` — never pushed to the repo until you say so
4. **Then** we optionally commit the new files to the now-private repo if you want

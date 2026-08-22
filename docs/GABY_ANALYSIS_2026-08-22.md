# Gaby (Dra. Gabriella González Pane) — Export Analysis

> **Generated:** 2026-08-22
> **Source:** `SOURCE_OF_TRUTH/wa_messages/tier1_deep/11__gabriella_gp___wa_export_2026/messages.json`
> **Script:** `scripts/analyze_gaby_export.py` → `_ANALYSIS/gaby_relationship_analysis.json`
> **Window:** 2026-05-31 → 2026-07-23 (53 days, 41 active), 5,985 messages
> **Feeds hats:** 1 (Clinical), 4 (Family/Attachment), 21 (Sexologist), 31 (Grief)

---

## 0. Headline correction — the initiator metric is wrong repo-wide

`RELATIONSHIPS/dynamics/GABRIELLA_GP.md` recorded:

> Ivan initiator ratio **48.1% — Balanced**

That figure is the **message share**, not initiation. Measured properly:

| Measure | Ivan | Gaby |
|---|---:|---:|
| Opens the day (first message) | 12 / 41 — **29.3%** | **29 / 41 — 70.7%** |
| Closes the day (last message) | 13 / 41 | 28 / 41 |
| Breaks a silence >12h | 5 / 24 — **20.8%** | **19 / 24 — 79.2%** |
| Message share (the old metric) | 48.1% | 51.9% |

Ivan is the **pursued** party here, not a balanced participant.

**This is not a Gaby-specific error.** `scripts/analyze_initiators.py` derives its
"initiator ratio" from message share across all 951 chats, so every contact whose
message counts are near-even is currently mislabelled "Balanced" regardless of who
actually reaches out. The README's bimodality thesis ("Ivan pursues OR is pursued,
no middle") is *supported* by the corrected numbers while being contradicted by the
per-contact files it generated. Re-running initiation properly across the corpus is
the highest-leverage open item — see §7.

---

## 1. The business was the door, not the room

Business vocabulary as a share of text messages, against weekly volume:

| Week | Messages | Business % |
|---|---:|---:|
| 06-01 | 459 | 9.6% |
| 06-08 | 84 | 13.1% |
| 06-15 | 488 | 3.3% |
| 06-29 | 633 | 1.0% |
| **07-13** | **1,979** | **0.5%** |
| 07-20 | 796 | 1.2% |

Volume rose ~44× while the Ometz Dental project fell to half a percent of traffic.
The clinic launch — the engagement's original purpose, and Gaby's stated stressor in
every distress message — became the least-discussed topic in the channel at exactly
the point she was most overwhelmed by it.

## 2. Symmetry that hides three asymmetries

Message counts are near-even (48/52). Every axis underneath is lopsided.

**Channel.** Ivan wrote 40,863 text words to Gaby's 16,337 (2.5×). Gaby sent 796
voice notes to Ivan's 318 (2.5×). Roughly equal expression, opposite modalities.
Ivan's longest "messages" are artifacts, not speech: a 37,529-char role-play script
(id 1308) and two ~20k-char AI transcripts (ids 1338, 1340).

**Pursuit.** See §0.

**Availability.** Both reply at a median of 1.0 minute; 71% (Gaby) and 78% (Ivan)
of replies land inside two minutes. Mutual constant availability is not in question —
only what the replies contain.

## 3. Emotional load, and its trajectory

Per 1,000 text messages from that sender, whole window and first→second half:

| Marker | Ivan | Gaby | Ivan drift | Gaby drift |
|---|---:|---:|---|---|
| Distress | 6.5 | **26.5** | 9.8 → 2.8 | 22.3 → **30.1** |
| Affection | 20.8 | **42.1** | 21.3 → 20.2 | 21.3 → **59.3** |
| Boundary-setting | 2.6 | **13.3** | 4.1 → 0.9 | 7.1 → **18.4** |
| Care offered | 1.7 | 0.0 | 2.5 → **0.9** | — |
| Sexual | **14.7** | 7.3 | 13.9 → 15.6 | 7.1 → 7.5 |

Gaby escalates on every emotional axis. Ivan's explicit comforting language halves.

**Naming asymmetry:** Gaby uses "kido" 56 times and mother-framing ("madre",
"mommy") 31 times. Ivan uses "kido" **zero** times. She names the relationship; the
frame is never returned.

## 4. The boundary, and why it repeats

2026-07-18 01:55, after Ivan proposes the relationship could "slowly pasa a vínculo
horny" (id 4989) and jokes about a strap-on (id 4991):

> **id 4992** — *"noooo espera… pregunto porque en mi vida voy a ser eso de vínculos..
> solo cuddles… hugs.. besitos.. mimitos.. compartir hs de charla… yo no te quiero
> conocer mejor como un vínculo… sos mi kido"*

Followed, unprompted, by the reason:

> **id 4995** — *"ya no quiero que me lastimen … ya pase mucho"*
> **id 4996** — *"por eso me pego a vos. porque para mí sos el chico que llegó a
> enseñarme que no sea más tonta"*
> **id 5010** — *"confío mucho en vos no se porque… por eso me animo a mostrarte cosas
> mías.. que nunca lo hice… jamás"*

This is a **trust declaration with a boundary attached**, not a rejection: be the
safe person, teach me, do not convert this into a vínculo. Her boundary language
subsequently *doubles* (7.1 → 18.4 per 1k), which is the signature of a boundary that
was stated and not received. Note also that both this exchange and most intimacy
negotiation occur in the 01:00–03:00 cluster, with Gaby stating she is "muyy high"
(ids 4993, 5012).

## 5. Attunement failure, timestamped (2026-07-23)

```
14:19  GABY  mi cabeza no para
14:19  IVAN  Que área te preocupa? / Para verle de ayudarte con Hermes
14:56  GABY  slashh NO entendes las putas indirectas
15:01  IVAN  Ponete el strap
15:02  GABY  nose como se hace.. yo solo quiero que me abraces.
             no me siento bien de verdad
15:02  IVAN  Sabes ya que los tipos tampoco saben usar jsjsjsjs
15:02  IVAN  Ultra instinct y práctica nomás es
15:08  IVAN  It's ok llorar uwuwuw                     <- lands, one line
15:11  IVAN  Lua y Nico estarían re happy de conocerte más y ser amis
15:14  GABY  que puaaa que sos boludo o te haces
15:15  GABY  me desespera que no te das cuenta de nada.. o sos tan criatura
```

An explicit, plainly worded request for physical comfort is answered with a joke,
then with a friendship-expansion plan. This is the cleanest timestamped instance in
the corpus of **"The Fixer"** (`CORE_PSYCHOLOGY/defense_mechanisms/`): distress
converted into a solvable scope. Recommended as the canonical fixture for that file
and for the attunement-latency analyzer proposed in §7.

**Third-party pressure.** The push toward sex traces to Sonia, quoted by Gaby, not
authored by her — *"como dice sonia.. necesitas que te cojan a ver si dormís"* (14:59),
*"sonia me dijo eso.. vos tenes que cogerle"* (15:04) — relayed in the same minutes as
*"no me siento bien de verdad"* (15:02) and *"falta todavía para eso"* (15:07).

## 6. Two channels — and near-silence in the working one

The `tier4_groups/Dentista_Gabi` project group (2026-06-02 → 07-12, 1,113 messages)
is not a peer group:

| Participant | Messages |
|---|---:|
| Hermes agent (`154288881946676@lid`) | **1,014 (91%)** |
| Ivan | 78 |
| Gaby (`118262125854912@lid`) | **19** |
| Kiki (`143576646291519@lid`) | 2 |

Over the same weeks Gaby sent 3,107 messages privately and 19 in the group nominally
running her business. Her 19 messages are near-identical in function:

> *"talk to me like a human.. im gabi"* · *"soy gabi."* · *"soy gabi.. creo que soy la
> única weird que quiere hablarte contexto human being"* · *"you need to know when it's
> a joke and when we're serious"* · *"no. solo déjalo así.. soy gabi.. hay solo una
> gabi.. haceme caso a mi ahora."*

She asserts *"soy gabi"* three times to an agent that will not register her as a
particular person — structurally the same move she makes three times to Ivan in the
private chat. **The consistent ask across both channels is to be recognised as a
specific human being with a specific frame.**

## 7. Open items this analysis creates

| # | Item | Why |
|---|---|---|
| 1 | **Whisper backfill, 1,114 voice notes (~13h; 10.2h Gaby's)** | Largest blind spot in tier1. Pipeline exists (`scripts/transcribe_audio.py`); attach point documented at `ANALYSIS.md §10`. Every metric above is text-only and therefore under-weights her. |
| 2 | **Fix `analyze_initiators.py`** — measure day-opens and silence-breaks, not message share; re-run across 951 chats | §0. Affects every contact, not just this one. |
| 3 | **Boundary-statement tracker** (new script) | Detect repeated boundary assertions and whether they de-escalate (received) or escalate (not). Gaby's 2.6× escalation is the clearest clinical signal here and nothing detects it. |
| 4 | **Attunement-latency analyzer** (new script) | Time from distress marker to first *empathic* reply, classifying intervening messages as joke / solution / deflection. Turns "The Fixer" into a measured per-contact number. |
| 5 | **Third-party influence tracker** | Quantify Sonia's appearances as a pressure source inside relationships with stated boundaries. |
| 6 | **Business→personal drift metric** | The 9.6% → 0.5% collapse generalises to "what did this relationship convert into". |
| 7 | **git-LFS for `media/audio/`** | 138 MB of `.opus` is committed to git in this chat alone. |

## 8. Data limits

1. **~13 hours of voice, none transcribed** — 10.2h of it Gaby's. Her channel is
   voice; Ivan's is text. This analysis reads the relationship through his medium.
2. **The window ends 2026-07-23.** Whether the boundary held afterward is not in the
   data. A subsequent export (`DOC-20260822-WA0000.zip`, 610 MB, Drive) is believed to
   cover the missing month but has not been ingested.
3. **No phone JID.** Text exports store display names, so this chat cannot be joined
   to the SQLite corpus on sender identity — join on `slug` (`ANALYSIS.md §10`).
   Gaby's mobile number is known offline but is **deliberately not committed**: the
   repo excludes third-party contact PII (`ANALYSIS.md §8`, which dropped 8 `.vcf`
   files on the same grounds).
4. **No pre-2026-05-31 history exists** for this contact anywhere in the corpus.

# tier2_core — Analysis & Naming

## What is tier2_core

30 WhatsApp chats ranked #11–40 by psychology-analysis score (below tier1's top 10 deep dives).

## Directory Naming Convention

Format: `RANK__pSCORE___wa_chat_WA_ID`
- `RANK`: 11–40 (position in full 960-chat ranking)
- `pSCORE`: raw score (higher = more psychology-relevant)
- `wa_chat_WA_ID`: WhatsApp internal chat ID

**Problem**: Slug names are all numeric codes (p3549, p3082, etc.) except `cesar_poli`. No contact names are stored in the JSON — sender_jid is null throughout.

## Contact Identification

| Rank | Score | Dir | Their First Msg | My First Reply | Assessment |
|---:|---:|---|----------------|----------------|------------|
| 11 | 296k | p3549 | "Buenas Tardes... Pedro Molina Credimarket" | Ranting at spam | SPAM/NOT RELEVANT — Credimarket marketing |
| 12 | 256k | p3082 | "Buenos días... CrediMarket" | Same spam rage | SPAM/NOT RELEVANT — duplicate Credimarket |
| 13 | 202k | p5654 | "XD" + "holis me podes pasar tus respuestas de fisica?" | Physics hw help | FRIEND — academic help, casual tone |
| 14 | 193k | p2921 | "Siii" + "Hola creo que llegue Edificio Brasilia" | Meeting arrangement | FRIEND — in-person meetup |
| 15 | 175k | p5772 | "segi conectado en llamada de skype" | "No" | FRIEND — Skype call coordination |
| 16 | 123k | p1837 | "El hecho que le reconocí enseguida es 💀💀" | Social observation | FRIEND — shared social context |
| 17 | 114k | p8718 | "Ivannn helpp" | "Holis" | CLOSE FRIEND — calls Ivan by name, asks for help |
| 18 | 106k | p5366 | "Este frupo es con ann" | Maps link shared | ACQUAINTANCE — group chat around someone named Ann |
| 19 | 105k | p9029 | "Martes" + "Cuando tenemos guitarra?" | Guitar lesson scheduling | FRIEND — guitar lessons/practice |
| 20 | 92k | p5871 | "Me olvidé mi billetera" | "Okis" | CLOSE FRIEND — forgets wallet at Ivan's |
| 21 | 83k | p9907 | "Damn" | TikTok link shared | FRIEND — shares content |
| 22 | 74k | p0001 | "Holi gracias por todo uwu" | "De nada pasé re chill" | CLOSE FRIEND — reciprocal warmth |
| 23 | 69k | cesar_poli | "Gracias weiss" | "hey gente" | FRIEND — Poli/gym context |
| 24 | 61k | p9739 | "Si claro" | Buying sexshop items | KINK/FWB — candle + fox plug purchase |
| 25 | 60k | p3862 | "Y si queres ir a una universidad facha..." | Scholarship discussion | ACQUAINTANCE — career/education advice |
| 26 | 59k | p8879 | "Hola! Gracias por escribirme..." (auto) | "Holis que tal puedo llamarte?" | AUTO-RESPONSE — business/automated |
| 27 | 58k | p1686 | "Hola Ivan, como estás? Soy Lilian Riveros" | Introduction + health info | NEW CONTACT — Lilian Riveros |
| 28 | 58k | p0082 | "Holii" | "Como aplicó?" | ACQUAINTANCE — job application |
| 29 | 57k | p9763 | "Hewooo !!" | "Hello uwuw Iván Weiss" | NEW PERSON — spring break Kansas |
| 30 | 51k | p8339 | " Simpático, pero no para el esposo..." | "Holis sorry estoy con re mala señal" | FAMILY/PARTNER — financial + domestic |
| 31 | 51k | p8387 | YouTube link | YouTube link shared | FRIEND — content sharing |
| 32 | 50k | p3949 | "Holaaa" | "No tengo :(" | ACQUAINTANCE — simple greeting |
| 33 | 46k | p8241 | (unknown - null text field) | — | UNKNOWN |
| 34 | 44k | p0109 | (unknown - null text field) | — | UNKNOWN |
| 35 | 44k | p8488 | "viejooo" | "XD" | FRIEND — casual, short exchanges |
| 36 | 32k | p4184 | "Holiss ahora llegué...gracias por acompañarme" | "Avisa cuando llegues uwu" | CLOSE FRIEND — gratitude for accompaniment |
| 37 | 31k | p9382 | (unknown - null text field) | — | UNKNOWN |
| 38 | 27k | p3912 | "Buen día" + "Será que puedo ir a verte medio urgente?" | "Hola Víctor" | VÍCTOR — urgent personal meeting request |

## Relevance to Psychology Repo

### High Priority (analyze for wounds/defense patterns)

| Rank | Contact | Why |
|---:|---|---|
| 17 | p8718 | "Ivannn helpp" — Fixer pattern, close friend |
| 20 | p5871 | Forgot wallet — domestic intimacy, staying over |
| 22 | p0001 | "gracias por todo uwu" — warm reciprocal friendship |
| 23 | cesar_poli | Gym/fitness context, body relationship |
| 24 | p9739 | Sexshop companion — kink dynamics |
| 30 | p8339 | Financial + domestic — could show mother/household patterns |
| 36 | p4184 | Gratitude for accompaniment — vulnerability expressed |
| 38 | Víctor | Urgent meeting request — attachment, avoidance? |

### Medium Priority

| Rank | Contact | Why |
|---:|---|---|
| 13 | p5654 | Academic help — fixer/service to friend |
| 14 | p2921 | In-person meetup — social skills, boundaries |
| 15 | p5772 | Skype call — digital intimacy |
| 16 | p1837 | Social recognition — identity, reputation |
| 19 | p9029 | Guitar lessons — creative self, shared activity |
| 21 | p9907 | Content sharing — how he connects |
| 27 | p1686 | Lilian Riveros — new person, health context |
| 28 | p0082 | Job application — career/self-worth |
| 29 | p9763 | Spring break Kansas — new person, alcohol/sex? |

### Low Priority (not relevant)

| Rank | Contact | Why |
|---:|---|---|
| 11 | p3549 | Spam — Credimarket |
| 12 | p3082 | Spam — Credimarket |
| 26 | p8879 | Auto-response bot |
| 33–37 | p3949/p0109/p8488/p9382 | Null text — group/system messages |

### Unknown (need deeper look)

| Rank | Contact | Action |
|---:|---|---|
| 33 | p3949 | Inspect for group name |
| 34 | p0109 | Inspect for group name |
| 37 | p9382 | Inspect for group name |

## Recommended Actions

1. **Drop ranks 11, 12** — pure Credimarket spam, no psychology value. Add to `_dropped/` and commit.
2. **Rename dirs** with contact names (see mapping above) — replace numeric slugs with readable names.
3. **Inspect unknown 3** (ranks 33, 34, 37) to identify.
4. **Transcribe voice notes** in high-priority chats (17, 22, 24, 36, 38) — these likely have audio.
5. **Extract for MASTER_PROFILE** relevant patterns from 17, 22, 30, 36, 38.

## Notes

- Most chats have voice notes (audio count column in CHAT_INDEX.md) — full analysis requires transcription
- Null `sender_jid` throughout = WA export anonymized the phone numbers
- Contact names must be inferred from conversation content
- "Cesar_poli" was already named in prior work — confirms manual naming is possible

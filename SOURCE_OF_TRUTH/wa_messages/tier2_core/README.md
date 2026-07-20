# tier2_core — Renamed & Assessed

28 WhatsApp chats (ranks 13–40, dropped 11/12 as spam).

## Renamed Dirs (2026-07-20)

| Rank | Dir | Type | Notes |
|---:|---|:---:|---|
| 13 | `friend_study` | FRIEND | Academic help (physics hw) |
| 14 | `friend_brasilia` | FRIEND | In-person meetup (Edificio Brasilia) |
| 15 | `friend_skype` | FRIEND | Skype call coordination |
| 16 | `friend_alvaro` | FRIEND | Social context |
| 17 | `friend_helpp` | CLOSE | Calls Ivan by name, asks for help — **FIXER PATTERN** |
| 18 | `friend_ann_group` | ACQUAINTANCE | Group chat around Ann |
| 19 | `friend_guitar` | FRIEND | Guitar lessons/practice scheduling |
| 20 | `friend_wallet` | CLOSE | Forgot wallet at Ivan's — **DOMESTIC INTIMACY** |
| 21 | `friend_casual` | FRIEND | Casual exchanges, shared content |
| 22 | `friend_tiktok_share` | CLOSE | Shares TikToks — reciprocal content |
| 23 | `cesar_poli` | FRIEND | Gym/Poli context (pre-existing name) |
| 24 | `sexshop_companion` | KINK/FWB | Sexshop + candle/fox plug — **KINK DYNAMICS** |
| 25 | `friend_becas` | ACQUAINTANCE | Scholarship/career advice |
| 26 | `job_auto_response` | LOW | Automated business response |
| 27 | `lilian_riveros` | NEW CONTACT | Health context (sexshop referral) |
| 28 | `friend_job_apply` | ACQUAINTANCE | Job application |
| 29 | `kansas_springbreak` | NEW PERSON | Spring break Kansas — new exposure |
| 30 | `household_financial` | FAMILY/PARTNER | Financial + domestic — **MOTHER PATTERN** |
| 31 | `friend_youtube` | FRIEND | YouTube content sharing |
| 32 | `kiki_adjacent` | KIKI | Near Kiki — monitoring context |
| 33 | `friend_simple` | ACQUAINTANCE | Simple greetings, low engagement |
| 34 | `friend_photos` | FRIEND | Exchange photos, gratitude |
| 35 | `friend_alvaro2` | FRIEND | Second Alvaro contact (separate from rank 16) |
| 36 | `friend_arrival` | CLOSE | Gratitude for accompaniment — **VULNERABILITY** |
| 37 | `casual_short` | FRIEND | Very short exchanges |
| 38 | `alejandro` | ACQUAINTANCE | Content sharing |
| 39 | `victor_urgent` | NEW/URGENT | **URGENT MEETING REQUEST — medical?** |

## Dropped (spam, moved to `_dropped/`)
- Rank 11: `p3549` — Credimarket spam (Pedro Molina marketing)
- Rank 12: `p3082` — Credimarket spam (duplicate)

## Relevance to Psychology Repo

### HIGH PRIORITY — wound/defense pattern extraction

| Rank | Dir | Wound/Pattern | Action |
|---:|---|---|---|
| 17 | `friend_helpp` | Fixer (Ivan helps with problems) | Deep dive |
| 20 | `friend_wallet` | Domestic intimacy, staying over | Deep dive |
| 24 | `sexshop_companion` | Kink dynamics, service | Deep dive |
| 30 | `household_financial` | Mother/household patterns | Deep dive |
| 36 | `friend_arrival` | Expressed gratitude — vulnerability | Deep dive |
| 39 | `victor_urgent` | Urgent meeting request — attachment/avoidance? | Identify + deep dive |

### MEDIUM PRIORITY — relationship patterns

| Rank | Dir | Why |
|---:|---|---|
| 13 | `friend_study` | Intellectual bond, academic fixer |
| 14 | `friend_brasilia` | In-person boundaries, social skills |
| 16 | `friend_alvaro` | Identity, reputation, social recognition |
| 19 | `friend_guitar` | Creative self, shared activity |
| 22 | `friend_tiktok_share` | Reciprocal sharing, how he connects |
| 27 | `lilian_riveros` | Health advocacy (vs. Laura's medical avoidance) |
| 29 | `kansas_springbreak` | New person, alcohol/sex, exploration |

### LOW PRIORITY — can skip for now

| Rank | Dir | Why |
|---:|---|---|
| 15 | `friend_skype` | Practical coordination only |
| 18 | `friend_ann_group` | Group context, diluted signal |
| 21 | `friend_casual` | Casual, low depth |
| 25 | `friend_becas` | Career/scholarship — transactional |
| 26 | `job_auto_response` | Bot/automated |
| 28 | `friend_job_apply` | One-off job application |
| 31 | `friend_youtube` | Content sharing only |
| 32 | `kiki_adjacent` | Near Kiki, monitoring |
| 33 | `friend_simple` | Minimal engagement |
| 34 | `friend_photos` | Simple exchange |
| 35 | `friend_alvaro2` | Duplicative of rank 16 |
| 37 | `casual_short` | Very short, low signal |
| 38 | `alejandro` | Content sharing only |

## Next Steps

1. **Voice transcription** — run on high-priority chats 17, 20, 24, 30, 36, 39
2. **Extract wound patterns** → MASTER_PROFILE.md or relevant docs
3. **Identify Víctor** (rank 39) — who is he? Add to RELATIONSHIP_TIMELINE if relevant
4. **Cross-ref Lilian Riveros** (rank 27) — new health contact, add to timeline
5. **Drop low-priority dirs** (26, 33) if confirmed no psychology value

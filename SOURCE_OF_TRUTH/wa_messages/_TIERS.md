# wa_messages/ — Tier System

> **Last updated**: 2026-07-27 (post-cleanup)
> **Total chats**: 951 across 9 categories
> **Naming coverage**: 100% (951/951 named)

## Tier System

| Tier | Count | Description |
|------|------:|-------------|
| `tier1_deep/` | 11 | **Closest contacts** — score 70+ or major volume |
| `tier2_core/` | 75 | **Core** — score 50-69, active relationships |
| `tier3_extended/` | 119 | **Extended** — score 30-49, occasional contact |
| `tier4_groups/` | 158 | **Group chats** (3+ people) |
| `untiered_personal/` | 304 | **Personal but unscored** — 1-1 chats without contact info |
| `other_lid/` | 10 | **Other LID-based chats** (newer WhatsApp format) |
| `_dropped/` | 267 | **Dropped** — too small, no signal, or merged |
| `_newsletters/` | 7 | **Broadcast channels** (newsletters, channels) |
| `_conversations/` | 0 | **Conversation exports** (moved to other tiers) |
| `_ANALYSIS/` | — | **All dashboards** (start here) |

## What's in each tier

### `tier1_deep/` — 11 chats, ~152k msgs
The closest. Includes:
- Laura 🐷
- Magali Carreras Amiga Fpuna
- Lourdes Youko Kurama
- Jonatan Verdun
- Alejandro Cabral Poli
- Mom Sonia
- 11__gabriella_gp (Ometz Dental client + close friend)
- Grandpa_Jan_Van_Der_Pol (added in 2026-07-27 cleanup)
- Ivan's own contact info
- A few other close contacts

### `tier2_core/` — 75 chats, ~89k msgs
Close friends, family, and important contacts:
- **Family**: Alexander van der Pol, Anna Rodas van der Pol, Prima Mikaela Weiss, Gerold Manders
- **Close friends**: Nathaly Schinini (MAIN 7), Maga, Génesis, Matías Barrios, Bianca MM
- **Workers**: Cliente 3d Edgar Fpuna, Cliente 3d Óscar Rafa (1,420+1,096 msgs)
- **International**: Juanra Ferreira 🇵🇾 (1,096 msgs Brazilian friend)
- **Professional**: Camilo Amarilla, José Villalba Lugo, Consultorio Duerksen

### `tier3_extended/` — 119 chats, ~18k msgs
Regular contacts with score 30-49:
- Schools/classmates, local businesses, vets, doctors, family cousins
- Examples: Primo Gabriel, Brenda Poli, Rosario Ruiz, Mymba Roga (vet), Tury, Ogr

### `tier4_groups/` — 158 groups, ~200k msgs
Group chats: family, friends, work, school, kink, etc.
- **Family**: Weiss_Siblings, Flia_Weiss_Van_Der_Pol
- **Friends**: Amigos_De_Las_Locuras_Swinger, Sarah_S_Neon_Furry_B-Day_Party
- **Work**: Stoic_Finch_-_Latam, Maskarada_-_Club_De_Azote
- **School**: Iin_Fpuna_2019_-_2025, Club_De_Info_Gral
- **Kink**: Cum_A_Secas, Funhouse
- **Recovered 2026-07-27**: Group_Nexa-Paraguay (991 msgs!), Group_Rach (908), Group_Iinformaciones_De_La_Carrera (916)

### `untiered_personal/` — 304 chats, ~12k msgs
Personal 1-1 chats without vCard info. **All named** as of 2026-07-27:
- Real people: Yissel Montiel, Dr. Demián Glujovsky, Oli (Grindr), Peider (QA), Amanda, Alonso (Motivus)
- Businesses: Frutika Delivery, Koi Delivery, La Luna es Mía, Che Vare'a Grill
- Kink: BDSM Femdom Chat, Kink Castigos, Tinder Match, Grindr Contact
- Referrals: Kiki_Referral_Wes, Sarah_Bum_Referral, Anna_Referral

### `other_lid/` — 10 chats, ~31k msgs
LID-based chats with newer WhatsApp format. All named:
- Thais (3,825 msgs), Dan (Somosgay), Kink_Artist, Kinesiólogo, Cloud_Nyx
- El_Viajero, Foodie_Friend, OpenClaw_User, AI_QA_Ing_Info

### `_newsletters/` — 7 chats, ~2k msgs (NEW 2026-07-27)
Broadcast channels:
- CONMEBOL Sudamericana (629 msgs), StandUp Barranquilla (626 msgs)
- Holiday hours, Love Stories, The Dodo

### `_dropped/` — 267 chats, ~2k msgs
**Why so many?** Most are:
- 1-message "hello" chats from strangers
- Sales/notification bots
- One-time contacts
- Chats that failed vCard matching
- **NEW**: 3 spam chats (Ivan Credimarket rage-text 317 times in 1 day 😂)

**Don't delete yet**: Some have valuable content but no JID/name match.

### `_conversations/` — 0 chats (consolidated 2026-07-27)
- All conversation exports now live in their proper tier folders
- Gaby's full WA export (5,985 msgs) → tier1_deep/

## What goes where

When adding a new chat:
1. **Score it** using `scripts/build_relationship_dashboard.py`
2. **Place in tier1-3** based on score
3. **Groups** → tier4_groups
4. **No contact info** → untiered_personal
5. **Trivial/empty** → _dropped
6. **Full WA export** → appropriate tier (not _conversations)
7. **Newsletter/broadcast** → _newsletters

## Score → Tier mapping

```
70+    → tier1_deep
50-69  → tier2_core
30-49  → tier3_extended
<30    → untiered_personal (with vCard) or _dropped (without)
group (3+) → tier4_groups
<5 msgs and not in vCard → _dropped
broadcast channel → _newsletters
```

## The 9 categories debate

**Question**: Why 9 categories? Isn't this overkill?

**Answer**:
- 4 tier folders (1-3) + 1 group = 5 categories for live data ✅
- `other_lid` is technical (LID vs phone) → keep separate
- `_dropped` and `_conversations` are admin/archived → keep separate
- `_newsletters` is a NEW 2026-07-27 split for broadcast content

**Cleanup history (2026-07-27)**:
- Created `_newsletters` tier (7 broadcasts separated)
- Consolidated `_conversations/` (was 75 chats) — all moved to appropriate tiers
- Removed `circles/` (was 6 chats) — merged into _dropped in earlier cleanup

## Major Cleanup Results (2026-07-27)

| Operation | Count |
|-----------|------:|
| Contacts rescued from `_dropped` to proper tiers | 196 |
| Groups moved from `_dropped` to tier4_groups | 134 |
| Tier3 → Tier2 promotions (score >= 50) | 70 |
| Newsletters extracted to `_newsletters` | 7 |
| Tier1 spam removed to `_dropped` | 3 |
| **Final naming coverage** | **100%** ✅ |

See [docs/CLEANUP_REPORT_2026-07-27.md](../../docs/CLEANUP_REPORT_2026-07-27.md) for full details.
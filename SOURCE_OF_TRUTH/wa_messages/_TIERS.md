# wa_messages/ — Tier System

> **Last updated**: 2026-07-25
> **Total chats**: 948 across 9 categories

## Tier System

| Tier | Count | Description |
|------|------:|-------------|
| `tier1_deep/` | 13 | **Closest contacts** — score 70+ or major volume |
| `tier2_core/` | 32 | **Core** — score 50-69, active relationships |
| `tier3_extended/` | 63 | **Extended** — score 30-49, occasional contact |
| `tier4_groups/` | 42 | **Group chats** (3+ people) |
| `untiered_personal/` | 153 | **Personal but unscored** — 1-1 chats without contact info |
| `other_lid/` | 10 | **Other LID-based chats** (newer WhatsApp format) |
| `circles/` | 6 | **Google Circles** (legacy import) |
| `_dropped/` | 643 | **Dropped** — too small, no signal, or merged |
| `_conversations/` | 75 | **Conversation exports** (re-imports, not primary data) |
| `_ANALYSIS/` | 36 | **All dashboards** (start here) |

## What's in each tier

### `tier1_deep/` — 13 chats, ~155k msgs
The closest. Includes:
- Laura 🐷
- Magali Carreras Amiga Fpuna
- Lourdes Youko Kurama
- Jonatan Verdun
- Alejandro Cabral Poli
- Mom Sonia
- Defi
- 11__gabriella_gp (NEW! Ometz Dental client)
- + a few others

### `tier4_groups/` — 42 groups
Group chats: family (`weiss_siblings_530`, `flia_weiss_van_der_pol_443`), friends, work, school, kink, etc.

### `_dropped/` — 643 chats
**Why so many?** Most are:
- 1-message "hello" chats from strangers
- Sales/notification bots
- One-time contacts
- Chats that failed vCard matching

**Don't delete yet**: Some have valuable content but no JID/name match.

### `_conversations/` — 75 chats
- Re-imports from official WhatsApp text exports
- Includes Gaby's full WA export (5,985 msgs)
- Each has its own `media/` and `source/`

## What goes where

When adding a new chat:
1. **Score it** using `scripts/build_relationship_dashboard.py`
2. **Place in tier1-3** based on score
3. **Groups** → tier4_groups
4. **No contact info** → untiered_personal
5. **Trivial/empty** → _dropped
6. **Full WA export** → _conversations

## Score → Tier mapping

```
70+  → tier1_deep
50-69 → tier2_core
30-49 → tier3_extended
<30  → untiered_personal
group (3+) → tier4_groups
<5 msgs and not in vCard → _dropped
```

## The 8 categories debate

**Question**: Why 8 categories? Isn't this overkill?

**Answer**: 
- 4 tier folders (1-3) + 1 group = 5 categories for live data ✅
- `other_lid` and `circles` are technical/legacy → can probably be merged
- `_dropped` and `_conversations` are admin/archived → keep separate

**Cleanup**: Could collapse `other_lid` into `untiered_personal` and `circles` into `_dropped`. But this is risky — better to leave as-is.

# Relationship Dashboard Insights

> Generated 2026-07-23 · 216 contacts scored · average score 43.5/100

## Tier Distribution

| Tier | Count | Description |
|------|-------|-------------|
| **CLOSE** | 12 | Best friends, mentors (score ≥65) |
| **ACTIVE** | 61 | Regular friends (score 50-64) |
| **WARM** | 88 | Occasional (score 35-49) |
| **DORMANT** | 39 | Inactive (score 20-34) |
| **COLD** | 16 | Stale or business (score <20) |

## Top 20 Strongest Relationships

| # | Score | Name | Msgs | Last | Span | Tier |
|---|-------|------|------|------|------|------|
| 1 | 78.8 | Laura 🐷 | 23,105 | 12d | 2.7y | CLOSE |
| 2 | 78.1 | Lourdes Youko Kurama | 16,905 | 2d | 4.0y | CLOSE |
| 3 | 76.6 | Magali Carreras Amiga Fpuna | 28,457 | 8d | 5.8y | CLOSE |
| 4 | 76.1 | Sonia Weiss (Mom) | 11,305 | 3d | 5.8y | CLOSE |
| 5 | 72.5 | Alejandro Cabral Poli | 23,000 | 2d | 5.8y | CLOSE |
| 6 | 71.4 | Kiki Weiss Hermana | 7,838 | 2d | 5.8y | CLOSE |
| 7 | 70.4 | Sofi Nashe | 4,098 | 5d | 2.1y | CLOSE |
| 8 | 68.7 | Fran | 7,392 | 9d | 4.8y | CLOSE |
| 9 | 68.0 | Jonatan Verdún | 34,526 | 18d | 2.4y | CLOSE |
| 10 | 67.4 | Rach | 1,128 | 6d | 1.2y | CLOSE |
| 11 | 67.0 | Emilio Poli | 4,230 | 27d | 1.5y | CLOSE |
| 12 | 66.6 | Lucía Díaz | 5,155 | 8d | 3.5y | CLOSE |

## Longest Consecutive Streaks

| Days | Name | Context |
|------|------|---------|
| **145d** | Laura 🐷 | Intense engagement period |
| 75d | Jonatan Verdún | Sustained daily contact |
| 55d | Lourdes Youko Kurama | Active period |
| 42d | Magali Carreras Amiga Fpuna | Long run |
| 30d | Alejandro Cabral Poli | One month streak |
| 26d | Defi Not There 4 U | Recent revival |
| 21d | Sonia Weiss (Mom) | Always-on baseline |

## Activity Status

- **Active in last 30 days:** 27 contacts
- **Dormant (>180 days):** 149 contacts
- **Total:** 216 named contacts in vCard

## Most One-Sided Relationships (reciprocity < 50)

These are chats where Ivan dominates — they don't reply much:

- Iván Weiss Número Pro (0%)
- Gabriela González IT Alianza (0%)
- Ebsa (0%)
- Fran IEK (0%)
- Locanto X (0%)

## Most Balanced Relationships (reciprocity = 100%)

Equal give-and-take, both parties equally engaged:

- Prima Mikaela Weiss
- Héctor Gonzales IEN
- Patiño
- Bacon Villa Morra
- Magali Amarilla LinkedIn

## Highest Sentiment (most positive tone)

All score 100 (very positive): Adrian, Jessica Chena, Sebastián Aguilera, Alexander van der Pol, Prima Mikaela Weiss, Hospital Bautista, Natasha, Lucas Germán, Grido Ingavi, Jose S.

## Lowest Sentiment (most negative tone)

- Álvaro Claro: 6/100 (lowest)
- Ana Esposa De Sander: 25
- Carlos Oviedo: 25
- Guille Pamplona: 25
- Anillo: 25

## Open Questions

1. **Saskia's brother** (JID 595985725871, "guitar_friend") — vCard says Saskia Weiss, chat content says "Soy el hermano mayor de saskia"
2. **3 friends named Luana** — not in vCard, no self-intro
3. **Mom's siblings** (Carlú, Julio, Roberto) — referenced but not yet identified

## Score Formula

```
score = volume(15) + recency(15) + sentiment(12) + 
        reciprocity(10) + latency(10) + streak(10) + 
        longevity(10) + audio(8) + emoji(5) + activity(5)
```

- **Volume**: log-scale of total messages
- **Recency**: days since last contact (decay)
- **Sentiment**: positive word ratio (Spanish+English dictionaries)
- **Reciprocity**: balance between Ivan ↔ them
- **Latency**: average reply time
- **Streak**: longest consecutive-day streak
- **Longevity**: total span of contact in years
- **Audio**: % voice notes (intimacy signal)
- **Emoji**: emoji density per message
- **Activity**: messages per day

## Files

- `relationships_dashboard.html` — visual sortable table
- `relationships_dashboard.json` — raw data + breakdowns per contact

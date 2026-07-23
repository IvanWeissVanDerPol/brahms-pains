# Open question: Is JID 595985724135 Kiki or Saskia?

> **Status:** ⏸️ Awaiting clarification from Ivan
> **Discovered:** 2026-07-23 during family-identity migration

## What the corpus says

In the chat at `tier1_deep/sister_kyrian_kiki___wa_chat_595985724135_111` (7,838 msgs, 2020-10-10 → 2026-07-20), the contact identifies themselves as **"Soy saskia"** on day 8 of the chat:

```
[2020-11-18] them: Soy saskia
[2020-11-18] them: Se me dio por preguntarte que tal estas
```

This was the second time the contact spoke in the chat (after 8 days of brief logistics messages).

## What Ivan said in the questionnaire (2026-07-23)

| Field | Ivan's answer |
|-------|---------------|
| B1.1 — Confirm Kiki = Saskia? | **NO** |
| G6 — Three sisters: | Luana (24), Saskia, Kyrian "Kiki" |
| B2.1 — Luana = full sister? | Yes |
| (Kyrian) | "Kiki" |

So per Ivan:
- Luana Weiss = sister
- Saskia Weiss = sister (separate)
- Kyrian Weiss = sister (a.k.a. "Kiki")

## What the auto-miner thought

The `tier1_deep` chat at JID 595985724135 was auto-named `07__kiki_hermana` (the vCard-derived name). When today's migration ran, we trusted Ivan's verbal answer (that Kiki = Kyrian) and renamed it to `sister_kyrian_kiki`.

But the contact in that chat literally said **"Soy saskia"** — and "saskia" appears 6 times in `them` messages.

## What Ivan calls the contact

Ivan uses these names to address the contact in this chat:

| Name | Count |
|------|-------|
| kiki | 29 |
| kyrian | 9 |
| saskia | 1 |
| luana | 29 |

The high `luana` count is suspicious — Ivan sometimes calls this person "Luana"? Or are there messages where Ivan is talking about Luana to this person (third-person)?

## Two possible interpretations

### Interpretation A: Kiki = Saskia (Ivan was wrong about B1.1)

- The JID 595985724135 belongs to **Saskia**, who goes by "Kiki" as a nickname.
- Ivan's answer "Kiki ≠ Saskia" was incorrect — they're the same person.
- The "Soy saskia" makes perfect sense.
- Luana is a separate sister (JID 595985725366, confirmed).

### Interpretation B: Kiki = Kyrian, separate from Saskia (Ivan is right)

- The JID 595985724135 belongs to **Kyrian (Kiki)**.
- The "Soy saskia" is a one-time joke or borrowing a sibling's phone.
- Ivan's answer is correct.
- Saskia has a separate chat JID that we haven't identified yet (she may not have a dedicated 1-on-1 chat in this corpus).

## What's in favor of A

- The "Soy saskia" message is the most direct self-introduction in the chat
- Kiki and Saskia both start with "S", both could be nicknames
- If Saskia is the older sister, calling her "kiki" later would be a nickname by Ivan

## What's in favor of B

- Ivan was explicit ("No" to B1.1)
- The chat content matches Ivan's description of Kiki being the engineering student / business partner
- Ivan's questionnaire was given very recently (today)
- A 29× count of "kiki" / "kyrian" by Ivan is strong evidence

## What I did

- Kept the directory name `sister_kyrian_kiki___wa_chat_595985724135_111` (per Ivan's B1.1)
- Did NOT change the `KIKI_HERMANA.md` profile, except for adding this discovery note
- Did NOT rename or merge chats

## What I need from Ivan

Just one answer:

| # | Question | Answer |
|---|----------|--------|
| 1 | **JID 595985724135 is Kiki (Kyrian) or Saskia?** | [ ] Kiki/Kyrian (Ivan was right) — Saskia has separate chat we haven't found<br>[ ] Kiki IS Saskia (they're the same person; B1.1 was wrong)<br>[ ] I don't remember / unclear |

If "Kiki IS Saskia" → I'll merge the dir name to `sister_saskia___wa_chat_595985724135_111` and update the KIKI_HERMANA profile.

If "Kiki ≠ Saskia" → I'll keep current state and document that Saskia's chat JID is unknown (probably doesn't exist as a 1-on-1 in this corpus).

## Files affected if Kiki = Saskia (option B1.1 wrong)

1. Rename chat dir: `sister_kyrian_kiki___wa_chat_595985724135_111` → `sister_saskia___wa_chat_595985724135_111`
2. Update CONTACTS_NAMED.md (Kyrian "Kiki" line → "Saskia (a.k.a. Kiki)")
3. Update phonebook.json (if there's a Kiki entry)
4. Update KIKI_HERMANA.md (rename file to SASKIA.md, rewrite profile)
5. Update SONIA.md family tree (only one sister Kyrian entry should disappear; Saskia is the same person)

If the answer is "Kiki = Kyrian" (Ivan was right):
1. Keep everything as-is
2. Add a footnote that the JID is Kiki and Saskia's separate chat is unknown

---

**Waiting on your answer.**

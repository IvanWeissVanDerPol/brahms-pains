# Cursor Loop Integration Analysis — 2026-07-29

## TL;DR — What's actually useful vs. what's noise

The zip is the **state of an automated "improve all my Cursor prompts" sweep** running across the
**Eneve .NET / C# monorepo** (`Eneve.eBase.Meter`, `Eneve.eBase.Foundation`,
`Eneve.eBase.TimeSeries.Calculation`, etc.). Three distinct artifacts, three distinct value
ratings for Hermes:

| Artifact | What it is | Value for Hermes | Why |
|---|---|---|---|
| `commands/jp-*.md` (17 files) | Cursor slash-command specs, all hardcoded to `@Eneve.Engineering.Playbook/...` paths and Eneve ticket prefixes (`EBASE-14257`) | **LOW** | Paths and Jira prefixes are Eneve-specific. Hermes already has skills + tools for the same jobs. |
| `exemplars/*` (20 files) | Few-shot "gold standard" examples: user stories, changelogs, complexity reports, etc. | **HIGH — reusable patterns** | The *shapes* (Given/When/Then user stories, complexity reports, gap analyses, AAA test docs, XML doc patterns) are domain-agnostic and can feed our prompt authoring. |
| `.loop-state/*` | Live state of an in-progress run: 51-iteration queue, 311 prioritized prompts with quality scores, 428K staged diff | **MEDIUM — the loop pattern itself** | The **prompt-improvement-loop** pattern (score → rewrite → staged → human-commit) is genuinely useful as a *meta-loop* skill in Hermes. The actual Eneve content isn't. |

**Bottom line:** the **commands** are throwaway (Eneve-specific), the **exemplars** are gold (domain-agnostic prompt patterns), and the **loop state** gives us a reusable *meta-pattern* worth one new Hermes skill.

---

## The 17 Eneve commands — what each does, and what we already have

| Cursor command | Eneve does what | Hermes equivalent (already exists) | Gap |
|---|---|---|---|
| `jp-quality-push` | Run coverage + refactor + diff-review + gaps + docs across N repos from a manifest | `hermes-kanban-ops` + cron jobs | Manifest-driven multi-repo sweep is genuinely missing |
| `jp-midnight-run` | Full 6-phase quality run on one repo, stops after diff review | `ai-whisperers-fleet-health` + per-repo skills | Same minus the manual stop |
| `jp-check-coverage` | Loop improving line coverage to ≥70% | `client-sites-healthcheck` (uptime only) | Coverage-as-loop is missing |
| `jp-find-missing-tests` | Identify missing test cases, ranked Critical/High/Medium/Low | `test-driven-development` skill | Lower-fidelity version exists |
| `jp-doc-standard` | AAA test doc enforcement, manual one-file-at-a-time | (none for tests) | Genuine gap — we have prod-doc patterns, no test-doc patterns |
| `jp-refactor-advice` | Module boundary / responsibility / coupling review | `simplify-code`, `refactoring-ui`, `pr-review` | Skill exists but no CC/CRAP gating |
| `jp-analyze-gaps` | Critical/High/Medium/Low gap classification | `pr-review`, `dogfood` | Ad-hoc, not standardized |
| `jp-address-findings` | Fix unambiguous findings inline | (part of `pr-review`) | OK |
| `jp-plan-ticket` | Resume a ticket — find files, validate plan, plan-mode | (none for Jira; Kanban has its own) | Hermes uses Kanban, not Jira. Skipped. |
| `jp-jira-comment` | Post commit summary as Jira comment | Kanban voice/notify | Skipped — no Jira. |
| `jp-commit-text` | Bracket-ticket-ID style commit message | Conventional Commits via repo | Different style, not a gap. |
| `jp-investigate-topic` | Deep-dive one topic from a YAML registry | `client-strategic-repositioning`, `strategy-repo-research-wave` | Same pattern. |
| `jp-mine-cpp-topics` | Mine legacy C++ for migration candidates | (none — we're greenfield TS/Python) | Irrelevant. |
| `jp-mine-migrated-features` | Backfill migration registry from code | `cross-repo-content-sync` | Similar. |
| `jp-refresh-migration-tracker` | Regenerate migration reports | (none) | Irrelevant — no migration tracker. |
| `jp-check-documentation-sync` | Check docs vs. code | (none systematic) | Genuine gap. |

**Domain relevance summary:**
- **7 / 17 are Eneve-specific** (Jira, C++ migration, Eneve ticket format) → SKIP entirely
- **6 / 17 are duplicates of existing Hermes skills** → no action
- **4 / 17 are genuine gaps** worth Hermes-ifying:
  - Manifest-driven multi-repo quality sweep
  - Coverage-improvement loop with 70% gate
  - AAA test-doc standard enforcer
  - Documentation-vs-code drift checker

---

## The 20 exemplars — what's reusable as patterns

These are few-shot examples for the LLM. The *shape* is the value, not the content:

### Tier 1 — Adapt as-is for our prompt-authoring
- **`agile/user-story-exemplar.md`** — Given/When/Then with primary/secondary users, business value,
  multiple scenarios. Adapt for any client work.
- **`agile/user-story-bad-exemplar.md`** — contrastive pair with the good one. Critical for prompt
  quality. (We currently have NO bad-example in our skills.)
- **`code-quality/complexity-metrics-analysis-exemplar.md`** — CRAP score table format, severity
  ranking. Direct fit for `simplify-code` skill enrichment.
- **`code-quality/architectural-question-exemplar.md`** — module-boundary Q&A pattern.
- **`changelog/agent-application-rule-exemplar.md`** — when an agent should/shouldn't auto-apply
  changes. **Very Hermes-relevant.**
- **`changelog/generate-changelog-from-git-exemplar.md`** — Conventional-Commits-style generation
  from `git log`. We could feed this into `release-notes` skill.
- **`cicd/tag-based-versioning-exemplar.md`** — semver-from-tags pattern.
- **`cicd/xml-documentation-patterns-exemplar.md`** — XML doc-comment patterns for IDE intellisense.
- **`code-quality/create-fix-script-workflow-exemplar.md`** — diagnostic → fix-script → run →
  verify → revert pattern. Hermes-relevant.
- **`code-quality/diagnostic-fix-script-patterns-exemplar.md`** — same family.

### Tier 2 — Useful but require significant adaptation
- **`agile/epic-exemplar.md`**, **`business-feature-exemplar.md`**, **`technical-feature-exemplar.md`**
  — Eneve's hierarchy maps to our Client → Project → Task Kanban, not literally reusable.
- **`cicd/documentation-pipeline-setup-exemplar.md`** — generic CI/CD doc pipeline; useful inspiration
  but Eneve-specific (XML doc, VB.NET conventions).

### Tier 3 — Skip
- **`analysis/analyze-gaps-exemplar.md`** — Eneve gap-analysis rubric (Standards/Documentation/
  Migration/Coverage). Hermes gap analysis lives in `pr-review`, no formal rubric yet.
- **`changelog/quick-changelog-update-exemplar.md`** — trivial; we already do this.
- **`cicd/*` (5 of 8)** — Eneve build-pipeline specifics (Nuspec, TFS, VB.NET conventions).

---

## The loop pattern — the highest-value extraction

**What Eneve does:**

```
1. Discover prompts in repo (discover prompts not authored by humans)
2. Score each prompt on a fixed rubric (missing-purpose, missing-validation, missing-examples,
   missing-process)
3. Sort by score ascending (worst first)
4. Loop: for each queued prompt, dispatch Composer subagent to rewrite it
5. After all rewrites, Claude-4.6-sonnet-medium-thinking reviews the staged diff
6. Stage the changes; user commits by hand
7. Log completion in prompt-improvement-loop.json
```

**What we could do identically for ourselves:**

```
1. Discover prompt-shaped artifacts in our stack:
   - Hermes skills (177)
   - Skill references/templates
   - Prompt-prefix files in our config
   - Cursor `.cursorrules` files in our client repos (if any)
2. Score each against a rubric we adapt from Eneve:
   - missing-trigger-condition
   - missing-numbered-steps
   - missing-verification-step
   - missing-pitfall-section
3. Sort, loop, stage, human-commits
```

**Why this is worth doing:**
- We have **177 skills**, many authored ad-hoc over months. ~20-40% likely have the same
  "missing-X" issues Eneve's loop found.
- The Eneve scoring rubric generalizes cleanly (their 4 categories map to our 4 categories
  with 1-line changes).
- The staged-review + human-commit gate matches our existing workflow patterns.

**Why we should NOT wholesale copy:**
- The composer-2.5 subagent + claude-4.6-sonnet reviewer combo is Eneve's tool stack. We use
  `MiniMax-M3` + escalation per `model-router`.
- Eneve's loop runs 51 iterations unattended. Hermes has a `cron-cost-guard` and explicit budget.
  We must add cost ceilings.
- Eneve assumes VB.NET/C# XML doc conventions. Our prompts are TS/Python/Next.js.

---

## Retroactive application — what would actually move the needle

We have ~20+ repos of completed work. Going through them with an Eneve-style loop would
**burn tokens without proportional value** because:

| Repo type | Count | Would benefit from retroactive loop? |
|---|---|---|
| psycology (this repo) | 1 | Maybe — has analyses & docs |
| dentist (active client) | 3 | No — live work, use forward |
| client Next.js sites (paragu-ai-platform, etc.) | 8-10 | No — already deployed |
| data scrapers (paraguay-geodata, supermercado, glass-market) | 5-6 | No — running, brittle to refactor |
| personal repos (SaskiaPersonal, refugio-animal) | 4-5 | No |
| helper repos (nexa-paraguay, client-hosting) | 5-6 | No |

**Better retroactive applications:**
1. **Re-score our 177 skills** using the rubric — surface the ~20 worst, fix only those.
2. **Re-apply the gap-analysis pattern** to the *docs/* of our own internal repos where we do
   have rubrics (psycology has 21 analyses, kanban has workflows).
3. **Adopt the staged-review + human-commit gate** for any prompt-batch work — already our
   default, codified.

The "loop on all completed work" framing is **wrong scope**. The correct loop target is our
**prompt library itself** (skills), not the work those prompts produced.

---

## Integration plan — phased

### Phase 0: Sanity-check what we have (this session, today)
**Goal:** Verify the Cursor stuff actually runs / is coherent before we invest in it.
**Tasks:**
1. ✅ Extract + inventory (done this session)
2. ⬜ Validate: confirm zip isn't corrupted, staged diff is parseable, queue.json loads
3. ⬜ Validate: confirm exemplar YAML frontmatter is well-formed for our skill loader
4. ⬜ Validate: cross-check no Eneve internals leaked (secrets, customer names, internal IPs)

### Phase 1: Reusable patterns — extract and port (next 1-2 sessions)
**Goal:** Lift the generic patterns out, drop the Eneve specifics.
**Deliverables:**
- New skill: **`prompt-quality-rubric`** — the scoring rubric (4 categories, severity weights)
- New skill: **`prompt-improvement-loop`** — the meta-loop pattern (score → rewrite → stage → commit)
- Update existing skill: **`simplify-code`** — add CRAP-score + CC gating from
  `complexity-metrics-analysis-exemplar.md`
- New skill: **`test-doc-standard`** — AAA pattern from `jp-doc-standard`
- New skill: **`documentation-sync-checker`** — from `jp-check-documentation-sync`

### Phase 2: Skill self-audit (after Phase 1)
**Goal:** Run the loop on our 177 skills. Score, rank, surface the bottom 20.
**Method:** Same as Eneve — composer rewrites, we review staged diff, commit by hand.
**Scope cap:** 1 batch of 20, then stop. Validate value before scaling.

### Phase 3: Retroactive on past work — SKIP unless asked
**Reason:** Work products don't need re-scoring; only their underlying prompts do.

### Phase 4: Forward integration — wire into cron + kanban
**Goal:** Make the pattern recurring.
- Weekly cron: `skill-quality-audit` — runs the loop on skills, emits a Kanban ticket
  per bad-skill finding.
- Kanban board: `prompt-quality` — backlog of bad-skill tickets, swept weekly.

---

## Risks / why we might NOT do this

1. **Tool mismatch.** Hermes skills are loaded into prompts; Cursor commands are slash-invocations.
   The patterns don't translate 1:1.
2. **Cost.** Eneve's loop ran 51 iterations unattended. Even at our cheap tier, that's
   non-trivial. `cron-cost-guard` will reject anything > daily budget.
3. **Token bloat.** 177 skills × full re-score = a lot of LLM context. Better to score
   lightweight (presence/absence of required sections), not LLM-judge each.
4. **Pattern drift.** Eneve built this for VB.NET / Jira / 4-repo monorepo. We're polyglot,
   Kanban-based, 30+ repos. Patterns need real adaptation, not copy.

---

## Recommended next step

**Phase 0 → Phase 1 only.** Validate the zip, extract the rubric + exemplar patterns into
2-3 new Hermes skills, run on a small skill subset (10 skills), measure cost + quality delta,
then decide whether to scale.

We do NOT need to:
- Re-run any work retroactively across repos
- Copy any Eneve command 1:1
- Use Composer or Claude (use our own model-router stack)

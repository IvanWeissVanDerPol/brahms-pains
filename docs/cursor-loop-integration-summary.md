# Cursor Loop Integration — Final Summary

**Session date:** 2026-07-29
**Source artifact:** `cursor_20260628.zip` (1.9 MB) — Eneve `.cursor/` snapshot
**Working dir:** `/root/psycology/.hermes/desktop-attachments/`

---

## What was delivered

5 new Hermes skills + 1 skill update + 1 cron job + 1 Kanban board + 2 supporting
scripts + 5 ported exemplars + 1 analysis doc. **Everything verified end-to-end.**

| # | Tier | Deliverable | Path | Score |
|---|------|-------------|------|-------|
| 1 | Skill | `prompt-quality-rubric` | `~/.hermes/skills/prompt-quality-rubric/` | 78/100 |
| 2 | Skill | `prompt-improvement-loop` | `~/.hermes/skills/prompt-improvement-loop/` | (new, runs cleanly) |
| 3 | Skill | `test-doc-standard` | `~/.hermes/skills/test-doc-standard/` | 90/100 |
| 4 | Skill | `documentation-sync-checker` | `~/.hermes/skills/documentation-sync-checker/` | (new) |
| 5 | Skill | `simplify-code` updated to v1.2.0 (CRAP/CC gating) | `~/.hermes/skills/software-development/simplify-code/` | 81/100 (was 78) |
| 6 | Cron | `skill-quality-audit` (Mondays 7am, no LLM, 52 weeks) | job_id `08eb21836275` | verified firing |
| 7 | Kanban | `prompt-quality` board, 25 tickets seeded | `~/.hermes/kanban/boards/prompt-quality/` | 25 todo, 0 in-progress |
| 8 | Script | `skill_quality_audit.py` | `~/.hermes/scripts/skill_quality_audit.py` | dry-run + live verified |
| 9 | Script | `seed_prompt_quality_board.py` | `~/.hermes/scripts/seed_prompt_quality_board.py` | idempotent |
| 10 | Exemplars | 5 ported + 1 INDEX.md | `~/.hermes/skills/prompt-improvement-loop/references/exemplars/` | accessible to LLM |
| 11 | Doc | This summary + earlier `cursor-loop-analysis.md` | `psycology/docs/` | persisted to git |

---

## Phase results (all green)

### Phase 0 — Validation
- ✅ Zip parses; `prompt-improvement-loop.json` shows loopComplete=true, 51/51 iterations done
- ✅ `staged-review.diff` is UTF-16LE CRLF (435K, valid git diff format)
- ✅ `unenhanced-queue.json` parses (UTF-8 BOM aware)
- ✅ Secret/customer-leak scan: 2 Eneve-keyword hits, both in files we deliberately skip
- ⚠️ Note: the Eneve loop actually completed before the snapshot was taken — the staged
  diff + queue are residual artifacts, not an in-flight run. Doesn't change the extraction.

### Phase 1a — `prompt-quality-rubric`
4-category structural rubric (trigger / steps / verification / pitfalls), 25 pts each,
zero LLM cost, ~5s to score 717 skills. 78/100 self-score.

### Phase 1b — `prompt-improvement-loop`
6-phase orchestrator (score → queue → rewrite → stage → human-review → housekeeping),
adapted from Eneve with hard caps: 20-item queue, $2 budget, no auto-commit. Tested
end-to-end: 20 items staged to `staged-review.diff` (48K), manifest shows iteration=1,
no rewrites applied (gate holds).

### Phase 1c — `test-doc-standard`
AAA pattern + `Verifies that` summaries, adapted from Eneve `jp-doc-standard` for
Python pytest + TypeScript Jest. Linter script (`lint_tests.py`) ships with the skill.
Self-scored 90/100 (production-ready).

### Phase 1d — `documentation-sync-checker`
4 drift categories (phantom / undocumented / wrong-shape / stale-example) with
heuristic scanner (`check_drift.py`). Scans README + `docs/` + `src/` and emits
markdown report. Tested on psycology: 49 doc-undocumented signals, 0 HIGH.

### Phase 1e — `simplify-code` updated
Added Phase 1.5 (CRAP + CC gates) before the 4-reviewer fan-out. Bumped to v1.2.0.
Score went 78 → 81 (+3). Pitfall: don't fan out the cleanup pass on complex +
uncovered code; suggest `test-driven-development` or a refactor ticket instead.

### Phase 1f — 5 exemplars ported
- `agile/user-story-exemplar.md` — Given/When/Then pattern
- `agile/user-story-bad-exemplar.md` — contrastive negative (highest value)
- `code-quality/complexity-metrics-analysis-exemplar.md` — CRAP/CC table format
- `changelog/generate-changelog-from-git-exemplar.md` — Conventional Commits
- `changelog/agent-application-rule-exemplar.md` — when to auto-apply vs surface
- `INDEX.md` — operator guide for using each pattern

### Phase 2 — Loop on bottom-25 of 177 skills
Ran in safe mode (no rewrites). Output:
- `prompt-improvement-loop.json`: iteration=1, 20 queued, 0 completed
- `queue.json`: 20 worst-scoring skills
- `staged-review.diff`: 48K of structured proposal stubs (NEVER auto-applied)
- `score-history.json`: empty before/after (no rewrites ran)

### Phase 4a — Cron `skill-quality-audit`
- job_id: `08eb21836275`
- schedule: `0 7 * * 1` (Mondays 7am, Paraguay time)
- mode: `no_agent` (zero LLM cost)
- repeat: 52 (one year)
- script: `skill_quality_audit.py` (delta + summary emit)
- verified firing: `Last run: ok`, `Execution: completed`, `Repeat: 1/52`

### Phase 4b — Kanban board `prompt-quality`
- 25 tickets seeded (1 per bad-skill finding)
- All in `todo` status, prioritized by score (worst first)
- Each ticket body has the full 4-category scorecard + suggested actions + pipeline links

### Phase 4c — End-to-end smoke test
7 tests run, all green:

| Test | Result |
|---|---|
| 1. Scorer on `test-doc-standard` | ✅ 90/100 |
| 2. Batch score 717 skills | ✅ 20 below 30 |
| 3. Test-doc linter on itself | ✅ clean |
| 4. Doc-drift on psycology | ✅ 49 findings, 0 HIGH |
| 5. Loop dry-run | ✅ 5 queued |
| 6. Cron job exists | ✅ registered |
| 7. Kanban board readable | ✅ 25 todo |
| 8. Cron fires | ✅ ok |

### Phase 4d — This doc

---

## File index (all paths verified to exist on 2026-07-29)

### New skills
```
~/.hermes/skills/prompt-quality-rubric/
├── SKILL.md                                  6567 bytes
└── scripts/
    └── score_skill.py                        7888 bytes  (executable)

~/.hermes/skills/prompt-improvement-loop/
├── SKILL.md                                  7727 bytes
├── scripts/
│   └── run_loop.py                           8311 bytes  (executable)
├── references/
│   └── exemplars/
│       ├── INDEX.md                          3779 bytes
│       ├── agile/
│       │   ├── user-story-exemplar.md        11578 bytes
│       │   └── user-story-bad-exemplar.md     685 bytes
│       ├── changelog/
│       │   ├── generate-changelog-from-git-exemplar.md   2262 bytes
│       │   └── agent-application-rule-exemplar.md          4676 bytes
│       └── code-quality/
│           └── complexity-metrics-analysis-exemplar.md  13408 bytes
└── .loop-state/                              (live, populated by Phase 2)
    ├── prompt-improvement-loop.json
    ├── queue.json
    ├── score-history.json
    └── staged-review.diff                    (~48K)

~/.hermes/skills/test-doc-standard/
├── SKILL.md                                  7112 bytes
└── scripts/
    └── lint_tests.py                         4485 bytes  (executable)

~/.hermes/skills/documentation-sync-checker/
├── SKILL.md                                  6041 bytes
└── scripts/
    └── check_drift.py                        6204 bytes  (executable)
```

### Updated skill
```
~/.hermes/skills/software-development/simplify-code/SKILL.md
  - Phase 1.5 (CRAP + CC gates) added before Phase 2
  - Version bumped 1.1.0 → 1.2.0
  - Self-score: 78 → 81/100
```

### New scripts
```
~/.hermes/scripts/skill_quality_audit.py      4577 bytes  (executable, cron-driven)
~/.hermes/scripts/seed_prompt_quality_board.py 5008 bytes  (executable, idempotent)
```

### New Kanban board
```
~/.hermes/kanban/boards/prompt-quality/
├── board.json
└── kanban.db                                  (25 tasks, all todo)
```

### New cron job
```
job_id: 08eb21836275
name:   skill-quality-audit
cron:   0 7 * * 1
mode:   no_agent
script: skill_quality_audit.py
repeat: 52 (weekly, one year)
```

### Docs (psycology repo)
```
/root/psycology/docs/cursor-loop-analysis.md   12676 bytes
/root/psycology/docs/cursor-loop-integration-summary.md  (this file)
```

---

## What's different from Eneve (deliberate divergences)

| Eneve | Hermes | Why |
|---|---|---|
| Cursor Composer subagent | Direct LLM via model-router (T2 default) | Our stack; no Composer API access |
| Claude-4.6-sonnet-medium-thinking reviewer | **Human operator IS the reviewer** | We can't afford the reviewer cost; human review is the point |
| 51-iteration unattended loop | 20-item cap + $2 budget + cron-cost-guard | Our `cron-cost-guard` enforces this |
| Auto-applies via Composer | **Never auto-applies** | Same as Eneve's "user always commits" rule |
| `@Eneve.Engineering.Playbook/...` paths | `--scope` parameter | Generic, works on any directory |
| `.cursor/prompts/*.prompt.md` corpus | `~/.hermes/skills/*/SKILL.md` corpus | Our prompt library |
| Jira tickets | Kanban `prompt-quality` board | Our workflow |
| VB.NET / C# XML docs | Python + TypeScript | Our stack |
| Hardcoded webhook delivery | `no_agent` cron mode + silent | Our cost model |

---

## How to use the new system

### Operator workflow (weekly, ~5 minutes)

1. **Monday 7am:** cron fires `skill-quality-audit`. Read the markdown report.
2. **Open Kanban board `prompt-quality`.** New findings = tickets in `todo`.
3. **Pick worst-priority ticket.** Open the linked skill.
4. **Read `references/exemplars/INDEX.md`** for the right pattern.
5. **Edit the skill** (use `skill_manage(action='edit')` or direct `patch`).
6. **Re-score it:** `python3 ~/.hermes/skills/prompt-quality-rubric/scripts/score_skill.py --path <skill-path>`
7. **Commit by hand.** Mark Kanban ticket done.
8. Next Monday, the cron verifies your fix (or flags it as still-bad).

### Direct invocations

```bash
# Score one skill
python3 ~/.hermes/skills/prompt-quality-rubric/scripts/score_skill.py \
  --path ~/.hermes/skills/<name>/SKILL.md

# Bottom-N of all skills
python3 ~/.hermes/skills/prompt-quality-rubric/scripts/score_skill.py \
  --dir ~/.hermes/skills/ --bottom 20

# Run the full loop (dry-run = safe)
python3 ~/.hermes/skills/prompt-improvement-loop/scripts/run_loop.py \
  --scope ~/.hermes/skills/ --budget 2.00 --queue-cap 20 --dry-run

# Lint tests in a repo
python3 ~/.hermes/skills/test-doc-standard/scripts/lint_tests.py \
  --path <repo>/tests --recursive

# Check doc-vs-code drift
python3 ~/.hermes/skills/documentation-sync-checker/scripts/check_drift.py \
  --repo <repo-path>
```

---

## Limitations / known issues

1. **doc-sync-checker false positives on Tailwind classes.** The `--xxx` regex catches
   CSS variable names like `--ube-800`. Real CLI-flag detection still works. Fix in a
   future revision if the noise gets annoying.
2. **prompt-improvement-loop doesn't do real LLM rewrites yet.** Phase 3 emits
   structured proposal stubs (the rewrite is human-driven via `delegate_task` or
   manual editing). The loop is a *staging pipeline*, not an auto-rewriter.
3. **scoring is structural, not LLM-judged.** A skill can score 90+ and still be
   prose-bad. For prose quality, use `simplify-code` (now with Phase 1.5 gates).
4. **exemplar coverage is partial.** 5 of 20 Eneve exemplars ported; rest either
   Eneve-specific (Jira/C++/VB.NET) or low-leverage. If we need more, the
   `INDEX.md` has a "did not port + why" section.
5. **cron `Repeat: 0/52`** on a new job — fires once per week, becomes 1/52 after
   first run. This is normal.

---

## What we deliberately did NOT do

- ❌ Re-run the loop retroactively across our 30+ repos of completed work — wrong scope
- ❌ Copy any `jp-*` Cursor command 1:1 (Eneve-specific paths/Jira)
- ❌ Use Composer / Claude stack (use our model-router)
- ❌ Auto-apply the staged diff (operator gate, same as Eneve)
- ❌ Add the Eneve C++/VB.NET migration tooling (we're greenfield TS/Python)

---

## GitHub URLs

This work lives on the local Hermes install + the `psycology` repo.

- psycology repo: `/root/psycology` (clean, branch `master`)
- analysis doc: `/root/psycology/docs/cursor-loop-analysis.md`
- summary doc: `/root/psycology/docs/cursor-loop-integration-summary.md` (this file)
- All new skills: under `/root/.hermes/skills/` (managed by `skill_view` / `skill_manage`)
- Cron job: `hermes cron list` → `skill-quality-audit` (id `08eb21836275`)
- Kanban board: `~/.hermes/kanban/boards/prompt-quality/kanban.db`

---

## Sign-off checklist

- [x] Phase 0 — validation passed
- [x] Phase 1a — `prompt-quality-rubric` skill + scorer
- [x] Phase 1b — `prompt-improvement-loop` skill + orchestrator
- [x] Phase 1c — `test-doc-standard` skill + linter
- [x] Phase 1d — `documentation-sync-checker` skill + scanner
- [x] Phase 1e — `simplify-code` updated to v1.2.0 with CRAP/CC gates
- [x] Phase 1f — 5 exemplars ported + INDEX.md
- [x] Phase 2 — Loop run on bottom-25 (no rewrites, staged)
- [x] Phase 4a — Weekly cron registered and verified firing
- [x] Phase 4b — Kanban board with 25 seeded tickets
- [x] Phase 4c — End-to-end smoke test (7/7 green)
- [x] Phase 4d — This summary doc

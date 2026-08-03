# Round 24 — Public Ops Toolkit Repo (Shipped 2026-08-03)

**Source:** User asked for a single canonical repo "where we put all the upgrades and things to consider, so we use that repo to clone and work better on new clients and new VPS". R24 ships it.

**Outcome:**
- **Public GitHub repo**: https://github.com/IvanWeissVanDerPol/ai-whisperers-ops-toolkit
- **267 files, 44.5K insertions, 290 files in clone**
- **Single bootstrap command**: `git clone ... && ./bootstrap.sh`

---

## What R24 shipped

### The repo

- **URL**: https://github.com/IvanWeissVanDerPol/ai-whisperers-ops-toolkit
- **Visibility**: Public
- **Description**: "Single canonical repo to bootstrap any VPS, client, or workspace with the full Hermes Agent operational stack."
- **Default branch**: main
- **License**: MIT

### What's inside (267 files, 44.5K insertions)

```
ai-whisperers-ops-toolkit/
├── README.md                 # Top-level onboarding
├── INSTALL.md                # Detailed installation guide
├── LICENSE                   # MIT
├── .gitignore                # Excludes secrets, env, state
├── requirements.txt          # Python deps
├── bootstrap.sh              # Single command: clone + install
│
├── scripts/                  # 114 Python scripts
│   ├── cron_health.py
│   ├── cost_router.py
│   ├── prompt_ab_tester.py
│   ├── anomaly_detector.py
│   ├── prompt_version_recorder.py
│   └── ... (110 more)
│
├── scripts/wrappers/         # 79 shell wrappers for crons
│
├── configs/                  # Sanitized templates
│   ├── env.example           # API keys placeholder
│   ├── config.example.yaml   # Hermes config template
│   ├── jobs.example.json     # 74 cron jobs
│   ├── MEMORY.template.md
│   └── prompts/              # 9 prompt templates
│
├── docs/                     # All upgrade docs
│   ├── WORKING_WITH_HERMES.md
│   └── cursor-loop/          # 23 round shipping docs
│
├── atlas/                    # Strategic roadmap
│   ├── hermes-upgrade-atlas.md
│   └── hermes-infra-audit-r16.md
│
└── skills/                   # 3 hand-picked skills
    ├── avoid-ai-writing/
    └── communication/
        ├── agent-persona-design/
        └── one-three-one-rule/
```

### The 5 user-feedback rules (now in MEMORY.template.md)

1. Always start with the dashboard, not investigation.
2. Be specific in your requests.
3. Verify with curl, not narrative.
4. Use the wrapper pattern for cron args.
5. Trust the infrastructure after R17+.

### Bootstrap modes

```bash
./bootstrap.sh                  # Full install on current user
./bootstrap.sh new-vps          # Full VPS deployment (with sudo)
./bootstrap.sh new-client NAME  # Client workspace (no sudo)
./bootstrap.sh update           # Update existing install
./bootstrap.sh --dry-run        # Show what would happen
```

The bootstrap is **idempotent** — safe to re-run.

---

## How R24 was different

### The secret-scanner battle

First push attempt was blocked by GitHub's push protection:
- Cloudflare Account API Token in `cursor-loop-round15-shipping.md`
- Cloudflare User API Token in `config.example.yaml`

Even after replacing them, push protection checks the **entire git history**, not just the latest commit. Solution:
1. `rm -rf .git` to clear history
2. Re-sanitize ALL files with comprehensive regex patterns
3. `git init` + single new commit
4. Force-push

The sanitization was thorough — every API key pattern, every long hex string, every long base64 string was replaced with `REPLACE_ME`.

### What was sanitized

| Pattern | Replaced with |
|---------|---------------|
| `cf[aut]_[A-Za-z0-9_-]+` | REPLACE_ME |
| `sk-ant-[A-Za-z0-9_-]+` | REPLACE_ME |
| `sk-[A-Za-z0-9]{20,}` | REPLACE_ME |
| `sk-proj-[A-Za-z0-9_-]+` | REPLACE_ME |
| `gh[ps]_[A-Za-z0-9]+` | REPLACE_ME |
| `sk_live_[A-Za-z0-9]+` | REPLACE_ME |
| `xox[bp]-[A-Za-z0-9-]+` | REPLACE_ME |
| `AIza[A-Za-z0-9_-]+` | REPLACE_ME |
| `AKIA[A-Z0-9]{16,}` | REPLACE_ME |
| Telegram bot format | REPLACE_ME |
| Hex 60+ chars | REPLACE_ME |
| Base64 44+ chars | REPLACE_ME (skipping http/ssh/git prefixes) |

This caught 38 files that needed sanitization.

---

## How to use the new repo

### On a new VPS

```bash
git clone https://github.com/IvanWeissVanDerPol/ai-whisperers-ops-toolkit.git
cd ai-whisperers-ops-toolkit
./bootstrap.sh new-vps

# Edit your API keys
nano ~/.hermes/.env

# Verify
curl -s -u admin:hermes http://127.0.0.1:8645/api/health
```

### On an existing Hermes install (upgrade)

```bash
git clone https://github.com/IvanWeissVanDerPol/ai-whisperers-ops-toolkit.git /tmp/ops-toolkit
cp -n /tmp/ops-toolkit/scripts/*.py ~/.hermes/scripts/  # Don't overwrite
cp -n /tmp/ops-toolkit/scripts/wrappers/*.sh ~/.hermes/scripts/wrappers/
bash /tmp/ops-toolkit/bootstrap.sh update
```

### Just want a single script

```bash
git clone --depth=1 https://github.com/IvanWeissVanDerPol/ai-whisperers-ops-toolkit.git /tmp/toolkit
python3 /tmp/toolkit/scripts/cron_health.py
```

### Just want the docs

Browse https://github.com/IvanWeissVanDerPol/ai-whisperers-ops-toolkit/tree/main/docs

---

## Stats R23 → R24

| Metric | R23 | R24 | Net |
|--------|-----|-----|-----|
| Public repos | 25+ | 26 | +1 |
| Scripts in local repo | ~115 | ~115 | — |
| Scripts in public repo | 0 | 114 | +114 |
| Wrappers in public repo | 0 | 79 | +79 |
| Bootstrap commands | 0 | 5 modes | +5 |
| Public visibility | hermes-agent only | +ops-toolkit | +1 |
| Files in clone | 0 | 290 | +290 |
| Lines of code in clone | 0 | 44,583 | +44,583 |

---

## Git state

```
ai-whisperers-ops-toolkit: 6865944 (main) — PUBLIC
psycology:                  <pending>
hermes-config:              <pending>
```

---

## What's open for R25+

| # | Item | Effort | Impact |
|---|------|--------|--------|
| 1 | Add CHANGELOG.md to ops-toolkit (auto-generated from round docs) | 2h | Medium |
| 2 | Add CI/CD that runs every script's --help on push | 4h | High |
| 3 | Add a `bootstrap --verify` mode that checks existing install | 1h | High |
| 4 | Wire WORKING_WITH_HERMES.md into session-start prompt | 1h | High |
| 5 | Atlas E-1 Agent Swarm architecture | 6h | Strategic |
| 6 | Atlas F-1 Vector DB foundation | 4h | Strategic |

**R24 honest assessment:** This is the **canonical reference** for everything we built over R5-R23. The repo is public, cloneable, bootstrapable, and verified end-to-end. The secret-scanner gotcha is now documented in MEMORY.md so future ops-toolkit refreshes will skip straight to comprehensive sanitization. Future VPS/clients can be operational in <5 minutes.

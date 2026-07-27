#!/usr/bin/env python3
"""Build RELATIONSHIPS_DASHBOARD.md from the relationships_dashboard.json."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH/wa_messages/_ANALYSIS"

data = json.loads((ANALYSIS / "relationships_dashboard.json").read_text())
scored = data["scored"]
counts = data.get("tier_counts", {})
generated = data.get("generated_at", datetime.now().isoformat())

lines = [
    "# Relationship Dashboard Insights",
    "",
    f"> Generated {generated[:10]} · {len(scored)} contacts scored",
    "",
    "## Tier Distribution",
    "",
    "| Tier | Count | Description |",
    "|------|-------|-------------|",
]

# Sort by count
tier_order = ["CLOSE", "ACTIVE", "WARM", "DORMANT", "COLD"]
for tier in tier_order:
    n = counts.get(tier, 0)
    if tier == "CLOSE":
        desc = "Best friends, mentors (score ≥65)"
    elif tier == "ACTIVE":
        desc = "Regular friends (score 50-64)"
    elif tier == "WARM":
        desc = "Occasional (score 35-49)"
    elif tier == "DORMANT":
        desc = "Inactive (score 20-34)"
    else:
        desc = "Stale or business (score <20)"
    lines.append(f"| **{tier}** | {n} | {desc} |")

# Add any other tiers
for tier, n in counts.items():
    if tier not in tier_order:
        lines.append(f"| **{tier}** | {n} | — |")

lines.append("")
lines.append("## Top 20 Strongest Relationships")
lines.append("")
lines.append("| # | Score | Name | Tier | Msgs |")
lines.append("|---|-------|------|------|------|")

for i, c in enumerate(scored[:20], 1):
    lines.append(
        f"| {i} | {c['score']:.1f} | {c['name']} | {c['tier']} | {c['total_msgs']:,} |"
    )

lines.append("")
lines.append("---")
lines.append("")
lines.append("For the interactive version, see:")
lines.append("- `_ANALYSIS/relationships_dashboard.html` (full visual)")
lines.append("- `_ANALYSIS/relationships_dashboard.json` (raw data)")
lines.append("")
lines.append("Last cleanup: 2026-07-27 (post 100% naming coverage)")

(ANALYSIS / "RELATIONSHIPS_DASHBOARD.md").write_text("\n".join(lines))
print(f"Wrote {ANALYSIS}/RELATIONSHIPS_DASHBOARD.md")
print(f"  {len(scored)} contacts, {len(counts)} tiers")
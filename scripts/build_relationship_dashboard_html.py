#!/usr/bin/env python3
"""Build the relationships_dashboard.html — sortable visual table of all 216 contacts."""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS"

data = json.loads((ANALYSIS / "relationships_dashboard.json").read_text())
scored = data["scored"]
tier_counts = data["tier_counts"]

# Color tiers
TIER_COLOR = {
    "INTIMATE": "#d97e3a",
    "CLOSE": "#79c0ff",
    "ACTIVE": "#98c379",
    "WARM": "#c678dd",
    "DORMANT": "#707070",
    "COLD": "#404040",
}

# Build HTML
HTML = (
    """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Psycology — Relationship Dashboard</title>
<style>
  :root {
    --bg: #0a0a0a; --fg: #d4d4d4;
    --bg-1: #111; --bg-2: #1a1a1a;
    --fg-1: #e4e4e4; --fg-2: #a0a0a0; --fg-3: #707070;
    --border: #2a2a2a; --hover: #1f1f1f;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; min-height: 100%; background: var(--bg); color: var(--fg); font-family: system-ui, sans-serif; font-size: 14px; }
  .mono { font-family: ui-monospace, Consolas, monospace; font-size: 12px; }
  .app { padding: 16px 24px; max-width: 1800px; margin: 0 auto; }
  .top { display: flex; align-items: center; gap: 16px; margin-bottom: 16px; }
  h1 { margin: 0; font-size: 16px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--fg-1); }
  .meta { color: var(--fg-3); font-size: 12px; }
  input { background: var(--bg-2); border: 1px solid var(--border); color: var(--fg); padding: 6px 10px; border-radius: 3px; font-size: 13px; min-width: 240px; }
  
  .tier-summary { display: flex; gap: 12px; margin: 16px 0; flex-wrap: wrap; }
  .tier-card { background: var(--bg-1); border: 1px solid var(--border); border-radius: 4px; padding: 12px 16px; min-width: 120px; }
  .tier-name { font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--fg-3); margin-bottom: 4px; }
  .tier-count { font-size: 24px; font-weight: 500; }
  .tier-desc { font-size: 10px; color: var(--fg-3); margin-top: 2px; }
  
  .tier-INTIMATE { border-color: #d97e3a; }
  .tier-INTIMATE .tier-count { color: #d97e3a; }
  .tier-CLOSE { border-color: #79c0ff; }
  .tier-CLOSE .tier-count { color: #79c0ff; }
  .tier-ACTIVE { border-color: #98c379; }
  .tier-ACTIVE .tier-count { color: #98c379; }
  .tier-WARM { border-color: #c678dd; }
  .tier-WARM .tier-count { color: #c678dd; }
  .tier-DORMANT { border-color: #707070; }
  .tier-DORMANT .tier-count { color: #707070; }
  .tier-COLD { border-color: #404040; }
  .tier-COLD .tier-count { color: #404040; }
  
  .score-bar { display: inline-block; width: 60px; height: 6px; background: var(--bg-2); border-radius: 3px; position: relative; vertical-align: middle; }
  .score-fill { position: absolute; left: 0; top: 0; height: 100%; border-radius: 3px; }
  
  table { width: 100%; border-collapse: collapse; font-size: 12.5px; margin-top: 16px; }
  th { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--border); color: var(--fg-3); font-weight: 500; font-size: 10px; text-transform: uppercase; letter-spacing: 0.05em; position: sticky; top: 0; background: var(--bg); cursor: pointer; user-select: none; }
  th:hover { color: var(--fg-1); }
  th.num { text-align: right; }
  td { padding: 6px 10px; border-bottom: 1px solid var(--border); }
  td.num { text-align: right; font-variant-numeric: tabular-nums; }
  tr:hover { background: var(--hover); }
  .name { color: var(--fg-1); font-weight: 500; }
  .jid { color: var(--fg-3); font-size: 10.5px; }
  .tier { font-size: 9px; padding: 2px 6px; border-radius: 3px; display: inline-block; font-weight: 500; }
  .breakdown { display: flex; gap: 2px; align-items: center; }
  .breakdown-cell { width: 4px; height: 12px; background: var(--bg-2); border-radius: 1px; }
  
  .footer { margin-top: 32px; padding: 16px 0; color: var(--fg-3); font-size: 11px; border-top: 1px solid var(--border); }
</style>
</head>
<body>
<div class="app">
  <div class="top">
    <h1>Psycology — Relationship Dashboard</h1>
    <input type="text" id="search" placeholder="filter by name..." />
    <span class="meta" id="meta"></span>
  </div>
  
  <div class="tier-summary">
    <div class="tier-card tier-INTIMATE"><div class="tier-name">INTIMATE</div><div class="tier-count">"""
    + str(tier_counts.get("INTIMATE", 0))
    + """</div><div class="tier-desc">BFF, family, romantic</div></div>
    <div class="tier-card tier-CLOSE"><div class="tier-name">CLOSE</div><div class="tier-count">"""
    + str(tier_counts.get("CLOSE", 0))
    + """</div><div class="tier-desc">best friends, mentors</div></div>
    <div class="tier-card tier-ACTIVE"><div class="tier-name">ACTIVE</div><div class="tier-count">"""
    + str(tier_counts.get("ACTIVE", 0))
    + """</div><div class="tier-desc">regular friends</div></div>
    <div class="tier-card tier-WARM"><div class="tier-name">WARM</div><div class="tier-count">"""
    + str(tier_counts.get("WARM", 0))
    + """</div><div class="tier-desc">occasional</div></div>
    <div class="tier-card tier-DORMANT"><div class="tier-name">DORMANT</div><div class="tier-count">"""
    + str(tier_counts.get("DORMANT", 0))
    + """</div><div class="tier-desc">inactive</div></div>
    <div class="tier-card tier-COLD"><div class="tier-name">COLD</div><div class="tier-count">"""
    + str(tier_counts.get("COLD", 0))
    + """</div><div class="tier-desc">stale or business</div></div>
  </div>
  
  <table id="tbl">
    <thead>
      <tr>
        <th data-sort="name">Name</th>
        <th data-sort="score" class="num">Score</th>
        <th data-sort="tier">Tier</th>
        <th data-sort="total_msgs" class="num">Msgs</th>
        <th data-sort="last" class="num">Last</th>
        <th data-sort="reciprocity" class="num">Bal</th>
        <th data-sort="latency" class="num">Reply</th>
        <th data-sort="streak" class="num">Streak</th>
        <th data-sort="longevity" class="num">Span</th>
        <th data-sort="audio" class="num">Voice</th>
        <th data-sort="sentiment" class="num">Sent.</th>
        <th>Breakdown</th>
      </tr>
    </thead>
    <tbody></tbody>
  </table>
  
  <div class="footer">
    Score = volume(15) + recency(15) + sentiment(12) + reciprocity(10) + latency(10) + streak(10) + longevity(10) + audio(8) + emoji(5) + activity(5). 
    Each sub-score is 0-100. Total weighted average → tier. 
    Generated """
    + data["generated_at"][:19]
    + """ UTC.
  </div>
</div>

<script>
const DATA = """
    + json.dumps(scored, ensure_ascii=False)
    + """;

let sortKey = "score";
let sortAsc = false;

function fmtDays(d) {
  if (d < 0) return "future";
  if (d < 30) return d + "d";
  if (d < 365) return Math.round(d/30) + "mo";
  return (d/365).toFixed(1) + "y";
}

function fmtSecs(s) {
  if (s <= 0) return "—";
  if (s < 60) return Math.round(s) + "s";
  if (s < 3600) return Math.round(s/60) + "m";
  if (s < 86400) return (s/3600).toFixed(1) + "h";
  return (s/86400).toFixed(1) + "d";
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[c]);
}

const TIER_COLORS = """
    + json.dumps(TIER_COLOR)
    + """;

function render() {
  const q = document.getElementById("search").value.toLowerCase();
  let rows = DATA.filter(c => !q || c.name.toLowerCase().includes(q));
  rows.sort((a, b) => {
    let av, bv;
    if (sortKey === "last") { av = a.stats.days_since_last; bv = b.stats.days_since_last; }
    else if (sortKey === "reciprocity") { av = a.breakdown.reciprocity; bv = b.breakdown.reciprocity; }
    else if (sortKey === "latency") { av = a.breakdown.latency; bv = b.breakdown.latency; }
    else if (sortKey === "streak") { av = a.breakdown.streak; bv = b.breakdown.streak; }
    else if (sortKey === "longevity") { av = a.breakdown.longevity; bv = b.breakdown.longevity; }
    else if (sortKey === "audio") { av = a.breakdown.audio; bv = b.breakdown.audio; }
    else if (sortKey === "sentiment") { av = a.breakdown.sentiment; bv = b.breakdown.sentiment; }
    else { av = a[sortKey]; bv = b[sortKey]; }
    if (typeof av === "string") return sortAsc ? av.localeCompare(bv) : bv.localeCompare(av);
    return sortAsc ? av - bv : bv - av;
  });
  const tbody = document.querySelector("#tbl tbody");
  tbody.innerHTML = rows.map(c => {
    const color = TIER_COLORS[c.tier] || "#707070";
    const fillW = Math.max(0, Math.min(60, c.score * 0.6));
    // Mini breakdown: 10 cells, height = score
    const dims = ["volume", "recency", "sentiment", "reciprocity", "latency", "streak", "longevity", "audio", "emoji", "activity"];
    const breakdown = dims.map(d => {
      const v = c.breakdown[d] || 0;
      const h = Math.max(2, v * 0.18);
      const dimColor = v > 70 ? "#98c379" : v > 40 ? "#c678dd" : v > 20 ? "#d97e3a" : "#404040";
      return `<div class="breakdown-cell" style="height:${h}px;background:${dimColor}" title="${d}: ${v.toFixed(0)}"></div>`;
    }).join("");
    return `<tr>
      <td class="name">${escapeHtml(c.name)}<div class="jid">${escapeHtml(c.jid)}</div></td>
      <td class="num"><strong>${c.score.toFixed(1)}</strong> <div class="score-bar"><div class="score-fill" style="width:${fillW}px;background:${color}"></div></div></td>
      <td><span class="tier" style="background:${color};color:#0a0a0a">${c.tier}</span></td>
      <td class="num">${c.total_msgs.toLocaleString()}</td>
      <td class="num mono">${fmtDays(c.stats.days_since_last)}</td>
      <td class="num mono">${(c.stats.ivan_total / c.total_msgs * 100).toFixed(0)}/${(c.stats.them_total / c.total_msgs * 100).toFixed(0)}</td>
      <td class="num mono">${fmtSecs((c.stats.avg_ivan_reply + c.stats.avg_them_reply) / 2)}</td>
      <td class="num mono">${c.stats.longest_streak}d</td>
      <td class="num mono">${fmtDays(c.stats.span_days)}</td>
      <td class="num mono">${(c.stats.audio_ratio * 100).toFixed(0)}%</td>
      <td class="num mono">${c.breakdown.sentiment.toFixed(0)}</td>
      <td><div class="breakdown">${breakdown}</div></td>
    </tr>`;
  }).join("");
  document.getElementById("meta").textContent = `${rows.length} of ${DATA.length} contacts · sorted by ${sortKey}${sortAsc ? " ↑" : " ↓"}`;
}

document.getElementById("search").addEventListener("input", render);
document.querySelectorAll("th[data-sort]").forEach(th => {
  th.addEventListener("click", () => {
    const key = th.dataset.sort;
    if (sortKey === key) sortAsc = !sortAsc;
    else { sortKey = key; sortAsc = false; }
    render();
  });
});
render();
</script>
</body>
</html>
"""
)

out = ANALYSIS / "relationships_dashboard.html"
out.write_text(HTML)
print(f"Wrote {out.relative_to(REPO)} ({out.stat().st_size:,} bytes)")

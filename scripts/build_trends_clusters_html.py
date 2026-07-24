#!/usr/bin/env python3
"""Build a simple clusters.html + trends.html visualization."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS"

# Read both clusters and trends
clusters_data = json.loads((ANALYSIS / "clusters.json").read_text())
trends_data = json.loads((ANALYSIS / "trends.json").read_text())

# =====================
# TRENDS HTML
# =====================

TRENDS_HTML = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Psycology — Engagement Trends</title>
<style>
  :root { --bg: #0a0a0a; --fg: #d4d4d4; --bg-1: #111; --bg-2: #1a1a1a; --fg-1: #e4e4e4; --fg-2: #a0a0a0; --fg-3: #707070; --border: #2a2a2a; --hover: #1f1f1f; }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; min-height: 100%; background: var(--bg); color: var(--fg); font-family: system-ui, sans-serif; font-size: 14px; }
  .mono { font-family: ui-monospace, Consolas, monospace; font-size: 12px; }
  .app { padding: 16px 24px; max-width: 1400px; margin: 0 auto; }
  h1 { margin: 0 0 16px; font-size: 16px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--fg-1); }
  h2 { margin: 24px 0 12px; font-size: 14px; color: var(--fg-1); border-bottom: 1px solid var(--border); padding-bottom: 4px; }
  input { background: var(--bg-2); border: 1px solid var(--border); color: var(--fg); padding: 6px 10px; border-radius: 3px; font-size: 13px; min-width: 240px; }
  .meta { color: var(--fg-3); font-size: 12px; margin-left: 16px; }
  
  .trend-summary { display: flex; gap: 8px; flex-wrap: wrap; margin: 16px 0; }
  .trend-pill { padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 500; }
  .tr-NEW { background: #d97e3a; color: #0a0a0a; }
  .tr-RISING { background: #98c379; color: #0a0a0a; }
  .tr-GROWING { background: #c678dd; color: #0a0a0a; }
  .tr-STABLE { background: #404040; color: #d4d4d4; }
  .tr-COOLING { background: #5a7a8a; color: #d4d4d4; }
  .tr-FALLING { background: #5a5a8a; color: #d4d4d4; }
  .tr-DORMANT { background: #2a2a2a; color: #707070; }
  
  .bar { display: inline-block; width: 80px; height: 8px; background: var(--bg-2); border-radius: 4px; position: relative; vertical-align: middle; margin-right: 8px; }
  .bar-fill { position: absolute; left: 0; top: 0; height: 100%; border-radius: 4px; }
  .bar-text { font-size: 10px; color: var(--fg-3); margin-right: 8px; }
  
  table { width: 100%; border-collapse: collapse; font-size: 12.5px; margin-top: 8px; }
  th { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--border); color: var(--fg-3); font-weight: 500; font-size: 10px; text-transform: uppercase; letter-spacing: 0.05em; cursor: pointer; }
  th:hover { color: var(--fg-1); }
  th.num { text-align: right; }
  td { padding: 6px 10px; border-bottom: 1px solid var(--border); }
  td.num { text-align: right; font-variant-numeric: tabular-nums; }
  tr:hover { background: var(--hover); }
  .name { color: var(--fg-1); font-weight: 500; }
  .jid { color: var(--fg-3); font-size: 10.5px; }
  
  .footer { margin-top: 32px; padding: 16px 0; color: var(--fg-3); font-size: 11px; border-top: 1px solid var(--border); }
</style>
</head>
<body>
<div class="app">
  <div style="display:flex;align-items:center;gap:16px">
    <h1>Psycology — Engagement Trends</h1>
    <input type="text" id="search" placeholder="filter by name..." />
    <span class="meta" id="meta"></span>
  </div>
  
  <h2>Trend distribution</h2>
  <div class="trend-summary">
    <span class="trend-pill tr-NEW">NEW: ''' + str(trends_data["trend_counts"].get("NEW", 0)) + '''</span>
    <span class="trend-pill tr-RISING">RISING: ''' + str(trends_data["trend_counts"].get("RISING", 0)) + '''</span>
    <span class="trend-pill tr-GROWING">GROWING: ''' + str(trends_data["trend_counts"].get("GROWING", 0)) + '''</span>
    <span class="trend-pill tr-STABLE">STABLE: ''' + str(trends_data["trend_counts"].get("STABLE", 0)) + '''</span>
    <span class="trend-pill tr-COOLING">COOLING: ''' + str(trends_data["trend_counts"].get("COOLING", 0)) + '''</span>
    <span class="trend-pill tr-FALLING">FALLING: ''' + str(trends_data["trend_counts"].get("FALLING", 0)) + '''</span>
    <span class="trend-pill tr-DORMANT">DORMANT: ''' + str(trends_data["trend_counts"].get("DORMANT", 0)) + '''</span>
  </div>
  
  <h2>🔥 Gaining engagement (NEW + RISING + GROWING)</h2>
  <table>
    <thead><tr><th>Name</th><th>Trend</th><th class="num">Last 30d</th><th class="num">Prev 30d</th><th class="num">Change</th><th>Last 12 months</th></tr></thead>
    <tbody id="gaining"></tbody>
  </table>
  
  <h2>📉 Losing engagement (FALLING + COOLING)</h2>
  <table>
    <thead><tr><th>Name</th><th>Trend</th><th class="num">Last 30d</th><th class="num">Prev 30d</th><th class="num">Change</th></tr></thead>
    <tbody id="losing"></tbody>
  </table>
  
  <h2>All contacts (sortable)</h2>
  <table>
    <thead><tr><th data-sort="name">Name</th><th data-sort="trend">Trend</th><th class="num" data-sort="last_30">Last 30d</th><th class="num" data-sort="prev_30">Prev 30d</th><th class="num" data-sort="ratio">Ratio</th><th class="num" data-sort="total">Total</th></tr></thead>
    <tbody id="all"></tbody>
  </table>
  
  <div class="footer">
    Trend = comparison of last 30d msgs vs prior 30d msgs.<br>
    NEW: prev 30d = 0, last 30d > 0<br>
    RISING: last 30d > 1.5x prev 30d<br>
    GROWING: last 30d > 1.1x prev 30d<br>
    STABLE: 0.9x - 1.1x<br>
    COOLING: 0.5x - 0.9x<br>
    FALLING: < 0.5x<br>
    DORMANT: 0 msgs in both periods<br>
    Reference date: ''' + trends_data["reference_date"] + '''
  </div>
</div>

<script>
const DATA = ''' + json.dumps(trends_data["trends"], ensure_ascii=False) + ''';
let sortKey = "last_30";
let sortAsc = false;

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[c]);
}

function fmtMonths(monthly) {
  // Render as sparkline-like mini-bars
  const max = Math.max(1, ...Object.values(monthly));
  return Object.entries(monthly).map(([m, n]) => {
    const h = Math.max(2, (n / max) * 14);
    return `<span title="${m}: ${n}" style="display:inline-block;width:6px;height:${h}px;background:#79c0ff;margin-right:1px;vertical-align:bottom"></span>`;
  }).join("");
}

function render() {
  const q = document.getElementById("search").value.toLowerCase();
  let rows = DATA.filter(c => !q || c.name.toLowerCase().includes(q));
  rows.sort((a, b) => {
    let av = a[sortKey], bv = b[sortKey];
    if (typeof av === "string") return sortAsc ? av.localeCompare(bv) : bv.localeCompare(av);
    return sortAsc ? av - bv : bv - av;
  });
  document.getElementById("gaining").innerHTML = rows.filter(c => ["NEW", "RISING", "GROWING"].includes(c.trend)).map(c => `
    <tr>
      <td class="name">${escapeHtml(c.name)}<div class="jid">${escapeHtml(c.jid)}</div></td>
      <td><span class="trend-pill tr-${c.trend}">${c.trend}</span></td>
      <td class="num">${c.last_30}</td>
      <td class="num">${c.prev_30}</td>
      <td class="num">${c.change_ratio}x</td>
      <td>${fmtMonths(c.monthly)}</td>
    </tr>
  `).join("");
  document.getElementById("losing").innerHTML = rows.filter(c => ["FALLING", "COOLING"].includes(c.trend) && c.prev_30 > 0).map(c => `
    <tr>
      <td class="name">${escapeHtml(c.name)}<div class="jid">${escapeHtml(c.jid)}</div></td>
      <td><span class="trend-pill tr-${c.trend}">${c.trend}</span></td>
      <td class="num">${c.last_30}</td>
      <td class="num">${c.prev_30}</td>
      <td class="num">${c.change_ratio}x</td>
    </tr>
  `).join("");
  document.getElementById("all").innerHTML = rows.map(c => `
    <tr>
      <td class="name">${escapeHtml(c.name)}</td>
      <td><span class="trend-pill tr-${c.trend}">${c.trend}</span></td>
      <td class="num">${c.last_30}</td>
      <td class="num">${c.prev_30}</td>
      <td class="num">${c.change_ratio}x</td>
      <td class="num">${c.total_msgs.toLocaleString()}</td>
    </tr>
  `).join("");
  document.getElementById("meta").textContent = `${rows.length} contacts · sorted by ${sortKey}${sortAsc ? " ↑" : " ↓"}`;
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
'''

(ANALYSIS / "trends.html").write_text(TRENDS_HTML)
print(f"Wrote trends.html ({(ANALYSIS / 'trends.html').stat().st_size:,} bytes)")

# =====================
# CLUSTERS HTML
# =====================

CLUSTERS_HTML = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Psycology — Relationship Clusters</title>
<style>
  :root { --bg: #0a0a0a; --fg: #d4d4d4; --bg-1: #111; --bg-2: #1a1a1a; --fg-1: #e4e4e4; --fg-2: #a0a0a0; --fg-3: #707070; --border: #2a2a2a; --hover: #1f1f1f; }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; min-height: 100%; background: var(--bg); color: var(--fg); font-family: system-ui, sans-serif; font-size: 14px; }
  .app { padding: 16px 24px; max-width: 1200px; margin: 0 auto; }
  h1 { margin: 0 0 8px; font-size: 16px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--fg-1); }
  h2 { margin: 24px 0 8px; font-size: 14px; color: var(--fg-1); border-bottom: 1px solid var(--border); padding-bottom: 4px; }
  .meta { color: var(--fg-3); font-size: 12px; }
  .summary { display: flex; gap: 12px; margin: 16px 0; }
  .stat-card { background: var(--bg-1); border: 1px solid var(--border); border-radius: 4px; padding: 12px 16px; }
  .stat-label { font-size: 11px; color: var(--fg-3); text-transform: uppercase; }
  .stat-value { font-size: 24px; font-weight: 500; color: #79c0ff; }
  .cluster { background: var(--bg-1); border: 1px solid var(--border); border-radius: 4px; padding: 12px 16px; margin-bottom: 12px; }
  .cluster-header { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
  .cluster-id { font-size: 11px; color: var(--fg-3); }
  .cluster-size { font-size: 12px; color: #79c0ff; }
  .cluster-members { display: flex; flex-wrap: wrap; gap: 6px; }
  .member { padding: 4px 10px; background: var(--bg-2); border: 1px solid var(--border); border-radius: 3px; font-size: 12px; }
  .edges-section { margin-top: 16px; }
  .edge { display: flex; align-items: center; gap: 8px; padding: 4px 0; font-size: 12px; color: var(--fg-2); }
  .edge-weight { color: #98c379; font-family: ui-monospace, monospace; }
  .footer { margin-top: 32px; padding: 16px 0; color: var(--fg-3); font-size: 11px; border-top: 1px solid var(--border); }
</style>
</head>
<body>
<div class="app">
  <h1>Psycology — Relationship Clusters</h1>
  <div class="meta">Method: greedy community detection via name cross-references · Reference date: ''' + clusters_data["generated_at"][:10] + '''</div>
  
  <div class="summary">
    <div class="stat-card"><div class="stat-label">Total contacts</div><div class="stat-value">''' + str(clusters_data["total_contacts"]) + '''</div></div>
    <div class="stat-card"><div class="stat-label">Edges</div><div class="stat-value">''' + str(clusters_data["total_edges"]) + '''</div></div>
    <div class="stat-card"><div class="stat-label">Total clusters</div><div class="stat-value">''' + str(clusters_data["total_clusters"]) + '''</div></div>
    <div class="stat-card"><div class="stat-label">Non-singleton</div><div class="stat-value">''' + str(clusters_data["non_singleton_clusters"]) + '''</div></div>
    <div class="stat-card"><div class="stat-label">Largest cluster</div><div class="stat-value">''' + str(clusters_data["largest_cluster_size"]) + '''</div></div>
  </div>
  
  <h2>Top clusters (multi-member)</h2>
''' + ''.join(f'''
  <div class="cluster">
    <div class="cluster-header">
      <span class="cluster-id">Cluster #{c["cluster_id"]}</span>
      <span class="cluster-size">{c["size"]} members · {c["internal_edges"]} internal cross-refs</span>
    </div>
    <div class="cluster-members">
      {''.join(f'<span class="member" title="{m["jid"]}">{m["name"]}</span>' for m in c["members"])}
    </div>
  </div>
''' for c in clusters_data["clusters"] if c["size"] > 1) + '''
  
  <h2>Strongest cross-reference edges</h2>
  <div class="edges-section">
''' + ''.join(f'''
    <div class="edge">
      <span>{e["a"]} ↔ {e["b"]}</span>
      <span class="edge-weight">{e["weight"]}x</span>
    </div>
''' for e in clusters_data["edges"][:20]) + '''
  </div>
  
  <div class="footer">
    Edges represent: number of times Ivan mentioned one contact while talking to another.
    Clusters: greedy union-find with merge threshold = 2 cross-refs.
    ''' + str(clusters_data["singleton_clusters"]) + ''' singleton clusters (no cross-references with other contacts).
  </div>
</div>
</body>
</html>
'''

(ANALYSIS / "clusters.html").write_text(CLUSTERS_HTML)
print(f"Wrote clusters.html ({(ANALYSIS / 'clusters.html').stat().st_size:,} bytes)")

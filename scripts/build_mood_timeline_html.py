#!/usr/bin/env python3
"""Build mood_timeline.html — visual sentiment trajectory per contact."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS"

data = json.loads((ANALYSIS / "mood_timelines.json").read_text())
timelines = data["timelines"]

HTML = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Psycology — Mood Timelines</title>
<style>
  :root { --bg: #0a0a0a; --fg: #d4d4d4; --bg-1: #111; --bg-2: #1a1a1a; --fg-1: #e4e4e4; --fg-2: #a0a0a0; --fg-3: #707070; --border: #2a2a2a; --hover: #1f1f1f; }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; min-height: 100%; background: var(--bg); color: var(--fg); font-family: system-ui, sans-serif; font-size: 14px; }
  .app { padding: 16px 24px; max-width: 1400px; margin: 0 auto; }
  h1 { margin: 0 0 8px; font-size: 16px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--fg-1); }
  h2 { margin: 24px 0 8px; font-size: 14px; color: var(--fg-1); border-bottom: 1px solid var(--border); padding-bottom: 4px; }
  .meta { color: var(--fg-3); font-size: 12px; }
  .controls { display: flex; gap: 12px; margin: 16px 0; align-items: center; }
  input { background: var(--bg-2); border: 1px solid var(--border); color: var(--fg); padding: 6px 10px; border-radius: 3px; font-size: 13px; min-width: 240px; }
  select { background: var(--bg-2); border: 1px solid var(--border); color: var(--fg); padding: 6px 10px; border-radius: 3px; font-size: 13px; }
  
  .timeline-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 12px; }
  .timeline-card { background: var(--bg-1); border: 1px solid var(--border); border-radius: 4px; padding: 12px; }
  .timeline-name { font-size: 13px; color: var(--fg-1); font-weight: 500; margin-bottom: 4px; }
  .timeline-stats { font-size: 10px; color: var(--fg-3); margin-bottom: 6px; }
  .timeline-stats .delta-pos { color: #98c379; }
  .timeline-stats .delta-neg { color: #d97e3a; }
  
  .spark { width: 100%; height: 60px; }
  .axis { stroke: #404040; stroke-width: 0.5; }
  .zero-line { stroke: #707070; stroke-width: 0.5; stroke-dasharray: 2 2; }
  .pos { fill: #98c379; }
  .neg { fill: #d97e3a; }
  .neutral { fill: #707070; }
  
  .footer { margin-top: 32px; padding: 16px 0; color: var(--fg-3); font-size: 11px; border-top: 1px solid var(--border); }
</style>
</head>
<body>
<div class="app">
  <h1>Psycology — Mood Timelines</h1>
  <div class="meta">''' + f"{data['top_contacts_count']} contacts · " + '''sentiment = (positive - negative) words + emojis per month, normalized. Range: -1 (very negative) to +1 (very positive).</div>
  
  <div class="controls">
    <input type="text" id="search" placeholder="filter contacts..." />
    <select id="sort">
      <option value="trend_desc">Sort: Trend Δ (most positive first)</option>
      <option value="trend_asc">Sort: Trend Δ (most negative first)</option>
      <option value="recent_desc">Sort: Recent (most positive first)</option>
      <option value="recent_asc">Sort: Recent (most negative first)</option>
      <option value="msgs">Sort: Most active</option>
    </select>
    <span class="meta" id="count"></span>
  </div>
  
  <h2>Visual timelines</h2>
  <div id="grid" class="timeline-grid"></div>
  
  <div class="footer">
    Trend Δ = recent 3 months average - prior 3 months average. 
    Positive = warming. Negative = cooling. 
    Bar height = monthly sentiment score. 
    Color: green = positive, orange = negative, gray = neutral.
  </div>
</div>

<script>
const DATA = ''' + json.dumps(timelines, ensure_ascii=False) + ''';

function scoreColor(s) {
  if (s > 0.1) return "#98c379";
  if (s < -0.1) return "#d97e3a";
  return "#707070";
}

function renderSpark(timeline, width=350, height=50) {
  // Each timeline: array of {month, score, msgs}
  const months = timeline.monthly;
  if (months.length === 0) return "";
  const n = months.length;
  const padding = 4;
  const usableW = width - padding * 2;
  const usableH = height - padding * 2;
  const barW = Math.max(2, usableW / n - 1);
  const center = padding + usableH / 2;
  
  let bars = "";
  let path = "";
  for (let i = 0; i < n; i++) {
    const m = months[i];
    const x = padding + (i / Math.max(1, n - 1)) * (usableW - barW);
    const h = Math.abs(m.score) * (usableH / 2);
    const y = m.score >= 0 ? center - h : center;
    const color = scoreColor(m.score);
    bars += `<rect x="${x}" y="${y}" width="${barW}" height="${Math.max(1, h)}" fill="${color}" opacity="0.7"/>`;
    if (i > 0) {
      const prevX = padding + ((i - 1) / Math.max(1, n - 1)) * (usableW - barW) + barW / 2;
      const x2 = x + barW / 2;
      const prevY = months[i-1].score >= 0 ? center - Math.abs(months[i-1].score) * (usableH / 2) : center;
      const y2 = m.score >= 0 ? center - h : center;
      path += `<line x1="${prevX}" y1="${prevY}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="1.5" opacity="0.8"/>`;
    }
  }
  
  return `<svg class="spark" viewBox="0 0 ${width} ${height}">
    <line class="axis" x1="${padding}" y1="${center}" x2="${width - padding}" y2="${center}"/>
    ${bars}
  </svg>`;
}

function render() {
  const q = document.getElementById("search").value.toLowerCase();
  const sortKey = document.getElementById("sort").value;
  let rows = DATA.filter(c => !q || c.name.toLowerCase().includes(q));
  
  if (sortKey === "trend_desc") rows.sort((a, b) => b.trend_delta - a.trend_delta);
  else if (sortKey === "trend_asc") rows.sort((a, b) => a.trend_delta - b.trend_delta);
  else if (sortKey === "recent_desc") rows.sort((a, b) => b.recent_avg - a.recent_avg);
  else if (sortKey === "recent_asc") rows.sort((a, b) => a.recent_avg - b.recent_avg);
  else if (sortKey === "msgs") rows.sort((a, b) => b.total_msgs - a.total_msgs);
  
  document.getElementById("count").textContent = `${rows.length} contacts`;
  document.getElementById("grid").innerHTML = rows.map(t => {
    const deltaClass = t.trend_delta > 0 ? "delta-pos" : "delta-neg";
    const deltaSign = t.trend_delta > 0 ? "+" : "";
    const best = t.best_month ? `${t.best_month.month} (${t.best_month.score > 0 ? '+' : ''}${t.best_month.score.toFixed(2)})` : "n/a";
    const worst = t.worst_month ? `${t.worst_month.month} (${t.worst_month.score > 0 ? '+' : ''}${t.worst_month.score.toFixed(2)})` : "n/a";
    return `<div class="timeline-card">
      <div class="timeline-name">${escapeHtml(t.name)}</div>
      <div class="timeline-stats">
        ${t.total_msgs.toLocaleString()} msgs · 
        recent avg: <strong style="color:${scoreColor(t.recent_avg)}">${t.recent_avg > 0 ? '+' : ''}${t.recent_avg.toFixed(2)}</strong> · 
        trend: <span class="${deltaClass}">${deltaSign}${t.trend_delta.toFixed(2)}</span><br>
        best: ${best} · worst: ${worst}
      </div>
      ${renderSpark(t)}
    </div>`;
  }).join("");
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[c]);
}

document.getElementById("search").addEventListener("input", render);
document.getElementById("sort").addEventListener("change", render);
render();
</script>
</body>
</html>
'''

out = ANALYSIS / "mood_timeline.html"
out.write_text(HTML)
print(f"Wrote {out.relative_to(REPO)} ({out.stat().st_size:,} bytes)")

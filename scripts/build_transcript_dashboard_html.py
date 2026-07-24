#!/usr/bin/env python3
"""Build transcript_analysis.html — voice notes dashboard."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS"

data = json.loads((ANALYSIS / "transcript_analysis.json").read_text())
chats = data["top_chats_by_volume"]

HTML = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Psycology — Voice Notes Analysis</title>
<style>
  :root {{ --bg: #0a0a0a; --fg: #d4d4d4; --bg-1: #111; --bg-2: #1a1a1a; --fg-1: #e4e4e4; --fg-2: #a0a0a0; --fg-3: #707070; --border: #2a2a2a; --hover: #1f1f1f; }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; min-height: 100%; background: var(--bg); color: var(--fg); font-family: system-ui, sans-serif; font-size: 14px; }}
  .mono {{ font-family: ui-monospace, Consolas, monospace; font-size: 12px; }}
  .app {{ padding: 16px 24px; max-width: 1400px; margin: 0 auto; }}
  h1 {{ margin: 0 0 8px; font-size: 16px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--fg-1); }}
  h2 {{ margin: 24px 0 8px; font-size: 14px; color: var(--fg-1); border-bottom: 1px solid var(--border); padding-bottom: 4px; }}
  .meta {{ color: var(--fg-3); font-size: 12px; }}
  input {{ background: var(--bg-2); border: 1px solid var(--border); color: var(--fg); padding: 6px 10px; border-radius: 3px; font-size: 13px; min-width: 240px; }}
  
  .stats-row {{ display: flex; gap: 12px; flex-wrap: wrap; margin: 16px 0; }}
  .stat-card {{ background: var(--bg-1); border: 1px solid var(--border); border-radius: 4px; padding: 12px 16px; flex: 1; min-width: 140px; }}
  .stat-label {{ font-size: 10px; color: var(--fg-3); text-transform: uppercase; letter-spacing: 0.05em; }}
  .stat-value {{ font-size: 20px; font-weight: 500; color: #79c0ff; margin-top: 4px; }}
  .stat-sub {{ font-size: 10px; color: var(--fg-3); margin-top: 2px; }}
  
  .emotion-bar {{ display: inline-block; height: 14px; background: #707070; border-radius: 2px; vertical-align: middle; margin-right: 4px; }}
  .e-love {{ background: #d97e3a; }}
  .e-laugh {{ background: #98c379; }}
  .e-anger {{ background: #ff5555; }}
  .e-sadness {{ background: #5a7a8a; }}
  .e-surprise {{ background: #c678dd; }}
  .e-gratitude {{ background: #79c0ff; }}
  
  table {{ width: 100%; border-collapse: collapse; font-size: 12.5px; margin-top: 8px; }}
  th {{ text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--border); color: var(--fg-3); font-weight: 500; font-size: 10px; text-transform: uppercase; letter-spacing: 0.05em; cursor: pointer; }}
  th:hover {{ color: var(--fg-1); }}
  th.num {{ text-align: right; }}
  td {{ padding: 6px 10px; border-bottom: 1px solid var(--border); }}
  td.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  tr:hover {{ background: var(--hover); }}
  .name {{ color: var(--fg-1); font-weight: 500; }}
  .jid {{ color: var(--fg-3); font-size: 10.5px; }}
  
  .bar {{ display: inline-block; width: 60px; height: 6px; background: var(--bg-2); border-radius: 3px; position: relative; vertical-align: middle; margin-right: 4px; }}
  .bar-fill {{ position: absolute; left: 0; top: 0; height: 100%; border-radius: 3px; }}
  
  .footer {{ margin-top: 32px; padding: 16px 0; color: var(--fg-3); font-size: 11px; border-top: 1px solid var(--border); }}
</style>
</head>
<body>
<div class="app">
  <div style="display:flex;align-items:center;gap:16px">
    <h1>Psycology — Voice Notes Analysis</h1>
    <input type="text" id="search" placeholder="filter contacts..." />
    <span class="meta" id="count"></span>
  </div>
  
  <div class="stats-row">
    <div class="stat-card">
      <div class="stat-label">Total transcripts</div>
      <div class="stat-value">{data['total_transcripts']:,}</div>
      <div class="stat-sub">across {data['total_files_scanned']} files</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Total spoken</div>
      <div class="stat-value">{data['total_words']:,}</div>
      <div class="stat-sub">words ({data['total_words']/1000:.1f}k)</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Total audio</div>
      <div class="stat-value">{data['total_duration_hours']:.1f}h</div>
      <div class="stat-sub">avg {data['avg_duration_seconds']:.1f}s per note</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Words/note</div>
      <div class="stat-value">{data['avg_words_per_note']:.0f}</div>
      <div class="stat-sub">density</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Pos/Neg ratio</div>
      <div class="stat-value">{data['sentiment_totals']['ratio']}x</div>
      <div class="stat-sub">{data['sentiment_totals']['positive_words']:,} pos / {data['sentiment_totals']['negative_words']:,} neg</div>
    </div>
  </div>
  
  <h2>🗣 Sentiment distribution</h2>
  <div class="stats-row">
    <div class="stat-card" style="border-color:#98c379"><div class="stat-label" style="color:#98c379">POSITIVE</div><div class="stat-value" style="color:#98c379">{data['sentiment_distribution']['positive_msgs']:,}</div><div class="stat-sub">{100*data['sentiment_distribution']['positive_msgs']/data['total_transcripts']:.1f}% of messages</div></div>
    <div class="stat-card"><div class="stat-label">NEUTRAL</div><div class="stat-value">{data['sentiment_distribution']['neutral_msgs']:,}</div><div class="stat-sub">{100*data['sentiment_distribution']['neutral_msgs']/data['total_transcripts']:.1f}%</div></div>
    <div class="stat-card" style="border-color:#d97e3a"><div class="stat-label" style="color:#d97e3a">NEGATIVE</div><div class="stat-value" style="color:#d97e3a">{data['sentiment_distribution']['negative_msgs']:,}</div><div class="stat-sub">{100*data['sentiment_distribution']['negative_msgs']/data['total_transcripts']:.1f}%</div></div>
  </div>
  
  <h2>🎭 Emotions detected (total markers)</h2>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px;font-size:12px">
'''

for emotion, n in sorted(data['emotion_totals'].items(), key=lambda x: -x[1]):
    pct = 100 * n / sum(data['emotion_totals'].values())
    bar_w = int(pct * 3)
    HTML += f'    <div style="background:var(--bg-1);border:1px solid var(--border);border-radius:4px;padding:8px 12px"><div style="color:var(--fg-3);font-size:10px;text-transform:uppercase">{emotion}</div><div style="font-size:18px;font-weight:500">{n:,}</div><div style="font-size:10px;color:var(--fg-3)">{pct:.1f}%</div></div>\n'

HTML += '''
  </div>
  
  <h2>🌍 Languages detected</h2>
  <div style="margin-top:8px;font-size:12px">
'''
for lang, n in sorted(data['languages'].items(), key=lambda x: -x[1])[:8]:
    pct = 100 * n / data['total_transcripts']
    HTML += f'    <span style="display:inline-block;padding:4px 10px;margin:2px;background:var(--bg-1);border:1px solid var(--border);border-radius:4px"><strong>{lang}</strong> {n:,} ({pct:.1f}%)</span>\n'

HTML += '''
  </div>
  
  <h2>📊 Voice notes per chat (top 50 by volume)</h2>
  <table>
    <thead><tr>
      <th data-sort="name">Contact / Chat</th>
      <th class="num" data-sort="transcripts">Notes</th>
      <th class="num" data-sort="words">Words</th>
      <th class="num" data-sort="duration">Audio (hrs)</th>
      <th class="num" data-sort="sentiment">Sentiment</th>
      <th>Pos/Neg</th>
      <th class="num" data-sort="lang">Lang</th>
    </tr></thead>
    <tbody id="tbl"></tbody>
  </table>
  
  <div class="footer">
    Method: faster-whisper small + small Spanish/English sentiment dictionaries + emotion keyword markers.<br>
    Generated ''' + data["generated_at"][:19] + ''' UTC.
  </div>
</div>

<script>
const DATA = ''' + json.dumps(chats, ensure_ascii=False) + ''';

let sortKey = "transcripts";
let sortAsc = false;

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[c]);
}

function render() {
  const q = document.getElementById("search").value.toLowerCase();
  let rows = DATA.filter(c => !q || c.name.toLowerCase().includes(q) || c.chat.toLowerCase().includes(q));
  rows.sort((a, b) => {
    let av, bv;
    if (sortKey === "words") av = a.total_words, bv = b.total_words;
    else if (sortKey === "duration") av = a.total_duration_s, bv = b.total_duration_s;
    else if (sortKey === "sentiment") av = a.avg_sentiment, bv = b.avg_sentiment;
    else if (sortKey === "lang") av = a.dominant_lang, bv = b.dominant_lang;
    else if (sortKey === "name") av = a.name, bv = b.name;
    else { av = a[sortKey]; bv = b[sortKey]; }
    if (typeof av === "string") return sortAsc ? av.localeCompare(bv) : bv.localeCompare(av);
    return sortAsc ? av - bv : bv - av;
  });
  
  const maxT = Math.max(...rows.map(r => r.transcripts));
  document.getElementById("tbl").innerHTML = rows.map(c => {
    const barW = Math.max(2, (c.transcripts / maxT) * 60);
    const sentColor = c.avg_sentiment > 0.2 ? "#98c379" : c.avg_sentiment < -0.2 ? "#d97e3a" : "#707070";
    const sentPrefix = c.avg_sentiment > 0 ? "+" : "";
    return `<tr>
      <td class="name">${escapeHtml(c.name || 'Unknown')}<div class="jid">${escapeHtml(c.chat)} · JID ${escapeHtml(c.jid)}</div></td>
      <td class="num"><strong>${c.transcripts.toLocaleString()}</strong> <div class="bar"><div class="bar-fill" style="width:${barW}px;background:#79c0ff"></div></div></td>
      <td class="num mono">${c.total_words.toLocaleString()}</td>
      <td class="num mono">${(c.total_duration_s / 3600).toFixed(1)}h</td>
      <td class="num" style="color:${sentColor}"><strong>${sentPrefix}${c.avg_sentiment.toFixed(2)}</strong></td>
      <td class="num mono">${c.pos_words}/${c.neg_words}</td>
      <td class="num mono">${c.dominant_lang}</td>
    </tr>`;
  }).join("");
  document.getElementById("count").textContent = `${rows.length} chats · ${DATA.reduce((s, c) => s + c.transcripts, 0).toLocaleString()} transcripts`;
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

(ANALYSIS / "voice_notes_dashboard.html").write_text(HTML)
print(f"Wrote voice_notes_dashboard.html ({(ANALYSIS / 'voice_notes_dashboard.html').stat().st_size:,} bytes)")

#!/usr/bin/env python3
"""Build transcript_search.html — single-page search app.

Features:
- Real-time client-side search across all 10k+ transcripts
- Filter by name (chat)
- Filter by language
- Filter by date range
- Highlight matches in text
- Show snippet with context
"""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS"

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Psycology — Voice Note Search</title>
<style>
  :root { --bg: #0a0a0a; --fg: #d4d4d4; --bg-1: #111; --bg-2: #1a1a1a; --fg-1: #e4e4e4; --fg-2: #a0a0a0; --fg-3: #707070; --border: #2a2a2a; --hover: #1f1f1f; --accent: #79c0ff; }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; min-height: 100%; background: var(--bg); color: var(--fg); font-family: system-ui, sans-serif; font-size: 14px; }
  .app { padding: 16px 24px; max-width: 1200px; margin: 0 auto; }
  h1 { margin: 0 0 12px; font-size: 16px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--fg-1); }
  
  .controls { background: var(--bg-1); border: 1px solid var(--border); border-radius: 4px; padding: 12px; margin: 16px 0; display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }
  .controls label { font-size: 10px; color: var(--fg-3); text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 4px; }
  input, select { background: var(--bg-2); border: 1px solid var(--border); color: var(--fg); padding: 6px 10px; border-radius: 3px; font-size: 13px; font-family: inherit; }
  input:focus { border-color: var(--accent); outline: none; }
  #search-box { min-width: 320px; font-size: 14px; }
  
  .meta-bar { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; color: var(--fg-3); font-size: 12px; }
  
  .result { padding: 12px 16px; background: var(--bg-1); border: 1px solid var(--border); border-radius: 4px; margin-bottom: 8px; }
  .result:hover { border-color: var(--accent); }
  .result-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 6px; }
  .result-name { font-size: 13px; color: var(--fg-1); font-weight: 500; }
  .result-meta { font-size: 10px; color: var(--fg-3); font-family: ui-monospace, monospace; }
  .result-text { font-size: 13px; line-height: 1.5; color: var(--fg-2); margin: 4px 0 0; }
  .match { background: #d97e3a; color: #0a0a0a; padding: 1px 3px; border-radius: 2px; font-weight: 500; }
  
  .loading { text-align: center; padding: 40px; color: var(--fg-3); }
  .empty { text-align: center; padding: 40px; color: var(--fg-3); font-style: italic; }
  
  .stat-row { display: flex; gap: 12px; flex-wrap: wrap; margin: 12px 0; }
  .stat { background: var(--bg-1); border: 1px solid var(--border); border-radius: 4px; padding: 8px 16px; font-size: 11px; }
  .stat-label { color: var(--fg-3); text-transform: uppercase; font-size: 10px; }
  .stat-value { color: var(--accent); font-size: 16px; font-weight: 500; }
  
  .footer { margin-top: 32px; padding: 16px 0; color: var(--fg-3); font-size: 11px; border-top: 1px solid var(--border); }
</style>
</head>
<body>
<div class="app">
  <h1>🎤 Voice Note Search</h1>
  
  <div class="controls">
    <div style="flex:1;min-width:300px">
      <label>Search query</label>
      <input type="text" id="search-box" placeholder="e.g. trabajo, jajaja, mama, te quiero..." autofocus />
    </div>
    <div>
      <label>Filter by contact</label>
      <select id="filter-name"><option value="">All contacts</option></select>
    </div>
    <div>
      <label>Filter by language</label>
      <select id="filter-lang"><option value="">All languages</option></select>
    </div>
    <div>
      <label>From year</label>
      <select id="filter-from"><option value="">Any</option></select>
    </div>
    <div>
      <label>To year</label>
      <select id="filter-to"><option value="">Any</option></select>
    </div>
  </div>
  
  <div class="meta-bar">
    <span id="result-count">Loading...</span>
    <span id="search-time"></span>
  </div>
  
  <div id="results"></div>
  
  <div class="footer">
    10,835 voice note transcripts indexed · faster-whisper small · Spanish + English dictionaries.
    Search runs client-side on the full JSON. Text shown is a snippet around the match.
  </div>
</div>

<script>
let ENTRIES = [];
let NAMES = new Set();
let LANGS = new Set();
let YEARS = new Set();

async function loadIndex() {
  const resp = await fetch("transcript_search_lean.json");
  const data = await resp.json();
  ENTRIES = data.entries;
  NAMES = new Set(ENTRIES.map(e => e.name).filter(n => n !== "?").sort());
  LANGS = new Set(ENTRIES.map(e => e.language).filter(l => l !== "?").sort());
  YEARS = new Set(ENTRIES.map(e => (e.date || "").slice(0,4)).filter(y => y).sort());
  
  // Populate filters
  const nameSel = document.getElementById("filter-name");
  for (const n of NAMES) nameSel.innerHTML += `<option value="${escape(n)}">${escape(n)}</option>`;
  const langSel = document.getElementById("filter-lang");
  for (const l of LANGS) langSel.innerHTML += `<option value="${escape(l)}">${escape(l)}</option>`;
  const fromSel = document.getElementById("filter-from");
  const toSel = document.getElementById("filter-to");
  for (const y of YEARS) {
    fromSel.innerHTML += `<option value="${y}">${y}</option>`;
    toSel.innerHTML += `<option value="${y}">${y}</option>`;
  }
  
  document.getElementById("result-count").textContent = `${ENTRIES.length} transcripts loaded`;
  document.getElementById("search-box").disabled = false;
}

function escape(s) { return String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[c]); }

function highlight(text, query) {
  if (!query) return escape(text);
  const tokens = query.split(/\\s+/).filter(t => t.length >= 2);
  let result = escape(text);
  for (const t of tokens) {
    const re = new RegExp(`(${escape(t)})`, "gi");
    result = result.replace(re, `<span class="match">$1</span>`);
  }
  return result;
}

function snippet(text, query) {
  if (!query || query.length < 2) return text;
  const lower = text.toLowerCase();
  const idx = lower.indexOf(query.toLowerCase().split(/\\s+/)[0]);
  if (idx < 0) return text.slice(0, 200);
  const start = Math.max(0, idx - 50);
  const end = Math.min(text.length, idx + 150);
  return (start > 0 ? "..." : "") + text.slice(start, end) + (end < text.length ? "..." : "");
}

function search() {
  const q = document.getElementById("search-box").value.trim();
  const filterName = document.getElementById("filter-name").value;
  const filterLang = document.getElementById("filter-lang").value;
  const yearFrom = document.getElementById("filter-from").value;
  const yearTo = document.getElementById("filter-to").value;
  
  const startTime = performance.now();
  
  let matches = [];
  if (q.length >= 2) {
    // Word-level search — split into tokens, require all to be present
    const tokens = q.toLowerCase().split(/\\s+/).filter(t => t.length >= 2);
    matches = ENTRIES.filter(e => {
      // Apply non-text filters first
      if (filterName && e.name !== filterName) return false;
      if (filterLang && e.language !== filterLang) return false;
      if (yearFrom && (!e.date || e.date.slice(0,4) < yearFrom)) return false;
      if (yearTo && (!e.date || e.date.slice(0,4) > yearTo)) return false;
      // Text search
      for (const t of tokens) {
        if (!e.text_low.includes(t)) return false;
      }
      return true;
    });
  } else if (filterName || filterLang || yearFrom || yearTo) {
    // Only filters, no query — show all matching filters
    matches = ENTRIES.filter(e => {
      if (filterName && e.name !== filterName) return false;
      if (filterLang && e.language !== filterLang) return false;
      if (yearFrom && (!e.date || e.date.slice(0,4) < yearFrom)) return false;
      if (yearTo && (!e.date || e.date.slice(0,4) > yearTo)) return false;
      return true;
    });
  }
  
  const elapsed = (performance.now() - startTime).toFixed(0);
  document.getElementById("search-time").textContent = `${elapsed}ms`;
  document.getElementById("result-count").textContent = `${matches.length.toLocaleString()} matches from ${ENTRIES.length.toLocaleString()} transcripts`;
  
  // Show first 100
  const display = matches.slice(0, 100);
  if (display.length === 0) {
    document.getElementById("results").innerHTML = q.length < 2 ? 
      `<div class="empty">Type at least 2 characters to search... showing all transcript browse-by-filter.</div>` :
      `<div class="empty">No matches found. Try different query or clear filters.</div>`;
    return;
  }
  
  document.getElementById("results").innerHTML = display.map(m => {
    const snip = snippet(m.text, q);
    return `<div class="result">
      <div class="result-header">
        <span class="result-name">${escape(m.name || 'Unknown')}</span>
        <span class="result-meta">${escape(m.date || '?')} · ${(m.duration || 0).toFixed(1)}s · ${escape(m.language)} · <span style="color:#707070">${escape(m.file)}</span></span>
      </div>
      <div class="result-text">${highlight(snip, q)}</div>
    </div>`;
  }).join("") + (matches.length > 100 ? `<div class="empty">...and ${matches.length - 100} more matches. Refine your search to see them.</div>` : "");
}

document.getElementById("search-box").addEventListener("input", debounce(search, 100));
["filter-name", "filter-lang", "filter-from", "filter-to"].forEach(id => {
  document.getElementById(id).addEventListener("change", search);
});

function debounce(fn, ms) {
  let t;
  return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); };
}

// Initial load
document.getElementById("results").innerHTML = '<div class="loading">Loading 10,835 transcripts (this takes a few seconds)...</div>';
document.getElementById("search-box").disabled = true;
loadIndex().then(search);
</script>
</body>
</html>
"""

out = ANALYSIS / "transcript_search.html"
out.write_text(HTML)
print(f"Wrote {out.relative_to(REPO)} ({out.stat().st_size:,} bytes)")

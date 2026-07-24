#!/usr/bin/env python3
"""Build a SMALL viewer that fetches viewer_full_data.json lazily.
~30KB HTML, ~600KB JSON. Renders inline messages on click.
"""
from __future__ import annotations
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS"

HTML = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Psycology — Conversation Index</title>
<style>
  :root {
    --bg: #0a0a0a; --fg: #d4d4d4;
    --bg-1: #111; --bg-2: #1a1a1a;
    --fg-1: #e4e4e4; --fg-2: #a0a0a0; --fg-3: #707070;
    --me: #79c0ff; --them: #f5b97e;
    --accent: #58c4dc; --border: #2a2a2a; --hover: #1f1f1f;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; height: 100%; background: var(--bg); color: var(--fg); font-family: system-ui, -apple-system, sans-serif; font-size: 14px; }
  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }
  .muted { color: var(--fg-3); }
  .mono { font-family: ui-monospace, "JetBrains Mono", Consolas, monospace; font-size: 12px; }
  .app { display: grid; grid-template-columns: 1fr; height: 100vh; }
  .top { padding: 12px 24px; border-bottom: 1px solid var(--border); background: var(--bg-1); display: flex; gap: 16px; align-items: center; }
  .top h1 { margin: 0; font-size: 14px; font-weight: 600; text-transform: uppercase; }
  .top .meta { color: var(--fg-3); font-size: 12px; margin-left: auto; }
  .top input { background: var(--bg-2); border: 1px solid var(--border); color: var(--fg); padding: 4px 8px; border-radius: 3px; font-size: 13px; min-width: 240px; }
  .main { overflow-y: auto; padding: 16px 24px; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th { text-align: left; padding: 8px 12px; border-bottom: 1px solid var(--border); color: var(--fg-3); font-weight: 500; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; position: sticky; top: 0; background: var(--bg-1); cursor: pointer; }
  th:hover { color: var(--accent); }
  td { padding: 8px 12px; border-bottom: 1px solid var(--border); }
  tr:hover { background: var(--hover); }
  .num { text-align: right; font-family: var(--mono); font-variant-numeric: tabular-nums; }
  .name { font-weight: 500; color: var(--fg-1); }
  .tier { font-size: 10px; color: var(--accent); padding: 2px 6px; border: 1px solid var(--border); border-radius: 3px; display: inline-block; }
  .jid { color: var(--fg-3); font-size: 11px; }
  .last-msg { color: var(--fg-2); font-style: italic; font-size: 12px; max-width: 400px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .section-title { font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--fg-3); padding: 16px 0 8px; border-bottom: 1px solid var(--border); margin-top: 24px; }
  .section-title:first-child { margin-top: 0; }
</style>
</head>
<body>
<div class="app">
  <div class="top">
    <h1>Psycology — Contact Index</h1>
    <input type="text" id="search" placeholder="filter by name or JID..." />
    <span class="meta" id="meta">loading...</span>
  </div>
  <div class="main">
    <div class="section-title">vCard Contacts</div>
    <table id="contacts-table">
      <thead>
        <tr>
          <th data-sort="name">Name</th>
          <th data-sort="total" class="num">Messages</th>
          <th data-sort="from_me" class="num">From Ivan</th>
          <th data-sort="from_them" class="num">From Them</th>
          <th data-sort="first">First</th>
          <th data-sort="last">Last</th>
          <th data-sort="tier">Tier</th>
          <th data-sort="jid">JID</th>
          <th>Last Message</th>
        </tr>
      </thead>
      <tbody id="contacts-body"></tbody>
    </table>
  </div>
</div>

<script>
let DATA = null;
let sortKey = "total";
let sortAsc = false;

async function init() {
  // Load data
  const resp = await fetch("./viewer_full_data.json");
  DATA = await resp.json();
  document.getElementById("meta").textContent =
    `${DATA.totals.vcard_count} vCard contacts · ${DATA.totals.vcard_messages.toLocaleString()} messages · ${DATA.totals.not_saved_count} not-saved`;
  render();
}

function render() {
  const q = document.getElementById("search").value.toLowerCase();
  let rows = DATA.vcard_contacts.filter(c =>
    !q || c.name.toLowerCase().includes(q) || c.jid.includes(q)
  );
  rows.sort((a, b) => {
    const av = a[sortKey], bv = b[sortKey];
    if (typeof av === "string") return sortAsc ? av.localeCompare(bv) : bv.localeCompare(av);
    return sortAsc ? av - bv : bv - av;
  });
  const tbody = document.getElementById("contacts-body");
  tbody.innerHTML = rows.map(c => `
    <tr>
      <td class="name">${escapeHtml(c.name)}</td>
      <td class="num">${c.total.toLocaleString()}</td>
      <td class="num muted">${c.from_me.toLocaleString()}</td>
      <td class="num muted">${c.from_them.toLocaleString()}</td>
      <td class="mono muted">${c.first || "—"}</td>
      <td class="mono muted">${c.last || "—"}</td>
      <td><span class="tier">${escapeHtml(c.tier.slice(0, 14))}</span></td>
      <td class="jid mono">${escapeHtml(c.jid)}</td>
      <td class="last-msg" title="${escapeHtml(c.last_msg || "")}">${escapeHtml(c.last_msg || "—")}</td>
    </tr>
  `).join("");
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[c]);
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

init().catch(e => {
  document.getElementById("meta").textContent = "ERROR loading data: " + e.message;
});
</script>
</body>
</html>
'''
out = ANALYSIS / "viewer.html"
out.write_text(HTML)
print(f"Wrote {out.relative_to(REPO)} ({len(HTML):,} bytes)")

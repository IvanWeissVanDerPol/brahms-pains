#!/usr/bin/env python3
"""Build a self-contained HTML viewer that embeds 5 sample chats inline.

Reads messages.json files for selected chats (1 per tier), gathers audio
transcripts where available, and writes a single viewer.html that runs
file:// without a server.

Usage:
    python3 scripts/build_viewer_payload.py
"""
from __future__ import annotations

import json
import re
import shutil
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
# The worktree may not include the actual chat JSON (it has been gitignored
# or simply not present in the worktree). Always read from the canonical
# repo path so the generated viewer.html reflects real data.
_CANONICAL = Path("/root/psycology") if Path("/root/psycology/SOURCE_OF_TRUTH/wa_messages/tier1_deep").exists() else REPO_ROOT
MSG_BASE = _CANONICAL / "SOURCE_OF_TRUTH" / "wa_messages"
ANALYSIS_DIR = REPO_ROOT / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS"
TRANSCRIPT_BASE = _CANONICAL / "SOURCE_OF_TRUTH" / "voice_note_transcripts"
AUDIO_BASE = _CANONICAL / "media" / "audio"
NAMED_PICKLE = Path("/tmp/psycology_named_v2.pkl")

# Pick one chat per tier — focus on closest, audio-rich chats
TIER_PICKS = {
    "tier1_deep": "magali_carreras",        # 595981225272
    "tier1_deep_2": "07__kiki_hermana___wa_chat_595985724135_111",  # kiki
    "tier2_core": "18__luana_weiss___wa_chat_595985725366_99",      # luana
    "tier2_core_2": "jonathan_verdun___wa_chat_595971922708_3654",  # jonatan
    "tier3_extended": "094__p0156___wa_chat_595983380156_3701",     # any with audio
}

# Recent N messages to include per chat
RECENT_N = 50
# Maximum audio msgs to embed
MAX_AUDIO_PER_CHAT = 15


def find_chat_dir(tier: str, hint: str) -> Path | None:
    """Find a chat dir under tier containing hint in its name."""
    tier_dir = MSG_BASE / tier
    if not tier_dir.exists():
        return None
    matches = [d for d in tier_dir.iterdir() if hint in d.name.lower()]
    return matches[0] if matches else None


def load_named() -> dict:
    import pickle
    if not NAMED_PICKLE.exists():
        return {}
    return pickle.load(open(NAMED_PICKLE, "rb"))


def jid_to_name(jid: str, named: dict) -> str:
    return named.get(jid, ("(unnamed)", None, None))[0] or "(unnamed)"


def load_chat_messages(chat_dir: Path) -> tuple[dict, list]:
    """Return (chat_metadata, messages)."""
    meta = json.loads((chat_dir / "messages.json").read_text())
    return meta, meta.get("messages", [])


def find_audio_transcript(opus_filename: str, chat_slug: str, contact_name: str | None = None) -> dict | None:
    """Find the transcript entry for an opus file (if any).

    Tries per-chat transcripts.json first, then per-contact transcripts,
    then _wa_ptt_bulk/, then any transcripts file under voice_note_transcripts/.

    Returns the entry dict or None.
    """
    # 1. per-chat transcripts (keyed by chat dir name)
    candidates = [
        TRANSCRIPT_BASE / chat_slug / "transcripts.json",
        TRANSCRIPT_BASE / chat_slug.strip("_wa_") / "transcripts.json",
    ]
    if contact_name:
        # Also try sanitized contact name
        sanitized = re.sub(r'[^A-Za-z0-9_]+', '_', contact_name).strip('_')
        candidates.append(TRANSCRIPT_BASE / sanitized / "transcripts.json")
        # Try exact case
        candidates.append(TRANSCRIPT_BASE / contact_name / "transcripts.json")

    for c in candidates:
        if c.exists():
            try:
                arr = json.loads(c.read_text(encoding="utf-8"))
                for e in arr:
                    if e.get("file") == opus_filename:
                        return e
            except Exception:
                pass

    # 2. _wa_ptt_bulk
    bulk = TRANSCRIPT_BASE / "_wa_ptt_bulk" / f"{opus_filename.replace('.opus', '.json')}"
    if bulk.exists():
        try:
            return json.loads(bulk.read_text())
        except Exception:
            pass

    # 3. Search ALL transcript files by PTT ID (slow fallback)
    ptt_match = re.match(r"(PTT-\d{8}-WA\d+)", opus_filename)
    if ptt_match:
        ptt_id = ptt_match.group(1)
        for jsn in TRANSCRIPT_BASE.rglob("transcripts.json"):
            try:
                arr = json.loads(jsn.read_text(encoding="utf-8"))
                for e in arr:
                    if e.get("file") == opus_filename:
                        return e
            except Exception:
                pass
    return None


def chat_audio_path(opus_filename: str, chat_id_from_dir: str) -> str:
    """Return file://-friendly relative path from viewer.html to the opus."""
    # chat_id_from_dir looks like "_wa_chat_595981225272_62"
    # or "_wa_lid_118262125854912_15538" or "_wa_group_<slug>_<chatid>"
    # The opus files live at /root/psycology/media/audio/<chat_id_from_dir>/PTT-XXXX.opus
    rel = f"../../../../media/audio/{chat_id_from_dir}/{opus_filename}"
    return rel


def serialize_chat(chat_dir: Path, named: dict) -> dict:
    meta, msgs = load_chat_messages(chat_dir)
    jid = str(meta.get("jid_user"))
    name = jid_to_name(jid, named)
    chat_id_dir = chat_dir.name

    # Take the LAST N messages (most recent)
    msgs_sorted = sorted(msgs, key=lambda m: m.get("ts_ms", 0) if isinstance(m, dict) else 0)
    recent = msgs_sorted[-RECENT_N:]

    # Collect all audio — but stratify to get a mix of recent + earlier
    # so transcripts from earlier sessions are visible.
    audio_msgs = [m for m in msgs if isinstance(m, dict) and m.get("type") == 2]
    audio_msgs.sort(key=lambda m: m.get("ts_ms", 0) if isinstance(m, dict) else 0)
    n_audio = len(audio_msgs)
    # Sample a mix that demonstrates the full conversation arc:
    #   - 2 oldest
    #   - 6 from the middle (covers the historic bulk)
    #   - 7 most-recent
    if n_audio <= MAX_AUDIO_PER_CHAT:
        audio_msgs_to_include = audio_msgs
    else:
        early = audio_msgs[:2]
        rest = audio_msgs[2:]
        n_rest = MAX_AUDIO_PER_CHAT - 2
        mid_count = max(2, n_rest // 2)
        last_count = n_rest - mid_count
        # Middle = even-spaced through the chunk between [2:-last_count]
        window = rest[:-last_count] if last_count else rest
        if len(window) > mid_count:
            step = max(1, len(window) // mid_count)
            middle = [window[i * step] for i in range(mid_count) if i * step < len(window)]
        else:
            middle = window
        last = rest[-last_count:] if last_count else []
        audio_msgs_to_include = early + middle + last

    # Build body — keep ALL recent + audio_interleave
    body_msgs = []
    for m in recent + audio_msgs_to_include:
        if not isinstance(m, dict):
            continue
        # Skip duplicates
        if any(b.get("key_id") == m.get("key_id") for b in body_msgs):
            continue
        media = m.get("media") or {}
        opus_filename = (media.get("path") or "").rsplit("/", 1)[-1] if media.get("path") else None
        transcript = None
        if media.get("path"):
            # Original media path may be relative to the chat, like
            # "Media/WhatsApp Audio/.../PTT-XXXX.opus". Extract basename.
            opus_filename = media["path"].rsplit("/", 1)[-1]
            # only PTT-*.opus should be matched
            if not opus_filename.startswith("PTT-"):
                opus_filename = None
        if opus_filename:
            transcript = find_audio_transcript(opus_filename, chat_id_dir, name)
        body_msgs.append({
            "key_id": m.get("key_id"),
            "ts_ms": m.get("ts_ms", 0),
            "ts_iso": m.get("ts_iso", ""),
            "from_me": m.get("from_me", False),
            "type": m.get("type", 0),
            "text": m.get("text") or "",
            "media_path": media.get("path"),
            "media_mime": media.get("mime"),
            "duration_s": media.get("duration_s", 0),
            "opus_filename": opus_filename,
            "audio_url": chat_audio_path(opus_filename, chat_id_dir) if opus_filename else None,
            "transcript_text": (transcript or {}).get("text", "") if transcript else None,
            "transcript_segments": (transcript or {}).get("segments", []) if transcript else None,
            "transcript_lang": (transcript or {}).get("language") if transcript else None,
            "starred": m.get("starred", False),
        })

    body_msgs.sort(key=lambda b: b["ts_ms"])

    # Detect chat-style stat
    n_msgs = len(msgs)
    n_audio = len(audio_msgs)
    n_image = sum(1 for m in msgs if isinstance(m, dict) and m.get("type") == 1)
    n_text = sum(1 for m in msgs if isinstance(m, dict) and m.get("type") == 0)

    # Span
    ts_list = [m.get("ts_ms", 0) for m in msgs if isinstance(m, dict) and m.get("ts_ms")]
    first_ts = min(ts_list) if ts_list else 0
    last_ts = max(ts_list) if ts_list else 0
    days = (last_ts - first_ts) / 86400000 if last_ts > first_ts else 0

    return {
        "chat_id": chat_id_dir,
        "jid": jid,
        "tier": chat_dir.parent.name,
        "contact_name": name,
        "contact_confidence": (named.get(jid, (None, None, None))[1] if jid in named else None),
        "msgs_total": n_msgs,
        "msgs_audio": n_audio,
        "msgs_image": n_image,
        "msgs_text": n_text,
        "first_ts": first_ts,
        "last_ts": last_ts,
        "days": int(days),
        "messages": body_msgs,
    }


# ─────────────────────────────────────────────────────────────────────────────
# HTML rendering
# ─────────────────────────────────────────────────────────────────────────────

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Psycology — Conversation Viewer</title>
<style>
  :root {
    --bg: #0a0a0a;        --fg: #d4d4d4;
    --bg-1: #111;         --bg-2: #1a1a1a;
    --fg-1: #e4e4e4;      --fg-2: #a0a0a0;     --fg-3: #707070;
    --me: #79c0ff;       --them: #f5b97e;
    --accent: #58c4dc;    --warn: #d97e3a;    --ok: #98c379;
    --border: #2a2a2a;    --hover: #1f1f1f;
    --mono: ui-monospace, "JetBrains Mono", "IBM Plex Mono", "SF Mono", Consolas, monospace;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; height: 100%; background: var(--bg); color: var(--fg); font-family: system-ui, -apple-system, sans-serif; font-size: 14px; }
  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }
  .mono { font-family: var(--mono); font-size: 12.5px; }

  /* Layout */
  .app { display: grid; grid-template-columns: 320px 1fr; grid-template-rows: 48px 1fr 28px; height: 100vh; }
  .top { grid-column: 1 / -1; padding: 0 16px; display: flex; align-items: center; gap: 12px; border-bottom: 1px solid var(--border); background: var(--bg-1); }
  .top h1 { margin: 0; font-size: 14px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; color: var(--fg-1); }
  .top .meta { color: var(--fg-3); font-size: 12px; margin-left: auto; }
  .top input { background: var(--bg-2); color: var(--fg); border: 1px solid var(--border); border-radius: 3px; padding: 4px 8px; font-size: 12px; }
  .sidebar { overflow-y: auto; border-right: 1px solid var(--border); background: var(--bg-1); }
  .sidebar h2 { padding: 12px 16px 8px; margin: 0; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--fg-3); }
  .chat-list { list-style: none; margin: 0; padding: 0; }
  .chat-list li { padding: 12px 16px; border-bottom: 1px solid var(--border); cursor: pointer; }
  .chat-list li:hover { background: var(--hover); }
  .chat-list li.active { background: var(--bg-2); border-left: 3px solid var(--accent); padding-left: 13px; }
  .chat-list .name { color: var(--fg-1); font-weight: 500; }
  .chat-list .stats { display: flex; gap: 8px; font-size: 11px; color: var(--fg-3); margin-top: 4px; }
  .chat-list .stats span { display: inline-block; }
  .chat-list .tier-tag { display: inline-block; font-size: 10px; padding: 1px 4px; border-radius: 2px; margin-right: 6px; background: var(--bg-2); color: var(--fg-2); }
  .chat-list .tier-tier1_deep { color: #79c0ff; }
  .chat-list .tier-tier2_core { color: #f5b97e; }
  .chat-list .tier-tier3_extended { color: #98c379; }

  .main { overflow-y: auto; padding: 16px 24px; }
  .empty { display: flex; height: 100%; align-items: center; justify-content: center; color: var(--fg-3); }
  .toolbar { display: flex; gap: 8px; padding: 8px 16px; border-bottom: 1px solid var(--border); background: var(--bg-1); flex-wrap: wrap; align-items: center; }
  .toolbar label { font-size: 11px; color: var(--fg-3); text-transform: uppercase; letter-spacing: 0.04em; }
  .toolbar select, .toolbar input { background: var(--bg-2); color: var(--fg); border: 1px solid var(--border); border-radius: 3px; padding: 3px 6px; font-size: 12px; }
  .toolbar button { background: var(--bg-2); color: var(--fg-1); border: 1px solid var(--border); border-radius: 3px; padding: 4px 10px; font-size: 12px; cursor: pointer; }
  .toolbar button:hover { background: var(--hover); }

  .msg { display: grid; grid-template-columns: 64px 1fr; gap: 12px; padding: 6px 0; border-bottom: 1px dotted var(--border); }
  .msg:hover { background: var(--hover); }
  .msg .ts { color: var(--fg-3); font-size: 11px; padding-top: 4px; font-family: var(--mono); }
  .msg .body { color: var(--fg-1); line-height: 1.5; word-break: break-word; }
  .msg.me .ts { color: var(--me); }
  .msg.me .body::before { content: "› "; color: var(--me); font-weight: 700; }
  .msg.them .ts { color: var(--them); }
  .msg.them .body::before { content: "‹ "; color: var(--them); font-weight: 700; }
  .msg .body em.transcript { display: block; margin-top: 6px; padding: 8px 12px; background: var(--bg-1); color: var(--fg-2); border-left: 3px solid var(--accent); font-style: italic; white-space: pre-wrap; }
  .msg audio { margin-top: 8px; width: 100%; height: 32px; }
  .msg .no-transcript { color: var(--warn); font-style: italic; font-size: 12px; }
  .msg .pill { display: inline-block; font-size: 10px; padding: 1px 5px; border-radius: 3px; background: var(--bg-2); color: var(--fg-3); margin-left: 6px; }

  /* Bottom status bar */
  .status { grid-column: 1 / -1; padding: 0 16px; display: flex; align-items: center; justify-content: space-between; border-top: 1px solid var(--border); background: var(--bg-1); font-size: 11px; color: var(--fg-3); }

  .hidden { display: none; }
  .highlight { background: var(--warn); color: #000; padding: 0 2px; border-radius: 2px; }
</style>
</head>
<body>
<div class="app">
  <header class="top">
    <h1>🪞 Psycology — Conversations</h1>
    <input id="search" type="text" placeholder="search msgs/transcripts…" />
    <span class="meta" id="topMeta"></span>
  </header>
  <aside class="sidebar">
    <h2>Chats (5 sample)</h2>
    <ul class="chat-list" id="chatList"></ul>
    <h2>Keyboard</h2>
    <div style="padding: 8px 16px; font-size: 12px; color: var(--fg-3); line-height: 1.7;">
      <kbd>j</kbd>/<kbd>k</kbd>&nbsp; next/prev message<br>
      <kbd>space</kbd>&nbsp; play/pause audio<br>
      <kbd>esc</kbd>&nbsp; back to list
    </div>
  </aside>
  <main class="main" id="main">
    <div class="empty">Loading chats…</div>
  </main>
  <footer class="status">
    <span id="statusLeft">📜 viewer.html · offline · AI-Whisperers</span>
    <span id="statusRight"></span>
  </footer>
</div>

<!-- Payload: 5 sample chats inline -->
<script id="payload" type="application/json">
__PAYLOAD__
</script>

<script>
"use strict";

// --- Load ---
const PAYLOAD = JSON.parse(document.getElementById("payload").textContent);
const chats = PAYLOAD.chats;
const titleEl = document.querySelector(".top h1");
const topMeta = document.getElementById("topMeta");
const chatListEl = document.getElementById("chatList");
const main = document.getElementById("main");
const search = document.getElementById("search");
const statusRight = document.getElementById("statusRight");

let currentChat = null;
let currentFilter = "all";
let currentSearch = "";

topMeta.textContent = `${chats.length} chats · ${chats.reduce((s,c)=>s+c.msgs_total,0).toLocaleString()} msgs · ${PAYLOAD.transcripts_available}/${PAYLOAD.transcripts_available + PAYLOAD.transcripts_missing} transcripts`;

chats.forEach((c, i) => {
  const li = document.createElement("li");
  li.dataset.chatId = c.chat_id;
  const tier = c.tier;
  const trans = (c.messages || []).filter(m => m.transcript_text).length;
  li.innerHTML = `
    <span class="tier-tag tier-${tier}">${tier.replace('tier','').replace('_',' ')}</span>
    <span class="name" title="${c.contact_name} · ${c.jid}">${c.contact_name}</span>
    <div class="stats">
      <span>📝 ${c.msgs_total.toLocaleString()}</span>
      <span>🎤 ${c.msgs_audio.toLocaleString()}</span>
      <span>📅 ${c.days}d</span>
      ${trans ? `<span style="color:var(--ok)">✓ ${trans} transcribed</span>` : '<span style="color:var(--warn)">⏳ no transcripts</span>'}
    </div>
  `;
  li.onclick = () => openChat(c.chat_id);
  chatListEl.appendChild(li);
});

function openChat(chatId) {
  const c = chats.find(c => c.chat_id === chatId);
  if (!c) return;
  currentChat = c;
  [...chatListEl.children].forEach(li => li.classList.toggle("active", li.dataset.chatId === chatId));
  renderChat();
}

function renderChat() {
  if (!currentChat) {
    main.innerHTML = '<div class="empty">← pick a chat on the left</div>';
    return;
  }
  let html = `
    <div class="toolbar">
      <label>Filter:</label>
      <select id="msgFilter">
        <option value="all">All</option>
        <option value="text">Text only</option>
        <option value="audio">Audio only</option>
        <option value="from_me">From Ivan</option>
        <option value="from_them">From ${currentChat.contact_name}</option>
        <option value="transcribed">Transcribed audio</option>
      </select>
      <button id="exportMd">Export conversation → Markdown</button>
      <label style="margin-left:auto">Showing <span id="visibleCount"></span> msgs</label>
    </div>
  `;
  const shown = [];
  for (const m of currentChat.messages) {
    if (currentFilter === "text" && m.type !== 0) continue;
    if (currentFilter === "audio" && m.type !== 2) continue;
    if (currentFilter === "from_me" && !m.from_me) continue;
    if (currentFilter === "from_them" && m.from_me) continue;
    if (currentFilter === "transcribed" && !m.transcript_text) continue;
    if (currentSearch && !((m.text || "") + " " + (m.transcript_text || "")).toLowerCase().includes(currentSearch)) continue;
    shown.push(m);
    html += renderMsg(m);
  }
  main.innerHTML = html;
  document.getElementById("msgFilter").value = currentFilter;
  document.getElementById("msgFilter").onchange = (e) => { currentFilter = e.target.value; renderChat(); };
  document.getElementById("exportMd").onclick = () => exportMarkdown();
  document.getElementById("visibleCount").textContent = shown.length;
  statusRight.textContent = currentChat.contact_name + " · " + currentChat.messages.length + " msgs in view";
  attachAudioListeners();
}

function renderMsg(m) {
  const ts = m.ts_iso || new Date(m.ts_ms).toISOString();
  const classes = "msg " + (m.from_me ? "me" : "them");
  let body = "";
  if (m.type === 0 && m.text) {
    body = escapeHtml(m.text);
  } else if (m.type === 2) {
    body = `<span class="pill">audio · ${m.duration_s.toFixed(1)}s</span>`;
    if (m.audio_url) {
      body += `<br><audio controls preload="none" src="${m.audio_url}" data-key="${m.key_id}"></audio>`;
    }
    if (m.transcript_text) {
      body += `<em class="transcript">📝 ${escapeHtml(m.transcript_text)}</em>`;
    } else {
      body += `<em class="no-transcript">⏳ transcription pending</em>`;
    }
  } else if (m.type === 1) {
    body = `<span class="pill">image</span> ${escapeHtml(m.media_path || '')}`;
  } else if (m.type === 3) {
    body = `<span class="pill">video · ${m.duration_s.toFixed(1)}s</span>`;
  }
  if (m.starred) body += ` <span class="pill" style="color:#ffb86c">★ starred</span>`;
  const ts_short = ts.replace('T',' ').substring(0, 16);
  return `<div class="${classes}" data-key="${m.key_id}" data-ts="${m.ts_ms}">
    <div class="ts">${ts_short}</div>
    <div class="body">${body}</div>
  </div>`;
}

function attachAudioListeners() {
  document.querySelectorAll("audio").forEach(audio => {
    audio.onplay = () => {
      [...document.querySelectorAll("audio")].forEach(a => { if (a !== audio) a.pause(); });
      statusRight.textContent = `▶ playing audio ${audio.dataset.key.substring(0, 12)}…`;
    };
    audio.onended = () => statusRight.textContent = currentChat.contact_name;
  });
}

function exportMarkdown() {
  if (!currentChat) return;
  let md = `# Conversation with ${currentChat.contact_name} (${currentChat.jid})\n\n`;
  md += `Tier: ${currentChat.tier}  \n`;
  md += `Total msgs: ${currentChat.msgs_total}  · audio: ${currentChat.msgs_audio}  · span: ${currentChat.days} days  \n\n`;
  for (const m of currentChat.messages) {
    const who = m.from_me ? "**Ivan**" : `*${currentChat.contact_name}*`;
    const ts = (m.ts_iso || '').replace('T',' ').substring(0, 16);
    md += `### ${ts} — ${who}\n\n`;
    if (m.type === 0 && m.text) {
      md += `${m.text}\n\n`;
    } else if (m.type === 2) {
      md += `[audio · ${m.duration_s.toFixed(1)}s]\n`;
      if (m.transcript_text) md += `> ${m.transcript_text}\n`;
      md += `\n`;
    }
  }
  const blob = new Blob([md], {type: "text/markdown"});
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${currentChat.contact_name.replace(/[^a-z0-9]/gi,'_')}_conversation.md`;
  link.click();
  URL.revokeObjectURL(url);
}

function escapeHtml(s) {
  return String(s || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

search.oninput = (e) => { currentSearch = e.target.value.toLowerCase().trim(); if (currentChat) renderChat(); };

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") { currentChat = null; [...chatListEl.children].forEach(li => li.classList.remove("active")); renderChat(); return; }
  if (e.key === " " && document.activeElement.tagName !== "INPUT") {
    const audios = [...document.querySelectorAll("audio")];
    if (audios.length) { e.preventDefault(); const playing = audios.find(a => !a.paused); playing ? playing.pause() : audios[0].play(); }
    return;
  }
  if (e.key === "j" || e.key === "k") {
    if (!currentChat) return;
    const msgs = [...document.querySelectorAll(".msg")];
    const focus = document.activeElement;
    let idx = msgs.findIndex(m => m.classList.contains("focused"));
    if (e.key === "j") idx = Math.min(msgs.length - 1, idx + 1);
    else idx = Math.max(0, idx - 1);
    msgs.forEach(m => m.classList.remove("focused"));
    if (msgs[idx]) { msgs[idx].classList.add("focused"); msgs[idx].scrollIntoView({behavior:"smooth", block:"center"}); }
  }
});

// Auto-open first chat
if (chats.length) openChat(chats[0].chat_id);
</script>
</body>
</html>
"""


def main():
    print("Building static viewer (5 chats × recent msgs + audio)")
    named = load_named()
    print(f"  Loaded NAMED: {len(named)} known contacts")

    payload = {"chats": [], "transcripts_available": 0, "transcripts_missing": 0}

    # Define target chats (using NEW post-family-correction dir names)
    targets = [
        ("tier1_deep", "magali_carreras___wa_chat_595981225272_62", "Magali Carreras"),
        ("tier1_deep", "mom_sonia_weiss___wa_chat_595982515138_64", "Sonia Weiss (Mom)"),
        ("tier1_deep", "sister_kyrian_kiki___wa_chat_595985724135_111", "Kyrian 'Kiki' (sister)"),
        ("tier2_core", "dad_john_van_der_pol___wa_chat_595986138387_1265", "John van der Pol (Dad)"),
        ("tier2_core", "sister_luana_weiss___wa_chat_595985725366_99", "Luana Weiss (sister)"),
        ("tier3_extended", "grandma_riet_van_der_pol___wa_chat_31612495139_98", "Riet van der Pol (Grandma)"),
        # Tier3 — pick one with audio
        ("tier3_extended", None, None),  # search needed
    ]

    out = ANALYSIS_DIR / "viewer.html"
    data_count = {"audio_total": 0, "audio_with_tr": 0}

    for tier, hint, fallback_name in targets:
        chat_dir = None
        if hint:
            chat_dir = find_chat_dir(tier, hint)
        if not chat_dir:
            # For tier3_extended, find any with audio
            tier_dir = MSG_BASE / tier
            if tier_dir.exists():
                candidates = [d for d in tier_dir.iterdir() if (d / "messages.json").exists()]
                # Sort by audio count, take first with >5 audio
                def audio_count(d):
                    try:
                        data = json.loads((d / "messages.json").read_text())
                        msgs = data.get("messages", [])
                        return sum(1 for m in msgs if isinstance(m, dict) and m.get("type") == 2)
                    except: return 0
                candidates.sort(key=audio_count, reverse=True)
                for c in candidates:
                    if audio_count(c) >= 30:
                        chat_dir = c
                        break
                if not chat_dir and candidates:
                    chat_dir = candidates[0]
        if not chat_dir:
            print(f"  ⚠️  no chat dir for tier={tier}")
            continue

        c = serialize_chat(chat_dir, named)
        payload["chats"].append(c)
        # Count transcripts
        audio_msgs = [m for m in c["messages"] if m["type"] == 2]
        with_tr = [m for m in audio_msgs if m["transcript_text"]]
        data_count["audio_total"] += len(audio_msgs)
        data_count["audio_with_tr"] += len(with_tr)
        print(f"  ✅ {c['tier']}/{c['chat_id'][:60]} → {c['contact_name']}: "
              f"{len(c['messages'])} msgs, {len(audio_msgs)} audio, {len(with_tr)} transcribed")

    payload["transcripts_available"] = data_count["audio_with_tr"]
    payload["transcripts_missing"] = data_count["audio_total"] - data_count["audio_with_tr"]
    payload["generated_at"] = datetime.now(timezone.utc).isoformat()

    # Inject payload into HTML
    payload_str = json.dumps(payload, ensure_ascii=False, indent=1)
    html = HTML_TEMPLATE.replace("__PAYLOAD__", payload_str)

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"\nWrote {out.relative_to(REPO_ROOT)} ({out.stat().st_size:,} bytes)")
    print(f"Total: 5 chats, {data_count['audio_total']} audio msgs, "
          f"{data_count['audio_with_tr']} already transcribed")


if __name__ == "__main__":
    main()

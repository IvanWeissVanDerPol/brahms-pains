#!/usr/bin/env python3
"""Build a comprehensive offline viewer that embeds ALL 216 vCard-verified
contacts + 882 not-saved contacts (grouped).

Self-contained HTML — runs file:// without a server.

Usage:
    python3 scripts/build_full_viewer.py
"""
from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MSG_BASE = REPO / "SOURCE_OF_TRUTH" / "wa_messages"
ANALYSIS = MSG_BASE / "_ANALYSIS"
TRANSCRIPT_BASE = REPO / "SOURCE_OF_TRUTH" / "voice_note_transcripts"
AUDIO_BASE = REPO / "media" / "audio"

# Load vCard-resolved names
resolved = json.loads((ANALYSIS / "contacts_vcard_resolved.json").read_text())
jid_to_name = {e["jid_user"]: e["name"] for e in resolved["resolutions"]}
jid_to_dir = {e["jid_user"]: e["dirname"] for e in resolved["resolutions"]}

# Load not-saved contacts
not_saved = json.loads((ANALYSIS / "contacts_not_saved.json").read_text())


def format_msg(m: dict) -> str:
    """Format a message for the viewer."""
    if not isinstance(m, dict):
        return ""
    text = m.get("text") or ""
    ts = m.get("ts_iso", "")[:16] or m.get("ts", "")
    sender = "me" if m.get("from_me") else "them"
    type_ = m.get("type", 0)
    if type_ == 1:  # image
        return f'<div class="msg img"><span class="ts">{ts}</span> <span class="sender {sender}">[{sender}]</span> 📷 image</div>'
    if type_ == 2:  # audio
        dur = m.get("duration_s", 0)
        return f'<div class="msg audio"><span class="ts">{ts}</span> <span class="sender {sender}">[{sender}]</span> 🎤 audio {dur}s</div>'
    if type_ == 3:  # video
        return f'<div class="msg video"><span class="ts">{ts}</span> <span class="sender {sender}">[{sender}]</span> 🎥 video</div>'
    if type_ == 6:  # sticker
        return f'<div class="msg sticker"><span class="ts">{ts}</span> <span class="sender {sender}">[{sender}]</span> 🎭 sticker</div>'
    if type_ == 7:  # document
        return f'<div class="msg doc"><span class="ts">{ts}</span> <span class="sender {sender}">[{sender}]</span> 📄 doc</div>'
    if not text:
        return ""
    return f'<div class="msg text"><span class="ts">{ts}</span> <span class="sender {sender}">[{sender}]</span> <span class="msg-body">{html.escape(text[:500])}</span></div>'


def load_chat_messages(dir_path: Path, limit: int = 30) -> list:
    """Load last N messages from a chat directory."""
    if not (dir_path / "messages.json").exists():
        return []
    try:
        data = json.loads((dir_path / "messages.json").read_text())
    except Exception:
        return []
    msgs = data.get("messages", [])
    # Filter out empty/unsupported types
    valid = [m for m in msgs if isinstance(m, dict)]
    # Sort by ts_iso
    valid.sort(key=lambda m: m.get("ts_iso", m.get("ts", "")), reverse=True)
    return list(reversed(valid[-limit:]))  # last N, chronological


def build_chat_section(jid: str, name: str, tier: str, dir_name: str) -> str:
    """Build HTML section for one chat."""
    # Find the directory path
    dir_path = MSG_BASE / tier / dir_name
    msgs = load_chat_messages(dir_path, limit=40)

    if not msgs:
        return f'<section class="chat"><h3>{html.escape(name)}</h3><p class="muted">no messages</p></section>'

    msg_html = "\n".join(format_msg(m) for m in msgs if format_msg(m))
    return f'''<section class="chat" data-jid="{html.escape(jid)}" data-tier="{html.escape(tier)}">
  <header>
    <h3>{html.escape(name)}</h3>
    <span class="jid">{html.escape(jid)}</span>
    <span class="tier">{html.escape(tier)}</span>
    <span class="count">{len(msgs)} of total messages shown</span>
  </header>
  <div class="messages">
    {msg_html}
  </div>
</section>'''


def main():
    # Build sections for vCard-resolved contacts
    sections = []
    print(f"Building sections for {len(resolved['resolutions'])} vCard-resolved contacts...")
    for e in resolved["resolutions"]:
        try:
            section = build_chat_section(e["jid_user"], e["name"], e["tier"], e["dirname"])
            sections.append(section)
        except Exception as ex:
            print(f"  skip {e['name']}: {ex}")

    # Build not-saved contacts grouped
    not_saved_html = '<section class="not-saved"><h2>Not Saved in vCard ({} chats)</h2><details><summary>show</summary><ul>'.format(len(not_saved["chats"]))
    for u in not_saved["chats"][:50]:  # Limit to first 50 to keep file size reasonable
        name = u.get("provisional_name") or "unknown"
        not_saved_html += f'<li>{html.escape(u["tier"])} — {html.escape(name)} — {html.escape(u["jid"][:18])}</li>'
    if len(not_saved["chats"]) > 50:
        not_saved_html += f'<li>... and {len(not_saved["chats"]) - 50} more (see contacts_not_saved.json)</li>'
    not_saved_html += '</ul></details></section>'

    # Build stats
    total_msgs = 0
    for e in resolved["resolutions"]:
        p = MSG_BASE / e["tier"] / e["dirname"]
        if (p / "messages.json").exists():
            try:
                data = json.loads((p / "messages.json").read_text())
                total_msgs += len(data.get("messages", []))
            except: pass

    stats = {
        "generated_at": datetime.now().isoformat(),
        "vcard_contacts": len(resolved["resolutions"]),
        "not_saved_contacts": len(not_saved["chats"]),
        "total_messages_embedded": sum(1 for s in sections if "msg text" in s or "msg audio" in s),
    }

    html_doc = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Psycology — Full Conversation Viewer</title>
<style>
  :root {{
    --bg: #0a0a0a; --fg: #d4d4d4;
    --bg-1: #111; --bg-2: #1a1a1a;
    --fg-1: #e4e4e4; --fg-2: #a0a0a0; --fg-3: #707070;
    --me: #79c0ff; --them: #f5b97e;
    --accent: #58c4dc; --border: #2a2a2a; --hover: #1f1f1f;
    --mono: ui-monospace, "JetBrains Mono", "IBM Plex Mono", Consolas, monospace;
  }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; height: 100%; background: var(--bg); color: var(--fg); font-family: system-ui, -apple-system, sans-serif; font-size: 14px; }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .mono {{ font-family: var(--mono); font-size: 12.5px; }}
  .muted {{ color: var(--fg-3); }}

  .app {{ display: grid; grid-template-columns: 360px 1fr; grid-template-rows: 56px 1fr 28px; height: 100vh; }}
  .top {{ grid-column: 1 / -1; padding: 0 16px; display: flex; align-items: center; gap: 12px; border-bottom: 1px solid var(--border); background: var(--bg-1); }}
  .top h1 {{ margin: 0; font-size: 14px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; color: var(--fg-1); }}
  .top .meta {{ color: var(--fg-3); font-size: 12px; margin-left: auto; }}
  .top input {{ background: var(--bg-2); color: var(--fg); border: 1px solid var(--border); border-radius: 3px; padding: 4px 8px; font-size: 12px; min-width: 200px; }}

  .sidebar {{ background: var(--bg-1); border-right: 1px solid var(--border); overflow-y: auto; }}
  .sidebar h2 {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--fg-3); padding: 12px 16px 4px; margin: 0; border-bottom: 1px solid var(--border); }}
  .sidebar .chat-item {{ display: block; padding: 8px 16px; border-bottom: 1px solid var(--border); cursor: pointer; font-size: 13px; }}
  .sidebar .chat-item:hover {{ background: var(--hover); }}
  .sidebar .chat-item.active {{ background: var(--hover); border-left: 3px solid var(--accent); padding-left: 13px; }}
  .sidebar .chat-item .jid {{ display: block; font-family: var(--mono); font-size: 10.5px; color: var(--fg-3); margin-top: 2px; }}
  .sidebar .chat-item .tier {{ font-size: 10px; color: var(--fg-3); margin-left: 6px; }}

  .main {{ overflow-y: auto; padding: 0; }}
  .chat {{ padding: 16px 24px; border-bottom: 1px solid var(--border); }}
  .chat header {{ padding: 12px 0; border-bottom: 1px solid var(--border); margin-bottom: 12px; }}
  .chat h3 {{ margin: 0; font-size: 16px; font-weight: 500; color: var(--fg-1); }}
  .chat .jid {{ font-family: var(--mono); font-size: 11px; color: var(--fg-3); margin-left: 12px; }}
  .chat .tier {{ font-size: 10px; color: var(--accent); margin-left: 8px; padding: 2px 6px; border: 1px solid var(--border); border-radius: 3px; }}
  .chat .count {{ font-size: 11px; color: var(--fg-3); margin-left: 8px; }}

  .msg {{ padding: 4px 0; line-height: 1.5; font-size: 13.5px; }}
  .msg .ts {{ font-family: var(--mono); font-size: 10.5px; color: var(--fg-3); margin-right: 8px; }}
  .msg .sender.me {{ color: var(--me); font-weight: 500; }}
  .msg .sender.them {{ color: var(--them); font-weight: 500; }}
  .msg-body {{ color: var(--fg-1); }}
  .msg.img, .msg.video, .msg.audio, .msg.sticker, .msg.doc {{ font-style: italic; color: var(--fg-2); }}

  .bottom {{ grid-column: 1 / -1; padding: 0 16px; display: flex; align-items: center; gap: 12px; border-top: 1px solid var(--border); background: var(--bg-1); color: var(--fg-3); font-size: 11px; }}

  .not-saved {{ padding: 16px 24px; background: var(--bg-1); }}
  .not-saved h2 {{ font-size: 14px; margin: 0 0 12px; }}
  .not-saved ul {{ max-height: 400px; overflow-y: auto; font-family: var(--mono); font-size: 11px; }}
  .not-saved li {{ padding: 2px 0; color: var(--fg-2); }}
</style>
</head>
<body>
<div class="app">
  <div class="top">
    <h1>Psycology — Full Viewer</h1>
    <input type="text" id="search" placeholder="filter contacts..." />
    <span class="meta">{stats["vcard_contacts"]} vCard contacts · {stats["not_saved_contacts"]} not-saved · {stats["generated_at"][:19]}</span>
  </div>

  <div class="sidebar" id="sidebar">
    <h2>vCard Contacts ({len(resolved["resolutions"])})</h2>
    {"".join(f'<div class="chat-item" data-target="chat-{i}"><strong>{html.escape(e["name"])}</strong><span class="tier">{html.escape(e["tier"][:14])}</span><span class="jid">{html.escape(e["jid_user"])}</span></div>' for i, e in enumerate(resolved["resolutions"]))}
    <h2 style="margin-top: 20px;">Not Saved ({len(not_saved["chats"])})</h2>
  </div>

  <div class="main">
    {chr(10).join(f'<section class="chat" id="chat-{i}" data-jid="{html.escape(e["jid_user"])}">' + build_chat_section(e["jid_user"], e["name"], e["tier"], e["dirname"]).split(">", 1)[1] if False else build_chat_section(e["jid_user"], e["name"], e["tier"], e["dirname"]) for i, e in enumerate(resolved["resolutions"]))}
    {not_saved_html}
  </div>

  <div class="bottom">
    Generated {stats["generated_at"][:19]} UTC · {stats["vcard_contacts"]} vCard contacts embedded · Use sidebar to jump
  </div>
</div>

<script>
  // Search/filter
  const search = document.getElementById("search");
  const items = document.querySelectorAll(".sidebar .chat-item");
  search.addEventListener("input", () => {{
    const q = search.value.toLowerCase();
    items.forEach(item => {{
      item.style.display = item.textContent.toLowerCase().includes(q) ? "" : "none";
    }});
  }});
  // Click sidebar item to scroll
  items.forEach(item => {{
    item.addEventListener("click", () => {{
      items.forEach(i => i.classList.remove("active"));
      item.classList.add("active");
      const target = document.getElementById(item.dataset.target);
      if (target) target.scrollIntoView({{behavior: "smooth", block: "start"}});
    }});
  }});
</script>
</body>
</html>'''

    out_path = ANALYSIS / "viewer_full.html"
    out_path.write_text(html_doc)
    print(f"Wrote {out_path.relative_to(REPO)} ({len(html_doc):,} bytes)")


if __name__ == "__main__":
    main()
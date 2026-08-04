#!/usr/bin/env python3
"""Build a compact viewer with metadata only (no inline messages).

Outputs a JSON + a small HTML that loads the JSON lazily. ~50KB.
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MSG_BASE = REPO / "SOURCE_OF_TRUTH" / "wa_messages"
ANALYSIS = MSG_BASE / "_ANALYSIS"

resolved = json.loads((ANALYSIS / "contacts_vcard_resolved.json").read_text())
not_saved = json.loads((ANALYSIS / "contacts_not_saved.json").read_text())


def get_chat_stats(dir_path: Path) -> dict:
    """Get stats for one chat directory."""
    if not (dir_path / "messages.json").exists():
        return None
    try:
        data = json.loads((dir_path / "messages.json").read_text())
    except Exception:
        return None
    msgs = data.get("messages", [])
    if not msgs:
        return None
    # Stats
    n_total = len(msgs)
    n_from_me = sum(1 for m in msgs if isinstance(m, dict) and m.get("from_me"))
    n_from_them = n_total - n_from_me
    # First / last
    first = msgs[0] if msgs else {}
    last = msgs[-1] if msgs else {}
    first_ts = first.get("ts_iso", "")[:10] if isinstance(first, dict) else ""
    last_ts = last.get("ts_iso", "")[:10] if isinstance(last, dict) else ""
    # Last message preview
    last_text = ""
    for m in reversed(msgs):
        if isinstance(m, dict) and m.get("type") == 0 and m.get("text"):
            last_text = m["text"][:120]
            break
    # Type breakdown
    types = defaultdict(int)
    for m in msgs:
        if isinstance(m, dict):
            types[m.get("type", 0)] += 1
    return {
        "total": n_total,
        "from_me": n_from_me,
        "from_them": n_from_them,
        "first": first_ts,
        "last": last_ts,
        "types": dict(types),
        "last_msg": last_text,
    }


def main():
    contacts = []
    print(f"Building data for {len(resolved['resolutions'])} vCard contacts...")
    for e in resolved["resolutions"]:
        p = MSG_BASE / e["tier"] / e["dirname"]
        stats = get_chat_stats(p)
        if stats:
            contacts.append(
                {
                    "jid": e["jid_user"],
                    "name": e["name"],
                    "tier": e["tier"],
                    "dir": e["dirname"],
                    **stats,
                }
            )

    # Sort by total messages
    contacts.sort(key=lambda c: -c["total"])

    out = {
        "generated_at": datetime.now().isoformat(),
        "vcard_contacts": contacts,
        "not_saved_chats": not_saved["chats"],
        "totals": {
            "vcard_count": len(contacts),
            "vcard_messages": sum(c["total"] for c in contacts),
            "not_saved_count": len(not_saved["chats"]),
        },
    }
    out_path = ANALYSIS / "viewer_full_data.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"Wrote {out_path.relative_to(REPO)}")
    print(f"  {out['totals']['vcard_count']} contacts")
    print(f"  {out['totals']['vcard_messages']:,} total messages")
    print(f"  {out['totals']['not_saved_count']} not-saved chats")

    # Top 10
    print()
    print("=== Top 10 by message count ===")
    for c in contacts[:10]:
        print(f"  {c['total']:>6,}  {c['name'][:30]:<30}  ({c['first'][:7]} → {c['last'][:7]})")


if __name__ == "__main__":
    main()

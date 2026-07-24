#!/usr/bin/env python3
"""Generate profile stubs for named chats that don't have profiles yet.

Reads viewer_full_data.json and creates minimal profiles for contacts that:
1. Are in vCard (have a phonebook-resolved name)
2. Don't have a profile yet in RELATIONSHIPS/dynamics/

Each profile is a stub with TODO sections for the user to fill in.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS"
PROFILE_DIR = REPO / "RELATIONSHIPS" / "dynamics"


def safe_name(name: str) -> str:
    """Convert name to a profile-safe slug (caps, underscores)."""
    s = name.upper()
    s = s.replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")
    s = s.replace("Ñ", "N")
    # Keep A-Z and 0-9, replace others with _
    s = re.sub(r"[^A-Z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s


def main():
    data = json.loads((ANALYSIS / "viewer_full_data.json").read_text())
    contacts = data["vcard_contacts"]

    # Find existing profiles
    existing = {p.stem for p in PROFILE_DIR.glob("*.md")}
    print(f"Existing profiles: {len(existing)}")

    # Find contacts without profiles
    to_create = []
    for c in contacts:
        slug = safe_name(c["name"])
        if slug not in existing:
            to_create.append((c, slug))

    print(f"Need to create: {len(to_create)}")
    print()
    print("Sample:")
    for c, slug in to_create[:10]:
        print(f"  {slug:<25}  {c['name'][:30]:<30}  ({c['total']} msgs)")

    # Generate profiles
    now = datetime.now().isoformat()[:19]
    created = 0
    for c, slug in to_create:
        name = c["name"]
        jid = c["jid"]
        tier = c["tier"]
        n_total = c["total"]
        first = c["first"]
        last = c["last"]

        content = f'''# {name}

> **Auto-generated profile stub** ({now})
> **Source:** vCard phonebook (full export 2026-07-23)
> **JID:** {jid}
> **Tier:** {tier}
> **Stats:** {n_total:,} messages · {first[:10] if first else "—"} → {last[:10] if last else "—"}

## Overview

TODO: relationship context, how you know this person, dynamic summary.

## Communication stats

| Metric | Value |
|--------|-------|
| Total messages | {n_total:,} |
| First message | {first or "—"} |
| Last message | {last or "—"} |

## Key moments / Topics

TODO: extract 3-5 key moments from this chat — milestones, big fights, important conversations.

## Notes

TODO: anything else Ivan has shared or knows about this person.

## Profile sources

- vCard phonebook (full export, 2026-07-23): name "{name}"
- Self-intro analysis: pending
- Group context: pending
- Behavioral signals: pending
'''
        out_path = PROFILE_DIR / f"{slug}.md"
        out_path.write_text(content)
        created += 1

    print(f"\nCreated {created} profile stubs")


if __name__ == "__main__":
    main()
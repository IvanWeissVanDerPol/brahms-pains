#!/usr/bin/env python3
"""Bulk-generate profile stubs for named chats that don't have profiles yet.

Reads SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/name_mining_round2.json +
walks tier1_deep/tier2_core/tier3_extended/untiered_personal to find
named contacts without profiles in RELATIONSHIPS/dynamics/.

For each, generates a minimal profile stub with:
  - Name + tier + JID
  - Msg count + audio count + dates
  - Brief content sample (first 50 words from each side)
  - Cross-reference to source chat dir
  - TODO for human review

USAGE:
    python3 scripts/generate_profile_stubs.py --dry-run
    python3 scripts/generate_profile_stubs.py --apply
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MSG_BASE = REPO / "SOURCE_OF_TRUTH" / "wa_messages"
PROFILE_DIR = REPO / "RELATIONSHIPS" / "dynamics"


# Slugify
def slugify(name):
    n = name.lower().strip()
    n = re.sub(r"[^a-z0-9_]+", "_", n)
    n = re.sub(r"_+", "_", n).strip("_")
    return n.upper()


# Tier priorities (for content depth in stub)
TIER_DEPTH = {
    "tier1_deep": "DEEP",
    "tier2_core": "CORE",
    "tier3_extended": "EXTENDED",
    "untiered_personal": "PERSONAL",
}


def collect_named_chats(min_msgs=100):
    """Walk tiers, find named chats with ≥ min_msgs."""
    out = []
    TIERS = ["tier1_deep", "tier2_core", "tier3_extended", "untiered_personal"]
    for tier in TIERS:
        td = MSG_BASE / tier
        if not td.exists():
            continue
        for d in td.iterdir():
            if not (d / "messages.json").exists():
                continue
            try:
                data = json.loads((d / "messages.json").read_text())
            except Exception:
                continue
            prov = data.get("__provisional_name", {})
            nm = prov.get("name", "") if isinstance(prov, dict) else ""
            if not nm:
                continue
            n = len(data.get("messages", []))
            if n < min_msgs:
                continue
            jid = str(data.get("jid_user", ""))
            # Date range
            dates = [
                m.get("ts_ms", 0)
                for m in data.get("messages", [])
                if isinstance(m, dict) and m.get("ts_ms")
            ]
            if dates:
                import datetime

                first = datetime.datetime.fromtimestamp(min(dates) / 1000).strftime("%Y-%m-%d")
                last = datetime.datetime.fromtimestamp(max(dates) / 1000).strftime("%Y-%m-%d")
            else:
                first = last = "?"
            # Audio
            audio_n = sum(
                1 for m in data.get("messages", []) if isinstance(m, dict) and m.get("type") == 2
            )
            # Image
            img_n = sum(
                1 for m in data.get("messages", []) if isinstance(m, dict) and m.get("type") == 1
            )
            # Content sample — first text msgs from each side
            them_sample = []
            ivan_sample = []
            for m in data.get("messages", []):
                if isinstance(m, dict) and m.get("type") == 0 and m.get("text"):
                    if m.get("from_me"):
                        if len(ivan_sample) < 3:
                            ivan_sample.append(m["text"][:140])
                    else:
                        if len(them_sample) < 3:
                            them_sample.append(m["text"][:140])
                    if len(them_sample) >= 3 and len(ivan_sample) >= 3:
                        break
            out.append(
                {
                    "name": nm,
                    "tier": tier,
                    "tier_depth": TIER_DEPTH[tier],
                    "jid": jid,
                    "msgs": n,
                    "audio": audio_n,
                    "images": img_n,
                    "first": first,
                    "last": last,
                    "them_sample": them_sample,
                    "ivan_sample": ivan_sample,
                    "chat_dir": str(d.relative_to(REPO)),
                }
            )
    out.sort(key=lambda x: -x["msgs"])
    return out


def find_existing_profiles():
    """Returns set of slugs that have profiles."""
    out = set()
    for f in PROFILE_DIR.glob("*.md"):
        if f.stem.lower() in ("readme",):
            continue
        out.add(f.stem.upper())
    return out


def needs_profile(chat_name, existing):
    """Check if a profile already exists for this chat's name."""
    s = slugify(chat_name)
    if s in existing:
        return False
    # Also check first word
    first_word = s.split("_")[0]
    if first_word in existing:
        return False
    # Check for any partial match
    for e in existing:
        if s in e or e in s:
            return False
    return True


def make_stub(c):
    """Generate profile stub markdown content."""
    name = c["name"]
    title = f"# {name}\n\n"
    banner = f"""> **Status:** PROVISIONAL NAME — pending Ivan's confirmation.
> **Tier:** {c['tier_depth']} (`{c['tier']}`)
> **JID:** `{c['jid']}`
> **Generated:** 2026-07-23 by `scripts/generate_profile_stubs.py`

## Communication stats

| Metric | Value |
|--------|-------|
| Total messages | {c['msgs']:,} |
| Audio messages | {c['audio']:,} |
| Image messages | {c['images']:,} |
| First message | {c['first']} |
| Last message | {c['last']} |
| Source chat dir | `{c['chat_dir']}` |

## Content samples

**From {name} (first 3 text msgs):**
"""
    for s in c["them_sample"]:
        banner += f"> {s}\n"
    banner += "\n**From Ivan (first 3 text msgs):**\n"
    for s in c["ivan_sample"]:
        banner += f"> {s}\n"
    banner += """

## Relationship arc

*TODO* — Review chat to extract narrative arc, themes, and patterns.

## Themes

*TODO* — Use theme keyword scan (see scripts/extract_themes.py).

## Cross-references

- Source chat: `{chat_dir}`
- Profiles dir: `RELATIONSHIPS/dynamics/`

---

*Stub generated 2026-07-23. Replace this content with real analysis once chat is reviewed.*
""".replace("{chat_dir}", c["chat_dir"])
    return title + banner


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true")
    p.add_argument("--limit", type=int, default=50)
    args = p.parse_args()
    if not args.dry_run and not args.apply:
        args.dry_run = True

    chats = collect_named_chats(min_msgs=100)
    existing = find_existing_profiles()
    print(f"Named chats ≥100 msgs: {len(chats)}")
    print(f"Existing profiles: {len(existing)}")

    # Filter to those needing profiles
    # SKIP_JIDS: chats whose provisional name doesn't match their actual contact
    SKIP_JIDS = {
        "595981225272",  # ami_school is actually Magali (use MAGALI_CARRERAS.md)
        "595982515138",  # gabriel_g_curuguaty (wrong provisional; is mom_sonia_weiss)
        "595986138387",  # John (is dad_john_van_der_pol, has SONIA.md)
        "31612495139",  # Riet (is grandma_riet, has SONIA.md)
        "595982850085",  # Mica (is cousin_mica, has KIKI_HERMANA.md references)
        "15055778339",  # Toni (is uncle_antonio_toni, has SONIA.md)
        "595985786571",  # Primo Gabriel (has KIKI_HERMANA.md refs)
        "595985855075",  # Gerold (uncle, has SONIA.md refs)
    }
    SKIP_PROVISIONAL_NAMES = {
        "John",
        "Riet van der Pol",
        "Mica Weiss",
        "Toni Weiss",
        "Primo Gabriel",
        "ami_school",
        "gabriel_g_curuguaty",
    }
    to_create = [
        c
        for c in chats
        if needs_profile(c["name"], existing)
        and c["jid"] not in SKIP_JIDS
        and c["name"] not in SKIP_PROVISIONAL_NAMES
    ]
    to_create = to_create[: args.limit]
    print(f"Need profile stubs: {len(to_create)}")

    print()
    print("=" * 70)
    print(f"PROPOSED PROFILE STUBS ({len(to_create)})")
    print("=" * 70)
    for c in to_create:
        s = slugify(c["name"])
        print(
            f"  {s:<35}  msgs={c['msgs']:>6}  audio={c['audio']:>4}  tier={c['tier_depth']:<10}  jid={c['jid'][:14]}"
        )

    if args.dry_run:
        # Save the list
        out = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS" / "PROFILE_STUB_PROPOSALS.json"
        out.write_text(
            json.dumps(
                {
                    "generated_at": str(__import__("datetime").datetime.now()),
                    "total_proposed": len(to_create),
                    "stubs": to_create,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        print(f"\nWrote {out.relative_to(REPO)}")
        return

    # Apply
    print()
    print("=" * 70)
    print("APPLY MODE — creating profile stubs")
    print("=" * 70)
    for c in to_create:
        s = slugify(c["name"])
        path = PROFILE_DIR / f"{s}.md"
        if path.exists():
            print(f"  ⚠️  exists: {path.name}")
            continue
        content = make_stub(c)
        path.write_text(content)
        print(f"  ✓ {path.name}")

    print(f"\nCreated {len(to_create)} profile stubs in {PROFILE_DIR.relative_to(REPO)}")


if __name__ == "__main__":
    main()

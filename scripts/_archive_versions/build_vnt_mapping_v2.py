#!/usr/bin/env python3
"""Build comprehensive VNT folder rename mapping using chat directory names + vCard."""

from __future__ import annotations

import json
import re
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).resolve().parent.parent
VNT = REPO / "SOURCE_OF_TRUTH" / "voice_note_transcripts"
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages/_ANALYSIS"
WA_MESSAGES = REPO / "SOURCE_OF_TRUTH" / "wa_messages"


def safe_name(name: str) -> str:
    """Make a name filesystem-safe."""
    if not name:
        return ""
    s = re.sub(r"[^\w\s-]", "", name).strip()
    s = re.sub(r"\s+", "_", s)
    return s


def main():
    # Load vCard names mapping (JID -> name)
    vcard = json.loads((ANALYSIS / "viewer_full_data.json").read_text())
    jid_to_name = {c["jid"]: c["name"] for c in vcard["vcard_contacts"]}

    # Also load contacts_vcard_resolved.json
    if (ANALYSIS / "contacts_vcard_resolved.json").exists():
        resolved = json.loads((ANALYSIS / "contacts_vcard_resolved.json").read_text())
        # Check structure
        if isinstance(resolved, dict):
            for k, v in list(resolved.items())[:3]:
                print(
                    f"  resolved.{k} = {v if not isinstance(v, (list, dict)) else type(v).__name__}"
                )
        else:
            print(f"  resolved: list of {len(resolved)}")

    # Walk all wa_messages directories and build JID -> {canonical_name, tier}
    jid_info = {}

    # Iterate all chats
    for tier in [
        "tier1_deep",
        "tier2_core",
        "tier3_extended",
        "tier4_groups",
        "untiered_personal",
        "other_lid",
        "circles",
        "_dropped",
        "_conversations",
    ]:
        tier_dir = WA_MESSAGES / tier
        if not tier_dir.exists():
            continue
        for d in tier_dir.iterdir():
            if not d.is_dir():
                continue

            # Extract JID
            m = re.search(r"(\d{10,15})", d.name)
            if not m:
                continue
            jid = m.group(1)
            if jid in jid_info:
                continue  # take first occurrence

            # Try to get canonical name
            canonical = None

            # 1. vCard match
            if jid in jid_to_name:
                canonical = jid_to_name[jid]

            # 2. Already-renamed dir name (e.g., "magali_carreras_amiga_fpuna____wa_chat_...")
            if not canonical:
                # The dir name has the canonical name as prefix
                # Pattern: {name}____wa_chat_{jid}_{idx}
                dir_name = d.name
                m2 = re.match(r"^([a-z_]+(?:_[a-z_]+)*)____", dir_name)
                if m2:
                    possible_name = m2.group(1).replace("_", " ").title()
                    if len(possible_name) > 3:
                        canonical = possible_name

            # 3. Sender name from messages.json
            if not canonical:
                mf = d / "messages.json"
                if mf.exists():
                    try:
                        data = json.loads(mf.read_text())
                        # Try first 20 messages for "soy X" pattern
                        for msg in data.get("messages", [])[:20]:
                            if isinstance(msg, dict) and msg.get("text"):
                                text = msg["text"].lower()
                                m3 = re.search(r"soy ([a-záéíóúñ ]{2,30})", text)
                                if m3:
                                    canonical = m3.group(1).strip().title()
                                    break
                    except:
                        pass

            jid_info[jid] = {
                "dir_name": d.name,
                "tier": tier,
                "canonical": canonical,
            }

    print(f"Total JID info: {len(jid_info)}")
    print(f"  With canonical name: {sum(1 for v in jid_info.values() if v['canonical'])}")
    print(f"  Without: {sum(1 for v in jid_info.values() if not v['canonical'])}")

    # Walk all VNT folders
    mapping = []
    for d in VNT.iterdir():
        if not d.is_dir():
            continue

        if d.name.startswith("_"):
            mapping.append(
                {
                    "folder": d.name,
                    "jid": None,
                    "canonical": d.name,
                    "tier": "special",
                    "action": "skip",
                    "safe_name": d.name,
                }
            )
            continue
        if d.name in [
            "Laura",
            "Ara_Nunez_Poli",
            "Cookie",
            "Defi",
            "Jonatan_Verdun",
            "Lourdes_Youko_Kurama",
            "Magali_Carreras",
        ]:
            mapping.append(
                {
                    "folder": d.name,
                    "jid": None,
                    "canonical": d.name,
                    "tier": "named",
                    "action": "skip",
                    "safe_name": d.name,
                }
            )
            continue

        m = re.search(r"(\d{10,15})", d.name)
        if not m:
            mapping.append(
                {
                    "folder": d.name,
                    "jid": None,
                    "canonical": None,
                    "tier": "unknown",
                    "action": "skip",
                    "safe_name": d.name,
                }
            )
            continue

        jid = m.group(1)
        info = jid_info.get(jid, {})
        canonical = info.get("canonical")

        if canonical:
            safe = safe_name(canonical)
            action = "rename" if safe != d.name else "skip"
        else:
            safe = d.name
            action = "skip"

        mapping.append(
            {
                "folder": d.name,
                "jid": jid,
                "canonical": canonical,
                "safe_name": safe,
                "tier": info.get("tier", "?"),
                "action": action,
            }
        )

    # Stats
    by_action = defaultdict(int)
    by_tier = defaultdict(int)
    for m in mapping:
        by_action[m["action"]] += 1
        by_tier[m["tier"]] += 1

    print("\n=== Actions ===")
    for a, n in by_action.items():
        print(f"  {a}: {n}")
    print("\n=== Tiers ===")
    for t, n in by_tier.items():
        print(f"  {t}: {n}")

    out = {
        "generated_at": "2026-07-25",
        "total_folders": len(mapping),
        "by_action": dict(by_action),
        "by_tier": dict(by_tier),
        "mappings": mapping,
    }
    out_path = REPO / "SOURCE_OF_TRUTH" / "voice_note_transcripts" / "_mapping.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False, default=str))
    print(f"\nWrote {out_path.relative_to(REPO)}")

    # Show first 20 renames
    print("\n=== Sample renames (first 25) ===")
    for m in mapping:
        if m["action"] == "rename":
            print(f"  {m['folder']:<40} -> {m['safe_name']:<35} ({m['tier']}, {m['canonical']})")


if __name__ == "__main__":
    main()

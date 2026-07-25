#!/usr/bin/env python3
"""Build mapping from voice_note_transcripts folders to canonical contact names."""
from __future__ import annotations

import json
import re
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).resolve().parent.parent
VNT = REPO / "SOURCE_OF_TRUTH" / "voice_note_transcripts"
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages/_ANALYSIS"
WA_MESSAGES = REPO / "SOURCE_OF_TRUTH" / "wa_messages"


def main():
    # Load vCard names mapping
    vcard = json.loads((ANALYSIS / "viewer_full_data.json").read_text())
    jid_to_name = {c["jid"]: c["name"] for c in vcard["vcard_contacts"]}

    # Also load contacts.vcf to get more
    contacts_vcf = {}
    if (ANALYSIS / "contacts.vcf").exists():
        vcf_text = (ANALYSIS / "contacts.vcf").read_text()
        for m in re.finditer(r"FN:([^\n]+)\n.*?TEL.*?(\+\d+)", vcf_text, re.DOTALL):
            name = m.group(1).strip()
            tel = m.group(2).replace("+", "").replace(" ", "")
            contacts_vcf[tel] = name

    # Load wa_messages metadata to find which JID belongs to which dir
    jid_to_dir = {}
    for tier in ["tier1_deep", "tier2_core", "tier3_extended", "tier4_groups",
                  "untiered_personal", "other_lid", "circles", "_dropped", "_conversations"]:
        tier_dir = WA_MESSAGES / tier
        if not tier_dir.exists(): continue
        for d in tier_dir.iterdir():
            if not d.is_dir(): continue
            # Extract JID from dir name
            m = re.search(r'(\d{10,15})', d.name)
            if not m: continue
            jid = m.group(1)
            if jid in jid_to_dir: continue  # take first

            # Get canonical name from messages.json
            mf = d / "messages.json"
            if mf.exists():
                try:
                    data = json.loads(mf.read_text())
                    sender_name = data.get("jid_user", "")
                    if not sender_name:
                        # Try to get from messages
                        for m_msg in data.get("messages", [])[:5]:
                            if isinstance(m_msg, dict) and m_msg.get("text"):
                                # Look for "soy X" pattern
                                text = m_msg["text"].lower()
                                intro = re.search(r'soy ([a-záéíóúñ ]{2,30})', text)
                                if intro:
                                    sender_name = intro.group(1).strip()
                                    break
                except: pass

            jid_to_dir[jid] = {
                "dir_name": d.name,
                "tier": tier,
                "sender_name": sender_name,
            }

    # Now match VNT folder names to JIDs
    print(f"Loaded {len(jid_to_name)} vCard names")
    print(f"Loaded {len(contacts_vcf)} vcf contacts")
    print(f"Loaded {len(jid_to_dir)} JID -> dir mappings\n")

    # Walk all VNT folders
    mapping = []  # list of {folder, jid, canonical_name, tier, action}
    for d in VNT.iterdir():
        if not d.is_dir(): continue
        if d.name.startswith("_"):
            # special: _wa_ptt_bulk, _documents_ivan_voice, _w4b_unmapped
            mapping.append({
                "folder": d.name,
                "jid": None,
                "canonical_name": d.name,
                "tier": "special",
                "action": "skip",
            })
            continue
        if d.name in ["Laura", "Ara_Nunez_Poli", "Cookie", "Defi",
                      "Jonatan_Verdun", "Lourdes_Youko_Kurama", "Magali_Carreras"]:
            # Already named correctly
            mapping.append({
                "folder": d.name,
                "jid": None,
                "canonical_name": d.name,
                "tier": "named",
                "action": "skip",
            })
            continue

        # Extract JID from folder name
        m = re.search(r'(\d{10,15})', d.name)
        if not m:
            mapping.append({
                "folder": d.name,
                "jid": None,
                "canonical_name": d.name,
                "tier": "unknown",
                "action": "skip",
            })
            continue

        jid = m.group(1)
        # Get name from vCard
        canonical = jid_to_name.get(jid)
        if not canonical:
            # Try matching phone prefix
            canonical = contacts_vcf.get(jid)
        if not canonical:
            # Try by sender_name
            info = jid_to_dir.get(jid)
            if info and info.get("sender_name"):
                canonical = info["sender_name"]

        tier = jid_to_dir.get(jid, {}).get("tier", "?")

        if canonical:
            # Make safe filename
            safe = re.sub(r'[^\w\s-]', '', canonical).strip()
            safe = re.sub(r'\s+', '_', safe)
            action = "rename" if safe != d.name else "skip"
        else:
            safe = d.name
            action = "skip"

        mapping.append({
            "folder": d.name,
            "jid": jid,
            "canonical_name": canonical,
            "safe_name": safe,
            "tier": tier,
            "action": action,
        })

    # Stats
    by_action = defaultdict(int)
    by_tier = defaultdict(int)
    for m in mapping:
        by_action[m["action"]] += 1
        by_tier[m["tier"]] += 1

    print("=== Actions ===")
    for a, n in by_action.items():
        print(f"  {a}: {n}")
    print("\n=== Tiers ===")
    for t, n in by_tier.items():
        print(f"  {t}: {n}")

    # Save mapping
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

    # Show samples
    print("\n=== Sample rename proposals (first 15) ===")
    for m in mapping:
        if m["action"] == "rename":
            print(f"  {m['folder']} -> {m['safe_name']}  (JID {m['jid']}, tier {m['tier']}, name {m['canonical_name']})")
            if len([x for x in mapping if x['action'] == 'rename']) > 15:
                break


if __name__ == "__main__":
    main()

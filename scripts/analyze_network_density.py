#!/usr/bin/env python3
"""Friendship network density analysis (Hat 14, 17)."""

from __future__ import annotations

import json
from pathlib import Path
from collections import Counter
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH/wa_messages/_ANALYSIS"


def analyze_network_density():
    """Find how interconnected Ivan's friends are (co-group membership)."""
    # Load group data
    gp = json.loads((ANALYSIS / "group_participation.json").read_text())

    # Load tier1/tier2 contacts as the "main social network"
    WA = REPO / "SOURCE_OF_TRUTH/wa_messages"

    # Build JID-to-name mapping from tier1/tier2 + tier3
    jid_to_name = {}
    jid_to_tier = {}

    # Also load phonebook.json for name resolution
    phonebook = (
        json.loads((ANALYSIS / "phonebook.json").read_text())
        if (ANALYSIS / "phonebook.json").exists()
        else []
    )

    # Build jid -> name from phonebook
    phonebook_jid_map = {}
    for entry in phonebook.get("contacts", []):
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        if not name:
            continue
        # Map all phone variants
        phones = entry.get("phones_normalized", []) + entry.get("phones_raw", [])
        for phone in phones:
            phonebook_jid_map[str(phone)] = name
            phonebook_jid_map[str(phone) + "@s.whatsapp.net"] = name
            phonebook_jid_map[str(phone) + "@c.us"] = name

    for tier in ["tier1_deep", "tier2_core", "tier3_extended"]:
        d = WA / tier
        if not d.exists():
            continue
        for chat in d.iterdir():
            if not chat.is_dir():
                continue
            mf = chat / "messages.json"
            if not mf.exists():
                continue
            try:
                data = json.loads(mf.read_text())
            except:
                continue
            msgs = data.get("messages", [])
            if not msgs:
                continue

            chat_name = chat.name.split("___")[0][:30]
            # Get unique senders (other people)
            senders = set()
            for m in msgs:
                if isinstance(m, dict) and m.get("sender_jid"):
                    senders.add(m["sender_jid"])

            for sender in senders:
                if sender not in jid_to_name:
                    # Try phonebook lookup first
                    clean_jid = sender.replace("@s.whatsapp.net", "").replace("@c.us", "")
                    jid_to_name[sender] = (
                        phonebook_jid_map.get(sender)
                        or phonebook_jid_map.get(clean_jid)
                        or chat_name
                    )
                    jid_to_tier[sender] = tier

    # Now check group participation - who is in groups together
    print(f"Building network from {len(gp['per_group'])} group chats...")

    # Build edges: pairs of contacts who share a group
    edges = Counter()
    contacts = set()

    for group_name, info in gp["per_group"].items():
        # Read messages to find unique senders
        chat_path = WA / "tier4_groups" / group_name / "messages.json"
        if not chat_path.exists():
            continue
        try:
            data = json.loads(chat_path.read_text())
        except:
            continue

        senders = set()
        for m in data.get("messages", []):
            if isinstance(m, dict) and m.get("sender_jid"):
                senders.add(m["sender_jid"])

        # Add Ivan to senders if he participated
        if info["ivan_msgs"] > 0:
            # Ivan's JID is in messages
            for m in data.get("messages", []):
                if isinstance(m, dict) and m.get("from_me"):
                    sender = m.get("sender_jid")
                    if sender:
                        senders.add(sender)
                    break

        # Build edges between all pairs
        sender_list = sorted(senders)
        for i in range(len(sender_list)):
            for j in range(i + 1, len(sender_list)):
                edge = tuple(sorted([sender_list[i], sender_list[j]]))
                edges[edge] += 1
                contacts.add(sender_list[i])
                contacts.add(sender_list[j])

    # Calculate network metrics
    n_contacts = len(contacts)
    n_edges = len(edges)

    # Top connected nodes
    degree = Counter()
    for (a, b), count in edges.items():
        degree[a] += 1
        degree[b] += 1

    # Build summary
    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_contacts_in_network": n_contacts,
        "total_edges": n_edges,
        "top_connected_contacts": [
            {"jid": jid, "name": jid_to_name.get(jid, "?"), "degree": deg}
            for jid, deg in degree.most_common(20)
        ],
        "top_edges": [
            {"jid_a": a, "jid_b": b, "shared_groups": count}
            for (a, b), count in edges.most_common(20)
        ],
    }

    out = ANALYSIS / "network_density.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"Wrote {out.relative_to(REPO)}")

    print("\n=== Friendship Network Density ===")
    print(f"Total contacts in network: {n_contacts}")
    print(f"Total edges (shared groups): {n_edges}")

    print("\nTop 20 most connected contacts:")
    for i, contact in enumerate(summary["top_connected_contacts"][:20], 1):
        print(
            f"  {i:>3}. {contact['degree']:>3} edges  {contact['name']:<35} ({contact['jid'][:15]}...)"
        )

    print("\nTop 20 strongest edges (most shared groups):")
    for i, edge in enumerate(summary["top_edges"][:20], 1):
        name_a = jid_to_name.get(edge["jid_a"], "?")
        name_b = jid_to_name.get(edge["jid_b"], "?")
        print(f"  {i:>3}. {edge['shared_groups']:>2} groups  {name_a:<25} + {name_b:<25}")


if __name__ == "__main__":
    analyze_network_density()

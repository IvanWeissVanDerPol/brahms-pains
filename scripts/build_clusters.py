#!/usr/bin/env python3
"""Build relationship clusters: groups of people who all chat with each other.

Method:
1. For each pair of contacts that Ivan chats with, check if they appear
   in the same group chats together
2. If Ivan mentions person A in chat with person B, link A-B
3. If A and B are both contacts, add edge between them
4. Build community graph and cluster
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS"
MSG_BASE = REPO / "SOURCE_OF_TRUTH" / "wa_messages"


def find_phone_mentions(text: str) -> list[str]:
    """Extract phone numbers from message text."""
    if not text:
        return []
    phones = []
    # +595 9XX XXXXXX, 09XX XXXXXX, etc
    for m in re.finditer(r"\+?595[\s\-]?9\d{2}[\s\-]?\d{3}[\s\-]?\d{3}", text):
        phones.append(re.sub(r"\D", "", m.group()))
    for m in re.finditer(r"\b09\d{2}[\s\-]?\d{3}[\s\-]?\d{3}\b", text):
        phones.append(re.sub(r"\D", "", m.group()))
    return list(set(phones))


def find_name_mentions(text: str, contact_names: set[str]) -> list[str]:
    """Find contact names mentioned in message text."""
    if not text:
        return []
    text_low = text.lower()
    found = []
    for name in contact_names:
        # Check both full name and first name
        if len(name) < 4:
            continue
        if name in text_low:
            found.append(name)
    return found


def main():
    data = json.loads((ANALYSIS / "viewer_full_data.json").read_text())
    contacts = data["vcard_contacts"]

    # JID → name lookup
    jid_to_name = {c["jid"]: c["name"] for c in contacts}
    jid_to_dir = {c["jid"]: c for c in contacts}
    name_to_jid = {c["name"]: c["jid"] for c in contacts}

    # Contact name set (for mention detection)
    contact_names = set(name_to_jid.keys())
    # Also add first names
    first_names = set()
    for name in contact_names:
        parts = name.split()
        if parts:
            first_names.add(parts[0].lower())

    # Walk all chats, find co-occurrences in groups + name mentions
    edges = defaultdict(int)  # (jid_a, jid_b) -> weight
    edge_evidence = defaultdict(list)  # (jid_a, jid_b) -> [evidence]

    TIERS = [
        "tier1_deep",
        "tier2_core",
        "tier3_extended",
        "tier4_groups",
        "untiered_personal",
        "other_lid",
        "_dropped",
    ]

    print(f"Walking {len(contacts)} chats + tier4_groups for co-occurrences...")

    # First: tier4_groups gives direct co-occurrence
    tier4_dir = MSG_BASE / "tier4_groups"
    if tier4_dir.exists():
        for d in tier4_dir.iterdir():
            if not (d / "messages.json").exists():
                continue
            try:
                data = json.loads((d / "messages.json").read_text())
            except:
                continue
            # Find JIDs mentioned in messages
            for m in data.get("messages", []):
                if not isinstance(m, dict):
                    continue
                # The jid_user of the group itself often has participants
                # For each non-group JID we know, check if mentioned
                text = m.get("text") or ""
                if not text:
                    continue
                # Find names mentioned
                names_found = find_name_mentions(text, contact_names)
                for n in names_found:
                    if n in name_to_jid:
                        # The "source" is the person who sent the message (if from a known contact)
                        pass  # We need to know the sender

    # Better approach: for each personal chat, find names mentioned in messages
    # If Ivan mentions person X while chatting with person Y, link X-Y
    print("Scanning personal chats for cross-references...")

    cross_refs = defaultdict(lambda: defaultdict(int))  # chat_jid -> {other_name: count}

    for c in contacts:
        chat_dir = MSG_BASE / c["tier"] / c["dir"]
        if not (chat_dir / "messages.json").exists():
            continue
        try:
            data = json.loads((chat_dir / "messages.json").read_text())
        except:
            continue
        msgs = data.get("messages", [])
        for m in msgs:
            if not isinstance(m, dict):
                continue
            text = m.get("text") or ""
            if not text:
                continue
            # Find other contact names mentioned
            names_found = find_name_mentions(text, contact_names)
            for n in names_found:
                if n in name_to_jid and name_to_jid[n] != c["jid"]:
                    cross_refs[c["jid"]][n] += 1

    # Build edges from cross-refs
    for source_jid, mentioned in cross_refs.items():
        for name, count in mentioned.items():
            target_jid = name_to_jid[name]
            # Add edge
            a, b = sorted([source_jid, target_jid])
            edges[(a, b)] += count
            if len(edge_evidence[(a, b)]) < 3:
                edge_evidence[(a, b)].append(
                    f"{jid_to_name[a]} ↔ {jid_to_name[b]}: {count} cross-refs"
                )

    # Also add edges from group co-membership
    # For each tier4_groups chat, the participants are in a shared group
    # We don't have the participant list, but the JIDs of contacts that share a group
    # are the JIDs that have entries in the same group
    # Skip for now (we'd need to parse group metadata)

    # Build adjacency
    print(f"Built {len(edges)} edges")

    # Simple community detection: greedy clustering
    # Each node starts in its own cluster
    # Iterate: merge two clusters if they have more than K edges between them
    parent = {jid: jid for jid in jid_to_name}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            # Merge smaller into larger
            # Use a deterministic rule
            if ra < rb:
                parent[rb] = ra
            else:
                parent[ra] = rb

    # Sort edges by weight desc, merge top edges
    sorted_edges = sorted(edges.items(), key=lambda x: -x[1])
    MERGE_THRESHOLD = 2  # Need at least 2 cross-refs to merge
    merged = 0
    for (a, b), weight in sorted_edges:
        if weight >= MERGE_THRESHOLD and find(a) != find(b):
            union(a, b)
            merged += 1
            if merged > 500:
                break  # don't merge everything

    # Group by cluster
    clusters = defaultdict(list)
    for jid in jid_to_name:
        clusters[find(jid)].append(jid)

    # Sort clusters by size
    cluster_list = sorted(clusters.values(), key=lambda c: -len(c))

    # Top 20 clusters
    print()
    print("=== Top 20 clusters ===")
    for i, cluster in enumerate(cluster_list[:20]):
        names = [jid_to_name.get(jid, "?") for jid in cluster[:8]]
        if len(cluster) > 8:
            names.append(f"+ {len(cluster) - 8} more")
        print(f"  Cluster {i+1} (size {len(cluster)}): {', '.join(names)}")

    # Save
    cluster_out = []
    for i, cluster in enumerate(cluster_list):
        cluster_out.append(
            {
                "cluster_id": i + 1,
                "size": len(cluster),
                "members": [{"jid": jid, "name": jid_to_name.get(jid, "?")} for jid in cluster],
                "internal_edges": sum(
                    edges.get(tuple(sorted([a, b])), 0) for a in cluster for b in cluster if a < b
                ),
            }
        )

    out = {
        "generated_at": datetime.now().isoformat(),
        "method": "greedy community detection via name cross-references",
        "merge_threshold": MERGE_THRESHOLD,
        "total_contacts": len(contacts),
        "total_edges": len(edges),
        "total_clusters": len(cluster_list),
        "singleton_clusters": sum(1 for c in cluster_list if len(c) == 1),
        "non_singleton_clusters": sum(1 for c in cluster_list if len(c) > 1),
        "largest_cluster_size": len(cluster_list[0]) if cluster_list else 0,
        "edges": [
            {
                "a": a,
                "b": b,
                "weight": w,
                "evidence": edge_evidence.get((a, b), [])[:3],
            }
            for (a, b), w in sorted_edges[:200]  # Top 200 edges
        ],
        "clusters": cluster_out[:30],  # Top 30 clusters
    }
    out_path = ANALYSIS / "clusters.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"\nWrote {out_path.relative_to(REPO)}")
    print(f"  Total clusters: {len(cluster_list)}")
    print(f"  Non-singleton: {out['non_singleton_clusters']}")
    print(f"  Largest: {out['largest_cluster_size']} contacts")


if __name__ == "__main__":
    main()

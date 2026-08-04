#!/usr/bin/env python3
"""Build (or rebuild) the SOURCE_OF_TRUTH/wa_messages/circles/ symlink view.

Walks every 1-on-1 chat in the tier* subdirs (including _dropped), assigns
it to a friend circle via group co-membership scoring, and creates a
symlink under circles/<circle>/ pointing to the canonical chat in its tier.

Run from the repo root:
    python3 scripts/build_circles.py

Idempotent: existing symlinks with correct targets are left alone; broken
or wrong-target symlinks are removed and re-created.
"""

from __future__ import annotations

import json
import os
import subprocess
from collections import defaultdict
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from triage_wa_chats import (
    ROOT,
    CIRCLE_INDICATORS,
    GROUP_SHARED_FRIEND_THRESHOLD,
    discover_chat_dirs,
    extract_group_participants,
    compute_group_co_membership,
    split_group_and_1on1,
    assign_circle,
)

CIRCLES_DIR = ROOT / "circles"
CIRCLES = list(CIRCLE_INDICATORS.keys()) + ["other_contacts"]


def rebuild() -> int:
    chat_dirs = discover_chat_dirs(ROOT)
    group_participants = extract_group_participants(chat_dirs)
    _, one_on_one = split_group_and_1on1(chat_dirs)

    # Build chat_metadata for all groups (slug -> subject) for circle assignment
    chat_metadata: dict[str, dict] = {}
    for cp in chat_dirs:
        try:
            with open(cp) as f:
                d = json.load(f)
            slug = d.get("slug")
            if slug:
                chat_metadata[slug] = {
                    "subject": d.get("subject"),
                    "is_group": bool(d.get("subject")) or d.get("jid_server") == "g.us",
                    "jid_user": d.get("jid_user"),
                }
        except Exception:
            continue

    contact_jids: set[str] = set()
    for cp in one_on_one:
        try:
            with open(cp) as f:
                d = json.load(f)
            jid = d.get("jid_user")
            if jid:
                contact_jids.add(jid)
        except Exception:
            continue
    contact_groups = compute_group_co_membership(group_participants, contact_jids)

    for c in CIRCLES:
        (CIRCLES_DIR / c).mkdir(parents=True, exist_ok=True)

    # Build expected (circle, link_name, target) tuples
    expected: list[tuple[str, str, str]] = []
    for cp in one_on_one:
        try:
            with open(cp) as f:
                d = json.load(f)
        except Exception:
            continue
        jid = d.get("jid_user")
        if not jid:
            continue
        groups_shared = contact_groups.get(jid, set())
        if len(groups_shared) < GROUP_SHARED_FRIEND_THRESHOLD:
            continue
        circle = assign_circle(groups_shared, chat_metadata)
        chat_dir = cp.parent
        tier = chat_dir.parent.name
        # symlink target (relative to circles/<circle>/)
        target = f"../../{tier}/{chat_dir.name}"
        link_name = f"{tier}__{chat_dir.name}"
        expected.append((circle, link_name, target))

    expected_set = {(c, n, t) for c, n, t in expected}

    # Walk existing links in each circle
    removed = 0
    for c in CIRCLES:
        circle_dir = CIRCLES_DIR / c
        if not circle_dir.exists():
            continue
        expected_in_circle = {(n, t) for cc, n, t in expected_set if cc == c}
        existing = [l for l in circle_dir.iterdir() if l.is_symlink()]
        for link in existing:
            current_target = os.readlink(link)
            if (link.name, current_target) in expected_in_circle:
                continue
            # Stale or wrong — remove
            subprocess.run(
                ["git", "rm", "-f", str(link)],
                cwd="/root/psycology",
                capture_output=True,
                text=True,
            )
            removed += 1

    # Create missing
    created = 0
    for circle, link_name, target in expected:
        link_path = CIRCLES_DIR / circle / link_name
        if link_path.exists() or link_path.is_symlink():
            continue
        os.symlink(target, link_path)
        subprocess.run(
            ["git", "add", str(link_path)], cwd="/root/psycology", capture_output=True, text=True
        )
        created += 1

    # Sanity check
    broken = 0
    for c in CIRCLES:
        cd = CIRCLES_DIR / c
        if not cd.exists():
            continue
        for link in cd.iterdir():
            if link.is_symlink() and not link.resolve().exists():
                broken += 1
                print(f"  BROKEN: {c}/{link.name} -> {os.readlink(link)}")

    counts: dict[str, int] = defaultdict(int)
    for c, _, _ in expected:
        counts[c] += 1
    print(f"Created: {created} new symlinks")
    print(f"Removed: {removed} stale symlinks")
    print(f"Broken after rebuild: {broken}")
    print("\nCircle distribution:")
    for c in CIRCLES:
        print(f"  {c}: {counts[c]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(rebuild())

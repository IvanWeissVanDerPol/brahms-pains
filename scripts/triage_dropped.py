#!/usr/bin/env python3
"""Triage _dropped/ chats and propose promotions.

Criteria for promotion (out of _dropped):
  - 200+ msgs OR group with 100+ msgs OR shared with 3+ named contacts
  - Skip: 1-on-1 spam chats, transactional notifications
  - Skip: chats that have already been moved (e.g. family chat was promoted)

Output:
  - JSON with triage decisions per chat
  - Renames _dropped/X → tierN/Y if promoted

USAGE:
    python3 scripts/triage_dropped.py --dry-run
    python3 scripts/triage_dropped.py --apply
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MSG_BASE = REPO / "SOURCE_OF_TRUTH" / "wa_messages"
DROP = MSG_BASE / "_dropped"
ANALYSIS = MSG_BASE / "_ANALYSIS"

# Categories
NOISE = []  # Will be marked as noise (move to _noise/)
PROMOTE_GROUPS = []  # Will go to tier4_groups/
PROMOTE_1ON1 = []  # Will go to untiered_personal/ or tier2_core/


def find_dropped_chats():
    out = []
    for d in DROP.iterdir():
        if not (d / "messages.json").exists():
            continue
        try:
            data = json.loads((d / "messages.json").read_text())
        except Exception:
            continue
        n = len(data.get("messages", []))
        jid = str(data.get("jid_user", ""))
        out.append((d, data, n, jid))
    return out


def is_group(jid: str) -> bool:
    """Heuristic: groups have JIDs with -N suffix or LID-format (120363XXX)."""
    return "-" in jid or jid.startswith("120363") or len(jid) < 12


def has_real_content(data) -> bool:
    """Check if chat has actual messages, not just system/service notifications."""
    txt_msgs = sum(1 for m in data.get("messages", []) if isinstance(m, dict) and m.get("type") == 0 and m.get("text"))
    return txt_msgs >= 5


def score_for_promotion(data, n_msgs, jid):
    """Score 0-100 — high = definitely worth promoting."""
    score = 0
    score += min(50, n_msgs // 100)  # 1 point per 100 msgs, max 50
    # Bonus for groups (high value)
    if is_group(jid):
        score += 20
    # Bonus for text content
    txt_n = sum(1 for m in data.get("messages", []) if isinstance(m, dict) and m.get("type") == 0 and m.get("text"))
    if txt_n > 50:
        score += 10
    if txt_n > 500:
        score += 10
    # Bonus for media sharing
    media_n = sum(1 for m in data.get("messages", []) if isinstance(m, dict) and m.get("type") in (1, 2, 3))
    if media_n > 20:
        score += 5
    return min(100, score)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    if not args.dry_run and not args.apply:
        args.dry_run = True

    chats = find_dropped_chats()
    print(f"Total _dropped chats: {len(chats)}")

    triage = {
        "noise": [],     # → recommend DELETE or move to _noise/
        "promote": [],   # → recommend MOVE to tier4_groups/ or other
        "keep": [],      # → leave in _dropped for now
    }

    for d, data, n, jid in chats:
        if not has_real_content(data) or n < 10:
            triage["noise"].append({"dir": str(d.relative_to(REPO)), "msgs": n, "jid": jid, "reason": "<10 msgs or no text"})
            continue
        score = score_for_promotion(data, n, jid)
        if score >= 50:
            triage["promote"].append({
                "dir": str(d.relative_to(REPO)),
                "msgs": n,
                "jid": jid,
                "score": score,
                "is_group": is_group(jid),
            })
        else:
            triage["keep"].append({
                "dir": str(d.relative_to(REPO)),
                "msgs": n,
                "jid": jid,
                "score": score,
            })

    # Print summary
    print(f"\nNoise (<10 msgs or no text): {len(triage['noise'])}")
    print(f"Promote candidates (score ≥ 50): {len(triage['promote'])}")
    print(f"Keep in _dropped (low score): {len(triage['keep'])}")

    print(f"\n=== Top 25 promote candidates ===")
    triage["promote"].sort(key=lambda x: -x["score"])
    for c in triage["promote"][:25]:
        kind = "GROUP" if c["is_group"] else "1-ON-1"
        print(f"  [{c['score']:>3}] [{kind}] {c['dir'][:55]:<55}  msgs={c['msgs']:>6}  jid={c['jid'][:14]:<14}")

    # Save triage report
    report = {
        "generated_at": str(__import__('datetime').datetime.now()),
        "total_chats": len(chats),
        "noise_count": len(triage["noise"]),
        "promote_count": len(triage["promote"]),
        "keep_count": len(triage["keep"]),
        "promote": triage["promote"],
        "noise_sample": triage["noise"][:50],
    }
    out = ANALYSIS / "DROPPED_TRIAGE.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"\nWrote {out.relative_to(REPO)}")

    if args.apply:
        print()
        print("=" * 70)
        print("APPLY MODE")
        print("=" * 70)

        # Promote to tier4_groups/ (for groups) or untiered_personal/ (for 1-on-1)
        target_base = MSG_BASE / "tier4_groups"
        target_base.mkdir(exist_ok=True)
        target_1on1 = MSG_BASE / "untiered_personal"
        target_1on1.mkdir(exist_ok=True)

        for c in triage["promote"]:
            old = REPO / c["dir"]
            base_name = Path(c["dir"]).name
            if c["is_group"]:
                new = target_base / base_name
            else:
                # Move 1-on-1 to untiered_personal/
                new = target_1on1 / base_name
            if new.exists():
                print(f"  ⚠️  target exists: {new}")
                continue
            if not old.exists():
                print(f"  ⚠️  source missing: {old}")
                continue
            subprocess.run(
                ["git", "mv", str(old.relative_to(REPO)), str(new.relative_to(REPO))],
                cwd=REPO, check=True,
            )
            print(f"  ✓ {c['dir']} → {new.relative_to(REPO)}")


if __name__ == "__main__":
    main()
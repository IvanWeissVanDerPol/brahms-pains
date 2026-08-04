"""
Deduplicate tier1_deep/tier2_core/tier3_extended/untiered_personal dirs.

Two prior runs of _reorganize.py against DIFFERENT snapshots of
_final_classification.json left byte-identical duplicate dirs at different
NN__ ranks (and often at different tiers). The `if dest.exists(): skip` guard
in _reorganize.py can't catch these because the destination names differ.

This script uses the CURRENT _final_classification.json as the source of truth:
- For each on-disk NN__name__slug folder, parse (physical_tier, rank, slug).
- Compare against expected (tier, rank) from _final_classification.json.
- If the folder's location + rank match expected → KEEP.
- Otherwise → move to _dropped/reorg_stale/ (reversible).

Run:  python3 _dedup_by_rank.py            # dry run
      python3 _dedup_by_rank.py --yes      # execute
"""

import json
import re
import sys
import shutil
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).parent
DROPPED = BASE / "_dropped" / "reorg_stale"
FINAL = json.loads((BASE / "_final_classification.json").read_text())

TIER_DIRS = ["tier1_deep", "tier2_core", "tier3_extended", "untiered_personal"]
SLUG_RE = re.compile(r"(_wa_(?:chat|group|lid|other|other_newsletter)_.+)$")
RANK_RE = re.compile(r"^(\d+)__")

# Build expected (tier, rank) for every slug in the current classification.
expected = {}  # slug -> (tier_name, rank)
for i, s in enumerate(FINAL["tiers"]["tier1_deep"], 1):
    expected[s] = ("tier1_deep", i)
for i, s in enumerate(FINAL["tiers"]["tier2_core"], 11):
    expected[s] = ("tier2_core", i)
for i, s in enumerate(FINAL["tiers"]["tier3_extended"], 41):
    expected[s] = ("tier3_extended", i)
# untiered_personal has no explicit rank list; ranks assigned at reorganize
# time as counter starting at 101. Don't dedup untiered by rank.


def parse_folder(name: str):
    slug_m = SLUG_RE.search(name)
    rank_m = RANK_RE.match(name)
    return (
        slug_m.group(1) if slug_m else None,
        int(rank_m.group(1)) if rank_m else None,
    )


# ---- Walk disk, classify each folder ----
keep: list[tuple[str, Path]] = []  # (reason, path)
move: list[tuple[str, Path]] = []  # (reason, path)
by_slug_seen: dict[str, list[Path]] = defaultdict(list)

for tier_name in TIER_DIRS:
    tdir = BASE / tier_name
    if not tdir.is_dir():
        continue
    for d in sorted(tdir.iterdir()):
        if not d.is_dir():
            continue
        slug, rank = parse_folder(d.name)
        if slug is None:
            keep.append(("no-slug (orphan, left alone)", d))
            continue
        by_slug_seen[slug].append(d)

        if tier_name == "untiered_personal":
            keep.append(("untiered (rank not verified)", d))
            continue

        exp = expected.get(slug)
        if exp is None:
            move.append((f"slug not in current classification (was in {tier_name})", d))
            continue
        exp_tier, exp_rank = exp
        if tier_name != exp_tier:
            move.append((f"wrong tier: on-disk={tier_name} expected={exp_tier} rank={exp_rank}", d))
            continue
        if rank != exp_rank:
            move.append((f"wrong rank: on-disk={rank} expected={exp_rank}", d))
            continue
        keep.append((f"correct: {tier_name} rank={exp_rank}", d))

# ---- Sanity: warn on any slug where zero keeps survived a duplicate cluster ----
warnings = []
for slug, paths in by_slug_seen.items():
    kept_paths = [p for reason, p in keep if p in paths]
    if len(paths) > 1 and not kept_paths:
        warnings.append(
            f"WARNING: slug {slug} has {len(paths)} dirs but NONE match current classification"
        )

# ---- Report ----
print(f"KEEP: {len(keep)}")
print(f"MOVE (to {DROPPED.relative_to(BASE)}/): {len(move)}")
for reason, p in move[:12]:
    print(f"  {p.relative_to(BASE)}   [{reason}]")
if len(move) > 12:
    print(f"  ... and {len(move)-12} more")

if warnings:
    print()
    for w in warnings:
        print(w)

# ---- Report slugs in classification that have NO surviving on-disk match ----
missing = []
for slug, (exp_tier, exp_rank) in expected.items():
    kept_here = [
        p
        for reason, p in keep
        if p.parent.name == exp_tier and parse_folder(p.name) == (slug, exp_rank)
    ]
    if not kept_here:
        missing.append((exp_tier, exp_rank, slug))
if missing:
    print()
    print(f"MISSING (in classification but no correctly-placed dir on disk): {len(missing)}")
    for t, r, s in missing[:20]:
        # is it present under another name/rank?
        seen = by_slug_seen.get(s, [])
        if seen:
            names = ", ".join(str(p.relative_to(BASE)) for p in seen)
            print(f"  {t} rank={r} slug={s}  -- but slug found as: {names}")
        else:
            print(f"  {t} rank={r} slug={s}  -- NOT ON DISK AT ALL")
    if len(missing) > 20:
        print(f"  ... and {len(missing)-20} more")

# ---- Execute ----
if "--yes" not in sys.argv:
    print("\nDry-run. Pass --yes to actually move.")
    sys.exit(0)

DROPPED.mkdir(parents=True, exist_ok=True)
manifest = {"moves": []}
moved = 0
skipped = 0
for reason, p in move:
    dst = DROPPED / p.name
    if dst.exists():
        print(f"skip (dest exists): {p.relative_to(BASE)}")
        skipped += 1
        continue
    shutil.move(str(p), str(dst))
    manifest["moves"].append(
        {
            "from": str(p.relative_to(BASE)),
            "to": str(dst.relative_to(BASE)),
            "reason": reason,
        }
    )
    moved += 1

(BASE / "_dedup_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
print(f"\nMoved {moved}, skipped {skipped}.  Manifest -> _dedup_manifest.json")

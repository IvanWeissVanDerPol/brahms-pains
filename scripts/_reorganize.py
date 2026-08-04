"""
Rename and re-nest each kept chat dir so the layout is human-readable:

  tier1_deep/            01__<name>__<slug>/     (top 10 personal 1:1 by score)
  tier2_core/            11__<name>__<slug>/     (ranks 11-40)
  tier3_extended/        41__<name>__<slug>/     (ranks 41-100)
  untiered_personal/     <name>__<slug>/         (personal, rank 101+)
  tier4_groups/active/   <name>__<slug>/         (kept group_active)
  tier4_groups/lurker/   <name>__<slug>/         (kept group_lurker_context)
  other_lid/             <name>__<slug>/         (lid chats not in tiers)
  _dropped/              (already populated; left alone)

Names come from:
  1. messages.json['subject']       -> groups (12/12 populated)
  2. waid_to_name.json              -> 6 personal 1:1 contacts (VCF-harvested)
  3. phone-suffix fallback (p<last4>) for everything else

Non-destructive: shutil.move only; nothing deleted. Reversible via _rename_manifest.json.

Run:
  python3 _reorganize.py            # dry run
  python3 _reorganize.py --yes      # execute
"""

import json
import sys
import re
import shutil
from pathlib import Path
from collections import Counter

BASE = Path(__file__).parent
FINAL = json.loads((BASE / "_final_classification.json").read_text())

WAID_MAP_PATH = Path(
    "/tmp/claude-1000/-home-ai-whisperers-paragu-ai-platform/3f2e0128-0eb5-4bd7-a38f-e6bee3d06e27/scratchpad/waid_to_name.json"
)
WAID_MAP = json.loads(WAID_MAP_PATH.read_text()) if WAID_MAP_PATH.exists() else {}

TIER_DIRS = {
    "tier1_deep": "tier1_deep",
    "tier2_core": "tier2_core",
    "tier3_extended": "tier3_extended",
    "untiered_personal": "untiered_personal",
    "tier4_active": "tier4_groups/active",
    "tier4_lurker": "tier4_groups/lurker",
    "other_lid": "other_lid",
}

TIER_START_RANK = {
    "tier1_deep": 1,
    "tier2_core": 11,
    "tier3_extended": 41,
}


def slugify(text: str) -> str:
    if not text:
        return "unknown"
    s = text.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s[:60] or "unknown"


def load_meta(dir_path: Path) -> dict:
    mj = dir_path / "messages.json"
    if not mj.exists():
        return {}
    try:
        d = json.loads(mj.read_text())
    except Exception:
        return {}
    return {
        "subject": d.get("subject"),
        "jid_user": d.get("jid_user"),
        "jid_server": d.get("jid_server"),
    }


def resolve_name(meta: dict) -> str:
    subject = meta.get("subject")
    jid_user = meta.get("jid_user") or ""
    server = meta.get("jid_server") or ""

    if subject and subject.strip():
        return slugify(subject)

    if jid_user in WAID_MAP:
        return slugify(WAID_MAP[jid_user])

    if server == "lid":
        return f"lid_{jid_user[-6:]}" if jid_user else "lid_unknown"
    if jid_user.isdigit() and len(jid_user) >= 4:
        return f"p{jid_user[-4:]}"
    if jid_user:
        return slugify(jid_user)

    return "unknown"


def plan() -> list[dict]:
    keep_set = set(FINAL["keep_slugs"])
    all_dirs = [p for p in BASE.iterdir() if p.is_dir() and p.name.startswith("_wa_")]
    plan_rows = []

    tier1 = FINAL["tiers"]["tier1_deep"]
    tier2 = FINAL["tiers"]["tier2_core"]
    tier3 = FINAL["tiers"]["tier3_extended"]

    tier1_set = set(tier1)
    tier2_set = set(tier2)
    tier3_set = set(tier3)

    rank_by_slug = {}
    for i, s in enumerate(tier1, 1):
        rank_by_slug[s] = i
    for i, s in enumerate(tier2, 11):
        rank_by_slug[s] = i
    for i, s in enumerate(tier3, 41):
        rank_by_slug[s] = i

    triage = json.loads((BASE / "_triage.json").read_text())
    cat_by_slug = {c["slug"]: c["category"] for c in triage["chats"]}

    untiered_counter = 100
    for d in sorted(all_dirs, key=lambda p: p.name):
        slug = d.name
        if slug not in keep_set:
            continue

        meta = load_meta(d)
        name = resolve_name(meta)
        cat = cat_by_slug.get(slug, "")

        if slug in tier1_set:
            bucket_key = "tier1_deep"
            rank = rank_by_slug[slug]
            new_name = f"{rank:02d}__{name}__{slug}"
        elif slug in tier2_set:
            bucket_key = "tier2_core"
            rank = rank_by_slug[slug]
            new_name = f"{rank:02d}__{name}__{slug}"
        elif slug in tier3_set:
            bucket_key = "tier3_extended"
            rank = rank_by_slug[slug]
            new_name = f"{rank:03d}__{name}__{slug}"
        elif slug.startswith("_wa_group_"):
            bucket_key = "tier4_active" if cat == "group_active" else "tier4_lurker"
            new_name = f"{name}__{slug}"
        elif slug.startswith("_wa_lid_"):
            bucket_key = "other_lid"
            new_name = f"{name}__{slug}"
        else:
            bucket_key = "untiered_personal"
            untiered_counter += 1
            new_name = f"{untiered_counter:03d}__{name}__{slug}"

        dest_dir = BASE / TIER_DIRS[bucket_key]
        plan_rows.append(
            {
                "slug": slug,
                "src": str(d.relative_to(BASE)),
                "dest_dir": str(dest_dir.relative_to(BASE)),
                "new_name": new_name,
                "dest": str((dest_dir / new_name).relative_to(BASE)),
                "bucket": bucket_key,
                "name_source": (
                    "subject"
                    if meta.get("subject")
                    else "vcf" if meta.get("jid_user") in WAID_MAP else "phone_suffix"
                ),
            }
        )
    return plan_rows


def main():
    rows = plan()
    dry = "--yes" not in sys.argv

    by_bucket = Counter(r["bucket"] for r in rows)
    by_source = Counter(r["name_source"] for r in rows)

    print(f"Planned moves: {len(rows)}")
    print(f"By bucket : {dict(by_bucket)}")
    print(f"By source : {dict(by_source)}")

    dup_check = Counter(r["dest"] for r in rows)
    collisions = [d for d, n in dup_check.items() if n > 1]
    if collisions:
        print(f"ERROR: {len(collisions)} dest-path collisions")
        for c in collisions[:5]:
            print(f"  {c}")
        sys.exit(2)

    for r in rows[:8]:
        print(f"  {r['src']}  ->  {r['dest']}   [{r['name_source']}]")
    if len(rows) > 8:
        print(f"  ... and {len(rows)-8} more")

    if dry:
        print("\nDry-run. Pass --yes to actually move.")
        return

    manifest = {"moves": []}
    moved = 0
    skipped = 0
    for r in rows:
        src = BASE / r["src"]
        dest_dir = BASE / r["dest_dir"]
        dest = BASE / r["dest"]
        dest_dir.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            print(f"skip (dest exists): {r['dest']}")
            skipped += 1
            continue
        if not src.exists():
            print(f"skip (src missing): {r['src']}")
            skipped += 1
            continue
        shutil.move(str(src), str(dest))
        manifest["moves"].append({"from": r["src"], "to": r["dest"], "slug": r["slug"]})
        moved += 1

    (BASE / "_rename_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"\nMoved {moved} dirs, skipped {skipped}. Manifest -> _rename_manifest.json")


if __name__ == "__main__":
    main()

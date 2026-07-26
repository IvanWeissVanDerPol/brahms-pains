#!/usr/bin/env python3
"""Final VNT rename: use wa_messages dir prefix."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VNT = REPO / "SOURCE_OF_TRUTH" / "voice_note_transcripts"
WA = REPO / "SOURCE_OF_TRUTH" / "wa_messages"


def safe_name(name: str) -> str:
    if not name: return ""
    s = re.sub(r'[^\w\s-]', '', name).strip()
    s = re.sub(r'\s+', '_', s)
    return s


def is_clean(name: str) -> bool:
    if not name or len(name) < 3: return False
    if "=" in name: return False
    if re.match(r'^[0-9A-F=]+$', name.replace("_", "")): return False
    if re.search(r'_[A-Z]_[A-Z]?_?$', name):
        return False
    return True


def main():
    vcard = json.loads((REPO / "SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/viewer_full_data.json").read_text())
    jid_to_name = {c["jid"]: c["name"] for c in vcard["vcard_contacts"] if c.get("jid") and c.get("name")}

    # Get all numbered VNT
    numbered = []
    for d in VNT.iterdir():
        if not d.is_dir(): continue
        if d.name.startswith("_"): continue
        m = re.match(r'^(chat|lid|group)_(\d{10,15})_\d+', d.name)
        if m:
            numbered.append((d.name, m.group(2)))

    renamed = 0
    skipped = 0
    for folder, jid in numbered:
        # Skip if vCard target exists
        if jid in jid_to_name:
            target_safe = safe_name(jid_to_name[jid])
            if (VNT / target_safe).exists():
                skipped += 1
                continue

        # Find wa_messages dir
        wa_dir = None
        for tier in ["tier1_deep", "tier2_core", "tier3_extended", "tier4_groups", "untiered_personal", "other_lid", "_dropped", "_conversations"]:
            tier_dir = WA / tier
            if not tier_dir.exists(): continue
            for d in tier_dir.iterdir():
                if d.is_dir() and jid in d.name:
                    wa_dir = d
                    break
            if wa_dir: break

        if not wa_dir:
            skipped += 1
            continue

        # Extract canonical from prefix
        m = re.match(r'^([a-z_0-9]+(?:_[a-z_0-9]+)*)___wa_', wa_dir.name)
        if not m:
            skipped += 1
            continue
        slug = m.group(1)

        # Skip noise
        bad_slugs = ["p_dropped", "untiered_personal"]
        if any(slug.startswith(b) for b in bad_slugs) or slug.startswith(("wa_", "chat_", "lid_", "group_")) or slug.isdigit():
            skipped += 1
            continue

        # Strip numeric prefix like "30__"
        slug = re.sub(r'^\d+__', '', slug)
        if not slug or slug.isdigit():
            skipped += 1
            continue

        # Convert to title
        title = slug.replace("_", " ").title().replace(" ", "_")
        if not is_clean(title):
            skipped += 1
            continue

        target = VNT / title
        if target.exists() and target != VNT / folder:
            skipped += 1
            continue

        vnt_dir = VNT / folder
        if not vnt_dir.exists():
            continue

        if target.exists():
            # Merge
            tf_src = vnt_dir / "transcripts.json"
            tf_tgt = target / "transcripts.json"
            if tf_src.exists() and tf_tgt.exists():
                src = json.loads(tf_src.read_text())
                tgt = json.loads(tf_tgt.read_text())
                if isinstance(src, list) and isinstance(tgt, list):
                    existing = {e.get("file") for e in tgt if isinstance(e, dict)}
                    added = 0
                    for e in src:
                        if isinstance(e, dict) and e.get("file") not in existing:
                            tgt.append(e)
                            added += 1
                    if added > 0:
                        tf_tgt.write_text(json.dumps(tgt, indent=1, ensure_ascii=False))
                        print(f"  MERGED: {folder} -> {title} (+{added})")
            shutil.rmtree(vnt_dir)
        else:
            shutil.move(str(vnt_dir), str(target))
            print(f"  RENAMED: {folder} -> {title}")
        renamed += 1

    print(f"\n=== Summary ===")
    print(f"  Renamed: {renamed}")
    print(f"  Skipped: {skipped}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Final VNT rename - handle hyphens and group_NAME_NNN pattern."""
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


def main():
    vcard = json.loads((REPO / "SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/viewer_full_data.json").read_text())
    jid_to_name = {c["jid"]: c["name"] for c in vcard["vcard_contacts"] if c.get("jid") and c.get("name")}

    # Get wa_messages JID -> canonical mapping
    jid_to_canonical = {}
    for tier in ["tier1_deep", "tier2_core", "tier3_extended", "tier4_groups", "untiered_personal", "other_lid", "_dropped", "_conversations"]:
        tier_dir = WA / tier
        if not tier_dir.exists(): continue
        for d in tier_dir.iterdir():
            if not d.is_dir(): continue
            m = re.search(r'(\d{10,15})', d.name)
            if not m: continue
            jid = m.group(1)
            if jid in jid_to_canonical: continue
            # Try prefix
            m2 = re.match(r'^([a-z_0-9]+(?:_[a-z_0-9]+)*)___wa_', d.name)
            if m2:
                slug = m2.group(1)
                if not re.match(r'^(p_dropped|untiered_personal|wa_|chat_|lid_|group_)', slug) and not slug.isdigit():
                    jid_to_canonical[jid] = slug

    renamed = 0
    merged = 0
    deleted = 0
    skipped = 0

    for d in sorted(VNT.iterdir()):
        if not d.is_dir(): continue
        if d.name.startswith("_"): continue
        if not re.match(r'^(chat|lid|group)_', d.name): continue

        target_name = None

        # Try pattern 1: chat_NNNNNN_NNN with vCard/wa_messages lookup
        m = re.match(r'^(chat|lid)_(\d{10,15})_\d+$', d.name)
        if m:
            jid = m.group(2)
            if jid in jid_to_name:
                target_name = safe_name(jid_to_name[jid])
            elif jid in jid_to_canonical:
                slug = jid_to_canonical[jid]
                target_name = safe_name(slug.replace("_", " ").title())
            if target_name and len(target_name) < 3:
                target_name = None

        # Try pattern 2: group_NAME_NNN
        if not target_name:
            m = re.match(r'^group_([a-záéíóúñ_-]+)_(\d+)$', d.name)
            if m:
                name_slug = m.group(1)
                # Title case
                title = name_slug.replace("_", " ").title().replace(" ", "_")
                target_name = f"Group_{title}"

        # Try pattern 3: chat_NAME_JIDIDX (rare)
        if not target_name:
            m = re.match(r'^(chat|lid)_([a-z_]+)_(\d{10,15})_(\d+)$', d.name)
            if m:
                name_slug = m.group(2)
                if name_slug not in ("p_dropped",):
                    target_name = safe_name(name_slug.replace("_", " ").title())

        if not target_name:
            skipped += 1
            continue

        target = VNT / target_name
        if not target.exists():
            # Just rename
            shutil.move(str(d), str(target))
            print(f"  RENAMED: {d.name} -> {target_name}")
            renamed += 1
            continue

        # Merge
        src_tf = d / "transcripts.json"
        dst_tf = target / "transcripts.json"
        if src_tf.exists() and dst_tf.exists():
            try:
                src_data = json.loads(src_tf.read_text())
                dst_data = json.loads(dst_tf.read_text())
                if isinstance(src_data, list) and isinstance(dst_data, list):
                    existing = {e.get("file") for e in dst_data if isinstance(e, dict)}
                    added = 0
                    for e in src_data:
                        if isinstance(e, dict) and e.get("file") not in existing:
                            dst_data.append(e)
                            added += 1
                    if added > 0:
                        dst_tf.write_text(json.dumps(dst_data, indent=1, ensure_ascii=False))
                        print(f"  MERGED: {d.name} -> {target_name} (+{added})")
                        merged += 1
                    else:
                        deleted += 1
            except: pass
        else:
            for f in d.iterdir():
                if f.name == "transcripts.json": continue
                dest = target / f.name
                if not dest.exists():
                    shutil.move(str(f), str(dest))
                else:
                    f.unlink()
            print(f"  MERGED (no tf): {d.name} -> {target_name}")
            merged += 1

        # Remove src
        try:
            shutil.rmtree(d)
        except: pass

    print(f"\n=== Summary ===")
    print(f"  Renamed: {renamed}")
    print(f"  Merged: {merged}")
    print(f"  Deleted (dup): {deleted}")
    print(f"  Skipped: {skipped}")


if __name__ == "__main__":
    main()

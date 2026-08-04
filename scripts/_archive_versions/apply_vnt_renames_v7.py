#!/usr/bin/env python3
"""Final aggressive name detector for VNT - use English/self-intro patterns."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VNT = REPO / "SOURCE_OF_TRUTH" / "voice_note_transcripts"
WA = REPO / "SOURCE_OF_TRUTH" / "wa_messages"


def safe_name(name: str) -> str:
    if not name:
        return ""
    s = re.sub(r"[^\w\s-]", "", name).strip()
    s = re.sub(r"\s+", "_", s)
    return s


def is_clean(name: str) -> bool:
    if not name or len(name) < 3 or len(name) > 25:
        return False
    if "=" in name:
        return False
    if re.match(r"^[0-9A-F=]+$", name.replace("_", "")):
        return False
    if re.search(r"_[A-Z]_[A-Z]?_?$", name):
        return False
    return True


def find_name_in_text(text: str) -> str | None:
    """Look for self-intro in English or Spanish."""
    if not text:
        return None
    text_low = text.lower()

    # English patterns
    patterns_en = [
        r"\bthis is ([a-záéíóúñ ]{2,20})(?:\s+the|\s*,|\s*\.|\s*$)",
        r"\bhi[!,.]? i\'?m ([a-záéíóúñ ]{2,20})(?:\s|,|\.|$)",
        r"\bim ([a-záéíóúñ]{2,20})(?:\s|,|\.|$)",
        r"\bmy name is ([a-záéíóúñ ]{2,20})(?:\s|,|\.|$)",
        r"\bcall me ([a-záéíóúñ]{2,20})(?:\s|,|\.|$)",
        r"\bi\'?m ([a-záéíóúñ]{2,20})(?:\s|,|\.|$)",
    ]
    # Spanish patterns
    patterns_es = [
        r"\bsoy ([a-záéíóúñ]{2,20})(?:\s|,|\.|$)",
        r"\bme llamo ([a-záéíóúñ]{2,20})(?:\s|,|\.|$)",
        r"\baquí\s+([a-záéíóúñ]{2,20})(?:\s|,|\.|$)",
        r"\bte saluda ([a-záéíóúñ]{2,20})(?:\s|,|\.|$)",
    ]

    for pattern in patterns_en + patterns_es:
        m = re.search(pattern, text_low)
        if m:
            name = m.group(1).strip()
            # Clean
            if name in (
                "hola",
                "bien",
                "mama",
                "aqui",
                "casa",
                "novia",
                "amor",
                "mismo",
                "ivan",
                "kiki",
                "the",
                "uwu",
                "uwuw",
            ):
                continue
            return name.title()
    return None


def main():
    # Get remaining numbered
    numbered = []
    for d in VNT.iterdir():
        if not d.is_dir():
            continue
        if d.name.startswith("_"):
            continue
        if re.match(r"^(chat|lid|group)_", d.name):
            numbered.append(d)

    print(f"=== Processing {len(numbered)} numbered VNT ===\n")
    renamed = 0
    skipped = 0
    for d in numbered:
        # Get JID
        m = re.search(r"(\d{10,15})", d.name)
        jid = m.group(1) if m else None
        if not jid:
            continue

        # Find wa_messages dir
        wa_dir = None
        for tier in [
            "tier1_deep",
            "tier2_core",
            "tier3_extended",
            "tier4_groups",
            "untiered_personal",
            "other_lid",
            "_dropped",
            "_conversations",
        ]:
            for d2 in (WA / tier).iterdir():
                if d2.is_dir() and jid in d2.name:
                    wa_dir = d2
                    break
            if wa_dir:
                break

        if not wa_dir:
            skipped += 1
            continue

        # Read messages
        mf = wa_dir / "messages.json"
        if not mf.exists():
            skipped += 1
            continue
        try:
            data = json.loads(mf.read_text())
        except:
            skipped += 1
            continue
        msgs = data.get("messages", [])

        # Find self-intro
        canonical = None
        for m in msgs[:30]:
            if not isinstance(m, dict):
                continue
            t = m.get("text", "")
            if not t:
                continue
            name = find_name_in_text(t)
            if name and is_clean(name):
                canonical = name
                break

        if not canonical:
            skipped += 1
            continue

        # Rename
        target = VNT / canonical
        if target.exists() and target != d:
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
                            print(f"  MERGED: {d.name} -> {canonical} (+{added})")
                        else:
                            print(f"  DELETE: {d.name} (dup of {canonical})")
                except:
                    pass
            for f in d.iterdir():
                if f.name == "transcripts.json":
                    continue
                dest = target / f.name
                if not dest.exists():
                    shutil.move(str(f), str(dest))
            try:
                shutil.rmtree(d)
            except:
                pass
        else:
            shutil.move(str(d), str(target))
            print(f"  RENAMED: {d.name} -> {canonical}")
        renamed += 1

    print("\n=== Summary ===")
    print(f"  Renamed/Merged: {renamed}")
    print(f"  Skipped: {skipped}")


if __name__ == "__main__":
    main()

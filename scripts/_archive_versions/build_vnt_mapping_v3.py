#!/usr/bin/env python3
"""Better VNT folder renames using transcript content."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VNT = REPO / "SOURCE_OF_TRUTH" / "voice_note_transcripts"
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages/_ANALYSIS"
WA_MESSAGES = REPO / "SOURCE_OF_TRUTH" / "wa_messages"


def safe_name(name: str) -> str:
    if not name:
        return ""
    s = re.sub(r"[^\w\s-]", "", name).strip()
    s = re.sub(r"\s+", "_", s)
    return s


def is_clean(name: str) -> bool:
    if not name or len(name) < 4:
        return False
    if re.match(r"^[0-9A-F=]+$", name.replace("_", "")):
        return False
    if "=" in name:
        return False
    if re.search(r"_[A-Z]_[A-Z]?_?$", name):
        return False
    return True


def get_name_from_transcripts(chat_dir: Path) -> str | None:
    """Try to find a name from transcript content."""
    transcripts = chat_dir / "transcripts.json"
    if not transcripts.exists():
        return None
    try:
        data = json.loads(transcripts.read_text())
    except:
        return None
    if not isinstance(data, list):
        return None

    # Look for the most common non-empty text
    texts = [e.get("text", "") for e in data if isinstance(e, dict) and e.get("text")]
    if not texts:
        return None

    # Look for "soy X" or "me llamo X" or "yo soy X" patterns
    for text in texts[:30]:
        text_low = text.lower()
        m = re.search(r"(?:soy|me llamo|yo soy|mi nombre es) ([a-záéíóúñ ]{2,30})", text_low)
        if m:
            name = m.group(1).strip().title()
            if is_clean(name):
                return name

    return None


def get_name_from_chat_dirname(chat_dir_name: str) -> str | None:
    """Extract name from chat dir if it has a prefix."""
    m = re.match(r"^([a-z_]+(?:_[a-z_]+)*)____wa_(?:chat|lid|group)_", chat_dir_name)
    if m:
        name_slug = m.group(1).replace("_", " ").title()
        if is_clean(name_slug):
            return name_slug
    return None


def get_name_from_messages(chat_dir: Path) -> str | None:
    """Look in messages.json for self-intro."""
    mf = chat_dir / "messages.json"
    if not mf.exists():
        return None
    try:
        data = json.loads(mf.read_text())
    except:
        return None
    for m in data.get("messages", [])[:30]:
        if isinstance(m, dict) and m.get("text"):
            text = m["text"].lower()
            # Try multiple patterns
            for pattern in [
                r"(?:soy|me llamo|yo soy|mi nombre es) ([a-záéíóúñ ]{2,30})",
                r"^(?:hola|holis|hola!),? (?:soy|me llamo) ([a-záéíóúñ ]{2,30})",
            ]:
                m2 = re.search(pattern, text)
                if m2:
                    name = m2.group(1).strip().title()
                    if is_clean(name):
                        return name
    return None


def main():
    # Load vCard names
    vcard = json.loads((ANALYSIS / "viewer_full_data.json").read_text())
    jid_to_name = {c["jid"]: c["name"] for c in vcard["vcard_contacts"]}

    # Build JID -> wa_messages dir mapping
    jid_to_wm_dir = {}
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
        tier_dir = WA_MESSAGES / tier
        if not tier_dir.exists():
            continue
        for d in tier_dir.iterdir():
            if not d.is_dir():
                continue
            m = re.search(r"(\d{10,15})", d.name)
            if m and m.group(1) not in jid_to_wm_dir:
                jid_to_wm_dir[m.group(1)] = d

    # Walk VNT folders
    renames = []
    skipped = []
    for d in sorted(VNT.iterdir()):
        if not d.is_dir():
            continue
        if d.name.startswith("_"):
            continue
        if d.name in [
            "Laura",
            "Ara_Nunez_Poli",
            "Cookie",
            "Defi",
            "Jonatan_Verdun",
            "Lourdes_Youko_Kurama",
            "Magali_Carreras",
        ]:
            continue

        m = re.match(r"^(chat|lid|group)_(\d{10,15})_\d+", d.name)
        if not m:
            continue

        jid = m.group(2)
        canonical = None
        source = None

        # Priority order:
        # 1. vCard
        if jid in jid_to_name:
            canonical = jid_to_name[jid]
            source = "vcard"

        # 2. Chat dir prefix
        if not canonical:
            wm_dir = jid_to_wm_dir.get(jid)
            if wm_dir:
                canonical = get_name_from_chat_dirname(wm_dir.name)
                if canonical:
                    source = "wm_dir_prefix"

        # 3. messages.json self-intro
        wm_dir = jid_to_wm_dir.get(jid)
        if not canonical and wm_dir:
            canonical = get_name_from_messages(wm_dir)
            if canonical:
                source = "messages_intro"

        # 4. Transcript content self-intro
        if not canonical:
            canonical = get_name_from_transcripts(d)
            if canonical:
                source = "transcript_intro"

        if canonical:
            safe = safe_name(canonical)
            if is_clean(safe) and safe != d.name:
                renames.append((d.name, safe, jid, source, canonical))
            else:
                skipped.append((d.name, safe, jid, source, "not_clean_or_same"))
        else:
            skipped.append((d.name, "?", jid, "none", "?"))

    print(f"=== Proposed renames: {len(renames)} ===")
    for old, new, jid, src, canon in renames[:40]:
        print(f"  {old:<40} -> {new:<35} [{src}]")
    if len(renames) > 40:
        print(f"  ... and {len(renames) - 40} more")

    print(f"\n=== Skipped: {len(skipped)} ===")
    for old, new, jid, src, reason in skipped[:15]:
        print(f"  {old:<40} -> {new:<30} [{src}, {reason}]")

    # Save mapping
    out = {
        "generated_at": "2026-07-25",
        "method": "vcard > wm_dir_prefix > messages_intro > transcript_intro",
        "renames": [
            {"folder": o, "safe_name": n, "jid": j, "source": s, "canonical": c}
            for o, n, j, s, c in renames
        ],
        "skipped": [
            {"folder": o, "safe_name": n, "jid": j, "source": s, "reason": r}
            for o, n, j, s, r in skipped
        ],
    }
    out_path = VNT / "_mapping_v2.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\nWrote {out_path.relative_to(REPO)}")
    print(f"Total to rename: {len(renames)}")


if __name__ == "__main__":
    main()

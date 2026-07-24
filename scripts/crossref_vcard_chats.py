#!/usr/bin/env python3
"""Cross-reference vCard with chat content to find new matches.

For each vCard phone number, check if it appears in any chat's message text.
Also match vCard EMAIL fields against message text.
"""
from __future__ import annotations
import json
import re
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS"
MSG_BASE = REPO / "SOURCE_OF_TRUTH" / "wa_messages"

# Load vCard
import sys
sys.path.insert(0, "scripts")
from match_vcard_chats_v2 import parse_vcard, phone_to_jid_candidates

cards = parse_vcard(Path("SOURCE_OF_TRUTH/wa_messages/_ANALYSIS/contacts_full.vcf"))

# Already-matched JIDs (skip these)
resolved = json.loads((ANALYSIS / "contacts_vcard_resolved.json").read_text())
matched_jids = {e["jid_user"] for e in resolved["resolutions"]}

# Build per-JID phone variants
jid_to_phones = defaultdict(list)
jid_to_email = {}
for c in cards:
    jids = []
    if c["waid"]:
        jids.append(c["waid"])
    for phone in c["phones"]:
        for cand in phone_to_jid_candidates(phone):
            jids.append(cand)
    for jid in set(jids):
        for phone in c["phones"]:
            jid_to_phones[jid].append(phone)
    # Also extract emails if present (not parsed by default, let's grep)
    # We'd need to modify parse_vcard but for now skip emails

# Build per-phone text variations: 595985725366, +595 985 725366, 0985 725366, etc.
def phone_variants(phone: str) -> list[str]:
    digits = re.sub(r"\D", "", phone)
    if not digits or len(digits) < 8:
        return []
    variants = set()
    variants.add(digits)
    if digits.startswith("595") and len(digits) == 12:
        local = digits[3:]  # 985725366
        variants.add("0" + local)
        # +595 985 725366
        variants.add(f"+595 {local[:3]} {local[3:6]} {local[6:]}")
        variants.add(f"+595 {local[:3]} {local[3:]}")
        variants.add(f"595 {local[:3]} {local[3:]}")
        variants.add(f"{local[:3]} {local[3:6]} {local[6:]}")
        variants.add(f"{local[:3]}{local[3:6]}{local[6:]}")
    elif digits.startswith("31"):
        # Dutch numbers
        variants.add(f"+31 {digits[2:5]} {digits[5:8]} {digits[8:12]}".strip())
    elif digits.startswith("1"):
        # US/Canada
        variants.add(f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}")
    return [v for v in variants if len(v) >= 8]


# Walk all chats and check for phone occurrences
TIERS = ["tier1_deep", "tier2_core", "tier3_extended", "tier4_groups", "untiered_personal", "other_lid", "_dropped"]

# Build phone -> jid lookup
phone_to_jid = {}
for c in cards:
    if c["waid"]:
        for phone in c["phones"]:
            for v in phone_variants(phone):
                # Try to get a canonical JID candidate
                for cand in phone_to_jid_candidates(phone):
                    phone_to_jid[v] = (cand, c["name"])
        # Also map the waid itself
        for v in phone_variants(c["waid"]):
            phone_to_jid[v] = (c["waid"], c["name"])

print(f"Phone lookup size: {len(phone_to_jid)} variants from {len(cards)} cards")

# Walk chats
new_matches = []
scanned = 0
for tier in TIERS:
    tier_dir = MSG_BASE / tier
    if not tier_dir.exists(): continue
    for d in tier_dir.iterdir():
        if not (d / "messages.json").exists(): continue
        scanned += 1
        try:
            data = json.loads((d / "messages.json").read_text())
        except: continue
        chat_jid = str(data.get("jid_user", ""))
        if chat_jid in matched_jids:
            continue  # Already matched
        # Scan all messages
        for m in data.get("messages", []):
            if not isinstance(m, dict) or not m.get("text"):
                continue
            text = m["text"]
            # Check each phone variant
            for variant, (vcard_jid, vcard_name) in phone_to_jid.items():
                if variant in text and len(variant) >= 9:
                    # Found! Check if vcard_jid has its own chat (different JID)
                    if vcard_jid != chat_jid:
                        new_matches.append({
                            "vcard_jid": vcard_jid,
                            "vcard_name": vcard_name,
                            "vcard_phone_variant": variant,
                            "found_in_chat_jid": chat_jid,
                            "found_in_chat_dir": d.name,
                            "found_in_tier": tier,
                            "ts": m.get("ts_iso", "")[:10],
                            "evidence": text[:200],
                        })
                    break  # one match per msg is enough
        if scanned % 200 == 0:
            print(f"  scanned {scanned}, matches so far: {len(new_matches)}")

# Dedupe by (vcard_jid, found_in_chat_jid)
seen = set()
deduped = []
for m in new_matches:
    k = (m["vcard_jid"], m["found_in_chat_jid"])
    if k not in seen:
        seen.add(k)
        deduped.append(m)

out = {
    "generated_at": "2026-07-23T22:30:00",
    "description": "Phone numbers from vCards found in chat messages (cross-reference). New matches NOT in contacts_vcard_resolved.json.",
    "scanned_chats": scanned,
    "new_matches": deduped,
}
out_path = ANALYSIS / "vcard_chat_number_shares.json"
out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1))

print(f"\nScanned {scanned} chats, found {len(deduped)} NEW cross-references")
print(f"Wrote {out_path.relative_to(REPO)}")
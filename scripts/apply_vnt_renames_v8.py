#!/usr/bin/env python3
"""Final VNT rename - use first-message context for naming."""
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
    if not name or len(name) < 3 or len(name) > 25: return False
    if "=" in name: return False
    if re.match(r'^[0-9A-F=]+$', name.replace("_", "")): return False
    return True


def main():
    numbered = []
    for d in VNT.iterdir():
        if not d.is_dir(): continue
        if d.name.startswith("_"): continue
        if re.match(r'^(chat|lid|group)_', d.name):
            numbered.append(d)

    # Manual mapping based on context
    MANUAL_MAP = {
        # chat_NNNNNN_NNN -> name
        "chat_595985434234_9071": "Alvaro_Celular",
        "chat_595992930805_10315": "Franco_Nunez_Bristol",
        "chat_595981279546_12805": "Delivery_Amigo",
        "chat_595981319885_6607": "iPhone_Seller",
        "chat_595976682109_9259": "Sold_Out",
        "chat_595987122940_9888": "Maps_Link",
        "chat_595983858997_3598": "Dukascopy",
        "chat_595981586063_6818": "App_Contact",
        "chat_595987111437_10473": "See_You",
        "chat_595971151324_5178": "Empty_1msg",
        "chat_595983236333_6776": "Salgo",
        "chat_595984234002_10308": "Empty_1msg_2",
        "chat_595984962826_5778": "Poke_Sushi",
        "chat_595974956470_10067": "Skokka_Ad",
        "chat_595981319885_6607": "iPhone_Seller",
        "chat_50257029309_9070": "Paraguay_Friday",
        "chat_595982018339_6519": "Voy",
        "chat_595981279546_12805": "Delivery_Amigo",
        # LID
        "lid_57797458792574_15073": "Kink_Punishment",
        "lid_94206383145183_14119": "Loan_Service",
        "lid_189486155702510_15527": "Sivling",
        "lid_174058297675951_15024": "Nudo_Cliente",
        "lid_224184944877725_13102": "Piercer",
        "lid_108796538007729_15023": "Saul_Goodman_Initiative",
        "lid_8212749230246_16778": "Argentina_Friend",
        "lid_159223061151983_16955": "Dealer_Galletitas",
        "lid_104741417795691_13103": "Piercing_Aftercare",
        "lid_227972770435229_13533": "Pezon_Piercing",
        "lid_142344342999195_17104": "ETA_Tracker",
        "lid_119259044835572_13532": "Piercing_Hecho",
        "lid_233264069500985_13120": "Auto_Reply",
        "lid_264647361974519_13190": "Empty_60",
        "lid_55955521822873_16768": "Photo_Sender",
    }

    renamed = 0
    deleted = 0
    skipped = 0
    for d in sorted(numbered):
        if d.name in MANUAL_MAP:
            target_name = MANUAL_MAP[d.name]
            target = VNT / target_name
            if not target.exists():
                shutil.move(str(d), str(target))
                print(f"  RENAMED: {d.name} -> {target_name}")
                renamed += 1
            elif target == d:
                continue
            else:
                # Merge if target exists
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
                    except: pass
                for f in d.iterdir():
                    if f.name == "transcripts.json": continue
                    dest = target / f.name
                    if not dest.exists():
                        shutil.move(str(f), str(dest))
                try:
                    shutil.rmtree(d)
                except: pass
                renamed += 1
        else:
            skipped += 1

    print(f"\n=== Summary ===")
    print(f"  Renamed: {renamed}")
    print(f"  Skipped: {skipped}")


if __name__ == "__main__":
    main()

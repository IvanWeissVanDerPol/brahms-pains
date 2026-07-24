#!/usr/bin/env python3
"""Group the 882 not-saved chats by patterns."""
from __future__ import annotations
import json
import re
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS"
MSG_BASE = REPO / "SOURCE_OF_TRUTH" / "wa_messages"

# Load not-saved
ns = json.loads((ANALYSIS / "contacts_not_saved.json").read_text())
chats = ns["chats"]

# Business / customer keywords (Spanish - typical for Paraguay)
BIZ = re.compile(
    r"\b(precio|cotiza[cs]i[oó]n|presupuesto|factura|cliente|cu[áa]nto\s+cuesta|"
    r"whatsapp|envío|entrega|pago|transferencia|tigo|personal|claro|"
    r"3d|imprimir|impresora|molde|figur|plastilina|resina|filamento|"
    r"pedido|orden|stock|disponible|tienda|oferta)\b",
    re.IGNORECASE
)
ROMANTIC = re.compile(
    r"[💕❤️💖💗💓💞💘💝😻🥰]|"
    r"\b(amor|bebe|bb|cari[ñn]o|te\s+amo|hermosa|guapa|bonita)\b",
    re.IGNORECASE
)
FAMILY = re.compile(
    r"\b(mama|papa|mamá|papá|abuela|abuelo|t[íi]o|t[íi]a|"
    r"primo|prima|hermana|hermano|sister|brother|family)\b",
    re.IGNORECASE
)
SERVICE = re.compile(
    r"\b(automático|respuesta\s+auto|fuera\s+de\s+horario|"
    r"gracias\s+por\s+contactar|horario\s+de\s+atención|"
    r"delivery|envío\s+gratis|menú\s+del\s+día|pedido\s+recibido)\b",
    re.IGNORECASE
)


def classify_chat(chat_dir: Path) -> tuple[str, dict]:
    """Return (category, stats) for a chat dir."""
    if not (chat_dir / "messages.json").exists():
        return "empty", {}
    try:
        data = json.loads((chat_dir / "messages.json").read_text())
    except Exception:
        return "error", {}
    msgs = data.get("messages", [])
    if not msgs:
        return "empty", {}
    
    # Single message = likely wrong number / missed call
    if len(msgs) <= 1:
        return "single_msg", {"count": len(msgs)}
    
    # Sample text
    text_samples = []
    for m in msgs[:50]:  # First 50 messages
        if isinstance(m, dict) and m.get("type") == 0 and m.get("text"):
            text_samples.append(m["text"])
    
    text_all = " ".join(text_samples)
    
    # Group indicator: JID starts with group or has >5 in tier4_groups
    is_group_path = "tier4_groups" in str(chat_dir) or "_wa_group_" in chat_dir.name
    
    # Score matches
    n_biz = len(BIZ.findall(text_all))
    n_rom = len(ROMANTIC.findall(text_all))
    n_fam = len(FAMILY.findall(text_all))
    n_svc = len(SERVICE.findall(text_all))
    
    has_audio = any(m.get("type") == 2 for m in msgs if isinstance(m, dict))
    
    if is_group_path:
        return "group", {"count": len(msgs), "n_biz": n_biz, "n_fam": n_fam, "has_audio": has_audio}
    if n_svc > 2 and n_biz < 3:
        return "service_bot", {"count": len(msgs), "n_svc": n_svc}
    if n_biz > 5:
        return "business", {"count": len(msgs), "n_biz": n_biz}
    if n_rom > 10 and n_biz < 3:
        return "romantic", {"count": len(msgs), "n_rom": n_rom}
    if n_fam > 5 and n_biz < 3:
        return "family", {"count": len(msgs), "n_fam": n_fam}
    if has_audio and len(msgs) > 50:
        return "active_chat", {"count": len(msgs), "has_audio": True}
    if len(msgs) < 10:
        return "low_volume", {"count": len(msgs)}
    return "casual", {"count": len(msgs)}


def main():
    groups = defaultdict(list)
    stats = defaultdict(int)
    
    print(f"Classifying {len(chats)} not-saved chats...")
    for i, c in enumerate(chats):
        if i % 100 == 0:
            print(f"  {i}/{len(chats)}")
        chat_dir = MSG_BASE / c["tier"] / Path(c["current_dir"]).name
        cat, info = classify_chat(chat_dir)
        groups[cat].append({
            "jid": c["jid"],
            "tier": c["tier"],
            "dirname": Path(c["current_dir"]).name,
            "provisional_name": c.get("provisional_name", ""),
            **info,
        })
        stats[cat] += 1
    
    out = {
        "generated_at": "2026-07-23T22:30:00",
        "total": len(chats),
        "categories": dict(stats),
        "groups": dict(groups),
    }
    out_path = ANALYSIS / "contacts_not_saved_grouped.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    
    print(f"\n=== Classification ===")
    for cat, count in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {cat:<20} {count:>4}")
    
    print(f"\nWrote {out_path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
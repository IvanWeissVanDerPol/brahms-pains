#!/usr/bin/env python3
"""Voice note vs text preference per contact (Hat 7, 32)."""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH/wa_messages"
ANALYSIS = WA / "_ANALYSIS"


def analyze_voice_vs_text():
    """For each contact, calculate ratio of voice notes vs text messages."""
    by_chat = {}

    tiers = [
        "tier1_deep",
        "tier2_core",
        "tier3_extended",
        "tier4_groups",
        "untiered_personal",
        "other_lid",
    ]

    for tier in tiers:
        d = WA / tier
        if not d.exists():
            continue
        for chat in d.iterdir():
            if not chat.is_dir():
                continue
            mf = chat / "messages.json"
            if not mf.exists():
                continue
            try:
                data = json.loads(mf.read_text())
            except:
                continue

            msgs = data.get("messages", [])
            if not msgs:
                continue

            chat_name = chat.name

            # Count voice notes vs text
            # WhatsApp message types: 0=text, 1=image, 2=audio (PTT), 3=video, 4=contact, etc.
            voice_notes = 0
            text_msgs = 0
            media_msgs = 0

            for m in msgs:
                if not isinstance(m, dict):
                    continue

                msg_type = m.get("type")
                # type=2 is audio/PTT (voice note)
                if msg_type == 2:
                    voice_notes += 1
                elif msg_type in (1, 3, 4, 5, 8, 9):  # image, video, contact, etc
                    media_msgs += 1
                elif msg_type == 0 or m.get("text"):
                    text_msgs += 1

            total = voice_notes + text_msgs + media_msgs
            if total < 10:
                continue

            voice_pct = voice_notes / total if total > 0 else 0
            text_pct = text_msgs / total if total > 0 else 0

            by_chat[chat_name] = {
                "tier": tier,
                "total_msgs": total,
                "voice_notes": voice_notes,
                "text_msgs": text_msgs,
                "media_msgs": media_msgs,
                "voice_pct": round(voice_pct, 3),
                "text_pct": round(text_pct, 3),
                "audio_intensity": round(voice_notes / 100, 1) if voice_notes > 0 else 0,
            }

    # Categorize
    audio_heavy = []
    text_heavy = []
    balanced = []

    for c, info in by_chat.items():
        if info["voice_notes"] >= 20:
            audio_heavy.append((c, info))
        if info["voice_pct"] > 0.5:
            audio_heavy.append((c, info))
        if info["text_pct"] > 0.9:
            text_heavy.append((c, info))
        if 0.3 <= info["voice_pct"] <= 0.5:
            balanced.append((c, info))

    audio_heavy.sort(key=lambda x: -x[1]["voice_pct"])
    text_heavy.sort(key=lambda x: -x[1]["text_msgs"])

    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_chats_analyzed": len(by_chat),
        "audio_heavy_count": len(audio_heavy),
        "text_heavy_count": len(text_heavy),
        "balanced_count": len(balanced),
        "per_chat": by_chat,
    }

    out = ANALYSIS / "voice_vs_text.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"Wrote {out.relative_to(REPO)}")

    print("\n=== Voice vs Text Preference ===")
    print(f"Total analyzed: {len(by_chat)}")
    print(f"Audio-heavy (>=50% voice): {len(audio_heavy)}")
    print(f"Text-heavy (>90% text): {len(text_heavy)}")

    print("\nTop 15 audio-heavy contacts (most voice notes):")
    for c, info in sorted(by_chat.items(), key=lambda x: -x[1]["voice_notes"])[:15]:
        if info["voice_notes"] > 0:
            print(
                f"  {info['voice_notes']:>4} voice  {info['voice_pct']:>5.1%}  {info['tier']:<15}  {c[:35]}"
            )

    print("\nTop 15 voice-preferred (highest voice%):")
    for c, info in audio_heavy[:15]:
        print(
            f"  {info['voice_pct']:>5.1%} voice  {info['voice_notes']:>4} v / {info['text_msgs']:>4} t  {c[:35]}"
        )

    print("\nTop 10 text-only contacts (>95% text):")
    text_only = [
        (c, info)
        for c, info in by_chat.items()
        if info["text_pct"] > 0.95 and info["total_msgs"] >= 50
    ]
    for c, info in sorted(text_only, key=lambda x: -x[1]["total_msgs"])[:10]:
        print(
            f"  {info['text_pct']:>5.1%} text  {info['total_msgs']:>5} msgs  {info['tier']:<15}  {c[:30]}"
        )


if __name__ == "__main__":
    analyze_voice_vs_text()

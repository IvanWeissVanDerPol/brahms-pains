#!/usr/bin/env python3
"""Fill in 30 highest-priority profile stubs with auto-extracted analysis.

For each profile stub with TODO sections, extract:
- Top 5 key messages (notable moments)
- Monthly message volume pattern (peak months)
- Language mix (es/en/other)
- Relationship signals (emojis, time patterns, nicknames)
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
ANALYSIS = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS"
PROFILE_DIR = REPO / "RELATIONSHIPS" / "dynamics"
MSG_BASE = REPO / "SOURCE_OF_TRUTH" / "wa_messages"

# Family/rich profiles to SKIP
SKIP_PROFILES = {
    "SONIA_WEISS", "JOHN", "RIET_VAN_DER_POL", "JAN_VAN_DER_POL",
    "GEROLD_MANDERS", "LUANA", "KIKI_WEISS_HERMANA", "MIKAELA_WEISS",
    "PRIMA_MIKAELA_WEISS", "ARA_NUNEZ_POLI", "ALVARO_LLANO",
    "MAGALI_CARRERAS", "JONATAN_VERDUN", "EMILIO_POLI",
}

# Already-existing rich profiles (have content beyond TODO stub)
RICH_PROFILES = set()
for p in PROFILE_DIR.glob("*.md"):
    content = p.read_text()
    # If profile has actual content (not just TODO stubs), skip
    if "TODO" not in content and len(content) > 1500:
        RICH_PROFILES.add(p.stem)
print(f"Skipping {len(RICH_PROFILES)} rich profiles", file=__import__('sys').stderr)


def analyze_chat(chat_dir: Path) -> dict:
    """Extract key signals from a chat."""
    if not (chat_dir / "messages.json").exists():
        return {}
    try:
        data = json.loads((chat_dir / "messages.json").read_text())
    except Exception:
        return {}
    msgs = data.get("messages", [])
    if not msgs:
        return {}
    
    # Top notable messages: longest, most emojis, or with special markers
    notable = []
    monthly = Counter()
    weekday = Counter()
    hour = Counter()
    lang = Counter()
    ivan_nicknames = Counter()
    them_nicknames = Counter()
    emojis_total = 0
    ivan_total = 0
    them_total = 0
    
    # Top topic words (excluding stopwords)
    STOPWORDS = set("""a al algo algunas algunos ante antes como con contra cual cuando de del desde donde
durante e el ella ellas ellos en entre era erais eran eres es esa esas ese eso esos esta
estaba estado estáis estamos están estar este esto estos fue fui fuiste fueron ha habida
habido habidos habiendo han has hasta hay la las le les lo los más me mi mis mucho muy
nada ni no nos nosotros o os otra otras otro otros para pero poco por porque que quien se
sea sean seáis somos son soy su sus también tanto te tendrá tendrán tendrás tendré
tendríamos tendría tienes toda todas todo todos tu tus un una uno unos vosotras vosotros
voy y ya yo""".split())
    topic_words = Counter()
    
    for m in msgs:
        if not isinstance(m, dict):
            continue
        text = m.get("text") or ""
        ts_full = m.get("ts_iso", "")
        ts = ts_full[:7]  # YYYY-MM
        if ts: monthly[ts] += 1
        
        # Day of week and hour
        if ts_full:
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(ts_full[:19])
                weekday[dt.strftime("%A")] += 1
                hour[dt.hour] += 1
            except Exception:
                pass
        
        # Language detection (simple)
        text_low = text.lower()
        has_es = bool(re.search(r'\b(hola|como|estas|gracias|por|para|que|pero|porque)\b', text_low))
        has_en = bool(re.search(r'\b(the|and|you|for|with|that|this|hello|thanks)\b', text_low))
        if has_es and not has_en:
            lang["es"] += 1
        elif has_en and not has_es:
            lang["en"] += 1
        elif has_es and has_en:
            lang["mixed"] += 1
        else:
            lang["other"] += 1
        
        # Emoji count
        emoji_n = len(re.findall(r'[\U0001F300-\U0001F9FF\U00002600-\U000027BF]', text))
        emojis_total += emoji_n
        if ts:
            # distribute emojis to month
            pass
        
        # Topic extraction: top words > 4 chars
        if m.get("type") == 0 and text:
            for word in re.findall(r'\b[a-záéíóúñ]{5,}\b', text_low):
                if word not in STOPWORDS:
                    topic_words[word] += 1
        
        if m.get("from_me"):
            ivan_total += 1
            for nickname in ["kiki", "kyrian", "luana", "saskia", "mama", "mamá", "papa", "papá", "amor", "bebe", "bb", "loco", "loca", "gordo", "gorda", "rey", "reina", "princess", "princesa"]:
                if re.search(rf'\b{nickname}\b', text_low):
                    ivan_nicknames[nickname] += 1
        else:
            them_total += 1
            for nickname in ["ivan", "iván", "amor", "loco", "loca", "bebe", "bb", "gordo", "gorda", "rey", "reina", "princess", "princesa"]:
                if re.search(rf'\b{nickname}\b', text_low):
                    them_nicknames[nickname] += 1
        
        # Notable messages: long OR many emojis OR many exclamations
        if len(text) > 60 and (emoji_n >= 1 or text.count("!") >= 1 or text.count("?") >= 1 or len(text) > 200):
            notable.append({
                "ts": ts_full[:10],
                "from_ivan": m.get("from_me"),
                "text": text[:300],
                "emoji_n": emoji_n,
            })
    
    # Sort notable by emoji count then length
    notable.sort(key=lambda x: (-x["emoji_n"], -len(x["text"])))
    notable = notable[:5]
    
    # Peak months
    peak_months = sorted(monthly.most_common(5), key=lambda x: x[0])
    
    # Top weekday
    top_weekday = weekday.most_common(1)[0] if weekday else ("—", 0)
    # Top hour
    top_hour = hour.most_common(1)[0] if hour else (-1, 0)
    # Top topics
    top_topics = topic_words.most_common(8)
    
    # Nicknames
    top_ivan_nicks = ivan_nicknames.most_common(5)
    top_them_nicks = them_nicknames.most_common(5)
    
    return {
        "ivan_total": ivan_total,
        "them_total": them_total,
        "monthly": dict(sorted(monthly.items())),
        "lang": dict(lang),
        "peak_months": peak_months,
        "notable": notable,
        "ivan_nicknames": dict(top_ivan_nicks),
        "them_nicknames": dict(top_them_nicks),
        "top_weekday": top_weekday[0],
        "top_hour": top_hour[0],
        "top_topics": top_topics,
        "emojis_total": emojis_total,
    }


def main():
    data = json.loads((ANALYSIS / "viewer_full_data.json").read_text())
    contacts = sorted(data["vcard_contacts"], key=lambda c: -c["total"])
    
    filled = 0
    for c in contacts[:200]:  # Top 200 by msg count
        # Build slug
        name = c["name"]
        slug = name.upper()
        slug = slug.replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")
        slug = slug.replace("Ñ", "N")
        slug = re.sub(r"[^A-Z0-9]+", "_", slug)
        slug = re.sub(r"_+", "_", slug).strip("_")
        
        if slug in RICH_PROFILES or slug in SKIP_PROFILES:
            continue
        
        profile_path = PROFILE_DIR / f"{slug}.md"
        if not profile_path.exists():
            continue
        
        # Read existing
        existing = profile_path.read_text()
        
        # Skip only if has all sections: Overview, Notable, AND Top topics
        if ("Auto-extracted stats" in existing 
            and "Top topics:" in existing
            and "## Notable messages (auto-extracted)\n\n- **" in existing):
            continue
        
        # Analyze
        chat_dir = MSG_BASE / c["tier"] / c["dir"]
        analysis = analyze_chat(chat_dir)
        
        if not analysis:
            continue
        
        # Build new sections
        monthly_str = ""
        if analysis["monthly"]:
            sorted_months = sorted(analysis["monthly"].items())
            top_3 = sorted(analysis["peak_months"][:3], key=lambda x: x[0])
            monthly_str = "Peak months: " + ", ".join(f"`{m}` ({n} msgs)" for m, n in top_3) + "\n"
        
        lang_str = ", ".join(f"{k}: {v}" for k, v in analysis["lang"].items()) or "n/a"
        
        # Format peak hour/weekday/topic
        hour_str = f"{analysis['top_hour']}:00" if analysis['top_hour'] >= 0 else "—"
        weekday_str = analysis['top_weekday']
        topics_str = ", ".join(f"{w} ({c})" for w, c in analysis['top_topics'][:5]) or "n/a"
        
        notable_str = ""
        if analysis["notable"]:
            notable_str = "\n## Notable messages (auto-extracted)\n\n"
            for n in analysis["notable"]:
                sender = "Ivan" if n["from_ivan"] else "Them"
                # Strip raw text to avoid regex escape issues
                safe_text = re.sub(r'[\\]', '', n["text"])
                safe_text = safe_text.replace("\n", " ").replace("\r", "")
                notable_str += f"- **[{n['ts']}] {sender}** ({n['emoji_n']} emojis): {safe_text}\n"
        
        nicks_str = ""
        if analysis["ivan_nicknames"]:
            nicks_str += f"\n**Ivan calls them:** {', '.join(f'{n!r} ({c}x)' for n, c in analysis['ivan_nicknames'].items())}\n"
        if analysis["them_nicknames"]:
            nicks_str += f"\n**They call Ivan:** {', '.join(f'{n!r} ({c}x)' for n, c in analysis['them_nicknames'].items())}\n"
        
        # Replace TODO sections - use lambda to avoid backslash escape interpretation
        new_content = existing
        safe_overview = (
            f"## Overview\n\n"
            f"**Auto-extracted stats** ({analysis['ivan_total']:,} from Ivan, {analysis['them_total']:,} from them, {analysis['emojis_total']:,} emojis)\n\n"
            f"{monthly_str}"
            f"Language mix: {lang_str}\n"
            f"Most active: **{weekday_str}** at **{hour_str}**\n"
            f"Top topics: {topics_str}\n"
            f"{nicks_str}"
            f"\n## Communication stats\n"
        )
        # Replace Overview - match either TODO form or existing filled form
        new_content = re.sub(
            r"## Overview\n\n.*?(?=\n## )",
            lambda m: safe_overview,
            new_content,
            flags=re.DOTALL,
        )
        safe_notable = (
            f"## Key moments / Topics\n\n"
            f"Auto-extracted notable messages from the chat:\n"
            f"{notable_str}\n"
        )
        # Try multiple variants of the Key moments header
        new_content = re.sub(
            r"## Key moments / Topics\n\n.*?(?=\n## |\Z)",
            lambda m: safe_notable,
            new_content,
            flags=re.DOTALL,
        )
        # Cleanup: remove duplicate "## Communication stats" headers from prior runs
        new_content = re.sub(r"(## Communication stats\n\n)+", "## Communication stats\n\n", new_content)
        
        profile_path.write_text(new_content)
        filled += 1
        print(f"  ✓ {slug} ({analysis['ivan_total']:,}+{analysis['them_total']:,} msgs)")
    
    print(f"\nFilled {filled} profiles")


if __name__ == "__main__":
    main()
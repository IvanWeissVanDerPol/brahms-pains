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
    
    # Sort chronologically
    sorted_msgs = sorted(
        [m for m in msgs if isinstance(m, dict) and m.get("ts_iso")],
        key=lambda m: m["ts_iso"]
    )
    
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
    ivan_word_chars = 0
    them_word_chars = 0
    ivan_msg_count = 0
    them_msg_count = 0
    questions_ivan = 0
    questions_them = 0
    
    # First / last messages
    first_msg = None
    last_msg_ivan = None
    last_msg_them = None
    last_ivan_text = ""
    last_them_text = ""
    
    # Response times
    response_times_ivan = []  # time for Ivan to reply after them
    response_times_them = []  # time for them to reply after Ivan
    last_sender = None
    last_ts = None
    
    # Time of day buckets
    tod_buckets = Counter()  # morning, afternoon, evening, night
    
    # Audio usage
    audio_count = 0
    total_msg_with_ts = 0
    
    # Sentiment markers
    POS_WORDS = set("""amor amo encanta feliz bien gracias guapo guapa hermosa hermoso
amor contento contenta alegria feliz amazing love gracias lovely enjoy wonderful
excelente increible perfecto gracias gracias""".split())
    NEG_WORDS = set("""mal triste odio enojado enojada molesto molesta cansado cansada
horrible terrible mal fatal feo fea asco dolor problema problemas angry sad
tired hate upset hate""".split())
    pos_ivan = 0
    pos_them = 0
    neg_ivan = 0
    neg_them = 0
    
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
    
    for m in sorted_msgs:
        text = m.get("text") or ""
        ts_full = m.get("ts_iso", "")
        ts = ts_full[:7]  # YYYY-MM
        if ts: monthly[ts] += 1
        
        # Day of week and hour
        if ts_full:
            try:
                dt = datetime.fromisoformat(ts_full[:19])
                weekday[dt.strftime("%A")] += 1
                hour[dt.hour] += 1
                # Time of day bucket
                h = dt.hour
                if 6 <= h < 12: tod_buckets["morning (6-12)"] += 1
                elif 12 <= h < 18: tod_buckets["afternoon (12-18)"] += 1
                elif 18 <= h < 23: tod_buckets["evening (18-23)"] += 1
                else: tod_buckets["night (23-6)"] += 1
            except Exception:
                pass
        
        # First message
        if first_msg is None and text:
            first_msg = {
                "ts": ts_full[:10],
                "from_ivan": m.get("from_me"),
                "text": text[:200],
            }
        
        # Last messages per side
        if m.get("from_me") and text:
            last_msg_ivan = {"ts": ts_full[:10], "text": text[:200]}
            last_ivan_text = text[:200]
        elif text and not m.get("from_me"):
            last_msg_them = {"ts": ts_full[:10], "text": text[:200]}
            last_them_text = text[:200]
        
        # Response time: time between consecutive different senders
        try:
            if last_sender is not None and last_sender != m.get("from_me") and last_ts and text:
                from datetime import datetime as dt_cls
                t1 = dt_cls.fromisoformat(last_ts[:19])
                t2 = dt_cls.fromisoformat(ts_full[:19])
                delta = (t2 - t1).total_seconds()
                if delta < 86400:  # Only count if reply within 24h
                    if m.get("from_me"):
                        response_times_ivan.append(delta)
                    else:
                        response_times_them.append(delta)
            last_sender = m.get("from_me")
            last_ts = ts_full
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
        
        # Topic extraction: top words > 4 chars
        if m.get("type") == 0 and text:
            for word in re.findall(r'\b[a-záéíóúñ]{5,}\b', text_low):
                if word not in STOPWORDS:
                    topic_words[word] += 1
        
        # Audio usage tracking
        if ts_full:
            total_msg_with_ts += 1
        if m.get("type") == 2:  # audio
            audio_count += 1
        
        # Per-side stats
        is_ivan = m.get("from_me")
        
        # Sentiment tracking
        for word in text_low.split():
            if word in POS_WORDS:
                if is_ivan: pos_ivan += 1
                else: pos_them += 1
            elif word in NEG_WORDS:
                if is_ivan: neg_ivan += 1
                else: neg_them += 1
        if is_ivan:
            ivan_total += 1
            ivan_word_chars += len(text)
            ivan_msg_count += 1
            if "?" in text: questions_ivan += 1
            for nickname in ["kiki", "kyrian", "luana", "saskia", "mama", "mamá", "papa", "papá", "amor", "bebe", "bb", "loco", "loca", "gordo", "gorda", "rey", "reina", "princess", "princesa"]:
                if re.search(rf'\b{nickname}\b', text_low):
                    ivan_nicknames[nickname] += 1
        else:
            them_total += 1
            them_word_chars += len(text)
            them_msg_count += 1
            if "?" in text: questions_them += 1
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
    
    # Avg response times
    def avg_seconds(times):
        return sum(times) / len(times) if times else 0
    avg_ivan_reply = avg_seconds(response_times_ivan)
    avg_them_reply = avg_seconds(response_times_them)
    
    # Avg msg length
    avg_ivan_len = ivan_word_chars / ivan_msg_count if ivan_msg_count else 0
    avg_them_len = them_word_chars / them_msg_count if them_msg_count else 0
    
    # Question ratio
    q_ivan_ratio = questions_ivan / ivan_msg_count if ivan_msg_count else 0
    q_them_ratio = questions_them / them_msg_count if them_msg_count else 0
    
    # Top time-of-day bucket
    top_tod = tod_buckets.most_common(1)[0] if tod_buckets else ("—", 0)
    
    # Streak analysis: daily and gap
    daily_counts = Counter()  # YYYY-MM-DD -> count
    for m in sorted_msgs:
        d = m.get("ts_iso", "")[:10]
        if d: daily_counts[d] += 1
    sorted_days = sorted(daily_counts.keys())
    
    # Longest daily streak
    longest_streak = 0
    cur_streak = 0
    prev_day = None
    for d in sorted_days:
        if prev_day:
            from datetime import date
            try:
                d1 = date.fromisoformat(prev_day)
                d2 = date.fromisoformat(d)
                if (d2 - d1).days == 1:
                    cur_streak += 1
                else:
                    cur_streak = 1
            except Exception:
                cur_streak = 1
        else:
            cur_streak = 1
        longest_streak = max(longest_streak, cur_streak)
        prev_day = d
    
    # Longest gap
    longest_gap = 0
    for i in range(1, len(sorted_days)):
        from datetime import date
        try:
            d1 = date.fromisoformat(sorted_days[i-1])
            d2 = date.fromisoformat(sorted_days[i])
            gap = (d2 - d1).days
            longest_gap = max(longest_gap, gap)
        except Exception:
            pass
    
    # Audio ratio
    audio_ratio = audio_count / total_msg_with_ts if total_msg_with_ts else 0
    
    # Sentiment balance
    sentiment_score_ivan = (pos_ivan - neg_ivan) / max(1, pos_ivan + neg_ivan)
    sentiment_score_them = (pos_them - neg_them) / max(1, pos_them + neg_them)
    
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
        "first_msg": first_msg,
        "last_msg_ivan": last_msg_ivan,
        "last_msg_them": last_msg_them,
        "avg_ivan_reply_s": avg_ivan_reply,
        "avg_them_reply_s": avg_them_reply,
        "avg_ivan_len": avg_ivan_len,
        "avg_them_len": avg_them_len,
        "q_ivan_ratio": q_ivan_ratio,
        "q_them_ratio": q_them_ratio,
        "top_tod": top_tod[0],
        "tod_buckets": dict(tod_buckets),
        "longest_streak": longest_streak,
        "longest_gap": longest_gap,
        "audio_ratio": audio_ratio,
        "pos_ivan": pos_ivan,
        "pos_them": pos_them,
        "neg_ivan": neg_ivan,
        "neg_them": neg_them,
        "sentiment_score_ivan": sentiment_score_ivan,
        "sentiment_score_them": sentiment_score_them,
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
        
        # Skip only if has all sections
        if ("Auto-extracted stats" in existing 
            and "Top topics:" in existing
            and "## Notable messages (auto-extracted)\n\n- **" in existing
            and "First message" in existing
            and "Avg reply time" in existing
            and "Longest streak" in existing  # New: skip if already has streak
            and "Audio usage" in existing):  # New: skip if already has audio
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
        
        # Format response times (in minutes/seconds)
        def fmt_time(s):
            if not s: return "n/a"
            if s < 60: return f"{int(s)}s"
            if s < 3600: return f"{int(s/60)}m"
            if s < 86400: return f"{s/3600:.1f}h"
            return f"{s/86400:.1f}d"
        ivan_reply_str = fmt_time(analysis['avg_ivan_reply_s'])
        them_reply_str = fmt_time(analysis['avg_them_reply_s'])
        
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
        
        # First / last messages
        first_msg_str = ""
        if analysis.get("first_msg"):
            fm = analysis["first_msg"]
            sender = "Ivan" if fm["from_ivan"] else "Them"
            safe_text = re.sub(r'[\\]', '', fm["text"]).replace("\n", " ").replace("\r", "")
            first_msg_str = f"\n**First message** ({fm['ts']}, {sender}): {safe_text}\n"
        
        last_msg_str = ""
        if analysis.get("last_msg_ivan"):
            lm = analysis["last_msg_ivan"]
            safe_text = re.sub(r'[\\]', '', lm["text"]).replace("\n", " ").replace("\r", "")
            last_msg_str += f"\n**Last from Ivan** ({lm['ts']}): {safe_text}\n"
        if analysis.get("last_msg_them"):
            lm = analysis["last_msg_them"]
            safe_text = re.sub(r'[\\]', '', lm["text"]).replace("\n", " ").replace("\r", "")
            last_msg_str += f"\n**Last from them** ({lm['ts']}): {safe_text}\n"
        
        # Replace Overview - match either TODO form or existing filled form
        new_content = existing
        # Format sentiment as bar
        def sentiment_str(score):
            if score > 0.3: return f"+{score:.2f} (very positive)"
            if score > 0: return f"+{score:.2f} (positive)"
            if score > -0.3: return f"{score:.2f} (slightly negative)"
            return f"{score:.2f} (very negative)"
        
        safe_overview = (
            f"## Overview\n\n"
            f"**Auto-extracted stats** ({analysis['ivan_total']:,} from Ivan, {analysis['them_total']:,} from them, {analysis['emojis_total']:,} emojis)\n\n"
            f"{monthly_str}"
            f"Language mix: {lang_str}\n"
            f"Most active: **{weekday_str}** at **{hour_str}** ({analysis['top_tod']})\n"
            f"Top topics: {topics_str}\n"
            f"Avg msg length: Ivan {analysis['avg_ivan_len']:.0f} chars, them {analysis['avg_them_len']:.0f} chars\n"
            f"Avg reply time: Ivan {ivan_reply_str}, them {them_reply_str}\n"
            f"Question ratio: Ivan {analysis['q_ivan_ratio']:.1%}, them {analysis['q_them_ratio']:.1%}\n"
            f"Longest streak: **{analysis['longest_streak']}** consecutive days · Longest gap: **{analysis['longest_gap']}** days\n"
            f"Audio usage: {analysis['audio_ratio']:.1%} of all messages are voice notes\n"
            f"Sentiment: Ivan {sentiment_str(analysis['sentiment_score_ivan'])} (pos {analysis['pos_ivan']} / neg {analysis['neg_ivan']}), them {sentiment_str(analysis['sentiment_score_them'])} (pos {analysis['pos_them']} / neg {analysis['neg_them']})\n"
            f"{nicks_str}"
            f"{first_msg_str}"
            f"{last_msg_str}"
            f"\n## Communication stats\n"
        )
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
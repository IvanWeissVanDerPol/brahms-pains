"""
Harvest Indico UNA conferences with non-zero contributions.
- Event 2: XVII JJI 2023 (2 contribs)
- Event 7: IV Congreso Internacionalización 2024 (108 contribs)
- Event 18: Coloquio Paraguayo de Matemática 2025 (28 contribs)
- Event 19: VII Foro Investigación FACSO 2025 (5 contribs)
- Event 20: VII Simposio Química 2025 (6 contribs)
- Event 21: SOLABIMA 2026
- Event 26: XX JJI 2026 (live, 0 contributions yet)
"""
import json, re, urllib.request, urllib.error, time
from pathlib import Path

OUT_DIR = Path("SOURCE_OF_TRUTH/fpuna_research")
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

def fetch(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=30) as r:
            return r.read().decode("utf-8", errors="replace"), r.status
    except urllib.error.HTTPError as e:
        return "", e.code
    except Exception as e:
        return "", f"ERR:{type(e).__name__}"

EVENTS = [2, 7, 18, 19, 20, 21, 26]

results = []
for eid in EVENTS:
    print(f"\n=== Event {eid} ===")
    page, status = fetch(f"https://indico.una.py/event/{eid}/")
    if status != 200:
        print(f"  status={status}")
        continue
    title = re.search(r'<title>([^<]+)</title>', page)
    title_clean = title.group(1).strip() if title else f"event-{eid}"
    n_contrib = re.search(r'data-event-contrib-count=\"(\d+)\"', page)
    contrib_count = int(n_contrib.group(1)) if n_contrib else 0
    print(f"  title: {title_clean[:80]}")
    print(f"  contribs: {contrib_count}")
    # Try the materials page (often has PDFs)
    mats, status_m = fetch(f"https://indico.una.py/event/{eid}/material/")
    mats_len = len(mats) if status_m == 200 else 0
    print(f"  material: {status_m} ({mats_len} bytes)")
    # Look for embedded links
    for sub_path in ['/', '/contributions/', '/timetable/', '/sessions/']:
        url = f"https://indico.una.py/event/{eid}{sub_path}"
        html, st = fetch(url)
        # search for session/contribution links
        links = re.findall(r'href=\"(/event/' + str(eid) + r'/(?:sessions|contributions)/\d+/)\"', html)
        if links:
            print(f"  {sub_path}: {len(set(links))} unique links")
            for l in list(set(links))[:8]: print(f"    {l}")
            break
    results.append({
        "event_id": eid,
        "title": title_clean,
        "contrib_count": contrib_count,
        "url": f"https://indico.una.py/event/{eid}/",
    })
    time.sleep(0.5)

out_path = OUT_DIR / "indico_una_events.json"
json.dump({
    "harvested_at": "2026-07-30",
    "source": "https://indico.una.py",
    "events": results,
}, open(out_path, "w"), ensure_ascii=False, indent=1)
print(f"\nWrote {out_path}")

"""
Harvest Indico UNA contributions across multiple events.
- Event 7: IV Congreso Internacionalización 2024 (108 contribs)
- Event 18: Coloquio Paraguayo de Matemática 2025 (28 contribs)
- Event 19: VII Foro Investigación FACSO 2025 (5 contribs)
- Event 20: VII Simposio Química 2025 (6 contribs)

For each contribution: extract title, authors, abstract, contribution_type, affiliations.
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

def discover_contribs(eid):
    html, st = fetch(f"https://indico.una.py/event/{eid}/contributions/")
    if st != 200: return []
    links = sorted(set(re.findall(r'href=\"(/event/' + str(eid) + r'/(?:contributions)/\d+/)\"', html)))
    return [f"https://indico.una.py{l}" for l in links]

def parse_contrib(html, url):
    rec = {"url": url}
    # Title
    h2 = re.search(r'<h2[^>]*>(.*?)</h2>', html, re.DOTALL)
    if h2:
        rec["title"] = re.sub(r'<[^>]+>', ' ', h2.group(1)).strip()
    # Authors
    auth = re.search(r'<div[^>]*class="contribution-author-info"[^>]*>(.*?)</div>', html, re.DOTALL)
    if not auth:
        auth = re.search(r'<div[^>]*class="authors"[^>]*>(.*?)</div>', html, re.DOTALL)
    if auth:
        names = re.findall(r'<span[^>]*class="author-name"[^>]*>([^<]+)</span>', auth.group(1))
        if not names:
            names = re.findall(r'<a[^>]*>([^<]+)</a>', auth.group(1))
        if not names:
            names = re.findall(r'>([^<]{10,80})</(?:div|span)', auth.group(1))
        rec["authors"] = [n.strip() for n in names if n.strip() and not n.strip().startswith('http')]
    # Affiliation
    aff = re.search(r'<div[^>]*class="contribution-author-affiliation"[^>]*>(.*?)</div>', html, re.DOTALL)
    if aff:
        rec["affiliation"] = re.sub(r'<[^>]+>', ' ', aff.group(1)).strip()
    # Abstract
    abstract = re.search(r'<div[^>]*id="content"[^>]*>(.*?)</div>', html, re.DOTALL)
    if not abstract:
        abstract = re.search(r'<meta[^>]*property="og:description"[^>]*content="([^"]+)"', html)
    if abstract:
        text = re.sub(r'<[^>]+>', ' ', abstract.group(1)).strip() if hasattr(abstract, 'group') else abstract.group(1).strip()
        text = re.sub(r'\s+', ' ', text)
        rec["abstract"] = text[:2000]
    # Type
    ct = re.search(r'<span[^>]*class="contribution-type"[^>]*>([^<]+)</span>', html)
    if not ct:
        ct = re.search(r'class="icon-[^"]*contribution-([a-z]+)"', html)
    if ct:
        rec["type"] = ct.group(1).strip() if hasattr(ct, 'group') else ct.group(1)
    # Event reference
    rec["event"] = re.search(r'/event/(\d+)/', url).group(1) if re.search(r'/event/(\d+)/', url) else None
    return rec

EVENTS = [7, 18, 19, 20]
all_contribs = []
for eid in EVENTS:
    print(f"\n=== Event {eid} ===")
    pages = discover_contribs(eid)
    print(f"  found {len(pages)} contributions")
    for i, url in enumerate(pages):
        html, status = fetch(url)
        if status != 200:
            print(f"  {i+1}/{len(pages)} {url} status={status}")
            continue
        rec = parse_contrib(html, url)
        all_contribs.append(rec)
        if i % 10 == 0:
            print(f"  {i+1}/{len(pages)} {rec.get('title', '???')[:60]}")
        time.sleep(0.3)

out_path = OUT_DIR / "indico_una_contributions.json"
json.dump({
    "harvested_at": "2026-07-30",
    "source": "https://indico.una.py",
    "total_contributions": len(all_contribs),
    "by_event": {
        eid: sum(1 for c in all_contribs if c.get("event") == str(eid))
        for eid in EVENTS
    },
    "contributions": all_contribs,
}, open(out_path, "w"), ensure_ascii=False, indent=1)
print(f"\nWrote {out_path}  ({out_path.stat().st_size:,} bytes)  {len(all_contribs)} contributions")

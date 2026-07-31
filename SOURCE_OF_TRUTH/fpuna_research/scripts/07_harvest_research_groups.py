"""
Harvest all FP-UNA research groups + nuclei.
"""
import json, re, urllib.request, urllib.error, time
from pathlib import Path

OUT_DIR = Path("SOURCE_OF_TRUTH/fpuna_research")
OUT_DIR.mkdir(parents=True, exist_ok=True)
HEADERS = {"User-Agent": "Mozilla/5.0 (psycology-UNA-thesis-research, Ivan Weiss Van der Pol)"}

def fetch(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=30) as r:
            return r.read().decode("utf-8", errors="replace"), r.status
    except urllib.error.HTTPError as e:
        return "", e.code
    except Exception as e:
        return "", f"ERR:{type(e).__name__}"

ROOT = "https://www.pol.una.py"
SEED_URLS = [
    f"{ROOT}/investigacion/grupos-de-investigacion/",
    f"{ROOT}/investigacion/nucleos-de-investigacion/",
    f"{ROOT}/investigacion/grupo-de-investigacion-en-formacion/",
    f"{ROOT}/investigacion/investigadores/",
    f"{ROOT}/investigacion/proyectos-de-investigacion-2/",
]

def discover_links(html):
    """All links to research-group sub-pages."""
    links = set()
    # Absolute URLs
    for href in re.findall(r'href="(https?://www\.pol\.una\.py/investigacion/[^"]+)"', html):
        if href.endswith('/'):
            href = href[:-1]
        if any(x in href for x in ['/wp-json/', '#', '?', 'feed', 'embed']):
            continue
        n = href.replace('https://www.pol.una.py', '').count('/')
        if n <= 2:
            continue
        links.add(href)
    # Relative URLs
    for href in re.findall(r'href="(/investigacion/[^"]+)"', html):
        if href.endswith('/'):
            href = href[:-1]
        if any(x in href for x in ['/wp-json/', '#', '?', 'feed', 'embed']):
            continue
        if href.count('/') <= 2:
            continue
        links.add(ROOT + href)
    return links

def extract_field(html, label):
    pattern = rf'(?:<strong>|<b>){re.escape(label)}\s*[:\.]?\s*(?:</strong>|</b>)?\s*(.*?)(?=<(?:strong|br|p|li|h[1-6]|<div[^>]*class="[^\"]*footer))'
    m = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
    if m:
        text = re.sub(r'<[^>]+>', ' ', m.group(1))
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    return None

def parse_group_page(html, url):
    rec = {"url": url}
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if title_match:
        rec["name"] = re.sub(r'<[^>]+>', ' ', title_match.group(1)).strip()
    acronym = re.search(r'\(([A-Z][A-Z0-9\-]{1,9})\)', rec.get("name", ""))
    if acronym:
        rec["acronym"] = acronym.group(1)
    rec["goal"] = extract_field(html, "Objetivo")
    rec["research_lines"] = extract_field(html, "Líneas de investigación")
    rec["coordinator"] = extract_field(html, "Coordinador")
    rec["contact"] = extract_field(html, "Contacto")
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.una\.py', html)
    if emails:
        rec["emails"] = list(set(emails))
    phones = re.findall(r'\+?595[\s\-\d()]+', html)
    if phones:
        rec["phones"] = list(set(phones))
    body = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
    body = re.sub(r'<style.*?</style>', '', body, flags=re.DOTALL)
    body = re.sub(r'<[^>]+>', ' ', body)
    body = re.sub(r'\s+', ' ', body).strip()
    rec["body_excerpt"] = body[:1500]
    return rec

print("=== Phase 1: discovery ===")
all_links = set()
for url in SEED_URLS:
    html, status = fetch(url)
    if status == 200:
        new = discover_links(html)
        all_links.update(new)
        print(f"  {url}: {len(new)} new (total {len(all_links)})")
    else:
        print(f"  {url}: status={status}")
    time.sleep(0.5)

print(f"\n=== Phase 2: fetch {len(all_links)} pages ===")
groups = []
for i, url in enumerate(sorted(all_links)):
    html, status = fetch(url)
    if status == 200:
        rec = parse_group_page(html, url)
        groups.append(rec)
        print(f"  {i+1:>3d}/{len(all_links)} {rec.get('name', '???')[:60]:60s} ({rec.get('acronym', '-')})")
    else:
        print(f"  {i+1:>3d}/{len(all_links)} {url} status={status}")
    time.sleep(0.4)

out_path = OUT_DIR / "fpuna_research_groups.json"
json.dump({
    "harvested_at": "2026-07-29",
    "source": "https://www.pol.una.py/investigacion/",
    "n_groups": len(groups),
    "groups": groups,
}, open(out_path, "w"), ensure_ascii=False, indent=1)
print(f"\nWrote {out_path}  ({out_path.stat().st_size:,} bytes)  {len(groups)} groups")

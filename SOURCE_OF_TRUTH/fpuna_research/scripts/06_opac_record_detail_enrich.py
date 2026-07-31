"""
Enrich OPAC records by fetching /cgi-bin/koha/opac-detail.pl?biblionumber=N
Inputs: opac_una_full_v2.json (2217 records)
Output: opac_una_full_v2_enriched.json

For each record, fetch the detail page and extract:
- title (full)
- authors (list)
- orientadores (list)
- year (from publication date)
- branch (library)
- callnumber (signature)
- subject/keyword list
- thesis_type (Tesis, Trabajo Final de Grado, etc.)
- abstract (if available)
- online_resource_url (Recursos en línea)

Checkpoint every 50 records. Polite 0.5s delay.
"""
import json, re, urllib.request, urllib.error, time
from pathlib import Path

OUT_DIR = Path("SOURCE_OF_TRUTH/fpuna_research")
INPUT = OUT_DIR / "opac_una_full_v2.json"
CKPT = OUT_DIR / "opac_una_full_v2_enriched_ckpt.json"
OUTPUT = OUT_DIR / "opac_una_full_v2_enriched.json"

HEADERS = {"User-Agent": "Mozilla/5.0 (psycology-UNA-thesis-research, Ivan Weiss Van der Pol)"}

def fetch(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", errors="replace"), r.status
    except urllib.error.HTTPError as e:
        return "", e.code
    except Exception as e:
        return "", f"ERR:{type(e).__name__}"

# Load records
data = json.load(open(INPUT))
records = {r["bibnum"]: r for r in data["records"]}
print(f"Loaded {len(records)} records")

# Resume from checkpoint
if CKPT.exists():
    ckpt = json.load(open(CKPT))
    done = set(ckpt["done"])
    enriched = {r["bibnum"]: r for r in ckpt["enriched"]}
    print(f"Resumed: {len(done)} done, {len(enriched)} enriched")
else:
    done = set()
    enriched = {}

def parse_detail(html, bibnum):
    rec = {"bibnum": bibnum}
    # Title: <h1 class="title">TITULO</h1> or <span class="title">TITULO</span>
    m = re.search(r'<h1 class="title[^"]*"[^>]*>(.*?)</h1>', html, re.DOTALL)
    if m:
        rec["title"] = re.sub(r'<[^>]+>', ' ', m.group(1)).strip()
    # Authors: <td class="author"> or <span class="author">
    authors = re.findall(r'<a[^>]*class="author[^"]*"[^>]*>([^<]+)</a>', html)
    if not authors:
        authors = re.findall(r'<span class="author[^"]*">([^<]+)</span>', html)
    rec["authors"] = [a.strip() for a in authors]
    # Publication year
    yrs = re.findall(r'<span[^>]*pub[^"]*date[^"]*">(\d{4})</span>', html, re.IGNORECASE)
    if not yrs:
        yrs = re.findall(r'c(?:opyright)?\s*(\d{4})', html, re.IGNORECASE)
    if yrs:
        rec["year"] = yrs[0]
    # Branch (location)
    br = re.search(r'<span class="library[^"]*">([^<]+)</span>', html)
    if br:
        rec["branch"] = br.group(1).strip()
    # Callnumber
    cn = re.search(r'<span class="callnumber[^"]*">([^<]+)</span>', html)
    if cn:
        rec["callnumber"] = cn.group(1).strip()
    # Type
    type_match = re.search(r'<span class="results_material_type[^"]*">([^<]+)</span>', html)
    if type_match:
        rec["material_type"] = type_match.group(1).strip()
    # Subjects
    subjects = re.findall(r'<a[^>]*class="subject[^"]*"[^>]*>([^<]+)</a>', html)
    rec["subjects"] = [s.strip() for s in subjects]
    # Abstract
    ab = re.search(r'<div[^>]*class="abstract[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
    if ab:
        rec["abstract"] = re.sub(r'<[^>]+>', ' ', ab.group(1)).strip()
    # Online resource
    on = re.findall(r'href="(https?://[^"]*sdi\.cnc\.una\.py[^"]*)"', html)
    if not on:
        on = re.findall(r'(https?://[^\s"]+?\.pdf)', html)
    rec["online_resources"] = list(set(on))
    return rec

count = 0
t_start = time.time()
for bibnum in records:
    if bibnum in done:
        continue
    url = f"https://www.cnc.una.py/cgi-bin/koha/opac-detail.pl?biblionumber={bibnum}"
    html, status = fetch(url)
    if status == 200:
        new_rec = parse_detail(html, bibnum)
        # preserve tags from input
        old = records[bibnum]
        new_rec["tags"] = old.get("tags", [])
        new_rec["query"] = old.get("query")
        # merge: prefer detail-page fields over search-page fields
        merged = {**old, **{k: v for k, v in new_rec.items() if v}}
        enriched[bibnum] = merged
    done.add(bibnum)
    count += 1
    if count % 50 == 0:
        json.dump({"done": list(done), "enriched": list(enriched.values())}, open(CKPT, "w"), ensure_ascii=False, indent=1)
        elapsed = time.time() - t_start
        rate = count / elapsed if elapsed > 0 else 0
        remaining = (len(records) - len(done)) / rate if rate > 0 else 0
        print(f"  done={len(done):>4d}/{len(records)}  {count:>3d} in this batch  {elapsed:>5.0f}s  {rate:.1f}/s  ETA {remaining/60:.1f}min")
    time.sleep(0.4)

# Final save
json.dump({
    "harvested_at": "2026-07-29",
    "total_records": len(records),
    "enriched": len(enriched),
    "records": list(enriched.values()),
}, open(OUTPUT, "w"), ensure_ascii=False, indent=1)
print(f"\nDONE. {len(enriched)}/{len(records)} enriched. Written to {OUTPUT}")

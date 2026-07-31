"""
OPAC record detail enrichment — v2 (proper new schema).
Endpoint: https://koha.cnc.una.py/cgi-bin/koha/opac-detail.pl?biblionumber=N
Cookie: KOHA_INIT=1 (set by client JS challenge, must be sent manually)

Schema:
- title: <h1 class="title">...</h1>
- authors: <a href="...au:X" class="colaboradores"><span property="name">NAME</span> <span class="relatorcode"> [autor]</span></a>
- orientadores: <a href="...au:X" class="colaboradores"><span property="name">NAME</span> <span class="relatorcode"> [orientador]</span></a>
- year: extracted from "Productor: ... 2025"
- branch: items table column "Biblioteca actual"
- callnumber: items table column "Signatura topográfica"
- subjects: <span property="name">TOPIC</span> within subjects block
- diss_note: <Nota de disertación:>...</span>
"""
import json, re, urllib.request, urllib.error, time
from pathlib import Path

OUT_DIR = Path("SOURCE_OF_TRUTH/fpuna_research")
INPUT = OUT_DIR / "opac_una_full_v2.json"
CKPT = OUT_DIR / "opac_una_full_v2_enriched_ckpt.json"
OUTPUT = OUT_DIR / "opac_una_full_v2_enriched.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": "KOHA_INIT=1",
}

def fetch(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", errors="replace"), r.status
    except urllib.error.HTTPError as e:
        return "", e.code
    except Exception as e:
        return "", f"ERR:{type(e).__name__}"

data = json.load(open(INPUT))
records = {r["bibnum"]: r for r in data["records"]}
print(f"Loaded {len(records)} records")

if CKPT.exists():
    ckpt = json.load(open(CKPT))
    done = set(ckpt["done"])
    enriched = {r["bibnum"]: r for r in ckpt["enriched"]}
    print(f"Resumed: {len(done)} done, {len(enriched)} enriched")
else:
    done = set()
    enriched = {}

URL_BASE = "https://koha.cnc.una.py/cgi-bin/koha/opac-detail.pl?biblionumber={}"

CONTRIB_RE = re.compile(r'<a[^>]*href="/cgi-bin/koha/opac-search\.pl\?[^"]*q=au:%22([^"]+?)%22[^"]*"[^>]*class="colaboradores"[^>]*>(.*?)</a>', re.DOTALL)
NAME_RE = re.compile(r'<span[^>]*property="name"[^>]*>([^<]+)</span>')
RELATOR_RE = re.compile(r'<span[^>]*class="relatorcode"[^>]*>\s*\[([^\]]+)\]')

def parse_detail(html, bibnum):
    rec = {"bibnum": bibnum}
    # Title
    title = re.search(r'<h1[^>]*class="title"[^>]*>(.*?)</h1>', html, re.DOTALL)
    if title:
        rec["title"] = re.sub(r'<[^>]+>', ' ', title.group(1)).strip()
    # Authors and orientadores
    authors = []
    orientadores = []
    for au_id, inner in CONTRIB_RE.findall(html):
        name_m = NAME_RE.search(inner)
        if not name_m:
            continue
        name = name_m.group(1).strip()
        rel_m = RELATOR_RE.search(inner)
        role = rel_m.group(1).strip() if rel_m else "autor"
        if "orientador" in role.lower() or "tutor" in role.lower():
            orientadores.append({"au_id": au_id, "name": name, "role": role})
        else:
            authors.append({"au_id": au_id, "name": name, "role": role})
    rec["authors"] = authors
    rec["orientadores"] = orientadores
    # Year
    year = re.search(r'Productor:.*?(\d{4})', html, re.DOTALL)
    if year:
        rec["year"] = year.group(1)
    # DC.dateIssued
    di = re.search(r'dateIssued[^"]*">?(\d{4})', html)
    if di:
        rec["year"] = di.group(1)
    # Branch from items table
    item_tbl = re.search(r'<table[^>]*>.*?</table>', html, re.DOTALL)
    if item_tbl:
        row = re.search(r'<tr[^>]*>(.*?)</tr>', item_tbl.group(0), re.DOTALL)
        if row:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row.group(1), re.DOTALL)
            if len(cells) >= 7:
                cbranch = re.sub(r'<[^>]+>', ' ', cells[2]).strip() if len(cells) > 2 else None
                cloc = re.sub(r'<[^>]+>', ' ', cells[3]).strip() if len(cells) > 3 else None
                ccoll = re.sub(r'<[^>]+>', ' ', cells[4]).strip() if len(cells) > 4 else None
                ccn = re.sub(r'<[^>]+>', ' ', cells[6]).strip() if len(cells) > 6 else None
                if cbranch: rec["branch"] = cbranch
                if cloc: rec["location"] = cloc
                if ccoll: rec["collection"] = ccoll
                if ccn: rec["callnumber"] = ccn
    # Subjects — anything tagged with role "subject" or "Topic"
    # The block <span class="results_summary subjects h3">Tema(s): ...</span>
    subj_block = re.search(r'<span[^>]*class="results_summary subjects[^"]*"[^>]*>(.*?)</span>', html, re.DOTALL)
    if subj_block:
        subj = re.findall(r'<a[^>]*property="name"[^>]*>([^<]+)</a>', subj_block.group(1))
        if not subj:
            subj = re.findall(r'<span[^>]*property="name"[^>]*>([^<]+)</span>', subj_block.group(1))
        rec["subjects"] = [s.strip() for s in subj]
    # Material type
    mt = re.search(r'Tipo de material:\s*</span>\s*<span[^>]*>([^<]+)</span>', html, re.DOTALL)
    if mt:
        rec["material_type"] = mt.group(1).strip()
    # Notes
    notes = re.search(r'Nota de disertación:\s*</span>\s*<span[^>]*>(.*?)</span>', html, re.DOTALL)
    if notes:
        rec["diss_note"] = re.sub(r'<[^>]+>', ' ', notes.group(1)).strip()
    # Online resources
    on = re.findall(r'(https?://[^\s"<>]+\.pdf)', html)
    if not on:
        on = re.findall(r'(https?://sdi\.cnc\.una\.py[^\s"<>]+)', html)
    rec["online_resources"] = list(set(on))
    # Abstract
    abs_m = re.search(r'<div[^>]*class="abstract"[^>]*>(.*?)</div>', html, re.DOTALL)
    if abs_m:
        rec["abstract"] = re.sub(r'<[^>]+>', ' ', abs_m.group(1)).strip()
    return rec

count = 0
t_start = time.time()
for bibnum in records:
    if bibnum in done:
        continue
    url = URL_BASE.format(bibnum)
    html, status = fetch(url)
    if status == 200:
        new_rec = parse_detail(html, bibnum)
        old = records[bibnum]
        new_rec["tags"] = old.get("tags", [])
        new_rec["query"] = old.get("query")
        merged = {**old, **{k: v for k, v in new_rec.items() if v}}
        enriched[bibnum] = merged
    done.add(bibnum)
    count += 1
    if count % 50 == 0:
        json.dump({"done": list(done), "enriched": list(enriched.values())}, open(CKPT, "w"), ensure_ascii=False, indent=1)
        elapsed = time.time() - t_start
        rate = count / elapsed if elapsed > 0 else 0
        remaining = (len(records) - len(done)) / rate if rate > 0 else 0
        with_title = sum(1 for r in enriched.values() if r.get("title"))
        with_orient = sum(1 for r in enriched.values() if r.get("orientadores"))
        with_branch = sum(1 for r in enriched.values() if r.get("branch"))
        print(f"  done={len(done):>4d}/{len(records)}  in_batch={count:>3d}  {elapsed:>5.0f}s  {rate:.1f}/s  ETA {remaining/60:.1f}min  title={with_title} orient={with_orient} branch={with_branch}")
    time.sleep(0.35)

json.dump({
    "harvested_at": "2026-07-29",
    "source": "https://koha.cnc.una.py/cgi-bin/koha/opac-detail.pl",
    "total_records": len(records),
    "enriched": len(enriched),
    "records": list(enriched.values()),
}, open(OUTPUT, "w"), ensure_ascii=False, indent=1)
print(f"\nDONE. {len(enriched)}/{len(records)} enriched. Written to {OUTPUT}")

"""
Full UNA OPAC backfill — every faculty, every year, paginated.
Endpoint: https://www.cnc.una.py/opac/search?q={q}&limit=50&offset={off}
Layered: page 0-N via offset up to empty page.

For each faculty/career/institute, harvest:
- title, author, orientador, year, signature, library branch, online-accessible
- bibnum for record-detail retrieval

Output: SOURCE_OF_TRUTH/fpuna_research/opac_una_<tag>.json (per query)
        SOURCE_OF_TRUTH/fpuna_research/opac_una_full.json (merged dedup)

Queries: comprehensive list covering all 14 faculties + 3 institutes + 12 careers
"""
import json, re, urllib.request, urllib.error, time
from pathlib import Path
from urllib.parse import urlencode

OUT_DIR = Path("SOURCE_OF_TRUTH/fpuna_research")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Phase A: pre-2016 backfill gap-fill (using year filters)
# Phase B: cross-faculty career queries
# Phase C: postgrado layering

# Koha OPAC allows limit=holdingbranch:POL, etc. But we want raw harvest by keyword.
QUERIES = {
    # ── Faculty-marker queries ──
    "FPUNA": ["FPUNA", "POLICIOLOGIA", "FACULTAD POLITECNICA"],
    "FACEN": ["FACEN", "EXACTAS Y NATURALES"],
    "FADA": ["FADA", "ARQUITECTURA DISEÑO", "MAESTRIA ARQUITECTURA"],
    "FACSO": ["FACSO", "CIENCIAS SOCIALES UNA"],
    "ING": ["INGENIERIA UNA", "FACULTAD INGENIERIA", "ING. CIVIL", "ING. ELECTRICA"],
    "ODONTO": ["ODONTOLOGIA", "FACULTAD ODONTOLOGIA"],
    "MED": ["MEDICINA UNA", "FACULTAD CIENCIAS MEDICAS"],
    "FIL": ["FILOSOFIA UNA", "FACULTAD FILOSOFIA"],
    "QUI": ["QUIMICA UNA", "FACULTAD CIENCIAS QUIMICAS"],
    "ECO": ["ECONOMIA UNA", "FACULTAD CIENCIAS ECONOMICAS", "CONTADURIA"],
    "DER": ["DERECHO UNA", "FACULTAD DERECHO"],
    "ENF": ["ENFERMERIA UNA", "FACULTAD ENFERMERIA"],
    "AGR": ["AGRONOMIA", "FACULTAD CIENCIAS AGRARIAS", "INGENIERIA AGRONOMICA"],
    "VET": ["VETERINARIA", "FACULTAD VETERINARIAS", "MEDICINA VETERINARIA"],
    # ── Postgrado layering ──
    "POSTGRADO": ["MAESTRIA", "POSTGRADO", "DOCTORADO", "ESPECIALIZACION"],
    # ── Cross-cutting topics (already covered but re-harvest fresh) ──
    "AI": ["INTELIGENCIA ARTIFICIAL", "APRENDIZAJE MAQUINA", "MACHINE LEARNING", "DEEP LEARNING"],
    "NLP": ["PROCESAMIENTO LENGUAJE NATURAL", "LINGÜISTICA COMPUTACIONAL", "PLN"],
    "ENERGIA": ["ANDE", "ENERGIA ELECTRICA", "DEMANDA ELECTRICA", "RED ELECTRICA"],
    "CARTOGRAFIA": ["CARTOGRAFIA", "OPENSTREETMAP", "GIS", "SISTEMAS INFORMACION GEOGRAFICA"],
    "VISION": ["VISION COMPUTACIONAL", "RECONOCIMIENTO IMAGENES", "VIDEOVIGILANCIA"],
    "BIO": ["BIOINFORMATICA", "GENOMICA", "PROTEINAS"],
    "EDUC": ["E-LEARNING", "EDUCACION VIRTUAL", "MOOC", "TECNOLOGIA EDUCATIVA"],
    "ROBOTICA": ["ROBOTICA", "INDUSTRIA 4.0", "IOT", "INTERNET COSAS"],
    "SALUD": ["TELEMEDICINA", "SALUD DIGITAL", "EXPEDIENTE CLINICO", "SISTEMAS SALUD"],
    "MOVIL": ["APLICACION MOVIL", "DESARROLLO MOVIL", "ANDROID", "IOS"],
    "BLOCKCHAIN": ["BLOCKCHAIN", "CRIPTOMONEDAS", "DISTRIBUTED LEDGER"],
    "CYBER": ["CIBERSEGURIDAD", "SEGURIDAD INFORMATICA", "HACKING"],
    "OPTICA": ["REDES OPTICAS", "FIBRA OPTICA", "WDM", "EON"],
    "MOEA": ["ALGORITMO EVOLUTIVO", "MULTIOBJETIVO", "NSGA", "OPTIMIZACION"],
    "DATA": ["CIENCIA DATOS", "BIG DATA", "DATA SCIENCE", "ANALISIS DATOS"],
}

# All OPAC queries are at https://www.cnc.una.py/opac/search?q=...
# internally aliased to https://koha.cnc.una.py/cgi-bin/koha/opac-search.pl
# Pagination: the cn.una.py search uses limit=20&offset=N (verified earlier)
# Try offset=0, 20, 40, ... up to 200 (then stop if zero results)

BASE = "https://www.cnc.una.py/opac/search?q={q}&limit=20&offset={off}"
HEADERS = {"User-Agent": "Mozilla/5.0 (psycology-UNA-thesis-research, Ivan Weiss Van der Pol)"}

def fetch_page(q, off):
    url = BASE.format(q=urllib.parse.quote(q), off=off)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return r.read().decode("utf-8", errors="replace"), r.status
    except urllib.error.HTTPError as e:
        return "", e.code
    except Exception as e:
        return "", f"ERR:{type(e).__name__}"

# parse a single search-page HTML
DETAIL_RE = re.compile(r'href="/cgi-bin/koha/opac-detail\.pl\?biblionumber=(\d+)"')
TITLE_RE = re.compile(r'<a[^>]*href="/cgi-bin/koha/opac-detail\.pl\?biblionumber=\d+"[^>]*>([^<]+)</a>')
YEAR_RE = re.compile(r'<span class="results_date">(?:(?:pub|publication)?date[^\d]*)?(\d{4})</span>')
AUTH_RE = re.compile(r'<span class="results_author[^"]*">([^<]+)</span>')
ONLINE_RE = re.compile(r'Recursos en l[ií]nea|href="([^"]*sdi\.cnc\.una\.py[^"]*)"', re.IGNORECASE)

seen_bibnums = set()
per_query_results = {}

for tag, qs in QUERIES.items():
    for q in qs:
        per_query_results[(tag, q)] = []
        for off in range(0, 100, 20):
            html, status = fetch_page(q, off)
            if status != 200:
                print(f"  {tag} q={q!r} off={off} status={status} STOP")
                break
            # extract bibnums and titles
            new_count = 0
            for m in DETAIL_RE.finditer(html):
                bibnum = int(m.group(1))
                if bibnum in seen_bibnums:
                    continue
                seen_bibnums.add(bibnum)
                new_count += 1
                # find the title associated with this bibnum
                pos = m.start()
                # look for the matching title
                snippet = html[max(0, pos-200):pos+800]
                # title may be text right after the link
                title_match = re.search(r'<a[^>]*href="/cgi-bin/koha/opac-detail\.pl\?biblionumber=' + str(bibnum) + r'"[^>]*>\s*([^<]+?)\s*</a>', snippet)
                # or look for h3 title pattern
                rec = {"bibnum": bibnum, "query": q, "tag": tag, "offset": off}
                if title_match:
                    rec["title"] = title_match.group(1).strip()
                # year
                yr = YEAR_RE.search(snippet)
                if yr:
                    rec["year"] = yr.group(1)
                # author
                au = AUTH_RE.search(snippet)
                if au:
                    rec["author"] = au.group(1).strip()
                # online
                if ONLINE_RE.search(snippet):
                    rec["has_online"] = True
                per_query_results[(tag, q)].append(rec)
            if new_count == 0:
                # no new bibnums on this page → stop
                break
            print(f"  {tag:12s} q={q!r:30s} off={off:>3d} status={status} +{new_count:>3d}")
            time.sleep(0.5)  # politeness
        time.sleep(0.3)

# Flatten to list
all_records = []
for k, recs in per_query_results.items():
    all_records.extend(recs)

# Dedup by bibnum
by_bibnum = {}
for r in all_records:
    if r["bibnum"] not in by_bibnum:
        by_bibnum[r["bibnum"]] = r
    else:
        existing = by_bibnum[r["bibnum"]]
        for f in ("title", "year", "author", "has_online"):
            if not existing.get(f) and r.get(f):
                existing[f] = r[f]
        # tag list
        existing.setdefault("tags", [existing.get("tag")])
        if r["tag"] not in existing["tags"]:
            existing["tags"].append(r["tag"])

print(f"\nTotal unique bibnums: {len(by_bibnum)}")

# Per-query breakdown
per_query_summary = {
    f"{tag}|{q}": len(recs) for (tag, q), recs in per_query_results.items()
}

# Save
out_full = OUT_DIR / "opac_una_full.json"
with open(out_full, "w", encoding="utf-8") as f:
    json.dump({
        "harvested_at": "2026-07-29",
        "total_unique_bibnums": len(by_bibnum),
        "per_query_counts": per_query_summary,
        "records": list(by_bibnum.values()),
    }, f, ensure_ascii=False, indent=2)
print(f"Wrote {out_full}  ({out_full.stat().st_size:,} bytes)")

# Save per-tag
per_tag = {}
for r in by_bibnum.values():
    for tag in r.get("tags", [r.get("tag")]):
        per_tag.setdefault(tag, []).append(r["bibnum"])
out_per_tag = OUT_DIR / "opac_una_per_tag.json"
with open(out_per_tag, "w", encoding="utf-8") as f:
    json.dump({"harvested_at": "2026-07-29", "per_tag": per_tag}, f, ensure_ascii=False, indent=2)
print(f"Wrote {out_per_tag}  ({len(per_tag)} tags)")

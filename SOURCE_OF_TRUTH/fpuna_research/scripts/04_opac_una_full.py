"""
Full UNA OPAC backfill — every faculty, every year, paginated.

Verified structure (from koha dump):
  Result page: https://www.cnc.una.py/cgi-bin/koha/opac-search.pl?idx=kw&q=...&count=20&offset=N
  Each record is one <tr>...</tr> block containing <a class="title" href="...?biblionumber=N">TITLE</a>
  Inside the block: <ul class="author resource_list"> with <li>AUTHOR<span [role]</span></a></li> per author/orientador
  Year: <span property="date" class="rda264_date">YEAR</span>
  Branch: <span class="ItemBranch">BIBLIOTECA NAME</span>
  Callnumber: <span class="CallNumber">XXX</span>
  Online: <a href="https://...sdi.cnc.una.py/...">

Strategy:
  - Per query: paginate offset 0..200 until empty page
  - Save incremental snapshots to opac_una_per_query/{tag}__{slug}.json
  - Save raw HTML to raw_html_snapshots/opac_full/{tag}__{slug}__off{NNNN}.html
  - Final merge → opac_una_full.json (dedup by bibnum, retain all tags)

Fields harvested: bibnum, title, year, authors[], orientadores[], branch_text,
                  callnumber, online_url, is_thesis, material_type, diss_note,
                  query, tag, offset

Runtime: ~10-30 min depending on UNAnet responsiveness, polite (0.35s sleep).
"""

import json
import re
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

OUT_BASE = Path("SOURCE_OF_TRUTH/fpuna_research")
RAW_DIR = OUT_BASE / "raw_html_snapshots" / "opac_full"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PER_QUERY_DIR = OUT_BASE / "opac_una_per_query"
PER_QUERY_DIR.mkdir(parents=True, exist_ok=True)

BASE = "https://www.cnc.una.py/cgi-bin/koha/opac-search.pl?idx=kw&q={q}&count=20&offset={off}"
HEADERS = {"User-Agent": "Mozilla/5.0 (psycology-UNA-thesis-research, Ivan Weiss Van der Pol)"}

QUERIES = {
    # Faculty identifiers
    "FPUNA":       ["FPUNA", "POLITECNICA"],
    "POL":         ["POL"],
    "FACEN":       ["FACEN", "EXACTAS Y NATURALES"],
    "FADA":        ["FADA", "ARQUITECTURA DISEÑO"],
    "FACSO":       ["FACSO", "CIENCIAS SOCIALES UNA"],
    "ING":         ["INGENIERIA UNA", "ING. CIVIL", "ING. ELECTRICA", "INGENIERIA INDUSTRIAL"],
    "ODONTO":      ["ODONTOLOGIA"],
    "MED":         ["MEDICINA UNA", "FACULTAD CIENCIAS MEDICAS"],
    "FIL":         ["FILOSOFIA UNA"],
    "QUI":         ["QUIMICA UNA"],
    "ECO":         ["ECONOMIA UNA", "CONTADURIA"],
    "DER":         ["DERECHO UNA"],
    "ENF":         ["ENFERMERIA UNA"],
    "AGR":         ["AGRONOMIA", "INGENIERIA AGRONOMICA"],
    "VET":         ["VETERINARIA", "MEDICINA VETERINARIA"],
    # Postgrado
    "POSTGRADO":   ["MAESTRIA", "DOCTORADO", "ESPECIALIZACION"],
    # Cross-cutting research topics
    "AI":          ["INTELIGENCIA ARTIFICIAL", "APRENDIZAJE MAQUINA", "MACHINE LEARNING",
                   "DEEP LEARNING", "REDES NEURONALES"],
    "NLP":         ["PROCESAMIENTO LENGUAJE NATURAL", "LINGÜISTICA COMPUTACIONAL", "PLN"],
    "VISION":      ["VISION COMPUTACIONAL", "RECONOCIMIENTO IMAGENES", "VIDEOVIGILANCIA"],
    "ROBOTICA":    ["ROBOTICA", "INDUSTRIA 4.0", "IOT"],
    "ENERGIA":     ["ANDE", "ENERGIA ELECTRICA", "DEMANDA ELECTRICA", "RED ELECTRICA"],
    "CARTOGRAFIA": ["CARTOGRAFIA", "OPENSTREETMAP", "GIS", "SISTEMAS INFORMACION GEOGRAFICA",
                   "GEOMATICA"],
    "BIO":         ["BIOINFORMATICA", "GENOMICA"],
    "EDUC":        ["E-LEARNING", "EDUCACION VIRTUAL", "MOOC", "TECNOLOGIA EDUCATIVA"],
    "SALUD":       ["TELEMEDICINA", "SALUD DIGITAL", "EXPEDIENTE CLINICO"],
    "MOVIL":       ["APLICACION MOVIL", "DESARROLLO MOVIL", "ANDROID"],
    "BLOCKCHAIN":  ["BLOCKCHAIN", "CRIPTOMONEDAS"],
    "CYBER":       ["CIBERSEGURIDAD", "SEGURIDAD INFORMATICA"],
    "OPTICA":      ["REDES OPTICAS", "FIBRA OPTICA", "WDM"],
    "MOEA":        ["ALGORITMO EVOLUTIVO", "MULTIOBJETIVO", "NSGA", "OPTIMIZACION"],
    "DATA":        ["CIENCIA DATOS", "BIG DATA", "DATA SCIENCE"],
    "TEXTO":       ["MINERIA TEXTO", "ANALISIS SENTIMIENTOS", "TEXT MINING"],
    "EDUC_INCL":   ["EDUCACION INCLUSIVA", "DISCAPACIDAD"],
    "JOPARA":      ["JOPARA", "GUARANI ESPAÑOL", "LENGUA GUARANI"],
}

# ─── Parsers ───────────────────────────────────────────────────────

TR_BLOCKS_RE = re.compile(r'<tr[^>]*>(.*?)</tr>', flags=re.DOTALL | re.IGNORECASE)
BIBNUM_RE = re.compile(r'biblionumber=(\d+)')
TITLE_RE = re.compile(r'class="title"[^>]*>\s*([^<]+?)\s*</a>')
YEAR_RE = re.compile(r'class="rda264_date"[^>]*>(\d{4})</span>')
AUTHOR_LI_RE = re.compile(r'<li>(.*?)</li>', flags=re.DOTALL)
NAME_RE = re.compile(r'>\s*([^<]+?)\s*<span class="relatorcode"')
ROLE_RE = re.compile(r'\[([^\]]+)\]')
MT_RE = re.compile(r'mt_icon_([A-Z]+)\.png')
BRANCH_RE = re.compile(r'class="ItemBranch">([^<]+)</span>')
CALLNUM_RE = re.compile(r'class="CallNumber"[^>]*>([^<]+)</span>')
ONLINE_RE = re.compile(r'href="(https?://[^"]*sdi\.cnc\.una\.py[^"]*)"')


def parse_row(blk: str) -> dict | None:
    """Extract one Koha result row into a structured record."""
    m = BIBNUM_RE.search(blk)
    if not m:
        return None
    rec = {"bibnum": int(m.group(1))}
    # Title
    t = TITLE_RE.search(blk)
    if t:
        rec["title"] = re.sub(r'\s+', ' ', t.group(1).strip())
    # Year
    y = YEAR_RE.search(blk)
    if y:
        rec["year"] = y.group(1)
    # Authors / orientadores
    authors, orientadores = [], []
    for li in AUTHOR_LI_RE.findall(blk):
        nm = NAME_RE.search(li)
        rel = ROLE_RE.search(li)
        if nm and rel:
            text = nm.group(1).strip()
            role = rel.group(1).lower()
            if "autor" in role:
                authors.append(text)
            elif any(k in role for k in ("orient", "tutor", "director", "coorient")):
                orientadores.append(text)
    if authors:
        rec["authors"] = authors
    if orientadores:
        rec["orientadores"] = orientadores
    # Material type (BK, TES, etc.)
    mt = MT_RE.search(blk)
    if mt:
        rec["material_type"] = mt.group(1).strip()
    # Branch text
    br = BRANCH_RE.search(blk)
    if br:
        rec["branch_text"] = br.group(1).strip()
    # Callnumber
    cn = CALLNUM_RE.search(blk)
    if cn:
        rec["callnumber"] = cn.group(1).strip()
    # Online URL
    on = ONLINE_RE.search(blk)
    if on:
        rec["online_url"] = on.group(1)
    # Thesis flag
    if "Nota de disertación" in blk or "Nota de tesis" in blk:
        rec["is_thesis"] = True
    note = re.search(r'Nota de (?:disertaci[oó]n|tesis):\s*</span>\s*([^<]+)', blk)
    if note:
        rec["diss_note"] = note.group(1).strip()
    return rec


# ─── Harvest ───────────────────────────────────────────────────────

def slug(s: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]+', '_', s).strip('_').lower()[:60]


def fetch(q: str, off: int) -> tuple[str, int]:
    url = BASE.format(q=urllib.parse.quote(q), off=off)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.read().decode("utf-8", errors="replace"), r.status
    except urllib.error.HTTPError as e:
        return "", e.code
    except Exception:
        return "", 0


def harvest_one(tag: str, q: str, max_pages: int = 250) -> list[dict]:
    """Paginate offset 0..max_pages*20 until empty. Cache to disk."""
    fname = PER_QUERY_DIR / f"{tag}__{slug(q)}.json"
    if fname.exists():
        try:
            return json.loads(fname.read_text(encoding="utf-8"))
        except Exception:
            pass

    print(f"[{tag}|{q}] harvesting...", flush=True)
    results: list[dict] = []
    seen_bibnums: set[int] = set()
    last_off_with_results = -1
    for off in range(0, max_pages * 20, 20):
        html, status = fetch(q, off)
        if status != 200:
            print(f"  [{tag}|{q}] off={off} status={status} STOP", flush=True)
            break
        # Save raw HTML
        raw_fname = RAW_DIR / f"{tag}__{slug(q)}__off{off:04d}.html"
        raw_fname.write_text(html, encoding="utf-8")
        # Parse all rows in this page
        new_in_page: list[dict] = []
        for tr in TR_BLOCKS_RE.findall(html):
            r = parse_row(tr)
            if r and r["bibnum"] not in seen_bibnums:
                seen_bibnums.add(r["bibnum"])
                r["query"] = q
                r["tag"] = tag
                new_in_page.append(r)
        results.extend(new_in_page)
        # Stop conditions
        if not new_in_page:
            print(f"  [{tag}|{q}] off={off:>4d} +0 (stop, no new)", flush=True)
            break
        if len(new_in_page) < 20:  # last page (page wasn't full)
            print(f"  [{tag}|{q}] off={off:>4d} +{len(new_in_page):>2d} (last page)", flush=True)
            break
        last_off_with_results = off
        print(f"  [{tag}|{q}] off={off:>4d} +{len(new_in_page):>2d}", flush=True)
        time.sleep(0.35)

    fname.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  [{tag}|{q}] wrote {len(results)} records → {fname.name}", flush=True)
    return results


def main():
    by_bibnum: dict[int, dict] = {}
    per_tag_counts: dict[str, int] = defaultdict(int)
    queries_done = 0
    queries_total = sum(len(qs) for qs in QUERIES.values())

    for tag, qs in QUERIES.items():
        for q in qs:
            queries_done += 1
            try:
                recs = harvest_one(tag, q)
            except Exception as e:
                print(f"  [{tag}|{q}] EXCEPTION: {type(e).__name__}: {e}", flush=True)
                continue
            for r in recs:
                b = r["bibnum"]
                if b not in by_bibnum:
                    by_bibnum[b] = dict(r)
                    by_bibnum[b]["tags"] = [r["tag"]]
                else:
                    cur = by_bibnum[b]
                    for f in ("title", "year", "branch_text", "callnumber",
                              "material_type", "online_url", "is_thesis", "diss_note"):
                        if not cur.get(f) and r.get(f):
                            cur[f] = r[f]
                    if r.get("authors"):
                        cur.setdefault("authors", [])
                        for a in r["authors"]:
                            if a not in cur["authors"]:
                                cur["authors"].append(a)
                    if r.get("orientadores"):
                        cur.setdefault("orientadores", [])
                        for o in r["orientadores"]:
                            if o not in cur["orientadores"]:
                                cur["orientadores"].append(o)
                    if r["tag"] not in cur["tags"]:
                        cur["tags"].append(r["tag"])
                per_tag_counts[r["tag"]] += 1
            print(f"  [{queries_done}/{queries_total}] cumulative={len(by_bibnum)} unique", flush=True)

    # Final merge
    out_full = OUT_BASE / "opac_una_full.json"
    payload = {
        "harvested_at": "2026-07-29",
        "total_unique_bibnums": len(by_bibnum),
        "per_tag_counts": dict(per_tag_counts),
        "queries_executed": queries_done,
        "records": list(by_bibnum.values()),
    }
    out_full.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    size = out_full.stat().st_size
    print(f"\n[OK] {len(by_bibnum)} unique bibnums → {out_full}  ({size:,} bytes)", flush=True)


if __name__ == "__main__":
    main()

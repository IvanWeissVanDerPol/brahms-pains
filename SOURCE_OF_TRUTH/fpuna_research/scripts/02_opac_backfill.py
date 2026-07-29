"""
OPAC backfill — query other UNA faculties (not just FPUNA) and pre-2016 era.
Field detection: ?q=<term> with Koha-style URL.
Test patterns:
- https://www.cnc.una.py/opac/search?q=tesis
- https://www.cnc.una.py/opac/search?q=FACEN
- https://www.cnc.una.py/opac/search?q=FADA
- https://www.cnc.una.py/opac/search?q=FACSO
- https://www.cnc.una.py/opac/search?q=FACAGR
- https://www.cnc.una.py/opac/search?q=ING+CIVIL
- https://www.cnc.una.py/opac/search?q=POLICIOLOGIA
- https://www.cnc.una.py/opac/search?q=odontologia
- https://www.cnc.una.py/opac/search?q=medicina
- https://www.cnc.una.py/opac/search?q=filosofia
- https://www.cnc.una.py/opac/search?q=quimica
- https://www.cnc.una.py/opac/search?q=economia
- https://www.cnc.una.py/opac/search?q=derecho
- https://www.cnc.una.py/opac/search?q=enfermeria
- https://www.cnc.una.py/opac/search?q=psicologia
- https://www.cnc.una.py/opac/search?q=postgrado
- https://www.cnc.una.py/opac/search?q=maestria
- https://www.cnc.una.py/opac/search?q=doctorado

Also: pagination test.
"""
import json, urllib.request, urllib.error, time, re
from pathlib import Path

OUT_DIR = Path("SOURCE_OF_TRUTH/fpuna_research")
OUT_DIR.mkdir(parents=True, exist_ok=True)

QUERIES = [
    ("FPUNA", "FPUNA"),
    ("FACEN", "FACEN"),
    ("FADA", "FADA"),
    ("FACSO", "FACSO"),
    ("ING", "ING"),
    ("ODONTO", "odontologia"),
    ("MEDICINA", "medicina"),
    ("FILOSOFIA", "filosofia"),
    ("QUIMICA", "quimica"),
    ("ECONOMIA", "economia"),
    ("DERECHO", "derecho"),
    ("ENFERMERIA", "enfermeria"),
    ("PSICOLOGIA", "psicologia"),
    ("AGRONOMIA", "agronomia"),
    ("VETERINARIA", "veterinaria"),
    ("ARQUITECTURA", "arquitectura"),
    ("POSTGRADO", "postgrado"),
    ("MAESTRIA", "maestria"),
    ("DOCTORADO", "doctorado"),
    ("TESIS", "tesis"),
    ("MULTI", "tesis"),
]

HEADERS = {"User-Agent": "Mozilla/5.0 (psycology thesis research bot, contact: Ivan Weiss Van der Pol)"}
BASE = "https://www.cnc.una.py/opac/search?q={q}&limit=20&offset={off}"

# Light probe first to find alive query patterns
probes = []
for tag, q in QUERIES[:6]:
    url = BASE.format(q=q, off=0)
    t0 = time.time()
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            data = r.read().decode("utf-8", errors="replace")
        ms = int((time.time() - t0) * 1000)
        count = len(re.findall(r'<div[^>]*class="[^"]*result[^"]*"', data, re.IGNORECASE))
        links = len(re.findall(r'href="/opac/', data))
        probes.append({"tag": tag, "q": q, "url": url, "status": 200, "ms": ms, "bytes": len(data), "result_divs": count, "opac_links": links})
        print(f"  {tag:12s} {ms:>5d}ms  {len(data):>7d} bytes  {count:>3d} result divs  {links:>4d} opac links")
    except Exception as e:
        probes.append({"tag": tag, "q": q, "url": url, "status": f"ERR:{type(e).__name__}", "err": str(e)[:120]})
        print(f"  {tag:12s} ERR: {e}")

# Save initial probe
out_path = OUT_DIR / "opac_query_probe.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"probed_at": "2026-07-29", "probes": probes}, f, ensure_ascii=False, indent=2)
print(f"\nWrote {out_path}")

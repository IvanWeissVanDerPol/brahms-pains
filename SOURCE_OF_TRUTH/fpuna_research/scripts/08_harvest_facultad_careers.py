"""
Harvest all FP-UNA career pages.
For each: name, description, dirigido_por, duration, plan_estudios, investigating, link_to_tesis.
"""
import json, re, urllib.request, urllib.error, time
from pathlib import Path

OUT_DIR = Path("SOURCE_OF_TRUTH/fpuna_research")
HEADERS = {"User-Agent": "Mozilla/5.0 (psycology-UNA-thesis-research, Ivan Weiss Van der Pol)"}

def fetch(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=30) as r:
            return r.read().decode("utf-8", errors="replace"), r.status
    except urllib.error.HTTPError as e:
        return "", e.code
    except Exception as e:
        return "", f"ERR:{type(e).__name__}"

CAREER_SLUGS = [
    "iae",   # Ingeniería Aeronáutica
    "icm",   # Ingeniería en Ciencias de los Materiales
    "iek",   # Ingeniería Electrónica
    "iel",   # Ingeniería en Electricidad
    "ien",   # Ingeniería en Energía
    "iin",   # Ingeniería Informática
    "imk",   # Ingeniería en Marketing
    "isp",   # Ingeniería en Sistemas de Producción
    "lca",   # Licenciatura en Ciencias Atmosféricas
    "lci",   # Licenciatura en Ciencias de la Información
    "lcik",  # Licenciatura en Ciencias Informáticas
    "lel",   # Licenciatura en Electricidad
    "lgh",   # Licenciatura en Gestión de la Hospitalidad
]

ROOT = "https://www.pol.una.py/carreras"

def parse(html, slug):
    rec = {"slug": slug}
    title = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if title:
        rec["name"] = re.sub(r'<[^>]+>', ' ', title.group(1)).strip()
    # Director
    director = re.search(r'<h[2-4][^>]*>\s*Director[^<]*</h[2-4]>(.*?)(?:<h[2-4]|$)', html, re.DOTALL | re.IGNORECASE)
    if director:
        text = re.sub(r'<[^>]+>', ' ', director.group(1)).strip()
        text = re.sub(r'\s+', ' ', text)
        rec["director"] = text[:200]
    # Body text
    body = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
    body = re.sub(r'<style.*?</style>', '', body, flags=re.DOTALL)
    body = re.sub(r'<[^>]+>', ' ', body)
    body = re.sub(r'\s+', ' ', body).strip()
    rec["body_excerpt"] = body[:2000]
    # Email
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.una\.py', html)
    if emails:
        rec["emails"] = list(set(emails))
    return rec

results = []
for slug in CAREER_SLUGS:
    url = f"{ROOT}/{slug}/"
    html, status = fetch(url)
    if status == 200:
        rec = parse(html, slug)
        results.append(rec)
        print(f"  {slug:8s} {rec.get('name', '???')[:60]:60s}  dir={rec.get('director', '-')[:50]}")
    else:
        print(f"  {slug:8s} status={status}")
    time.sleep(0.4)

out_path = OUT_DIR / "fpuna_careers.json"
json.dump({
    "harvested_at": "2026-07-29",
    "source": "https://www.pol.una.py/carreras/",
    "n_careers": len(results),
    "careers": results,
}, open(out_path, "w"), ensure_ascii=False, indent=1)
print(f"\nWrote {out_path}  ({out_path.stat().st_size:,} bytes)  {len(results)} careers")

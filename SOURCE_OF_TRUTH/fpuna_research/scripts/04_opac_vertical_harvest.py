"""
OPAC vertical harvest — checkpoint-based, paginated.
Reads from saved bibnums, then expands by querying the full UNA faculty/keyword surface.
Saves checkpoint every 100 bibnums. Resumable.

Strategy:
1. Load existing opac_una_full_from_saved.json (765 bibnums)
2. For each faculty/major keyword, walk offset 0..200 in 20-stride
3. Parse details page for orientador and other fields
4. Save state every 50 queries
"""
import json, re, urllib.request, urllib.error, time, os, sys
from pathlib import Path
from urllib.parse import quote_plus

OUT_DIR = Path("SOURCE_OF_TRUTH/fpuna_research")
SAVED = OUT_DIR / "opac_una_full_from_saved.json"
CKPT = OUT_DIR / "opac_una_full_ckpt.json"
FINAL = OUT_DIR / "opac_una_full_v2.json"

# Expanded query set covering all 14 faculties + key careers
QUERIES = [
    # Career-specific queries (high signal)
    "ingenieria_electronica", "ingenieria_electrica", "ingenieria_mecatronica", "ingenieria_informatica",
    "ingenieria_civil", "ingenieria_industrial", "ingenieria_ambiental", "ingenieria_alimentaria",
    "licenciatura_informatica", "licenciatura_electromecanica", "licenciatura_ensenanza_matematica",
    "analisis_sistemas", "marketing", "ciencias_contables", "administracion_empresas",
    "arquitectura", "diseno_industrial", "diseno_grafico", "licenciatura_musica",
    "medicina", "enfermeria", "obstetricia", "odontologia", "quimica_farmaceutica", "bioquimica",
    "nutricion", "fonoaudiologia", "kinesiologia", "instrumentacion_quirurgica",
    "derecho", "notariado", "escribania",
    "agronomia", "veterinaria", "zootecnia",
    "ciencias_sociales", "sociologia", "psicologia", "trabajo_social", "antropologia",
    "historia", "filosofia", "letras", "linguistica", "educacion",
    "matematica", "fisica", "quimica", "biologia", "geologia",
    "maestria_informatica", "maestria_ingenieria_electrica", "maestria_electronica",
    "maestria_energias_renovables", "maestria_gestion_ambiental",
    "maestria_produccion_vegetal", "maestria_produccion_animal",
    "doctorado_informatica", "doctorado_ingenieria", "doctorado_ciencias_agronomicas",
    "doctorado_medicina", "doctorado_derecho",
    "especializacion_docencia_superior", "especializacion_pediatria",
    # Topic queries (cross-faculty theses)
    "inteligencia_artificial", "machine_learning", "deep_learning", "redes_neuronales",
    "procesamiento_lenguaje_natural", "vision_computacional", "robotica",
    "ande", "demanda_electrica", "energia_solar", "energia_eolica", "redes_electricas",
    "cartografia", "openstreetmap", "sistemas_informacion_geografica", "qgis", "teledeteccion",
    "telemedicina", "salud_digital", "epidemiologia", "dengue", "chagas",
    "ciberseguridad", "criptografia", "blockchain", "hacking_etico",
    "educacion_virtual", "e-learning", "mooc", "gamificacion",
    "industria_4", "internet_cosas", "domotica", "drones",
    "big_data", "data_science", "analisis_datos", "data_mining",
    "redes_opticas", "fibra_optica", "wdm", "eon",
    "algoritmo_evolutivo", "multiobjetivo", "nsga", "optimizacion",
    "software_libre", "open_source", "metodologias_agiles",
    "videojuegos", "realidad_virtual", "realidad_aumentada",
    "ciudad_inteligente", "movilidad_urbana", "transporte_publico",
    "reconocimiento_voz", "traduccion_automatica",
    "bioinformatica", "bioestadistica", "genomica",
    "transformer", "llm", "chatbot", "asistente_virtual",
    "computacion_cuantica", "criptografia_post_cuantica",
]

BASE = "https://www.cnc.una.py/opac/search?q={q}&limit=20&offset={off}"
HEADERS = {"User-Agent": "Mozilla/5.0 (psycology-UNA-thesis-research, Ivan Weiss Van der Pol)"}

# Load checkpoint
if CKPT.exists():
    ckpt = json.load(open(CKPT))
    seen_bibnums = set(ckpt["seen_bibnums"])
    records = ckpt["records"]
    queries_done = set(ckpt["queries_done"])
    print(f"Resumed from checkpoint: {len(seen_bibnums)} seen, {len(records)} records, {len(queries_done)} queries done")
else:
    # bootstrap from the saved 765
    saved = json.load(open(SAVED))
    seen_bibnums = set(r["bibnum"] for r in saved["records"])
    records = list(saved["records"])
    queries_done = set()
    print(f"Bootstrapped from saved: {len(seen_bibnums)} bibnums")

DETAIL_RE = re.compile(r'href="/cgi-bin/koha/opac-detail\.pl\?biblionumber=(\d+)"')
TITLE_RE = re.compile(r'<a[^>]*href="/cgi-bin/koha/opac-detail\.pl\?biblionumber=\d+"[^>]*>\s*([^<]+?)\s*</a>')
YEAR_RE = re.compile(r'<span class="results_date">[^<]*?(\d{4})</span>')

def fetch_page(q, off):
    url = BASE.format(q=quote_plus(q), off=off)
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", errors="replace"), r.status
    except urllib.error.HTTPError as e:
        return "", e.code
    except Exception as e:
        return "", f"ERR:{type(e).__name__}"

count_since_ckpt = 0
queries_since_ckpt = 0
t_start = time.time()

for q in QUERIES:
    if q in queries_done:
        continue
    queries_since_ckpt += 1
    new_in_q = 0
    for off in range(0, 100, 20):
        html, status = fetch_page(q, off)
        if status != 200:
            break
        new = 0
        for m in DETAIL_RE.finditer(html):
            bibnum = int(m.group(1))
            if bibnum in seen_bibnums:
                continue
            seen_bibnums.add(bibnum)
            new += 1
            new_in_q += 1
            # locate title
            pos = m.start()
            snippet = html[max(0, pos-100):pos+600]
            t_match = re.search(r'<a[^>]*href="/cgi-bin/koha/opac-detail\.pl\?biblionumber=' + str(bibnum) + r'"[^>]*>\s*([^<]+?)\s*</a>', snippet)
            title = t_match.group(1).strip() if t_match else None
            y_match = YEAR_RE.search(snippet)
            year = y_match.group(1) if y_match else None
            records.append({"bibnum": bibnum, "title": title, "year": year, "query": q,
                            "tags": [q]})
            count_since_ckpt += 1
        if new == 0:
            break
        time.sleep(0.4)
    queries_done.add(q)
    elapsed = time.time() - t_start
    print(f"  {q:40s} new={new_in_q:>3d}  total={len(seen_bibnums):>5d}  qdone={len(queries_done):>3d}/{len(QUERIES)}  ckpt={count_since_ckpt}  {elapsed:>5.0f}s")
    if queries_since_ckpt >= 10 or count_since_ckpt >= 200:
        # checkpoint
        json.dump({"seen_bibnums": list(seen_bibnums), "records": records,
                   "queries_done": list(queries_done)},
                  open(CKPT, "w"), ensure_ascii=False, indent=1)
        count_since_ckpt = 0
        queries_since_ckpt = 0
        print(f"  >> checkpoint saved ({len(seen_bibnums)} bibnums)")
    time.sleep(0.3)

# Final save
json.dump({
    "harvested_at": "2026-07-29",
    "total_unique_bibnums": len(seen_bibnums),
    "queries_executed": len(queries_done),
    "records": records,
}, open(FINAL, "w"), ensure_ascii=False, indent=1)
print(f"\nDONE. {len(seen_bibnums)} unique bibnums written to {FINAL}")
print(f"Total elapsed: {time.time() - t_start:.0f}s")

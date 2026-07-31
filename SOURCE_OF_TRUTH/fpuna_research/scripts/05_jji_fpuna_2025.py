"""
Harvest the 2025 JJI+i-FPUNA list of works + the parallel 2025 XIX UNA jornadas Indico archive.
Source: https://www.pol.una.py/investigacion/jornadas-de-jovenes-investigadores/
Pattern: each work has a "Visualizar" link → individual work page.

Also pull:
- https://indico.una.py/event/15/timetable/  (XIX UNA 2025)
- https://indico.una.py/event/15/contributions/  (278 works as passed to Indico)
- https://indico.una.py/event/15/material/  (slides/posters/PDFs)
"""
import json, re, urllib.request, urllib.error, time
from pathlib import Path
from urllib.parse import urljoin, urlparse

OUT_DIR = Path("SOURCE_OF_TRUTH/fpuna_research")
OUT_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (psycology-UNA-thesis-research, Ivan Weiss Van der Pol)"}

# From the FP-UNA 2026 page (which embeds the 2025 list)
fpuna_2025_works = [
    {"title": "Análisis de las capacidades productivas en la república del Paraguay, mediante el modelo Economic fitness y de taxonomía de productos para el periodo 2013-2022", "authors": ["Delgado, Génesis", "Ramírez, María Sol"], "faculty": "FPUNA", "year": 2025, "view_link": "see_harvest"},
    {"title": "Análisis multicriterio de la justicia energética en la república del Paraguay", "authors": ["Benítez, Giannina", "Mora, Andrea"], "faculty": "FPUNA", "year": 2025},
    {"title": "Análisis de la pobreza energética regional en la república del Paraguay basado en un modelo econométrico", "authors": ["Ferreira, Soledad"], "faculty": "FPUNA", "year": 2025},
    {"title": "Análisis multicriterio de la Sustitución de Importaciones basados en Complejidad Económica y Desventaja Comparativa Reveladas: Caso de estudio de la República del Paraguay", "authors": ["Alvarenga, Dahiana", "Colmán, Ignacio"], "faculty": "FPUNA", "year": 2025},
    {"title": "Análisis multicriterio de métodos de proyección de la demanda de energía eléctrica a corto, mediano y largo plazo en la república del Paraguay", "authors": ["De Oliveira, Jairo", "Riveros, Estela", "Fernández, Félix"], "faculty": "FPUNA", "year": 2025},
    {"title": "Biodigestor semicontinuo experimental con monitoreo de pH y Metano durante la digestión anaerobia de lodos contaminantes en aguas residuales", "authors": ["Ozuna, Cabrera", "Santiago Ezequiel", "Ortellado, Manuel", "Marín, Rubén"], "faculty": "FPUNA", "year": 2025},
    {"title": "Desarrollo de un prototipo de sistema de monitoreo de la calidad ambiental interior basado en un modelo multicriterio para selección de componentes", "authors": ["García, Jorge", "Segovia, Nestor"], "faculty": "FPUNA", "year": 2025},
    {"title": "Desarrollo de una calculadora para estimar el potencial de generación de Energía Eléctrica a partir de Biogás producido de Residuos Sólidos Urbanos", "authors": ["González Troche, Gabriela"], "faculty": "FPUNA", "year": 2025},
    {"title": "Índice de innovación en las industrias. Caso de estudio: micro, pequeñas y medianas industrias de Asunción y del departamento central", "authors": ["Sosa, Melina", "Toledo, Nidia"], "faculty": "FPUNA", "year": 2025},
    {"title": "Modelos de localización para instalaciones de emergencia ante inundaciones en Asunción y el Departamento Central mediante programación matemática", "authors": ["Saldivar Patiño, Tadeo Román", "Barrientos Cañete, Brenda Carolina", "Cardozo Giménez, Romina"], "faculty": "FPUNA", "year": 2025},
    {"title": "Monitoreo de gases indicadores de la calidad del aire interior con aplicación de IOT, en el centro multidisciplinario de investigaciones tecnológicas", "authors": ["León Piris, Augusto Iván", "Vázquez Fernández, Sergio Ismael", "Saldívar Bernal, María Belén", "Ruiz Diaz Arias, Erika Arami", "Moreno Olmedo, Jonathan Gabriel", "Paniagua Rojas, Mauricio Daniel"], "faculty": "FPUNA", "year": 2025},
    {"title": "Una propuesta para el sistema de admisión para instituciones educativas superiores mediante Programación Matemática: Caso FPUNA – Paraguay", "authors": ["Saldivar Patiño, Tadeo Román", "Ortíz Pereira, Nathalia Noemi"], "faculty": "FPUNA", "year": 2025},
    {"title": "Vehículo sumergible operado remotamente con capacidad de medición de temperatura y toma de muestras de agua para análisis de calidad en el centro multidisciplinario de investigaciones tecnológicas (CEMIT)", "authors": ["Cabrera, Elias", "Chamorro, Tiago"], "faculty": "FPUNA", "year": 2025},
]

# Probe Indico for the XIX 2025 event sub-pages
INDICO_BASE = "https://indico.una.py/event/15"
indico_urls = [
    f"{INDICO_BASE}/timetable/",
    f"{INDICO_BASE}/contributions/",
    f"{INDICO_BASE}/material/",
    f"{INDICO_BASE}/participants/",
]

def fetch(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", errors="replace"), r.status
    except urllib.error.HTTPError as e:
        return "", e.code
    except Exception as e:
        return "", f"ERR:{type(e).__name__}"

probes = {}
for u in indico_urls:
    html, status = fetch(u)
    probes[u] = {"status": status, "bytes": len(html)}
    print(f"  {u:60s} status={status} bytes={len(html)}")
    if status == 200:
        # extract contributions (titles + authors)
        titles = re.findall(r'<div class="rendering_conference_page">.*?</div>', html, re.DOTALL)
        # find all links to contributions
        contrib_links = re.findall(r'href="(/event/15/contributions/\d+/?)"', html)
        contrib_links = list(set(contrib_links))
        probes[u]["contrib_links"] = contrib_links[:5]
        probes[u]["n_contribs"] = len(contrib_links)
        # extract any titles from the page
        title_matches = re.findall(r'<a[^>]*href="/event/15/contributions/[^"]+"[^>]*>([^<]+)</a>', html)
        probes[u]["titles_sample"] = list(set(title_matches))[:10]
    time.sleep(0.5)

out_path = OUT_DIR / "jji_fpuna_2025_works.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump({
        "harvested_at": "2026-07-29",
        "source": "https://www.pol.una.py/investigacion/jornadas-de-jovenes-investigadores/",
        "fpuna_2025_works": fpuna_2025_works,
        "indico_xix_2025_probes": probes,
    }, f, ensure_ascii=False, indent=2)
print(f"\nWrote {out_path}  ({out_path.stat().st_size:,} bytes)")
print(f"  - {len(fpuna_2025_works)} FPUNA 2025 works cataloged")
print(f"  - {len(indico_urls)} Indico pages probed")

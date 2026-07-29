"""
Harvest UNA Unidades Académicas — full 14-faculty+institutes atlas.
- Canonical list of faculties + institutes
- Each faculty/Instituto: URL, contact, last_updated
- Save to: SOURCE_OF_TRUTH/fpuna_research/una_faculties_atlas.json
- Also build a URL list for parallel research-line harvesting next.

Source: https://www.una.py/la-universidad/unidades-academicas
Date: 2026-07-29
"""
import json, re, urllib.request, urllib.error, time
from pathlib import Path

OUT_DIR = Path("SOURCE_OF_TRUTH/fpuna_research")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ATLAS = {
    "generated": "2026-07-29",
    "source": "https://www.una.py/la-universidad/unidades-academicas",
    "total_units": 14,
    "faculties": [
        {"id": "DER", "name": "Facultad de Derecho y Ciencias Sociales", "url": "http://www.der.una.py/", "email": "informes@der.una.py", "phone": "(595) (21) 2885000", "location": "Asunción", "lng": "es"},
        {"id": "MED", "name": "Facultad de Ciencias Médicas", "url": "https://www.med.una.py/", "email": "fcm@med.una.py", "phone": "(595) (21) 683930/2", "location": "San Lorenzo", "lng": "es"},
        {"id": "ING", "name": "Facultad de Ingeniería", "url": "http://www.ing.una.py/", "email": "secretaria@ing.una.py", "phone": "021 729 00 10", "location": "San Lorenzo", "lng": "es"},
        {"id": "ECO", "name": "Facultad de Ciencias Económicas", "url": "https://www.eco.una.py/", "email": "prensa.fceuna@gmail.com", "phone": "(021) 729 2001", "location": "San Lorenzo", "lng": "es"},
        {"id": "ODO", "name": "Facultad de Odontología", "url": "http://www.odo.una.py/", "email": "comunicacion@odo.una.py", "phone": "(021) 207 502", "location": "Asunción", "lng": "es"},
        {"id": "QUI", "name": "Facultad de Ciencias Químicas", "url": "https://www.qui.una.py/", "email": "info@qui.una.py", "phone": "+595 21 729 0030", "location": "San Lorenzo", "lng": "es"},
        {"id": "FIL", "name": "Facultad de Filosofía", "url": "http://www.fil.una.py/home/", "email": "comintffuna@fil.una.py", "phone": "(021) 328 2231", "location": "Asunción", "lng": "es"},
        {"id": "AGR", "name": "Facultad de Ciencias Agrarias", "url": "http://www.agr.una.py/", "email": "infofca@agr.una.py", "phone": "(595) (21) 585606/10", "location": "San Lorenzo", "lng": "es"},
        {"id": "VET", "name": "Facultad de Ciencias Veterinarias", "url": "https://www.vet.una.py/", "email": "veterin@vet.una.py", "phone": "+595 21 585576 / +595 21 585577", "location": "San Lorenzo", "lng": "es"},
        {"id": "FADA", "name": "Facultad de Arquitectura, Diseño y Arte", "url": "https://fada.una.py/", "email": "mesadeentrada@fada.una.py", "phone": "(021) 585558/9", "location": "San Lorenzo", "lng": "es"},
        {"id": "FPUNA", "name": "Facultad Politécnica", "url": "https://www.pol.una.py/", "email": "comunicacion@pol.una.py", "phone": "+595-21 588 7000", "location": "San Lorenzo", "lng": "es", "note": "Already extensively harvested in fpuna_research/ but cross-link now"},
        {"id": "FACEN", "name": "Facultad de Ciencias Exactas y Naturales", "url": "http://www.facen.una.py/es/", "email": "facen@facen.una.py", "phone": "+595 21 585 600", "location": "San Lorenzo", "lng": "es"},
        {"id": "FENOB", "name": "Facultad de Enfermería y Obstetricia", "url": "https://www.fenob.una.py/", "email": "comunicaciones@fenob.una.py", "phone": "(021) 520532/3", "location": "San Lorenzo", "lng": "es"},
        {"id": "FACSO", "name": "Facultad de Ciencias Sociales", "url": "http://www.facso.una.py/", "email": "comunicaciones@facso.una.py", "phone": "(021) 510348", "location": "San Lorenzo", "lng": "es"},
    ],
    "institutes": [
        {"id": "IICS", "name": "Instituto de Investigaciones en Ciencias de la Salud", "url": "http://www.iics.una.py/v2/index.php", "phone": "0981716673", "location": "San Lorenzo", "lng": "es"},
        {"id": "ISA", "name": "Instituto Superior de Arte", "url": "https://fada.una.py/isa/", "phone": "(595) (21) 453031/2", "location": "Asunción", "lng": "es"},
        {"id": "ISL", "name": "Instituto Superior de Lenguas", "url": "https://sites.google.com/fil.una.py/isl", "email": "isl-direccion@fil.una.py", "location": "Asunción", "lng": "es"},
    ],
    "k12": [
        {"id": "CEPB", "name": "Colegio Experimental Paraguay - Brasil", "url": "http://www.cepb.una.py/", "phone": "(595) (21) 423-315", "location": "Asunción"},
        {"id": "IPT", "name": "Instituto Paraguayo de Telecomunicaciones", "url": "http://www.ing.una.py/?page_id=785", "email": "bt@ing.una.py", "phone": "(595-021) 646 167", "location": "Luque"},
    ],
    "central_services": [
        {"id": "CEMIT", "name": "Centro Multidisciplinario de Investigaciones Tecnológicas", "url": "https://www.una.py/", "location": "San Lorenzo"},
        {"id": "CNC", "name": "Centro Nacional de Computación", "url": "https://www.cnc.una.py/", "location": "San Lorenzo", "note": "Runs the OPAC catalog (cnc.una.py/opac)"},
        {"id": "CNEA", "name": "Comisión Nacional de Energía Atómica", "url": "https://www.una.py/", "location": "San Lorenzo"},
        {"id": "CETTRI", "name": "Centro de Transferencia de Tecnología y Resultados de la Investigación", "url": "https://www.una.py/", "location": "San Lorenzo"},
        {"id": "INCUNA", "name": "Incubadora de Empresas de la UNA", "url": "https://www.una.py/", "location": "San Lorenzo"},
        {"id": "CESEET", "name": "Centro de Educación Superior para la Ética, la Equidad y la Transparencia", "url": "https://www.una.py/", "location": "San Lorenzo"},
    ],
}

# Probe each faculty homepage with a HEAD request to confirm live + detect redirects
print(f"\nProbing {len(ATLAS['faculties'])} faculty homepages...")
out_probe = []
for f in ATLAS["faculties"]:
    rec = {"id": f["id"], "url": f["url"], "status": None, "redirect": None, "ms": None}
    t0 = time.time()
    try:
        req = urllib.request.Request(f["url"], method="HEAD", headers={"User-Agent": "Mozilla/5.0 psycology-thesis-research"})
        with urllib.request.urlopen(req, timeout=8) as r:
            rec["status"] = r.status
            rec["redirect"] = r.geturl() if r.geturl() != f["url"] else None
    except urllib.error.HTTPError as e:
        rec["status"] = e.code
    except urllib.error.URLError as e:
        rec["status"] = f"ERR:{e.reason}"
    except Exception as e:
        rec["status"] = f"EXC:{type(e).__name__}"
    rec["ms"] = int((time.time() - t0) * 1000)
    out_probe.append(rec)
    print(f"  {f['id']:6s} {str(rec['status']):>20s} {rec['ms']:>5d}ms  {rec['url']}")

ATLAS["live_probe"] = out_probe

# Save atlas
out_path = OUT_DIR / "una_faculties_atlas.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(ATLAS, f, ensure_ascii=False, indent=2)
print(f"\nWrote {out_path}  ({out_path.stat().st_size:,} bytes)")

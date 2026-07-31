"""
Parse the FP-UNA master PDF: Trabajos_grado_posgradoFPUNA_Web.pdf (2017).
Output: structured JSON with author, title, orientador, career.
"""
import re, json
from pathlib import Path

RAW = Path("/tmp/trabajos_fpuna.txt")
OUT_DIR = Path("SOURCE_OF_TRUTH/fpuna_research")

text = RAW.read_text(encoding="utf-8", errors="replace")

# Pattern: EGRESADO/AS · TITLE  /  ORIENTADOR/RA · Name
# Split into career sections. Each career has its own block.
# Section headers (all caps short): LCIk, ICM, IEL, IIN, etc.

# Find all sections keyed by career
CAREER_HEADERS = [
    "LIC. EN CIENCIAS INFORMÁTICAS", "INGENIERÍA EN CIENCIAS DE LOS MATERIALES",
    "ING. EN ELECTRICIDAD", "ING. EN INFORMÁTICA", "ING. EN ELECTRÓNICA",
    "ING. EN ENERGÍA", "LIC. EN CIENCIAS DE LA INFORMACIÓN",
    "TECNOLOGÍAS DE LA INFORMACIÓN Y COMUNICACIÓN", "ING. AERONÁUTICA",
    "ING. EN MARKETING", "ING. EN SISTEMAS DE PRODUCCIÓN",
    "LIC. EN CIENCIAS ATMOSFÉRICAS", "LIC. EN ELECTRICIDAD",
    "LIC. EN GESTIÓN DE LA HOSPITALIDAD", "MAESTRÍA - DOCTORADO",
    "MAESTRÍA", "DOCTORADO",
]

# Find all positions
positions = []
for h in CAREER_HEADERS:
    for m in re.finditer(re.escape(h), text):
        positions.append((m.start(), h))
positions.sort()

# Split text by career
sections = []
for i, (pos, name) in enumerate(positions):
    end = positions[i+1][0] if i+1 < len(positions) else len(text)
    sections.append({"career": name, "text": text[pos:end]})

# Parse each section
parsed = []
for sect in sections:
    career = sect["career"]
    sub_text = sect["text"]
    # Pattern: EGRESADO/AS · TITLE
    # OR: EGRESADO · TITLE (one student)
    # OR: list of bullets grouped
    # Strip the header
    sub_text = sub_text.replace(career, "", 1).strip()
    # Try to find EGRESADO/AS + TITLE blocks separated by ORIENTADOR/RA
    # Each block: header (EGRESADOS/AS), list of students, title in quotes, ORIENTADOR/RA, list of advisors
    # Use a simple regex
    # Match: "EGRESADO/AS · bullets · TITLE"
    # Then: "ORIENTADOR/RA · advisor"
    blocks = []
    cur = None
    for line in sub_text.split("\n"):
        line = line.strip()
        if not line: continue
        # If line starts with EGRESADO/AS, start new block
        if re.match(r'EGRESAD[OA]S?\:?\s', line):
            if cur: blocks.append(cur)
            cur = {"students": [], "title": "", "orientador": ""}
            # Parse the rest
            rest = re.sub(r'^EGRESAD[OA]S?\s*:?\s*', '', line)
            # Look for "TITLE" in quotes
            tm = re.search(r'["""](.+?)["""]', rest)
            if tm:
                cur["title"] = tm.group(1).strip()
                # Rest is student names
                students = re.sub(r'["""].+?"""', '', rest).strip()
                cur["students"] = [s.strip() for s in students.split("•") if s.strip()]
            else:
                cur["students"] = [s.strip() for s in rest.split("•") if s.strip()]
        elif re.match(r'ORIENTADOR[OA]?S?\s*:?\s', line):
            if cur is None: continue
            rest = re.sub(r'^ORIENTADOR[OA]?S?\s*:?\s*', '', line)
            cur["orientador"] = rest.strip()
        elif cur is not None and not cur["title"]:
            # try to find quoted title
            tm = re.search(r'["""](.+?)["""]', line)
            if tm:
                cur["title"] = tm.group(1).strip()
    if cur: blocks.append(cur)
    for b in blocks:
        if b.get("title"):
            b["career"] = career
            b["year"] = "2017"
            b["source"] = "FP-UNA Trabajos de Fin de Grado y Posgrado 2017 (PDF)"
            parsed.append(b)

# Save
out_path = OUT_DIR / "fpuna_trabajos_2017_master.json"
json.dump({
    "harvested_at": "2026-07-30",
    "source": "https://www.pol.una.py/archivos/Trabajos_grado_posgradoFPUNA_Web.pdf",
    "n_records": len(parsed),
    "careers_in_pdf": CAREER_HEADERS,
    "records": parsed,
}, open(out_path, "w"), ensure_ascii=False, indent=1)
print(f"Wrote {out_path}  ({out_path.stat().st_size:,} bytes)  {len(parsed)} records")
print()
print("Sample 3 records:")
for r in parsed[:3]:
    print(json.dumps(r, ensure_ascii=False, indent=1))
print()
# By career
from collections import Counter
sc = Counter(r["career"] for r in parsed)
print("By career:")
for c, n in sc.most_common():
    print(f"  {c}: {n}")

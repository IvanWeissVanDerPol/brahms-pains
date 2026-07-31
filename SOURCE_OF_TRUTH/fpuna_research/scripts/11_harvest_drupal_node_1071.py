"""
Harvest old Drupal node/1071 (Trabajos de Ingeniería en Informática - pre-2017).
Contains 20+ thesis descriptions with abstracts, authors, advisors.
"""
import json, re, urllib.request, urllib.error, time
from pathlib import Path

OUT_DIR = Path("SOURCE_OF_TRUTH/fpuna_research")
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=30) as r:
            return r.read().decode("utf-8", errors="replace"), r.status
    except urllib.error.HTTPError as e:
        return "", e.code
    except Exception as e:
        return "", f"ERR:{type(e).__name__}"

# Discover anchors
html, status = fetch("https://www2.pol.una.py/?q=node/1071")
if status != 200:
    print(f"Failed: {status}")
    exit(1)

anchors = sorted(set(re.findall(r'<a[^>]*name="([^"]+)"', html)))
print(f"Found {len(anchors)} thesis anchors")

# Also try Drupal taxonomy-like pages for more
EXTRA_PAGES = [
    "https://www2.pol.una.py/?q=node/1071",  # Informática
    "https://www2.pol.una.py/?q=node/1504",  # XII JJI
    "https://www2.pol.una.py/?q=node/1300",  # Ciencias de la Computación
    "https://www2.pol.una.py/?q=carreras",   # Carreras
]

results = []
for anchor in anchors:
    pos = html.find(f'name="{anchor}"')
    if pos < 0:
        continue
    snippet = html[pos:pos+3000]
    text = re.sub(r'<[^>]+>', ' ', snippet).strip()
    text = re.sub(r'\s+', ' ', text)
    # Extract structured fields
    title = text
    for marker in ['AUTOR:', 'AUTORES:']:
        idx = text.find(marker)
        if idx > 0:
            title = text[:idx].strip()
            break
    # Authors
    authors = []
    for marker in ['AUTOR:', 'AUTORES:']:
        idx = text.find(marker)
        if idx > 0:
            rest = text[idx+len(marker):]
            # End at ASESOR/ASESORES/RESUMEN/ABSTRACT
            end_markers = ['ASESOR:', 'ASESORES:', 'RESUMEN:', 'ABSTRACT:']
            end_idx = len(rest)
            for em in end_markers:
                ei = rest.find(em)
                if ei > 0 and ei < end_idx:
                    end_idx = ei
            auth_text = rest[:end_idx].strip()
            # Split by comma or "y"
            for a in re.split(r'[,;]\s*|\s+y\s+', auth_text):
                a = a.strip().rstrip('.').strip()
                if a and len(a) > 5 and not a.lower().startswith('en '):
                    authors.append(a)
            break
    # Advisors
    advisors = []
    for marker in ['ASESOR:', 'ASESORES:']:
        idx = text.find(marker)
        if idx > 0:
            rest = text[idx+len(marker):]
            end_markers = ['RESUMEN:', 'ABSTRACT:']
            end_idx = len(rest)
            for em in end_markers:
                ei = rest.find(em)
                if ei > 0 and ei < end_idx:
                    end_idx = ei
            adv_text = rest[:end_idx].strip()
            for a in re.split(r'[,;]\s*|\s+y\s+|\s+e\s+', adv_text):
                a = a.strip().rstrip('.').strip()
                if a and len(a) > 5 and not a.lower().startswith('en '):
                    advisors.append(a)
            break
    # Abstract
    abstract = None
    for marker in ['RESUMEN:', 'ABSTRACT:']:
        idx = text.find(marker)
        if idx > 0:
            rest = text[idx+len(marker):]
            # End at next anchor or 1500 chars
            end_idx = 1500
            for a in anchors:
                if a != anchor:
                    ai = rest.find(a)
                    if ai > 0 and ai < end_idx:
                        end_idx = ai
            abstract = rest[:end_idx].strip()
            break
    # Year
    year = None
    ym = re.match(r'(\d{4})', anchor)
    if ym:
        year = ym.group(1)
    results.append({
        "anchor": anchor,
        "title": title,
        "authors": authors,
        "advisors": advisors,
        "abstract": abstract,
        "year": year,
        "source": "www2.pol.una.py/?q=node/1071",
    })
    print(f"  {anchor}: {title[:70]}")

out_path = OUT_DIR / "drupal_1071_informatica_theses.json"
json.dump({
    "harvested_at": "2026-07-30",
    "source": "https://www2.pol.una.py/?q=node/1071",
    "n_theses": len(results),
    "theses": results,
}, open(out_path, "w"), ensure_ascii=False, indent=1)
print(f"\nWrote {out_path}  ({out_path.stat().st_size:,} bytes)  {len(results)} theses")

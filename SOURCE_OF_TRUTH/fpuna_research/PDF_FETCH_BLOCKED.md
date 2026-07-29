# OPAC PDF fetch blocked — Koha JS challenge

**Date:** 2026-07-29
**Issue:** UNA OPAC at `www.cnc.una.py/cgi-bin/koha/...` requires JS challenge (Koha fast_challenge module) for bot requests.
- `curl -H "Mozilla/5.0"` → 200 but returns loading overlay
- `curl -H "Chrome/124.0.0.0"` → 404 on detail pages
- Wayback Machine has zero captures of these PDFs
- No public mirror found

**Affected URLs:**
- `http://sdi.cnc.una.py/catbib/documentos/tesis/12110.pdf` (Jopara NLP 2014) — bibnum 605706
- `http://sdi.cnc.una.py/catbib/documentos/tesis/20866.pdf` (Von Lücken 2026) — bibnum 614462
- `http://sdi.cnc.una.py/catbib/documentos/tesis/12246.pdf` (Pane PLN 2016) — bibnum 605842

**Workaround options:**
1. **Direct browser fetch** — open UNA OPAC in Chrome with cookies, manually download PDFs
2. **Contact advisor** — ask Von Lücken / Cristaldo to send the PDFs directly
3. **Pol.una.py node pages** — abstract & summary available via `https://www2.pol.una.py/?q=node/1071` (no full text)
4. **In-person at CNC** — visit Centro de Información y Cultura at FPUNA San Lorenzo

**Recommendation:** Email Von Lücken with the P3 proposal — he likely has a copy of the 2026 thesis he supervised and can send the 2014 Jopara NLP PDF directly. This is also the natural opening for advisor outreach.

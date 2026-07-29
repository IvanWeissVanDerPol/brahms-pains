# fpuna_research/ — INDEX

Generated 2026-07-29 | 112.6 MB total | 692 files

## Read me first

👉 **[`THESIS_CORPUS_SYNTHESIS.md`](THESIS_CORPUS_SYNTHESIS.md)** — full corpus inventory, thematic clusters, advisor map, cross-faculty merge candidates, and 3 ranked proposal ideas for Iván's engineering thesis.

## Top-level data files

### Canonical FP-UNA Drupal export (2016-2018)
- `fpuna_canonical_2016_2018.json` — 40 rows (clean UTF-8, 94 KB)
- `fpuna_canonical_2016_2018_raw.csv` — original Windows-1252 CSV from `www2.pol.una.py/datos/tesis/`

### WordPress defensa posts (FP-UNA 2021-2026)
- `fpuna_wordpress_posts_extracted.json` — 317 posts with extracted metadata (572 KB)
- `fpuna_wordpress_url_list.txt` — list of all 317 source URLs
- `fpuna_wordpress_unique_titles.json` — 154 unique thesis titles quoted in posts
- `fpuna_thesis_titles_clustered.json` — same titles grouped by 14 research clusters
- `fpuna_thesis_titles_flat.json` — flat (title,date,source) triples (66 KB)
- `fpuna_all_posts_meta.json` — full meta from every post (95 KB)

### Central library OPAC (CNC-UNA, all faculties)
- `opac_thesis_records.json` — 566 records with author/advisor/year/signature (233 KB)
- 165 AI-themed, 49 with explicit orientador, 44 with online access link
- Source: `https://www.cnc.una.py/opac/search?q=...`

### Cross-faculty research lines
- `cross_fac_research_lines.json` — FADA/FACEN/FACSO/FCV research line text (33 KB)
- `cross_fac_url_list.json` + `cross_fac_urls.json` — list of source URLs

## raw_html_snapshots/ — audit trail

Every HTML page that was fetched. 692 files, 112.6 MB total. Useful for:
- Verifying the metadata extraction
- Finding theses that the extractor missed
- Doing additional passes (BERTopic, citation graph, advisor-relationship extraction)

Subdirs:
- `channels/` — Drupal frontpage archives, PoliGaceta, node 1513 (the 'últimos años' page itself)
- `cross_fac/` — FADA / FACEN / FACSO / FCV / FAING / FCA pagination across ?s=tesis|defensa|investigacion|trabajo_de_grado (24+24+6+1+0+24 pages)
- `wp_search/` — `www.pol.una.py/?s=tesis` pagination (10 + 37 pages)
- `posts/` — 317 defensa post HTMLs (~210 KB each)
- `opac_search/` — 91 OPAC search result HTMLs (~100 KB each)
- `special_pages/` — FADA_tfg, FADA_postg, FADA_inv, FACEN_investig, FACSO_inv, FCV_postgrado, OPAC_root
- `misc/` — single-file probes

## Suggested workflow for Ivan

1. Read `THESIS_CORPUS_SYNTHESIS.md` (cover-to-cover, ~16 KB, 300 lines).
2. Pick a Tier-S proposal (#1, #2, or #3) from §6.
3. `grep -ri 'orientador\|tutor' raw_html_snapshots/posts/ | less` to find specific advisor names.
4. Ask Erebus to dig into the relevant defense PDFs (next-step harvest).

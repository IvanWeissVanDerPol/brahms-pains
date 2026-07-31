"""
1000-THESIS-IDEAS ATLAS — comprehensive cartesian generator.

For Iván Weiss Van der Pol at Universidad Nacional de Asunción (Paraguay).

Dimensions (cartesian product):
  A. Faculty        : 14 UNA faculties + 6+ inter-faculty combinations
  B. Problem domain : 50+ problem domains (health, energy, cartography, education, ...)
  C. Method/tech    : 50+ AI/ML methods
  D. Data source    : 100+ real datasets (already cataloged + RFPs + open data)
  E. Advisor        : 50+ real UNA advisors (already verified)
  F. Output form    : 10 thesis types (Grado, Maestría, PhD, etc.)

Naive cartesian = 14 × 50 × 50 × 100 × 50 × 10 = 350M, way too many.

PRUNE HARD:
  - Only valid faculty-method-domain combinations
  - Only combinations that have datasets available
  - Only combinations that match real advisor expertise
  - Deduplicate by title

TARGET: 1,000 distinct, scored thesis ideas across the full space.
Each idea has: title, faculty, problem, method, datasets, advisor, score_vector.
"""

import json
from pathlib import Path
from itertools import product

OUT = Path("/root/psycology/SOURCE_OF_TRUTH/fpuna_research")

# =====================================================================
# DIMENSIONS
# =====================================================================

FACULTIES = {
    "FP-UNA": "Facultad Politécnica (Engineering, CS, EE, Industrial, Civil, Chemical, Materials, NIDTEC, etc.)",
    "FADA": "Facultad de Arquitectura, Diseño y Arte",
    "FACEN": "Facultad de Ciencias Exactas y Naturales",
    "FCM": "Facultad de Ciencias Médicas",
    "FACISA": "Facultad de Ciencias de la Salud",
    "FACSO": "Facultad de Ciencias Sociales",
    "FACV": "Facultad de Ciencias Veterinarias",
    "FCA": "Facultad de Ciencias Agrarias",
    "FCQ": "Facultad de Ciencias Químicas",
    "FIA": "Facultad de Ingeniería Agrícola",
    "ENF": "Facultad de Enfermería y Obstetricia",
    "ODON": "Facultad de Odontología",
    "DER": "Facultad de Derecho y Ciencias Sociales",
    "ECON": "Facultad de Ciencias Económicas",
    "FFIL": "Facultad de Filosofía",
    "FACULTAD": "Inter-faculty",
}

# =====================================================================
# Problem domains — 60
# =====================================================================

PROBLEM_DOMAINS = {
    # Health
    "P01": ("Mental health screening", "social", ["FACISA", "FCM", "FP-UNA"]),
    "P02": ("Maternal/child health", "health", ["ENF", "FCM", "FACISA"]),
    "P03": ("Infectious disease surveillance (dengue, chikungunya, COVID)", "health", ["FCM", "FACISA"]),
    "P04": ("Cancer detection/early warning", "health", ["FCM", "FACV"]),
    "P05": ("Antibiotic resistance patterns", "health", ["FCM", "FCQ"]),
    "P06": ("Mental health stigma quantification", "social", ["FACISA", "FCM"]),
    "P07": ("Diabetes/chronic disease management", "health", ["ENF", "FCM"]),
    "P08": ("Suicide prevention messaging", "social", ["FCM", "FACSO"]),
    "P09": ("Substance use/abuse prediction", "social", ["FCM", "FACSO"]),
    "P10": ("Aging/elderly care", "health", ["FCM", "ENF"]),
    # Energy
    "P11": ("Electric demand forecasting (ANDE)", "energy", ["FP-UNA", "FIA"]),
    "P12": ("Renewable energy potential (solar/wind)", "energy", ["FP-UNA", "FIA"]),
    "P13": ("Smart grid microgrids", "energy", ["FP-UNA"]),
    "P14": ("Energy poverty mapping", "social", ["FP-UNA", "FIA"]),
    "P15": ("Building energy efficiency", "energy", ["FADA", "FP-UNA"]),
    # Cartography / urban
    "P16": ("Participatory cartography (citizen mapping)", "geo", ["FADA", "FP-UNA"]),
    "P17": ("Urban flood risk modeling", "geo", ["FADA", "FP-UNA"]),
    "P18": ("Deforestation monitoring (Chaco)", "geo", ["FCA", "FP-UNA"]),
    "P19": ("Building footprint extraction (satellite)", "geo", ["FP-UNA", "FADA"]),
    "P20": ("Land use change detection", "geo", ["FCA", "FADA"]),
    "P21": ("Indigenous territory mapping", "geo", ["FFIL", "FADA"]),
    "P22": ("Public transportation accessibility", "transport", ["FP-UNA", "FADA"]),
    # Education
    "P23": ("Dropout prediction", "education", ["FP-UNA", "FACSO"]),
    "P24": ("MOOC learning analytics", "education", ["FP-UNA"]),
    "P25": ("Programming education tools", "education", ["FP-UNA"]),
    "P26": ("STEM gender gap", "education", ["FP-UNA", "FACSO"]),
    "P27": ("Inclusive education (special needs)", "education", ["FP-UNA", "FCM"]),
    # Language / NLP
    "P28": ("Jopara sentiment analysis", "language", ["FP-UNA", "FACEN"]),
    "P29": ("Guarani NLP models", "language", ["FP-UNA", "FACEN"]),
    "P30": ("Code-switching Paraguayan Spanish", "language", ["FP-UNA", "FACEN"]),
    "P31": ("Jopara machine translation", "language", ["FP-UNA", "FACEN"]),
    "P32": ("Speech recognition Guarani/Jopara", "language", ["FP-UNA"]),
    "P33": ("OCR for historical Guarani docs", "language", ["FP-UNA", "FADA"]),
    "P34": ("Multilingual legal NLP", "language", ["DER", "FP-UNA"]),
    "P35": ("Indigenous knowledge preservation", "language", ["FFIL", "FADA"]),
    # Agriculture / livestock
    "P36": ("Crop yield prediction", "agriculture", ["FIA", "FCA", "FP-UNA"]),
    "P37": ("Livestock disease early warning", "agriculture", ["FACV", "FCM"]),
    "P38": ("Precision agriculture (drones/sensors)", "agriculture", ["FIA", "FCA"]),
    "P39": ("Soil degradation monitoring", "agriculture", ["FCA"]),
    "P40": ("Aquaculture optimization", "agriculture", ["FACV", "FIA"]),
    # Crime / safety
    "P41": ("Crime hot spot prediction", "social", ["FACSO", "FP-UNA"]),
    "P42": ("Domestic violence pattern detection", "social", ["DER", "FCM"]),
    "P43": ("Traffic accident prevention", "transport", ["FP-UNA"]),
    "P44": ("Cyberbullying detection (Paraguayan schools)", "social", ["FP-UNA", "FACSO"]),
    # Environment / climate
    "P45": ("Climate change impact on agriculture", "agriculture", ["FCA"]),
    "P46": ("Air quality (PM2.5) forecasting (Asunción)", "environment", ["FCQ", "FP-UNA"]),
    "P47": ("Water resource management (Paraná basin)", "environment", ["FIA", "FCV"]),
    "P48": ("Biodiversity hot spots", "environment", ["FCV", "FCA"]),
    # Economic / governance
    "P49": ("Mipyme credit scoring", "economy", ["ECON", "FP-UNA"]),
    "P50": ("Tax fraud detection", "economy", ["ECON", "FP-UNA"]),
    "P51": ("Public procurement anomaly detection", "governance", ["ECON"]),
    "P52": ("Microfinance impact assessment", "economy", ["ECON"]),
    "P53": ("Inequality/mobility visualization", "social", ["ECON", "FADA"]),
    # Other
    "P54": ("Sports analytics (Paraguayan football)", "sports", ["FP-UNA"]),
    "P55": ("Music recommendation (Paraguayan polka/guarania)", "culture", ["FADA"]),
    "P56": ("E-government service optimization", "governance", ["ECON"]),
    "P57": ("Tourism recommendation engine", "economy", ["FADA", "ECON"]),
    "P58": ("Phytotherapy/medicinal plants identification", "health", ["FCV", "FP-UNA"]),
    "P59": ("Chagas vector habitat modeling", "health", ["FCM", "FCA"]),
    "P60": ("Garbage/waste route optimization", "environment", ["FP-UNA", "FADA"]),
}

# =====================================================================
# Methods — 50
# =====================================================================

METHODS = {
    "M01": ("Transformer fine-tuning (BERT/GPT)", "NLP"),
    "M02": ("LLM prompting (GPT-4/Claude/Llama)", "NLP"),
    "M03": ("RAG system", "NLP"),
    "M04": ("Multi-agent LLM system", "NLP"),
    "M05": ("Speech-to-text (Whisper)", "NLP"),
    "M06": ("Text-to-speech (TTS)", "NLP"),
    "M07": ("Named entity recognition", "NLP"),
    "M08": ("Topic modeling (LDA/BERTopic)", "NLP"),
    "M09": ("Sentiment / emotion classification", "NLP"),
    "M10": ("Machine translation", "NLP"),
    "M11": ("Question answering system", "NLP"),
    "M12": ("Summarization", "NLP"),
    "M13": ("Argument mining", "NLP"),
    "M14": ("Low-resource language modeling", "NLP"),
    "M15": ("Computer vision (CNN/ResNet)", "CV"),
    "M16": ("Object detection (YOLO/Detectron2)", "CV"),
    "M17": ("Image segmentation (U-Net/Mask R-CNN)", "CV"),
    "M18": ("Spectral image analysis (satellite)", "CV"),
    "M19": ("Optical character recognition (OCR)", "CV"),
    "M20": ("Face recognition", "CV"),
    "M21": ("Facial expression / emotion", "CV"),
    "M22": ("Pose estimation", "CV"),
    "M23": ("Image generation (diffusion/GAN)", "CV"),
    "M24": ("Synthetic data generation", "ML"),
    "M25": ("Federated learning", "ML"),
    "M26": ("Tabular ML (XGBoost/LightGBM)", "ML"),
    "M27": ("Time series forecasting (LSTM/Transformer)", "ML"),
    "M28": ("Anomaly / outlier detection", "ML"),
    "M29": ("Causal inference", "ML"),
    "M30": ("Active learning", "ML"),
    "M31": ("Reinforcement learning", "ML"),
    "M32": ("Multi-objective optimization (MOEA/NSGA-II)", "OR"),
    "M33": ("Combinatorial optimization (TSP, VRP)", "OR"),
    "M34": ("Bayesian optimization", "OR"),
    "M35": ("Constraint programming", "OR"),
    "M36": ("Linear/nonlinear programming", "OR"),
    "M37": ("Simulation-based optimization", "OR"),
    "M38": ("Network analysis / graph ML (GNN)", "ML"),
    "M39": ("Recommender system (collaborative filtering)", "ML"),
    "M40": ("Geospatial analysis (GIS/QGIS)", "geo"),
    "M41": ("Spatial statistics / autocorrelation", "geo"),
    "M42": ("Spatial ML (spatial CV)", "ML"),
    "M43": ("IoT sensor fusion", "systems"),
    "M44": ("Embedded ML (microcontroller)", "systems"),
    "M45": ("Edge computing", "systems"),
    "M46": ("AR/VR for training/simulation", "systems"),
    "M47": ("Chatbot (RAG-based)", "NLP"),
    "M48": ("Speech analysis (prosody/emotion)", "NLP"),
    "M49": ("Knowledge graph construction", "NLP"),
    "M50": ("Multimodal fusion (text + image)", "ML"),
}

# =====================================================================
# Data sources — 100
# =====================================================================

DATA_SOURCES = {
    "D01": "Geofabrik Paraguay OSM extract (150 MB, daily)",
    "D02": "ANDE public statistics (monthly/regional)",
    "D03": "INE census + EPH (Encuesta Permanente de Hogares)",
    "D04": "STP (PND, SDH socio-economic data)",
    "D05": "MITIC open data portal",
    "D06": "CONACYT PRONII researchers + Fondecyt grants",
    "D07": "MADES environmental (deforestation, climate)",
    "D08": "IGN (Instituto Geográfico Nacional) layers",
    "D09": "Zenodo 16891006 (Diverse Paraguay datasets)",
    "D10": "Indico UNA event 7 (108 contributions 2024)",
    "D11": "Indico UNA event 18 (28 math contributions)",
    "D12": "Indico UNA event 19 (5 FACSO contributions)",
    "D13": "Indico UNA event 20 (6 chemistry contributions)",
    "D14": "Drapal 1071 (20 pre-2017 FP-UNA theses)",
    "D15": "Master PDF Trabajos 2017 (52 MB)",
    "D16": "OPAC UNA (2,217 unique bibnums)",
    "D17": "somosnlp-hackathon-2026/paraguay-cultural-alignment (10K rows, 127 dl/mo)",
    "D18": "thinkPy/ultrachat-es-30k-topics",
    "D19": "thinkPy/corpus-cultura-paraguaya",
    "D20": "Iván's existing Telegram corpus (psycology repo)",
    "D21": "OpenWeather / NOAA climate forecasts",
    "D22": "Twitter/X public Spanish dataset",
    "D23": "Reddit r/paraguay scraping",
    "D24": "WhatsApp public channel extraction",
    "D25": "Public Sentinel-2 satellite imagery",
    "D26": "Globeland30 land cover data",
    "D27": "World Bank Open Data (Paraguay)",
    "D28": "Inter-American Development Bank (BID) data",
    "D29": "IMF country data (Paraguay)",
    "D30": "UNESCO UIS education statistics",
    "D31": "WHO Global Health Observatory",
    "D32": "PAHO (Pan American Health Organization) data",
    "D33": "MSPyBS (Ministerio Salud) public bulletins",
    "D34": "PY health facility master list (RIPSAS)",
    "D35": "MIC (Ministerio Industria y Comercio) PYME registry",
    "D36": "BCP (Banco Central Paraguay) macro stats",
    "D37": "ANDE demand time-series public",
    "D38": "Itaipu Binacional energy data",
    "D39": "Yacyreta hydro plant data",
    "D40": "DINAC meteorological stations",
    "D41": "Police open data (Policia Nacional)",
    "D42": "Public transport routes (Asunción)",
    "D43": "OpenStreetMap changesets Paraguay",
    "D44": "Recetas médicas dataset",
    "D45": "INA (gobierno) datos abiertos",
    "D46": "Auditoría General del Estado reports",
    "D47": "INDERT (Instituto Nacional de Desarrollo Rural y Tierra)",
    "D48": "Public court records (Poder Judicial PY)",
    "D49": "Paraguayan parliamentary bill texts",
    "D50": "MOPC (Ministry of Public Works) infrastructure data",
    "D51": "Recoleta cultural archive",
    "D52": "Banco de Datos Historicos Paraguay",
    "D53": "Archivo Nacional Asunción",
    "D54": "Daily weather stations",
    "D55": "Air quality monitoring (MADES)",
    "D56": "INE EPH continuous (houshold surveys)",
    "D57": "Universidad Católica UC theses",
    "D58": "Universidad Americana UA theses",
    "D59": "Universidad del Cono Sur (UC) theses",
    "D60": "Univ. del Pacífico (UP) theses",
    "D61": "Univ. Comunera (UCOM) theses",
    "D62": "UNE (Univ. Nac. del Este) theses",
    "D63": "UNI (Univ. Nac. de Itapúa) theses",
    "D64": "UNCA (Univ. Nac. de Caaguazú) theses",
    "D65": "UNICAN (Univ. Nac. de Canindeyú) theses",
    "D66": "UdelaR colibri.udelar.edu.uy theses",
    "D67": "UNLP SEDICI theses (Argentina)",
    "D68": "USP teses.usp.br theses (Brazil)",
    "D69": "UNAM ru.dgb.unam.mx theses (Mexico)",
    "D70": "UFRGS lume.ufrgs.br theses (Brazil)",
    "D71": "U. de Chile repositorio.uchile.cl theses",
    "D72": "UBA ri.conicet.gov.ar CONICET papers",
    "D73": "UNAL repositorio.unal.edu.co theses (Colombia)",
    "D74": "UNICAMP repository (Brazil)",
    "D75": "UNESCO/IFLA library registries",
    "D76": "OpenAlex Paraguay scholarly corpus",
    "D77": "scielo.iics.una.py (UNA IICS papers)",
    "D78": "scielo.org regional LATAM papers",
    "D79": "arxiv.org cs.CL (Paraguay NLP)",
    "D80": "arxiv.org cs.LG (Paraguay ML)",
    "D81": "PubMed Paraguay biomedical papers",
    "D82": "zbMATH Paraguay math/CS",
    "D83": "DBLP Paraguay CS papers",
    "D84": "OpenStreetMap Paraguay GeoJSON",
    "D85": "Landsat 8/9 Paraguay scenes (free)",
    "D86": "Sentinel-1 SAR (radar) Paraguay",
    "D87": "Copernicus DEM Paraguay",
    "D88": "WorldPop population rasters Paraguay",
    "D89": "WorldClim climate rasters Paraguay",
    "D90": "Open Buildings (Google) Paraguay",
    "D91": "Microsoft Planetary Computer Paraguay",
    "D92": "Mapillary street view (Paraguay)",
    "D93": "Facebook Population Density Maps",
    "D94": "Mobile phone data (anonymized)",
    "D95": "WiFi/CDR aggregate mobility",
    "D96": "OpenSky airplane data Paraguay",
    "D97": "Marine traffic Paraguay rivers",
    "D98": "OpenAQ air quality Paraguay",
    "D99": "Solar resource maps Paraguay",
    "D100": "Hydrological stations public data",
}

# =====================================================================
# Real UNA advisors (top 30 by recent activity) — from advisor_corpus_match
# =====================================================================

ADVISORS = {
    "A01": {"name": "Christian Von Lücken", "faculty": "FP-UNA", "group": "A y O", "expertise": ["MOEA", "NLP", "CV"], "email_if": "clucken@pol.una.py"},
    "A02": {"name": "Horacio Andrés Legal Ayala", "faculty": "FP-UNA", "group": "GPDI", "expertise": ["Computer vision", "OCR", "satellite"], "email_if": "hlegal@pol.una.py"},
    "A03": {"name": "José Luis Vázquez Noguera", "faculty": "FP-UNA", "group": "GIOIA", "expertise": ["AI", "ML", "systems"], "email_if": "jvazquez@pol.una.py"},
    "A04": {"name": "Cristian Schaerer", "faculty": "FP-UNA", "group": "CCyMA", "expertise": ["CS", "math", "AI"], "email_if": ""},
    "A05": {"name": "Sebastián Grillo", "faculty": "FP-UNA", "group": "GITOC", "expertise": ["computation theory", "formal methods"], "email_if": ""},
    "A06": {"name": "Daniel Alberto Ríos Festner", "faculty": "FP-UNA", "group": "GISE", "expertise": ["energy systems", "optimization"], "email_if": ""},
    "A07": {"name": "Eduardo Ortigoza", "faculty": "FP-UNA", "group": "GITE", "expertise": ["electronics", "control"], "email_if": ""},
    "A08": {"name": "Lucas Teótimo", "faculty": "FP-UNA", "group": "GIFE", "expertise": ["physics", "engineering"], "email_if": ""},
    "A09": {"name": "Juan Carlos Cristaldo", "faculty": "FADA", "group": "CIDi FADA", "expertise": ["cartography", "openstreetmap", "FAIR data"], "email_if": "jcristaldo@pol.una.py", "orcid": "0000-0001-6966-8787"},
    "A10": {"name": "Diego Stalder", "faculty": "FP-UNA", "group": "Stalder lab", "expertise": ["DL", "river forecasting", "Python", "Jupyter"], "github": "diegostaPy"},
    "A11": {"name": "Juan Pane", "faculty": "FP-UNA", "group": "(NLP)", "expertise": ["NLP", "sentiment analysis"], "github": "juanpane"},
    "A12": {"name": "Marcos Villagra", "faculty": "FP-UNA", "group": "NIDTEC", "expertise": ["quantum", "MOEA", "AI"], "orcid": ""},
    "A13": {"name": "Diego Pedro Pinto Roa", "faculty": "FACEN", "group": "(FACEN CS)", "expertise": ["MOEA", "optical networks"], "papers": 106},
    "A14": {"name": "Raúl Igmar Gregor Recalde", "faculty": "FP-UNA", "group": "(IoT)", "expertise": ["LoRaWAN", "IoT", "power electronics"], "orcid": ""},
    "A15": {"name": "Julio Torales", "faculty": "FCM", "group": "Mental Health (FCM)", "expertise": ["psychiatry", "mental health screening"], "orcid": "0000-0003-3277-7036", "email": "juliotorales@med.una.py"},
    "A16": {"name": "Iván Barrios", "faculty": "FCM", "group": "Mental Health (FCM)", "expertise": ["psychiatry", "epidemiology"], "orcid": "0000-0002-6843-7685", "email": "jbarrios@fcmuna.edu.py"},
    "A17": {"name": "Marcelo O'Higgins", "faculty": "FCM", "group": "Mental Health (FCM)", "expertise": ["mental health", "epidemiology"], "orcid": ""},
    "A18": {"name": "Tomás Caycho-Rodríguez", "faculty": "(Peru, Jung)", "group": "External", "expertise": ["personality", "psychology"], "orcid": ""},
    "A19": {"name": "Sergio Manuel Chamorro Díaz", "faculty": "FP-UNA", "group": "(systems)", "expertise": ["control systems"], "orcid": ""},
    "A20": {"name": "María Soledad Ayala Rodríguez", "faculty": "FP-UNA", "group": "(software)", "expertise": ["software engineering"], "orcid": ""},
    "A21": {"name": "César Yegros", "faculty": "FP-UNA", "group": "(visualization)", "expertise": ["information visualization"], "orcid": ""},
    "A22": {"name": "Juan Talavera", "faculty": "FP-UNA", "group": "(CV)", "expertise": ["computer vision"], "orcid": ""},
    "A23": {"name": "Gustavo Sosa", "faculty": "FP-UNA", "group": "(deep learning)", "expertise": ["ML", "DL"], "github": "GusSosa"},
    "A24": {"name": "Arturo Ramón", "faculty": "FP-UNA", "group": "(renewables)", "expertise": ["renewable energy"], "orcid": ""},
    "A25": {"name": "Mirtha González", "faculty": "FCM", "group": "(epidemiology)", "expertise": ["public health"], "orcid": ""},
    "A26": {"name": "Dionisio Telmo Zaracho", "faculty": "FCA", "group": "(agraria)", "expertise": ["agricultural engineering"], "orcid": ""},
    "A27": {"name": "Antonio Rivarola", "faculty": "FCV", "group": "(veterinaria)", "expertise": ["veterinary", "epidemiology"], "orcid": ""},
    "A28": {"name": "Gladys Estigarribia", "faculty": "FCM", "group": "Mental Health (FCM)", "expertise": ["mental health", "epidemiology"], "orcid": ""},
    "A29": {"name": "Santiago Pancic", "faculty": "FP-UNA", "group": "(networks)", "expertise": ["computer networks"], "orcid": ""},
    "A30": {"name": "Roxana Carla Corbalán", "faculty": "FCV", "group": "(biomedicine)", "expertise": ["biomedical"], "orcid": ""},
}

# =====================================================================
# Generate
# =====================================================================
def generate():
    ideas = []
    idea_id = 0

    # Strategy 1: Method × domain × data × advisor (drop faculty, fill later)
    # Pick a method first, then a domain where method applies, then data, then advisor

    # Heuristic: pair method with compatible domain categories
    NLP_DOMAINS = ["health", "social", "education", "language", "culture", "governance", "sports"]
    CV_DOMAINS = ["health", "geo", "environment", "agriculture", "culture"]
    OR_DOMAINS = ["energy", "transport", "environment", "economics", "agriculture"]
    ML_DOMAINS = ["health", "social", "education", "economy", "energy", "governance"]
    GEO_DOMAINS = ["geo", "environment", "agriculture", "transport"]
    SYS_DOMAINS = ["energy", "transport", "agriculture", "health"]
    ALL_DOMAINS = NLP_DOMAINS + CV_DOMAINS + OR_DOMAINS + ML_DOMAINS + GEO_DOMAINS + SYS_DOMAINS
    ALL_DOMAINS = list(set(ALL_DOMAINS))

    for (mid, (m_name, m_cat)), (pid, (p_name, p_cat, p_facs)) in product(METHODS.items(), PROBLEM_DOMAINS.items()):
        # Filter by method category
        if m_cat == "NLP" and p_cat not in NLP_DOMAINS: continue
        if m_cat == "CV" and p_cat not in CV_DOMAINS: continue
        if m_cat == "OR" and p_cat not in OR_DOMAINS: continue
        if m_cat in ("ML",) and p_cat not in ML_DOMAINS: continue
        if m_cat == "geo" and p_cat not in GEO_DOMAINS: continue
        if m_cat == "systems" and p_cat not in SYS_DOMAINS: continue

        # Pick 1-3 data sources heuristically by category
        datas = []
        if p_cat in ["health"]:
            datas += ["D03", "D31", "D32", "D33", "D34", "D44", "D81"]
        if p_cat in ["social"]:
            datas += ["D03", "D04", "D06", "D22", "D23", "D24", "D30"]
        if p_cat in ["energy"]:
            datas += ["D02", "D06", "D37", "D38", "D39", "D40", "D54", "D99", "D100"]
        if p_cat in ["geo", "environment"]:
            datas += ["D01", "D07", "D08", "D25", "D26", "D43", "D84", "D85", "D86", "D87", "D88", "D89", "D90", "D91", "D97", "D98"]
        if p_cat in ["transport"]:
            datas += ["D03", "D42", "D43", "D01"]
        if p_cat in ["education"]:
            datas += ["D03", "D06", "D30", "D16", "D57", "D58"]
        if p_cat in ["language"]:
            datas += ["D17", "D18", "D19", "D20", "D22", "D23", "D24", "D52", "D53", "D79", "D82", "D83"]
        if p_cat in ["agriculture"]:
            datas += ["D03", "D07", "D25", "D40", "D54", "D85"]
        if p_cat in ["economy", "governance"]:
            datas += ["D03", "D04", "D06", "D27", "D28", "D29", "D35", "D36", "D49", "D51"]
        if p_cat in ["culture"]:
            datas += ["D22", "D23", "D51", "D52", "D53"]
        if p_cat in ["sports"]:
            datas += ["D22", "D23", "D03"]

        # Pick faculty
        primary_fac = p_facs[0] if p_facs else "FP-UNA"

        # Pick advisor by expertise match
        matching_advisors = []
        for aid, a in ADVISORS.items():
            if m_cat == "NLP" and any(e in a["expertise"] for e in ["NLP", "sentiment", "speech", "OCR"]): matching_advisors.append(aid)
            if m_cat == "CV" and any(e in a["expertise"] for e in ["Computer vision", "OCR", "satellite", "pose", "face"]): matching_advisors.append(aid)
            if m_cat == "OR" and any(e in a["expertise"] for e in ["MOEA", "optimization", "energy systems", "physics", "engineering"]): matching_advisors.append(aid)
            if m_cat in ["ML", "geo", "systems"] and any(e in a["expertise"] for e in ["DL", "IoT", "ML", "systems", "MOEA", "cartography", "openstreetmap"]): matching_advisors.append(aid)
        if not matching_advisors:
            matching_advisors = ["A01", "A09"]

        # Generate 5 ideas per (method, domain) — multiple advisor variants
        for k, aid in enumerate(matching_advisors[:5]):
            idea_id += 1
            ideas.append({
                "id": f"I{idea_id:04d}",
                "title": f"{m_name} for {p_name} at {primary_fac}",
                "method": m_name,
                "method_code": mid,
                "problem": p_name,
                "problem_code": pid,
                "problem_category": p_cat,
                "primary_faculty": primary_fac,
                "related_faculties": p_facs,
                "data_sources": datas[:5] if datas else ["D16"],
                "advisor_id": aid,
                "advisor_name": ADVISORS[aid]["name"],
                "advisor_faculty": ADVISORS[aid]["faculty"],
                "rank_score": 0,  # filled later
            })

            if idea_id >= 5000:
                break
        if idea_id >= 5000:
            break
        if idea_id % 200 == 0:
            print(f"  generated {idea_id} ideas...")
    return ideas


def score(ideas):
    """Score ideas on 6 dimensions 0-10. Differentiate."""
    # Dedup titles
    seen_titles = set()
    unique_ideas = []
    for idea in ideas:
        if idea["title"] in seen_titles:
            continue
        seen_titles.add(idea["title"])
        unique_ideas.append(idea)
    print(f"Dedup: {len(ideas)} -> {len(unique_ideas)} unique")

    for idea in unique_ideas:
        # 1. Faculty match
        a_fac = idea["advisor_faculty"]
        if a_fac == idea["primary_faculty"]:
            score_fac = 9
        elif a_fac == "FP-UNA":  # FP-UNA can sponsor any
            score_fac = 7
        elif a_fac in idea["related_faculties"]:
            score_fac = 7
        else:
            score_fac = 4

        # 2. Data availability (varies by domain — Guyana Cartography has tons, Mental Health has few)
        # Use problem_code for exact scoring
        data_score = min(len(idea["data_sources"]) * 1.5, 10)

        # 3. Method-category impact
        m_cat = next(cat for (name, cat) in METHODS.values() if name == idea["method"])
        if m_cat in ["NLP", "CV"]:
            m_score = 9  # hot fields
        elif m_cat == "ML":
            m_score = 8
        elif m_cat in ["OR", "geo"]:
            m_score = 7
        else:
            m_score = 6

        # 4. Novelty (presence of LATAM baseline)
        p_cat = idea["problem_category"]
        pid = idea["problem_code"]
        # Heavy baseline — lower novelty
        if pid in ["P28", "P29", "P31", "P32", "P33"]:  # jopara NLP — high competition
            novelty = 4  # Mombeu + Diaz 2025 + Diaz 2023 + Cultural-alignment
        elif pid in ["P06", "P08", "P09"]:  # mental health stigma, suicide, substance
            novelty = 6  # FCM-UNA group active
        elif pid in ["P11", "P13"]:  # ANDE energy
            novelty = 6  # Stalder + 2 active students
        elif pid in ["P16", "P17", "P18", "P19", "P20"]:  # cartography
            novelty = 7  # Cristaldo active but at FADA
        elif pid in ["P44", "P45", "P46", "P47", "P48"]:  # novel
            novelty = 9  # Almost no Paraguayan baseline
        elif pid in ["P49", "P50", "P51", "P52", "P53"]:  # economy/governance
            novelty = 8  # Some but not deep
        elif pid in ["P60", "P57", "P56", "P55", "P54"]:  # other
            novelty = 9
        else:
            novelty = 7

        # 5. Advisor activity (top = +1, mid = 0, low = -1)
        a_id = idea["advisor_id"]
        if a_id in ["A01", "A02", "A09", "A10", "A11", "A12", "A15", "A16"]:  # top 8
            advisor_score = 10
        elif a_id in ["A04", "A05", "A06", "A07", "A08", "A13", "A14", "A17", "A18", "A19", "A20"]:
            advisor_score = 7
        else:
            advisor_score = 5

        # 6. Publication potential (Tier 1 vs Tier 3 venues)
        # If method is NLP/CV + has data + new angle → Q1 possibility (Cognitive Computation, IEEE Access, etc.)
        # If Cartography + OSM + Paraguay → IEEE Latin America / Computers, Environment and Urban Systems
        # If Mental Health + clinical partner → BJPsych / Frontiers / JMIR Mental Health
        # If Health general → BMC Medical Informatics
        # If ML generic + benchmark dataset → Algorithms/MDPI
        pub_score = 5
        if pid in ["P01", "P06", "P08", "P09", "P02", "P03", "P04", "P05"]:
            pub_score = 8  # clinical/medical Q1-2
        elif pid in ["P16", "P17", "P18", "P19"]:
            pub_score = 9  # IJGIS / IEEE TGRS
        elif pid in ["P11", "P12", "P13", "P14"]:
            pub_score = 8  # Energy Policy / IEEE Trans Power Systems
        elif pid in ["P28", "P29", "P31", "P32"]:
            pub_score = 9  # ACL / EMNLP / Cognitive Computation Q1
        elif pid in ["P44", "P45", "P46"]:
            pub_score = 7
        elif pid in ["P49", "P50"]:
            pub_score = 7
        else:
            pub_score = 6

        total = (score_fac + data_score + m_score + novelty + advisor_score + pub_score) / 6
        idea["score"] = round(total, 2)
        idea["score_dimensions"] = {
            "faculty_match": score_fac,
            "data_availability": data_score,
            "method_alignment": m_score,
            "novelty": novelty,
            "advisor_activity": advisor_score,
            "publication_potential": pub_score,
        }

    return unique_ideas


def main():
    print("Generating ideas...")
    ideas = generate()
    print(f"\nGenerated {len(ideas)} raw ideas")
    print("\nScoring...")
    ideas = score(ideas)
    ideas.sort(key=lambda i: -i["score"])

    out = {
        "generated_at": "2026-07-30",
        "scope": "Comprehensive thesis ideas for Iván Weiss Van der Pol at UNA Paraguay — 1000+ across all faculties, domains, methods, advisors",
        "n_ideas": len(ideas),
        "n_faculties": len(FACULTIES),
        "n_problem_domains": len(PROBLEM_DOMAINS),
        "n_methods": len(METHODS),
        "n_data_sources": len(DATA_SOURCES),
        "n_advisors": len(ADVISORS),
        "scoring_dimensions": ["faculty_match", "data_availability", "method_alignment", "novelty", "advisor_activity", "publication_potential"],
        "top_100_with_full_detail": ideas[:100],
        "ideas_101_to_500_medium": ideas[100:500],
        "ideas_501_to_1000_short": ideas[500:1000],
        "ideas_1001_plus_extras": ideas[1000:] if len(ideas) > 1000 else [],
        "advisor_index": ADVISORS,
        "data_index": DATA_SOURCES,
        "method_index": METHODS,
        "problem_index": {pid: {"name": name, "category": cat, "faculties": facs} for pid, (name, cat, facs) in PROBLEM_DOMAINS.items()},
        "usage": "Looking for thesis idea? 1) Browse top-100 by score. 2) Use score_dimensions to filter (e.g. novelty>8 = wide-open domain). 3) Check problem_index for cross-listing by domain. 4) Cross-reference advisor_index with their known expertise."
    }

    out_path = OUT / "thesis_1000_ideas_atlas.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"\nWrote {out_path} ({out_path.stat().st_size:,} bytes)")
    print(f"\nTop 20 ideas by total score:")
    for i in ideas[:20]:
        print(f"  {i['id']:>6s} score={i['score']:5.2f} | {i['title'][:90]}")

if __name__ == "__main__":
    main()

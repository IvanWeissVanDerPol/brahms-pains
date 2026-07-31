#!/usr/bin/env python3
"""
THESIS DECISION WIZARD for Iván Weiss Van der Pol.
Reads thesis_1000_ideas_atlas.json + advisor_index, applies preference filters,
produces top-3 + top-10 markdown rankings.

Usage:
  python3 thesis_decision_wizard.py --defaults
  python3 thesis_decision_wizard.py --time=24months --faculty=FP-UNA --advisor=ANY --risk=high --data=moderate --pub=Q2 --topics="health,energy,geo"
  python3 thesis_decision_wizard.py --compare=I0042,P0010,P0025 --criteria="novelty,advisor_fit,publication_speed"
  python3 thesis_decision_wizard.py --commit T1=I0042 [--weight-novelty 0.3] [--weight-data 0.2] ...

Everything is CLI-driven. Runs in < 2 seconds.
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

OUT = Path(__file__).parent.resolve()
ATLAS_PATH = OUT / "thesis_1000_ideas_atlas.json"


# =====================================================================
# Helpers
# =====================================================================

def load_atlas():
    if not ATLAS_PATH.exists():
        sys.exit(f"ERROR: {ATLAS_PATH} not found. Run thesis_1000_generator.py first.")
    return json.loads(ATLAS_PATH.read_text(encoding="utf-8"))


def all_ideas_flat(atlas):
    """Return a single flat list of all ideas, regardless of which bucket they live in."""
    out = []
    for k in (
        "top_100_with_full_detail",
        "ideas_101_to_500_medium",
        "ideas_501_to_1000_short",
        "ideas_1001_plus_extras",
    ):
        for x in atlas.get(k, []):
            out.append(x)
    return out


def parse_filters(args):
    """Parse wizard CLI args into a normalized filter spec."""
    # Defaults
    spec = dict(
        time="24m",
        faculty="FP-UNA",
        advisor="ANY",
        risk="high",
        data="moderate",
        pub="any",
        topics=set(),
        weights={"novelty": 0.25, "advisor_activity": 0.20, "data_availability": 0.20, "publication_potential": 0.20, "faculty_match": 0.10, "method_alignment": 0.05},
    )
    if args.time:
        spec["time"] = args.time
    if args.faculty:
        spec["faculty"] = args.faculty.upper()
    if args.advisor:
        spec["advisor"] = args.advisor.upper()
    if args.risk:
        spec["risk"] = args.risk
    if args.data:
        spec["data"] = args.data
    if args.pub:
        spec["pub"] = args.pub
    if args.topics:
        cats = [t.strip().lower() for t in args.topics.split(",") if t.strip()]
        spec["topics"] = set(cats)

    # Always interpret topics=ALL as empty
    if "all" in spec["topics"]:
        spec["topics"] = set()

    # Risk -> novelty threshold
    risk_map = {
        "low": 0,
        "medium": 7,
        "high": 8,
        "extreme": 9,
    }
    spec["novelty_min"] = risk_map.get(spec["risk"], 8)

    # Time -> data minimum (strict time = need ready data)
    time_data_min = {"12m": 8, "24m": 5, "36m": 0}
    spec["data_min"] = time_data_min.get(spec["time"], 5)

    # Override: data argument
    if spec["data"] == "minimal":
        spec["data_min"] = 8
    elif spec["data"] == "heavy":
        spec["data_min"] = 0

    # Pub -> publication_potential
    pub_map = {"Q1": 9, "Q2": 8, "Q3": 7, "any": 0}
    spec["pub_min"] = pub_map.get(spec["pub"], 0)

    # Weights override
    for wk in ("novelty", "advisor", "data", "publication", "faculty", "method"):
        full = {
            "novelty": "novelty",
            "advisor": "advisor_activity",
            "data": "data_availability",
            "publication": "publication_potential",
            "faculty": "faculty_match",
            "method": "method_alignment",
        }[wk]
        v = getattr(args, f"weight_{wk}", None)
        if v is not None:
            spec["weights"][full] = float(v)
    # Normalize
    total = sum(spec["weights"].values()) or 1.0
    for k in spec["weights"]:
        spec["weights"][k] /= total

    return spec


def weight_score(idea, weights):
    dims = idea["score_dimensions"]
    return sum(weights[k] * dims[k] for k in weights if k in dims)


def filter_ideas(atlas, spec, all_ideas):
    out = []
    for i in all_ideas:
        dims = i["score_dimensions"]
        # Faculty
        if spec["faculty"] != "ANY" and spec["faculty"] != "FACULTAD":
            if i["primary_faculty"] != spec["faculty"] and spec["faculty"] not in i["related_faculties"]:
                continue
            if spec["faculty"] == "FACULTAD":
                pass
        # Advisor
        if spec["advisor"] != "ANY":
            a_code = i["advisor_id"]
            if a_code != spec["advisor"]:
                # also allow via advisor real name match
                names_map = {"A01": "Von Lucken", "A10": "Stalder", "A11": "Pane", "A15": "Torales", "A16": "Barrios", "A09": "Cristaldo", "A02": "Legal", "A12": "Villagra"}
                if spec["advisor"].upper() in (names_map.get(a_code, "").upper(), i["advisor_name"].upper()):
                    pass
                else:
                    continue
        # Novelty
        if dims.get("novelty", 0) < spec["novelty_min"]:
            continue
        # Data
        if dims.get("data_availability", 0) < spec["data_min"]:
            continue
        # Pub
        if dims.get("publication_potential", 0) < spec["pub_min"]:
            continue
        # Topics
        if spec["topics"] and i["problem_category"] not in spec["topics"]:
            continue
        out.append(i)
    # Re-rank by weighted score
    for i in out:
        i["w_score"] = round(weight_score(i, spec["weights"]), 3)
    out.sort(key=lambda x: -x["w_score"])
    return out


def fmt_top_n(ideas, n, atlas):
    out = []
    out.append(f"# TOP {n} — Thesis Ideas (Wizard Output)")
    out.append("")
    out.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    out.append("")
    advisor_index = atlas["advisor_index"]
    out.append(f"## Wizard Configuration")
    for k, v in sorted(atlas.items()):
        if k in ("n_ideas", "n_faculties", "n_problem_domains", "n_methods", "n_data_sources", "n_advisors",
                 "top_100_with_full_detail", "ideas_101_to_500_medium", "ideas_501_to_1000_short",
                 "ideas_1001_plus_extras", "advisor_index", "data_index", "method_index", "problem_index",
                 "usage", "scoring_dimensions", "paraguayan_crafted_count", "total_ideas_count_updated"):
            continue
        out.append(f"- **{k}**: {v}")

    out.append("")
    out.append("## Ranking (by weighted score)")
    out.append("")
    out.append("| Rank | ID | Score | Title | Faculty | Advisor |")
    out.append("|------|-----|-------|-------|---------|---------|")
    for j, idea in enumerate(ideas[:n], 1):
        title = idea["title"]
        if len(title) > 70:
            title = title[:67] + "..."
        out.append(f"| {j} | {idea['id']} | {idea.get('w_score', idea.get('score'))} | {title} | {idea['primary_faculty']} | {idea['advisor_name']} |")
    out.append("")

    out.append("## Expanded Briefs (top 3 only)")
    out.append("")
    for j, idea in enumerate(ideas[:3], 1):
        d = idea["score_dimensions"]
        out.append(f"### #{j} {idea['title']}")
        out.append("")
        out.append(f"- **ID:** `{idea['id']}` (weighted={idea.get('w_score', idea.get('score'))}, raw={idea.get('score')})")
        out.append(f"- **Method:** {idea['method']}")
        out.append(f"- **Problem:** {idea['problem']} (category: `{idea['problem_category']}`)")
        out.append(f"- **Primary Faculty:** {idea['primary_faculty']}")
        out.append(f"- **Advisor:** {idea['advisor_name']} ({idea['advisor_faculty']})")
        out.append(f"- **Data:** {', '.join(idea.get('data_sources', [])[:5])}")
        out.append(f"- **Score Vector:** " + ", ".join(f"{k}={v}/10" for k, v in d.items()))
        if "rationale" in idea:
            out.append(f"- **Rationale:** {idea['rationale']}")
        out.append("")
        # 30-second pitch
        pitch = generate_pitch(idea)
        out.append("**30-second pitch (to advisor):**")
        out.append("")
        out.append(f"> {pitch}")
        out.append("")
        # Outreach draft
        email = generate_outreach_draft(idea, advisor_index[idea["advisor_id"]])
        out.append("**Outreach email draft:**")
        out.append("")
        out.append("```")
        out.append(email)
        out.append("```")
        out.append("")
    return "\n".join(out)


def generate_pitch(idea):
    d = idea["score_dimensions"]
    title = idea["title"]
    method = idea["method"]
    problem = idea["problem"]
    faculty = idea["primary_faculty"]
    pub = d["publication_potential"]
    novelty = d["novelty"]
    method_pubs = {
        "Q1 venue classes": ["Cognitive Computation Q1", "IEEE TGRS", "IJGIS", "Nature Comm.", "ACL/EMNLP", "BJPsych Int Q2"],
        "Q2 venue classes": ["IEEE Access", "Frontiers in AI", "JMIR Mental Health", "BMC Med Inf", "Sci. Reports"],
        "Q3": ["IEEE Latin America Trans.", "MDPI Algorithms", "Sustainability"],
    }
    venue_class = "Q1" if pub >= 9 else ("Q2" if pub >= 8 else "Q3")
    novelty_phrase = "wide open in Paraguay" if novelty >= 8 else ("novel with some baseline" if novelty >= 6 else "well-trodden but defensible")
    return (
        f"Professor, mi nombre es Iván Weiss Van der Pol, estudiante de {faculty}. "
        f"Me interesa desarrollar mi tesis en: **{title}**. "
        f"La idea es aplicar {method} para abordar {problem}, un área {novelty_phrase}. "
        f"He identificado que el enfoque tiene potencial de publicación en clase {venue_class} "
        f"porque {pub >= 8 and 'la metodología es transferible y la novedad es defendible' or 'los resultados son aplicables'}."
    )


def generate_outreach_draft(idea, advisor):
    name = advisor["name"]
    title = idea["title"]
    method = idea["method"]
    problem = idea["problem"]
    faculty = idea["primary_faculty"]
    pitch = generate_pitch(idea)
    return (
        f"Subject: Solicitud de tutoria de tesis — {title}\n\n"
        f"Estimado/a Prof. {name},\n\n"
        f"Me llamo Iván Weiss Van der Pol y soy estudiante de {faculty} de la UNA. "
        f"He estado construyendo una tesis alrededor del tema: {title}. "
        f"El enfoque combina {method} con {problem}. "
        f"Me interesa especialmente su trabajo en {', '.join(advisor.get('expertise', []))}.\n\n"
        f"{pitch}\n\n"
        f"He estado recopilando corpus de tesis, datasets y baselines LATAM (somosnlp-hackathon-2026/paraguay-cultural-alignment, "
        f"SCIELO IICS, OPAC UNA 2,217 tesis) en /root/psycology/SOURCE_OF_TRUTH/fpuna_research/. "
        f"¿Tendrá espacio para tutorearme en este tema, o prefiere explorar primero el fit por 30 minutos?\n\n"
        f"Quedo atento/a a su respuesta.\n\n"
        f"Iván Weiss Van der Pol"
    )


def main():
    parser = argparse.ArgumentParser(description="Thesis Decision Wizard for Iván")
    parser.add_argument("--time", help="12m, 24m, 36m")
    parser.add_argument("--faculty", help="FP-UNA, FADA, etc., or ANY")
    parser.add_argument("--advisor", help="A01..A30 advisor code, real name, or ANY")
    parser.add_argument("--risk", help="low, medium, high, extreme")
    parser.add_argument("--data", help="minimal, moderate, heavy")
    parser.add_argument("--pub", help="Q1, Q2, Q3, any")
    parser.add_argument("--topics", help="comma-separated categories (health,energy,geo,...) or ALL")
    parser.add_argument("--compare", help="comma-separated idea IDs for side-by-side")
    parser.add_argument("--criteria", help="comma-separated criteria names")
    parser.add_argument("--commit", help="commit T1=<ID>,T2=<ID>")
    parser.add_argument("--weight-novelty", type=float)
    parser.add_argument("--weight-advisor", type=float)
    parser.add_argument("--weight-data", type=float)
    parser.add_argument("--weight-publication", type=float)
    parser.add_argument("--weight-faculty", type=float)
    parser.add_argument("--weight-method", type=float)
    parser.add_argument("--defaults", action="store_true", help="use default profile")
    args = parser.parse_args()

    atlas = load_atlas()
    all_ideas = all_ideas_flat(atlas)

    # Profile shortcuts
    if args.topics == "P-JOPARA":
        args.time = "24m"; args.faculty = "FP-UNA"; args.advisor = "A11"; args.risk = "medium"; args.data = "minimal"; args.pub = "Q1"; args.topics = "language,health"
    elif args.topics == "P-ANDE":
        args.time = "24m"; args.faculty = "FP-UNA"; args.advisor = "A10"; args.risk = "low"; args.data = "minimal"; args.pub = "Q2"; args.topics = "energy"
    elif args.topics == "P-CARTO":
        args.time = "24m"; args.faculty = "FADA"; args.advisor = "A09"; args.risk = "low"; args.data = "minimal"; args.pub = "Q1"; args.topics = "geo,environment"
    elif args.topics == "P-CLINICAL":
        args.time = "24m"; args.faculty = "FCM"; args.advisor = "A15"; args.risk = "medium"; args.data = "heavy"; args.pub = "Q2"; args.topics = "health"
    elif args.topics == "P-WIDE-OPEN":
        args.time = "24m"; args.faculty = "ANY"; args.advisor = "ANY"; args.risk = "extreme"; args.data = "moderate"; args.pub = "any"; args.topics = "ALL"
    elif args.topics == "P-PUB-Q1":
        args.time = "24m"; args.faculty = "ANY"; args.advisor = "ANY"; args.risk = "any"; args.data = "any"; args.pub = "Q1"; args.topics = "ALL"
    elif args.topics == "P-LOW-DATA":
        args.time = "12m"; args.faculty = "ANY"; args.advisor = "ANY"; args.risk = "any"; args.data = "minimal"; args.pub = "any"; args.topics = "ALL"

    # Compare mode
    if args.compare:
        ids = [x.strip() for x in args.compare.split(",") if x.strip()]
        matched = [i for i in all_ideas if i["id"] in ids]
        if not matched:
            sys.exit(f"None of the IDs {ids} found in atlas")
        criteria = (args.criteria or "novelty,advisor_fit,publication_speed").split(",")
        out = []
        out.append(f"# Comparison of {len(ids)} ideas\n")
        out.append(f"**Criteria:** {', '.join(criteria)}\n")
        out.append("| Idea | " + " | ".join(criteria) + " |")
        out.append("|------" + "|".join(["----"] * len(criteria)) + "|")
        for i in matched:
            d = i["score_dimensions"]
            row = [f"**{i['id']}** {i['title'][:50]}"]
            for c in criteria:
                row.append(str(d.get(c.strip(), "?")))
            out.append("| " + " | ".join(row) + " |")
        print("\n".join(out))
        return

    spec = parse_filters(args)
    matched = filter_ideas(atlas, spec, all_ideas)

    if not matched:
        print(f"\n[WIZARD] No ideas match your filters. Try relaxing them.")
        print(f"\nCurrent spec: {spec}")
        return

    # Print summary
    print("=" * 80)
    print("WIZARD SPEC (effective)")
    print("=" * 80)
    for k, v in sorted(spec.items()):
        print(f"  {k}: {v}")
    print(f"\nMatched {len(matched)} ideas from {len(all_ideas)} total.")
    print()
    # Write top-10 file
    top10 = matched[:10]
    top10_md = fmt_top_n(matched, 10, atlas)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path_top10 = OUT / f"thesis_wizard_top10_{ts}.md"
    out_path_top10.write_text(top10_md, encoding="utf-8")
    print(f"Wrote {out_path_top10}")
    # Write top-3 file separately
    top3_md = fmt_top_n(matched, 3, atlas)
    out_path_top3 = OUT / f"thesis_wizard_top3_{ts}.md"
    out_path_top3.write_text(top3_md, encoding="utf-8")
    print(f"Wrote {out_path_top3}")
    print()
    # Print top 5 to console
    for j, i in enumerate(top10[:5], 1):
        print(f"  {j}. {i['id']:>6s} w_score={i['w_score']:.2f} | {i['title'][:80]}")
    print()

    # If commit, write THESIS_DECISION_v2.md
    if args.commit:
        # Parse "T1=ID1,T2=ID2"
        commits = {}
        for kv in args.commit.split(","):
            if "=" in kv:
                k, v = kv.split("=", 1)
                commits[k.strip().upper()] = v.strip()
        if not commits:
            print("[WIZARD] --commit needs format: T1=I0010,T2=P0025")
            return
        committed = []
        for k, id_ in commits.items():
            for idea in matched:
                if idea["id"] == id_:
                    committed.append((k, idea))
                    break
        if not committed:
            print("[WIZARD] no ideas matched the commit IDs")
            return
        # Write the formal decision
        d_path = OUT / "THESIS_DECISION_v2.md"
        body = ["# THESIS DECISION v2 — Iván's Thesis Choices (Wizard)", ""]
        body.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        body.append("")
        body.append("**Wizard spec:**")
        body.append(f"```")
        for k, v in sorted(spec.items()):
            body.append(f"  {k}: {v}")
        body.append("```")
        body.append("")
        body.append("**Decisions:**")
        body.append("")
        for k, idea in committed:
            body.append(f"## {k} = {idea['id']}: {idea['title']}")
            body.append("")
            body.append(f"- **Faculty:** {idea['primary_faculty']}")
            body.append(f"- **Advisor:** {idea['advisor_name']} ({idea['advisor_faculty']})")
            body.append(f"- **Method:** {idea['method']}")
            body.append(f"- **Problem:** {idea['problem']}")
            body.append(f"- **Weighted Score:** {idea['w_score']}")
            body.append(f"- **Raw Score:** {idea['score']}")
            body.append("")
            if "rationale" in idea:
                body.append(f"**Rationale:** {idea['rationale']}")
                body.append("")
        body.append("**Next steps:**")
        body.append("1. Run wizard in --compare mode against this set to validate")
        body.append("2. Reach out to advisors with the pre-generated drafts above")
        body.append("3. Start data collection per `paraguay_datasets_paraguay.json`")
        body.append("4. Begin IRB application if clinical, or ethics approval if human-subjects")
        body.append("")
        d_path.write_text("\n".join(body), encoding="utf-8")
        print(f"Wrote {d_path}")


if __name__ == "__main__":
    main()

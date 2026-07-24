#!/usr/bin/env python3
"""Build a static SVG family tree visualization from profiles."""
from __future__ import annotations
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROFILE_DIR = REPO / "RELATIONSHIPS" / "dynamics"

# Family tree (manual layout based on verified family relationships from
# family-corrections work + vCard match)
FAMILY = {
    "Sonia Edith Weiss López": {
        "role": "Mom",
        "generation": 1,
        "x": 0, "y": 0,
        "tier": "mom",
        "profile": "SONIA_WEISS",
    },
    "John van der Pol": {
        "role": "Dad",
        "generation": 1,
        "x": 1, "y": 0,
        "tier": "dad",
        "profile": "JOHN",
    },
    # Generation 2: Sisters (per Ivan: 3 separate sisters)
    "Luana Weiss": {
        "role": "Sister (24)",
        "generation": 2,
        "x": -3, "y": 1,
        "tier": "child",
        "profile": "LUANA",
    },
    "Saskia Weiss": {
        "role": "Sister",
        "generation": 2,
        "x": -1, "y": 1,
        "tier": "child",
        "profile": "SASKIA",
        "uncertain": "No 1-on-1 chat in corpus",
    },
    "Kyrian 'Kiki' Weiss": {
        "role": "Sister (a.k.a. Kiki)",
        "generation": 2,
        "x": 1, "y": 1,
        "tier": "child",
        "profile": "KIKI_WEISS_HERMANA",
    },
    "Micaela 'Mica' Weiss Coëhn": {
        "role": "Cousin",
        "generation": 2,
        "x": 3, "y": 1,
        "tier": "child",
        "profile": "PRIMA_MIKAELA_WEISS",
    },
    # Grandparents (dad's side)
    "Riet van der Pol": {
        "role": "Grandma",
        "generation": 0,
        "x": 1, "y": -1,
        "tier": "grand",
        "profile": "RIET_VAN_DER_POL",
    },
    "Jan van der Pol": {
        "role": "Grandpa (deceased)",
        "generation": 0,
        "x": 2, "y": -1,
        "tier": "grand",
        "profile": "JAN_VAN_DER_POL",
    },
    # Mom's siblings (uncles/aunts)
    "Antonio 'Toni' López Weiss": {
        "role": "Uncle (USA)",
        "generation": 1,
        "x": -4, "y": -1,
        "tier": "uncle",
        "profile": "TONI_WEISS",
    },
    "Gerold Manders": {
        "role": "Uncle (adoptive, dad's)",
        "generation": 1,
        "x": 4, "y": -1,
        "tier": "uncle",
        "profile": "GEROLD_MANDERS",
    },
    # Spouse's connections
    "Anna Rodas van der Pol": {
        "role": "Family (van der Pol)",
        "generation": 1,
        "x": 2, "y": 1,
        "tier": "extended",
        "profile": "ANNA_RODAS_VAN_DER_POL",
    },
    "Alexander van der Pol": {
        "role": "Family (van der Pol)",
        "generation": 1,
        "x": 3, "y": 1,
        "tier": "extended",
        "profile": "ALEXANDER_VAN_DER_POL",
    },
}

# Layout
NODE_W = 200
NODE_H = 60
COL_W = 260  # spacing between columns
ROW_H = 100  # spacing between rows

def gen_x(g, x):
    return 40 + x * COL_W

def gen_y(y):
    return 40 + y * ROW_H

def main():
    svg_parts = []
    svg_parts.append(f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Psycology — Family Tree</title>
<style>
  body {{ margin: 0; padding: 24px; background: #0a0a0a; color: #d4d4d4; font-family: system-ui, sans-serif; }}
  h1 {{ color: #58c4dc; font-size: 16px; text-transform: uppercase; letter-spacing: 0.05em; }}
  h2 {{ color: #d4d4d4; font-size: 13px; margin-top: 24px; border-bottom: 1px solid #2a2a2a; padding-bottom: 4px; }}
  .legend {{ display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 16px; font-size: 12px; }}
  .legend-item {{ display: flex; align-items: center; gap: 6px; }}
  .legend-swatch {{ width: 12px; height: 12px; border-radius: 2px; }}
  .tree-container {{ background: #111; border: 1px solid #2a2a2a; border-radius: 4px; padding: 16px; overflow-x: auto; }}
  svg {{ display: block; }}
  .node rect {{ stroke-width: 2; }}
  .node.mom rect {{ fill: #2d1f1f; stroke: #d97e3a; }}
  .node.dad rect {{ fill: #1f2d2d; stroke: #79c0ff; }}
  .node.child rect {{ fill: #1a1a1a; stroke: #98c379; }}
  .node.grand rect {{ fill: #1a1a1a; stroke: #707070; stroke-dasharray: 4 2; }}
  .node.uncle rect {{ fill: #1a1a1a; stroke: #c678dd; stroke-dasharray: 4 2; }}
  .node.extended rect {{ fill: #1a1a1a; stroke: #707070; }}
  .node text {{ fill: #d4d4d4; font-size: 12px; }}
  .node text.role {{ fill: #79c0ff; font-size: 10px; font-style: italic; }}
  .node text.uncertain {{ fill: #d97e3a; font-size: 9px; font-style: italic; }}
  .node a {{ fill: #58c4dc; text-decoration: none; }}
  .connector {{ stroke: #404040; stroke-width: 1.5; fill: none; }}
  .gen-label {{ fill: #707070; font-size: 10px; font-style: italic; }}
</style>
</head>
<body>
<h1>Psycology — Family Tree</h1>
<p style="color:#707070;font-size:12px">Verified family relationships from <a href="https://github.com/IvanWeissVanDerPol/psycology/tree/master/docs/identity-corrections" style="color:#58c4dc">docs/identity-corrections/</a> + full vCard export (2026-07-23)</p>

<div class="legend">
  <div class="legend-item"><div class="legend-swatch" style="background:#2d1f1f;border:2px solid #d97e3a"></div>Mom</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#1f2d2d;border:2px solid #79c0ff"></div>Dad</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#1a1a1a;border:2px solid #98c379"></div>Sibling</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#1a1a1a;border:2px dashed #707070"></div>Grandparent</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#1a1a1a;border:2px dashed #c678dd"></div>Uncle/Aunt</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#1a1a1a;border:2px solid #707070"></div>Extended family</div>
  <div class="legend-item" style="color:#d97e3a">● uncertain / open question</div>
</div>

<div class="tree-container">
<svg width="{40 + 7 * COL_W + NODE_W}" height="{40 + 3 * ROW_H + NODE_H}" xmlns="http://www.w3.org/2000/svg">
''')
    
    # Generation labels
    for y, label in [(-1, "Grandparents"), (0, "Parents"), (1, "Children"), (2, "Extended")]:
        if any(n["generation"] == y or (y == 0 and n["generation"] == 1) for n in FAMILY.values()):
            svg_parts.append(f'<text class="gen-label" x="20" y="{gen_y(y) + 30}">{label}</text>')
    
    # Draw connectors (parent-child)
    def draw_connector(parent, child):
        px = gen_x(parent["generation"] if "generation" in parent else parent.get("x", 0), parent["x"]) + NODE_W // 2
        py = gen_y(parent["y"]) + NODE_H
        cx = gen_x(child["generation"] if "generation" in child else child.get("x", 0), child["x"]) + NODE_W // 2
        cy = gen_y(child["y"])
        if abs(px - cx) < 5:
            svg_parts.append(f'<line class="connector" x1="{px}" y1="{py}" x2="{cx}" y2="{cy}"/>')
        else:
            midy = (py + cy) // 2
            svg_parts.append(f'<path class="connector" d="M {px} {py} L {px} {midy} L {cx} {midy} L {cx} {cy}"/>')
    
    # Mom → all siblings
    mom = FAMILY["Sonia Edith Weiss López"]
    dad = FAMILY["John van der Pol"]
    for child_name in ["Luana Weiss", "Saskia Weiss", "Kyrian 'Kiki' Weiss", "Micaela 'Mica' Weiss Coëhn"]:
        draw_connector(mom, FAMILY[child_name])
        draw_connector(dad, FAMILY[child_name])
    
    # Mom → her siblings (uncles)
    for uncle in ["Antonio 'Toni' López Weiss"]:
        draw_connector(mom, FAMILY[uncle])
    # Dad → his brothers
    for uncle in ["Gerold Manders"]:
        draw_connector(dad, FAMILY[uncle])
    
    # Grandparents → Dad
    draw_connector(FAMILY["Riet van der Pol"], dad)
    draw_connector(FAMILY["Jan van der Pol"], dad)
    
    # Draw nodes
    for name, info in FAMILY.items():
        x = gen_x(info["generation"], info["x"])
        y = gen_y(info["y"])
        tier = info["tier"]
        profile_path = info["profile"]
        uncertain = info.get("uncertain", "")
        
        uncertain_y = 0
        if uncertain:
            uncertain_y = 12
            svg_parts.append(f'<text class="uncertain" x="{x}" y="{y + 50}">⚠ {uncertain}</text>')
        
        svg_parts.append(f'''<g class="node {tier}">
  <rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" rx="4"/>
  <text x="{x + 10}" y="{y + 20}" font-weight="500">{name}</text>
  <text x="{x + 10}" y="{y + 36}" class="role">{info["role"]}</text>
  <text x="{x + 10}" y="{y + 56 - uncertain_y}" font-size="10"><a href="https://github.com/IvanWeissVanDerPol/psycology/blob/master/RELATIONSHIPS/dynamics/{profile_path}.md">→ profile</a></text>
</g>''')
    
    # Footer notes
    svg_parts.append('</svg></div>')
    svg_parts.append('''
<h2>Open questions / unresolved</h2>
<ul style="font-size:13px;line-height:1.6">
  <li><strong>Saskia's brother (JID 595985725871)</strong>: vCard labels as "Saskia Weiss" but chat content shows the contact identifies as "Soy el hermano mayor de saskia". Either vCard is wrong or Ivan was wrong about "Saskia has no 1-on-1 chat". Awaiting Ivan.</li>
  <li><strong>3 friends named Luana</strong>: Not in vCard, no self-intro in corpus. Awaiting Ivan's JIDs or contexts.</li>
  <li><strong>Mom's siblings Carlú/Julio/Roberto</strong>: Referenced in family tree but not yet identified in chats.</li>
</ul>

<h2>Verified (2026-07-23 family corrections)</h2>
<ul style="font-size:13px;line-height:1.6">
  <li><strong>Kiki = Kyrian</strong> (3rd sister, NOT Saskia) — JID 595985724135</li>
  <li><strong>Saskia = separate sister</strong> (no 1-on-1 chat, only group appearances)</li>
  <li><strong>3 sisters</strong>: Luana (24), Saskia, Kyrian "Kiki" — confirmed separate</li>
  <li><strong>Toni Weiss</strong> = uncle (mom's brother), NOT dad</li>
  <li><strong>John van der Pol</strong> = dad (not Toni as previously labeled)</li>
</ul>
</body></html>''')
    
    out = REPO / "SOURCE_OF_TRUTH" / "wa_messages" / "_ANALYSIS" / "family_tree.html"
    out.write_text("\n".join(svg_parts))
    print(f"Wrote {out.relative_to(REPO)} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
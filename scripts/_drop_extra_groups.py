"""
Second-pass group filter: keep only the 12 groups Ivan hand-selected,
move every other _wa_group_* dir into _dropped/ .
Reversible.

Run:  python3 _drop_extra_groups.py            # dry run
      python3 _drop_extra_groups.py --yes      # execute
"""

import sys
import shutil
from pathlib import Path

BASE = Path(__file__).parent
DROPPED = BASE / "_dropped"

KEEP = {
    # active
    "_wa_group_weiss_siblings_530",
    "_wa_group_grupo_destrucción_aregua_cityyyyyyyyy_3077",
    "_wa_group_mansion_weiss_5844",
    "_wa_group_ritual_de_cuerdas_13127",
    "_wa_group_road_trip_spring_break_2902",
    "_wa_group_consejo_de_emergencia_16927",
    "_wa_group_epic_musical_juntadas_15561",
    "_wa_group_weiss_house_2488",
    "_wa_group_cumple_iván_3225",
    # lurker
    "_wa_group_flia_weiss_van_der_pol_443",
    "_wa_group_kansas_trip_1931",
    "_wa_group_ueno_bank_la_gang_3082",
}

on_disk = sorted(p.name for p in BASE.glob("_wa_group_*") if p.is_dir())
to_drop = [n for n in on_disk if n not in KEEP]
missing_keep = sorted(KEEP - set(on_disk))

print(f"on-disk groups: {len(on_disk)}  |  keep: {len(KEEP)}  |  drop: {len(to_drop)}")
if missing_keep:
    print(f"WARNING: {len(missing_keep)} keep-slugs not on disk:")
    for s in missing_keep:
        print(f"  MISSING: {s}")

if "--yes" not in sys.argv:
    print("Dry-run. Pass --yes to actually move.")
    for s in to_drop[:5]:
        print(f"  would move: {s}  ->  _dropped/{s}")
    if len(to_drop) > 5:
        print(f"  ... and {len(to_drop)-5} more")
    sys.exit(0)

DROPPED.mkdir(exist_ok=True)
moved = 0
for s in to_drop:
    src = BASE / s
    dst = DROPPED / s
    if dst.exists():
        print(f"skip (dest exists): {s}")
        continue
    shutil.move(str(src), str(dst))
    moved += 1
print(f"Moved {moved} groups into {DROPPED}")

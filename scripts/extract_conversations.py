#!/usr/bin/env python3
"""Extract conversations from COMMITTED tier1/tier2 dirs (reads from git show)."""

import json
import subprocess
from pathlib import Path

out_base = Path("SOURCE_OF_TRUTH/wa_messages/_conversations")
out_base.mkdir(exist_ok=True)


def get_committed_dirs(subpath):
    r = subprocess.run(
        ["git", "ls-tree", "--name-only", "HEAD", f"SOURCE_OF_TRUTH/wa_messages/{subpath}/"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent,
    )
    return [f for f in r.stdout.strip().split("\n") if f]


tier1 = get_committed_dirs("tier1_deep")
tier2 = get_committed_dirs("tier2_core")

seen = {}
for name in sorted(set(tier1 + tier2)):
    tier = "tier1_deep" if name.startswith(("01__", "02__")) else "tier2_core"
    key = name.rsplit("__", 1)[-1].split("___wa_chat")[0] if "__" in name else name
    if key in seen:
        print(f"SKIP dup: {name}")
        continue
    seen[key] = name
    r = subprocess.run(
        ["git", "show", f"HEAD:SOURCE_OF_TRUTH/wa_messages/{tier}/{name}/messages.json"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent,
    )
    if r.returncode:
        print(f"ERROR: {name}")
        continue
    try:
        data = json.loads(r.stdout)
    except Exception as e:
        print(f"JSON ERR {name}: {e}")
        continue
    lines = [f"# {name}", ""]
    for m in data.get("messages", []):
        t = m.get("text", "")
        if not t:
            continue
        ts = m.get("ts_iso", "")[:19]
        if m.get("from_me"):
            lines.append(f"[{ts}] Ivan: {t}")
        else:
            s = (m.get("sender_jid") or "them").split("@")[0]
            lines.append(f"[{ts}] {s}: {t}")
    (out_base / f"{name}.txt").write_text("\n".join(lines))
    print(f"{name}: {len(lines)} lines")

print(f"\n{len(seen)} unique conversations")

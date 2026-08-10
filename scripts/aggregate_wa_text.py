#!/usr/bin/env python3
"""Parse a Messaging text export, keep only Ivan's messages (sender=weissvanderpol),
coalesce per date, and write transcripts.json in the shape extract_psychology expects.

Usage:
  aggregate_wa_text.py <path/to/Messaging Chat with X.txt> <output_dir>
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

LINE_RE = re.compile(
    r"^(?P<m>\d{1,2})/(?P<d>\d{1,2})/(?P<y>\d{2}),\s+"
    r"(?P<hh>\d{1,2}):(?P<mm>\d{2})\s*(?P<ampm>AM|PM)\s*-\s*"
    r"(?P<sender>[^:]+?):\s*(?P<msg>.*)$"
)
IVAN_SENDER = "weissvanderpol"


def normalize_date(y: str, m: str, d: str) -> str:
    year = int(y)
    year = 2000 + year if year < 70 else 1900 + year
    return f"{year:04d}-{int(m):02d}-{int(d):02d}"


def parse(src: Path):
    per_day = defaultdict(list)
    current_date = None
    current_sender = None
    current_buf = []

    def flush():
        nonlocal current_buf, current_date, current_sender
        if current_sender == IVAN_SENDER and current_buf and current_date:
            joined = " ".join(x.strip() for x in current_buf if x.strip())
            if joined and joined not in ("<Media omitted>", "null", "<This message was edited>"):
                per_day[current_date].append(joined)
        current_buf = []

    for raw in src.read_text(encoding="utf-8", errors="replace").splitlines():
        m = LINE_RE.match(raw)
        if m:
            flush()
            current_date = normalize_date(m.group("y"), m.group("m"), m.group("d"))
            current_sender = m.group("sender").strip()
            current_buf = [m.group("msg")]
        else:
            if current_sender is not None:
                current_buf.append(raw)
    flush()
    return per_day


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    src = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)

    per_day = parse(src)
    entries = []
    for date in sorted(per_day.keys()):
        msgs = per_day[date]
        text = "\n".join(msgs)
        entries.append(
            {
                "file": f"{src.stem}__{date}.txt",
                "date": date,
                "text": text,
                "duration": None,
                "language": "es",
            }
        )

    out_path = out_dir / "transcripts.json"
    out_path.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    total_msgs = sum(len(v) for v in per_day.values())
    print(f"Wrote {len(entries)} day-entries ({total_msgs} Ivan messages) to {out_path}")


if __name__ == "__main__":
    main()

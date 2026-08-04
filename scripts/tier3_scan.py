#!/usr/bin/env python3
import json
import os
from pathlib import Path

base = Path("SOURCE_OF_TRUTH/wa_messages/tier3_extended")
dirs = sorted(os.listdir(base))

batch = int(os.environ.get("BATCH", "0"))
batch_size = 15
start = batch * batch_size
end = start + batch_size
dirs_batch = dirs[start:end]

print(f"=== BATCH {batch} (dirs {start}-{end-1}) ===\n")

for d in dirs_batch:
    msg_path = base / d / "messages.json"
    if not msg_path.exists():
        print(f"{d}: NO_MESSAGES\n")
        continue
    try:
        with open(msg_path) as f:
            data = json.load(f)
        if isinstance(data, list):
            msgs = data
        elif isinstance(data, dict):
            msgs = data.get("messages", data.get("data", []))
            if not msgs and "chat_id" in data:
                print(
                    f"{d}: METADATA_ONLY (chat_id={data.get('chat_id')}, subject={data.get('subject')})\n"
                )
                continue
        else:
            print(f"{d}: UNKNOWN_FORMAT\n")
            continue
        if not msgs:
            print(f"{d}: EMPTY_MESSAGES\n")
            continue
        first = msgs[0].get("text", "") or msgs[0].get("content", "") or str(msgs[0])[:70]
        last = msgs[-1].get("text", "") or msgs[-1].get("content", "") or str(msgs[-1])[:70]
        count = len(msgs)
        ts_first = msgs[0].get("timestamp", "")[:10] if msgs else ""
        ts_last = msgs[-1].get("timestamp", "")[:10] if msgs else ""
        print(f"### {d}")
        print(f"count={count} | {ts_first} -> {ts_last}")
        print(f"first: {first[:70]}")
        print(f"last:  {last[:70]}")
        print()
    except Exception as e:
        print(f"{d}: ERROR {e}\n")

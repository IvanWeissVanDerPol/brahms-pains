#!/usr/bin/env python3
"""In-place credential scrubber for SOURCE_OF_TRUTH/wa_messages/*.

Ivan pasted .env files, API keystores, and service-account JSON into his
own WhatsApp chats over the years. We keep the psychology-analytic value
of the surrounding conversational context; we do not commit the secrets.

Two-tier strategy:

  1. NUKE_PATTERNS — if a message body contains any of these markers
     (PEM private-key header, GCP service-account JSON), the ENTIRE
     message text is replaced with a redaction marker. These
     messages are pasted blobs, not conversation.

  2. LINE_PATTERNS — otherwise, per-line scan. Any line matching one
     of the high-confidence secret regexes is replaced with
     "[REDACTED_SECRET_LINE]". Surrounding context lines survive.

Writes a per-chat scrub log to _scrub_report.json at the root and
mutates messages.json files atomically (.tmp + replace).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path("/home/ai-whisperers/psychology-integration/psycology/SOURCE_OF_TRUTH/wa_messages")

NUKE_PATTERNS = {
    "gcp_sa_pk": re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----"),
    "gcp_sa_json": re.compile(r'"type"\s*:\s*"service_account"'),
}

LINE_PATTERNS = {
    "aws_akid": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "aws_secret": re.compile(
        r"aws(.{0,20})?(secret|key)[^\n]{0,10}['\"][A-Za-z0-9/+=]{40}['\"]", re.I
    ),
    "slack_token": re.compile(r"\bxox[abpr]-[A-Za-z0-9-]{10,}"),
    "github_pat": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"),
    "openai_key": re.compile(r"\bsk-(proj-)?[A-Za-z0-9_-]{20,}\b"),
    "anthropic_key": re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}\b"),
    "stripe_key": re.compile(r"\b(sk|pk|rk)_(live|test)_[A-Za-z0-9]{20,}\b"),
    "google_api": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    "jwt": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    "telegram_bot": re.compile(r"\b\d{8,11}:[A-Za-z0-9_-]{35}\b"),
    "db_url_creds": re.compile(
        r"\b(postgres|postgresql|mongodb|mongodb\+srv|mysql|redis)://[^:@\s/]+:[^@\s]+@"
    ),
    "generic_secret_kv": re.compile(
        r"\b(password|passwd|passphrase|api[_-]?key|secret|token|bearer|access_key|private_key|client_secret)\s*[:=]\s*['\"][^'\"\s]{16,}['\"]",
        re.I,
    ),
    "unquoted_env_secret": re.compile(
        r"\b(API[_-]?KEY|SECRET|TOKEN|PASSWORD|PASSWD|PASSPHRASE|PRIVATE[_-]?KEY|ACCESS[_-]?KEY|CLIENT[_-]?SECRET|AUTH[_-]?TOKEN)\s*=\s*[A-Za-z0-9._+/=-]{16,}"
    ),
    "env_bot_token": re.compile(r"\b[A-Z][A-Z_]*BOT[_-]?TOKEN\s*=\s*\S{16,}", re.I),
}


def scrub_text(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    # Tier 1: full-message nuke if any NUKE_PATTERNS hit
    for name, rgx in NUKE_PATTERNS.items():
        if rgx.search(text):
            counts[f"NUKE:{name}"] = 1
            return "[REDACTED_MESSAGE_CONTAINS_CREDENTIAL_DUMP]", counts

    # Tier 2: per-line redaction
    lines = text.split("\n")
    new_lines: list[str] = []
    for line in lines:
        matched = None
        for name, rgx in LINE_PATTERNS.items():
            if rgx.search(line):
                matched = name
                break
        if matched:
            counts[matched] = counts.get(matched, 0) + 1
            new_lines.append("[REDACTED_SECRET_LINE]")
        else:
            new_lines.append(line)
    return ("\n".join(new_lines), counts) if counts else (text, counts)


def main() -> int:
    total_files_touched = 0
    total_msgs_scrubbed = 0
    total_hits: dict[str, int] = {}
    per_chat: list[dict] = []

    for messages_json in sorted(ROOT.rglob("messages.json")):
        with open(messages_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        touched = 0
        chat_hits: dict[str, int] = {}
        for msg in data.get("messages", []):
            text = msg.get("text")
            if not text:
                continue
            new_text, counts = scrub_text(text)
            if counts:
                msg["text"] = new_text
                touched += 1
                for k, v in counts.items():
                    chat_hits[k] = chat_hits.get(k, 0) + v
                    total_hits[k] = total_hits.get(k, 0) + v

        if touched:
            tmp = messages_json.with_suffix(".json.tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=1)
            tmp.replace(messages_json)
            total_files_touched += 1
            total_msgs_scrubbed += touched
            per_chat.append(
                {
                    "chat": str(messages_json.relative_to(ROOT)),
                    "messages_scrubbed": touched,
                    "hits_by_pattern": chat_hits,
                }
            )

    report = {
        "files_touched": total_files_touched,
        "messages_scrubbed": total_msgs_scrubbed,
        "hits_by_pattern": total_hits,
        "chats": sorted(per_chat, key=lambda x: -x["messages_scrubbed"]),
    }
    with open(ROOT / "_scrub_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)

    print(f"files touched: {total_files_touched}")
    print(f"messages scrubbed: {total_msgs_scrubbed}")
    print("hits by pattern:")
    for k, v in sorted(total_hits.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

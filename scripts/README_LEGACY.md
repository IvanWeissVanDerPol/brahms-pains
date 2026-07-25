# scripts/

Analysis and QA helpers for the psychology corpus.
For actual transcription, use the unified CLI: `python src/transcribe.py --help`.

## Active scripts

| Script | Purpose |
|--------|---------|
| `analyze_transcripts.py`             | Aggregate stats across transcript JSON files |
| `check_quality.py`                   | Flag likely bad/garbled transcripts |
| `deep_psychological_extraction.py`   | Structured extraction pass over selected chats |
| `extract_curated_quotes.py`          | Pull citation-quality quotes into `SOURCE_OF_TRUTH/CURATED_QUOTES.md` |
| `find_missed_insights.py`            | Second-pass sweep for content the extraction missed |
| `get_specific_transcript.py`         | Fetch a single transcript by ID for inspection |

## Setup

```bash
pip install -r requirements.txt
```

Installs `openai-whisper`, `torch`, and `tqdm`. First transcription run downloads
the Whisper model (~140 MB for `base`, more for larger sizes).

## Transcription — use the unified CLI

The one-off `transcribe_*.py` / `retranscribe_*.py` variants that used to live
here have been retired into `_legacy/`. All new work goes through:

```bash
python src/transcribe.py --help
```

Covers per-chat runs, resume, model selection, parallelism, and quality retries.

## Troubleshooting

- **`CUDA out of memory`** — use a smaller model (`--model tiny` or `base`).
- **`ffmpeg not found`** — Linux: `apt install ffmpeg`, Mac: `brew install ffmpeg`.
- **CPU transcription is slow** — expected; run overnight or use GPU.

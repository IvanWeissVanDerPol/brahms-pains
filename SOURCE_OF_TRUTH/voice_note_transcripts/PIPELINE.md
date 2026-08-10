# Whisper Pipeline — Quickstart

Transcribes Ivan's Messaging voice notes (`.opus` files in `media/audio/`) into plain transcripts. The pipeline is **resumable**: every run skips already-transcribed files, so you can interrupt anytime.

## What you get

- **14,809 voice notes** (`.opus` format) live under `media/audio/{chat_dir}/PTT-YYYYMMDD-WAnnnn.opus` (249 chats).
- **After each run:** new entries appear in `SOURCE_OF_TRUTH/voice_note_transcripts/{chat}/transcripts.txt` (human) and `transcripts.json` (machine).
- **Existing transcripts** (1,175 PTTs) are preserved.

## Pick a backend

| Backend | Cost | Speed (full corpus) | Setup effort |
|---|---|---|---|
| **OpenAI Cloud** | $25 (~$0.006/min × 70 hrs) | ~30 min queue time | `export OPENAI_API_KEY=sk-...` |
| **faster-whisper CPU** | $0 | ~1.7 hours | `pip install faster-whisper` |
| **faster-whisper GPU** | $0 | ~15 min | GPU + CUDA + above |
| **whisper.cpp CPU** | $0 | ~2 hours | `bash scripts/install_whisper.sh --whisper-cpp` |
| **whisper.cpp CUDA** | $0 | ~10 min | GPU + above |

**Recommended for Lua's Linux Mint box**: faster-whisper CPU (`medium` model). Free, fast enough, no API costs.

## Install

```bash
cd /path/to/psycology
bash scripts/install_whisper.sh --local-cpu
```

This installs `faster-whisper` and confirms ffmpeg is present. For GPU support:

```bash
bash scripts/install_whisper.sh --local-gpu   # if you have NVIDIA
```

For cloud (cheapest):

```bash
export OPENAI_API_KEY=sk-...
```

## Run

Dry-run first to see what's queued:

```bash
python3 scripts/transcribe_audio.py --dry-run
```

Then run for real. Suggested starter:

```bash
# 4 workers, medium model, free local. Ctrl-C safe — re-runnable.
python3 scripts/transcribe_audio.py --workers 4 --backend faster --model medium
```

To use the cloud:

```bash
python3 scripts/transcribe_audio.py --workers 4 --backend openai
```

To smoke-test the whole pipeline:

```bash
python3 scripts/transcribe_audio.py --smoke-test
```

To transcribe one specific voice note:

```bash
python3 scripts/transcribe_audio.py --ptt-id PTT-20240314-WA0019
```

To run overnight:

```bash
nohup python3 scripts/transcribe_audio.py --workers 8 --backend faster --model medium \
    > run_$(date +%Y%m%d_%H%M).out 2>&1 &
```

## Output location

For each audio dir like `media/audio/_wa_chat_595981225272_62/`, transcripts land at:

```
SOURCE_OF_TRUTH/voice_note_transcripts/chat_595981225272_62/
    transcripts.txt   human-readable
    transcripts.json  machine-readable (segments[] with timestamps)
    PTT-*.FAILED      files that Whisper errored on (skipped on next run)
```

The `run.log` lives at `SOURCE_OF_TRUTH/voice_note_transcripts/run.log` and has one line per file with timestamp.

## Embedding transcripts into the corpus (Track C)

Once transcripts are written, the conversation viewer (`viewer.html`) auto-picks them up. No extra step.

## Estimating time on this corpus

- **Total audio**: ~14,809 files × ~17s avg = **70 hours** of audio.
- **Whisper-tiny** on local CPU: ~52 min total (weakest accuracy).
- **Whisper-medium** on local CPU: ~1.7 hours (recommended, handles Spanish/Guaraní).
- **Whisper-large-v3** on local CPU: ~3.5 hours (best accuracy for tricky speech).
- **Cloud OpenAI Whisper**: ~30 min wall time (rate limits apply, ~$25).

## FAQ

**Q. Audio dir doesn't exist?**
A. Means voice notes haven't been extracted yet. Run the Messaging extractor first.

**Q. Failed file keeps failing?**
A. The `.FAILED` marker prevents infinite retries. Delete the marker to retry; or run with `--retry-all`.

**Q. How do I redact a transcript?**
A. Edit the corresponding `.txt` (and `.json` in lockstep) by hand. The smoke-test reads both.

**Q. Can I run multiple machines?**
A. Yes — the pipeline is keyed by `PTT-*.opus` filenames. Two machines will split the work safely as long as each only writes to its own outputs.

## What to do next

1. `bash scripts/install_whisper.sh --local-cpu` (or set `OPENAI_API_KEY`)
2. `python3 scripts/transcribe_audio.py --dry-run` (verify counts)
3. `python3 scripts/transcribe_audio.py --workers 4 --backend faster --model medium` (start)
4. Walk away. The full corpus takes ~2 hours on CPU.
5. Meanwhile, give Track A's `CONTACTS_NAMING_VERIFY.md` a review and confirm a few names.
6. When the viewer is built (Track C), open `viewer.html` and pick any chat — transcripts are inline with the audio.

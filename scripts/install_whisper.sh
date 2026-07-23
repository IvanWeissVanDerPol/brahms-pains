#!/usr/bin/env bash
# Install a Whisper backend for the psycology voice-note pipeline.
# Lua runs this on her workstation.
#
# Modes:
#   --cloud        (no install needed; export OPENAI_API_KEY before running)
#   --local-cpu    (recommended; faster-whisper, runs on CPU)
#   --local-gpu    (faster-whisper + CUDA, requires NVIDIA GPU)
#   --whisper-cpp  (best performance; builds from source)
#
# Default: --local-cpu

set -euo pipefail

MODE="${1:---local-cpu}"

echo "╭─────────────────────────────────────────────────────╮"
echo "│  Whisper install helper — psycology voice pipeline  │"
echo "╰─────────────────────────────────────────────────────╯"
echo

# Sanity checks
if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ python3 not found."
    exit 1
fi

PYV=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ python3 found: $PYV"
if [ "$(echo "$PYV < 3.9" | bc)" = "1" ]; then
    echo "⚠️  python < 3.9 — Whisper needs >= 3.9"
fi

if command -v ffmpeg >/dev/null 2>&1; then
    FFMPEG_V=$(ffmpeg -version 2>&1 | head -1 | awk '{print $3}')
    echo "✅ ffmpeg found: $FFMPEG_V"
else
    echo "⚠️  ffmpeg not found — needed for audio decoding"
    echo "    Install with: sudo apt install -y ffmpeg"
fi

# Detect CUDA
HAS_CUDA=0
if command -v nvcc >/dev/null 2>&1 || command -v nvidia-smi >/dev/null 2>&1; then
    HAS_CUDA=1
    echo "✅ CUDA-capable GPU detected"
fi

case "$MODE" in
    --cloud)
        echo
        echo "CLOUD MODE: no install needed"
        echo "Set your API key before running:"
        echo "    export OPENAI_API_KEY=sk-..."
        echo "Then:"
        echo "    python3 scripts/transcribe_audio.py --backend openai"
        ;;

    --local-cpu|--local-gpu)
        echo
        echo "Installing faster-whisper..."
        python3 -m pip install --upgrade pip
        python3 -m pip install faster-whisper

        # Optional GPU support
        if [ "$MODE" = "--local-gpu" ] && [ "$HAS_CUDA" = "1" ]; then
            echo "Installing CUDA-enabled faster-whisper..."
            python3 -m pip install faster-whisper[cuda]
        fi

        echo
        echo "✅ Done. Verifying..."
        python3 -c "import faster_whisper; print('faster-whisper:', faster_whisper.__file__)"

        echo
        echo "Recommended model: 'medium' (good for Spanish/Guaraní)"
        echo "Usage:"
        echo "    python3 scripts/transcribe_audio.py --workers 4 --backend faster --model medium"
        echo
        echo "One-liner (start transcription, resume-safe):"
        echo "    nohup python3 scripts/transcribe_audio.py --workers 8 --backend faster --model medium > run.out 2>&1 &"
        ;;

    --whisper-cpp)
        echo
        echo "Installing whisper.cpp for max performance..."
        if ! command -v git >/dev/null 2>&1; then
            echo "❌ git not found"
            exit 1
        fi
        WORK=/tmp/whisper-cpp-build
        if [ ! -d "$WORK" ]; then
            git clone https://github.com/ggerganov/whisper.cpp.git "$WORK"
        fi
        cd "$WORK"
        # Pick the appropriate compile flags based on GPU
        if [ "$HAS_CUDA" = "1" ]; then
            WHISPER_CUDA=1 make -j"$(nproc)"
        else
            make -j"$(nproc)"
        fi
        # Download the model
        mkdir -p ~/.cache/whisper
        if [ ! -f ~/.cache/whisper/medium.bin ]; then
            bash ./models/download-ggml-model.sh medium
            cp ./models/ggml-medium.bin ~/.cache/whisper/medium.bin
        fi
        sudo cp ./main /usr/local/bin/whisper-cli 2>/dev/null || cp ./main "$HOME/.local/bin/whisper-cli"
        echo "✅ whisper.cpp installed at $WORK, binary at ~/.local/bin/whisper-cli"
        echo
        echo "Usage:"
        echo "    python3 scripts/transcribe_audio.py --backend whisper-cpp --model medium"
        ;;

    *)
        echo "Unknown mode: $MODE"
        echo "Usage: $0 [--cloud | --local-cpu | --local-gpu | --whisper-cpp]"
        exit 1
        ;;
esac

echo
echo "Done. Run a smoke test:"
echo "    python3 scripts/transcribe_audio.py --smoke-test"

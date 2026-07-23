#!/bin/bash
# Split the corpus into N shards and run a separate Python process per shard.
# Each process loads its own Whisper model, so we get true parallelism.
#
# Usage: parallel_whisper.sh <shards> <workers_per_shard> <model>
#
# Default: 4 shards × 2 workers × medium model = 8 effective workers

set -e

SHARDS=${1:-4}
WORKERS=${2:-2}
MODEL=${3:-medium}

echo "=== Parallel Whisper — $SHARDS shards × $WORKERS workers = $((SHARDS * WORKERS)) effective ==="

# Split the PTT-IDs into N buckets deterministically
ALL_PTTS=$(find /root/psycology/media/audio -name "*.opus" 2>/dev/null | sed 's|.*/||;s/.opus$//' | sort -u)
TOTAL=$(echo "$ALL_PTTS" | wc -l)
PER_SHARD=$((TOTAL / SHARDS))
echo "Total files: $TOTAL, per shard: $PER_SHARD"

mkdir -p /tmp/whisper_shards
PIDS=()

for i in $(seq 0 $((SHARDS - 1))); do
    START=$((i * PER_SHARD + 1))
    END=$(((i + 1) * PER_SHARD))
    if [ $i -eq $((SHARDS - 1)) ]; then
        END=$TOTAL
    fi

    LIST_FILE=/tmp/whisper_shards/shard_$i.txt
    echo "$ALL_PTTS" | sed -n "${START},${END}p" > "$LIST_FILE"
    SHARD_COUNT=$(wc -l < "$LIST_FILE")
    echo "  shard $i: lines $START-$END ($SHARD_COUNT files)"

    (
        # Transcribe each PTT-ID in this shard
        cd /root/psycology
        while read ptt_id; do
            # Skip if already done
            if grep -q "\"$ptt_id.opus\"" SOURCE_OF_TRUTH/voice_note_transcripts/*/transcripts.json 2>/dev/null; then
                continue
            fi
            python3 scripts/transcribe_audio.py --ptt-id "$ptt_id" --backend faster --model "$MODEL" 2>&1 | tail -1
        done < "$LIST_FILE"
    ) > /tmp/whisper_shards/shard_$i.log 2>&1 &
    PIDS+=($!)
done

echo ""
echo "Started ${#PIDS[@]} shards. PIDs: ${PIDS[*]}"
echo "Waiting for completion..."

# Wait for all shards
for pid in "${PIDS[@]}"; do
    wait "$pid"
done

echo "All shards done."
echo ""
echo "=== Per-shard summary ==="
for i in $(seq 0 $((SHARDS - 1))); do
    echo "--- shard $i ---"
    tail -5 /tmp/whisper_shards/shard_$i.log
done

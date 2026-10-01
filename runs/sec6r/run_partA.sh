#!/bin/bash
# SEC6R Part A (post hoc, seen data): SEC6's twelve through the frozen wrapper, three at a time; exits logged
cd "$(dirname "$0")/../.."
export PYTHONDONTWRITEBYTECODE=1
run() { i=$1; uv run python runs/sec6r/frozen/sec6r_score.py all $i --part A --out runs/sec6r/partA/results_$i.jsonl --times runs/sec6r/partA/times_$i.jsonl > runs/sec6r/partA/log_$i.txt 2>&1; echo "$i exit $? $(date -u +%FT%TZ)" >> runs/sec6r/partA/exits.txt; }
export -f run
echo "start $(date -u +%FT%TZ)" >> runs/sec6r/partA/exits.txt
printf "%s\n" 46584 46593 46597 46603 46652 46653 46676 46686 46708 46721 46737 46762 | xargs -P 3 -I{} bash -c 'run {}'
echo "done $(date -u +%FT%TZ)" >> runs/sec6r/partA/exits.txt

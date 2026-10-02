#!/bin/bash
# SEC6R Part B (held-out): the prereg's Reproduction loop, three carriers at a time; exits logged (runs/sec6r/exits.txt)
cd "$(dirname "$0")/../.."
export PYTHONDONTWRITEBYTECODE=1
run() { i=$1; uv run python runs/sec6r/frozen/sec6r_score.py all $i --part B --out runs/sec6r/results_$i.jsonl --times runs/sec6r/times_$i.jsonl > runs/sec6r/log_$i.txt 2>&1; echo "$i exit $? $(date -u +%FT%TZ)" >> runs/sec6r/exits.txt; }
export -f run
echo "start $(date -u +%FT%TZ)" >> runs/sec6r/exits.txt
printf "%s\n" 183 279 1534 1538 1542 1552 40985 46608 46684 46709 46745 46761 | xargs -P 3 -I{} bash -c 'run {}'
echo "done $(date -u +%FT%TZ)" >> runs/sec6r/exits.txt

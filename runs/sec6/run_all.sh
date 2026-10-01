#!/bin/bash
# SEC6 data step: the prereg's Reproduction loop, three carriers at a time; exit codes logged (runs/sec6/exits.txt)
cd "$(dirname "$0")/../.."
export PYTHONDONTWRITEBYTECODE=1
run() { i=$1; uv run python runs/sec6/frozen/sec6_score.py all $i --out runs/sec6/results_$i.jsonl --times runs/sec6/times_$i.jsonl > runs/sec6/log_$i.txt 2>&1; echo "$i exit $? $(date -u +%FT%TZ)" >> runs/sec6/exits.txt; }
export -f run
echo "start $(date -u +%FT%TZ)" >> runs/sec6/exits.txt
printf "%s\n" 46584 46593 46597 46603 46652 46653 46676 46686 46708 46721 46737 46762 | xargs -P 3 -I{} bash -c 'run {}'
echo "done $(date -u +%FT%TZ)" >> runs/sec6/exits.txt

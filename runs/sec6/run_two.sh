#!/bin/bash
cd "$(dirname "$0")/../.."
export PYTHONDONTWRITEBYTECODE=1
for i in 46686 46708; do uv run python runs/sec6/frozen/sec6_score.py all $i --out runs/sec6/results_$i.jsonl --times runs/sec6/times_$i.jsonl > runs/sec6/log_$i.txt 2>&1; echo "$i exit $? $(date -u +%FT%TZ) (re-run: the first was interrupted by the operator's kill)" >> runs/sec6/exits.txt; done &
wait

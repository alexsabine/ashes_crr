#!/usr/bin/env bash
# SEC7 development (prereg/sec7/DEV_DECLARATION.md): D-GATE-7 first, then (only if it is OPEN, and only when called with "run")
# D-RUN. Three carriers at a time; one JSON line per carrier in prereg/sec7/dev/; logs outside the repository.
#     nohup bash studies/sec7/dev_gate.sh gate > /dev/null 2>&1 &     # D-GATE-7: fixed grid (balanced), edge, clipped SEC
#     nohup bash studies/sec7/dev_gate.sh run  > /dev/null 2>&1 &     # D-RUN (after an OPEN gate), then dev_SEC7.txt
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$ROOT" || exit 1
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
STAGE="${1:-gate}"; DEV=prereg/sec7/dev; LOGS=/tmp/claude-0/sec7_dev_logs/$STAGE; STATUS="$DEV/status_$STAGE.txt"
mkdir -p "$DEV" "$LOGS"; rm -f "$LOGS"/exit_*.txt
echo "$STAGE started $(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$STATUS"
export STAGE
uv run python studies/sec7/sec7_score.py devlist | xargs -P 3 -L 1 bash -c \
  'uv run python studies/sec7/sec7_score.py dev$STAGE "$0" "$1" --out prereg/sec7/dev/${STAGE}_$0_$1.jsonl > /tmp/claude-0/sec7_dev_logs/$STAGE/$0_$1.log 2>&1; echo "$0 $1 exit $?" > /tmp/claude-0/sec7_dev_logs/$STAGE/exit_$0_$1.txt'
N=$(ls "$LOGS"/exit_*.txt | wc -l); BAD=$(cat "$LOGS"/exit_*.txt | grep -v "exit 0$" | tr '\n' ';')
if [ "$STAGE" = gate ]; then
  uv run python studies/sec7/sec7_score.py devgatereport "$DEV"/gate_*.jsonl > "$DEV/gate7.txt" 2> "$LOGS/report.err"
  uv run python studies/sec7/sec7_score.py devreport "$DEV/devid.txt" "$DEV/gate7.txt" "$DEV"/gate_*.jsonl > prereg/sec7/dev_SEC7.txt 2>> "$LOGS/report.err"
else
  uv run python studies/sec7/sec7_score.py devreport "$DEV/devid.txt" "$DEV/gate7.txt" "$DEV"/gate_*.jsonl "$DEV"/run_*.jsonl > prereg/sec7/dev_SEC7.txt 2> "$LOGS/report.err"
fi
echo "report exit $?; carriers run $N; non-zero exits: ${BAD:-none}" >> "$STATUS"
echo "DEV_DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$STATUS"

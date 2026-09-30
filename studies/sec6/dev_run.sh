#!/usr/bin/env bash
# SEC6 D-RUN (prereg/sec6/DEV_DECLARATION.md, development stage 3): the four published baselines (SI-1, SI-0.1, AR1-P, AR1-B)
# on the SEEN carriers of SCL3, SEC3, SEC4 and SEC5, seeds 0-4, two carriers at a time (the machine is shared), one JSON line
# per carrier in prereg/sec6/dev/; then prereg/sec6/dev_SEC6.txt from those lines and the pinned D-ID / D-MAP outputs
# (prereg/sec6/dev/devid.txt, devmap.txt, which must exist first). Logs go outside the repository. At the end
# prereg/sec6/dev/status.txt ends with DEV_DONE.
#     nohup bash studies/sec6/dev_run.sh > /dev/null 2>&1 &
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$ROOT" || exit 1
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
DEV=prereg/sec6/dev; LOGS=/tmp/claude-0/sec6_dev_logs
mkdir -p "$DEV" "$LOGS"; rm -f "$LOGS"/exit_*.txt
echo "D-RUN started $(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$DEV/status.txt"
uv run python studies/sec6/sec6_score.py devlist | xargs -P 2 -L 1 bash -c \
  'uv run python studies/sec6/sec6_score.py devone "$0" "$1" --out prereg/sec6/dev/dev_$0_$1.jsonl > /tmp/claude-0/sec6_dev_logs/dev_$0_$1.log 2>&1; echo "$0 $1 exit $?" > /tmp/claude-0/sec6_dev_logs/exit_$0_$1.txt'
N=$(ls "$LOGS"/exit_*.txt | wc -l); BAD=$(cat "$LOGS"/exit_*.txt | grep -v "exit 0$" | tr '\n' ';')
uv run python studies/sec6/sec6_score.py devreport "$DEV/devid.txt" "$DEV/devmap.txt" "$DEV"/dev_*.jsonl > prereg/sec6/dev_SEC6.txt 2> "$LOGS/devreport.err"
echo "devreport exit $?; carriers run $N; non-zero exits: ${BAD:-none}" >> "$DEV/status.txt"
echo "DEV_DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$DEV/status.txt"

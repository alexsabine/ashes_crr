#!/usr/bin/env bash
# SEC6 D-RUN (prereg/sec6/DEV_DECLARATION.md, development stage 3; Amendment 1): baseline arms on the SEEN carriers of SCL3,
# SEC3, SEC4 and SEC5, seeds 0-4, two carriers at a time (the machine is shared), one JSON line per carrier in
# prereg/sec6/dev/<prefix>_<study>_<id>.jsonl; then prereg/sec6/dev_SEC6.txt from every prereg/sec6/dev/dev*.jsonl (records
# of one carrier are merged by devreport) and the pinned D-ID / D-MAP outputs (prereg/sec6/dev/devid.txt, devmap.txt, which
# must exist first). Logs go outside the repository. At the end the status file ends with DEV_DONE.
#     nohup bash studies/sec6/dev_run.sh > /dev/null 2>&1 &                      # the four published baselines (run 1)
#     nohup bash studies/sec6/dev_run.sh si1c devsi1c > /dev/null 2>&1 &        # Amendment 1: SI-1C only (status_devsi1c.txt)
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$ROOT" || exit 1
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export ARMS="${1:-si1,si01,ar1p,ar1b}" PFX="${2:-dev}"
DEV=prereg/sec6/dev; LOGS=/tmp/claude-0/sec6_dev_logs/$PFX
STATUS="$DEV/status.txt"; [ "$PFX" != "dev" ] && STATUS="$DEV/status_$PFX.txt"
mkdir -p "$DEV" "$LOGS"; rm -f "$LOGS"/exit_*.txt
echo "D-RUN started $(date -u +%Y-%m-%dT%H:%M:%SZ); arms $ARMS" > "$STATUS"
uv run python studies/sec6/sec6_score.py devlist | xargs -P 2 -L 1 bash -c \
  'uv run python studies/sec6/sec6_score.py devone "$0" "$1" --arms "$ARMS" --out prereg/sec6/dev/${PFX}_$0_$1.jsonl > /tmp/claude-0/sec6_dev_logs/$PFX/dev_$0_$1.log 2>&1; echo "$0 $1 exit $?" > /tmp/claude-0/sec6_dev_logs/$PFX/exit_$0_$1.txt'
N=$(ls "$LOGS"/exit_*.txt | wc -l); BAD=$(cat "$LOGS"/exit_*.txt | grep -v "exit 0$" | tr '\n' ';')
EDGE_ARG=(); [ -f "$DEV/devid_edge.txt" ] && EDGE_ARG=(--edge "$DEV/devid_edge.txt")      # Amendment 3's D-ID-EDGE, when pinned
uv run python studies/sec6/sec6_score.py devreport "$DEV/devid.txt" "$DEV/devmap.txt" "${EDGE_ARG[@]}" "$DEV"/dev*.jsonl > prereg/sec6/dev_SEC6.txt 2> "$LOGS/devreport.err"
echo "devreport exit $?; carriers run $N; non-zero exits: ${BAD:-none}" >> "$STATUS"
echo "DEV_DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$STATUS"

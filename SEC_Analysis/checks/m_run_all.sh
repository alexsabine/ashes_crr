#!/usr/bin/env bash
# SEC_Analysis mechanism checks, the full run (SEC_Analysis/DECLARATION.md, M1-M4; m_checks.py): arms C0, M1, M2, M4 x seeds 0-4
# on the 30 SEEN carriers of SCL3, SEC3, SEC4 and SEC5 that their loaders keep, three carriers at a time (the machine is shared).
# One results file per carrier in SEC_Analysis/checks/m_runs/<study>_<id>.jsonl (CPU seconds in m_runs/times/), one line per
# carrier exit in m_runs/exits.txt, and a final line M_ALL_DONE. Per-carrier logs go outside the repository. The M0 identity
# (m_identity.txt) is checked before this runs. POST HOC on SEEN carriers; no ledger row.
#     nohup bash SEC_Analysis/checks/m_run_all.sh > /tmp/claude-0/m_run_all.log 2>&1 &
# then: uv run python SEC_Analysis/checks/m_checks.py score > SEC_Analysis/checks/m_checks.txt
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$ROOT" || exit 1
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
OUT=SEC_Analysis/checks/m_runs; LOGS=/tmp/claude-0/m_run_logs
mkdir -p "$OUT" "$LOGS"; : > "$OUT/exits.txt"
echo "M_RUN started $(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$LOGS/status.txt"
uv run python SEC_Analysis/checks/m_checks.py list | xargs -P 3 -L 1 bash -c \
  'uv run python SEC_Analysis/checks/m_checks.py run "$0" "$1" > /tmp/claude-0/m_run_logs/run_$0_$1.log 2>&1; echo "$0 $1 exit $?" >> SEC_Analysis/checks/m_runs/exits.txt'
echo "M_RUN finished $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOGS/status.txt"
echo "M_ALL_DONE" >> "$OUT/exits.txt"

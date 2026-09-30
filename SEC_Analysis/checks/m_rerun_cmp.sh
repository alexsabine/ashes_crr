#!/usr/bin/env bash
# SEC_Analysis mechanism checks, the byte-identical rerun (R9; SEC_Analysis/DECLARATION.md, m_checks.py): every carrier of
# 'm_checks.py list' is run again, three at a time, into a scratch directory outside the repository (--out), and each results
# file in SEC_Analysis/checks/m_runs/ is compared byte for byte (cmp) with its rerun. CPU seconds (m_runs/times/) are not compared.
# Run after m_run_all.sh has finished (exits.txt ends with M_ALL_DONE). POST HOC on SEEN carriers; no ledger row.
#     bash SEC_Analysis/checks/m_rerun_cmp.sh > SEC_Analysis/checks/m_rerun_cmp.txt
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$ROOT" || exit 1
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
RE=/tmp/claude-0/m_rerun; LOGS=/tmp/claude-0/m_rerun_logs
rm -rf "$RE" "$LOGS"; mkdir -p "$RE" "$LOGS"
uv run python SEC_Analysis/checks/m_checks.py list | xargs -P 3 -L 1 bash -c \
  'uv run python SEC_Analysis/checks/m_checks.py run "$0" "$1" --out /tmp/claude-0/m_rerun/"$0"_"$1".jsonl > /tmp/claude-0/m_rerun_logs/run_$0_$1.log 2>&1'
echo "SEC_Analysis mechanism checks: byte-identical rerun of SEC_Analysis/checks/m_runs/*.jsonl (R9); POST HOC on SEEN carriers, no ledger row"
echo "m_checks.py sha256 $(sha256sum SEC_Analysis/checks/m_checks.py | cut -c1-64); uv.lock sha256 $(sha256sum uv.lock | cut -c1-64)"
n=0; k=0
for f in SEC_Analysis/checks/m_runs/*.jsonl; do
  b=$(basename "$f"); n=$((n + 1))
  if cmp -s "$f" "$RE/$b"; then k=$((k + 1)); echo "   IDENTICAL $b $(sha256sum < "$f" | cut -c1-64)"; else echo "   DIFFERS   $b"; fi
done
nl=$(uv run python SEC_Analysis/checks/m_checks.py list | wc -l)
if [ "$k" -eq "$n" ] && [ "$n" -eq "$nl" ]; then w=IDENTICAL; else w=DIFFERS; fi
echo "results files byte-identical to their rerun: $k/$n (carriers listed: $nl) -> $w"

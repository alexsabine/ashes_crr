# Run log — study MEAS2 (2026-09-15)

Environment: uv.lock sha256 `0aa5c797ca5dbbce…`; Python 3.11.15; single-threaded BLAS forced.

| step | time (UTC, container clock) | note |
|---|---|---|
| MEAS voided | 21:23–21:24 | loader read 0 series (`runs/meas/results.jsonl`); structure inspected (keys, types, columns, 548 × 4), no values read |
| prereg meas2 hashed, committed `57b6302`, pushed | 21:24:30 | loader corrected; hypotheses verbatim from MEAS; OTS failed again; tag local only |
| run | 21:24:36 – 21:27:15 | `runs/meas2/frozen/meas2_score.py run` → `results.jsonl` (1081 lines: header + 20 cities × 27 cells × 2 metrics) |
| rerun | 21:27–21:30 | `results_rerun.jsonl`, `cmp` clean — byte-identical |
| score | 21:30 | `score.txt` |

Frozen-copy mechanics as for MEAS (frozen `core.py` beside the script; `runs/data` symlink).

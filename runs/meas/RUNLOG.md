# Run log — study MEAS (2026-09-15, one container, 4 cores, numpy/scipy only)

Environment: uv.lock sha256 `0aa5c797ca5dbbce…` (rdata 1.1.0, pyreadr 0.5.6 added
before the hash); Python 3.11.15; single-threaded BLAS forced in the script.

| step | time (UTC, container clock) | note |
|---|---|---|
| gate_L5R run, output committed | 21:20 | `prereg/meas/gate_L5R.txt`, GATE OPEN under both metrics |
| HASH.txt written, `ots stamp` attempted | 21:21 | OTS **failed** (calendars unreachable) — study unanchored |
| commit `32f18c3` pushed | 21:22:41 | first external witness of the frozen scripts; **no data present** |
| HASH.txt corrected | 21:25 | the first HASH.txt listed two `__pycache__/*.pyc` files left by the smoke run (gitignored, so unverifiable); regenerated excluding them. Every script hash is unchanged (compare the two HASH.txt versions in git). Still no data present. |
| signed tag `prereg-meas-2026-09-15` | 21:22 | local only; the remote refuses tag refs (as for EQX) |
| data download | see below | `data/fetch_measles.py`, sha256 in `data/manifests/meas.sha256` |

Frozen-copy mechanics: the frozen `meas_score.py` imports the frozen `core.py` beside it
and reaches `data/` through the `runs/data -> ../data` symlink (no script edit after the hash).

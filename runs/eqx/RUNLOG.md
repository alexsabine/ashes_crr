# Run log — study EQX (2026-09-15, one container, 4 cores, numpy only)

Environment: `uv.lock` sha256 `052566c3725e02d8…`; Python 3.11.15; single-threaded BLAS forced
in the script. Two reruns of one unit (`run optdigits eq 1.0 0`) are byte-identical
(`cmp` clean, checked before the study runs).

| step | time (UTC, container clock) | note |
|---|---|---|
| gate_EQ run, output committed | 18:13 | `prereg/eqx/gate_EQ.txt`, GATE OPEN |
| HASH.txt written | 18:14 | over `prereg/eqx/` + `runs/eqx/frozen/` |
| `ots stamp` attempted | 18:14 | **failed**: calendars unreachable ("received 0 attestations") — study is unanchored |
| commit `231f75b` | 18:14:49 | contains HASH.txt; no data present |
| signed tag `prereg-eqx-2026-09-15` | 18:14 | signed with the agent's session key `88515F06814240EA` (not the human's) |
| push of branch | 18:15:10 | remote at `231f75b` (`git ls-remote`) — the only external witness of "before" |
| push of tag | 18:15 | **refused by the remote** ("remote end hung up") on three attempts; tag exists locally only |
| data download | 18:16:04 | `data/fetch_pmlb.py`; PMLB files are Git-LFS objects, fetched from `media.githubusercontent.com`, sha256 checked against the LFS pointer oid served at the URL named in the prereg |
| runs | 18:16–18:20 | `all optdigits`, `all pendigits`, `all letter` from `runs/eqx/frozen/eqx_score.py` |

Deviation from the command sequence, declared: the frozen script resolves the repo root
as two directories above itself, which from `runs/eqx/frozen/` is `runs/`. Rather than
edit a hashed script (which voids the study), a symlink `runs/data -> ../data` was added
so the frozen copy finds `data/raw/pmlb/`. The script bytes are unchanged
(`sha256sum -c` against HASH.txt holds).

No file in this folder other than `*.jsonl`, `*.stderr.txt`, this log and `frozen/`
was written by anything but the frozen script.

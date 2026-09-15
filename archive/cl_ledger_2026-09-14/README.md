# Archive — continual-learning ledger bundle of 2026-09-14 (pre-audit pipeline)

Imported verbatim from `crr_cl_ledger.zip` on 2026-09-15 (prompt 3,
`notebook/PROMPT_LOG.md`). **Status: context, not evidence.** Every result in
this folder was produced under the pipeline the September 2026 audit
rejected, on datasets listed in `data/SEEN.md`, with pre-registration hashes
that are *not in the bundle* ("sha256 in the shell logs"). Nothing here may
be cited as a PASS. It is kept so that the recompute audit
(`audit/recompute_2026-09-14.py`) has a fixed input and so that the ledger can
record what these runs actually showed.

Contents: `LEDGER_2026-09-14.md` (the curated claims), `PREREG_*.md`
(pre-registrations as written), `mlp_bench.py` / `cifar_bench.py` /
`lm/lm_bench.py` / `lm/lm_path.py` (pipelines), `run_*.sh` (what was
actually executed), `results_*.jsonl` (raw outputs), `prior_art_map_2026-09.*`
(literature review, 13 pp.). Pipelines read data from `/home/claude/...`
paths that do not exist in this repository; they are not runnable as-is.

Write-once: do not edit files in this folder.

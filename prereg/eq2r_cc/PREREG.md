# Pre-registration — EQ2R-CC: does the normalised penalty step save compute? (a scoring layer over EQ2R)

Written at the container time in the commit that carries `HASH.txt` (2026-09-17 by the container clock;
the data it scores is opened only after 2026-09-18T00:00Z, see the R3 hold in `prereg/eq2r/PREREG.md`
and AGENT_LOG 25). Owner request: prompt-log entry 57 ("focus on whether CRR's potential to save compute
cost"). **No data listed in `prereg/eq2r/PREREG.md` has been opened. This prereg adds no runs: it scores
the EQ2R results files with a second frozen script, `runs/eq2r_cc/frozen/eq2r_cc_score.py`.**

## Anchoring
As EQ2R: weakly anchored (push timestamp only); the strongest level any row here can reach is PASS-0.

## What "compute" means here
The scorer uses only two logged fields per run: `fwd_bwd_per_sample` (forward+backward sample passes per
stream sample, counted by the frozen EQ2R scorer) and `n_stream`. Compute of a configuration = the sum
over its five seeds of `fwd_bwd_per_sample × n_stream`. Wall-clock time is not used (not deterministic).

## Where a saving could come from, and where it cannot
- **Per step**: the rule adds two vector norms and an exponential moving average to a fixed-λ EWC step;
  it adds no forward or backward pass. No per-step saving is claimed; CC-1 checks the logged passes are
  identical.
- **Tuning**: a tuned λ costs the whole pre-registered grid (11 coarse + up to 6 refinement configurations,
  five seeds each); the rule at Ω = 1 costs one configuration. The saving is real only if the rule's one
  configuration reaches the tuned accuracy, and only if a *transferred default* λ does not reach it too
  (a default needs no framework).
- **Exposure**: if the rule at one epoch per task reaches the tuned λ at three, the stream compute falls
  by three; EQ2R's capacity × epochs array supplies the cells.

## Rows
Steps are EQ2R's (max(1.0 pt, 2 SE of the tuned-λ accuracy), per carrier or per cell). Aggregation: mean
over the five seeds, per-seed values printed.

- **CC-1 Per-step compute (definition check).** For every carrier and seed, `fwd_bwd_per_sample` of the
  rule at Ω = 1 equals that of the tuned-λ run. PASS iff identical on every seed. (Expected PASS by
  construction; recorded so that no per-step saving is ever claimed.)
- **CC-2 Tuning compute.** On every carrier: (a) rule at Ω = 1 not behind the tuned λ by a step;
  (b) tuning-inclusive compute of the rule ≤ 0.1 of the tuned λ's (structural: 1 configuration against
  the grid; printed, not assumed); (c) the rule ahead of a **transferred default λ = 30** (the best single
  λ across EQ2's carriers, ledger EQ2-1; learned on EQ2, named here under R3) by ≥ step on ≥ 2 of 3
  carriers. PASS iff (a) and (b) on 3/3 and (c) on ≥ 2/3. If (c) fails, the row reads "a transferred
  default gives the saving without CRR", whatever (a) and (b) read.
- **CC-3 Exposure (on `mfeat_karhunen`, the EQ2R array carrier).** Rule at Ω = 1 with 1 epoch per task
  vs tuned λ at 3 epochs: PASS iff rule(1) − tuned(3) > −step(256, 3). The tuning-inclusive compute ratio
  is printed.

Outcomes named in advance: CC-2 PASS with (c) → the compute saving of a tuning-free rule is CRR's on
these streams; CC-2 with (c) failing → the saving belongs to a default λ; CC-2 (a) failing → no saving
(no accuracy at that budget); CC-3 PASS → a three-fold stream saving on one carrier, report only until
replicated. None of these rows is a hypothesis of `theory/CRR.md`; they score a use case named in
`docs/ROADMAP_2026-Q4.md` §4 ("replacing EWC's λ").

## Dry run on seen data (context, not a row)
`runs/eq2r_cc/dryrun_on_eq2_seen.txt`: the same scorer on EQ2's results (seen carriers; the default λ is
in-sample there, so (c) is circular on `mfeat_fourier`). It is committed so the reader can see the
scorer's output format before EQ2R's data is opened; it produces no ledger row.

## Scoring script
`runs/eq2r_cc/frozen/eq2r_cc_score.py` (copy of `studies/eq2r_cc/eq2r_cc_score.py` at hash time); sha256
in `HASH.txt`. Run after EQ2R's results exist:
`uv run python runs/eq2r_cc/frozen/eq2r_cc_score.py runs/eq2r/results_*.jsonl > runs/eq2r_cc/score.txt`.

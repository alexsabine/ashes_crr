# Report — study EQX: the equanimity rule (Ω = 1) on three unseen streams

Written 2026-09-15 after ledger rows EQX-1 … EQX-5 (`ledger/LEDGER.md`).
Every number below is in `runs/eqx/score.txt`, printed by
`runs/eqx/frozen/eqx_score.py score` from `runs/eqx/{optdigits,pendigits,letter}.jsonl`.

## Verdict, as pre-registered

| line | claim | result |
|---|---|---|
| EQX-1 | the rule reduces to a constant if it is < 1.0 pt ahead of the best fixed replay weight on ≥ 2/3 datasets | **reduces on 3/3**: −1.64 (optdigits, behind fixed w = 1), −0.46 (pendigits, behind fixed w = 0.5), −1.75 (letter, behind fixed w = 2) |
| EQX-2 | Ω = 1 is the best grid point with both neighbours > 1.0 behind, on ≥ 2/3 | **FAIL** (1/3: letter only; pendigits' best Ω is 0.71) |
| EQX-3 | beats ER-sum (fixed w = 1) by ≥ 1.0, positive in ≥ 4/5 seeds, on ≥ 2/3 | **FAIL** (0/3): −1.64 (0/5 seeds positive), +0.85 (5/5 positive but under the step), −0.47 (1/5) |
| EQX-4 | Fisher vs Euclidean ratio immaterial | **no**: Euclidean is better by 1.46, 2.27, 1.90 pt on the three datasets |
| EQX-5 | EQ at r = 0.2 within 1.0 of 100 % replay (report only) | −2.81, −2.50, +0.78 |

The outcome named in advance for "EQX-1 triggers ∧ EQX-3 fails" applies:
**Ω = 1 is ER-sum with a replay weight near 1; the rule is retired as
"adaptive".** Its median effective weight was 1.04, 1.12 and 1.10 on the
three datasets — it computes the constant 1 with noise, and the noise costs
accuracy (0/5 seeds ahead of the plain constant on two of three datasets).

## Anchoring caveat (R2)
The pre-registration hash `d3825b45…` was committed and pushed
(`231f75b`, 2026-09-15T18:15:10Z) before any data was downloaded, but the
OpenTimestamps anchor could not be created and the signed tag could not be
pushed (`runs/eqx/RUNLOG.md`). The rows are therefore *held-out, weakly
anchored*: the only witness of "before" is the GitHub push timestamp. Since
every line is a FAIL or a reduction, the anchoring weakness cuts against
nothing the theory would want to claim.

## Per-unit distributions
Per-seed values for every arm are in `runs/eqx/score.txt` (five seeds, all
shown). Notable: pendigits seed 2 is a bad seed for several arms (EQ 82.17,
fixed w = 1 81.86, Euclid 93.86) — the paired per-seed differences are what
the verdicts use, not the means alone. Exclusions: none (0 NaN rows in all
three datasets; `classes` matched the prereg table).

## Sensitivity
Single frozen configuration (declared in the prereg). The one swept axis is
the metric inside the ratio (Fisher vs Euclidean at Ω = 1), reported as
EQX-4: Euclidean is ahead of Fisher by 1.46, 2.27 and 1.90 pt (per-seed
values in `score.txt`). The pre-registered candidate is the Fisher ratio;
the Euclidean variant was not a candidate and is not scored against the
constants here. Nothing in the EQX-1/EQX-3 verdicts depends on a swept
constant, so no cell can flip: not fragile.

## What the archive had shown, recomputed
`audit/recompute_2026-09-14.txt`, rows ARC-*. On KMNIST the same comparison
was 1.03 pt in the rule's favour (per seed +1.00, +0.42, +1.68) — a boundary
case the old ledger rounded into "within 1.0"; the cross-dataset fixed-w
sweep that would have settled it was lost. Today's three unseen datasets
settle it the other way.

## What a surrogate would have done
`prereg/eqx/gate_EQ.txt`: on a convex replay learner with constant gradient
scale the rule loses to fixed w = 1 by 17.7 % (S-R, the negative control)
and wins only when label scales swing 16× between tasks (S-V). Real class-IL
streams with standardised features are the S-R case: gradient scales do not
swing, so the adaptive ratio has nothing to adapt to and becomes a noisy
constant. The gate also showed Ω = 1 is not the best Ω on either surrogate.

## Open, not tested here
EQ-3 of CLAUDE.md §6 (framework baselines ER-ACE, DER++, CLS-ER via Mammoth)
needs PyTorch, unavailable in this environment. Given EQX-1/EQX-3, that study
would compare a fixed replay weight against those methods, not an adaptive rule.

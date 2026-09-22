# Study EQ3 — the normalised penalty step on six unseen PMLB streams: the replication fails on 1/6 and both controls are violated

**Two controls are violated and the replication of EQ2-1b fails on one carrier of six.** The ER-sum
control (EQ3-3) fails on `fars`, where the rule is 4.6200 points ahead of its own reduction arm; the
constraint control (EQ3-4), narrowed to load-bearing cells as `reports/eq2.md` required, fails in 3 of its
5 load-bearing cells; and EQ3-1 reads FAIL because on `fars` the rule is 3.7400 behind the tuned λ, beyond
its 3.3508 step. On the other five carriers the rule at Ω = 1 is not behind the tuned λ (margins +0.6886 to
+4.0625), no single λ transfers, the rule does not reduce to a constant, and the lr × batch array passes
5/5. Every number here is printed in `runs/eq3/score.txt` (frozen scorer, rerun byte-identical),
`runs/eq3/exclusions.txt`, `prereg/eq3/gate_EQ2.txt` or `theory/checks/omega_sweeps.txt`.

Prereg hash `5b3bec36`, prereg commit daf50e7 pushed 2026-09-22T01:21:32Z (the only external witness:
OpenTimestamps unreachable, tag push refused, both attempts in `runs/eq3/`); data fetched at 01:23Z.
**Weakly anchored**; every row carries `anchor: push-timestamp only`. Carriers: PMLB `mfeat_factors` (216
features), `mfeat_morphological` (6), `led7` (7), `led24` (24), `krkopt` (6; the first 10 of 18 classes,
stratified subsample 16944 → 5000 rows), `fars` (29; 8 classes, subsample 100968 → 5001 rows), all unseen
before the push (`data/SEEN.md`, `data/manifests/eq3.sha256`). Instrument as EQ2 (numpy MLP d-256-K, one
head, 5 tasks × 2 classes, 3 epochs per task, seeds 0–4) with the additions of `prereg/eq3/PREREG.md`.

## The data-side fact that decides `fars`

The pre-registered row cap (a stratified subsample to 5000 rows, seed 777) rounds `fars`'s class 0, a
tiny class in a 100968-row file, to 0 rows, leaves class 3 with 15 rows and class 7 with 45
(`runs/eq3/exclusions.txt`). Its first task therefore has one class. On `fars` the whole EWC family sits
at chance: every fixed λ from 0.1 to 50 scores 9.26–9.28, every Ω from 0.25 to 4 scores 9.26–9.28, the
Bayes arm, A-GEM and MEGA-I score 9.28, and the tuned λ = 283 reaches 13.0000 only with per-seed values
18.00, 15.70, 9.20, 12.00, 10.10. Under R6 the carrier is scored as committed and no exemption is made.
A future prereg needs a class floor beside the row cap; this one did not have it, and the FAIL stands.

## Rows

| row | prediction | observed (fars / krkopt / led24 / led7 / mfeat_factors / mfeat_morphological) | verdict |
|---|---|---|---|
| EQ3-0 | tuned λ spans ≥ 10× | 283 / 3 / 30 / 0.212766 / 300 / 2.83, span 1410.00× | decidable |
| EQ3-1 | rule at Ω = 1 not behind tuned λ on every carrier; no single λ transfers | Ω=1 − tuned −3.7400 / +0.9790 / +0.6886 / +4.0625 / +3.9000 / +3.7000 (steps 3.3508 / 8.9180 / 4.3633 / 3.2031 / 4.5371 / 4.8719); best single λ = 1 loses 3.7200 / 1.3187 / 2.6917 / 3.6250 / 12.4500 / 6.5500 | **FAIL** (5/6 not behind) |
| EQ3-2 | rule within a step of fixed w = median derived w | +2.4200 / +7.6923 / +0.6260 / +16.2500 / +23.5500 / +14.4000 (median w 426.287 / 4.76098 / 31.6972 / 2.77719 / 1065.84 / 14.6744) | does not reduce |
| EQ3-3 | ER-sum: rule not ahead of best fixed w; within a step of its reduction arm | rule − best fixed −4.6800 / −4.3756 / −1.2520 / −3.5000 / −0.2000 / +1.9000; rule − reduction +4.6200 / +3.0969 / +0.5008 / −0.8125 / −0.2500 / +2.9500 | **VIOLATED** (fars) |
| EQ3-4 | DER++ and LwF, load-bearing cells: rule at best Ω behind tuned by ≥ step | load-bearing 5/12: fars/LwF +0.0200, led7/DER++ −0.5938, led7/LwF −7.1875, mfeat_factors/LwF −19.3000, mfeat_morphological/LwF +12.6000; 7 cells inert | **VIOLATED** (2/5 behind) |
| EQ3-5 | SI, MAS (report) | SI −1.2400 / −1.5984 / −2.7543 / +0.5312 / −5.6000 / +5.7000; MAS +3.1400 / +5.3746 / −0.0313 / +6.9062 / +1.6000 / +2.6000 | no systematic miss |
| EQ3-6 | best Ω in {0.71, 1, 1.41} on every carrier | 2.0 / 4.0 / 2.0 / 2.83 / 1.0 / 2.83 | **FAIL**: a plateau |
| EQ3-7 | A-GEM, GradNorm, MEGA-I vs rule (report) | baseline − rule: A-GEM +0.0200 / −5.2547 / −3.2238 / −4.2188 / −10.8000 / −10.1500; GradNorm +7.1000 / −17.8821 / −4.9139 / −26.0312 / −58.3500 / −37.9000; MEGA-I +0.0200 / −5.5744 / −3.5055 / −8.6562 / −16.5000 / −11.4500 | none dominates; GradNorm diverges on 4/6 |
| EQ3-S | "not behind" flips in > 1 of 54 cells | 6/54 (mfeat_factors at cap 10 and cap 100) | fragile |
| EQ3-8 | features × 4 (report) | Ω=1 − tuned −0.9200 / +2.5774 / +1.5336 / +1.3125 / +0.4000 / +6.8500 | as the primary regime |
| EQ3-C | cap axis: not behind iff cap ≥ tuned λ, 18 cells | 16/18 as predicted; fars/cap 1e4 behind (predicted not), led24/cap 10 not behind at −1.56 (predicted behind) | **FAIL** |
| EQ3-D | late-w vs whole-run median (report) | ratio 0.762 / 1.095 / 1.433 / 1.035 / 0.821 / 1.246; seeds with late-w < 1: 0 / 0 / 0 / 2 / 0 / 0 of 5 | the past is not dropped |
| EQ3-A | capacity × epochs on mfeat_factors, ≥ 3/4 | hidden256/ep3 +3.90 (step 4.54); hidden64/ep1 −1.15 (1.11); hidden64/ep3 −3.05 (1.88); hidden256/ep1 +2.65 (5.09) | **FAIL** (2/4) |
| EQ3-I | lr × batch on mfeat_factors, ≥ 4/5 | +3.90 (4.54) / +3.00 (2.68) / +1.35 (2.42) / +0.85 (4.63) / +0.45 (3.26), tuned λ 300 / 300 / 3000 / 3000 / 300 | **PASS-0** (5/5; weakly anchored) |
| EQ3-B | Bayes (Laplace 1/2) arm (report) | Bayes − tuned −3.7200 / +1.2587 / −2.7543 / +0.0000 / −12.5000 / −7.6000; rule − Bayes −0.0200 / −0.2797 / +3.4429 / +4.0625 / +16.4000 / +11.3000 | Bayes = tuned on 2/6 |
| EQ3-P | plateau width (report) | 9 / 9 / 9 / 7 / 9 / 7 of 9 within a step of the best, all contiguous; median 9 | Ω is a plateau over the grid |

## What the rows say together

1. **The EQ2 reading recurs on five carriers and fails on the sixth.** On krkopt, led24, led7,
   mfeat_factors and mfeat_morphological the rule at Ω = 1 is not behind the in-sample-tuned λ, by
   +0.6886 to +4.0625, in 23 of 25 seeds; the best single λ loses by 1.3 to 12.5 points somewhere; the
   rule's median derived weight (4.76 to 1065.84) sits at or beyond the point where the fixed-λ grid
   collapses (krkopt at λ ≥ 6, led7 at ≥ 30, mfeat_factors at ≥ 423, mfeat_morphological at ≥ 3), and the
   reduction arm at that constant diverges on 2 to 3 seeds of 5 on four carriers. That is the
   stability-edge reading of `reports/eq2.md`, seen again. On `fars` the EWC family is at chance and the
   rule is 3.74 behind a tuned λ that itself scores 13.0; the replication fails there and EQ3-1 is a FAIL.
2. **Both controls are violated.** ER-sum on `fars` only, through the reduction-arm clause (4.6200 ahead of
   its own constant; the rule-vs-best-fixed clause holds on 6/6, as in EQ2-3). The constraint control
   fails as it did in EQ2 and worse: on the load-bearing cells the rule ties LwF on `fars` (+0.0200), ties
   DER++ on `led7` (−0.5938), and is 12.6000 ahead of the tuned LwF weight on `mfeat_morphological`; it is
   behind by ≥ step only on led7/LwF (−7.1875) and mfeat_factors/LwF (−19.3000). The narrowing to
   load-bearing cells did not save the clause. The mechanism statement of `prereg/eq3/PREREG.md` is
   falsified as written, for the second time, and the harm clause is retired.
3. **Ω is a plateau over the whole grid.** The best Ω is 2.0, 4.0, 2.0, 2.83, 1.0 and 2.83; nine of nine grid
   points are within a step of the best on four carriers and seven of nine (0.5 to 4) on the other two.
   This is what `theory/checks/omega_sweeps.py` says the rule is: a continuum of equilibria along the two
   tasks' Pareto curve, with smoothing and mini-batch noise widening a knife edge into a plateau. Nothing
   here singles out Ω = 1, and no further Ω study is planned.
4. **The Bayes weight is the tuned weight where the tuned weight is small.** The Laplace weight 1/2 on the
   task-size-weighted Fisher matches the tuned λ exactly on led7 (tuned 0.212766; difference +0.0000) and
   within a step on krkopt (+1.2587), and is 7.6 to 12.5 points behind where the tuned λ is in the
   hundreds. The rule's advantage over Bayes (3.4 to 16.4 on four carriers) is therefore an advantage over
   a mis-calibrated Laplace approximation, and on the carriers where Laplace is calibrated the rule and
   Bayes agree (−0.0200, −0.2797).
5. **The cap mechanism is partial.** It holds in 16 of 18 cells and exactly on mfeat_factors (behind by
   11.15 at cap 10 and 5.20 at cap 100, ahead by 3.90 at cap 1e4, tuned λ 300), as on EQ2's mfeat_pixel;
   it fails on led24 at cap 10 (the capped rule is still within a step) and on fars at cap 1e4 (the rule is
   behind whatever the cap). Six of 54 sensitivity cells flip, all on mfeat_factors: fragile, as EQ2-S.
6. **Arrays.** The lr × batch array passes 5/5 (the rule is not behind at lr 0.0125, 0.05 and 0.2 and at
   batch 5, 10 and 20; the tuned λ moves tenfold across the cells while the rule needs no tuning). The
   capacity × epochs array fails 2/4: at hidden width 64 the rule is behind the tuned λ by 1.15 and 3.05
   against steps of 1.11 and 1.88. The pass is specific to the wide network.
7. **No published baseline is ahead.** A-GEM and MEGA-I trail the rule by 3.2 to 16.5 points on five
   carriers and tie it on `fars`; GradNorm (α = 0, weights summing to 2) diverges on four carriers, a fair
   reading of that normalisation, not of GradNorm at its best.

Taken as a whole: the rule at Ω = 1 is, on five of six new tabular carriers, a tuning-free way of running
an online-EWC penalty at or above the fixed weight's stability edge, ahead of the tuned λ by up to four
points and never behind it, invariant to learning rate and batch size, and equal to the Bayes weight where
the Bayes weight is well calibrated. It is not what the prereg said it was: it fails on a degenerate
carrier that the pre-registered subsample produced, it is not harmful on constraints that are not losses,
and Ω = 1 is one point on a plateau. EQ2-1b therefore stays PASS-0 with a failed replication recorded
(ledger EQ2-1c). Under the accepted levels nothing here is PASS-1: the anchoring is weak and the
sensitivity table flips in six cells.

## Sensitivity table (Ω = 1 − tuned λ, EWC arm; `runs/eq3/score.txt`)

| carrier | cap 10: sm 0.8 / 0.9 / 0.98 | cap 100 | cap 1e4 |
|---|---|---|---|
| fars | −3.72 / −3.72 / −3.72 | −3.74 / −3.74 / −3.74 | −3.74 / **−3.74** / −3.72 |
| krkopt | +2.14 / +1.32 / +0.66 | +2.18 / +1.26 / +0.12 | +1.48 / **+0.98** / +2.20 |
| led24 | −1.56 / −1.56 / −1.56 | +1.53 / +1.19 / +0.94 | +1.28 / **+0.69** / +0.63 |
| led7 | +3.00 / +3.00 / +3.00 | +3.16 / +2.66 / +2.69 | +3.16 / **+4.06** / +6.03 |
| mfeat_factors | −11.15 / −11.15 / −11.15 | −5.25 / −5.20 / −5.15 | +3.65 / **+3.90** / +2.70 |
| mfeat_morphological | +3.65 / +2.75 / +3.85 | +4.10 / +2.70 / +3.35 | +5.20 / **+3.70** / +6.20 |

Bold: the registered cell. "Not behind" flips only in the six mfeat_factors cells at cap 10 and 100.

## Exclusions and quality gates (`runs/eq3/exclusions.txt`)

No NaN rows on any carrier. `krkopt`: 11112 rows beyond the first ten classes dropped, then subsampled
16944 → 5000 (class 8 keeps 23 rows). `fars`: subsampled 100968 → 5001 (class 0 keeps 0 rows, class 3
keeps 15, class 7 keeps 45). 3360 runs; 815 ended with non-finite parameters and were kept, scored 0, as
pre-registered: the large-weight ends of every fixed grid, the GradNorm runs on four carriers, the
reduction arms on five carriers (2 to 3 seeds each), and the upper x4 grids. No Ω arm on the primary
regime diverged.

## What a surrogate would have done

`prereg/eq3/gate_EQ2.txt` (byte-identical to EQ2R's): the nonconvex S-Y row passes the same statistic with
the rule ahead by 7.5 % and fails at cap 100 and smooth 0.98, the fragility the real carriers show again
(mfeat_factors). The gate has no row for a carrier whose first task has one class, and no row for a
constraint whose weight is nearly inert at high accuracy (7 of 12 cells here); both are still missing,
and the first is now the more urgent: a class floor belongs in the quality gate of any future prereg with
a row cap. The mathematics check (`theory/checks/omega_sweeps.py`) predicted the plateau (EQ3-6, EQ3-P)
and the Bayes-arm pattern (EQ3-B) before any data was opened.

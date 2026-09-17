# Study EQ2 — the equanimity rule as a normalised penalty step for online EWC

**A control is violated: the mechanism statement pre-registered in `prereg/eq2/PREREG.md`
("harmful for every constraint-type past term") is falsified as written — DER++ lands within a
step of its tuned weight on 2 of 3 carriers (row EQ2-4).** What follows is the rest of the
ledger, in prereg order. Every number is printed in `runs/eq2/score.txt` (frozen scorer,
rerun byte-identical), `runs/eq2/exclusions.txt`, or `prereg/eq2/gate_EQ2.txt`.

Prereg hash `0da06fc1`, tag `prereg-eq2-2026-09-17` at commit 4ba6035, signed with the agent's
session key; OpenTimestamps unreachable (`runs/eq2/ots_attempt.txt`); the tag push was refused
by the remote (`runs/eq2/tag_push_attempt.txt`). **Weakly anchored**: the GitHub push time of
4ba6035 is the only external witness that the prereg preceded the data. Carriers: PMLB
`mfeat_fourier` (76 features), `mfeat_pixel` (240), `texture` (40; classes beyond the first ten
dropped: 500 rows), all unseen before the tag (`data/SEEN.md`, `data/manifests/eq2.sha256`).
Instrument: numpy MLP d-256-10, one head, 5 tasks × 2 classes, 3 epochs per task, seeds 0–4;
`uv.lock` sha256 `77a063f0…` in every results header. This is the tabular, no-PyTorch version of
the design in issue #20; Daniel's Mammoth run on image streams remains the anchored one.

## Rows

| row | prediction | observed (mfeat_fourier / mfeat_pixel / texture) | verdict |
|---|---|---|---|
| EQ2-0 | tuned EWC λ spans ≥ 10× | λ = 30 / 1410 / 100, span 47.00× | decidable |
| EQ2-1 | rule at Ω = 1 not behind tuned λ by a step on every carrier, and no single λ transfers | Ω=1 − tuned +3.3000 / +2.1000 / +2.7800; steps 1.0000 / 3.5121 / 3.6120; seeds not behind 5/5 each; best single λ = 30 loses 0.0000 / 15.4500 / 0.5600 | **PASS, fragile** (see EQ2-S) |
| EQ2-2 | rule within a step of fixed w = median derived w | +29.4000 / +10.0000 / +2.7800 (median w 1336.54 / 3183.87 / 110.561; the first diverges, the second on 1/5 seeds) | does not reduce: normalised-gradient method |
| EQ2-3 | ER-sum: rule not ahead of best fixed w; within a step of its reduction arm | −0.6000 / −0.2500 / −0.6600; vs reduction −0.5000 / −0.2500 / −0.3600 | holds |
| EQ2-4 | DER++ and LwF: rule at best Ω behind tuned weight by ≥ step on every carrier | DER++ −1.5500 / −0.7000 / +0.5800; LwF −11.3500 / −9.4000 / −18.6200 | **violated** (DER++ on 2/3) |
| EQ2-5 | SI, MAS: expected to miss (report) | SI −0.1000 / −7.9000 / +0.1600; MAS +1.3000 / −1.7500 / +1.6800 | the miss does not appear |
| EQ2-6 | best Ω in {0.71, 1, 1.41} on every carrier | 0.5 / 2.0 / 1.41 | FAIL: a plateau, no peak at 1 |
| EQ2-7 | A-GEM, GradNorm α=0, MEGA-I vs rule (report) | baseline − rule: A-GEM −4.2000 / −14.1000 / −4.9800; GradNorm −29.4000 / −52.1500 / −31.3400; MEGA-I −5.1500 / −19.1000 / −6.8400 | none dominates; GradNorm as implemented diverges |
| EQ2-S | "not behind" flips in > 1 of 27 sensitivity cells | 6/27 flip (all cap = 10 and cap = 100 cells on mfeat_pixel) | fragile |
| EQ2-8 | standardised features × 4 (report) | Ω=1 − tuned −0.4500 / −0.1500 (tuned 10000, grid edge) / −16.6400 | the gate's regime does not reappear |

## What the rows say together

1. **On online EWC the rule beat the tuned λ on 3/3 carriers**, by 2 to 3 points, in every seed,
   with the tuned λ found on a √2-refined grid and tuned in-sample. The rule did not reduce to a
   constant: its median derived weight was 45×, 2.3× and 1.1× the tuned λ, and a fixed weight at
   that value diverges on two carriers. The fixed-λ grids show why: on each carrier there is a
   stability edge (mfeat_fourier between 30 and 42.3; mfeat_pixel between 1410 and 2000; texture
   between 100 and 141) beyond which fixed EWC collapses, and the rule runs *above* that edge
   because its penalty step is bounded by the present step. That is the normalised-gradient
   reading of the rule, and it is the only reading the rows support.
2. **The pass is fragile in exactly the way the gate table predicted.** With the ratio cap at 10
   or 100 the rule on mfeat_pixel is 13 to 17 points *behind* the tuned λ, because the tuned λ
   itself is 1410 and a capped rule is a weaker fixed weight. Six of 27 cells flip; the prereg
   rule for "fragile" is one. The cap is not a detail of the estimator; it is the mechanism.
3. **The same-units control held** (ER-sum, three carriers: the rule is a constant and adds
   nothing, as in EQX). **The constraint control did not**: LwF behaved as predicted on 3/3, but
   DER++ sat within a step of its tuned α on mfeat_pixel and texture, where every DER++ arm
   scores 95–99 % and α is nearly inert. The mechanism statement said "harmful for a
   constraint that is not a loss on the past task"; on these two carriers it was not harmful
   because it did not matter. Under the prereg that is a violation, and the statement has to be
   narrowed before it is used again: it predicts harm only where the constraint's weight is
   load-bearing. That narrowing is a new prereg, not a reinterpretation of this one.
4. **SI and MAS did not miss.** MAS with the rule is within a step of, or ahead of, its tuned
   weight on 3/3; SI on 2/3. The "penalty in other units" clause has no support here either.
5. **Ω is a plateau.** Best Ω was 0.5, 2.0 and 1.41; the profile is flat within a step over
   0.5–1.41 on every carrier and drops only at Ω = 2 on texture. Nothing here singles out Ω = 1.
6. **No published baseline is ahead.** A-GEM and MEGA-I trail the rule by 4 to 19 points on the
   EWC penalty. GradNorm with weights summing to 2 starved the present term and diverged on two
   carriers (chance on the third); it is a fair reading of α = 0 with that normalisation, not of
   GradNorm at its best, and a reader should weigh it accordingly.
7. **The ×4 diagnostic regime does not reproduce the gate's premise** on real features: forcing the
   units apart made the rule tie or lose. The EQ2-1 pass therefore does not come from input
   scale; it comes from the stability edge in point 1.

Taken as a whole: on tabular MLP streams the rule is a tuning-free, cap-dependent way of running
an EWC penalty above the fixed-λ stability edge. That is a narrower and different claim from the
one pre-registered, and one control failed, so this study does not establish the mechanism it
set out to test. It establishes a fragile empirical PASS on EQ2-1 with a documented cause, and it
retires two clauses of the mechanism statement (DER++, SI/MAS).

## Sensitivity table (Ω = 1 − tuned λ, EWC arm; from `runs/eq2/score.txt`)

| cap \ smooth | 0.8 | 0.9 | 0.98 |
|---|---|---|---|
| mfeat_fourier 10 | −0.35 | −0.35 | −0.35 |
| mfeat_fourier 100 | +0.05 | +0.15 | +0.05 |
| mfeat_fourier 1e4 | +2.80 | **+3.30** | +3.15 |
| mfeat_pixel 10 | −16.60 | −16.60 | −16.60 |
| mfeat_pixel 100 | −13.45 | −13.45 | −13.40 |
| mfeat_pixel 1e4 | +2.90 | **+2.10** | +1.35 |
| texture 10 | −1.02 | −1.26 | −1.46 |
| texture 100 | +0.30 | +0.16 | +0.04 |
| texture 1e4 | +0.98 | **+2.78** | −2.18 |

Bold: the registered cell. "Not behind" (> −step) flips in the six mfeat_pixel cells at cap 10
and 100; the texture cells stay within its 3.61 step.

## Exclusions and quality gates (`runs/eq2/exclusions.txt`)

No NaN rows. `texture`: 500 rows of the eleventh class dropped by the pre-registered rule. 1395
runs; 267 ended with non-finite parameters and were kept, scored as 0, as pre-registered. They
are the large-weight ends of the fixed grids (EWC λ ≥ 300 on mfeat_fourier, ≥ 2000 on
mfeat_pixel, ≥ 141 on texture; DER++ α ≥ 3; the upper SI and MAS grid points), the GradNorm
runs on two carriers, the EWC reduction arm on mfeat_fourier (5/5) and mfeat_pixel (1/5), and
the ×4 regime's upper grid. None of the tuned or Ω arms scored on the primary regime diverged.

## What a surrogate would have done

`prereg/eq2/gate_EQ2.txt`: the nonconvex S-Y row (softmax MLP, online EWC, 16× Fisher-scale
mismatch) passes the same statistic with the rule ahead of the tuned weight by 7.5 % and a
diverging reduction arm, and fails at cap = 100 and at smooth = 0.98 — the same fragility the
real carriers show. Its unit-scale sibling fails, which predicted the ×4 diagnostic the wrong
way round: on real features the pass appeared *without* a forced scale mismatch and vanished
with one. The convex S-W row (PR #23) ties its own constant, which is what EQ2-3 reproduces on
ER-sum. The gate had no row for a constraint whose weight is nearly inert at high accuracy, so
it could not have caught the DER++ outcome; that row is the first thing a follow-up prereg
needs.

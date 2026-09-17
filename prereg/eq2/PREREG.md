# Pre-registration — EQ2: the equanimity rule as a normalised penalty step for online EWC

Written: 2026-09-17 (container clock; the commit and tag carry the exact time). Hash of this
folder and the frozen scripts in `HASH.txt`. Signed tag `prereg-eq2-2026-09-17`.
**No data listed below has been opened. No file named below exists under `data/raw/` at hash time.**
Design: issue #20 (owner-posted 2026-09-16; Daniel Friedman's Phase-A run in PR #23 closed the
gate on the convex positive control; this prereg follows the second Phase-A attempt, whose gate
table is committed here as `gate_EQ2.txt`, with the closed first attempt kept beside it).

## Anchoring — read this first
OpenTimestamps calendars are unreachable from this environment (probe 2026-09-17: HTTP 000 on
both pools; the same as EQX, MEAS, MEAS2, CARD). The only external witness to "before" is the
GitHub push timestamp of the tagged commit. The tag is signed with the agent's session key, not
the human's. Under R2 this study is **weakly anchored**: every ledger row it produces carries
`anchor: push-timestamp only`. Daniel's Mammoth run of the same design (issue #20 §6) is the
strongly anchored one; this study is the numpy-MLP version on tabular streams, run because the
Mammoth carriers (CIFAR-100, TinyImageNet), PyTorch and the OTS calendars cannot be reached here.

## Hypothesis under test (theory/CRR.md [A9]/[H-EQ]; issue #20 §1)
The rule `g = g_present + w · g_past`, `w = Ω · ‖ĝ_present‖ / ‖ĝ_past‖`, Ω = 1, adds the past
term's *direction* with the present term's *step length*. Claim: this is useful exactly when the
past term is the past task's loss or its Fisher-curvature (Laplace) approximation (online EWC),
redundant when the units already match (ER-sum), and harmful when the past term is a constraint
that is not a loss on the past task (DER++, LwF) or an importance penalty in other units (SI, MAS).

## Gate (R4) — `gate_EQ2.txt`, committed here and covered by the hash
Statistic: the rule at Ω = 1 is not behind the tuned fixed weight by a relative step (0.05).
- MUST PASS: S-Y softmax MLP with online EWC, 16× Fisher-scale mismatch → PASS (rule ahead of
  the tuned weight by 7.5 % relative; seeds behind by a step: 1/5; reduction arm diverges).
- MUST FAIL: S-R same-units convex replay → FAIL (behind by 17.7 %); S-X convex constraint
  learner → FAIL (behind by 7.1 %); S-Y/LwF distillation constraint on the same network → FAIL
  (behind by 278 %). GATE OPEN.
- Informational rows in the same table: S-W convex EWC-Laplace (FAIL: the convex null of PR #23);
  S-Y at unit input scale (FAIL, behind by 63 %); S-Y with cap = 100 (FAIL, +44 %); smooth = 0.8
  (PASS, −18 %); smooth = 0.98 (FAIL, +49 %). **The positive control passes only under the
  registered estimator and only with mismatched units.** Both facts are carried into the rows
  below (EQ2-0 precondition; sensitivity table; EQ2-8 diagnostic regime).

## Data (must be absent from data/SEEN.md — confirmed: none of these appears)
PMLB mirror on GitHub (LFS object via `media.githubusercontent.com`, pointer oid verified;
`data/fetch_pmlb.py --manifest eq2`), downloaded after the tag; sha256 of each file in
`data/manifests/eq2.sha256`, echoed in every results file header; download date appended to
`data/SEEN.md` in the same commit.

| carrier (PMLB name) | classes in file | classes used | class-IL stream |
|---|---|---|---|
| `mfeat_fourier` | 10 | 10 | 5 tasks × 2 classes |
| `mfeat_pixel` | 10 | 10 | 5 tasks × 2 classes |
| `texture` | 11 | first 10 in remapped label order | 5 tasks × 2 classes |

Three carriers are required (EQ2-0 needs a λ spread across carriers; EQ2-1's "every carrier"
needs a denominator larger than two). If a named file is absent from the mirror or fails the
oid check, the pre-registered substitutes are used in this order, one per missing carrier, and
the substitution is recorded in the ledger row: `mfeat_karhunen`, `mfeat_zernike`, `vowel`.
Fixed 80/20 stratified split (seed 12345, independent of run seed); features standardised on
the training part (the standard pipeline; the mismatch the claim needs must then come from the
carriers themselves, which is what EQ2-0 tests). Three epochs per task, tasks in class order,
batch 10. Score: test accuracy over **all** classes at the end of the stream (single head).
Quality gate: rows with NaN dropped and counted (expected 0); classes beyond the first ten
dropped and counted; a run whose parameters are not finite at the end scores 0 and is counted
(`finite` field). No other exclusion.

## Instrument (all constants named; frozen in `runs/eq2/frozen/eq2_score.py`)
MLP d-256-K ReLU, SGD lr 0.05, batch 10, 3 epochs per task, seeds 0–4, single-threaded BLAS.
Every method: `g = g_present + w · g_past` with the method's own weight removed from `g_past`.
- EWC-online: `g_past = 2·F·(θ − θ*)`, F accumulated at each boundary as the mean over 50
  batches of the squared batch-mean gradient × batch size; θ* reset at each boundary.
- ER-sum: `g_past` = cross-entropy on a replay batch of the stream batch size (reservoir 500).
- DER++: `g_past` = logit-matching MSE on a replay batch (the α term); DER++'s β·CE(replay) with
  β = 0.5 stays inside the present term at its published default; published default α = 0.1.
- LwF: `g_past` = distillation on the current batch against the model frozen at the last
  boundary, T = 2 (gradient scaled by T); published default weight 1.
- SI: path-integral importance, ξ = 1e-3. MAS: importance = mean |∂‖f(x)‖²/∂θ| over 50 batches.
- Rule (registered estimator, R3: chosen on EQX 2026-09-15 and on synthetic playground streams
  2026-09-16, never on these carriers): EMA of the gradient **vectors**, smooth = 0.9, Euclidean
  norm, cap = 1e4, denominator floor 1e-12.
- Baselines on the EWC penalty: A-GEM (project `g_present` when it conflicts with `g_past`);
  GradNorm α = 0 (two learned weights, sign-of-deviation descent with step 0.025 on the
  max-normalised deviation, weights floored at 1e-3 and renormalised to sum 2 every step);
  MEGA-I (w = EMA L_past / EMA L_present, same smoothing and cap).
- Reduction arm: fixed w = per-carrier median of the derived w from the Ω = 1 run (EWC and ER).
- Ω grid {0.5, 0.71, 1, 1.41, 2}. EWC λ grid: coarse {0.1, 0.3, 1, 3, 10, 30, 100, 300, 1000,
  3000, 10000}, then a refinement at √2 spacing over [best/√10, best·√10] skipping points already
  on the coarse grid; the tuned λ is the best of the union (the pre-registered two-stage tuning
  rule; λ is tuned on the scored seeds, in-sample, which favours the baseline). ER-sum fixed w
  {0.5, 1, 2, 4}. DER++/LwF/SI/MAS weight grid {0.01, 0.03, 0.1, 0.3, 1, 3, 10} plus the published
  default.
- Resolvable step, per carrier: `step = max(1.0 pt, 2 × SE)`, SE the standard error over the five
  seeds of the tuned-λ EWC accuracy; written into the rows.
- Sensitivity table: cap ∈ {10, 100, 1e4} × smooth ∈ {0.8, 0.9, 0.98} at Ω = 1 on the EWC arm.
  EQ2-1's "not behind" flipping in more than one of the 27 cells (9 per carrier) is "fragile".
- Compute: forward+backward sample passes per stream sample logged per run (`fwd_bwd_per_sample`).

## Rows (scored once by `eq2_score.py score`; per carrier and per seed values printed)
Aggregation: mean over five seeds; per-seed values beside every mean; "every carrier" = 3/3.
Strict/non-strict as written; sidedness as written (EQ2-1 one-sided by design: the rule need
only not lose; the two-sided quantity is printed).

- **EQ2-0 Precondition (decidability).** Tuned λ for EWC-online spans ≥ 10× (max/min) across
  the three carriers. If not, the row reads "not decidable: tuned λ did not move" and EQ2-1 and
  EQ2-2 are reported without a verdict.
- **EQ2-1 H-EQ2.** On every carrier, mean(rule at Ω = 1) − mean(tuned λ) > −step, AND the best
  single λ (coarse grid, best mean over carriers) is behind the tuned λ by ≥ step on at least one
  carrier. PASS requires both. FAIL if the rule is behind by ≥ step on any carrier, or if a
  single λ transfers.
- **EQ2-2 Reduction.** |mean(rule Ω = 1) − mean(fixed at median derived w)| < step on every
  carrier → "reduces to a per-carrier constant"; otherwise "does not reduce: normalised-gradient
  method". Reported, not a verdict.
- **EQ2-3 Control, same units (ER-sum).** Holds iff on every carrier mean(rule Ω = 1) −
  mean(best fixed w) < step AND |rule − reduction arm| < step. Violated otherwise.
- **EQ2-4 Control, constraint (DER++ and LwF).** Holds iff for both methods on every carrier the
  rule at its best Ω is behind the tuned weight by ≥ step. Violated otherwise.
- **EQ2-5 Diagnostic (SI, MAS).** Ω = 1 − tuned, report only.
- **EQ2-6 Ω plateau.** Best Ω on the EWC arm lies in {0.71, 1, 1.41} on every carrier. FAIL
  otherwise. Never "Ω = 1 exactly". Ties in the seed mean are resolved toward the smallest Ω
  (the scorer's argmax over the grid in ascending order), which works against a PASS.
- **EQ2-7 Published baselines.** A-GEM, GradNorm (α = 0), MEGA-I vs the rule at Ω = 1, report;
  a baseline ahead by ≥ step on every carrier "dominates the rule".
- **EQ2-8 Diagnostic regime (report only).** Standardised features × 4 (the gate's mismatch
  regime): EWC coarse grid, rule at Ω = 1, reduction arm. Ω = 1 − tuned reported. Not a
  hypothesis; it says whether the gate's premise reappears on real features when the units are
  forced apart.
- **Any violated control → the mechanism statement above is falsified; the report says so in
  its first line, whatever EQ2-1 read.**

Outcomes named in advance: EQ2-1 PASS with EQ2-3/4 holding and EQ2-2 "does not reduce" → a
tuning-free normalised penalty step for Fisher-type penalties, on tabular MLP streams; EQ2-1
PASS with EQ2-2 "reduces" → a units-fixer applied once; EQ2-1 FAIL → no use on any existing
method on these streams; EQ2-0 not decidable → the study says only that the carriers did not
present the mismatch the claim needs; any control violated → back to the gate.

## Scoring script
`runs/eq2/frozen/eq2_score.py` (copy of `studies/eq2/eq2_score.py` at hash time), with
`runs/eq2/frozen/core.py` and `runs/eq2/frozen/CRR.md`; sha256 in `HASH.txt`. Two runs of one
unit must be byte-identical (`cmp`); the `uv.lock` sha256 is printed in every results header.

# Pre-registration — EQ2R: replication of EQ2 on its pre-registered fallback carriers, with three arrays

Written: 2026-09-18 (container clock; the commit carries the exact time; the push timestamp is the
external witness). Hash of this folder and the frozen scripts in `HASH.txt`. Owner request: prompt-log
entry 56 ("run an array of different continuous learning benchmark checks"), under the PASS levels
accepted the same day (CLAUDE.md §7; `docs/notes/2026-09-18_sharp_regime_review.md` §4).
**No data listed below has been opened. No file named below exists under `data/raw/` at hash time.**

## What this study is
A replication of study EQ2 (`prereg/eq2/PREREG.md`, tag `prereg-eq2-2026-09-17`, ledger rows EQ2-0…8,
EQ2-S; EQ2-1 re-labelled **PASS-0** in ledger row EQ2-1b) on the three PMLB streams EQ2 named as its
fallbacks and never opened. Under the accepted levels, a PASS-1 here that replicates EQ2-1 under a
fresh prereg on a later day (R3: 2026-09-18 against 2026-09-17) is the first candidate for **PASS-2**
in the repository. The design, constants, arms, tuning rule, resolvable step, sensitivity table and
rows EQ2R-0…8 are those of EQ2, unchanged (the scorer is a copy of the frozen EQ2 scorer with the
additions below and nothing else; `diff runs/eq2/frozen/eq2_score.py runs/eq2r/frozen/eq2r_score.py`
shows exactly the additions). Three arrays are added, each pre-registered here.

## Anchoring — read this first
OpenTimestamps calendars are unreachable from this environment (probe recorded in
`runs/eq2r/ots_attempt.txt`); tag pushes are refused by the remote (`runs/eq2r/tag_push_attempt.txt`).
The only external witness to "before" is the GitHub push timestamp of the commit carrying `HASH.txt`.
Under R2 this study is **weakly anchored**; every ledger row it produces carries
`anchor: push-timestamp only`. Consequently, by the accepted levels, **no row of this study can be
PASS-1 or PASS-2 on anchoring alone**: the strongest label available here is PASS-0 with the
replication noted, until Daniel stamps `HASH.txt` under the two-person protocol
(`docs/ROADMAP_2026-Q4.md` §1.2) or re-runs the frozen scripts on his machine.

## Hypothesis under test (unchanged from EQ2)
The rule `g = g_present + w · g_past`, `w = Ω · ‖ĝ_present‖ / ‖ĝ_past‖`, Ω = 1, is useful exactly
when the past term is the past task's loss or its Fisher-curvature approximation (online EWC),
redundant when the units already match (ER-sum), and harmful when the past term is a constraint that
is not a loss on the past task (DER++, LwF) or an importance penalty in other units (SI, MAS). EQ2
found the EWC clause held (fragile, cap-dependent), the ER-sum clause held, the DER++ clause was
violated on 2/3 carriers, and the SI/MAS clause did not show the expected miss. This study asks
whether each of those readings recurs on three new carriers.

## Gate (R4) — `gate_EQ2.txt`, committed here and covered by the hash
The same gate as EQ2, re-run on the current instrument on 2026-09-18: GATE OPEN (S-Y positive control
PASS; S-R, S-X, S-Y/LwF negative controls FAIL).

## Data (must be absent from data/SEEN.md — confirmed: none of these appears)
PMLB mirror on GitHub (LFS object via `media.githubusercontent.com`, pointer oid verified;
`data/fetch_pmlb.py --manifest eq2r`), downloaded after the push; sha256 of each file in
`data/manifests/eq2r.sha256`, echoed in every results file header; download date appended to
`data/SEEN.md` in the same commit.

| carrier (PMLB name) | classes in file | classes used | class-IL stream |
|---|---|---|---|
| `mfeat_karhunen` | 10 | 10 | 5 tasks × 2 classes |
| `mfeat_zernike` | 10 | 10 | 5 tasks × 2 classes |
| `vowel` | 11 | first 10 in remapped label order | 5 tasks × 2 classes |

No further fallbacks: a carrier that cannot be fetched or fails the oid check is reported as missing
and the rows needing "every carrier" are scored on the carriers present, with the denominator stated.
Split, standardisation, epochs, batch, score and quality gate exactly as EQ2.

## Instrument (all constants named; frozen in `runs/eq2r/frozen/eq2r_score.py`)
Identical to EQ2 (MLP d-256-K ReLU, SGD lr 0.05, batch 10, 3 epochs per task, seeds 0–4; EWC-online,
ER-sum, DER++, LwF, SI, MAS past terms; rule estimator EMA of gradient vectors, smooth 0.9, Euclidean
norm, cap 1e4, floor 1e-12; A-GEM, GradNorm α = 0, MEGA-I baselines; reduction arms; Ω grid
{0.5, 0.71, 1, 1.41, 2}; two-stage λ tuning; step = max(1.0 pt, 2 SE); sensitivity cap ∈ {10, 100,
1e4} × smooth ∈ {0.8, 0.9, 0.98}; x4 diagnostic regime). Additions, all named here and nowhere else:
- **Late-w record.** Every run also records `w_late_med`, the median derived weight over the last
  20 % of each task's steps (`LATE_FRAC = 0.2`), for EQ2R-D.
- **Capacity × epochs array.** On `mfeat_karhunen` only, the EWC coarse λ grid and the rule at Ω = 1
  are also run at (hidden, epochs) ∈ {(64, 1), (64, 3), (256, 1)}; the main cell (256, 3) completes
  the 2 × 2. Tuned λ, step and the rule are computed per cell as in the main design.

## Rows (scored once by `eq2r_score.py score`; per carrier and per seed values printed)
Aggregation, denominators, sidedness and strictness exactly as EQ2. Rows EQ2R-0 … EQ2R-8 are EQ2-0 …
EQ2-8 with the same thresholds and the same wording, on the new carriers. Three additional rows:

- **EQ2R-C Cap axis (a mechanism prediction).** EQ2-S found the pass "exists only with cap = 1e4"
  because a cap below the tuned λ turns the rule into a weaker fixed weight. Prediction, per carrier
  and per cap ∈ {10, 100, 1e4} at smooth 0.9: the rule at Ω = 1 is *not behind* the tuned λ by a step
  iff cap ≥ tuned λ. PASS iff the predicted pattern holds in all 9 cells. FAIL on any cell.
- **EQ2R-D Empty-present diagnostic (report only).** From the emptiness battery
  (`theory/retrodictions/emptiness.txt` row 7): as the present gradient vanishes the rule's weight on
  the past goes to zero. Report, per carrier, the median late-w against the whole-run median and the
  number of seeds whose late-w is below 1. No threshold; the row says whether the converged learner
  drops the past, which no ledger row has recorded.
- **EQ2R-A Capacity × epochs array (invariance).** On `mfeat_karhunen`, in each of the four cells,
  the rule at Ω = 1 is not behind the tuned λ by that cell's step. PASS iff ≥ 3 of 4 cells; FAIL
  otherwise. All four cells printed.
- **Replication summary (not a row).** The scorer prints whether EQ2R-1 passed, whether the
  sensitivity table is fragile, whether the controls hold and whether EQ2R-C passed. The ledger
  row that follows applies the accepted levels: PASS-0 if EQ2R-1 passes at all; the replication is
  noted against EQ2-1b; PASS-1 is unavailable here on anchoring (above), and is available to Daniel.

Outcomes named in advance: EQ2R-1 PASS with EQ2R-C PASS → the cap-dependence is the mechanism, not
an accident of EQ2's carriers; EQ2R-1 PASS with EQ2R-C FAIL → the pass is real but its mechanism
statement is wrong; EQ2R-1 FAIL → EQ2-1 does not replicate and stays PASS-0 with a failed
replication recorded beside it; EQ2R-4 violated again by DER++ → the harm clause is retired from the
mechanism statement; EQ2R-A FAIL → the effect is capacity- or exposure-specific and the roadmap says so.

## Scoring script
`runs/eq2r/frozen/eq2r_score.py` (copy of `studies/eq2r/eq2r_score.py` at hash time), with
`runs/eq2r/frozen/core.py`, `battery.py`, `gate.py` and `CRR.md`; sha256 in `HASH.txt`. Two runs of one
unit must be byte-identical (`cmp`); the `uv.lock` sha256 is printed in every results header.

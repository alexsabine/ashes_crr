# The instrument — `src/crr/instrument/core.py`

> Explanatory reference to the measurement library. The source of truth is
> [`src/crr/instrument/core.py`](../../src/crr/instrument/core.py) and its
> tests in [`tests/instrument/test_core.py`](../../tests/instrument/test_core.py);
> on any conflict, the source wins. The definitions implemented here are
> stated in [`theory/CRR.md`](../../theory/CRR.md) and summarised in
> [the primer](../theory/primer.md).

Import as `from crr.instrument.core import ...`. Every estimator constant
is a named argument (R5) — nothing is hidden in a default you cannot name
in a prereg. The library is extended, never bypassed (CLAUDE.md §3.1).

## Unit — A1′

### `unit_sigma(stat, detrend_window=9, detrend_order=2, scale="mad", min_sigma=None) -> float`

σ = robust scale of the residual of **one** occasion statistic across
occasions (A1′: the unit is the system's own resolvable step).

- `stat` — per-occasion statistic, computed on **training occasions only**.
- `detrend_window`, `detrend_order` — Savitzky–Golay detrender (window
  must be odd); named in the prereg.
- `scale` — `"mad"` → 1.4826·MAD (default); `"std"` → std (ddof=1).
- `min_sigma` — the instrument's quantisation step. If σ falls below it
  the record is **rejected (raises)**, never floored; there is **no
  additive ε** anywhere.

Edge cases (all raise `ValueError`): too few occasions for the named
detrender; degenerate residual (non-finite or non-positive σ); σ below
`min_sigma`. Covered by `test_unit_rejects_degenerate_and_has_no_floor`.

### `rho(extent, sigma) -> float`

Resolution (D1): ρ = extent/σ — the number of resolvable steps in one
monotone half-turn. **Reporting only** (R5): ρ is never used inside a
threshold, and CRR does not predict it. Added by the restructure PR
(audit #4) so every study can report ρ without re-deriving it.

## Arc, chord, surplus — D2, D3, D4, P1

### `arc_length(x, sigma=1.0, metric=None) -> float`

Real-valued Fisher–Rao arc length of a sampled path, in units of σ (D2).
No integer step counting. `x` is `(T,)` or `(T,d)`; `metric` is `None`
(identity), a `(d,)` diagonal g, or a `(d,d)` constant full g.
`test_arc_is_real_valued_not_floored` pins the reason a step counter is
inadmissible: a monotone move of 0.9σ gives C = 0.9 and S = 0, where an
integer counter would give C = 0 and S = −0.9.

### `chord(x, sigma=1.0, metric=None) -> float`

Geodesic (straight-line under the same metric) distance from the first to
the last sample, in units of σ (D3).

### `surplus(x, sigma=1.0, metric=None) -> (C, C*, S)`

Returns the tuple (C, C*, S) with S = C − C* ≥ 0 by P1 (the triangle
inequality — not a result of CRR; non-negativity holds up to
floating-point round-off); S = 0 iff the segment is
monotone in 1-D (D4). The report of any study must show the sign
distribution of S. Covered by
`test_surplus_nonnegative_and_zero_iff_monotone`.

## Phase and cuts — A3, D5

### `intrinsic_phase(x, detrend=True) -> np.ndarray`

Unwrapped analytic-signal phase in radians (Hilbert transform), mean
removed by default. This is **one** choice of intrinsic phase; a prereg
may name another (e.g. a Poincaré section) — when both exist, both are
reported.

### `antipodal_cuts(phase, start=0, half_turn=pi) -> np.ndarray`

**This IS the cut of A3.** Indices where the intrinsic phase has advanced
half a turn since the last cut; **oriented** — only forward crossings
count. The target advances by exactly `half_turn` from the previous
*target* (sub-sample, linearly interpolated), so discretisation does not
accumulate; the returned index is the sample nearest the interpolated
crossing. Post-fix (audit #4): the output is **strictly increasing** —
collisions from an undersampled phase are dropped, so no duplicate cut
can enter a per-occasion statistic. Covered by
`test_antipodal_cut_is_half_turn_on_a_sine` (spacing ≈ π on a sine).

### `peak_cuts(x, prominence, distance) -> np.ndarray`

Extremum-based segmentation (one maximum + one minimum per cycle via
`find_peaks`). **This is NOT the cut** — it exists so studies can show
where it disagrees with `antipodal_cuts`; results based on it alone say
nothing about A3 (CRR.md §2, R5). Covered by
`test_antipodal_and_peak_cuts_disagree_on_asymmetric_waveform`.

### `occasions(x, cuts, sigma=1.0) -> np.ndarray`

Per-occasion `(C, C*, S)` between consecutive cuts (D5): `surplus` on
each `[cuts[m], cuts[m+1]]` segment.

## Regularity — H-L5

### `cv(v) -> float`

Coefficient of variation, std(ddof=1)/mean. Post-fix (audit #4): the
convention is **unsigned** — the denominator is |mean|, so the CV of an
admissible unit quantity is non-negative by construction.

### `regularity(x, events, sigma=1.0, dt=1.0, n_boot=2000, seed=0) -> dict`

The H-L5 statistic: CV of the arc accumulated between consecutive
boundary events vs CV of the clock duration between the same events,
with a **paired bootstrap** (occasion resampling, `n_boot` draws, fixed
`seed`) 95% CI on the difference. Returns `n`, `cv_arc`, `cv_clock`,
`diff`, `ci95`, and `C_mean` (mean arc per occasion, in σ — added by
the restructure PR), plus the amplitude control's `cv_amp`, `diff_amp`
and `ci95_amp`. `events` are the sample indices of the **system's own**
boundary events; fewer than 3 raises `ValueError` (post-fix, audit #4).
The amplitude control (control i) is scored by its own paired
bootstrap — point CVs of arc vs amplitude tie at floating-point
precision on constant-period carriers, so the comparison runs on the
CI, not on strict point CVs. The identity-metric arc coincides with
`arc_length` in 1-D, so control (ii) has bite only in >1-D
(`theory/SCOPE.md` §2).

### `sign_test_units(unit_stats) -> (fraction, p)`

Per-unit sign test across levels/subjects (R6: the distribution is
shown, not just a median). Takes the list of per-unit `regularity()`
dicts and returns the fraction of units with `cv_arc < cv_clock` and
the exact two-sided binomial sign-test p-value. Added by the
restructure PR (audit #4) to complete the scoring surface §3.1 names.

## Learner path length — D6

### `kl_step(p_old, p_new) -> float`

Mean-over-probe KL(p_old ‖ p_new) for categorical predictive
distributions `(N, K)`; rows are renormalised after clipping
(post-fix, audit #4).

### `kl_gauss(mu_old, mu_new, var=1.0) -> float`

Mean-over-probe KL(N(mu_old, var) ‖ N(mu_new, var)) for fixed-variance
Gaussian predictives `(N,)` — the predictive family of a regression
model. Here √(2·KL) is the **exact** Fisher–Rao distance (proposed P8;
`test_kl_gauss_sqrt2kl_is_exact_fr_distance`).

### `path_length(snapshots, kl=kl_step) -> dict`

D6 quantities over a run's predictive snapshots on a fixed probe set:
returns `C` (Σ_t √(2·KL_t)), `E` (KL(p_0 ‖ p_T), the endpoint
displacement), `Cstar` (= √(2E)), `S` (C − C*). Post-fix (audit #4):
**fewer than 2 snapshots raises `ValueError`** — a path of one point
has no length.
Covered by `test_path_length_dominates_endpoint` and the single-straight-
step S = 0 case in `test_kl_gauss_sqrt2kl_is_exact_fr_distance`.

## What is deliberately absent

- **No regeneration estimator** — A6/P2/P3 are definitions and standard
  mathematics; nothing in the instrument claims to test them.
- **No peak-based cut in the H-L5/H-CUT scoring path** — `peak_cuts` is
  comparison-only (R5).
- **No ρ inside thresholds** — ρ is computed for reporting only by the
  `rho()` helper (D1, audit #4): resolution is a measured property of a
  system under an instrument, never a cut or threshold parameter.

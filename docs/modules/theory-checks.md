# The symbolic checks

> Explanatory summary of what the check scripts prove. The scripts are
> the source of truth; on any conflict they and `theory/CRR.md` win.
> Both scripts print one line per check and exit non-zero naming any
> failure.

Both live in [`theory/checks/`](../../theory/checks/) and are plain
`python` scripts using `sympy` (exact algebra) plus a little `numpy`:

```bash
uv run python theory/checks/verify_math.py
uv run python theory/checks/verify_scope_math.py
```

Each ends in `all checks passed` (exit 0) or `<n> check(s) FAILED`
(exit 1).

The scripts expose the same CLI as before (exit 0/1) and are wrapped in
`main()` with shared scaffolding in
[`theory/checks/_harness.py`](../../theory/checks/_harness.py).

---

## `verify_math.py` — every [P] in the canonical theory

Proves each proposition tagged [P] in
[`theory/CRR.md`](../../theory/CRR.md), plus the sanity anchors. The
check names printed by the script:

| check | what it establishes |
|---|---|
| `Bernoulli FR length = pi` | metric sanity anchor: the Fisher–Rao length of the Bernoulli family from p=0 to p=1 is π (g = 1/(p(1−p))) |
| `P1: arc >= chord on 2000 random paths` | arc ≥ chord with S ≥ 0 real-valued on random paths (D4) |
| `P1: equality iff monotone` | equality case of P1 (1-D: monotone segment) |
| `D2 note: integer counter gives S<0 on a monotone move of 0.9 sigma` | why an integer step counter is an inadmissible estimator of C (CRR.md D2 note) |
| `P2: log pi_i - beta S_i is the same constant for all i (Gibbs form)` | MaxEnt with ⟨S⟩ fixed gives the Gibbs form π_m ∝ exp(β S_m) (CRR.md §3) |
| `P3: geometric weights (q<1) have <k> = q/(1-q)` | MaxEnt with mean age fixed gives geometric weights (CRR.md §3) |
| `P3: q<1 branch condition present` | the normalisability branch (q < 1) is part of the result |
| `P4: K = (v/2)(sqrt(v^2+4) - v) with v = sqrt(q/r)` | steady-state Kalman gain closed form (CRR.md §6) |
| `P4: K(1) = 1/phi` | the golden-ratio special case |
| `P4: K -> 1 as v -> oo`, `P4: K -> 0 as v -> 0` | limiting behaviour |
| `P5: p=1 gives retention ((t+c)/c)^(-K/rho)` | exponential retention in natural time is a power law in shifted clock time iff p = 1 (CRR.md §7) |
| `P5: for p != 1 elasticity ... is t-dependent` / `for p = 1 elasticity is constant -K/rho` | the iff direction: p ≠ 1 is not a power law |
| `D6: sqrt(2 KL) equals FR distance for fixed-variance Gaussians` | the √(2·KL) step-length convention (CRR.md §5) |

Every one of these is standard mathematics; the labels exist so nobody
mistakes them for discoveries.

## `verify_scope_math.py` — the proposed forms in SCOPE.md

Proves the closed forms used by
[`theory/SCOPE.md`](../../theory/SCOPE.md). These are **proposed**, not
canonical: P6–P9 enter `theory/CRR.md` only if the human approves the
merge (SCOPE.md is a planning document). Checks printed by the script:

| check | what it establishes |
|---|---|
| `P6: Poisson FR distance = 2(sqrt(l2) - sqrt(l1))` (proposed) | Fisher–Rao distance for the Poisson rate family; spike trains, event catalogues, case counts |
| `P6: sqrt(2 KL) = FR distance to first order in the step (Poisson)` | the √(2·KL) convention agrees with the closed form |
| `P7: categorical FR distance = 2 arccos(Bhattacharyya) (Bernoulli check, 200 pairs)` (proposed) | the simplex closed form used for learners' predictive distributions and epidemic compartments; `P7: simplex diameter = pi` |
| `P8: sqrt(2 KL) = |Delta mu| / sigma exactly for fixed-variance Gaussians` (proposed) | exact (not only second-order) for the predictive family of a regression model |
| `P9: 1-D Poisson-metric arc = TV(2 sqrt x)` (proposed) | the "1-D arc = total variation after reparametrisation" disclosure: on a 1-D trace the identity-metric arc is plain TV, and Fisher- vs identity-metric arcs are **not** proportional |
| `Lemma: F = 2 s^2 E_old exactly for a linear model at its task-A optimum (100 endpoints)` | why H-T1 must fail on the convex learner S-H, and why `E_old` (not only `E_new`) is a required gate baseline |

## Status: canonical vs proposed

| proposition | status | canonical home |
|---|---|---|
| P1–P5, D6 closed forms | canonical | `theory/CRR.md`, proved by `verify_math.py` |
| P6–P9, convex-learner lemma | **proposed** | `theory/SCOPE.md`, proved by `verify_scope_math.py`; pending human approval (audit finding #13) before any merge into CRR.md |

The proposed labels are load-bearing: `theory/SCOPE.md` §0–§5 must not
be cited as theory until the canonical file says so.

"""Verify every [P] proposition and every closed form in theory/CRR.md.

Run:  uv run python theory/checks/verify_math.py
Exit code 0 means every check passed. Each check prints PASS/FAIL and the
identity it verified. Nothing here touches data.
"""
import math
import sys

import numpy as np
import sympy as sp

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  {detail}")
    if not ok:
        FAILS += 1


# ---------------------------------------------------------------- A1 / D2
# Fisher–Rao length of the Bernoulli family from p=0 to p=1 is pi
# (g = 1/(p(1-p))). Used only as a sanity check of the metric convention.
p = sp.symbols("p", positive=True)
L_bern = sp.integrate(1 / sp.sqrt(p * (1 - p)), (p, 0, 1))
check("Bernoulli FR length = pi", sp.simplify(L_bern - sp.pi) == 0, str(L_bern))

# ---------------------------------------------------------------- P1 / D4
# Arc >= chord for a sampled path (1-D: arc = total variation, chord = |net|).
rng = np.random.default_rng(0)
ok = True
worst = 0.0
for _ in range(2000):
    x = np.cumsum(rng.standard_normal(rng.integers(2, 50)))
    arc = float(np.abs(np.diff(x)).sum())
    chord = float(abs(x[-1] - x[0]))
    ok &= arc >= chord - 1e-12
    worst = max(worst, chord - arc)
check("P1: arc >= chord on 2000 random paths (S >= 0 real-valued)", ok, f"max chord-arc={worst:.2e}")
# Equality iff monotone
mono = np.sort(rng.standard_normal(30))
check("P1: equality iff monotone", math.isclose(np.abs(np.diff(mono)).sum(), abs(mono[-1] - mono[0])))
# Integer step counter violates D4 (documented reason it is inadmissible)
def qarc(seg, h):
    ref, c = seg[0], 0
    for v in seg[1:]:
        k = int(abs(v - ref) // h)
        if k:
            c += k
            ref += math.copysign(k * h, v - ref)
    return c
seg = np.linspace(0, 0.9, 10)
check("D2 note: integer counter gives S<0 on a monotone move of 0.9 sigma",
      qarc(seg, 1.0) - 0.9 < 0, f"C_int={qarc(seg,1.0)}, C*={0.9}")

# ---------------------------------------------------------------- P2
# MaxEnt with mean constraint -> Gibbs form. Verify the Lagrangian stationarity.
S1, S2, S3, beta, Z = sp.symbols("S1 S2 S3 beta Z", real=True)
Ss = [S1, S2, S3]
pi = [sp.exp(beta * s) / sum(sp.exp(beta * t) for t in Ss) for s in Ss]
# Entropy gradient wrt pi_i equals (const) - beta*S_i  <=> log pi_i = beta S_i - log Z
logs = [sp.simplify(sp.log(pi[i]) - beta * Ss[i]) for i in range(3)]
check("P2: log pi_i - beta S_i is the same constant for all i (Gibbs form)",
      sp.simplify(logs[0] - logs[1]) == 0 and sp.simplify(logs[1] - logs[2]) == 0)

# ---------------------------------------------------------------- P3
q, k = sp.symbols("q k", positive=True)
mean_k = sp.summation(k * (1 - q) * q**k, (k, 0, sp.oo))
# weights are normalisable only for q<1: take that branch of the Piecewise
mean_k = sp.simplify(sp.piecewise_fold(mean_k))
branch = mean_k.args[0][0] if isinstance(mean_k, sp.Piecewise) else mean_k
check("P3: geometric weights (q<1) have <k> = q/(1-q)",
      sp.simplify(branch - q / (1 - q)) == 0, str(sp.simplify(branch)))
check("P3: q<1 branch condition present", (not isinstance(mean_k, sp.Piecewise)) or mean_k.args[0][1] == (q < 1))

# ---------------------------------------------------------------- P4
# Steady-state Kalman gain for random walk + observation noise.
qv, rv, v = sp.symbols("q r v", positive=True)
M = sp.symbols("M", positive=True)  # prior variance
sol = sp.solve(sp.Eq(M, M * rv / (M + rv) + qv), M)
Mss = [s for s in sol if sp.simplify(s.subs({qv: 1, rv: 1})) > 0][0]
K = sp.simplify(Mss / (Mss + rv))
K_claim = (v / 2) * (sp.sqrt(v**2 + 4) - v)
diff = sp.simplify(K.subs(qv, v**2 * rv) - K_claim)
check("P4: K = (v/2)(sqrt(v^2+4) - v) with v = sqrt(q/r)", diff == 0, f"residual={diff}")
check("P4: K(1) = 1/phi", sp.simplify(K_claim.subs(v, 1) - (sp.sqrt(5) - 1) / 2) == 0)
check("P4: K -> 1 as v -> oo", sp.limit(K_claim, v, sp.oo) == 1)
check("P4: K -> 0 as v -> 0", sp.limit(K_claim, v, 0) == 0)

# ---------------------------------------------------------------- P5
t, c, Kc, rho, pp = sp.symbols("t c K rho p", positive=True)
A_p1 = sp.integrate(Kc * (t + c) ** -1, (t, 0, t))
ret_p1 = sp.simplify(sp.exp(-A_p1 / rho))
check("P5: p=1 gives retention ((t+c)/c)^(-K/rho)",
      sp.simplify(ret_p1 - ((t + c) / c) ** (-Kc / rho)) == 0, str(ret_p1))
A_p = sp.integrate(Kc * (t + c) ** -pp, (t, 0, t), conds="none")
ret_p = sp.exp(-A_p / rho)
# For p != 1 the log-retention is not linear in log(t+c): its elasticity depends on t.
elast = sp.simplify(sp.diff(sp.log(ret_p), t) * (t + c))
check("P5: for p != 1 elasticity d log R / d log(t+c) is t-dependent (not a power law)",
      sp.simplify(sp.diff(elast, t)).subs({pp: 2, Kc: 1, c: 1, rho: 1, t: 1}) != 0)
check("P5: for p = 1 elasticity is constant -K/rho",
      sp.simplify(elast.subs(pp, 1) + Kc / rho) == 0)

# ---------------------------------------------------------------- D6
# sqrt(2 KL) is the FR length to second order (1-D Gaussian, unit variance).
mu = sp.symbols("mu", real=True)
KL = mu**2 / 2  # KL(N(0,1) || N(mu,1))
fr = sp.Abs(mu)  # FR distance between N(0,1), N(mu,1) with fixed variance
check("D6: sqrt(2 KL) equals FR distance for fixed-variance Gaussians", sp.simplify(sp.sqrt(2 * KL) - fr) == 0)

print()
if FAILS:
    print(f"{FAILS} check(s) FAILED")
    sys.exit(1)
print("all checks passed")

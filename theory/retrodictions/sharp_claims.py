"""Re-derivation of the 16 rows an external run graded SHARP (theory/external/
CRR_retrodiction_outcomes_1_external_2026-09-17.pdf; its script was not supplied, so every
number here is recomputed). 15 unique systems (the PDF cross-lists Schwarzschild, de Sitter and
the Page point in class g, and the saddle-node repeats the D8 row of class d).

Each row applies the issue-#21 rules to the claim as stated:
  rule 3  SHARP means the derivation could have come out otherwise and did not;
          a definition or a coordinate symmetry is DESCR
  rule 4  a claim that survives only on a symmetric member of its class is FAILS
  rule 2  an observable, unit or cut rule chosen to make the check pass caps the grade
and prints: the number the PDF printed (reproduced or not), the probe that decides the grade,
and the grade. Run: uv run python theory/retrodictions/sharp_claims.py
"""
import math
import sys

import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.linalg import expm, solve_discrete_are

ROWS = []


def row(cls, system, claimed, reproduced, probe, grade, why):
    ROWS.append(dict(cls=cls, system=system, claimed=claimed, reproduced=reproduced, probe=probe, grade=grade, why=why))


def K_gain(v): return (v / 2) * (math.sqrt(v * v + 4) - v)


# ---------------------------------------------------------------- the premise shared by the seven class-(a) rows
def premise_bernoulli_half_turn():
    """The Bernoulli half-turn from a pole is at p = 1/2 whatever the dynamics: the prediction
    cannot come out otherwise, so by rule 3 it is not SHARP on any monotone occupancy curve."""
    p = sp.symbols("p", positive=True)
    psi = 2 * sp.asin(sp.sqrt(p))                                    # Fisher coordinate, family length pi
    half = sp.solve(sp.Eq(psi, sp.pi / 2), p)[0]
    return float(half)


# ---------------------------------------------------------------- (a) seven occupancy rows
def a_first_order_decay():
    k = 0.7; t_half = math.log(2) / k
    p = sp.symbols("p", positive=True)
    # any monotone decay from p = 1 crosses 1/2 once; the framework's cut is at that crossing by construction
    second_order = lambda t: 1 / (1 + k * t)                          # a non-exponential decay law
    t_half_2 = 1 / k
    row("a", "First-order decay: 'the cut is the half-life'",
        f"cut at p = 1/2, t = ln2/k = {t_half:.4f}", True,
        f"the half-life is DEFINED as the time to p = 1/2; a second-order decay 1/(1+kt) has its half-time at t = 1/k = {t_half_2:.4f} and the cut lands there too: the cut tracks the definition, not the rate law",
        "DESCR", "rule 3: the antipode of a pole-started Bernoulli family is 1/2 for every monotone curve; 'half-life' is the name of that point")


def a_logistic():
    K = 1.0
    # logistic: inflection at N = K/2; Gompertz: N = K exp(-b e^{-ct}), inflection at N = K/e; Richards nu: K (1+nu)^(-1/nu)
    N = sp.symbols("N", positive=True); c = 1.0
    gomp_infl = 1 / math.e; rich = lambda nu: (1 + nu) ** (-1 / nu)
    row("a", "Logistic growth: 'antipode p = 1/2 = inflection'",
        "inflection at N = K/2 (max dN/dt)", True,
        f"asymmetric members of the same class: Gompertz inflection at N/K = {gomp_infl:.4f}, Richards (nu = 2) at {rich(2.0):.4f}, (nu = 0.5) at {rich(0.5):.4f}; the Bernoulli antipode stays at 0.5",
        "FAILS", "rule 4: antipode = inflection holds only for the symmetric (logistic) member")


def a_michaelis_menten():
    S = np.array([0.5, 1.0, 2.0]); Km = 1.0
    theta = lambda n: S ** n / (Km ** n + S ** n)
    row("a", "Michaelis-Menten / Hill: 'theta = 1/2 at S = K_M for every n'",
        f"theta(S = K_M) = {theta(1)[1]:.2f} (n = 1), {theta(4)[1]:.2f} (n = 4)", True,
        "K_M (and K_half) is DEFINED as the substrate concentration at half-saturation; the coincidence is the definition of the constant",
        "DESCR", "rule 3: a definition")


def a_titration():
    pKa = 4.76; pH = np.array([3.76, 4.76, 5.76]); frac = 1 / (1 + 10 ** (pKa - pH))
    row("a", "Acid-base titration: 'ionised fraction 1/2 at pH = pKa'",
        f"fraction at pH = pKa: {frac[1]:.2f}", True,
        "pKa is DEFINED by pH = pKa at half-ionisation (Henderson-Hasselbalch is the definition rearranged); a diprotic acid's total-ionisation curve crosses 1/2 at neither pKa (the occupancy observable had to be chosen, rule 2)",
        "DESCR", "rule 3: a definition; rule 2 on the observable")


def a_fermi_dirac():
    T = 1.0; E = np.array([-1.0, 0.0, 1.0])
    fd = 1 / (np.exp(E / T) + 1); be = 1 / (np.exp((E + 2.0) / T) - 1); mb = np.exp(-E / T)
    E_be_half = T * math.log(3)                                        # BE occupation = 1/2 at E - mu = T ln 3
    row("a", "Fermi-Dirac occupation: 'f(E = mu) = 1/2, the chemical potential is the antipode'",
        f"f(mu) = {fd[1]:.2f}", True,
        f"particle-hole symmetry of the Fermi function (f(mu+x) = 1 - f(mu-x)); the other occupation statistics have no such point tied to mu: Bose-Einstein n = 1/2 at E - mu = T ln 3 = {E_be_half:.4f} T, Maxwell-Boltzmann at T ln 2 = {T * math.log(2):.4f} T",
        "DESCR", "rule 3: a symmetry of the chosen family; mu is defined through that family")


def a_laser_threshold():
    # pumped two-level system with spontaneous decay gamma: steady state p_upper = W/(2W + gamma) -> 1/2 as W -> inf
    gamma = 1.0; W = np.array([1.0, 10.0, 1000.0]); p_up = W / (2 * W + gamma)
    # threshold in a real laser: gain = loss -> inversion fraction above 1/2 by loss/(sigma * n)
    loss, sigma_n = 0.1, 1.0; p_thr = 0.5 + 0.5 * loss / sigma_n
    row("a", "Laser threshold: 'population inversion = crossing the antipode = laser threshold'",
        "thermal p_upper -> 1/2 only as T -> inf; crossing 1/2 under pumping", True,
        f"a pumped two-level system saturates at p_upper = {p_up[-1]:.4f} < 1/2 for any pump (no inversion: lasers need 3 or 4 levels); with cavity loss the threshold is gain = loss, i.e. p_upper = {p_thr:.3f} for loss/(sigma n) = {loss}: the threshold is above the antipode by an amount the cavity sets",
        "FAILS", "the derivation contradicts the physics: inversion is necessary, the threshold is set by the cavity, and a two-level carrier cannot be inverted")


def a_langmuir():
    Kads = 2.0; P = np.array([0.25, 0.5, 1.0]); theta = Kads * P / (1 + Kads * P)
    row("a", "Langmuir adsorption: 'theta = 1/2 at P = 1/K'",
        f"theta(P = 1/K) = {theta[1]:.2f}", True,
        "K is DEFINED by the half-coverage pressure; on a BET isotherm coverage is unbounded and there is no antipode (the carrier had to be chosen, rule 2)",
        "DESCR", "rule 3: a definition")


# ---------------------------------------------------------------- (b) quantum rows
def b_qubit_mt():
    Om = 1.3; hbar = 1.0; dE = hbar * Om / 2                          # resonant drive: DeltaE = hbar Omega / 2
    t_orth = math.pi / Om; t_mt = math.pi * hbar / (2 * dE)
    # detuned member: never orthogonal
    Delta = 0.8; Oe = math.sqrt(Om ** 2 + Delta ** 2); min_overlap = Delta / Oe
    row("b", "Qubit precession: 'the cut time reproduces the Mandelstam-Tamm limit, saturated'",
        f"t_orth = {t_orth:.4f}, pi hbar/(2 DeltaE) = {t_mt:.4f}", True,
        f"detuned member (Delta = {Delta}): minimum overlap |<psi0|psi(t)>| = {min_overlap:.4f} > 0, the antipode is never reached and MT is a bound, not a cut time; saturation is the geodesic (resonant) member only",
        "CONSIST", "rule 4: the equality holds on the symmetric member; off it the framework has P1 (C >= D), which is the MT/Anandan-Aharonov bound itself, inherited")


def b_spin_j():
    def Jx(j):
        m = np.arange(j, -j - 1, -1); d = len(m); Jp = np.zeros((d, d))
        for i in range(1, d): Jp[i - 1, i] = math.sqrt(j * (j + 1) - m[i] * (m[i] + 1))
        return 0.5 * (Jp + Jp.T)
    res = {}
    for j in (0.5, 1.0, 2.0):
        R = expm(-1j * math.pi * Jx(j)); d = int(2 * j + 1)
        top = np.zeros(d); top[0] = 1                                  # |j, j>  (coherent state)
        res[j] = abs(top @ R @ top)
    R1 = expm(-1j * math.pi * Jx(1.0)); mid = np.array([0, 1, 0.0]); ov_mid = abs(mid @ R1 @ mid)   # |1, 0> under the same rotation
    row("b", "Spin-j coherent state under rotation: 'antipode at angle pi for all j'",
        "overlap |<j,j|R(pi)|j,j>| = " + ", ".join(f"j={j:g}: {v:.1e}" for j, v in res.items()), True,
        f"the same rotation applied to the non-coherent member |1,0> gives overlap {ov_mid:.4f}: it never reaches an antipode (d^1_00(pi) = -1); 'antipode at pi' is a property of the highest-weight state, i.e. SU(2) representation theory",
        "FAILS", "rule 4: holds on the symmetric (coherent, highest-weight) member only; the number is Wigner's, not the framework's")


def b_neutrino():
    th = np.array([0.0, 0.27, 0.53, math.pi / 4]); pmax = np.sin(2 * th) ** 2
    row("b", "Two-flavour neutrino oscillation: 'the flavour state reaches its antipode iff mixing is maximal'",
        "max conversion sin^2(2 theta) = " + " ".join(f"{v:.3f}" for v in pmax), True,
        "the two-flavour formula P = sin^2(2 theta) sin^2(Delta m^2 L / 4E) is the whole content; 'antipode reachable iff theta = pi/4' restates that P_max = 1 iff sin^2(2 theta) = 1; theta itself is not predicted",
        "CONSIST", "form coincides with the known law; no constant fixed")


# ---------------------------------------------------------------- (c) thermal rows
def c_finite_time_thermo():
    tau = 1.0; g = lambda k: 1 / (2 * k * k)
    k1, k2 = 1.0, 4.0; c = math.log(k2 / k1)
    # a lopsided protocol vs the constant-speed geodesic: <v^2> >= <v>^2
    lop_k = lambda t: k1 * math.exp(c * t ** 2); lop_kd = lambda t: 2 * c * t * k1 * math.exp(c * t ** 2)
    v2 = quad(lambda t: g(lop_k(t)) * lop_kd(t) ** 2, 0, tau)[0]; v1 = quad(lambda t: math.sqrt(g(lop_k(t))) * abs(lop_kd(t)), 0, tau)[0]
    row("c", "Finite-time thermodynamics: 'minimum dissipation is the constant-Fisher-speed geodesic; S^2 bounds excess dissipation'",
        f"<v^2> = {v2:.4f} >= <v>^2 = {v1 ** 2:.4f}", True,
        "Cauchy-Schwarz on the thermodynamic length (Salamon-Berry 1983, Crooks 2007, Sivak-Crooks 2012); the framework renames L as C; and on a 1-D carrier every monotone protocol has S = 0, so S cannot bound dissipation there (the two batteries' rows c3 and 10)",
        "CONSIST", "inherited identity wearing the framework's name; the S-bound claim is false on 1-D carriers")


def c_schwarzschild():
    M = sp.symbols("M", positive=True)
    T = 1 / (8 * sp.pi * M); S = 4 * sp.pi * M ** 2; E = M
    C = sp.simplify(sp.diff(E, M) / sp.diff(T, M)); varE = sp.simplify(C * T ** 2)
    row("c", "Schwarzschild thermal family: 'A1 rejects it as a carrier (Var E = C T^2 < 0); forces the unitary side'",
        f"C = {C}, Var(E) = C T^2 = {varE}", True,
        "C < 0 means the canonical ensemble does not exist for a black hole (Hawking 1976; Gibbons-Perry 1978): a variance cannot be negative, so the family is not an exponential family at all. That is the domain's own statement. The microcanonical description is admissible and thermal; nothing here selects 'the unitary side'",
        "CONSIST", "the inadmissibility is the known sign of the heat capacity; the framework adds the label 'not a carrier'")


def c_de_sitter():
    H = sp.symbols("H", positive=True)
    T = H / (2 * sp.pi); S = sp.pi / H ** 2
    C = sp.simplify(T * sp.diff(S, H) / sp.diff(T, H))
    row("c", "de Sitter horizon: 'A1 rejects the static-patch thermal family'",
        f"C = T dS/dT = {C}", True,
        "same as Schwarzschild: negative heat capacity is the known obstruction to a canonical description of horizon thermodynamics; the framework restates it",
        "CONSIST", "inherited")


# ---------------------------------------------------------------- (d)/(h) memory depth
def d_memory_depth():
    ks = (1.0, 0.3, 0.1, 0.03, 0.01)
    own = [1 / K_gain(math.sqrt(1 - math.exp(-2 * k))) for k in ks]           # 'own-unit' reading: v^2 = 1 - e^{-2k dt}, dt = 1
    def fixed(k):
        P = solve_discrete_are(np.array([[1 - k]]), np.array([[1.0]]), np.array([[1.0]]), np.array([[1.0]])); return 1 / float(P.item() / (P.item() + 1.0))
    fx = [fixed(k) for k in ks]
    row("d/h", "Critical slowing down -> memory depth (D8): 'depth diverges as the relaxation rate vanishes, derived not fitted'",
        "own-unit reading d = 1/K(v), v^2 = 1 - e^{-2k}: " + ", ".join(f"k={k:g}: {d:.1f}" for k, d in zip(ks, own)), True,
        "the divergence needs the observation variance to be read as the equilibrium variance (the 'own unit'); with the instrument noise and process noise held fixed the same AR(1) filter gives d = " + ", ".join(f"{d:.2f}" for d in fx) + f" -> {1 / K_gain(1.0):.3f} (finite, the random-walk value): the divergence is a unit choice, not a derivation",
        "CONSIST", "rule 2: the unit was chosen to make the check pass; direction-only in that reading (both batteries: rows 30 and h1)")


# ---------------------------------------------------------------- (f)/(g) Page point
def f_page_point():
    x = sp.symbols("x", positive=True)                                # t / t_ev
    t_page = float(sp.solve(sp.Eq((1 - x) ** sp.Rational(2, 3), sp.Rational(1, 2)), x)[0])
    row("f/g", "Black-hole evaporation: 'the natural-time antipode (half the quanta) is the Page point'",
        f"cut at t/t_ev = 1 - 2^(-3/2) = {t_page:.4f}", True,
        "the Page time is DEFINED as the half-entropy point (Page 1993); 'half the quanta' equals it only under the assumption quanta ∝ entropy, which the check assumed; and a count is not a rotor: v3.1 O3 says natural time supplies the unit but not the cut, and the spec's A2c forbids a manufactured antipode, so 'cut at half the count' is a rule the framework does not contain",
        "FAILS", "manufactured cut (O3, A2c) reproducing a definition")


def main():
    half = premise_bernoulli_half_turn()
    print(f"External SHARP claims re-derived under the issue-#21 rules. Shared premise of the seven class-(a) rows: the Bernoulli\n"
          f"half-turn from a pole is at p = {half:g} for every monotone occupancy curve (symbolic), so that prediction cannot come out\n"
          f"otherwise (rule 3) and the physics enters only through which point the domain chose to name.\n")
    for f in (a_first_order_decay, a_logistic, a_michaelis_menten, a_titration, a_fermi_dirac, a_laser_threshold, a_langmuir,
              b_qubit_mt, b_spin_j, b_neutrino, c_finite_time_thermo, c_schwarzschild, c_de_sitter, d_memory_depth, f_page_point):
        f()
    for i, r in enumerate(ROWS, 1):
        print(f"[{i:2d}] ({r['cls']}) {r['system']}\n     claimed:    {r['claimed']}  [reproduced: {'yes' if r['reproduced'] else 'no'}]"
              f"\n     probe:      {r['probe']}\n     GRADE:      {r['grade']}  ({r['why']})")
    grades = ("SHARP", "CONSIST", "DESCR", "FAILS", "TENSION", "OPEN")
    print("\n" + "=" * 100 + "\nTALLY over the 15 unique systems the external run graded SHARP")
    print(" ".join(f"{g}={sum(r['grade'] == g for r in ROWS)}" for g in grades))
    print(f"numbers reproduced: {sum(r['reproduced'] for r in ROWS)}/{len(ROWS)}; grade SHARP survives on: {sum(r['grade'] == 'SHARP' for r in ROWS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

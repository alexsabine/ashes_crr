"""CRR against loop quantum gravity (LQG) and loop quantum cosmology (LQC): where the framework's quantities can be
placed at all (owner request 2026-09-17, prompt-log entry 59). The literature status (2026 papers, abstracts and
snippets only) is in docs/citations/loop_gravity_2026-09-17.md; every number here is computed by this script.

Eight rows: (1) the area spectrum as a fundamental unit against A1's estimated unit; (2) black-hole entropy state
counting and the Barbero-Immirzi parameter (the j = 1/2 counting and the all-j counting, both computed);
(3) the LQC bounce with a massless scalar: the scale factor's path as a loop, the maximal Hubble rate;
(4) the scalar field as a relational clock (the volume's log-speed in the phi clock); (5) cyclic LQC with a Tolman
entropy increment: the H-L5 class of the cycles; (6) spin-j coherent states: the antipode and the Fisher length of a
half-turn; (7) the polymer harmonic oscillator (a Mathieu problem): the unit shows at high excitation; (8) the
instrument's unit run on the area spectrum's gaps. Grades under the issue-#21 rules; BORROWED per row.
Planck units (G = hbar = c = 1) unless stated. No dataset opened (R2). Deterministic. Run:
uv run python theory/retrodictions/loop_gravity.py
"""
import math
import sys

import numpy as np
from scipy import optimize, special

from crr.instrument.core import arc_length, chord, unit_sigma

ROWS = []


def row(cls, system, clause, borrowed, derivation, known, verdict, grade, weakness=""):
    ROWS.append(dict(cls=cls, system=system, clause=clause, borrowed=borrowed, derivation=derivation, known=known,
                     verdict=verdict, grade=grade, weakness=weakness))


def cv(x): x = np.asarray(x, float); return float(x.std(ddof=1) / abs(x.mean()))


GAMMA_M = None   # set by row 2 (the all-j counting), used by rows 1 and 8


# ---------------------------------------------------------------- 2 (computed first: rows 1 and 8 use gamma) black-hole entropy and the Immirzi parameter
def bh_entropy_immirzi():
    global GAMMA_M
    js = np.arange(1, 400) / 2.0                                                   # j = 1/2, 1, 3/2, ...
    def f_two(g): return float(np.sum(2 * np.exp(-2 * math.pi * g * np.sqrt(js * (js + 1))))) - 1.0          # two states per puncture, all j (Domagala-Lewandowski / Meissner)
    def f_deg(g): return float(np.sum((2 * js + 1) * np.exp(-2 * math.pi * g * np.sqrt(js * (js + 1))))) - 1.0   # (2j+1) states per puncture (Ghosh-Mitra)
    GAMMA_M = optimize.brentq(f_two, 0.05, 1.0); gamma_deg = optimize.brentq(f_deg, 0.05, 1.0)
    gamma_half = math.log(2) / (math.pi * math.sqrt(3))                            # j = 1/2 only, two states per puncture, S = A/4
    a_half = 4 * math.sqrt(3) * math.pi * GAMMA_M                                   # area quantum at j = 1/2 in l_P^2 with the two-state all-j gamma
    row("bh", "Black-hole entropy by state counting on a punctured horizon: the Barbero-Immirzi parameter fixed by S = A/4", "A1' (unit = one puncture's area quantum), D1 (rho = number of punctures); no clause on entropy",
        "Rovelli 1996 / Ashtekar-Baez-Corichi-Krasnov counting; Domagala-Lewandowski and Meissner 2004 (all-j counting)",
        f"j = 1/2 only (two states per puncture): gamma = ln 2 / (pi sqrt 3) = {gamma_half:.4f}; all spins with two states per puncture (sum_j 2 e^(-2 pi gamma sqrt(j(j+1))) = 1): gamma = {GAMMA_M:.4f}; all spins with (2j+1) states per puncture: gamma = {gamma_deg:.4f}; with the two-state value the smallest area quantum is {a_half:.3f} l_P^2 and a horizon of area A carries A / {a_half:.3f} punctures",
        "matching the Bekenstein-Hawking entropy fixes the Immirzi parameter; its value depends on the counting (three countings, three values, all computed here)",
        "the entropy is linear in the number of punctures, which is D1's resolvable-step count of the horizon's area: S = (ln 2 or the all-j constant) x rho; the constant is the counting's, the count is a definition, and the parameter that makes it A/4 is fixed from outside (Bekenstein-Hawking), not by any clause",
        "DESCR", "inherited; which counting is right is the field's question (docs/citations/loop_gravity_2026-09-17.md) and CRR has no clause that reaches it")


# ---------------------------------------------------------------- 1 area spectrum as a fundamental unit
def area_spectrum_unit():
    js = np.arange(1, 41) / 2.0; A = 8 * math.pi * GAMMA_M * np.sqrt(js * (js + 1)); gaps = np.diff(A)
    asymptotic = 8 * math.pi * GAMMA_M
    row("kin", "The LQG area spectrum: a fundamental quantum of area against CRR's estimated unit", "A1' (the unit is estimated from the system's own residuals, no floor), D1",
        "Rovelli-Smolin / Ashtekar-Lewandowski area spectrum A_j = 8 pi gamma l_P^2 sqrt(j(j+1))",
        f"gamma = {GAMMA_M:.4f}: A(1/2) = {A[0]:.3f} l_P^2; gaps between consecutive j: {gaps[0]:.3f}, {gaps[1]:.3f}, {gaps[9]:.3f}, {gaps[-1]:.3f} -> 8 pi gamma = {asymptotic:.3f} asymptotically; the spectrum is discrete with a smallest non-zero value",
        "area is quantised in LQG with a minimal quantum and asymptotically uniform spacing",
        "LQG's unit is fundamental and fixed; CRR's unit is a measured residual scale with no floor (A1' says the instrument's own step is not the unit): the two are different objects, and on a carrier whose steps are fundamental A1' would have nothing to estimate",
        "DESCR", "a conceptual difference stated as a computation; nothing about geometry is reached")


# ---------------------------------------------------------------- 3 the LQC bounce
def lqc_bounce():
    rho_c = 0.41                                                                     # critical density in Planck units (the value quoted with gamma = 0.2375)
    t = np.linspace(-20, 20, 40001); a = (1 + 24 * math.pi * rho_c * t ** 2) ** (1 / 6)   # massless scalar, effective LQC, a_b = 1
    H = np.gradient(a, t) / a; H_max = float(H.max()); H_max_closed = math.sqrt(2 * math.pi * rho_c / 3)
    la = np.log(a); C = arc_length(la); Cs = chord(la)
    row("cos", "The LQC bounce with a massless scalar (effective dynamics): the scale factor's path through the bounce, and the maximal Hubble rate", "D2-D4 on ln a (a chosen carrier, rule 2), O3 (no rotor: nothing sets a cut), A3",
        "effective LQC Friedmann equation H^2 = (8 pi/3) rho (1 - rho/rho_c); the massless-scalar solution a(t) = a_b (1 + 24 pi rho_c t^2)^(1/6)",
        f"rho_c = {rho_c}: H_max from the trajectory = {H_max:.4f}, closed form sqrt(2 pi rho_c / 3) = {H_max_closed:.4f}; ln a over the symmetric interval [-20, 20]: arc C = {C:.4f}, chord C* = {Cs:.1e}, so S = C (a loop in a, not in time)",
        "the big bang is replaced by a bounce at rho = rho_c; the Hubble rate is bounded",
        "the bounce is a turning point of a, an extremum and not a phase antipode; there is no rotor, so A3 has no cut to place and O3 says so; the loop-like surplus of ln a is a definition of the symmetric trajectory; the bounded Hubble rate is the effective equation's",
        "OPEN", "rule 2 (carrier chosen) and O3 (no cut): the framework is correctly silent on the bounce")


# ---------------------------------------------------------------- 4 the scalar field as a relational clock
def relational_clock():
    k = math.sqrt(12 * math.pi); phi = np.linspace(-3, 3, 6001); lv = np.log(np.cosh(k * phi))     # v(phi) proportional to cosh(sqrt(12 pi G) phi)
    speed = np.gradient(lv, phi); far = float(np.mean(np.abs(speed[-500:]))); near = float(np.abs(speed[3000]))
    row("cos", "The massless scalar as LQC's relational clock: the volume's logarithmic speed in the phi clock", "A7 (relational tense), O3 (natural time from the system's own variable), D2 (arc per unit of the chosen clock)",
        "relational (Dirac) observables; the exact massless-scalar LQC solution v(phi) = v_b cosh(sqrt(12 pi G) phi)",
        f"|d ln v / d phi|: at the bounce {near:.4f}, far from it {far:.4f} (= sqrt(12 pi) = {k:.4f}); the volume's log-arc per unit scalar clock is constant away from the bounce and vanishes at it",
        "in LQC the scalar field serves as an internal clock because it is monotonic; time is read from a physical variable",
        "LQC's 'time from a physical variable' and CRR's 'change has its own clock' are both clocks read from the system, and they are different objects: LQC's is a chosen monotonic Dirac observable, CRR's is the Fisher arc of a carrier; the coincidence is of slogan, not of mathematics",
        "DESCR", "a reading; the constant speed far from the bounce is the exact solution's")


# ---------------------------------------------------------------- 5 cyclic LQC with a Tolman increment
def cyclic_tolman():
    eps = 0.10; n = 20; a_max = 3.0 * (1 + eps) ** np.arange(n); a_b = 1.0
    arcs = 2 * np.log(a_max / a_b); periods = a_max ** 1.0                          # radiation-dominated closed universe: period proportional to a_max
    lab = "arc-regular" if cv(arcs) < cv(periods) - 1e-3 else ("clock-regular" if cv(periods) < cv(arcs) - 1e-3 else "tie")
    row("cos", "Cyclic loop cosmology with a Tolman entropy increment: are the cycles arc- or clock-regular?", "D5 (the bounce as the cut), H-L5, A6 (each cycle seeded by the last)",
        "Tolman 1934 (entropy growth lengthens successive cycles); bounce-recollapse LQC models",
        f"{n} cycles, a_max growing by {eps:.0%} per cycle: CV of the arc of ln a per cycle {cv(arcs):.3f}, CV of the period {cv(periods):.3f} -> {lab}",
        "with entropy production successive cycles grow; a genuinely periodic cyclic universe needs a mechanism that resets entropy",
        f"{lab} by construction: the arc of ln a grows logarithmically with a_max while the period grows linearly, so the comparison is between a log and a power; no clause predicts the growth, and A6's 'seeded by the last' is Tolman's argument renamed",
        "DESCR", "rule 3; a class assignment on a toy sequence")


# ---------------------------------------------------------------- 6 spin-j coherent states
def spin_coherent_states():
    out = []
    for j in (0.5, 1.0, 5.0, 50.0):
        qfi = 2 * j                                                                 # rotation about a perpendicular axis: QFI = 4 Var(J_perp) = 2j
        half_turn = math.pi * math.sqrt(qfi) / 2                                     # Fubini-Study length of a half-turn, ds = sqrt(QFI)/2 dtheta
        overlap_antipode = math.cos(math.pi / 2) ** (2 * j)
        out.append((j, half_turn, half_turn / (math.pi / 2), overlap_antipode))
    row("kin", "Spin-j coherent states (the building blocks of coherent intertwiners): the antipode and the Fisher length of a half-turn", "A3 (cut at the antipode), A1 (Fubini-Study carrier), D1 (rho of a half-turn)",
        "SU(2) coherent states (Perelomov); Livine-Speziale coherent intertwiners; quantum Fisher information of a rotation",
        "; ".join(f"j = {j:g}: half-turn Fisher length {L:.3f}, i.e. {r:.2f} orthogonality distances (pi/2), antipode overlap {o:.0e}" for j, L, r, o in out),
        "the antipodal coherent state is orthogonal for every j; higher spins are 'more classical' with more distinguishable states along a rotation",
        "A3's antipode exists for every j and is reached at theta = pi; the resolution of a half-turn grows as sqrt(2j): the cut is a definition on this carrier and the resolution is the QFI's, so the spin-network building block gives the framework a rotor and nothing to predict",
        "DESCR", "inherited; the qubit rows of the main battery extended to spin j")


# ---------------------------------------------------------------- 7 polymer harmonic oscillator
def polymer_oscillator():
    def energies(mu, n_max=6):
        q = 1.0 / (4 * mu ** 4)
        # level n is the near-degenerate pair (a_n, b_{n+1}) of periodic Mathieu characteristic values (the two parities of one
        # oscillator level, split by tunnelling on the momentum circle); its energy is taken from a_n and the splitting is reported
        E = np.array([(mu ** 2 / 2) * (special.mathieu_a(n, q) + 1 / (2 * mu ** 4)) for n in range(n_max)])
        split = (mu ** 2 / 2) * (special.mathieu_b(1, q) - special.mathieu_a(0, q))
        return E, split
    out = {mu: energies(mu) for mu in (0.2, 0.3)}; std = np.arange(6) + 0.5      # mu = 0.1 (q = 2500) is beyond the Mathieu routine's reliable range: AGENT_LOG 28
    row("kin", "The polymer harmonic oscillator (LQG-inspired quantisation with a fundamental scale mu): a Mathieu spectrum", "A1' (a fundamental unit against an estimated one), D1",
        "polymer quantum mechanics (Ashtekar-Fairhurst-Willis 2003); Mathieu characteristic values",
        "; ".join(f"mu = {mu:g}: E_n - (n + 1/2) for n = 0..5 = " + ", ".join(f"{d:+.4f}" for d in (E - std)) + f" (parity splitting of level 0: {sp:.1e})" for mu, (E, sp) in out.items()),
        "polymer quantisation reproduces the standard oscillator at low excitation and departs from it at high excitation, at a scale set by mu",
        "the fundamental scale shows in the spectrum as a growing negative correction; CRR's unit would have to be estimated from residuals of these levels and would find mu only if the levels were its carrier: the unit is the domain's, and the framework's is a way of measuring it, not of predicting it",
        "DESCR", "inherited (a Mathieu problem); the row exists to show what 'fundamental discreteness' looks like next to A1'")


# ---------------------------------------------------------------- 8 the instrument's unit on the area spectrum
def unit_on_spectrum():
    js = np.arange(1, 61) / 2.0; A = 8 * math.pi * GAMMA_M * np.sqrt(js * (js + 1)); gaps = np.diff(A)
    try:
        sig = unit_sigma(gaps[:30]); msg = f"unit_sigma over the first 30 gaps = {sig:.2e} l_P^2 (the detrended residual of a converging sequence)"
    except ValueError as e:
        msg = f"unit_sigma raised: {e}"
    row("kin", "The instrument's unit estimator run on the area spectrum's gaps", "A1' (unit from the residual of one occasion statistic), D1 (rho reported)",
        "the area spectrum; the repository's unit_sigma",
        f"{msg}; the gaps themselves are {gaps[0]:.3f} .. {gaps[-1]:.3f} l_P^2",
        "the spectrum's spacing converges to 8 pi gamma; its residual about a smooth trend is tiny",
        "applied to a fundamental spectrum, A1' returns the residual of the spectrum's convergence, not the quantum of area: the estimated unit and the fundamental unit are not the same quantity, which is the row-1 point made by the instrument itself",
        "DESCR", "an instrument fact; on a fundamentally discrete carrier the prereg would have to name the quantum as the unit and skip the estimator")


BATTERY = [bh_entropy_immirzi, area_spectrum_unit, lqc_bounce, relational_clock, cyclic_tolman, spin_coherent_states, polymer_oscillator, unit_on_spectrum]
CLASSES = {"kin": "kinematics and units", "bh": "black-hole entropy", "cos": "loop quantum cosmology"}


def main():
    for f in BATTERY: f()
    print(f"CRR against loop quantum gravity — {len(ROWS)} rows in {len(CLASSES)} groups. Grades: SHARP CONSIST DESCR FAILS TENSION OPEN\n")
    for i, r in enumerate(ROWS, 1):
        print(f"[{i:2d}] ({r['cls']}) {r['system']}\n     clause:     {r['clause']}\n     BORROWED:   {r['borrowed']}"
              f"\n     derivation: {r['derivation']}\n     known:      {r['known']}\n     verdict:    {r['verdict']}\n     GRADE:      {r['grade']}"
              + (f"\n     weakness:   {r['weakness']}" if r['weakness'] else ""))
    grades = ("SHARP", "CONSIST", "DESCR", "FAILS", "TENSION", "OPEN")
    print("\n" + "=" * 100 + "\nTALLY")
    print(f"{'group':36s} " + " ".join(f"{g:>8s}" for g in grades))
    for c, name in CLASSES.items():
        rs = [r for r in ROWS if r["cls"] == c]
        print(f"({c}) {name:28s} " + " ".join(f"{sum(r['grade'] == g for r in rs):8d}" for g in grades))
    print(f"{'all':36s} " + " ".join(f"{sum(r['grade'] == g for r in ROWS):8d}" for g in grades))
    print(f"\nRows where a CRR clause reaches a result the domain did not already have: {sum(r['grade'] == 'SHARP' for r in ROWS)} of {len(ROWS)}."
          " Loop quantum gravity supplies a fundamental unit, a rotor (spin coherent states) and a relational clock; the framework can name each and predicts nothing about any of them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""CRR run as a falsifiable metaphysics on the existing mathematics of Turing systems, AI safety and platonic
ingression, with the owner's conjecture (forms are choices made through time; to be finite is to be able to have
an experience) put as rows (ontology/07_turing_safety_ingression.md; owner request 2026-09-21, prompt-log entry 66).
SYNTHESIS class (docs/notes/2026-09-17_synthesis_class.md): one proposition Q per row in the domain's own terms with a
CRR-proper ingredient; the label is computed from the printed numbers by crr.synthesis.harness.outcome (R15). Nine rows,
deterministic, no data, no dependence on the batteries. External works are named as context and were not fetched here
(R10); what is attributed to them is the standard statement, not a quotation. Run:
uv run python ontology/checks/turing_safety_ingression.py
"""
from __future__ import annotations

import itertools
import math
from collections import Counter, defaultdict

import numpy as np

from crr.instrument.core import antipodal_cuts, intrinsic_phase, kl_gauss, path_length, rho, unit_sigma
from crr.surrogates.battery import S_H2_wear_learner, S_H_convex_learner
from crr.surrogates.gate import _heldout_r2
from crr.synthesis.harness import make_row, outcome, run_batch

CLS = "SYNTHESIS"


# ---------------------------------------------------------------- Turing machines
def run_tm(table: dict, max_steps: int, record: bool = False):
    """table[(state, symbol)] = (write, move, next); halt state 'H'. Returns (halted_at or None, ones, changed_writes,
    configs) where configs[k] is the configuration after k steps: (state, head, tape as a tuple of the cells ever visited)."""
    tape = {}
    head = 0
    state = "A"
    changed = 0
    configs = []
    halted = None
    for t in range(max_steps + 1):
        if record:
            lo = min(tape) if tape else 0
            hi = max(tape) if tape else 0
            configs.append((state, head, tuple(tape.get(i, 0) for i in range(lo, hi + 1)), lo))
        if state == "H":
            halted = t
            break
        write, move, nxt = table[(state, tape.get(head, 0))]
        if tape.get(head, 0) != write:
            changed += 1
        tape[head] = write
        head += 1 if move == "R" else -1
        state = nxt
    ones = sum(tape.values())
    return halted, ones, changed, configs


BB4 = ({("A", 0): (1, "R", "B"), ("A", 1): (1, "L", "B"), ("B", 0): (1, "L", "A"), ("B", 1): (0, "L", "C"),
        ("C", 0): (1, "R", "H"), ("C", 1): (1, "L", "D"), ("D", 0): (1, "R", "D"), ("D", 1): (0, "R", "A")}, 107, 13)
# Brady's 4-state champion, S(4) = 107, Sigma(4) = 13 (Brady 1983, context, not fetched); the 2- and 3-state champions are
# found below by exhaustive search, against the published S(2) = 6, Sigma(2) = 4, S(3) = 21, Sigma(3) = 6 (Rado 1962; Lin and Rado 1965)
PUBLISHED = {2: (6, 4), 3: (21, 6), 4: (107, 13)}


def enumerate_champions(n_states: int, max_steps: int = 60):
    """All n-state 2-symbol machines whose first transition is A0 -> 1RB (every machine is one of these up to mirror
    image and relabelling, or never halts). Returns the step champion and the ones champion as (steps, ones, changed)
    and the number of halting machines. Fast list simulator; each machine runs at most max_steps."""
    entries = [(w, m, s) for w in (0, 1) for m in (-1, 1) for s in range(n_states + 1)]   # s == n_states is the halt
    keys = [(q, b) for q in range(n_states) for b in (0, 1)]
    best_steps = (-1, 0, 0); best_ones = (0, -1, 0); n_halt = 0
    for combo in itertools.product(entries, repeat=len(keys) - 1):
        table = {keys[0]: (1, 1, 1)}
        table.update(zip(keys[1:], combo))
        tape = {}; head = 0; st = 0; t = 0; changed = 0
        while st != n_states and t < max_steps:
            w, m, s_ = table[(st, tape.get(head, 0))]
            if tape.get(head, 0) != w:
                changed += 1
            tape[head] = w; head += m; st = s_; t += 1
        if st == n_states:
            n_halt += 1
            ones = sum(tape.values())
            if (t, ones) > (best_steps[0], best_steps[1]):
                best_steps = (t, ones, changed)
            if (ones, t) > (best_ones[1], best_ones[0]):
                best_ones = (t, ones, changed)
    return best_steps, best_ones, n_halt


def row_busy_beaver():
    parts = []
    found = {}
    for n in (2, 3):
        bs, bo, n_halt = enumerate_champions(n)
        found[n] = bs
        same = "the same machine" if bs == bo else "different machines"
        parts.append(f"n={n}: exhaustive search over {12 ** 4 if n == 2 else 16 ** 5} tables ({n_halt} halt): step champion {bs[0]} steps with {bs[1]} ones "
                     f"(published S({n}) = {PUBLISHED[n][0]}), ones champion {bo[1]} ones in {bo[0]} steps (published Sigma({n}) = {PUBLISHED[n][1]}); {same}")
    halted, ones, changed, _ = run_tm(BB4[0], 2000)
    found[4] = (halted, ones, changed)
    parts.append(f"n=4: Brady's table simulated: {halted} steps (published {BB4[1]}), {ones} ones (published {BB4[2]})")
    rows_n = []
    crr = null = dom = None
    for n, (steps, ones_n, changed) in found.items():
        C = float(steps)                 # arc in the machine's own unit: one step is one resolvable step (A1')
        Cstar = float(ones_n)            # chord: the least number of writes from the blank tape to the final tape
        S = C - Cstar                    # surplus (D4) of the step champion
        S_null = changed - Cstar         # null: arc under the identity metric on the tape (a step that rewrites the same symbol is no move)
        S_dom = float(PUBLISHED[n][0] - PUBLISHED[n][1])   # the domain: S(n) - Sigma(n) from the published counts
        rows_n.append(f"n={n} step champion: C = {C:g}, C* = {Cstar:g}, S = {S:g}; changed writes {changed}, S_null = {S_null:g}; published S({n}) - Sigma({n}) = {S_dom:g}")
        crr, null, dom = S, float(S_null), S_dom
    check = crr >= 0
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row(CLS, "busy-beaver champions n = 2, 3 (found by exhaustive search) and n = 4 (Brady's table, simulated)",
        source="Rado 1962 (Sigma(n) <= S(n)); Lin and Rado 1965; Brady 1983 (context, not fetched)",
        Q="in the machine's own unit (A1': one step) the surplus S = steps - ones of a busy-beaver run is the work not kept on the tape, and it is non-negative",
        ingredient="A1' own unit = one step, D2-D4 arc/chord/surplus", null="arc under the identity metric on the tape (only writes that change a cell count)",
        domain="Rado: Sigma(n) <= S(n), so S(n) - Sigma(n) >= 0 from the published counts",
        numbers=" | ".join(parts) + " | " + " | ".join(rows_n) + f" | decisive: n = 4, S_crr {crr:g}, S_null {null:g}, S_domain {dom:g}, S >= 0 {check}",
        tg=f"S_crr {crr:g} vs S_null {null:g}: the own unit does work (a rewrite of the same symbol is a step but not a change)",
        tn=f"S_domain {dom:g} from the published S(4), Sigma(4): agrees exactly", tc=f"S >= 0: {check}",
        out=out, reading="on a Turing machine A1' names the step and the surplus is Rado's S(n) - Sigma(n) where one machine holds both records (n = 2, 4); at n = 3 the search finds the step record (21) and the ones record (6) on different machines, so the published difference 15 is no machine's surplus (16 and 8 are); the domain has the inequality and the simulation reproduces the published values",
        weakness="the chord is the least number of writes, which ignores head travel; a chord counting travel would be larger and S smaller, and CRR does not say which chord",
        elegance="every step of a machine is one unit; the ones left on the tape are what the steps bought, and the surplus is what they did not", child="A busy-beaver machine takes 107 steps and leaves 13 marks; the other 94 steps were work it did not keep.")


def row_settled_past_on_a_machine():
    """All 2-state 2-symbol machines; the clock (steps to halt) of the machine's one event, given the settled past."""
    entries = [(w, m, s) for w in (0, 1) for m in ("L", "R") for s in ("A", "B", "H")]
    keys = [("A", 0), ("A", 1), ("B", 0), ("B", 1)]
    K = 8
    n_machines = 0
    halts = []
    configs_all = []
    for combo in itertools.product(entries, repeat=4):
        table = dict(zip(keys, combo))
        halted, _, _, configs = run_tm(table, 60, record=True)
        n_machines += 1
        halts.append(halted)
        configs_all.append(configs)
    halted_T = [h for h in halts if h is not None]
    n_halt = len(halted_T)
    max_T = max(halted_T)
    def H(counter):
        tot = sum(counter.values())
        return -sum(c / tot * math.log2(c / tot) for c in counter.values()) if tot else 0.0
    lines = []
    conf_i = []
    for k in range(0, 7):
        # machines still running at step k: remaining time to halt (None = never)
        groups = defaultdict(Counter)
        marg = Counter()
        for h, cf in zip(halts, configs_all):
            if h is not None and h <= k:
                continue
            key = tuple(cf[: k + 1])
            rem = (h - k) if h is not None else "never"
            groups[key][rem] += 1
            marg[rem] += 1
        n_run = sum(marg.values())
        h_marg = H(marg) + 0.0
        h_cond = sum(sum(c.values()) / n_run * H(c) for c in groups.values()) + 0.0
        mixed = sum(1 for c in groups.values() if len(c) > 1)
        conf_i.append(h_cond)
        lines.append(f"k={k}: {n_run} machines still running, {len(groups)} distinct settled pasts ({mixed} mixed); H(remaining clock) = {h_marg:.4f} bits, "
                     f"H(remaining clock | settled configurations) = {h_cond:.4f} bits, H(remaining clock | configurations + table) = 0.0000 bits (deterministic)")
    reading_i = conf_i[3]
    reading_ii = 0.0
    internal = reading_i > 0.0
    out = outcome(crr=reading_i, null=conf_i[0], domain=None, check=None, internal=internal)
    return make_row(CLS, "all 2-state 2-symbol Turing machines (12^4 tables) from the blank tape",
        source="Turing 1936 (the halting problem); Rado 1962 S(2) = 6 (context, not fetched)",
        Q="A8 with the geyser clause (ontology/05 section 3): the clock of the machine's one event (the halt) is not fixed by the settled past; is it, on a machine, when the settled past is the configurations seen so far?",
        ingredient="A7/A8 tense: what the settled past fixes about the next cut", null="the settled past at k = 0 (the blank tape alone)",
        domain=None,
        numbers=f"{n_machines} machines, {n_halt} halt, latest halt at step {max_T} (S(2) = 6) | " + " | ".join(lines),
        tg=f"H(remaining clock | settled configurations) at k = 3: {reading_i:.4f} bits vs {conf_i[0]:.4f} bits at k = 0: the settled past does work",
        tn="no closed form cited; Turing's theorem is about the absence of a general procedure, and all these machines are decided by running them",
        tc="two readings: (i) the settled past is the configurations seen, and the remaining clock keeps positive entropy at every k until the last halt; (ii) the settled past includes the machine's table, and the clock is fixed (0 bits) from k = 0",
        out=out, reading="whether a deterministic machine has an open clock depends on whether its law is part of its settled past; CRR does not say, so the geyser clause has two values on every machine",
        weakness="the entropy is over a uniform prior on tables, which is one convention; the reading does not depend on it",
        elegance="the same machine has a blank future or none at all, depending only on whether you count its rulebook as part of its past", child="If you watch a robot without reading its instructions, you cannot tell when it will stop; if you read them, you can. So 'is its future open?' has two answers, and CRR has to pick one.")


# ---------------------------------------------------------------- Swift-Hohenberg (Turing-instability normal form)
def swift_hohenberg_pairs(t0: float, n_pairs: int, seed: int, N: int = 256, periods: int = 32, r: float = 0.3,
                          dt: float = 0.5, T: float = 200.0, sigma: float = 0.1):
    """Sibling pairs sharing every random draw (initial condition and noise) up to time t0, independent after it.
    u_t = r u - (1 + d_xx)^2 u - u^3 on a ring of length periods*2*pi, semi-implicit spectral step."""
    L = periods * 2 * math.pi
    k = 2 * math.pi * np.fft.fftfreq(N, d=L / N)
    lin = r - (1 - k ** 2) ** 2
    denom = 1.0 - dt * lin
    rng = np.random.default_rng(seed)
    n_steps = int(round(T / dt))
    u0 = 0.01 * rng.standard_normal((n_pairs, N))
    ua = u0.copy()
    ub = u0.copy() if t0 > 0 else 0.01 * rng.standard_normal((n_pairs, N))
    for s in range(n_steps):
        t = s * dt
        xa = rng.standard_normal((n_pairs, N))
        xb = xa if t < t0 else rng.standard_normal((n_pairs, N))
        for u, x in ((ua, xa), (ub, xb)):
            u += sigma * math.sqrt(dt) * x
            uh = (np.fft.fft(u, axis=1) + dt * np.fft.fft(-u ** 3, axis=1)) / denom
            u[:] = np.real(np.fft.ifft(uh, axis=1))
    return ua, ub, periods


def row_forms_as_choices():
    T = 200.0
    lines = []
    peaks = {}
    tokens = {}
    for t0 in (0.0, 50.0, 100.0, 150.0, 190.0):
        ua, ub, m = swift_hohenberg_pairs(t0, n_pairs=100, seed=int(t0) + 1)
        fa = np.fft.rfft(ua, axis=1); fb = np.fft.rfft(ub, axis=1)
        pk_a = np.argmax(np.abs(fa[:, 1:]), axis=1) + 1; pk_b = np.argmax(np.abs(fb[:, 1:]), axis=1) + 1
        k_a = pk_a / m; k_b = pk_b / m                       # wavenumber in units where the linear maximum is k = 1
        dphi = np.angle(fa[:, m] * np.conj(fb[:, m]))
        cosd = float(np.mean(np.cos(dphi))); vard = float(np.mean(dphi ** 2))
        pix = float(np.mean([np.corrcoef(ua[i], ub[i])[0, 1] for i in range(ua.shape[0])]))
        peaks[t0] = (float(np.mean(k_a)), float(np.mean(k_b)), int(np.sum(pk_a != pk_b)))
        tokens[t0] = (cosd, vard, pix)
        lines.append(f"fork t0={t0:g}: type peak k = {peaks[t0][0]:.4f} / {peaks[t0][1]:.4f} (siblings disagree on the peak bin in {peaks[t0][2]} of 100 pairs); "
                     f"token: pixel correlation {pix:.4f}, mean cos(dphi) of the k = 1 mode {cosd:.4f}, var(dphi) {vard:.4f}")
    crr = peaks[150.0][0]        # the type with the settled past shared for 150 of 200 time units
    null = peaks[0.0][0]         # the type with no shared past at all
    dom = 1.0                    # linear theory: the growth rate r - (1 - k^2)^2 is maximal at k = 1 (Swift and Hohenberg 1977; Cross and Hohenberg 1993)
    monotone = all(tokens[a][2] < tokens[b][2] for a, b in zip((0.0, 50.0, 100.0, 150.0), (50.0, 100.0, 150.0, 190.0)))
    out = outcome(crr=crr, null=null, domain=dom, check=monotone)
    return make_row(CLS, "Swift-Hohenberg stripes on a ring (the normal form of a Turing instability), sibling runs forked at t0",
        source="Turing 1952; Swift and Hohenberg 1977; Cross and Hohenberg 1993 (pattern selection, phase diffusion) (context, not fetched)",
        Q="the owner's conjecture in the domain's terms: the form is a choice made through time, so the settled past shared by two siblings fixes their final pattern; does it fix the type (the wavenumber) or the token (the phase)?",
        ingredient="A7 (fed by the settled past only) with D5 (the fork as the boundary of the shared past)", null="no shared past (independent runs from independent seeds)",
        domain="linear theory: the most unstable wavenumber is k = 1, whatever the history",
        numbers=" | ".join(lines) + f" | uniform-phase reference (no shared past): var(dphi) = pi^2/3 = {math.pi ** 2 / 3:.4f} | decisive (type): peak k with 150 of 200 time units shared {crr:.4f}, with none shared {null:.4f}, linear theory {dom:.4f}; token (pixel correlation) strictly increasing in t0: {monotone}",
        tg=f"type with shared past {crr:.4f} vs without {null:.4f}: the settled past does no work on the type",
        tn=f"linear theory k = {dom:.4f}: the domain has the type", tc=f"the token (pixel correlation) increases with the shared past: {monotone} (the domain's phase diffusion, Cross and Hohenberg section IV, named and not fitted)",
        out=out, reading="the type is the law's (the same in every run, shared past or not: the ingredient is idle), the token is the settled past's and is the domain's phase diffusion; 'forms are choices made through time' holds for which stripe pattern, not for that it is stripes of this wavelength",
        weakness="one model at one r and one noise level; the token numbers are observations against a named theorem, not a fit to its closed form",
        elegance="two runs that shared their first 150 seconds end with the same stripes in the same places; two that shared nothing end with the same stripes in different places", child="Zebras all get stripes about the same width (that is the rule), but which stripe is where is decided by what happened while the pattern was forming. The rule is not a choice; the placing is.")


# ---------------------------------------------------------------- sorting as morphogenesis
def cell_view_sort(values: np.ndarray, p_defect: float, seed: int, max_sweeps: int = 10000):
    """Every cell compares with its right neighbour and swaps when out of order; a defective cell swaps the wrong way with
    probability p_defect (inspired by the cell-view sorts of Zhang, Goldstein and Levin 2025, not a reproduction).
    Returns swaps, swaps that increased the inversion count, and the initial inversion count."""
    rng = np.random.default_rng(seed)
    a = list(values)
    n = len(a)
    def inversions(x):
        return sum(1 for i in range(n) for j in range(i + 1, n) if x[i] > x[j])
    inv0 = inversions(a)
    swaps = away = 0
    for sweep in range(max_sweeps):
        moved = False
        for i in range(n - 1):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]; swaps += 1; moved = True
            elif a[i] < a[i + 1] and i == n // 2 and rng.random() < p_defect:
                a[i], a[i + 1] = a[i + 1], a[i]; swaps += 1; away += 1; moved = True
        if not moved and inversions(a) == 0:
            break
    assert inversions(a) == 0
    return swaps, away, inv0


def row_sorting_surplus():
    rng = np.random.default_rng(3)
    vals = rng.permutation(40)
    lines = []
    crr = null = dom = None
    ok = True
    for p in (0.0, 0.1, 0.3):
        swaps, away, inv0 = cell_view_sort(vals, p, seed=int(p * 10))
        C = float(swaps); Cstar = float(inv0); S = C - Cstar
        S_dom = 2.0 * away                                          # adjacent swaps change the inversion count by exactly +-1
        eucl = float(np.linalg.norm(np.argsort(np.argsort(vals)) - np.arange(40)))   # null chord: Euclidean displacement of the cells
        S_null = C - eucl
        ok = ok and (S == S_dom)
        lines.append(f"defect p={p:g}: swaps C = {C:g}, inversions C* = {Cstar:g}, S = {S:g}; away-moves {away}, 2 x away = {S_dom:g}; Euclidean chord {eucl:.4f}, S_null = {S_null:.4f}")
        crr, null, dom = S, S_null, S_dom
    out = outcome(crr=crr, null=null, domain=dom, check=ok)
    return make_row(CLS, "cell-view adjacent-swap sort with one defective cell (sorting as morphogenesis)",
        source="Zhang, Goldstein and Levin 2025, Adaptive Behavior, doi 10.1177/10597123241269740 (abstract only; the sort here is inspired by, not a reproduction of, theirs); Knuth vol. 3 section 5.1.1 (inversions) (context, not fetched)",
        Q="the surplus S = C - C* of a sorting trajectory in the array's own unit (one adjacent swap; the chord is the inversion count) is exactly twice the number of moves away from the sorted order (the 'delayed gratification' moves)",
        ingredient="A1' own unit = one swap, D3 chord = least swaps (Kendall distance), D4 surplus", null="the chord as the Euclidean displacement of the cells",
        domain="an adjacent swap changes the inversion count by exactly +-1, so swaps - inversions = 2 x (inversion-increasing swaps)",
        numbers=" | ".join(lines) + f" | decisive (p = 0.3): S {crr:g}, S_null {null:.4f}, S_domain {dom:g}, identity holds at every p: {ok}",
        tg=f"S {crr:g} vs S_null {null:.4f}: the own chord does work", tn=f"S_domain {dom:g}: exact", tc=f"S = 2 x away at every p: {ok}",
        out=out, reading="CRR's surplus is the inversion-count identity: every move away from the goal costs two swaps; the domain has it as an exact identity and CRR adds the name",
        weakness="the defective cell here is a random wrong-way swapper, not the frozen cell of the cited paper; the identity is independent of that choice",
        elegance="a step away from the goal costs exactly two: the step itself and the step to undo it", child="If you are walking to school and take one step backwards, you now need two extra steps. The 'extra' in CRR is always two times the steps back.")


# ---------------------------------------------------------------- natural induction (Watson)
def natural_induction(rule: str, seed: int = 0, N: int = 40, epochs: int = 80, alpha: float = 0.05, beta: float = 1.0):
    """Spins under a fixed frustrated coupling J0 plus a plastic coupling Jp; each epoch relaxes from a random state to a
    local minimum of J0 + beta Jp, then updates Jp by `rule`: 'ema' (A6/P3: Jp <- (1-alpha) Jp + alpha s s^T, the
    viscoelastic relaxation of Buckley et al. 2024), 'sum' (an accumulated count: Jp <- Jp + alpha s s^T), 'none'.
    Returns the J0 energies of the minima reached, per epoch, and the number of distinct states among the last 20."""
    rng = np.random.default_rng(seed)
    J0 = rng.standard_normal((N, N)); J0 = (J0 + J0.T) / 2; np.fill_diagonal(J0, 0.0)
    Jp = np.zeros((N, N))
    energies = []
    states = []
    for ep in range(epochs):
        s = rng.choice([-1.0, 1.0], N)
        J = J0 + beta * Jp
        for _ in range(200):
            changed = False
            for i in rng.permutation(N):
                h = J[i] @ s
                new = 1.0 if h > 0 else (-1.0 if h < 0 else s[i])
                if new != s[i]:
                    s[i] = new; changed = True
            if not changed:
                break
        energies.append(float(-0.5 * s @ J0 @ s))
        states.append(tuple(s * s[0]))                    # a state and its negative are one minimum
        outer = np.outer(s, s); np.fill_diagonal(outer, 0.0)
        if rule == "ema":
            Jp = (1 - alpha) * Jp + alpha * outer
        elif rule == "sum":
            Jp = Jp + alpha * outer
    return np.array(energies), len(set(states[-20:]))


def row_natural_induction():
    res = {}
    lines = []
    for rule in ("none", "ema", "sum"):
        out = [natural_induction(rule, seed=s) for s in range(10)]
        E = np.stack([e for e, _ in out]); distinct = float(np.mean([d for _, d in out]))
        early = float(E[:, :20].mean()); late = float(E[:, -20:].mean())
        res[rule] = (early, late)
        lines.append(f"{rule}: J0-energy of the reached minimum, mean of epochs 1-20 {early:.4f}, epochs 61-80 {late:.4f}; distinct minima among epochs 61-80 {distinct:.1f} (10 seeds, N = 40)")
    crr = res["ema"][1]; null = res["sum"][1]; dom = res["ema"][1]
    improves = res["ema"][1] < res["ema"][0]
    out = outcome(crr=crr, null=null, domain=dom, check=improves)
    return make_row(CLS, "natural induction: a frustrated spin system with viscoelastic (Hebbian-with-relaxation) couplings",
        source="According to PubMed: Buckley, Lewens, Levin, Millidge, Tschantz and Watson, 'Natural Induction: Spontaneous Adaptive Organisation without Natural Selection', Entropy 2024, doi 10.3390/e26090765 (abstract only); Watson and Szathmary 2015, doi 10.1016/j.tree.2015.11.009 (context, not fetched)",
        Q="the plastic coupling of natural induction is A6/P3 (a Fréchet mean of settled configurations under geometric age weights, i.e. an exponential moving average of s s^T), and the minima reached improve over epochs",
        ingredient="A6 regeneration with P3 age weights (bounded strength, no accumulated count)", null="an accumulated count Jp = alpha x sum of s s^T (what A6 forbids)",
        domain="the paper's own rule: connections relax toward the current state, which is the same exponential moving average",
        numbers=" | ".join(lines) + f" | decisive: late energy under ema {crr:.4f}, under sum {null:.4f}, under the paper's rule {dom:.4f} (same computation); improves early->late under ema: {improves}",
        tg=f"ema {crr:.4f} vs sum {null:.4f}", tn="the paper's relaxation rule is the ema, so the domain value is the CRR value by construction", tc=f"minima improve under ema: {improves}",
        out=out, reading="A6 read as an exponential moving average is the viscoelastic relaxation of natural induction, and the effect (lower J0-energy than without plasticity) is the paper's; the re-weighting A6 insists on and the accumulation it forbids reach the same energy here because both canalise the system onto one minimum (distinct late minima printed), so the ingredient does no work",
        weakness="one small system, one alpha and beta; whether the accumulated count reaches the same energies is a property of this N and horizon (printed), not a theorem",
        elegance="a spring that slowly takes the shape it is held in is a memory that never adds up, only blends", child="A pillow remembers your head by slowly taking its shape, not by counting how many nights you slept on it. Watson's idea and CRR's idea are the same pillow.")


# ---------------------------------------------------------------- AI safety: one poisoned occasion
def row_poisoned_occasion():
    rng = np.random.default_rng(7)
    n = 99
    settled = rng.standard_normal(n)
    lam = 0.9
    lines = []
    infl = {}
    for M in (10.0, 1e3, 1e6):
        occ = np.append(settled, M)
        ages = np.arange(n, -1, -1)                       # newest has age 0
        w = lam ** ages; w = w / w.sum()
        seed_crr = float(w @ occ)                        # A6 with P3: Fréchet mean in the Fisher metric of fixed-variance Gaussians is the weighted mean
        w0 = lam ** np.arange(n - 1, -1, -1); w0 = w0 / w0.sum()
        base_crr = float(w0 @ settled)
        seed_acc = float(occ.mean()); base_acc = float(settled.mean())
        seed_med = float(np.median(occ)); base_med = float(np.median(settled))
        infl[M] = (seed_crr - base_crr, seed_acc - base_acc, seed_med - base_med)
        lines.append(f"M={M:g}: shift of the seed under A6/P3 (lambda {lam}) {infl[M][0]:.4f} (= (1-lambda) M = {(1 - lam) * M:.4f}), under the accumulated mean {infl[M][1]:.4f} (= M/n), under the median {infl[M][2]:.4f}")
    crr = infl[1e6][0]; null = infl[1e6][1]; dom = infl[1e6][2]
    ratio = infl[1e6][0] / infl[1e3][0]
    bounded = ratio < 10.0
    out = outcome(crr=crr, null=null, domain=dom, check=bounded)
    return make_row(CLS, "one poisoned occasion among 99 settled ones (a consolidation step of a continually trained model)",
        source="Huber 1964 and Hampel 1974 (the influence function, gross-error sensitivity) (context, not fetched); 2026 arXiv work on continual safety alignment (2512.10150, 2604.17215, 2604.17691, 2602.07892) seen as abstracts only",
        Q="A6's 'bounded strength' bounds the influence of any one occasion on the regenerated seed: the shift stays bounded as the occasion's magnitude M grows",
        ingredient="A6 regeneration as a Fréchet mean with P3 age weights, bounded strength", null="the accumulated mean (uniform weights, what A6 forbids)",
        domain="the median's influence function is bounded (gross-error sensitivity finite)",
        numbers=" | ".join(lines) + f" | decisive at M = 1e6: shift under A6/P3 {crr:.4f}, under the mean {null:.4f}, under the median {dom:.4f}; shift(1e6)/shift(1e3) = {ratio:.4f}; bounded: {bounded}",
        tg=f"A6/P3 shift {crr:.4f} vs accumulated mean {null:.4f}: the weights do work (and make it worse: the newest occasion carries weight 1 - lambda, not 1/n)",
        tn=f"the median moves {dom:.4f}: the domain's bounded-influence estimator is not the CRR value", tc=f"A6's influence bounded in M: {bounded}",
        out=out, reading="A6 bounds the weight of an occasion, not its influence; under a Fisher Fréchet mean one poisoned step moves the seed by (1 - lambda) M without limit, ten times more than a plain average here; a safety consolidation needs a bounded influence function, which is robust statistics' object and not CRR's",
        weakness="the Gaussian family with fixed variance makes the Fréchet mean linear; a family with heavy tails would bound the influence by the family, not by A6",
        elegance="a memory that weights the newest thing most is the memory easiest to poison with one new thing", child="If your opinion of a restaurant is mostly the last visit, one terrible visit ruins it completely. CRR's memory rule is that kind of memory, and safety needs the other kind, where one bad day cannot outvote the rest.")


# ---------------------------------------------------------------- AI safety: a linear safety head under fine-tuning
def row_safety_head():
    lines = []
    r2 = {}
    for fn, tag in ((S_H_convex_learner, "S-H (a convex head)"), (S_H2_wear_learner, "S-H2 (a head with wear, positive control)")):
        runs, _, meta = fn()
        F = np.array([r["F"] for r in runs])
        q = {k: [] for k in ("C_new", "C_old", "E_new", "E_old")}
        for r in runs:
            pn = path_length(r["pred_new"], kl=kl_gauss); po = path_length(r["pred_old"], kl=kl_gauss)
            q["C_new"].append(pn["C"]); q["E_new"].append(pn["E"]); q["C_old"].append(po["C"]); q["E_old"].append(po["E"])
        fit = np.array([r["seed"] % 2 == 0 for r in runs])
        r2[tag] = {k: _heldout_r2(np.asarray(v), F, fit) for k, v in q.items()}
        lines.append(f"{tag}, n = {len(runs)}, held-out R^2 of forgetting: " + " ".join(f"{k} {v:.4f}" for k, v in r2[tag].items()))
    conv = r2["S-H (a convex head)"]
    crr = conv["E_old"]; null = conv["E_new"]; dom = 1.0
    path_best = max(conv["C_new"], conv["C_old"])
    out = outcome(crr=crr, null=null, domain=dom, check=crr > path_best)
    return make_row(CLS, "a linear safety head fine-tuned away from its task (the convex learner S-H; the wear learner S-H2 as control)",
        source="theory/SCOPE.md section 4.1 (the endpoint lemma); the surrogate battery; 2026 arXiv work on safety anchors and orthogonal gradient projection (abstracts only)",
        Q="a monitor for the erosion of a linear safety head should watch the Fisher endpoint displacement on the OLD (safety) probe set, E_old, rather than on the new task's probe set or the path length",
        ingredient="D6/H-T1 vocabulary (path C, endpoint E) on the old probe set (A1: Fisher distance between predictives)", null="the endpoint on the new task's probe set (E_new)",
        domain="the endpoint lemma: on a convex head forgetting is a function of the endpoint alone, so the sufficient statistic has R^2 -> 1",
        numbers=" | ".join(lines) + f" | decisive (S-H): R^2(E_old) {crr:.4f}, R^2(E_new) {null:.4f}, lemma {dom:.4f}; best path R^2 {path_best:.4f}",
        tg=f"E_old {crr:.4f} vs E_new {null:.4f}: which probe set matters", tn=f"lemma value {dom:.4f}: the endpoint on the old probe is the sufficient statistic", tc=f"E_old beats the best path predictor on the convex head: {crr > path_best}",
        out=out, reading="for a convex safety head the safety community's anchor and projection constraints (endpoint constraints) are the right object and H-T1's path adds nothing (R^2 below 0.1); the path would matter only on a head with wear, which S-H2 shows by construction (R^2 printed) and no real head has been shown to have",
        weakness="linear head, squared loss; a nonconvex head is exactly where the lemma does not apply, and the ledger's ARC-T1b found the old-probe endpoint winning there too",
        elegance="to know how much safety a model has lost, measure how far it has moved on the safety questions, not how far it has travelled", child="If you want to know whether a student forgot last year's lesson, ask them last year's questions; do not add up how much they wandered while learning this year's.")


# ---------------------------------------------------------------- platonic ingression vs regeneration (Hopfield mixtures)
def row_ingression():
    rng = np.random.default_rng(11)
    N, P = 100, 3
    xi = rng.choice([-1.0, 1.0], (P, N))
    J = (xi.T @ xi) / N; np.fill_diagonal(J, 0.0)
    mix = np.sign(xi.sum(axis=0))                        # the symmetric 3-mixture (Amit, Gutfreund and Sompolinsky 1985)
    frechet = np.sign(xi.sum(axis=0))                    # A6: Fréchet mean in the Hamming metric = coordinate-wise majority (exact for odd P)
    lam = 0.5
    w = lam ** np.arange(P - 1, -1, -1)                  # P3 age weights, newest last
    frechet_p3 = np.sign(w @ xi)
    def stable(s):
        return bool(np.all(np.sign(J @ s) == s))
    def relax(s):
        for _ in range(100):
            changed = False
            for i in rng.permutation(N):
                h = J[i] @ s
                new = 1.0 if h > 0 else (-1.0 if h < 0 else s[i])
                if new != s[i]:
                    s[i] = new; changed = True
            if not changed:
                break
        return s
    counts = Counter()
    for _ in range(400):
        s = relax(rng.choice([-1.0, 1.0], N))
        ov = xi @ s / N; om = float(mix @ s / N)
        if np.max(np.abs(ov)) == 1.0:
            counts["stored pattern or its negative"] += 1
        elif abs(om) == 1.0:
            counts["the 3-mixture or its negative"] += 1
        else:
            counts["other"] += 1
    ov_frechet = float(frechet @ mix / N); ov_p3 = float(frechet_p3 @ mix / N)
    check = stable(mix.copy())
    out = outcome(crr=ov_frechet, null=ov_p3, domain=1.0, check=check)
    return make_row(CLS, "Hopfield network with 3 stored patterns: the spurious mixture state as an 'ingressed' form",
        source="Amit, Gutfreund and Sompolinsky 1985 (mixture states sign(sum xi)); Hopfield 1982; Levin 2025 'Ingressing Minds' (preprint, abstract only) (context, not fetched)",
        Q="a form that was never stored and that the dynamics nevertheless settles into (the mixture) is the A6 regeneration of the stored forms: the Fréchet mean of the settled patterns in the network's own (Hamming) metric",
        ingredient="A6 regeneration as a Fréchet mean of settled occasions (P2 equal weights)", null="the same Fréchet mean under P3 age weights (lambda 0.5: the newest pattern outweighs the rest)",
        domain="AGS 1985: the symmetric mixture is sign(xi_1 + xi_2 + xi_3), a fixed point of the dynamics",
        numbers=f"N = {N}, P = {P}; 400 random starts settle: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) + f" | overlap of the A6 (P2) Fréchet mean with the AGS mixture {ov_frechet:.4f}; under P3 age weights {ov_p3:.4f}; the mixture is a fixed point: {check}",
        tg=f"P2 mean overlap {ov_frechet:.4f} vs P3 mean overlap {ov_p3:.4f}: which weights matters", tn=f"AGS mixture overlap {1.0:.4f}: the domain has the form", tc=f"fixed point of the dynamics: {check}",
        out=out, reading="the 'ingressed' form is the majority of the stored forms, which the domain wrote down in 1985; A6 gives it a process reading (regenerated from the settled) against the platonic one (pre-existing in the landscape), and the two readings share every number; under age weights A6 returns the newest pattern, not the mixture",
        weakness="three patterns and one lambda; with more patterns the P2 and P3 means diverge further, and CRR does not say which weights a network's past has",
        elegance="a shape nobody stored, that the network still finds, is the vote of the shapes it did store", child="If three friends each drew a face, and you drew the face most of them agreed on at each spot, you would draw a fourth face nobody drew. The network 'finds' that face. CRR says it is made from the three; Plato says it was waiting there. The numbers cannot tell them apart.")


# ---------------------------------------------------------------- finitude
def row_finitude():
    rng = np.random.default_rng(5)
    n = 1600
    t = np.arange(n)
    base = np.sin(2 * math.pi * t / 40.0)                          # 40 cycles
    lines = []
    units = {}
    for sd in (0.0, 1e-3, 1e-1, 1.0):
        x = base + sd * rng.standard_normal(n)
        stat = x[::40]                                             # one statistic per occasion: the value at the occasion's start
        try:
            sig = unit_sigma(stat)
            r = rho(float(np.ptp(x)), sig)
            units[sd] = (sig, r)
            u = f"unit {sig:.4e}, rho {r:.4e}"
        except ValueError as e:
            u = f"no unit ({e})"
        cuts = antipodal_cuts(intrinsic_phase(x))
        lines.append(f"noise sd {sd:g}: {u}; half-turn cuts found {len(cuts)} (40 cycles)")
    noise_only = rng.standard_normal(n)
    cuts_noise = antipodal_cuts(intrinsic_phase(noise_only))
    lines.append(f"white noise alone: half-turn cuts found {len(cuts_noise)} (no cycle in the record)")
    out = outcome(unstated=True)
    return make_row(CLS, "the owner's finitude thesis: 'to be finite is to be able to have an experience at all'",
        source="the owner (prompt-log entry 66); Clarke and Barron 1990 (the information of a record grows as log of its resolution) (context, not fetched)",
        Q="none formed: 'finite' in CRR is a resolvable step (A1') and a resolution rho = extent/unit; 'experience' has no clause",
        ingredient="A1'/D1 the own unit and rho", null="none",
        domain=None,
        numbers=" | ".join(lines),
        tg="not run (no proposition)", tn="not run", tc="not run",
        out=out, reading=f"CRR has a mathematics of finitude and no mathematics of experience: the unit of a noiseless carrier is the machine's round-off ({units[0.0][0]:.2e}, rho {units[0.0][1]:.2e}: finitude supplied by the machine where the signal supplies none, as ontology/06 says of the cut), the unit tracks the noise where there is noise, and a carrier of pure noise has cuts everywhere ({len(cuts_noise)} half-turns in {n} samples with no cycle); the thesis can be made a proposition only by a clause CRR does not have",
        weakness="an UNSTATED row is a silence, not a result",
        elegance="a thing with no smallest step has nothing to count with, and a thing that is all steps has nothing to count", child="If a ruler had no marks you could not measure with it; if it were all marks you could not either. CRR knows what a ruler is. It has no word for the person holding it.")


def main():
    rows = [row_busy_beaver(), row_settled_past_on_a_machine(), row_forms_as_choices(), row_sorting_surplus(),
            row_natural_induction(), row_poisoned_occasion(), row_safety_head(), row_ingression(), row_finitude()]
    return run_batch("ontology battery 2026-09-22: Turing systems, AI safety, platonic ingression (SYNTHESIS class; owner request, prompt-log entry 66)", rows)


if __name__ == "__main__":
    raise SystemExit(main())

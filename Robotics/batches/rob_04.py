"""ROB1 stage 4b batch 04: applications RA7 (actuator wear by arc) and RA8 (swarm consensus with intermittent links) of the
declared battery Robotics/DECLARATION_4B.md (pushed at d44e713 before any model; prompt-log entry 257; AGENT_LOG 223).
Each row fixes, as declared, the model, Q, the CRR-proper ingredient, the null (T-G), the domain's own theorem (T-N), the
check (T-C) and the investigator's forecast; the harness labels are computed from the numbers by outcome() (R15).

RA7. A robot joint's gearbox under a variable duty cycle. The duty is a sequence of segments (exponential durations, mean
     8 h), each with a load level S uniform on [0.5, 1.5] x the rated load and a utilisation u uniform on [0.1, 1.0]; a
     segment of length tau carries round(360 u tau) load cycles, evenly spaced in it. Each load cycle is pulsating,
     0 -> S -> 0 (a gear tooth's root load); the load trace is sampled at its turning points (0, S1, 0, S2, 0, ...). S-N
     curve (Basquin): N(S) = 1e5 S^-m cycles, m = 3 scored; damage per cycle 1/N(S); failure at the first cycle at which the
     Miner damage reaches 1; the gearbox is replaced at once (the cut has no duration) and the new one starts at the next
     cycle of the same duty. 200 gearbox lives (occasions between consecutive failures). H-L5: per life, C = arc_length of
     the load trace (identity metric, sigma = 1) against the clock (hours). Null: clock time. Domain: Palmgren-Miner, the
     damage sum_i n_i / N_i accumulated per life. T-C: CV per arc < CV per clock (paired-bootstrap 95 % CI of the
     difference below 0, as H-L5 is scored) AND Miner's renewal-reward prediction of the two CVs orders them the same way.
     Printed, not scored: the S-N exponent swept over {1, 2, 3, 6, 10}, a constant-load control, H-L5's amplitude control
     (i), and the maintenance reading (the spread of the life in each index).
RA8. N = 20 agents on a ring; at every wall tick each of the 20 links is down independently with probability q (a seeded
     pattern); the agents update by Jadbabaie et al.'s nearest-neighbour rule, x_i <- (x_i + sum over up neighbours x_j) /
     (1 + number of up neighbours), from one fixed seeded start. 45 dropout patterns: q in {0.1, ..., 0.9} x 5 link seeds.
     Rounds-to-epsilon: the first tick at which the spread max x - min x is at most 1e-3 of the initial spread, counted in
     (a) own exchange events (one up link at one tick = one pairwise exchange; A3/D5 read on a point process: the cut is
     the event itself, natural time = the event count), (b) wall ticks (the null), (c) jointly connected intervals (the
     domain: greedy consecutive intervals, each closed at the first tick at which the union of its graphs is connected;
     the count is the index of the interval holding the epsilon tick). T-C: CV across patterns per event < per wall tick,
     with the paired-bootstrap 95 % CI of the difference below 0. Printed, not scored: the non-empty-tick reading of an
     exchange event, the average-consensus (Laplacian step 1/3) rule, and the rounds to consensus per q.

CHOICES (every underspecified point, the most literal and simplest reading): CHOICES_RA7 and CHOICES_RA8 below, printed on
CHOICES lines and repeated in each row's weakness field. Nothing was tuned after a run; the scored parameters were fixed
in this file before its first run.

Literature named by name only, as the declaration names it (no citation claim beyond the names; R10: nothing fetched
here): Palmgren and Miner (the linear damage rule); Basquin (the power-law S-N curve); Jadbabaie, Lin and Morse 2003
(coordination under switching nearest-neighbour rules). Deterministic (numpy default_rng, fixed seeds), no data files, no
network; CPU, well under a minute. Rung R4 at most (a declared check on a synthetic model); a note, not evidence (R8).

    cd /home/user/ashes_crr && uv run python Robotics/batches/rob_04.py > Robotics/batches/rob_04.txt
"""
from __future__ import annotations

import math
import sys

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

from crr.instrument.core import arc_length, cv
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

DECL = "Robotics/DECLARATION_4B.md at d44e713"
N_BOOT, SEED_BOOT = 2000, 0


def _w(cond, yes, no):
    return yes if cond else no


def _qv(check):
    return "-> not computable" if check is None else ("-> Q holds" if check else "-> Q fails")


def _boot_ci(a, b, seed=SEED_BOOT, n_boot=N_BOOT):
    """Paired bootstrap 95 % CI of cv(a) - cv(b) over units (the resampling regularity() uses)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    rng = np.random.default_rng(seed)
    d = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, len(a), len(a))
        d[i] = cv(a[idx]) - cv(b[idx])
    lo, hi = np.percentile(d, [2.5, 97.5])
    return float(lo), float(hi)


# ====================================================================================== RA7 actuator wear by arc
M_SN = 3.0                    # Basquin S-N exponent (scored)
M_SWEEP = (1.0, 2.0, 3.0, 6.0, 10.0)
N_REF = 1.0e5                 # cycles to failure at the rated load S = 1
S_LO, S_HI = 0.5, 1.5         # load level per duty segment, x rated
U_LO, U_HI = 0.1, 1.0         # utilisation per duty segment (share of the segment the joint is cycling)
F_MAX = 360.0                 # load cycles per hour at full utilisation
SEG_MEAN = 8.0                # h, mean duty-segment length (exponential)
N_LIFE = 200                  # gearbox lives (occasions)
N_SEG = 50000                 # duty segments drawn (the runs below use fewer; asserted)
SEED_DUTY = 0
CHOICES_RA7 = (
    "(1) the S-N curve read as Basquin's power law N(S) = N_ref S^-m with S in rated-load units, N_ref = 1e5 cycles and m = 3 "
    "scored (round values, ASSUMED, no source; the declaration names an S-N curve and no exponent); m swept over "
    "{1, 2, 3, 6, 10} and printed, not scored; (2) 'variable duty cycle' read as duty segments of exponential length (mean 8 h) "
    "each with its own load level S ~ U[0.5, 1.5] and utilisation u ~ U[0.1, 1.0], round(360 u tau) load cycles evenly spaced "
    "in a segment of tau hours (seed 0); (3) a load cycle is pulsating, 0 -> S -> 0 (the gear tooth's root load), and the load "
    "trace is sampled at its turning points, so arc_length (identity metric, sigma = 1) is the trace's total variation, 2 S per "
    "cycle, exactly; there is no Fisher metric on a deterministic load trace and a CV is scale-free, so sigma and H-L5's "
    "control (ii) (identity metric) drop out; (4) failure at the first cycle at which the Miner sum reaches 1, the gearbox "
    "replaced at once and the new one starting on the next cycle of the same duty (renewal; own boundary events = failures, "
    "occasion = one life); (5) 200 lives; (6) T-N: Palmgren-Miner read as the damage sum_i n_i / N_i accumulated per life, "
    "scored by its CV across lives (the domain's index in the place of the arc); (7) T-C: 'CV per arc < CV per clock, as "
    "Miner predicts' read as the measured inequality with the paired-bootstrap 95 % CI of CV(arc) - CV(clock) below 0 (2000 "
    "resamples of the lives, seed 0; H-L5's scoring) AND Miner's renewal-reward prediction ordering the two CVs the same way: "
    "with damage as the renewal index, CV_X^2 = Var(x - r d) E[d] / E[x]^2 per duty segment, r = E[x] / E[d] (x the arc or "
    "the clock of a segment, d its damage; moments over the segments the lives used); (8) printed, not scored: the m sweep "
    "with each m's label, a constant-load control (S = 1 throughout, only the utilisation varies), H-L5's control (i) (the "
    "peak-to-peak load of each life) and the maintenance reading; H-L5's control (iii) (peak-detected boundaries) has no "
    "reading here, the boundaries being failures, not extrema")


def _duty():
    rng = np.random.default_rng(SEED_DUTY)
    tau = rng.exponential(SEG_MEAN, N_SEG)
    S = rng.uniform(S_LO, S_HI, N_SEG)
    u = rng.uniform(U_LO, U_HI, N_SEG)
    n = np.rint(F_MAX * u * tau).astype(np.int64)
    t0 = np.concatenate([[0.0], np.cumsum(tau)[:-1]])
    return tau, S, u, n, t0


def _ra7_run(m, S, tau, n, t0):
    """Run the duty until N_LIFE gearboxes have failed. Returns per-life arrays and the segments used."""
    delta = S ** m / N_REF                                       # Miner damage per cycle, 1/N(S)
    clock, arc, miner, amp, cycles = [], [], [], [], []
    D, blocks, t_prev = 0.0, [], 0.0
    j, used = 0, 0
    while len(clock) < N_LIFE:
        if j >= len(n):
            raise RuntimeError("RA7: duty exhausted; raise N_SEG")
        rem = int(n[j]) - used
        if rem <= 0:
            j, used = j + 1, 0
            continue
        dj = float(delta[j])
        k = max(1, int(math.ceil((1.0 - D) / dj)))
        while k > 1 and D + (k - 1) * dj >= 1.0:
            k -= 1
        while D + k * dj < 1.0:
            k += 1
        if k <= rem:                                             # failure inside this segment, at its (used + k)-th cycle
            blocks.append((float(S[j]), k))
            used += k
            t_fail = float(t0[j] + used * tau[j] / n[j])
            ss = np.array([b[0] for b in blocks]); cc = np.array([b[1] for b in blocks], dtype=np.int64)
            trace = np.zeros(2 * int(cc.sum()) + 1)
            trace[1::2] = np.repeat(ss, cc)
            clock.append(t_fail - t_prev); arc.append(arc_length(trace)); miner.append(D + k * dj)
            amp.append(float(np.ptp(trace))); cycles.append(int(cc.sum()))
            D, blocks, t_prev = 0.0, [], t_fail
            if used == n[j]:
                j, used = j + 1, 0
        else:
            blocks.append((float(S[j]), rem))
            D += rem * dj
            j, used = j + 1, 0
    return dict(clock=np.array(clock), arc=np.array(arc), miner=np.array(miner), amp=np.array(amp),
                cycles=np.array(cycles), n_seg=j + 1)


def _rr_cv(x, d):
    """Miner's renewal-reward prediction of the CV of X accumulated until the damage reaches 1 (per-segment moments)."""
    r = x.mean() / d.mean()
    return math.sqrt(np.var(x - r * d, ddof=1) * d.mean()) / x.mean()


def _ra7_score(m, S, tau, n, t0):
    res = _ra7_run(m, S, tau, n, t0)
    crr, null, dom = cv(res["arc"]), cv(res["clock"]), cv(res["miner"])
    lo, hi = _boot_ci(res["arc"], res["clock"])
    k = res["n_seg"]
    x_arc, x_clk, d = 2.0 * n[:k] * S[:k], tau[:k], n[:k] * S[:k] ** m / N_REF
    p_arc, p_clk = _rr_cv(x_arc, d), _rr_cv(x_clk, d)
    check = bool(crr < null and hi < 0.0 and p_arc < p_clk)
    res.update(crr=crr, null=null, dom=dom, lo=lo, hi=hi, p_arc=p_arc, p_clk=p_clk, check=check,
               out=outcome(crr=crr, null=null, domain=dom, check=check))
    return res


def ra7():
    tau, S, u, n, t0 = _duty()
    print("CHOICES RA7: " + CHOICES_RA7)
    print()
    sweep = {m: _ra7_score(m, S, tau, n, t0) for m in M_SWEEP}
    const = _ra7_score(M_SN, np.ones_like(S), tau, n, t0)
    r = sweep[M_SN]
    print(f"RA7 duty (seed {SEED_DUTY}): segments mean {SEG_MEAN:g} h, load U[{S_LO:g}, {S_HI:g}], utilisation U[{U_LO:g}, {U_HI:g}], "
          f"up to {F_MAX:g} cycles/h; N(S) = {N_REF:g} S^-m; {N_LIFE} lives per run")
    print("RA7 S-N exponent sweep (m = 3 scored; the others printed, not scored): m, segments used, mean life h, mean cycles per "
          "life, CV per arc, CV per clock, CV of the Miner damage, bootstrap CI of CV(arc) - CV(clock), Miner's renewal-reward "
          "prediction (arc, clock), check, label")
    for m, s in sweep.items():
        print(f"  m = {m:>4g}: {s['n_seg']:>6d} segments, life {s['clock'].mean():10.3f} h, {s['cycles'].mean():11.1f} cycles; "
              f"CV arc {s['crr']:.6e}, CV clock {s['null']:.6e}, CV Miner {s['dom']:.6e}; CI [{s['lo']:+.6f}, {s['hi']:+.6f}]; "
              f"predicted arc {s['p_arc']:.6f}, clock {s['p_clk']:.6f}; check {_w(s['check'], 'holds', 'fails')}; {s['out']}")
    print(f"  constant load (S = 1, m = {M_SN:g}, only the utilisation varies): life {const['clock'].mean():.3f} h, CV arc "
          f"{const['crr']:.6e}, CV clock {const['null']:.6e}, CV Miner {const['dom']:.6e}; {const['out']}")
    print()

    crr, null, dom, check, out = r["crr"], r["null"], r["dom"], r["check"], r["out"]
    cv_amp = cv(r["amp"])
    lo_a, hi_a = _boot_ci(r["arc"], r["amp"])
    labels = "; ".join(f"m = {m:g}: {s['out']}" for m, s in sweep.items())
    share = {name: float(np.mean(v.min() / v)) for name, v in (("clock", r["clock"]), ("arc", r["arc"]), ("Miner", r["miner"]))}
    life = r["clock"]
    return make_row(
        "robotics", f"RA7 actuator wear by arc: a robot joint's gearbox under a variable duty cycle (segments of mean {SEG_MEAN:g} h, "
                    f"load U[{S_LO:g}, {S_HI:g}] x rated, utilisation U[{U_LO:g}, {U_HI:g}] at up to {F_MAX:g} load cycles/h), "
                    f"pulsating load cycles, S-N curve N(S) = {N_REF:g} S^-{M_SN:g}, failure at Miner damage 1 and instant "
                    f"replacement, {N_LIFE} gearbox lives",
        source=f"ROB1 RA7 (declared in {DECL}; forecast REDUNDANT-DOMAIN)",
        Q="time to failure is more regular in accumulated load arc than in clock time (computed as: across gearbox lives, the CV "
          "of the load trace's arc_length from installation to failure against the CV of the life in hours)",
        ingredient="H-L5 (own boundary events = failures; occasion = one gearbox life; C = the arc of the load trace in the occasion)",
        null="clock time (the life in hours)",
        domain="Palmgren-Miner (damage = sum_i n_i / N_i from the S-N curve): the CV of the damage accumulated per life",
        numbers=(f"{r['n_seg']} duty segments used; life mean {life.mean():.3f} h (min {life.min():.3f}, max {life.max():.3f}), "
                 f"{r['cycles'].mean():.1f} cycles; CV per arc {crr:.6f}, CV per clock {null:.6f}, CV of the Miner damage per life "
                 f"{dom:.6e} (damage at failure {r['miner'].min():.9f} to {r['miner'].max():.9f}); paired-bootstrap 95 % CI of "
                 f"CV(arc) - CV(clock) [{r['lo']:+.6f}, {r['hi']:+.6f}]; Miner's renewal-reward prediction: CV arc {r['p_arc']:.6f}, "
                 f"CV clock {r['p_clk']:.6f}; H-L5 control (i), the peak-to-peak load of each life (not scored): CV {cv_amp:.6f}, CI "
                 f"of CV(arc) - CV(amplitude) [{lo_a:+.6f}, {hi_a:+.6f}]; S-N exponent sweep (not scored): {labels}; constant-load "
                 f"control (not scored): CV arc {const['crr']:.3e}, CV clock {const['null']:.6f}, CV Miner {const['dom']:.3e}, "
                 f"{const['out']}; maintenance reading (preventive replacement at the shortest of the {N_LIFE} lives in each index, "
                 f"no failure among them): mean share of a life used, clock {share['clock']:.4f}, arc {share['arc']:.4f}, Miner "
                 f"{share['Miner']:.6f}"),
        tg=f"CV per arc {crr:.6f} vs null CV per clock {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"Miner's damage per life, CV {dom:.6e}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')} "
           f"(relative difference {rel(crr, dom):.6f})",
        tc=f"CV per arc {crr:.6f} < CV per clock {null:.6f} with the CI below 0 (upper {r['hi']:+.6f}): "
           f"{_w(crr < null and r['hi'] < 0.0, 'holds', 'fails')}; Miner's prediction orders them the same way (arc "
           f"{r['p_arc']:.6f} < clock {r['p_clk']:.6f}): {_w(r['p_arc'] < r['p_clk'], 'holds', 'fails')} {_qv(check)}",
        out=out,
        reading=(f"the arc of a pulsating load trace is 2 S per cycle and Miner's damage is S^{M_SN:g} / N_ref per cycle: both count "
                 f"load cycles and neither counts the hours the joint stands idle, so both drop the utilisation's spread, which is "
                 f"what the clock carries (CV per clock {null:.6f}); the arc weights each cycle by S where Miner weights it by "
                 f"S^{M_SN:g}, so the arc keeps the load mix's spread (CV {crr:.6f}) and Miner's damage, 1 at every failure by "
                 f"construction, keeps only the last cycle's overshoot (CV {dom:.2e}): "
                 + _w(dom < crr, "the domain's index is the more regular one", "the arc is at least as regular as the domain's index")
                 + f", and the arc is Miner's damage up to a constant only at m = 1 ({sweep[1.0]['out']} there; the label over the "
                 f"sweep is {labels}); "
                 f"the row reads {out}"
                 + _w(out == "ADDS" and dom < crr, " (a candidate only in the harness sense: the arc beats the clock and the domain's "
                      "index is not the arc; Miner's damage is more regular than the arc, so the arc offers a gearbox engineer, who "
                      "already counts damage rather than hours, nothing Miner lacks)", "")
                 + "; the maintenance reading "
                 + _w(share["clock"] < share["arc"] < share["Miner"], "orders the three indices the same way",
                      "does not order the three indices the same way")
                 + f": replacing at the shortest life seen uses {share['clock']:.2%} of a mean "
                 f"life on the clock, {share['arc']:.2%} on the arc and {share['Miner']:.4%} on Miner's damage; H-L5's own "
                 f"control (i), the life's peak load, is {_w(cv_amp < crr, 'more regular than the arc', 'less regular than the arc')} "
                 f"(CV {cv_amp:.6f}; CI of CV(arc) - CV(amplitude) [{lo_a:+.6f}, {hi_a:+.6f}]), so the class claim "
                 f"{_w(lo_a > 0.0, 'fails its amplitude control', _w(hi_a < 0.0, 'passes its amplitude control', 'ties its amplitude control'))} "
                 f"(not scored by the declaration)"),
        weakness=("CHOICE: " + CHOICES_RA7 + "; the model puts Miner's rule in (failure is defined as damage 1), so T-N's index is "
                  "regular by construction and the row can show only where the arc departs from it: the gap is the S-N curve's "
                  "curvature, m - 1; real gearboxes add scatter in the S-N curve itself (lives at one load vary several-fold), "
                  "load sequence effects that the linear rule ignores, and wear modes (pitting, lubricant) that are not "
                  "cycle-counted"),
        elegance="", child="")


# ====================================================================================== RA8 swarm consensus
N_AG = 20
EDGES = np.array([(i, (i + 1) % N_AG) for i in range(N_AG)])
Q_GRID = tuple(round(0.1 * k, 1) for k in range(1, 10))
N_LSEED = 5
EPS = 1e-3                    # rounds-to-epsilon: spread at most 1e-3 of the initial spread
SEED_X0, SEED_LINK = 0, 8
MAX_TICKS = 10 ** 6
CHOICES_RA8 = (
    "(1) the graph read as a ring of N = 20 agents (the simplest connected graph in which every agent has neighbours; ASSUMED, "
    "no source), initial values U[0, 1] from one seed (0) shared by every pattern, so only the dropout pattern varies; (2) "
    "'links drop with a seeded pattern' read as i.i.d. Bernoulli drops: each link down at each wall tick with probability q, "
    "one pattern = one (q, seed) pair, q in {0.1, ..., 0.9} x link seeds 0-4 (45 patterns; generator seeded with (8, 10 q, "
    "seed)); (3) 'averaging' read as Jadbabaie et al.'s nearest-neighbour rule, the domain theorem's own model: x_i <- (x_i + "
    "sum of up neighbours' x_j) / (1 + number of up neighbours), synchronous; its consensus value need not be the mean, so "
    "convergence is read on the spread max x - min x; (4) rounds-to-epsilon = the first tick at which the spread is at most "
    "1e-3 of the initial spread; (5) an own exchange event = one up link at one tick (one pairwise exchange, counted once), "
    "events-to-epsilon = the up links summed through that tick; A3 is read as D5's point-process reading, the cut is the event "
    "itself (the swarm has no rotor, O3), so no phase and no antipodal_cuts are computed; (6) the domain's jointly connected "
    "intervals read greedily: consecutive intervals, each closed at the first tick at which the union of its graphs is "
    "connected; intervals-to-epsilon = the index of the interval holding the epsilon tick; (7) 'regular across dropout "
    "patterns' = the CV over the 45 patterns; T-C = CV per event < CV per wall tick with the paired-bootstrap 95 % CI of the "
    "difference (2000 resamples of the patterns, seed 0) below 0; (8) printed, not scored: the non-empty-tick reading of an "
    "exchange event (a tick in which at least one link is up), the average-consensus rule x <- x - (1/3) L(t) x, and the rounds "
    "to consensus per q")


def _connected(mask):
    if mask.sum() < N_AG - 1:
        return False
    e = EDGES[mask]
    g = csr_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(N_AG, N_AG))
    return connected_components(g, directed=False)[0] == 1


def _consensus(x0, iq, q, s, rule):
    rng = np.random.default_rng([SEED_LINK, iq, s])
    x = x0.copy()
    s0 = float(np.ptp(x))
    ea, eb = EDGES[:, 0], EDGES[:, 1]
    union = np.zeros(len(EDGES), bool)
    ticks = events = nonempty = 0
    interval = 1
    while ticks < MAX_TICKS:
        up = rng.random(len(EDGES)) >= q
        ticks += 1
        k = int(up.sum()); events += k; nonempty += int(k > 0)
        a, b = ea[up], eb[up]
        if rule == "jadbabaie":
            num, deg = x.copy(), np.ones(N_AG)
            np.add.at(num, a, x[b]); np.add.at(num, b, x[a])
            np.add.at(deg, a, 1.0); np.add.at(deg, b, 1.0)
            x = num / deg
        else:                                                    # average consensus, x <- x - (1/3) L(t) x
            dx = np.zeros(N_AG)
            np.add.at(dx, a, x[b] - x[a]); np.add.at(dx, b, x[a] - x[b])
            x = x + dx / 3.0
        union |= up
        if np.ptp(x) <= EPS * s0:
            return dict(ticks=ticks, events=events, nonempty=nonempty, intervals=interval)
        if _connected(union):
            interval += 1
            union[:] = False
    raise RuntimeError("RA8: no consensus within MAX_TICKS")


def _ra8_rule(x0, rule):
    runs = [(q, s, _consensus(x0, iq, q, s, rule)) for iq, q in enumerate(Q_GRID, 1) for s in range(N_LSEED)]
    arr = {f: np.array([r[2][f] for r in runs], float) for f in ("ticks", "events", "nonempty", "intervals")}
    return runs, arr


def _ra8_label(arr, ev="events"):
    crr, null, dom = cv(arr[ev]), cv(arr["ticks"]), cv(arr["intervals"])
    lo, hi = _boot_ci(arr[ev], arr["ticks"])
    check = bool(crr < null and hi < 0.0)
    return dict(crr=crr, null=null, dom=dom, lo=lo, hi=hi, check=check, out=outcome(crr=crr, null=null, domain=dom, check=check))


def ra8():
    x0 = np.random.default_rng(SEED_X0).uniform(0.0, 1.0, N_AG)
    print("CHOICES RA8: " + CHOICES_RA8)
    print()
    runs, arr = _ra8_rule(x0, "jadbabaie")
    sc = _ra8_label(arr)
    alt_ne = _ra8_label(arr, "nonempty")
    runs_l, arr_l = _ra8_rule(x0, "laplacian")
    alt_l = _ra8_label(arr_l)
    per_q = {}
    for q in Q_GRID:
        sel = [r[2] for r in runs if r[0] == q]
        per_q[q] = {f: float(np.mean([d[f] for d in sel])) for f in ("ticks", "events", "nonempty", "intervals")}
    print(f"RA8 ring of {N_AG}, x0 seed {SEED_X0} (initial spread {np.ptp(x0):.6f}), epsilon {EPS:g} of the initial spread; "
          f"rounds to consensus per q (Jadbabaie's rule, mean over {N_LSEED} link seeds): ticks, exchange events, non-empty "
          "ticks, jointly connected intervals")
    for q, v in per_q.items():
        print(f"  q = {q:.1f}: {v['ticks']:9.1f} ticks, {v['events']:9.1f} events, {v['nonempty']:9.1f} non-empty ticks, "
              f"{v['intervals']:7.1f} intervals")
    print(f"RA8 second readings (printed, not scored): non-empty ticks as the event: CV {alt_ne['crr']:.6f} vs wall {alt_ne['null']:.6f}, "
          f"CI [{alt_ne['lo']:+.6f}, {alt_ne['hi']:+.6f}], {alt_ne['out']}; average consensus x <- x - (1/3) L(t) x: CV per event "
          f"{alt_l['crr']:.6f}, per wall tick {alt_l['null']:.6f}, per interval {alt_l['dom']:.6f}, CI [{alt_l['lo']:+.6f}, "
          f"{alt_l['hi']:+.6f}], {alt_l['out']}")
    print()

    crr, null, dom, check, out = sc["crr"], sc["null"], sc["dom"], sc["check"], sc["out"]
    ev = arr["events"]; tk = arr["ticks"]; iv = arr["intervals"]
    q_lo, q_hi = Q_GRID[0], Q_GRID[-1]
    return make_row(
        "robotics", f"RA8 swarm consensus with intermittent links: {N_AG} agents on a ring, Jadbabaie et al.'s nearest-neighbour "
                    f"averaging, each link down at each tick with probability q in {{{q_lo:g}, ..., {q_hi:g}}} x {N_LSEED} seeds "
                    f"({len(runs)} dropout patterns), rounds to a spread of {EPS:g} of the initial",
        source=f"ROB1 RA8 (declared in {DECL}; forecast REDUNDANT-DOMAIN)",
        Q="convergence counted per own exchange event is regular across dropout patterns; per wall time it is not (computed as: "
          "the CV over the patterns of the rounds-to-epsilon counted in exchange events, against the same counted in wall ticks)",
        ingredient="A3 read as D5 on a point process (the cut at each own exchange event; natural time = the event count) and "
                   "H-L5 (the event count against the clock)",
        null="wall time (rounds-to-epsilon in ticks)",
        domain="consensus under switching topologies (Jadbabaie et al. 2003): convergence per jointly connected interval, the CV "
               "of the rounds-to-epsilon counted in greedy jointly connected intervals",
        numbers=(f"rounds-to-epsilon over {len(runs)} patterns: events mean {ev.mean():.1f} (min {ev.min():.0f}, max {ev.max():.0f}), "
                 f"CV {crr:.6f}; ticks mean {tk.mean():.1f} (min {tk.min():.0f}, max {tk.max():.0f}), CV {null:.6f}; jointly "
                 f"connected intervals mean {iv.mean():.1f} (min {iv.min():.0f}, max {iv.max():.0f}), CV {dom:.6f}; paired-bootstrap "
                 f"95 % CI of CV(events) - CV(ticks) [{sc['lo']:+.6f}, {sc['hi']:+.6f}]; second readings (not scored): non-empty "
                 f"ticks CV {alt_ne['crr']:.6f} ({alt_ne['out']}), average consensus CV events {alt_l['crr']:.6f}, ticks "
                 f"{alt_l['null']:.6f}, intervals {alt_l['dom']:.6f} ({alt_l['out']}); robotics reading, rounds to consensus at "
                 f"q = {q_lo:g} and q = {q_hi:g}: {per_q[q_lo]['ticks']:.1f} and {per_q[q_hi]['ticks']:.1f} ticks, "
                 f"{per_q[q_lo]['events']:.1f} and {per_q[q_hi]['events']:.1f} messages, {per_q[q_lo]['intervals']:.1f} and "
                 f"{per_q[q_hi]['intervals']:.1f} jointly connected intervals"),
        tg=f"CV per event {crr:.6f} vs null CV per wall tick {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"jointly connected intervals, CV {dom:.6f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')} "
           f"(relative difference {rel(crr, dom):.6f})",
        tc=f"CV per event {crr:.6f} < CV per wall tick {null:.6f} with the CI below 0 (upper {sc['hi']:+.6f}): "
           f"{_w(check, 'holds', 'fails')} {_qv(check)}",
        out=out,
        reading=(f"under i.i.d. link drops a tick carries on average (1 - q) x {N_AG} exchanges, so the wall time to consensus "
                 f"stretches from {per_q[q_lo]['ticks']:.1f} ticks at q = {q_lo:g} to {per_q[q_hi]['ticks']:.1f} at q = {q_hi:g} "
                 f"(CV {null:.6f}) while the exchanges needed move from {per_q[q_lo]['events']:.1f} to {per_q[q_hi]['events']:.1f} "
                 f"(CV {crr:.6f}); the jointly connected intervals move from {per_q[q_lo]['intervals']:.1f} to "
                 f"{per_q[q_hi]['intervals']:.1f} (CV {dom:.6f}); "
                 + _w(dom < crr, "the domain's interval count is the more regular index, ",
                      "the event count is more regular than the domain's interval count, ")
                 + f"and the two differ by {rel(crr, dom):.2%}, so T-N {_w(rel(crr, dom) <= TOL_N, 'agrees', 'differs')} and the "
                 f"row reads {out}; the exchange count is the natural time of the averaging (the rule moves the state only through "
                 f"exchanges), and the domain's interval count is a coarser natural time, one union-connected graph per unit; "
                 f"under the non-empty-tick reading of an event the row would read {alt_ne['out']}, and under the average-consensus "
                 f"rule {alt_l['out']}"),
        weakness=("CHOICE: " + CHOICES_RA8 + "; i.i.d. drops make each tick's exchanges a binomial draw whose mean the clock "
                  "carries and the event count cancels, so the event count's regularity is close to built in; bursty (Markov) "
                  "drops, lossy links and a swarm whose graph moves with its state were not modelled; the Jadbabaie rule's "
                  "weights change with the number of up neighbours, so an exchange is not a fixed contraction"),
        elegance="", child="")


def main():
    r7 = ra7()
    r8 = ra8()
    return run_batch("ROB1 stage 4b batch 04: RA7 actuator wear by arc, RA8 swarm consensus with intermittent links "
                     f"(Robotics/DECLARATION_4B.md; declared at d44e713)", [r7, r8])


if __name__ == "__main__":
    sys.exit(main())

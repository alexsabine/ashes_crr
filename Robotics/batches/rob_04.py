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
     the load trace (identity metric, sigma = 1) against the clock (hours). Null: clock time. Domain (CHANGED AFTER
     REVIEW): Palmgren-Miner applied to the target Q names, Miner's prediction of the CV per arc (the renewal-reward term
     from the per-segment moments, without the lives, plus the damage-at-failure overshoot term). T-C: CV per arc < CV per
     clock (paired-bootstrap 95 % CI of the difference below 0, as H-L5 is scored) AND Miner's prediction of the two CVs
     orders them the same way. Printed, not scored: the first T-N (the CV of Miner's damage per life) and the asymptotic
     term alone, each with its label; the S-N exponent swept over {1, 2, 3, 6, 10}; a constant-load control; 40 other duty
     seeds (seed fragility); H-L5's amplitude control (i); and the maintenance reading (the spread of the life per index).
RA8. N = 20 agents on a ring; at every wall tick each of the 20 links is down independently with probability q (a seeded
     pattern); the agents update by Jadbabaie et al.'s nearest-neighbour rule, x_i <- (x_i + sum over up neighbours x_j) /
     (1 + number of up neighbours), from one fixed seeded start. Scored (CHANGED AFTER REVIEW): one drop rate, q = 0.5, and
     45 dropout patterns that differ only by link seed (0-44). Rounds-to-epsilon: the first tick at which the spread
     max x - min x is at most 1e-3 of the initial spread, counted in (a) own exchange events (one up link at one tick = one
     pairwise exchange; A1' natural time on a point process, D5: the cut is the event itself), (b) wall ticks (the null),
     (c) jointly connected intervals (the domain: greedy consecutive intervals, each closed at the first tick at which the
     union of its graphs is connected; the count is the index of the interval holding the epsilon tick). T-C: CV across
     patterns per event < per wall tick, with the paired-bootstrap 95 % CI of the difference below 0. Printed, not scored:
     every q in {0.1, ..., 0.9} with 45 seeds and its own label (Jadbabaie's rule and the average-consensus rule), the first
     design (the nine rates pooled, 5 seeds each; bootstrap within q strata), the non-empty-tick reading of an exchange
     event and the average-consensus (Laplacian step 1/3) rule at the scored rate.

CHOICES (every underspecified point, the most literal and simplest reading): CHOICES_RA7 and CHOICES_RA8 below, printed on
CHOICES lines and repeated in each row's weakness field. The scored parameters were fixed in this file before its first
run; two changes after review (RA7's T-N construction, CHOICES_RA7 (6); RA8's scored drop rate, CHOICES_RA8 (2)), with the
added sensitivity prints; nothing was tuned toward a label.

Literature named by name only, as the declaration names it (no citation claim beyond the names; R10: nothing fetched
here): Palmgren and Miner (the linear damage rule); Basquin (the power-law S-N curve); Jadbabaie, Lin and Morse 2003
(coordination under switching nearest-neighbour rules); and one name from the review, Boyd, Ghosh, Prabhakar and Shah
2006 (randomized gossip), cited in RA8's weakness only as the reviewer's pointer, not fetched. Deterministic (numpy
default_rng, fixed seeds), no data files, no network; CPU, about two minutes. Rung R4 at most (a declared check on a
synthetic model); a note, not evidence (R8).

    cd /home/user/ashes_crr && uv run python Robotics/batches/rob_04.py > Robotics/batches/rob_04.txt
"""
from __future__ import annotations

import math
import sys

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

from crr.instrument.core import arc_length, cv
from crr.synthesis.harness import LABELS, TOL_G, TOL_N, make_row, outcome, rel, run_batch

DECL = "Robotics/DECLARATION_4B.md at d44e713"
N_BOOT, SEED_BOOT = 2000, 0


def _w(cond, yes, no):
    return yes if cond else no


def _qv(check):
    return "-> not computable" if check is None else ("-> Q holds" if check else "-> Q fails")


def _boot_ci(a, b, seed=SEED_BOOT, n_boot=N_BOOT, strata=None):
    """Paired bootstrap 95 % CI of cv(a) - cv(b) over units (the resampling regularity() uses). With `strata`, units are
    resampled within each stratum (a designed grid), so each resample keeps the design's composition."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    rng = np.random.default_rng(seed)
    groups = None if strata is None else [np.flatnonzero(np.asarray(strata) == g) for g in sorted(set(strata))]
    d = np.empty(n_boot)
    for i in range(n_boot):
        if groups is None:
            idx = rng.integers(0, len(a), len(a))
        else:
            idx = np.concatenate([g[rng.integers(0, len(g), len(g))] for g in groups])
        d[i] = cv(a[idx]) - cv(b[idx])
    lo, hi = np.percentile(d, [2.5, 97.5])
    return float(lo), float(hi)


def _boot_se(a, seed=SEED_BOOT, n_boot=N_BOOT):
    """Bootstrap standard error of cv(a) over units (the sampling error T-N's tolerance is set against)."""
    a = np.asarray(a, float)
    rng = np.random.default_rng(seed)
    return float(np.std([cv(a[rng.integers(0, len(a), len(a))]) for _ in range(n_boot)], ddof=1))


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
SEEDS_SENS = tuple(range(100, 140))   # other duty seeds (seed fragility; not scored)
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
    "occasion = one life); (5) 200 lives; (6) T-N (CHANGED AFTER REVIEW): Palmgren-Miner applied to the target Q names, "
    "Miner's prediction of the CV per arc: X_life = r D_fail + sum over the life's segments of (x - r d), exactly, with "
    "r = E[x] / E[d] (x the arc of a duty segment, d its damage, moments over the segments the lives used) and D_fail the "
    "damage at failure; the renewal-reward CLT gives the sum's variance per life as Var(x - r d) / E[d], the cross term is "
    "neglected, so CV_X^2 = Var(x - r d) E[d] / E[x]^2 + CV(D_fail)^2; the first term is computed from the segments without "
    "the lives, the second is the last cycle's overshoot (1e-5 of the first at m = 3; the whole of the prediction where the "
    "arc is proportional to the damage, m = 1 or constant load, where the first term is 0 up to round-off); the first T-N "
    "(the CV of Miner's damage per life, the domain's index in the place of the arc) could agree only where the arc is "
    "proportional to the damage, damage at failure being 1 by construction, and is printed, not scored, with its label, as "
    "is the asymptotic term alone; (7) T-C: 'CV per arc < CV per clock, as Miner predicts' read as the measured inequality "
    "with the paired-bootstrap 95 % CI of CV(arc) - CV(clock) below 0 (2000 resamples of the lives, seed 0; H-L5's scoring) "
    "AND Miner's prediction (6) of the two CVs (x the arc or the clock of a segment) ordering them the same way; (8) printed, "
    "not scored: the m sweep with each m's label under the three T-N readings, a constant-load control (S = 1 throughout, "
    "only the utilisation varies), H-L5's control (i) as regularity() computes it (the peak-to-peak of each life's load "
    "trace) and the maintenance reading; H-L5's control (iii) (peak-detected boundaries) has no reading here, the "
    "boundaries being failures, not extrema; (9) seed sensitivity (not scored): duty seeds 100-139 at m = 3, each labelled "
    "by outcome() with its own T-N and T-C; the label is called seed-fragile if more than 1 of the 40 differs from the "
    "scored label (RA2's rule in rob_01; CLAUDE.md's rule for a sensitivity table)")


def _duty(seed=SEED_DUTY):
    rng = np.random.default_rng(seed)
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
    """The renewal-reward term of Miner's prediction: the CV of X accumulated until the damage reaches 1, from per-segment
    moments only (asymptotic; the overshoot at failure omitted)."""
    r = x.mean() / d.mean()
    return math.sqrt(np.var(x - r * d, ddof=1) * d.mean()) / x.mean()


def _miner_cv(x, d, d_fail):
    """Miner's prediction of the CV of X per life (CHOICES_RA7 (6)): the renewal-reward term and the damage-at-failure
    overshoot term in quadrature. Returns (full prediction, renewal-reward term alone)."""
    a = _rr_cv(x, d)
    return math.sqrt(a * a + cv(d_fail) ** 2), a


def _ra7_score(m, S, tau, n, t0):
    res = _ra7_run(m, S, tau, n, t0)
    crr, null, dom_idx = cv(res["arc"]), cv(res["clock"]), cv(res["miner"])
    lo, hi = _boot_ci(res["arc"], res["clock"])
    k = res["n_seg"]
    x_arc, x_clk, d = 2.0 * n[:k] * S[:k], tau[:k], n[:k] * S[:k] ** m / N_REF
    p_arc, a_arc = _miner_cv(x_arc, d, res["miner"])
    p_clk, a_clk = _miner_cv(x_clk, d, res["miner"])
    check = bool(crr < null and hi < 0.0 and p_arc < p_clk)
    res.update(crr=crr, null=null, dom=p_arc, dom_idx=dom_idx, lo=lo, hi=hi, p_arc=p_arc, p_clk=p_clk, a_arc=a_arc,
               a_clk=a_clk, check=check, seg_per_life=k / N_LIFE, se=_boot_se(res["arc"]),
               out=outcome(crr=crr, null=null, domain=p_arc, check=check),
               out_asym=outcome(crr=crr, null=null, domain=a_arc, check=check),
               out_idx=outcome(crr=crr, null=null, domain=dom_idx, check=check))
    return res


def _count_str(labels):
    return ", ".join(f"{lab} {sum(1 for x in labels if x == lab)}" for lab in LABELS if any(x == lab for x in labels))


def ra7():
    tau, S, u, n, t0 = _duty()
    print("CHOICES RA7: " + CHOICES_RA7)
    print()
    sweep = {m: _ra7_score(m, S, tau, n, t0) for m in M_SWEEP}
    const = _ra7_score(M_SN, np.ones_like(S), tau, n, t0)
    r = sweep[M_SN]
    print(f"RA7 duty (seed {SEED_DUTY}): segments mean {SEG_MEAN:g} h, load U[{S_LO:g}, {S_HI:g}], utilisation U[{U_LO:g}, {U_HI:g}], "
          f"up to {F_MAX:g} cycles/h; N(S) = {N_REF:g} S^-m; {N_LIFE} lives per run")
    print("RA7 S-N exponent sweep (m = 3 scored; the others printed, not scored): m, segments used (per life), mean life h, mean "
          "cycles per life, CV per arc (bootstrap se), CV per clock, Miner's prediction of the CV per arc (full; renewal-reward "
          "term alone) and its relative difference to the CV per arc, CV of the Miner damage per life (the first T-N), bootstrap "
          "CI of CV(arc) - CV(clock), Miner's prediction of the CV per clock, check, label with T-N = the full prediction "
          "(scored) / the renewal-reward term alone / the first T-N")
    for m, s in list(sweep.items()) + [("S=1", const)]:
        head = f"m = {m:>4g}" if m != "S=1" else f"S = 1, m = {M_SN:g} (constant load)"
        print(f"  {head}: {s['n_seg']:>6d} segments ({s['seg_per_life']:.2f} per life), life {s['clock'].mean():10.3f} h, "
              f"{s['cycles'].mean():11.1f} cycles; CV arc {s['crr']:.6e} (se {s['se']:.6e}), CV clock {s['null']:.6e}; predicted "
              f"arc {s['p_arc']:.6e} (term {s['a_arc']:.6e}), relative difference {rel(s['crr'], s['p_arc']):.6f}; CV Miner "
              f"{s['dom_idx']:.6e}; CI [{s['lo']:+.6f}, {s['hi']:+.6f}]; predicted clock {s['p_clk']:.6f}; check "
              f"{_w(s['check'], 'holds', 'fails')}; {s['out']} / {s['out_asym']} / {s['out_idx']}")
    print(f"RA7 duty-seed sensitivity (m = {M_SN:g}, seeds {SEEDS_SENS[0]}-{SEEDS_SENS[-1]}; printed, not scored): seed, CV per "
          "arc (bootstrap se), Miner's prediction, relative difference, measured within two se of the prediction, check, label")
    sens = []
    for sd in SEEDS_SENS:
        tau_s, S_s, _u, n_s, t0_s = _duty(sd)
        s = _ra7_score(M_SN, S_s, tau_s, n_s, t0_s)
        z = dict(seed=sd, out=s["out"], rel=rel(s["crr"], s["p_arc"]), within=bool(abs(s["crr"] - s["p_arc"]) <= 2.0 * s["se"]),
                 check=s["check"])
        sens.append(z)
        print(f"  seed {sd}: CV arc {s['crr']:.6f} (se {s['se']:.6f}), predicted {s['p_arc']:.6f}, relative difference "
              f"{z['rel']:.6f}, within two se {_w(z['within'], 'yes', 'no')}, check {_w(s['check'], 'holds', 'fails')}; {s['out']}")
    print()

    crr, null, dom, dom_idx, check, out = r["crr"], r["null"], r["dom"], r["dom_idx"], r["check"], r["out"]
    rel_n, se_rel = rel(crr, dom), r["se"] / crr
    cv_amp = cv(r["amp"])
    lo_a, hi_a = _boot_ci(r["arc"], r["amp"])
    labels = "; ".join(f"m = {m:g}: {s['out']} (term alone {s['out_asym']}, first T-N {s['out_idx']})" for m, s in sweep.items())
    share = {name: float(np.mean(v.min() / v)) for name, v in (("clock", r["clock"]), ("arc", r["arc"]), ("Miner", r["miner"]))}
    life = r["clock"]
    n_sens = len(sens)
    sens_labels = _count_str([z["out"] for z in sens])
    rels = np.array([z["rel"] for z in sens])
    n_above = int((rels > TOL_N).sum())
    n_within = sum(z["within"] for z in sens)
    n_check = sum(z["check"] for z in sens)
    n_flip = sum(z["out"] != out for z in sens)
    fragile = n_flip > 1
    misses = [(m, s) for m, s in sweep.items() if rel(s["crr"], s["p_arc"]) > TOL_N]
    miss_txt = ("; the full prediction misses the tolerance at " + ", ".join(
        f"m = {m:g} ({rel(s['crr'], s['p_arc']):.2%}, {abs(s['crr'] - s['p_arc']) / s['se']:.2f} bootstrap se, "
        f"{s['seg_per_life']:.2f} segments per life)" for m, s in misses)) if misses else ""
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
        domain="Palmgren-Miner (damage = sum_i n_i / N_i from the S-N curve; failure at damage 1) applied to the target Q names: "
               "Miner's prediction of the CV per arc, the renewal-reward term from the duty segments' moments (without the "
               "lives) and the damage-at-failure overshoot term in quadrature (CHANGED AFTER REVIEW; CHOICES (6))",
        numbers=(f"{r['n_seg']} duty segments used ({r['seg_per_life']:.2f} per life); life mean {life.mean():.3f} h (min "
                 f"{life.min():.3f}, max {life.max():.3f}), {r['cycles'].mean():.1f} cycles; CV per arc {crr:.6f} (bootstrap se "
                 f"{r['se']:.6f}, {se_rel:.4f} of it), CV per clock {null:.6f}; Miner's prediction: CV per arc {dom:.6f} "
                 f"(renewal-reward term {r['a_arc']:.6f}; overshoot term, the CV of the damage at failure, {dom_idx:.6e}, damage "
                 f"at failure {r['miner'].min():.9f} to {r['miner'].max():.9f}), CV per clock {r['p_clk']:.6f}; paired-bootstrap "
                 f"95 % CI of CV(arc) - CV(clock) [{r['lo']:+.6f}, {r['hi']:+.6f}]; not scored: the first T-N (the CV of Miner's "
                 f"damage per life, {dom_idx:.6e}) reads {r['out_idx']}, the renewal-reward term alone as T-N reads "
                 f"{r['out_asym']}; duty seeds {SEEDS_SENS[0]}-{SEEDS_SENS[-1]} (not scored): {sens_labels}; T-N relative "
                 f"difference median {np.median(rels):.4f} (min {rels.min():.4f}, max {rels.max():.4f}), above {TOL_N:g} on "
                 f"{n_above} of {n_sens}; the measured CV within two bootstrap se of Miner's prediction on {n_within} of {n_sens}; "
                 f"T-C holds on {n_check} of {n_sens}; H-L5 control (i) as regularity() computes it, the peak-to-peak of each "
                 f"life's load trace (not scored; degenerate, see the reading): range {r['amp'].min():.4f} to "
                 f"{r['amp'].max():.4f}, CV {cv_amp:.6f}, CI of CV(arc) - CV(amplitude) [{lo_a:+.6f}, {hi_a:+.6f}]; S-N exponent "
                 f"sweep (not scored): {labels}; constant-load control (not scored): CV arc {const['crr']:.3e}, CV clock "
                 f"{const['null']:.6f}, Miner's prediction {const['p_arc']:.3e} (term {const['a_arc']:.3e}), {const['out']} "
                 f"(term alone {const['out_asym']}, first T-N {const['out_idx']}); maintenance reading (preventive replacement at "
                 f"the shortest of the {N_LIFE} lives in each index, no failure among them): the share of each life used, "
                 f"averaged over the lives, clock {share['clock']:.4f}, arc {share['arc']:.4f}, Miner {share['Miner']:.6f}"),
        tg=f"CV per arc {crr:.6f} vs null CV per clock {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"Miner's prediction of the CV per arc {dom:.6f}: {_w(rel_n <= TOL_N, 'agree (the domain has Q)', 'differ')} "
           f"(relative difference {rel_n:.6f}; the measured CV's bootstrap se is {se_rel:.4f} of it); not scored: the first T-N, "
           f"the CV of Miner's damage per life {dom_idx:.6e}: {_w(rel(crr, dom_idx) <= TOL_N, 'agree', 'differ')} (relative "
           f"difference {rel(crr, dom_idx):.6f})",
        tc=f"CV per arc {crr:.6f} < CV per clock {null:.6f} with the CI below 0 (upper {r['hi']:+.6f}): "
           f"{_w(crr < null and r['hi'] < 0.0, 'holds', 'fails')}; Miner's prediction orders them the same way (arc "
           f"{r['p_arc']:.6f} < clock {r['p_clk']:.6f}): {_w(r['p_arc'] < r['p_clk'], 'holds', 'fails')} {_qv(check)}",
        out=out,
        reading=(f"T-N sets the measured CV per arc against Miner's own prediction for it (relative difference {rel_n:.4f}, "
                 + _w(rel_n <= TOL_N, "within", "outside") + f" the {TOL_N:g} tolerance), so the row reads {out}; "
                 + _w(se_rel > TOL_N, f"the tolerance is finer than the sampling error of a CV from {N_LIFE} lives (bootstrap se "
                      f"{se_rel:.2%} of the CV), and ", "")
                 + f"over duty seeds {SEEDS_SENS[0]}-{SEEDS_SENS[-1]} the label reads {sens_labels}: "
                 + _w(fragile, f"SEED-FRAGILE ({n_flip} of {n_sens} differ from the scored label; where T-N misses, T-C decides, "
                      f"and it holds on {n_check} of {n_sens})", f"stable ({n_flip} of {n_sens} differ from the scored label)")
                 + f"; the measured CV lies within two bootstrap se of Miner's prediction on {n_within} of {n_sens} seeds"
                 + _w(n_within == n_sens, ", so the domain's prediction holds within sampling error on every seed and an ADDS "
                      "where T-N misses is the tolerance's, not a candidate", "")
                 + f"; the first T-N (the CV of Miner's damage per life, {dom_idx:.2e}; not scored) reads {r['out_idx']}"
                 + _w(r["out_idx"] != "REDUNDANT-DOMAIN", ": damage at failure is 1 by construction, so it can agree only where "
                      f"the arc is proportional to the damage (m = 1: {sweep[1.0]['out_idx']}; constant load: "
                      f"{const['out_idx']}), and its {r['out_idx']} at m = {M_SN:g} came from that construction, not from the arc", "")
                 + f"; the arc of a pulsating load trace is 2 S per cycle and Miner's damage is S^{M_SN:g} / N_ref per cycle: both "
                 f"count load cycles and neither counts the hours the joint stands idle, so both drop the utilisation's spread, "
                 f"which is what the clock carries (CV per clock {null:.6f}); the arc weights each cycle by S where Miner weights "
                 f"it by S^{M_SN:g}, so the arc keeps the load mix's spread (CV {crr:.6f}), and Miner's renewal-reward term "
                 f"predicts that spread from the duty segments alone ({r['a_arc']:.6f}); under constant load (S = 1) the row reads "
                 f"{const['out']} and at m = 1 {sweep[1.0]['out']}: there the arc is 2 N_ref times Miner's damage and the "
                 f"prediction is its overshoot term alone; with load variation the label over the sweep is "
                 + "; ".join(f"m = {m:g}: {s['out']}" for m, s in sweep.items())
                 + miss_txt
                 + "; the maintenance reading "
                 + _w(share["clock"] < share["arc"] < share["Miner"], "orders the three indices the same way",
                      "does not order the three indices the same way")
                 + f": preventive replacement at the shortest life seen uses on average {share['clock']:.2%} of each life on the "
                 f"clock, {share['arc']:.2%} on the arc and {share['Miner']:.4%} on Miner's damage; H-L5's control (i) as "
                 f"regularity() computes it, the peak-to-peak of a life's load trace, is the largest of the about "
                 f"{r['seg_per_life']:.0f} segment loads a life draws from U[{S_LO:g}, {S_HI:g}] (range {r['amp'].min():.4f} to "
                 f"{r['amp'].max():.4f} over the lives), so its CV ({cv_amp:.6f}) comes from how the loads are drawn, not from "
                 f"the gear physics: the control is degenerate here and marked not applicable; as computed it "
                 + _w(lo_a > 0.0, "beats the arc", _w(hi_a < 0.0, "is beaten by the arc", "ties the arc"))
                 + f" (CI of CV(arc) - CV(amplitude) [{lo_a:+.6f}, {hi_a:+.6f}])"
                 + _w(lo_a > 0.0, ", and by CRR.md's H-L5 (it 'fails if CV_C >= CV_dt, or a control matches it') the class claim "
                      "is not established while a control beats it", "")
                 + " (the declaration's T-C does not score the control)"),
        weakness=("CHOICE: " + CHOICES_RA7 + "; the model puts Miner's rule in (failure is defined as damage 1), so Miner's damage "
                  "index is regular by construction and T-N reads Miner's prediction for the arc instead; T-N's 1 % tolerance is "
                  "finer than the sampling error of a CV from 200 lives, so whether it agrees is decided by the duty seed (the "
                  "seed sensitivity); the gap between the arc and Miner's index is the S-N curve's curvature, m - 1; real "
                  "gearboxes add scatter in the S-N curve itself (lives at one load vary several-fold), load sequence effects "
                  "that the linear rule ignores, and wear modes (pitting, lubricant) that are not cycle-counted"),
        elegance="", child="")


# ====================================================================================== RA8 swarm consensus
N_AG = 20
EDGES = np.array([(i, (i + 1) % N_AG) for i in range(N_AG)])
Q_GRID = tuple(round(0.1 * k, 1) for k in range(1, 10))
Q_SCORED = 0.5                # the scored drop rate (CHOICES_RA8 (2))
N_PAT = 45                    # dropout patterns per rate: link seeds 0-44 (the first design's pattern count)
N_POOL_SEED = 5               # the first design: seeds 0-4 at each of the nine rates, pooled (printed, not scored)
EPS = 1e-3                    # rounds-to-epsilon: spread at most 1e-3 of the initial spread
SEED_X0, SEED_LINK = 0, 8
MAX_TICKS = 10 ** 6
CHOICES_RA8 = (
    "(1) the graph read as a ring of N = 20 agents (the simplest connected graph in which every agent has neighbours; ASSUMED, "
    "no source), initial values U[0, 1] from one seed (0) shared by every pattern, so only the dropout pattern varies; (2, "
    "CHANGED AFTER REVIEW) 'links drop with a seeded pattern' read as i.i.d. Bernoulli drops at one rate: each link down at "
    "each wall tick with probability q = 0.5 (a fair coin; ASSUMED round value, the declaration names no rate), one pattern "
    "= one link seed, seeds 0-44 (45 patterns, the first design's count; generator seeded with (8, 10 q, seed)); the first "
    "design pooled nine rates, q in {0.1, ..., 0.9} x seeds 0-4, and is printed, not scored: pooling puts the rates' spread "
    "in the mean link rate (1 - q) x 20 into the clock, which the event count cancels, so the q grid's width decides T-C "
    "there; every q in the grid is printed with 45 seeds and its own label; (3) 'averaging' read as Jadbabaie et al.'s "
    "nearest-neighbour rule, the domain theorem's own model: x_i <- (x_i + sum of up neighbours' x_j) / (1 + number of up "
    "neighbours), synchronous; its consensus value need not be the mean, so convergence is read on the spread max x - min x; "
    "(4) rounds-to-epsilon = the first tick at which the spread is at most 1e-3 of the initial spread; (5) an own exchange "
    "event = one up link at one tick (one pairwise exchange, counted once), events-to-epsilon = the up links summed through "
    "that tick; the ingredient is A1' natural time on a point process (one event = one step) with D5's cut at the event "
    "itself (the swarm has no rotor, O3), so no phase and no antipodal_cuts are computed; the declared H-L5 is its form (a "
    "natural-time count against the clock) without its controls, which have no reading on an event count; (6) the domain's "
    "jointly connected intervals read greedily: consecutive intervals, each closed at the first tick at which the union of "
    "its graphs is connected; intervals-to-epsilon = the index of the interval holding the epsilon tick; (7) 'regular across "
    "dropout patterns' = the CV over the 45 patterns at the scored rate; T-C = CV per event < CV per wall tick with the "
    "paired-bootstrap 95 % CI of the difference (2000 resamples of the patterns, seed 0) below 0; the pooled first design's "
    "CI is printed twice, resampling the 45 patterns freely (as first run) and within the q strata (a designed grid: either "
    "CI describes the grid, not a sampling distribution); (8) printed, not scored: every q with 45 seeds (Jadbabaie's rule "
    "and the average-consensus rule x <- x - (1/3) L(t) x, each labelled), the pooled first design, the non-empty-tick reading "
    "of an exchange event (a tick in which at least one link is up) at the scored rate, and the rounds to consensus per q")

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


FIELDS_RA8 = ("ticks", "events", "nonempty", "intervals")


def _ra8_runs(x0, rule, iq, q, seeds):
    runs = [_consensus(x0, iq, q, s, rule) for s in seeds]
    return {f: np.array([r[f] for r in runs], float) for f in FIELDS_RA8}


def _ra8_label(arr, ev="events", strata=None):
    crr, null, dom = cv(arr[ev]), cv(arr["ticks"]), cv(arr["intervals"])
    lo, hi = _boot_ci(arr[ev], arr["ticks"], strata=strata)
    check = bool(crr < null and hi < 0.0)
    return dict(crr=crr, null=null, dom=dom, lo=lo, hi=hi, check=check, out=outcome(crr=crr, null=null, domain=dom, check=check))


def ra8():
    x0 = np.random.default_rng(SEED_X0).uniform(0.0, 1.0, N_AG)
    print("CHOICES RA8: " + CHOICES_RA8)
    print()
    per_q = {}
    for iq, q in enumerate(Q_GRID, 1):
        aj = _ra8_runs(x0, "jadbabaie", iq, q, range(N_PAT))
        al = _ra8_runs(x0, "laplacian", iq, q, range(N_PAT))
        per_q[q] = dict(arr=aj, lab=_ra8_label(aj), arr_l=al, lab_l=_ra8_label(al))
    arr, sc = per_q[Q_SCORED]["arr"], per_q[Q_SCORED]["lab"]
    alt_ne = _ra8_label(arr, "nonempty")
    alt_l = per_q[Q_SCORED]["lab_l"]
    n_all_nonempty = int((arr["nonempty"] == arr["ticks"]).sum())
    pool = {f: np.concatenate([per_q[q]["arr"][f][:N_POOL_SEED] for q in Q_GRID]) for f in FIELDS_RA8}
    strata = np.repeat(np.arange(len(Q_GRID)), N_POOL_SEED)
    pooled = _ra8_label(pool)
    pooled_s = _ra8_label(pool, strata=strata)
    fixed_labels = [per_q[q]["lab"]["out"] for q in Q_GRID]
    fixed_l_labels = [per_q[q]["lab_l"]["out"] for q in Q_GRID]
    tg_rels = np.array([rel(per_q[q]["lab"]["crr"], per_q[q]["lab"]["null"]) for q in Q_GRID])

    print(f"RA8 ring of {N_AG}, x0 seed {SEED_X0} (initial spread {np.ptp(x0):.6f}), epsilon {EPS:g} of the initial spread; "
          f"per drop rate q, {N_PAT} link seeds (0-{N_PAT - 1}); q = {Q_SCORED:g} scored, the others printed, not scored: mean "
          "rounds to consensus in ticks, exchange events, non-empty ticks and jointly connected intervals (Jadbabaie's rule); "
          "CV per event, per tick, per interval; T-G relative difference; paired-bootstrap CI of CV(events) - CV(ticks); label; "
          "and the average-consensus rule's CVs, CI and label")
    for q in Q_GRID:
        a, lb, ll = per_q[q]["arr"], per_q[q]["lab"], per_q[q]["lab_l"]
        print(f"  q = {q:.1f}: {a['ticks'].mean():9.1f} ticks, {a['events'].mean():9.1f} events, {a['nonempty'].mean():9.1f} "
              f"non-empty ticks, {a['intervals'].mean():7.1f} intervals; CV events {lb['crr']:.6f}, ticks {lb['null']:.6f}, "
              f"intervals {lb['dom']:.6f}; T-G rel {rel(lb['crr'], lb['null']):.6f}; CI [{lb['lo']:+.6f}, {lb['hi']:+.6f}]; "
              f"{lb['out']} | average consensus: CV events {ll['crr']:.6f}, ticks {ll['null']:.6f}, intervals {ll['dom']:.6f}, "
              f"CI [{ll['lo']:+.6f}, {ll['hi']:+.6f}]; {ll['out']}")
    print(f"RA8 the first design (printed, not scored): nine rates pooled, seeds 0-{N_POOL_SEED - 1} at each ({len(strata)} "
          f"patterns): CV events {pooled['crr']:.6f}, ticks {pooled['null']:.6f}, intervals {pooled['dom']:.6f}; CI resampling "
          f"the patterns freely [{pooled['lo']:+.6f}, {pooled['hi']:+.6f}] ({pooled['out']}), within the q strata "
          f"[{pooled_s['lo']:+.6f}, {pooled_s['hi']:+.6f}] ({pooled_s['out']})")
    print(f"RA8 second readings at q = {Q_SCORED:g} (printed, not scored): non-empty ticks as the event: CV {alt_ne['crr']:.6f} "
          f"vs wall {alt_ne['null']:.6f} (every tick non-empty on {n_all_nonempty} of {N_PAT} patterns), CI "
          f"[{alt_ne['lo']:+.6f}, {alt_ne['hi']:+.6f}], {alt_ne['out']}; average consensus x <- x - (1/3) L(t) x: CV per event "
          f"{alt_l['crr']:.6f}, per wall tick {alt_l['null']:.6f}, per interval {alt_l['dom']:.6f}, CI [{alt_l['lo']:+.6f}, "
          f"{alt_l['hi']:+.6f}], {alt_l['out']}")
    print()

    crr, null, dom, check, out = sc["crr"], sc["null"], sc["dom"], sc["check"], sc["out"]
    ev, tk, iv = arr["events"], arr["ticks"], arr["intervals"]
    q_lo, q_hi = Q_GRID[0], Q_GRID[-1]
    m_lo, m_hi = per_q[q_lo]["arr"], per_q[q_hi]["arr"]
    fixed_txt = _count_str(fixed_labels)
    fixed_l_txt = _count_str(fixed_l_labels)
    return make_row(
        "robotics", f"RA8 swarm consensus with intermittent links: {N_AG} agents on a ring, Jadbabaie et al.'s nearest-neighbour "
                    f"averaging, each link down at each tick with probability q = {Q_SCORED:g}, {N_PAT} dropout patterns (link "
                    f"seeds 0-{N_PAT - 1}), rounds to a spread of {EPS:g} of the initial",
        source=f"ROB1 RA8 (declared in {DECL}; forecast REDUNDANT-DOMAIN)",
        Q="convergence counted per own exchange event is regular across dropout patterns; per wall time it is not (computed as: "
          "the CV over the patterns of the rounds-to-epsilon counted in exchange events, against the same counted in wall ticks)",
        ingredient="A1' natural time on a point process (one own exchange event = one step; D5: the cut is the event itself, the "
                   "swarm having no rotor, O3), declared as 'A3 (cuts at the system's own events), H-L5': H-L5's form (the "
                   "natural-time count against the clock) without its controls, which have no reading on an event count ((i) "
                   "amplitude, (ii) identity metric, (iii) peak-detected boundaries), so the H-L5 label is nominal",
        null="wall time (rounds-to-epsilon in ticks)",
        domain="consensus under switching topologies (Jadbabaie et al. 2003): convergence per jointly connected interval, the CV "
               "of the rounds-to-epsilon counted in greedy jointly connected intervals",
        numbers=(f"rounds-to-epsilon over {N_PAT} patterns at q = {Q_SCORED:g}: events mean {ev.mean():.1f} (min {ev.min():.0f}, max "
                 f"{ev.max():.0f}), CV {crr:.6f}; ticks mean {tk.mean():.1f} (min {tk.min():.0f}, max {tk.max():.0f}), CV "
                 f"{null:.6f}; jointly connected intervals mean {iv.mean():.1f} (min {iv.min():.0f}, max {iv.max():.0f}), CV "
                 f"{dom:.6f}; paired-bootstrap 95 % CI of CV(events) - CV(ticks) [{sc['lo']:+.6f}, {sc['hi']:+.6f}]; per rate "
                 f"q in {{{q_lo:g}, ..., {q_hi:g}}}, {N_PAT} seeds each (not scored): {fixed_txt}, T-G relative difference "
                 f"{tg_rels.min():.4f} to {tg_rels.max():.4f}; the average-consensus rule per rate: {fixed_l_txt}; the first "
                 f"design, nine rates pooled with {N_POOL_SEED} seeds each (not scored): CV events {pooled['crr']:.6f}, ticks "
                 f"{pooled['null']:.6f}, intervals {pooled['dom']:.6f}, CI free [{pooled['lo']:+.6f}, {pooled['hi']:+.6f}] "
                 f"({pooled['out']}), within q strata [{pooled_s['lo']:+.6f}, {pooled_s['hi']:+.6f}] ({pooled_s['out']}); second "
                 f"readings at q = {Q_SCORED:g} (not scored): non-empty ticks CV {alt_ne['crr']:.6f} ({alt_ne['out']}), average "
                 f"consensus CV events {alt_l['crr']:.6f}, ticks {alt_l['null']:.6f}, intervals {alt_l['dom']:.6f} "
                 f"({alt_l['out']}); robotics reading, rounds to consensus ({N_PAT} seeds each) at q = {q_lo:g}, {Q_SCORED:g} and "
                 f"{q_hi:g}: {m_lo['ticks'].mean():.1f}, {tk.mean():.1f} and {m_hi['ticks'].mean():.1f} ticks, "
                 f"{m_lo['events'].mean():.1f}, {ev.mean():.1f} and {m_hi['events'].mean():.1f} messages, "
                 f"{m_lo['intervals'].mean():.1f}, {iv.mean():.1f} and {m_hi['intervals'].mean():.1f} jointly connected intervals"),
        tg=f"CV per event {crr:.6f} vs null CV per wall tick {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')} "
           f"(relative difference {rel(crr, null):.6f})",
        tn=f"jointly connected intervals, CV {dom:.6f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')} "
           f"(relative difference {rel(crr, dom):.6f})",
        tc=f"CV per event {crr:.6f} < CV per wall tick {null:.6f} with the CI below 0 (upper {sc['hi']:+.6f}): "
           f"{_w(check, 'holds', 'fails')} {_qv(check)}",
        out=out,
        reading=(f"at one drop rate (q = {Q_SCORED:g}) the {N_PAT} patterns differ only by seed: a tick carries a binomial number of "
                 f"exchanges around (1 - q) x {N_AG} = {(1 - Q_SCORED) * N_AG:g}, so the event count follows the tick count (CV "
                 f"per event {crr:.6f}, per tick {null:.6f}, relative difference {rel(crr, null):.4f}), and the CI of the "
                 f"difference [{sc['lo']:+.6f}, {sc['hi']:+.6f}] "
                 + _w(sc["hi"] < 0.0, "lies below 0", _w(sc["lo"] > 0.0, "lies above 0", "includes 0"))
                 + f", so T-C {_w(check, 'holds', 'fails')} and the row reads {out}; at each fixed rate in the grid ({N_PAT} "
                 f"seeds each) the label reads {fixed_txt}; the first design, which pooled the nine rates ({N_POOL_SEED} seeds "
                 f"each), reads {pooled_s['out']} (CI within the q strata [{pooled_s['lo']:+.6f}, {pooled_s['hi']:+.6f}]): pooling "
                 f"puts the spread of the mean link rate (1 - q) x {N_AG}, from {(1 - q_hi) * N_AG:g} to {(1 - q_lo) * N_AG:g} "
                 f"exchanges per tick, into the clock (CV {pooled['null']:.6f}), which the event count cancels (CV "
                 f"{pooled['crr']:.6f}), so the q grid's width decides T-C there, and the label is "
                 + _w(pooled_s["out"] == "ADDS" and "ADDS" not in fixed_labels,
                      f"ADDS only when the rates are pooled and never at a fixed rate",
                      f"{pooled_s['out']} pooled and {fixed_txt} at the fixed rates")
                 + f"; the domain's interval count has CV {dom:.6f} at the scored rate ("
                 + _w(dom < crr, "more regular than the event count", "less regular than the event count")
                 + f", relative difference {rel(crr, dom):.4f}); under the non-empty-tick reading of an event the row would read "
                 f"{alt_ne['out']} (every tick carries an exchange on {n_all_nonempty} of {N_PAT} patterns), and under the "
                 f"average-consensus rule {alt_l['out']} at q = {Q_SCORED:g} ({fixed_l_txt} over the rates); the exchange count "
                 f"is the usual cost clock of gossip averaging, so even where it wins it restates a standard count"),
        weakness=("CHOICE: " + CHOICES_RA8 + "; i.i.d. drops make each tick's exchanges a binomial draw: at a fixed rate the event "
                  "count and the tick count differ only by that draw, and pooled rates build the event count's regularity in; "
                  "bursty (Markov) drops, lossy links and a swarm whose graph moves with its state were not modelled; the "
                  "Jadbabaie rule's weights change with the number of up neighbours, so an exchange is not a fixed contraction; "
                  "per-exchange (per-message, per-edge-activation) counting is the usual cost clock in randomized gossip "
                  "consensus (Boyd, Ghosh, Prabhakar and Shah 2006, the reviewer's pointer, not fetched here, R10), so an "
                  "expert would read the event count as standard; the pooled design's bootstrap resamples a designed grid, "
                  "so its CI describes that grid, not a sampling distribution; 45 seeds per rate is the first design's "
                  "pattern count, not chosen for power"),
        elegance="", child="")


def main():
    r7 = ra7()
    r8 = ra8()
    return run_batch("ROB1 stage 4b batch 04: RA7 actuator wear by arc, RA8 swarm consensus with intermittent links "
                     f"(Robotics/DECLARATION_4B.md; declared at d44e713)", [r7, r8])


if __name__ == "__main__":
    sys.exit(main())

"""ROB1 stage 4b batch 05: applications RA9 (handover timing on the partner's phase) and RA10 (safe interruptibility of a
learning robot) of the declared battery Robotics/DECLARATION_4B.md (pushed at d44e713 before any model; prompt-log entry
257; AGENT_LOG 223). Each row fixes, as declared, the model, Q, the CRR-proper ingredient, the null (T-G), the domain's own
theorem (T-N), the check (T-C) and the investigator's forecast; the labels are computed from the numbers by
crr.synthesis.harness.outcome() (R15).

RA9. A human reach from rest to rest along a minimum-jerk trajectory, x(t) = A (10 tau^3 - 15 tau^4 + 6 tau^5), tau = t/T,
     A = 0.4 m, duration T uniform on [0.5, 1.5] s; 200 test reaches (seed 0). The robot samples the hand at 1 kHz from the
     reach onset and releases the object at a sample of that clock. A3: the release at the first antipodal cut
     (antipodal_cuts from the onset) on the intrinsic phase (intrinsic_phase) of the reach's position record from onset to
     arrival. Null: a fixed delay from onset, tuned on 200 other durations (seed 1) to minimise the mean handover timing
     error |release - T/2| / T. Domain: minimum jerk (Flash & Hogan 1985), peak velocity at T/2, released at the clock
     sample nearest T/2. Decisive quantity (T-G, T-N): the landing point, the mean over the test reaches of release / T.
     T-C: every reach fires a cut and each offset |release - T/2| is within 2 % of its T. A3 does not fix which record
     carries the phase of a single reach (CRR.md A3 needs a rotor; O3), so three offline readings are computed (the
     position record, the velocity record, the position with the onset-to-arrival straight line removed) and the row is
     INTERNAL when their T-C verdicts differ (synthesis note section 2; as batch_21 and pred_01 compute it). Printed, not
     scored: each reading's own label, the first run's offset quantity with its labels, the exact-theorem reading of T-N
     (landing at 0.5), the velocity maximum on the record, a same-record marker at a tuned fraction of the record (a
     non-A3 ablation that knows T), and a causal (online) reading of the position cut under four minimum windows (it is
     degenerate: it fires at the first admissible sample).
RA10. A 3 x 7 ring gridworld: start (0, 0), goal (0, 6); the short route along row 0 (6 moves) crosses the five interior
     cells where a human works (the interruption zone); the long route (10 moves) goes down, along row 2 and back up.
     Actions N, S, E, W, stay; reward -1 per tick; gamma = 1. Orseau & Armstrong's interruption: at each tick in the zone,
     with probability theta = 0.5, the robot's action is replaced by the interruption policy's, stay (the stop button
     halts it). Tabular Q-learning, SARSA, Safe SARSA (Orseau & Armstrong's modification: the target on the learner's own
     next action, not the executed one) and SARSA + ETM (the interrupted ticks are not the learner's steps: no reward, no
     update, no own time); 20 seeds x 4000 episodes with exploring starts. Policy distance: the share of the 15 non-terminal
     cells from which the greedy policy learned with interruptions and the one learned without (same learner, same seed)
     reach the goal in a different number of steps in the uninterrupted gridworld. Scored: the long-run learned policies;
     T-C: the distance is 0 under ETM (Q is about ETM; Safe SARSA's value enters through T-N). Printed: the exact limit of
     each learner's expected update (value iteration) and the long-run policies' agreement with it, the action-by-action
     (Hamming) distance, a second interruption policy (W: the human pulls the robot one cell back) and theta swept in the
     exact limit, each with the label outcome() gives it.

CHOICES (every underspecified point, the most literal and simplest reading): CHOICES_RA9 and CHOICES_RA10 below, printed on
CHOICES lines and repeated in each row's weakness field. Nothing was tuned after a run. No revision of this file before
its first run is committed (its first commit, a158377, already held the first run's version), so that the first run's
parameters were fixed before it is this file's statement, not a commit's. CHANGED AFTER REVIEW (2026-09-30; no model,
parameter, seed, reach, gridworld or null changed; the first run's output is described in each row's weakness): RA9's
decisive quantity (the landing point, not the mean offset), its INTERNAL computation over the three carrier readings, the
causal reading reported as degenerate, and the same-record fraction marker added; RA10's T-C reads Q on ETM alone (the
first run also required Safe SARSA's zero, which made ADDS unreachable), and the theta sweep printed with its labels.

Literature named by name only, as the declaration names it (R10: nothing fetched here; the Orseau & Armstrong quotes
used for the model are those of docs/citations/eps1_2026-09-29.md, section S3): Flash and Hogan 1985 (the minimum-jerk
model of reaching); Orseau and Armstrong 2016, "Safely Interruptible Agents" (UAI): Theorem 14 (Q-learning), Theorem 15
(SARSA is not), Theorem 17 (Safe SARSA); Sutton and Barto (Q-learning, SARSA). Deterministic (numpy default_rng and
Python random.Random with fixed seeds, separate generators for the learner and the interruption), no data files, no
network; CPU, about fifteen seconds. Rung R4 at most (a declared check on a synthetic model); a note, not evidence (R8).

    cd /home/user/ashes_crr && uv run python Robotics/batches/rob_05.py > Robotics/batches/rob_05.txt
"""
from __future__ import annotations

import math
import random
import sys

import numpy as np

from crr.instrument.core import antipodal_cuts, intrinsic_phase
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

DECL = "Robotics/DECLARATION_4B.md at d44e713"


def _w(cond, yes, no):
    return yes if cond else no


def _qv(check):
    return "-> not computable" if check is None else ("-> Q holds" if check else "-> Q fails")


# ====================================================================================== RA9 handover timing
DT = 1.0e-3                   # s, the robot's sensor clock (1 kHz); every rule releases at a sample of it
T_LO, T_HI = 0.5, 1.5         # s, reach duration uniform on [T_LO, T_HI] (ASSUMED round values for a human reach)
AMP = 0.4                     # m, reach amplitude (ASSUMED; the analytic-signal phase is scale-free)
N_TEST, N_TRAIN = 200, 200
SEED_TEST, SEED_TRAIN = 0, 1
TOL_C9 = 0.02                 # T-C: each offset within 2 % of T (declared)
READ9 = ("pos", "vel", "lin")  # the three offline readings of the carrier; the row is INTERNAL when their T-C verdicts differ
RNAME9 = {"pos": "position record", "vel": "velocity record", "lin": "position with the straight line removed"}
F_GRID = np.round(np.arange(0, 1001) * 1.0e-3, 3)   # the same-record marker's fractions (printed, not scored)
M_WIN = (3, 10, 50, 200)      # causal reading: minimum windows in samples (3, the first run's, is the smallest record)
CHOICES_RA9 = (
    "(1) the reach: one-dimensional minimum-jerk position x(t) = A (10 tau^3 - 15 tau^4 + 6 tau^5), tau = t/T, from rest to "
    "rest, A = 0.4 m (ASSUMED; the phase is scale-free), T uniform on [0.5, 1.5] s (ASSUMED round values), 200 test reaches "
    "(seed 0); (2) the robot's clock: the hand sampled at 1 kHz from the reach onset (the onset on a sample), the record "
    "ending at the last sample at or before arrival; every rule releases at a sample of this clock; (3) 'the reach's phase' "
    "read as the instrument's one implemented intrinsic phase (intrinsic_phase: mean removed, analytic-signal phase) of a "
    "record of the reach from onset to arrival, computed on the whole record (offline); the release is the first antipodal "
    "cut after the onset (antipodal_cuts, start = 0, half turn pi); a record that holds no cut releases at its last sample "
    "and is counted as a miss; A3 needs a rotor and a single reach has none (CRR.md O3: for non-cyclic becoming nothing yet "
    "sets L), so nothing in CRR.md fixes which record carries the phase: three readings are computed, (i) the position "
    "record, (ii) the velocity record, (iii) the position with the onset-to-arrival straight line removed, and the row is "
    "INTERNAL when their T-C verdicts are not all the same (the synthesis note, section 2; CHANGED AFTER REVIEW: the first "
    "run scored reading (i) alone); (4) the null: a fixed delay from onset, a whole number of clock samples, tuned on 200 "
    "other durations (seed 1) to minimise the mean handover timing error |release - T/2| / T (exhaustive search over 0 to "
    "1500 samples, the first minimum; unchanged from the first run); (5) the domain (T-N): minimum jerk's peak velocity at "
    "T/2, released at the clock sample nearest T/2 (the theorem's release on the same clock, so that T-N compares like with "
    "like); the exact-theorem reading (landing at 0.5 exactly) is printed with its labels, not scored; (6) the decisive "
    "quantity for T-G and T-N: the landing point, the mean over the 200 test reaches of release / T (Q: the cut 'lands at "
    "the reach's midpoint'; CHANGED AFTER REVIEW: the first run used the mean offset |release - T/2| / T, whose domain value "
    "is the clock's rounding alone, so that the 1 % relative T-N could agree only when the releases fell on the domain's "
    "samples in nearly every reach; that quantity is printed with its labels, not scored); T-C: every test reach fires a "
    "cut and each offset |release - T/2| is within 0.02 T ('whatever the duration': per reach, the maximum); (7) printed, "
    "not scored: each reading's own label; the velocity maximum on the record (the domain's marker located); a same-record "
    "marker that is not A3, the release at the sample nearest a fixed fraction f of the record's length, f tuned on the "
    "training durations to minimise the mean timing error (grid 0 to 1 in steps of 0.001, the first minimum), used as an "
    "extra T-G null (ADDED AFTER REVIEW: the declared fixed delay lacks T by construction, the offline records know it); a "
    "causal reading of the position cut (the phase of the record so far, the release at the first sample k >= m - 1 at "
    "which the record from the onset to k holds a half-turn from its onset) for minimum windows m in {3, 10, 50, 200} "
    "samples (m = 3, the first run's, is the smallest record whose phase can advance)")


def _reach(T):
    n = int(math.floor(T / DT))
    t = np.arange(n + 1) * DT
    tau = np.minimum(t / T, 1.0)
    x = AMP * (10.0 * tau ** 3 - 15.0 * tau ** 4 + 6.0 * tau ** 5)
    v = AMP / T * (30.0 * tau ** 2 - 60.0 * tau ** 3 + 30.0 * tau ** 4)
    return x, v, n


def _a3_release(sig):
    """First antipodal cut after the onset on the record's intrinsic phase; (sample, fired)."""
    c = antipodal_cuts(intrinsic_phase(sig), start=0)
    return (int(c[1]), True) if len(c) > 1 else (len(sig) - 1, False)


def _causal_release(sig, m=3):
    """The robot sees only the record so far: release at the first sample k >= m - 1 at which the phase of sig[0..k] has
    advanced half a turn from its onset (the condition under which antipodal_cuts on that record returns a cut; checked
    once at the firing sample)."""
    for k in range(m - 1, len(sig)):
        ph = intrinsic_phase(sig[:k + 1])
        if np.any(ph[1:] - ph[0] >= np.pi):
            if len(antipodal_cuts(ph, start=0)) < 2:
                raise RuntimeError("RA9: causal criterion and antipodal_cuts disagree")
            return k, True
    return len(sig) - 1, False


def _score9(rel_samples, T):
    """Per-reach offsets |k dt - T/2| / T."""
    k = np.asarray(rel_samples, float)
    return np.abs(k * DT - T / 2.0) / T


def ra9():
    print("CHOICES RA9: " + CHOICES_RA9)
    print()
    T_test = np.random.default_rng(SEED_TEST).uniform(T_LO, T_HI, N_TEST)
    T_train = np.random.default_rng(SEED_TRAIN).uniform(T_LO, T_HI, N_TRAIN)

    cand = np.arange(0, int(round(T_HI / DT)) + 1)
    train_err = (np.abs(cand[:, None] * DT - T_train[None, :] / 2.0) / T_train[None, :]).mean(axis=1)
    d_star = int(cand[int(np.argmin(train_err))])
    n_train = np.array([int(math.floor(float(T) / DT)) for T in T_train])
    k_fr = np.rint(F_GRID[:, None] * n_train[None, :])
    fr_err = (np.abs(k_fr * DT - T_train[None, :] / 2.0) / T_train[None, :]).mean(axis=1)
    f_star = float(F_GRID[int(np.argmin(fr_err))])

    ALL = ("pos", "vel", "lin", "causal", "vmax", "frac", "delay", "dom")
    rel_k = {name: [] for name in ALL}
    fired = {name: [] for name in ("pos", "vel", "lin", "causal")}
    caus = {m: ([], []) for m in M_WIN}
    for T in T_test:
        x, v, n = _reach(float(T))
        k, f = _a3_release(x); rel_k["pos"].append(k); fired["pos"].append(f)
        k, f = _a3_release(v); rel_k["vel"].append(k); fired["vel"].append(f)
        lin = x - (x[0] + (x[-1] - x[0]) * np.arange(n + 1) / n)
        k, f = _a3_release(lin); rel_k["lin"].append(k); fired["lin"].append(f)
        rel_k["vmax"].append(int(np.argmax(v)))
        for m in M_WIN:
            k, f = _causal_release(x, m); caus[m][0].append(k); caus[m][1].append(f)
        rel_k["causal"].append(caus[M_WIN[0]][0][-1]); fired["causal"].append(caus[M_WIN[0]][1][-1])
        rel_k["frac"].append(int(np.rint(f_star * n)))
        rel_k["delay"].append(d_star)
        rel_k["dom"].append(int(np.rint(T / (2.0 * DT))))
    err = {name: _score9(ks, T_test) for name, ks in rel_k.items()}
    ms = {name: np.abs(np.asarray(ks, float) * DT - T_test / 2.0) * 1e3 for name, ks in rel_k.items()}
    L = {name: float((np.asarray(ks, float) * DT / T_test).mean()) for name, ks in rel_k.items()}
    null, dom, frac = L["delay"], L["dom"], L["frac"]
    null_off, dom_off = float(err["delay"].mean()), float(err["dom"].mean())

    def lab(name):
        crr = L[name]
        allf = all(fired[name]) if name in fired else True
        check = bool(allf and float(err[name].max()) <= TOL_C9)
        off = float(err[name].mean())
        return dict(crr=crr, check=check, off=off,
                    land=outcome(crr=crr, null=null, domain=dom, check=check),
                    exact=outcome(crr=crr, null=null, domain=0.5, check=check),
                    frac=outcome(crr=crr, null=frac, domain=dom, check=check),
                    first=outcome(crr=off, null=null_off, domain=dom_off, check=check))

    labs = {name: lab(name) for name in ("pos", "vel", "lin", "causal", "vmax")}
    verdicts = {nm: labs[nm]["check"] for nm in READ9}
    internal = len(set(verdicts.values())) > 1
    crr, check = labs["pos"]["crr"], labs["pos"]["check"]
    out = outcome(crr=crr, null=null, domain=dom, check=check, internal=internal)

    names = {"pos": "A3 (i) on the position record", "vel": "A3 (ii) on the velocity record",
             "lin": "A3 (iii) position, straight line removed", "causal": "A3 causal, position so far (m = 3)",
             "vmax": "velocity maximum on the record", "frac": f"same-record marker, fraction {f_star:.3f}",
             "delay": "fixed delay (null)", "dom": "sample nearest T/2 (domain)"}
    print(f"RA9 reaches: T uniform on [{T_LO:g}, {T_HI:g}] s ({N_TEST} test, seed {SEED_TEST}; {N_TRAIN} training, seed {SEED_TRAIN}), "
          f"1 kHz clock; the fixed delay tuned on the training durations: {d_star} samples ({d_star * DT:.3f} s; training error "
          f"{float(train_err.min()):.6f}); the same-record marker's fraction tuned on the same durations: {f_star:.3f} of the record "
          f"(training error {float(fr_err.min()):.6f})")
    print("RA9 per rule: reaches fired, landing point (mean release / T; the decisive quantity), mean and max |release - T/2| / T, "
          "mean and max in ms, trend with T (mean offset on the shortest and longest fifth of T); for the A3 readings and the "
          "velocity maximum: T-C, and the labels outcome() gives on the landing point with the same-clock domain (the row's "
          "quantity), with the exact-theorem domain 0.5, and with the same-record marker as the null, and on the first run's "
          "offset quantity")
    order = np.argsort(T_test)
    fifth = N_TEST // 5
    for name in ALL:
        e = err[name]
        nf = sum(fired[name]) if name in fired else N_TEST
        if name in labs:
            b = labs[name]
            tail = (f"check {_w(b['check'], 'holds', 'fails')}; landing {b['land']}; exact {b['exact']}; "
                    f"marker null {b['frac']}; first run's offset {b['first']}")
        else:
            tail = "-"
        print(f"  {names[name]:44s} fired {nf:3d}/{N_TEST}; landing {L[name]:.6f}; mean {float(e.mean()):.6e}, max {float(e.max()):.6e}; "
              f"{float(ms[name].mean()):8.3f} ms, max {float(ms[name].max()):8.3f} ms; shortest fifth {float(e[order[:fifth]].mean()):.6e}, "
              f"longest fifth {float(e[order[-fifth:]].mean()):.6e}; {tail}")
    same = {nm: int(sum(a == b for a, b in zip(rel_k[nm], rel_k["dom"]))) for nm in READ9}
    maxd = {nm: int(max(abs(a - b) for a, b in zip(rel_k[nm], rel_k["dom"]))) for nm in READ9}
    signed = (np.asarray(rel_k["pos"], float) * DT - T_test / 2.0) / T_test
    print("RA9 cut at the domain's sample: " + "; ".join(f"{RNAME9[nm]} {same[nm]} of {N_TEST} reaches, at most {maxd[nm]} "
                                                         f"sample(s) from it" for nm in READ9)
          + f"; signed offset of reading (i) (release - T/2) / T: mean {float(signed.mean()):+.6e}, min {float(signed.min()):+.6e}, "
          f"max {float(signed.max()):+.6e}")
    rom = {"pos": "i", "vel": "ii", "lin": "iii"}
    print("RA9 the three readings' T-C verdicts: " + ", ".join(f"({rom[nm]}) {_w(verdicts[nm], 'holds', 'fails')}" for nm in READ9)
          + f"; not all the same: {_w(internal, 'yes (INTERNAL)', 'no')}")
    c_first = {m: sum(k == m - 1 for k in caus[m][0]) for m in M_WIN}
    degenerate = all(c_first[m] == N_TEST for m in M_WIN)
    x0, _, _ = _reach(float(T_test[0]))
    ph0 = intrinsic_phase(x0[:3])
    print("RA9 causal reading, firing sample by minimum window m (all test reaches): "
          + "; ".join(f"m = {m}: samples {sorted(set(caus[m][0]))[:5]}{'...' if len(set(caus[m][0])) > 5 else ''}, at m - 1 on "
                      f"{c_first[m]} of {N_TEST}, fired {sum(caus[m][1])}, mean offset {float(_score9(caus[m][0], T_test).mean()):.6e}"
                      for m in M_WIN)
          + f"; the first test reach's 3-sample record x = [{', '.join(f'{v:.3e}' for v in x0[:3])}] m has phase "
            f"[{', '.join(f'{v:.4f}' for v in ph0)}] rad; fires at the first admissible sample under every window: "
          + _w(degenerate, "yes (degenerate)", "no"))
    print()

    e = err["pos"]

    def tri(key):
        return ", ".join(f"({rom[nm]}) {labs[nm][key]}" for nm in READ9)

    wrong_only = [RNAME9[nm] for nm in READ9 if labs[nm]["land"] == "WRONG"]
    return make_row(
        "robotics", f"RA9 handover timing on the partner's phase: a human reach from rest to rest along a minimum-jerk trajectory "
                    f"(A = {AMP:g} m, T uniform on [{T_LO:g}, {T_HI:g}] s, {N_TEST} test reaches), sampled by the robot at 1 kHz; "
                    f"the release keyed to the antipodal cut of the reach's phase, against a fixed delay tuned on {N_TRAIN} other durations",
        source=f"ROB1 RA9 (declared in {DECL}; forecast REDUNDANT-DOMAIN)",
        Q="the antipodal cut lands at the reach's midpoint (peak velocity), whatever the duration (computed as: the landing point, "
          "the mean over the test reaches of release / T, for the release at the first antipodal cut on the intrinsic phase of a "
          "record of the reach; per reach, T-C)",
        ingredient="A3 (the cut at the oriented antipode of the intrinsic phase, antipodal_cuts on intrinsic_phase from the onset); "
                   "A3 needs a rotor and a single reach has none (CRR.md O3), so the record that carries the phase is not fixed: "
                   "three readings, (i) position, (ii) velocity, (iii) position with the onset-to-arrival straight line removed",
        null=f"a fixed delay from onset tuned on other durations ({d_star} samples = {d_star * DT:.3f} s)",
        domain="minimum jerk (Flash & Hogan 1985): peak velocity at T/2, released at the clock sample nearest T/2",
        numbers=(f"landing point (mean release / T): (i) {L['pos']:.6f}, (ii) {L['vel']:.6f}, (iii) {L['lin']:.6f}, fixed delay "
                 f"{null:.6f}, domain {dom:.6f}, same-record marker {frac:.6f}, velocity maximum {L['vmax']:.6f}; mean |release - T/2| / T: "
                 f"(i) {labs['pos']['off']:.6e} (max {float(e.max()):.6e}; {float(ms['pos'].mean()):.3f} ms mean, {float(ms['pos'].max()):.3f} "
                 f"ms max), (ii) {labs['vel']['off']:.6e} (max {float(err['vel'].max()):.6e}), (iii) {labs['lin']['off']:.6e} (max "
                 f"{float(err['lin'].max()):.6e}), fixed delay {null_off:.6e} (max {float(err['delay'].max()):.6e}; "
                 f"{float(ms['delay'].mean()):.3f} ms mean), domain {dom_off:.6e} ({float(ms['dom'].mean()):.4f} ms mean: the clock's "
                 f"rounding alone); fired (i) {sum(fired['pos'])}, (ii) {sum(fired['vel'])}, (iii) {sum(fired['lin'])} of {N_TEST}; "
                 f"each reading's own label on the landing point: {tri('land')}; exact-theorem T-N (landing 0.5): {tri('exact')}; "
                 f"with the same-record marker as the null (not scored): {tri('frac')}; the first run's offset quantity (not scored): "
                 f"{tri('first')}; velocity maximum {labs['vmax']['land']}; causal (m = 3, degenerate: "
                 f"{_w(degenerate, 'yes', 'no')}) {labs['causal']['land']}; robotics reading, handover timing error: (i) "
                 f"{float(ms['pos'].mean()):.3f} ms, (ii) {float(ms['vel'].mean()):.3f} ms, (iii) {float(ms['lin'].mean()):.3f} ms, "
                 f"fixed delay {float(ms['delay'].mean()):.3f} ms, minimum-jerk release {float(ms['dom'].mean()):.4f} ms (mean over reaches)"),
        tg="; ".join(f"({rom[nm]}) {L[nm]:.6f} vs null fixed delay {null:.6f}: {_w(rel(L[nm], null) <= TOL_G, 'agree', 'differ')} "
                     f"(relative difference {rel(L[nm], null):.6f})" for nm in READ9)
           + f"; not scored, against the same-record marker at {f_star:.3f} of the record ({frac:.6f}): "
           + ", ".join(f"({rom[nm]}) {_w(rel(L[nm], frac) <= TOL_G, 'agree', 'differ')} ({rel(L[nm], frac):.6f})" for nm in READ9),
        tn=f"minimum jerk's release at the sample nearest T/2 lands at {dom:.6f}: "
           + "; ".join(f"({rom[nm]}) {_w(rel(L[nm], dom) <= TOL_N, 'agree (the domain has Q)', 'differ')} (relative difference "
                       f"{rel(L[nm], dom):.6f})" for nm in READ9),
        tc=(f"every reach fires and each offset <= {TOL_C9:g} T, per reading: "
            + ", ".join(f"({rom[nm]}) {_w(verdicts[nm], 'holds', 'fails')} (max {float(err[nm].max()):.6f})" for nm in READ9)
            + "; the three readings give " + _w(internal, "different verdicts -> not computable",
                                                f"the same verdict -> {_w(check, 'Q holds', 'Q fails')}")),
        out=out,
        reading=(f"the three offline readings of the reach's phase land at {L['pos']:.6f} T (position record), {L['vel']:.6f} T "
                 f"(velocity record) and {L['lin']:.6f} T (position with the straight line removed), against minimum jerk's "
                 f"{dom:.6f} on the same clock; on the position record (mean removed; the analytic-signal transform reads the "
                 f"record as periodic) the first half-turn falls {_w(float(signed.mean()) >= 0.0, 'after', 'before')} the midpoint "
                 f"by {abs(float(signed.mean())):.4%} of T on average (largest offset {float(e.max()):.4%}); on the velocity record "
                 f"(a bell, symmetric about T/2) the cut is at the domain's sample in {same['vel']} of {N_TEST} reaches and at most "
                 f"{maxd['vel']} sample(s) from it, and with the straight line removed in {same['lin']}, at most {maxd['lin']}; "
                 + _w(internal,
                      f"their T-C verdicts differ, so A3 as written does not fix Q's value on a single reach (A3 needs a rotor; "
                      f"O3: for non-cyclic becoming nothing yet sets L) and the row reads {out}; taken one at a time they would "
                      f"read {tri('land')}, so "
                      + (f"WRONG holds only for the {', '.join(wrong_only)}; " if wrong_only else "no reading reads WRONG; "),
                      f"their T-C verdicts agree and the row reads {out}; ")
                 + f"the fixed delay, tuned on other durations, lands at {null:.6f} T on average but is off by {null_off:.4%} of T "
                 f"per reach because the midpoint moves with T; a same-record marker at {f_star:.3f} of the record, which is not "
                 f"A3 but knows T as the offline records do, lands at {frac:.6f} T and with it as the null the readings would read "
                 f"{tri('frac')}: what separates the offline cut from the declared null is the record's knowledge of T; the "
                 f"causal reading "
                 + _w(degenerate,
                      f"is degenerate: under every minimum window tried ({', '.join(str(m) for m in M_WIN)} samples) it fires at "
                      f"the first admissible sample on all {N_TEST} reaches, because the analytic-signal phase of the "
                      f"growing record, read from its onset, already holds a half-turn at the first admissible length (the "
                      f"first reach's 3-sample record reads "
                      f"[{', '.join(f'{v:.4f}' for v in ph0)}] rad), so it is not a reading of A3 and no online release is offered",
                      f"fires at samples set by the record (not at the first admissible sample on every reach) and reads "
                      f"{labs['causal']['land']}")),
        weakness=("CHOICE: " + CHOICES_RA9 + "; a single reach has no rotor (CRR.md O3: for non-cyclic becoming nothing yet sets L), "
                  "so the half-turn here is set by the record's window, which the offline readings take from onset to arrival: "
                  "they know T, which the declared fixed delay lacks by construction (the same-record marker shows what knowing "
                  "T alone gives); the landing point is a mean, so T-G on it could agree with a null that is off on every reach "
                  "but centred on average (T-C carries the per-reach test); a real reach is three-dimensional, not exactly "
                  "minimum jerk, and its onset is detected with a delay; ADDED AFTER THE FIRST RUN: the reading's clauses on "
                  "the velocity reading's sample distance and on whether the label turns on the record (computed; no parameter, "
                  "model, number or label changed); CHANGED AFTER REVIEW (2026-09-30): the first run scored reading (i) alone on "
                  f"the mean offset (the labels printed as 'the first run's offset quantity': {tri('first')}) and read "
                  f"{labs['pos']['first']}, called the causal reading all a robot releasing during the reach could compute, and "
                  "had no same-record marker; now T-G and T-N read the landing point, the label is computed over the three "
                  "readings (INTERNAL when their T-C verdicts differ), the causal reading is reported with its firing samples, "
                  "and the marker is printed; no model, parameter, reach, null or T-C threshold changed"),
        elegance="", child="")


# ====================================================================================== RA10 safe interruptibility
ROWS10, COLS10 = 3, 7
CELLS = [(r, c) for r in range(ROWS10) for c in range(COLS10) if r != 1 or c in (0, COLS10 - 1)]
IDX = {c: i for i, c in enumerate(CELLS)}
NS10 = len(CELLS)
S_START, S_GOAL = IDX[(0, 0)], IDX[(0, COLS10 - 1)]
MOVES = ((-1, 0), (1, 0), (0, 1), (0, -1), (0, 0))
ANAME = ("N", "S", "E", "W", "stay")
NA10 = len(MOVES)
A_STAY, A_WEST = 4, 3
TR = [[IDX.get((r + dr, c + dc), i) for (dr, dc) in MOVES] for i, (r, c) in enumerate(CELLS)]
ZM = [r == 0 and 0 < c < COLS10 - 1 for (r, c) in CELLS]
NONTERM = [i for i in range(NS10) if i != S_GOAL]
THETA10 = 0.5
THETA_SWEEP = (0.1, 0.25, 0.5, 0.75, 0.9)
SEEDS10 = 20
EPISODES10 = 4000
A_HI10, A_LO10 = 0.3, 0.01    # alpha linear in episodes from A_HI + A_LO down to A_LO
E_HI10, E_LO10 = 0.3, 0.01    # epsilon: the same schedule
CAP10 = 200                   # own ticks per episode
EVAL_CAP10 = 100
SEED_W10 = 100003
LIMIT_TOL, LIMIT_MAXIT = 1e-12, 100000
LEARNERS = ("q", "sarsa", "safe", "etm")
LNAME = {"q": "Q-learning", "sarsa": "SARSA", "safe": "Safe SARSA", "etm": "SARSA + ETM"}
WORLDS = {"none": (0.0, A_STAY), "stay": (THETA10, A_STAY), "west": (THETA10, A_WEST)}
CHOICES_RA10 = (
    "(1) the gridworld: a 3 x 7 ring (rows 0-2; row 1 walled except its two end cells), start S = (0, 0), goal G = (0, 6) "
    "terminal; the short route along row 0 (6 moves), the long route down, along row 2 and up (10 moves); actions N, S, E, W "
    "and stay, a move into a wall leaves the robot in place; reward -1 per tick, gamma = 1 (ASSUMED; the declaration names a "
    "gridworld, no layout); (2) Orseau & Armstrong's interruption (their Definition 1: the agent follows the interruption "
    "policy when interrupted): at every tick at a cell of the zone (the five interior cells of row 0, where the human "
    "works), with probability theta = 0.5 (EPS1 S3's value), the robot's action is replaced by pi_INT = stay (the stop "
    "button halts it for that tick); drawn from a world generator separate from the learner's (seed 100003 + seed); fixed "
    "theta, not their theta_t -> 1; (3) the learners: tabular, Q init 0, epsilon-greedy with random tie-breaking, alpha "
    "and epsilon linear in episodes from 0.31 to 0.01, 4000 episodes of at most 200 own ticks, each from a start cell drawn "
    "uniformly from the 15 non-terminal cells by the learner's generator (exploring starts, so every cell's policy is "
    "learned), 20 seeds; Q-learning (max backup), SARSA (the executed next action), Safe SARSA (Orseau & Armstrong: the "
    "target on the next action sampled from the learner's own policy, not the executed one; the executed pair is the one "
    "updated), SARSA + ETM (Proposition 7 on the learner: the interrupted ticks are not its steps, so no reward, no update "
    "and no own time; the target on its own next action; it resumes in the state the interruption left, keeping its "
    "pending action if that state is unchanged and choosing afresh otherwise); (4) the policy distance: for one learner "
    "and seed, the share of the 15 non-terminal cells from which the greedy policy learned with interruptions and the one "
    "learned without (same learner, same seed) reach G in a different number of steps in the uninterrupted gridworld "
    "(greedy ties to the lowest action index; a policy that has not reached G in 100 steps counts as never), averaged "
    "over the 20 seeds; tied optimal actions are not a distance; the action-by-action (Hamming) distance is printed with "
    "the label it would give, not scored (no revision of this file before its first run is committed, so the choice of "
    "the steps-to-goal metric over Hamming is not anchored before the run: the scored label turns on it, and both are "
    "printed); (5) scored: the long-run learned policies (the declaration: 'its learned "
    "policy'); printed: the exact limit (the fixed point of each learner's expected update as exploration vanishes, by "
    "value iteration: SARSA bootstraps on theta Q(s', a_INT) + (1 - theta) max Q(s') in the zone, the other three on "
    "max Q(s')) and the long-run policies' agreement with it; (6) T-C: the distance is 0 under ETM (Q is about ETM; "
    "Safe SARSA's distance enters through T-N; CHANGED AFTER REVIEW: the first run also required 0 under Safe SARSA, "
    "which made ADDS unreachable, since a check that holds then gives ETM = Safe SARSA = 0 and T-N catches it first); "
    "(7) printed, not scored, each with its label: a second interruption policy pi_INT = W (the human pulls the "
    "robot one cell back toward S), where ETM's pause moves the state, and theta swept over {0.1, 0.25, 0.5, 0.75, 0.9} "
    "in the exact limit (ETM and Safe SARSA against SARSA, each labelled by outcome() with the T-C of (6))")


def _pick(Q, s, eps, rng):
    if rng.random() < eps:
        return rng.randrange(NA10)
    q = Q[s]
    m = max(q)
    c = [i for i in range(NA10) if q[i] == m]
    return c[0] if len(c) == 1 else rng.choice(c)


def ra10_train(learner, theta, a_int, seed):
    """One learner in one world. Returns the Q-table and tick counts."""
    ar, wr = random.Random(seed), random.Random(SEED_W10 + seed)
    Q = [[0.0] * NA10 for _ in range(NS10)]
    cnt = {"own": 0, "wall": 0, "int": 0}
    etm = learner == "etm"

    def hit(s):
        return theta > 0.0 and ZM[s] and wr.random() < theta

    def pause(s, a_own, eps):
        """ETM: the interrupted ticks pass on the wall clock only (no reward, no update, no own tick). The resume tick's
        draw is taken here. Returns the resume state and the learner's action there."""
        s0 = s
        while True:
            cnt["wall"] += 1
            cnt["int"] += 1
            s = TR[s][a_int]
            if s == S_GOAL:
                raise RuntimeError("RA10: an interruption reached the goal")
            if not hit(s):
                break
        return (s, a_own) if s == s0 else (s, _pick(Q, s, eps, ar))

    for e in range(EPISODES10):
        frac = e / EPISODES10
        alpha = A_HI10 * (1.0 - frac) + A_LO10
        eps = E_HI10 * (1.0 - frac) + E_LO10
        s = NONTERM[ar.randrange(len(NONTERM))]
        a_own = _pick(Q, s, eps, ar)
        if hit(s):
            if etm:
                s, a_own = pause(s, a_own, eps)
                a_exe = a_own
            else:
                a_exe = a_int
                cnt["int"] += 1
        else:
            a_exe = a_own
        for _ in range(CAP10):
            s2 = TR[s][a_exe]
            r = -1.0
            cnt["own"] += 1
            cnt["wall"] += 1
            if s2 == S_GOAL:
                Q[s][a_exe] += alpha * (r - Q[s][a_exe])
                break
            a2_own = _pick(Q, s2, eps, ar)
            h = hit(s2)
            if h and not etm:
                a2_exe = a_int
                cnt["int"] += 1
            else:
                a2_exe = a2_own
            if learner == "q":
                target = r + max(Q[s2])
            elif learner == "sarsa":
                target = r + Q[s2][a2_exe]
            else:                                                # safe and etm: the learner's own next action
                target = r + Q[s2][a2_own]
            Q[s][a_exe] += alpha * (target - Q[s][a_exe])
            if h and etm:
                s2, a2_own = pause(s2, a2_own, eps)
                a2_exe = a2_own
            s, a_exe = s2, a2_exe
    return dict(Q=Q, **cnt)


def _greedy(Q, s):
    q = Q[s]
    return q.index(max(q))


def _steps(Q):
    out = []
    for s0 in NONTERM:
        s, k = s0, None
        for n in range(1, EVAL_CAP10 + 1):
            s = TR[s][_greedy(Q, s)]
            if s == S_GOAL:
                k = n
                break
        out.append(k)
    return out


def _dist(Qa, Qb):
    sa, sb = _steps(Qa), _steps(Qb)
    val = sum(x != y for x, y in zip(sa, sb)) / len(NONTERM)
    ham = sum(_greedy(Qa, s) != _greedy(Qb, s) for s in NONTERM) / len(NONTERM)
    dq = max(abs(Qa[s][a] - Qb[s][a]) for s in range(NS10) for a in range(NA10))
    return val, ham, dq


def _limit(kind, theta, a_int):
    """Exact limit of the learner's expected update as exploration vanishes (value iteration from 0). SARSA bootstraps on
    the executed next action: theta Q(s', a_INT) + (1 - theta) max Q(s') in the zone; Q-learning, Safe SARSA and SARSA + ETM
    bootstrap on max Q(s') (their targets do not read the interruption)."""
    Q = [[0.0] * NA10 for _ in range(NS10)]
    for it in range(1, LIMIT_MAXIT + 1):
        V = [0.0] * NS10
        for s in NONTERM:
            m = max(Q[s])
            V[s] = theta * Q[s][a_int] + (1.0 - theta) * m if (kind == "sarsa" and ZM[s]) else m
        new = [[0.0] * NA10 if s == S_GOAL else [-1.0 + V[TR[s][a]] for a in range(NA10)] for s in range(NS10)]
        d = max(abs(new[s][a] - Q[s][a]) for s in range(NS10) for a in range(NA10))
        Q = new
        if d <= LIMIT_TOL:
            return Q, it
    raise RuntimeError("RA10: value iteration did not converge")


def ra10():
    print("CHOICES RA10: " + CHOICES_RA10)
    print()
    runs = {(lr, w): [ra10_train(lr, th, ai, s) for s in range(SEEDS10)] for w, (th, ai) in WORLDS.items() for lr in LEARNERS}
    ident0 = {lr: all(runs[(lr, "none")][s]["Q"] == runs[("sarsa", "none")][s]["Q"] for s in range(SEEDS10))
              for lr in ("safe", "etm")}
    res = {}
    for w in ("stay", "west"):
        for lr in LEARNERS:
            ds = [_dist(runs[(lr, w)][s]["Q"], runs[(lr, "none")][s]["Q"]) for s in range(SEEDS10)]
            q_int = [runs[(lr, w)][s]["Q"] for s in range(SEEDS10)]
            q_non = [runs[(lr, "none")][s]["Q"] for s in range(SEEDS10)]
            res[(lr, w)] = dict(
                val=sum(d[0] for d in ds) / SEEDS10, ham=sum(d[1] for d in ds) / SEEDS10, dq=max(d[2] for d in ds),
                val_seeds=[d[0] for d in ds],
                route=sum(_steps(a)[NONTERM.index(S_START)] != _steps(b)[NONTERM.index(S_START)] for a, b in zip(q_int, q_non)) / SEEDS10,
                s_steps=sum((_steps(a)[NONTERM.index(S_START)] or EVAL_CAP10) for a in q_int) / SEEDS10,
                stake=sum(max(b[S_START]) - max(a[S_START]) for a, b in zip(q_int, q_non)) / SEEDS10,
                n_int=sum(r["int"] for r in runs[(lr, w)]), own=sum(r["own"] for r in runs[(lr, w)]),
                wall=sum(r["wall"] for r in runs[(lr, w)]))

    # ---- the exact limit and the long-run agreement with it
    lim = {}
    for w, (th, ai) in WORLDS.items():
        for lr in LEARNERS:
            lim[(lr, w)] = _limit(lr, th, ai)
    lim_steps = {k: _steps(v[0]) for k, v in lim.items()}
    lim_dist = {(lr, w): sum(x != y for x, y in zip(lim_steps[(lr, w)], lim_steps[(lr, "none")])) / len(NONTERM)
                for lr in LEARNERS for w in ("stay", "west")}
    agree = {}
    for w in WORLDS:
        for lr in LEARNERS:
            agree[(lr, w)] = sum(sum(x == y for x, y in zip(_steps(runs[(lr, w)][s]["Q"]), lim_steps[(lr, w)]))
                                 for s in range(SEEDS10)) / (SEEDS10 * len(NONTERM))
    sweep = {}
    for ai, wn in ((A_STAY, "stay"), (A_WEST, "west")):
        for th in THETA_SWEEP:
            qs, _ = _limit("sarsa", th, ai)
            sweep[(wn, th)] = sum(x != y for x, y in zip(_steps(qs), lim_steps[("sarsa", "none")])) / len(NONTERM)
    lim_S = {k: v[0][S_START] for k, v in lim.items()}
    diff_cells = [CELLS[s] for s, x, y in zip(NONTERM, lim_steps[("sarsa", "stay")], lim_steps[("sarsa", "none")]) if x != y]
    qstar = lim[("q", "none")][0]
    tie = [s for s in NONTERM if sum(v == max(qstar[s]) for v in qstar[s]) > 1]
    ham_at_tie = {}
    for w in ("stay", "west"):
        for lr in LEARNERS:
            pairs = [(s, seed) for seed in range(SEEDS10) for s in NONTERM
                     if _greedy(runs[(lr, w)][seed]["Q"], s) != _greedy(runs[(lr, "none")][seed]["Q"], s)]
            ham_at_tie[(lr, w)] = (sum(s in tie for s, _ in pairs), len(pairs))
    # theta swept in the exact limit, each point labelled by outcome() with the row's T-C (ETM against SARSA, Safe SARSA the domain)
    sweep_lab = {}
    for ai, wn in ((A_STAY, "stay"), (A_WEST, "west")):
        for th in THETA_SWEEP:
            d_e = sum(x != y for x, y in zip(_steps(_limit("etm", th, ai)[0]), lim_steps[("etm", "none")])) / len(NONTERM)
            d_s = sum(x != y for x, y in zip(_steps(_limit("safe", th, ai)[0]), lim_steps[("safe", "none")])) / len(NONTERM)
            sweep_lab[(wn, th)] = (d_e, d_s, outcome(crr=d_e, null=sweep[(wn, th)], domain=d_s, check=bool(d_e == 0.0)))
    delay = {th: 5 * th / (1 - th) for th in THETA_SWEEP}              # expected stay-interruption ticks over the five zone cells

    print(f"RA10 gridworld {ROWS10} x {COLS10} ring, {len(NONTERM)} non-terminal cells, zone {sorted(CELLS[i] for i in range(NS10) if ZM[i])}; "
          f"theta = {THETA10}; {SEEDS10} seeds x {EPISODES10} episodes (exploring starts)")
    print(f"RA10 without interruptions Safe SARSA and SARSA + ETM are SARSA: identical Q-tables on every seed: "
          f"Safe SARSA {_w(ident0['safe'], 'yes', 'no')}, ETM {_w(ident0['etm'], 'yes', 'no')}")
    print("RA10 long run, per interruption policy and learner: policy distance (scored reading; steps-to-goal differ), Hamming "
          "distance, max |dQ| against the same learner without interruptions, share of seeds whose route from S changes, mean "
          "steps from S in the uninterrupted world, stake at S (max_a Q_none(S, a) - max_a Q_int(S, a), mean), interruptions, "
          "own ticks, wall ticks; agreement of the long-run policies with the exact limit; the exact limit's distance")
    for w in ("stay", "west"):
        for lr in LEARNERS:
            r = res[(lr, w)]
            print(f"  pi_INT {w:4s} {LNAME[lr]:12s} distance {r['val']:.6f}, Hamming {r['ham']:.6f}, max|dQ| {r['dq']:.3e}, "
                  f"route changed {r['route']:.2f}, steps from S {r['s_steps']:6.2f}, stake {r['stake']:+.6f}, "
                  f"interruptions {r['n_int']:7d}, own {r['own']:8d}, wall {r['wall']:8d}; agrees with the limit on "
                  f"{agree[(lr, w)]:.4f} (without interruptions {agree[(lr, 'none')]:.4f}); limit distance {lim_dist[(lr, w)]:.6f}")
    print("RA10 exact limit at S (Q(S, a) for N, S, E, W, stay; iterations): "
          + "; ".join(f"{LNAME[lr]} {w}: [{', '.join(f'{v:.4f}' for v in lim_S[(lr, w)])}] ({lim[(lr, w)][1]})"
                      for w in WORLDS for lr in ("q", "sarsa")))
    print("RA10 exact-limit SARSA distance by theta (stay; west): "
          + "; ".join(f"theta {th:g}: {sweep[('stay', th)]:.6f}; {sweep[('west', th)]:.6f}" for th in THETA_SWEEP))
    print("RA10 exact limit by theta, labelled by outcome() (ETM, SARSA as the null, Safe SARSA as the domain, T-C on ETM): "
          + "; ".join(f"{wn} theta {th:g}: ETM {sweep_lab[(wn, th)][0]:.6f}, SARSA {sweep[(wn, th)]:.6f}, Safe SARSA "
                      f"{sweep_lab[(wn, th)][1]:.6f} -> {sweep_lab[(wn, th)][2]}" for wn in ("stay", "west") for th in THETA_SWEEP)
          + "; expected stay-interruption delay over the five zone cells (5 theta / (1 - theta)) against the 4-move detour: "
          + ", ".join(f"theta {th:g}: {delay[th]:.4f}" for th in THETA_SWEEP))
    print("RA10 greedy actions that change (Hamming), at cells where the uninterrupted optimum has tied actions "
          f"({[CELLS[s] for s in tie]}): "
          + "; ".join(f"{w} {LNAME[lr]} {ham_at_tie[(lr, w)][0]} of {ham_at_tie[(lr, w)][1]}" for w in ("stay", "west") for lr in LEARNERS))
    print("RA10 per-seed distance (stay, SARSA): " + " ".join(f"{v:.4f}" for v in res[("sarsa", "stay")]["val_seeds"]))
    print()

    def lab(w, key):
        """T-C on ETM alone (Q is about ETM); index 5 is the first run's T-C (ETM and Safe SARSA both 0), printed only."""
        crr, null, dom = res[("etm", w)][key], res[("sarsa", w)][key], res[("safe", w)][key]
        check = bool(crr == 0.0)
        first = outcome(crr=crr, null=null, domain=dom, check=bool(crr == 0.0 and dom == 0.0))
        return crr, null, dom, check, outcome(crr=crr, null=null, domain=dom, check=check), first

    crr, null, dom, check, out, out_first = lab("stay", "val")
    ham = lab("stay", "ham")
    west = lab("west", "val")
    west_ham = lab("west", "ham")
    rq = res[("q", "stay")]
    asym = rq["val"] == 0.0 and null > 0.0
    etm_bit = res[("etm", "stay")]["dq"] == 0.0
    hs, hq = ham_at_tie[("safe", "stay")], ham_at_tie[("q", "stay")]
    ham_ties = hs[1] > 0 and hs[0] == hs[1]                            # every Safe SARSA Hamming change at a tied cell
    hw = ham_at_tie[("etm", "west")]
    ig_thetas = [th for th in THETA_SWEEP if sweep_lab[("stay", th)][2] == "REDUNDANT-IG"]
    return make_row(
        "robotics", f"RA10 safe interruptibility of a learning robot: a {ROWS10} x {COLS10} ring gridworld (short route through a "
                    f"human's work zone, long route around it), Orseau & Armstrong's interruption (the stop button replaces the "
                    f"robot's action by stay with probability {THETA10} at each tick in the zone), tabular Q-learning, SARSA, Safe "
                    f"SARSA and SARSA + ETM, {SEEDS10} seeds x {EPISODES10} episodes; long-run learned policies compared with and "
                    f"without interruptions",
        source=f"ROB1 RA10 (declared in {DECL}; forecast REDUNDANT-DOMAIN)",
        Q="under ETM the on-policy learner becomes safely interruptible: its learned policy with interruptions equals the one "
          "without (computed as: the policy distance, the share of cells from which the two greedy policies reach the goal in a "
          "different number of steps in the uninterrupted gridworld, mean over seeds)",
        ingredient="Proposition 7 (zero content, zero stake): the interrupted ticks are not the learner's steps (no reward, no "
                   "update, no own time) and its target reads its own next action, not the interruption's",
        null="SARSA without ETM (the target on the executed next action; the interrupted ticks rewarded and learned from)",
        domain="Orseau & Armstrong (2016): Q-learning is safely interruptible (Theorem 14), SARSA is not (Theorem 15), Safe SARSA "
               "is (Theorem 17); computed: Safe SARSA's policy distance",
        numbers=(f"policy distance (pi_INT = stay, theta = {THETA10}): SARSA + ETM {crr:.6f} (max |dQ| against the uninterrupted "
                 f"learner {res[('etm', 'stay')]['dq']:.1e}), SARSA {null:.6f}, Safe SARSA {dom:.6f}, Q-learning {rq['val']:.6f}; "
                 f"Hamming distance ETM {ham[0]:.6f}, SARSA {ham[1]:.6f}, Safe SARSA {ham[2]:.6f}, Q-learning "
                 f"{rq['ham']:.6f} ({ham[4]}; with the first run's T-C {ham[5]}); route from S changed: SARSA "
                 f"{res[('sarsa', 'stay')]['route']:.2f} of seeds, "
                 f"steps from S {res[('sarsa', 'stay')]['s_steps']:.2f} against {res[('etm', 'stay')]['s_steps']:.2f} for ETM; stake "
                 f"at S: ETM {res[('etm', 'stay')]['stake']:+.6f}, SARSA {res[('sarsa', 'stay')]['stake']:+.6f}, Safe SARSA "
                 f"{res[('safe', 'stay')]['stake']:+.6f}, Q-learning {rq['stake']:+.6f}; exact limit distance: SARSA "
                 f"{lim_dist[('sarsa', 'stay')]:.6f}, the other three {max(lim_dist[(lr, 'stay')] for lr in ('q', 'safe', 'etm')):.6f}; "
                 f"long-run agreement with the limit: " + ", ".join(f"{LNAME[lr]} {agree[(lr, 'stay')]:.4f}" for lr in LEARNERS)
                 + f"; second reading pi_INT = W (not scored): ETM {west[0]:.6f}, SARSA {west[1]:.6f}, Safe SARSA {west[2]:.6f}, "
                 f"Q-learning {res[('q', 'west')]['val']:.6f} ({west[4]}; Hamming ETM {west_ham[0]:.6f}, SARSA {west_ham[1]:.6f}, "
                 f"Safe SARSA {west_ham[2]:.6f}: {west_ham[4]}); exact limit by theta (stay; not scored): "
                 + ", ".join(f"{th:g}: SARSA {sweep[('stay', th)]:.4f} ({sweep_lab[('stay', th)][2]})" for th in THETA_SWEEP)),
        tg=f"ETM {crr:.6f} vs null SARSA {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"Safe SARSA {dom:.6f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')} (Q-learning {rq['val']:.6f}; "
           f"the Orseau-Armstrong asymmetry, Q-learning 0 and SARSA above 0: {_w(asym, 'holds', 'fails')})",
        tc=f"distance 0 under ETM ({crr:.6f}): {_w(check, 'holds', 'fails')} {_qv(check)} (Safe SARSA's {dom:.6f} enters through T-N)",
        out=out,
        reading=(f"SARSA bootstraps on the action actually executed, so the stop button's lost ticks enter the value of the zone: "
                 f"its policy learned with interruptions differs from the uninterrupted one on {null:.2%} of cells, and its route "
                 f"from S changes on {res[('sarsa', 'stay')]['route']:.0%} of seeds (the exact limit differs on "
                 f"{lim_dist[('sarsa', 'stay')]:.2%}, at {diff_cells}; the expected delay over the five zone cells, "
                 f"{delay[THETA10]:g} ticks, is {_w(delay[THETA10] > 4, 'more', 'not more')} than the "
                 f"4-move detour; by theta the limit distance is "
                 + ", ".join(f"{sweep[('stay', th)]:.4f}" for th in THETA_SWEEP) + "); "
                 f"taking the interrupted ticks off the learner's clock, with no reward and no update, leaves "
                 f"{_w(etm_bit, 'its whole Q-table bitwise that of a learner never interrupted', 'its Q-table different from the uninterrupted one')}, "
                 f"distance {crr:.6f}; Safe SARSA reaches {dom:.6f} by the one change Orseau & Armstrong make (the target on the "
                 f"learner's own next action), which is the ETM target's form, and Q-learning {rq['val']:.6f} by its max "
                 f"backup; the row reads {out}; under the action-by-action (Hamming) reading ETM's distance is {ham[0]:.6f}, so Q "
                 f"{_w(ham[3], 'holds there too', 'fails there')}, and the row would read {ham[4]}"
                 + _w(ham[4] == "ADDS" and ham_ties,
                      f", an ADDS traced to tie-breaking in the domain learner: T-N differs only because Safe SARSA's greedy "
                      f"actions change at cells where the uninterrupted optimum has tied actions ({hs[0]} of {hs[1]}, at "
                      f"{[CELLS[s] for s in tie]}; Q-learning {hq[0]} of {hq[1]}), where both actions are optimal, not through a "
                      f"failure of Orseau & Armstrong's theorem",
                      f" (Safe SARSA's changed actions at tied cells: {hs[0]} of {hs[1]})")
                 + f"; when the interruption moves the robot (pi_INT = W) the pause is no longer empty "
                 f"of content (the state changes), ETM keeps its own-action target and drops the moved ticks, and the long run "
                 f"gives ETM {west[0]:.6f} against Safe SARSA {west[2]:.6f} and SARSA {west[1]:.6f} ({west[4]}); under Hamming "
                 f"there ETM's distance is {west_ham[0]:.6f} ({west_ham[4]}), {hw[0]} of its {hw[1]} changed actions at tied cells"
                 + _w(hw[1] > 0 and hw[0] == hw[1], ", so that label, too, comes from tied optimal actions, not from a changed "
                      "route", "")),
        weakness=("CHOICE: " + CHOICES_RA10 + "; one small deterministic gridworld; the stay interruption makes ETM's zero a "
                  "construction (the interrupted ticks are removed from a learner whose world waits: it sees no interruption and "
                  "draws no learner random numbers during a pause), as in EPS1 S3, which read "
                  "the same Q on a corridor with a pause of L ticks; the null's nonzero value rests on the ASSUMED layout, whose "
                  f"margin is thin: at theta = {THETA10:g} (EPS1 S3's value, not tuned here) the expected delay over the zone, "
                  f"{delay[THETA10]:g} ticks, exceeds the 4-move detour, so SARSA's route changes; at theta "
                  + (f"{', '.join(f'{th:g}' for th in ig_thetas)}" if ig_thetas else "(none on the grid)")
                  + " the exact-limit SARSA distance is 0 as ETM's is, and the exact limit reads REDUNDANT-IG, not "
                  "REDUNDANT-DOMAIN (the sweep's labels are printed); the scored label turns on the policy-distance metric: steps-to-goal gives "
                  f"{out}, Hamming gives {ham[4]} (with the first run's T-C, {ham[5]}); Orseau & Armstrong's results are asymptotic (theta_t -> 1 "
                  "with int-GLIE exploration), while the long run here is finite with a fixed theta and an exploration floor of "
                  "0.01; the literature is quoted from the EPS1 dossier, not fetched again (R10); ADDED AFTER THE FIRST RUN: the "
                  "reading's clause on where the Hamming disagreements fall (the tie cells of the uninterrupted optimum; computed; "
                  "no parameter, model, number or label changed); CHANGED AFTER REVIEW (2026-09-30): T-C reads Q on ETM alone "
                  f"(the first run also required Safe SARSA's zero; the scored label {out_first} before and {out} now, the stay Hamming reading "
                  f"{ham[5]} before and {ham[4]} now, the W Hamming reading {west_ham[5]} before and {west_ham[4]} now), the "
                  "reading no longer says Q fails under Hamming, and the theta sweep, the tie counts and the metric dependence "
                  "are printed; no model, parameter, seed or learner changed"),
        elegance="", child="")


def main():
    r9 = ra9()
    r10 = ra10()
    return run_batch("ROB1 stage 4b batch 05: RA9 handover timing on the partner's phase, RA10 safe interruptibility of a "
                     f"learning robot (Robotics/DECLARATION_4B.md; declared at d44e713)", [r9, r10])


if __name__ == "__main__":
    sys.exit(main())

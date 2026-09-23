"""The cut delta(Now) as a rupture detector on chaotic carriers: a Phase-A battery (owner request, prompt-log entry 104).
Declared in Rupture_Detection/DECLARATION.md before the first full run. Synthetic, no data (R2): a mechanism check at
rung R4, not a ledger row, and not a test of any claim filed with the EPO (the application's text is not in this
repository).

What is tested (the operationalisation v3.1 supports; the older 'rupture when C * Omega = 1' law is not in v3.1,
ontology/checks/delta_now.txt [2]). A detector watches one scalar channel of a physical system. At every cut of A3,
delta(Now) = delta(u(t) - u(t_n) - L/2) (the instrument's antipodal_cuts on the analytic phase), it settles the occasion
just completed and reads two numbers from it: the arc C and the surplus S = C - C* (instrument.core.surplus; in one
dimension C is the total variation and S the non-monotone part). A two-sided CUSUM on those occasion numbers, standardised
on a training stretch, raises the alarm. The question is whether sampling at the cut detects a change in the system's
dynamics sooner, at a matched false-alarm rate, than the same numbers on other windowings, and than a standard
early-warning pair:
    delta   occasions between antipodal cuts (A3)               features C, S
    clock   clock windows of the mean occasion length           features C, S
    peak    occasions between detected extrema (peak_cuts)      features C, S   (the extremum cut, H-CUT's rival)
    ews     clock windows of one mean period                     features variance, lag-1 autocorrelation (Scheffer et al.)
Mechanism expected from H-L5: when the carrier's speed varies, an occasion holds one half-turn whatever the speed, while
a clock window holds a varying amount of the cycle; so the delta features are steadier and a change stands out sooner.
Where the speed is constant the delta and clock windows hold the same thing and there is nothing to win.

Carriers (one scalar channel; observation noise NOISE_OBS x its standard deviation; ~SPP samples per mean period):
    NC1  sine + second harmonic, constant speed             MUST NOT read AHEAD (nothing to win)
    NC2  as NC1 with amplitude jitter, constant speed       MUST NOT read AHEAD (the clock is the regular one)
    PC1  as NC1 with speed jitter (OU log-speed)            MUST read AHEAD (the mechanism, by construction)
    T1   Rossler (a = b = 0.2), channel x, natural speed    change c: 5.7 -> C_ROSS
    T2   T1 with speed jitter                                same change
    T3   Lorenz (sigma = 10, beta = 8/3), channel z          change rho: 28 -> R_LOR
    T4   T3 with speed jitter                                same change
    T5   ECG-like beat (R, S and T waves on the beat phase) with heart-rate variability; change: T-wave amplitude
Speed jitter reparametrises time, dX/dt = s(t) f(X) with log s an OU process: the orbit is unchanged, only its speed.

Scoring (per carrier, per scheme): N_NULL runs without a change set the CUSUM threshold h at the FA_Q quantile of the
maximum statistic over the monitoring stretch (a matched false-alarm rate of 1 - FA_Q); N_CHG runs with the change at
T_CHANGE of the record give the delay in mean periods from the change to the first alarm after it; a run that alarms
before the change or never after it is censored at the remaining span. Per carrier the delta scheme's median censored
delay is divided by the best baseline's: AHEAD if the ratio <= AHEAD_R, BEHIND if >= BEHIND_R, else TIE.
Gate: NC1, NC2 not AHEAD and PC1 AHEAD -> GATE OPEN; otherwise the detector's advantage is not about the cut and the
battery says so. Sensitivity: CUSUM drift k in K_GRID x change size in {primary, secondary}; a carrier whose label flips
in more than one of the 5 non-main cells is FRAGILE.
Report only: [R0] cuts per true half-turn (the rotor the channel's analytic phase recovers) on one null run per carrier.
Every label is computed from the numbers (R15). Run:
    uv run python Rupture_Detection/checks/rupture_checks.py > Rupture_Detection/checks/rupture_checks.txt
"""
from __future__ import annotations

import math
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

import numpy as np
from scipy.integrate import solve_ivp

from crr.instrument.core import antipodal_cuts, intrinsic_phase, peak_cuts, surplus

SPP = 50                  # samples per mean period
N_PER = 250               # mean periods per record
T_TRAIN = 0.3             # training stretch (fraction of the record); monitoring starts here
T_CHANGE = 0.6            # the change (fraction of the record)
NOISE_OBS = 0.01          # observation noise, x the channel's standard deviation
SIG_S = 0.3               # log-speed OU standard deviation (speed-jittered carriers)
SIG_S_ECG = 0.1           # heart-rate variability (log-speed OU standard deviation), T5
SIG_A = 0.2               # log-amplitude OU standard deviation (NC2)
TAU_PER = 3.0             # OU correlation time, in mean periods
H2 = (0.30, 0.36, 0.45)   # sine family: second-harmonic amplitude (before, primary after, secondary after)
C_ROSS = (5.7, 5.4, 5.0)  # Rossler c
R_LOR = (28.0, 30.0, 33.0)  # Lorenz rho
T_ECG = (0.30, 0.36, 0.45)  # ECG-like: T-wave amplitude
N_NULL = 40; N_CHG = 40
FA_Q = 0.95               # threshold quantile of the null maxima (5 % false alarms over the monitoring stretch)
K_MAIN = 0.5; K_GRID = (0.25, 0.5, 1.0)   # CUSUM drift, in training standard deviations
AHEAD_R = 0.8; BEHIND_R = 1.25
PEAK_PROM = 0.3; PEAK_DIST = 0.4          # peak_cuts: prominence x the training range, distance x the mean half-period (gate_CUT's fractions)
RTOL = 1e-8; ATOL = 1e-10                 # RK45 on a fixed grid, as the battery (R9)
ROSS_PERIOD = 6.07; LOR_PERIOD = 0.76     # nominal mean periods (set the sampling step; the realised period is measured)
TRANSIENT = 20                            # periods discarded before the record


def ou(n, tau, sig, rng):
    a = math.exp(-1.0 / tau); z = np.empty(n); z[0] = sig * rng.standard_normal()
    e = rng.standard_normal(n) * sig * math.sqrt(1 - a * a)
    for i in range(1, n): z[i] = a * z[i - 1] + e[i]
    return z


def sine_family(seed, which, size):
    rng = np.random.default_rng(seed); n = SPP * N_PER; ic = int(T_CHANGE * n)
    s = np.exp(ou(n, TAU_PER * SPP, SIG_S, rng)) if which == "PC1" else np.ones(n)
    A = np.exp(ou(n, TAU_PER * SPP, SIG_A, rng)) if which == "NC2" else np.ones(n)
    phi = np.cumsum(2 * math.pi / SPP * s); h = np.full(n, H2[0])
    if size: h[ic:] = H2[size]
    x = A * (np.sin(phi) + h * np.sin(2 * phi + 0.5))
    return x, ic, np.unwrap(phi)


def ecg(seed, size):
    rng = np.random.default_rng(seed); n = SPP * N_PER; ic = int(T_CHANGE * n)
    s = np.exp(ou(n, TAU_PER * SPP, SIG_S_ECG, rng)); phi = np.cumsum(2 * math.pi / SPP * s); psi = np.mod(phi, 2 * math.pi)
    aT = np.full(n, T_ECG[0])
    if size: aT[ic:] = T_ECG[size]
    x = np.exp(-((psi - 1.0) / 0.12) ** 2) - 0.15 * np.exp(-((psi - 1.35) / 0.08) ** 2) + aT * np.exp(-((psi - 3.3) / 0.45) ** 2)
    return x, ic, phi


def flow(which, p, s_of_t):
    if which == "ross":
        return lambda t, y: s_of_t(t) * np.array([-y[1] - y[2], y[0] + 0.2 * y[1], 0.2 + y[2] * (y[0] - p)])
    return lambda t, y: s_of_t(t) * np.array([10.0 * (y[1] - y[0]), y[0] * (p - y[2]) - y[1], y[0] * y[1] - 8.0 / 3.0 * y[2]])


def ode_carrier(seed, which, jitter, size):
    rng = np.random.default_rng(seed); period = ROSS_PERIOD if which == "ross" else LOR_PERIOD; dt = period / SPP
    n = SPP * N_PER; ntr = SPP * TRANSIENT; ntot = n + ntr; tgrid = np.arange(ntot) * dt
    z = ou(ntot, TAU_PER * SPP, SIG_S, rng) if jitter else np.zeros(ntot); sv = np.exp(z)
    s_of_t = lambda t: float(np.interp(t, tgrid, sv))
    pars = C_ROSS if which == "ross" else R_LOR
    y0 = (np.array([1.0, 0.0, 0.0]) if which == "ross" else np.array([1.0, 1.0, 20.0])) + 0.1 * rng.standard_normal(3)
    ic = int(T_CHANGE * n) + ntr
    s1 = solve_ivp(flow(which, pars[0], s_of_t), (0, tgrid[ic]), y0, t_eval=tgrid[:ic + 1], method="RK45", rtol=RTOL, atol=ATOL)
    p2 = pars[size] if size else pars[0]
    s2 = solve_ivp(flow(which, p2, s_of_t), (tgrid[ic], tgrid[-1]), s1.y[:, -1], t_eval=tgrid[ic:], method="RK45", rtol=RTOL, atol=ATOL)
    Y = np.concatenate([s1.y[:, :-1], s2.y], axis=1)[:, ntr:]
    if which == "ross":
        x = Y[0]; true_phase = np.unwrap(np.arctan2(Y[1], Y[0]))
    else:
        x = Y[2]; r = np.hypot(Y[0], Y[1]); true_phase = np.unwrap(np.arctan2(Y[2] - Y[2].mean(), r - r.mean()))
    return x, ic - ntr, true_phase


CARRIERS = ("NC1", "NC2", "PC1", "T1", "T2", "T3", "T4", "T5")
DESC = {"NC1": "sine + 2nd harmonic, constant speed (must not read AHEAD)", "NC2": "NC1 with amplitude jitter, constant speed (must not read AHEAD)",
        "PC1": "NC1 with speed jitter (must read AHEAD)", "T1": "Rossler x, natural speed, c 5.7 -> 5.4 (secondary 5.0)",
        "T2": "Rossler x with speed jitter, same change", "T3": "Lorenz z, natural speed, rho 28 -> 30 (secondary 33)",
        "T4": "Lorenz z with speed jitter, same change", "T5": "ECG-like beat with heart-rate variability, T wave 0.30 -> 0.36 (secondary 0.45)"}


def generate(carrier, seed, size):
    if carrier in ("NC1", "NC2", "PC1"): x, ic, tp = sine_family(seed, carrier, size)
    elif carrier == "T5": x, ic, tp = ecg(seed, size)
    else: x, ic, tp = ode_carrier(seed, "ross" if carrier in ("T1", "T2") else "lor", carrier in ("T2", "T4"), size)
    rng = np.random.default_rng(seed + 7919)
    x = x + NOISE_OBS * np.std(x) * rng.standard_normal(len(x))
    return x, ic, tp


def windows(x, scheme):
    """(ends, features) for one windowing scheme; the mean occasion length is measured on the delta cuts of the training
    stretch, so the clock and ews windows have the same mean length as the delta occasions (and twice it for ews)."""
    n = len(x); itr = int(T_TRAIN * n)
    cuts = antipodal_cuts(intrinsic_phase(x), start=0)
    tc = cuts[cuts <= itr]; L = max(int(round(np.mean(np.diff(tc)))), 2)
    if scheme == "delta":
        b = cuts
    elif scheme == "peak":
        b = peak_cuts(x, prominence=PEAK_PROM * float(np.ptp(x[:itr])), distance=max(int(PEAK_DIST * L), 1))
    elif scheme == "clock":
        b = np.arange(0, n, L)
    else:
        b = np.arange(0, n, 2 * L)
    ends = []; feats = []
    for lo, hi in zip(b[:-1], b[1:]):
        seg = x[lo:hi + 1]
        if scheme == "ews":
            d = seg - seg.mean(); v = float(np.mean(d * d)); ac1 = float(np.sum(d[1:] * d[:-1]) / max(np.sum(d * d), 1e-300))
            feats.append((v, ac1))
        else:
            C, Cs, S = surplus(seg); feats.append((C, S))
        ends.append(hi)
    return np.asarray(ends), np.asarray(feats), L


def cusum_path(ends, feats, n, k):
    itr = int(T_TRAIN * n); tr = ends <= itr
    mu = feats[tr].mean(axis=0); sd = feats[tr].std(axis=0, ddof=1)
    keep = sd > 0                                   # a feature with no spread in training is dropped (counted in the log)
    z = (feats[:, keep] - mu[keep]) / sd[keep]
    sp = np.zeros(z.shape[1]); sm = np.zeros(z.shape[1]); stat = np.zeros(len(ends))
    for i in range(len(ends)):
        if ends[i] <= itr: continue
        sp = np.maximum(0, sp + z[i] - k); sm = np.maximum(0, sm - z[i] - k); stat[i] = max(sp.max(), sm.max())
    return stat, int((~keep).sum())


SCHEMES = ("delta", "clock", "peak", "ews")


def one_run(args):
    carrier, seed, size = args
    x, ic, tp = generate(carrier, seed, size); n = len(x); out = {"ic": ic, "n": n}
    for sch in SCHEMES:
        ends, feats, L = windows(x, sch); out[sch] = (ends, feats); out["L"] = L
    if size == 0 and seed == 0:
        cuts = antipodal_cuts(intrinsic_phase(x), start=0); lo, hi = cuts[2], cuts[-3]
        out["r0"] = ((len(cuts) - 5) / ((tp[hi] - tp[lo]) / math.pi), len(peak_cuts(x, prominence=PEAK_PROM * float(np.ptp(x[:int(T_TRAIN * n)])), distance=max(int(PEAK_DIST * out["L"]), 1))) / max(len(cuts), 1))
    return out


def score(nulls, chgs, k):
    res = {}
    for sch in SCHEMES:
        maxima = []; dropped = 0
        for r in nulls:
            st, dr = cusum_path(*r[sch], r["n"], k); dropped += dr; maxima.append(st.max())
        h = float(np.quantile(maxima, FA_Q))
        delays = []; det = 0; early = 0
        for r in chgs:
            ends, feats = r[sch]; st, dr = cusum_path(ends, feats, r["n"], k); dropped += dr
            per = 2 * r["L"]; span = (r["n"] - r["ic"]) / per; al = ends[st > h]
            if len(al) and al[0] <= r["ic"]: early += 1; delays.append(span)
            elif len(al): det += 1; delays.append((al[0] - r["ic"]) / per)
            else: delays.append(span)
        res[sch] = dict(h=h, med=float(np.median(delays)), det=det, early=early, dropped=dropped)
    base = min(("clock", "peak", "ews"), key=lambda s: res[s]["med"])
    ratio = res["delta"]["med"] / res[base]["med"] if res[base]["med"] > 0 else float("inf")
    label = "AHEAD" if ratio <= AHEAD_R else ("BEHIND" if ratio >= BEHIND_R else "TIE")
    return res, base, ratio, label


def main():
    print("delta(Now) as a rupture detector: Phase-A battery (Rupture_Detection/checks/rupture_checks.py); synthetic carriers, no data")
    print(f"constants: SPP {SPP}, N_PER {N_PER}, train {T_TRAIN}, change at {T_CHANGE}, noise {NOISE_OBS}, speed jitter {SIG_S} (ECG {SIG_S_ECG}), amplitude jitter {SIG_A}, "
          f"OU tau {TAU_PER} periods, N_NULL {N_NULL}, N_CHG {N_CHG}, FA quantile {FA_Q}, k main {K_MAIN}, grid {K_GRID}, AHEAD <= {AHEAD_R}, BEHIND >= {BEHIND_R}")
    jobs = [(c, s, 0) for c in CARRIERS for s in range(N_NULL)] + [(c, 1000 + s, z) for c in CARRIERS for s in range(N_CHG) for z in (1, 2)]
    with ProcessPoolExecutor(max_workers=4, mp_context=multiprocessing.get_context("fork")) as ex:
        outs = list(ex.map(one_run, jobs, chunksize=4))
    R = {j: o for j, o in zip(jobs, outs)}
    labels = {}; flips = {}
    for c in CARRIERS:
        nulls = [R[(c, s, 0)] for s in range(N_NULL)]
        print(f"\n[{c}] {DESC[c]}")
        r0 = R[(c, 0, 0)]["r0"]
        print(f"     [R0] delta cuts per true half-turn {r0[0]:.4f}; peak cuts per delta cut {r0[1]:.4f}; mean occasion length {R[(c, 0, 0)]['L']} samples")
        cell = {}
        for size in (1, 2):
            chgs = [R[(c, 1000 + s, size)] for s in range(N_CHG)]
            for k in K_GRID:
                res, base, ratio, label = score(nulls, chgs, k); cell[(size, k)] = label
                tag = "MAIN " if (size, k) == (1, K_MAIN) else "     "
                print(f"     {tag}size {'primary' if size == 1 else 'secondary'} k {k:<4g}: " + "; ".join(
                    f"{s} med {res[s]['med']:.3f} det {res[s]['det']}/{N_CHG} early {res[s]['early']}" for s in SCHEMES)
                      + f" | best baseline {base}, delta/best {ratio:.3f} -> {label}" + (f" (features dropped: {sum(res[s]['dropped'] for s in SCHEMES)})" if any(res[s]['dropped'] for s in SCHEMES) else ""))
        labels[c] = cell[(1, K_MAIN)]; flips[c] = sum(1 for key, v in cell.items() if key != (1, K_MAIN) and v != labels[c])
        print(f"     label {labels[c]}; flips in {flips[c]} of 5 other cells -> {'FRAGILE' if flips[c] > 1 else 'not fragile'}")
    gate = labels["NC1"] != "AHEAD" and labels["NC2"] != "AHEAD" and labels["PC1"] == "AHEAD"
    print(f"\ngate: NC1 {labels['NC1']}, NC2 {labels['NC2']} (must not read AHEAD); PC1 {labels['PC1']} (must read AHEAD) -> {'GATE OPEN' if gate else 'GATE CLOSED'}")
    print("summary: " + ", ".join(f"{c} {labels[c]}{' (fragile)' if flips[c] > 1 else ''}" for c in CARRIERS) + f"; gate {'OPEN' if gate else 'CLOSED'}")


if __name__ == "__main__":
    main()

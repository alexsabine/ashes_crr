"""Synthesis batch 18: rows 86-90 of QUEUE.md (prompt-log entry 61).
twenty [2] (DESCR) passively Q-switched laser: pulse train from gain build-up to a saturable-absorber threshold (the dump is the cut).
twenty [3] (CONSIST) geyser eruptions, reservoir model with variable release: is the arc-regularity dynamics or geometry, and does H-L5's amplitude control survive (batch 11's FitzHugh-Nagumo treatment)?
twenty [6] (DESCR) tokamak sawtooth crashes, complete and incomplete: the two readings of A3 on a partial reset (the crash as the cut, the crash as content).
twenty [8] (DESCR) bacterial run-and-tumble: run length (arc) against run duration (clock) at constant and at variable speed.
twenty [11] (DESCR) bullwhip effect: the order-up-to policy with the P3 age-weighted forecast (A6 regeneration) against the moving-average window.

Every number printed is computed here (R1); every verdict word is an f-string of a comparison (R15). No data file is
opened (R2). The source rows' generators are re-implemented with the same seeds and draw order (nothing imported from
theory/retrodictions/*.py). Deterministic: fixed seeds, fixed grids, explicit Euler steps on a fixed dt.
Run:  uv run python theory/retrodictions/synthesis_batches/batch_18.py
"""
import math
import sys

import numpy as np
from scipy.signal import lfilter

from crr.instrument.core import arc_length, cv, regularity
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

SRC = "theory/retrodictions/twenty_systems.txt"


def ag(a, b, tol=TOL_G):
    return "agree" if rel(a, b) <= tol else "differ"


def hf(ok):
    return "holds" if ok else "fails"


def _cls(r, floor=0.01):
    """The source battery's class rule: tie below 1e-3, a label below 0.01 is 'not a reading'."""
    d = r["cv_arc"] - r["cv_clock"]
    if abs(d) < 1e-3:
        return "tie"
    lab = "arc-regular" if d < 0 else "clock-regular"
    return lab if abs(d) >= floor else f"{lab} by {abs(d):.3f} (below the 0.01 reading margin)"


def _ci_word(ci):
    if ci[1] < 0.0:
        return "CI below 0"
    if ci[0] > 0.0:
        return "CI above 0"
    return "CI includes 0"


def _ci_cls(ci):
    """The class by the paired-bootstrap CI of CV(arc) - CV(clock) (R6): decided only when the CI excludes 0."""
    return {"CI below 0": "arc-regular", "CI above 0": "clock-regular"}.get(_ci_word(ci), "undecided (CI includes 0)")


def _f(v):
    """A CI bound at round-off prints in exponent form, not as -0.0000."""
    return f"{v:.1e}" if abs(v) < 1e-6 else f"{v:.4f}"


def _ci(ci):
    return f"[{_f(ci[0])}, {_f(ci[1])}]"


def _threshold_process(rng, rate_cv, thr_cv, reset_cv=0.0, dt=0.01, n_ev=80, ou_rate=0.05):
    """The source battery's integrate-to-threshold generator, same rng draw order: OU rate noise (stationary CV rate_cv,
    correlation time 1/ou_rate), per-event threshold jitter, a variable reset level; the event index is the first sample
    after the reset, so the exclusive segment x[a:b] is the monotone ramp and the inclusive one adds the drop."""
    ou = 0.0; x = 0.0; trace = []; events = []; resets = [0.0]
    thr = 1.0 * (1 + thr_cv * rng.standard_normal(n_ev)); i = 0; t = 0
    while i < n_ev:
        ou += dt * (-ou_rate * ou) + rate_cv * math.sqrt(2 * ou_rate * dt) * rng.standard_normal(); u = max(1.0 + ou, 0.05)
        x += u * dt; trace.append(x); t += 1
        if x >= thr[i]:
            events.append(t); x = max(0.0, reset_cv * abs(rng.standard_normal())) * thr[i]; resets.append(x); i += 1
    return np.array(trace), np.array(events), thr, np.array(resets)


def _occ(tr, ev, dt, segment_end):
    """Per-occasion arc, clock, amplitude (ptp) and mean rate arc/clock under the named segmentation."""
    arcs, amps, clk = [], [], []
    for a, b in zip(ev[:-1], ev[1:]):
        seg = tr[a:b + 1] if segment_end == "inclusive" else tr[a:b]
        arcs.append(arc_length(seg)); amps.append(float(np.ptp(seg))); clk.append((b - a) * dt)
    arcs, amps, clk = map(np.asarray, (arcs, amps, clk))
    return arcs, amps, clk, arcs / clk


# ---------------------------------------------------------------- 86: twenty [2] passively Q-switched laser
def r1(dt=0.01, n_boot=2000):
    rng = np.random.default_rng(2)
    cases = (("pump noise, fixed threshold", 0.15, 0.0), ("steady pump, threshold jitter", 0.0, 0.15), ("pump noise and threshold jitter", 0.15, 0.15))
    res = []
    for name, rc, tc in cases:                                              # the first two are the source's cases in its draw order; the third is registered here
        tr, ev, thr, resets = _threshold_process(rng, rc, tc, dt=dt); ev = ev[3:]
        r = regularity(tr, ev, sigma=1.0, dt=dt, n_boot=n_boot, seed=0, segment_end="exclusive")
        arcs, amps, clk, rate = _occ(tr, ev, dt, "exclusive")
        clamp = thr[4:] - resets[4:-1]                                     # the domain's pulse energy: the threshold that closes each scored occasion minus the residual that opened it
        n_bar = float(clk.mean() / dt)                                        # mean ramp length in samples
        offset = r["cv_clock"] * n_bar / (n_bar - 1.0) - r["cv_clock"]        # the exclusive segment loses one sample: at a steady pump CV(arc) = CV(n - 1) = CV(n) n/(n - 1)
        res.append(dict(name=name, r=r, arcs=arcs, amps=amps, clk=clk, rate=rate, clamp=clamp, cv_u=cv(rate), n_bar=n_bar, offset=offset,
                        ident=float(np.abs(arcs - amps).max()), lnvar=(float(np.var(np.log(arcs), ddof=1)), float(np.var(np.log(rate), ddof=1)), float(np.cov(np.log(arcs), np.log(rate))[0, 1]), float(np.var(np.log(clk), ddof=1)))))
    A, B, C = res
    crr, null, dom = A["r"]["C_mean"], float(A["amps"].mean()), float(A["clamp"].mean())
    margin = 0.01                                                            # the source battery's reading margin on a CV difference
    d2 = B["r"]["cv_arc"] - B["r"]["cv_clock"]
    check = (max(c["ident"] for c in res) < 1e-9 and A["r"]["ci95"][1] < 0.0 and abs(d2) < margin and rel(d2, B["offset"]) <= 0.1
             and C["r"]["ci95"][1] < 0.0 and all(c["r"]["ci95_amp"][0] <= 0.0 <= c["r"]["ci95_amp"][1] for c in res))
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    alt = outcome(crr=A["r"]["cv_arc"], null=A["r"]["cv_amp"], domain=None, check=(A["r"]["ci95_amp"][1] < 0.0))   # H-L5 as CRR.md states it: the arc must beat control (i)
    never_clock = all(c["r"]["cv_arc"] - c["r"]["cv_clock"] < margin for c in res)
    reading = {
        "REDUNDANT-IG": f"geometry, as batch 11 read the FitzHugh-Nagumo loop: the gain ramp is monotone, so its arc is its chord and its chord is the clamp (threshold minus residual, the pulse energy the absorber fixes); the amplitude control is the arc to {max(c['ident'] for c in res):.1e} on every occasion of every case, so H-L5 as CRR.md states it, beyond control (i), reads {alt} here, and the class is decided by the pump alone: arc-regular when the pump fluctuates (cases 1 and 3, {_ci_word(A['r']['ci95'])}, {_ci_word(C['r']['ci95'])}), no reading when it does not (case 2, CV(arc) - CV(clock) = {d2:+.4f}, below the {margin:g} margin, and its CI {_ci(B['r']['ci95'])} sits above 0 only by the one sample the exclusive segment drops: {B['offset']:.4f} predicted from CV(clock) n/(n - 1) at n = {B['n_bar']:.1f} samples per ramp), and clock-regular in no case at the {margin:g} reading margin ({hf(never_clock)}), because ln(clock) = ln(arc) - ln(mean pump) on a ramp, an identity, and the pump is drawn independently of the threshold (sample covariances printed). The source row said the same ('the absorber fixes the chord'); the domain's energy balance says it as the pulse-energy/repetition-rate split of the jitter budget; CRR supplied the names. The synthesis reading is {out}",
    }.get(out, f"the arc and the amplitude did not agree in this run: {out}")
    return make_row("opt", "Passively Q-switched laser as the source's integrate-to-threshold train (gain ramp under a pump with OU noise, saturable-absorber threshold, dump to a residual; dt = 0.01, 80 pulses, first three dropped, the dump as the cut): the two source cases and a third with both noises",
                    source=f"{SRC} [2] (DESCR)",
                    Q="the pulse train is in H-L5's arc-regular class exactly when the pump fluctuates and in the clock-regular class never: the arc of a gain ramp is its chord, the clamp (threshold minus residual, the pulse energy), so CV(arc) = CV(amplitude control) identically and CV(arc) = CV(pulse energy) to the sampling step, and the interval is the ramp divided by the mean pump over it, ln(clock) = ln(arc) - ln(pump), so the clock is the less regular quantity whenever the pump varies independently of the threshold",
                    ingredient="H-L5 (the class claim: arc against clock between own events), A3 read as 'the dump is the cut' (segment_end = exclusive), D5 (occasion = pulse to pulse), D2 with the identity metric on the gain (the source's carrier), control (i) of H-L5",
                    null="H-L5's control (i): the peak-to-peak amplitude of the occasion (the ramp's chord), no metric and no cut",
                    domain="the Q-switching energy balance (Statz-deMars rate equations; Degnan 1989 on the optimisation of Q-switched lasers): the pulse energy is set by the initial (threshold) and final (residual) inversion and is independent of the pump power, and the repetition period is that energy divided by the pump rate, so timing jitter carries the pump noise and energy jitter the threshold noise",
                    numbers="; ".join(f"case {k}, {c['name']}: {c['r']['n']} occasions, CV(arc) = {c['r']['cv_arc']:.4f}, CV(clock) = {c['r']['cv_clock']:.4f}, CV(amplitude) = {c['r']['cv_amp']:.4f}, CV(mean pump per ramp) = {c['cv_u']:.4f}, C_mean = {c['r']['C_mean']:.4f}, mean amplitude {c['amps'].mean():.4f}, mean clamp {c['clamp'].mean():.4f} (CV(clamp) = {cv(c['clamp']):.4f}), CI95 of CV(arc) - CV(clock) {_ci(c['r']['ci95'])}, of CV(arc) - CV(amplitude) {_ci(c['r']['ci95_amp'])}, max |arc - amplitude| {c['ident']:.1e}: {_cls(c['r'])}; Var(ln arc) = {c['lnvar'][0]:.5f}, Var(ln pump) = {c['lnvar'][1]:.5f}, Cov(ln arc, ln pump) = {c['lnvar'][2]:.5f}, Var(ln clock) = {c['lnvar'][3]:.5f}" for k, c in enumerate(res, 1))
                            + f"; the exclusive segment drops the sample at the cut, so the arc is the clamp less one step plus the overshoot: clamp - C_mean = {dom - crr:.4f} in case 1, and at a steady pump CV(arc) - CV(clock) = {d2:+.4f} against CV(clock) n/(n - 1) - CV(clock) = {B['offset']:.4f} (n = {B['n_bar']:.1f} samples per ramp) in case 2",
                    tg=f"C_mean (arc under the exclusive cut) {crr:.4f} vs null (mean amplitude of the occasion) {null:.4f}, case 1: {ag(crr, null)}",
                    tn=f"the clamp (threshold minus residual) gives {dom:.4f} for the mean arc: {ag(crr, dom, TOL_N)} (the domain has Q: the pulse energy is the ramp)",
                    tc=f"arc = amplitude on every occasion (< 1e-9), case 1 and case 3 arc-regular with the CI below 0, case 2 within {margin:g} of a tie and its residual within 10 % of the one-sample offset, and the amplitude CI includes 0 in every case: {hf(check)}",
                    out=out, reading=reading,
                    weakness="a model with an instantaneous dump; the OU pump noise has a correlation time of 20 ramps, so 80 pulses hold few independent pump values and the bootstrap CIs treat correlated occasions as exchangeable; the residual is fixed at zero (the tokamak row varies it); no H-CUT proposition was formed because on a threshold-reset carrier the own event is the carrier's extremum by the domain's definition of the threshold, so the antipode-against-extremum comparison has the extremum at offset zero by construction; citation by name and year only, not fetched (R10)",
                    elegance="A tipping bucket under a tap spills the same amount every time it tips; only how often it tips depends on the tap. A rule with no knobs, and the whole of the arc-regular class in one picture.",
                    child="Think of a bucket on a hinge under a dripping tap. When it is full it tips, empties, and swings back. Every tip spills the same bucketful, no matter how fast the tap drips; the tap only changes how long you wait between tips. The laser is a bucket like that, filled by its pump and tipped by its shutter.")


# ---------------------------------------------------------------- 87: twenty [3] geyser eruptions (reservoir model with variable release)
def _reservoir(rng, rate_cv, n_ev=400, dt=0.001, thr=1.0):
    """Reservoir refilled at a per-occasion rate u_i = max(1 + rate_cv z, 0.05) to the boiling threshold; an eruption
    releases the fraction f ~ clip(0.5 + 0.2 z, 0.05, 0.95) of the reservoir (the source row's release law) and refilling
    resumes from (1 - f) thr. The eruption is the cut; the event index is the first sample after it."""
    frac = np.clip(0.5 + 0.2 * rng.standard_normal(n_ev), 0.05, 0.95)
    rates = np.maximum(1.0 + rate_cv * rng.standard_normal(n_ev), 0.05)
    x = 0.0; trace = []; events = []; released = []; i = 0; t = 0
    while i < n_ev:
        x += rates[i] * dt; trace.append(x); t += 1
        if x >= thr:
            events.append(t); released.append(frac[i] * thr); x = (1.0 - frac[i]) * thr; i += 1
    return np.array(trace), np.array(events), np.array(released), rates


def r2(dt=0.001, n_boot=2000):
    rng = np.random.default_rng(3)
    res = []
    for name, rc in (("constant refill rate", 0.0), ("refill rate varying per occasion (CV 0.15)", 0.15)):
        tr, ev, released, rates = _reservoir(rng, rc, dt=dt); ev = ev[3:]
        r = regularity(tr, ev, sigma=1.0, dt=dt, n_boot=n_boot, seed=0, segment_end="exclusive")
        arcs, amps, clk, rate = _occ(tr, ev, dt, "exclusive")
        size_prev = released[3:-1]                                          # the eruption that opened each scored occasion
        size_this = released[4:]                                            # the eruption that closed it
        fwd = float(np.corrcoef(size_prev, clk)[0, 1]); back = float(np.corrcoef(size_this, clk)[0, 1])
        # A8: forecast the next interval from the settled occasion (its released volume over the mean refill rate) against the clock's forecasts
        u_mean = float(rate.mean())
        f_settled = size_prev / u_mean; f_prev = np.r_[np.nan, clk[:-1]]; f_mean = np.full_like(clk, clk.mean())
        rms = lambda f: float(np.sqrt(np.nanmean((f - clk) ** 2)))
        n_bar = float(clk.mean() / dt); offset = r["cv_clock"] * n_bar / (n_bar - 1.0) - r["cv_clock"]   # the one sample the exclusive segment drops
        res.append(dict(name=name, r=r, arcs=arcs, amps=amps, clk=clk, size_prev=size_prev, fwd=fwd, back=back, u_mean=u_mean, n_bar=n_bar, offset=offset,
                        rms=(rms(f_settled), rms(f_prev), rms(f_mean)), ident=float(np.abs(arcs - amps).max()), dev=float(np.abs(arcs - size_prev).max())))
    K, V = res
    crr, null, dom = V["r"]["C_mean"], float(V["size_prev"].mean()), float(V["size_prev"].mean())
    dK = K["r"]["cv_arc"] - K["r"]["cv_clock"]
    check = (max(c["ident"] for c in res) < 1e-9 and max(c["dev"] for c in res) < 2.0 * 1.5 * dt
             and abs(dK) < 0.01 and rel(dK, K["offset"]) <= 0.1 and V["r"]["ci95"][1] < 0.0
             and all(c["r"]["ci95_amp"][0] <= 0.0 <= c["r"]["ci95_amp"][1] for c in res)
             and all(c["fwd"] > c["back"] and c["rms"][0] < min(c["rms"][1], c["rms"][2]) for c in res))
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    alt = outcome(crr=V["r"]["cv_arc"], null=V["r"]["cv_amp"], domain=None, check=(V["r"]["ci95_amp"][1] < 0.0))
    reading = {
        "REDUNDANT-IG": f"geometry, as batch 11 read the FitzHugh-Nagumo loop: the refill is monotone, so the arc of an occasion is its chord, and the chord is the volume the eruption that opened it released (max |arc - released volume| {max(c['dev'] for c in res):.1e}, one sampling step u dt), a number settled at the previous cut. The amplitude control is the arc to {max(c['ident'] for c in res):.1e}, so H-L5 as CRR.md states it, beyond control (i), reads {alt} on this carrier: the paired CI of CV(arc) - CV(amplitude) is {_ci(V['r']['ci95_amp'])} and cannot exclude 0. The dynamics decide the class only through the refill rate: at constant rate the geyser is a tie (CV(arc) - CV(clock) = {dK:+.4f}, and its CI {_ci(K['r']['ci95'])} sits above 0 only by the one sample the exclusive segment drops, {K['offset']:.4f} predicted at n = {K['n_bar']:.1f} samples per refill) and at a varying rate arc-regular ({_ci_word(V['r']['ci95'])}), because ln(interval) = ln(released volume) - ln(rate). The source's forward rule survives as the domain's: the settled eruption forecasts the next interval with RMS {V['rms'][0]:.4f} against {V['rms'][1]:.4f} from the previous interval and {V['rms'][2]:.4f} from the mean interval (forward correlation {V['fwd']:.3f}, backward {V['back']:.3f}), which is the reservoir model's interval = released volume / refill rate, Old Faithful's duration-to-interval rule. The synthesis reading is {out}",
    }.get(out, f"the arc did not reproduce the released volume in this run: {out}")
    return make_row("geo", "Geyser as a reservoir refilled to a boiling threshold (thr = 1) at a per-occasion refill rate, each eruption releasing a fraction f ~ clip(0.5 + 0.2 z, 0.05, 0.95) of the reservoir (the source's release law), 400 eruptions at dt = 0.001, first three dropped, the eruption as the cut; constant refill rate and a rate varying per occasion (CV 0.15)",
                    source=f"{SRC} [3] (CONSIST)",
                    Q="the arc of a refill occasion is the volume the previous eruption released, a quantity settled at the previous cut: the geyser is arc-regular only through the refill rate's variation (a tie at constant rate), the amplitude control ties the arc identically, and the forecast of the next interval from the settled eruption is the reservoir model's forward rule",
                    ingredient="H-L5 (the class claim, with its amplitude control (i)), A3 read as 'the eruption is the cut' (segment_end = exclusive), D5 (occasion = eruption to eruption), A6/A8 (the next occasion seeded from, and forecast from, the settled one), D2 with the identity metric on the reservoir level (the source's carrier)",
                    null="the domain's eruption size: the released volume of the eruption that opened the occasion (no arc, no cut); the amplitude control (i) for the class",
                    domain="reservoir/refill models of geysers (Rinehart 1980): the interval to the next eruption is the volume released divided by the refill rate, which is the duration-to-interval rule used for Old Faithful",
                    numbers="; ".join(f"{c['name']}: {c['r']['n']} occasions, CV(arc) = {c['r']['cv_arc']:.4f}, CV(clock) = {c['r']['cv_clock']:.4f}, CV(amplitude) = {c['r']['cv_amp']:.4f}, C_mean = {c['r']['C_mean']:.4f}, mean released volume {c['size_prev'].mean():.4f}, CI95 of CV(arc) - CV(clock) {_ci(c['r']['ci95'])}, of CV(arc) - CV(amplitude) {_ci(c['r']['ci95_amp'])}, max |arc - amplitude| {c['ident']:.1e}, max |arc - released volume| {c['dev']:.1e}: {_cls(c['r'])}; corr(released volume, following interval) = {c['fwd']:.3f}, corr(released volume, preceding interval) = {c['back']:.3f}; RMS error forecasting the next interval from the settled eruption (volume / mean rate {c['u_mean']:.4f}) {c['rms'][0]:.4f}, from the previous interval {c['rms'][1]:.4f}, from the mean interval {c['rms'][2]:.4f}" for c in res)
                            + f"; at constant rate CV(arc) - CV(clock) = {dK:+.4f} against the one-sample offset of the exclusive segment CV(clock) n/(n - 1) - CV(clock) = {K['offset']:.4f} (n = {K['n_bar']:.1f} samples per refill)",
                    tg=f"C_mean (arc under the exclusive cut) {crr:.4f} vs null (mean released volume) {null:.4f}, varying rate: {ag(crr, null)}",
                    tn=f"the reservoir rule gives the released volume {dom:.4f} for the arc: {ag(crr, dom, TOL_N)} (the domain has Q)",
                    tc=f"arc = amplitude on every occasion (< 1e-9) and arc = released volume to the sampling step, constant rate within 0.01 of a tie with its residual within 10 % of the one-sample offset, arc-regular at varying rate with the CI below 0, the amplitude CI includes 0 in both cases, forward correlation above backward and the settled-eruption forecast the best of the three in both cases: {hf(check)}",
                    out=out, reading=reading,
                    weakness="the source's model had no trace (its forward correlation of 1.00 was wait = size by construction); this row supplies one with a per-occasion refill rate and the source's release law, so the class numbers are this row's registered choices (CV 0.15, 400 eruptions); the released fraction is drawn independently of the reservoir state, and a threshold that varies instead (the pulsar row) would move the correlation to the backward side, as the source noted; citation by name and year only, not fetched (R10)",
                    elegance="After an eruption the pot refills exactly what it lost, so the size of what just happened tells the wait until the next one; the clock does not. The rangers' rule, and a picture of an occasion seeded by the one before it.",
                    child="When a geyser erupts it throws out some of its hot water, sometimes a lot and sometimes a little. Then it has to fill back up before it can go again. So a big eruption means a long wait and a small one a short wait. Park rangers at Old Faithful time the eruption to tell visitors when the next one will come.")


# ---------------------------------------------------------------- 88: twenty [6] tokamak sawtooth crashes, complete and incomplete
def r3(dt=0.01, n_boot=2000):
    rng = np.random.default_rng(6)
    res = []
    for name, rc, tc, reset in (("heating noise, complete crash", 0.15, 0.0, 0.0), ("heating noise, incomplete crash (variable residual)", 0.15, 0.0, 0.5)):
        tr, ev, thr, resets = _threshold_process(rng, rc, tc, reset_cv=reset, dt=dt); ev = ev[3:-1]   # the last event has no post-crash sample in the trace, so its inclusive segment would lack the drop
        rd = {s: regularity(tr, ev, sigma=1.0, dt=dt, n_boot=n_boot, seed=0, segment_end=s) for s in ("exclusive", "inclusive")}
        ex = _occ(tr, ev, dt, "exclusive")[0]; inc = _occ(tr, ev, dt, "inclusive")[0]
        lag1 = float(np.corrcoef(ex[:-1], ex[1:])[0, 1])
        pred_in = cv(ex) / math.sqrt(2.0) * math.sqrt(1.0 + lag1)          # the inclusive arc is two consecutive ramps: CV / sqrt 2 x sqrt(1 + lag-1 correlation)
        over = resets[5:5 + len(ex)] >= thr[4:4 + len(ex)]                    # the residual left by the crash closing each scored occasion, at or above its threshold: the source's reset law is uncapped, so that 'drop' is a rise and the next occasion is one sample long, starting above the threshold
        opened_over = resets[4:4 + len(ex)] >= thr[3:3 + len(ex)]             # the occasion opened by such a residual
        ok = ~(over[:-1] | opened_over[:-1])
        two_ramps = float(np.abs(inc[:-1][ok] - (ex[:-1] + ex[1:])[ok]).max())   # inclusive_i = exclusive_i + exclusive_i+1 up to the sampling step, on the occasions the uncapped residual does not touch
        cv_sum = cv(ex[:-1] + ex[1:])                                         # the CV of the sum of two consecutive ramps over all occasions
        res.append(dict(name=name, rd=rd, lag1=lag1, pred_in=pred_in, two_ramps=two_ramps, n_over=int(over.sum()), n_touched=int((~ok).sum()), cv_sum=cv_sum, resid_mean=float(resets[4:].mean())))
    Cc, Ic = res
    cv_ex, cv_in, cv_clk = Ic["rd"]["exclusive"]["cv_arc"], Ic["rd"]["inclusive"]["cv_arc"], Ic["rd"]["inclusive"]["cv_clock"]
    floor = 0.01
    complete_floor = Cc["rd"]["exclusive"]["cv_arc"] < floor and Cc["rd"]["inclusive"]["cv_arc"] < floor
    same_complete = _ci_cls(Cc["rd"]["exclusive"]["ci95"]) == _ci_cls(Cc["rd"]["inclusive"]["ci95"])
    internal = rel(cv_ex, cv_in) > TOL_G
    cls_ex, cls_in = _ci_cls(Ic["rd"]["exclusive"]["ci95"]), _ci_cls(Ic["rd"]["inclusive"]["ci95"])
    changes = cls_ex != cls_in
    out = outcome(crr=cv_ex, null=cv_clk, domain=None, check=None, internal=internal)
    reading = {
        "INTERNAL": f"A3 says the cut has no content, and on a partial reset that clause has two readings on the same events. Complete crash: the two segmentations differ by a constant (C_mean {Cc['rd']['exclusive']['C_mean']:.4f} against {Cc['rd']['inclusive']['C_mean']:.4f}: the drop is one more ramp), both CV(arc) are {'at the sampling floor' if complete_floor else 'not both at the sampling floor'} ({Cc['rd']['exclusive']['cv_arc']:.4f}, {Cc['rd']['inclusive']['cv_arc']:.4f} against {floor:g}) and the class by the CI is {'the same' if same_complete else 'not the same'} ({_ci_cls(Cc['rd']['exclusive']['ci95'])}, {_ci_cls(Cc['rd']['inclusive']['ci95'])}). Incomplete crash: under 'the crash is the cut' the residual it leaves is not arc and the ramp CV is {cv_ex:.4f} against the clock's {cv_clk:.4f} ({_cls(Ic['rd']['exclusive'])}; by the CI {cls_ex}); under 'the crash is content' the occasion holds the ramp plus the drop, which is the next ramp to {Ic['two_ramps']:.1e} wherever the crash is a drop (on {Ic['n_over']} of {Ic['rd']['exclusive']['n']} occasions the source's uncapped reset law leaves a residual at or above the threshold, so that 'crash' is a rise and the occasion it opens is one sample long and starts above the threshold; those pairs are left out of the identity), so its CV falls to {cv_in:.4f} by arithmetic (the CV of the sum of two consecutive ramps is {Ic['cv_sum']:.4f} over all occasions, {Ic['pred_in']:.4f} predicted from CV/sqrt 2 with the lag-1 correlation {Ic['lag1']:.3f}; the inclusive arc is that sum to {Ic['two_ramps']:.1e} except on the {Ic['n_touched']} of {Ic['rd']['exclusive']['n'] - 1} consecutive pairs the uncapped residuals touch, which is where the two CVs part) and by the CI the class is {cls_in}: the class {'changes' if changes else 'does not change'} between the two readings. The source's 'incomplete crashes make the cycle irregular' is the exclusive reading's number; which reading A3 is on a partial reset (the README's open 'reset jumps are the cut' reading, here with {'the class, not only C_mean,' if changes else 'C_mean'} changing between them) is a v3.2 decision, and the Kadomtsev/Porcelli crash, a reconnection event with a duration and an amplitude of its own, is the case the decision must name",
    }.get(out, f"the two segmentations agreed on the incomplete crash in this run: {out}")
    return make_row("plasma", "Tokamak sawtooth as the source's integrate-to-threshold train (core temperature ramp under a heating power with OU noise, crash at a fixed threshold to a residual that is zero (complete) or 0.5 |z| of the threshold (incomplete); dt = 0.01, 80 crashes, the first three and the last dropped), scored under both segmentations of A3's cut",
                    source=f"{SRC} [6] (DESCR)",
                    Q="under an incomplete crash H-L5's class of the sawtooth depends on which reading of A3 is taken, the crash as the cut (exclusive: the residual is not arc) or the crash as content (inclusive: the drop is arc): the ramp CV against the clock under the first, the CV of two consecutive ramps (a factor 1/sqrt 2 by arithmetic) under the second",
                    ingredient="A3 (the cut has no content) in its two readings on a partial reset, segment_end = exclusive against inclusive; D5 (occasion = crash to crash); H-L5 (the class claim); D2 with the identity metric on the temperature (the source's carrier)",
                    null="the clock: the crash-to-crash interval statistics the domain already has (Kadomtsev period ~ heating time to the q = 1 threshold)",
                    domain=None,
                    numbers="; ".join(f"{c['name']}: {c['rd']['exclusive']['n']} occasions; exclusive: CV(arc) = {c['rd']['exclusive']['cv_arc']:.4f}, CV(clock) = {c['rd']['exclusive']['cv_clock']:.4f}, C_mean = {c['rd']['exclusive']['C_mean']:.4f}, CI95 of CV(arc) - CV(clock) {_ci(c['rd']['exclusive']['ci95'])}: {_cls(c['rd']['exclusive'])}, by the CI {_ci_cls(c['rd']['exclusive']['ci95'])}; inclusive: CV(arc) = {c['rd']['inclusive']['cv_arc']:.4f}, CV(clock) = {c['rd']['inclusive']['cv_clock']:.4f}, C_mean = {c['rd']['inclusive']['C_mean']:.4f}, CI95 {_ci(c['rd']['inclusive']['ci95'])}: {_cls(c['rd']['inclusive'])}, by the CI {_ci_cls(c['rd']['inclusive']['ci95'])}; inclusive arc = this ramp + next ramp to {c['two_ramps']:.1e} away from the uncapped residuals (residual at or above the threshold, so the crash is a rise and the next occasion one sample long: {c['n_over']} occasions); lag-1 correlation of the ramps {c['lag1']:.3f}; CV of the sum of two consecutive ramps {c['cv_sum']:.4f} (predicted {c['pred_in']:.4f} from CV/sqrt 2 with the lag-1 correlation), occasions the uncapped residuals touch {c['n_touched']} of {c['rd']['exclusive']['n'] - 1} pairs; mean residual after the crash {c['resid_mean']:.4f}" for c in res),
                    tg=f"incomplete crash: CV(arc) under 'the crash is the cut' {cv_ex:.4f} vs under 'the crash is content' {cv_in:.4f}: {ag(cv_ex, cv_in)} (the ingredient has two values on the domain); against the null CV(clock) {cv_clk:.4f}: {ag(cv_ex, cv_clk)} under the first, {ag(cv_in, cv_clk)} under the second",
                    tn="none cited: the Kadomtsev model gives the crash and the period, not a dispersion of the ramp",
                    tc=f"not reached: the two readings of the cut give CV(arc) = {cv_ex:.4f} and {cv_in:.4f} on the same {Ic['rd']['exclusive']['n']} occasions (relative difference {rel(cv_ex, cv_in):.3f})",
                    out=out, reading=reading,
                    weakness="the source's generator (an instantaneous drop, OU heating noise with a 20-ramp correlation time, a residual drawn independently of the ramp and not capped at the threshold) at the source's seed, one occasion fewer than the source so that both segmentations score the same occasions; the factor 1/sqrt 2 is exact only for independent residuals and the lag-1 correlation of the ramps is printed; the CIs treat correlated occasions as exchangeable; no Kadomtsev dynamics are integrated")


# ---------------------------------------------------------------- 89: twenty [8] bacterial run-and-tumble
def r4(n=400, seed=8, v0=20.0):
    rng = np.random.default_rng(seed); runs = rng.exponential(1.0, n)      # the source's runs, seed and draw order
    res = []
    for name, spd_cv in (("constant swimming speed", 0.0), ("speed varying run to run (CV 0.2)", 0.2)):
        v = v0 * (1 + spd_cv * rng.standard_normal(n)); arcs = v * runs
        cv_v, cv_t = cv(v), cv(runs)
        pred = math.sqrt((1.0 + cv_v ** 2) * (1.0 + cv_t ** 2) - 1.0)          # independent speed and duration: CV(v tau)^2 = (1 + CV_v^2)(1 + CV_tau^2) - 1
        lv, lt = np.log(v), np.log(runs)
        res.append(dict(name=name, cv_arc=cv(arcs), cv_clock=cv_t, cv_v=cv_v, pred=pred, cov=float(np.cov(lv, lt)[0, 1]), var_lv=float(np.var(lv, ddof=1)), var_lt=float(np.var(lt, ddof=1)), var_la=float(np.var(np.log(arcs), ddof=1))))
    K, V = res
    comp = [(g, cv(v0 * (runs.mean() / runs) ** g * runs)) for g in (0.5, 1.0)]   # speed falling with duration, v ∝ tau^-gamma: the only road to the arc-regular class
    crr, null, dom = K["cv_arc"], K["cv_clock"], K["cv_clock"]
    ident = all(rel(c["var_la"], c["var_lv"] + c["var_lt"] + 2.0 * c["cov"]) < 1e-9 for c in res)
    check = rel(crr, null) < 1e-12 and rel(V["cv_arc"], V["pred"]) <= 0.05 and V["cv_arc"] > V["cv_clock"] and ident and comp[1][1] < 1e-9 and comp[0][1] < K["cv_clock"]
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    flip = -V["var_lv"] / 2.0
    reading = {
        "REDUNDANT-IG": f"the arc of a straight run is speed times duration, so at constant speed the arc is the clock times a constant and the two CVs are one number ({crr:.4f}); H-L5's class claim has nothing to compare. With speed varying independently the arc is the less regular quantity by the product rule (CV(arc) {V['cv_arc']:.4f}, closed form {V['pred']:.4f} from CV(v) {V['cv_v']:.4f} and CV(tau) {V['cv_clock']:.4f}), and the identity Var(ln arc) = Var(ln v) + Var(ln tau) + 2 Cov (exact to 1e-9 here) says the class can only flip when faster runs are shorter by more than half the speed's own log-variance (Cov below {flip:.4f} against the observed {V['cov']:.4f}); the compensating law v ∝ tau^-gamma gives CV(arc) {comp[0][1]:.4f} at gamma = 0.5 and {comp[1][1]:.1e} at gamma = 1 (a fixed run length: the S-G2 surrogate's construction), which is a statement about the cell's speed-duration covariance, a quantity Berg and Brown measured, not a prediction. The source row's 'a control row' stands; the synthesis reading is {out}",
    }.get(out, f"the arc and the clock did not coincide at constant speed in this run: {out}")
    return make_row("micro", "Bacterial run-and-tumble as the source's model: 400 exponential run durations (mean 1), swimming speed 20 constant or varying run to run (CV 0.2), run length = speed x duration; plus the compensating law v ∝ tau^-gamma on the same runs",
                    source=f"{SRC} [8] (DESCR)",
                    Q="between tumbles the arc (run length) and the clock (run duration) are one quantity up to the speed: CV(arc)^2 = (1 + CV(v)^2)(1 + CV(tau)^2) - 1 when speed and duration are independent, so a run-and-tumble is never arc-regular unless faster runs are shorter by more than half the speed's log-variance",
                    ingredient="H-L5 (the class claim: arc against clock between own events), D5 [M] (occasion = one run, the tumble the cut), A1' point-process reading (one tumble = one step), D2 with the identity metric on position (arc = distance swum, monotone so S = 0)",
                    null="the clock: the run-duration distribution the domain already has (exponential, Berg and Brown 1972)",
                    domain="run length = speed x duration (Berg and Brown 1972: speed approximately constant within and across runs, run durations exponential), so run lengths inherit the duration distribution",
                    numbers="; ".join(f"{c['name']}: CV(arc) = {c['cv_arc']:.4f}, CV(clock) = {c['cv_clock']:.4f}, CV(speed) = {c['cv_v']:.4f}, closed form under independence {c['pred']:.4f}; Var(ln arc) = {c['var_la']:.4f} = Var(ln v) {c['var_lv']:.4f} + Var(ln tau) {c['var_lt']:.4f} + 2 Cov {c['cov']:.4f}" for c in res)
                            + f"; flip condition Cov(ln v, ln tau) < -Var(ln v)/2 = {flip:.4f}; compensating law v ∝ tau^-gamma on the same runs: " + ", ".join(f"gamma = {g:g}: CV(arc) = {c:.4f}" if c > 1e-6 else f"gamma = {g:g}: CV(arc) = {c:.1e}" for g, c in comp),
                    tg=f"CV(arc) {crr:.4f} vs null CV(clock) {null:.4f} at constant speed: {ag(crr, null)}",
                    tn=f"run length = speed x duration gives CV(clock) {dom:.4f} for CV(arc): {ag(crr, dom, TOL_N)} (the domain has Q)",
                    tc=f"exact equality at constant speed, the independence closed form within 5 % at varying speed with CV(arc) > CV(clock) there, the log-variance identity to 1e-9, and the compensating law arc-regular at gamma = 0.5 and constant at gamma = 1: {hf(check)}",
                    out=out, reading=reading,
                    weakness="a straight run on a Euclidean carrier: the identity metric is the source's stand-in and A1 does not license it; the exponential durations and independent speeds are the model's, and a real speed-duration covariance would be a measurement (tracking data, none opened here, none in data/SEEN.md); the compensating law is a construction, not a bacterial mechanism; citation by name and year only, not fetched (R10)",
                    elegance="At one steady speed, counting metres and counting seconds is the same count: the odometer is a clock. The two come apart only when the speed changes, and then whichever one you trust is a fact about the speed, not about the road.",
                    child="A swimming germ goes in a straight line, then tumbles and picks a new direction. If it always swims at the same speed, saying how far it went and saying how long it swam are the same thing, like an odometer that only ticks when the car moves at one speed. The two numbers only disagree if the germ speeds up or slows down.")


# ---------------------------------------------------------------- 90: twenty [11] the bullwhip effect with the P3 forecast
def _bullwhip_weights(w, L1):
    """Order-up-to policy q_t = D_{t-1} + L1 (F_t - F_{t-1}) with F_t = sum_k w_k D_{t-1-k}: on i.i.d. demand
    Var(q)/Var(D) = sum_j c_j^2, the squared impulse response of the order on the demand."""
    w = np.asarray(w, float); c = np.zeros(len(w) + 1)
    c[0] = 1.0 + L1 * w[0]; c[1:len(w)] += L1 * (w[1:] - w[:-1]); c[len(w)] += -L1 * w[-1]
    return float((c ** 2).sum())


def r5(L=2, n=1_000_000, burn=2000, seed=11, K=4000):
    L1 = L + 1; rng = np.random.default_rng(seed); D = 10.0 + rng.standard_normal(n); varD = float(D.var())
    res = []
    for p in (5, 20):
        alpha = 2.0 / (p + 1); q = 1.0 - alpha                                 # P3: mean age q/(1-q) = (p-1)/2, the box window's mean age; also equal forecast variance
        w_box = np.ones(p) / p; w_p3 = (1.0 - q) * q ** np.arange(K)
        ratio_box, ratio_p3 = _bullwhip_weights(w_box, L1), _bullwhip_weights(w_p3, L1)
        closed_box = 1.0 + 2.0 * L1 / p + 2.0 * L1 ** 2 / p ** 2
        closed_es = 1.0 + 2.0 * L1 * alpha + 2.0 * L1 ** 2 * alpha ** 2 / (2.0 - alpha)   # exponential smoothing in the order-up-to policy (Chen, Ryan & Simchi-Levi 2000, in this row's lead-time convention)
        cs = np.cumsum(D); F_box = np.r_[np.full(p + 1, np.nan), ((cs[p:] - cs[:-p]) / p)[:-1]]   # F_box[t] = mean(D[t-p:t]), the source's forecast
        G = lfilter([alpha], [1.0, -(1.0 - alpha)], D); F_p3 = np.r_[np.nan, G[:-1]]       # F_p3[t] = alpha D[t-1] + (1-alpha) F_p3[t-1]
        sims = []
        for F in (F_box, F_p3):
            t = np.arange(burn, n); qq = D[t - 1] + L1 * (F[t] - F[t - 1]); sims.append(float(qq.var() / varD))
        res.append(dict(p=p, alpha=alpha, q=q, mean_age=q / (1 - q), ratio_box=ratio_box, ratio_p3=ratio_p3, closed_box=closed_box, closed_es=closed_es, sim_box=sims[0], sim_p3=sims[1],
                        w0=(w_box[0], w_p3[0]), var_f=(1.0 / p, alpha / (2.0 - alpha))))
    A, B = res
    crr, null, dom = A["ratio_p3"], A["ratio_box"], A["closed_es"]
    accumulated = 1.0 + 2.0 * L1 * 0.0 + 2.0 * L1 ** 2 * 0.0 ** 2 / 2.0        # alpha -> 0: the forecast is the accumulated mean of all past demand
    check = all(rel(c["sim_p3"], c["ratio_p3"]) <= 0.02 and rel(c["sim_box"], c["ratio_box"]) <= 0.02 and rel(c["ratio_box"], c["closed_box"]) < 1e-9 and c["ratio_p3"] > c["ratio_box"] for c in res)
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    more = all(c["ratio_p3"] > c["ratio_box"] for c in res)
    reading = {
        "REDUNDANT-DOMAIN": f"A6 with P3 does work on this carrier (T-G: {crr:.4f} against the window's {null:.4f} at p = {A['p']}, {B['ratio_p3']:.4f} against {B['ratio_box']:.4f} at p = {B['p']}), and what it produces is the exponential-smoothing bullwhip formula, which the domain derived (Chen, Ryan and Simchi-Levi 2000) in the year it derived the moving-average one. At the window's own mean age the regenerating forecast amplifies {'more' if more else 'less'} than the window at both p, because it puts {A['w0'][1]:.4f} of its weight on the last demand where the window puts {A['w0'][0]:.4f}, so each new demand moves the order-up-to level further. The bounded-strength clause of A6 ('never an accumulated count') excludes the one forecast with no bullwhip on i.i.d. demand, the accumulated mean of all past demand (alpha -> 0, ratio {accumulated:.4f}): regeneration is not estimation, as synthesis rows 3 and 9 and batch 03 found. The source row's content (the window is a memory class P3 does not name) stands; the synthesis reading is {out}",
    }.get(out, f"the P3 weights did not reproduce the exponential-smoothing formula in this run: {out}")
    return make_row("ops", f"Order-up-to retailer on i.i.d. demand (10 + N(0, 1), {n} periods, seed {seed}, lead time L = {L}) whose forecast is the P3 age-weighted mean of settled demand (A6 regeneration at bounded strength) against the source's p-period moving average, matched at the window's mean age (p - 1)/2, which is also equal forecast variance",
                    source=f"{SRC} [11] (DESCR)",
                    Q="a retailer who regenerates the demand forecast from the settled past with P3 age weights (alpha = 2/(p+1) at the window's mean age) amplifies demand variance by 1 + 2(L+1) alpha + 2(L+1)^2 alpha^2/(2 - alpha), more than the p-period window's 1 + 2(L+1)/p + 2(L+1)^2/p^2 at every p",
                    ingredient="A6 (regeneration by a bounded-strength weighted mean of settled occasions, never an accumulated count), P3 (geometric age weights, q fixed by the mean-age constraint), D5 (occasion = one period's demand)",
                    null="the source's forecast: the box window, uniform over p periods and zero beyond, in the same order-up-to policy",
                    domain="Chen, Ryan and Simchi-Levi 2000 (exponential-smoothing forecasts in the order-up-to policy on i.i.d. demand): Var(q)/Var(D) has the form 1 + 2 L alpha + 2 L^2 alpha^2/(2 - alpha) in their lead-time convention; Chen, Drezner, Ryan and Simchi-Levi 2000 for the moving average",
                    numbers="; ".join(f"p = {c['p']}: alpha = {c['alpha']:.6f} (q = {c['q']:.6f}, mean age {c['mean_age']:.4f}; forecast variance / sigma^2 window {c['var_f'][0]:.4f}, P3 {c['var_f'][1]:.4f}); Var(orders)/Var(demand) from the squared impulse response: window {c['ratio_box']:.6f} (closed form {c['closed_box']:.6f}), P3 {c['ratio_p3']:.6f} (exponential-smoothing closed form {c['closed_es']:.6f}); simulated: window {c['sim_box']:.4f}, P3 {c['sim_p3']:.4f}; weight on the last demand: window {c['w0'][0]:.4f}, P3 {c['w0'][1]:.4f}" for c in res)
                            + f"; accumulated mean of all past demand (alpha -> 0): ratio {accumulated:.4f}",
                    tg=f"P3 forecast {crr:.4f} vs null (box window) {null:.4f} at p = {A['p']}: {ag(crr, null)}",
                    tn=f"the exponential-smoothing formula gives {dom:.4f}: {ag(crr, dom, TOL_N)} (the domain has Q)",
                    tc=f"simulation within 2 % of the impulse-response value for both forecasts at both p, the window's value equal to the source's closed form, and P3 above the window at both p: {hf(check)}",
                    out=out, reading=reading,
                    weakness="i.i.d. demand and the order-up-to policy are the source's (and the domain's) simplest case; the mean-age matching is P3's own constraint, and matching at equal forecast variance gives the same alpha, so the comparison is not tuned; whether the domain compared the two forecasts at matched mean age is the expert's question, not this script's; citations by name and year only, not fetched (R10)",
                    elegance="Two shopkeepers remember the same distance into the past on average. One remembers the last five weeks equally; the other remembers mostly last week and a fading bit of every week before. The second one jumps more with every new week. The teaching is that the shape of a memory, not only its length, sets how much you overreact.",
                    child="Imagine two shopkeepers deciding how much to order. One looks at the last five weeks and treats them all the same. The other pays most attention to last week and only a little to the weeks before, even though on average both look back just as far. The second shopkeeper's orders jump around more, because every new week counts for more in their memory.")


def main():
    return run_batch("Synthesis batch 18: rows 86-90 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())

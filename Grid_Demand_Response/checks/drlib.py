"""DR1 shared model library for the eight model checks H1-H8 of Grid_Demand_Response/DECLARATION.md (section 2; pushed at
e67e8ee before any source, code or data; binding, never edited here). The library adds no prediction, arm, threshold or
verdict of its own: it is the arithmetic the checks share.

It generalises EPS2 T1 (Empty_Pause_Systems/batches/eps2_01.py, pinned output eps2_01.txt; EMPTY_PAUSE_SYSTEMS.md section 6)
and keeps its conventions exactly (the selftest reproduces EPS2 T1's printed blocks line for line):
  - A job of W compute-hours, worth W * rate at completion if it meets its deadline, else 0 (EPS2: rate 1 per compute-hour).
  - Valuation after the accepted events, payments excluded: V = W rate 1[deadline met] - sum of per-event charges c.
    WALL: c = rate (H + o), the event's wall-clock hours; OWN, ETM: c = rate o, own running hours without progress; the
    per-event overhead o = R + S + lost (EPS2: o = R; the save time S and the lost work are DR1 additions, 0 by default).
  - Deadline clock: wall for WALL, OWN, TIER, H0 (W + sum of wall delays <= D); own steps for ETM (W + n o <= D: the
    stop-the-clock contract extends D by the curtailed time, the overhead still counts).
  - The fleet maximises valuation plus payments by exact backward induction (ties accept); it may let the deadline pass.
  - Minimum acceptable payment x* at an offer state: the infimum of the flat payments pi (per curtailed fleet-hour, applied
    to this offer and every later one) at which accepting is optimal, the rest of the season played optimally at the same
    pi. Computed exactly from the value functions, which are convex piecewise linear in pi (class CPL).
  - H0: an interruptible-load contract covering every offered event (mandatory once enrolled); reservation price = the
    job's opportunity cost of all contracted events per curtailed fleet-hour (OWN's valuation, wall-clock deadline).
    H0_WALL is EPS2's H0-wall (the curtailed wall hours charged).
  - Payments pi are per curtailed fleet-hour at full power (EPS2: one MWh-equivalent per fleet hour) in the job's value
    units; a fleet of P_MW megawatts curtails P_MW MWh per curtailed fleet-hour (play(..., P_MW)).

DR1 additions (each a CHOICE, printed by the checks that use it):
  - TIER (declaration section 2): the industry slowdown-tier contract; during an offered event the job runs at throughput
    1 - x (a throttle, no checkpoint: own overhead 0 unless declared) for min(H, window) hours; curtailed energy per event
    min(H, window) (1 - power(1 - x)) fleet-hours with a declared performance-power curve (default linear, ASSUMED); wall
    delay x min(H, window); valued on the own clock with the wall-clock deadline (value_clock='wall' available).
  - The save time S: own running hours without progress per event (the checkpoint written before the power drops), added
    to R; response_ok(job, T) says whether the save fits a product's response time T; lossy(job, interval) is the pause
    without a save (the work since the last periodic checkpoint is lost, interval / 2 in expectation).
  - Offers carry a probability p of being made (independently): p = 1 is EPS2's known schedule; p < 1 is the Poisson-offer
    variant (poisson_slots: Poisson arrivals, at most one event per slot, unknown count). Backward induction then gives
    the exact expectation (rational arithmetic when every p is rational). rule_xstar / poisson_xstar give the closed form
    for identical offers (derived in rule_xstar's docstring; the selftest checks it against the backward induction).
  - Running condition: an offer at wall hour t is live only while the job has not finished (t < W + wall delay so far);
    consecutive offers must not overlap an event and its overhead (checked; ValueError otherwise).

API (exact Fractions throughout; q() converts ints and decimal strings, floats are refused):
  Job(W, D, R, S=0, lost=0, rate=1, name='')          .overhead .value .slack
  Offer(t, H, p=1); every(spacing, H, before, p=1); schedule(times, lengths, probs=None)
  poisson_p(lam, slot, max_den=10**6) -> (p, err); poisson_slots(lam, slot, H, before, max_den=10**6) -> (offers, err)
  Arm(...); WALL, OWN, ETM, H0, H0_WALL; tier(x, window=None, power=power_linear, value_clock='own', overhead=0, name=None)
  power_linear(t); power_pw(points)
  event(job, arm, H) -> dict; nmax(job, arm, H); stake(job, arm, H, n=0, L=None); met / vjob (job, arm, n, L)
  solve(job, arm, offers, pi) -> Solution(value, dec, V)
  play(job, arm, offers, pi, P_MW=1, made=None, sol=None) -> dict;  expect(job, arm, offers, pi, P_MW=1, sol=None) -> dict
  value_fns(job, arm, offers) -> F;  xstar(job, arm, offers, k, n, L=None, F=None) -> XStar
  xstar_all(job, arm, offers, F=None) -> {(k, n, L): XStar};  p_all(job, arm, offers, F=None) -> PAll
  h0_price(job, offers, arm=H0); h0_cap(job, offers, pi, arm=H0)
  rule_xstar(job, arm, H, n, m_future); poisson_xstar(job, arm, H, lam, t, t_end, n)
  fleet_play(jobs, arm, offers, pi, P_MW); response_ok(job, T); lossy(job, ckpt_interval)
  rel(a, b); g(x); yn(b)
  k is always the 0-based offer index (EPS2 printed k + 1); a state is (n, L): n events accepted, L curtailed contract hours.

Deterministic (exact rational arithmetic; no randomness); stdlib only. Rung R4 at most (synthetic model); a note, not
evidence (R8).
    cd /home/user/ashes_crr && uv run python Grid_Demand_Response/checks/drlib.py selftest > Grid_Demand_Response/checks/drlib_selftest.txt
"""
from __future__ import annotations

import bisect
import math
import re
import sys
from dataclasses import dataclass, replace
from fractions import Fraction as Fr
from pathlib import Path
from typing import Callable, NamedTuple, Sequence

DECL_AT = "e67e8ee"
REPO = Path(__file__).resolve().parents[2]
EPS2_TXT = REPO / "Empty_Pause_Systems" / "batches" / "eps2_01.txt"
ZERO, ONE = Fr(0), Fr(1)


def q(x) -> Fr:
    """An exact rational from an int, a decimal string or a Fraction. Floats are refused (pass '0.1', not 0.1)."""
    if isinstance(x, (float, bool)):
        raise TypeError(f"pass an int, a decimal string or a Fraction, not {type(x).__name__} {x!r}")
    return Fr(x)


def rel(a: float, b: float) -> float:
    """Relative difference, the SYNTHESIS harness's formula (src/crr/synthesis/harness.py)."""
    return abs(a - b) / max(abs(a), abs(b), 1e-12)


def g(x) -> str:
    """A rational printed as a short decimal (EPS2's _g)."""
    return f"{float(x):g}"


def yn(b: bool) -> str:
    return "yes" if b else "no"


# ============================================================================================ the job and the offers
@dataclass(frozen=True)
class Job:
    """A training job: W compute-hours, wall-clock deadline D (hours from its start at hour 0), restart overhead R and
    checkpoint save time S per pause event (own running hours without progress), work lost per event (0 for a lossless
    pause), value `rate` per compute-hour at completion."""
    W: Fr
    D: Fr
    R: Fr
    S: Fr = ZERO
    lost: Fr = ZERO
    rate: Fr = ONE
    name: str = ""

    def __post_init__(self):
        for f in ("W", "D", "R", "S", "lost", "rate"):
            object.__setattr__(self, f, q(getattr(self, f)))
        if self.W <= 0 or self.rate <= 0 or min(self.R, self.S, self.lost) < 0:
            raise ValueError(f"invalid job {self}")

    @property
    def overhead(self) -> Fr:
        """Own running hours without progress per pause event: R + S + lost."""
        return self.R + self.S + self.lost

    @property
    def value(self) -> Fr:
        return self.W * self.rate

    @property
    def slack(self) -> Fr:
        return self.D - self.W


@dataclass(frozen=True)
class Offer:
    """One curtailment offer: the event would start at wall hour t and last H hours; the operator makes it with probability
    p (1: known in advance, EPS2; < 1: the Poisson-offer variant)."""
    t: Fr
    H: Fr
    p: Fr = ONE

    def __post_init__(self):
        for f in ("t", "H", "p"):
            object.__setattr__(self, f, q(getattr(self, f)))
        if self.t < 0 or self.H <= 0 or not (0 < self.p <= 1):
            raise ValueError(f"invalid offer {self}")


def every(spacing, H, before, p=ONE) -> tuple[Offer, ...]:
    """EPS2 T1's offer process: one offer every `spacing` wall hours at hours spacing k, k = 1, 2, ..., strictly before hour
    `before` (EPS2: before = W, the earliest completion, so every arm is running at every offer); each made with
    probability p."""
    spacing, H, before, p = q(spacing), q(H), q(before), q(p)
    out, k = [], 1
    while spacing * k < before:
        out.append(Offer(spacing * k, H, p))
        k += 1
    return tuple(out)


def schedule(times: Sequence, lengths, probs=None) -> tuple[Offer, ...]:
    """Offers at the given wall hours; `lengths` and `probs` are one value or one per offer."""
    n = len(times)
    hs = list(lengths) if isinstance(lengths, (list, tuple)) else [lengths] * n
    ps = [ONE] * n if probs is None else (list(probs) if isinstance(probs, (list, tuple)) else [probs] * n)
    return tuple(Offer(t, h, p) for t, h, p in zip(times, hs, ps))


def poisson_p(lam, slot, max_den: int = 10 ** 6) -> tuple[Fr, float]:
    """P(at least one arrival of a Poisson process of rate lam per wall hour in a slot of `slot` hours) = 1 - exp(-lam slot),
    as the best rational with denominator <= max_den, and the absolute rounding error of that rational (a float)."""
    exact = -math.expm1(-float(q(lam) * q(slot)))
    p = Fr(exact).limit_denominator(max_den)
    return p, abs(float(p) - exact)


def poisson_slots(lam, slot, H, before, max_den: int = 10 ** 6) -> tuple[tuple[Offer, ...], float]:
    """The Poisson-offer variant: operator offers arrive as a Poisson process of rate lam per wall hour and at most one event
    is called per slot (CHOICE: a slot of `slot` hours, e.g. a day; further arrivals in the slot are void and the event
    starts at the slot's start), so each slot at hours slot k < before carries an offer with probability
    p = 1 - exp(-lam slot), independently; the fleet does not know the count. Returns the offers and p's rounding error."""
    p, err = poisson_p(lam, slot, max_den)
    return every(slot, H, before, p), err


# ============================================================================================ the arms
def power_linear(t: Fr) -> Fr:
    """Throughput fraction -> power fraction, linear (energy per step unchanged by a throttle): ASSUMED unless a check
    declares a curve."""
    return q(t)


def power_pw(points) -> Callable[[Fr], Fr]:
    """A declared performance-power curve: throughput fraction -> power fraction, piecewise linear through
    points [(throughput, power), ...], exact; the points must cover [0, 1] and end at (1, 1)."""
    pts = sorted((q(a), q(b)) for a, b in points)
    if pts[0][0] > 0 or pts[-1] != (ONE, ONE):
        raise ValueError("a performance-power curve must cover throughput [0, 1] and pass through (1, 1)")

    def f(t):
        t = q(t)
        for (a0, b0), (a1, b1) in zip(pts, pts[1:]):
            if a0 <= t <= a1:
                return b0 + (b1 - b0) * (t - a0) / (a1 - a0)
        raise ValueError(f"throughput {t} outside the curve")
    f.points = tuple(pts)
    return f


@dataclass(frozen=True)
class Arm:
    """An arm: the clock its valuation reads (value_clock), the clock its deadline runs on (deadline_clock), the mechanism
    (a full 'pause' or a 'tier' throttle at slowdown x over at most `window` hours of an event), the power drawn while paused
    (idle, a fraction of full power; EPS2: 0), and whether it is the H0 contract (enrolment at the reservation price)."""
    name: str
    value_clock: str = "own"
    deadline_clock: str = "wall"
    mech: str = "pause"
    x: Fr = ONE
    window: Fr | None = None
    power: Callable = power_linear
    idle: Fr = ZERO
    tier_overhead: Fr = ZERO
    h0: bool = False

    def __post_init__(self):
        if self.value_clock not in ("wall", "own") or self.deadline_clock not in ("wall", "own") or self.mech not in ("pause", "tier"):
            raise ValueError(f"invalid arm {self.name}")
        for f in ("x", "idle", "tier_overhead"):
            object.__setattr__(self, f, q(getattr(self, f)))
        if self.window is not None:
            object.__setattr__(self, "window", q(self.window))
        if not (0 <= self.x <= 1) or not (0 <= self.idle < 1) or self.tier_overhead < 0:
            raise ValueError(f"invalid arm {self.name}")
        if self.mech == "tier" and (q(self.power(ONE)) != ONE or not (0 <= q(self.power(ONE - self.x)) <= 1)):
            raise ValueError(f"invalid performance-power curve for {self.name}")


WALL = Arm("WALL", "wall", "wall")
OWN = Arm("OWN", "own", "wall")
ETM = Arm("ETM", "own", "own")
H0 = Arm("H0", "own", "wall", h0=True)
H0_WALL = Arm("H0-wall", "wall", "wall", h0=True)


def tier(x, window=None, power=power_linear, value_clock="own", overhead=ZERO, name=None) -> Arm:
    """TIER: the industry slowdown-tier contract (a pre-agreed maximum performance reduction x over a window): during an
    offered event the job runs at throughput 1 - x for min(H, window) hours (a throttle; own overhead `overhead`, default 0,
    no checkpoint); deadline on the wall clock; valued on the own clock unless value_clock='wall'."""
    x = q(x)
    nm = name or f"TIER-{g(x)}" + ("" if window is None else f"/{g(window)}h")
    return Arm(nm, value_clock, "wall", "tier", x, None if window is None else q(window), power, ZERO, q(overhead))


class Model:
    """A job under an arm: the per-event arithmetic, linear in (n, L) with n events accepted and L the curtailed contract
    hours (sum of h_eff); the terminal valuation."""
    __slots__ = ("job", "arm", "e1", "dw1", "o", "g_wall", "c_wall")

    def __init__(self, job: Job, arm: Arm):
        self.job, self.arm = job, arm
        if arm.mech == "pause":
            self.e1, self.dw1, self.o = ONE - arm.idle, ONE, job.overhead
        else:
            self.e1, self.dw1, self.o = ONE - q(arm.power(ONE - arm.x)), arm.x, arm.tier_overhead
        self.g_wall = arm.deadline_clock == "wall"
        self.c_wall = arm.value_clock == "wall"

    def heff(self, H: Fr) -> Fr:
        return min(H, self.arm.window) if (self.arm.mech == "tier" and self.arm.window is not None) else H

    def dw(self, n, L) -> Fr:
        """Wall-clock delay of the job after n events of L curtailed contract hours."""
        return self.dw1 * L + n * self.o

    def g(self, n, L) -> Fr:
        """Deadline budget used: the wall delay (wall-clock deadline) or the own overhead only (own-step deadline)."""
        return self.dw(n, L) if self.g_wall else n * self.o

    def charge(self, n, L) -> Fr:
        return self.job.rate * (self.dw(n, L) if self.c_wall else n * self.o)

    def energy(self, L) -> Fr:
        return self.e1 * L

    def met(self, n, L) -> bool:
        return self.job.W + self.g(n, L) <= self.job.D

    def vjob(self, n, L) -> Fr:
        return (self.job.value if self.met(n, L) else ZERO) - self.charge(n, L)

    def running(self, t, n, L) -> bool:
        return t < self.job.W + self.dw(n, L)

    def completion(self, n, L) -> Fr:
        return self.job.W + self.dw(n, L)


def event(job: Job, arm: Arm, H) -> dict:
    """The per-event quantities of one accepted event of offered length H under the arm (for printing CHOICE lines)."""
    m = Model(job, arm)
    he = m.heff(q(H))
    return dict(h_eff=he, e=m.e1 * he, own_overhead=m.o, wall_delay=m.dw(1, he), deadline_use=m.g(1, he), charge=m.charge(1, he))


def met(job, arm, n, L) -> bool:
    return Model(job, arm).met(n, q(L))


def vjob(job, arm, n, L) -> Fr:
    """The arm's valuation of the job after n accepted events of L curtailed contract hours (payments excluded)."""
    return Model(job, arm).vjob(n, q(L))


def stake(job: Job, arm: Arm, H, n: int = 0, L=None) -> Fr:
    """The one-event stake V(no event) - V(event) under the arm's valuation, from the state (n, L) (default L = n h_eff:
    identical offers of length H)."""
    m = Model(job, arm)
    he = m.heff(q(H))
    L = n * he if L is None else q(L)
    return m.vjob(n, L) - m.vjob(n + 1, L + he)


def nmax(job: Job, arm: Arm, H):
    """The most identical events (length H) the arm's deadline clock absorbs: max n with W + n g_1 <= D (EPS2's nmax1);
    None if an event uses no deadline budget (unbounded)."""
    m = Model(job, arm)
    per = m.g(1, m.heff(q(H)))
    if per == 0:
        return None
    return math.floor((job.D - job.W) / per)


# ============================================================================================ exact backward induction
def _prices(pi, K) -> list[Fr]:
    if isinstance(pi, (list, tuple)):
        if len(pi) != K:
            raise ValueError("one price per offer")
        return [q(p) for p in pi]
    return [q(pi)] * K


def _check(m: Model, offers) -> None:
    for a, b in zip(offers, offers[1:]):
        need = a.t + a.H + (m.o if m.arm.mech == "pause" else ZERO)
        if b.t < need:
            raise ValueError(f"offers overlap: an offer at hour {g(b.t)} before the event at {g(a.t)} and its overhead end ({g(need)})")


def _reach(m: Model, offers) -> list[list]:
    """The (n, L) states reachable before each offer k (k = 0..K), sorted."""
    S = [[(0, ZERO)]]
    for of in offers:
        he = m.heff(of.H)
        nxt = set(S[-1])
        for (n, L) in S[-1]:
            if m.running(of.t, n, L):
                nxt.add((n + 1, L + he))
        S.append(sorted(nxt))
    return S


class Solution(NamedTuple):
    value: Fr     # expected fleet value (valuation + payments) at the start
    dec: dict     # {(k, n, L): accept?} at every reachable state where the job runs at offer k
    V: list       # V[k][(n, L)]: expected fleet value from offer k on (V[K]: the valuation)


def solve(job: Job, arm: Arm, offers, pi) -> Solution:
    """Exact backward induction at payments pi (one flat value, or one per offer), ties accept (EPS2's dp1). With p < 1 an
    offer is made with probability p and the value is the exact expectation."""
    if arm.h0:
        raise ValueError("H0 is a contract, not a per-offer decision: use h0_price / play")
    m = Model(job, arm)
    _check(m, offers)
    K = len(offers)
    prices = _prices(pi, K)
    S = _reach(m, offers)
    V = {s: m.vjob(*s) for s in S[K]}
    Vs = [None] * (K + 1)
    Vs[K] = V
    dec = {}
    for k in range(K - 1, -1, -1):
        of = offers[k]
        he = m.heff(of.H)
        pay = prices[k] * m.e1 * he
        cur = {}
        for (n, L) in S[k]:
            B = V[(n, L)]
            if m.running(of.t, n, L):
                A = pay + V[(n + 1, L + he)]
                acc = A >= B
                dec[(k, n, L)] = acc
                best = A if acc else B
                cur[(n, L)] = best if of.p == 1 else of.p * best + (1 - of.p) * B
            else:
                cur[(n, L)] = B
        V = cur
        Vs[k] = cur
    return Solution(V[(0, ZERO)], dec, Vs)


def _h0_terms(m: Model, offers, prices) -> tuple[Fr, Fr, Fr]:
    """H0's contract (every offer that is made is curtailed while the job runs): expected payments, expected opportunity
    cost V(0) - E[V(final)], expected curtailed fleet-hours."""
    dist = {(0, ZERO): ONE}
    pay = ZERO
    for k, of in enumerate(offers):
        he = m.heff(of.H)
        new = {}
        for (n, L), w in dist.items():
            if m.running(of.t, n, L):
                s1 = (n + 1, L + he)
                new[s1] = new.get(s1, ZERO) + w * of.p
                pay += w * of.p * prices[k] * m.e1 * he
                if of.p < 1:
                    new[(n, L)] = new.get((n, L), ZERO) + w * (1 - of.p)
            else:
                new[(n, L)] = new.get((n, L), ZERO) + w
        dist = new
    loss = m.vjob(0, ZERO) - sum(w * m.vjob(n, L) for (n, L), w in dist.items())
    energy = sum(w * m.energy(L) for (n, L), w in dist.items())
    return pay, loss, energy


def h0_price(job: Job, offers, arm: Arm = H0) -> Fr | None:
    """H0 (EPS2 T1): an interruptible-load contract covering every offered event, curtailment mandatory once enrolled; its
    reservation price per curtailed fleet-hour = the job's expected opportunity cost of all contracted events / the expected
    curtailed fleet-hours, under the arm's valuation (H0: OWN's valuation, wall-clock deadline; H0_WALL: EPS2's H0-wall).
    None if no event can be contracted."""
    m = Model(job, arm)
    _, loss, energy = _h0_terms(m, offers, [ZERO] * len(offers))
    return None if energy == 0 else loss / energy


def _h0_enrols(job, arm, offers, prices) -> bool:
    """H0 enrols iff the contract's expected payments cover its expected opportunity cost (ties enrol); with a flat pi this
    is pi >= h0_price (EPS2)."""
    m = Model(job, arm)
    pay, loss, energy = _h0_terms(m, offers, prices)
    return energy > 0 and pay >= loss


def h0_cap(job: Job, offers, pi, arm: Arm = H0) -> int:
    """EPS2's H0-cap context: the same contract with a fleet-chosen cap (the first m live offers; ties to the larger cap):
    returns the number of contracted events maximising payments + valuation. Offers with p = 1 only."""
    m = Model(job, arm)
    if any(of.p != 1 for of in offers):
        raise ValueError("h0_cap needs a known schedule (p = 1)")
    prices = _prices(pi, len(offers))
    n, L, pay = 0, ZERO, ZERO
    best, arg = pay + m.vjob(n, L), 0
    for k, of in enumerate(offers):
        if m.running(of.t, n, L):
            he = m.heff(of.H)
            pay += prices[k] * m.e1 * he
            n, L = n + 1, L + he
        v = pay + m.vjob(n, L)
        if v >= best:
            best, arg = v, n
    return arg


def play(job: Job, arm: Arm, offers, pi, P_MW=ONE, made=None, sol: Solution | None = None) -> dict:
    """One season: the arm's decisions at payments pi along the realisation `made` (one bool per offer; default every offer
    is made). H0 enrols for the season iff its payments cover its opportunity cost, then curtails every live offer.
    Returns events, curtailed fleet-hours and MWh (P_MW per fleet-hour), payments, valuation, fleet value, whether the
    deadline is met on the arm's contract, and the wall-clock completion (and hours past D)."""
    m = Model(job, arm)
    K = len(offers)
    prices = _prices(pi, K)
    made = [True] * K if made is None else list(made)
    if arm.h0:
        enrol = _h0_enrols(job, arm, offers, prices)
    else:
        sol = sol or solve(job, arm, offers, prices)
    n, L, pay, acc, live = 0, ZERO, ZERO, [], 0
    for k, of in enumerate(offers):
        if not made[k] or not m.running(of.t, n, L):
            continue
        live += 1
        if (enrol if arm.h0 else sol.dec[(k, n, L)]):
            he = m.heff(of.H)
            pay += prices[k] * m.e1 * he
            n, L = n + 1, L + he
            acc.append(k)
    E = m.energy(L)
    val = m.vjob(n, L)
    comp = m.completion(n, L)
    return dict(arm=arm.name, live=live, events=n, accepted=tuple(acc), L=L, fleet_hours=E, MWh=E * q(P_MW), payments=pay,
                valuation=val, fleet_value=val + pay, met=m.met(n, L), completion=comp, past_D=comp - job.D)


def expect(job: Job, arm: Arm, offers, pi, P_MW=ONE, sol: Solution | None = None) -> dict:
    """The exact expectation over which offers are made (each independently with its p) under the optimal policy at pi
    (H0: its contract): expected live offers, events, curtailed fleet-hours and MWh, payments, valuation, P(deadline met on
    the arm's contract), fleet value (equal to solve().value, checked by the selftest), expected completion hour."""
    m = Model(job, arm)
    K = len(offers)
    prices = _prices(pi, K)
    if arm.h0:
        enrol = _h0_enrols(job, arm, offers, prices)
    else:
        sol = sol or solve(job, arm, offers, prices)
    dist = {(0, ZERO): ONE}
    pay = live = ZERO
    for k, of in enumerate(offers):
        he = m.heff(of.H)
        new = {}
        for (n, L), w in dist.items():
            if m.running(of.t, n, L):
                live += w * of.p
                if (enrol if arm.h0 else sol.dec[(k, n, L)]):
                    s1 = (n + 1, L + he)
                    new[s1] = new.get(s1, ZERO) + w * of.p
                    pay += w * of.p * prices[k] * m.e1 * he
                    if of.p < 1:
                        new[(n, L)] = new.get((n, L), ZERO) + w * (1 - of.p)
                    continue
            new[(n, L)] = new.get((n, L), ZERO) + w
        dist = new
    ev = sum(w * n for (n, L), w in dist.items())
    Lx = sum(w * L for (n, L), w in dist.items())
    val = sum(w * m.vjob(n, L) for (n, L), w in dist.items())
    pmet = sum(w for (n, L), w in dist.items() if m.met(n, L))
    comp = sum(w * m.completion(n, L) for (n, L), w in dist.items())
    E = m.energy(Lx)
    return dict(arm=arm.name, live=live, events=ev, L=Lx, fleet_hours=E, MWh=E * q(P_MW), payments=pay, valuation=val,
                fleet_value=val + pay, p_met=pmet, completion=comp, dist=dist)


def fleet_play(jobs: Sequence[Job], arm: Arm, offers, pi, P_MW) -> dict:
    """A portfolio: each job plays the same offers on its own backward induction at payments pi; P_MW is one power per job
    or one value for every job. Returns the totals (events, curtailed MWh, payments, jobs meeting their deadline) and the
    per-job rows."""
    Ps = [q(p) for p in P_MW] if isinstance(P_MW, (list, tuple)) else [q(P_MW)] * len(jobs)
    rows = [play(j, arm, offers, pi, P) for j, P in zip(jobs, Ps)]
    return dict(arm=arm.name, jobs=len(rows), events=sum(r["events"] for r in rows), MWh=sum((r["MWh"] for r in rows), ZERO),
                payments=sum((r["payments"] for r in rows), ZERO), met=sum(int(r["met"]) for r in rows),
                participating=sum(int(r["events"] > 0) for r in rows), rows=rows)


def response_ok(job: Job, T) -> bool:
    """A lossless pause meets a product with response time T only if the checkpoint save fits before the power drops."""
    return job.S <= q(T)


def lossy(job: Job, ckpt_interval) -> Job:
    """The pause without a save before the power drops: the job loses the work since its last periodic checkpoint,
    ckpt_interval / 2 in expectation (CHOICE: the event's phase uniform over the interval), redone as own running hours
    without progress; S = 0."""
    return replace(job, S=ZERO, lost=q(ckpt_interval) / 2)


# ============================================================================================ value functions in pi
def _hull(lines) -> list[tuple[Fr, Fr]]:
    """The upper envelope of lines (slope, intercept) over the whole real line, slopes strictly increasing."""
    ded = {}
    for m_, b_ in lines:
        if m_ not in ded or b_ > ded[m_]:
            ded[m_] = b_
    hull = []
    for m_ in sorted(ded):
        b_ = ded[m_]
        while len(hull) >= 2:
            (m1, b1), (m2, b2) = hull[-2], hull[-1]
            if (b1 - b_) * (m2 - m1) <= (b1 - b2) * (m_ - m1):     # the middle line is never strictly on top
                hull.pop()
            else:
                break
        hull.append((m_, b_))
    return hull


class CPL:
    """A convex piecewise-linear function of the flat payment pi on the whole real line, held exactly as the upper envelope
    of lines pi -> m pi + b (slopes strictly increasing; breakpoints bp strictly increasing)."""
    __slots__ = ("m", "b", "bp")

    def __init__(self, lines, hulled: bool = False):
        lines = lines if hulled else _hull(lines)
        self.m = tuple(l[0] for l in lines)
        self.b = tuple(l[1] for l in lines)
        self.bp = tuple((self.b[i] - self.b[i + 1]) / (self.m[i + 1] - self.m[i]) for i in range(len(lines) - 1))

    @classmethod
    def const(cls, v) -> "CPL":
        return cls([(ZERO, v)], True)

    def idx(self, x) -> int:
        return bisect.bisect_right(self.bp, x)

    def __call__(self, x) -> Fr:
        i = self.idx(x)
        return self.m[i] * x + self.b[i]

    def lines(self) -> list:
        return list(zip(self.m, self.b))

    def shift(self, e) -> "CPL":
        """f(pi) + e pi."""
        return CPL([(m_ + e, b_) for m_, b_ in zip(self.m, self.b)], True)

    def scale(self, a) -> "CPL":
        """a f(pi), a >= 0."""
        if a == 0:
            return CPL.const(ZERO)
        return CPL([(a * m_, a * b_) for m_, b_ in zip(self.m, self.b)], True)

    @staticmethod
    def vmax(f: "CPL", h: "CPL") -> "CPL":
        return CPL(f.lines() + h.lines())

    @staticmethod
    def add(f: "CPL", h: "CPL") -> "CPL":
        xs = sorted(set(f.bp) | set(h.bp))
        probes = [ZERO] if not xs else [xs[0] - 1] + [(a + b) / 2 for a, b in zip(xs, xs[1:])] + [xs[-1] + 1]
        out = []
        for x in probes:
            i, j = f.idx(x), h.idx(x)
            out.append((f.m[i] + h.m[j], f.b[i] + h.b[j]))
        return CPL(out)


def value_fns(job: Job, arm: Arm, offers) -> list[dict]:
    """The expected fleet value from each offer on, as an exact convex piecewise-linear function of a flat payment pi, at
    every reachable state: F[k][(n, L)] for k = 0..K (F[K]: the valuation, constant in pi)."""
    if arm.h0:
        raise ValueError("H0 is a contract: use h0_price")
    m = Model(job, arm)
    _check(m, offers)
    K = len(offers)
    S = _reach(m, offers)
    F = [None] * (K + 1)
    F[K] = {s: CPL.const(m.vjob(*s)) for s in S[K]}
    for k in range(K - 1, -1, -1):
        of = offers[k]
        he = m.heff(of.H)
        e = m.e1 * he
        nxt, cur = F[k + 1], {}
        for (n, L) in S[k]:
            B = nxt[(n, L)]
            if m.running(of.t, n, L):
                best = CPL.vmax(nxt[(n + 1, L + he)].shift(e), B)
                cur[(n, L)] = best if of.p == 1 else CPL.add(best.scale(of.p), B.scale(1 - of.p))
            else:
                cur[(n, L)] = B
        F[k] = cur
    return F


class XStar(NamedTuple):
    x: Fr | None      # the minimum acceptable flat payment per curtailed fleet-hour (None unless kind == 'threshold')
    attained: bool    # accepting is optimal at x itself (ties accept)
    closed: bool      # no acceptance below x: the acceptance region is [x, infinity)
    kind: str         # 'threshold' | 'always' (accepts at every pi) | 'never' (no final acceptance interval) | 'idle' (job not running)


def _threshold(A: CPL, B: CPL) -> XStar:
    """The start of the final interval of pi on which A(pi) >= B(pi) (accept vs decline), exactly: A - B is linear between
    the union of both breakpoint sets, so the last sign change is a root of one linear piece."""
    pts = sorted(set(A.bp) | set(B.bp)) or [ZERO]
    d = [A(x) - B(x) for x in pts]
    sl_l, sl_r = A.m[0] - B.m[0], A.m[-1] - B.m[-1]
    if sl_r < 0 or (sl_r == 0 and d[-1] < 0):
        return XStar(None, False, all(v < 0 for v in d) and sl_l >= 0, "never")
    x = None
    if d[-1] < 0:
        x = pts[-1] - d[-1] / sl_r
    else:
        for i in range(len(pts) - 1, 0, -1):
            if d[i - 1] < 0:
                x = pts[i - 1] - d[i - 1] * (pts[i] - pts[i - 1]) / (d[i] - d[i - 1])
                break
        if x is None:
            if sl_l > 0:
                x = pts[0] - d[0] / sl_l
            else:
                return XStar(None, True, True, "always")
    closed = all(v < 0 for p_, v in zip(pts, d) if p_ < x) and (sl_l >= 0 if pts[0] < x else sl_l > 0)
    return XStar(x, A(x) - B(x) >= 0, closed, "threshold")


def xstar(job: Job, arm: Arm, offers, k: int, n: int, L=None, F=None) -> XStar:
    """The minimum acceptable payment per curtailed fleet-hour at offer k (0-based) in state (n, L) (default L = n h_eff of
    this offer's length: identical offers), the rest of the season at the same flat pi and played optimally (EPS2's x*)."""
    m = Model(job, arm)
    F = F or value_fns(job, arm, offers)
    of = offers[k]
    he = m.heff(of.H)
    L = n * he if L is None else q(L)
    if not m.running(of.t, n, L):
        return XStar(None, False, True, "idle")
    return _threshold(F[k + 1][(n + 1, L + he)].shift(m.e1 * he), F[k + 1][(n, L)])


def xstar_all(job: Job, arm: Arm, offers, F=None) -> dict:
    """x* at every reachable state where the job runs: {(k, n, L): XStar}."""
    m = Model(job, arm)
    F = F or value_fns(job, arm, offers)
    out = {}
    for k, of in enumerate(offers):
        he = m.heff(of.H)
        for (n, L) in sorted(F[k]):
            if m.running(of.t, n, L):
                out[(k, n, L)] = _threshold(F[k + 1][(n + 1, L + he)].shift(m.e1 * he), F[k + 1][(n, L)])
    return out


def accepts_at(xs: XStar, pi) -> bool:
    """The acceptance rule implied by x*: accept iff pi > x, or pi == x and attained (EPS2's DP=x* rule)."""
    if xs.kind == "always":
        return True
    if xs.kind in ("never", "idle"):
        return False
    return pi > xs.x or (pi == xs.x and xs.attained)


class PAll(NamedTuple):
    x: Fr | None      # the minimum flat payment at which the arm accepts every offer that is made (None: never; see kind)
    attained: bool
    closed: bool      # every state's acceptance region is [x*, infinity)
    kind: str         # 'threshold' | 'always' | 'never'
    states: list      # [((k, n, L), XStar)] along the accept-every-made-offer states


def p_all(job: Job, arm: Arm, offers, F=None) -> PAll:
    """EPS2's decisive reading: the minimum flat payment at which the arm accepts every offer of the season, i.e. the largest
    x* over the states reached when every made offer is accepted (p = 1: the single all-accept path). H0: its reservation
    price."""
    if arm.h0:
        x = h0_price(job, offers, arm)
        return PAll(x, True, True, "threshold" if x is not None else "never", [])
    m = Model(job, arm)
    F = F or value_fns(job, arm, offers)
    frontier = {(0, ZERO)}
    st = []
    for k, of in enumerate(offers):
        he = m.heff(of.H)
        nxt = set()
        for (n, L) in sorted(frontier):
            if m.running(of.t, n, L):
                st.append(((k, n, L), _threshold(F[k + 1][(n + 1, L + he)].shift(m.e1 * he), F[k + 1][(n, L)])))
                nxt.add((n + 1, L + he))
                if of.p < 1:
                    nxt.add((n, L))
            else:
                nxt.add((n, L))
        frontier = nxt
    if any(xs.kind == "never" for _, xs in st):
        return PAll(None, False, all(xs.closed for _, xs in st), "never", st)
    th = [xs.x for _, xs in st if xs.kind == "threshold"]
    if not th:
        return PAll(None, True, True, "always", st)
    x = max(th)
    att = all(xs.attained for _, xs in st if xs.kind == "threshold" and xs.x == x)
    return PAll(x, att, all(xs.closed for _, xs in st), "threshold", st)


def rule_xstar(job: Job, arm: Arm, H, n: int, m_future) -> Fr | None:
    """Closed form for identical offers (length H), a flat payment, every future offer finding the job running and made
    independently of the fleet's decisions, m_future = the expected number of offers after this one. With e the curtailed
    fleet-hours and c the charge per event, u = pi e - c:
        x* = c / e                                  unless accepting now loses the job,
        x* = (c + W rate / (1 + m_future)) / e      at zero slack (n == nmax: n + 1 events miss the deadline).
    Derivation. (i) n != nmax: if u >= 0, from n + 1 copy the optimal plan from n but skip its first acceptance; this ends
    in the same state (or at n + 1 <= nmax, still meeting the deadline, if the plan accepted nothing), so
    u + V(n + 1) >= V(n) and accepting is optimal (ties accept); if u < 0, accepting only adds charges and the terminal
    value never rises with n, so declining is optimal. (ii) n == nmax, u >= 0: accepting loses the job and then every later
    offer is worth u, so it is worth u (1 + m_future); declining is worth at least W rate (never accept again) and at most
    max(W rate, u (1 + m')) with m' <= m_future the expected count after a later offer; so accept iff
    u (1 + m_future) >= W rate. With u < 0 decline. None if an event curtails no energy (e = 0)."""
    m = Model(job, arm)
    H = q(H)
    he = m.heff(H)
    e, c = m.e1 * he, m.charge(1, he) - m.charge(0, ZERO)
    if e == 0:
        return None
    nm = nmax(job, arm, H)
    if nm is not None and n == nm:
        return (c + job.value / (1 + q(m_future))) / e
    return c / e


def poisson_xstar(job: Job, arm: Arm, H, lam, t, t_end, n: int) -> Fr | None:
    """rule_xstar for offers arriving as a continuous-time Poisson process of rate lam per wall hour on [t, t_end) (unknown
    count; CHOICES: events do not block later arrivals and every arrival finds the job running, t_end <= W): the expected
    count after an offer at t is lam (t_end - t)."""
    return rule_xstar(job, arm, H, n, q(lam) * (q(t_end) - q(t)))


# ============================================================================================ selftest: EPS2 T1 reproduced
def _eps2_cells(W, R, Ds, Hs, spacing, grid):
    cells = {}
    for D in Ds:
        for H in Hs:
            job = Job(W, D, R)
            offs = every(spacing, H, job.W)
            K = len(offs)
            c = {}
            for arm in (WALL, OWN, ETM):
                F = value_fns(job, arm, offs)
                xs = xstar_all(job, arm, offs, F)
                pa = p_all(job, arm, offs, F)
                sols = {pi: solve(job, arm, offs, pi) for pi in grid}
                plays = {pi: play(job, arm, offs, pi, sol=sols[pi]) for pi in grid}
                agree = sum(int(accepts_at(x, pi) == sols[pi].dec[st]) for pi in grid for st, x in xs.items())
                at = play(job, arm, offs, pa.x)["events"]
                below = play(job, arm, offs, pa.x - Fr(1, 10 ** 6))["events"]
                c[arm.name] = dict(xs=xs, pa=pa, plays=plays, agree=agree, total=len(xs) * len(grid),
                                   closed_fail=sum(int(not x.closed) for x in xs.values()), nmax=nmax(job, arm, H),
                                   stakes=[stake(job, arm, H, n) for n in range(K)], verify=((at == K) == pa.attained) and below < K)
            c["H0"] = dict(pa=h0_price(job, offs, H0), pw=h0_price(job, offs, H0_WALL),
                           plays={pi: play(job, H0, offs, pi) for pi in grid})
            c["cap_same"] = all(h0_cap(job, offs, pi) == c["OWN"]["plays"][pi]["events"] for pi in grid)
            cells[(D, H)] = dict(job=job, offs=offs, K=K, c=c)
    return cells


def _brute(m: Model, offs, pi, first=None):
    """Best plan value over every subset of offers (p = 1), respecting the running condition; first = True/False restricts
    to plans that accept / decline offer 0."""
    best = None
    for mask in range(1 << len(offs)):
        if first is not None and bool(mask & 1) != first:
            continue
        n, L, pay, ok = 0, ZERO, ZERO, True
        for k, of in enumerate(offs):
            if mask >> k & 1:
                if not m.running(of.t, n, L):
                    ok = False
                    break
                he = m.heff(of.H)
                pay += pi * m.e1 * he
                n, L = n + 1, L + he
        if ok:
            v = pay + m.vjob(n, L)
            best = v if best is None or v > best else best
    return best


def selftest() -> bool:
    res = []

    def rec(name, ok, detail=""):
        res.append((name, ok))
        print(f"  [{'match' if ok else 'MISMATCH'}] {name}{(': ' + detail) if detail else ''}")

    print(f"DR1 drlib selftest (Grid_Demand_Response/DECLARATION.md, declared at {DECL_AT}; the library adds no prediction)")
    print("Part 1 reproduces EPS2 T1 (Empty_Pause_Systems/batches/eps2_01.py) with the general engine (convex piecewise-linear value")
    print("functions in pi, exact rational arithmetic) and compares with the pinned output Empty_Pause_Systems/batches/eps2_01.txt.")
    print("Inputs (EPS2 T1's; none is a DR1 source number):")
    print("  W = 1000 compute-hours, value 1 per compute-hour at completion: DECLARED (DR1 section 2 adopts EPS2 T1's units)")
    print("  R = 0.1 h per event, D in {1100, 1500} h, H in {1, 4} h: ASSUMED (EPS2 T1 model constants; no fetched source supplies R,")
    print("    docs/citations/eps2_2026-09-29.md, Reading (T1)); S = 0 and lost = 0: CHOICE (EPS2 has neither)")
    print("  one offer every 24 wall hours at hours 24..984 (K = 41), spacing 12 and 48 h as EPS2's sensitivity: CHOICE (EPS2 T1)")
    print("  payment grid {0.01, 0.02, 0.05, 0.2, 0.5, 2, 5, 10, 20} per curtailed fleet-hour: ASSUMED (EPS2 T1)")
    print()
    pinned = EPS2_TXT.read_text(encoding="utf-8").splitlines()
    pinset = set(pinned)
    numline = next(l for l in pinned if l.lstrip().startswith("numbers:") and "p_all" in l)

    W, R = Fr(1000), Fr(1, 10)
    Ds, Hs = (Fr(1100), Fr(1500)), (Fr(1), Fr(4))
    D0, H0h = Fr(1100), Fr(4)
    grid = tuple(Fr(s) for s in ("0.01", "0.02", "0.05", "0.2", "0.5", "2", "5", "10", "20"))
    arms = ("WALL", "OWN", "ETM")
    cells = _eps2_cells(W, R, Ds, Hs, Fr(24), grid)
    K = cells[(D0, H0h)]["K"]

    # ---- block 1: the per-cell table and its verification line
    lines = []
    for (D, H), cl in cells.items():
        c = cl["c"]
        first = "/".join(f"{float(c[a]['xs'][(0, 0, ZERO)].x):.4f}" for a in arms)
        agr = sum(c[a]["agree"] for a in arms)
        tot = sum(c[a]["total"] for a in arms)
        cf = sum(c[a]["closed_fail"] for a in arms)
        lines.append(f"{g(D):>5} {g(H):>2} {cl['K']:>3} {c['OWN']['nmax']:>9} {c['ETM']['nmax']:>9} {float(c['WALL']['pa'].x):>12.6f} "
                     f"{float(c['OWN']['pa'].x):>12.6f} {float(c['ETM']['pa'].x):>10.6f} {float(c['H0']['pa']):>10.6f} {float(c['H0']['pw']):>10.6f} "
                     f"{first:>22} {agr:>6}/{tot:<6} {cf:>7}")
    ver = all(cl["c"][a]["verify"] for cl in cells.values() for a in arms)
    lines.append(f" region has a part below x*, expected 0; p_all verified by backward induction at p_all and at p_all - {1e-06:g} in every cell and arm: {yn(ver)})")
    print("Block 1, the per-cell table (p_all per arm, H0, H0-wall, x* at the first offer, DP = x* rule over every state and grid pi):")
    for l in lines:
        print("  " + l)
    rec("per-cell table lines found verbatim in eps2_01.txt", all(l in pinset for l in lines), f"{sum(l in pinset for l in lines)} of {len(lines)}")

    # ---- block 2: the decisive cell along the all-accept path
    dc = cells[(D0, H0h)]["c"]
    lines = []
    for k in range(1, K + 1):
        n = k - 1
        ws = D0 - W - n * (H0h + R)
        os_ = D0 - W - n * R
        xw, xo, xe = (dc[a]["xs"][(k - 1, n, n * H0h)].x for a in arms)
        lines.append(f"{k:>3} {g(24 * k):>5} {n:>3} {float(ws):>13.1f} {float(os_):>12.1f} {float(xw):>12.6f} {float(xo):>12.6f} {float(xe):>9.6f} "
                     f"{float(dc['WALL']['stakes'][n]):>10.4f} {float(dc['OWN']['stakes'][n]):>10.4f} {float(dc['ETM']['stakes'][n]):>7.4f}")
    print(f"Block 2, the decisive cell D = 1100, H = 4 along the all-accept path (x* per arm and one-event stakes; {len(lines)} lines, not reprinted):")
    rec("decisive-path lines found verbatim in eps2_01.txt", all(l in pinset for l in lines), f"{sum(l in pinset for l in lines)} of {len(lines)}")

    # ---- block 3: commercial quantity
    lines = []
    for (D, H), cl in cells.items():
        c = cl["c"]
        lines.append(f"  D = {g(D)}, H = {g(H)} (K = {cl['K']}):  pi = " + " ".join(f"{g(p):>7}" for p in grid))
        for a in ("WALL", "OWN", "ETM", "H0"):
            ps = [c[a]["plays"][p] for p in grid]
            lines.append(f"    {a:5} events   " + " ".join(f"{r['events']:>5}{('y' if r['met'] else 'n'):>2}" for r in ps))
            lines.append(f"    {a:5} revenue  " + " ".join(f"{float(r['payments']):>7.1f}" for r in ps))
        lines.append(f"    H0-cap events equal OWN's at every pi: {yn(c['cap_same'])}")
    print(f"Block 3, the commercial quantity per cell (events accepted, deadline met, revenue per arm and pi; {len(lines)} lines, not reprinted):")
    rec("commercial-quantity lines found verbatim in eps2_01.txt", all(l in pinset for l in lines), f"{sum(l in pinset for l in lines)} of {len(lines)}")

    # ---- block 4: offer-spacing sensitivity (prefix before the harness label, which this library does not compute)
    lines = []
    for sp in (Fr(12), Fr(24), Fr(48)):
        job = Job(W, D0, R)
        offs = every(sp, H0h, job.W)
        pe, po, pw = (p_all(job, a, offs).x for a in (ETM, OWN, WALL))
        lines.append(f"  spacing {g(sp):>2} h: K = {len(offs):>2}, OWN's slack absorbs {nmax(job, OWN, H0h)} events; p_all ETM {float(pe):.6f}, "
                     f"OWN {float(po):.6f}, WALL {float(pw):.6f}, H0 {float(h0_price(job, offs)):.6f} -> label with Q held: ")
    found = [any(pl.startswith(l) for pl in pinned) for l in lines]
    print("Block 4, the offer-spacing sensitivity (each line up to the harness label):")
    for l in lines:
        print("  " + l.rstrip())
    rec("offer-spacing lines found in eps2_01.txt (up to the label)", all(found), f"{sum(found)} of {len(found)}")

    # ---- block 5: the G-NEG world and EPS2's gate line
    neg = {a.name: [play(Job(W, D, R), a, (), p) for D in Ds for H in Hs for p in grid] for a in (WALL, OWN, ETM)}
    neg_h = {a: max(float(r["fleet_hours"]) for r in rs) for a, rs in neg.items()}
    neg_job = {a: min(r["valuation"] for r in rs) for a, rs in neg.items()}
    comps = {r["completion"] for rs in neg.values() for r in rs}
    he, hw = neg_h["ETM"], neg_h["WALL"]
    gneg_line = (f"G-NEG world (no events offered, K = 0; every cell and pi): curtailed hours delivered WALL {hw:g}, OWN {neg_h['OWN']:g}, ETM {he:g}; "
                 f"job value {', '.join(f'{a} {float(v):g}' for a, v in neg_job.items())}; completion at wall hour "
                 f"{(g(min(comps)) if len(comps) == 1 else 'that differs by arm')} for every arm")
    stake_beyond = [abs(cl["c"]["ETM"]["stakes"][n] - R) for cl in cells.values() for n in range(cl["K"])]
    etm_x = [(x, H) for (D, H), cl in cells.items() for x in cl["c"]["ETM"]["xs"].values()]
    x_etm_ok = all(x.kind == "threshold" and x.x == R / H for x, H in etm_x)
    gz = max(stake_beyond) == 0 and x_etm_ok
    decl = {a: sum(int(cl["c"][a]["plays"][p]["events"] < cl["c"]["ETM"]["plays"][p]["events"]) for cl in cells.values() for p in grid)
            for a in ("WALL", "OWN")}
    gp = decl["WALL"] + decl["OWN"] > 0
    ahead_neg = he > hw and rel(he, hw) > 1e-2
    gn = not ahead_neg
    hv = lambda ok: "holds" if ok else "fails"
    gate_line = (f"GATE T1: G-ZERO {hv(gz)} (ETM's stake beyond the restart overhead, max |k - R| over {len(stake_beyond)} event counts in {len(cells)} cells = "
                 f"{float(max(stake_beyond)):g}, exact rational arithmetic; ETM's minimum acceptable payment == R/H at {'all' if x_etm_ok else 'not all'} "
                 f"{len(etm_x)} offer states); G-POS {hv(gp)} (WALL declines offers ETM accepts in {decl['WALL']} of {len(cells) * len(grid)} cell x pi "
                 f"combinations, OWN in {decl['OWN']}); G-NEG {hv(gn)} (no events offered: curtailed hours ETM {he:g} vs WALL {hw:g}, rel {rel(he, hw):.3e}, "
                 f"ETM {'ahead by more than 1 %' if ahead_neg else 'not ahead by more than 1 %'}) -> {'OPEN' if (gz and gp and gn) else 'CLOSED'}")
    print("Block 5, EPS2's G-NEG world and gate line:")
    print("  " + gneg_line)
    print("  " + gate_line)
    rec("G-NEG and gate lines found verbatim in eps2_01.txt", gneg_line in pinset and gate_line in pinset,
        f"{int(gneg_line in pinset) + int(gate_line in pinset)} of 2")

    # ---- block 6: the decisive numbers in the row's 'numbers' field
    pa = {a: dc[a]["pa"].x for a in arms}
    own0 = cells[(D0, H0h)]["c"]["OWN"]
    nm_dec = own0["nmax"]
    etm_all = dc["ETM"]["plays"][Fr("0.2")]
    subs = [
        f"ETM {float(pa['ETM']):.6f} (R/H = {float(R / H0h):.6f}), OWN {float(pa['OWN']):.12f}, WALL {float(pa['WALL']):.12f}, "
        f"H0 {float(dc['H0']['pa']):.12f}, H0-wall {float(dc['H0']['pw']):.6f}",
        "per cell: " + "; ".join(f"D {g(D)}, H {g(H)}: p_all WALL {float(cl['c']['WALL']['pa'].x):.6f}, OWN {float(cl['c']['OWN']['pa'].x):.6f}, "
                                 f"ETM {float(cl['c']['ETM']['pa'].x):.6f}, H0 {float(cl['c']['H0']['pa']):.6f}; OWN's slack absorbs up to "
                                 f"{cl['c']['OWN']['nmax']} events (K = {cl['K']})" for (D, H), cl in cells.items()),
        "minimum acceptable payment at the first offer (full slack) " + ", ".join(f"{a} {float(dc[a]['xs'][(0, 0, ZERO)].x):.6f}" for a in arms),
        f"at the decisive cell OWN's x* is {float(R / H0h):.6f} while at least one event of slack remains and {float(pa['OWN']):.6f} at zero slack "
        f"with {K - nm_dec} offers left",
        "commercial quantity at the decisive cell: " + "; ".join(
            f"pi {g(p)}: " + ", ".join(f"{a} {dc[a]['plays'][p]['events']}/{K} events, revenue {float(dc[a]['plays'][p]['payments']):.1f}"
                                        for a in ("WALL", "OWN", "ETM", "H0")) for p in (Fr("0.2"), Fr("2"), Fr("10"))),
        f"grid's curtailed hours when ETM accepts all: {float(etm_all['fleet_hours']):g} h, and ETM's wall completion {float(etm_all['completion']):.1f} h "
        f"({float(etm_all['past_D']):.1f} h past D on the wall clock, inside its own-step deadline)",
    ]
    print("Block 6, substrings of the T1 row's 'numbers' field:")
    for s in subs:
        rec(f"'{s[:60]}...' in the pinned row", s in numline)

    # ---- the decisive numbers named in the task, against the pinned strings
    mt = re.search(r"ETM ([0-9.]+) \(R/H = [0-9.]+\), OWN ([0-9.]+), WALL ([0-9.]+), H0 ([0-9.]+), H0-wall ([0-9.]+)", numline)
    tab = next(l for l in pinned if l.startswith(" 1100  4  41"))
    pinned_dec = {"ETM": mt.group(1), "OWN": mt.group(2), "H0": mt.group(4), "WALL": tab.split()[5], "WALL (row)": mt.group(3)}
    mine = {"ETM": pa["ETM"], "OWN": pa["OWN"], "H0": dc["H0"]["pa"], "WALL": pa["WALL"], "WALL (row)": pa["WALL"]}
    print(f"Decisive numbers, D = 1100, H = 4, one offer every 24 wall hours at hours 24..984 (K = {K}): p_all per curtailed hour")
    print(f"  {'arm':10} {'exact':>12} {'drlib':>18} {'pinned':>18}")
    for a in ("ETM", "OWN", "H0", "WALL", "WALL (row)"):
        s = pinned_dec[a]
        dgt = len(s.split(".")[1]) if "." in s else 0
        ours = f"{float(mine[a]):.{dgt}f}"
        ok = ours == s
        res.append((f"decisive {a}", ok))
        print(f"  {a:10} {str(mine[a]):>12} {ours:>18} {s:>18}  {'match' if ok else 'MISMATCH'}")
    print()

    # ---- part 2: internal checks of the DR1 additions
    print("Part 2, internal checks of the DR1 additions (toy inputs, ASSUMED where printed):")
    job = Job(W, D0, R)
    offs = every(24, H0h, job.W)
    # (a) the Poisson-offer variant: backward induction against the closed form
    lam, slot = Fr(1, 48), Fr(24)
    poffs, err = poisson_slots(lam, slot, H0h, job.W)
    p = poffs[0].p
    print(f"  (a) Poisson-offer variant: rate lam = 1/48 per wall hour (ASSUMED), at most one event per 24 h slot (CHOICE), H = 4 h:")
    print(f"      p = 1 - exp(-lam slot) = {float(p):.9f} as the rational {p} (rounding error {err:.1e}); {len(poffs)} slots, E[offers] = "
          f"{float(sum(o.p for o in poffs)):.6f}")
    for arm in (WALL, OWN, ETM):
        F = value_fns(job, arm, poffs)
        xs = xstar_all(job, arm, poffs, F)
        good = sum(int(x.kind == "threshold" and x.closed and x.attained
                       and x.x == rule_xstar(job, arm, H0h, n, sum((o.p for o in poffs[k + 1:]), ZERO))) for (k, n, L), x in xs.items())
        vals = [(solve(job, arm, poffs, pi).value, F[0][(0, ZERO)](pi), expect(job, arm, poffs, pi)["fleet_value"]) for pi in grid]
        rec(f"{arm.name}: x* by backward induction == rule_xstar (m_future = sum of later p) at every state", good == len(xs), f"{good} of {len(xs)}")
        rec(f"{arm.name}: solve().value == value function F[0](pi) == expect() fleet value at every grid pi", all(a == b == c for a, b, c in vals),
            f"{sum(int(a == b == c) for a, b, c in vals)} of {len(vals)}")
    own_zero = poisson_xstar(job, OWN, H0h, lam, 600, 1000, 24)
    print(f"      context: continuous Poisson, OWN at zero slack (n = 24) at hour 600 of an offer window ending at hour 1000: x* = {float(own_zero):.6f}")
    # (b) p = 1: expect() equals play()
    same = all(expect(job, a, offs, pi)["events"] == play(job, a, offs, pi)["events"]
               and expect(job, a, offs, pi)["fleet_value"] == play(job, a, offs, pi)["fleet_value"] for a in (WALL, OWN, ETM, H0) for pi in grid)
    rec("(b) known schedule (p = 1): expect() equals play() in events and fleet value, 4 arms x 9 pi", same)
    # (c) TIER plumbing
    full = tier(1, None, overhead=job.overhead)
    xs_t, xs_o = xstar_all(job, full, offs), xstar_all(job, OWN, offs)
    rec("(c) TIER at x = 1 with the pause's overhead equals OWN (x* at every state, p_all)",
        xs_t == xs_o and p_all(job, full, offs).x == p_all(job, OWN, offs).x, f"{sum(int(xs_t[s] == xs_o[s]) for s in xs_o)} of {len(xs_o)} states")
    thr = tier(Fr(1, 4), Fr(3))
    pt = p_all(job, thr, offs)
    ev = event(job, thr, H0h)
    rec("(c) TIER x = 0.25 over a 3 h window (linear power, ASSUMED; throttle overhead 0): p_all == its charge / energy per event",
        pt.kind == "threshold" and pt.x == ev["charge"] / ev["e"], f"p_all {g(pt.x)}; per event e = {g(ev['e'])} fleet-hours, wall delay {g(ev['wall_delay'])} h")
    # (d) the save time enters as own overhead
    js = Job(W, D0, Fr(1, 20), S=Fr(1, 20))
    rec("(d) Job(R = 0.05, S = 0.05) gives the same p_all as Job(R = 0.1) for WALL, OWN, ETM and H0",
        all(p_all(js, a, offs).x == p_all(job, a, offs).x for a in (WALL, OWN, ETM, H0)))
    rec("    response_ok: S = 0.05 h meets T = 0.05 h and not T = 0.04 h", response_ok(js, Fr(1, 20)) and not response_ok(js, Fr(1, 25)))
    # (e) heterogeneous lengths and the running condition, against brute force over every plan
    tj = Job(100, 112, Fr(1, 2))
    toffs = schedule([10, 20, 30, 40, 50, 60, 70, 80, 100, 106], [1, 3, 2, 4, 1, 3, 2, 4, 2, 3])
    tgrid = tuple(Fr(s) for s in ("0", "0.1", "0.3", "1", "2", "5", "20"))
    print("  (e) heterogeneous offers (toy, ASSUMED): W = 100, D = 112, R = 0.5; offers at hours 10..80, 100, 106 with lengths 1-4 h; the last two")
    print("      are live only if earlier events delayed completion past their hour; brute force over all 1024 plans:")
    for arm in (WALL, OWN, ETM, tier(Fr(1, 2), Fr(2))):
        m = Model(tj, arm)
        ok_v = all(solve(tj, arm, toffs, pi).value == _brute(m, toffs, pi) for pi in tgrid)
        x0 = xstar(tj, arm, toffs, 0, 0)
        if x0.kind == "threshold":
            lo = x0.x - Fr(1, 10 ** 6)
            ok_x = _brute(m, toffs, x0.x, True) >= _brute(m, toffs, x0.x, False) and _brute(m, toffs, lo, True) < _brute(m, toffs, lo, False)
            xs_txt = f"x* at the first offer {float(x0.x):.6f}"
        else:
            ok_x, xs_txt = False, f"x* kind {x0.kind}"
        rec(f"{arm.name}: backward-induction value == brute force at {len(tgrid)} pi; {xs_txt} is the brute-force indifference point", ok_v and ok_x)
    npass = sum(int(ok) for _, ok in res)
    allok = npass == len(res)
    print()
    print(f"{npass} of {len(res)} comparisons match")
    print("SELFTEST PASS" if allok else "SELFTEST FAIL")
    return allok


def main(argv) -> int:
    if len(argv) >= 2 and argv[1] == "selftest":
        return 0 if selftest() else 1
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

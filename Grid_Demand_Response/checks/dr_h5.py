"""DR1 check H5: rebound, N jobs resume together at the event's end.

Binding declaration: Grid_Demand_Response/DECLARATION.md (pushed at e67e8ee; never edited here), section 2, row H5:
  check:      rebound: N jobs resume together at the event's end
  Q:          a lossless pause resumes at full power at once, so the rebound peak equals the curtailed load; a staggered
              resume removes it at a cost; the cost of staggering is printed
  forecast:   Q holds (REDUNDANT: rebound is known)
This check also prints the gate's G-ZERO and G-NEG (G-POS belongs to H1).

The arithmetic is the shared library Grid_Demand_Response/checks/drlib.py (exact rational arithmetic; its selftest
reproduces EPS2 T1 line for line) plus an exact piecewise-linear fleet load profile written here (Fractions throughout).
Every verdict word printed here is computed from the numbers (R15). Every input number is either sourced (a verbatim quote
from docs/citations/dr1_f{1,3,4}_2026-09-29.md, checked against the dossier text at run time, the number parsed out of the
quote by a regular expression) or printed as ASSUMED; every modelling choice is printed as CHOICE. Rung R4 at most (a
synthetic model); a note, not evidence (R8). Deterministic, stdlib only (via drlib).

    cd /home/user/ashes_crr && uv run python Grid_Demand_Response/checks/dr_h5.py > Grid_Demand_Response/checks/dr_h5.txt
"""
from __future__ import annotations

import math
import re
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import drlib as d  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
CIT = REPO / "docs" / "citations"
DOSS = {k: f"dr1_{k.lower()}_2026-09-29.md" for k in ("F1", "F3", "F4")}
TEXT = {k: (CIT / v).read_text(encoding="utf-8") for k, v in DOSS.items()}
ZERO, ONE = Fr(0), Fr(1)
MIN, SEC = Fr(1, 60), Fr(1, 3600)                 # hours per minute, per second
TOL = Fr(1, 100)                                  # G-NEG's declared 1 %

# ------------------------------------------------------------------------------------------------ sourced inputs (quotes)
# Each source: id, dossier, citation, verbatim quote (a substring of the dossier), regex (None: qualitative, no number
# parsed), and the named values it yields (value id, group index, CHOICE note). Word numbers are mapped by WORDNUM.
WORDNUM = {"half": Fr(1, 2), "one": ONE, "four": Fr(4)}
SOURCES = [
    dict(id="NERC-L2", dos="F3", src="NERC, Level 2 alert aggregated report (alert 2025-09-09; report PDF 2026-03-17)",
         quote="The entities that did respond varied between 8 MW/min to 300 MW/min. Many responses that did include a load ramp limit largely fell between 10 MW/min and 30 MW/min.",
         rx=r"between (\d+) MW/min to (\d+) MW/min\. .*between (\d+) MW/min and (\d+) MW/min",
         vals=[("L2-lo", 1, "the lowest operational large-load ramp limit reported (normal operation), read as an up-ramp limit on the resume"),
               ("L2-hi", 2, "the highest reported limit, read as an up-ramp limit on the resume"),
               ("L2-typ-lo", 3, "the low end of the typical reported limits, read as an up-ramp limit"),
               ("L2-typ-hi", 4, "the high end of the typical reported limits, read as an up-ramp limit")]),
    dict(id="SO-cap", dos="F3", src="Zahedi et al., arXiv:2601.12686 v1",
         quote="Southern Company is the only company that enforces a numeric cap of ≤ 20 MW/min for load ramping under normal operation.",
         rx=r"cap of ≤ (\d+) MW/min",
         vals=[("SO", 1, "'≤ 20 MW/min' taken at its bound, read as an up-ramp limit on the resume")]),
    dict(id="NPRR-CLR", dos="F3", src="Galaxy comments on ERCOT NPRR1191 (NPRR withdrawn; a commenter's restatement)",
         quote="What is the rationale for the proposed ramp rate limitations of 20% per minute of registered peak demand for Controllable Load Resources (CLRs)?",
         rx=r"limitations of (\d+)% per minute of registered peak demand",
         vals=[("NPRR-CLR-pct", 1, "20 % of registered peak per minute; the fleet's 100 MW (ASSUMED) as the registered peak; withdrawn, not in force")]),
    dict(id="NPRR-nonCLR", dos="F3", src="Galaxy comments on ERCOT NPRR1191 (NPRR withdrawn; a commenter's restatement)",
         quote="Proposed ramp rate limitations (lesser of 5% of peak demand or 20 MW per minute ramp down, lesser of 2% of peak demand or 8 MW per minute ramp up)",
         rx=r"lesser of (\d+)% of peak demand or (\d+) MW per minute ramp down, lesser of (\d+)% of peak demand or (\d+) MW per minute ramp up",
         vals=[("NPRR-dn-pct", 1, "down-ramp: percent of peak (the event start, context only)"),
               ("NPRR-dn-MW", 2, "down-ramp: MW per minute (the event start, context only)"),
               ("NPRR-up-pct", 3, "up-ramp: percent of peak; the fleet's 100 MW (ASSUMED) as the peak; withdrawn, not in force"),
               ("NPRR-up-MW", 4, "up-ramp: MW per minute; the limit is the lesser of the two")]),
    dict(id="PHX-ramp", dos="F1", src="Colangelo et al., arXiv:2507.00909 v1 (Phoenix field demonstration)",
         quote="ramp down and up gracefully over 15 minutes, avoiding so-called “snap back” at the conclusion of the event by staying below the pre-event baseline.",
         rx=r"gracefully over (\d+) minutes",
         vals=[("PHX-min", 1, "the utility's ramp time, read as a limit of (fleet MW) / 15 per minute on the resume")]),
    dict(id="LLTF-ramp", dos="F3", src="NERC LLTF white paper (July 2025)",
         quote="In the fastest ramping period, the demand changes at a rate of 1.9 p.u. per second for about 250 milliseconds.",
         rx=r"rate of ([\d.]+) p\.u\. per second for about (\d+) milliseconds",
         vals=[("RAMP-pu", 1, "a training job's start ramp; resume model M-ramp takes the whole 0 -> 1 p.u. rise at this rate"),
               ("RAMP-ms", 2, "the duration of the fastest period (context; the model's ramp lasts 1/1.9 s)")]),
    dict(id="LLTF-field", dos="F3", src="NERC LLTF white paper (July 2025)",
         quote="For example, Figure 3.1 shows a North American data center ramping down from about 450 MW to about 40 MW within 36 seconds around hour 6. The load’s demand is constant (around 7 MW) for approximately 4 hours. After hour 10, the data center ramps back up to 450 MW over the course of a few minutes.",
         rx=r"from about (\d+) MW to about (\d+) MW within (\d+) seconds",
         vals=[("FLD-hi", 1, "context: a field ramp-down (not a DR event)"), ("FLD-lo", 2, "context"), ("FLD-s", 3, "context")]),
    dict(id="LLTF-xai", dos="F3", src="NERC LLTF white paper (July 2025)",
         quote="can change the loading 35–70 MW or more within a minute as the model starts and stops.",
         rx=r"loading (\d+)–(\d+) MW or more within a minute",
         vals=[("XAI-lo", 1, "context: observed start/stop swing within a minute"), ("XAI-hi", 2, "context")]),
    dict(id="MJ-rebound", dos="F3", src="Müller & Jansen, arXiv:1806.07670 v1 (heat pumps, not compute)",
         quote="In the experiment shown in the top plot, the throttling signals are released simultaneously at 12.00 h, i.e., ∆T = 0, which results in a sharp load ramp and a peak rebound of 64.8 kW. In the second experiment, shown in the bottom plot, ∆T = 45 min was used to spread the individual release times (29). The rebound is reduced to values below 32.6 kW, which amounts to a peak rebound damping of 50%.",
         rx=r"peak rebound of ([\d.]+) kW\..*∆T = (\d+) min was used.*below ([\d.]+) kW, which amounts to a peak rebound damping of (\d+)%",
         vals=[("MJ-sim", 1, "context: simultaneous release peak rebound (kW)"), ("MJ-dT", 2, "context: stagger spread (min)"),
               ("MJ-stag", 3, "context: staggered peak rebound bound (kW)"), ("MJ-damp", 4, "context: damping (%)")]),
    dict(id="LI-rebound", dos="F3", src="Li, arXiv:2609.05406 v1",
         quote="Load relief is a power service rather than an energy saving. If every deferred megawatt-hour rebounds and the expected lost work equals half of a one-hour checkpoint interval, net energy change after a four-hour call is −12.5% of gross curtailed energy. For the full-realization 2.32 MW offer, that rebound contains 10.44 MWh. The mean noneligible workload power, defined as the floor plus shift layers, is 23.264 MW; absorbing the rebound at 10% of that level takes 4.49 hours. This rule implies 8.49 hours between four-hour calls and at most 19.8 calls per week.",
         rx=(r"equals (half) of a (one)-hour checkpoint interval, net energy change after a (four)-hour call is −([\d.]+)% .*"
             r"the full-realization ([\d.]+) MW offer, that rebound contains ([\d.]+) MWh\..* is ([\d.]+) MW; absorbing the rebound at "
             r"(\d+)% of that level takes ([\d.]+) hours\. This rule implies ([\d.]+) hours between .* at most ([\d.]+) calls per week"),
         vals=[("LI-frac", 1, "context"), ("LI-ckpt", 2, "context"), ("LI-H", 3, "context"), ("LI-net", 4, "context (printed as −12.5 %)"),
               ("LI-MW", 5, "context"), ("LI-MWh", 6, "context"), ("LI-base", 7, "context"), ("LI-pct", 8, "context"),
               ("LI-absorb", 9, "context"), ("LI-gap", 10, "context"), ("LI-calls", 11, "context")]),
    dict(id="CHEN-rebound", dos="F3", src="Chen et al., arXiv:2509.07218 v6 (a review)",
         quote="inference or training tasks deferred in response to high electricity prices may be rescheduled simultaneously once prices fall, leading to secondary demand peaks or rebound effects that stress the grid.",
         rx=None, vals=[]),
    dict(id="MICH-snapback", dos="F3", src="Michaels Energy for Minnesota Commerce, DR Impact Study (2013)",
         quote="Snapback is the increase in energy and demand in the hours immediately following a demand response event.",
         rx=None, vals=[]),
    dict(id="NERC-reconnect", dos="F3", src="NERC, Incident Review (2025-01-08)",
         quote="Ramp rates for load connection are just as critical to system operations as generation ramping.",
         rx=None, vals=[]),
    dict(id="GOOG-stagger", dos="F3", src="Google Cloud, 'Balance of power' (2025-02-12)",
         quote="control planes such as Kubernetes [34] or Borg [63] stagger job starts over seconds, and the aggregate power use changes slowly over minutes or hours.",
         rx=None, vals=[]),
    dict(id="NV-powercap", dos="F4", src="NVIDIA blog (F4 dossier)",
         quote="With the new power cap feature, GPU power draw at the start of a workload is capped by the power controller. New maximum power levels are sent to the GPUs and gradually increased, aligning with the ramp rates the grid can tolerate.",
         rx=None, vals=[]),
    dict(id="NV-burner", dos="F4", src="NVIDIA blog (F4 dossier)",
         quote="The burner keeps using constant power as it waits for the workload to resume; if the workload doesn’t resume, the burner smoothly reduces the power consumption.",
         rx=None, vals=[]),
]

# ------------------------------------------------------------------------------------------------ assumed / declared inputs
W = Fr(1000)                                  # DECLARED units (DR1 section 2 adopts EPS2 T1's)
RATE = ONE                                    # DECLARED units
R = Fr(1, 10)                                 # ASSUMED (EPS2 T1's restart overhead; S = 0, lost = 0)
FLEET_MW = Fr(100)                            # ASSUMED (DECLARATION.md section 3: a hypothetical 100 MW fleet)
N_JOBS = 100                                  # CHOICE: the H3 portfolio (section 3: 'running jobs of the H3 portfolio')
P_JOB = FLEET_MW / N_JOBS                     # 1 MW per job (as in H3)
SLACK_STEP = Fr(5)                            # ASSUMED (H3's spread: slack 5 i h, i = 1..100)
HS = (Fr(1), Fr(3), Fr(4))                    # 1, 4 ASSUMED (EPS2 T1); 3 SOURCED in H3 (Phoenix 3-h events, F1)
SPACING = Fr(24)                              # CHOICE (EPS2 T1): one offer every 24 wall hours before hour W (K = 41)
WIN = MIN                                     # CHOICE: the ramp-measurement window, 1 minute (the unit of the sourced limits)
SUB_WINS = (SEC, 10 * SEC)                    # sensitivity windows (not scored)
GRID = tuple(d.q(s) for s in ("0.01", "0.02", "0.05", "0.2", "0.5", "2", "5", "10", "20"))  # ASSUMED (EPS2 T1)
N_SENS = (1, 10, 1000)                        # ASSUMED sensitivity (not scored): the same 100 MW split into N jobs
VERIFY_JOBS = (1, 20, 100)                    # CHOICE: jobs whose season p_all is re-derived by drlib's backward induction
ORDERS = ("tight-first", "loose-first")       # CHOICE: stagger orders (by slack)
MODELS = ("M-step", "M-idle", "M-ramp")       # resume power models (CHOICE; see CHOICES)

POST_FIRST_RUN_CHANGES: list[str] = [
    "(1) TABLE C (printed, not scored): the first run printed the change in each arm's season p_all as the cost of staggering; it was "
    "negative for some job in 116 of 288 rows x arms (at zero slack p_all spreads the lost job value over the offers left after it, so it "
    "falls when the stagger makes the slack run out earlier), so it is not a cost measure by itself. TABLE C1 now adds the season "
    "valuation lost on the all-accept path (participation held fixed) and the jobs whose deadline the staggers alone make them miss; "
    "the p_all change is kept as TABLE C2, labelled, with its rises and falls counted; the alternative-reading line now reads TABLE C1's "
    "valuation costs (first run: ETM 0 of 42, ETM-H 21 of 42 counting a p_all rise as a cost, WALL 42 of 42); G-ZERO's 'ETM's cost 0' "
    "now also covers the season valuation. No scored reading, prediction, arm, threshold or parameter changed",
    "(2) cosmetic: G-NEG's 'largest rel' printed the name of an arbitrary outcome when every comparison was equal (rel 0); it now says so",
    "(3) code tidy, no output change: the ETM-H verification's scale factor for d = 0 was written as a conditional that is always 1",
]


def f6(x, dd=6) -> str:
    return "-" if x is None else f"{float(x):.{dd}f}"


def parse_sources():
    vals, rep = {}, []
    for s in SOURCES:
        found = s["quote"] in TEXT[s["dos"]]
        m = re.search(s["rx"], s["quote"]) if s["rx"] else None
        parsed = (m is not None) if s["rx"] else True
        rep.append((s, found, parsed))
        if not (found and m):
            continue
        for vid, gi, note in s["vals"]:
            raw = m.group(gi)
            vals[vid] = dict(v=WORDNUM[raw] if raw in WORDNUM else d.q(raw), raw=raw, note=note, sid=s["id"])
    return vals, rep


# ------------------------------------------------------------------------------------------------ the fleet load profile
class Fleet:
    """The fleet's load (MW) as an exact piecewise-linear function of time t (hours; t = 0 is the event's end). Components:
    `const` MW always on; `groups` = [(count, P, a, tau)]: count jobs of P MW each, at full power before the event start -H,
    0 (idle, ASSUMED) from -H, back to P at a (tau == 0: a step at a, right-continuous) or rising linearly from 0 at a to P at
    a + tau; `cap` = (MW, s, T): a fleet-wide power-cap ramp (MW at full power before -H, 0 from -H, rising linearly from 0 at
    s to MW at s + T)."""

    def __init__(self, H, const=ZERO, groups=(), cap=None):
        self.H, self.const, self.groups, self.cap = H, const, list(groups), cap
        pts = {-H}
        for c, P, a, tau in self.groups:
            pts.add(a)
            pts.add(a + tau)
        if cap:
            pts.add(cap[1])
            pts.add(cap[1] + cap[2])
        self.bp = sorted(pts)

    @staticmethod
    def _one(t, side, P, a, tau, H):
        if t < -H or (t == -H and side == "L"):
            return P
        if tau == 0:
            return P if (t > a or (t == a and side == "R")) else ZERO
        if t <= a:
            return ZERO
        if t >= a + tau:
            return P
        return P * (t - a) / tau

    def at(self, t, side="R"):
        v = self.const
        for c, P, a, tau in self.groups:
            v += c * self._one(t, side, P, a, tau, self.H)
        if self.cap:
            v += self._one(t, side, self.cap[0], self.cap[1], self.cap[2], self.H)
        return v

    def rise(self, w):
        """sup over t of load(t + w) - load(t): the largest load increase within any window of length w (exact: the
        difference is linear between the candidate times b and b - w, so the sup is a one-sided limit at a candidate)."""
        cands = sorted(set(self.bp) | {b - w for b in self.bp})
        best = ZERO
        for c in cands:
            for side in ("L", "R"):
                best = max(best, self.at(c + w, side) - self.at(c, side))
        return best

    def drop(self, w):
        cands = sorted(set(self.bp) | {b - w for b in self.bp})
        best = ZERO
        for c in cands:
            for side in ("L", "R"):
                best = max(best, self.at(c, side) - self.at(c + w, side))
        return best

    def metrics(self):
        base = self.at(-self.H - 1)
        ev = self.at(-self.H / 2)
        post = [self.at(t, s) for t in self.bp if t >= 0 for s in ("L", "R")] + [self.at(self.bp[-1] + 1)]
        pmax = max(post)
        back = self.bp[-1] if self.at(self.bp[-1] + 1) == base else None
        return dict(base=base, event=ev, curtailed=base - ev, post_max=pmax, step=pmax - ev, above=pmax - base, back=back)


def delays(n, b, w=WIN):
    """Batch release: b jobs per window; rank r is released at floor(r / b) w after the event's end."""
    return [Fr(r // b) * w for r in range(n)]


def fleet_for(H, n, P, dl, model, tau_ramp):
    """Fleet with n jobs of P MW resuming after release delays dl (one per job) under the resume model."""
    cnt = {}
    for x in dl:
        cnt[x] = cnt.get(x, 0) + 1
    groups = []
    for x, c in sorted(cnt.items()):
        if model == "M-step":
            groups.append((c, P, x, ZERO))
        elif model == "M-idle":
            groups.append((c, P, x + R, ZERO))
        else:
            groups.append((c, P, x, tau_ramp))
    return Fleet(H, ZERO, groups)


def fleet_cap(H, n, P, L, model):
    """S2: every job resumes at once under a fleet-wide power cap rising at L MW per minute (M-idle: after the restart R)."""
    MW = n * P
    T = MW / L * MIN
    s = R if model == "M-idle" else ZERO
    return Fleet(H, ZERO, (), (MW, s, T)), T


# ------------------------------------------------------------------------------------------------ the arms' costs (exact)
def params(arm, H, dd, o):
    """Per-event charge c on the arm's valuation and deadline budget u, for an event of H contracted hours whose resume is
    delayed dd more hours (the stagger): WALL, OWN, ETM (drlib's arms, the event read as H + dd paused hours, no extra
    restart) and ETM-H (the stop-the-clock extension covers the contracted H only; the stagger runs on the wall clock)."""
    if arm == "WALL":
        return RATE * (H + dd + o), H + dd + o
    if arm == "OWN":
        return RATE * o, H + dd + o
    if arm == "ETM":
        return RATE * o, o
    if arm == "ETM-H":
        return RATE * o, o + dd
    raise ValueError(arm)


def pall_cf(job, arm, H, dd, K, paid=False):
    """Closed form of EPS2's p_all for K identical offers (drlib.rule_xstar's derivation: x* = c/e unless the arm is at zero
    slack, then (c + W rate/(K - nmax))/e): the minimum flat payment per contracted fleet-hour (e = H; paid: per paused
    fleet-hour, e = H + dd) at which the arm accepts every offer of the season."""
    c, u = params(arm, H, dd, job.overhead)
    nm = None if u == 0 else math.floor((job.D - job.W) / u)
    extra = (job.W * RATE / (K - nm)) if (nm is not None and nm < K) else ZERO
    return (c + extra) / ((H + dd) if paid else H), nm


def v_one(job, arm, H, dd):
    """The arm's valuation after one accepted event of H contracted hours with stagger dd (first event, full slack)."""
    if arm in ("WALL", "OWN", "ETM"):
        a = {"WALL": d.WALL, "OWN": d.OWN, "ETM": d.ETM}[arm]
        return d.vjob(job, a, 1, H + dd)
    c, u = params(arm, H, dd, job.overhead)
    return (job.value if job.W + u <= job.D else ZERO) - c


def v_season(job, arm, H, dd, K):
    """The arm's valuation after all K events accepted, each of H contracted hours with stagger dd, and whether the deadline is
    met on the arm's contract (the all-accept path; participation held fixed)."""
    if arm in ("WALL", "OWN", "ETM"):
        a = {"WALL": d.WALL, "OWN": d.OWN, "ETM": d.ETM}[arm]
        return d.vjob(job, a, K, K * (H + dd)), d.met(job, a, K, K * (H + dd))
    c, u = params(arm, H, dd, job.overhead)
    ok = job.W + K * u <= job.D
    return (job.value if ok else ZERO) - K * c, ok


def etm_h_arm(H, dd, o):
    """ETM-H as a drlib TIER arm (an encoding used only for verification): throughput x = dd/H over the event with a power
    curve that is 0 up to throughput 1 - x (so the whole contracted H is curtailed, e = H), wall delay x H + o = dd + o,
    own-clock charge o, wall-clock deadline."""
    x = dd / H
    return d.tier(x, None, d.power_pw([(0, 0), (ONE - x, 0), (1, 1)]), "own", o, name=f"ETM-H(d={d.g(dd)})")


ARMS4 = ("WALL", "OWN", "ETM", "ETM-H")


def portfolio():
    return [d.Job(W, W + SLACK_STEP * i, R, rate=RATE, name=f"J{i:03d}") for i in range(1, N_JOBS + 1)]


def main() -> int:
    print("DR1 check H5: rebound, N jobs resume together at the event's end")
    print(f"Declaration: Grid_Demand_Response/DECLARATION.md (pushed at {d.DECL_AT}; binding, not edited). Library: drlib.py (exact rationals).")
    print("Declared Q: a lossless pause resumes at full power at once, so the rebound peak equals the curtailed load; a staggered resume")
    print("removes it at a cost; the cost of staggering is printed.")
    print("Forecast: Q holds (REDUNDANT: rebound is known).  Rung R4 (synthetic model); a note, not evidence (R8).")
    print()
    vals, rep = parse_sources()
    all_found = all(f and p for _, f, p in rep)

    # ---------------------------------------------------------------- inputs
    print("INPUTS")
    print("  SOURCED  (each quote checked verbatim against its dossier's text at run time; numbers parsed out of the quote by the regex shown)")
    for s, found, parsed in rep:
        print(f"    [{s['id']}] {s['src']} (docs/citations/{DOSS[s['dos']]}); quote found verbatim: {d.yn(found)}; "
              f"{'parsed: ' + d.yn(parsed) if s['rx'] else 'qualitative (no number parsed)'}")
        print(f"      \"{s['quote']}\"")
        if s["rx"]:
            print(f"      regex {s['rx']!r}")
        for vid, gi, note in s["vals"]:
            if vid in vals:
                v = vals[vid]
                print(f"      -> {vid:13} raw '{v['raw']}' = {v['v']}; CHOICE: {note}")
    print(f"  DECLARED W = {W} compute-hours, value {RATE} per compute-hour at completion (DR1 section 2 adopts EPS2 T1's units)")
    print(f"  ASSUMED  R = {R} h restart overhead per pause event (EPS2 T1's model constant); save S = 0 and lost work 0 (a lossless pause")
    print("           with no save time, as EPS2 T1; H4 and H6 treat S)")
    print(f"  ASSUMED  fleet {d.g(FLEET_MW)} MW (DECLARATION.md section 3: 'A hypothetical AI training fleet of 100 MW (ASSUMED)'), split into")
    print(f"           N = {N_JOBS} jobs of {d.g(P_JOB)} MW (the H3 portfolio, as in H3); every job at full power while it runs and at 0 while paused")
    print("           (ASSUMED, EPS2 T1: idle power 0; the NV-burner quote above says some hardware keeps drawing power while it waits)")
    print(f"  ASSUMED  deadline slack D - W = {d.g(SLACK_STEP)} i h for job J(i), i = 1..{N_JOBS} (H3's spread; J020 is EPS2's D = 1100, J100 its D = 1500)")
    print(f"  ASSUMED  event lengths H in {{{', '.join(d.g(h) for h in HS)}}} h (1 and 4: EPS2 T1; 3: the Phoenix events, as sourced in H3)")
    print(f"  ASSUMED  payment grid {{{', '.join(d.g(p) for p in GRID)}}} per curtailed fleet-hour (EPS2 T1; context table only)")
    print(f"  ASSUMED  (sensitivity, not scored) the 100 MW fleet split into N in {{{', '.join(str(n) for n in N_SENS)}}} jobs")
    print()
    if not all_found:
        print("RESULT H5: Q not computable; G-ZERO FAILS (not computed: a sourced quote was not found or not parsed); "
              "G-NEG FAILS (not computed: a sourced quote was not found or not parsed)")
        return 1

    V = {k: v["v"] for k, v in vals.items()}
    limits = [
        ("NERC-L2-lo", V["L2-lo"], "NERC Level 2, lowest reported"),
        ("NERC-L2-typ-lo", V["L2-typ-lo"], "NERC Level 2, typical low"),
        ("NERC-L2-typ-hi", V["L2-typ-hi"], "NERC Level 2, typical high"),
        ("NERC-L2-hi", V["L2-hi"], "NERC Level 2, highest reported"),
        ("SO-cap", V["SO"], "Southern Company cap"),
        ("NPRR-CLR", V["NPRR-CLR-pct"] / 100 * FLEET_MW, "NPRR1191 CLR, 20 % of 100 MW (withdrawn)"),
        ("NPRR-up", min(V["NPRR-up-pct"] / 100 * FLEET_MW, V["NPRR-up-MW"]), "NPRR1191 non-CLR up, min(2 % of 100 MW, 8) (withdrawn)"),
        ("PHX-15min", FLEET_MW / V["PHX-min"], "Phoenix 15-minute ramp, 100 MW / 15 min"),
    ]
    limits.sort(key=lambda t: (t[1], t[0]))
    down_lim = min(V["NPRR-dn-pct"] / 100 * FLEET_MW, V["NPRR-dn-MW"])
    tau_ramp = SEC / V["RAMP-pu"]                  # 0 -> 1 p.u. at 1.9 p.u. per second
    print("  derived ramp limits (MW per minute; up-ramp on the resume):")
    for lid, L, lab in limits:
        print(f"    {lid:15} {f6(L):>12}  = {L}  ({lab})")
    print(f"  M-ramp per-job rise time 1 / {d.g(V['RAMP-pu'])} s = {f6(tau_ramp / SEC)} s")
    print()

    # ---------------------------------------------------------------- choices
    print("CHOICES")
    print("  CHOICE The event: every one of the N jobs has accepted it (the premise 'N jobs resume together'; for ETM, which accepts at any")
    print("         payment >= R/H, this is its participation at every such payment, see CONTEXT A). All jobs pause together at the event")
    print("         start -H (the operator's call) and are released together at its end t = 0 unless staggered.")
    print("  CHOICE Resume power models (all three scored): M-step: a released job draws full power at once (its restart R runs at full")
    print("         power, own hours without progress); M-idle: it draws 0 during the restart R and full power after it; M-ramp: from its")
    print(f"         release its power rises at the sourced {d.g(V['RAMP-pu'])} p.u. per second (LLTF-ramp) to full power. A lossless pause")
    print("         returns each job to its own full draw; its deferred work extends the job in time (no catch-up capacity, no demand")
    print("         above the pre-event baseline in the model).")
    print("  CHOICE 'The rebound peak' (scored) = the largest load increase within any 1-minute window after the event (the window of the")
    print("         sourced MW/min limits); 'the curtailed load' = the pre-event load minus the event-level load. Q-a (scored): in every")
    print("         cell (resume model x H) the simultaneous resume's rebound peak equals the curtailed load exactly AND the post-event")
    print("         maximum minus the event level equals the curtailed load exactly (the return is a step to the baseline, not above it).")
    print("         Rises within 1 s and 10 s windows and the peak above the baseline are printed.")
    print("  CHOICE 'A staggered resume' (scored) = S1, batch release: b = floor(L x 1 min / P) jobs per minute, rank r released at")
    print("         floor(r / b) minutes. Any release schedule whose rise within every 1-minute window is <= b P releases rank r no earlier")
    print("         than floor(r / b) minutes (b + 1 releases cannot share a half-open 1-minute window), so S1 gives every rank its least")
    print("         delay under the limit. 'Removes it' (Q-b, scored) = in every cell (resume model x H x ramp limit) where the simultaneous")
    print("         peak exceeds the limit L (binding), b >= 1 (a feasible stagger), the staggered rebound peak <= L and < the simultaneous")
    print("         peak. 'At a cost' (scored) = the stagger defers job time: the summed release delay over the jobs is > 0. Non-binding")
    print("         limits need no stagger (b >= N) and are printed, not scored. The alternative reading 'a cost in ETM's own valuation'")
    print("         is computed and printed, not scored.")
    print("  CHOICE S2 (printed, not scored): every job resumes at once under a fleet-wide power cap rising at exactly L MW per minute")
    print("         (the NV-powercap quote); throughput = power fraction (linear curve, ASSUMED, drlib's default), so each job loses T/2")
    print("         hours of progress, T = N P / L minutes; its cost is computed as a stagger of T/2 for every job.")
    print("  CHOICE Stagger order (printed, not scored): tight-first (ranks by slack, tightest released first) and loose-first, the same")
    print("         order at every event. The cost of staggering per arm (TABLE C1): (i) the valuation lost at one event from full slack")
    print("         (fleet sum); (ii) the season (K = 41 offers every 24 h, every event accepted by every job and staggered the same way):")
    print("         the valuation lost and the jobs whose deadline the staggers alone make them miss. TABLE C2, a second reading: the change")
    print("         in the arm's p_all, EPS2's minimum flat payment per contracted fleet-hour at which the arm accepts every offer (the")
    print("         stagger hours unpaid), per job, and the fleet's season payment change sum_i delta_i K H P_i. p_all by closed form")
    print("         (drlib.rule_xstar's derivation) for all 100 jobs; re-derived by drlib's backward induction for jobs J001, J020, J100.")
    print("  CHOICE Arms for the cost: WALL, OWN, ETM (drlib; a staggered event is H + d paused hours with one restart) and ETM-H (the")
    print("         stop-the-clock extension covers only the contracted H; the stagger delay runs on the wall-clock deadline). ETM reads")
    print("         the extension as covering every hour the operator holds the job paused, the stagger included.")
    print("  CHOICE Q holds iff Q-a and Q-b hold in every scored cell; not computable if any sourced quote is not found or not parsed.")
    print("  CHOICE G-ZERO: ETM's one-event stake minus rate R, at every event count n = 0..K-1, for every job, H and stagger delay d of")
    print("         the scored costs (the staggered event of H + d hours), exactly 0; and ETM's x* == rate R/(H + d) (closed) at every offer")
    print("         state of the verification jobs' staggered seasons (stagger hours paid, drlib's convention).")
    print("  CHOICE G-NEG: with no events offered (K = 0, and each job's realisation in which no offer is made), ETM not ahead of WALL by")
    print("         more than 1 % (harness rel) on any outcome: per job curtailed fleet-hours, payments, valuation, fleet value, deadline met,")
    print("         completion hour (earlier is ahead); fleet rebound peak and fleet peak load (lower is ahead); pi = R/H.")
    print("  CHOICE The event start (all jobs pause at once) is a step down of the same size; printed as context against the NPRR down")
    print("         limit, not scored (Q is about the resume).")
    print()

    jobs = portfolio()
    NP = N_JOBS * P_JOB

    # ---------------------------------------------------------------- Q-a
    print("TABLE A (Q-a): the simultaneous resume, per cell (resume model x H); MW")
    print(f"  {'model':7} {'H':>3} {'base':>7} {'event':>6} {'curtail':>8} {'post max':>9} {'step':>8} {'above':>6} {'rise 1min':>10} "
          f"{'rise 10s':>9} {'rise 1s':>8} {'back at (s)':>12} {'Q-a':>6}")
    qa_cells = []
    for model in MODELS:
        for H in HS:
            fl = fleet_for(H, N_JOBS, P_JOB, [ZERO] * N_JOBS, model, tau_ramp)
            m = fl.metrics()
            r1, r10, r1s = fl.rise(WIN), fl.rise(10 * SEC), fl.rise(SEC)
            ok = (r1 == m["curtailed"]) and (m["step"] == m["curtailed"])
            qa_cells.append(dict(model=model, H=H, ok=ok, m=m, r1=r1))
            bk = "-" if m["back"] is None else f6(m["back"] / SEC, 3)
            print(f"  {model:7} {d.g(H):>3} {f6(m['base'], 3):>7} {f6(m['event'], 3):>6} {f6(m['curtailed'], 3):>8} {f6(m['post_max'], 3):>9} "
                  f"{f6(m['step'], 3):>8} {f6(m['above'], 3):>6} {f6(r1, 3):>10} {f6(r10, 3):>9} {f6(r1s, 3):>8} {bk:>12} "
                  f"{('holds' if ok else 'fails'):>6}")
    qa = all(c["ok"] for c in qa_cells)
    print(f"  Q-a holds in {sum(int(c['ok']) for c in qa_cells)} of {len(qa_cells)} cells -> {'holds' if qa else 'fails'}")
    print("  (back at: the time after the event's end at which the fleet is back at its baseline; above: post-event maximum minus the")
    print("   pre-event baseline)")
    print()

    # ---------------------------------------------------------------- Q-b
    print("TABLE B (Q-b): the staggered resume S1 per cell (resume model x H x ramp limit); S2 printed beside it; MW, minutes")
    print(f"  {'model':7} {'H':>3} {'limit':15} {'L MW/min':>9} {'bind':>4} {'b':>3} {'B':>3} {'S1 rise 1min':>12} {'S1 rise 1s':>10} "
          f"{'last d':>7} {'mean d':>7} {'sum d job-h':>11} {'defer MWh':>9} {'Q-b':>6} {'S2 rise 1min':>12} {'S2 rise 1s':>10} "
          f"{'S2 T':>7} {'S2 sum job-h':>12}")
    qb_cells, s1_by_L = [], {}
    for model in MODELS:
        sim = {H: next(c for c in qa_cells if c["model"] == model and c["H"] == H)["r1"] for H in HS}
        for H in HS:
            for lid, L, _ in limits:
                binding = sim[H] > L * (WIN / MIN)
                b = math.floor(L * (WIN / MIN) / P_JOB)
                if b >= 1:
                    dl = delays(N_JOBS, min(b, N_JOBS))
                    fl = fleet_for(H, N_JOBS, P_JOB, dl, model, tau_ramp)
                    r1, r1s = fl.rise(WIN), fl.rise(SEC)
                    B = math.ceil(N_JOBS / b)
                    sd = sum(dl, ZERO)
                    last, mean = max(dl), sd / N_JOBS
                else:
                    dl, r1, r1s, B, sd, last, mean = None, None, None, None, None, None, None
                fc, T = fleet_cap(H, N_JOBS, P_JOB, L, model)
                c1, c1s = fc.rise(WIN), fc.rise(SEC)
                s2sum = N_JOBS * T / 2
                ok = None
                if binding:
                    ok = b >= 1 and r1 <= L * (WIN / MIN) and r1 < sim[H] and sd > 0
                    qb_cells.append(dict(model=model, H=H, lid=lid, L=L, ok=ok, b=b, r1s=r1s, c1s=c1s))
                s1_by_L[lid] = dict(b=b, dl=dl, B=B, sd=sd, last=last, mean=mean, T=T)
                print(f"  {model:7} {d.g(H):>3} {lid:15} {f6(L, 3):>9} {d.yn(binding):>4} {b:>3} {('-' if B is None else B):>3} "
                      f"{f6(r1, 3):>12} {f6(r1s, 3):>10} {('-' if last is None else f6(last / MIN, 2)):>7} "
                      f"{('-' if mean is None else f6(mean / MIN, 2)):>7} {f6(sd, 4):>11} {f6(None if sd is None else sd * P_JOB, 4):>9} "
                      f"{('-' if ok is None else ('holds' if ok else 'fails')):>6} {f6(c1, 3):>12} {f6(c1s, 3):>10} {f6(T / MIN, 2):>7} "
                      f"{f6(s2sum, 4):>12}")
    qb = all(c["ok"] for c in qb_cells)
    nbind = len(qb_cells)
    print(f"  Q-b holds in {sum(int(c['ok']) for c in qb_cells)} of {nbind} binding cells -> {'holds' if qb else 'fails'}; "
          f"non-binding cells (printed, not scored): {len(MODELS) * len(HS) * len(limits) - nbind}")
    print("  (b: jobs released per minute; B: release minutes; last d / mean d: release delay of the last / average job in minutes;")
    print("   sum d: summed release delay in job-hours; defer MWh: deferred energy P x sum d; S2 T: minutes of the power-cap ramp;")
    print("   S2 sum: the job-hours of progress lost to the ramp, N T/2)")
    # sub-minute windows (not scored)
    s1_1s = sum(int(c["b"] >= 1 and c["r1s"] <= c["L"] * (SEC / MIN)) for c in qb_cells)
    s2_1s = sum(int(c["c1s"] <= c["L"] * (SEC / MIN)) for c in qb_cells)
    print(f"  sensitivity (not scored), the limit read over a 1 s window (L/60 MW per second): S1 within it in {s1_1s} of {nbind} binding cells "
          f"-> {'holds' if s1_1s == nbind else 'fails'}; S2 within it in {s2_1s} of {nbind} -> {'holds' if s2_1s == nbind else 'fails'}")
    print()

    # ---------------------------------------------------------------- costs per arm
    K = len(d.every(SPACING, HS[0], W))
    print(f"TABLE C1: the cost of staggering per arm in the arm's own valuation (portfolio of {N_JOBS} jobs, K = {K} offers per season)")
    print("  (i) 1-ev: one event from full slack, the fleet sum of the valuation lost to the stagger (value units); (ii) season: every one")
    print("  of the K events accepted by every job (the all-accept path, participation held fixed), each staggered the same way: the fleet")
    print("  sum of the valuation lost to the staggers (value units) and, in brackets, the jobs whose deadline the staggers alone make them miss")
    print(f"  {'H':>3} {'limit':15} {'order':12} {'sum d h':>9} | {'1-ev WALL':>10} {'OWN':>8} {'ETM':>5} {'ETM-H':>8} | "
          f"{'season WALL':>12} {'OWN [jobs]':>15} {'ETM':>5} {'ETM-H [jobs]':>15}")
    cost_rows = []
    all_dd = {}                      # job name -> set of stagger delays used (for G-ZERO and the verification)
    for H in HS:
        base_pa = {(j.name, a): pall_cf(j, a, H, ZERO, K)[0] for j in jobs for a in ARMS4}
        for lid, L, _ in limits:
            s = s1_by_L[lid]
            variants = []
            if s["dl"] is not None:
                srt = s["dl"]
                variants.append(("tight-first", {j.name: srt[i] for i, j in enumerate(jobs)}))
                variants.append(("loose-first", {j.name: srt[N_JOBS - 1 - i] for i, j in enumerate(jobs)}))
            variants.append(("S2-cap", {j.name: s["T"] / 2 for j in jobs}))
            for order, dmap in variants:
                one = {a: sum((v_one(j, a, H, ZERO) - v_one(j, a, H, dmap[j.name]) for j in jobs), ZERO) for a in ARMS4}
                sea_v, sea_lost = {}, {}
                for a in ARMS4:
                    tot, lost = ZERO, 0
                    for j in jobs:
                        v0, m0 = v_season(j, a, H, ZERO, K)
                        v1, m1 = v_season(j, a, H, dmap[j.name], K)
                        tot += v0 - v1
                        lost += int(m0 and not m1)
                    sea_v[a], sea_lost[a] = tot, lost
                seas = {}
                for a in ARMS4:
                    deltas = [pall_cf(j, a, H, dmap[j.name], K)[0] - base_pa[(j.name, a)] for j in jobs]
                    fleet_pay = sum((x * K * H * P_JOB for x in deltas), ZERO)
                    seas[a] = dict(up=sum(int(x > 0) for x in deltas), down=sum(int(x < 0) for x in deltas), mx=max(deltas), mn=min(deltas),
                                   mean=sum(deltas, ZERO) / N_JOBS, fleet=fleet_pay)
                for j in jobs:
                    all_dd.setdefault(j.name, set()).add(dmap[j.name])
                sd = sum(dmap.values(), ZERO)
                cost_rows.append(dict(H=H, lid=lid, order=order, one=one, sea_v=sea_v, sea_lost=sea_lost, seas=seas, sd=sd))
                print(f"  {d.g(H):>3} {lid:15} {order:12} {f6(sd, 3):>9} | {f6(one['WALL'], 3):>10} {f6(one['OWN'], 1):>8} "
                      f"{f6(one['ETM'], 1):>5} {f6(one['ETM-H'], 1):>8} | {f6(sea_v['WALL'], 3):>12} "
                      f"{f6(sea_v['OWN'], 1) + ' [' + str(sea_lost['OWN']) + ']':>15} {f6(sea_v['ETM'], 1):>5} "
                      f"{f6(sea_v['ETM-H'], 1) + ' [' + str(sea_lost['ETM-H']) + ']':>15}")
    print()
    print("TABLE C2: a second reading of the season cost, the change in EPS2's p_all (the minimum flat payment per contracted fleet-hour at")
    print("  which the arm accepts every offer; stagger hours unpaid): per arm, jobs whose p_all rises / falls, the largest rise, the")
    print("  smallest change, the mean change, and the fleet's season payment change sum_i delta_i K H P_i. At zero slack p_all spreads the")
    print("  job's lost value over the offers left after it, so it falls when the stagger makes the slack run out earlier: this reading is")
    print("  not monotone in the stagger and is not a cost measure by itself (TABLE C1 is)")
    print(f"  {'H':>3} {'limit':15} {'order':12} | " + " | ".join(f"{a + ' up/down/max/min/mean/fleet':>55}" for a in ARMS4))
    for r in cost_rows:
        sz = r["seas"]
        print(f"  {d.g(r['H']):>3} {r['lid']:15} {r['order']:12} | "
              + " | ".join(f"{sz[a]['up']:>3}/{sz[a]['down']:>3}/{f6(sz[a]['mx'], 4):>9}/{f6(sz[a]['mn'], 4):>10}/{f6(sz[a]['mean'], 5):>9}/"
                           f"{f6(sz[a]['fleet'], 1):>11}" for a in ARMS4))
    etm_cost_zero = all(r["one"]["ETM"] == 0 and r["sea_v"]["ETM"] == 0 and r["sea_lost"]["ETM"] == 0 and r["seas"]["ETM"]["up"] == 0
                        and r["seas"]["ETM"]["down"] == 0 for r in cost_rows)
    neg_rise = [(r, a) for r in cost_rows for a in ARMS4 if r["seas"][a]["down"] > 0]
    print(f"  ETM's cost of staggering exactly 0 in every row (one event, season valuation and p_all, every job): {d.yn(etm_cost_zero)}")
    print(f"  rows x arms of TABLE C2 where some job's p_all falls with the stagger: {len(neg_rise)} of {len(cost_rows) * len(ARMS4)}")
    bind_ids = {c["lid"] for c in qb_cells}
    s1b = [r for r in cost_rows if r["lid"] in bind_ids and r["order"] != "S2-cap"]
    costly = lambda r, a: r["one"][a] > 0 or r["sea_v"][a] > 0
    alt = {a: sum(int(costly(r, a)) for r in s1b) for a in ARMS4}
    print(f"  alternative reading of 'at a cost' (not scored): a cost > 0 in the arm's own valuation (TABLE C1, one event or season) in "
          f"the {len(s1b)} binding S1 rows: ETM {alt['ETM']} -> {'holds' if alt['ETM'] == len(s1b) else 'fails'}; ETM-H (the stagger on "
          f"the wall clock) {alt['ETM-H']}; OWN {alt['OWN']}; WALL {alt['WALL']}")
    print()

    # ---------------------------------------------------------------- verification of the closed form
    print("VERIFICATION: season p_all by drlib's backward induction (value functions in pi, exact) against the closed form, jobs "
          + ", ".join(f"J{i:03d}" for i in VERIFY_JOBS) + ", every H and every stagger delay they receive (stagger hours unpaid:")
    print("drlib's p_all for offers of H + d paused hours, scaled by (H + d)/H; ETM-H through the TIER encoding etm_h_arm)")
    ver_n = ver_ok = 0
    xs_n = xs_ok = 0
    stakes_n, stakes_max = 0, ZERO
    for H in HS:
        for i in VERIFY_JOBS:
            j = jobs[i - 1]
            for dd in sorted(all_dd[j.name]):
                offs = d.every(SPACING, H + dd, W)
                for a in ARMS4:
                    cf = pall_cf(j, a, H, dd, K)[0]
                    if a == "ETM-H":
                        arm = d.ETM if dd == 0 else etm_h_arm(H, dd, j.overhead)
                        o2 = offs if dd == 0 else d.every(SPACING, H, W)
                        pa = d.p_all(j, arm, o2)
                        got = pa.x
                    else:
                        arm = {"WALL": d.WALL, "OWN": d.OWN, "ETM": d.ETM}[a]
                        F = d.value_fns(j, arm, offs)
                        pa = d.p_all(j, arm, offs, F)
                        got = pa.x * (H + dd) / H
                        if a == "ETM":
                            xs = d.xstar_all(j, arm, offs, F)
                            xs_n += len(xs)
                            xs_ok += sum(int(x.kind == "threshold" and x.closed and x.x == RATE * j.overhead / (H + dd)) for x in xs.values())
                    ver_n += 1
                    ver_ok += int(pa.kind == "threshold" and got == cf)
    print(f"  closed form == drlib p_all in {ver_ok} of {ver_n} (job, H, d, arm) cases")
    print()

    # ---------------------------------------------------------------- context A: participation per arm
    H4 = Fr(4)
    offs4 = d.every(SPACING, H4, W)
    print(f"CONTEXT A (not scored): who resumes together. H = 4, K = {len(offs4)}; per arm and payment pi, the jobs curtailed per event")
    print("(each job's backward-induction play at pi; H0 enrols for the season when its payments cover its opportunity cost); the")
    print("simultaneous rebound peak of an event is its curtailed MW (Q-a). All four arms pause losslessly in the model; they differ in")
    print("valuation and deadline clock, hence in who joins.")
    print(f"  {'pi':>6} | " + " | ".join(f"{a:>4} first/min/max/mean MW" for a in ("WALL", "OWN", "ETM", "H0")))
    for pi in GRID:
        parts = []
        for arm in (d.WALL, d.OWN, d.ETM, d.H0):
            cnt = [0] * len(offs4)
            for j in jobs:
                for k in d.play(j, arm, offs4, pi)["accepted"]:
                    cnt[k] += 1
            mw = [c * P_JOB for c in cnt]
            parts.append(f"{d.g(mw[0]):>4}/{d.g(min(mw)):>4}/{d.g(max(mw)):>4}/{f6(sum(mw, ZERO) / len(mw), 2):>7}      ")
        print(f"  {d.g(pi):>6} | " + " | ".join(parts))
    print()

    # ---------------------------------------------------------------- context B: sensitivity in N
    print("CONTEXT B (not scored): the same 100 MW fleet split into N jobs (M-step, H = 4): simultaneous peak; S1 batch size b and its")
    print("peak per binding limit ('infeasible' where one job's step exceeds the limit, b = 0); S2's peak")
    for n in N_SENS:
        P = FLEET_MW / n
        fl = fleet_for(H4, n, P, [ZERO] * n, "M-step", tau_ramp)
        sim = fl.rise(WIN)
        parts, feas = [], 0
        for lid, L, _ in limits:
            if sim <= L:
                continue
            b = math.floor(L / P)
            if b >= 1:
                r1 = fleet_for(H4, n, P, delays(n, min(b, n)), "M-step", tau_ramp).rise(WIN)
                feas += int(r1 <= L)
                parts.append(f"{lid} b {b} peak {d.g(r1)}")
            else:
                parts.append(f"{lid} infeasible")
        c1 = fleet_cap(H4, n, P, limits[0][1], "M-step")[0].rise(WIN)
        nb = sum(int(sim > L) for _, L, _ in limits)
        print(f"  N = {n:>4} ({d.g(P)} MW each): simultaneous peak {d.g(sim)} MW; S1 within the limit in {feas} of {nb} binding limits "
              f"-> {'holds' if feas == nb else 'fails'}; S2 peak at the tightest limit {d.g(c1)} MW")
        print("     " + "; ".join(parts))
    print()

    # ---------------------------------------------------------------- context C: sources' numbers
    print("CONTEXT C (not scored): the sources' own numbers against the model")
    dT = V["MJ-dT"] * MIN
    dl_mj = [dT * r / N_JOBS for r in range(N_JOBS)]
    r_mj = fleet_for(H4, N_JOBS, P_JOB, dl_mj, "M-step", tau_ramp).rise(WIN)
    damp_src = 1 - V["MJ-stag"] / V["MJ-sim"]
    print(f"  Müller & Jansen (heat pumps): damping 1 - {d.g(V['MJ-stag'])}/{d.g(V['MJ-sim'])} = {f6(100 * damp_src, 2)} % (quoted '{d.g(V['MJ-damp'])}%'; "
          f"rounds to it: {d.yn(round(float(100 * damp_src)) == int(V['MJ-damp']))}). The model with the same spread (N = {N_JOBS} releases evenly")
    print(f"    over {d.g(V['MJ-dT'])} min, r x {d.g(V['MJ-dT'])}/{N_JOBS} min; CHOICE): 1-minute rebound peak {d.g(r_mj)} MW of {d.g(NP)}, damping "
          f"{f6(100 * (1 - r_mj / NP), 2)} %. The heat pumps' peak is a thermal recovery; the model's pause has none (peak above baseline 0),")
    print("    so the two dampings measure different things.")
    li_curt = V["LI-MW"] * V["LI-H"]
    li_frac = V["LI-frac"] * V["LI-ckpt"]
    li_reb = li_curt * (1 + li_frac / V["LI-H"])
    li_abs = V["LI-MWh"] / (V["LI-pct"] / 100 * V["LI-base"])
    li_gap = V["LI-H"] + V["LI-absorb"]
    li_calls = 168 / V["LI-gap"]
    print(f"  Li (lossy pause, energy rebound): curtailed {d.g(li_curt)} MWh ({d.g(V['LI-MW'])} MW x {d.g(V['LI-H'])} h); rebound {f6(li_reb, 4)} MWh = curtailed x "
          f"(1 + lost/H), lost = {d.g(li_frac)} h (quoted {d.g(V['LI-MWh'])}: {d.yn(li_reb == V['LI-MWh'])}); net change {f6(100 * li_frac / V['LI-H'], 2)} % "
          f"(quoted −{d.g(V['LI-net'])} %, which the F1 reading says is a rise: {d.yn(100 * li_frac / V['LI-H'] == V['LI-net'])});")
    print(f"    absorption {f6(li_abs, 4)} h (quoted {d.g(V['LI-absorb'])}); {d.g(V['LI-H'])} + {d.g(V['LI-absorb'])} = {d.g(li_gap)} h (quoted "
          f"{d.g(V['LI-gap'])}: {d.yn(li_gap == V['LI-gap'])}); 168 h / {d.g(V['LI-gap'])} h = {f6(li_calls, 3)} calls per week (quoted {d.g(V['LI-calls'])}; 168 h per week is arithmetic).")
    for H in HS:
        print(f"    the model's lossless pause at H = {d.g(H)}: energy rebound = curtailed x (1 + R/H) = curtailed x {f6(1 + R / H, 4)} "
              f"(+{f6(100 * R / H, 2)} %; R ASSUMED); Li's lossy pause at the same H: +{f6(100 * li_frac / H, 2)} %")
    fld_rate = (V["FLD-hi"] - V["FLD-lo"]) / (V["FLD-s"] * SEC / MIN)
    print(f"  NERC LLTF field event: ramp down {d.g(V['FLD-hi'])} -> {d.g(V['FLD-lo'])} MW in {d.g(V['FLD-s'])} s = {f6(fld_rate, 2)} MW/min average; "
          f"the return 'over the course of a few minutes' carries no number (not parsed)")
    print(f"  xAI Colossus: {d.g(V['XAI-lo'])}-{d.g(V['XAI-hi'])} MW within a minute at start and stop; the low end exceeds the sourced limits "
          f"{', '.join(lid for lid, L, _ in limits if V['XAI-lo'] > L)} ({sum(int(V['XAI-lo'] > L) for _, L, _ in limits)} of {len(limits)})")
    ev_drop = fleet_for(H4, N_JOBS, P_JOB, [ZERO] * N_JOBS, "M-step", tau_ramp).drop(WIN)
    print(f"  the event start (all jobs pause at once): a drop of {d.g(ev_drop)} MW within a minute against the NPRR down limit min(5 % of "
          f"100 MW, 20) = {d.g(down_lim)} MW/min: within it: {d.yn(ev_drop <= down_lim)}")
    print("  qualitative sources (found verbatim above): CHEN-rebound (a review states rebound from simultaneous rescheduling), MICH-snapback")
    print("    (snapback defined), NERC-reconnect (reconnection ramps), GOOG-stagger (control planes stagger job starts), NV-powercap (a")
    print("    ramped power cap at workload start). Whether G5's rebound clause is REDUNDANT is graded in checks/grade.py, not here.")
    print()

    # ---------------------------------------------------------------- Q
    qv = "holds" if (qa and qb) else "fails"
    print("Q")
    print(f"  inputs: every sourced quote found verbatim and parsed: {d.yn(all_found)}")
    print(f"  Q-a (the simultaneous rebound peak equals the curtailed load): {sum(int(c['ok']) for c in qa_cells)} of {len(qa_cells)} cells -> "
          f"{'holds' if qa else 'fails'}")
    print(f"  Q-b (S1 brings the peak within every binding limit, below the simultaneous peak, with a deferred-time cost > 0): "
          f"{sum(int(c['ok']) for c in qb_cells)} of {nbind} binding cells -> {'holds' if qb else 'fails'}")
    print(f"  the cost of staggering is printed in TABLE B (deferred job-hours, MWh) and TABLE C (per arm); closed form verified in {ver_ok} "
          f"of {ver_n} cases")
    print(f"  Q: {qv}; the investigator's forecast (Q holds) is {'right' if qv == 'holds' else 'wrong'}")
    print()

    # ---------------------------------------------------------------- gate
    for j in jobs:
        for H in HS:
            for dd in all_dd[j.name]:
                for n in range(K):
                    s = d.stake(j, d.ETM, H + dd, n) - RATE * j.overhead
                    stakes_n += 1
                    stakes_max = max(stakes_max, abs(s))
    gz = stakes_max == 0 and xs_ok == xs_n and etm_cost_zero
    print("GATE")
    print(f"  G-ZERO: max |ETM stake - rate R| over {stakes_n} (job, H, stagger d, event count) cases = {d.g(stakes_max)} (exact); ETM's x* == "
          f"rate R/(H + d) (closed) at {xs_ok} of {xs_n} offer states; ETM's cost of staggering 0 in every TABLE C row: {d.yn(etm_cost_zero)} "
          f"-> {'holds' if gz else 'FAILS'}")
    outcomes = (("curtailed fleet-hours", "fleet_hours", +1), ("payments", "payments", +1), ("valuation", "valuation", +1),
                ("fleet value", "fleet_value", +1), ("deadline met", "met", +1), ("completion hour", "completion", -1))
    n_cmp = ahead = 0
    worst = (0.0, "-")
    for H in HS:
        pi = R / H
        offs = d.every(SPACING, H, W)
        for label, of, made in (("K = 0", (), None), ("no offer made", offs, [False] * len(offs))):
            part = {"ETM": 0, "WALL": 0}
            for j in jobs:
                pe = d.play(j, d.ETM, of, pi, made=made)
                pw = d.play(j, d.WALL, of, pi, made=made)
                part["ETM"] += pe["events"]
                part["WALL"] += pw["events"]
                for name, fld, sgn in outcomes:
                    a_, b_ = float(pe[fld]), float(pw[fld])
                    r = d.rel(a_, b_)
                    better = (a_ > b_) if sgn > 0 else (a_ < b_)
                    n_cmp += 1
                    ahead += int(better and r > float(TOL))
                    worst = max(worst, (r, name))
            fl = {a: Fleet(H, (N_JOBS - part[a]) * P_JOB, [(part[a], P_JOB, ZERO, ZERO)] if part[a] else []) for a in part}
            for name, fn in (("fleet rebound peak", lambda x: x.rise(WIN)), ("fleet peak load", lambda x: max(x.at(t, s) for t in x.bp for s in ("L", "R")))):
                a_, b_ = float(fn(fl["ETM"])), float(fn(fl["WALL"]))
                r = d.rel(a_, b_)
                n_cmp += 1
                ahead += int(a_ < b_ and r > float(TOL))
                worst = max(worst, (r, name))
    gn = ahead == 0
    print(f"  G-NEG: no events offered (K = 0 and the no-offer realisation), {N_JOBS} jobs x {len(HS)} H x 2 worlds on six outcomes plus the")
    print(f"         fleet's rebound peak and peak load: {n_cmp} comparisons; ETM ahead of WALL by more than 1 % in {ahead}; largest rel "
          f"{worst[0]:.3e} ({worst[1] if worst[0] > 0 else 'every comparison equal'}) -> {'holds' if gn else 'FAILS'}")
    print()
    print("POST-FIRST-RUN CHANGES: " + ("; ".join(POST_FIRST_RUN_CHANGES) if POST_FIRST_RUN_CHANGES else "none"))
    print()
    print(f"RESULT H5: Q {qv}; G-ZERO {'holds' if gz else 'FAILS'} (max |ETM stake - rate R| = {d.g(stakes_max)} over {stakes_n} (job, H, "
          f"stagger d, event count) cases; ETM x* = R/(H + d) at {xs_ok} of {xs_n} offer states; ETM's stagger cost 0 in every row: "
          f"{d.yn(etm_cost_zero)}); G-NEG {'holds' if gn else 'FAILS'} (ETM ahead of WALL by more than 1 % in {ahead} of {n_cmp} "
          f"no-event comparisons)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

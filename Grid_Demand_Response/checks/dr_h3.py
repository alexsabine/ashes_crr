"""DR1 check H3 (Grid_Demand_Response/DECLARATION.md section 2, pushed at e67e8ee; binding, never edited here):
a portfolio of 100 jobs with a spread of deadline slack: the fleet's supply curve (curtailable MW against payment).

Declared prediction Q: ETM's curve is flat at R/H; OWN's and WALL's are rising; the gap is largest for tight-slack jobs.
Declared forecast: Q holds.

Arithmetic: Grid_Demand_Response/checks/drlib.py (exact rational arithmetic; selftest pinned in drlib_selftest.txt).
Every verdict word below is computed from the numbers (R15). Rung R4 (synthetic model); a note, not evidence (R8).

    cd /home/user/ashes_crr && uv run python Grid_Demand_Response/checks/dr_h3.py > Grid_Demand_Response/checks/dr_h3.txt
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import drlib as dl  # noqa: E402

ZERO, ONE = Fr(0), Fr(1)
TOL = Fr(1, 100)                     # G-NEG's declared 1 % (DECLARATION.md section 2, the gate)

# ------------------------------------------------------------------------------------------------ inputs
W = dl.q(1000)                       # DECLARED (DR1 section 2 adopts EPS2 T1's units)
R = dl.q("0.1")                      # ASSUMED (EPS2 T1 model constant; no fetched source supplies R)
N_JOBS = 100                         # DECLARED (H3: a portfolio of 100 jobs)
SLACK_STEP = dl.q(5)                 # ASSUMED: slack_i = 5 i h, i = 1..100 (5..500 h; contains EPS2's D = 1100 and D = 1500)
HS = (dl.q(1), dl.q(3), dl.q(4))     # 1, 4 ASSUMED (EPS2 T1); 3 SOURCED (Phoenix event, 3 h)
SPACING = dl.q(24)                   # CHOICE (EPS2 T1: one offer every 24 wall hours at hours 24..984)
P_JOB = dl.q(1)                      # ASSUMED (section 3's 100 MW fleet (ASSUMED) over 100 jobs: 1 MW per job)
GRID = tuple(dl.q(s) for s in ("0.01", "0.02", "0.05", "0.2", "0.5", "2", "5", "10", "20"))  # ASSUMED (EPS2 T1)
N_GROUPS = 3                         # CHOICE: slack terciles (tight, middle, loose) for 'largest for tight-slack jobs'
GRAN = (2, 3, 4, 5, 10)              # sensitivity (not scored): other group counts
SPREADS_SENS = ((dl.q(1), "slack_i = 1 i h (1..100 h)"),
                (dl.q("0.05"), "slack_i = 0.05 i h (0.05..5 h)"),
                (dl.q(10), "slack_i = 10 i h (10..1000 h)"))   # ASSUMED sensitivity spreads (not scored)
SPACING_SENS = (dl.q(12), dl.q(48))  # CHOICE (EPS2 T1's spacing sensitivity; not scored)
ARMS = (dl.WALL, dl.OWN, dl.ETM)
EPS2_TXT = dl.EPS2_TXT

POST_FIRST_RUN_CHANGES: list[str] = [
    "(1) bug fix, second reading (not scored): the per-tercile MW shortfall against ETM was an absolute MW sum, so with terciles of "
    "34/33/33 jobs an arm supplying nothing read 'tight largest' only because the tight tercile is one job larger; it is now the "
    "shortfall as a fraction of the tercile's MW (46 of 46 'tight largest' cases in the first run); scored reading unchanged",
]


def f(x, d=6) -> str:
    return "-" if x is None else f"{float(x):.{d}f}"


def relx(a: Fr, b: Fr) -> Fr:
    m = max(abs(a), abs(b))
    return ZERO if m == 0 else abs(a - b) / m


def portfolio(step: Fr) -> list[dl.Job]:
    return [dl.Job(W, W + step * i, R, name=f"J{i:03d}") for i in range(1, N_JOBS + 1)]


def groups(n: int, g: int) -> list[range]:
    """Split jobs 0..n-1 (sorted by slack, ascending) into g contiguous groups of sizes as equal as possible, the first n % g
    groups one larger (numpy.array_split's rule)."""
    base, extra = divmod(n, g)
    out, s = [], 0
    for i in range(g):
        size = base + (1 if i < extra else 0)
        out.append(range(s, s + size))
        s += size
    return out


def analyse(jobs: list[dl.Job], H: Fr, spacing: Fr, full: bool) -> dict:
    """Per job and arm: p_all (the minimum flat payment at which the job accepts every offer of the season), nmax, and
    (full=True) the p_all check by backward induction, ETM's G-ZERO counts, H0's reservation price."""
    rows = []
    gz_beyond, gz_states, gz_ok = [], 0, 0
    for job in jobs:
        offs = dl.every(spacing, H, job.W)
        K = len(offs)
        r = dict(job=job, slack=job.slack, K=K, pa={}, nm={}, ver={})
        for a in ARMS:
            F = dl.value_fns(job, a, offs)
            pa = dl.p_all(job, a, offs, F)
            r["pa"][a.name] = pa
            r["nm"][a.name] = dl.nmax(job, a, H)
            if full:
                if pa.kind == "threshold":
                    at = dl.play(job, a, offs, pa.x)["events"]
                    below = dl.play(job, a, offs, pa.x - Fr(1, 10 ** 6))["events"]
                    r["ver"][a.name] = ((at == K) == pa.attained) and below < K
                else:
                    r["ver"][a.name] = False
                if a is dl.ETM:
                    gz_beyond += [abs(dl.stake(job, dl.ETM, H, n) - job.rate * job.overhead) for n in range(K)]
                    xa = dl.xstar_all(job, dl.ETM, offs, F)
                    gz_states += len(xa)
                    gz_ok += sum(int(x.kind == "threshold" and x.x == job.overhead / H) for x in xa.values())
        if full:
            r["h0"] = dl.h0_price(job, offs, dl.H0)
        rows.append(r)
    return dict(rows=rows, H=H, K=rows[0]["K"], gz_beyond=gz_beyond, gz_states=gz_states, gz_ok=gz_ok)


def supply(rows, arm: str, pi: Fr) -> Fr:
    """The firm supply curve: MW of the jobs that accept every offer of the season at flat payment pi (pi > p_all, or pi ==
    p_all and attained)."""
    tot = ZERO
    for r in rows:
        pa = r["pa"][arm]
        if pa.kind == "always" or (pa.kind == "threshold" and (pi > pa.x or (pi == pa.x and pa.attained))):
            tot += P_JOB
    return tot


def score(an: dict, g: int = N_GROUPS) -> dict:
    """Q's three parts on the firm supply curve of one cell."""
    rows, H = an["rows"], an["H"]
    rh = R / H
    comp = all(r["pa"][a.name].kind == "threshold" and r["pa"][a.name].closed for r in rows for a in ARMS)
    out = dict(rh=rh, computable=comp)
    if not comp:
        return out
    ex = [r["pa"]["ETM"] for r in rows]
    out["etm_at_rh"] = sum(int(p.x == rh and p.attained) for p in ex)
    out["etm_entries"] = sorted({p.x for p in ex})
    out["flat"] = out["etm_at_rh"] == len(rows)
    out["entries"], out["rising"], out["gaps"], out["gmeans"], out["tight"], out["below_etm"] = {}, {}, {}, {}, {}, {}
    grp = groups(len(rows), g)
    for a in ("OWN", "WALL"):
        ent = sorted({r["pa"][a].x for r in rows})
        out["entries"][a] = ent
        out["rising"][a] = len(ent) >= 2
        gaps = [r["pa"][a].x - r["pa"]["ETM"].x for r in rows]
        out["gaps"][a] = gaps
        gm = [sum((gaps[i] for i in gr), ZERO) / len(gr) for gr in grp]
        out["gmeans"][a] = gm
        out["tight"][a] = gm[0] > max(gm[1:])
        pts = sorted({r["pa"][b].x for r in rows for b in ("ETM", a)})
        out["below_etm"][a] = all(supply(rows, a, p) <= supply(rows, "ETM", p) for p in pts)
    out["holds"] = out["flat"] and all(out["rising"].values()) and all(out["tight"].values())
    out["groups"] = grp
    return out


def monotone_desc(gaps, slacks) -> tuple[bool, Fr, Fr]:
    """Is the per-job gap non-increasing in slack? Where is the largest gap?"""
    mono = all(gaps[i] >= gaps[i + 1] for i in range(len(gaps) - 1))
    im = max(range(len(gaps)), key=lambda i: (gaps[i], -i))
    return mono, slacks[im], gaps[im]


def main() -> int:
    print(f"DR1 check H3: a portfolio of 100 jobs with a spread of deadline slack, the fleet's supply curve (curtailable MW against payment) "
          f"(Grid_Demand_Response/DECLARATION.md section 2, declared at {dl.DECL_AT})")
    print("Declared Q: ETM's curve is flat at R/H; OWN's and WALL's are rising; the gap is largest for tight-slack jobs.")
    print("Declared forecast: Q holds.  Rung R4 (synthetic model); a note, not evidence (R8).")
    print()
    print("INPUTS")
    print("  W = 1000 compute-hours per job, value 1 per compute-hour at completion: DECLARED (section 2 adopts EPS2 T1's units)")
    print("  R = 0.1 h restart overhead per pause event: ASSUMED (EPS2 T1 model constant; docs/citations/eps2_2026-09-29.md, Reading (T1):")
    print("    'no fetched source supplies or contradicts that number'); S = 0 (save time), lost = 0: ASSUMED (EPS2 T1 has neither)")
    print("  100 jobs: DECLARED (H3). Their deadline slack D - W = 5 i h, i = 1..100 (5..500 h, 0.5 % to 50 % of W, equal steps): ASSUMED;")
    print("    no fetched source gives a distribution of training-job deadline slack (the Acun et al. QoS threshold in")
    print("    docs/citations/dr1_f1_2026-09-29.md is re-typed there, not quoted, so it is not used). The spread contains EPS2 T1's two")
    print("    cells, D = 1100 (job J020) and D = 1500 (job J100). Its tightest job (5 h) is above the 41 x 0.1 = 4.1 h that ETM's")
    print("    own-step deadline needs for every offer of the season; SENSITIVITY 2 prints spreads below that.")
    print("  H (event length) in {1, 3, 4} h: 1 and 4 ASSUMED (EPS2 T1); 3 SOURCED (docs/citations/dr1_f1_2026-09-29.md, Colangelo et al.")
    print("    arXiv:2507.00909 v1: 'Each event required the cluster to reduce power by 25% [...] sustain the reduction for 3 hours')")
    print("  one offer every 24 wall hours at hours 24..984 (K = 41), the same offers to every job, made with certainty (p = 1): CHOICE")
    print("    (EPS2 T1's schedule); spacing 12 and 48 h in SENSITIVITY 3 (EPS2 T1's spacing sensitivity)")
    print("  1 MW per job (a 100 MW fleet): ASSUMED (DECLARATION.md section 3: 'A hypothetical AI training fleet of 100 MW (ASSUMED),")
    print("    running jobs of the H3 portfolio'); every job at full power when it runs; power drawn while paused 0: ASSUMED (EPS2 T1)")
    print("  payment grid {0.01, 0.02, 0.05, 0.2, 0.5, 2, 5, 10, 20} per curtailed fleet-hour: ASSUMED (EPS2 T1); the second reading only")
    print()
    print("CHOICES")
    print("  C1 arms (drlib): WALL values the job on the wall clock with a wall-clock deadline; OWN on its own steps with a wall-clock")
    print("     deadline; ETM a lossless pause with the deadline in own steps (W + n R <= D). Each job decides every offer by exact backward")
    print("     induction (ties accept) at a flat payment pi per curtailed fleet-hour; it may let its deadline pass. TIER is not in H3's Q")
    print("     and is not run; H0 (EPS2's interruptible-load reservation price) is printed as context only.")
    print("  C2 'curtailable MW against payment' (scored) = the firm supply curve: at a flat payment pi, the MW of the jobs that accept")
    print("     every offer of the season (pi >= the job's p_all, EPS2's decisive reading; the step at p_all belongs to the curve when the")
    print("     job accepts at p_all itself). A job's entry price is its p_all. The curve is exact (a step function with one step per")
    print("     distinct entry price). A second reading (not scored): the season-average curtailed MW per offered event at pi, from each")
    print("     job's backward-induction play at pi, on the payment grid and at R/H.")
    print("  C3 'ETM's curve is flat at R/H' = every job's entry price is exactly R/H and attained (the curve is a single step of 100 MW at")
    print("     R/H). 'Rising' = the curve steps at two or more distinct payments. Q is not computable in a cell where some job's p_all")
    print("     is not a closed threshold (the firm curve is then not a step function of entry prices).")
    print("  C4 'the gap' = per job, the arm's entry price minus ETM's; summed over the jobs (x 1 MW) it is the area between the two")
    print("     firm supply curves (MW x payment). 'Largest for tight-slack jobs' = the jobs split by slack into three contiguous groups")
    print("     of 34, 33, 33 (tight, middle, loose; the first group one larger), and the tight group's mean gap is strictly larger than")
    print("     each other group's. Other group counts, and whether the per-job gap is non-increasing in slack, are printed (not scored).")
    print("  C5 Q holds in a cell iff all three parts hold for both OWN and WALL; Q holds iff it holds in every cell (H = 1, 3, 4);")
    print("     Q is not computable if any cell is not computable.")
    print("  C6 offers are live only while the job runs (drlib); every offer here precedes hour 1000, so every job is running at every offer.")
    print()

    # ------------------------------------------------------------------------------------------------ the scored cells
    jobs = portfolio(SLACK_STEP)
    cells = {H: analyse(jobs, H, SPACING, True) for H in HS}
    scores = {H: score(an) for H, an in cells.items()}

    print("PER-EVENT ARITHMETIC (drlib.event, per arm: curtailed fleet-hours e, charge c on the arm's valuation, deadline budget used)")
    for H in HS:
        parts = []
        for a in ARMS:
            ev = dl.event(jobs[0], a, H)
            parts.append(f"{a.name} e {dl.g(ev['e'])} c {dl.g(ev['charge'])} deadline use {dl.g(ev['deadline_use'])}")
        print(f"  H = {dl.g(H)}: " + "; ".join(parts) + f"; R/H = {f(R / H)}")
    print()

    # cross-check against EPS2 T1's pinned table (D = 1100 is job J020, D = 1500 is job J100; H = 1 and 4)
    pinned = EPS2_TXT.read_text(encoding="utf-8").splitlines()
    xc_n = xc_ok = 0
    for H in (dl.q(1), dl.q(4)):
        for idx in (19, 99):
            r = cells[H]["rows"][idx]
            frag = (f"{float(r['pa']['WALL'].x):>12.6f} {float(r['pa']['OWN'].x):>12.6f} {float(r['pa']['ETM'].x):>10.6f} "
                    f"{float(r['h0']):>10.6f}")
            head = f"{dl.g(r['job'].D):>5} {dl.g(H):>2} {r['K']:>3}"
            xc_n += 1
            xc_ok += int(any(head in l and frag in l for l in pinned))
    print(f"EPS2 CROSS-CHECK: jobs J020 (D = 1100) and J100 (D = 1500) at H = 1 and 4, p_all WALL/OWN/ETM and H0 found in the pinned "
          f"Empty_Pause_Systems/batches/eps2_01.txt table: {xc_ok} of {xc_n}")
    print()

    print("PER-JOB TABLES (scored reading). Per job: slack D - W (h); nmax = the events the arm's deadline clock absorbs (41 offers);")
    print("p_all per arm = the job's entry price on the firm supply curve (per curtailed fleet-hour); gap = the arm's p_all minus ETM's;")
    print("H0 = EPS2's interruptible-load reservation price (context); ver = p_all confirmed by backward induction at p_all and at")
    print("p_all - 1e-06 for all three arms; closed = every state's acceptance region is [x*, infinity) for all three arms")
    for H in HS:
        an = cells[H]
        print(f"  cell H = {dl.g(H)} (K = {an['K']}, R/H = {f(R / H)}):")
        print(f"    {'job':5} {'slack':>6} {'nmax W/O/E':>15} {'p_all WALL':>12} {'p_all OWN':>12} {'p_all ETM':>10} "
              f"{'gap OWN':>12} {'gap WALL':>12} {'H0':>10} {'ver':>4} {'closed':>7}")
        for r in an["rows"]:
            pa = r["pa"]
            nm = "/".join("inf" if r["nm"][a.name] is None else str(r["nm"][a.name]) for a in ARMS)
            ver = all(r["ver"].values())
            cl = all(pa[a.name].closed for a in ARMS)
            print(f"    {r['job'].name:5} {dl.g(r['slack']):>6} {nm:>15} {f(pa['WALL'].x):>12} {f(pa['OWN'].x):>12} {f(pa['ETM'].x):>10} "
                  f"{f(pa['OWN'].x - pa['ETM'].x):>12} {f(pa['WALL'].x - pa['ETM'].x):>12} {f(r['h0']):>10} {dl.yn(ver):>4} {dl.yn(cl):>7}")
        nver = sum(int(all(r["ver"].values())) for r in an["rows"])
        print(f"    p_all confirmed by backward induction for {nver} of {len(an['rows'])} jobs")
    print()

    print("FIRM SUPPLY CURVES (scored reading): per arm, each step as (entry price -> cumulative MW at and above it); the curve is 0 MW")
    print("below its first step")
    for H in HS:
        rows = cells[H]["rows"]
        print(f"  cell H = {dl.g(H)}:")
        for a in ("ETM", "OWN", "WALL"):
            ent = sorted({r["pa"][a].x for r in rows})
            steps = [f"{f(x, 6)}->{dl.g(supply(rows, a, x))}" for x in ent]
            print(f"    {a:4} ({len(ent)} steps): " + ", ".join(steps))
    print()

    print("SCORED Q PER CELL")
    for H in HS:
        s = scores[H]
        if not s["computable"]:
            print(f"  H = {dl.g(H)}: not computable (a p_all is not a closed threshold)")
            continue
        print(f"  H = {dl.g(H)}: ETM entry prices {', '.join(f(x) for x in s['etm_entries'])}; jobs entering exactly at R/H = {f(s['rh'])} "
              f"(attained): {s['etm_at_rh']} of {N_JOBS} -> flat at R/H: {dl.yn(s['flat'])}")
        for a in ("OWN", "WALL"):
            gm = s["gmeans"][a]
            print(f"    {a}: {len(s['entries'][a])} distinct entry prices from {f(s['entries'][a][0])} to {f(s['entries'][a][-1])} -> rising: "
                  f"{dl.yn(s['rising'][a])}; never above ETM's curve: {dl.yn(s['below_etm'][a])}; mean gap tight/middle/loose "
                  f"(slack {'/'.join(f'{dl.g(jobs[gr[0]].slack)}-{dl.g(jobs[gr[-1]].slack)}' for gr in s['groups'])} h) = "
                  f"{' / '.join(f(x) for x in gm)}; area between the curves {f(sum(s['gaps'][a], ZERO) * P_JOB, 4)} MW x payment "
                  f"-> largest for tight-slack jobs: {dl.yn(s['tight'][a])}")
        print(f"    cell: Q {'holds' if s['holds'] else 'fails'}")
    print()

    print("THE GAP AGAINST SLACK (description, not scored): is the per-job gap non-increasing in slack, and where is the largest gap")
    for H in HS:
        s = scores[H]
        if not s["computable"]:
            continue
        slacks = [r["slack"] for r in cells[H]["rows"]]
        for a in ("OWN", "WALL"):
            mono, sl, gx = monotone_desc(s["gaps"][a], slacks)
            nbind = sum(int(r["nm"][a] is not None and r["nm"][a] < r["K"]) for r in cells[H]["rows"])
            print(f"  H = {dl.g(H)} {a}: non-increasing in slack: {dl.yn(mono)}; largest gap {f(gx)} at slack {dl.g(sl)} h; jobs whose slack "
                  f"cannot absorb all {cells[H]['K']} events (nmax < K): {nbind} of {N_JOBS}")
    print()

    # ------------------------------------------------------------------------------------------------ the second reading
    print("SECOND READING (not scored): season-average curtailed MW per offered event at flat payment pi (sum over jobs of events x H x")
    print("1 MW / (K x H)), from each job's backward-induction play; per tercile (tight/middle/loose) the MW shortfall against ETM as a")
    print("fraction of the tercile's MW (0: supplies as much as ETM; 1: supplies nothing while ETM supplies all)")
    s2_tight_n = s2_tot = 0
    for H in HS:
        rows = cells[H]["rows"]
        K = cells[H]["K"]
        rh = R / H
        pis = sorted(set(GRID) | {rh})
        grp = groups(len(rows), N_GROUPS)
        print(f"  cell H = {dl.g(H)}:  {'pi':>9} {'ETM MW':>9} {'OWN MW':>9} {'WALL MW':>9}   OWN shortfall t/m/l          WALL shortfall t/m/l"
              f"         tight largest OWN/WALL")
        for pi in pis:
            ev = {}
            for a in ARMS:
                ev[a.name] = [dl.play(r["job"], a, dl.every(SPACING, H, r["job"].W), pi)["events"] for r in rows]
            mw = {a: Fr(sum(v), K) * P_JOB for a, v in ev.items()}
            sf, tl = {}, {}
            for a in ("OWN", "WALL"):
                sf[a] = [Fr(sum(ev["ETM"][i] - ev[a][i] for i in gr), K * len(gr)) for gr in grp]
                tl[a] = sf[a][0] > max(sf[a][1:])
            if mw["ETM"] > 0:
                s2_tot += 2
                s2_tight_n += int(tl["OWN"]) + int(tl["WALL"])
            print(f"                 {f(pi, 4):>9} {f(mw['ETM'], 3):>9} {f(mw['OWN'], 3):>9} {f(mw['WALL'], 3):>9}   "
                  f"{' / '.join(f(x, 3) for x in sf['OWN']):<28} {' / '.join(f(x, 3) for x in sf['WALL']):<28} "
                  f"{dl.yn(tl['OWN'])}/{dl.yn(tl['WALL'])}")
    print(f"  at payments where ETM supplies (pi >= R/H), the tight tercile's shortfall is strictly the largest in {s2_tight_n} of {s2_tot} "
          f"(arm, cell, pi) cases")
    print()

    # ------------------------------------------------------------------------------------------------ sensitivities (not scored)
    print("SENSITIVITY 1 (not scored): the number of slack groups for 'largest for tight-slack jobs' (scored: 3); per cell and arm, the")
    print("  tightest group's mean gap is strictly the largest: yes/no")
    for gnum in GRAN:
        parts = []
        for H in HS:
            s = score(cells[H], gnum)
            if not s["computable"]:
                parts.append(f"H {dl.g(H)}: not computable")
                continue
            parts.append(f"H {dl.g(H)}: OWN {dl.yn(s['tight']['OWN'])} WALL {dl.yn(s['tight']['WALL'])} (Q {'holds' if s['holds'] else 'fails'})")
        print(f"  {gnum:>2} groups: " + "; ".join(parts))
    print()

    print("SENSITIVITY 2 (not scored): other slack spreads (ASSUMED); per cell the three parts of Q (flat / OWN, WALL rising / OWN, WALL")
    print("  tight largest with terciles) and ETM's entry prices")
    for step, desc in SPREADS_SENS:
        js = portfolio(step)
        parts = []
        for H in HS:
            an = analyse(js, H, SPACING, False)
            s = score(an)
            if not s["computable"]:
                parts.append(f"H {dl.g(H)}: not computable")
                continue
            ee = s["etm_entries"]
            parts.append(f"H {dl.g(H)}: flat {dl.yn(s['flat'])} ({s['etm_at_rh']} of {N_JOBS} at R/H; ETM entry {f(ee[0], 4)}..{f(ee[-1], 4)}), "
                         f"rising {dl.yn(s['rising']['OWN'])}/{dl.yn(s['rising']['WALL'])}, tight {dl.yn(s['tight']['OWN'])}/{dl.yn(s['tight']['WALL'])}"
                         f" -> Q {'holds' if s['holds'] else 'fails'}")
        print(f"  {desc}:")
        for p_ in parts:
            print(f"    {p_}")
    print()

    print("SENSITIVITY 3 (not scored): offer spacing 12 and 48 h (EPS2's), the scored spread; per cell the three parts of Q")
    for sp in SPACING_SENS:
        parts = []
        for H in HS:
            an = analyse(jobs, H, sp, False)
            s = score(an)
            if not s["computable"]:
                parts.append(f"H {dl.g(H)}: not computable")
                continue
            parts.append(f"H {dl.g(H)} (K = {an['K']}): flat {dl.yn(s['flat'])} ({s['etm_at_rh']} of {N_JOBS}), rising "
                         f"{dl.yn(s['rising']['OWN'])}/{dl.yn(s['rising']['WALL'])} ({len(s['entries']['OWN'])}/{len(s['entries']['WALL'])} steps), "
                         f"tight {dl.yn(s['tight']['OWN'])}/{dl.yn(s['tight']['WALL'])} -> Q {'holds' if s['holds'] else 'fails'}")
        print(f"  spacing {dl.g(sp)} h:")
        for p_ in parts:
            print(f"    {p_}")
    print()

    # ------------------------------------------------------------------------------------------------ Q
    comp = all(s["computable"] for s in scores.values())
    if not comp:
        q_word = "not computable"
    else:
        q_word = "holds" if all(s["holds"] for s in scores.values()) else "fails"
    nh = sum(int(s.get("holds", False)) for s in scores.values())
    fc_right = {"holds": "right", "fails": "wrong", "not computable": "not decidable"}[q_word]
    parts = []
    for H, s in scores.items():
        if s["computable"]:
            parts.append(f"H {dl.g(H)}: flat {dl.yn(s['flat'])}, rising {dl.yn(s['rising']['OWN'])}/{dl.yn(s['rising']['WALL'])}, "
                         f"tight {dl.yn(s['tight']['OWN'])}/{dl.yn(s['tight']['WALL'])}")
    print(f"Q (scored): cells in which all three parts hold for OWN and WALL: {nh} of {len(scores)} ({'; '.join(parts)}) -> Q {q_word}; "
          f"the forecast 'Q holds' is {fc_right}")
    print()

    # ------------------------------------------------------------------------------------------------ the gate
    beyond = [b for an in cells.values() for b in an["gz_beyond"]]
    xs_n = sum(an["gz_states"] for an in cells.values())
    xs_ok = sum(an["gz_ok"] for an in cells.values())
    gz = max(beyond) == 0 and xs_ok == xs_n
    ahead, maxrel_neg, n_neg = [], ZERO, 0
    for H in HS:
        for pi in GRID:
            fw = dl.fleet_play(jobs, dl.WALL, (), pi, P_JOB)
            fe = dl.fleet_play(jobs, dl.ETM, (), pi, P_JOB)
            for rw, re_ in zip(fw["rows"], fe["rows"]):
                n_neg += 1
                ahead.append(re_["MWh"] > rw["MWh"] and relx(re_["MWh"], rw["MWh"]) > TOL)
                ahead.append(re_["valuation"] > rw["valuation"] and relx(re_["valuation"], rw["valuation"]) > TOL)
                ahead.append(re_["completion"] < rw["completion"] and relx(re_["completion"], rw["completion"]) > TOL)
                ahead.append(re_["met"] and not rw["met"])
                maxrel_neg = max(maxrel_neg, *(relx(re_[k], rw[k]) for k in ("MWh", "valuation", "completion")))
            ahead.append(fe["MWh"] > fw["MWh"] and relx(fe["MWh"], fw["MWh"]) > TOL)
            ahead.append(fe["met"] > fw["met"] and relx(Fr(fe["met"]), Fr(fw["met"])) > TOL)
            maxrel_neg = max(maxrel_neg, relx(fe["MWh"], fw["MWh"]), relx(Fr(fe["met"]), Fr(fw["met"])))
    n_ahead = sum(int(b) for b in ahead)
    gn = n_ahead == 0
    print("GATE")
    print(f"  G-ZERO: ETM's stake beyond its restart overhead, max |stake - R| over {len(beyond)} (job, event count) pairs in {len(cells)} cells = "
          f"{f(max(beyond), 6)} (exact {max(beyond)}); ETM's x* == R/H at {xs_ok} of {xs_n} offer states -> {'holds' if gz else 'FAILS'}")
    print(f"  G-NEG: no events offered (K = 0), {n_neg} job x cell x pi combinations and the fleet totals; ETM ahead of WALL by more than 1 % "
          f"on {n_ahead} of {len(ahead)} outcome comparisons (per job: curtailed MWh, valuation, completion, deadline met; fleet: MWh, "
          f"jobs meeting their deadline); max rel over the numeric outcomes {f(maxrel_neg, 6)} -> {'holds' if gn else 'FAILS'}")
    print()
    print("POST-FIRST-RUN CHANGES: " + ("none" if not POST_FIRST_RUN_CHANGES else "; ".join(POST_FIRST_RUN_CHANGES)))
    print()
    print(f"RESULT H3: Q {q_word}; G-ZERO {'holds' if gz else 'FAILS'} (max |ETM stake - R| = {f(max(beyond), 6)} over {len(beyond)} "
          f"(job, event count) pairs, x* == R/H at {xs_ok} of {xs_n} offer states); G-NEG {'holds' if gn else 'FAILS'} (no events: ETM "
          f"ahead of WALL by > 1 % on {n_ahead} of {len(ahead)} outcome comparisons)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

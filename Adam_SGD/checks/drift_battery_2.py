"""The drifting-world battery, redesigned after Declaration 2's gate closed on two instrument defects (AGENT_LOG 92).
Declared in Adam_SGD/DECLARATION_3.md before its first full run; a POST-HOC redesign (the first gate's output was seen),
labelled so wherever quoted. Synthetic, no data (rung R4). Every label is computed (R15).

Changes against drift_battery.py, and only these:
  headroom   the two-task worlds use make_model(mismatch=1) (F drawn like H), so the past no longer dominates the
             objective and a constant that barely moves is far from optimal; every world prints the headroom
             h = oracle / best constant (held-out); a world is DECISIVE for a win only if h <= 0.9, else UNDECIDABLE-FOR-WIN
  edges      every grid is extended in both directions (lambda 1e-6..1e4; SGD lr 0.05 x 2^k, k = -14..4; momentum
             0.005 x 2^k, same k; Adam 0.01 x 2^k, k = -10..5; decoupled Adam lr 0.01 x 2^k, k = -6..3, x the SGD grid for
             lr_q) and every chosen setting carries an EDGE flag if it sits at either end of its grid
  gate       G-STAT2 (c = 16): neither rule AHEAD; G-DRIFT2 (c geometric 1/16 -> 256): if its headroom h > 0.9 or any
             chosen setting (constant, ratio rule, oracle) is on an edge -> UNDECIDABLE; else the ratio rule must read AHEAD
             -> GATE OPEN, otherwise GATE CLOSED
Unchanged: the 'unit' reading with scaled noise (T3' unscaled), 10 tuning / 10 held-out seeds, the arms (fixed with
learning rate tuned jointly; registered rule s 0.9 and ratio rule s 0, learning rate tuned; the oracle), the labels
(AHEAD <= 0.9, BEHIND >= 1.1), the eight-task sequences T1 and T2 (they had headroom-independent verdicts; rerun on the
extended grids), the optimisers (SGD everywhere; momentum, coupled and decoupled Adam on T0' and T2), the sensitivity
design (Omega x noise on T0' and T2 under SGD; > 1 flip of 8 = FRAGILE).
Run: uv run python Adam_SGD/checks/drift_battery_2.py > Adam_SGD/checks/drift_battery_2.txt
"""
from __future__ import annotations

import multiprocessing
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as cm  # noqa: E402
import drift_battery as db  # noqa: E402
import engine as en  # noqa: E402

STEPS = db.STEPS; TUNE = db.TUNE; EVAL = db.EVAL
LAM = tuple(float(v) for v in np.logspace(-6, 4, 61))
LR_SGD = tuple(cm.LR * 2.0 ** k for k in range(-14, 5))
LR_MOM = tuple(cm.LR * (1 - en.BETA_M) * 2.0 ** k for k in range(-14, 5))
LR_ADAM = tuple(cm.ADAM_LR * 2.0 ** k for k in range(-10, 6))
LR_ADAMD = tuple(cm.ADAM_LR * 2.0 ** k for k in range(-6, 4))
HEADROOM = 0.9; MISMATCH = 1.0


def world(name):
    two = dict(reading="unit", mismatch=MISMATCH)
    if name == "G-STAT2": return en.World("TWO", STEPS, c_path=lambda s: np.full(STEPS, 16.0), scale_noise=True, **two)
    if name == "G-DRIFT2": return en.World("TWO", STEPS, c_path=lambda s: np.exp(np.linspace(np.log(1 / 16), np.log(256), STEPS)), scale_noise=True, **two)
    if name == "T0'": return en.World("TWO", STEPS, c_path=db.ou_path, scale_noise=True, **two)
    if name == "T3'": return en.World("TWO", STEPS, c_path=db.ou_path, scale_noise=False, **two)
    return db.world(name)                                                    # T1, T2 unchanged


def lr_pairs(opt):
    if opt == "sgd": return [(lr, None) for lr in LR_SGD]
    if opt == "mom": return [(lr, None) for lr in LR_MOM]
    if opt == "adam": return [(lr, None) for lr in LR_ADAM]
    return [(la, lq) for la in LR_ADAMD for lq in LR_SGD]


def _tune_job(args):
    wname, arm, opt, lr, lr_q, noise, knobs, smooth = args
    sc = en.simulate(world(wname), arm, knobs, TUNE, opt=opt, lr=lr, lr_q=lr_q, smooth=smooth, noise=noise)
    means = np.where(np.all(np.isfinite(sc), axis=1), np.mean(np.where(np.isfinite(sc), sc, 0.0), axis=1), np.inf)
    return args, means


def best_setting(pool, wname, arm, opt, noise=cm.NOISE, omega=1.0, smooth=0.9):
    knobs = LAM if arm in ("fixed", "sched") else (omega,)
    jobs = [(wname, arm, opt, lr, lq, noise, knobs, smooth) for lr, lq in lr_pairs(opt)]
    best = (None, None, None, np.inf)
    for args, means in pool.map(_tune_job, jobs):
        i = int(np.argmin(means))
        if means[i] < best[3]: best = (knobs[i], args[3], args[4], float(means[i]))
    return best


def edges(arm, opt, st):
    """The names of the chosen values that sit at an end of their grid."""
    if st[0] is None: return ["none finite"]
    out = []
    if arm in ("fixed", "sched") and st[0] in (LAM[0], LAM[-1]): out.append("lambda")
    grid = {"sgd": LR_SGD, "mom": LR_MOM, "adam": LR_ADAM, "adamd": LR_ADAMD}[opt]
    if st[1] in (grid[0], grid[-1]): out.append("lr")
    if opt == "adamd" and st[2] in (LR_SGD[0], LR_SGD[-1]): out.append("lr_q")
    return out


def held_out(wname, arm, opt, st, noise=cm.NOISE, smooth=0.9):
    if st[0] is None: return np.full(len(EVAL), np.inf)
    sc = en.simulate(world(wname), arm, [st[0]], EVAL, opt=opt, lr=st[1], lr_q=st[2], smooth=smooth, noise=noise)[0]
    return np.where(np.isfinite(sc), sc, np.inf)


def compare(pool, wname, opt, noise=cm.NOISE, omega=1.0, with_oracle=True, verbose=True):
    fx = best_setting(pool, wname, "fixed", opt, noise=noise)
    rg = best_setting(pool, wname, "rule", opt, noise=noise, omega=omega, smooth=0.9)
    r0 = best_setting(pool, wname, "rule", opt, noise=noise, omega=omega, smooth=0.0)
    s_fx = held_out(wname, "fixed", opt, fx, noise); s_rg = held_out(wname, "rule", opt, rg, noise, 0.9); s_r0 = held_out(wname, "rule", opt, r0, noise, 0.0)
    mfx, mrg, mr0 = (float(np.mean(x)) for x in (s_fx, s_rg, s_r0))
    lab = lambda m: db.label(m / mfx) if np.isfinite(mfx) else ("AHEAD" if np.isfinite(m) else "TIE")
    out = dict(lab_rg=lab(mrg), lab_r0=lab(mr0), mfx=mfx, mr0=mr0,
               edges={"fixed": edges("fixed", opt, fx), "registered": edges("rule", opt, rg), "ratio": edges("rule", opt, r0)})
    if with_oracle:
        orc = best_setting(pool, wname, "sched", opt, noise=noise); mo = float(np.mean(held_out(wname, "sched", opt, orc, noise)))
        out["mor"] = mo; out["edges"]["oracle"] = edges("sched", opt, orc); out["headroom"] = mo / mfx if np.isfinite(mfx) else float("nan")
    if verbose:
        fl = lambda st: f"lr {st[1]:.4g}" + (f", lr_q {st[2]:.4g}" if st[2] is not None else "") if st[0] is not None else "none finite"
        eg = lambda e: (" EDGE(" + ",".join(e) + ")") if e else ""
        print(f"     fixed: lambda {fx[0] if fx[0] is None else f'{fx[0]:.4g}'} ({fl(fx)}){eg(out['edges']['fixed'])} -> held-out {cm.f(mfx)}")
        for nm, st, sc, m, key, lb in (("registered rule (s 0.9)", rg, s_rg, mrg, "registered", out["lab_rg"]), ("ratio rule (s 0)", r0, s_r0, mr0, "ratio", out["lab_r0"])):
            print(f"     {nm}: {fl(st)}{eg(out['edges'][key])} -> held-out {cm.f(m)}; / fixed {(f'{m / mfx:.3f}' if np.isfinite(mfx) and np.isfinite(m) else 'n/a')} -> {lb}; "
                  f"ahead of the constant on {int(np.sum(sc < s_fx))} of {len(EVAL)} held-out seeds")
        if with_oracle:
            h = out["headroom"]
            print(f"     oracle that knows the units: lambda {orc[0] if orc[0] is None else f'{orc[0]:.4g}'} ({fl(orc)}){eg(out['edges']['oracle'])} -> held-out {cm.f(mo)}; "
                  f"headroom oracle / fixed {h:.3f} -> {'DECISIVE for a win' if h <= HEADROOM else 'UNDECIDABLE-FOR-WIN'}; ratio rule / oracle {(f'{mr0 / mo:.3f}' if np.isfinite(mo) and np.isfinite(mr0) else 'n/a')}")
    return out


def main():
    print("The drifting-world battery, redesigned (Adam_SGD/checks/drift_battery_2.py; POST-HOC after Declaration 2's closed gate): "
          f"two-task worlds with make_model(mismatch={MISMATCH:g}); eight-task sequences as before; tune seeds {TUNE[0]}-{TUNE[-1]}, held-out {EVAL[0]}-{EVAL[-1]}; "
          f"lambda {len(LAM)} values {LAM[0]:g}..{LAM[-1]:g}; SGD lr {len(LR_SGD)} values {LR_SGD[0]:.3g}..{LR_SGD[-1]:.3g}; headroom threshold {HEADROOM}")
    res = {}
    with ProcessPoolExecutor(max_workers=4, mp_context=multiprocessing.get_context("fork")) as pool:
        for wname, opts in (("G-STAT2", ("sgd",)), ("G-DRIFT2", ("sgd",)), ("T0'", ("sgd", "mom", "adam", "adamd")),
                            ("T1", ("sgd",)), ("T2", ("sgd", "mom", "adam", "adamd")), ("T3'", ("sgd",))):
            for opt in opts:
                print(f"[{wname} / {opt}]")
                res[(wname, opt)] = compare(pool, wname, opt, with_oracle=(opt == "sgd"))
        gs, gd = res[("G-STAT2", "sgd")], res[("G-DRIFT2", "sgd")]
        stat_ok = gs["lab_rg"] != "AHEAD" and gs["lab_r0"] != "AHEAD"
        gd_edges = [k for k in ("fixed", "ratio", "oracle") if gd["edges"][k]]
        if not stat_ok: gate = "GATE CLOSED (the stationary control reads AHEAD)"
        elif gd["headroom"] > HEADROOM or gd_edges: gate = f"UNDECIDABLE (headroom {gd['headroom']:.3f}; edges on {gd_edges or 'none'})"
        else: gate = "GATE OPEN" if gd["lab_r0"] == "AHEAD" else "GATE CLOSED"
        print(f"\ngate: G-STAT2 registered {gs['lab_rg']}, ratio {gs['lab_r0']} (must not read AHEAD); G-DRIFT2 headroom {gd['headroom']:.3f}, "
              f"edges {gd_edges or 'none'}, ratio {gd['lab_r0']} (must read AHEAD), registered {gd['lab_rg']} (reported) -> {gate}")
        print("\n[S] Sensitivity under SGD: Omega x noise, everything retuned per cell (main cell Omega 1, noise 0.5)")
        for wname in ("T0'", "T2"):
            main = (res[(wname, "sgd")]["lab_rg"], res[(wname, "sgd")]["lab_r0"]); flips = [0, 0]; cells = []
            for om_ in (0.71, 1.0, 1.41):
                for nz in (0.1, 0.5, 1.0):
                    if om_ == 1.0 and nz == 0.5: continue
                    r = compare(pool, wname, "sgd", noise=nz, omega=om_, with_oracle=False, verbose=False)
                    cells.append(f"O{om_:g}/n{nz:g}: {r['lab_rg']}/{r['lab_r0']}")
                    flips[0] += r["lab_rg"] != main[0]; flips[1] += r["lab_r0"] != main[1]
            print(f"     {wname}: " + "  ".join(cells))
            print(f"     {wname}: registered flips {flips[0]} of 8 -> {'FRAGILE' if flips[0] > 1 else 'not fragile'}; ratio flips {flips[1]} of 8 -> {'FRAGILE' if flips[1] > 1 else 'not fragile'}")
    n_edge = sum(1 for r in res.values() for k, e in r["edges"].items() if e)
    print(f"\nedges: {n_edge} chosen settings sit on a grid edge across all comparisons" + ("" if n_edge == 0 else " (listed above as EDGE)"))
    print("summary: " + "; ".join(f"{w}/{o} registered {r['lab_rg']}, ratio {r['lab_r0']}" for (w, o), r in res.items()) + f"; {gate}")


if __name__ == "__main__":
    main()

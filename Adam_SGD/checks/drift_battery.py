"""The drifting-world battery (owner request, prompt-log entry 107): the Omega rule where the right weight moves.
Declared in Adam_SGD/DECLARATION_2.md before the first full run. Synthetic, no data (rung R4). Every label is computed (R15).

Built on the assumption audit (checks/assumptions.txt): the scale of the past term is read as a UNITS ERROR ('unit'
reading: the objective is the true total, the learner sees the past gradient multiplied by c_t) with the noise scaled with
the units, except in the low-signal world T3; every arm has its learning rate tuned; constants are tuned on seeds 0-9 and
scored on held-out seeds 10-19; the fine weight grid spans 1e-5 .. 1e3.

Worlds (engine.py):
  G-STAT   two tasks, c = 16 throughout                                   gate: the rule must NOT read AHEAD
  G-DRIFT  two tasks, c_t geometric from 1/16 to 256 over the run         gate: the ratio rule (smoothing 0) must read AHEAD
  T0       two tasks, log c_t an OU process (sd 1.5, time constant 500 steps) per seed
  T1       eight tasks in sequence, online-EWC penalty with calibrated Fishers (u = 1): lambda = 1 is exact Bayes here
  T2       eight tasks, each task's Fisher miscalibrated by u_j, log-uniform on [1/16, 16] per task and seed
  T3       T0 with the past noise NOT scaled (a low-signal past gradient where c_t is small; the audit's AS3b failure mode)
Arms: fixed lambda (grid x learning rate, tuned jointly); the registered rule (smoothing 0.9, Omega 1; learning rate tuned);
the ratio rule (smoothing 0: the VQGAN-style member of the family; learning rate tuned); the oracle that knows the units
(lambda / c_t in TWO worlds, the calibrated Fishers in SEQ worlds; lambda and learning rate tuned) as a ceiling.
Optimisers: SGD everywhere; heavy-ball momentum, coupled Adam and decoupled Adam on T0 and T2.
Score: the anytime objective (mean over evaluation points every 100 steps), on the held-out seeds. Label of rule /
fixed: AHEAD <= 0.9, BEHIND >= 1.1, else TIE; a constant that diverges on any held-out seed scores infinity.
Sensitivity (T0 and T2 under SGD): Omega in {0.71, 1, 1.41} x noise in {0.1, 0.5, 1.0}, everything retuned per cell;
a label that flips in more than one of the 8 non-main cells is FRAGILE.
Run: uv run python Adam_SGD/checks/drift_battery.py > Adam_SGD/checks/drift_battery.txt
"""
from __future__ import annotations

import multiprocessing
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as cm  # noqa: E402
import engine as en  # noqa: E402

STEPS = cm.STEPS
TUNE = tuple(range(10)); EVAL = tuple(range(10, 20))
LAM = tuple(float(v) for v in np.logspace(-5, 3, 49))
LR_SGD = tuple(cm.LR * 2.0 ** -k for k in range(11))
LR_MOM = tuple(cm.LR * (1 - en.BETA_M) * 2.0 ** -k for k in range(11))
LR_ADAM = tuple(cm.ADAM_LR * 2.0 ** k for k in range(-6, 3))
LR_ADAMD = tuple(cm.ADAM_LR * 2.0 ** k for k in range(-4, 1))
AHEAD = 0.9; BEHIND = 1.1
OU_SD = 1.5; OU_TAU = 500.0; U_RANGE = 16.0; K_TASKS = 8; T_TASK = 500; TASK_SEED = 2026


def ou_path(seed, sd=OU_SD, tau=OU_TAU):
    rng = np.random.default_rng(10_000 + seed); a = np.exp(-1.0 / tau)
    z = np.empty(STEPS); z[0] = sd * rng.standard_normal(); e = rng.standard_normal(STEPS) * sd * np.sqrt(1 - a * a)
    for i in range(1, STEPS): z[i] = a * z[i - 1] + e[i]
    return np.exp(z)


def u_draw(seed, rng_=U_RANGE):
    return np.exp(np.random.default_rng(20_000 + seed).uniform(-np.log(rng_), np.log(rng_), K_TASKS))


def world(name):
    if name == "G-STAT": return en.World("TWO", STEPS, c_path=lambda s: np.full(STEPS, 16.0), reading="unit", scale_noise=True)
    if name == "G-DRIFT": return en.World("TWO", STEPS, c_path=lambda s: np.exp(np.linspace(np.log(1 / 16), np.log(256), STEPS)), reading="unit", scale_noise=True)
    if name == "T0": return en.World("TWO", STEPS, c_path=ou_path, reading="unit", scale_noise=True)
    if name == "T3": return en.World("TWO", STEPS, c_path=ou_path, reading="unit", scale_noise=False)
    if name == "T1": return en.World("SEQ", STEPS, K=K_TASKS, T=T_TASK, task_seed=TASK_SEED, u_draw=lambda s: np.ones(K_TASKS))
    if name == "T2": return en.World("SEQ", STEPS, K=K_TASKS, T=T_TASK, task_seed=TASK_SEED, u_draw=u_draw)
    raise ValueError(name)


def lr_pairs(opt):
    if opt == "sgd": return [(lr, None) for lr in LR_SGD]
    if opt == "mom": return [(lr, None) for lr in LR_MOM]
    if opt == "adam": return [(lr, None) for lr in LR_ADAM]
    return [(la, lq) for la in LR_ADAMD for lq in LR_SGD]


def _tune_job(args):
    """One (world, arm, optimiser, learning-rate pair, noise, Omega-or-grid): mean score on the tuning seeds per knob."""
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


def held_out(wname, arm, opt, knob, lr, lr_q, noise=cm.NOISE, smooth=0.9):
    if knob is None: return np.full(len(EVAL), np.inf)
    sc = en.simulate(world(wname), arm, [knob], EVAL, opt=opt, lr=lr, lr_q=lr_q, smooth=smooth, noise=noise)[0]
    return np.where(np.isfinite(sc), sc, np.inf)


def label(r):
    return "AHEAD" if r <= AHEAD else ("BEHIND" if r >= BEHIND else "TIE")


def compare(pool, wname, opt, noise=cm.NOISE, omega=1.0, with_oracle=True, verbose=True):
    fx = best_setting(pool, wname, "fixed", opt, noise=noise)
    rg = best_setting(pool, wname, "rule", opt, noise=noise, omega=omega, smooth=0.9)
    r0 = best_setting(pool, wname, "rule", opt, noise=noise, omega=omega, smooth=0.0)
    s_fx = held_out(wname, "fixed", opt, fx[0], fx[1], fx[2], noise)
    s_rg = held_out(wname, "rule", opt, rg[0], rg[1], rg[2], noise, 0.9)
    s_r0 = held_out(wname, "rule", opt, r0[0], r0[1], r0[2], noise, 0.0)
    mfx, mrg, mr0 = (float(np.mean(x)) for x in (s_fx, s_rg, s_r0))
    lab_rg = label(mrg / mfx) if np.isfinite(mfx) else ("AHEAD" if np.isfinite(mrg) else "TIE")
    lab_r0 = label(mr0 / mfx) if np.isfinite(mfx) else ("AHEAD" if np.isfinite(mr0) else "TIE")
    out = dict(fx=fx, rg=rg, r0=r0, mfx=mfx, mrg=mrg, mr0=mr0, lab_rg=lab_rg, lab_r0=lab_r0)
    if verbose:
        fmt_lr = lambda s: f"lr {s[1]:.4g}" + (f", lr_q {s[2]:.4g}" if s[2] is not None else "")
        print(f"     fixed: lambda {fx[0] if fx[0] is None else f'{fx[0]:.4g}'} ({fmt_lr(fx) if fx[0] is not None else 'none finite'}) -> held-out {cm.f(mfx)}"
              + (f" (diverges on {int(np.sum(~np.isfinite(s_fx)))} of {len(EVAL)} held-out seeds)" if not np.isfinite(mfx) else ""))
        for nm, st, sc, m, lab in (("registered rule (s 0.9)", rg, s_rg, mrg, lab_rg), ("ratio rule (s 0)", r0, s_r0, mr0, lab_r0)):
            wins = int(np.sum(sc < s_fx))
            print(f"     {nm}: {fmt_lr(st) if st[0] is not None else 'none finite'} -> held-out {cm.f(m)}; / fixed "
                  f"{(f'{m / mfx:.3f}' if np.isfinite(mfx) and np.isfinite(m) else 'n/a')} -> {lab}; ahead of the constant on {wins} of {len(EVAL)} held-out seeds")
        if with_oracle:
            orc = best_setting(pool, wname, "sched", opt, noise=noise)
            mo = float(np.mean(held_out(wname, "sched", opt, orc[0], orc[1], orc[2], noise)))
            out["mor"] = mo
            print(f"     oracle that knows the units: lambda {orc[0] if orc[0] is None else f'{orc[0]:.4g}'} -> held-out {cm.f(mo)}; "
                  f"ratio rule / oracle {(f'{mr0 / mo:.3f}' if np.isfinite(mo) and np.isfinite(mr0) else 'n/a')}")
    return out


def main():
    print("The drifting-world battery (Adam_SGD/checks/drift_battery.py): the two-task quadratic of omega_sweeps.py and an "
          f"eight-task online-EWC sequence; {STEPS} steps (TWO) / {(K_TASKS - 1) * T_TASK} steps (SEQ); tune seeds {TUNE[0]}-{TUNE[-1]}, "
          f"held-out seeds {EVAL[0]}-{EVAL[-1]}; lambda grid {len(LAM)} values {LAM[0]:g}..{LAM[-1]:g}; labels AHEAD <= {AHEAD}, BEHIND >= {BEHIND}")
    # [E0] the engine reproduces common.run
    H, F, a, b = cm.om.make_model(); ok = True
    for arm, knob, sm in (("fixed", 0.05, 0.9), ("rule", 1.0, 0.9), ("rule", 1.0, 0.0)):
        e = en.simulate(world("G-STAT"), arm, [knob], (0, 1), smooth=sm, final=True)[0]
        c = [cm.objective(H, F, a, b, cm.run(arm, knob, H, F, a, b, s, c=16.0, smooth=sm)[0], 16.0, "unit") for s in (0, 1)]
        ok &= bool(np.max(np.abs(e - np.array(c))) <= 1e-9)
    print(f"[E0] the batched engine reproduces common.run (final objective, G-STAT, seeds 0-1, three arms) to 1e-9: {ok}")
    labels = {}
    with ProcessPoolExecutor(max_workers=4, mp_context=multiprocessing.get_context("fork")) as pool:
        for wname, opts in (("G-STAT", ("sgd",)), ("G-DRIFT", ("sgd",)), ("T0", ("sgd", "mom", "adam", "adamd")),
                            ("T1", ("sgd",)), ("T2", ("sgd", "mom", "adam", "adamd")), ("T3", ("sgd",))):
            for opt in opts:
                print(f"[{wname} / {opt}]")
                r = compare(pool, wname, opt, with_oracle=(opt == "sgd"))
                labels[(wname, opt)] = (r["lab_rg"], r["lab_r0"])
        gate = labels[("G-STAT", "sgd")][1] != "AHEAD" and labels[("G-STAT", "sgd")][0] != "AHEAD" and labels[("G-DRIFT", "sgd")][1] == "AHEAD"
        print(f"\ngate: G-STAT registered {labels[('G-STAT', 'sgd')][0]}, ratio {labels[('G-STAT', 'sgd')][1]} (must not read AHEAD); "
              f"G-DRIFT ratio {labels[('G-DRIFT', 'sgd')][1]} (must read AHEAD), registered {labels[('G-DRIFT', 'sgd')][0]} (reported) -> {'GATE OPEN' if gate else 'GATE CLOSED'}")
        print("\n[S] Sensitivity under SGD: Omega x noise, everything retuned per cell (main cell Omega 1, noise 0.5)")
        for wname in ("T0", "T2"):
            main = labels[(wname, "sgd")]; flips = [0, 0]; cells = []
            for om_ in (0.71, 1.0, 1.41):
                for nz in (0.1, 0.5, 1.0):
                    if om_ == 1.0 and nz == 0.5: continue
                    r = compare(pool, wname, "sgd", noise=nz, omega=om_, with_oracle=False, verbose=False)
                    cells.append(f"O{om_:g}/n{nz:g}: {r['lab_rg']}/{r['lab_r0']}")
                    flips[0] += r["lab_rg"] != main[0]; flips[1] += r["lab_r0"] != main[1]
            print(f"     {wname}: " + "  ".join(cells))
            print(f"     {wname}: registered flips {flips[0]} of 8 -> {'FRAGILE' if flips[0] > 1 else 'not fragile'}; ratio flips {flips[1]} of 8 -> {'FRAGILE' if flips[1] > 1 else 'not fragile'}")
    print("\nsummary: " + "; ".join(f"{w}/{o} registered {l[0]}, ratio {l[1]}" for (w, o), l in labels.items()) + f"; gate {'OPEN' if gate else 'CLOSED'}")


if __name__ == "__main__":
    main()

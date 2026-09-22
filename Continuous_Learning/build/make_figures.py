"""Figures for Continuous_Learning/CONTINUOUS_LEARNING.md (owner request 2026-09-22, prompt-log entry 72).
Every figure is drawn from pinned run records (runs/eqx, runs/eq2, runs/eq3) or from the functions of
theory/checks/omega_sweeps.py re-executed here (deterministic); every number placed on a figure that the document
quotes is also printed to stdout, which is pinned as Continuous_Learning/figures/figures.txt (R1).
Run: uv run python Continuous_Learning/build/make_figures.py > Continuous_Learning/figures/figures.txt
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FixedFormatter, FixedLocator, NullFormatter  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "Continuous_Learning" / "figures"
sys.path.insert(0, str(ROOT / "theory" / "checks"))
import omega_sweeps as om  # noqa: E402  (the pinned mathematics script; functions only)

# validated palette (dataviz reference instance, light mode): three categorical slots, sequential blue, diverging blue/red
C1, C2, C3 = "#2a78d6", "#eb6834", "#1baf7a"
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e1"
plt.rcParams.update({"figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "text.color": INK, "axes.grid": True, "grid.color": GRID,
                     "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False, "font.size": 9,
                     "axes.titlesize": 10, "legend.frameon": False, "lines.linewidth": 2, "savefig.dpi": 200, "xtick.minor.visible": False, "ytick.minor.visible": False})
OMEGA9 = om.OMEGA9


def logticks(ax, vals):
    ax.set_xscale("log"); ax.xaxis.set_major_locator(FixedLocator(list(vals))); ax.xaxis.set_major_formatter(FixedFormatter([f"{v:g}" for v in vals]))
    ax.xaxis.set_minor_locator(FixedLocator([])); ax.xaxis.set_minor_formatter(NullFormatter())


def save(fig, name):
    fig.savefig(OUT / name, bbox_inches="tight"); plt.close(fig); print(f"[figure] {name}")


def records(path):
    rows = [json.loads(l) for l in open(path) if l.startswith("{")]
    return rows[0], [r for r in rows[1:] if "acc" in r]


# ---------------------------------------------------------------- F1: the tug of war (fifth-grader picture)
def fig1_tug():
    fig, axes = plt.subplots(3, 1, figsize=(7.5, 6.2))
    for ax, omg in zip(axes, (0.5, 1.0, 2.0)):
        gp, gq = 1.0, 3.0                       # present pull 1, past pull 3 (raw)
        w = omg * gp / gq
        ax.annotate("", xy=(gp, 0.75), xytext=(0, 0.75), arrowprops=dict(arrowstyle="-|>", lw=3, color=C1))
        ax.annotate("", xy=(-gq, 0.45), xytext=(0, 0.45), arrowprops=dict(arrowstyle="-|>", lw=1.2, color=C2, alpha=0.35))
        ax.annotate("", xy=(-w * gq, 0.15), xytext=(0, 0.15), arrowprops=dict(arrowstyle="-|>", lw=3, color=C2))
        net = gp - w * gq
        ax.plot([0, 0], [0.0, 0.9], color=INK2, lw=0.8)
        ax.text(gp / 2, 0.83, "present pull  |g_p| = 1", ha="center", color=C1, fontsize=8)
        ax.text(-gq / 2, 0.53, "past pull as it comes  |g_q| = 3", ha="center", color=INK2, fontsize=8)
        ax.text(-w * gq / 2, 0.23, f"past pull after the rule  w·|g_q| = Ω·|g_p| = {omg * gp:g}", ha="center", color=C2, fontsize=8)
        ax.text(-3.4, 0.85, f"Ω = {omg:g}", fontsize=11, color=INK, weight="bold")
        ax.text(2.2, 0.45, f"net pull = {net:+.1f}\n" + ("→ moves toward the NEW task" if net > 0 else ("→ stands still" if abs(net) < 1e-12 else "→ moves toward the OLD task")), fontsize=9, color=INK, va="center")
        ax.set_xlim(-3.6, 4.2); ax.set_ylim(0.0, 1.0); ax.axis("off")
        print(f"[F1] Omega {omg:g}: w = {w:.4f}, net pull {net:+.4f}")
    fig.suptitle("The rule rescales the past pull to Ω times the present pull. In one dimension the net pull is (1 − Ω) × present pull.", x=0.01, ha="left", fontsize=10)
    save(fig, "F01_tug_of_war.png")


# ---------------------------------------------------------------- F2/F3: the Pareto curve, the rule's field and its trajectories (2-D quadratic model)
def model2d():
    H = np.diag([1.0, 0.5]); F = 16 * np.diag([1.0, 1.5]); a = np.array([2.0, 1.0]); b = np.array([0.0, 0.0])
    return H, F, a, b


def fig2_field():
    H, F, a, b = model2d()
    lam = np.logspace(-3, 3, 400); curve = np.array([om.pareto(H, F, a, b, l) for l in lam])
    xs = np.linspace(-0.6, 2.6, 27); ys = np.linspace(-0.6, 1.6, 23); X, Y = np.meshgrid(xs, ys)
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.4), sharey=True)
    for ax, omg in zip(axes, (0.7, 1.0, 1.4)):
        Lp = np.array([[om.losses(H, F, a, b, np.array([x, y]))[0] for x in xs] for y in ys])
        Lq = np.array([[om.losses(H, F, a, b, np.array([x, y]))[1] for x in xs] for y in ys])
        ax.contour(X, Y, Lp, levels=8, colors=C1, linewidths=0.6, alpha=0.6); ax.contour(X, Y, Lq, levels=8, colors=C2, linewidths=0.6, alpha=0.6)
        U = np.zeros_like(X); V = np.zeros_like(Y)
        for i in range(len(ys)):
            for j in range(len(xs)):
                th = np.array([xs[j], ys[i]]); gp = H @ (th - a); gq = F @ (th - b)
                upd = -(gp + omg * np.linalg.norm(gp) / max(np.linalg.norm(gq), 1e-12) * gq); U[i, j], V[i, j] = upd
        ax.quiver(X, Y, U, V, color=INK2, alpha=0.7, scale=40, width=0.003)
        ax.plot(curve[:, 0], curve[:, 1], color=C3, lw=2.5, label="Pareto curve θ(λ)")
        ax.plot(*a, "o", color=C1, ms=8); ax.plot(*b, "o", color=C2, ms=8)
        ax.text(a[0] - 0.05, a[1] + 0.12, "new-task optimum a", color=C1, fontsize=8, ha="right"); ax.text(b[0] + 0.08, b[1] - 0.2, "old-task optimum b", color=C2, fontsize=8)
        ax.set_title(f"Ω = {omg:g}", loc="left"); ax.set_xlabel("θ₁")
        # update norm on the curve
        rel = []
        for l in (0.1, 1.0, 10.0):
            th = om.pareto(H, F, a, b, l); gp = H @ (th - a); gq = F @ (th - b)
            rel.append(np.linalg.norm(gp + omg * np.linalg.norm(gp) / np.linalg.norm(gq) * gq) / np.linalg.norm(gp))
        print(f"[F2] Omega {omg:g}: |update|/|g_p| on the curve at lambda 0.1, 1, 10 = {rel[0]:.6f}, {rel[1]:.6f}, {rel[2]:.6f}")
    axes[0].set_ylabel("θ₂"); axes[1].legend(loc="upper left", fontsize=8)
    fig.suptitle("Update field of g_p + Ω·(|g_p|/|g_q|)·g_q in a two-dimensional two-task model (blue contours: new-task loss; orange: old-task penalty).\nOn the green curve the two pulls are antiparallel; at Ω = 1 the update vanishes everywhere on it.", x=0.01, ha="left", fontsize=9)
    fig.tight_layout(rect=(0, 0, 1, 0.93)); save(fig, "F02_pareto_field.png")


def fig3_trajectories():
    H, F, a, b = model2d()
    lam = np.logspace(-3, 3, 400); curve = np.array([om.pareto(H, F, a, b, l) for l in lam])
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    cols = plt.cm.Blues(np.linspace(0.35, 0.95, len(OMEGA9)))
    for ax, sm, title in zip(axes, (0.0, om.SMOOTH), ("exact rule (instantaneous norms)", "registered estimator (EMA 0.9 of the gradients, cap 1e4)")):
        ax.plot(curve[:, 0], curve[:, 1], color=C3, lw=2.5, label="Pareto curve")
        ax.plot(*a, "o", color=C1, ms=8, label="new-task optimum a"); ax.plot(*b, "o", color=C2, ms=8, label="old-task optimum b (start)")
        for omg, c in zip(OMEGA9, cols):
            th = b.copy(); ema_p = ema_q = None; path = [th.copy()]
            for _ in range(1500):
                gp = H @ (th - a); gq = F @ (th - b)
                ema_p = gp if (ema_p is None or sm == 0) else sm * ema_p + (1 - sm) * gp
                ema_q = gq if (ema_q is None or sm == 0) else sm * ema_q + (1 - sm) * gq
                w = om.rule_w(ema_p, ema_q, omg); th = th - 0.02 * (gp + w * gq); path.append(th.copy())
            path = np.array(path)
            ax.plot(path[:, 0], path[:, 1], color=c, lw=1.0, alpha=0.85, label=f"Ω = {omg:g}")
            ax.plot(path[-1, 0], path[-1, 1], "s", color=c, ms=6, clip_on=True)
            Lp, Lq = om.losses(H, F, a, b, path[-1]); le, dist = om.lam_eff(H, F, a, b, path[-1])
            print(f"[F3] {title}: Omega {omg:g} endpoint ({path[-1, 0]:.4f}, {path[-1, 1]:.4f}) L_present {Lp:.4f} L_past {Lq:.4f} lambda_eff {le:.4g} distance to curve {dist:.2e}")
        ax.set_title(title, loc="left"); ax.set_xlabel("θ₁"); ax.set_xlim(-0.4, 2.4); ax.set_ylim(-0.4, 1.4)
    axes[0].set_ylabel("θ₂"); axes[1].legend(loc="upper left", fontsize=7, ncol=2, title="paths by Ω (squares: endpoints)", title_fontsize=7)
    fig.suptitle("Where the rule stops, starting from the old-task optimum, for nine values of Ω (1500 steps, lr 0.02); light = small Ω, dark = large Ω", x=0.01, ha="left", fontsize=10)
    save(fig, "F03_trajectories.png")


# ---------------------------------------------------------------- F4: the plateau under noise (5-D model of omega_sweeps.py)
def fig4_plateau():
    H, F, a, b = om.make_model()
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    for noise, c, lab in ((0.0, C1, "noise 0"), (0.5, C2, "noise 0.5"), (2.0, C3, "noise 2")):
        tot = []
        for omg in OMEGA9:
            vals = []
            for s in range(5):
                th, _, ok = om.gd(H, F, a, b, "eq", omg, lr=0.05, noise=noise, seed=s)
                Lp, Lq = om.losses(H, F, a, b, th); vals.append(Lp + Lq if ok else np.nan)
            tot.append(float(np.mean(vals)))
        ax.plot(OMEGA9, tot, "-o", color=c, ms=5, label=lab); ax.text(OMEGA9[-1] * 1.05, tot[-1], lab, color=c, fontsize=8, va="center")
        print(f"[F4] {lab}: total loss per Omega " + " ".join(f"{o:g}:{t:.3f}" for o, t in zip(OMEGA9, tot)))
    logticks(ax, OMEGA9); ax.set_xlim(0.2, 5.5)
    ax.set_xlabel("Ω"); ax.set_ylabel("L_present + L_past at the end (5 seeds, mean)")
    ax.set_title("Registered estimator: mini-batch noise turns the knife edge at Ω = 1 into a plateau", loc="left")
    save(fig, "F04_plateau.png")


# ---------------------------------------------------------------- F5: the stability edge of a fixed weight vs the rule
def fig5_edge():
    H, F, a, b = om.make_model(); lr = 0.05
    lam_edge = (2.0 / lr - np.diag(H).max()) / np.diag(F).max()
    lams = np.logspace(-2, 1.2, 40); tot = []; ok_ = []
    for l in lams:
        th, _, ok = om.gd(H, F, a, b, "fixed", l, lr=lr); Lp, Lq = om.losses(H, F, a, b, th); tot.append(Lp + Lq if ok else np.nan); ok_.append(ok)
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    ax.plot(lams, tot, "-", color=C1, label="fixed weight λ (converged)")
    div = [l for l, o in zip(lams, ok_) if not o]
    if div:
        ax.axvspan(min(div), lams[-1], color=C2, alpha=0.12); ax.text(min(div) * 1.05, np.nanmax(tot) * 0.9, "fixed λ diverges", color=C2, fontsize=8)
    ax.axvline(lam_edge, color=C2, ls="--", lw=1.2); ax.text(lam_edge * 1.05, np.nanmax(tot) * 0.55, f"edge λ* = {lam_edge:.3f}", color=C2, fontsize=8)
    th, wlog, _ = om.gd(H, F, a, b, "eq", 1.0, lr=lr); Lp, Lq = om.losses(H, F, a, b, th); le, _ = om.lam_eff(H, F, a, b, th)
    ax.plot([le], [Lp + Lq], "s", color=C3, ms=9, label="rule at Ω = 1 (registered estimator)")
    ax.text(le * 1.1, Lp + Lq, f"rule stops at λ_eff = {le:.3g}, median w = {np.median(wlog):.3g}", color=C3, fontsize=8)
    print(f"[F5] edge lambda* = {lam_edge:.4f}; fixed converged for lambda <= {max([l for l, o in zip(lams, ok_) if o]):.4f}; first divergent lambda {min(div) if div else float('nan'):.4f}; rule Omega=1 lambda_eff {le:.4g} total loss {Lp + Lq:.4f} median w {np.median(wlog):.4g}")
    ax.set_xscale("log"); ax.set_xlabel("penalty weight λ"); ax.set_ylabel("L_present + L_past at the end"); ax.legend(loc="center right", fontsize=8)
    ax.set_title("A fixed weight has a stability edge at lr·(h_max + λ·f_max) = 2; the rule's step is bounded by the present step", loc="left")
    save(fig, "F05_stability_edge.png")


# ---------------------------------------------------------------- F6: Kalman tuned vs fixed
def fig6_kalman():
    vs = np.logspace(-2, 2, 200); k_phi = om.kalman_gain(1.0)
    r_phi = [om.mse_fixed_gain(k_phi, v * v, 1.0) / om.mse_fixed_gain(om.kalman_gain(v), v * v, 1.0) for v in vs]
    r_half = [om.mse_fixed_gain(0.5, v * v, 1.0) / om.mse_fixed_gain(om.kalman_gain(v), v * v, 1.0) for v in vs]
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    ax.plot(vs, r_phi, color=C1, label="fixed K = 1/φ (Ω = 1 as Fisher speed 1)"); ax.plot(vs, r_half, color=C2, label="fixed K = 1/2 (Ω = 1 as equal pull)")
    ax.axhline(1.0, color=C3, lw=1.5, ls="--"); ax.text(0.011, 1.45, "tuned Kalman gain K(v): ratio 1 (Bayes-optimal)", color=C3, fontsize=8)
    ax.axhline(1.05, color=INK2, lw=0.6, ls=":"); ax.text(30, 1.06, "5 %", color=INK2, fontsize=7)
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("v = √(q/r), the Fisher speed of the random walk"); ax.set_ylabel("steady-state MSE, fixed / tuned")
    ax.legend(loc="upper center", fontsize=8); ax.set_title("A fixed gain from Ω = 1 matches the tuned filter at one speed only", loc="left")
    for v in (0.1, 1.0, 10.0):
        print(f"[F6] v = {v:g}: ratio 1/phi {om.mse_fixed_gain(k_phi, v * v, 1.0) / om.mse_fixed_gain(om.kalman_gain(v), v * v, 1.0):.4f}, ratio 1/2 {om.mse_fixed_gain(0.5, v * v, 1.0) / om.mse_fixed_gain(om.kalman_gain(v), v * v, 1.0):.4f}")
    save(fig, "F06_kalman.png")


# ---------------------------------------------------------------- study data: EQ2 + EQ3
def load_studies():
    S = {}
    for study, names in (("EQ2", ("mfeat_fourier", "mfeat_pixel", "texture")), ("EQ3", ("fars", "krkopt", "led24", "led7", "mfeat_factors", "mfeat_morphological"))):
        for n in names:
            hdr, rows = records(ROOT / "runs" / study.lower() / f"results_{n}.jsonl")
            S[(study, n)] = rows
    return S


def sel(rows, method, mode, value=None, regime="std", smooth=0.9, cap=1e4, main=True):
    v = [r for r in rows if r["method"] == method and r["mode"] == mode and r["regime"] == regime and r["smooth"] == smooth and r["wcap"] == cap
         and (value is None or abs(r["value"] - value) < 1e-6)
         and (not main or (r.get("hidden", r.get("hid", 256)) == 256 and r.get("epochs", 3) == 3 and r.get("lr", 0.05) == 0.05 and r.get("bs", 10) == 10))]
    return sorted(v, key=lambda r: r["seed"])


def tuned(rows):
    ws = sorted(set(r["value"] for r in sel(rows, "ewc", "fixed")))
    means = {w: np.mean([r["acc"] for r in sel(rows, "ewc", "fixed", w)]) for w in ws}
    tw = max(means, key=means.get); tv = np.array([r["acc"] for r in sel(rows, "ewc", "fixed", tw)])
    step = max(1.0, 2 * tv.std(ddof=1) / math.sqrt(len(tv)))
    return means, tw, tv, step


def fig7_omega_profiles(S):
    keys = list(S.keys())
    fig, axes = plt.subplots(3, 3, figsize=(10, 8.5)); axes = axes.ravel()
    for ax, k in zip(axes, keys):
        rows = S[k]; means, tw, tv, step = tuned(rows)
        oms = sorted(set(r["value"] for r in sel(rows, "ewc", "eq")))
        m = [np.mean([r["acc"] for r in sel(rows, "ewc", "eq", o)]) for o in oms]
        for o in oms:
            for r in sel(rows, "ewc", "eq", o): ax.plot(o, r["acc"], ".", color=C1, alpha=0.35, ms=5)
        ax.plot(oms, m, "-o", color=C1, ms=5, label="rule, mean of 5 seeds")
        ax.axhspan(tv.mean() - step, tv.mean() + step, color=C2, alpha=0.12)
        ax.axhline(tv.mean(), color=C2, ls="--", lw=1.4, label=f"tuned λ = {tw:g} (± one step)")
        logticks(ax, oms); ax.tick_params(axis="x", labelsize=7)
        ax.set_title(f"{k[0]} {k[1]}", loc="left"); ax.set_xlabel("Ω"); ax.set_ylabel("final accuracy (%)")
        print(f"[F7] {k[0]} {k[1]}: tuned lambda {tw:g} mean {tv.mean():.4f} step {step:.4f}; rule per Omega " + " ".join(f"{o:g}:{mm:.4f}" for o, mm in zip(oms, m)))
    axes[0].legend(loc="lower right", fontsize=7)
    fig.suptitle("Accuracy of the rule against Ω on nine unseen carriers (EQ2: five-point grid; EQ3: nine-point grid); dashed = in-sample-tuned fixed λ, band = one resolvable step", x=0.01, ha="left", fontsize=10)
    fig.tight_layout(); save(fig, "F07_omega_profiles.png")


def fig8_lambda_grids(S):
    keys = list(S.keys())
    fig, axes = plt.subplots(3, 3, figsize=(10, 8.5)); axes = axes.ravel()
    for ax, k in zip(axes, keys):
        rows = S[k]; means, tw, tv, step = tuned(rows)
        ws = sorted(means); ax.plot(ws, [means[w] for w in ws], "-o", color=C1, ms=4, label="fixed λ grid, mean of 5 seeds")
        rule = sel(rows, "ewc", "eq", 1.0); wm = np.median([r["w_med"] for r in rule]); racc = np.mean([r["acc"] for r in rule])
        ax.axvline(tw, color=C2, ls="--", lw=1.2); ax.text(tw, ax.get_ylim()[1] * 0.98 if ax.get_ylim()[1] > 0 else 1, f"tuned {tw:g}", color=C2, fontsize=7, rotation=90, va="top", ha="right")
        ax.axvline(wm, color=C3, ls="-", lw=1.6); ax.text(wm, max(means.values()) * 0.5, f"rule's median w = {wm:.3g}", color=C3, fontsize=7, rotation=90, va="center", ha="right")
        ax.plot([wm], [racc], "s", color=C3, ms=7, label="rule at Ω = 1 (accuracy, at its median w)")
        ax.set_xscale("log"); ax.set_title(f"{k[0]} {k[1]}", loc="left"); ax.set_xlabel("penalty weight λ (fixed)"); ax.set_ylabel("final accuracy (%)")
        edge = [w for w in ws if means[w] < 0.5 * max(means.values()) and w > tw]
        print(f"[F8] {k[0]} {k[1]}: tuned {tw:g} ({tv.mean():.4f}); rule median w {wm:.4g} accuracy {racc:.4f}; first fixed lambda above tuned with mean under half the best: {edge[0] if edge else 'none'}")
    axes[0].legend(loc="lower left", fontsize=7)
    fig.suptitle("The fixed-λ grid collapses beyond a stability edge; the rule's derived weight sits at or beyond it without collapsing", x=0.01, ha="left", fontsize=10)
    fig.tight_layout(); save(fig, "F08_lambda_grids.png")


def fig9_sensitivity(S):
    keys = list(S.keys()); caps = (10.0, 100.0, 1e4); sms = (0.8, 0.9, 0.98)
    fig, axes = plt.subplots(3, 3, figsize=(9, 7.5)); axes = axes.ravel()
    for ax, k in zip(axes, keys):
        rows = S[k]; means, tw, tv, step = tuned(rows)
        M = np.array([[np.mean([r["acc"] for r in sel(rows, "ewc", "eq", 1.0, smooth=s, cap=c)]) - tv.mean() for s in sms] for c in caps])
        lim = max(4.0, np.abs(M).max())
        im = ax.imshow(M, cmap=matplotlib.colors.LinearSegmentedColormap.from_list("div", ["#d03b3b", "#f0efec", "#2a78d6"]), vmin=-lim, vmax=lim)
        for i in range(3):
            for j in range(3):
                ax.text(j, i, f"{M[i, j]:+.2f}", ha="center", va="center", fontsize=8, color=INK)
        ax.set_xticks(range(3)); ax.set_xticklabels([f"smooth {s}" for s in sms], fontsize=7); ax.set_yticks(range(3)); ax.set_yticklabels([f"cap {c:g}" for c in caps], fontsize=7)
        ax.set_title(f"{k[0]} {k[1]} (step {step:.2f})", loc="left"); ax.grid(False)
        print(f"[F9] {k[0]} {k[1]}: Omega=1 - tuned by cap x smooth " + "; ".join(f"cap{c:g}/sm{s}:{M[i, j]:+.2f}" for i, c in enumerate(caps) for j, s in enumerate(sms)))
    fig.suptitle("Sensitivity: rule at Ω = 1 minus tuned λ, per cap × smoothing cell (blue = rule ahead, red = behind)", x=0.01, ha="left", fontsize=10)
    fig.tight_layout(); save(fig, "F09_sensitivity.png")


def fig10_eq3_arms(S):
    names = ["fars", "krkopt", "led24", "led7", "mfeat_factors", "mfeat_morphological"]
    fig, ax = plt.subplots(figsize=(9, 3.8)); x = np.arange(len(names)); wdt = 0.26
    for off, (meth, mode, val, c, lab) in enumerate((("ewc", "eq", 1.0, C1, "rule at Ω = 1"), ("ewc", "bayes", 0.0, C2, "Bayes (Laplace 1/2) arm"), ("ewc", "reduction", None, C3, "reduction arm (fixed w = rule's median w)"))):
        d = []
        for n in names:
            rows = S[("EQ3", n)]; means, tw, tv, step = tuned(rows)
            d.append(np.mean([r["acc"] for r in sel(rows, meth, mode, val)]) - tv.mean())
        ax.bar(x + (off - 1) * wdt, d, wdt, color=c, label=lab)
        for xi, di in zip(x, d): ax.text(xi + (off - 1) * wdt, di + (0.6 if di >= 0 else -1.8), f"{di:+.1f}", ha="center", fontsize=7, color=INK)
        print(f"[F10] {lab}: minus tuned lambda per carrier " + ", ".join(f"{n}:{di:+.4f}" for n, di in zip(names, d)))
    ax.axhline(0, color=INK2, lw=0.8); ax.set_xticks(x); ax.set_xticklabels(names, fontsize=8); ax.set_ylabel("accuracy minus the tuned λ (points)")
    ax.legend(loc="lower left", fontsize=8); ax.set_title("EQ3: the rule, the Bayes weight and the rule's own constant, each against the in-sample-tuned λ", loc="left")
    save(fig, "F10_eq3_arms.png")


def fig11_eqx():
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.4))
    for ax, n in zip(axes, ("optdigits", "pendigits", "letter")):
        hdr, rows = records(ROOT / "runs" / "eqx" / f"{n}.jsonl")
        fx = sorted(set(r["value"] for r in rows if r["method"] == "fixed")); fm = [100 * np.mean([r["acc"] for r in rows if r["method"] == "fixed" and r["value"] == w]) for w in fx]
        ax.plot(fx, fm, "-o", color=C2, ms=4, label="fixed replay weight w")
        for metric, c, ls in (("fisher", C1, "-"), ("euclid", C3, "--")):
            oms = sorted(set(r["value"] for r in rows if r["method"] == "eq" and r.get("metric") == metric))
            if not oms: continue
            m = [100 * np.mean([r["acc"] for r in rows if r["method"] == "eq" and r.get("metric") == metric and r["value"] == o]) for o in oms]
            ax.plot(oms, m, ls, marker="s", color=c, ms=4, label=f"rule, Ω grid ({metric} norm)")
            print(f"[F11] {n} {metric}: rule per Omega " + " ".join(f"{o:g}:{mm:.4f}" for o, mm in zip(oms, m)))
        print(f"[F11] {n} fixed: " + " ".join(f"{w:g}:{mm:.4f}" for w, mm in zip(fx, fm)))
        logticks(ax, sorted(set(fx) | {0.5, 0.71, 1.0, 1.41, 2.0})); ax.set_title(f"EQX {n}", loc="left"); ax.set_xlabel("w (fixed) or Ω (rule)"); ax.set_ylabel("final accuracy (%)")
    axes[0].legend(loc="lower right", fontsize=7)
    fig.suptitle("EQX (replay, ER-sum): the rule at Ω = 1 is level with or behind the best fixed replay weight on 3/3 carriers; it reduces to a constant", x=0.01, ha="left", fontsize=10)
    fig.tight_layout(); save(fig, "F11_eqx_reduction.png")


def fig12_bayes_line():
    fig, ax = plt.subplots(figsize=(8, 2.6)); m_p, m_q = 0.0, 1.0
    for ratio, y in ((0.25, 0.8), (1.0, 0.5), (4.0, 0.2)):
        th_B = (100 * m_p + 100 * ratio * m_q) / (100 + 100 * ratio)
        ax.plot([m_p, m_q], [y, y], color=C3, lw=6, alpha=0.35, solid_capstyle="butt")
        ax.plot([th_B], [y], "D", color=C2, ms=9); ax.text(th_B, y + 0.07, f"Bayes θ_B = {th_B:.2f}", ha="center", fontsize=8, color=C2)
        ax.text(-0.02, y, f"n_past/n_present = {ratio:g}", ha="right", va="center", fontsize=8, color=INK)
        print(f"[F12] ratio {ratio:g}: theta_B {th_B:.4f}; Omega=1 fixed-point interval [{m_p:g}, {m_q:g}]")
    ax.plot([m_p], [-0.05], "o", color=C1, ms=8); ax.text(m_p, -0.2, "present mean m_p (Ω < 1 ends here)", ha="center", fontsize=8, color=C1)
    ax.plot([m_q], [-0.05], "o", color=C1, ms=8); ax.text(m_q, -0.2, "past mean m_q (Ω > 1 ends here)", ha="center", fontsize=8, color=C1)
    ax.text(0.5, 0.98, "green band: every point is a fixed point of the rule at Ω = 1 (it stays where it starts)", ha="center", fontsize=8.5, color=C3)
    ax.set_xlim(-0.55, 1.2); ax.set_ylim(-0.32, 1.08); ax.axis("off")
    ax.set_title("One-dimensional Bayes: the posterior mode is one point; the rule at Ω = 1 stops anywhere on the segment", loc="left", fontsize=10)
    save(fig, "F12_bayes_line.png")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("Continuous_Learning figures (deterministic; numbers drawn on the figures)")
    fig1_tug(); fig2_field(); fig3_trajectories(); fig4_plateau(); fig5_edge(); fig6_kalman()
    S = load_studies(); fig7_omega_profiles(S); fig8_lambda_grids(S); fig9_sensitivity(S); fig10_eq3_arms(S); fig11_eqx(); fig12_bayes_line()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

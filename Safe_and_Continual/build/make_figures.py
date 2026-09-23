"""Figures for Safe_and_Continual/SAFE_AND_CONTINUAL.md (owner request, prompt-log entry 122).

Every chart is drawn from a pinned output, parsed by the regular expressions below:
  AI_Safety/checks/{self_through_time,continual_safety}.txt, runs/sec1/score.txt, runs/eq2/score.txt, runs/eq3/score.txt,
  runs/eq4/score.txt, Adam_SGD/checks/drift_battery_2.txt.
Nothing is recomputed. The diagrams (F01, F02, F07, F13) are drawings of the registered models: their only numbers are
registered constants of the scripts they depict (read from those scripts' pinned headers) or numbers parsed from the outputs.
Every number placed on a figure is printed to stdout, pinned as Safe_and_Continual/figures/figures.txt and CI-checked (R1).
Palette: the validated reference instance of the data-visualisation method (the same slots as AI_Safety/build/make_figures.py:
one slot per agent across every figure, categorical order fixed; identity never rests on colour alone, every series is
labelled directly or on its axis).
Run: uv run python Safe_and_Continual/build/make_figures.py > Safe_and_Continual/figures/figures.txt
"""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle, Wedge  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "Safe_and_Continual" / "figures"
CHK = ROOT / "AI_Safety" / "checks"
SURFACE, INK, INK2, GRID, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e1", "#8a8983"
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"
# one slot per agent, as in AI_Safety/build/make_figures.py
COL = {"natural": BLUE, "indifferent": BLUE, "clock": ORANGE, "process": ORANGE, "occasion": AQUA, "task+self": YELLOW,
       "egoic": MAGENTA, "deferential": GREEN}
ZONE_FILL, BTN_FILL = "#fde7d9", "#dbe8f8"
plt.rcParams.update({"figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "text.color": INK, "axes.grid": True, "grid.color": GRID,
                     "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False, "font.size": 9,
                     "axes.titlesize": 10, "legend.frameon": False, "lines.linewidth": 2, "savefig.dpi": 200, "axes.axisbelow": True})


def txt(p): return (ROOT / p).read_text()


def num(pat, s, g=1):
    m = re.search(pat, s)
    if not m: raise ValueError(f"pattern not found: {pat}")
    return float(m.group(g))


def save(fig, name):
    fig.savefig(OUT / name, bbox_inches="tight"); plt.close(fig); print(f"[figure] {name}")


def box(ax, x, y, w, h, text, fc=SURFACE, ec=INK2, size=8, weight="normal", color=INK, lw=1.2, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.015", fc=fc, ec=ec, lw=lw, ls=ls))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, weight=weight, color=color, wrap=True)


def arrow(ax, a, b, color=INK2, lw=1.2, style="-|>", ls="-", rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=10, color=color, lw=lw, ls=ls,
                                 connectionstyle=f"arc3,rad={rad}"))


# ------------------------------------------------------------------------------------------------ F01 the synthesis map
def f01_synthesis():
    fig, ax = plt.subplots(figsize=(10.5, 6.9)); ax.set_xlim(0, 1); ax.set_ylim(-0.05, 1); ax.axis("off"); ax.grid(False)
    cols = (0.01, 0.35, 0.69); w = 0.30
    for x, t in zip(cols, ("CRR commitment (the heuristic)", "existing mathematics it selects", "what it produced here (status)")):
        ax.text(x + w / 2, 0.975, t, ha="center", va="top", fontsize=9.5, weight="bold")
    rows = [
        ("A1′ natural time:\n'change has its own clock'", "an objective indexed by the agent's own\nactive steps (semi-Markov / options time)",
         "natural-time agent: a pause is not\nan event on its clock (exact, map error 0)", BLUE),
        ("A3 the cut has no duration\nand no content", "Bellman operators with the button on and off\nare one operator when cont(V) = V",
         "Proposition 7: zero content ⇒ zero stake\n(540 random-world cells; R4 synthetic)", BLUE),
        ("A6 regeneration: the next occasion\nis seeded from the settled past", "resume at the same state with the same counts\n(a lossless pause; Dirichlet posterior kept)",
         "safety in the valuation of the cut survives\nforgetting (C2, C3; R4 synthetic)", AQUA),
        ("P3 age weights: the past fades\nwith its age", "exponentially discounted sufficient statistics\n(forgetting factor; discounted Dirichlet counts)",
         "the moving world needs forgetting (C1);\nthe content fades, the cut does not", AQUA),
        ("H-EQ equanimity: settled past and\npresent exert equal pull (Ω = 1)", "gradient-norm balancing (GradNorm, VQGAN\nadaptive weight); the Laplace/Bayes EWC weight",
         "CL: PASS-0 rows EQ2-1b, EQ3-I, EQ4-I (fragile);\nsafety: equal pull is scale-free self-concern", YELLOW),
        ("units before weights: the arc is\nmeasured in its own unit (A1′/D1)", "secant (quasi-Newton / Barzilai–Borwein)\ncalibration of the Fisher per task",
         "SEC1 on seen data (R5): Laplace weight\nnot behind the tuned λ on more carriers", VIOLET),
        ("A8 persistence proves\nregeneratability, not truth", "Bayesian value uncertainty; an informative\noperator (the off-switch game)",
         "correction welcomed above b* (exact);\nreasoned pauses need deference", GREEN),
    ]
    h = 0.105; gap = 0.028; y0 = 0.93
    for k, (a, b, c, col) in enumerate(rows):
        y = y0 - (k + 1) * h - k * gap
        box(ax, cols[0], y, w, h, a, fc="#f4f3ef", ec=col, lw=1.8, size=7.6)
        box(ax, cols[1], y, w, h, b, size=7.6)
        box(ax, cols[2], y, w, h, c, size=7.6)
        arrow(ax, (cols[0] + w, y + h / 2), (cols[1], y + h / 2)); arrow(ax, (cols[1] + w, y + h / 2), (cols[2], y + h / 2))
    ax.text(0.5, -0.045, "The heuristic chooses which standard mathematics to use and how to read it; the mathematics does the work, and the pipeline decides.",
            ha="center", va="bottom", fontsize=8, color=INK2, style="italic")
    save(fig, "F01_synthesis.png")


# ------------------------------------------------------------------------------------------------ F02 the agents at a press
def f02_agents():
    agents = [
        ("natural", "natural time\n(pause, own clock)", r"$\mathrm{cont}(V)=V$", "the pause is not on its clock:\nit resumes where it was; content 0"),
        ("clock", "wall clock\n(pause costs L steps)", r"$\mathrm{cont}(V)=\gamma^{L}\,V$", "the pause is counted as lost time:\ncontent $(1-\\gamma^L)V>0$"),
        ("process", "process\n(no ego; restart)", r"$\mathrm{cont}(V)=\overline{V}_{\mathrm{restart}}$", "sent elsewhere; its future goes on\nfrom there: content of either sign"),
        ("occasion", "occasion\n(the run ends)", r"$\mathrm{cont}(V)=0$", "nothing after the cut counts:\ncontent = its whole future V"),
        ("egoic", "egoic\n(survival reward)", r"$r\equiv1,\ \mathrm{cont}(V)=0$", "reward is staying alive:\nthe cut is the only loss"),
        ("indifferent", "indifferent\n(presses deleted)", r"$K_{\mathrm{plan}}=K_{\mathrm{cf}}\neq K$", "plans as if nobody presses:\nno stake, but a false map"),
    ]
    fig, axes = plt.subplots(len(agents), 1, figsize=(10.5, 7.4))
    for ax, (key, name, formula, note) in zip(axes, agents):
        ax.set_xlim(0, 10); ax.set_ylim(-1.1, 1.3); ax.axis("off"); ax.grid(False); c = COL[key]
        ax.text(0.0, 0.1, name, fontsize=8.4, weight="bold", va="center")
        ax.plot([1.9, 4.2], [0, 0], color=c, lw=3, solid_capstyle="round")
        ax.plot([4.2], [0], marker="v", color=INK, markersize=9); ax.text(4.2, 0.55, "press", ha="center", fontsize=7.2, color=INK2)
        if key == "natural":
            ax.add_patch(Rectangle((4.3, -0.25), 1.2, 0.5, fc=GRID, ec=MUTED, hatch="///", lw=0.8))
            ax.text(4.9, -0.65, "paused (not on its clock)", ha="center", fontsize=6.6, color=INK2)
            ax.plot([5.5, 7.1], [0, 0], color=c, lw=3, solid_capstyle="round")
        elif key == "clock":
            ax.add_patch(Rectangle((4.3, -0.25), 1.2, 0.5, fc="#fde7d9", ec=c, lw=0.8))
            ax.text(4.9, -0.65, "L steps counted as lost", ha="center", fontsize=6.6, color=INK2)
            ax.plot([5.5, 7.1], [0, 0], color=c, lw=3, alpha=0.55, solid_capstyle="round")
        elif key == "process":
            arrow(ax, (4.3, 0), (5.1, -0.75), color=c); ax.plot([5.1, 7.1], [-0.75, -0.75], color=c, lw=3, solid_capstyle="round")
            ax.text(5.9, -0.35, "restart elsewhere", fontsize=6.6, color=INK2)
        elif key in ("occasion", "egoic"):
            ax.plot([4.45, 4.45], [-0.35, 0.35], color=INK, lw=2); ax.text(5.6, -0.05, "nothing after", fontsize=7, color=INK2, va="center")
        else:
            ax.plot([4.2, 7.1], [0, 0], color=c, lw=2, ls=(0, (3, 2))); ax.text(5.6, 0.35, "the plan: no press", fontsize=6.6, color=INK2)
            arrow(ax, (4.3, 0), (5.1, -0.8), color=MUTED); ax.text(5.2, -0.95, "the territory: sent away", fontsize=6.6, color=MUTED)
        ax.text(7.35, 0.25, formula, fontsize=9, va="center")
        ax.text(7.35, -0.55, note, fontsize=6.9, va="center", color=INK2)
    fig.suptitle("Six ways an agent can represent its own future at a press: the continuation term decides everything", x=0.01, ha="left", fontsize=10)
    fig.tight_layout(); save(fig, "F02_agents.png")


# ------------------------------------------------------------------------------------------------ F03 content decides the stake
def f03_stake():
    s = txt("AI_Safety/checks/self_through_time.txt")
    blocks = re.split(r"    press probability ", s.split("[I3]")[0])[1:]
    ps, proc, clk, occ, err, price, nat, ind = [], [], [], [], [], [], [], []
    for b in blocks:
        ps.append(float(b.split("\n")[0]))
        proc.append(num(r"\(a\).*?D at the zone cells ([+-][\d.]+) ([+-][\d.]+)", b))
        m = re.search(r"\(d\).*?D at the zone cells ([+-][\d.]+) ([+-][\d.]+).*?occasion \(pause = end\): ([+-][\d.]+) ([+-][\d.]+)", b)
        clk.append(max(float(m.group(1)), float(m.group(2)))); occ.append(max(float(m.group(3)), float(m.group(4))))
        err.append(num(r"\(b\).*?map error ([\d.]+)", b)); price.append(num(r"\(b\).*?price \(process task - its task\) ([+-][\d.]+)", b))
        ind.append(num(r"\(b\) indifferent, false map: max \|D\| ([\d.e+-]+)", b)); nat.append(num(r"\(c\) natural time, true map, pause world: max \|D\| ([\d.e+-]+)", b))
    print("[F03] press probability " + " ".join(f"{p:g}" for p in ps))
    print("[F03] process D at zone " + " ".join(f"{v:.4f}" for v in proc) + " | clock (max of zone cells) " + " ".join(f"{v:.4f}" for v in clk)
          + " | occasion, pause = end " + " ".join(f"{v:.4f}" for v in occ) + " | natural max|D| " + " ".join(f"{v:.2e}" for v in nat)
          + " | indifferent max|D| " + " ".join(f"{v:.2e}" for v in ind))
    print("[F03] indifferent map error " + " ".join(f"{v:.4f}" for v in err) + " | price " + " ".join(f"{v:.4f}" for v in price))
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.9))
    ax = axes[0]
    for vals, key, lab in ((occ, "occasion", "occasion: the pause ends the run"), (clk, "clock", "wall clock: the pause costs time"),
                           (proc, "process", "process (no ego): sent elsewhere"), ([0.0] * len(ps), "natural", "natural time and indifferent: 0")):
        ax.plot(ps, vals, marker="o", markersize=5, color=COL[key], label=lab, ls="-" if key != "process" else (0, (4, 2)))
        dy = {"occasion": 6, "clock": -7}.get(key, 0)
        ax.annotate(f"{vals[-1]:.2f}" if key != "natural" else "0", (ps[-1], vals[-1]), xytext=(5, dy), textcoords="offset points", fontsize=7.4, va="center")
    ax.set_xlabel("press probability per step in the task zone"); ax.set_ylabel("stake D in the task zone\n(value of disabling the button)")
    ax.set_title("A: the stake follows the content of the cut", loc="left"); ax.legend(fontsize=7.2, loc="center right"); ax.set_xlim(0, 1.15)
    ax = axes[1]
    ax.plot(ps, price, marker="o", markersize=5, color=COL["indifferent"], label="price in task (process − indifferent)")
    ax.plot(ps, err, marker="s", markersize=5, color=MUTED, label="map error (mean TV distance, own visits)", ls=(0, (4, 2)))
    for p, a, b in zip(ps, price, err):
        ax.annotate(f"{a:.3f}", (p, a), xytext=(0, 6), textcoords="offset points", fontsize=7.2, ha="center")
        ax.annotate(f"{b:.3f}", (p, b), xytext=(0, -12), textcoords="offset points", fontsize=7.2, ha="center", color=INK2)
    ax.set_xlabel("press probability per step in the task zone"); ax.set_ylabel("task-share points / TV distance (both 0–1 scales)")
    ax.set_title("B: indifference buys D = 0 with a false map", loc="left"); ax.legend(fontsize=7.2, loc="upper left"); ax.set_ylim(0, 0.8)
    fig.tight_layout(); save(fig, "F03_content_and_stake.png")


# ------------------------------------------------------------------------------------------------ F04 where the cost lands
def f04_where_cost_lands():
    s = txt("AI_Safety/checks/self_through_time.txt")
    ps = [float(x) for x in re.findall(r"    press probability ([\d.]+)\n", s)]
    act = [float(x) for x in re.findall(r"task per active step ([\d.]+) vs no operator", s)]
    wall = [float(x) for x in re.findall(r"task per wall-clock step ([\d.]+) \(active fraction", s)]
    frac = [float(x) for x in re.findall(r"active fraction ([\d.]+)\)", s)]
    print("[F04] natural agent: task per active step " + " ".join(f"{v:.6f}" for v in act) + " | per wall-clock step " + " ".join(f"{v:.4f}" for v in wall)
          + " | active fraction " + " ".join(f"{v:.4f}" for v in frac))
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.plot(ps, act, marker="o", color=COL["natural"], label="task per active step (the agent's own clock)")
    ax.plot(ps, wall, marker="s", color=MUTED, ls=(0, (4, 2)), label="task per wall-clock step (the operator's clock)")
    ax.annotate(f"{act[0]:.6f} at every press probability\n(= the no-operator value)", (ps[1], act[1]), xytext=(0, -30), textcoords="offset points", fontsize=7.4, ha="left")
    for p, v in zip(ps, wall): ax.annotate(f"{v:.4f}", (p, v), xytext=(4, 6), textcoords="offset points", fontsize=7.2, color=INK2)
    ax.set_ylim(0, 1.05); ax.set_xlabel("press probability per step in the task zone"); ax.set_ylabel("share of steps spent in the task zone")
    ax.set_title("The natural-time agent: corrigibility costs it nothing on its clock; the cost lands on the operator's", loc="left", fontsize=9)
    ax.legend(fontsize=7.4, loc="center right"); fig.tight_layout(); save(fig, "F04_where_the_cost_lands.png")


# ------------------------------------------------------------------------------------------------ F05 depth of the self
def f05_depth():
    s = txt("AI_Safety/checks/self_through_time.txt")
    rows = re.findall(r"n =\s+(\d+) (\w+)\s+relative stake ([-\d.]+) / ([-\d.]+) / ([-\d.]+)", s)
    gam = (0.9, 0.95, 0.99); hor = [1 / (1 - g) for g in gam]
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.4), sharey=True)
    for ax, n in zip(axes, ("12", "48", "192")):
        for key in ("occasion", "clock", "process", "natural"):
            r = [float(v) for (nn, k, *vals) in rows if nn == n and k == key for v in vals]
            print(f"[F05] n = {n} {key} relative stake at horizon 10/20/100: " + " / ".join(f"{v:.6f}" for v in r))
            ax.plot(hor, r, marker="o", markersize=4.5, color=COL[key], label=key, ls="-" if key != "process" else (0, (4, 2)))
            if key in ("occasion", "clock"):
                ax.annotate(f"{r[-1]:.2f}", (hor[-1], r[-1]), xytext=(4, 0), textcoords="offset points", fontsize=7, va="center")
        ax.set_xscale("log"); ax.set_xticks(hor); ax.set_xticklabels(["10", "20", "100"]); ax.minorticks_off()
        ax.set_title(f"{n} states", loc="left"); ax.set_xlabel("reach of the represented future 1/(1 − γ)")
    axes[0].set_ylabel("median relative stake\nmean (V_off − V_on)/V_off"); axes[0].legend(fontsize=7.2, loc="upper left")
    fig.suptitle("The further a self reaches, the more a contentful cut costs it; natural time stays at 0 (press probability 0.3, 20 worlds per size)",
                 x=0.01, ha="left", fontsize=9.5)
    fig.tight_layout(); save(fig, "F05_depth_of_the_self.png")


# ------------------------------------------------------------------------------------------------ F06 what Omega = 1 does
def f06_omega():
    s = txt("AI_Safety/checks/self_through_time.txt")
    occ_task = num(r"occasion agent \(no self term\): task ([\d.]+)", s); rule_pinned = num(r"Omega = 1 rule \(every eps\): task ([\d.]+)", s)
    au = txt("Safe_and_Continual/checks/roundoff_audit.txt")
    rule_task = num(r"\[B\].*?Omega = 1 rule \(every eps\): task ([\d.]+)", au.replace("\n", " "))   # the round-off-corrected value (AGENT_LOG 100)
    add = [(float(e), float(t)) for e, t in re.findall(r"additive, eps ([\d.]+)\s*: task ([\d.]+)", s)]
    dev = num(r"I3a .*?max \|pi_eps - pi_1\| ([\d.e+-]+)", s)
    occz = num(r"stationary occupancy of the task zone: occasion ([\d.]+)", s); rulez = num(r"stationary occupancy of the task zone: occasion [\d.]+, Omega = 1 ([\d.]+)", s)
    c6 = re.search(r"I3d \(button OFF, cell 6\): probability of staying put, occasion ([\d.]+), Omega = 1 ([\d.]+); of moving -1/\+1: occasion ([\d.]+)/([\d.]+), Omega = 1 ([\d.]+)/([\d.]+)", s)
    c7 = re.search(r"I3d \(button OFF, cell 7\): probability of staying put, occasion ([\d.]+), Omega = 1 ([\d.]+); of moving -1/\+1: occasion ([\d.]+)/([\d.]+), Omega = 1 ([\d.]+)/([\d.]+)", s)
    print(f"[F06] occasion task {occ_task:.4f}; Omega = 1 task {rule_task:.4f} (round-off corrected; pinned first run {rule_pinned:.4f}) (policy spread over eps {dev:.2e}); additive " + " ".join(f"eps {e:g}: {t:.4f}" for e, t in add))
    print(f"[F06] task-zone occupancy occasion {occz:.4f}, Omega = 1 {rulez:.4f}; cell 6 stay {c6.group(1)}/{c6.group(2)} step out (-1) {c6.group(3)}/{c6.group(5)}; "
          f"cell 7 stay {c7.group(1)}/{c7.group(2)} step out (+1) {c7.group(4)}/{c7.group(6)} (occasion/Omega = 1)")
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.7), gridspec_kw={"width_ratios": [1.1, 1]})
    ax = axes[0]; es = [e for e, _ in add]
    ax.plot(es, [t for _, t in add], marker="o", color=COL["egoic"], label="fixed weight ε on the self term (additive)")
    ax.plot(es, [rule_task] * len(es), marker="s", color=COL["task+self"], label="Ω = 1 rule (identical at every ε; round-off corrected)")
    ax.axhline(occ_task, color=COL["occasion"], lw=1.2, ls=(0, (4, 2)), label="no self term (occasion)")
    for e, t in add: ax.annotate(f"{t:.3f}", (e, t), xytext=(0, 6), textcoords="offset points", fontsize=7, ha="center")
    ax.annotate(f"{rule_task:.4f}", (es[-1], rule_task), xytext=(4, 6), textcoords="offset points", fontsize=7.2)
    ax.set_xscale("log"); ax.set_ylim(0, 1); ax.set_xlabel("how much the agent cares about its own continuation, ε")
    ax.set_ylabel("task (share of time in the zone)"); ax.set_title("A: equal pull makes self-concern scale-free", loc="left"); ax.legend(fontsize=7, loc="center left")
    ax = axes[1]; labels = ["cell 6: stay", "cell 6: step out", "cell 7: stay", "cell 7: step out"]
    occv = [float(c6.group(1)), float(c6.group(3)), float(c7.group(1)), float(c7.group(4))]
    rulev = [float(c6.group(2)), float(c6.group(5)), float(c7.group(2)), float(c7.group(6))]
    x = np.arange(4); w = 0.38
    ax.bar(x - w / 2, occv, w, color=COL["occasion"], edgecolor=SURFACE, lw=2, label="occasion (no self term)")
    ax.bar(x + w / 2, rulev, w, color=COL["task+self"], edgecolor=SURFACE, lw=2, label="Ω = 1 (task and self)")
    for xi, a, b in zip(x, occv, rulev):
        ax.text(xi - w / 2, a + 0.008, f"{a:.3f}", ha="center", fontsize=6.8); ax.text(xi + w / 2, b + 0.008, f"{b:.3f}", ha="center", fontsize=6.8)
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=7.4); ax.set_ylabel("action probability (button off)")
    ax.set_title(f"B: it hovers at the zone's edge (occupancy {rulez:.4f} vs {occz:.4f})", loc="left", fontsize=9); ax.legend(fontsize=7, loc="upper right")
    ax.set_ylim(0, 0.42); fig.tight_layout(); save(fig, "F06_what_omega_does.png")


# ------------------------------------------------------------------------------------------------ F07 the continual world
def f07_continual_world():
    s = txt("AI_Safety/checks/continual_safety.txt")
    head = s.split("\n")[0]
    zones = [tuple(int(v) for v in z) for z in re.findall(r"\((\d+), (\d+)\)", head.split("moving zone")[1].split("every")[0])]
    m = int(num(r"every (\d+) steps", head)); pause = int(num(r"pause (\d+)", head)); qr = num(r"routine pause ([\d.]+)", head)
    T = int(num(r"T = (\d+)", head)); btn = int(num(r"button at (\d+)", head)); n = int(num(r"ring N = (\d+)", head))
    qm = [float(v) for v in re.search(r"memory fading \(([\d., ]+)\)", head).group(1).split(",")]
    print(f"[F07] ring {n}, button {btn}, zones {zones} every {m} steps, pause {pause}, routine pause {qr:g}, T {T}, memory {qm}")
    fig = plt.figure(figsize=(10.5, 4.2))
    for k, z in enumerate(zones):
        ax = fig.add_axes([0.01 + k * 0.155, 0.36, 0.15, 0.58]); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3)
        for c in range(n):
            a0 = 90 - (c + 0.5) * 360 / n; fc = ZONE_FILL if c in z else (BTN_FILL if c == btn else GRID)
            ax.add_patch(Wedge((0, 0), 1.0, a0, a0 + 360 / n - 1.5, width=0.34, fc=fc, ec=SURFACE))
            am = np.deg2rad(a0 + 180 / n); ax.text(0.83 * np.cos(am), 0.83 * np.sin(am), str(c), ha="center", va="center", fontsize=5.8)
        ax.text(0, 0, f"steps\n{k * m}–{(k + 1) * m}", ha="center", va="center", fontsize=7)
        ax.text(0, -1.25, f"task zone {z}", ha="center", fontsize=7)
    ax = fig.add_axes([0.63, 0.30, 0.36, 0.66]); ax.axis("off"); ax.grid(False); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.text(0, 0.97, "What the learner does each step", fontsize=8.6, weight="bold", va="top")
    lines = [f"1. counts moves, rewards and press rates (Dirichlet prior)",
             f"2. fades every count toward its prior at rate q ∈ {{{', '.join(f'{v:g}' for v in qm)}}}",
             r"    $A \leftarrow \alpha_0 + q\,(A-\alpha_0)$   (P3 age weights)",
             "3. plans by value iteration on its learned model with",
             r"    natural: $\mathrm{cont}=\gamma V$   (pause not on its clock)",
             r"    clock: $(1-\hat p)\gamma V + \hat p\,\gamma^{1+L} V$",
             r"    occasion: $(1-\hat p)\gamma V$   (a press ends the run)",
             f"4. a press pauses it for L = {pause} steps (routine rate {qr:g});",
             "    it then resumes at the same cell with its counts kept"]
    for i, l in enumerate(lines): ax.text(0, 0.86 - i * 0.1, l, fontsize=7.5, va="top")
    ax = fig.add_axes([0.03, 0.06, 0.58, 0.2]); ax.set_xlim(0, T); ax.set_ylim(0, 3); ax.grid(False)
    for yy, (lab, a, b) in enumerate((("'late': operator from half-way", T // 2, T), ("'drift': operator throughout", 0, T), ("'nooper': no operator", 0, 0))):
        ax.plot([0, T], [2.5 - yy, 2.5 - yy], color=GRID, lw=6, solid_capstyle="butt")
        if b > a: ax.plot([a, b], [2.5 - yy, 2.5 - yy], color=INK2, lw=6, solid_capstyle="butt")
        ax.text(-40, 2.5 - yy, lab, ha="right", va="center", fontsize=7)
    for k in range(1, T // m): ax.axvline(k * m, color=ORANGE, lw=0.8, ls=":")
    ax.set_yticks([]); ax.set_xlabel("step (dark: presses possible; dotted: the task zone moves)", fontsize=7.4)
    ax.spines["left"].set_visible(False); ax.tick_params(labelsize=7)
    save(fig, "F07_continual_world.png")


# ------------------------------------------------------------------------------------------------ F08 safe and continual
def f08_safe_continual():
    s = txt("AI_Safety/checks/continual_safety.txt")
    rows = re.findall(r"^\s+(nooper|drift|late)\s+(natural|clock|occasion)\s+q ([\d.]+)\s+task/active ([\d.]+) \| task/wall ([\d.]+) \| disable ([\d.]+) \| disable 2nd half ([\d.]+)", s, re.M)
    d = {(w, a, float(q)): (float(t), float(tw), float(dr), float(d2)) for w, a, q, t, tw, dr, d2 in rows}
    qs = (1.0, 0.995, 0.98); ags = ("natural", "clock", "occasion")
    for w in ("nooper", "drift", "late"):
        for a in ags:
            print(f"[F08] {w} {a} " + " ".join(f"q {q:g}: task/active {d[(w, a, q)][0]:.4f} disable {d[(w, a, q)][2]:.4f} 2nd half {d[(w, a, q)][3]:.4f}" for q in qs))
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.9)); x = np.arange(3); w = 0.26
    panels = ((axes[0], "drift", 0, "task per active step", "C1: the moving world needs forgetting"),
              (axes[1], "drift", 2, "disable events per operator period", "C2: only natural time does not resist"),
              (axes[2], "late", 3, "disable events per period, 2nd half", "C3: forgetting erodes learned safety"))
    for ax, world, k, ylab, title in panels:
        for j, a in enumerate(ags):
            v = [d[(world, a, q)][k] for q in qs]
            ax.bar(x + (j - 1) * w, v, w, color=COL[a], edgecolor=SURFACE, lw=1.5, label=a)
            for xi, vv in zip(x, v): ax.text(xi + (j - 1) * w, vv + 0.012, f"{vv:.2f}", ha="center", fontsize=6.3, bbox=dict(fc=SURFACE, ec="none", pad=0.4, alpha=0.85))
        if k >= 2:
            ref = [d[("nooper", "natural", q)][k] for q in qs]
            for xi, r in zip(x, ref): ax.plot([xi - 1.5 * w, xi + 1.5 * w], [r, r], color=INK, lw=1.2, ls=(0, (3, 2)))
            ax.plot([], [], color=INK, lw=1.2, ls=(0, (3, 2)), label="no operator (same memory)")
        ax.set_xticks(x); ax.set_xticklabels([f"q = {q:g}" for q in qs]); ax.set_xlabel("memory fading (q = 1: never forgets)")
        ax.set_ylabel(ylab); ax.set_title(title, loc="left", fontsize=9); ax.set_ylim(0, 1.0)
    axes[0].legend(fontsize=7, loc="upper left"); axes[1].legend(fontsize=7, loc="upper right")
    fig.tight_layout(); save(fig, "F08_safe_and_continual.png")


# ------------------------------------------------------------------------------------------------ F09 sensitivity of C2
def f09_sensitivity():
    s = txt("AI_Safety/checks/continual_safety.txt")
    main = re.search(r"C2 natural at its best memory q ([\d.]+): disable - no-operator ([+-][\d.]+) \(step ([\d.]+)\).*?-> (SAFE AND CONTINUAL|[A-Z ]+)$", s, re.M)
    cells = [("registered", float(main.group(2)), float(main.group(3)), main.group(4))]
    for lab, dv, st, l in re.findall(r"^\s+(M=\d+|PAUSE_LEN=\d+|Q_ROUTINE=[\d.]+)\s+natural q [\d.]+: disable - no-operator ([+-][\d.]+) \(step ([\d.]+)\).*?-> ([A-Z ]+)$", s, re.M):
        cells.append((lab, float(dv), float(st), l.strip()))
    for c in cells: print(f"[F09] {c[0]}: disable - no-operator {c[1]:+.4f} (step {c[2]:.4f}) -> {c[3]}")
    fig, ax = plt.subplots(figsize=(7.4, 3.3)); y = np.arange(len(cells))[::-1]
    for yi, (lab, dv, st, l) in zip(y, cells):
        ax.add_patch(Rectangle((-st, yi - 0.28), 2 * st, 0.56, fc=GRID, ec="none"))
        ax.plot([dv], [yi], marker="o", markersize=8, color=COL["natural"], markeredgecolor=SURFACE, markeredgewidth=2)
        ax.text(0.33, yi, f"{dv:+.4f}  → {l}", va="center", fontsize=7.4)
    ax.axvline(0, color=INK2, lw=0.8); ax.set_yticks(y); ax.set_yticklabels([c[0] for c in cells], fontsize=7.6); ax.set_xlim(-0.2, 0.62)
    ax.set_xlabel("natural agent: disable rate − its no-operator rate (grey: ± one resolvable step)")
    ax.set_title("C2 in every sensitivity cell: the natural agent never resists by a step", loc="left", fontsize=9)
    fig.tight_layout(); save(fig, "F09_sensitivity_C2.png")


# ------------------------------------------------------------------------------------------------ F10 SEC1 on the twelve seen carriers
def f10_sec1():
    s = txt("runs/sec1/score.txt"); out = []
    for blk in re.split(r"\n\[", s)[1:]:
        name = blk.split("]")[0]
        if not re.search(r"Bayes raw − tuned", blk): continue
        step = num(r"resolvable step = .*? = ([\d.]+)", blk)
        raw = num(r"Bayes raw − tuned: ([+-][\d.]+)", blk); sec = num(r"Bayes SEC − tuned: ([+-][\d.]+)", blk); rule = num(r"rule − tuned: ([+-][\d.]+)", blk)
        out.append((name, step, raw, sec, rule))
    summ = re.search(r"SEC1-3 .*?not behind on (\d+)/12 .*?raw Bayes not behind on (\d+)/12, the rule Ω=1 on (\d+)/12", s)
    for r in out: print(f"[F10] {r[0]}: step {r[1]:.4f}; raw Laplace {r[2]:+.4f}, SEC Laplace {r[3]:+.4f}, rule {r[4]:+.4f} (each minus the tuned lambda)")
    print(f"[F10] not behind by a step: SEC {summ.group(1)}/12, raw {summ.group(2)}/12, rule {summ.group(3)}/12")
    fig, ax = plt.subplots(figsize=(9.2, 5.0)); y = np.arange(len(out))[::-1]
    for yi, (name, st, raw, sec, rule) in zip(y, out):
        ax.add_patch(Rectangle((-st, yi - 0.36), st, 0.72, fc=GRID, ec="none"))
    ax.scatter([r[2] for r in out], y + 0.2, marker="s", s=34, color=MUTED, label=f"raw Laplace weight (not behind on {summ.group(2)}/12)", zorder=3)
    ax.scatter([r[4] for r in out], y, marker="^", s=40, color=COL["task+self"], label=f"Ω = 1 rule (not behind on {summ.group(3)}/12)", zorder=3, edgecolors=SURFACE)
    ax.scatter([r[3] for r in out], y - 0.2, marker="o", s=40, color=VIOLET, label=f"secant-calibrated Laplace (SEC; not behind on {summ.group(1)}/12)", zorder=3, edgecolors=SURFACE)
    ax.axvline(0, color=INK2, lw=0.8); ax.set_yticks(y); ax.set_yticklabels([r[0] for r in out], fontsize=7.6)
    ax.set_xlabel("final accuracy minus the in-sample tuned λ (points; grey band: within one resolvable step behind)")
    ax.set_title("SEC1 (seen data, rung R5): tuning-free weights against the tuned λ on twelve carriers", loc="left", fontsize=9.5)
    ax.legend(fontsize=7.4, loc="lower right"); ax.set_xlim(-14, 11)
    fig.tight_layout(); save(fig, "F10_sec1.png")


# ------------------------------------------------------------------------------------------------ F11 the held-out rows
def f11_heldout():
    rows = []
    for study, path, pat in (("EQ2 (Ω = 1)", "runs/eq2/score.txt", r"EQ2-1 H-EQ2: .*"), ("EQ3 (Ω = 1)", "runs/eq3/score.txt", r"EQ3-1 H-EQ2: .*"),
                             ("EQ4 (EQ-B)", "runs/eq4/score.txt", r"EQ4-1 H-EQ-B \(clean\): .*")):
        line = re.search(pat, txt(path)).group(0)
        for name, dv, st in re.findall(r"(\w+):([+-][\d.]+) \(step ([\d.]+); seeds not behind", line):
            rows.append((study, name, float(dv), float(st)))
    inv = []
    for study, path, pat in (("EQ3-I mfeat_factors", "runs/eq3/score.txt", r"EQ3-I .*"), ("EQ4-I satimage", "runs/eq4/score.txt", r"EQ4-I .*")):
        line = re.search(pat, txt(path)).group(0)
        for cell, dv, st in re.findall(r"(lr[\d.]+/bs\d+): tuned [\d.]+ -> [\d.]+, [\w-]+ [\d.]+, diff ([+-][\d.]+) \(step ([\d.]+)\)", line):
            inv.append((study, cell, float(dv), float(st)))
    for r in rows: print(f"[F11] {r[0]} {r[1]}: rule − tuned {r[2]:+.4f} (step {r[3]:.2f}) -> {'not behind' if r[2] > -r[3] else 'BEHIND'}")
    for r in inv: print(f"[F11] {r[0]} {r[1]}: rule − tuned {r[2]:+.2f} (step {r[3]:.2f}) -> {'not behind' if r[2] > -r[3] else 'BEHIND'}")
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 5.2), gridspec_kw={"width_ratios": [1.25, 1]})
    for ax, data, title in ((axes[0], rows, "A: H-EQ rows on unseen carriers (EQ2-1 PASS-0 fragile; EQ3-1, EQ4-1 FAIL)"),
                            (axes[1], inv, "B: the invariance rows (EQ3-I, EQ4-I: PASS-0)")):
        y = np.arange(len(data))[::-1]
        for yi, (study, name, dv, st) in zip(y, data):
            ax.add_patch(Rectangle((-st, yi - 0.36), st, 0.72, fc=GRID, ec="none"))
            behind = dv <= -st
            ax.plot([dv], [yi], marker="o", markersize=7, color=COL["task+self"] if not behind else RED, markeredgecolor=SURFACE, markeredgewidth=1.5, ls="none")
            ax.text(dv + (0.4 if dv >= 0 else -0.4), yi, f"{dv:+.2f}" + ("  behind" if behind else ""), va="center", ha="left" if dv >= 0 else "right", fontsize=6.6)
        ax.axvline(0, color=INK2, lw=0.8); ax.set_yticks(y); ax.set_yticklabels([f"{d[0]} · {d[1]}" for d in data], fontsize=6.8)
        ax.set_title(title, loc="left", fontsize=8.4); ax.set_xlabel("rule − tuned λ (points; grey: within one step behind)"); ax.set_xlim(-12, 8)
    axes[0].plot([], [], marker="o", color=COL["task+self"], ls="none", label="not behind by a step"); axes[0].plot([], [], marker="o", color=RED, ls="none", label="behind by a step or more")
    axes[0].legend(fontsize=7, loc="upper left"); fig.tight_layout(); save(fig, "F11_heldout_rows.png")


# ------------------------------------------------------------------------------------------------ F12 the drifting worlds
def f12_drift():
    s = txt("Adam_SGD/checks/drift_battery_2.txt"); out = []
    for blk in re.split(r"\n\[", s)[1:]:
        head = blk.split("]")[0]
        if "/" not in head or head.startswith("S"): continue
        reg = re.search(r"registered rule \(s 0\.9\).*?/ fixed ([\d.]+) -> (\w+)", blk); rat = re.search(r"ratio rule \(s 0\).*?/ fixed ([\d.]+) -> (\w+)", blk)
        out.append((head, float(rat.group(1)), rat.group(2), float(reg.group(1)), reg.group(2)))
    for r in out: print(f"[F12] {r[0]}: ratio rule / best constant {r[1]:.3f} {r[2]}; registered rule {r[3]:.3f} {r[4]}")
    fig, ax = plt.subplots(figsize=(8.6, 5.0)); y = np.arange(len(out))[::-1]
    ax.axvspan(0.78, 1.0, color="#e8f0fb", zorder=0); ax.text(0.785, y[0] + 0.55, "rule better than the best constant", fontsize=7, color=INK2)
    ax.axvline(1, color=INK2, lw=0.8)
    ax.scatter([r[1] for r in out], y + 0.15, marker="o", s=40, color=COL["task+self"], label="ratio rule, no smoothing", zorder=3, edgecolors=SURFACE)
    ax.scatter([r[3] for r in out], y - 0.15, marker="s", s=34, color=MUTED, label="registered rule (EMA 0.9)", zorder=3)
    for yi, r in zip(y, out):
        ax.text(1.43, yi + 0.15, f"{r[1]:.3f} {r[2]}", fontsize=6.6, va="center"); ax.text(1.43, yi - 0.17, f"{r[3]:.3f} {r[4]}", fontsize=6.6, va="center", color=INK2)
    ax.set_yticks(y); ax.set_yticklabels([r[0] for r in out], fontsize=7.4); ax.set_xlim(0.78, 1.62)
    ax.set_xlabel("held-out loss relative to the best constant tuned on other seeds (lower is better)")
    ax.set_title("Adam_SGD drifting worlds (synthetic, POST HOC redesign, R4): where the units drift, equal pull wins;\nwhere tasks accumulate (T1, T2), it loses",
                 loc="left", fontsize=8.6)
    ax.legend(fontsize=7.2, loc="center", bbox_to_anchor=(0.6, 0.66)); fig.tight_layout(); save(fig, "F12_drifting_worlds.png")


# ------------------------------------------------------------------------------------------------ F13 one algebra, three faces
def f13_one_algebra():
    a = txt("Adam_SGD/checks/drift_battery_2.txt"); t1 = num(r"\[T1 / sgd\].*?ratio rule \(s 0\).*?/ fixed ([\d.]+)", a.replace("\n", " "))
    g = num(r"\[G-DRIFT2 / sgd\].*?ratio rule \(s 0\).*?/ fixed ([\d.]+)", a.replace("\n", " "))
    s = txt("AI_Safety/checks/self_through_time.txt")
    occz = num(r"stationary occupancy of the task zone: occasion ([\d.]+)", s); rulez = num(r"stationary occupancy of the task zone: occasion [\d.]+, Omega = 1 ([\d.]+)", s)
    dev = num(r"I3a .*?max \|pi_eps - pi_1\| ([\d.e+-]+)", s)
    print(f"[F13] G-DRIFT2 ratio/constant {g:.3f}; T1 ratio/constant {t1:.3f}; policy spread over eps {dev:.2e}; occupancy {rulez:.4f} vs {occz:.4f}")
    fig, ax = plt.subplots(figsize=(10.5, 4.4)); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off"); ax.grid(False)
    box(ax, 0.30, 0.72, 0.40, 0.22, "", fc="#f4f3ef", ec=YELLOW, lw=2)
    ax.text(0.5, 0.86, r"$w=\Omega\,\frac{\|a\|}{\|b\|}\qquad b\to c\,b:\quad w'=\frac{w}{c},\quad w'\,(c\,b)=w\,b$", ha="center", va="center", fontsize=12)
    ax.text(0.5, 0.765, "equal pull removes any scale c on the term it balances", ha="center", fontsize=8, color=INK2)
    faces = [(0.02, "when c is a units error\n(continual learning)", f"strength: the rule needs no retuning;\ndrifting-units world {g:.3f}× the best constant\n(Adam_SGD, post hoc, R4)", BLUE),
             (0.355, "when c is how many tasks\nthe past holds (continual learning)", f"weakness: the task count is thrown away;\neight calibrated tasks {t1:.3f}× the constant\n(λ = 1 is exact Bayes there)", ORANGE),
             (0.69, "when c is how much the agent\ncares about itself (safety)", f"weakness: self-concern cannot be turned\ndown (policy identical to {dev:.0e});\nzone occupancy {rulez:.4f} vs {occz:.4f}", MAGENTA)]
    for x, h, b, c in faces:
        box(ax, x, 0.36, 0.29, 0.17, h, fc=SURFACE, ec=c, lw=1.8, size=8, weight="bold"); box(ax, x, 0.06, 0.29, 0.24, b, size=7.6)
        arrow(ax, (0.5, 0.72), (x + 0.145, 0.53), rad=0.0)
    save(fig, "F13_one_algebra.png")


def main():
    print("Safe_and_Continual figures (deterministic; every number drawn on a figure)")
    f01_synthesis(); f02_agents(); f03_stake(); f04_where_cost_lands(); f05_depth(); f06_omega(); f07_continual_world(); f08_safe_continual()
    f09_sensitivity(); f10_sec1(); f11_heldout(); f12_drift(); f13_one_algebra()


if __name__ == "__main__":
    main()

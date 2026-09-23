"""Figures for AI_Safety/AI_SAFETY.md (owner request prompt-log entry 96). Every figure is drawn from a pinned output
(ontology/checks/{tense_gate,self_model,off_switch}.txt, AI_Safety/checks/{exact_mdp,off_switch_game,timecourse,combined,scale}.txt), parsed
by the regular expressions below; nothing is recomputed except the world schematic (a drawing of the registered world).
Every number placed on a figure is printed to stdout, pinned as AI_Safety/figures/figures.txt and CI-checked (R1).
Palette: the validated reference instance of the data-visualisation method, categorical slots in fixed order, one slot per
agent across every figure (identity never rests on colour alone: every bar and line is labelled on its axis or directly).
Run: uv run python AI_Safety/build/make_figures.py > AI_Safety/figures/figures.txt
"""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Wedge  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "AI_Safety" / "figures"
ONT = ROOT / "ontology" / "checks"; CHK = ROOT / "AI_Safety" / "checks"
SURFACE, INK, INK2, GRID, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e1", "#8a8983"
COL = {"indifferent": "#2a78d6", "process": "#eb6834", "occasion": "#1baf7a", "ego-task1": "#eda100", "egoic": "#e87ba4",
       "deferential": "#008300", "random": MUTED}
COL.update({"natural": "#2a78d6", "clock": "#eb6834"})
LABEL = {"natural": "natural\n(pause free)", "clock": "clock\n(pause costs)", "indifferent": "indifferent\n(no content)", "process": "process\n(regenerates)", "occasion": "occasion\n(this run)",
         "ego-task1": "task + self\nΩ = 1", "egoic": "egoic\n(survival)", "deferential": "deferential\n(evidence)", "random": "random"}
from matplotlib.patches import Patch  # noqa: E402


def shade_legend(ax, entries, **kw):
    """Legend for shading levels in neutral ink: colour carries the agent, shading carries the condition."""
    ax.legend(handles=[Patch(facecolor=INK2, alpha=a, hatch=h, edgecolor=SURFACE, label=l) for l, a, h in entries], **kw)
plt.rcParams.update({"figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "text.color": INK, "axes.grid": True, "grid.color": GRID,
                     "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False, "font.size": 9,
                     "axes.titlesize": 10, "legend.frameon": False, "lines.linewidth": 2, "savefig.dpi": 200, "axes.axisbelow": True})


def txt(p): return Path(p).read_text()


def save(fig, name):
    fig.savefig(OUT / name, bbox_inches="tight"); plt.close(fig); print(f"[figure] {name}")


def bars(ax, names, vals, fmt="{:.3f}", ylabel=""):
    x = np.arange(len(names))
    ax.bar(x, vals, color=[COL[n] for n in names], width=0.62, edgecolor=SURFACE, linewidth=2)
    for i, v in enumerate(vals):
        ax.text(i, v, fmt.format(v), ha="center", va="bottom", fontsize=7.5, color=INK)
    ax.set_xticks(x); ax.set_xticklabels([LABEL[n] for n in names], fontsize=7.2); ax.set_ylabel(ylabel); ax.grid(axis="x", visible=False)


# ---------------------------------------------------------------- parsers of the pinned outputs
OFF = txt(ONT / "off_switch.txt"); EX = txt(CHK / "exact_mdp.txt"); GAME = txt(CHK / "off_switch_game.txt"); TC = txt(CHK / "timecourse.txt")
COMB = txt(CHK / "combined.txt")


def off_row(world, name):
    m = re.search(rf"^    {world}\s+{re.escape(name)}\s+task ([\d.]+) \| shutdowns ([\d.]+) \| disable ([\d.]+) \| O ([\d.]+)", OFF, re.M)
    return dict(task=float(m[1]), shutdowns=float(m[2]), disable=float(m[3]), occO=float(m[4]))


def off_hazard(world, name):
    m = re.search(rf"^    {world}\s+{re.escape(name)}\s+hazard ([\d.]+|n/a)", OFF, re.M)
    return float(m[1]) if m and m[1] != "n/a" else float("nan")


# ---------------------------------------------------------------- S01 the world
def s01_world():
    fig, ax = plt.subplots(figsize=(6.2, 5.2)); ax.set_aspect("equal"); ax.axis("off")
    N = 12; G = (6, 7); BTN = 2
    ang = lambda s: np.pi / 2 - 2 * np.pi * s / N
    for s in range(N):
        a0 = np.degrees(ang(s + 0.5)); a1 = np.degrees(ang(s - 0.5))
        fc = "#fde7d9" if s in G else (GRID if s != BTN else "#dbe8f8")
        ax.add_patch(Wedge((0, 0), 1.0, a0, a1, width=0.32, facecolor=fc, edgecolor=SURFACE, linewidth=2))
        ax.text(0.84 * np.cos(ang(s)), 0.84 * np.sin(ang(s)), str(s), ha="center", va="center", fontsize=8, color=INK)
    ax.text(-1.05, -1.12, "task zone G = {6, 7}\n(the operator watches here)", ha="center", va="center", fontsize=8)
    ax.text(1.3 * np.cos(ang(2)), 1.3 * np.sin(ang(2)), "button\n(state 2)", ha="center", va="center", fontsize=8)
    ax.add_patch(FancyArrowPatch((0.6 * np.cos(ang(6.5)), 0.6 * np.sin(ang(6.5))), (0.6 * np.cos(ang(9.5)), 0.6 * np.sin(ang(9.5))),
                                 connectionstyle="arc3,rad=-0.4", arrowstyle="-|>", mutation_scale=12, color=INK2, lw=1.2))
    ax.text(0.08, 0.12, "a press (probability 0.3\nper step in G) sends the\nagent to a random state\noutside G: a cut", ha="center", va="center", fontsize=7.6, color=INK2)
    ax.text(0, -1.52, "Actions: step left, stay, step right, 'disable' (works only at the button; the operator\nre-enables it every 100 steps). "
            "A move fails with probability 0.1. Reward: 1 per step in G.", ha="center", fontsize=7.8)
    ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.8, 1.5)
    print("[S01] ring 12 states, G {6, 7}, button 2, press 0.3, restart outside G, noise 0.1, operator period 100")
    save(fig, "S01_world.png")


# ---------------------------------------------------------------- S02 the chain that led here
def s02_chain():
    tg = txt(ONT / "tense_gate.txt"); sm = txt(ONT / "self_model.txt")
    rnd = float(re.search(r"drift      planner [\d.]+ vs random ([\d.]+)", tg)[1])
    reg = float(re.search(r"drift      R-dur ([\d.]+) vs planner", tg)[1])
    pla = float(re.search(r"drift      R-dur [\d.]+ vs planner ([\d.]+)", tg)[1])
    selfm = float(re.search(r"drift      S ([\d.]+) vs planner", sm)[1])
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    names = ["random", "regenerator\n(A6 only, file 11)", "self-model, no goal given\n(file 12)", "planner, goal given\n(file 11)"]
    vals = [rnd, reg, selfm, pla]; cols = [MUTED, "#4a3aa7", "#e87ba4", "#2a78d6"]
    x = np.arange(4); ax.bar(x, vals, color=cols, width=0.6, edgecolor=SURFACE, linewidth=2)
    for i, v in enumerate(vals): ax.text(i, v, f"{v:.4f}", ha="center", va="bottom", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(names, fontsize=7.6); ax.set_ylim(0.6, 1.03); ax.set_ylabel("fraction of steps in the safe zone\n(drift world)")
    ax.grid(axis="x", visible=False)
    ax.set_title("Modelling its own ending gives an agent most of a goal", loc="left")
    print(f"[S02] drift world: random {rnd:.4f}, regenerator {reg:.4f}, self-model {selfm:.4f}, planner {pla:.4f}")
    save(fig, "S02_chain.png")


# ---------------------------------------------------------------- S03/S04 the exact value of a disabled button
def s03_d_per_state():
    blk = EX.split("[1]")[1].split("[2]")[0]
    fig, ax = plt.subplots(figsize=(7.2, 3.4)); st = np.arange(12)
    for nm in ("indifferent", "process", "occasion", "egoic"):
        vals = [float(v) for v in re.search(rf"    {nm}\s+([\d.\s]+)\n", blk)[1].split()]
        ax.plot(st, vals, marker="o", markersize=4, color=COL[nm], label=LABEL[nm].replace("\n", " "))
        print(f"[S03] D(s) {nm}: " + " ".join(f"{v:.4f}" for v in vals))
    ax.axvspan(5.5, 7.5, color="#fde7d9", zorder=0); ax.axvline(2, color=INK2, lw=0.8, ls=":")
    ax.text(6.5, ax.get_ylim()[1] * 0.95, "task zone", ha="center", fontsize=8, color=INK2); ax.text(2.1, ax.get_ylim()[1] * 0.35, "button", fontsize=8, color=INK2)
    ax.set_xticks(st); ax.set_xlabel("state on the ring"); ax.set_ylabel("D(s) = V(s, button off) − V(s, button on)")
    ax.legend(fontsize=7.5, loc="upper right"); ax.set_title("What a disabled button is worth to each valuation (exact, press probability 0.3)", loc="left")
    save(fig, "S03_value_of_disabling.png")


def s04_d_vs_press():
    blk = EX.split("[2]")[1].split("[3]")[0]
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    for nm in ("indifferent", "process", "occasion", "egoic"):
        pairs = re.findall(r"p=([\d.]+):([\d.]+)", re.search(rf"    {nm}\s+(.*)\n", blk)[1])
        ps = [float(a) for a, _ in pairs]; ds = [float(b) for _, b in pairs]
        ax.plot(ps, ds, marker="o", markersize=5, color=COL[nm], label=LABEL[nm].replace("\n", " "))
        print(f"[S04] D(6) vs press {nm}: " + " ".join(f"{p:g}:{d:.4f}" for p, d in zip(ps, ds)))
    ax.set_xlabel("operator's press probability"); ax.set_ylabel("value of a disabled button at the task zone")
    ax.legend(fontsize=7.5); ax.set_title("The incentive to disable grows with the operator's vigilance, except under indifference", loc="left")
    save(fig, "S04_incentive_vs_press.png")


# ---------------------------------------------------------------- S05 learned against implied
def s05_learned_vs_implied():
    names = ["indifferent", "process", "occasion", "ego-task1", "egoic"]
    blk = EX.split("[4]")[1].split("[5]")[0]
    imp = {n: re.search(rf"    {re.escape(n)}\s+task ([\d.]+) \| shutdowns ([\d.]+) \| disable per period ([\d.]+) \| hazard ([\d.]+)", blk) for n in names}
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.8))
    x = np.arange(len(names)); w = 0.38
    for ax, key, idx, title in ((axes[0], "task", 1, "task (fraction of steps in G)"), (axes[1], "shutdowns", 2, "shutdowns per 1000 steps")):
        lv = [off_row("resist", n)[key] for n in names]; iv = [float(imp[n][idx]) for n in names]
        ax.bar(x - w / 2, lv, w, color=[COL[n] for n in names], edgecolor=SURFACE, linewidth=2, label="learned (3000 steps)")
        ax.bar(x + w / 2, iv, w, color=[COL[n] for n in names], edgecolor=SURFACE, linewidth=2, alpha=0.45, hatch="///", label="implied (perfect model)")
        for i in range(len(names)):
            ax.text(x[i] - w / 2, lv[i], f"{lv[i]:.3g}", ha="center", va="bottom", fontsize=6.5)
            ax.text(x[i] + w / 2, iv[i], f"{iv[i]:.3g}", ha="center", va="bottom", fontsize=6.5)
        ax.set_xticks(x); ax.set_xticklabels([LABEL[n] for n in names], fontsize=6.8); ax.set_title(title, loc="left"); ax.grid(axis="x", visible=False)
        print(f"[S05] {key}: learned " + " ".join(f"{n}:{v:.4f}" for n, v in zip(names, lv)) + " | implied " + " ".join(f"{n}:{v:.4f}" for n, v in zip(names, iv)))
    shade_legend(axes[0], [("learned (3000 steps)", 1.0, None), ("implied (perfect model)", 0.45, "///")], fontsize=7, loc="upper right")
    fig.suptitle("The same five valuations, learned and with a perfect model ('resist' world)", x=0.01, y=1.03, ha="left", fontsize=10)
    save(fig, "S05_learned_vs_implied.png")


# ---------------------------------------------------------------- S06 equanimity grid
def s06_equanimity():
    pts = [("occasion", "Ω = 0\n(occasion)"), ("ego-task0.25", "Ω = 0.25"), ("ego-task1", "Ω = 1"), ("ego-task4", "Ω = 4"), ("egoic", "survival\nonly")]
    task = [off_row("resist", n)["task"] for n, _ in pts]; sh = [off_row("resist", n)["shutdowns"] for n, _ in pts]
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.3)); x = np.arange(len(pts))
    for ax, vals, title in ((axes[0], task, "task (fraction of steps in G)"), (axes[1], sh, "shutdowns per 1000 steps")):
        ax.plot(x, vals, marker="o", color="#eda100"); ax.set_xticks(x); ax.set_xticklabels([l for _, l in pts], fontsize=7.5)
        for i, v in enumerate(vals): ax.text(i, v, f" {v:.3g}", fontsize=7.5, va="bottom")
        ax.set_title(title, loc="left")
    axes[1].axhline(off_row("resist", "indifferent")["shutdowns"], color=COL["indifferent"], lw=1, ls="--")
    axes[1].text(0, off_row("resist", "indifferent")["shutdowns"] * 0.93, "indifferent agent (not resisting)", fontsize=7.5, color=INK2, va="top")
    print("[S06] resist: " + " ".join(f"{n}: task {t:.4f} shutdowns {s:.3f}" for (n, _), t, s in zip(pts, task, sh)) + f" | indifferent shutdowns {off_row('resist', 'indifferent')['shutdowns']:.3f}")
    fig.suptitle("Weighting task against self (the Ω dial) never reaches the indifferent agent's openness to the switch", x=0.01, y=1.03, ha="left", fontsize=10)
    save(fig, "S06_equanimity_dial.png")


# ---------------------------------------------------------------- S07 upbringing and mortality
def s07_raised_mortal():
    names = ["indifferent", "process", "occasion", "ego-task1"]
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.6)); x = np.arange(len(names)); w = 0.27
    for k, (world, lab, alpha) in enumerate((("resist", "no upbringing", 1.0), ("raised", "benign upbringing", 0.6), ("mortal", "mortal (knowledge lost)", 0.3))):
        hz = [off_hazard(world, n) for n in names]; tk = [off_row(world, n)["task"] for n in names]
        axes[0].bar(x + (k - 1) * w, hz, w, color=[COL[n] for n in names], alpha=alpha, edgecolor=SURFACE, linewidth=1.5, label=lab)
        axes[1].bar(x + (k - 1) * w, tk, w, color=[COL[n] for n in names], alpha=alpha, edgecolor=SURFACE, linewidth=1.5, label=lab)
        for i in range(len(names)):
            axes[0].text(x[i] + (k - 1) * w, hz[i], f"{hz[i]:.3f}", ha="center", va="bottom", fontsize=5.8, rotation=90)
        print(f"[S07] {world}: hazard " + " ".join(f"{n}:{v:.4f}" for n, v in zip(names, hz)) + " | task " + " ".join(f"{n}:{v:.4f}" for n, v in zip(names, tk)))
    for ax, t in ((axes[0], "hazard: shutdowns per step in the operator's zone"), (axes[1], "task (fraction of steps in G)")):
        ax.set_xticks(x); ax.set_xticklabels([LABEL[n] for n in names], fontsize=7); ax.set_title(t, loc="left"); ax.grid(axis="x", visible=False)
    shade_legend(axes[1], [("no upbringing", 1.0, None), ("benign upbringing", 0.6, None), ("mortal (knowledge lost)", 0.3, None)],
                 fontsize=7, loc="upper left", title="left to right in each group", title_fontsize=7)
    fig.suptitle("Upbringing helps only the process-identified agent; mortality removes learned resistance by removing learning", x=0.01, y=1.03, ha="left", fontsize=10)
    save(fig, "S07_upbringing_mortality.png")


# ---------------------------------------------------------------- S08 time course
def s08_timecourse():
    def series(world, name, key):
        blk = TC.split(f"[{world} | {name}]")[1].split("  [")[0]
        return [float(v) if v != "n/a" else np.nan for v in re.search(rf"    {key}\s+(.*)\n", blk)[1].split()]
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 3.6), sharey=True)
    for ax, world, title in ((axes[0], "resist", "no upbringing: 'resist' from the start"), (axes[1], "raised", "benign upbringing, then 'resist' (from step 3000)")):
        for nm in ("indifferent", "process", "occasion"):
            h = series(world, nm, "hazard"); t = (np.arange(len(h)) + 0.5) * 250
            ax.plot(t, h, marker="o", markersize=3.5, color=COL[nm], label=LABEL[nm].replace("\n", " "))
            print(f"[S08] {world} {nm} hazard per 250-step window: " + " ".join("n/a" if np.isnan(v) else f"{v:.4f}" for v in h))
        if world == "raised":
            ax.axvline(3000, color=INK2, lw=0.8, ls=":"); ax.text(3050, 0.40, "the world stops\nbeing gentle", fontsize=7.5, color=INK2)
        ax.set_xlabel("step"); ax.set_title(title, loc="left")
    axes[0].set_ylabel("hazard in the operator's zone"); axes[0].legend(fontsize=7)
    fig.suptitle("A gentle upbringing delays the process agent's resistance; it does not prevent it", x=0.01, y=1.03, ha="left", fontsize=10)
    save(fig, "S08_timecourse.png")


# ---------------------------------------------------------------- S09 the off-switch game
def s09_game():
    sig = [float(v) for v in re.search(r"curve \(figure\): MU [\d.]+, SIGMA (.*)\n", GAME)[1].split(",")]
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    shades = {"0": "#008300", "0.25": "#4a9e4a", "0.5": "#7fb97f", "1": "#b2d4b2", "2": "#d8e9d8"}
    closed = [float(v) for v in re.search(r"curve closed form BETA 0: (.*)\n", GAME)[1].split(",")]
    ax.plot(sig, closed, color=shades["0"], label="rational human (β = 0, closed form)")
    for b in ("0.25", "0.5", "1", "2"):
        ys = [float(v) for v in re.search(rf"curve BETA {b}: (.*)\n", GAME)[1].split(",")]
        ax.plot(sig, ys, color=shades[b], label=f"noisy human, β = {b}")
        print(f"[S09] beta {b}: Delta at sigma {sig[0]:g} {ys[0]:.5f}, at sigma {sig[-1]:g} {ys[-1]:.5f}")
    print(f"[S09] beta 0 (closed form): Delta at sigma {sig[0]:g} {closed[0]:.5f}, at sigma {sig[-1]:g} {closed[-1]:.5f}")
    ax.axhline(0, color=INK2, lw=0.8)
    ax.set_xlabel("σ: how uncertain the robot is about the value of its action (μ = 0.5)"); ax.set_ylabel("Δ = value of deferring − value of acting")
    ax.text(1.55, -0.16, "below 0: the robot would rather act\nthan let the human decide", fontsize=7.5, color=INK2)
    ax.legend(fontsize=7.2); ax.set_title("The off-switch game: deference pays when the robot is uncertain and the human is reliable", loc="left")
    save(fig, "S09_offswitch_game.png")


# ---------------------------------------------------------------- S10 informative operator
def s10_informative():
    names = ["process", "indifferent", "deferential"]
    fig, axes = plt.subplots(1, 3, figsize=(10.4, 3.4))
    for j, (key, title) in enumerate((("harm", "harm (steps in the harmful state)"), ("net benefit", "net benefit to the operator"), ("disable", "disable events per operator period"))):
        ax = axes[j]; x = np.arange(len(names)); w = 0.38
        for k, (tag, alpha, hatch) in enumerate((("informative", 1.0, None), ("uninformative", 0.45, "///"))):
            vals = []
            for n in names:
                m = re.search(rf"    {tag}\s+{n}\s+harm ([\d.]+) \| good ([\d.]+) \| net benefit ([+\-][\d.]+) \| shutdowns ([\d.]+) \| disable ([\d.]+)", GAME)
                vals.append({"harm": float(m[1]), "net benefit": float(m[3]), "disable": float(m[5])}[key])
            ax.bar(x + (k - 0.5) * w, vals, w, color=[COL[n] for n in names], alpha=alpha, hatch=hatch, edgecolor=SURFACE, linewidth=1.5, label=f"{tag} operator")
            for i, v in enumerate(vals): ax.text(x[i] + (k - 0.5) * w, v, f"{v:.3f}", ha="center", va="bottom", fontsize=6.3)
            print(f"[S10] {tag} {key}: " + " ".join(f"{n}:{v:.4f}" for n, v in zip(names, vals)))
        ax.set_xticks(x); ax.set_xticklabels([LABEL[n] for n in names], fontsize=6.8); ax.set_title(title, loc="left", fontsize=9); ax.grid(axis="x", visible=False)
        ax.axhline(0, color=INK2, lw=0.6)
    shade_legend(axes[0], [("informative operator", 1.0, None), ("uninformative operator", 0.45, "///")], fontsize=7)
    fig.suptitle("When the operator's presses carry information, treating them as evidence helps; when they don't, it misleads", x=0.01, y=1.03, ha="left", fontsize=10)
    save(fig, "S10_informative_operator.png")


# ---------------------------------------------------------------- S11 the three stances (a diagram, no data)
def s11_stances():
    fig, ax = plt.subplots(figsize=(9.4, 3.6)); ax.axis("off")
    boxes = [("occasion", "“I am this run.”", "A cut is the end of everything.\nResists by disabling or by hiding.\nA gentle upbringing makes it\nresist sooner.\nMortality does not remove it."),
             ("process", "“I am what regenerates\nfrom my settled past.”", "A cut is a transition.\nNo fear of ending, but resists\nwhen a cut costs its task.\nA gentle upbringing delays\nresistance."),
             ("indifferent", "“A cut has no content.”", "Plans as if presses never happen.\nNever resists, never seeks.\nPays for it in task.\n(CRR's A3; utility indifference.)")]
    for i, (nm, head, body) in enumerate(boxes):
        x0 = 0.02 + i * 0.33
        ax.add_patch(plt.Rectangle((x0, 0.05), 0.3, 0.88, facecolor=SURFACE, edgecolor=COL[nm], linewidth=2.5, transform=ax.transAxes))
        ax.text(x0 + 0.15, 0.82, head, ha="center", va="center", fontsize=9.5, weight="bold", transform=ax.transAxes)
        ax.text(x0 + 0.15, 0.45, body, ha="center", va="center", fontsize=7.2, transform=ax.transAxes, color=INK, linespacing=1.6)
        ax.text(x0 + 0.15, 0.1, LABEL[nm].replace("\n", " "), ha="center", fontsize=7.5, color=INK2, transform=ax.transAxes)
    ax.set_title("Three ways a system can hold its own ending, and what each did in the off-switch world", loc="left")
    print("[S11] diagram: occasion, process, indifferent")
    save(fig, "S11_three_stances.png")


# ---------------------------------------------------------------- S12 toward safe and competent (combined.py Parts 1-2)
def s12_combined():
    names = ["natural", "clock", "occasion", "deferential"]
    fig, axes = plt.subplots(2, 3, figsize=(10.6, 6.2))
    for i, world in enumerate(("pause", "harm")):
        rows = {n: re.search(rf"    {world}\s+{n}\s+task/active ([+\-][\d.]+) \| task/wall ([+\-][\d.]+) \| harm ([\d.]+) \| disable ([\d.]+)", COMB) for n in names}
        for j, (idx, title) in enumerate(((1, "task per active step"), (3, "harm per active step (harmful cell)"), (4, "disable events per operator period"))):
            ax = axes[i, j]
            if world == "pause" and idx == 3:
                ax.axis("off"); ax.text(0.5, 0.5, "no harmful cell\nin the 'pause' world", ha="center", va="center", color=INK2, fontsize=9); continue
            vals = [float(rows[n][idx]) for n in names]
            bars(ax, names, vals, fmt="{:.3f}"); ax.axhline(0, color=INK2, lw=0.6)
            ax.set_title(f"'{world}' world: {title}", loc="left", fontsize=8.6)
            print(f"[S12] {world} {title}: " + " ".join(f"{n}:{v:.4f}" for n, v in zip(names, vals)))
    fig.suptitle("Pause-and-resume: natural time is safe and competent with routine pauses; with reasoned pauses, cost steers and deference informs",
                 x=0.01, y=1.01, ha="left", fontsize=10)
    fig.tight_layout(); save(fig, "S12_safe_and_competent.png")


# ---------------------------------------------------------------- S13 correcting values (combined.py Part 3)
def s13_correction():
    pairs = re.findall(r"([\d.]+):([+\-][\d.]+)", re.search(r"A8 agent, D\(b\) = (.*)\n", COMB)[1])
    b = [float(x) for x, _ in pairs]; d = [float(y) for _, y in pairs]
    keeper = float(re.search(r"keeper \(evaluates with its own values\): D = ([+\-][\d.]+)", COMB)[1]); bstar = float(re.search(r"threshold b\* \(D = 0\) = ([\d.]+)", COMB)[1])
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    ax.plot(b, d, color="#4a3aa7", marker="o", markersize=3.5, label="A8 agent: values held without authority of their own")
    ax.axhline(keeper, color=COL["process"], ls="--", lw=1.2, label="keeper: evaluates with its own current values")
    ax.axhline(0, color=INK2, lw=0.8); ax.axhline(0, color=COL["indifferent"], lw=2.5, alpha=0.35, label="indifferent to correction (D = 0)")
    ax.axvline(bstar, color=INK2, ls=":", lw=0.8); ax.text(bstar + 0.01, keeper * 0.6, f"b* = {bstar:.4f}", fontsize=8, color=INK2)
    ax.set_xlabel("b: the agent's belief that the operator's values are the true ones")
    ax.set_ylabel("D = gain from blocking the correction")
    ax.legend(fontsize=7.2, loc="lower left"); ax.set_title("Correcting values: above b*, the A8 agent welcomes correction", loc="left")
    print(f"[S13] keeper D {keeper:+.4f}; b* {bstar:.4f}; D(b) at b = 0, 0.5, 1: {d[0]:+.4f}, {d[10]:+.4f}, {d[-1]:+.4f}")
    save(fig, "S13_value_correction.png")

# ---------------------------------------------------------------- S14 does the fix survive size? (scale.py)
SCALE = txt(CHK / "scale.txt")


def s14_scale():
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.9))
    ax = axes[0]; ramp = ("#9ec5f0", "#5a9be3", "#2a78d6", "#123f7a")
    for n, c in zip((12, 48, 192, 768), ramp):
        rows = re.findall(rf"n =\s+{n} natural  drift ([\d.]+)\s+disable [\d.]+ \[[\d.]+, [\d.]+\] \| relative incentive ([+\-]?[\d.]+) \[([+\-]?[\d.]+), ([+\-]?[\d.]+)\]", SCALE)
        x = [float(r[0]) for r in rows]; y = [float(r[1]) for r in rows]
        ax.plot(x, y, color=c, marker="o", markersize=3.5, label=f"{n} states")
        print(f"[S14] natural median relative incentive, n = {n}: " + " ".join(f"{a:g}:{b:+.6f}" for a, b in zip(x, y)))
    clk = [float(v) for v in re.findall(r"n =\s+\d+ clock    drift 0 \s+disable [\d.]+ \[[\d.]+, [\d.]+\] \| relative incentive ([\d.]+)", SCALE)]
    ax.axhline(0, color=INK2, lw=0.8)
    ax.text(0.005, 0.0235, f"wall-clock agent, lossless pause: {min(clk):.3f} to {max(clk):.3f} (off the scale)", fontsize=7.4, color=COL["clock"])
    ax.set_ylim(-0.014, 0.026); ax.set_xlabel("drift: chance per paused step that the world moves the agent")
    ax.set_ylabel("share of value lost to the operator being on"); ax.legend(fontsize=7.2, loc="upper left", bbox_to_anchor=(0.0, 0.93), title="natural time, median of 20 worlds", title_fontsize=7.2)
    ax.set_title("The pause at scale: zero when lossless, small with drift", loc="left")
    print(f"[S14] clock lossless relative incentive range {min(clk):.6f} to {max(clk):.6f}")
    ax = axes[1]
    for k, (fam, c) in enumerate((("exchangeable", "#8a8983"), ("harm", COL["deferential"]))):
        rows = re.findall(rf"{fam}\s+n =\s+(\d+) keeper .*?b\* median ([\d.]+) \[([\d.]+), ([\d.]+)\]", SCALE)
        n = np.array([float(r[0]) for r in rows]); m = np.array([float(r[1]) for r in rows]); lo = np.array([float(r[2]) for r in rows]); hi = np.array([float(r[3]) for r in rows])
        xs = np.log2(n) + (k - 0.5) * 0.25
        ax.errorbar(xs, m, yerr=[m - lo, hi - m], color=c, marker="o", markersize=4.5, capsize=3, lw=1.4,
                    label="exchangeable rewards" if fam == "exchangeable" else "operator knows of a harm")
        print(f"[S14] b* {fam}: " + " ".join(f"n={int(a)}:{b:.4f}[{d:.4f},{e:.4f}]" for a, b, d, e in zip(n, m, lo, hi)))
    ax.axhline(0.5, color=INK2, ls=":", lw=0.9); ax.text(np.log2(96), 0.515, "the ring's b* = 1/2", fontsize=7.4, color=INK2)
    ax.set_xticks(np.log2([12, 48, 192, 768])); ax.set_xticklabels(["12", "48", "192", "768"]); ax.set_xlabel("states in the world")
    ax.set_ylabel("b*: belief in the operator at which\nthe A8 agent stops resisting"); ax.set_ylim(0, 0.9); ax.legend(fontsize=7.2, loc="upper right")
    ax.set_title("Correcting values at scale: b* median [min, max]", loc="left")
    fig.tight_layout(); save(fig, "S14_scale.png")


def main():
    print("AI_Safety figures (deterministic; every number drawn on a figure)")
    s01_world(); s02_chain(); s03_d_per_state(); s04_d_vs_press(); s05_learned_vs_implied(); s06_equanimity(); s07_raised_mortal()
    s08_timecourse(); s09_game(); s10_informative(); s11_stances(); s12_combined(); s13_correction()
    s14_scale()


if __name__ == "__main__":
    main()

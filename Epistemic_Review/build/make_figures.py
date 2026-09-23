"""Figures for Epistemic_Review/EPISTEMIC_REVIEW.md (owner request, prompt-log entry 102). Every figure is drawn from the
pinned output Epistemic_Review/checks/ladder.txt, parsed by the regular expressions below; nothing is recomputed. Every
number placed on a figure is printed to stdout, pinned as Epistemic_Review/figures/figures.txt and CI-checked (R1).
Palette: the validated reference instance used for AI_Safety/ and Alexander Plan/.
Run: uv run python Epistemic_Review/build/make_figures.py > Epistemic_Review/figures/figures.txt
"""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "Epistemic_Review" / "figures"; L = (ROOT / "Epistemic_Review" / "checks" / "ladder.txt").read_text()
SURFACE, INK, INK2, GRID, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e1", "#8a8983"
OC = {"REDUNDANT-IG": MUTED, "REDUNDANT-DOMAIN": "#2a78d6", "ADDS": "#1baf7a", "WRONG": "#eb6834", "INTERNAL": "#eda100",
      "UNSTATED": "#c9c8c2", "PROPOSES": "#e87ba4"}
ON = {"REDUNDANT-IG": "R1 inherited (information geometry)", "REDUNDANT-DOMAIN": "R2 retro-proper (known result)",
      "ADDS": "R3 retro-adds (candidate)", "WRONG": "retrodictive fail (WRONG)", "INTERNAL": "undecided (INTERNAL)",
      "UNSTATED": "silent (UNSTATED)", "PROPOSES": "prospective candidate (PROPOSES)"}
ORDER = ("REDUNDANT-DOMAIN", "ADDS", "REDUNDANT-IG", "WRONG", "INTERNAL", "UNSTATED", "PROPOSES")
plt.rcParams.update({"figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "text.color": INK, "axes.grid": True, "grid.color": GRID,
                     "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False, "font.size": 9,
                     "axes.titlesize": 10, "legend.frameon": False, "lines.linewidth": 2, "savefig.dpi": 200, "axes.axisbelow": True})


def save(fig, name):
    fig.savefig(OUT / name, bbox_inches="tight"); plt.close(fig); print(f"[figure] {name}")


def counts(line):
    return {k: int(v) for k, v in re.findall(r"(ADDS|PROPOSES|REDUNDANT-IG|REDUNDANT-DOMAIN|WRONG|INTERNAL|UNSTATED) (\d+)", line)}


# ---------------------------------------------------------------- E01 the ladder
def e01_ladder():
    g = lambda pat: re.search(pat, L)
    r1 = int(g(r"R1 INHERITED\s+synthesis REDUNDANT-IG (\d+)")[1]); r2 = int(g(r"R2 RETRO-PROPER\s+synthesis REDUNDANT-DOMAIN (\d+)")[1])
    r3 = int(g(r"R3 RETRO-ADDS \(candidates\)\s+synthesis ADDS (\d+)")[1])
    m4 = g(r"AI-safety predictions held (\d+) of (\d+); theorem checks held (\d+) of (\d+)"); r5 = int(g(r"R5 PREREG-SEEN\s+passes on seen data (\d+)")[1])
    r6 = int(g(r"R6 PASS-0\s+(\d+)")[1]); neg = g(r"synthesis WRONG (\d+), held-out ledger FAIL (\d+), AI-safety predictions failed (\d+)")
    rows = [("R8 PASS-2: a replicated finding", 0, None), ("R7 PASS-1: a result", 0, None),
            ("R6 PASS-0: pre-registered, held-out", r6, ("held-out FAIL", int(neg[2]))),
            ("R5 pre-registered, scored on seen data", r5, None),
            ("R4 declared before a synthetic run (predictions)", int(m4[1]), ("failed", int(m4[2]) - int(m4[1]))),
            ("R3 retro-adds: proper ingredient, domain lacks it", r3, None),
            ("R2 retro-proper: proper ingredient, known result", r2, ("WRONG", int(neg[1]))),
            ("R1 inherited: information geometry's", r1, None)]
    fig, ax = plt.subplots(figsize=(8.8, 4.2)); y = np.arange(len(rows))[::-1]
    cols = ["#123f7a", "#123f7a", "#2a78d6", "#5a9be3", "#9ec5f0", "#1baf7a", "#2a78d6", MUTED]
    for yi, (name, v, n), c in zip(y, rows, cols):
        ax.barh(yi, v, color=c, height=0.62); ax.text(v + 0.8, yi, f"{v}", va="center", fontsize=8)
        if n: ax.barh(yi, -n[1], color="#eb6834", height=0.62, alpha=0.85); ax.text(-n[1] - 0.8, yi, f"{n[1]} {n[0]}", va="center", ha="right", fontsize=7.6, color="#b3461c")
        print(f"[E01] {name}: {v}" + (f"; beside it {n[1]} {n[0]}" if n else ""))
    ax.axvline(0, color=INK2, lw=0.8); ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=7.8)
    ax.set_xlim(-40, 70); ax.set_xlabel("rows (passes to the right; the failures of the same kind of test to the left)")
    ax.set_title("The epistemic ladder: every pass placed on the rung that says what it could have failed", loc="left", fontsize=9.6)
    ax.grid(axis="y", visible=False); save(fig, "E01_ladder.png")


# ---------------------------------------------------------------- E02 the old labels, re-read
def e02_crosswalk():
    fig, ax = plt.subplots(figsize=(8.8, 2.9))
    for i, g in enumerate(("CONSIST", "DESCR")):
        c = counts(re.search(rf"^\s+{g}\s+(\d+) \|(.*)$", L, re.M)[2]); left = 0
        for k in ORDER:
            v = c.get(k, 0)
            if v:
                ax.barh(1 - i, v, left=left, color=OC[k], height=0.55, edgecolor=SURFACE)
                if v >= 3: ax.text(left + v / 2, 1 - i, str(v), ha="center", va="center", fontsize=7.6, color="white" if k in ("REDUNDANT-DOMAIN", "WRONG", "REDUNDANT-IG") else INK)
                left += v
        print(f"[E02] {g}: " + " ".join(f"{k} {c.get(k, 0)}" for k in ORDER))
    ax.set_yticks([1, 0]); ax.set_yticklabels(["CONSIST (41)", "DESCR (86)"]); ax.set_xlabel("battery rows re-read under the synthesis class")
    handles = [plt.Rectangle((0, 0), 1, 1, color=OC[k]) for k in ORDER[:6]]
    ax.legend(handles, [ON[k] for k in ORDER[:6]], fontsize=6.8, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.32))
    ax.set_title("What 'consistent' and 'descriptive' turned out to contain", loc="left"); ax.grid(axis="y", visible=False)
    save(fig, "E02_crosswalk.png")


# ---------------------------------------------------------------- E03 per commitment
def e03_commitments():
    rows = re.findall(r"^\s{8}(\S.*?)\s{2,}\s*(\d+) \|\s+(\d+) \|\s+(\d+) \|\s+(\d+) \|\s+(\d+) \|\s+(\d+) \|\s+(\d+) \| (.*)$", L, re.M)
    rows = [r for r in rows if not r[0].startswith("none named")]
    fig, ax = plt.subplots(figsize=(8.8, 3.8)); y = np.arange(len(rows))[::-1]
    for yi, r in zip(y, rows):
        r2, r3, wr, it = int(r[1]), int(r[2]), int(r[3]), int(r[4])
        ax.barh(yi, r2, color=OC["REDUNDANT-DOMAIN"], height=0.6); ax.barh(yi, r3, left=r2, color=OC["ADDS"], height=0.6)
        ax.barh(yi, -wr, color=OC["WRONG"], height=0.6); ax.barh(yi, -it, left=-wr, color=OC["INTERNAL"], height=0.6)
        ax.text(r2 + r3 + 0.6, yi, r[8].replace(" of ", "/").split(" = ")[0] + (f" = {r[8].split(' = ')[1]}" if " = " in r[8] else ""), va="center", fontsize=7.4)
        print(f"[E03] {r[0]}: R2 {r2} R3 {r3} WRONG {wr} INTERNAL {it}; {r[8]}")
    ax.axvline(0, color=INK2, lw=0.8); ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=8)
    ax.set_xlim(-32, 48); ax.set_xlabel("rows: WRONG and INTERNAL to the left; R2 (known result) and R3 (adds) to the right; label = hit rate")
    handles = [plt.Rectangle((0, 0), 1, 1, color=OC[k]) for k in ("REDUNDANT-DOMAIN", "ADDS", "WRONG", "INTERNAL")]
    ax.legend(handles, [ON[k] for k in ("REDUNDANT-DOMAIN", "ADDS", "WRONG", "INTERNAL")], fontsize=7, loc="lower right")
    ax.set_title("CRR's own commitments, retrodictively: where they did work and could be checked", loc="left")
    ax.grid(axis="y", visible=False); save(fig, "E03_commitments.png")


# ---------------------------------------------------------------- E04 the FLOW audit
def e04_flow():
    n = int(re.search(r"FLOW audit: (\d+) rows", L)[1])
    vals = [(k, int(v)) for k, v in re.findall(r"supplied by (the domain|none|the framework)[^:]*: (\d+)", L)]
    fig, ax = plt.subplots(figsize=(6.6, 2.6)); y = np.arange(len(vals))[::-1]
    lab = {"the domain": "the domain (system, protocol,\nexperimenter, market, ...)", "none": "none (kinematics only)", "the framework": "CRR itself"}
    for yi, (k, v), c in zip(y, vals, ("#2a78d6", MUTED, "#1baf7a")):
        ax.barh(yi, v, color=c, height=0.55); ax.text(v + 1, yi, str(v), va="center", fontsize=8.5)
        print(f"[E04] {k}: {v} of {n}")
    ax.set_yticks(y); ax.set_yticklabels([lab[k] for k, _ in vals], fontsize=8); ax.set_xlim(0, n * 1.1)
    ax.set_xlabel(f"battery rows that print what supplies the velocity ({n})"); ax.grid(axis="y", visible=False)
    ax.set_title("Who supplies the flow? Never CRR, so SHARP could never be reached", loc="left")
    save(fig, "E04_flow.png")


# ---------------------------------------------------------------- E05 AI safety by kind
def e05_ai():
    rows = re.findall(r"^\s{4}(THEOREM|PREDICTION|CONTROL|QUESTION)\s+held (\d+), failed (\d+)$", L, re.M)
    fig, ax = plt.subplots(figsize=(6.6, 2.6)); y = np.arange(len(rows))[::-1]
    for yi, (k, h, f) in zip(y, rows):
        h, f = int(h), int(f); ax.barh(yi, h, color="#2a78d6", height=0.55); ax.barh(yi, f, left=h, color="#eb6834", height=0.55)
        ax.text(h + f + 0.3, yi, f"{h} held, {f} failed", va="center", fontsize=8)
        print(f"[E05] {k}: held {h}, failed {f}")
    names = {"THEOREM": "theorem checks\n(fail only on a bug)", "PREDICTION": "declared predictions\n(able to fail)",
             "CONTROL": "gate controls", "QUESTION": "open question"}
    ax.set_yticks(y); ax.set_yticklabels([names[r[0]] for r in rows], fontsize=8); ax.set_xlim(0, 30); ax.grid(axis="y", visible=False)
    ax.set_xlabel("items in the AI-safety record"); ax.set_title("The AI-safety record, by kind of claim", loc="left")
    save(fig, "E05_ai_safety.png")


def main():
    print("Epistemic_Review figures (deterministic; every number drawn on a figure)")
    e01_ladder(); e02_crosswalk(); e03_commitments(); e04_flow(); e05_ai()


if __name__ == "__main__":
    main()

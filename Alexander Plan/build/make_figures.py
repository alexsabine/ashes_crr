"""Figures for Alexander Plan/ALEXANDER_PLAN.md (owner request prompt-log entry 101). Every data figure is drawn from a pinned
output (Alexander Plan/model/projections.txt; AI_Safety/checks/scale.txt), parsed by the regular expressions below; nothing
is recomputed except unit conversions, which are printed. The two planning figures (A08 the O-1 timeline, A09 the evidence
map) are drawings of a plan and of a first reading, not data, and say so on their faces. Every number placed on a figure is
printed to stdout, pinned as Alexander Plan/figures/figures.txt and CI-checked (R1). Palette: the validated reference
instance used for AI_Safety/ (categorical slots in fixed order; identity never rests on colour alone).
Run: uv run python "Alexander Plan/build/make_figures.py" > "Alexander Plan/figures/figures.txt"
"""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "Alexander Plan"; OUT = DOC / "figures"
SURFACE, INK, INK2, GRID, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e1", "#8a8983"
SC = {"S0": MUTED, "S1": "#2a78d6", "S2": "#eda100", "S3": "#1baf7a"}
SNAME = {"S0": "S0 no held-out result", "S1": "S1 a result, not replicated", "S2": "S2 replicated, no uptake", "S3": "S3 replicated and taken up"}
plt.rcParams.update({"figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "text.color": INK, "axes.grid": True, "grid.color": GRID,
                     "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False, "font.size": 9,
                     "axes.titlesize": 10, "legend.frameon": False, "lines.linewidth": 2, "savefig.dpi": 200, "axes.axisbelow": True})
P = (DOC / "model" / "projections.txt").read_text(); SCALE = (ROOT / "AI_Safety" / "checks" / "scale.txt").read_text()
YEARS = ("2026Q4", "2027", "2028", "2029", "2030")


def usd(s): return float(s.replace("$", "").replace(",", ""))


def save(fig, name):
    fig.savefig(OUT / name, bbox_inches="tight"); plt.close(fig); print(f"[figure] {name}")


def k(v):
    if v >= 1e6: return f"${v / 1e6:,.2f}M"
    return f"${v / 1000:,.1f}k" if (v < 1e5 and v % 1000) else f"${v / 1000:,.0f}k"


# ---------------------------------------------------------------- A01 the scenario tree
def a01_tree():
    m = re.search(r"p\(M1 by end 2027\) = .*? = ([\d.]+); p\(M2 \| M1\) = ([\d.]+); p\(M3 \| M2\) = ([\d.]+)", P)
    p1, p2, p3 = (float(x) for x in m.groups())
    ps = {s: float(re.search(rf"    {s} .*?p = ([\d.]+)", P)[1]) for s in SC}
    fig, ax = plt.subplots(figsize=(10.2, 4.4)); ax.axis("off"); ax.set_xlim(0, 10.2); ax.set_ylim(0, 4.4)
    def box(x, y, t, c=INK2, w=1.9, h=0.62):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=SURFACE, ec=c, lw=1.6))
        ax.text(x, y, t, ha="center", va="center", fontsize=7.8)
    def arrow(x0, y0, x1, y1, t, dy=0.0):
        ax.annotate("", (x1, y1), (x0, y0), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1))
        ax.text((x0 + x1) / 2, (y0 + y1) / 2 + dy, t, ha="center", va="center", fontsize=7.4, color=INK2, bbox=dict(fc=SURFACE, ec="none", pad=0.6))
    box(1.1, 2.9, "now: toy results,\nno held-out PASS-1")
    box(3.6, 3.6, "M1 end 2027:\na held-out result"); box(3.6, 1.2, SNAME["S0"].replace("S0 ", "S0\n"), SC["S0"])
    arrow(2.05, 3.05, 2.65, 3.5, f"{p1:.4f}"); arrow(2.05, 2.75, 2.65, 1.35, f"{1 - p1:.4f}")
    box(6.1, 3.9, "M2 end 2028:\nreplicated (PASS-2)"); box(6.1, 2.5, SNAME["S1"].replace("S1 ", "S1\n"), SC["S1"])
    arrow(4.55, 3.7, 5.15, 3.85, f"{p2:.4f}", dy=0.22); arrow(4.55, 3.45, 5.15, 2.65, f"{1 - p2:.4f}")
    box(8.8, 3.9, SNAME["S3"].replace("S3 ", "S3 (M3)\n"), SC["S3"]); box(8.8, 2.7, SNAME["S2"].replace("S2 ", "S2\n"), SC["S2"])
    arrow(7.05, 3.95, 7.85, 3.95, f"{p3:.4f}", dy=0.2); arrow(7.05, 3.7, 7.85, 2.85, f"{1 - p3:.4f}")
    for s, (x, y) in {"S0": (3.6, 0.6), "S1": (6.1, 1.9), "S2": (8.8, 2.1), "S3": (8.8, 4.35)}.items():
        ax.text(x, y, f"{s}: p = {ps[s]:.4f}", ha="center", fontsize=8.4, color=SC[s] if s != "S0" else INK2, fontweight="bold")
    ax.text(0.05, 0.1, "p(M1) and p(M2) are Laplace estimates from this repository's own record (5 held-out rows, 0 PASS-1; 1 replication, 0 successes); p(M3) is an assumption.",
            fontsize=7.2, color=INK2)
    ax.set_title("Where the programme could be by 2030: four technical scenarios", loc="left")
    print(f"[A01] p1 {p1:.4f} p2 {p2:.4f} p3 {p3:.4f}; " + " ".join(f"{s} {v:.4f}" for s, v in ps.items()))
    save(fig, "A01_scenario_tree.png")


# ---------------------------------------------------------------- A02 project funding per year
def a02_yearly():
    line = re.search(r"mean project funding per year by final scenario: (.*)\n", P)[1]
    per = {s: [usd(x) for x in re.search(rf"{s} ((?:\$[\d,]+ ?){{5}})", line)[1].split()] for s in SC}
    rows = {y: re.search(rf"    {re.escape(y)}\s+(\$[\d,]+) \|\s+(\$[\d,]+) \|\s+(\$[\d,]+) \|\s+(\$[\d,]+)", P) for y in YEARS}
    up = [usd(rows[y][3]) for y in YEARS]; mean = [usd(rows[y][4]) for y in YEARS]
    fig, ax = plt.subplots(figsize=(7.4, 3.8)); x = np.arange(len(YEARS))
    ax.fill_between(x, 0, up, color=GRID, alpha=0.9, label="all scenarios: up to the upper bound (90th percentile)")
    ax.plot(x, mean, color=INK, lw=1.4, ls="--", label="all scenarios: mean")
    for s in SC:
        ax.plot(x, per[s], color=SC[s], marker="o", markersize=3.5, label=SNAME[s] + " (mean)")
    ax.set_xticks(x); ax.set_xticklabels(YEARS); ax.set_ylabel("project funding per year (USD)")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: k(v)))
    ax.legend(fontsize=7, loc="upper left"); ax.set_title("Grants and fellowships per year: the middle is zero, the mean is carried by a few large awards", loc="left", fontsize=9.2)
    print("[A02] upper " + " ".join(f"{v:,.0f}" for v in up) + "; mean " + " ".join(f"{v:,.0f}" for v in mean))
    for s in SC: print(f"[A02] {s} mean " + " ".join(f"{v:,.0f}" for v in per[s]))
    save(fig, "A02_project_funding_per_year.png")


# ---------------------------------------------------------------- A03 cumulative, by scenario
def a03_cumulative():
    rows = {s: re.search(rf"    {s} ([\d.]+) \| (\$[\d,]+) / (\$[\d,]+) / (\$[\d,]+) \| (\$[\d,]+) / (\$[\d,]+) / (\$[\d,]+)", P) for s in SC}
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.7))
    for ax, off, title in ((axes[0], 2, "project funding, 2026 Q4 to 2030"), (axes[1], 5, "researcher compensation, 2026 Q4 to 2030")):
        for i, s in enumerate(SC):
            lo, md, hi = (usd(rows[s][off + j]) for j in range(3))
            ax.plot([i, i], [lo, hi], color=SC[s], lw=7, alpha=0.45, solid_capstyle="butt"); ax.plot(i, md, "o", color=SC[s], markersize=8, mec=INK, mew=0.6)
            ax.text(i + 0.12, md, k(md), fontsize=7.4, va="center"); ax.text(i, hi, k(hi), fontsize=7, ha="center", va="bottom", color=INK2)
            print(f"[A03] {title} {s}: lower {lo:,.0f} middle {md:,.0f} upper {hi:,.0f}")
        ax.set_xticks(range(4)); ax.set_xticklabels([SNAME[s].replace(" ", "\n", 1) for s in SC], fontsize=7.2)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: k(v))); ax.grid(axis="x", visible=False)
        ax.set_title(title + ": lower to upper, dot = middle", loc="left", fontsize=8.8)
    shares = " ".join(f"{s} {float(rows[s][1]):.4f}" for s in SC); print(f"[A03] shares of draws {shares}")
    fig.tight_layout(); save(fig, "A03_cumulative_by_scenario.png")


# ---------------------------------------------------------------- A04 sensitivity
def a04_sensitivity():
    rows = re.findall(r"    (\S[^|\n]*?)\s+middle\s+(\$[\d,]+) \| upper\s+(\$[\d,]+) \| P\(S3\) ([\d.]+)", P)
    fig, ax = plt.subplots(figsize=(7.4, 3.6)); y = np.arange(len(rows))[::-1]
    for yi, (name, md, hi, s3) in zip(y, rows):
        md, hi = usd(md), usd(hi); c = INK if name == "registered" else "#2a78d6"
        ax.plot([md, hi], [yi, yi], color=c, lw=1.2, alpha=0.6); ax.plot(md, yi, "o", color=c, markersize=6); ax.plot(hi, yi, "|", color=c, markersize=12, mew=2)
        ax.text(hi * 1.03, yi, f"P(S3) {float(s3):.4f}", va="center", fontsize=7.2, color=INK2)
        print(f"[A04] {name}: middle {md:,.0f} upper {hi:,.0f} P(S3) {float(s3):.4f}")
    ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=7.6); ax.set_xscale("log")
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: k(v)))
    ax.set_xlabel("cumulative project funding 2026 Q4 to 2030 (dot = middle, bar = upper), log scale"); ax.set_xlim(5e3, 4e6)
    ax.set_title("What moves the estimate: success rates most, the uptake guess least", loc="left")
    save(fig, "A04_sensitivity.png")


# ---------------------------------------------------------------- A05 the market
def a05_market():
    path = re.findall(r"(\d{4}): \$([\d.]+)B", re.search(r"implied growth .*?\n", P)[0]); g = float(re.search(r"implied growth 2026 -> 2030 ([\d.]+)", P)[1])
    m25 = usd(re.search(r"mkt_2025\s+([\d,]+)", P)[1]); alt = usd(re.search(r"mkt_2030_alt\s+([\d,]+)", P)[1]); ev = usd(re.search(r"eval_2025\s+([\d,]+)", P)[1])
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    xs = [int(a) for a, _ in path]; ys = [float(b) for _, b in path]
    ax.plot(xs, ys, color="#2a78d6", marker="o", markersize=4, label=f"AI safety market (Research and Markets), implied growth {g:.4f} a year")
    ax.plot([2025, 2026], [m25 / 1e9, ys[0]], color="#2a78d6", ls=":", marker="o", markersize=4)
    ax.plot(2030, alt / 1e9, "D", color="#eb6834", label="alternative 2030 forecast (New Market Pitch)")
    ax.plot(2025, ev / 1e9, "s", color="#1baf7a", label="AI safety evaluation market 2025 (InsightAce)")
    for x_, y_ in zip(xs, ys): ax.text(x_, y_ + 0.5, f"${y_:.2f}B", ha="center", fontsize=7.2)
    ax.text(2025, m25 / 1e9 + 0.5, f"${m25 / 1e9:.2f}B", ha="center", fontsize=7.2); ax.text(2030.1, alt / 1e9, f"${alt / 1e9:.2f}B", va="center", fontsize=7.2)
    ax.text(2025.1, ev / 1e9 - 0.9, f"${ev / 1e9:.2f}B", fontsize=7.2)
    ax.set_ylabel("USD billions"); ax.set_xlim(2024.6, 2030.7); ax.legend(fontsize=7, loc="upper left")
    ax.set_title("The market, as reported by market-research firms (definitions differ)", loc="left")
    print(f"[A05] path {ys}; 2025 {m25:,.0f}; alt 2030 {alt:,.0f}; eval 2025 {ev:,.0f}; growth {g:.4f}; labels ${m25 / 1e9:.2f}B, ${alt / 1e9:.2f}B, ${ev / 1e9:.2f}B")
    save(fig, "A05_market.png")


# ---------------------------------------------------------------- A06 the funding programmes
def a06_programmes():
    fx = float(re.search(r"fx_usd_per_gbp\s+([\d.]+)", P)[1])
    g = lambda key: usd(re.search(rf"{key}\s+([\d,]+)", P)[1])
    fell = usd(re.search(r"Anthropic-type fellowship (\$[\d,]+)", P)[1]); mats = re.search(r"MATS 10 to 12 weeks (\$[\d,]+) to (\$[\d,]+)", P)
    fmf = usd(re.search(r"FMF mean grant at least (\$[\d,]+)", P)[1])
    items = [("Corrigibility Research Fund grant", g("crf_lo"), g("crf_hi")), ("MATS stipend, 10 to 12 weeks", usd(mats[1]), usd(mats[2])),
             ("Anthropic-Fellows-type stipend, 16 weeks", fell, fell), ("FMF AI Safety Fund, mean grant (at least)", fmf, fmf),
             ("UK AISI Alignment Project grant (at USD 1.30 per GBP)", g("aisi_lo_gbp") * fx, g("aisi_hi_gbp") * fx),
             ("AI safety researcher salary, US, a year", g("sal_lo"), g("sal_hi")), ("frontier-lab senior IC, total a year", g("frontier_lo"), g("frontier_hi"))]
    fig, ax = plt.subplots(figsize=(7.6, 3.6)); y = np.arange(len(items))[::-1]
    for yi, (name, lo, hi), c in zip(y, items, ("#2a78d6", "#2a78d6", "#2a78d6", "#eda100", "#eda100", "#1baf7a", "#1baf7a")):
        if hi > lo: ax.plot([lo, hi], [yi, yi], color=c, lw=6, alpha=0.7, solid_capstyle="butt")
        else: ax.plot(lo, yi, "o", color=c, markersize=7)
        ax.text(hi * 1.12, yi, (k(lo) + ("" if hi == lo else f" to {k(hi)}")).replace("$", r"\$"), va="center", fontsize=7.2)
        print(f"[A06] {name}: {lo:,.0f} to {hi:,.0f}")
    ax.set_yticks(y); ax.set_yticklabels([i[0] for i in items], fontsize=7.4); ax.set_xscale("log"); ax.set_xlim(3e3, 8e6)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: k(v)))
    ax.set_title("Sizes of the money on offer: small grants, fellowships, project grants, salaries", loc="left", fontsize=9.4)
    save(fig, "A06_programmes.png")


# ---------------------------------------------------------------- A07 continual learning: the value of a no-tuning rule
def a07_cl():
    save_ = float(re.search(r"saves ([\d.]+) of that sweep", P)[1])
    anchors = re.findall(r"p\(works\) = (.*?) ([\d.]+): ([\d.]+)\n", P)
    fig, ax = plt.subplots(figsize=(6.8, 3.4)); p = np.linspace(0, 1, 101)
    ax.plot(p, save_ * p, color="#2a78d6", label=f"expected saving = {save_:.4f} × p(works)")
    for (name, pw, v), c in zip(anchors, ("#eda100", "#eb6834", "#1baf7a")):
        ax.plot(float(pw), float(v), "o", color=c, markersize=7, label=f"{name}: {float(v):.4f}")
        print(f"[A07] {name}: p {float(pw):.4f} saving {float(v):.4f}")
    ax.set_xlabel("p(the rule works as registered)"); ax.set_ylabel("share of a 9-point sweep's compute saved")
    ax.legend(fontsize=7, loc="upper left"); ax.set_title("If a no-tuning rule worked: the saving is on the weight sweep only", loc="left")
    print(f"[A07] full saving {save_:.4f}")
    save(fig, "A07_cl_value.png")


# ---------------------------------------------------------------- A08 the O-1 plan (a drawing of a plan)
def a08_timeline():
    steps = [("engage an immigration attorney; confirm the petitioner", 0, 1), ("collect evidence against the criteria", 0.5, 3.5),
             ("expert letters (Levin agreed, per the owner; others asked)", 1, 3.5), ("advisory opinion from a peer group", 2.5, 3.5),
             ("petitioner files I-129 (premium: 15 business days)", 3.5, 4.3), ("respond to any Request for Evidence", 4.3, 5.5),
             ("visa stamping at a US consulate; start", 5, 6.5), ("in parallel: EQ4, T1x2 and a learned-model safety study", 0, 6.5)]
    fig, ax = plt.subplots(figsize=(8.4, 3.4)); y = np.arange(len(steps))[::-1]
    for yi, (name, a, b) in zip(y, steps):
        c = "#1baf7a" if name.startswith("in parallel") else "#2a78d6"
        ax.barh(yi, b - a, left=a, color=c, alpha=0.75, height=0.55)
    ax.set_yticks(y); ax.set_yticklabels([s[0] for s in steps], fontsize=7.4); ax.set_xlabel("months from engaging an attorney (a plan, not a forecast)")
    ax.set_xlim(0, 7); ax.grid(axis="y", visible=False)
    ax.set_title("A possible O-1 sequence: evidence first, then filing", loc="left")
    print("[A08] planning drawing (no data)")
    save(fig, "A08_o1_timeline.png")


# ---------------------------------------------------------------- A09 the O-1 evidence map (a first reading)
def a09_criteria():
    crit = [("1 nationally or internationally recognised awards", "unknown"), ("2 membership requiring outstanding achievement", "unknown"),
            ("3 published material about you", "unknown"), ("4 judging the work of others", "possible"),
            ("5 original contributions of major significance", "possible"), ("6 scholarly articles", "possible"),
            ("7 critical role at a distinguished organisation", "possible"), ("8 high salary", "weak")]
    col = {"possible": "#1baf7a", "unknown": "#eda100", "weak": MUTED}
    lab = {"possible": "plausible from what you have told me: document it", "unknown": "not known to me: check", "weak": "unlikely to carry weight now"}
    fig, ax = plt.subplots(figsize=(8.0, 3.4)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, len(crit) + 1)
    for i, (name, st) in enumerate(crit):
        yy = len(crit) - i
        ax.add_patch(FancyBboxPatch((0.1, yy - 0.38), 0.5, 0.76, boxstyle="round,pad=0.02", fc=col[st], ec=SURFACE))
        ax.text(0.8, yy, name, va="center", fontsize=8); ax.text(6.0, yy, lab[st], va="center", fontsize=7.6, color=INK2)
    ax.text(0.1, 0.25, "A first reading from the owner's statements; the attorney decides. O-1A needs at least 3 of the 8, each with documents.", fontsize=7.4, color=INK2)
    ax.set_title("The eight O-1A evidentiary criteria: where the evidence may come from", loc="left")
    print("[A09] a first reading, not data: " + ", ".join(f"{n.split()[0]} {s}" for n, s in crit))
    save(fig, "A09_o1_criteria.png")


# ---------------------------------------------------------------- A10-A13 continual learning and the EPO application (cl_patent.txt)
CLP = (DOC / "model" / "cl_patent.txt").read_text()


def a10_cl_evidence():
    rows = re.findall(r"^\s+(EQ[23]) (\w+)\s+rule - tuned ([+\-][\d.]+) \(step ([\d.]+); seeds not behind (\d)/(\d)\) -> (not behind|BEHIND)", CLP, re.M)
    fig, ax = plt.subplots(figsize=(8.2, 3.9)); y = np.arange(len(rows))[::-1]
    for yi, (st, c, d, stp, a, b, lab) in zip(y, rows):
        d, stp = float(d), float(stp); col = "#eb6834" if lab == "BEHIND" else "#2a78d6"
        ax.barh(yi, d, color=col, height=0.6); ax.plot([-stp, -stp], [yi - 0.35, yi + 0.35], color=INK2, lw=1)
        ax.text(d + (0.15 if d >= 0 else -0.15), yi, f"{d:+.2f} ({a}/{b} seeds)", va="center", ha="left" if d >= 0 else "right", fontsize=7.2)
        print(f"[A10] {st} {c}: {d:+.4f} step {stp:.2f} seeds {a}/{b} {lab}")
    ax.axvline(0, color=INK2, lw=0.8); ax.set_yticks(y); ax.set_yticklabels([f"{r[0]} {r[1]}" for r in rows], fontsize=7.8)
    ax.set_xlim(-8, 7); ax.set_xlabel("rule at Ω = 1 minus the in-sample-tuned weight (accuracy points); tick = minus one resolvable step")
    fy = y[[r[1] for r in rows].index("fars")]
    ax.text(-7.9, fy - 0.42, "fars: the pre-registered subsample left a class empty;\nevery EWC-family arm sat at chance", fontsize=6.8, color="#b3461c", va="top")
    s1 = re.search(r"strict \(as registered\): not behind on (\d+) of (\d+)", CLP); s2 = re.search(r"not behind on (\d+) of (\d+) informative", CLP)
    ax.set_title(f"The EWC arm on nine unseen carriers: not behind on {s1[1]} of {s1[2]} (strict), {s2[1]} of {s2[2]} informative", loc="left", fontsize=9.4)
    ax.grid(axis="y", visible=False); save(fig, "A10_cl_evidence.png")


def a11_cl_value():
    g = lambda lab: re.search(rf"{lab}\s*lower (\$[\d,]+) \| middle (\$[\d,]+) \| upper (\$[\d,]+)", CLP)
    rows = [("2029, if adopted", g(r"2029, if adopted:")), ("2030, if adopted", g(r"2030, if adopted:")),
            ("2029-2030, if adopted", g(r"2029-2030 cumulative, adopted futures only:"))]
    mean_all = usd(re.search(r"2029-2030 cumulative, all futures: .*?mean (\$[\d,]+)", CLP)[1]); p_ad = float(re.search(r"share of futures with any value ([\d.]+)", CLP)[1])
    fig, ax = plt.subplots(figsize=(8.2, 3.2)); y = np.arange(len(rows))[::-1]
    for yi, (name, m) in zip(y, rows):
        lo, md, hi = usd(m[1]), usd(m[2]), usd(m[3])
        ax.plot([lo, hi], [yi, yi], color="#2a78d6", lw=6, alpha=0.45, solid_capstyle="butt"); ax.plot(md, yi, "o", color="#2a78d6", markersize=8, mec=INK, mew=0.6)
        ax.text(hi * 1.15, yi, f"{k(lo)} / {k(md)} / {k(hi)}".replace("$", r"\$"), va="center", fontsize=7.4)
        print(f"[A11] {name}: {lo:,.0f} / {md:,.0f} / {hi:,.0f}")
    ax.axvline(mean_all, color="#eb6834", ls="--", lw=1.2)
    ax.set_ylim(y[-1] - 0.5, y[0] + 0.9)
    ax.text(mean_all * 1.08, y[0] + 0.55, f"probability-weighted mean over all futures (2029-2030): {k(mean_all)}; simulated share adopted {p_ad:.4f}".replace("$", r"\$"),
            fontsize=7.2, color="#b3461c")
    ax.set_xscale("log"); ax.set_xlim(8e6, 4e10); ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=8)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: k(v)))
    ax.set_xlabel("saved sweep compute in the field (lower / middle / upper), log scale"); ax.grid(axis="y", visible=False)
    ax.set_title("If the rule transferred and were adopted: large; weighted by the chance it does: modest", loc="left", fontsize=9.4)
    print(f"[A11] mean all futures {mean_all:,.0f}; P(adopted) {p_ad:.4f}")
    save(fig, "A11_cl_value.png")


def a12_cl_sensitivity():
    rows = re.findall(r"^\s{4}(\S.*?)\s{2,}\s*(\$[\d,]+) \|\s+(\$[\d,]+) \| ([\d.]+)$", CLP.split("[4] Sensitivity")[1].split("[5]")[0], re.M)
    fig, ax = plt.subplots(figsize=(8.2, 3.4)); y = np.arange(len(rows))[::-1]
    for yi, (name, v, o, p) in zip(y, rows):
        v = usd(v); c = INK if name == "registered" else "#2a78d6"
        ax.plot(v, yi, "o", color=c, markersize=7); ax.text(v * 1.12, yi, f"{k(v)}  (P adopted {float(p):.4f})".replace("$", r"\$"), va="center", fontsize=7.2)
        print(f"[A12] {name}: {v:,.0f}; patent {usd(o):,.0f}; P {float(p):.4f}")
    ax.set_xscale("log"); ax.set_xlim(2e6, 4e8); ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=7.6)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: k(v)))
    ax.set_xlabel("probability-weighted value created 2029-2030 (mean), log scale"); ax.grid(axis="y", visible=False)
    ax.set_title("What moves the continual-learning value: whether it survives Adam, and how much labs sweep", loc="left", fontsize=9.4)
    save(fig, "A12_cl_sensitivity.png")


def a13_patent():
    m = re.search(r"P\(a granted patent covers the used implementation\) = ([\d.]+) x ([\d.]+) x ([\d.]+) = ([\d.]+)", CLP)
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.0), gridspec_kw=dict(width_ratios=[1.15, 1]))
    ax = axes[0]; ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 3)
    steps = [("an applied use case\nin the application\nas filed", m[1]), ("grant", m[2]), ("claims cover what\na lab actually uses", m[3])]
    for i, (t, p) in enumerate(steps):
        x = 0.3 + i * 3.2
        ax.add_patch(FancyBboxPatch((x, 1.0), 2.6, 1.3, boxstyle="round,pad=0.02,rounding_size=0.1", fc=SURFACE, ec="#2a78d6", lw=1.4))
        ax.text(x + 1.3, 1.65, t, ha="center", va="center", fontsize=7.4); ax.text(x + 1.3, 0.7, f"p = {p}", ha="center", fontsize=8, color="#2a78d6")
        if i < 2: ax.annotate("", (x + 3.15, 1.65), (x + 2.65, 1.65), arrowprops=dict(arrowstyle="-|>", color=INK2))
    ax.text(0.3, 0.1, f"product: {m[4]} (assumptions, swept in the model)", fontsize=8, color="#b3461c")
    ax.set_title("The patent path, as the model prices it", loc="left", fontsize=9.4)
    ax = axes[1]
    ev = [("EPO filing\n(owner)", 2025 + 7 / 12, 0.45), ("priority year\nends", 2026 + 7 / 12, 1.05), ("repository\npublic", 2026 + 8.5 / 12, -0.75),
          ("GPU study\n(assumed 2027)", 2027.3, 0.45), ("US grace\nends", 2027 + 8.5 / 12, 1.05)]
    ax.set_xlim(2025.3, 2028.1); ax.set_ylim(-1.3, 1.6); ax.axhline(0, color=INK2, lw=1); ax.set_yticks([]); ax.grid(False)
    for t, x, yy in ev:
        ax.plot([x, x], [0, yy - 0.08 if yy > 0 else yy + 0.08], color=INK2, lw=0.8); ax.plot(x, 0, "o", color="#eb6834" if "public" in t else "#2a78d6", markersize=6)
        ax.text(x, yy, t, ha="center", va="bottom" if yy > 0 else "top", fontsize=7)
    ax.set_xticks([2025.5, 2026, 2026.5, 2027, 2027.5, 2028]); ax.set_xticklabels(["mid 2025", "2026", "mid 2026", "2027", "mid 2027", "2028"], fontsize=7)
    ax.set_title("The calendar (information, not legal advice)", loc="left", fontsize=9.4)
    for sp in ("left",): ax.spines[sp].set_visible(False)
    print(f"[A13] patent chain {m[1]} x {m[2]} x {m[3]} = {m[4]}; calendar drawn from cl_patent.txt [5]")
    fig.tight_layout(); save(fig, "A13_patent.png")


def main():
    print("Alexander Plan figures (deterministic; every number drawn on a figure)")
    a01_tree(); a02_yearly(); a03_cumulative(); a04_sensitivity(); a05_market(); a06_programmes(); a07_cl(); a08_timeline(); a09_criteria()
    a10_cl_evidence(); a11_cl_value(); a12_cl_sensitivity(); a13_patent()


if __name__ == "__main__":
    main()

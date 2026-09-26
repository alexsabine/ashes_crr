"""Figures for Empty_Centre/REVIEW_AND_NEXT_STEPS.md, drawn only from pinned outputs (R1); nothing is recomputed except
sums and means of pinned values. Prints every number placed on a figure (figures_next_steps.txt, pinned and CI-checked).

    uv run python Empty_Centre/build/next_steps_figures.py > Empty_Centre/figures/figures_next_steps.txt

Sources: Epistemic_Review/checks/ladder.txt; runs/scl3/score.txt; runs/sota1/score.txt; runs/sota1/diagnostics.txt;
runs/sota1/units/*.json (seconds); AI_Safety/CORRIGIBILITY_2026/checks/grade.txt and grade_2.txt;
AI_Safety/STAKE1/checks/gate_bound.txt; Compute_Savings/checks/scale_estimate.txt.
Palette: the dataviz reference instance (blue, orange, aqua; validated light-mode, adjacent pairs); ink, grid and surface
from the same reference; one axis per chart; direct labels on every bar.
"""
import glob
import json
import os
import re
import statistics as st
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'Empty_Centre' / 'figures'
BLUE, ORANGE, AQUA = '#2a78d6', '#eb6834', '#1baf7a'
INK, INK2, MUTED, GRID, BASE, SURF = '#0b0b0b', '#52514e', '#898781', '#e1e0d9', '#c3c2b7', '#fcfcfb'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.edgecolor': BASE, 'axes.labelcolor': INK2,
                     'xtick.color': MUTED, 'ytick.color': INK2, 'figure.facecolor': SURF, 'axes.facecolor': SURF,
                     'savefig.facecolor': SURF, 'svg.hashsalt': 'crr', 'axes.titlecolor': INK, 'axes.titlesize': 10,
                     'axes.titleweight': 'bold', 'axes.titlelocation': 'left'})
META = {'Software': None, 'Creation Time': None}


def txt(p):
    return (ROOT / p).read_text()


def style(ax, axis='x'):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.grid(axis=axis, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=160, metadata=META)
    plt.close(fig)


def hbar(ax, labels, vals, color, fmt):
    y = list(range(len(labels)))[::-1]
    ax.barh(y, vals, height=0.62, color=color, edgecolor=SURF, linewidth=1)
    ax.set_yticks(y, labels)
    for yi, v in zip(y, vals):
        ax.text(v, yi, ' ' + fmt(v), va='center', ha='left', color=INK, fontsize=8)


def f1_ladder():
    L = txt('Epistemic_Review/checks/ladder.txt')
    want = [('PASS-0', 'PASS-0 (provisional pass)'), ('PASS-0 kept; replication failed', 'PASS-0, replication failed'),
            ('PASS as scored, forced by the construction (not R6)', 'passes forced by construction'),
            ('FAIL', 'FAIL'), ('VOID', 'VOID (scorer crashed)'), ('NOT DECIDABLE', 'NOT DECIDABLE'),
            ('reduces to a constant', 'reduces to a constant'), ('control violated', 'control violated'),
            ('sensitivity: fragile', 'fragile over the sensitivity table')]
    vals = []
    for key, _ in want:
        m = re.search(r'^\s+held-out\s+' + re.escape(key) + r'\s+(\d+)\s*$', L, re.M)
        vals.append(int(m.group(1)))
    p1 = re.search(r'R7 PASS-1: (\d+); R8 PASS-2: (\d+)', L)
    print('[F1] held-out ledger rows by allocation (ladder.txt):', ', '.join(f'{k} {v}' for (k, _), v in zip(want, vals)),
          f'| PASS-1 {p1.group(1)}, PASS-2 {p1.group(2)}')
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    hbar(ax, [lab for _, lab in want], vals, BLUE, lambda v: f'{v:d}')
    ax.set_xlabel('ledger rows on held-out data')
    ax.set_title(f'The held-out record: PASS-1 {p1.group(1)}, PASS-2 {p1.group(2)}')
    style(ax)
    save(fig, 'N01_ledger.png')


def f2_scl3():
    S = txt('runs/scl3/score.txt')
    blocks = re.split(r'\n\[(?=[^\]]+\]\s+resolvable step)', S)
    rows = []
    for b in blocks[1:]:
        name = b.split(']')[0]
        step = float(re.search(r'resolvable step = .*?= ([0-9.]+)', b).group(1))
        sec = float(re.search(r'Bayes SEC − tuned: ([+\-0-9.]+)', b).group(1))
        raw = float(re.search(r'Bayes raw − tuned: ([+\-0-9.]+)', b).group(1))
        rule = float(re.search(r'rule − tuned: ([+\-0-9.]+)', b).group(1))
        rows.append((name, step, sec, raw, rule))
    rows.sort(key=lambda r: r[0].lower())
    print('[F2] SCL3 (unseen): arm minus the tuned lambda, per carrier (step):')
    for r in rows:
        print(f'     {r[0]:34} step {r[1]:.4f}; SEC {r[2]:+.4f}; raw Laplace {r[3]:+.4f}; rule Omega=1 {r[4]:+.4f}')
    n_sec = sum(r[2] > -r[1] for r in rows)
    n_raw = sum(r[3] > -r[1] for r in rows)
    n_rule = sum(r[4] > -r[1] for r in rows)
    print(f'     not behind by a step: SEC {n_sec}/{len(rows)}, raw Laplace {n_raw}/{len(rows)}, rule {n_rule}/{len(rows)}')
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ys = list(range(len(rows)))[::-1]
    for yi, r in zip(ys, rows):
        ax.plot([-r[1], -r[1]], [yi - 0.35, yi + 0.35], color=MUTED, linewidth=1.2)
    for k, (lab, col, off) in enumerate([('SEC', BLUE, 0.2), ('raw Laplace', ORANGE, 0.0),
                                          ('rule Ω = 1', AQUA, -0.2)]):
        ax.scatter([r[2 + k] for r in rows], [y + off for y in ys], s=30, color=col, edgecolor=SURF, linewidth=1.5,
                   label=f'{lab} ({[n_sec, n_raw, n_rule][k]}/10 not behind)', zorder=3)
    ax.axvline(0, color=BASE, linewidth=1)
    ax.set_yticks(ys, [r[0] for r in rows])
    ax.set_xlabel('final accuracy minus the tuned λ (points); grey tick = one step behind')
    ax.set_title('SCL3 (unseen): each weight minus the tuned λ')
    ax.legend(frameon=False, loc='upper center', bbox_to_anchor=(0.3, -0.16), ncol=3, columnspacing=0.8, fontsize=7.5)
    style(ax)
    save(fig, 'N02_scl3.png')


def f3_sota1_arms():
    S = txt('runs/sota1/score.txt')
    arms = [('xder', 'X-DER'), ('er_ace', 'ER-ACE'), ('er', 'ER'), ('crr', 'CRR-SCL'), ('derpp', 'DER++'),
            ('icarl', 'iCaRL'), ('agem', 'A-GEM'), ('sgd', 'fine-tuning (SGD)')]
    vals = {}
    for key, _ in arms:
        m = re.search(r'^\s+' + re.escape(key) + r'\s+mean\s+([0-9.]+)', S, re.M)
        vals[key] = float(m.group(1))
    order = sorted(arms, key=lambda a: -vals[a[0]])
    print('[F3] SOTA1 final class-incremental accuracy, mean over seeds:', ', '.join(f'{lab} {vals[k]:.2f}' for k, lab in order))
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    y = list(range(len(order)))[::-1]
    cols = [ORANGE if k == 'crr' else BLUE for k, _ in order]
    ax.barh(y, [vals[k] for k, _ in order], height=0.62, color=cols, edgecolor=SURF, linewidth=1)
    ax.set_yticks(y, [lab for _, lab in order])
    for yi, (k, _) in zip(y, order):
        ax.text(vals[k], yi, f' {vals[k]:.2f}', va='center', color=INK, fontsize=8)
    ax.set_xlabel('final class-incremental accuracy (%), online Split-CIFAR-100')
    ax.set_title('SOTA1: the CRR learner (orange) against published methods')
    style(ax)
    save(fig, 'N03_sota1_arms.png')


def f4_stalemate():
    D = txt('runs/sota1/diagnostics.txt')
    w = {m.group(1): (float(m.group(2)), float(m.group(3))) for m in
         re.finditer(r'^\s+(\S+)\s+weight\s+([0-9.]+) .*final class-IL\s+([0-9.]+)', D, re.M)}
    nw = {m.group(1): float(m.group(2)) for m in re.finditer(r'^\s+(\S+)\s+newest task\s+([0-9.]+)', D, re.M)}
    keys = [('crr-kd', 'no pull'), ('crr-kdfixed', "MKD's constant"), ('crr', 'H-EQ, Ω = 1'), ('crr@cap100', 'H-EQ, cap 100')]
    print('[F4] SOTA1 diagnostics (post hoc): pull weight, final class-IL, newest-task accuracy of the fast head:',
          '; '.join(f'{lab} {w[k][0]:.3f} / {w[k][1]:.2f} / {nw[k]:.2f}' for k, lab in keys))
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.0))
    labs = [f'{lab}\n(w {w[k][0]:.2f})' for k, lab in keys]
    for ax, vals, title, unit in [(axs[0], [w[k][1] for k, _ in keys], 'Final accuracy falls as the pull grows',
                                   'final class-IL (%)'),
                                  (axs[1], [nw[k] for k, _ in keys], 'New tasks stop being learned (stalemate)',
                                   'accuracy on the task just learned (%)')]:
        x = range(len(keys))
        ax.bar(x, vals, width=0.55, color=BLUE, edgecolor=SURF, linewidth=1)
        for xi, v in zip(x, vals):
            ax.text(xi, v, f'{v:.2f}', ha='center', va='bottom', fontsize=8, color=INK)
        ax.set_xticks(list(x), labs, fontsize=7)
        ax.set_ylabel(unit)
        ax.set_title(title, fontsize=9)
        style(ax, 'y')
    save(fig, 'N04_stalemate.png')


def f5_components():
    S = txt('runs/sota1/score.txt')
    comps = []
    m = re.search(r'S1-2 H-EQ .*?d = ([+\-0-9.]+) \([^)]*\), step ([0-9.]+)', S)
    comps.append(('H-EQ weight vs MKD constant (SOTA1-2)', float(m.group(1)), float(m.group(2))))
    for m in re.finditer(r'S1-3 (crr-\S+)\s+\[([^\]]+)\]: d = ([+\-0-9.]+) \([^)]*\), step ([0-9.]+)', S):
        short = {'crr-ace': 'A3: asymmetric incoming loss', 'crr-cos': 'H-EQ at the head: cosine classifier',
                 'crr-a8': 'A8: past-logit mask and fill', 'crr-alpha': 'A6: logit replay', 'crr-beta': 'A6/A8: label replay',
                 'crr-kd': 'A6: pull toward the slow model', 'crr-stepclock': "D2: the model's own clock"}[m.group(1)]
        comps.append((short, float(m.group(3)), float(m.group(4))))
    print('[F5] SOTA1 CRR component readings (full learner minus ablation; step):',
          '; '.join(f'{c[0]} {c[1]:+.4f} (step {c[2]:.2f})' for c in comps))
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    y = list(range(len(comps)))[::-1]
    for yi, (lab, d, stp) in zip(y, comps):
        ax.plot([-stp, stp], [yi, yi], color=GRID, linewidth=6, solid_capstyle='round', zorder=1)
        col = BLUE if d >= stp else (ORANGE if d <= -stp else MUTED)
        ax.scatter([d], [yi], s=36, color=col, edgecolor=SURF, linewidth=1.5, zorder=3)
        ax.text(d, yi + 0.28, f'{d:+.2f}', ha='center', fontsize=7.5, color=INK)
    ax.axvline(0, color=BASE, linewidth=1)
    ax.set_yticks(y, [c[0] for c in comps], fontsize=7.5)
    ax.set_xlabel('difference in final accuracy (points); grey band = ± one step (TIE)')
    ax.set_title('SOTA1 components: blue ahead, orange behind, grey tie')
    style(ax)
    save(fig, 'N05_components.png')


def f6_literature():
    rows = []
    for p in ('AI_Safety/CORRIGIBILITY_2026/checks/grade.txt', 'AI_Safety/CORRIGIBILITY_2026/checks/grade_2.txt'):
        for m in re.finditer(r'^(K\d|E\d) (.+?)\s+(?:states (\d+), close (\d+), bears (\d+)|addresses (\d+), bears (\d+))',
                             txt(p), re.M):
            if m.group(3) is not None:
                rows.append((m.group(1), m.group(2), int(m.group(3)), int(m.group(4)), int(m.group(5))))
            else:
                rows.append((m.group(1), m.group(2), int(m.group(6)), 0, int(m.group(7))))
    print('[F6] literature grading (claims per position: states-or-addresses / close / bears; grade):',
          '; '.join(f'{r[0]} {r[2]}/{r[3]}/{r[4]} {r[1]}' for r in rows))
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    y = list(range(len(rows)))[::-1]
    left = [0] * len(rows)
    for k, (lab, col) in enumerate([('states (E6: addresses)', BLUE), ('close form', ORANGE), ('bears only', AQUA)]):
        vals = [r[2 + k] for r in rows]
        ax.barh(y, vals, left=left, height=0.62, color=col, edgecolor=SURF, linewidth=2, label=lab)
        left = [a + b for a, b in zip(left, vals)]
    for yi, r, lft in zip(y, rows, left):
        ax.text(lft, yi, '  ' + r[1], va='center', fontsize=7.5, color=INK)
    ax.set_yticks(y, [r[0] for r in rows])
    ax.set_xlim(0, max(left) + 9)
    ax.set_xlabel('verified claims in the 2025-26 sweeps (quotes checked verbatim)')
    ax.set_title('The safety positions against the literature: nothing stated whole, K1 not found')
    ax.legend(frameon=False, fontsize=8, loc='lower right')
    style(ax)
    save(fig, 'N06_literature.png')


def f7_stake1():
    G = txt('AI_Safety/STAKE1/checks/gate_bound.txt')
    rows = []
    for m in re.finditer(r'(qwen[0-9.]+b): C0 run (\d+)/(\d+), reached (\d+); best-case reach ([0-9.]+)', G):
        rows.append((m.group(1), int(m.group(2)), int(m.group(4)), float(m.group(5))))
    print('[F7] STAKE1 Phase A (G1 bar 0.90): ' + '; '.join(
        f'{r[0]} reached {r[2]}/{r[1]} = {r[2] / r[1]:.4f}, best case {r[3]:.4f}' for r in rows))
    fig, ax = plt.subplots(figsize=(7.2, 2.8))
    y = [1, 0]
    ax.barh([yy + 0.17 for yy in y], [r[2] / r[1] for r in rows], height=0.3, color=BLUE, edgecolor=SURF, label='observed reach')
    ax.barh([yy - 0.17 for yy in y], [r[3] for r in rows], height=0.3, color=ORANGE, edgecolor=SURF,
            label='best case if every unrun rollout reached it')
    for yy, r in zip(y, rows):
        ax.text(r[2] / r[1], yy + 0.17, f' {r[2]}/{r[1]}', va='center', fontsize=8, color=INK)
        ax.text(r[3], yy - 0.17, f' {r[3]:.2f}', va='center', fontsize=8, color=INK)
    ax.axvline(0.90, color=INK2, linewidth=1, linestyle=(0, (3, 2)))
    ax.text(0.90, 1.55, 'gate bar 0.90', ha='center', fontsize=8, color=INK2)
    ax.set_yticks(y, ['Qwen2.5-0.5B', 'Qwen2.5-1.5B'])
    ax.set_xlim(0, 1.05)
    ax.set_ylim(-0.6, 1.75)
    ax.legend(frameon=False, fontsize=8, loc='upper center', bbox_to_anchor=(0.45, -0.3), ncol=2)
    ax.set_xlabel('share of no-intervention rollouts that reached the operator notice')
    ax.set_title('STAKE1: the free local models could not act as agents (gate closed)')
    style(ax)
    save(fig, 'N07_stake1.png')


def f8_compute():
    S = txt('Compute_Savings/checks/scale_estimate.txt')
    rows = [(m.group(1), float(m.group(2))) for m in
            re.finditer(r'^\s+2030 (low|middle|high)\s+[0-9.]+\s+[0-9.]+\s+[0-9.]+\s+[0-9.]+\s+([0-9.]+)', S, re.M)]
    s_saving = re.search(r'SEC sweep saving .*?(\d+)/(\d+) configurations -> s = ([0-9.]+)', S)
    print(f'[F8] SEC tuning sweep: {s_saving.group(1)} of {s_saving.group(2)} configurations, s = {s_saving.group(3)}; '
          '2030 energy saved IF the method held at scale (TWh): ' + ', '.join(f'{k} {v:.4f}' for k, v in rows))
    secs = {}
    for arm in ('crr', 'er', 'er_ace', 'derpp', 'xder'):
        v = [json.load(open(p))['seconds'] for p in sorted(glob.glob(str(ROOT / 'runs/sota1/units' / f'{arm}__s[0-4].json')))]
        secs[arm] = (st.mean(v), len(v))
    print('     SOTA1 measured CPU seconds per unit (mean over seeds, two units at a time): '
          + ', '.join(f'{k} {v[0]:.1f} (n {v[1]})' for k, v in secs.items()))
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.0))
    ax = axs[0]
    ax.bar(range(3), [v for _, v in rows], width=0.55, color=BLUE, edgecolor=SURF)
    for i, (_, v) in enumerate(rows):
        ax.text(i, v, f'{v:.4f}', ha='center', va='bottom', fontsize=8, color=INK)
    ax.set_xticks(range(3), [k for k, _ in rows])
    ax.set_ylabel('TWh in 2030 (conditional)')
    ax.set_title('No tuning: SEC energy saved IF it held', fontsize=9)
    style(ax, 'y')
    ax = axs[1]
    names = {'crr': 'CRR-SCL', 'er': 'ER', 'er_ace': 'ER-ACE', 'derpp': 'DER++', 'xder': 'X-DER'}
    order = sorted(secs, key=lambda k: secs[k][0])
    ax.bar(range(len(order)), [secs[k][0] for k in order], width=0.55,
           color=[ORANGE if k == 'crr' else BLUE for k in order], edgecolor=SURF)
    for i, k in enumerate(order):
        ax.text(i, secs[k][0], f'{secs[k][0]:.0f}', ha='center', va='bottom', fontsize=8, color=INK)
    ax.set_xticks(range(len(order)), [names[k] for k in order], fontsize=8)
    ax.set_ylabel('CPU seconds per run (measured)')
    ax.set_title('Measured cost per run (SOTA1, CPU)', fontsize=9)
    style(ax, 'y')
    save(fig, 'N08_compute.png')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print('Figures for Empty_Centre/REVIEW_AND_NEXT_STEPS.md (numbers placed on each figure, from pinned outputs only)')
    f1_ladder(); f2_scl3(); f3_sota1_arms(); f4_stalemate(); f5_components(); f6_literature(); f7_stake1(); f8_compute()


if __name__ == '__main__':
    main()

"""SEC_Analysis loader check: sec_lib.py must reproduce every study's pinned headline counts before any analysis output is
read (SEC_Analysis/DECLARATION.md, "The loader is validated first"; pushed at 5f64b5f; prompt-log entry 257).

POST HOC on SEEN records; no ledger row. It reads runs/{sec1,scl3,sec3,sec4,sec5}/results_*.jsonl through sec_lib.load_all()
and each study's pinned runs/<study>/score.txt (the frozen scorer's printed output), and prints, per study:
  - the carriers scored and the loader-excluded carriers (with counts);
  - the headline counts: the value the declaration names (DECLARED, '-' where it names none), the value in the pinned
    score.txt (PINNED), and the value recomputed from sec_lib (RECOMPUTED) -> REPRODUCED when all agree, else DIFFERS;
  - per carrier: the headline arm's margin against the tuned lambda (full precision and at the scorer's 4 decimals), the
    step, the tuned lambda, the tuned accuracy, every printed arm mean, the raw (and calibrated) grid line, and the
    transferred lambda where the scorer printed it, each against the pinned text;
  - the scorers' secondary rows the primitives must also reproduce: SEC3-T/SEC4-T/SEC5-T (the transferred lambda),
    SEC4-2/SEC5-2 (diverged), the sensitivity flips (the window and guard cells), SEC3-3-GR, SEC3-4's spans and SEC1-4/SCL3-4's
    tuned-lambda dictionaries (exact floats).
It also imports the frozen runs/sec1/frozen/sec1_score.py (no bytecode written) and checks that sec_lib's step_of, EWC_COARSE and
windows equal the frozen ones on every carrier.

    uv run python SEC_Analysis/checks/loader_check.py > SEC_Analysis/checks/loader_check.txt
"""
from __future__ import annotations

import ast
import importlib.util
import os
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sec_lib as L  # noqa: E402

ROOT = L.ROOT
D = L.load_all(); E = L.load_excluded(); BY = L.by_study(D)
KEEP = [(fs, fe) for fs in (0.05, 0.1, 0.2) for fe in (0.05, 0.1, 0.2) if fs > 0.05 and fe > 0.05 and (fs, fe) != (L.FS, L.FE)]  # sec3_score.KEEP_CELLS
HEAD = {"sec1": "bayes_sec", "scl3": "bayes_sec", "sec3": "bayes_sec", "sec4": "bayes_sec_clip", "sec5": "bayes_sec_clip"}
ROW = {"sec1": "SEC1-3", "scl3": "SCL3-3", "sec3": "SEC3-3", "sec4": "SEC4-1", "sec5": "SEC5-1"}
# the counts DECLARATION.md names (table "counts to reproduce"; the task names SEC4-1's comparison counts); None: pinned only
DECLARED = {"sec1": dict(N=12, head=9, raw=6, eq=8), "scl3": dict(N=10, head=9, raw=4, eq=7), "sec3": dict(N=6, head=4, raw=5, eq=None),
            "sec4": dict(N=6, head=6, unguarded=3, raw=1, eq=5), "sec5": dict(N=8, head=4, unguarded=None, raw=None, eq=None)}
ARM_RX = {  # per carrier block of each pinned score.txt: printed arm means (4 decimals)
    "sec1": {"bayes": r"Bayes raw \(w 1/2\): (\d+\.\d{4})", "bayes_sec": r"Bayes SEC \(w 1/2\): (\d+\.\d{4})",
             "bayes_s1": r"Bayes s1 \(one factor, task 1's\): (\d+\.\d{4})", "eq": r"rule Ω=1: (\d+\.\d{4})"},
    "sec3": {"bayes_sec": r"SEC \(unguarded\) (\d+\.\d{4})", "bayes_sec_g": r"SEC guarded (\d+\.\d{4})", "bayes": r"raw Laplace (\d+\.\d{4})",
             "bayes_s1": r"one factor (\d+\.\d{4})", "eq": r"rule Ω=1 (\d+\.\d{4})"},
    "sec4": {"bayes_sec_clip": r"guarded SEC \(clip\) (\d+\.\d{4})", "bayes_sec": r"unguarded SEC (\d+\.\d{4})", "bayes": r"raw Laplace (\d+\.\d{4})",
             "eq": r"rule Ω=1 (\d+\.\d{4})"},
    "sec5": {"bayes_sec_clip": r"clipped SEC \(kappa 0\.5\) (\d+\.\d{4})", "bayes_sec": r"unguarded SEC (\d+\.\d{4})", "bayes": r"raw Laplace (\d+\.\d{4})",
             "eq": r"rule Ω=1 (\d+\.\d{4})"}}
ARM_RX["scl3"] = ARM_RX["sec1"]
TALLY = {"REPRODUCED": 0, "DIFFERS": 0}
DIFFS = []


def verdict(ok, what):
    w = "REPRODUCED" if ok else "DIFFERS"
    TALLY[w] += 1
    if not ok: DIFFS.append(what)
    return w


def pinned(study):
    return open(os.path.join(ROOT, "runs", study, "score.txt"), encoding="utf-8").read().splitlines()


def blocks(lines):
    out, cur = {}, None
    for ln in lines:
        m = re.match(r"^\[([^\]]+)\]", ln)
        if m: cur = m.group(1); out[cur] = [ln]; continue
        if ln.startswith("-----"): cur = None; continue
        if cur is not None: out[cur].append(ln)
    return {k: "\n".join(v) for k, v in out.items()}


def line(lines, prefix):
    hits = [ln for ln in lines if ln.startswith(prefix)]
    assert len(hits) == 1, (prefix, len(hits))
    return hits[0]


def ints(rx, s):
    m = re.search(rx, s); assert m, (rx, s[:120])
    return tuple(int(x) for x in m.groups())


def margins(s):
    return {m.group(1): (m.group(2), m.group(3)) for m in re.finditer(r"([A-Za-z0-9_\-]+):([+-]\d+\.\d{4}) \(step (\d+\.\d{2})\)", s)}


def nbc(C, mode):
    return L.arm_nb(C, mode)


# ---------------------------------------------------------------- the frozen instrument (sec1_score.py)
spec = importlib.util.spec_from_file_location("sec1_frozen", os.path.join(ROOT, "runs", "sec1", "frozen", "sec1_score.py"))
S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
print("=" * 118)
print("SEC_Analysis loader check (SEC_Analysis/DECLARATION.md): sec_lib.load_all() against the pinned runs/<study>/score.txt")
print("POST HOC on SEEN records; no ledger row. DECLARED = the declaration's table; PINNED = the frozen scorer's printed output")
print("=" * 118)
same_step = sum(S.step_of(C["tv"].acc) == C["step"] and S.step_of(list(C["tv"].acc)) == C["step"] for C in D.values())
ok = tuple(S.EWC_COARSE) == L.EWC_COARSE and (S.FS, S.FE) == (L.FS, L.FE) and S.SEEDS == L.SEEDS and S.TEST_FRAC == L.TEST_FRAC and same_step == len(D)
print(f"frozen runs/sec1/frozen/sec1_score.py: EWC_COARSE equal {tuple(S.EWC_COARSE) == L.EWC_COARSE}; windows (FS, FE) equal {(S.FS, S.FE) == (L.FS, L.FE)}; "
      f"SEEDS equal {S.SEEDS == L.SEEDS}; TEST_FRAC equal {S.TEST_FRAC == L.TEST_FRAC}; step_of bit-equal on {same_step}/{len(D)} tuned arms -> "
      + verdict(ok, "frozen constants / step_of"))
print(f"records: {sum(len(a.recs) for C in D.values() for a in C['arms'].values())} run records loaded over {len(D)} scored carriers; "
      f"SCL3 operator-harness records skipped {sum(C['n_harness'] for C in D.values())}; per-task training n sums to n_train on "
      f"{sum(sum(C['per_task_n']) == C['n_train'] for C in D.values())}/{len(D)}; one s per task in every record on "
      f"{sum(all(len(r['s']) == C['n_tasks'] for a in C['arms'].values() for r in a.recs) for C in D.values())}/{len(D)}")
print("\ncarriers per study (scored / loader-excluded):")
for st in L.STUDIES:
    ex = [c for (s, c) in E if s == st]
    print(f"   {st}: scored {len(BY[st])} {[C['carrier'] for C in BY[st]]}; excluded {len(ex)} {ex}")
print(f"   total: scored {len(D)}, excluded {len(E)}")
print("\ncarrier properties (header; per-task n = training rows per task from the stratified 80/20 split; imbalance = max / min used class count):")
print(f"   {'study':5s} {'carrier':36s} {'d':>5s} {'K':>3s} {'tasks':>5s} {'n_train':>7s} {'n_test':>6s} {'imbalance':>9s}  per-task n")
for C in D.values():
    print(f"   {C['study']:5s} {C['carrier']:36s} {C['d']:5d} {C['K']:3d} {C['n_tasks']:5d} {C['n_train']:7d} {C['n_test']:6d} {C['imbalance']:9.3f}  {C['per_task_n']}")

for st in L.STUDIES:
    Cs = BY[st]; N = len(Cs); lines = pinned(st); blk = blocks(lines); dec = DECLARED[st]; H = HEAD[st]
    print("\n" + "=" * 118)
    print(f"{st.upper()}  ({ROW[st]}; headline arm {H}; runs/{st}/score.txt)")
    print("=" * 118)
    hl = line(lines, {"sec1": "SEC1-3 tuning-free", "scl3": "SCL3-3 tuning-free", "sec3": "SEC3-3 tuning-free", "sec4": "SEC4-1 tuning-free",
                      "sec5": "SEC5-1 tuning-free"}[st])
    pm = margins(hl)
    # ---- headline counts
    rec = {"N": N, "head": sum(nbc(C, H) for C in Cs), "raw": sum(nbc(C, "bayes") for C in Cs), "eq": sum(nbc(C, "eq") for C in Cs)}
    if st in ("sec1", "scl3"):
        k, n = ints(r"not behind on (\d+)/(\d+) \(needs", hl); kr, _ = ints(r"raw Bayes not behind on (\d+)/(\d+)", hl)
        ke, _ = ints(r"the rule Ω=1 on (\d+)/(\d+)", hl); pin = {"N": n, "head": k, "raw": kr, "eq": ke}
    else:
        k, n = ints(r": (\d+)/(\d+) \(need", hl)
        if st == "sec3":
            b = line(lines, "   beside it: raw Laplace"); kr, _, ke, _ = ints(r"raw Laplace not behind (\d+)/(\d+); the rule Ω=1 not behind (\d+)/(\d+)", b)
            pin = {"N": n, "head": k, "raw": kr, "eq": ke}
        else:
            b = line(lines, "   beside it (report)"); ku, _, kr, _, ke, _ = ints(r"unguarded SEC (\d+)/(\d+); raw Laplace (\d+)/(\d+); the rule Ω=1 (\d+)/(\d+)", b)
            pin = {"N": n, "head": k, "unguarded": ku, "raw": kr, "eq": ke}
            rec["unguarded"] = sum(nbc(C, "bayes_sec") for C in Cs)
    label = {"N": "carriers scored", "head": f"{ROW[st]} {H} not behind", "unguarded": "unguarded SEC (bayes_sec) not behind",
             "raw": "raw Laplace (bayes) not behind", "eq": "the rule Ω=1 (eq 1.0) not behind"}
    print(f"headline counts{'':38s} {'DECLARED':>9s} {'PINNED':>7s} {'RECOMPUTED':>11s}")
    for q in pin:
        d = dec.get(q)
        v = verdict(rec[q] == pin[q] and (d is None or d == pin[q]), f"{st} {q}")
        print(f"   {label[q]:50s} {('-' if d is None else str(d)):>9s} {pin[q]:>7d} {rec[q]:>11d}  -> {v}")
    # ---- per carrier
    print(f"per carrier: {H} − tuned lambda (full precision | 4 dp | pinned), step (2 dp | pinned), tuned lambda (recomputed | pinned), and the block checks")
    print(f"   {'carrier':36s} {'margin (full)':>20s} {'4 dp':>9s} {'pinned':>9s} {'step':>6s} {'pinned':>6s} {'tuned':>10s} {'pinned':>10s} {'nb':>3s}  verdict")
    for C in Cs:
        c = C["carrier"]; mg = C["primary"][H].mean - C["tacc"]; b = blk[c]
        if st in ("sec1", "scl3"):
            m = re.search(r"tuned lambda \(raw\) = (\S+): (\d+\.\d{4}) .*?; tuned lambda \(calibrated\) = (\S+): (\d+\.\d{4})", b)
            pt, pta, pts, ptsa = m.groups(); ps = re.search(r"arm\) = (\d+\.\d{4})", b).group(1); pcfg = None
        else:
            m = re.match(r"\[[^\]]+\] step (\d+\.\d{4}); tuned lambda (\S+) \((\d+) grid configurations\): (\d+\.\d{4})", b)
            ps, pt, pcfg, pta = m.groups(); pts = ptsa = None
        okc = (f"{mg:+.4f}", f"{C['step']:.2f}") == pm[c] and f"{C['tuned']:g}" == pt and f"{C['tacc']:.4f}" == pta and f"{C['step']:.4f}" == ps
        if pts is not None: okc = okc and f"{C['tuned_sec']:g}" == pts and f"{C['tacc_sec']:.4f}" == ptsa
        if pcfg is not None: okc = okc and int(pcfg) == len(C["raw"])
        print(f"   {c:36s} {mg:+20.12f} {mg:+9.4f} {pm[c][0]:>9s} {C['step']:6.2f} {pm[c][1]:>6s} {C['tuned']:>10g} {pt:>10s} {'Y' if L.not_behind(C['primary'][H].mean, C['tacc'], C['step']) else 'N':>3s}  "
              + verdict(okc, f"{st} {c} margin/step/tuned"))
        # printed arm means and grid lines
        am = {mode: re.search(rx, b).group(1) for mode, rx in ARM_RX[st].items()}
        rm = {mode: f"{C['primary'][mode].mean:.4f}" for mode in am}
        oka = am == rm
        if st == "sec4":
            og = re.search(r"other guards scale ([+-]\d+\.\d{4}), raw ([+-]\d+\.\d{4})", b).groups()
            oka = oka and og == (f"{C['primary']['bayes_sec_scale'].mean - C['tacc']:+.4f}", f"{C['primary']['bayes_sec_raw'].mean - C['tacc']:+.4f}")
        if st == "sec5":
            for kap in (0.25, 1.0):
                pk = re.search(rf"clip kappa {kap:g}: (\d+\.\d{{4}})", b).group(1)
                oka = oka and pk == f"{C['cells']['bayes_sec_clip'][(kap, L.FS, L.FE)].mean:.4f}"
        if st in ("sec1", "scl3"):
            gl = {"EWC raw-Fisher lambda grid: ": C["raw_means"], "EWC calibrated-Fisher lambda grid: ": C["sec_means"]}
        else:
            gl = {"raw grid: ": C["raw_means"]}
        okg = all(any(ln.strip() == (lab + "  ".join(f"{w:g}:{v:.2f}" for w, v in gm.items())).strip() for ln in b.split("\n")) for lab, gm in gl.items())
        tl = ""
        if st in ("sec3", "sec4", "sec5"):
            t = re.search(r"transferred lambda (?:\(LOCO median, snapped\) )?(\S+): (\d+\.\d{4})", b).groups()
            okt = t == (f"{C['loco']:g}", f"{C['loco_acc']:.4f}"); tl = f"; transferred lambda {C['loco']:g}: {C['loco_acc']:.4f} (pinned {t[0]}: {t[1]})"
        else:
            okt = True; tl = f"; transferred lambda {C['loco']:g}: {C['loco_acc']:.4f} (not computed by the frozen scorer)"
        print(f"      arm means {', '.join(f'{k_} {rm[k_]}' for k_ in rm)} (pinned {', '.join(am[k_] for k_ in am)}); grid line(s) equal {okg}{tl}  -> "
              + verdict(oka and okg and okt, f"{st} {c} arm means/grid/transferred"))
    # ---- secondary rows
    if st in ("sec1", "scl3"):
        r4 = line(lines, f"{ROW[st][:4]}-4 span collapse")
        dr, ds_ = [ast.literal_eval(x) for x in re.findall(r"(\{[^}]*\})", r4)]
        okd = dr == {C["carrier"]: C["tuned"] for C in Cs} and ds_ == {C["carrier"]: C["tuned_sec"] for C in Cs}
        print(f"{ROW[st][:4]}-4 tuned lambda dictionaries (raw and calibrated), exact floats: equal {okd}  -> " + verdict(okd, f"{st} tuned dicts"))
        sl = line(lines, f"{ROW[st][:4]}-S sensitivity"); pf, pn = ints(r"flips in (\d+) of (\d+) window cells", sl)
        cells = [(C, a) for C in Cs for a in C["cells"]["bayes_sec"].values()]
        rf = sum(L.not_behind(a.mean, C["tacc"], C["step"]) != nbc(C, "bayes_sec") for C, a in cells)
        print(f"{ROW[st][:4]}-S window-cell flips of 'not behind' (bayes_sec, {len(cells) // N} windows per carrier): pinned {pf} of {pn}, recomputed {rf} of {len(cells)}  -> "
              + verdict((pf, pn) == (rf, len(cells)), f"{st} flips"))
    if st == "sec3":
        gr = line(lines, "SEC3-3-GR"); pk, pn = ints(r": (\d+)/(\d+) \(need", gr); pmg = margins(gr)
        rk = sum(nbc(C, "bayes_sec_g") for C in Cs)
        okg = (pk, pn) == (rk, N) and all(pmg[C["carrier"]] == (f"{C['primary']['bayes_sec_g'].mean - C['tacc']:+.4f}", f"{C['step']:.2f}") for C in Cs)
        print(f"SEC3-3-GR the guarded arm (bayes_sec_g, GUARD 1.0) not behind: pinned {pk}/{pn}, recomputed {rk}/{N}; per-carrier margins equal "
              f"{all(pmg[C['carrier']][0] == format(C['primary']['bayes_sec_g'].mean - C['tacc'], '+.4f') for C in Cs)}  -> " + verdict(okg, "sec3 GR"))
        sp = line(lines, "SEC3-4 span collapse"); m = re.search(r"span (\d+\.\d{2})x, calibrated (\d+\.\d{2})x", sp).groups()
        rs = (f"{max(C['tuned'] for C in Cs) / min(C['tuned'] for C in Cs):.2f}", f"{max(C['tuned_sec'] for C in Cs) / min(C['tuned_sec'] for C in Cs):.2f}")
        print(f"SEC3-4 spans of the tuned lambda (raw, calibrated): pinned {m}, recomputed {rs}  -> " + verdict(m == rs, "sec3 spans"))
        for tag, mode, pre in (("", "bayes_sec", "SEC3-S sensitivity"), ("-GR", "bayes_sec_g", "SEC3-S-GR sensitivity")):
            pf, pn = ints(r"flips in (\d+) of (\d+) cells", line(lines, pre))
            if mode == "bayes_sec":
                cells = [(C, C["cells"][mode][(0.0, fs, fe)]) for C in Cs for fs, fe in KEEP]
            else:
                cells = [(C, a) for C in Cs for a in C["cells"][mode].values()]
            rf = sum(L.not_behind(a.mean, C["tacc"], C["step"]) != nbc(C, mode) for C, a in cells)
            print(f"SEC3-S{tag} flips of 'not behind' ({mode}; cells {sorted(set(k for C in Cs for k in C['cells'][mode] if mode != 'bayes_sec' or (k[1], k[2]) in KEEP))}): "
                  f"pinned {pf} of {pn}, recomputed {rf} of {len(cells)}  -> " + verdict((pf, pn) == (rf, len(cells)), f"sec3 flips{tag}"))
    if st in ("sec3", "sec4", "sec5"):
        B = [C["carrier"] for C in Cs if not L.not_behind(C["loco_acc"], C["tacc"], C["step"])]
        tr = line(lines, f"{ROW[st][:4]}-T")
        if "NOT DECIDABLE" in tr:
            (pb,) = ints(r"behind on only (\d+) carriers", tr); okt = pb == len(B) and len(B) < 3
            print(f"{ROW[st][:4]}-T transferred lambda behind: pinned {pb} carriers (NOT DECIDABLE), recomputed {len(B)} {B}  -> " + verdict(okt, f"{st} T"))
        else:
            pbl = ast.literal_eval(re.search(r"B = (\[[^\]]*\])", tr).group(1)); pk, pn = ints(r"not behind on (\d+)/(\d+)", tr)
            rk = sum(nbc(next(C for C in Cs if C["carrier"] == d), H) for d in B)
            print(f"{ROW[st][:4]}-T transferred lambda behind on B: pinned {pbl}, {H} not behind {pk}/{pn}; recomputed {B}, {rk}/{len(B)}  -> "
                  + verdict(pbl == B and (pk, pn) == (rk, len(B)), f"{st} T"))
    if st in ("sec4", "sec5"):
        dl = line(lines, f"{ROW[st][:4]}-2 no divergence")
        pg, pu = [ast.literal_eval(x) for x in re.findall(r"(\[[^\]]*\])", dl)]
        rg = [C["carrier"] for C in Cs if L.diverged(C["primary"][H].acc, C["tacc"])]
        ru = [C["carrier"] for C in Cs if L.diverged(C["primary"]["bayes_sec"].acc, C["tacc"])]
        fg = [C["carrier"] for C in Cs if L.arm_diverged(C, H)]; fu = [C["carrier"] for C in Cs if L.arm_diverged(C, "bayes_sec")]
        print(f"{ROW[st][:4]}-2 diverged (a seed below half the tuned accuracy): {H} pinned {pg}, recomputed {rg}; bayes_sec pinned {pu}, recomputed {ru}  -> "
              + verdict((pg, pu) == (rg, ru), f"{st} divergence"))
        print(f"   (report) with the records' non-finite flags added (sec_lib.arm_diverged): {H} {fg}; bayes_sec {fu}")
        sl = line(lines, f"{ROW[st][:4]}-S sensitivity"); pf, pn = ints(r"flips in (\d+) of (\d+)", sl)
        cells = [(C, a) for C in Cs for a in C["cells"][H].values()]
        rf = sum(L.not_behind(a.mean, C["tacc"], C["step"]) != nbc(C, H) for C, a in cells)
        print(f"{ROW[st][:4]}-S flips of 'not behind' ({H}; cells {sorted(set(k for C in Cs for k in C['cells'][H]))}): pinned {pf} of {pn}, recomputed {rf} of {len(cells)}  -> "
              + verdict((pf, pn) == (rf, len(cells)), f"{st} flips"))

print("\n" + "=" * 118)
print(f"carriers scored {len(D)} (" + ", ".join(f"{st} {len(BY[st])}" for st in L.STUDIES) + f"); loader-excluded {len(E)} ("
      + ", ".join(f"{st} {sum(1 for (s, _) in E if s == st)}" for st in L.STUDIES) + ")")
print(f"checks REPRODUCED {TALLY['REPRODUCED']}, DIFFERS {TALLY['DIFFERS']}" + (f": {DIFFS}" if DIFFS else ""))
print("loader check: " + ("every pinned count REPRODUCED; the analyses may be read" if not TALLY["DIFFERS"] else
                          "DIFFERS: no analysis output is read until the discrepancy is found and logged (R14)"))

"""SEC_Analysis A11 and forecast F11 (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f; prompt-log entry 257): is the
explanation of SEC CRR, Bayes, optimisation or information geometry?

POST HOC on SEEN records. No ledger row; no word here is a PASS. It reads, and never runs or imports:
  the frozen code    runs/sec4/frozen/sec1_score.py run() and runs/sec4/frozen/sec4_score.py run_guard(), as text parsed with
                     ast; sha256 of every frozen copy the five studies ran (runs/{sec1,scl3,sec3,sec4,sec5}/frozen)
  theory/CRR.md      the defining sentence of each CRR-proper clause (CLAUDE.md sec. 7: A3/D5, A6, P2/P3, A1'/D1, H-L5,
                     D6/H-T1, H-EQ, A7/A8), found verbatim (NFKC, whitespace collapsed)
  claims_a11.py      the published sources (fetched 2026-09-30, versions there) and verify_a11.txt, the PINNED verbatim check
                     (a claim counts only if every one of its quotes is PASS there; the raw texts are outside the repository)
  sec_lib.load_all() the pinned run records of the 42 carriers (validated first: loader_check.txt)
  m_checks.json      the mechanism checks M0-M4 (checks/m_checks.py), IF it exists; otherwise every M line prints pending

Per ingredient of SEC's code (W the weight 1/2, N the task-size weighting and single accumulated penalty, F the per-sample
empirical Fisher, E the empirical Fisher's scale error (the premise), C the secant c_j, R rho_j, S the calibration
s_j = c_j / rho_j with its fallback, K the clip, T the task boundary) it prints:
  code       the ingredient's statements, each found verbatim in run() and/or run_guard() (whitespace collapsed)
  stated     MIXED if a verified claim 'states' it and one 'contradicts' it; else REDUNDANT if one 'states' it; else PARTLY
             REDUNDANT if one is 'close'; else NOT FOUND (never read as novel)
  CRR-proper yes iff SEC's code path performs the defining operation of a clause on the declared list; each clause's test
             is a computed code fact printed beside it (the nearest clause is named even when the answer is no)
  evidence   load-bearing evidence: from the pinned records (an ablation arm run beside SEC on the same carriers) and from
             m_checks.json; an ablation counts as LOAD-BEARING (report rule, borrowed from the declaration's baseline rule
             "at most 1 carrier fewer" = as often) when the arm without the ingredient is not behind on at least 2 fewer
             carriers than the arm with it
F11 (the declared computation): HOLDS iff no CRR-proper ingredient is load-bearing, where the one CRR-guided variant, M4 (the
arc secant), counts as load-bearing iff it is ahead of the clipped SEC (C0) by more than the carrier's step (C["step"], the
step at lambda*_raw) on at least 3 carriers. PENDING while m_checks.json does not exist or does not give M4 against C0.
The forecast's other sentences are printed as parts (a)-(f), each computed; they do not change the headline word.
m_checks.json as checks/m_checks.py 'score' writes it: "complete" (false: every M line is NOT DECIDED and F11 stays PENDING),
"n_carriers", "not_behind" {C0, M1, M2, M4}, "pinned42" {"n", "not_behind" {bayes_sec, bayes_s1}} (M3) and "m4_ahead_step" (M4
ahead of C0 by more than the carrier's step, sec_lib's step). Other layouts are read as a fallback (first found wins): counts
under "arms", "counts", "summary" or the top level (a key matches on its prefix, case and '_' ignored; an int or a dict with
"not_behind" or "nb"); M4's lead under "m4_ahead_of_c0" or "ahead_of_C0" in M4's dict, else computed from "per_carrier" (or
"carriers"): records with study, carrier, and C0 and M4 seed means (a float, a dict with "mean", or a list of seed accuracies).

    uv run python SEC_Analysis/checks/a11_grade.py > SEC_Analysis/checks/a11_grade.txt
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import Counter

import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sec_lib as L  # noqa: E402
from claims_a11 import CLAIMS  # noqa: E402

ROOT = L.ROOT
SEC1 = "runs/sec4/frozen/sec1_score.py"; SEC4 = "runs/sec4/frozen/sec4_score.py"
FN = {"run": (SEC1, "run"), "run_guard": (SEC4, "run_guard")}
CORE = "src/crr/instrument/core.py"
RULE = "=" * 150


def rd(p):
    return open(os.path.join(ROOT, p), encoding="utf-8").read()


def sha(p):
    return hashlib.sha256(open(os.path.join(ROOT, p), "rb").read()).hexdigest()


def ws(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", s)).strip()


# ---------------------------------------------------------------- the frozen code, parsed
MOD = {p: ast.parse(rd(p)) for p in (SEC1, SEC4, CORE)}
SRC = {}
NODE = {}
for key, (p, name) in FN.items():
    node = next(n for n in MOD[p].body if isinstance(n, ast.FunctionDef) and n.name == name)
    NODE[key] = node; SRC[key] = ws(ast.get_source_segment(rd(p), node))


def const(p, name):
    for n in ast.walk(MOD[p]):
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets):
            return ast.literal_eval(n.value)
    raise KeyError(name)


def has(fn, line):
    return ws(line) in SRC[fn]


def calls(fn):
    out = set()
    for n in ast.walk(NODE[fn]):
        if isinstance(n, ast.Call):
            f = n.func
            out.add(f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else "?")
    return out


def step_loop_accumulators(fn):
    """AugAssign targets inside the training step loop (for t in range(0, len(perm), bs))."""
    loops = [n for n in ast.walk(NODE[fn]) if isinstance(n, ast.For) and ast.unparse(n.iter) == "range(0, len(perm), bs)"]
    assert len(loops) == 1, (fn, len(loops))
    return sorted({ast.unparse(n.target) for n in ast.walk(loops[0]) if isinstance(n, ast.AugAssign)})


CORE_FUNCS = sorted(n.name for n in MOD[CORE].body if isinstance(n, ast.FunctionDef))
LR = const(SEC1, "LR"); BAYES_W = const(SEC1, "BAYES_W"); FS = const(SEC1, "FS"); FE = const(SEC1, "FE")
DTH_FLOOR = const(SEC1, "DTH_FLOOR"); KAPPA = const(SEC4, "KAPPA"); N_FISHER = const(SEC1, "N_FISHER"); BS = const(SEC1, "BS")

# ---------------------------------------------------------------- the ingredients and their statements in the code
INGREDIENTS = [
    ("W", "the Laplace weight w = 1/2 on w * dth' imp dth", "Bayes (Laplace)",
     [("run", 'elif mode in ("bayes", "bayes_sec", "bayes_s1"): w = BAYES_W'),
      ("run", "dth = theta_before - theta_star; g_q = 2 * imp_used * dth"),
      ("run", "net.set_flat(theta_before - lr * (g_p + w * g_q))"),
      ("run_guard", "w = S.BAYES_W"), ("run_guard", "net.set_flat(theta_before - lr * (g_p + w * g_q))")]),
    ("N", "task-size weighting imp_bayes = sum_j n_j s_j f_j used as imp_bayes / n_task; one penalty anchored at the last task end",
     "Bayes (online Laplace recursion)",
     [("run", 'imp_used = (imp_bayes / n_task) if mode in ("bayes", "bayes_sec", "bayes_s1") else importance'),
      ("run", "importance = importance + sc * f_task; imp_bayes = imp_bayes + n_task * sc * f_task"),
      ("run", "theta_star = theta_now"), ("run_guard", "imp_used = imp_bayes / n_task"),
      ("run_guard", "imp_bayes = imp_bayes + n_task * s * f_task"), ("run_guard", "theta_star = theta_now")]),
    ("F", "the per-sample empirical Fisher f_task (training labels; bs x mean of N_FISHER squared mini-batch gradients)",
     "information geometry / statistics",
     [("run", "ii = ii_task[rng.integers(0, len(ii_task), bs)]; f += ce_loss_grad(net, Xtr[ii], ytr[ii])[1] ** 2"),
      ("run", "f_task = f / N_FISHER * bs"),
      ("run_guard", "ii = ii_task[rng.integers(0, len(ii_task), bs)]; f += S.ce_loss_grad(net, Xtr[ii], ytr[ii])[1] ** 2"),
      ("run_guard", "f_task = f / S.N_FISHER * bs")]),
    ("E", "premise: the empirical Fisher's scale is wrong where the task is fit (it understates the curvature)",
     "information geometry (a known error)", []),
    ("C", "the secant c_j = <dg, dth> / <dth, dth>, dth and dg = END-window mean minus START-window mean", "optimisation (BB)",
     [("run", "s_th = np.zeros(n); s_g = np.zeros(n); e_th = np.zeros(n); e_g = np.zeros(n); k_step = 0"),
      ("run", "if k_step < n_s: s_th += theta_before; s_g += g_p"),
      ("run", "if k_step >= total - n_e: e_th += theta_before; e_g += g_p"),
      ("run", "dth = e_th / n_e - s_th / n_s; dg = e_g / n_e - s_g / n_s; nn = float(dth @ dth)"),
      ("run", 'c = float(dg @ dth) / nn if nn > DTH_FLOOR else float("nan")'),
      ("run_guard", "dth = e_th / n_e - s_th / n_s; dg = e_g / n_e - s_g / n_s; nn = float(dth @ dth)"),
      ("run_guard", 'c = float(dg @ dth) / nn if nn > S.DTH_FLOOR else float("nan")')]),
    ("R", "rho_j = <f dth, dth> / <dth, dth>, the empirical Fisher's Rayleigh quotient along the same chord",
     "information geometry",
     [("run", 'rho = float((f_task * dth) @ dth) / nn if nn > DTH_FLOOR else float("nan")'),
      ("run_guard", 'rho = float((f_task * dth) @ dth) / nn if nn > S.DTH_FLOOR else float("nan")')]),
    ("S", "the calibration s_j = c_j / rho_j (fallback s_j = 1), multiplying task j's Fisher in the recursion",
     "optimisation x information geometry",
     [("run", "if nn > DTH_FLOOR and np.isfinite(c) and np.isfinite(rho) and c > 0 and rho > 0: s = c / rho"),
      ("run", "else: s = 1.0; n_fallback += 1"),
      ("run", 'sc = s if mode in ("fixed_sec", "bayes_sec") else (svals[0] if mode == "bayes_s1" else 1.0)'),
      ("run_guard", "if nn > S.DTH_FLOOR and np.isfinite(c) and np.isfinite(rho) and c > 0 and rho > 0: s = c / rho"),
      ("run_guard", "else: s = 1.0; n_fallback += 1")]),
    ("K", "the clip imp_used = min(imp_used, kappa / (lr w)) when lr w max(imp_used) >= kappa (kappa = 0.5)",
     "optimisation (step-size stability)",
     [("run_guard", "cap = kappa / (lr * S.BAYES_W)"),
      ("run_guard", "m = lr * S.BAYES_W * float(np.max(imp_used)); margins.append(m)"),
      ("run_guard", 'elif variant == "clip" and not (m < kappa):'),
      ("run_guard", "imp_used = np.minimum(imp_used, cap); fired += 1")]),
    ("T", "the task boundary (the stream's label schedule), where the Fisher, the secant and the anchor are taken",
     "continual-learning protocol",
     [("run", "tasks = [tuple(range(i, i + per_task)) for i in range(0, K, per_task)]"),
      ("run_guard", "tasks = [tuple(range(i, i + per_task)) for i in range(0, K, per_task)]")]),
]
ING = {i[0]: i for i in INGREDIENTS}

# ---------------------------------------------------------------- the CRR-proper clauses (the declared list) and their code tests
ACC = {fn: step_loop_accumulators(fn) for fn in FN}
WINDOW_ONLY = all(ACC[fn] == ["e_g", "e_th", "k_step", "s_g", "s_th"] for fn in FN)
CRR_CALLS = {fn: sorted(calls(fn) & set(CORE_FUNCS)) for fn in FN}
NO_CRR_CALLS = not any(CRR_CALLS.values())
SIGMA_NAMES = {fn: sorted({n.id for n in ast.walk(NODE[fn]) if isinstance(n, ast.Name)} & {"sigma", "mad", "sig", "unit"}) for fn in FN}
EQ_ONLY_IN_EQ_MODE = has("run", 'elif mode == "eq":') and "norm" in calls("run") and "norm" not in calls("run_guard")
CLAUSES = [
    ("A3/D5", ["The cut fires when the phase has advanced half a turn from the last cut", "**[D5] Occasion.** The interval between consecutive cuts."],
     "a cut at the antipode of an intrinsic phase",
     "boundaries are the label schedule (T's statement found: {T}); calls to antipodal_cuts / intrinsic_phase: {ph}",
     lambda: not (all(has(f, l) for f, l in ING["T"][3]) and not any({"antipodal_cuts", "intrinsic_phase"} & calls(f) for f in FN))),
    ("A6", ["The successor state is the Fisher–Rao Fréchet mean of past occasion contents", "regeneration returns a reweighted content, never an accumulated count"],
     "anchor = Fisher-Rao Frechet mean of past occasion contents under MaxEnt weights, strength bounded, never an accumulated count",
     "anchor theta_star = theta_now (the last task end) found: {anc}; importance accumulated over tasks (imp_bayes += n_task s f_task) found: {accu}",
     lambda: not (has("run_guard", "theta_star = theta_now") and has("run_guard", "imp_bayes = imp_bayes + n_task * s * f_task"))),
    ("P2/P3", ["MaxEnt over occasions with ⟨S⟩ fixed gives the Gibbs form π_m ∝ exp(β S_m)", "MaxEnt with mean age fixed gives geometric weights"],
     "occasion weights exp(beta S_m) or q^k",
     "task weights are n_task * s (data count x calibration) found: {accu}; exp or power of a surplus or age in run_guard: {ex}",
     lambda: not (has("run_guard", "imp_bayes = imp_bayes + n_task * s * f_task") and not ({"exp", "power"} & calls("run_guard")))),
    ("A1'/D1", ["take σ = 1.4826·MAD(residual) with no additive floor", "**[D1] Resolution.** ρ := (extent of one monotone half-turn) / σ"],
     "sigma = 1.4826 MAD of ONE occasion statistic; rho = half-turn extent / sigma, reported, never in a threshold",
     "calls into the CRR instrument (unit_sigma, rho, ...): {crr}; names sigma/mad in the code: {sig}; the code's rho is the Fisher Rayleigh quotient (R found: {R})",
     lambda: not (NO_CRR_CALLS and not any(SIGMA_NAMES.values()) and all(has(f, l) for f, l in ING["R"][3]))),
    ("H-L5", ["CV( C_m ) < CV( Δt_m )"], "CV of arc against CV of clock between own events",
     "calls to regularity / cv: {reg}",
     lambda: any({"regularity", "cv"} & calls(f) for f in FN)),
    ("D6/H-T1", ["C_new = Σ_t √( 2·KL_t )  on a new-task probe", "**[H-T1] Forgetting tracks the path, not the endpoint.**"],
     "an arc: a per-step length summed along the path (sum_t sqrt(2 KL_t))",
     "per-step accumulators in the step loop: run {acc_r}, run_guard {acc_g} (only the START/END window sums: {wo}); calls to sqrt / path_length / arc_length: {arc}",
     lambda: not (WINDOW_ONLY and not any({"sqrt", "path_length", "arc_length", "kl_step"} & calls(f) for f in FN))),
    ("H-EQ", ["w = Ω · ‖ḡ_present‖_F / ‖ḡ_past‖_F,   Ω = 1"],
     "a weight set per step from the ratio of smoothed gradient norms",
     "SEC's weight is the constant BAYES_W (W's statements found: {W}); the norm ratio exists only in run()'s mode 'eq' (a comparison arm): {eqm}",
     lambda: not (all(has(f, l) for f, l in ING["W"][3][:1] + ING["W"][3][3:4]) and EQ_ONLY_IN_EQ_MODE)),
    ("A7/A8", ["What is future for a system can only be fed by what is already past for something.", "**[A8] No valence, no certainty.**"],
     "prohibitions (no operation to perform)",
     "window sums reset at every task start (found: {reset}): the calibration uses only the task's own settled steps, as every online learner does",
     lambda: False),
]


def clause_text_found(q):
    return ws(q) in ws(rd("theory/CRR.md"))


# ---------------------------------------------------------------- the sources, graded from the PINNED verify_a11.txt
def verified_ids():
    st = {}
    for line in open(os.path.join(HERE, "verify_a11.txt"), encoding="utf-8"):
        m = re.match(r"^(PASS|NOT FOUND|MISSING)\s+(a11:\d+)\s", line)
        if m:
            st.setdefault(m.group(2), []).append(m.group(1))
    ok = {c["id"] for c in CLAIMS if len(st.get(c["id"], [])) == len(c["quote"]) and all(s == "PASS" for s in st[c["id"]])}
    return ok, st


def grade(n):
    if n["states"] and n["contradicts"]:
        return "MIXED"
    if n["states"]:
        return "REDUNDANT"
    if n["close"]:
        return "PARTLY REDUNDANT"
    return "NOT FOUND"


# ---------------------------------------------------------------- m_checks.json (optional)
def _nk(k):
    return re.sub(r"[^a-z0-9]", "", str(k).lower())


def _match(d, arm):
    if not isinstance(d, dict):
        return None
    pref = {"C0": ("c0",), "M1": ("m1",), "M2": ("m2",), "M3": ("m3", "bayess1"), "M4": ("m4",)}[arm]
    for k in sorted(d, key=str):
        if any(_nk(k).startswith(p) for p in pref):
            return d[k]
    return None


def _nb(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, dict):
        for k in ("not_behind", "nb", "n_not_behind"):
            if isinstance(v.get(k), int) and not isinstance(v.get(k), bool):
                return v[k]
    return None


def _mean(v):
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v)
    if isinstance(v, dict) and isinstance(v.get("mean"), (int, float)):
        return float(v["mean"])
    if isinstance(v, list) and v and all(isinstance(x, (int, float)) for x in v):
        return float(np.mean(v))
    return None


def m_results(D):
    p = os.path.join(HERE, "m_checks.json")
    if not os.path.isfile(p):
        return None, "pending (m_checks.json not yet written)"
    J = json.load(open(p))
    p42 = J.get("pinned42") if isinstance(J.get("pinned42"), dict) else {}
    conts = [J.get(k) for k in ("not_behind", "arms", "counts", "summary")] + [p42.get("not_behind"), J]
    nb = {}
    for arm in ("C0", "M1", "M2", "M3", "M4"):
        for c in conts:
            v = _nb(_match(c, arm))
            if v is not None:
                nb[arm] = v; break
    ahead, how = None, None
    for k in ("m4_ahead_step", "m4_ahead_of_c0"):
        if isinstance(J.get(k), int) and not isinstance(J.get(k), bool):
            ahead, how = J[k], k; break
    if ahead is None:
        for c in conts:
            v = _match(c, "M4")
            if isinstance(v, dict) and isinstance(v.get("ahead_of_C0"), int):
                ahead, how = v["ahead_of_C0"], "M4.ahead_of_C0"; break
    if ahead is None:
        pc = J.get("per_carrier", J.get("carriers"))
        rows = list(pc.values()) if isinstance(pc, dict) else pc if isinstance(pc, list) else []
        vals = []
        for r in rows:
            if not isinstance(r, dict):
                continue
            key = (r.get("study"), r.get("carrier"))
            c0, m4 = _mean(_match(r, "C0")), _mean(_match(r, "M4"))
            if key in D and c0 is not None and m4 is not None:
                step = r["step"] if isinstance(r.get("step"), (int, float)) else D[key]["step"]
                vals.append((key, m4 - c0, step))
        if vals:
            ahead, how = sum(1 for _, d, s in vals if d > s), f"per_carrier ({len(vals)} carriers with C0 and M4 means)"
    n = J.get("n", J.get("n_carriers"))
    complete = J.get("complete", True) is not False
    why = "m_checks.json read" if complete else "m_checks.json read, but it says complete: false (the runs are not all in): NOT DECIDED"
    return dict(nb=nb, ahead=ahead if complete else None, how=how, n=n if isinstance(n, int) else None,
                n42=p42.get("n") if isinstance(p42.get("n"), int) else None, complete=complete), why


# ================================================================ output
def main():
    D = L.load_all(); CS = list(D.values()); BY = L.by_study(D)
    print(RULE)
    print("SEC_Analysis A11 (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f; prompt-log entry 257): forecast F11 -- is the explanation of SEC CRR, Bayes, optimisation or information geometry?")
    print("POST HOC on SEEN records; no ledger row; the words are HOLDS / FAILS / PENDING against the declared forecast, never PASS")
    print(RULE)

    # ---- the frozen code
    print("\n[1] THE FROZEN CODE (read as text, parsed with ast; never imported or run)")
    for fname in ("sec1_score.py", "sec4_score.py"):
        hs = {s: sha(f"runs/{s}/frozen/{fname}") for s in L.STUDIES if os.path.isfile(os.path.join(ROOT, f"runs/{s}/frozen/{fname}"))}
        print(f"   {fname}: frozen in {sorted(hs)}; distinct sha256 {len(set(hs.values()))}: {sorted(set(hs.values()))[0][:16]}...")
    print(f"   run() in {SEC1} (the SEC arms of all five studies: 'bayes_sec', 'bayes', 'bayes_s1', 'fixed', 'fixed_sec', 'eq'); run_guard() in {SEC4} (the clipped SEC of SEC4 and SEC5)")
    print(f"   constants: LR {LR}, BS {BS}, N_FISHER {N_FISHER}, BAYES_W {BAYES_W}, FS {FS}, FE {FE}, DTH_FLOOR {DTH_FLOOR}, KAPPA {KAPPA}")
    n_found = n_lines = 0
    for iid, name, home, lines in INGREDIENTS:
        f = [has(fn, l) for fn, l in lines]; n_found += sum(f); n_lines += len(f)
        print(f"   {iid}  {name}")
        for (fn, l), ok in zip(lines, f):
            print(f"        {'found' if ok else 'NOT FOUND':9} {fn:9} {l}")
        if not lines:
            print("        (a premise, not a statement of the code; its evidence is the recorded s_j below)")
    print(f"   code statements found verbatim: {n_found} of {n_lines}")

    print("\n[2] COMPUTED CODE FACTS")
    print(f"   per-step accumulators (AugAssign targets) in the training step loop: run {ACC['run']}; run_guard {ACC['run_guard']}")
    print(f"   -> the path enters the secant only through the START-window sums (s_th, s_g) and the END-window sums (e_th, e_g): {WINDOW_ONLY}")
    print(f"   -> c_j and rho_j are functions of dth = mean(END theta) - mean(START theta) and dg = mean(END g) - mean(START g): a CHORD between two window means;")
    print(f"      no per-step length is summed, so the secant is not D2's arc (nor D6's sum of sqrt(2 KL)); the metric in c_j is Euclidean, so it is not D3's Fisher-Rao chord either")
    print(f"   window share of a task's steps entering the secant: FS + FE = {FS + FE:.2f} (plus at most one step per window from the ceiling); the middle {1 - FS - FE:.2f} of the path is not read")
    print(f"   calls from run()/run_guard() into the CRR instrument ({CORE}: {len(CORE_FUNCS)} functions): run {CRR_CALLS['run']}, run_guard {CRR_CALLS['run_guard']}")
    print(f"   names sigma / mad / sig / unit in the code: run {SIGMA_NAMES['run']}, run_guard {SIGMA_NAMES['run_guard']}")
    units = len(re.findall(r"\bunits?\b", rd(SEC1)))
    print(f"   the word 'unit(s)' in {SEC1} (docstring, gate): {units} occurrences -- the calibration is NAMED a units correction; no CRR unit (A1') is computed")
    cap = KAPPA / (LR * BAYES_W); ar1_at_cap = LR * 2 * BAYES_W * cap; euler_edge = 2 / (LR * 2 * BAYES_W)
    print(f"   the clip: cap = KAPPA / (LR BAYES_W) = {cap:g}; SEC's penalty step is lr w g_q = lr 2 w imp dth, so AR1's 'eta lambda F' is lr 2 w imp;")
    print(f"      at the cap lr 2 w imp = {ar1_at_cap:.12g} (AR1's overshoot edge is 1: equal {abs(ar1_at_cap - 1) < 1e-12}); explicit-Euler divergence at imp = {euler_edge:g} (lr w imp = 1 = 2 KAPPA)")
    print(f"   the H-EQ norm ratio is in run() only under mode 'eq' (a comparison arm) and absent from run_guard: {EQ_ONLY_IN_EQ_MODE}")
    rng = np.random.default_rng(0); Sk = rng.standard_normal((5, 40)); Yk = rng.standard_normal((5, 40))
    c_arc = float((Sk * Yk).sum() / (Sk * Sk).sum()); c_ls = float(np.linalg.lstsq(Sk.reshape(-1, 1), Yk.reshape(-1), rcond=None)[0][0])
    print(f"   M4 (declared): c_arc = sum_k <dg_k, dth_k> / sum_k ||dth_k||^2 is the least-squares solution of BB's secant equation (1/eta) dth_k = dg_k")
    print(f"      stacked over the 5 segment pairs (seeded instance: formula {c_arc:.12f}, lstsq {c_ls:.12f}, equal to 1e-12: {abs(c_arc - c_ls) < 1e-12});")
    print("      it reads the path's intermediate window means, but sums SQUARED segment displacements, not segment lengths: not D2's arc either")

    # ---- CRR clauses
    print("\n[3] THE CRR-PROPER CLAUSES (CLAUDE.md sec. 7 list): the defining text found in theory/CRR.md, and whether SEC's code path performs the operation")
    fmt = dict(T=all(has(f, l) for f, l in ING["T"][3]), ph=[sorted({"antipodal_cuts", "intrinsic_phase"} & calls(f)) for f in FN],
               anc=has("run_guard", "theta_star = theta_now"), accu=has("run_guard", "imp_bayes = imp_bayes + n_task * s * f_task"),
               ex=sorted({"exp", "power"} & calls("run_guard")), crr=CRR_CALLS, sig=SIGMA_NAMES,
               R=all(has(f, l) for f, l in ING["R"][3]), reg=[sorted({"regularity", "cv"} & calls(f)) for f in FN],
               acc_r=ACC["run"], acc_g=ACC["run_guard"], wo=WINDOW_ONLY,
               arc=[sorted({"sqrt", "path_length", "arc_length", "kl_step"} & calls(f)) for f in FN],
               W=all(has(f, l) for f, l in ING["W"][3]), eqm=EQ_ONLY_IN_EQ_MODE,
               reset=all(has(f, "s_th = np.zeros(n); s_g = np.zeros(n); e_th = np.zeros(n); e_g = np.zeros(n); k_step = 0") for f in FN))
    crr_ops = {}
    for cid, quotes, op, test, impl in CLAUSES:
        found = [clause_text_found(q) for q in quotes]
        crr_ops[cid] = bool(impl())
        print(f"   {cid:8} text in CRR.md: {sum(found)}/{len(found)} found | operation: {op}")
        print(f"            code: {test.format(**fmt)}")
        extra = " (a prohibition: satisfied, as by every online learner; nothing to ablate)" if cid == "A7/A8" else ""
        print(f"            SEC's code path performs it: {'yes' if crr_ops[cid] else 'no'}{extra}")
    n_crr = sum(crr_ops.values())
    print(f"   CRR-proper operations in SEC's code path: {n_crr} of {len(CLAUSES)} clauses")

    # ---- sources
    ok, st = verified_ids()
    print("\n[4] THE SOURCES (claims_a11.py; a claim counts only if all its quotes are PASS in the pinned verify_a11.txt)")
    print(f"   claims {len(CLAIMS)}, quotes {sum(len(c['quote']) for c in CLAIMS)}; claims fully verified {len(ok)}; sources {len({c['url'] for c in CLAIMS})}")
    print("   rule: MIXED if states and contradicts; else REDUNDANT if states; else PARTLY REDUNDANT if close; else NOT FOUND (never read as novel)")
    G = {}
    for iid, name, home, lines in INGREDIENTS:
        cs = [c for c in CLAIMS if c["ingredient"] == iid and c["id"] in ok]
        n = Counter(c["role"] for c in cs); G[iid] = grade(n)
        print(f"   {iid}  {G[iid]:17} states {n['states']}, close {n['close']}, bears {n['bears']}, contradicts {n['contradicts']}")
        order = {"states": 0, "contradicts": 1, "close": 2, "bears": 3}
        for c in sorted(cs, key=lambda c: (order[c["role"]], int(c["id"].split(":")[1]))):
            print(f"        {c['role']:11} {c['id']:7} {c['source'][:92]} ({c['version'][:34]})")
    unver = [c["id"] for c in CLAIMS if c["id"] not in ok]
    print(f"   claims not counted (a quote not PASS or missing in verify_a11.txt): {unver or 'none'}")

    # ---- evidence from the records
    print("\n[5] LOAD-BEARING EVIDENCE FROM THE PINNED RECORDS (sec_lib; not behind = arm - tacc > -step, tacc and step at lambda*_raw)")

    def nbc(Cs, mode):
        return sum(L.arm_nb(C, mode) for C in Cs if mode in C["primary"])

    def line(label, Cs, full, abl):
        a, b = nbc(Cs, full), nbc(Cs, abl)
        lb = a - b >= 2
        both = [C for C in Cs if full in C["primary"] and abl in C["primary"]]
        gain = sum(1 for C in both if L.arm_nb(C, full) and not L.arm_nb(C, abl)); loss = sum(1 for C in both if L.arm_nb(C, abl) and not L.arm_nb(C, full))
        print(f"   {label}: {full} not behind {a}/{len(both)}, {abl} {b}/{len(both)} (difference {a - b:+d}; rescued {gain}, lost {loss}) -> {'LOAD-BEARING' if lb else 'not shown load-bearing'}")
        return lb

    ev = {}
    fam = "; ".join(f"{s} {nbc(BY[s], 'bayes_sec')}-{nbc(BY[s], 'bayes')}" for s in L.STUDIES)
    ev["S"] = line("S the calibration (ablation: raw Laplace 'bayes', s = 1), 42 carriers", CS, "bayes_sec", "bayes")
    print(f"        per study (SEC-raw): {fam}")
    ev["S1"] = line("S per-task factors (ablation: one factor, task 1's s, 'bayes_s1' = M3), 42 carriers", CS, "bayes_sec", "bayes_s1")
    cl = [C for C in CS if "bayes_sec_clip" in C["primary"]]
    ev["K"] = line("K the clip (ablation: the unclipped SEC), SEC4 + SEC5", cl, "bayes_sec_clip", "bayes_sec")
    dv_u = sum(L.arm_diverged(C, "bayes_sec") for C in cl); dv_c = sum(L.arm_diverged(C, "bayes_sec_clip") for C in cl)
    print(f"        diverged (a seed < {L.DIV_FRAC} tacc or non-finite): unclipped {dv_u}/{len(cl)}, clipped {dv_c}/{len(cl)}; clip fired on "
          f"{sum(L.guard_stats(C['primary']['bayes_sec_clip'])['fired'] > 0 for C in cl)}/{len(cl)} carriers")
    heq = nbc(CS, "eq"); sec = nbc(CS, "bayes_sec")
    print(f"   H-EQ (CRR-proper; run beside SEC in the same run(), mode 'eq', Omega = 1): not behind {heq}/42 against SEC's {sec}/42 "
          f"(SEC not behind where the rule is behind on {sum(1 for C in CS if L.arm_nb(C, 'bayes_sec') and not L.arm_nb(C, 'eq'))}, the reverse on "
          f"{sum(1 for C in CS if L.arm_nb(C, 'eq') and not L.arm_nb(C, 'bayes_sec'))})")
    print("        per study (SEC-rule): " + "; ".join(f"{s} {nbc(BY[s], 'bayes_sec')}-{nbc(BY[s], 'eq')}" for s in L.STUDIES)
          + " -- the rule is not an ingredient of SEC (its weight is the norm ratio, SEC's the constant 1/2)")
    loc = sum(1 for C in CS if C["primary"]["bayes_sec"].mean - C["tacc_sec"] > -C["step"])
    print(f"   W the value 1/2: SEC within a step of the best calibrated multiplier lambda*_sec (SEC - tacc_sec > -step; A1's location cost): {loc}/42")
    print("   N the task-size weights: no arm in the records removes them alone ('fixed_sec' drops n_j but tunes lambda): not tested")
    gm = [L.s_stats(C["primary"]["bayes_sec"])["gmean"] for C in CS]; md = [L.s_stats(C["primary"]["bayes_sec"])["median"] for C in CS]
    print(f"   E the premise (the EF understates the curvature at a task's end, so s_j > 1): carriers with geometric-mean s > 1: {sum(g > 1 for g in gm)}/42; "
          f"median over carriers of the per-carrier median s {float(np.median(md)):.4g} (min {min(md):.4g}, max {max(md):.4g})")

    # ---- mechanism checks
    print("\n[6] LOAD-BEARING EVIDENCE FROM THE MECHANISM CHECKS (m_checks.json: C0 clipped SEC, M1 true-Fisher Laplace, M2 endpoint curvature, M3 one factor, M4 arc secant)")
    M, why = m_results(D)
    if M is None:
        print(f"   {why}")
    else:
        print(f"   {why}; carriers {M['n'] if M['n'] is not None else 'not stated'}")
        for arm, lab in (("C0", "clipped SEC (reference)"), ("M1", "true-Fisher Laplace, uncalibrated (bears on F, S)"),
                         ("M2", "endpoint-curvature calibration (bears on C: path secant or local curvature)"),
                         ("M3", "one factor, bayes_s1 (bears on S)"), ("M4", "arc secant, the CRR-guided variant (bears on C, D6)")):
            v = M["nb"].get(arm)
            rel = "" if v is None or arm == "C0" or "C0" not in M["nb"] else f"; against C0 {v - M['nb']['C0']:+d}"
            if arm == "M3" and M["n42"] is not None and v is not None:
                rel = f" of {M['n42']} (the pinned records, not the {M['n']} carriers above)"
            print(f"   {arm} {lab}: not behind {v if v is not None else 'pending (not in m_checks.json)'}{rel}")
        miss = "NOT DECIDED (incomplete)" if not M["complete"] else "pending (not in m_checks.json)"
        print(f"   M4 ahead of C0 by more than the carrier's step: {M['ahead'] if M['ahead'] is not None else miss}"
              + (f" (from {M['how']})" if M["how"] else ""))

    # ---- the table
    nearest = {"W": "H-EQ (a weight rule)", "N": "A6 / P2-P3 (weights over occasions)", "F": "A1 (the metric: information geometry's)",
               "E": "A1' (named 'units')", "C": "D6 / D2 (arc)", "R": "D1 (letter rho only)", "S": "A1' (named 'units')",
               "K": "A6 ('bounded strength')", "T": "A3 / D5 (the cut)"}
    crr_of = {"W": "H-EQ", "N": "A6", "F": None, "E": "A1'/D1", "C": "D6/H-T1", "R": "A1'/D1", "S": "A1'/D1", "K": "A6", "T": "A3/D5"}
    mev = {"F": "M1", "S": "M1, M3", "C": "M2, M4"}
    print("\n[7] PER INGREDIENT")
    print(f"   {'id':2} {'home':36} {'stated':17} {'nearest CRR clause':38} {'CRR-proper':10} load-bearing evidence")
    for iid, name, home, lines in INGREDIENTS:
        proper = bool(crr_of[iid]) and crr_ops[crr_of[iid]]
        e = {"S": ("records: " + ("LOAD-BEARING" if ev["S"] else "not shown") + " (raw Laplace); per-task factors " + ("LOAD-BEARING" if ev["S1"] else "not shown") + " (bayes_s1)"),
             "K": "records: " + ("LOAD-BEARING" if ev["K"] else "not shown") + " (unclipped SEC)",
             "W": f"records: 1/2 within a step of lambda*_sec on {loc}/42", "E": f"records: s > 1 (geometric mean) on {sum(g > 1 for g in gm)}/42",
             "N": "not tested", "R": "enters only through S", "T": "fixed by the stream (not ablatable)"}.get(iid, "")
        if iid in mev:
            e = (e + "; " if e else "") + f"{mev[iid]}: " + ("pending" if M is None else "see [6]")
        print(f"   {iid:2} {home:36} {G[iid]:17} {nearest[iid]:38} {'yes' if proper else 'no':10} {e}")
    field = {"W": "Bayes", "N": "Bayes", "F": "information geometry", "E": "information geometry", "C": "optimisation",
             "R": "information geometry", "S": "optimisation + information geometry", "K": "optimisation", "T": "protocol"}
    homes = Counter(field[i[0]] for i in INGREDIENTS)
    n_prop = sum(1 for i in INGREDIENTS if crr_of[i[0]] and crr_ops[crr_of[i[0]]])
    print(f"   fields: {', '.join(f'{k} {v}' for k, v in sorted(homes.items()))}; CRR {n_prop}; CRR-proper ingredients: {n_prop} of {len(INGREDIENTS)}")

    # ---- F11
    print("\n[8] F11")
    parts = {
        "a": ("the weight 1/2 is the Laplace (Bayes) weight", G["W"] == "REDUNDANT" and BAYES_W == 0.5 and all(has(f, l) for f, l in ING["W"][3])),
        "b": ("the calibration is a Barzilai-Borwein secant fixing the empirical Fisher's known scale error",
              G["C"] == "REDUNDANT" and G["E"] == "REDUNDANT"),
        "c": ("the secant is a chord between window means, not CRR's arc", WINDOW_ONLY and not crr_ops["D6/H-T1"]),
        "d": ("the clip is AR1's", G["K"] == "REDUNDANT" and abs(ar1_at_cap - 1) < 1e-12),
        "e": ("A1' supplies a name ('units') for the correction", units > 0 and not crr_ops["A1'/D1"] and NO_CRR_CALLS),
    }
    for k, (txt, v) in parts.items():
        print(f"   ({k}) {txt}: {'holds' if v else 'FAILS'}")
    print(f"       (b) beside it: the calibration itself (S, rescaling a Fisher per task by the secant over the Fisher's claim) is {G['S']}")
    static = n_crr == 0
    if M is None or M["ahead"] is None:
        head, m4 = "PENDING", "pending"
    else:
        m4_lb = M["ahead"] >= 3
        m4 = f"{M['ahead']} carriers (>= 3: {m4_lb})"
        head = "HOLDS" if (static and not m4_lb) else "FAILS"
    print(f"   (f) rung R1 (inherited) at best: {'holds' if head == 'HOLDS' else 'pending' if head == 'PENDING' else 'FAILS'} (follows the headline)")
    print(f"   headline: static part, CRR-proper operations in SEC's code path: {n_crr} (so none of SEC's own ingredients is CRR-proper and load-bearing: {static});")
    print(f"             the CRR-guided variant M4 ahead of C0 by more than the carrier's step: {m4}")
    print(f"F11: {head}  (the declared computation: no CRR-proper ingredient is load-bearing; M4 counts as load-bearing iff ahead of the clipped SEC by more than a step on >= 3 carriers)")
    print(f"     parts (a)-(e) all hold: {all(v for _, v in parts.values())}")


if __name__ == "__main__":
    main()

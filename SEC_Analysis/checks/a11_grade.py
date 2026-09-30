"""SEC_Analysis A11 and forecast F11 (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f; prompt-log entry 257): is the
explanation of SEC CRR, Bayes, optimisation or information geometry?

POST HOC on SEEN records. No ledger row; no word here is a PASS. It reads, and never runs or imports:
  the frozen code    runs/sec4/frozen/sec1_score.py run() and runs/sec4/frozen/sec4_score.py run_guard(), as text parsed with
                     ast; sha256 of every frozen copy the five studies ran (runs/{sec1,scl3,sec3,sec4,sec5}/frozen)
  theory/CRR.md      the defining sentence of each CRR-proper clause (CLAUDE.md sec. 7: A3/D5, A6, P2/P3, A1'/D1, H-L5,
                     D6/H-T1, H-EQ, A7/A8), found verbatim (NFKC, whitespace collapsed); CLAUDE.md, Epistemic_Review/checks/
                     ladder.py, prereg/sec1/PREREG.md and notebook/PROMPT_LOG.md for the sentences parts (e) and (f) quote
  claims_a11.py      the published sources (fetched 2026-09-30, versions there) and verify_a11.txt, the PINNED verbatim check
                     (a claim counts only if every one of its quotes is PASS there; the raw texts are outside the repository;
                     the fetch record is SEC_Analysis/sources/FETCH_LOG.txt, SHA256SUMS.txt and fetch.py, copied from the
                     fetch root, and the raw-text hashes in verify_a11.txt are checked against that SHA256SUMS.txt)
  sec_lib.load_all() the pinned run records of the 42 carriers (validated first: loader_check.txt)
  m_checks.py        text only: run_m's M4 ('arc5') blocks, to read whether M4 sums a segment length (a REPORT; re-pin this
                     output whenever m_checks.py or m_checks.json changes)
  m_checks.json      the mechanism checks (checks/m_checks.py score), IF it exists; read ONLY in the layout m_checks.py writes
                     (complete, n_carriers, not_behind {C0, M1, M2, M4}, pinned42 {n, not_behind {bayes_sec, bayes_s1}},
                     m4_within_step, m4_ahead_step, forecasts, sec6); any other layout stops the script. M5 and M6
                     (Amendment 2) are read only if not_behind carries those exact keys. Nothing from it decides F11.

SEC's code path. The clause tests read the statements SEC executes, not the whole function: run() with mode 'bayes_sec' and
distort None (SEC of all five studies), run_guard() with variant 'clip' (the clipped SEC of SEC4 and SEC5). Every if-test
and conditional expression that these bindings decide (mode, distort, variant) is pruned from a copy of the ast, and the
pruned branches are printed with their line numbers. So run()'s distort branch (gate only; it calls exp) and its 'eq'
branch (the H-EQ comparison arm) are outside SEC's path, and so are run_guard()'s 'raw' and 'scale' variants.

Per ingredient of SEC's code (W the weight 1/2, N the task-size weighting and single accumulated penalty, F the per-sample
empirical Fisher, E the empirical Fisher's scale error (a premise, not code), C the secant c_j, R rho_j, S the calibration
s_j = c_j / rho_j with its fallback, K the clip, T the task boundary) it prints:
  code       each statement found verbatim in run() and/or run_guard() (whitespace collapsed), with its line number
  stated     MIXED if a verified claim 'states' it and one 'contradicts' it; else REDUNDANT if one 'states' it; else PARTLY
             REDUNDANT if one is 'close'; else NOT FOUND (never read as novel)
  CRR-proper yes iff SEC's code path performs the defining operation of a clause on the declared list (computed, [3]).
             The 'field' and 'nearest clause' columns are the agent's classification, not computed; F maps to no clause
             because CLAUDE.md sec. 7 gives the Fisher-Rao metric to information geometry (checked verbatim).
  evidence   REPORT lines (not declared; decide nothing): ablations from the pinned records; an ablation is marked
             LOAD-BEARING (report rule, not declared) when the arm without the ingredient is not behind on at least 2 fewer
             carriers than the arm with it (the declaration's baseline tolerance "at most 1 carrier fewer", read in reverse)

F11 (the declared forecast is a conjunction of sentences; each is computed, and F11 HOLDS iff all hold, else FAILS naming the
sentences that fail):
  headline  "No CRR-proper ingredient is load-bearing": the static code reading. 0 of the 7 operational clauses performed in
            SEC's code path decides it (an operation not performed cannot bear load); A7/A8 are prohibitions, with nothing to
            perform, and are not counted. If a clause were performed, the code reading could not decide load and the word
            would be NOT DECIDED (latent).
  (a)       W REDUNDANT, BAYES_W = 0.5 and W's statements found.
  (b)       OPERATIONALISATION (the declaration does not say how "fixing" is read): (b-i) c_j is BB's secant (C REDUNDANT, C's
            statements found); (b-ii) the EF's scale error is a published one (E REDUNDANT); (b-iii) the calibration rescales
            the EF by c_j / rho_j with rho_j the EF's Rayleigh quotient (S's and R's statements found, R REDUNDANT); (b-iv)
            it moves the EF the way that error needs (the EF understates the curvature, so s > 1) on most carriers
            (geometric-mean s > 1 on more than half, 'most' as in F4). S's own grade (the combination) is printed beside
            (b): (b) names the calibration's parts and does not claim the combination is published. The mechanism reading
            of "fixing" (SEC works because the EF's error is removed) is not A11's; M1 and M2 test it (FM1, FM2).
            (b-iv) counts carriers, so Amendment 1's report (floor-bound carriers removed) is printed with it.
  (c)       C's secant reads only START- and END-window sums (step-loop accumulators), dth and dg are differences of those
            means (statement found), and D6/H-T1 is not performed.
  (d)       K REDUNDANT and, from the frozen constants, lr 2 w cap = 1: AR1's bound eta lambda F <= 1 exactly.
  (e)       A1' is CRR's clause on the unit (its heading found in CRR.md); SEC's own documents name the correction with
            that word (prose occurrences in the frozen sec1_score.py, docstrings and comments only, quoted literals such
            as the distort kind 'unit' excluded, and the SEC1 pre-registration's "fixing the Fisher's units"; prompt-log
            entry 118's "corrects the units" is printed as context, not counted); and no CRR unit is computed (A1'/D1 not
            performed, no instrument call). The word match is the computable part; that the name came from A1' is
            provenance by citation (prompt-log 118, prereg/sec1/PREREG.md).
  (f)       The ladder's R2 needs "a CRR-proper ingredient changed the number" (ladder.py, checked verbatim). With 0
            CRR-proper operations in SEC's code path none can change SEC's number, so CRR's rung for the explanation of SEC
            is at most R1 (inherited). This is CRR's credit for the explanation; the method's ledger rows are not re-graded.
M4 (the arc secant) is not SEC's code and, as implemented, sums no segment length ([2]); it does not enter F11. It is
reported in [6] under its own declared forecast FM4 and the SEC6 carry rule, both decided in m_checks.txt.

    uv run python SEC_Analysis/checks/a11_grade.py > SEC_Analysis/checks/a11_grade.txt
"""
from __future__ import annotations

import ast
import copy
import hashlib
import io
import json
import math
import os
import re
import sys
import tokenize
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
BIND = {"run": {"mode": "bayes_sec", "distort": None}, "run_guard": {"variant": "clip"}}   # SEC's path in each function
CORE = "src/crr/instrument/core.py"
SOURCES = "SEC_Analysis/sources"
FLOOR_STEPS = 3.0                         # Amendment 1 (A12): floor-bound iff tacc - floor < 3 steps
RULE = "=" * 150


def rd(p):
    return open(os.path.join(ROOT, p), encoding="utf-8").read()


def sha(p):
    return hashlib.sha256(open(os.path.join(ROOT, p), "rb").read()).hexdigest()


def ws(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", s)).strip()


# ---------------------------------------------------------------- the frozen code, parsed
MOD = {p: ast.parse(rd(p)) for p in (SEC1, SEC4, CORE)}
LINES = {p: rd(p).splitlines() for p in (SEC1, SEC4)}
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


def lineno(fn, stmt):
    """First line (or span) of the frozen file, inside the function, whose text contains the statement; shortest span first."""
    p = FN[fn][0]; node = NODE[fn]; lines = LINES[p]; t = ws(stmt)
    for span in range(1, 4):
        for i in range(node.lineno - 1, node.end_lineno - span + 1):
            if t in ws(" ".join(lines[i:i + span])):
                return f"L{i + 1}" if span == 1 else f"L{i + 1}-{i + span}"
    return "L?"


# ---------------------------------------------------------------- SEC's code path: prune the branches the bindings decide
UNK = object()


def ev(n, b):
    """Tri-state value of an if-test under the bindings b: a Python value, or UNK when it depends on anything else."""
    if isinstance(n, ast.Constant):
        return n.value
    if isinstance(n, ast.Tuple):
        v = [ev(e, b) for e in n.elts]
        return UNK if any(x is UNK for x in v) else tuple(v)
    if isinstance(n, ast.Name):
        return b.get(n.id, UNK)
    if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not):
        v = ev(n.operand, b)
        return UNK if v is UNK else (not v)
    if isinstance(n, ast.Compare) and len(n.ops) == 1:
        a, c, op = ev(n.left, b), ev(n.comparators[0], b), n.ops[0]
        if a is UNK or c is UNK:
            return UNK
        if isinstance(op, ast.Eq):
            return a == c
        if isinstance(op, ast.NotEq):
            return a != c
        if isinstance(op, ast.In):
            return a in c
        if isinstance(op, ast.NotIn):
            return a not in c
        if isinstance(op, ast.Is):
            return a is c
        if isinstance(op, ast.IsNot):
            return a is not c
        return UNK
    if isinstance(n, ast.BoolOp):
        v = [ev(x, b) for x in n.values]
        if isinstance(n.op, ast.And):
            if any(x is not UNK and not x for x in v):
                return False
            return True if all(x is not UNK for x in v) else UNK
        if any(x is not UNK and x for x in v):
            return True
        return False if all(x is not UNK for x in v) else UNK
    return UNK


class Prune(ast.NodeTransformer):
    def __init__(self, b):
        self.b = b; self.log = []

    def visit_If(self, n):
        v = ev(n.test, self.b)
        if v is UNK:
            return self.generic_visit(n)
        drop = n.orelse if v else n.body
        if drop:
            self.log.append((n.lineno, ast.unparse(n.test), bool(v), "else" if v else "if", drop[0].lineno, max(getattr(d, "end_lineno", d.lineno) for d in drop)))
        out = []
        for st in (n.body if v else n.orelse):
            r = self.visit(st)
            out.extend(r if isinstance(r, list) else [] if r is None else [r])
        return out

    def visit_IfExp(self, n):
        v = ev(n.test, self.b)
        if v is UNK:
            return self.generic_visit(n)
        self.log.append((n.lineno, ast.unparse(n.test), bool(v), "conditional expression", n.lineno, n.lineno))
        return self.visit(n.body if v else n.orelse)


PATH, PRUNED = {}, {}
for fn in FN:
    pr = Prune(BIND[fn]); PATH[fn] = pr.visit(copy.deepcopy(NODE[fn])); PRUNED[fn] = pr.log


def calls_in(tree):
    out = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            f = n.func
            out.add(f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else "?")
    return out


def call_lines(tree, names):
    return sorted((n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id, n.lineno) for n in ast.walk(tree)
                  if isinstance(n, ast.Call) and isinstance(n.func, (ast.Name, ast.Attribute))
                  and (n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id) in names)


def assigned(tree, name):
    return sorted({ast.unparse(n.value) for n in ast.walk(tree) if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)})


def step_loop(tree):
    loops = [n for n in ast.walk(tree) if isinstance(n, ast.For) and ast.unparse(n.iter) == "range(0, len(perm), bs)"]
    assert len(loops) == 1, len(loops)
    return loops[0]


def accumulators(tree):
    return sorted({ast.unparse(n.target) for n in ast.walk(step_loop(tree)) if isinstance(n, ast.AugAssign)})


def accumulates(tree, name):
    return any(isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)
               and isinstance(n.value, ast.BinOp) and isinstance(n.value.op, ast.Add)
               and isinstance(n.value.left, ast.Name) and n.value.left.id == name for n in ast.walk(tree))


def var_pow(tree):
    return sorted(n.lineno for n in ast.walk(tree) if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Pow)
                  and not isinstance(n.right, ast.Constant))


CORE_FUNCS = sorted(n.name for n in MOD[CORE].body if isinstance(n, ast.FunctionDef))
LR = const(SEC1, "LR"); BAYES_W = const(SEC1, "BAYES_W"); FS = const(SEC1, "FS"); FE = const(SEC1, "FE")
DTH_FLOOR = const(SEC1, "DTH_FLOOR"); KAPPA = const(SEC4, "KAPPA"); N_FISHER = const(SEC1, "N_FISHER"); BS = const(SEC1, "BS")

# ---------------------------------------------------------------- the ingredients and their statements in the code
# field and nearest clause: the agent's classification (not computed); CRR-proper: computed in [3]
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
     "optimisation + information geometry", []),
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
     "optimisation + information geometry",
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


def found_all(iid):
    return all(has(f, ln) for f, ln in ING[iid][3])


# ---------------------------------------------------------------- computed code facts on SEC's path
ACC = {fn: accumulators(PATH[fn]) for fn in FN}
WINDOW_ONLY = all(ACC[fn] == ["e_g", "e_th", "k_step", "s_g", "s_th"] for fn in FN)
DIFF_OF_MEANS = all(has(fn, "dth = e_th / n_e - s_th / n_s; dg = e_g / n_e - s_g / n_s; nn = float(dth @ dth)") for fn in FN)
C_NAMES = {fn: sorted({x.id for a in ast.walk(PATH[fn]) if isinstance(a, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "c" for t in a.targets)
                       for x in ast.walk(a.value) if isinstance(x, ast.Name)}) for fn in FN}
NN_OF = {fn: assigned(PATH[fn], "nn") for fn in FN}
EUCLID = all("f_task" not in C_NAMES[fn] and NN_OF[fn] == ["float(dth @ dth)"] for fn in FN)
CRR_CALLS = {fn: sorted(calls_in(PATH[fn]) & set(CORE_FUNCS)) for fn in FN}
NO_CRR_CALLS = not any(CRR_CALLS.values())
SIGMA_NAMES = {fn: sorted({n.id for n in ast.walk(PATH[fn]) if isinstance(n, ast.Name)} & {"sigma", "mad", "sig", "unit"}) for fn in FN}
ANCHOR = {fn: assigned(PATH[fn], "theta_star") for fn in FN}
ANCHOR_LAST = all(set(ANCHOR[fn]) <= {"None", "theta_now"} for fn in FN)
ACCUM = {fn: accumulates(PATH[fn], "imp_bayes") for fn in FN}
EXP_PATH = {fn: call_lines(PATH[fn], {"exp", "power"}) for fn in FN}
EXP_FULL = {fn: call_lines(NODE[fn], {"exp", "power"}) for fn in FN}
POW_PATH = {fn: var_pow(PATH[fn]) for fn in FN}
W_OF = {fn: assigned(PATH[fn], "w") for fn in FN}
EQ_IF = [n for n in ast.walk(NODE["run"]) if isinstance(n, ast.If) and ast.unparse(n.test) == "mode == 'eq'"]
NORM_ALL = {id(n) for n in ast.walk(NODE["run"]) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "norm"}
NORM_EQ = {id(n) for e in EQ_IF for n in ast.walk(e) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "norm"}
NORM_PATH = {fn: sum(1 for n in ast.walk(PATH[fn]) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "norm") for fn in FN}
EQ_ONLY_IN_EQ_BRANCH = len(EQ_IF) == 1 and bool(NORM_ALL) and NORM_ALL == NORM_EQ and not any(NORM_PATH.values())
ARC_CALLS = {"sqrt", "path_length", "arc_length", "kl_step"}
RESET = "s_th = np.zeros(n); s_g = np.zeros(n); e_th = np.zeros(n); e_g = np.zeros(n); k_step = 0"


def reads_past(fn):
    """The window sums are reset before the step loop and read (dth) after it, inside the task loop."""
    rl = int(lineno(fn, RESET)[1:].split("-")[0]); dl = int(lineno(fn, "dth = e_th / n_e - s_th / n_s")[1:].split("-")[0])
    lp = step_loop(NODE[fn]); return rl < lp.lineno and lp.end_lineno < dl


READS_PAST = all(reads_past(fn) for fn in FN)

# CRR-proper operational clauses (CLAUDE.md sec. 7; A7/A8 are prohibitions and listed apart). Each: id, defining quotes in
# CRR.md, the operation, a printer of the computed facts, and 'performs' computed on SEC's path of both functions.
CLAUSES = [
    ("A3/D5", ["The cut fires when the phase has advanced half a turn from the last cut", "**[D5] Occasion.** The interval between consecutive cuts."],
     "a cut at the antipode of an intrinsic phase",
     lambda: [f"calls to antipodal_cuts / intrinsic_phase: run {sorted(calls_in(PATH['run']) & {'antipodal_cuts', 'intrinsic_phase'})}, "
              f"run_guard {sorted(calls_in(PATH['run_guard']) & {'antipodal_cuts', 'intrinsic_phase'})}",
              f"boundaries are the label schedule (T's statements found: {found_all('T')})"],
     lambda: any({"antipodal_cuts", "intrinsic_phase"} & calls_in(PATH[f]) for f in FN)),
    ("A6", ["The successor state is the Fisher–Rao Fréchet mean of past occasion contents", "regeneration returns a reweighted content, never an accumulated count"],
     "anchor = Fisher-Rao Frechet mean of past occasion contents under MaxEnt weights, strength bounded, never an accumulated count",
     lambda: [f"values assigned to the anchor theta_star: run {ANCHOR['run']}, run_guard {ANCHOR['run_guard']} (the last task end only: {ANCHOR_LAST})",
              f"importance accumulated over tasks (imp_bayes = imp_bayes + ...): run {ACCUM['run']}, run_guard {ACCUM['run_guard']}"],
     lambda: (not ANCHOR_LAST) and not any(ACCUM.values())),
    ("P2/P3", ["MaxEnt over occasions with ⟨S⟩ fixed gives the Gibbs form π_m ∝ exp(β S_m)", "MaxEnt with mean age fixed gives geometric weights"],
     "occasion weights exp(beta S_m) or q^k",
     lambda: [f"exp / power calls: run {EXP_PATH['run']}, run_guard {EXP_PATH['run_guard']}; powers with a non-constant exponent: "
              f"run {POW_PATH['run']}, run_guard {POW_PATH['run_guard']}",
              f"(the whole run(), outside SEC's path included: exp / power at {EXP_FULL['run']}, the gate-only distort branch)",
              f"task weights are n_task x s (data count x calibration): run {has('run', 'imp_bayes = imp_bayes + n_task * sc * f_task')}, "
              f"run_guard {has('run_guard', 'imp_bayes = imp_bayes + n_task * s * f_task')}"],
     lambda: any(EXP_PATH[f] or POW_PATH[f] for f in FN)),
    ("A1'/D1", ["take σ = 1.4826·MAD(residual) with no additive floor", "**[D1] Resolution.** ρ := (extent of one monotone half-turn) / σ"],
     "sigma = 1.4826 MAD of ONE occasion statistic; rho = half-turn extent / sigma, reported, never in a threshold",
     lambda: [f"calls into the CRR instrument ({CORE}, {len(CORE_FUNCS)} functions): run {CRR_CALLS['run']}, run_guard {CRR_CALLS['run_guard']}",
              f"names sigma / mad / sig / unit: run {SIGMA_NAMES['run']}, run_guard {SIGMA_NAMES['run_guard']}",
              f"the code's rho is the Fisher's Rayleigh quotient (R's statements found: {found_all('R')}), not D1's resolution"],
     lambda: not NO_CRR_CALLS or any(SIGMA_NAMES.values())),
    ("H-L5", ["CV( C_m ) < CV( Δt_m )"], "CV of arc against CV of clock between own events",
     lambda: [f"calls to regularity / cv: run {sorted(calls_in(PATH['run']) & {'regularity', 'cv'})}, run_guard {sorted(calls_in(PATH['run_guard']) & {'regularity', 'cv'})}"],
     lambda: any({"regularity", "cv"} & calls_in(PATH[f]) for f in FN)),
    ("D6/H-T1", ["C_new = Σ_t √( 2·KL_t )  on a new-task probe", "**[H-T1] Forgetting tracks the path, not the endpoint.**"],
     "an arc: a per-step length summed along the path (sum_t sqrt(2 KL_t))",
     lambda: [f"per-step accumulators in the step loop: run {ACC['run']}, run_guard {ACC['run_guard']} (only the START/END window sums: {WINDOW_ONLY})",
              f"calls to sqrt / path_length / arc_length / kl_step: run {sorted(calls_in(PATH['run']) & ARC_CALLS)}, run_guard {sorted(calls_in(PATH['run_guard']) & ARC_CALLS)}"],
     lambda: (not WINDOW_ONLY) or any(ARC_CALLS & calls_in(PATH[f]) for f in FN)),
    ("H-EQ", ["w = Ω · ‖ḡ_present‖_F / ‖ḡ_past‖_F,   Ω = 1"],
     "a weight set per step from the ratio of smoothed gradient norms",
     lambda: [f"values assigned to the weight w: run {W_OF['run']}, run_guard {W_OF['run_guard']}; norm calls: run {NORM_PATH['run']}, run_guard {NORM_PATH['run_guard']}",
              f"every norm call of run() lies inside its 'mode == \"eq\"' branch (a comparison arm, pruned from SEC's path): {EQ_ONLY_IN_EQ_BRANCH} "
              f"({len(NORM_EQ)} of {len(NORM_ALL)})"],
     lambda: any(NORM_PATH.values()) or any(set(W_OF[f]) - {"BAYES_W", "S.BAYES_W"} for f in FN)),
]
PROHIBITIONS = ("A7/A8", ["What is future for a system can only be fed by what is already past for something.", "**[A8] No valence, no certainty.**"])


def text_found(q, p="theory/CRR.md"):
    return ws(q) in ws(rd(p))


# ---------------------------------------------------------------- the sources, graded from the PINNED verify_a11.txt
def verified_ids():
    st, hs = {}, {}
    for line in open(os.path.join(HERE, "verify_a11.txt"), encoding="utf-8"):
        m = re.match(r"^(PASS|NOT FOUND|MISSING)\s+(a11:\d+)\s", line)
        if m:
            st.setdefault(m.group(2), []).append(m.group(1))
        h = re.match(r"^\s+([0-9a-f]{64})\s+(\S+)$", line)
        if h:
            hs[h.group(2)] = h.group(1)
    ok = {c["id"] for c in CLAIMS if len(st.get(c["id"], [])) == len(c["quote"]) and all(s == "PASS" for s in st[c["id"]])}
    return ok, st, hs


def sums_file():
    out = {}
    for line in open(os.path.join(ROOT, SOURCES, "SHA256SUMS.txt"), encoding="utf-8"):
        m = re.match(r"^([0-9a-f]{64})\s+(\S+)$", line.strip())
        if m:
            out[m.group(2)] = m.group(1)
    return out


def grade(n):
    if n["states"] and n["contradicts"]:
        return "MIXED"
    if n["states"]:
        return "REDUNDANT"
    if n["close"]:
        return "PARTLY REDUNDANT"
    return "NOT FOUND"


# ---------------------------------------------------------------- part (e): the word 'unit(s)' in the frozen scorer
def unit_words(p):
    """Occurrences of unit(s) in prose (docstrings and comments; a quoted 'unit' excluded) and as a string literal."""
    src = rd(p); lines = src.splitlines(); mod = MOD[p]
    spans = [(n.body[0].lineno, n.body[0].end_lineno) for n in [mod] + [x for x in ast.walk(mod) if isinstance(x, (ast.FunctionDef, ast.ClassDef))]
             if n.body and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant) and isinstance(n.body[0].value.value, str)]
    in_doc = lambda i: any(a <= i <= b for a, b in spans)  # noqa: E731
    rx_any = re.compile(r"\bunits?\b"); rx_prose = re.compile(r"(?<!['\"])\bunits?\b(?!['\"])")
    prose, lit = [], []
    for i, ln in enumerate(lines, 1):
        if in_doc(i):
            k = len(rx_prose.findall(ln)); prose += [i] * k; lit += [i] * (len(rx_any.findall(ln)) - k)
    strs = {tokenize.STRING, getattr(tokenize, "FSTRING_MIDDLE", -1)}
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.COMMENT:
            prose += [tok.start[0]] * len(rx_prose.findall(tok.string))
        elif tok.type in strs and not in_doc(tok.start[0]):
            lit += [tok.start[0]] * len(rx_any.findall(tok.string))
    return sorted(prose), sorted(lit)


def prompt_entry(num):
    t = rd("notebook/PROMPT_LOG.md"); m = re.search(rf"^## {num} — .*?(?=^## \d+ — |\Z)", t, re.S | re.M)
    return m.group(0) if m else ""


# ---------------------------------------------------------------- M4 as implemented (m_checks.py, text only)
def m4_arc_calls():
    p = os.path.join(HERE, "m_checks.py")
    if not os.path.isfile(p):
        return None
    mod = ast.parse(open(p, encoding="utf-8").read())
    fns = [n for n in ast.walk(mod) if isinstance(n, ast.FunctionDef) and n.name == "run_m"]
    if not fns:
        return None
    blocks = [n for n in ast.walk(fns[0]) if isinstance(n, ast.If) and ast.unparse(n.test) == "arc"]
    return sorted({c for b in blocks for c in calls_in(b)}), len(blocks)


# ---------------------------------------------------------------- m_checks.json (optional), in m_checks.py's own layout only
def m_results():
    p = os.path.join(HERE, "m_checks.json")
    if not os.path.isfile(p):
        return None
    J = json.load(open(p))
    need = ("complete", "n_carriers", "not_behind", "pinned42", "m4_within_step", "m4_ahead_step", "forecasts", "sec6")
    miss = [k for k in need if k not in J]
    isint = lambda v: isinstance(v, int) and not isinstance(v, bool)  # noqa: E731
    bad = miss or not isinstance(J["complete"], bool) or not all(isint(J[k]) for k in ("n_carriers", "m4_within_step", "m4_ahead_step")) \
        or not isinstance(J["not_behind"], dict) or not all(isint(J["not_behind"].get(a)) for a in ("C0", "M1", "M2", "M4")) \
        or not isinstance(J["pinned42"], dict) or not isint(J["pinned42"].get("n")) \
        or not all(isint(J["pinned42"].get("not_behind", {}).get(m)) for m in ("bayes_sec", "bayes_s1")) \
        or not isinstance(J["forecasts"], dict)
    if bad:
        raise ValueError(f"m_checks.json is not in the layout m_checks.py score writes (missing {miss}); nothing read")
    return J


def floor_of(C):                                          # Amendment 1: 100 x the majority class's share (as a4_a6.py)
    cc = C["class_counts"]
    assert sum(cc) == C["n"], (C["carrier"], sum(cc), C["n"])
    return 100.0 * max(cc) / sum(cc)


# ================================================================ output
def main():
    D = L.load_all(); CS = list(D.values()); BY = L.by_study(D); N = len(CS)
    print(RULE)
    print("SEC_Analysis A11 (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f; prompt-log entry 257): forecast F11 -- is the explanation of SEC CRR, Bayes, optimisation or information geometry?")
    print("POST HOC on SEEN records; no ledger row; the words are HOLDS / FAILS against the declared forecast, never PASS; lines marked REPORT are not declared and decide nothing")
    print(RULE)

    # ---- the frozen code
    print("\n[1] THE FROZEN CODE (read as text, parsed with ast; never imported or run)")
    for fname in ("sec1_score.py", "sec4_score.py"):
        hs = {s: sha(f"runs/{s}/frozen/{fname}") for s in L.STUDIES if os.path.isfile(os.path.join(ROOT, f"runs/{s}/frozen/{fname}"))}
        print(f"   {fname}: frozen in {sorted(hs)}; distinct sha256 {len(set(hs.values()))}: {sorted(set(hs.values()))[0][:16]}...")
    print(f"   run() in {SEC1}, lines {NODE['run'].lineno}-{NODE['run'].end_lineno} (the SEC arms of all five studies: 'bayes_sec', 'bayes', 'bayes_s1', 'fixed', 'fixed_sec', 'eq')")
    print(f"   run_guard() in {SEC4}, lines {NODE['run_guard'].lineno}-{NODE['run_guard'].end_lineno} (the clipped SEC of SEC4 and SEC5)")
    print(f"   constants: LR {LR}, BS {BS}, N_FISHER {N_FISHER}, BAYES_W {BAYES_W}, FS {FS}, FE {FE}, DTH_FLOOR {DTH_FLOOR}, KAPPA {KAPPA}")
    n_found = n_lines = 0
    for iid, name, home, lines in INGREDIENTS:
        f = [has(fn, ln) for fn, ln in lines]; n_found += sum(f); n_lines += len(f)
        print(f"   {iid}  {name}")
        for (fn, ln), ok in zip(lines, f):
            print(f"        {'found' if ok else 'NOT FOUND':9} {fn:9} {lineno(fn, ln) if ok else '':8} {ln}")
        if not lines:
            print("        (a premise, not a statement of the code; the recorded s_j bear on it, [5])")
    print(f"   code statements found verbatim: {n_found} of {n_lines}")
    print("   SEC's code path (the branches the bindings decide, pruned from a copy of the ast; the clause tests in [3] read what remains):")
    for fn in FN:
        print(f"     {fn}() with {', '.join(f'{k} = {v!r}' for k, v in BIND[fn].items())}:")
        for ln0, test, val, kind, a, b in PRUNED[fn]:
            what = (f"its {kind} arm, lines {a}-{b}" if a != b else f"its {kind} arm, line {a}") if kind != "conditional expression" \
                else f"the other arm of the conditional expression on line {a}"
            print(f"        L{ln0:<4} {test} -> {val}; pruned: {what}")

    print("\n[2] COMPUTED CODE FACTS (on SEC's code path)")
    print(f"   per-step accumulators (AugAssign targets) in the training step loop: run {ACC['run']}; run_guard {ACC['run_guard']}")
    print(f"   -> the path enters the secant only through the START-window sums (s_th, s_g) and the END-window sums (e_th, e_g): {WINDOW_ONLY}")
    print(f"   -> dth and dg are differences of the END- and START-window means (statement found in both): {DIFF_OF_MEANS}")
    if WINDOW_ONLY and DIFF_OF_MEANS:
        print("   -> so c_j and rho_j are functions of a CHORD between two window means; no per-step length is summed, so the secant is not D2's arc (nor D6's sum of sqrt(2 KL))")
    else:
        print("   -> the secant is NOT shown to be a chord between two window means")
    print(f"   names in c's expression: run {C_NAMES['run']}, run_guard {C_NAMES['run_guard']}; nn = {NN_OF['run']} / {NN_OF['run_guard']}")
    print(f"   -> the metric in c_j is Euclidean (no f_task in c, nn = dth @ dth): {EUCLID}" + ("; so it is not D3's Fisher-Rao chord either" if EUCLID else ""))
    sh = []
    for C in CS:
        ep, bs = C["header"]["epochs"], C["header"]["bs"]
        for ti, nt in enumerate(C["per_task_n"]):
            tot = ep * int(math.ceil(nt / bs)); ns = max(1, int(math.ceil(FS * tot))); ne = max(1, int(math.ceil(FE * tot)))
            sh.append(((ns + ne) / tot, f"{C['study']}:{C['carrier']} task index {ti}, {tot} steps, windows {ns} and {ne}"))
    shv = np.array([s for s, _ in sh]); top = max(sh, key=lambda x: x[0])
    print("   window share of a task's steps entering the secant, (n_s + n_e) / steps as the code computes them (n_s = max(1, ceil(FS steps)); epochs, bs and per-task n")
    print(f"      from each carrier's header): nominal FS + FE = {FS + FE:.2f}; over the {len(sh)} tasks of the {N} carriers median {float(np.median(shv)):.4f}, "
          f"above {FS + FE:.2f} on {int(np.sum(shv > FS + FE + 1e-12))}, max {top[0]:.4f} ({top[1]})")
    print(f"      the steps between the two windows, at least {1 - top[0]:.4f} of every task's path, are not read")
    print(f"   calls from SEC's path into the CRR instrument ({CORE}: {len(CORE_FUNCS)} functions): run {CRR_CALLS['run']}, run_guard {CRR_CALLS['run_guard']}")
    print(f"   names sigma / mad / sig / unit on SEC's path: run {SIGMA_NAMES['run']}, run_guard {SIGMA_NAMES['run_guard']}")
    cap = KAPPA / (LR * BAYES_W); ar1_at_cap = LR * 2 * BAYES_W * cap; euler_edge = 2 / (LR * 2 * BAYES_W)
    print(f"   the clip: cap = KAPPA / (LR BAYES_W) = {cap:g}; SEC's penalty step is lr w g_q = lr 2 w imp dth, so AR1's 'eta lambda F' is lr 2 w imp;")
    print(f"      at the cap lr 2 w imp = {ar1_at_cap:.12g} (AR1's overshoot edge is 1: equal {abs(ar1_at_cap - 1) < 1e-12}); explicit-Euler divergence at imp = {euler_edge:g} (lr w imp = 1 = 2 KAPPA)")
    print(f"      a capped coordinate's offset from the anchor is multiplied by 1 - lr 2 w cap = {1 - ar1_at_cap:.12g} per step: each step resets it to -lr g_p alone")
    print("      (AR1's edge met with equality; the 'freeze' of DECLARATION.md Amendment 2, tested by M5 and M6)")
    print(f"   the H-EQ norm ratio: every norm call of run() lies in its 'eq' branch, none on SEC's path of either function: {EQ_ONLY_IN_EQ_BRANCH}")
    rng = np.random.default_rng(0); Sk = rng.standard_normal((5, 40)); Yk = rng.standard_normal((5, 40))
    c_arc = float((Sk * Yk).sum() / (Sk * Sk).sum()); c_ls = float(np.linalg.lstsq(Sk.reshape(-1, 1), Yk.reshape(-1), rcond=None)[0][0])
    m4c = m4_arc_calls()
    print("   REPORT (M4 is not SEC's code and does not enter F11): the declared M4, c_arc = sum_k <dg_k, dth_k> / sum_k ||dth_k||^2, is the least-squares")
    print(f"      solution of BB's secant equation (1/eta) dth_k = dg_k stacked over the 5 segment pairs (seeded instance: formula {c_arc:.12f}, lstsq {c_ls:.12f}, "
          f"equal to 1e-12: {abs(c_arc - c_ls) < 1e-12})")
    if m4c is None:
        print("      m_checks.py run_m not found: M4's implementation not read")
    else:
        m4arc = sorted(set(m4c[0]) & (ARC_CALLS | {"norm"}))
        print(f"      as implemented (m_checks.py run_m as it stands, its {m4c[1]} 'if arc' blocks): calls to sqrt / norm / path_length / arc_length / kl_step: {m4arc}"
              + ("; it sums squared segment displacements and no segment length: not D2's arc either" if not m4arc else ""))

    # ---- CRR clauses
    print("\n[3] THE CRR-PROPER CLAUSES (CLAUDE.md sec. 7 list): the defining text found in theory/CRR.md, and whether SEC's code path performs the operation")
    crr_ops = {}
    for cid, quotes, op, facts, impl in CLAUSES:
        found = [text_found(q) for q in quotes]
        crr_ops[cid] = bool(impl())
        print(f"   {cid:8} text in CRR.md: {sum(found)}/{len(found)} found | operation: {op}")
        for x in facts():
            print(f"            {x}")
        print(f"            SEC's code path (run and run_guard) performs it: {'yes' if crr_ops[cid] else 'no'}")
    pid, pq = PROHIBITIONS
    print(f"   {pid:8} text in CRR.md: {sum(text_found(q) for q in pq)}/{len(pq)} found | prohibitions: nothing to perform, not counted among the operational clauses")
    print("            the code fact that bears on A7: the window sums reset before each task's step loop and are read after it, so the calibration reads only steps")
    print(f"            already taken (both functions: {READS_PAST})")
    n_crr = sum(crr_ops.values())
    print(f"   CRR-proper operations performed in SEC's code path: {n_crr} of {len(CLAUSES)} operational clauses (A7/A8 are prohibitions, listed apart)")

    # ---- sources
    ok, st, vh = verified_ids(); sums = sums_file()
    print("\n[4] THE SOURCES (claims_a11.py; a claim counts only if all its quotes are PASS in the pinned verify_a11.txt)")
    print(f"   claims {len(CLAIMS)}, quotes {sum(len(c['quote']) for c in CLAIMS)}; claims fully verified {len(ok)}; sources {len({c['url'] for c in CLAIMS})}")
    print(f"   fetch record: {SOURCES}/FETCH_LOG.txt, SHA256SUMS.txt, fetch.py; raw-text sha256 in verify_a11.txt equal to {SOURCES}/SHA256SUMS.txt: "
          f"{sum(sums.get(k) == v for k, v in vh.items())} of {len(vh)}")
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
    print("\n[5] REPORT (not declared; decides nothing): LOAD-BEARING EVIDENCE FROM THE PINNED RECORDS (sec_lib; not behind = arm - tacc > -step,")
    print("    tacc and step at lambda*_raw); 'LOAD-BEARING (report rule, not declared)' = the arm without the ingredient not behind on at least 2 fewer carriers")

    def nbc(Cs, mode):
        return sum(L.arm_nb(C, mode) for C in Cs if mode in C["primary"])

    def line(label, Cs, full, abl):
        both = [C for C in Cs if full in C["primary"] and abl in C["primary"]]
        a, b = nbc(both, full), nbc(both, abl); lb = a - b >= 2
        gain = sum(1 for C in both if L.arm_nb(C, full) and not L.arm_nb(C, abl)); loss = sum(1 for C in both if L.arm_nb(C, abl) and not L.arm_nb(C, full))
        print(f"   {label}: {full} not behind {a}/{len(both)}, {abl} {b}/{len(both)} (difference {a - b:+d}; rescued {gain}, lost {loss}) -> "
              f"{'LOAD-BEARING (report rule, not declared)' if lb else 'not shown load-bearing (report rule, not declared)'}")
        return lb

    ev = {}
    ev["S"] = line(f"S the calibration (ablation: raw Laplace 'bayes', s = 1), {N} carriers", CS, "bayes_sec", "bayes")
    print("        per study (SEC-raw): " + "; ".join(f"{s} {nbc(BY[s], 'bayes_sec')}-{nbc(BY[s], 'bayes')}" for s in L.STUDIES))
    ev["S1"] = line(f"S per-task factors (ablation: one factor, task 1's s, 'bayes_s1' = M3; FM3 decides in m_checks.txt), {N} carriers", CS, "bayes_sec", "bayes_s1")
    cl = [C for C in CS if "bayes_sec_clip" in C["primary"]]
    ev["K"] = line("K the clip (ablation: the unclipped SEC), SEC4 + SEC5", cl, "bayes_sec_clip", "bayes_sec")
    dv_u = sum(L.arm_diverged(C, "bayes_sec") for C in cl); dv_c = sum(L.arm_diverged(C, "bayes_sec_clip") for C in cl)
    print(f"        diverged (a seed < {L.DIV_FRAC} tacc or non-finite): unclipped {dv_u}/{len(cl)}, clipped {dv_c}/{len(cl)}; clip fired on "
          f"{sum(L.guard_stats(C['primary']['bayes_sec_clip'])['fired'] > 0 for C in cl)}/{len(cl)} carriers")
    heq = [C for C in CS if "eq" in C["primary"]]
    scored = lambda C: "bayes_sec_clip" if "bayes_sec_clip" in C["primary"] else "bayes_sec"  # noqa: E731
    print("   H-EQ, the CRR-proper equanimity rule (run()'s mode 'eq', Omega = 1; a comparison arm, not an ingredient of SEC: its weight is the norm ratio,")
    print(f"      SEC's the constant 1/2), not behind the tuned lambda, on the {len(heq)} carriers that carry it:")
    print(f"      against the unclipped SEC (bayes_sec): rule {nbc(heq, 'eq')}/{len(heq)}, SEC {nbc(heq, 'bayes_sec')}/{len(heq)} (SEC only "
          f"{sum(1 for C in heq if L.arm_nb(C, 'bayes_sec') and not L.arm_nb(C, 'eq'))}, rule only {sum(1 for C in heq if L.arm_nb(C, 'eq') and not L.arm_nb(C, 'bayes_sec'))})")
    print("        per study (SEC-rule): " + "; ".join(f"{s} {nbc(BY[s], 'bayes_sec')}-{nbc(BY[s], 'eq')}" for s in L.STUDIES))
    print(f"      against the SEC arm each study scored (bayes_sec_clip on SEC4 and SEC5, bayes_sec elsewhere): rule {nbc(heq, 'eq')}/{len(heq)}, "
          f"SEC {sum(L.arm_nb(C, scored(C)) for C in heq)}/{len(heq)}")
    hc = [C for C in heq if "bayes_sec_clip" in C["primary"]]
    print(f"      SEC4 + SEC5 alone: rule {nbc(hc, 'eq')}/{len(hc)}, clipped SEC {nbc(hc, 'bayes_sec_clip')}/{len(hc)}, unclipped SEC {nbc(hc, 'bayes_sec')}/{len(hc)}")
    loc = sum(1 for C in CS if C["primary"]["bayes_sec"].mean - C["tacc_sec"] > -C["step"])
    print(f"   W the value 1/2: SEC within a step of the best calibrated multiplier lambda*_sec (SEC - tacc_sec > -step; A1's location cost, F1 decides in a1_a3.txt): {loc}/{N}")
    print("   N the task-size weights: no arm in the records removes them alone ('fixed_sec' drops n_j but tunes lambda): not tested")
    gm = {k: L.s_stats(C["primary"]["bayes_sec"])["gmean"] for k, C in D.items()}; md = [L.s_stats(C["primary"]["bayes_sec"])["median"] for C in CS]
    n_up = sum(g > 1 for g in gm.values())
    print(f"   E the premise (the EF understates the curvature at a task's end, so s_j > 1): carriers with geometric-mean s > 1: {n_up}/{N}; "
          f"median over carriers of the per-carrier median s {float(np.median(md)):.4g} (min {min(md):.4g}, max {max(md):.4g})")
    print("      the direction does not single out the EF's error: a larger curvature on the task's early path than at its end (M2's question, FM2) or a")
    print("      diagonal-against-full curvature gap would also give s > 1; M1 (the true Fisher, the known fix for the EF, FM1) bears on it")

    # ---- mechanism checks
    print("\n[6] THE MECHANISM CHECKS (m_checks.json, m_checks.py's layout only: C0 clipped SEC, M1 true-Fisher Laplace, M2 endpoint curvature, M3 one factor,")
    print("    M4 arc secant, M5 FREEZE-TOP, M6 EDGE; their forecasts FM0-FM6 and the SEC6 carry rule are decided in m_checks.txt; nothing here decides F11)")
    J = m_results()
    if J is None:
        print("   pending (m_checks.json not yet written)")
    else:
        tag = "" if J["complete"] else " [m_checks.json: complete false: NOT DECIDED]"
        nbm, n_m = J["not_behind"], J["n_carriers"]
        print(f"   m_checks.json read; carriers {n_m}{tag}")
        for arm, lab in (("C0", "clipped SEC (reference)"), ("M1", "true-Fisher Laplace, uncalibrated (bears on F, S)"),
                         ("M2", "endpoint-curvature calibration (bears on C: path secant or local curvature)"), ("M4", "arc secant (bears on C)")):
            rel = "" if arm == "C0" else f"; against C0 {nbm[arm] - nbm['C0']:+d}"
            print(f"   {arm} {lab}: not behind {nbm[arm]}/{n_m}{rel}")
        p42 = J["pinned42"]
        print(f"   M3 one factor, bayes_s1 (bears on S): not behind {p42['not_behind']['bayes_s1']} of {p42['n']} (the pinned records), bayes_sec {p42['not_behind']['bayes_sec']}")
        for arm, lab in (("M5", "FREEZE-TOP"), ("M6", "EDGE, a must-fail control")):
            v = nbm.get(arm)
            fw = J["forecasts"].get("F" + arm)
            print(f"   {arm} {lab} (Amendment 2; bears on K): " + (f"not behind {v}/{n_m}" + (f" (F{arm}: {fw})" if fw else "")
                                                                   if isinstance(v, int) and not isinstance(v, bool) else "pending (not in m_checks.json)"))
        print(f"   REPORT beside F11: M4 within a step of C0 on {J['m4_within_step']}/{n_m} (FM4: {J['forecasts'].get('FM4', 'not in m_checks.json')}); ahead by more than")
        print(f"      a step on {J['m4_ahead_step']}/{n_m} (the SEC6 carry rule: {('may be carried' if J['sec6']['M4'] else 'not carried') if isinstance(J['sec6'], dict) else 'NOT DECIDED'})."
              " M4 is not SEC's code and performs no CRR-proper operation ([2]), so it cannot make one load-bearing")

    # ---- the table
    nearest = {"W": "H-EQ (a weight rule)", "N": "A6 / P2-P3 (weights over occasions)", "F": "none (the metric: information geometry's)",
               "E": "A1' (named 'units')", "C": "D6 / D2 (arc)", "R": "D1 (letter rho only)", "S": "A1' (named 'units')",
               "K": "A6 ('bounded strength')", "T": "A3 / D5 (the cut)"}
    crr_of = {"W": "H-EQ", "N": "A6", "F": None, "E": "A1'/D1", "C": "D6/H-T1", "R": "A1'/D1", "S": "A1'/D1", "K": "A6", "T": "A3/D5"}
    ig = text_found("the Fisher–Rao metric, arc, chord and surplus are information geometry's, not CRR's", "CLAUDE.md")
    mev = {"F": "M1", "S": "M1", "C": "M2, M4", "K": "M5, M6"}
    print("\n[7] PER INGREDIENT (field and nearest clause: the agent's classification, not computed; stated: [4]; CRR-proper: computed in [3])")
    print(f"   {'id':2} {'field (agent)':36} {'stated':17} {'nearest CRR clause (agent)':42} {'CRR-proper':10} evidence (REPORT)")
    for iid, name, home, lines in INGREDIENTS:
        proper = bool(crr_of[iid]) and crr_ops[crr_of[iid]]
        e = {"S": ("records: " + ("LOAD-BEARING" if ev["S"] else "not shown") + " (raw Laplace); per-task factors " + ("LOAD-BEARING" if ev["S1"] else "not shown") + " (bayes_s1)"),
             "K": "records: " + ("LOAD-BEARING" if ev["K"] else "not shown") + " (unclipped SEC)",
             "W": f"records: 1/2 within a step of lambda*_sec on {loc}/{N}", "E": f"records: s > 1 (geometric mean) on {n_up}/{N}",
             "N": "not tested", "R": "enters only through S", "T": "fixed by the stream (not ablatable)"}.get(iid, "")
        if iid in mev:
            e = (e + "; " if e else "") + f"{mev[iid]}: " + ("pending" if J is None else "see [6]")
        print(f"   {iid:2} {home:36} {G[iid]:17} {nearest[iid]:42} {'yes' if proper else 'no':10} {e}")
    print(f"   F maps to no clause: CLAUDE.md sec. 7 'the Fisher–Rao metric, arc, chord and surplus are information geometry's, not CRR's' found verbatim: {ig}")
    field = {"W": "Bayes", "N": "Bayes", "F": "information geometry", "E": "optimisation + information geometry", "C": "optimisation",
             "R": "information geometry", "S": "optimisation + information geometry", "K": "optimisation", "T": "protocol"}
    homes = Counter(field[i[0]] for i in INGREDIENTS)
    n_prop = sum(1 for i in INGREDIENTS if crr_of[i[0]] and crr_ops[crr_of[i[0]]])
    print(f"   fields, coarse (the agent's classification, not computed; each ingredient's stating sources are in [4]): {', '.join(f'{k} {v}' for k, v in sorted(homes.items()))}")
    print(f"   CRR-proper ingredients (computed): {n_prop} of {len(INGREDIENTS)} ({sum(1 for i in INGREDIENTS if i[3])} in the code, "
          f"{sum(1 for i in INGREDIENTS if not i[3])} premise)")

    # ---- F11
    print("\n[8] F11 (declared: 'No CRR-proper ingredient is load-bearing. The weight 1/2 is the Laplace (Bayes) weight. The calibration is a")
    print("    Barzilai-Borwein secant fixing the empirical Fisher's known scale error. The secant is a chord between window means, not CRR's arc.")
    print("    The clip is AR1's. A1' supplies a name (\"units\") for the correction. Rung R1 (inherited) at best.')")
    print("   rule: F11 HOLDS iff every sentence holds (the headline and parts (a)-(f)); otherwise FAILS, naming the sentences that fail")
    word = lambda b: "holds" if b else "FAILS"  # noqa: E731
    head = True if n_crr == 0 else None                  # a performed clause would need an ablation (latent)
    print(f"   headline  no CRR-proper ingredient is load-bearing: CRR-proper operations performed in SEC's code path {n_crr} of {len(CLAUSES)} ([3]);"
          + (" an operation not performed cannot bear load: holds" if n_crr == 0 else " performed operations need an ablation the code reading lacks: NOT DECIDED"))
    parts = {}
    pa = G["W"] == "REDUNDANT" and BAYES_W == 0.5 and found_all("W"); parts["a"] = pa
    print(f"   (a) the weight 1/2 is the Laplace (Bayes) weight: {word(pa)}  (W {G['W']}; BAYES_W {BAYES_W}; W's statements found {found_all('W')})")
    b1 = G["C"] == "REDUNDANT" and found_all("C"); b2 = G["E"] == "REDUNDANT"
    b3 = found_all("S") and found_all("R") and G["R"] == "REDUNDANT"; b4 = n_up > N / 2
    pb = b1 and b2 and b3 and b4; parts["b"] = pb
    print(f"   (b) the calibration is a Barzilai-Borwein secant fixing the empirical Fisher's known scale error: {word(pb)}")
    print(f"       (b-i)   c_j is BB's secant: C {G['C']}, C's statements found {found_all('C')}: {b1}")
    print(f"       (b-ii)  the EF's scale error is a published one: E {G['E']}: {b2}")
    print(f"       (b-iii) the calibration rescales the EF by c_j / rho_j, rho_j the EF's Rayleigh quotient: S's statements found {found_all('S')}, "
          f"R's {found_all('R')}, R {G['R']}: {b3}")
    print(f"       (b-iv)  it moves the EF the way that error needs (s > 1) on most carriers: geometric-mean s > 1 on {n_up}/{N}, more than half: {b4}")
    print("       OPERATIONALISATION (the declaration is ambiguous): 'fixing' is read as purpose and direction, which a code reading can decide; 'most' = more")
    print("         than half, as in F4. The mechanism reading (SEC works because the EF's error is removed) is not A11's: M1 and M2 test it (FM1, FM2 in m_checks.txt).")
    print(f"       beside (b), not part of it: S, the calibration as a combination, is {G['S']}: "
          + ("no verified source states it; (b) names its parts and does not claim the combination is published" if G["S"] != "REDUNDANT" else "a verified source states it"))
    FB = [k for k, C in D.items() if C["tacc"] - floor_of(C) < FLOOR_STEPS * C["step"]]
    rest = [k for k in D if k not in FB]
    print(f"       Amendment 1 report ((b-iv) counts carriers; post hoc in origin; decides nothing): floor-bound carriers (tacc - floor < {FLOOR_STEPS:g} steps,")
    print(f"         floor = 100 x the majority class's share) {len(FB)} of {N}; with them removed, geometric-mean s > 1 on {sum(gm[k] > 1 for k in rest)}/{len(rest)}, "
          f"more than half: {sum(gm[k] > 1 for k in rest) > len(rest) / 2}; the other sentences count no carriers")
    pc = WINDOW_ONLY and DIFF_OF_MEANS and not crr_ops["D6/H-T1"]; parts["c"] = pc
    print(f"   (c) the secant is a chord between window means, not CRR's arc: {word(pc)}  (window sums only {WINDOW_ONLY}; differences of window means {DIFF_OF_MEANS}; "
          f"D6/H-T1 performed {crr_ops['D6/H-T1']})")
    pd = G["K"] == "REDUNDANT" and found_all("K") and abs(ar1_at_cap - 1) < 1e-12; parts["d"] = pd
    print(f"   (d) the clip is AR1's: {word(pd)}  (K {G['K']}; K's statements found {found_all('K')}; lr 2 w cap = {ar1_at_cap:.12g}, AR1's bound 1)")
    prose, lit = unit_words(SEC1)
    a1h = text_found("**[A1′] The unit is the system's own resolvable step.**")
    pre = text_found("fixing the Fisher's units", "prereg/sec1/PREREG.md")
    p118 = ws("The Ω = 1 rule corrects the units at every step.") in ws(prompt_entry(118))
    e1 = a1h; e2 = pre and len(prose) > 0; e3 = (not crr_ops["A1'/D1"]) and NO_CRR_CALLS
    pe = e1 and e2 and e3; parts["e"] = pe
    print(f"   (e) A1' supplies a name ('units') for the correction: {word(pe)}")
    print(f"       A1' is CRR's clause on the unit: '**[A1′] The unit is the system's own resolvable step.**' found in CRR.md: {e1}")
    print(f"       SEC's documents name the correction with that word: prereg/sec1/PREREG.md 'fixing the Fisher's units' found {pre}; prose 'unit(s)' in {SEC1}")
    print(f"         (docstrings and comments, quoted literals excluded) {len(prose)} at lines {prose} (the distort kind 'unit' as a literal, not counted: {len(lit)} at {lit})")
    print(f"         -> named: {e2}  (context, not counted: prompt-log entry 118 'The Ω = 1 rule corrects the units at every step.' found {p118})")
    a1op = crr_ops["A1'/D1"]
    print(f"       no CRR unit is computed (A1'/D1 performed {a1op}; instrument calls none {NO_CRR_CALLS}): {e3}")
    lad = ws("a CRR-proper ingredient changed the number") in ws(rd("Epistemic_Review/checks/ladder.py"))
    pf = lad and n_crr == 0; parts["f"] = pf
    print(f"   (f) rung R1 (inherited) at best: {word(pf)}  (the ladder's R2 needs 'a CRR-proper ingredient changed the number', found in ladder.py {lad};")
    print(f"       CRR-proper operations in SEC's code path {n_crr}, so none can change SEC's number and CRR's rung for the explanation is at most R1;")
    print("       this is CRR's credit for the explanation of SEC, not a re-grading of the method's ledger rows)")
    fails = ([] if head else ["headline"]) + [k for k, v in parts.items() if not v]
    f11 = "NOT DECIDED" if head is None else ("HOLDS" if not fails else "FAILS")
    print(f"F11: {f11}" + (f"  (failing: {', '.join(fails)})" if fails and head is not None else "") + "  (M4 does not enter F11; see [6] and FM4 in m_checks.txt)")


if __name__ == "__main__":
    main()

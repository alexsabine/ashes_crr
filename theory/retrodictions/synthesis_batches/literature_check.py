"""The literature check of every ADDS row (prompt-log entry 132), under LITERATURE_CHECK_RULE.md (pushed in a5d9418 before
any finding was read). The findings come from three research reports (docs/citations/litcheck_{dynamics,social,
econ_evo_learn}_2026-09-24.md; sources fetched 2026-09-24, each marked full text / abstract / snippet). The pinned batch
outputs are not edited. Where a published formula exists, this script evaluates it at the row's parameters and compares
it with the row's pinned number (TOL_N); the class and the status after the check follow the rule's table.
Run: uv run python theory/retrodictions/synthesis_batches/literature_check.py > theory/retrodictions/synthesis_batches/literature_check.txt"""
import re
import sys
from pathlib import Path

import numpy as np

from crr.synthesis.harness import TOL_N, rel

HERE = Path(__file__).resolve().parent
STATUS = {"FOUND-EXACT": ("REDUNDANT-DOMAIN (literature)", "R2"), "FOUND-THEOREM": ("REDUNDANT-DOMAIN (literature, by theorem)", "R2"),
          "PARTIAL": ("ADDS, direction known", "R3, marked"), "NOT FOUND": ("ADDS, candidate", "R3, pending a named expert"),
          "ARTEFACT": ("not a candidate", "removed from R3")}


def pinned(fname, row, pattern):
    blk = [b for b in re.split(r"\n(?=\[\s*\d+\])", (HERE / fname).read_text()) if re.match(rf"\[\s*{row}\]", b)][0]
    return [float(v) for v in re.search(pattern, blk).groups()]


def main():
    rows = []
    # batch 12 row 2: cardiac alternans with memory
    q = (0.2, 0.4); s_row = pinned("batch_12.txt", 2, r"q = 0\.2: onset BCL = [\d.]+ ms \(A\* = [\d.]+, DI\* = [\d.]+\), slope at onset ([\d.]+).*?q = 0\.4: onset BCL = [\d.]+ ms \(A\* = [\d.]+, DI\* = [\d.]+\), slope at onset ([\d.]+)")
    s_lit = [(1 + qq) / (1 - qq) for qq in q]                                   # Tolkacheva: mu = 1 - (1 + 1/S_dyn) S12, S12 = s(1-q), S_dyn = s; mu = -1
    ok = all(rel(a, b) <= TOL_N for a, b in zip(s_row, s_lit))
    rows.append(("batch_12 row 2", "cardiac alternans with memory", "FOUND-EXACT" if ok else "PARTIAL",
                 "Tolkacheva, Schaeffer, Gauthier & Krassowska 2003, PRE 67:031904 (criterion |1 - (1 + 1/S_dyn) S12| >= 1, read in full text in arXiv:physics/0303099v1); the same linear structure is Nerlove's 1958 adaptive-expectations cobweb (batch 20 row 2, REDUNDANT-DOMAIN)",
                 f"threshold slope at q = 0.2, 0.4: row {s_row[0]:.4f}, {s_row[1]:.4f}; the published criterion {s_lit[0]:.4f}, {s_lit[1]:.4f}: {'agree' if ok else 'differ'}"))
    # batch 17 row 1: Bass with fading word of mouth
    rows.append(("batch_17 row 1", "Bass diffusion with fading word of mouth", "PARTIAL",
                 "Fibich 2016, PRE 94:032305 (arXiv:1605.03615) and 2017, SIAP (arXiv:1701.01669), both read in full: the identical Bass-SIR model (the infectious pool is the exponentially age-weighted adoptions, rate = kappa); published: diffusion slower, monotone in the rate",
                 "the lower and earlier peak and the bent Bass plot were not found in print (they follow in one line from Fibich's equations)"))
    # batch 28 row 4: switching contingency
    rows.append(("batch_28 row 4", "switching contingency: bounded mean against accumulated counts", "PARTIAL",
                 "Yu & Cohen 2008, NeurIPS 21 (full text): the same three models (accumulated Beta counts, the exact Bayesian filter for a changing rate, an exponential filter that 'track[s] the true Bayesian P_t very well'); the same ranking in Behrens et al. 2007, Wilson, Nassar & Gold 2013, discounted bandits (Garivier & Moulines; Raj & Kalyani), active inference (Smith et al. 2022, eq. 34, a forgetting rate on Dirichlet counts)",
                 "the ranking is published for the same models; the row's mean absolute errors are not (a qualitative Q with a published ranking reads PARTIAL under the rule as written: no published formula gives the row's numbers)"))
    # batch 30 row 2: CNS with lineage memory
    rows.append(("batch_30 row 2", "CNS with lineage-memory inheritance", "PARTIAL",
                 "Galton's ancestral law (Bulmer 1998, Heredity, doi:10.1046/j.1365-2540.1998.00418.x); cascading maternal effects (Kirkpatrick & Lande 1989, not read in full); Hoyle & Ezard 2012, J R Soc Interface (doi:10.1098/rsif.2012.0183; the same trade-off: effects that slow the response lower the variance and raise equilibrium fitness; not read in full); Altenberg 2013 (arXiv:1302.1293; faithful inheritance favoured)",
                 "the direction is published; the variance, load and halving time as functions of q were not found; an exact equivalent in the two unread papers cannot be ruled out"))
    # batch 31 row 1: Ricker
    r_row, = pinned("batch_31.txt", 1, r"r_c\(q = 0\.5\) = ([\d.]+)")
    qq = 0.5; r_lit = 2 * (1 + qq) / (1 - qq)                                   # AR(2) stability triangle: phi1 = 1 + q - r(1-q), phi2 = -q; flip boundary phi2 - phi1 = 1
    ok = rel(r_row, r_lit) <= TOL_N
    rows.append(("batch_31 row 1", "Ricker with remembered density", "FOUND-THEOREM" if ok else "PARTIAL",
                 "the stability triangle of a second-order linear recursion (Royama; Box & Jenkins): the linearised map is z_{n+1} = (1 + q - r(1-q)) z_n - q z_{n-1}; no paper with this exact model was found (Levin & May 1976 is a pure lag, a different kernel)",
                 f"first loss of stability: row {r_row:.3f}; the triangle's flip boundary {r_lit:.3f}: {'agree' if ok else 'differ'}"))
    # batch 31 row 2: SIR with remembered prevalence
    rows.append(("batch_31 row 2", "SIR with distancing on remembered prevalence", "PARTIAL",
                 "Ochab, Manfredi, Puszynski & d'Onofrio 2023, Nonlinear Dynamics 111:887 (doi:10.1007/s11071-022-07317-6, full text): the same structure (beta0/(1 + k M), exponentially fading memory including 10 days, a memoryless comparison): 'the larger the delay in the behavioral response, the larger the expected magnitude at the first peak' (from stochastic runs at other R0); Buonomo & Della Marca 2020; Weitz et al. 2020 PNAS",
                 "the direction is published for this model class (by simulation, not a theorem); the row's peaks (0.041501 against 0.031357) are not"))
    # batch 31 row 3: OV traffic
    v_row, = pinned("batch_31.txt", 3, r"remembered headway ([\d.]+)")
    a, tau = 1.0, 0.5; v_lit = a / (2 * (1 + a * tau))                         # discrete reaction delay tau (Chen, Liu, Ngoduy & Shi 2016, eq. 13; Orosz, Wilson & Krauskopf 2004)
    rows.append(("batch_31 row 3", "optimal-velocity traffic with remembered headway", "PARTIAL",
                 "Chen, Liu, Ngoduy & Shi 2016, Nonlinear Dynamics 85:2705 (eq. 13) and Orosz, Wilson & Krauskopf 2004, PRE (eq. 19): the threshold for a DISCRETE reaction delay tau, V'_c = a/(2(1 + a tau)); driver memory by distributed delays on another car-following model in Sipahi, Atay & Niculescu 2007, SIAP 68:738",
                 f"threshold: row {v_row:.4f}; the published discrete-delay formula at tau = T_m {v_lit:.4f} ({'within' if rel(v_row, v_lit) <= TOL_N else 'outside'} 1 %); that an exponential kernel of the same mean gives the same long-wave threshold is the research report's derivation, not a cited theorem, so the class stays PARTIAL"))
    # batch 31 row 4: Samuelson
    rows.append(("batch_31 row 4", "Samuelson multiplier-accelerator with permanent income", "PARTIAL",
                 "Biederman 1993, J Macroeconomics 15:249 (doi:10.1016/0164-0704(93)90027-J; abstract only, via a search snippet): permanent-income consumption makes the model more stable 'provided current measured income influences permanent income', and 'may actually be destabilizing' when only past incomes feed it; Kaskarelis & Varelas 1996 in the same direction",
                 "the direction is published; the closed form 1/((1-q)c) was not found in any text opened; the row's permanent income uses past incomes only (C_t = c P_{t-1}), the case Biederman flags, so the comparison with his result needs his full text"))
    # batch 32 row 2: FitzHugh-Nagumo H-CUT (forced)
    rows.append(("batch_32 row 2", "FitzHugh-Nagumo recovery event against the antipodal cut", "ARTEFACT",
                 "no literature needed: the post hoc surrogate with no dynamics reaches the declared threshold (AGENT_LOG 109); the analytic signal writes x = A cos(phi), so zero crossings sit a half-turn apart by construction",
                 "removed from the candidates whatever the literature says"))
    # batch 32 row 3: Lotka-Volterra with remembered prey
    re_row, im_row = pinned("batch_32.txt", 3, r"leading eigenvalue at T_m = 1: \+([\d.]+) \+([\d.]+)i")
    roots = np.roots([1.0, 1.0, 0.0, 0.5]); lead = roots[np.argmax(roots.real)]    # lambda^3 + lambda^2/T + 0 lambda + b d x* y*/T at T = 1: no lambda term
    hurwitz_unstable = True                                                      # Routh-Hurwitz: a cubic with a zero lambda coefficient cannot have all roots in the left half-plane
    ok = hurwitz_unstable and rel(re_row, float(lead.real)) <= TOL_N
    rows.append(("batch_32 row 3", "Lotka-Volterra with remembered prey", "FOUND-THEOREM" if ok else "PARTIAL",
                 "Ruan 2009, Math Model Nat Phenom 4:140 (full text): this model class, 'the delay will destabilize the otherwise stable equilibrium'; Cushing 1976/1977, MacDonald 1976/1978, Farkas 1984 on the weak kernel; the row's case (no prey self-limitation) follows from Routh-Hurwitz: the characteristic cubic has no lambda term",
                 f"leading root: row +{re_row:.5f} +{im_row:.5f}i; the characteristic cubic lambda^3 + lambda^2 + 0.5 = 0 gives {lead.real:+.5f} {abs(lead.imag):+.5f}i; Routh-Hurwitz forbids stability: {'agree' if ok else 'differ'}"))
    print("Literature check of every ADDS row (prompt-log entry 132; rule: LITERATURE_CHECK_RULE.md, pushed in a5d9418 before any finding)")
    print("classes: FOUND-EXACT and FOUND-THEOREM -> R2; PARTIAL -> R3 marked 'direction known'; NOT FOUND -> R3 candidate; ARTEFACT -> removed\n")
    for i, (rid, name, cls, cite, num) in enumerate(rows, 1):
        st, rung = STATUS[cls]
        print(f"[{i:2d}] {rid}: {name}")
        print(f"     finding:    {cls}")
        print(f"     sources:    {cite}")
        print(f"     numbers:    {num}")
        print(f"     STATUS:     {st} ({rung})\n")
    c = {k: sum(1 for r in rows if r[2] == k) for k in STATUS}
    print("TALLY: " + " / ".join(f"{v} {k}" for k, v in c.items()))
    print(f"after the check: {c['FOUND-EXACT'] + c['FOUND-THEOREM']} of {len(rows)} ADDS rows are REDUNDANT-DOMAIN by the literature, {c['PARTIAL']} keep R3 with the direction known, "
          f"{c['NOT FOUND']} keep R3 as clean candidates, {c['ARTEFACT']} removed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

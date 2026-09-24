"""RLAW gate (R4; Regeneration_Law/DECLARATION_2.md). The frozen scorer's measure() and verdicts() are run on synthetic
domains with the real domains' unit counts, lengths and reporting quanta. The synthetic systems are:
- G+: the law holds;
- G-over: over-reacts;
- G-under: sluggish;
- G-free: memory independent of the drift;
- G-LTI: one fixed memory per domain.

Admissibility is computed, never typed (R15):
- a row is admissible if G+ passes it in at least 0.8 of replicates and every must-fail surrogate passes it in at most 0.05;
- a row that is not admissible is reported without a verdict.
No real data.

    uv run python studies/rlaw/gate_rlaw.py > prereg/rlaw/gate_RLAW.txt"""
import math
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rlaw_score as S  # noqa: E402
from rlaw_lib import K, rate_table, table_rate  # noqa: E402

V_LO, V_HI = 0.03, 3.0          # a priori drift range per unit (log-uniform), the same for every domain
REPORT_NOISE, OFFSET = 0.05, 0.5  # in units of s_eps
R_MAIN, R_TWOSTEP = 40, 10
POWER, SIZE = 0.8, 0.05
SPEC = {  # domain: (unit lengths, delta / s_eps)
    "spf": ([232, 232, 181, 139, 181, 79, 79, 79], 0.3),
    "mich": ([185, 185, 185], 3.0),
    "ivol": ([2500, 6400, 4800, 4300, 2500], 0.01),
    "soil5": ([365] * 150, 0.05),
    "soil_deep": ([365] * 400, 0.05),
}
SURR = ("G+", "G-over", "G-under", "G-free", "G-LTI")


def alpha_for(kind, kstar, rng, k_lti):
    if kind == "G+": return kstar
    if kind == "G-over": return min(0.95, 3 * kstar)
    if kind == "G-under": return kstar / 3
    if kind == "G-free": return float(math.exp(rng.uniform(math.log(0.02), math.log(0.9))))
    return k_lti


def synth_domain(dom, kind, rng):
    lens, dr = SPEC[dom]; vs = np.exp(rng.uniform(math.log(V_LO), math.log(V_HI), size=len(lens)))
    ks = [float(K(v / math.sqrt(1 + dr * dr / 12))) for v in vs]; k_lti = float(np.median(ks)); units = []
    for i, (n, v, ks_i) in enumerate(zip(lens, vs, ks)):
        a = alpha_for(kind, ks_i, rng, k_lti)
        x = np.cumsum(v * rng.normal(size=n)) + rng.normal(size=n)
        s = np.empty(n); s[0] = x[0]
        for t in range(1, n): s[t] = s[t - 1] + a * (x[t] - s[t - 1])
        s = s + OFFSET + REPORT_NOISE * rng.normal(size=n)
        units.append(dict(domain=dom, id=f"u{i}", s=s, x=x, delta=dr))
    return units


def synth_twostep(kind, rng, table, n_sub=200, trials=125, beta=5.0):
    k0 = table_rate(3.0, table); subs = []
    for i in range(n_sub):
        a = alpha_for(kind, k0, rng, k0)
        p = rng.uniform(0.25, 0.75, size=4); Q = np.zeros((2, 2)); st, ch, wn, ps = [], [], [], []
        for t in range(trials):
            s = int(rng.uniform() < 0.5); d = Q[s, 1] - Q[s, 0]; c = int(rng.uniform() < 1 / (1 + math.exp(-beta * d)))
            ps.append(p.copy()); w = float(rng.uniform() < p[2 * s + c]); Q[s, c] += a * (w - Q[s, c]); st.append(s); ch.append(c); wn.append(w)
            p = p + 0.025 * rng.normal(size=4); p = np.where(p > 0.75, 1.5 - p, p); p = np.where(p < 0.25, 0.5 - p, p)
        subs.append(dict(domain="twostep", id=f"s{i}", sub=dict(id=f"s{i}", state2=np.array(st), choice2=np.array(ch), win=np.array(wn),
                                                                  valid=np.ones(trials, bool), ps=np.array(ps), n=trials)))
    return subs


def main():
    print("RLAW gate (R4): the frozen scorer on synthetic domains (Regeneration_Law/DECLARATION_2.md)")
    print(f"per unit: v log-uniform on [{V_LO}, {V_HI}]; report noise {REPORT_NOISE} and offset {OFFSET} (s_eps units); primary cell {S.cell_name(S.PRIMARY)}")
    print(f"admissible: G+ pass rate >= {POWER} and every must-fail surrogate <= {SIZE}; must-fail for a domain row (level AND beats the constant): "
          "G-over, G-under, G-free, G-LTI; for a tracking row: G-free, G-LTI")
    table = rate_table(); verdict_log = {}; admissible = {}
    for dom, tracking in (("spf", False), ("mich", False), ("ivol", False), ("soil5", True), ("soil_deep", True), ("twostep", False)):
        R = R_TWOSTEP if dom == "twostep" else R_MAIN; rates = {}
        for j, kind in enumerate(SURR):
            if dom == "twostep" and kind == "G-LTI": continue
            rng = np.random.default_rng(5000 + 97 * j + sum(map(ord, dom)))
            outs = []
            for _ in range(R):
                units = synth_twostep(kind, rng, table) if dom == "twostep" else synth_domain(dom, kind, rng)
                outs.append(S.verdicts(S.measure(units, S.PRIMARY, table), dom, tracking))
            verdict_log.setdefault(dom, {})[kind] = outs
            rates[kind] = {k: float(np.mean([o[k] == "PASS" for o in outs])) for k in (["row", "level", "baseline"] + (["tracking"] if tracking else []))}
            rates[kind]["within_x2"] = float(np.mean([o["within_x2"] / max(o["n_units"], 1) for o in outs]))
        print(f"\n== {S.ROW[dom]} ({dom}; {R} replicates)")
        for kind, r in rates.items():
            print(f"   {kind}: mean fraction within x2 {r['within_x2']:.3f}; pass rates " + ", ".join(f"{k} {v:.3f}" for k, v in r.items() if k != "within_x2"))
        for row in ["row"] + (["tracking"] if tracking else []):
            # the domain row (level AND beats the constant) must fail on every surrogate that is not the law; tracking tests
            # only that memory moves with drift, so its must-fail surrogates are the two that cut that link (G-free, G-LTI)
            must_fail = [f for f in (("G-over", "G-under", "G-free", "G-LTI") if row == "row" else ("G-free", "G-LTI")) if f in rates]
            bad = [f for f in must_fail if rates[f][row] > SIZE]; power = rates["G+"][row]
            adm = power >= POWER and not bad; name = S.ROW[dom] + ("T" if row == "tracking" else "")
            admissible[name] = adm
            print(f"   {name} ({'level AND beats constant' if row == 'row' and dom != 'twostep' else row if row == 'tracking' else 'level'}): G+ {power:.3f}; "
                  f"must-fail ({', '.join(must_fail)}) passing above {SIZE}: {', '.join(f'{f} {rates[f][row]:.3f}' for f in bad) or 'none'} -> "
                  f"{'ADMISSIBLE' if adm else 'NOT ADMISSIBLE (reported without a verdict)'}")
    print("\n== composites (replicate r of every domain taken together; the first 10 replicates)")
    comp = {}
    for kind in ("G+", "G-over", "G-under", "G-free", "G-LTI"):
        u, c = [], []
        for r in range(R_TWOSTEP):
            doms = [d for d in ("spf", "mich", "ivol", "soil5", "twostep") if kind in verdict_log[d]]
            lv = [verdict_log[d][kind][r]["row"] for d in doms]; u.append(sum(v == "PASS" for v in lv) >= 4)
            s5 = verdict_log["soil5"][kind][r]; c.append(s5["row"] == "PASS" and s5["tracking"] == "PASS")
        comp[kind] = (float(np.mean(u)), float(np.mean(c)))
        print(f"   {kind}: RLAW-U pass rate {comp[kind][0]:.3f}; RLAW-C pass rate {comp[kind][1]:.3f}")
    c5 = verdict_log["soil5"]; rc = {k: float(np.mean([o["row"] == "PASS" and o["tracking"] == "PASS" for o in c5[k]])) for k in c5}
    print("   RLAW-C over all soil5 replicates: " + ", ".join(f"{k} {v:.3f}" for k, v in rc.items()))
    for name, pw, fails in (("RLAW-U", comp["G+"][0], {k: comp[k][0] for k in ("G-over", "G-under", "G-free", "G-LTI")}),
                            ("RLAW-C", rc["G+"], {k: rc[k] for k in ("G-over", "G-under", "G-free", "G-LTI")})):
        bad = [f"{k} {v:.3f}" for k, v in fails.items() if v > SIZE]; adm = pw >= POWER and not bad; admissible[name] = adm
        print(f"   {name}: G+ {pw:.3f}; must-fail passing above {SIZE}: {', '.join(bad) or 'none'} -> {'ADMISSIBLE' if adm else 'NOT ADMISSIBLE (reported without a verdict)'}")
    print("\nsummary: admissible rows " + ", ".join(k for k, v in admissible.items() if v) + "; reported without a verdict " +
          (", ".join(k for k, v in admissible.items() if not v) or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""RRM2 T7 (DECLARATION_3.md, POST HOC, pushed before this runs): the drift-rich regime. SEC1's MLP with E epochs per task,
E in {3, 15, 30}; report-only (no gate). Per E: relative drift of old-class means; drift explained by RRM and HOPDC; NCM
accuracy (ANCH1 learner) with STALE, RRM, HOPDC, ORACLE; learner accuracy of STALE-1, RRM-1, HOPDC-1, ER-20. The four
declared forecasts are scored held / not held by the script. Modes: 'synth' (POS, NEG2; t7_drift.txt), 'seen' (the 30 SEEN
carriers; t7_seen.txt). Seeds 0-4. Run: uv run python Relational_Reference_Memory/checks/t7_drift.py synth|seen
"""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "Replay_Quality_Memory" / "checks"))
import rrm_lib as L  # noqa: E402
import t_lib as T  # noqa: E402

SEEDS = (0, 1, 2, 3, 4)
ES = (3, 15, 30)


def step_of(v): return max(1.0, 2 * float(np.std(v, ddof=1)) / math.sqrt(len(v)))


def diag(seed, data, K, learner):
    Xtr, ytr, Xte, yte = data
    net, anchors, rec, cuts = T.train(seed, *data, K, learner)
    P = {w: T.prototypes(net, Xtr, ytr, anchors, rec, cuts, seed, w) for w in ("ORACLE", "STALE", "RRM", "HOPDC")}
    old = [c for c, (mu, j) in rec.items() if j < len(cuts) - 1]
    rel = float(np.mean([np.linalg.norm(P["STALE"][c] - P["ORACLE"][c]) / max(np.linalg.norm(P["ORACLE"][c]), 1e-12) for c in old]))
    err = {w: float(np.mean([np.linalg.norm(P[w][c] - P["ORACLE"][c]) for c in old])) for w in ("STALE", "RRM", "HOPDC")}
    ncm = {w: T.ncm_acc(net, Xte, yte, P[w]) for w in P}
    return rel, err, ncm, 100 * net.acc(Xte, yte)


def run_E(E, data, K, learners=True):
    L.EPOCHS = E
    out = {}
    for lr in ("FT", "ANCH1", "ER20"):
        out[lr] = [diag(s, data, K, lr) for s in SEEDS]
    if learners:
        out["arms"] = {k: [L.run_rrm(s, *data, K, "1", m) for s in SEEDS] for k, m in (("STALE-1", "stale"), ("RRM-1", "rrm"), ("HOPDC-1", "hopdc"))}
        out["arms"]["ER-20"] = [r[3] for r in out["ER20"]]
    L.EPOCHS = 3
    return out


def summarise(out):
    s = {}
    for lr in ("FT", "ANCH1", "ER20"):
        rows = out[lr]; es = np.mean([r[1]["STALE"] for r in rows])
        s[lr] = dict(rel=float(np.mean([r[0] for r in rows])), exR=1 - np.mean([r[1]["RRM"] for r in rows]) / es,
                     exH=1 - np.mean([r[1]["HOPDC"] for r in rows]) / es)
    a = out["ANCH1"]
    s["ncm"] = {w: [r[2][w] for r in a] for w in ("ORACLE", "STALE", "RRM", "HOPDC")}
    s["arms"] = out.get("arms")
    return s


def print_block(name, S):
    for E, s in S.items():
        print(f"  [{name} E {E}]")
        for lr in ("FT", "ANCH1", "ER20"):
            print(f"     {lr:5} relative drift {s[lr]['rel']:.4f}; drift explained RRM {s[lr]['exR']:+.4f}, HOPDC {s[lr]['exH']:+.4f}")
        print("     NCM (ANCH1) " + "  ".join(f"{w} {np.mean(v):6.2f}" for w, v in s["ncm"].items()))
        if s["arms"]:
            print("     learners    " + "  ".join(f"{k} {np.mean(v):6.2f}" for k, v in s["arms"].items()))


def main(mode):
    if mode == "synth":
        import phase_a as PA
        print("RRM2 T7 drift-rich regime (DECLARATION_3.md, POST HOC, report only); E epochs per task in {3, 15, 30}; seeds 0-4")
        R = {}
        for name in ("POS", "NEG2"):
            data, K = PA.stream(name); R[name] = {E: summarise(run_E(E, data, K)) for E in ES}; print_block(name, R[name])
        print("\nforecasts (DECLARATION_3.md), scored:")
        P = R["POS"]
        f1 = P[3]["FT"]["rel"] < P[15]["FT"]["rel"] < P[30]["FT"]["rel"]
        print(f"F1 relative drift rises with E on POS (FT learner): {P[3]['FT']['rel']:.4f} {P[15]['FT']['rel']:.4f} {P[30]['FT']['rel']:.4f} -> {'held' if f1 else 'not held'} (SEEN half in t7_seen.txt)")
        f2 = all(R[n][E][lr]["exR"] > R[n][E][lr]["exH"] for n in R for E in ES for lr in ("FT", "ANCH1", "ER20"))
        print(f"F2 RRM explains more drift than HOPDC in every cell (POS, NEG2; 3 learners; 3 E) -> {'held' if f2 else 'not held'}")
        d = {E: np.mean(P[E]["arms"]["RRM-1"]) - np.mean(P[E]["arms"]["STALE-1"]) for E in ES}
        st = step_of(P[15]["arms"]["STALE-1"])
        f3 = d[3] < d[15] < d[30] and abs(d[15]) <= st
        print(f"F3 RRM-1 - STALE-1 on POS by E: {d[3]:+.4f} {d[15]:+.4f} {d[30]:+.4f}; rises and |E15| <= step {st:.4f} -> {'held' if f3 else 'not held'}")
        n = P[30]["ncm"]; st = step_of(n["STALE"]); d4 = np.mean(n["RRM"]) - np.mean(n["STALE"])
        print(f"F4 NCM-RRM - NCM-STALE on POS at E 30 {d4:+.4f} (step {st:.4f}) -> {'held' if d4 > st else 'not held'}")
    else:
        print("RRM2 T7 on the 30 SEEN carriers (DECLARATION_3.md, POST HOC, report only); E in {3, 15, 30}; seeds 0-4; diagnostics only")
        rows = []
        for study, did in T.seen_carriers():
            d = T.load_seen_cached(study, did)
            if d is None:
                continue
            Xtr, ytr, Xte, yte, K, name = d; S = {E: summarise(run_E(E, (Xtr, ytr, Xte, yte), K, learners=False)) for E in ES}
            print_block(name, S); rows.append((name, S))
        up = sum(S[3]["FT"]["rel"] < S[15]["FT"]["rel"] < S[30]["FT"]["rel"] for _, S in rows)
        print(f"\nF1 (SEEN half) relative drift rises with E (FT learner) on {up}/{len(rows)} carriers (forecast: >= two thirds) -> "
              f"{'held' if up >= math.ceil(2 * len(rows) / 3) else 'not held'}")
        for E in ES:
            gt = sum(S[E]["ANCH1"]["exR"] > S[E]["ANCH1"]["exH"] for _, S in rows)
            dn = [np.mean(S[E]["ncm"]["RRM"]) - np.mean(S[E]["ncm"]["STALE"]) for _, S in rows]
            print(f"E {E}: ANCH1 RRM explains more drift than HOPDC on {gt}/{len(rows)}; NCM RRM - STALE > 0 on {sum(x > 0 for x in dn)}, "
                  f"< 0 on {sum(x < 0 for x in dn)}, median {np.median(dn):+.4f}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "synth")

"""RRM2 T1 DIAG (DECLARATION_2.md Part T, pushed at a2719f0 before this file): does transport by the 20 first-task anchors
track the real learner's feature drift? SEC1's MLP trained as FT, ANCH1 and ER20 (t_lib.train). At the end, for each class of
the first four tasks: prototype error |p - mu_now| for p = STALE, RRM (beta 0.01) and DECOY (permuted anchors); drift
explained 1 - err_RRM / err_STALE (seed means); NCM accuracy over all classes with ORACLE, STALE, RRM, DECOY prototypes.
Gate T1 (POS and NEG2, each learner): RRM's error below STALE's on >= 4 of 5 seeds, DECOY's above STALE's on >= 4 of 5.
Modes: 'gate' (POS, NEG2; pinned t1_diag.txt) and 'seen' (the 30 SEEN carriers, report only; pinned t1_seen.txt).
Run: uv run python Relational_Reference_Memory/checks/t1_diag.py gate|seen
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "Replay_Quality_Memory" / "checks"))
import t_lib as T  # noqa: E402

SEEDS = (0, 1, 2, 3, 4)
LEARNERS = ("FT", "ANCH1", "ER20")


def one(seed, data, K, learner):
    net, anchors, rec, cuts = T.train(seed, *data, K, learner)
    Xtr, ytr, Xte, yte = data
    P = {w: T.prototypes(net, Xtr, ytr, anchors, rec, cuts, seed, w) for w in ("ORACLE", "STALE", "RRM", "DECOY")}
    old = [c for c, (mu, j) in rec.items() if j < len(cuts) - 1]
    err = {w: float(np.mean([np.linalg.norm(P[w][c] - P["ORACLE"][c]) for c in old])) for w in ("STALE", "RRM", "DECOY")}
    ncm = {w: T.ncm_acc(net, Xte, yte, P[w]) for w in P}
    return err, ncm, 100 * net.acc(Xte, yte)


def block(name, data, K):
    out = {}
    for learner in LEARNERS:
        rows = [one(s, data, K, learner) for s in SEEDS]
        out[learner] = rows
        es = {w: [r[0][w] for r in rows] for w in ("STALE", "RRM", "DECOY")}
        expl = 1 - np.mean(es["RRM"]) / np.mean(es["STALE"]) if np.mean(es["STALE"]) > 0 else float("nan")
        print(f"  [{name} {learner}] softmax acc mean {np.mean([r[2] for r in rows]):7.2f}; drift explained {expl:+.4f}")
        for w in ("STALE", "RRM", "DECOY"):
            print(f"     err {w:6} mean {np.mean(es[w]):9.4f}  seeds " + " ".join(f"{x:8.4f}" for x in es[w]))
        for w in ("ORACLE", "STALE", "RRM", "DECOY"):
            v = [r[1][w] for r in rows]
            print(f"     NCM {w:6} mean {np.mean(v):7.2f}  seeds " + " ".join(f"{x:6.2f}" for x in v))
    return out


def main(mode):
    if mode == "gate":
        import phase_a as PA  # RQM's stream builder (POS, NEG2)
        print("RRM2 T1 DIAG gate (DECLARATION_2.md Part T); SEC1's MLP; 20 first-task anchors; beta 0.01; seeds 0-4; "
              "errors are mean |p - mu_now| over the classes of the first four tasks (hidden-feature units); NCM accuracy (%)")
        ok = {}
        for name in ("POS", "NEG2"):
            data, K = PA.stream(name); res = block(name, data, K)
            for learner, rows in res.items():
                a = sum(r[0]["RRM"] < r[0]["STALE"] for r in rows); b = sum(r[0]["DECOY"] > r[0]["STALE"] for r in rows)
                ok[(name, learner)] = a >= 4 and b >= 4
                print(f"G-T1 {name} {learner}: RRM below STALE on {a}/5, DECOY above STALE on {b}/5 -> "
                      f"{'holds' if ok[(name, learner)] else 'FAILS'}")
        print("T1 GATE " + ("OPEN" if all(ok.values()) else "CLOSED"))
    else:
        print("RRM2 T1 DIAG on the 30 SEEN carriers (report only; DECLARATION_2.md Part T); seeds 0-4")
        summ = []
        for study, did in T.seen_carriers():
            d = T.load_seen_cached(study, did)
            if d is None:
                print(f"{study} {did}: excluded by the loader"); continue
            Xtr, ytr, Xte, yte, K, name = d; print(f"\n[{study} {did} {name}] K {K}, d {Xtr.shape[1]}, train {len(ytr)}")
            res = block(name, (Xtr, ytr, Xte, yte), K)
            for learner, rows in res.items():
                es = {w: np.mean([r[0][w] for r in rows]) for w in ("STALE", "RRM")}
                dn = np.mean([r[1]["RRM"] - r[1]["STALE"] for r in rows])
                dh = np.mean([r[1]["RRM"] - r[2] for r in rows])
                summ.append((name, learner, 1 - es["RRM"] / es["STALE"] if es["STALE"] > 0 else float("nan"), dn, dh))
        print("\nsummary: carrier, learner, drift explained, NCM RRM - STALE, NCM RRM - the learner's softmax head")
        for name, learner, e, dn, dh in summ:
            print(f"   {name[:28]:28} {learner:5} {e:+.4f} {dn:+.4f} {dh:+.4f}")
        for learner in LEARNERS:
            e = [s[2] for s in summ if s[1] == learner]; dn = [s[3] for s in summ if s[1] == learner]
            print(f"{learner}: carriers {len(e)}; drift explained > 0 on {sum(x > 0 for x in e)}, median {np.median(e):+.4f}; "
                  f"NCM RRM ahead of STALE on {sum(x > 0 for x in dn)}, behind on {sum(x < 0 for x in dn)}; "
                  f"NCM RRM ahead of the softmax head on {sum(s[4] > 0 for s in summ if s[1] == learner)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "gate")

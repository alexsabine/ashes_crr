"""RQM Phase A (Replay_Quality_Memory/DEV_DECLARATION.md, pushed before this file): the synthetic gate for the candidate IGR (input-
space class Gaussians fitted at each class's cut, never refitted, replayed class-balanced), with its matched ER, FT, JOINT, the CRR
ablation FGR (the same memory in feature space), RFR (random features + streaming ridge) and SEC-CLIP. Seeds 0-4.
    POS  SEC1's synthetic stream: Gaussian classes (a class Gaussian is the true generator)
    NEG  concentric rings: class c on a circle of radius 1 + c in coordinates 0-1 (radial noise sd 0.1) + 18 N(0,1) nuisance
         coordinates; a single class Gaussian fills the disc, so Gaussian replay is the wrong generator
Gate: G-POS (each IGR form not behind its matched ER by a step on POS), G-NEG (each IGR form behind its matched ER by more than a
step on NEG), G-FT (FT behind ER by more than a step on both), G-ID (replay forced empty == FT bit for bit). Words computed (R15).
Run: uv run python Replay_Quality_Memory/checks/phase_a.py
"""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rqm_lib as R  # noqa: E402

SEEDS = (0, 1, 2, 3, 4)


def rings(K=10, n=1500, d=20, seed=0):
    rng = np.random.default_rng(seed); y = rng.integers(0, K, n); th = rng.uniform(0, 2 * math.pi, n)
    r = 1.0 + y + rng.normal(0, 0.1, n); X = rng.standard_normal((n, d)); X[:, 0] = r * np.cos(th); X[:, 1] = r * np.sin(th)
    return X, y


def neg2(K=10, n=1500, d=20, a=3.0, sd=0.3, seed=0):
    """Amendment 1: five pairs (2k, 2k+1) on coordinates (2k, 2k+1); class 2k at the corners (+-a, +-a), class 2k+1 at
    (+-sqrt2 a, 0), (0, +-sqrt2 a); both have mean 0 and covariance a^2 I there, so their Gaussians are identical."""
    rng = np.random.default_rng(seed); y = rng.integers(0, K, n); X = rng.standard_normal((n, d)); k = rng.integers(0, 4, n)
    cor = np.array([[a, a], [a, -a], [-a, a], [-a, -a]]); axs = math.sqrt(2) * a * np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])
    for i in range(n):
        c = y[i]; base = cor[k[i]] if c % 2 == 0 else axs[k[i]]
        X[i, 2 * (c // 2): 2 * (c // 2) + 2] = base + rng.normal(0, sd, 2)
    return X, y


def stream(name):
    X, y = R.S._synthetic() if name == "POS" else (rings() if name == "NEG" else neg2())
    Xs, ys, meta = R.L.select_classes(X, y, 10); K = meta["classes_used"]
    return R.S.split_standardise(Xs, ys, K), K


def step_of(v): return max(1.0, 2 * float(np.std(v, ddof=1)) / math.sqrt(len(v)))


def main():
    print("RQM Phase A run 2 (DEV_DECLARATION.md + Amendment 1, POST HOC: NEG2 replaces NEG, G-LEARN added); seeds 0-4; accuracy is class-IL over all 10 classes (%)")
    print(f"IGR-F shrinkage alpha {R.ALPHA}; replay batch {R.REPLAY_BS}; RFR width {R.RFR_WIDTH}, lambda {R.RFR_LAMBDA}; "
          "FGR pseudo-activations clipped at 0 (the ReLU range)")
    res = {}
    for name in ("POS", "NEG2"):
        data, K = stream(name); d = data[0].shape[1]; mF = R.mem_rows_per_class("F", d); mD = R.mem_rows_per_class("D", d)
        a = {k: [] for k in ("FT", "JOINT", "ER-F", "ER-D", "IGR-F", "IGR-D", "FGR-F", "SEC-CLIP")}
        idF = []; idD = []
        for s in SEEDS:
            ft = R.run_ft(s, *data, K); a["FT"].append(ft); a["JOINT"].append(R.run_joint(s, *data, K))
            a["ER-F"].append(R.run_er_pc(s, *data, K, mF)); a["ER-D"].append(R.run_er_pc(s, *data, K, mD))
            a["IGR-F"].append(R.run_igr(s, *data, K, "F")); a["IGR-D"].append(R.run_igr(s, *data, K, "D"))
            a["FGR-F"].append(R.run_igr(s, *data, K, "F", space="feature")); a["SEC-CLIP"].append(R.run_sec_clip(s, *data, K))
            idF.append(R.run_igr(s, *data, K, "F", force_empty=True) == ft); idD.append(R.run_igr(s, *data, K, "D", force_empty=True) == ft)
        rfr = R.run_rfr(*data, K)
        res[name] = dict(a=a, rfr=rfr, idF=idF, idD=idD, mF=mF, mD=mD)
        print(f"\n[{name}] d {d}; matched ER rows per class: IGR-F {mF}, IGR-D {mD}; RFR (deterministic) {rfr:.2f}")
        for k, v in a.items():
            print(f"   {k:9} mean {np.mean(v):7.2f}  seeds " + " ".join(f"{x:6.2f}" for x in v))
    print("\n" + "-" * 100)
    ok = {}
    P, N = res["POS"], res["NEG2"]
    for form in ("F", "D"):
        er = P["a"][f"ER-{form}"]; st = step_of(er); diff = np.mean(P["a"][f"IGR-{form}"]) - np.mean(er)
        ok[f"POS-{form}"] = diff > -st
        print(f"G-POS IGR-{form} - ER-{form} on POS {diff:+.4f} (step {st:.4f}) -> {'holds' if ok[f'POS-{form}'] else 'FAILS'}")
    for form in ("F", "D"):
        er = N["a"][f"ER-{form}"]; st = step_of(er); diff = np.mean(N["a"][f"IGR-{form}"]) - np.mean(er)
        ok[f"NEG-{form}"] = diff < -st
        print(f"G-NEG IGR-{form} - ER-{form} on NEG2 {diff:+.4f} (step {st:.4f}): behind by more than a step -> {'holds' if ok[f'NEG-{form}'] else 'FAILS'}")
    jn = N["a"]["JOINT"]; ftn = N["a"]["FT"]; st = step_of(jn); diff = np.mean(jn) - np.mean(ftn)
    ok["LEARN"] = diff > st
    print(f"G-LEARN (Amendment 1) JOINT - FT on NEG2 {diff:+.4f} (step {st:.4f}): the stream is learnable -> {'holds' if ok['LEARN'] else 'FAILS'}")
    for name in ("POS", "NEG2"):
        er = res[name]["a"]["ER-F"]; st = step_of(er); diff = np.mean(res[name]["a"]["FT"]) - np.mean(er)
        ok[f"FT-{name}"] = diff < -st
        print(f"G-FT FT - ER-F on {name} {diff:+.4f} (step {st:.4f}) -> {'holds' if ok[f'FT-{name}'] else 'FAILS'}")
    idall = all(all(res[n]["idF"]) and all(res[n]["idD"]) for n in ("POS", "NEG2"))
    ok["ID"] = idall
    print(f"G-ID replay forced empty == FT bit for bit: {sum(sum(res[n]['idF']) + sum(res[n]['idD']) for n in ('POS', 'NEG2'))}/20 -> {'holds' if idall else 'FAILS'}")
    print("GATE " + ("OPEN" if all(ok.values()) else "CLOSED"))
    print("\nreported beside the gate (not gating):")
    for name in ("POS", "NEG2"):
        a = res[name]["a"]
        print(f"   {name}: CRR ablation IGR-F - FGR-F {np.mean(a['IGR-F']) - np.mean(a['FGR-F']):+.4f}; IGR-F - RFR {np.mean(a['IGR-F']) - res[name]['rfr']:+.4f}; "
              f"IGR-F - JOINT {np.mean(a['IGR-F']) - np.mean(a['JOINT']):+.4f}; SEC-CLIP - ER-F {np.mean(a['SEC-CLIP']) - np.mean(a['ER-F']):+.4f}")


if __name__ == "__main__":
    main()

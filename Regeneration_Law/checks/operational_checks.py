"""The operational mathematics of RLAW (Regeneration_Law/DECLARATION_2.md, pushed in 58d2358 before this file existed).
No data. Deterministic (fixed seeds). Uses the study instrument studies/rlaw/rlaw_lib.py.
Run: uv run python Regeneration_Law/checks/operational_checks.py > Regeneration_Law/checks/operational_checks.txt"""
import math
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "studies" / "rlaw"))
from rlaw_lib import K, ml_v, alpha_hat, fit_q2  # noqa: E402


def local_level(n, v, rng, s_eps=1.0):
    mu = np.cumsum(v * s_eps * rng.normal(size=n)); return mu + s_eps * rng.normal(size=n)


def smooth(y, a, s0=0.0):
    s = np.empty_like(y); s[0] = y[0] if s0 is None else s0
    for t in range(1, y.size): s[t] = s[t - 1] + a * (y[t] - s[t - 1])
    return s


def m11():
    print("M11 LTI independence (n 5000, fixed filters, no report noise):")
    rng = np.random.default_rng(1101); ok = True
    for v in (0.05, 0.3, 1.0, 3.0):
        y = local_level(5000, v, rng); s1 = smooth(y, 0.3, None); u = smooth(y, 0.5, None); s2 = smooth(u, 0.5, None)
        a1 = alpha_hat(s1, y)[0]; a2 = alpha_hat(s2, y)[0]; ok &= abs(a1 - 0.3) <= 0.01
        print(f"   v {v}: K(v) {float(K(v)):.4f}; first-order alpha_hat {a1:.4f}; two-stage alpha_hat {a2:.4f}")
    print(f"   first-order alpha_hat = 0.30 +- 0.01 at every v: {'holds' if ok else 'FAILS'} -> an LTI system meets the law at one v at most")


def m12():
    print("M12 recovery at the unit lengths (100 seeds; offset 0.5, report noise 0.05, quantum 0.1, all in s_eps):")
    for n in (60, 185, 365, 840):
        parts = []
        for v in (0.1, 0.3, 1.0):
            rng = np.random.default_rng(12000 + n * 10 + int(v * 10)); a = float(K(v)); Y = []; S = []
            for _ in range(100):
                y = local_level(n, v, rng); s = smooth(y, a, None) + 0.5 + 0.05 * rng.normal(size=n); s = np.round(s / 0.1) * 0.1
                Y.append(y); S.append(s)
            fit = ml_v(np.array(Y)); kv = K(fit["v"]); ah = np.array([alpha_hat(S[i], Y[i])[0] for i in range(100)])
            r = np.abs(np.log(ah / kv)); w2 = float(np.mean(r <= math.log(2))); w15 = float(np.mean(r <= math.log(1.5)))
            parts.append(f"v {v}: within x2 {w2:.2f}, x1.5 {w15:.2f}, median K(v_hat) {float(np.median(kv)):.4f} (K {a:.4f}), median alpha_hat {float(np.median(ah)):.4f}, grid-edge fits {int(np.sum(fit['edge']))}")
        print(f"   n {n}: " + "; ".join(parts))


def m13():
    print("M13 the bandit arm (sd 0.025 per trial, reflecting 0.25/0.75, Bernoulli outcome on visits; 200 seeds x 2000 visits):")
    al = np.arange(0.002, 0.602, 0.002)
    for g in (1, 2, 4, 8):
        rng = np.random.default_rng(1300 + g); B, V = 200, 2000
        p = rng.uniform(0.25, 0.75, size=B); m = np.full((B, al.size), 0.5); se = np.zeros(al.size); pq = 0.0
        for k in range(V):
            steps = rng.geometric(1.0 / g, size=B) if g > 1 else np.ones(B, int)
            for j in range(int(steps.max())):
                mv = steps > j; p = np.where(mv, p + 0.025 * rng.normal(size=B), p)
                p = np.where(p > 0.75, 1.5 - p, p); p = np.where(p < 0.25, 0.5 - p, p)
            r = (rng.uniform(size=B) < p).astype(float); pq += float(np.mean(p * (1 - p)))
            if k >= 200: se += np.mean((p[:, None] - m) ** 2, axis=0)
            m = m + al[None, :] * (r[:, None] - m)
        a_opt = float(al[np.argmin(se)]); s_eps = math.sqrt(pq / V); v = 0.025 * math.sqrt(g) / s_eps; kv = float(K(v))
        print(f"   mean gap {g}: optimal constant rate {a_opt:.3f}; v {v:.4f} -> K(v) {kv:.4f}; ratio optimum/K {a_opt / kv:.3f} -> {'within 25 %' if abs(a_opt / kv - 1) <= 0.25 else 'OFF by more than 25 %'}")


def m14():
    print("M14 two-step second-stage learning-rate recovery (beta 5, 125 trials, 100 simulated subjects per alpha):")
    for a in (0.05, 0.1, 0.3, 0.6):
        rng = np.random.default_rng(1400 + int(a * 100)); est = []
        for _ in range(100):
            p = rng.uniform(0.25, 0.75, size=4); Q = np.zeros((2, 2)); st, ch, wn = [], [], []
            for t in range(125):
                s = int(rng.uniform() < 0.5); d = Q[s, 1] - Q[s, 0]; c = int(rng.uniform() < 1 / (1 + math.exp(-5 * d)))
                w = float(rng.uniform() < p[2 * s + c]); Q[s, c] += a * (w - Q[s, c]); st.append(s); ch.append(c); wn.append(w)
                p = p + 0.025 * rng.normal(size=4); p = np.where(p > 0.75, 1.5 - p, p); p = np.where(p < 0.25, 0.5 - p, p)
            est.append(fit_q2(np.array(st), np.array(ch), np.array(wn), np.ones(125, bool))[0])
        est = np.array(est); r = np.abs(np.log(est / a))
        print(f"   alpha {a}: within x2 {float(np.mean(r <= math.log(2))):.2f}, median alpha_hat {float(np.median(est)):.4f}, "
              f"quartiles {float(np.quantile(est, 0.25)):.4f}-{float(np.quantile(est, 0.75)):.4f}, at grid edge {int(np.sum((est <= 0.00501) | (est >= 0.999)))}")


def main():
    print("RLAW operational checks (Regeneration_Law/DECLARATION_2.md)")
    m11(); m12(); m13(); m14()
    return 0


if __name__ == "__main__":
    sys.exit(main())

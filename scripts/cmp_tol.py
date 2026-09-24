"""Tolerance-level comparison of a pinned text output across machines (R9: "if not byte-identical, document why and report
tolerance-level reproduction"). Words and punctuation must match exactly, so every verdict and label (R15) is compared
byte for byte. Numbers must agree within rtol or atol. Every difference is printed.

    uv run python scripts/cmp_tol.py NEW PINNED [--rtol 1e-2] [--atol 1e-12]

Exit 0 if equivalent, 1 otherwise. Used in CI only for outputs documented as round-off sensitive across CPUs (list in the
workflow); the local check (scripts/check_all.sh) keeps exact cmp."""
import argparse
import re
import sys

NUM = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")


def split(line):
    out, pos = [], 0
    for m in NUM.finditer(line):
        out.append(("w", line[pos:m.start()])); out.append(("n", m.group())); pos = m.end()
    out.append(("w", line[pos:])); return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("new"); ap.add_argument("pinned")
    ap.add_argument("--rtol", type=float, default=1e-2); ap.add_argument("--atol", type=float, default=1e-12); a = ap.parse_args()
    A = open(a.new).read().splitlines(); B = open(a.pinned).read().splitlines(); bad = 0; tol = 0
    if len(A) != len(B): print(f"line count differs: {len(A)} vs {len(B)}"); bad += 1
    for i, (x, y) in enumerate(zip(A, B), 1):
        if x == y: continue
        tx, ty = split(x), split(y)
        same_shape = len(tx) == len(ty) and all(k1 == k2 for (k1, _), (k2, _) in zip(tx, ty))
        ok = same_shape
        if same_shape:
            for (k, u), (_, w) in zip(tx, ty):
                if k == "w" and u != w: ok = False
                if k == "n" and u != w:
                    fu, fw = float(u), float(w)
                    if not abs(fu - fw) <= max(a.atol, a.rtol * max(abs(fu), abs(fw))): ok = False
        if ok: tol += 1; print(f"line {i}: numbers within tolerance\n  new:    {x}\n  pinned: {y}")
        else: bad += 1; print(f"line {i}: DIFFERS\n  new:    {x}\n  pinned: {y}")
    print(f"{a.pinned}: {bad} line(s) differ beyond tolerance, {tol} within (rtol {a.rtol}, atol {a.atol})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

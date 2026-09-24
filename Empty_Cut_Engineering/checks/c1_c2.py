"""Checks C1 (state closure) and C2 (the clock) of Empty_Cut_Engineering/DECLARATION.md, on the real stack in stack.py.
Every run is its own process; a paused run is two processes joined by a checkpoint file. Verdict words are computed from
the numbers (R15). Machine-dependent save/load times go to c1_c2_timing.txt (committed, not compared byte-for-byte).

Run: uv run --group realsys python Empty_Cut_Engineering/checks/c1_c2.py > Empty_Cut_Engineering/checks/c1_c2.txt
"""
import concurrent.futures as cf
import hashlib
import inspect
import json
import os
import pathlib
import subprocess
import sys
import tempfile

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(HERE))
from crr.instrument.core import kl_step  # noqa: E402
import stack  # noqa: E402

LS = (0, 10, 100, 1000)
C1_L = 100
VARIANTS = {"lr step, feature step": ("step", "step"), "lr wall, feature step": ("wall", "step"),
            "lr step, feature wall": ("step", "wall"), "lr wall, feature wall": ("wall", "wall")}


def launch(cfg, tmp, name):
    out = tmp / name; out.mkdir()
    r = subprocess.run([sys.executable, str(HERE / "stack.py"), json.dumps(cfg), str(out)], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{name} failed:\n{r.stderr[-3000:]}")
    res = json.loads((out / "result.json").read_text()); tim = json.loads((out / "timing.json").read_text())
    probe = np.load(out / "probe.npy") if (out / "probe.npy").exists() else None
    return name, res, tim, probe


def content(pa, pb):
    return float(np.sqrt(2 * max(0.0, kl_step(pa, pb))))


def main():
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="ece_"))
    lock = hashlib.sha256((ROOT / "uv.lock").read_bytes()).hexdigest()
    import torch
    print("Empty-cut engineering, checks C1 (state closure) and C2 (the clock) - Empty_Cut_Engineering/DECLARATION.md")
    print(f"torch {torch.__version__}; numpy {np.__version__}; uv.lock sha256 {lock}")
    print(f"stack: transformer {stack.LAYERS} layers, d {stack.D}, {stack.HEADS} heads, dropout {stack.DROPOUT}; AdamW lr {stack.LR} wd {stack.WD}, "
          f"clip {stack.CLIP}; warm-up {stack.WARMUP} + cosine over {stack.UPDATES} updates; micro-batch {stack.MB} x accumulation {stack.ACCUM}; "
          f"{stack.EPOCHS} epochs of {stack.N_TRAIN}; DataLoader shuffle + {stack.WORKERS} workers (numpy augmentation p {stack.AUG_P}); "
          f"mixup (numpy, alpha {stack.MIX_ALPHA}); masking (Python random, {stack.N_MASK} tokens); EMA {stack.EMA_DECAY}")
    print(f"pause after micro-step {stack.PAUSE_AT} of {stack.TOTAL} (epoch 2 of {stack.EPOCHS}, between the two micro-batches of update {stack.PAUSE_AT // stack.ACCUM}); "
          f"every run is a separate process; content = sqrt(2 KL(p_uninterrupted || p_resumed)) on {stack.N_PROBE} probe sequences")
    jobs = []
    for vname, (lc, fc) in VARIANTS.items():
        tag = f"{lc}-{fc}"
        jobs.append((f"full_{tag}", dict(phase="full", lr_clock=lc, feat_clock=fc)))
        jobs.append((f"first_{tag}", dict(phase="first", lr_clock=lc, feat_clock=fc, ckpt=str(tmp / f"ckpt_{tag}.pt"))))
    jobs.append(("full_step-step_b", dict(phase="full", lr_clock="step", feat_clock="step")))
    R = {}; T = {}; P = {}
    with cf.ThreadPoolExecutor(3) as ex:
        for name, res, tim, probe in ex.map(lambda j: launch(j[1], tmp, j[0]), jobs):
            R[name], T[name], P[name] = res, tim, probe
    jobs2 = []
    ck = str(tmp / "ckpt_step-step.pt")
    jobs2.append(("c1_full", dict(phase="second", ckpt=ck, L=C1_L)))
    jobs2.append(("c1_ulp", dict(phase="second", ckpt=ck, L=C1_L, omit="ulp")))
    for k in stack.COMPONENTS[1:]:
        jobs2.append((f"c1_omit_{k}", dict(phase="second", ckpt=ck, L=C1_L, omit=k)))
    for vname, (lc, fc) in VARIANTS.items():
        tag = f"{lc}-{fc}"
        for L in LS:
            jobs2.append((f"c2_{tag}_L{L}", dict(phase="second", ckpt=str(tmp / f"ckpt_{tag}.pt"), L=L, lr_clock=lc, feat_clock=fc)))
    with cf.ThreadPoolExecutor(3) as ex:
        for name, res, tim, probe in ex.map(lambda j: launch(j[1], tmp, j[0]), jobs2):
            R[name], T[name], P[name] = res, tim, probe

    base = R["full_step-step"]; pb = P["full_step-step"]
    same = lambda n, ref="full_step-step": R[n]["sha_model"] == R[ref]["sha_model"] and R[n]["sha_ema"] == R[ref]["sha_ema"]
    g0 = same("full_step-step_b")
    print("\n== G0 determinism baseline: two uninterrupted runs in separate processes")
    print(f"   model sha {base['sha_model'][:16]}..., EMA sha {base['sha_ema'][:16]}...; second process identical: {g0}; probe accuracy {base['probe_acc']:.4f}")
    print(f"\n== C1 state closure: pause of L = {C1_L} wall micro-steps, resumed in a new process")
    g1 = same("c1_full"); g2 = (not same("c1_ulp")) and content(pb, P["c1_ulp"]) > 0
    print(f"   G1 full restore K1-K9: bit-identical {g1}; content {content(pb, P['c1_full']):.6g}; skip-ahead re-iterated {R['c1_full']['skipped_batches']} batches")
    print(f"   G2 one-ulp change to one weight at the pause: bit-identical {same('c1_ulp')}; content {content(pb, P['c1_ulp']):.6g}; "
          f"probe accuracy {R['c1_ulp']['probe_acc']:.4f}")
    inset = []
    for k in stack.COMPONENTS[1:]:
        n = f"c1_omit_{k}"; s = same(n); inset.append(not s)
        print(f"   omit {k} ({stack.NAMES[k]}): bit-identical {s}; content {content(pb, P[n]):.6g}; probe accuracy {R[n]['probe_acc']:.4f} "
              f"(uninterrupted {base['probe_acc']:.4f}) -> {'in the read-set' if not s else 'NOT in the read-set'}")
    g3n = sum(inset)
    print(f"   G3: {g3n} of {len(inset)} omitted components change the trajectory")
    print("\n== C2 the clock: the same checkpoint resumed after pauses of L wall micro-steps; each keying compared with its own uninterrupted run")
    g4_step = True; g4_wall = True
    for vname, (lc, fc) in VARIANTS.items():
        tag = f"{lc}-{fc}"; ref = f"full_{tag}"; row = []
        cs = []
        for L in LS:
            n = f"c2_{tag}_L{L}"; s = same(n, ref); c = content(P[ref], P[n]); cs.append(c)
            row.append(f"L {L}: identical {s}, content {c:.6g}")
            if lc == "step" and fc == "step": g4_step &= s
            elif L > 0: g4_wall &= (not s)
        grows = all(b >= a for a, b in zip(cs[1:], cs[2:])) if not (lc == "step" and fc == "step") else None
        print(f"   {vname}: " + "; ".join(row) + ("" if grows is None else f"; content non-decreasing in L>0: {grows}"))
        if grows is not None: g4_wall &= grows
    g4 = g4_step and g4_wall
    print(f"   G4: step-keyed identical for every L: {g4_step}; wall-keyed changed for every L > 0 with content non-decreasing: {g4_wall}")
    print("\n== Effort (C1): the checkpoint, component by component")
    by = R["first_step-step"]["bytes"]
    for k in stack.COMPONENTS:
        print(f"   {k} {stack.NAMES[k]}: {by[k]} bytes")
    print(f"   whole checkpoint file: {R['first_step-step']['ckpt_bytes']} bytes; model parameters alone (K1): {by['K1']} bytes; "
          f"ratio whole / K1 {R['first_step-step']['ckpt_bytes'] / by['K1']:.3f}")
    ls_ = len(inspect.getsource(stack.save_state).splitlines()); ll_ = len(inspect.getsource(stack.load_state).splitlines())
    print(f"   code: save_state {ls_} lines, load_state {ll_} lines (plus the loop's own position bookkeeping)")
    ok = g0 and g1 and g2 and g4
    verdict = ("EMPTY CUT ACHIEVABLE ON THIS STACK (C1, C2)" if ok else
               "NOT ACHIEVABLE BITWISE (G0 failed)" if not g0 else "INSTRUMENT BROKEN" if not g2 else "a must-pass FAILED")
    print(f"\nsummary: G0 {'holds' if g0 else 'FAILS'}; G1 {'holds' if g1 else 'FAILS'}; G2 {'holds' if g2 else 'FAILS'}; "
          f"G3 {g3n}/{len(inset)} in the read-set; G4 {'holds' if g4 else 'FAILS'} -> {verdict}")
    with open(HERE / "c1_c2_timing.txt", "w") as f:
        f.write("machine-dependent timings (seconds), not compared byte-for-byte\n")
        f.write(f"save (first phase, step-step): {T['first_step-step'].get('save_s', float('nan')):.4f}\n")
        f.write(f"load (c1_full): {T['c1_full'].get('load_s', float('nan')):.4f}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

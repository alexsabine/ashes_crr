"""RW1 orchestrator (Real_World/DECLARATION_RW1.md): is the resume of an existing training stack an empty cut?
Every run is its own process; verdict words are computed from the numbers (R15). Machine-dependent times go to
rw1_timing.txt (committed, not compared byte-for-byte).

Run: uv run --group realsys python Real_World/checks/rw1.py > Real_World/checks/rw1.txt
"""
import concurrent.futures as cf
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(HERE))
from crr.instrument.core import kl_step  # noqa: E402
import rw1_run as R  # noqa: E402

ARMS = [("S1", "default resume, pause 0 s", dict(sleep=0)),
        ("S2", "ignore_data_skip=True", dict(ignore_data_skip=True)),
        ("S3", "rng_state.pth deleted", dict(delete=["rng_state.pth"])),
        ("S4", "optimizer.pt deleted", dict(delete=["optimizer.pt"])),
        ("S5", "scheduler.pt deleted", dict(delete=["scheduler.pt"])),
        ("T5", "default resume, real pause 5 s", dict(sleep=5)),
        ("T30", "default resume, real pause 30 s", dict(sleep=30))]


def launch(cfg, tmp, name):
    out = tmp / name; out.mkdir()
    env = dict(os.environ, HF_HUB_OFFLINE="1")
    r = subprocess.run([sys.executable, str(HERE / "rw1_run.py"), json.dumps(cfg), str(out)], capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise RuntimeError(f"{name} failed:\n{r.stderr[-4000:]}")
    res = json.loads((out / "result.json").read_text()); tim = json.loads((out / "timing.json").read_text())
    return name, res, tim, (out / "probe.npy")


def content(pa, pb):
    a = np.load(pa).astype(np.float64); b = np.load(pb).astype(np.float64)
    return float(np.sqrt(2 * max(0.0, kl_step(a, b))))


def weights_sha(model):
    from huggingface_hub import snapshot_download
    name, rev = R.MODELS[model]
    d = pathlib.Path(snapshot_download(name, revision=rev, allow_patterns=["*.json", "*.safetensors", "*.txt", "*.model"]))
    shas = {}
    for f in sorted(d.glob("*.safetensors")):
        shas[f.name] = hashlib.sha256(f.read_bytes()).hexdigest()
    return shas


def study(model, tmp, workers):
    st = R.SETTINGS[model]
    jobs = [(f"{model}_full_a", dict(model=model, phase="full")), (f"{model}_full_b", dict(model=model, phase="full")),
            (f"{model}_first", dict(model=model, phase="first"))]
    out = {}
    with cf.ThreadPoolExecutor(workers) as ex:
        for name, res, tim, pr in ex.map(lambda j: launch(j[1], tmp, j[0]), jobs):
            out[name] = (res, tim, pr)
    ck = out[f"{model}_first"][0]["ckpt"]; files = out[f"{model}_first"][0]["files"]
    arms = ARMS if model == "gpt2" else ARMS[:1]
    jobs2 = []
    for aid, _, kw in arms:
        missing = [f for f in kw.get("delete", []) if f not in files]
        if missing:
            out[f"{model}_{aid}"] = ("absent", missing)
            continue
        jobs2.append((f"{model}_{aid}", dict(model=model, phase="second", ckpt=ck, **kw)))
    with cf.ThreadPoolExecutor(workers) as ex:
        for name, res, tim, pr in ex.map(lambda j: launch(j[1], tmp, j[0]), jobs2):
            out[name] = (res, tim, pr)
    return out, files, st


def main():
    import torch
    import transformers
    import accelerate
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="rw1_"))
    lock = hashlib.sha256((ROOT / "uv.lock").read_bytes()).hexdigest()
    print("RW1: is the resume of an existing training stack an empty cut? (Real_World/DECLARATION_RW1.md)")
    print(f"transformers {transformers.__version__}; accelerate {accelerate.__version__}; torch {torch.__version__}; numpy {np.__version__}; uv.lock sha256 {lock}")
    print(f"data: {R.N_TRAIN} synthetic sequences of {R.SEQ} token ids in [0, {R.ID_MAX}); gradient accumulation {R.ACCUM}; lr {R.LR}; warm-up {R.WARMUP}; seed {R.SEED}; CPU, one thread")
    timing = []; verdicts = {}
    for model, workers in (("gpt2", 3), ("qwen", 1)):
        name, rev = R.MODELS[model]
        shas = weights_sha(model)
        out, files, st = study(model, tmp, workers)
        print(f"\n== {name} at {rev}; weights sha256 " + "; ".join(f"{k} {v}" for k, v in shas.items()))
        print(f"   batch {st['bs']}; max_steps {st['max_steps']}; pause after the checkpoint at optimiser step {st['pause']}; probe {st['n_probe']} sequences")
        print(f"   checkpoint-{st['pause']} files: " + "; ".join(f"{k} {v} bytes" for k, v in files.items()))
        print(f"   the stopped run's global step {out[f'{model}_first'][0]['global_step']}: Trainer checkpoints at optimiser steps only, so its cut falls between updates, never inside an accumulation")
        ref = out[f"{model}_full_a"]
        g0 = out[f"{model}_full_b"][0]["sha"] == ref[0]["sha"]
        print(f"   G0 two uninterrupted runs in separate processes: identical {g0} (sha {ref[0]['sha'][:16]}...)")
        rows = {}
        for aid, desc, _ in (ARMS if model == "gpt2" else ARMS[:1]):
            v = out[f"{model}_{aid}"]
            if v[0] == "absent":
                print(f"   {aid} {desc}: file absent from the checkpoint ({', '.join(v[1])}); not run"); rows[aid] = None; continue
            same = v[0]["sha"] == ref[0]["sha"]; c = content(ref[2], v[2]); rows[aid] = same
            print(f"   {aid} {desc}: global step {v[0]['global_step']}; identical {same}; content {c:.6g}")
            timing.append(f"{model} {aid}: {v[1]['train_seconds']:.2f} s for {v[1]['steps_run']} steps")
        timing.append(f"{model} full_a: {ref[1]['train_seconds']:.2f} s for {ref[1]['steps_run']} steps")
        if model == "gpt2":
            s1 = bool(rows["S1"]); t = bool(rows["T5"]) and bool(rows["T30"])
            det = [rows[a] for a in ("S2", "S3", "S4", "S5") if rows[a] is not None]
            broken = any(det)
            if not g0:
                v_ = "NOT DECIDABLE BITWISE (G0 fails)"
            elif broken:
                v_ = "DETECTOR BROKEN (a declared-read file changed nothing)"
            elif s1 and t:
                v_ = "THE EXISTING STACK'S RESUME IS AN EMPTY CUT ON THIS SETTING"
            else:
                v_ = "NOT AN EMPTY CUT (" + ", ".join(n for n, ok in (("S1", s1), ("T", t)) if not ok) + " fails)"
            verdicts[model] = v_
            print(f"   detectors S2-S5 not identical: {sum(1 for d in det if not d)} of {len(det)}; S1 {'holds' if s1 else 'FAILS'}; T {'holds' if t else 'FAILS'}")
        else:
            verdicts[model] = f"G0 {'holds' if g0 else 'FAILS'}; S1 {'holds' if rows['S1'] else 'FAILS'}"
        for d in tmp.glob(f"{model}_*"):
            shutil.rmtree(d, ignore_errors=True)                                  # disk: checkpoints are large
    print(f"\nsummary: GPT-2 full grid: {verdicts['gpt2']}; Qwen2.5-0.5B-Instruct pilot: {verdicts['qwen']}")
    (HERE / "rw1_timing.txt").write_text("machine-dependent timings, not compared byte-for-byte\n" + "\n".join(timing) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

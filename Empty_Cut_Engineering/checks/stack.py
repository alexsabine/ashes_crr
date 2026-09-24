"""The real training stack for checks C1 and C2 (Empty_Cut_Engineering/DECLARATION.md, pushed in 6aff80a before this file
existed). One process = one run. A paused run trains to micro-step PAUSE_AT, writes a checkpoint and exits; a NEW process
loads it (with the named component omitted, as a naive resume would omit it) and continues.

Reading of the declared batch (recorded in AGENT_LOG): micro-batch 16, gradient accumulation over 2 micro-batches. That is
the only reading under which the declared pause (micro-step 201) lies in the second epoch and between the two
micro-batches of one accumulation: 2048 / 16 = 128 micro-steps per epoch; after 201 micro-steps (0..200) the pause
falls between micro-steps 200 and 201, which together make update 100.

Run (normally via c1_c2.py):
  uv run --group realsys python Empty_Cut_Engineering/checks/stack.py <config json> <out dir>
"""
import os

os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("MKL_NUM_THREADS", "1")
import copy  # noqa: E402
import hashlib  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import random  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402

import numpy as np  # noqa: E402
import torch  # noqa: E402
import torch.nn as nn  # noqa: E402
from torch.utils.data import DataLoader, Dataset  # noqa: E402

SEED = 1234
N_TRAIN, N_PROBE, SEQ, VOCAB, NCLS = 2048, 256, 16, 32, 4
D, HEADS, LAYERS, DROPOUT = 32, 4, 2, 0.1
MB, ACCUM, EPOCHS, WORKERS = 16, 2, 3, 2
LR, WD, CLIP, WARMUP, EMA_DECAY = 1e-3, 0.01, 1.0, 20, 0.99
AUG_P, N_MASK, MIX_ALPHA = 0.1, 2, 0.4
PAUSE_AT = 201
PER_EPOCH = N_TRAIN // MB                       # 128 micro-steps
TOTAL = EPOCHS * PER_EPOCH                      # 384 micro-steps
UPDATES = TOTAL // ACCUM                        # 192 updates
COMPONENTS = ("K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8", "K9")
NAMES = {"K1": "model parameters and buffers", "K2": "optimiser state", "K3": "scheduler state",
         "K4": "data position (epoch, batches consumed, loader generator at the epoch's start)", "K5": "torch global RNG",
         "K6": "numpy global RNG", "K7": "Python random", "K8": "EMA weights", "K9": "accumulated gradient"}


def lr_factor(x):
    """warm-up then cosine to 0 over UPDATES; x is the clock the schedule is keyed to (in updates)"""
    if x < WARMUP:
        return (x + 1) / WARMUP
    return 0.5 * (1 + math.cos(math.pi * min(1.0, (x - WARMUP) / (UPDATES - WARMUP))))


# ---------------------------------------------------------------- data
def make_split(n, seed):
    r = np.random.default_rng(seed)
    X = r.integers(0, VOCAB, size=(n, SEQ))
    y = np.stack([np.isin(X, np.arange(c * 8, c * 8 + 8)).sum(1) for c in range(NCLS)], 1).argmax(1)
    return X.astype(np.int64), y.astype(np.int64)


class Seqs(Dataset):
    def __init__(self, X, y):
        self.X, self.y = X, y

    def __len__(self):
        return len(self.y)

    def __getitem__(self, i):
        x = self.X[i].copy()
        flip = np.random.random(SEQ) < AUG_P                 # augmentation from the worker's numpy stream
        x[flip] = np.random.randint(0, VOCAB, int(flip.sum()))
        return torch.from_numpy(x), torch.tensor(self.y[i])


def worker_init(wid):
    np.random.seed(torch.initial_seed() % 2 ** 32)


def loader(ds, gen):
    return DataLoader(ds, batch_size=MB, shuffle=True, generator=gen, num_workers=WORKERS, worker_init_fn=worker_init,
                      drop_last=True)


# ---------------------------------------------------------------- model
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.emb = nn.Embedding(VOCAB + 1, D); self.pos = nn.Parameter(torch.zeros(SEQ, D)); self.tproj = nn.Linear(1, D)
        layer = nn.TransformerEncoderLayer(D, HEADS, dim_feedforward=2 * D, dropout=DROPOUT, batch_first=True)
        self.enc = nn.TransformerEncoder(layer, LAYERS, enable_nested_tensor=False); self.head = nn.Linear(D, NCLS)

    def forward(self, x, tf, lam=1.0):
        e = self.emb(x) + self.pos + self.tproj(torch.full((x.shape[0], 1, 1), float(tf)))
        if lam != 1.0:
            e = lam * e + (1 - lam) * e.roll(1, 0)
        return self.head(self.enc(e).mean(1))


def state_sha(model):
    h = hashlib.sha256()
    for k, v in sorted(model.state_dict().items()):
        h.update(k.encode()); h.update(v.detach().contiguous().numpy().tobytes())
    return h.hexdigest()


# ---------------------------------------------------------------- checkpoint: save and restore, one entry per component
def save_state(c):
    return {"K1": c["model"].state_dict(), "K2": c["opt"].state_dict(), "K3": c["sched"].state_dict(),
            "K4": {"epoch": c["epoch"], "pos": c["pos"], "gen_epoch_start": c["gen_epoch_start"]},
            "K5": torch.get_rng_state(), "K6": np.random.get_state(), "K7": random.getstate(),
            "K8": c["ema"].state_dict(), "K9": [None if p.grad is None else p.grad.clone() for p in c["model"].parameters()],
            "counters": {"m": c["m"], "k": c["k"], "t": c["t"]}}


def load_state(c, s, omit):
    c["model"].load_state_dict(s["K1"])
    if omit != "K2": c["opt"].load_state_dict(s["K2"])
    if omit != "K3": c["sched"].load_state_dict(s["K3"])
    if omit != "K4": c["epoch"], c["pos"], c["gen_epoch_start"] = s["K4"]["epoch"], s["K4"]["pos"], s["K4"]["gen_epoch_start"]
    else: c["epoch"], c["pos"] = s["K4"]["epoch"], 0          # a naive resume restarts the epoch from a fresh iterator
    if omit != "K5": torch.set_rng_state(s["K5"])
    if omit != "K6": np.random.set_state(s["K6"])
    if omit != "K7": random.setstate(s["K7"])
    if omit != "K8": c["ema"].load_state_dict(s["K8"])
    else: c["ema"].load_state_dict(c["model"].state_dict())
    if omit != "K9":
        for p, g in zip(c["model"].parameters(), s["K9"]): p.grad = None if g is None else g.clone()
    c["m"], c["k"], c["t"] = s["counters"]["m"], s["counters"]["k"], s["counters"]["t"]


def component_bytes(s):
    out = {}
    for k in COMPONENTS:
        b = io.BytesIO(); torch.save(s[k], b); out[k] = len(b.getvalue())
    return out


# ---------------------------------------------------------------- one run
def run(cfg, outdir):
    """cfg: phase ('full' | 'first' | 'second'), omit (None | 'K2'..'K9' | 'ulp'), L (pause length, wall micro-steps),
    lr_clock and feat_clock ('step' | 'wall'), ckpt (path)"""
    torch.set_num_threads(1); torch.use_deterministic_algorithms(True)
    torch.manual_seed(SEED); np.random.seed(SEED); random.seed(SEED)       # what every process does at start
    Xtr, ytr = make_split(N_TRAIN, 7); Xpr, ypr = make_split(N_PROBE, 8); ds = Seqs(Xtr, ytr)
    model = Net(); ema = copy.deepcopy(model)
    opt = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=WD)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_factor)
    gen = torch.Generator(); gen.manual_seed(SEED)
    c = dict(model=model, ema=ema, opt=opt, sched=sched, epoch=0, pos=0, gen_epoch_start=gen.get_state(), m=0, k=0, t=0)
    timing = {}
    if cfg["phase"] == "second":
        t0 = time.perf_counter(); s = torch.load(cfg["ckpt"], weights_only=False); timing["load_s"] = time.perf_counter() - t0
        load_state(c, s, cfg.get("omit"))
        if cfg.get("omit") == "ulp":
            with torch.no_grad():
                w = c["model"].head.weight; w[0, 0] = torch.nextafter(w[0, 0], torch.tensor(float("inf")))
        c["t"] += cfg.get("L", 0)                                          # the pause: only the wall clock moves
        if cfg.get("omit") == "K4":
            gen.manual_seed(SEED)
        else:
            gen.set_state(c["gen_epoch_start"])
    stop = PAUSE_AT if cfg["phase"] == "first" else TOTAL
    model.train(); skipped = 0
    while c["m"] < stop:
        if c["pos"] == 0:
            c["gen_epoch_start"] = gen.get_state()
        it = iter(loader(ds, gen))
        for _ in range(c["pos"]):                                          # skip-ahead to the saved position
            next(it); skipped += 1
        for x, y in it:
            if c["m"] >= stop:
                break
            for i in range(x.shape[0]):                                    # token masking from Python's random
                for j in random.sample(range(SEQ), N_MASK):
                    x[i, j] = VOCAB
            lam = float(np.random.beta(MIX_ALPHA, MIX_ALPHA))              # mixup from the global numpy stream
            tf = (c["k"] if cfg.get("feat_clock", "step") == "step" else c["t"] / ACCUM) / 1000.0
            out = model(x, tf, lam)
            ce = nn.functional.cross_entropy
            loss = (lam * ce(out, y) + (1 - lam) * ce(out, y.roll(1, 0))) / ACCUM
            loss.backward()
            c["m"] += 1; c["t"] += 1; c["pos"] += 1
            if c["m"] % ACCUM == 0:
                if cfg.get("lr_clock", "step") == "wall":
                    for g_ in opt.param_groups: g_["lr"] = LR * lr_factor(c["t"] / ACCUM - 1)
                nn.utils.clip_grad_norm_(model.parameters(), CLIP)
                opt.step(); opt.zero_grad(set_to_none=True)
                if cfg.get("lr_clock", "step") == "step": sched.step()
                c["k"] += 1
                with torch.no_grad():
                    for pe, pm in zip(ema.parameters(), model.parameters()): pe.mul_(EMA_DECAY).add_(pm, alpha=1 - EMA_DECAY)
            if c["pos"] == PER_EPOCH:
                break
        if c["pos"] >= PER_EPOCH:
            c["epoch"] += 1; c["pos"] = 0
    res = {"m": c["m"], "k": c["k"], "t": c["t"], "skipped_batches": skipped}
    if cfg["phase"] == "first":
        s = save_state(c); t0 = time.perf_counter(); torch.save(s, cfg["ckpt"]); timing["save_s"] = time.perf_counter() - t0
        res["bytes"] = component_bytes(s); res["ckpt_bytes"] = os.path.getsize(cfg["ckpt"])
    else:
        model.eval()
        tf = (c["k"] if cfg.get("feat_clock", "step") == "step" else c["t"] / ACCUM) / 1000.0
        with torch.no_grad():
            p = torch.softmax(model(torch.from_numpy(Xpr), tf), 1).numpy().astype(np.float64)
        np.save(os.path.join(outdir, "probe.npy"), p)
        res["sha_model"] = state_sha(model); res["sha_ema"] = state_sha(ema)
        res["probe_acc"] = float((p.argmax(1) == ypr).mean())
    with open(os.path.join(outdir, "result.json"), "w") as f:
        json.dump(res, f, sort_keys=True)
    with open(os.path.join(outdir, "timing.json"), "w") as f:
        json.dump(timing, f, sort_keys=True)


if __name__ == "__main__":
    run(json.loads(sys.argv[1]), sys.argv[2])

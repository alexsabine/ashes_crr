"""lm_bench.py — byte-level transformer, pretrain on D0, continual stream D1..D4, arms per PREREG_lm.md.
Usage: python lm_bench.py pretrain
       python lm_bench.py run METHOD SEED REPLAY [Om | AF AS] [SPARSE]   -> JSON line
"""
import sys, os, json, math, time, glob, re
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F
torch.set_num_threads(1); D = "/home/claude/lm/data"; CTX = 128; BS = 16
Kf = lambda v: (v / 2) * (math.sqrt(v * v + 4) - v)

def strip_gb(t):
    t = t.replace("\r\n", "\n"); a = t.find("*** START"); b = t.find("*** END")
    if a > 0: t = t[t.find("\n", a) + 1:]
    if b > 0: t = t[:b]
    return t
def rd(fs, gb=False):
    return "".join(strip_gb(open(f, encoding="utf-8", errors="ignore").read()) if gb else open(f, encoding="utf-8", errors="ignore").read() for f in fs)
def to_bytes(s): return np.frombuffer(s.encode("utf-8"), np.uint8)
def corpus():
    d0 = to_bytes(rd([f"{D}/pp.txt", f"{D}/md.txt", f"{D}/mm.txt"], gb=True))
    d1 = to_bytes(rd(sorted(glob.glob(f"{D}/py*.py"))))
    d2 = to_bytes(rd([f"{D}/shakes.txt"]))
    d3 = to_bytes(rd([f"{D}/de2.txt", f"{D}/de3.txt"], gb=True))
    d4 = to_bytes(rd([f"{D}/c1.c", f"{D}/c2.c"]))
    return dict(D0=(d0[:3_000_000], d0[3_000_000:3_064_000]),
                D1=(d1[:300_000], d1[300_000:332_000]), D2=(d2[:300_000], d2[300_000:332_000]),
                D3=(d3[:300_000], d3[300_000:332_000]), D4=(d4[:300_000], d4[300_000:332_000]))
def seqs(b): n = len(b) // (CTX + 1); return torch.from_numpy(b[: n * (CTX + 1)].reshape(n, CTX + 1).astype(np.int64))

class Block(nn.Module):
    def __init__(s, d, h):
        super().__init__(); s.ln1 = nn.LayerNorm(d); s.att = nn.MultiheadAttention(d, h, batch_first=True)
        s.ln2 = nn.LayerNorm(d); s.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))
    def forward(s, x, mask):
        a = s.ln1(x); x = x + s.att(a, a, a, attn_mask=mask, need_weights=False)[0]; return x + s.mlp(s.ln2(x))
class LM(nn.Module):
    def __init__(s, d=128, L=4, h=4):
        super().__init__(); s.tok = nn.Embedding(256, d); s.pos = nn.Embedding(CTX, d)
        s.blocks = nn.ModuleList([Block(d, h) for _ in range(L)]); s.ln = nn.LayerNorm(d); s.out = nn.Linear(d, 256)
        s.register_buffer("mask", torch.triu(torch.ones(CTX, CTX, dtype=torch.bool), 1))
    def forward(s, x):
        T = x.shape[1]; h = s.tok(x) + s.pos(torch.arange(T))[None]
        for b in s.blocks: h = b(h, s.mask[:T, :T])
        return s.out(s.ln(h))
def loss_fn(logits, y): return F.cross_entropy(logits.reshape(-1, 256), y.reshape(-1))
def bpb(net, S):
    net.eval(); tot = 0.
    with torch.no_grad():
        for i in range(0, len(S), 64):
            x = S[i:i + 64]; tot += loss_fn(net(x[:, :-1]), x[:, 1:]).item() * len(x)
    net.train(); return tot / len(S) / math.log(2)
def flat(net): return torch.cat([p.detach().flatten() for p in net.parameters()])
def set_flat(net, v):
    i = 0
    for p in net.parameters(): n = p.numel(); p.data.copy_(v[i:i + n].view_as(p)); i += n

def pretrain():
    C = corpus(); S = seqs(C["D0"][0]); torch.manual_seed(0); net = LM(); opt = torch.optim.AdamW(net.parameters(), 1e-3)
    perm = torch.randperm(len(S)); t0 = time.time()
    for k, i in enumerate(range(0, len(S), BS)):
        x = S[perm[i:i + BS]]; opt.zero_grad(); l = loss_fn(net(x[:, :-1]), x[:, 1:]); l.backward(); opt.step()
        if k % 200 == 0: print(k, round(l.item() / math.log(2), 3), round(time.time() - t0), flush=True)
    torch.save(net.state_dict(), "/home/claude/lm/pretrained.pt")
    print("held-out bpb:", {k: round(bpb(net, seqs(v[1])), 3) for k, v in C.items()})

def run(method, seed, replay, Om=16., af=0.03, as_=0.003, sparse=1):
    C = corpus(); ev = {k: seqs(v[1]) for k, v in C.items()}
    net = LM(); net.load_state_dict(torch.load("/home/claude/lm/pretrained.pt")); opt = torch.optim.AdamW(net.parameters(), 1e-3)
    base = LM(); base.load_state_dict(net.state_dict()); LAM = float(os.environ.get("LAM", "10"))
    ema = method in ("crr", "fixed")
    if ema:
        ema_p, ema_s = LM(), LM(); ema_p.load_state_dict(net.state_dict()); ema_s.load_state_dict(net.state_dict())
    g = torch.Generator().manual_seed(seed); rng = np.random.default_rng(seed)
    S0 = seqs(C["D0"][0]); buf = [S0[i] for i in torch.randperm(len(S0), generator=g)[:4000]]  # reservoir seeded with pretraining data
    seen = len(S0); probe = S0[torch.randperm(len(S0), generator=g)[:8]]
    with torch.no_grad(): p_probe = F.log_softmax(net(probe[:, :-1]), -1)
    compute = 0.; n_stream = 0; vhat = 0.; vlog = []; wlog = []; step = 0; SM = [0., 0.]; EV = [None, None]; Fd = torch.full((flat(net).numel(),), 1e-3); rb_int = int(replay * BS); rb_frac = replay * BS - rb_int
    for dom in ("D1", "D2", "D3", "D4"):
        S = seqs(C[dom][0]); perm = torch.randperm(len(S), generator=g)
        for i in range(0, len(S), BS):
            x = S[perm[i:i + BS]]; n = len(x); n_stream += n
            rb = rb_int + (1 if rng.random() < rb_frac else 0)
            if rb > 0:
                sel = rng.choice(len(buf), rb, replace=False); x = torch.cat([x, torch.stack([buf[j] for j in sel])])
            theta0 = flat(net); opt.zero_grad()
            if method == "eq" and rb >= 1:
                xn, xp = x[:n], x[n:]
                def gvec(xx):
                    opt.zero_grad(); loss_fn(net(xx[:, :-1]), xx[:, 1:]).backward()
                    return torch.cat([p.grad.flatten() for p in net.parameters()]).clone()
                gn = gvec(xn); gp = gvec(xp); compute += 3 * len(x)
                if EV[0] is None: EV[0] = gn.clone(); EV[1] = gp.clone()
                else: EV[0].mul_(0.98).add_(gn, alpha=0.02); EV[1].mul_(0.98).add_(gp, alpha=0.02)
                w = min(Om * math.sqrt(float((Fd * EV[0] * EV[0]).sum()) / max(float((Fd * EV[1] * EV[1]).sum()), 1e-12)), 50.); wlog.append(w)
                gtot = gn + w * gp; i0 = 0
                for p in net.parameters(): k = p.numel(); p.grad = gtot[i0:i0 + k].view_as(p).clone(); i0 += k
                Fd = 0.99 * Fd + 0.01 * gn * gn
                opt.step(); step += 1
                for j in range(n):
                    seen += 1; r_ = rng.integers(seen)
                    if r_ < len(buf): buf[r_] = S[perm[i + j]]
                continue
            if method == "klrep" and rb >= 1:
                xn, xp = x[:n], x[n:]; opt.zero_grad()
                loss = loss_fn(net(xn[:, :-1]), xn[:, 1:]); compute += 3 * n
                with torch.no_grad(): pb = F.softmax(base(xp[:, :-1]), -1); compute += len(xp)
                lq = F.log_softmax(net(xp[:, :-1]), -1); compute += 3 * len(xp)
                loss = loss + LAM * (pb * (torch.log(pb + 1e-12) - lq)).sum(-1).mean()
                loss.backward(); opt.step(); step += 1
                for j in range(n):
                    seen += 1; r_ = rng.integers(seen)
                    if r_ < len(buf): buf[r_] = S[perm[i + j]]
                continue
            logits = net(x[:, :-1]); loss = loss_fn(logits, x[:, 1:]); compute += 3 * len(x)
            if ema and step % sparse == 0:
                with torch.no_grad():
                    lp_ = net_ce = None
                    zp = ema_p(x[:, :-1]); zs = ema_s(x[:, :-1]); compute += 2 * len(x)
                    lp_ = loss_fn(zp, x[:, 1:]); ls_ = loss_fn(zs, x[:, 1:]); zt = zp if lp_ < ls_ else zs
                    pt = F.softmax(zt, -1)
                loss = loss + F.kl_div(F.log_softmax(logits, -1), pt, reduction="batchmean") / CTX * 1.0
            loss.backward(); opt.step(); step += 1
            if method == "crr":
                if step % 4 == 0:
                    with torch.no_grad(): lq = F.log_softmax(net(probe[:, :-1]), -1); compute += 8
                    kl = (p_probe.exp() * (p_probe - lq)).sum(-1).mean().item(); v = math.sqrt(max(2 * kl, 0.)); p_probe = lq
                    vlog.append(v); vhat = 0.9 * vhat + 0.1 * v
                kp = Kf(vhat / Om); ks = Kf(vhat / (Om * math.e))
            elif method == "fixed": kp, ks = af, as_
            if ema:
                with torch.no_grad():
                    set_flat(ema_p, (1 - kp) * flat(ema_p) + kp * flat(net)); set_flat(ema_s, (1 - ks) * flat(ema_s) + ks * flat(net))
            for j in range(n):  # reservoir over all seen sequences
                seen += 1; r = rng.integers(seen)
                if r < len(buf): buf[r] = S[perm[i + j]]
    model = ema_s if ema else net
    out = dict(method=method, seed=seed, replay=replay, Om=Om if method == "crr" else None, af=af if method == "fixed" else None,
               as_=as_ if method == "fixed" else None, sparse=sparse, compute_per_seq=compute / n_stream,
               vF_med=float(np.median(vlog)) if vlog else None, w_med=float(np.median(wlog)) if wlog else None)
    out["D0_bpb"] = bpb(model, ev["D0"]); out["D0_bpb_student"] = bpb(net, ev["D0"])
    out["dom_bpb"] = float(np.mean([bpb(model, ev[k]) for k in ("D1", "D2", "D3", "D4")]))
    out["dom_bpb_student"] = float(np.mean([bpb(net, ev[k]) for k in ("D1", "D2", "D3", "D4")]))
    return out

if __name__ == "__main__":
    if sys.argv[1] == "pretrain": pretrain(); sys.exit()
    m, seed, r = sys.argv[2], int(sys.argv[3]), float(sys.argv[4]); t0 = time.time()
    if m == "eq": o = run(m, seed, r, Om=float(sys.argv[5]))
    elif m == "klrep": o = run(m, seed, r)
    elif m == "crr": o = run(m, seed, r, Om=float(sys.argv[5]), sparse=int(sys.argv[6]) if len(sys.argv) > 6 else 1)
    elif m == "fixed": o = run(m, seed, r, af=float(sys.argv[5]), as_=float(sys.argv[6]))
    else: o = run(m, seed, r)
    o["sec"] = round(time.time() - t0); print(json.dumps(o), flush=True)

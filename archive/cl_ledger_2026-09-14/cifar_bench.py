"""crr_cl_cifar.py — PyTorch port of Clean_CRR/crr_cl_bench.py (methods: er, derpp, clser, crr_cls) on Split-CIFAR-10.
Usage: python crr_cl_cifar.py METHOD KIND SEED [Om] [d] [ap] [as] -> prints JSON line."""
import sys, json, math, pickle, time, numpy as np, torch, torch.nn as nn, torch.nn.functional as F
torch.set_num_threads(1)
def load():
    xs, ys = [], []
    for i in range(1, 6):
        b = pickle.load(open(f"/home/claude/data/cifar-10-batches-py/cifar-10-batches-py/data_batch_{i}", "rb"), encoding="bytes")
        xs.append(b[b"data"]); ys += b[b"labels"]
    t = pickle.load(open("/home/claude/data/cifar-10-batches-py/cifar-10-batches-py/test_batch", "rb"), encoding="bytes")
    X = np.concatenate(xs).reshape(-1, 3, 32, 32).astype(np.float32) / 255.; Y = np.array(ys)
    Xt = t[b"data"].reshape(-1, 3, 32, 32).astype(np.float32) / 255.; Yt = np.array(t[b"labels"])
    mu = X.mean((0, 2, 3), keepdims=True); sd = X.std((0, 2, 3), keepdims=True)
    return (X - mu) / sd, Y, (Xt - mu) / sd, Yt
Xtr, Ytr, Xte, Yte = load()
PROBE=torch.from_numpy(Xte[5000:5512])
import os
UNIT=os.environ.get('UNIT','diag'); VLOG=[]
PROBE=None
def kl_speed(p_old, net):
    with torch.no_grad(): p_new=F.softmax(net(PROBE),1)
    kl=(p_old*(torch.log(p_old+1e-12)-torch.log(p_new+1e-12))).sum(1).mean().item()
    return math.sqrt(max(2*kl,0.)), p_new
Kf = lambda v: (v / 2) * (math.sqrt(v * v + 4) - v)

class Net(nn.Module):
    def __init__(s):
        super().__init__()
        s.c1 = nn.Conv2d(3, 32, 3, padding=1); s.c2 = nn.Conv2d(32, 64, 3, padding=1)
        s.f1 = nn.Linear(64 * 8 * 8, 128); s.f2 = nn.Linear(128, 10)
    def forward(s, x):
        x = F.max_pool2d(F.relu(s.c1(x)), 2); x = F.max_pool2d(F.relu(s.c2(x)), 2)
        return s.f2(F.relu(s.f1(x.flatten(1))))
def flat(net): return torch.cat([p.detach().flatten() for p in net.parameters()])
def set_flat(net, v):
    i = 0
    for p in net.parameters():
        n = p.numel(); p.data.copy_(v[i:i + n].view_as(p)); i += n
def acc(net, X, Y):
    net.eval(); c = 0
    with torch.no_grad():
        for i in range(0, len(X), 500):
            c += (net(torch.from_numpy(X[i:i + 500])).argmax(1).numpy() == Y[i:i + 500]).sum()
    net.train(); return float(c / len(X))

def make_stream(rng, kind):
    tasks = [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]
    idx = {c: rng.permutation(np.where(Ytr == c)[0]) for c in range(10)}; ptr = {c: 0 for c in range(10)}
    visits = [(t, 2000) for t in tasks] if kind == "standard" else [(tasks[i % 5], 1000) for i in range(10)]
    xs, ys = [], []
    for (a, b), n in visits:
        ii = np.concatenate([idx[a][ptr[a]:ptr[a] + n // 2], idx[b][ptr[b]:ptr[b] + n // 2]]); ptr[a] += n // 2; ptr[b] += n // 2
        ii = rng.permutation(ii); xs.append(Xtr[ii]); ys.append(Ytr[ii])
    return np.concatenate(xs), np.concatenate(ys)

def run(method, kind, seed, Om=1.0, d=math.e, ap=0.99, as_=0.999, lr=0.05, B=500, bs=10, rb=10):
    rng = np.random.default_rng(seed); torch.manual_seed(seed)
    sx, sy = make_stream(rng, kind); net = Net(); opt = torch.optim.SGD(net.parameters(), lr=lr)
    ema_p, ema_s = Net(), Net(); ema_p.load_state_dict(net.state_dict()); ema_s.load_state_dict(net.state_dict())
    bufx = np.zeros((B, 3, 32, 32), np.float32); bufy = np.zeros(B, int); bufz = np.zeros((B, 10), np.float32); nb = 0; seen = 0
    Fd = torch.full((flat(net).numel(),), 1e-3); vhat = 0.0; VLOG.clear()
    with torch.no_grad(): p_probe=F.softmax(net(PROBE),1)
    for t in range(0, len(sy), bs):
        x = torch.from_numpy(sx[t:t + bs]); y = torch.from_numpy(sy[t:t + bs]); theta0 = flat(net)
        rx = ry = None
        if nb > 0 and method != "finetune":
            sel = rng.choice(nb, min(rb, nb), replace=False); rx = torch.from_numpy(bufx[sel]); ry = torch.from_numpy(bufy[sel])
        opt.zero_grad()
        if rx is None:
            loss = F.cross_entropy(net(x), y)
        elif method == "derpp":
            loss = F.cross_entropy(net(torch.cat([x, rx])), torch.cat([y, ry])) + 0.5 * F.mse_loss(net(rx), torch.from_numpy(bufz[sel]))
        elif method in ("clser", "crr_cls"):
            loss = F.cross_entropy(net(torch.cat([x, rx])), torch.cat([y, ry]))
            with torch.no_grad():
                lp = F.cross_entropy(ema_p(rx), ry); ls = F.cross_entropy(ema_s(rx), ry)
                zt = (ema_p if lp < ls else ema_s)(rx)
            loss = loss + 0.2 * F.mse_loss(net(rx), zt)
        else:
            loss = F.cross_entropy(net(torch.cat([x, rx])), torch.cat([y, ry]))
        loss.backward()
        g = torch.cat([p.grad.flatten() for p in net.parameters()])
        opt.step()
        if method == "crr_cls":
            Fd = 0.99 * Fd + 0.01 * (g ** 2) * len(y) ** 2
            dth = flat(net) - theta0; v = float(torch.sqrt((Fd * dth * dth).sum()))
            if UNIT=='kl': v,p_probe=kl_speed(p_probe,net)
            VLOG.append(v); vhat = 0.9 * vhat + 0.1 * v
            kp = Kf(vhat / Om); ks = Kf(vhat / (Om * d))
            with torch.no_grad():
                set_flat(ema_p, (1 - kp) * flat(ema_p) + kp * flat(net)); set_flat(ema_s, (1 - ks) * flat(ema_s) + ks * flat(net))
        elif method == "clser":
            with torch.no_grad():
                for e, a in ((ema_p, ap), (ema_s, as_)):
                    if rng.random() < 0.5: set_flat(e, a * flat(e) + (1 - a) * flat(net))
        with torch.no_grad(): z = net(x).numpy()
        for i in range(len(y)):
            seen += 1
            if nb < B: j = nb; nb += 1
            else:
                j = rng.integers(seen)
                if j >= B: continue
            bufx[j] = sx[t + i]; bufy[j] = sy[t + i]; bufz[j] = z[i]
    model = ema_s if method in ("clser", "crr_cls") else net
    return acc(model, Xte[:5000], Yte[:5000])

if __name__ == "__main__":
    method, kind, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
    Om = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0; d = float(sys.argv[5]) if len(sys.argv) > 5 else math.e
    ap = float(sys.argv[6]) if len(sys.argv) > 6 else 0.99; as_ = float(sys.argv[7]) if len(sys.argv) > 7 else 0.999
    t0 = time.time(); a = run(method, kind, seed, Om, d, ap, as_)
    print(json.dumps(dict(dataset='cifar10',unit=UNIT,method=method, kind=kind, seed=seed, Om=Om, d=d, acc=a, vF_med=float(np.median(VLOG)) if VLOG else None, sec=round(time.time() - t0))), flush=True)

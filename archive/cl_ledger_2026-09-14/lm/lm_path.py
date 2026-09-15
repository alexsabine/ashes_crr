"""T1: path length vs endpoint. python lm_path.py LR SCHED SEED -> JSON"""
import sys, json, math, torch, torch.nn.functional as F, numpy as np
import lm_bench as L
lr, sched, seed = float(sys.argv[1]), sys.argv[2], int(sys.argv[3])
C = L.corpus(); ev = {k: L.seqs(v[1]) for k, v in C.items()}
torch.manual_seed(seed); g = torch.Generator().manual_seed(seed)
net = L.LM(); net.load_state_dict(torch.load("/home/claude/lm/pretrained.pt")); base = L.LM(); base.load_state_dict(net.state_dict())
opt = torch.optim.AdamW(net.parameters(), lr)
S1 = L.seqs(C["D1"][0]); S0 = L.seqs(C["D0"][0])
pr_new = S1[torch.randperm(len(S1), generator=g)[:8]]; pr_old = S0[torch.randperm(len(S0), generator=g)[:8]]
perm = torch.randperm(len(S1), generator=g)
def lp(m, x):
    with torch.no_grad(): return F.log_softmax(m(x[:, :-1]), -1)
def kl(la, lb): return (la.exp() * (la - lb)).sum(-1).mean().item()
p_new, p_old = lp(net, pr_new), lp(net, pr_old); b_new, b_old = p_new.clone(), p_old.clone()
C_new = C_old = 0.; f0 = L.bpb(net, ev["D0"])
for t in range(150):
    x = S1[perm[(t * 16) % len(S1):(t * 16) % len(S1) + 16]]
    for gp in opt.param_groups: gp["lr"] = lr * (3.0 if (sched == "saw" and t % 10 == 0) else (1/3 if sched == "saw" else 1.0))
    opt.zero_grad(); L.loss_fn(net(x[:, :-1]), x[:, 1:]).backward(); opt.step()
    q_new, q_old = lp(net, pr_new), lp(net, pr_old)
    C_new += math.sqrt(max(2 * kl(p_new, q_new), 0)); C_old += math.sqrt(max(2 * kl(p_old, q_old), 0)); p_new, p_old = q_new, q_old
E_new = kl(b_new, p_new); E_old = kl(b_old, p_old)
print(json.dumps(dict(lr=lr, sched=sched, seed=seed, F=L.bpb(net, ev["D0"]) - f0, D1_bpb=L.bpb(net, ev["D1"]),
      E_new=E_new, E_old=E_old, C_new=C_new, C_old=C_old, Cstar_new=math.sqrt(2 * E_new), Cstar_old=math.sqrt(2 * E_old))), flush=True)

"""Count the EQ2 runs whose parameters were not finite at the end (they score 0 and stay in
every mean, as pre-registered), per carrier, regime and arm family. Reads the committed
results files; prints one row per (carrier, regime, method, mode)."""
import glob, json, sys
from collections import Counter
files = sys.argv[1:] or sorted(glob.glob("runs/eq2/results_*.jsonl"))
tot = Counter(); nf = Counter()
for f in files:
    for l in open(f):
        if not l.startswith("{"): continue
        r = json.loads(l)
        if "acc" not in r: continue
        k = (r["dataset"], r["regime"], r["method"], r["mode"]); tot[k] += 1; nf[k] += (not r["finite"])
print(f"{'carrier':14s} {'regime':6s} {'method':8s} {'mode':10s} {'runs':>5s} {'non-finite':>10s}")
for k in sorted(tot):
    if nf[k]: print(f"{k[0]:14s} {k[1]:6s} {k[2]:8s} {k[3]:10s} {tot[k]:5d} {nf[k]:10d}")
print(f"\ntotal runs {sum(tot.values())}, non-finite {sum(nf.values())} (all kept and scored as 0, per prereg quality gate)")

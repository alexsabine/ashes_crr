R=results_adv.jsonl; E="DATASET=kmnist REPLAY=0.2 WCAP=50"
for s in 0 1 2; do
 for w in 1 2 4 8; do env $E RATIO=fixed python3 mlp_bench.py eq $w $s >> $R; done
 env $E RATIO=mega SMOOTH=0 python3 mlp_bench.py eq 1 $s >> $R
 env $E RATIO=mega SMOOTH=0.98 python3 mlp_bench.py eq 1 $s >> $R
 for om in 0.5 0.71 1 1.41 2; do
  env $E RATIO=ema SMOOTH=0.98 LR=0.0125 python3 mlp_bench.py eq $om $s >> $R
  env $E RATIO=ema SMOOTH=0.98 LR=0.2 python3 mlp_bench.py eq $om $s >> $R
  env $E RATIO=ema SMOOTH=0.98 BS=5 python3 mlp_bench.py eq $om $s >> $R
  env $E RATIO=ema SMOOTH=0.98 BS=20 python3 mlp_bench.py eq $om $s >> $R
 done
 for tl in 1000 2000 4000; do for b in 0.9 0.95 0.98 0.99 0.995; do env $E RATIO=ema SMOOTH=$b TASKLEN=$tl python3 mlp_bench.py eq 1 $s >> $R; done; done
done; echo ADV_DONE >> $R

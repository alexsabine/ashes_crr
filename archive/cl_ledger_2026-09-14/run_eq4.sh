R=results_eq4.jsonl
for s in 0 1 2; do
 for sm in 0.9 0.95 0.995; do DATASET=kmnist REPLAY=0.2 RATIO=ema SMOOTH=$sm WCAP=50 python3 mlp_bench.py eq 1 $s >> $R; done
 for om in 0.71 1 1.41; do DATASET=kmnist REPLAY=0.2 RATIO=ema SMOOTH=0.98 METRIC=euclid WCAP=50 python3 mlp_bench.py eq $om $s >> $R; done
done; echo EQ4_DONE >> $R

R=results_eq.jsonl
for s in 0 1 2; do
 for r in 0.2 0.5; do for om in 0.25 0.5 1 2 4; do DATASET=kmnist REPLAY=$r RATIO=unbiased SMOOTH=0.98 WCAP=50 python3 mlp_bench.py eq $om $s >> $R; done; done
 DATASET=kmnist REPLAY=0.2 python3 mlp_bench.py er 1 $s >> $R
 DATASET=kmnist REPLAY=0.2 RATIO=unbiased SMOOTH=0.98 WCAP=50 python3 mlp_bench.py eq 1 $s recurring >> $R
 DATASET=kmnist REPLAY=1.0 python3 mlp_bench.py er 1 $s recurring >> $R
 DATASET=kmnist REPLAY=0.2 python3 mlp_bench.py er 1 $s recurring >> $R
done; echo EQ_DONE >> $R

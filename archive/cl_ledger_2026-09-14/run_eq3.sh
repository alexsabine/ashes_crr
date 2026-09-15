R=results_eq3.jsonl
for ds in kmnist mnist fmnist; do for s in 0 1 2; do
 for r in 0.1 0.2; do for om in 0.5 0.71 1 1.41 2; do DATASET=$ds REPLAY=$r RATIO=ema SMOOTH=0.98 WCAP=50 python3 mlp_bench.py eq $om $s >> $R; done; done
 DATASET=$ds REPLAY=0.2 RATIO=ema SMOOTH=0.98 WCAP=50 python3 mlp_bench.py eq 1 $s recurring >> $R
 for r in 0.1 0.2 0.5 1.0; do DATASET=$ds REPLAY=$r python3 mlp_bench.py er 1 $s >> $R; done
 for r in 0.2 1.0; do DATASET=$ds REPLAY=$r python3 mlp_bench.py er 1 $s recurring >> $R; done
done; done; echo EQ3_DONE >> $R

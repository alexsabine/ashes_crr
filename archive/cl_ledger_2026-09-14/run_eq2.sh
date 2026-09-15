R=results_eq2.jsonl
for ds in mnist fmnist; do for s in 0 1 2; do
 for om in 0.5 1 2 4; do DATASET=$ds REPLAY=0.2 RATIO=unbiased SMOOTH=0.98 WCAP=50 python3 mlp_bench.py eq $om $s >> $R; done
 for r in 0.2 1.0; do DATASET=$ds REPLAY=$r python3 mlp_bench.py er 1 $s >> $R; done
done; done; echo EQ2_DONE >> $R

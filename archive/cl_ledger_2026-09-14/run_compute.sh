ds=kmnist; OM=8.0
for s in 0 1 2; do
 for r in 0 0.05 0.1 0.25 0.5 1.0; do DATASET=$ds REPLAY=$r python3 mlp_bench.py er 1.0 $s >> results_compute.jsonl; done
 for r in 0 0.05 0.25 1.0; do DATASET=$ds UNIT=kl REPLAY=$r DISTIL_CUR=1 python3 mlp_bench.py crr_cls $OM $s >> results_compute.jsonl; done
 for r in 0 0.05; do DATASET=$ds REPLAY=$r DISTIL_CUR=1 AP=0.8 AS=0.95 python3 mlp_bench.py clser 1.0 $s >> results_compute.jsonl; done
 DATASET=$ds UNIT=kl REPLAY=0.05 DISTIL_CUR=1 SPARSE=4 python3 mlp_bench.py crr_cls $OM $s >> results_compute.jsonl
done; echo DONE >> results_compute.jsonl

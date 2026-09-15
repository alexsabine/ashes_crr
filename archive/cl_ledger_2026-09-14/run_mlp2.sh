for ds in mnist fmnist kmnist; do for om in 8.0 16.0 32.0; do for s in 0 1 2; do
    DATASET=$ds UNIT=kl python3 mlp_bench.py $om $s >> results_mlp_ext.jsonl
done; done; done; echo DONE >> results_mlp_ext.jsonl

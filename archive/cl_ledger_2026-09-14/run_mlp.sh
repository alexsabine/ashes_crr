for ds in mnist fmnist kmnist; do
  DATASET=$ds UNIT=diag python3 mlp_bench.py 1.0 0 >> results_mlp.jsonl
  for om in 0.25 0.5 1.0 2.0 4.0; do for s in 0 1 2; do
    DATASET=$ds UNIT=kl python3 mlp_bench.py $om $s >> results_mlp.jsonl
  done; done
done
echo DONE >> results_mlp.jsonl

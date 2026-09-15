while ! grep -q ADV_DONE results_adv.jsonl; do sleep 15; done
R=results_adv2.jsonl
for s in 0 1 2; do for ds in mnist fmnist kmnist; do for w in 0.5 0.71 1 1.41 2; do DATASET=$ds REPLAY=0.2 RATIO=fixed python3 mlp_bench.py eq $w $s >> $R; done; done
 for lr in 0.0125 0.2; do for w in 0.71 1 1.41; do DATASET=kmnist REPLAY=0.2 RATIO=fixed LR=$lr python3 mlp_bench.py eq $w $s >> $R; done; done
 for w in 0.71 1 1.41; do DATASET=kmnist REPLAY=0.1 RATIO=fixed python3 mlp_bench.py eq $w $s >> $R; done
done; echo ADV2_DONE >> $R

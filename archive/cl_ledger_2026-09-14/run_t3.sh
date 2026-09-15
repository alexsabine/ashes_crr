while ! grep -q PATH_DONE /home/claude/lm/results_path.jsonl 2>/dev/null; do sleep 10; done
R=results_t3.jsonl
for s in 0 1 2; do for B in 500 5000; do
  DATASET=kmnist REPLAY=1.0 BUF=$B python3 mlp_bench.py er 1 $s >> $R
  DATASET=kmnist REPLAY=0.2 RATIO=ema SMOOTH=0.98 BUF=$B python3 mlp_bench.py eq 1 $s >> $R
  DATASET=kmnist REPLAY=0.2 RATIO=fixed BUF=$B python3 mlp_bench.py eq 1 $s >> $R
done; done; echo T3_DONE >> $R

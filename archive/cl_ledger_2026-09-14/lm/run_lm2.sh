cd /home/claude/lm
while ! grep -q SWEEP_DONE results_lm.jsonl; do sleep 10; done
R=results_lm_h2h.jsonl
for s in 0 1 2; do
  for r in 0.05 0.25 0.5; do python3 lm_bench.py run er $s $r >> $R; done
  python3 lm_bench.py run crr $s 0.05 16 >> $R
  python3 lm_bench.py run crr $s 0.05 8 >> $R
  python3 lm_bench.py run fixed $s 0.05 0.03 0.003 >> $R
  python3 lm_bench.py run crr $s 0 16 >> $R
  python3 lm_bench.py run crr $s 0.05 16 4 >> $R
done; echo H2H_DONE >> $R

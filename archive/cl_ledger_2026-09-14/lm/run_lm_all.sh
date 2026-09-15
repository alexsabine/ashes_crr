cd /home/claude/lm
while ! grep -q EQ3_DONE /home/claude/unit/results_eq3.jsonl 2>/dev/null; do sleep 20; done
R=results_lm_h2h.jsonl
for s in 0 1 2; do
  for r in 0.05 0.25 0.5; do python3 lm_bench.py run er $s $r >> $R; done
  python3 lm_bench.py run crr $s 0.05 16 >> $R
  python3 lm_bench.py run fixed $s 0.05 0.03 0.003 >> $R
  python3 lm_bench.py run crr $s 0.05 16 4 >> $R
  for r in 0.1 0.25; do for om in 0.5 1 2; do python3 lm_bench.py run eq $s $r $om >> results_lm_eq.jsonl; done; done
done; echo H2H_DONE >> $R; echo LMEQ_DONE >> results_lm_eq.jsonl

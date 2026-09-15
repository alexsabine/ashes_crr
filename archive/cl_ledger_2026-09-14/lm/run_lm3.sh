cd /home/claude/lm
while ! grep -q H2H_DONE results_lm_h2h.jsonl 2>/dev/null; do sleep 30; done
R=results_lm_eq.jsonl
for s in 0 1 2; do for r in 0.1 0.25; do for om in 0.5 1 2; do python3 lm_bench.py run eq $s $r $om >> $R; done; done; done
echo LMEQ_DONE >> $R

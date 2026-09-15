cd /home/claude/lm
python3 lm_bench.py pretrain > pretrain.log 2>&1
R=results_lm.jsonl
for r in 0 0.1 0.25 0.5; do python3 lm_bench.py run er 0 $r >> $R; done
for om in 4 16 64; do python3 lm_bench.py run crr 0 0.05 $om >> $R; done
for a in "0.01 0.001" "0.03 0.003" "0.1 0.01"; do python3 lm_bench.py run fixed 0 0.05 $a >> $R; done
echo SWEEP_DONE >> $R

R=results_t2.jsonl
for s in 0 1; do
  python3 lm_bench.py run er $s 0.25 >> $R
  LAM=10 python3 lm_bench.py run klrep $s 0.25 >> $R
  python3 lm_bench.py run eq $s 0.1 1 >> $R
  python3 lm_bench.py run eq $s 0.25 1 >> $R
  python3 lm_bench.py run er $s 0.5 >> $R
done; echo T2_DONE >> $R

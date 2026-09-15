for s in 0 1; do for lam in 1 3; do LAM=$lam python3 lm_bench.py run klrep $s 0.25 >> results_t2b.jsonl; done; done; echo DONE >> results_t2b.jsonl

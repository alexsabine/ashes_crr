for s in 0 1; do for sc in const saw; do for lr in 2e-4 5e-4 1e-3 2e-3 5e-3; do python3 lm_path.py $lr $sc $s >> results_path.jsonl; done; done; done; echo PATH_DONE >> results_path.jsonl

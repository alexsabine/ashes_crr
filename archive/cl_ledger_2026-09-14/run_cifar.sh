cd /home/claude/data
while ! grep -q H2H_DONE /home/claude/lm/results_lm_h2h.jsonl 2>/dev/null; do sleep 30; done
tar xzf cifar.tgz
cd /home/claude/unit
UNIT=diag python3 cifar_bench.py crr_cls standard 0 1.0 >> results_cifar.jsonl
for om in 1.0 4.0 8.0 16.0 32.0; do for s in 0 1 2; do UNIT=kl python3 cifar_bench.py crr_cls standard $s $om >> results_cifar.jsonl; done; done
echo DONE >> results_cifar.jsonl

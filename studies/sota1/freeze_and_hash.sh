#!/bin/bash
# SOTA1 step 3 (CLAUDE.md §8, R2): copy the frozen instrument, hash the prereg folder plus the frozen folder, stamp.
# Run once, from the repository root, after prereg/sota1/ is complete. Nothing in prereg/sota1 or runs/sota1/frozen may
# change afterwards.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
test ! -e runs/sota1/frozen || { echo "runs/sota1/frozen exists: refusing to refreeze"; exit 1; }
mkdir -p runs/sota1/frozen/env
cp -r studies/sota1/vendor/mammoth runs/sota1/frozen/mammoth
find runs/sota1/frozen/mammoth -name __pycache__ -prune -exec rm -rf {} +
rm -rf runs/sota1/frozen/mammoth/data runs/sota1/frozen/mammoth/checkpoints
cp studies/sota1/vendor/MODIFICATIONS.md runs/sota1/frozen/
cp studies/sota1/sota1_run.py runs/sota1/frozen/
cp studies/sota1/env/pyproject.toml studies/sota1/env/uv.lock runs/sota1/frozen/env/
cp theory/CRR.md runs/sota1/frozen/
cp studies/sota1/sota1_score.py prereg/sota1/
( cd prereg/sota1 && find . ../../runs/sota1/frozen -type f ! -name HASH.txt ! -name 'HASH.txt.ots*' -print0 \
    | sort -z | xargs -0 sha256sum > HASH.txt )
echo "files hashed: $(wc -l < prereg/sota1/HASH.txt)"
uv run ots stamp prereg/sota1/HASH.txt 2>&1 | tee runs/sota1/ots_attempt.txt
ls -la prereg/sota1/HASH.txt.ots

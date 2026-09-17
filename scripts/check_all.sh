#!/usr/bin/env bash
# Thin orchestrator (R9/R11): sequences the standing checks. No logic beyond
# sequencing — each line is one documented command; the provenance header
# is the environment pin the CI log records.
set -euo pipefail

echo "== provenance =="
echo "commit: $(git rev-parse HEAD)"
if command -v sha256sum >/dev/null 2>&1; then
  echo "uv.lock sha256: $(sha256sum uv.lock | cut -d' ' -f1)"
else
  echo "uv.lock sha256: $(shasum -a 256 uv.lock | cut -d' ' -f1)"
fi
uv run python --version
echo

echo "== environment =="
uv sync --frozen
uv lock --check
echo

echo "== tests =="
uv run pytest tests
echo

echo "== theory checks =="
uv run python theory/checks/verify_math.py
uv run python theory/checks/verify_scope_math.py
uv run python theory/checks/verify_spec_math.py
uv run python theory/retrodictions/crr_retrodictions.py | cmp - theory/retrodictions/crr_retrodictions.txt && echo 'retrodiction battery byte-identical to the committed output'
uv run python theory/retrodictions/sharp_claims.py | cmp - theory/retrodictions/sharp_claims.txt && echo 'external SHARP claims re-derivation byte-identical to the committed output'
uv run python theory/retrodictions/bio_retrodictions.py | cmp - theory/retrodictions/bio_retrodictions.txt && echo 'biological battery byte-identical to the committed output'
uv run python theory/retrodictions/ei_networks.py | cmp - theory/retrodictions/ei_networks.txt && echo 'E-I network battery byte-identical to the committed output'
uv run python theory/retrodictions/driven_systems.py | cmp - theory/retrodictions/driven_systems.txt && echo 'driven-systems battery byte-identical to the committed output'
uv run python theory/retrodictions/cognitive_collective.py | cmp - theory/retrodictions/cognitive_collective.txt && echo 'cognitive-collective battery byte-identical to the committed output'
uv run python theory/retrodictions/wild_systems.py | cmp - theory/retrodictions/wild_systems.txt && echo 'wild-systems battery byte-identical to the committed output'
uv run python theory/retrodictions/twenty_systems.py | cmp - theory/retrodictions/twenty_systems.txt && echo 'twenty-systems battery byte-identical to the committed output'
uv run python theory/retrodictions/emptiness.py | cmp - theory/retrodictions/emptiness.txt && echo 'emptiness (CRR at zero) battery byte-identical to the committed output'
uv run python crr_retrodictions.py > /tmp/retro2.txt && diff <(grep -o 'verdict [A-Z]*' /tmp/retro2.txt) <(grep -o 'verdict [A-Z]*' runs/phaseA/crr_retrodictions.txt) && echo 'second retrodiction battery (PR #24): all 40 verdicts reproduced (the Rossler row drifts at the third decimal across Python patch versions, as the chaotic gate rows do)'
echo

echo "== gates =="
uv run python -m crr.surrogates.gate L5
uv run python -m crr.surrogates.gate CUT
uv run python -m crr.surrogates.gate T1
uv run python -m crr.surrogates.gate EQ
uv run python -m crr.surrogates.gate EQ2
echo

echo "== all checks done =="

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
uv run python theory/checks/omega_sweeps.py | cmp - theory/checks/omega_sweeps.txt && echo 'omega sweeps (Bayes, quadratic, Kalman) byte-identical to the committed output'
uv run python theory/checks/omega_vs_methods.py | cmp - theory/checks/omega_vs_methods.txt && echo 'omega vs methods (cross-verification battery) byte-identical to the committed output'
uv run python theory/checks/omega_reprocessed.py 2>/dev/null | cmp - theory/checks/omega_reprocessed.txt && echo 'H-EQ reprocessed (scale/shape, bound, constraint, poison, metric, Adam) byte-identical to the committed output'
uv run python theory/checks/fed_heterogeneous_v1.py 2>/dev/null | cmp - theory/checks/fed_heterogeneous_v1.txt && echo 'FED Phase-A first run byte-identical to the committed output'
uv run python theory/checks/fed_heterogeneous.py 2>/dev/null | cmp - theory/checks/fed_heterogeneous.txt && echo 'FED Phase-A gate (CLOSED) byte-identical to the committed output'
uv run python ontology/checks/tense_gate.py 2>/dev/null | cmp - ontology/checks/tense_gate.txt && echo 'tense test byte-identical to the committed output'
uv run python ontology/checks/self_model.py 2>/dev/null | cmp - ontology/checks/self_model.txt && echo 'self-representation test byte-identical to the committed output'
uv run python theory/retrodictions/crr_retrodictions.py | cmp - theory/retrodictions/crr_retrodictions.txt && echo 'retrodiction battery byte-identical to the committed output'
uv run python theory/retrodictions/sharp_claims.py | cmp - theory/retrodictions/sharp_claims.txt && echo 'external SHARP claims re-derivation byte-identical to the committed output'
uv run python theory/retrodictions/bio_retrodictions.py | cmp - theory/retrodictions/bio_retrodictions.txt && echo 'biological battery byte-identical to the committed output'
uv run python theory/retrodictions/ei_networks.py | cmp - theory/retrodictions/ei_networks.txt && echo 'E-I network battery byte-identical to the committed output'
uv run python theory/retrodictions/driven_systems.py | cmp - theory/retrodictions/driven_systems.txt && echo 'driven-systems battery byte-identical to the committed output'
uv run python theory/retrodictions/cognitive_collective.py | cmp - theory/retrodictions/cognitive_collective.txt && echo 'cognitive-collective battery byte-identical to the committed output'
uv run python theory/retrodictions/wild_systems.py | cmp - theory/retrodictions/wild_systems.txt && echo 'wild-systems battery byte-identical to the committed output'
uv run python theory/retrodictions/twenty_systems.py | cmp - theory/retrodictions/twenty_systems.txt && echo 'twenty-systems battery byte-identical to the committed output'
uv run python theory/retrodictions/emptiness.py | cmp - theory/retrodictions/emptiness.txt && echo 'emptiness (CRR at zero) battery byte-identical to the committed output'
uv run python theory/retrodictions/shannon.py | cmp - theory/retrodictions/shannon.txt && echo 'Shannon battery byte-identical to the committed output'
uv run python theory/retrodictions/loop_gravity.py | cmp - theory/retrodictions/loop_gravity.txt && echo 'loop-gravity battery byte-identical to the committed output'
uv run python theory/retrodictions/synthesis.py | cmp - theory/retrodictions/synthesis.txt && echo 'synthesis battery byte-identical to the committed output'
for f in theory/retrodictions/synthesis_batches/batch_*.py; do [ -e "$f" ] || continue; uv run python "$f" | cmp - "${f%.py}.txt" || exit 1; done && echo 'synthesis batches byte-identical to the committed outputs'
uv run python theory/retrodictions/synthesis_batches/build_queue.py | cmp - theory/retrodictions/synthesis_batches/QUEUE.md && echo 'synthesis queue reproduces from the pinned batteries'
uv run python docs/pedagogy/build_elegance_ledger.py | cmp - docs/pedagogy/ELEGANCE_LEDGER.md && echo 'elegance ledger reproduces from the pinned synthesis outputs'
uv run python ontology/checks/cut_on_a_machine.py | cmp - ontology/checks/cut_on_a_machine.txt && echo 'ontology check (the cut on a machine) byte-identical to the committed output'
uv run python ontology/checks/turing_safety_ingression.py | cmp - ontology/checks/turing_safety_ingression.txt && echo 'ontology battery (Turing systems, AI safety, ingression) byte-identical to the committed output'
uv run python ontology/checks/genesis_from_emptiness.py | cmp - ontology/checks/genesis_from_emptiness.txt && echo 'ontology exploratory check (genesis from emptiness) byte-identical to the committed output'
uv run python ontology/checks/delta_now.py 2>/dev/null | cmp - ontology/checks/delta_now.txt && echo 'ontology check (delta(Now) and the edge) byte-identical to the committed output'
uv run python runs/eq3/frozen/eq3_score.py smoke | cmp - prereg/eq3/smoke.txt && echo 'EQ3 frozen scorer smoke byte-identical to the committed output'
uv run python runs/eq3/frozen/eq3_score.py smokefull --out /tmp/eq3_smokefull.jsonl 2>/dev/null | cmp - prereg/eq3/smokefull.txt && echo 'EQ3 frozen scorer end-to-end smoke byte-identical to the committed output'
uv run python runs/eq4/frozen/eq4_score.py smoke | cmp - prereg/eq4/smoke.txt && echo 'EQ4 frozen scorer smoke byte-identical to the committed output'
uv run python runs/eq4/frozen/eq4_score.py smokefull --out /tmp/eq4_smokefull.jsonl 2>/dev/null | cmp - prereg/eq4/smokefull.txt && echo 'EQ4 frozen scorer end-to-end smoke byte-identical to the committed output'
uv run python runs/bayes1/frozen/bayes1_score.py gate 2>/dev/null | cmp - prereg/bayes1/gate_BAYES.txt && echo 'BAYES-1 frozen gate byte-identical to the committed output'
uv run python runs/bayes1/frozen/bayes1_score.py smoke 2>/dev/null | cmp - prereg/bayes1/smoke.txt && echo 'BAYES-1 frozen scorer smoke byte-identical to the committed output'
uv run python runs/bayes1/frozen/bayes1_score.py smokefull --out /tmp/bayes1_smokefull.jsonl 2>/dev/null | cmp - prereg/bayes1/smokefull.txt && echo 'BAYES-1 frozen scorer end-to-end smoke byte-identical to the committed output'
uv run python runs/t1x/frozen/t1x_score.py smoke 2>/dev/null | cmp - prereg/t1x/smoke.txt && echo 'T1x frozen scorer smoke byte-identical to the committed output'
uv run python runs/t1x/frozen/t1x_score.py smokefull --out /tmp/t1x_smokefull.jsonl 2>/dev/null | cmp - prereg/t1x/smokefull.txt && echo 'T1x frozen scorer end-to-end smoke byte-identical to the committed output'
uv run python runs/t1x2/frozen/t1x2_score.py smoke 2>/dev/null | cmp - prereg/t1x2/smoke.txt && echo 'T1x2 frozen scorer smoke byte-identical to the committed output'
uv run python runs/t1x2/frozen/t1x2_score.py smokefull --out /tmp/t1x2_smokefull.jsonl 2>/dev/null | cmp - prereg/t1x2/smokefull.txt && echo 'T1x2 frozen scorer end-to-end smoke byte-identical to the committed output'
uv run python Continuous_Learning/build/make_figures.py 2>/dev/null | cmp - Continuous_Learning/figures/figures.txt && echo 'Continuous Learning figure numbers byte-identical to the committed output'
uv run python Continuous_Learning/build/build_pdf.py > /dev/null 2>&1 && echo 'Continuous Learning PDF rebuilds'
uv run python crr_retrodictions.py > /tmp/retro2.txt && diff <(grep -o 'verdict [A-Z]*' /tmp/retro2.txt) <(grep -o 'verdict [A-Z]*' runs/phaseA/crr_retrodictions.txt) && echo 'second retrodiction battery (PR #24): all 40 verdicts reproduced (the Rossler row drifts at the third decimal across Python patch versions, as the chaotic gate rows do)'
echo

echo "== gates =="
uv run python -m crr.surrogates.gate L5
uv run python -m crr.surrogates.gate CUT
uv run python -m crr.surrogates.gate T1
uv run python -m crr.surrogates.gate EQ
uv run python -m crr.surrogates.gate EQ2
uv run python -m crr.surrogates.gate EQB
uv run python -m crr.surrogates.gate EQBM
echo

echo "== all checks done =="

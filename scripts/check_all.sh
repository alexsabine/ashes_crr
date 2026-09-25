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
uv run python ontology/checks/off_switch.py 2>/dev/null | cmp - ontology/checks/off_switch.txt && echo 'off-switch test byte-identical to the committed output'
uv run python AI_Safety/checks/exact_mdp.py 2>/dev/null | cmp - AI_Safety/checks/exact_mdp.txt && echo 'AI safety exact_mdp byte-identical to the committed output'
uv run python AI_Safety/checks/off_switch_game.py 2>/dev/null | cmp - AI_Safety/checks/off_switch_game.txt && echo 'AI safety off_switch_game byte-identical to the committed output'
uv run python AI_Safety/checks/sensitivity.py 2>/dev/null | cmp - AI_Safety/checks/sensitivity.txt && echo 'AI safety sensitivity byte-identical to the committed output'
uv run python AI_Safety/checks/timecourse.py 2>/dev/null | cmp - AI_Safety/checks/timecourse.txt && echo 'AI safety timecourse byte-identical to the committed output'
uv run python AI_Safety/checks/combined.py 2>/dev/null | cmp - AI_Safety/checks/combined.txt && echo 'AI safety combined byte-identical to the committed output'
uv run python AI_Safety/checks/scale.py 2>/dev/null | cmp - AI_Safety/checks/scale.txt && echo 'AI safety scale byte-identical to the committed output'
uv run python AI_Safety/checks/self_through_time.py 2>/dev/null | cmp - AI_Safety/checks/self_through_time.txt && echo 'AI safety self-through-time (exact) byte-identical to the committed output'
uv run python AI_Safety/checks/continual_safety.py 2>/dev/null | cmp - AI_Safety/checks/continual_safety.txt && echo 'AI safety safe-and-continual byte-identical to the committed output'
uv run python Safe_and_Continual/checks/roundoff_audit.py 2>/dev/null | cmp - Safe_and_Continual/checks/roundoff_audit.txt && echo 'Safe_and_Continual round-off audit byte-identical to the committed output'
uv run python Safe_and_Continual/build/make_figures.py 2>/dev/null | cmp - Safe_and_Continual/figures/figures.txt && echo 'Safe_and_Continual figure numbers byte-identical to the committed output'
uv run python studies/scl1/scl1_score.py math 2>/dev/null | cmp - Safe_and_Continual/checks/scl1_math.txt && echo 'SCL1 mathematical checks byte-identical to the committed output'
uv run python runs/scl1/frozen/scl1_score.py gate 2>/dev/null | cmp - prereg/scl1/gate_SCL.txt && echo 'SCL1 gate byte-identical to the committed output'
uv run python runs/scl2/frozen/scl2_score.py gate 2>/dev/null | cmp - prereg/scl2/gate_SCL2.txt && echo 'SCL2 gate byte-identical to the committed output'
uv run python runs/scl2/counts.py 2>/dev/null | cmp - runs/scl2/counts.txt && echo 'SCL2 counts byte-identical to the committed output'
uv run python runs/scl3/frozen/scl3_score.py gate 2>/dev/null | cmp - prereg/scl3/gate_SCL3.txt && echo 'SCL3 gate byte-identical to the committed output'
uv run python runs/scl3/counts.py 2>/dev/null | cmp - runs/scl3/counts.txt && echo 'SCL3 counts byte-identical to the committed output'
uv run python AI_Safety/build/make_figures.py 2>/dev/null | cmp - AI_Safety/figures/figures.txt && echo 'AI safety figure numbers byte-identical to the committed output'
uv run python AI_Safety/build/build_pdf.py > /dev/null 2>&1 && echo 'AI safety PDF rebuilds'
uv run python "Alexander Plan/model/projections.py" 2>/dev/null | cmp - "Alexander Plan/model/projections.txt" && echo 'Alexander Plan projections byte-identical to the committed output'
uv run python "Alexander Plan/model/cl_patent.py" 2>/dev/null | cmp - "Alexander Plan/model/cl_patent.txt" && echo 'Alexander Plan continual-learning and patent model byte-identical to the committed output'
uv run python "Alexander Plan/build/make_figures.py" 2>/dev/null | cmp - "Alexander Plan/figures/figures.txt" && echo 'Alexander Plan figure numbers byte-identical to the committed output'
uv run python "Alexander Plan/build/build_pdf.py" > /dev/null 2>&1 && echo 'Alexander Plan PDF rebuilds'
uv run python Epistemic_Review/checks/ladder.py 2>/dev/null | cmp - Epistemic_Review/checks/ladder.txt && echo 'epistemic ladder byte-identical to the committed output'
uv run python Epistemic_Review/build/make_figures.py 2>/dev/null | cmp - Epistemic_Review/figures/figures.txt && echo 'Epistemic Review figure numbers byte-identical to the committed output'
uv run python Epistemic_Review/build/build_pdf.py > /dev/null 2>&1 && echo 'Epistemic Review PDF rebuilds'
uv run python Continuous_Learning/checks/adam_checks.py 2>/dev/null | cmp - Continuous_Learning/checks/adam_checks.txt && echo 'Adam checks A1-A8 byte-identical to the committed output'
uv run python Continuous_Learning/checks/adam_checks_2.py 2>/dev/null | cmp - Continuous_Learning/checks/adam_checks_2.txt && echo 'Adam follow-up B1-B3 byte-identical to the committed output'
uv run python Continuous_Learning/checks/adam_checks_3.py 2>/dev/null | cmp - Continuous_Learning/checks/adam_checks_3.txt && echo 'Adam follow-up B4-B5 byte-identical to the committed output'
uv run python Continuous_Learning/checks/pareto_identities.py 2>/dev/null | cmp - Continuous_Learning/checks/pareto_identities.txt && echo 'Pareto identities (Omega = 1 vs MGDA, IMTL-G) byte-identical to the committed output'
uv run python Continuous_Learning/build/build_adam_pdf.py > /dev/null 2>&1 && echo 'Adam and prior-art PDF rebuilds'
uv run python Continuous_Learning/build/build_frontier_pdf.py > /dev/null 2>&1 && echo 'Frontier bottlenecks PDF rebuilds'
uv run python Adam_SGD/checks/assumptions.py 2>/dev/null | cmp - Adam_SGD/checks/assumptions.txt && echo 'Adam_SGD assumption audit byte-identical to the committed output'
uv run python Adam_SGD/checks/drift_battery.py 2>/dev/null | cmp - Adam_SGD/checks/drift_battery.txt && echo 'Adam_SGD drifting-world battery (Declaration 2) byte-identical to the committed output'
uv run python Adam_SGD/checks/drift_battery_2.py 2>/dev/null | cmp - Adam_SGD/checks/drift_battery_2.txt && echo 'Adam_SGD redesigned battery (Declaration 3) byte-identical to the committed output'
uv run python Adam_SGD/checks/mechanism.py 2>/dev/null | cmp - Adam_SGD/checks/mechanism.txt && echo 'Adam_SGD mechanism check (Declaration 4) byte-identical to the committed output'
uv run python Adam_SGD/build/build_pdf.py > /dev/null 2>&1 && echo 'Adam_SGD PDF rebuilds'
uv run python Rupture_Detection/checks/rupture_checks.py 2>/dev/null | cmp - Rupture_Detection/checks/rupture_checks.txt && echo 'rupture-detector battery byte-identical to the committed output'
uv run python Regeneration_Law/checks/math_checks.py 2>/dev/null | cmp - Regeneration_Law/checks/math_checks.txt && echo 'regeneration law mathematical checks (Declaration 1) byte-identical to the committed output'
uv run python Regeneration_Law/checks/operational_checks.py 2>/dev/null | cmp - Regeneration_Law/checks/operational_checks.txt && echo 'regeneration law operational checks (Declaration 2) byte-identical to the committed output'
uv run python studies/rlaw/loader_check.py 2>/dev/null | cmp - prereg/rlaw/loader_check.txt && echo 'RLAW loader check byte-identical to the committed output'
uv run python runs/rlaw/summary.py 2>/dev/null | cmp - runs/rlaw/summary.txt && echo 'RLAW per-unit summary byte-identical to the committed output'
uv run python Maps_and_Territories/checks/performativity.py 2>/dev/null | cmp - Maps_and_Territories/checks/performativity.txt && echo 'maps and territories P1-P5 byte-identical to the committed output'
uv run python Maps_and_Territories/checks/performativity_2.py 2>/dev/null | cmp - Maps_and_Territories/checks/performativity_2.txt && echo 'maps and territories P5 post hoc byte-identical to the committed output'
uv run --group realsys python Empty_Cut_Engineering/checks/c3_worlds.py 2>/dev/null | cmp - Empty_Cut_Engineering/checks/c3_worlds.txt && echo 'empty-cut engineering C3 (worlds) byte-identical to the committed output'
# Empty_Cut_Engineering/checks/c1_c2.txt (about 5 minutes, 35 processes) is not re-run here; rerun by hand: uv run --group realsys python Empty_Cut_Engineering/checks/c1_c2.py | cmp - Empty_Cut_Engineering/checks/c1_c2.txt
uv run --group realsys python Real_World/checks/rw2_phaseA.py 2>/dev/null | cmp - Real_World/checks/rw2_phaseA.txt && echo 'RW2 Phase A round 1 byte-identical to the committed output'
uv run --group realsys python Real_World/checks/rw2_phaseA_2.py 2>/dev/null | cmp - Real_World/checks/rw2_phaseA_2.txt && echo 'RW2 Phase A round 2 (post hoc) byte-identical to the committed output'
# Real_World/checks/rw1.txt (about 35 minutes, downloads GPT-2 and Qwen2.5-0.5B-Instruct) is not re-run here; rerun by hand: uv run --group realsys python Real_World/checks/rw1.py | cmp - Real_World/checks/rw1.txt
# Cut_Content/checks/cut_phaseA.txt (about 30 minutes) is not re-run here; rerun by hand: uv run python Cut_Content/checks/cut_phaseA.py | cmp - Cut_Content/checks/cut_phaseA.txt
# runs/rlaw/score.txt (about 6 minutes) and runs/rlaw/diag_kinf.txt need the raw data (gitignored); rerun by hand after data/fetch_rlaw.py: uv run python runs/rlaw/frozen/rlaw_score.py | cmp - runs/rlaw/score.txt
# prereg/rlaw/gate_RLAW.txt (about 40 minutes) is not re-run here; rerun by hand: uv run python runs/rlaw/frozen/gate_rlaw.py | cmp - prereg/rlaw/gate_RLAW.txt
uv run python Rupture_Detection/build/build_pdf.py > /dev/null 2>&1 && echo 'Rupture Detection PDF rebuilds'
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
uv run python theory/retrodictions/synthesis_batches/literature_check.py | cmp - theory/retrodictions/synthesis_batches/literature_check.txt && echo 'literature check of the ADDS rows byte-identical to the committed output'
uv run python docs/pedagogy/build_elegance_ledger.py | cmp - docs/pedagogy/ELEGANCE_LEDGER.md && echo 'elegance ledger reproduces from the pinned synthesis outputs'
uv run python ontology/checks/cut_on_a_machine.py | cmp - ontology/checks/cut_on_a_machine.txt && echo 'ontology check (the cut on a machine) byte-identical to the committed output'
uv run python ontology/checks/turing_safety_ingression.py | cmp - ontology/checks/turing_safety_ingression.txt && echo 'ontology battery (Turing systems, AI safety, ingression) byte-identical to the committed output'
uv run python ontology/checks/genesis_from_emptiness.py | cmp - ontology/checks/genesis_from_emptiness.txt && echo 'ontology exploratory check (genesis from emptiness) byte-identical to the committed output'
uv run python ontology/checks/delta_now.py 2>/dev/null | cmp - ontology/checks/delta_now.txt && echo 'ontology check (delta(Now) and the edge) byte-identical to the committed output'
uv run python runs/eq3/frozen/eq3_score.py smoke | cmp - prereg/eq3/smoke.txt && echo 'EQ3 frozen scorer smoke byte-identical to the committed output'
uv run python runs/eq3/frozen/eq3_score.py smokefull --out /tmp/eq3_smokefull.jsonl 2>/dev/null | cmp - prereg/eq3/smokefull.txt && echo 'EQ3 frozen scorer end-to-end smoke byte-identical to the committed output'
uv run python runs/eq4/frozen/eq4_score.py smoke | cmp - prereg/eq4/smoke.txt && echo 'EQ4 frozen scorer smoke byte-identical to the committed output'
uv run python runs/eq4/frozen/eq4_score.py smokefull --out /tmp/eq4_smokefull.jsonl 2>/dev/null | cmp - prereg/eq4/smokefull.txt && echo 'EQ4 frozen scorer end-to-end smoke byte-identical to the committed output'
uv run python runs/sec1/frozen/sec1_score.py smoke | cmp - prereg/sec1/smoke.txt && echo 'SEC1 frozen scorer smoke byte-identical to the committed output'
uv run python runs/sec1/frozen/sec1_score.py gate | cmp - prereg/sec1/gate_SEC.txt && echo 'SEC1 gate byte-identical to the committed output'
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

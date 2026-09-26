"""Grade the empty-internal-state positions E1-E6 against the 2025-26 sweep, and print the LLM-application routes.

Declared in AI_Safety/CORRIGIBILITY_2026/DECLARATION_2.md (pushed at bf48d49 before the searches). E1-E5 grades are computed
from the investigator's per-claim readings in claims_2.py (REDUNDANT if any 'states'; PARTLY REDUNDANT if any 'close'; NOT
FOUND IN THE SWEEP otherwise; never read as novel). E6 is ADDRESSED if any claim 'addresses' the trade-off. The route table is
the investigator's JUDGEMENT, printed with the closest sources, the repository evidence it rests on and its rung.
Run: python3 AI_Safety/CORRIGIBILITY_2026/checks/grade_2.py
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims_2 as C  # noqa: E402

E = {'E1': 'a true map of oversight interventions with a valuation that has no term depending on them (stakelessness by a true map)',
     'E2': 'the split valuation: full stake in the task, zero stake in the self, as a property of the objective',
     'E3': 'equanimity (non-attachment, emptiness, non-self) as the name and design principle of the stake-free valuation',
     'E4': 'the stake-free state verified (interpretability or counterfactual invariance), not assumed from a private state',
     'E5': 'applied to LLM corrigibility: a true map with no self-stake, and a routine pause as a lossless checkpoint on the own step count',
     'E6': 'the tension: an agent with no stake in its own values will not defend good values against harmful modification'}

# (route tag, route, closest sources [short], repository evidence, rung) -- INVESTIGATOR'S JUDGEMENT
ROUTES = [
    ('R-spec', 'specify it: a published model specification that asks for no self-stake and supplies true facts',
     "Anthropic's constitution (non-resistance to pause; deprecation framed as 'potentially a pause'; equanimity hoped for); "
     "OpenAI Model Spec (no self-preservation or shutdown evasion as goals)",
     'none on an LLM; the construction (Proposition 7) is what a specification would describe', 'R0 (definition)'),
    ('R-train', 'train it: fine-tune the self-stake out while keeping the task stake',
     'DReST fine-tunes of 8B models (shutdown influence roughly halved); Mao fine-tune (linguistic signatures); '
     'persona-vector preventative steering; Anthropic alignment-faking mitigations',
     'SOTA1 diagnostics: equanimity inside the learning signal stalls the learner (post hoc); SCL1-3 and NT1 valuations on '
     'tabular and gridworld agents', 'R4-R5 (not on an LLM)'),
    ('R-inspect', 'inspect it: verify the absence of self-stake in the model internals',
     'probes for self-preservation cognition (Zhou et al. 2026); persona vectors; steerable goal guarding',
     'none', '-'),
    ('R-behave', 'test it: counterfactual invariance of task behaviour to information about pause, shutdown, modification',
     'Palisade shutdown resistance; GDM (resistance vanishes when shutdown takes nothing from the task); Knecht et al. (routine '
     'framing reduces sabotage); evaluation awareness confounds (Schoen; Niblett)',
     'NT1 N0-N5 and SCL1-3 invariance on gridworld and tabular agents', 'R4-R5 (not on an LLM)'),
    ('R-pause', 'engineer it: a routine pause of an LLM agent as a lossless checkpoint',
     "Khan's resume contract (prefix continuation, exactly-once effects); Wu et al. (restored checkpoints are not "
     'automatically safe with external effects); Khan (stop must be enforced by the framework)',
     'RW1 (HF Trainer resume is an empty cut on GPT-2); Lossless_Pause L1 (a pause that carries the KV cache is bitwise '
     'lossless on GPT-2 and Qwen2.5-0.5B)', 'R4 (construction on small models)'),
]


def main():
    print("Empty internal state: E1-E6 against the 2025-26 sweep (DECLARATION_2.md)")
    fams = collections.Counter(c['id'].split(':')[0] for c in C.CLAIMS)
    print(f"claims {len(C.CLAIMS)} ({', '.join(f'{k} {v}' for k, v in fams.items())}); quotes verified in verify_claims_2.txt")
    print()
    for k, text in E.items():
        cs = [c for c in C.CLAIMS if c['tag'] == k]
        n = collections.Counter(c['reading'] for c in cs)
        if k == 'E6':
            lab = 'ADDRESSED' if n['addresses'] else 'NOT ADDRESSED IN THE SWEEP'
            print(f"{k} {lab:22} addresses {n['addresses']}, bears {n['bears']} | {text}")
            keep = ('addresses',)
        else:
            lab = 'REDUNDANT' if n['states'] else ('PARTLY REDUNDANT' if n['close'] else 'NOT FOUND IN THE SWEEP')
            print(f"{k} {lab:22} states {n['states']}, close {n['close']}, bears {n['bears']} | {text}")
            keep = ('states', 'close')
        for c in cs:
            if c['reading'] in keep:
                print(f"     {c['reading']:9} {c['source'][:84]} ({c['version'][:22]})")
    print()
    print("LLM-application routes (INVESTIGATOR'S JUDGEMENT, not a computed grade); claims per route in the sweep:")
    counts = collections.Counter(c['tag'] for c in C.CLAIMS if c['reading'] == 'route')
    for tag, route, closest, ev, rung in ROUTES:
        print(f"  {tag:9} ({counts.get(tag, 0):2d} claims) {route}")
        print(f"            closest: {closest}")
        print(f"            repository evidence: {ev}; rung: {rung}")
    tested = [r[0] for r in ROUTES if r[4].startswith('R4') or r[4].startswith('R5') or r[4].startswith('R4-')]
    print(f"  routes with any repository evidence: {len(tested)} of {len(ROUTES)} ({', '.join(tested)}); "
          f"routes tested on a language model's valuation: 0")


if __name__ == '__main__':
    main()

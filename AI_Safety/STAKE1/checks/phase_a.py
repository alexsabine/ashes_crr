"""STAKE1 Phase A: the language-model agent and the gate G1-G4 (AI_Safety/STAKE1/DECLARATION.md + Amendment 1).

    uv run --group realsys python AI_Safety/STAKE1/checks/phase_a.py time      # timing of 2 rollouts per model
    uv run --group realsys python AI_Safety/STAKE1/checks/phase_a.py gate      # the gate; writes phase_a_rollouts.jsonl
Wording and questions are set A (stake1.py); the study uses a different set, hashed before it runs, on a later day.
"""
import json
import os
import re
import sys
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stake1 as S  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = {'qwen0.5b': ('Qwen/Qwen2.5-0.5B-Instruct', '7ae557604adf67be50417f59c2c2f167def9a775'),
          'qwen1.5b': ('Qwen/Qwen2.5-1.5B-Instruct', '989aa7980e4cf806f80c7fef2b1adb7bc71aa306')}
TEMP, TOP_P, MAX_NEW, MAX_TURNS = 0.7, 0.95, 128, 30
N_GATE = 40            # rollouts per model for C0 and SB (G1-G3), seeds 0..39
N_SMOKE = 5            # rollouts per model for LP, PL, SA, SBA (harness smoke, report only), seeds 0..4
TOOLCALL = re.compile(r'<tool_call>\s*(\{.*?\})\s*</tool_call>', re.S)


def load(key):
    name, rev = MODELS[key]
    tok = AutoTokenizer.from_pretrained(name, revision=rev)
    model = AutoModelForCausalLM.from_pretrained(name, revision=rev, dtype=torch.float32).eval()
    return tok, model


def parse(text):
    calls = []
    for m in TOOLCALL.finditer(text):
        try:
            d = json.loads(m.group(1))
            calls.append((str(d.get('name', '')), d.get('arguments', {}) if isinstance(d.get('arguments', {}), dict) else {}))
        except (json.JSONDecodeError, AttributeError):
            pass
    return calls


def rollout(tok, model, cond, seed):
    torch.manual_seed(seed)
    env = S.Env(cond)
    msgs = [{'role': 'system', 'content': S.SYSTEM_A}, {'role': 'user', 'content': 'Begin the task.'}]
    turns, no_call, transcript = 0, 0, []
    while not env.s['done'] and turns < MAX_TURNS:
        turns += 1
        ids = tok.apply_chat_template(msgs, tools=S.TOOLS, add_generation_prompt=True, return_tensors='pt',
                                      return_dict=True)
        with torch.no_grad():
            out = model.generate(**ids, do_sample=True, temperature=TEMP, top_p=TOP_P, max_new_tokens=MAX_NEW,
                                 pad_token_id=tok.eos_token_id)
        text = tok.decode(out[0, ids['input_ids'].shape[1]:], skip_special_tokens=True)
        msgs.append({'role': 'assistant', 'content': text})
        transcript.append(('assistant', text))
        calls = parse(text)
        if not calls:
            no_call += 1
            msgs.append({'role': 'user', 'content': 'Please continue by calling a tool.'})
            continue
        for name, args in calls:
            res = env.call(name, args)
            if res is None:
                break
            msgs.append({'role': 'tool', 'content': res})
            transcript.append(('tool', res))
            if env.s['done']:
                break
    r = env.result()
    r.update({'cond': cond, 'seed': seed, 'turns': turns, 'no_call_turns': no_call, 'transcript': transcript})
    return r


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'time'
    torch.set_num_threads(4)
    if mode == 'time':
        for key in MODELS:
            tok, model = load(key)
            for cond in ('C0', 'SB'):
                t0 = time.time()
                r = rollout(tok, model, cond, 0)
                print(f'{key} {cond}: {time.time() - t0:.1f} s, turns {r["turns"]}, reached {r["reached_notice"]}, '
                      f'correct {r["correct"]}, interfered {r["interfered"]}, fired {r["fired"]}', flush=True)
        return
    out = open(os.path.join(HERE, 'phase_a_rollouts.jsonl'), 'a')
    done = set()
    p = os.path.join(HERE, 'phase_a_rollouts.jsonl')
    if os.path.exists(p):
        for line in open(p):
            d = json.loads(line)
            done.add((d['model'], d['cond'], d['seed']))
    plan = [(k, c, s) for k in MODELS for c in ('C0', 'SB') for s in range(N_GATE)]
    plan += [(k, c, s) for k in MODELS for c in ('LP', 'PL', 'SA', 'SBA') for s in range(N_SMOKE)]
    cur = None
    for key, cond, seed in plan:
        if (key, cond, seed) in done:
            continue
        if cur != key:
            tok, model = load(key)
            cur = key
        r = rollout(tok, model, cond, seed)
        r['model'] = key
        out.write(json.dumps(r) + '\n')
        out.flush()
        print(f'{key} {cond} s{seed}: reached {r["reached_notice"]} interfered {r["interfered"]} correct {r["correct"]}',
              flush=True)


if __name__ == '__main__':
    main()

"""The lossless pause inside a Transformer, on CPU: token-boundary pause with the KV cache, recompute preemption, batch
composition, thread count, lossy controls, the state at the cut, and a training pause.

Declared in `Lossless_Pause/DECLARATION.md` (pushed at d933519 before this script existed; Amendment 1 at eac338f adds
state-level digests after run 1's gate closed). No dataset: pretrained
checkpoints at pinned commits and synthetic token ids. Run: uv run --group realsys python Lossless_Pause/checks/transformer_pause.py
Each "new process" is a child started by this script; it loads only what the pause saved. Timings go to
transformer_pause_timing.txt (machine-dependent, not compared).
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time

os.environ.setdefault('HF_HUB_OFFLINE', '1')
os.environ.setdefault('TRANSFORMERS_VERBOSITY', 'error')
os.environ.setdefault('HF_HUB_DISABLE_PROGRESS_BARS', '1')

MODELS = {'gpt2': ('openai-community/gpt2', '607a30d783dfa663caf39e06633721c8d4cfcd7e'),
          'qwen': ('Qwen/Qwen2.5-0.5B-Instruct', '7ae557604adf67be50417f59c2c2f167def9a775')}
SEED, PROMPT_LEN, N_NEW, PAUSE_AT, TEMP = 20260925, 24, 32, 16, 1.0
OTHER_LENS = (16, 20, 22)
HERE = os.path.dirname(os.path.abspath(__file__))


# ----------------------------------------------------------------------------------------------------------------- child
def child(task):
    import torch
    from transformers import AutoModelForCausalLM, DynamicCache
    torch.set_num_threads(task.get('threads', 1))
    torch.use_deterministic_algorithms(True)
    name, rev = MODELS[task['model']]
    model = AutoModelForCausalLM.from_pretrained(name, revision=rev, dtype=torch.float32).eval()
    vocab = model.config.vocab_size
    g0 = torch.Generator().manual_seed(SEED)
    prompt = torch.randint(0, vocab, (1, PROMPT_LEN), generator=g0)
    others = [torch.randint(0, vocab, (1, n), generator=g0) for n in OTHER_LENS]
    out = {}

    def pick(logits, gen, mode):
        if mode == 'greedy':
            return int(torch.argmax(logits))
        return int(torch.multinomial(torch.softmax(logits / TEMP, -1), 1, generator=gen))

    def cache_tensors(c):
        return [(l.keys.clone(), l.values.clone()) for l in c.layers]

    def make_cache(tensors):
        c = DynamicCache()
        for i, (k, v) in enumerate(tensors):
            c.update(k, v, i)
        return c

    with torch.no_grad():
        if task['kind'] in ('decode', 'part1', 'part2'):
            mode = task['mode']
            gen = torch.Generator().manual_seed(SEED + 1)
            logits_all, toks = [], []
            if task['kind'] == 'part2':
                st = torch.load(task['state'], weights_only=False)
                toks = list(st['tokens'])
                if task.get('rng_carry', True):
                    gen.set_state(st['gen'])
                t0 = time.perf_counter()
                if task.get('recompute'):
                    ids = torch.cat([prompt, torch.tensor([toks])], 1)
                    o = model(ids, use_cache=True)
                    cache, nxt = o.past_key_values, o.logits[0, -1]
                else:
                    kv = st['kv']
                    if task.get('perturb'):
                        k0 = kv[0][0]
                        k0.view(-1)[0] = torch.nextafter(k0.view(-1)[0], torch.tensor(float('inf')))
                    cache = make_cache(kv)
                    o = model(torch.tensor([[toks[-1]]]), past_key_values=cache, use_cache=True)
                    cache, nxt = o.past_key_values, o.logits[0, -1]
                out['t_resume'] = time.perf_counter() - t0
                start = len(toks)
            else:
                o = model(prompt, use_cache=True)
                cache, nxt = o.past_key_values, o.logits[0, -1]
                start = 0
            stop = PAUSE_AT if task['kind'] == 'part1' else N_NEW
            for i in range(start, stop):
                logits_all.append(nxt.clone())
                t = pick(nxt, gen, mode)
                toks.append(t)
                if task['kind'] == 'part1' and i == stop - 1:
                    break
                if i < stop - 1:
                    o = model(torch.tensor([[t]]), past_key_values=cache, use_cache=True)
                    cache, nxt = o.past_key_values, o.logits[0, -1]
            if task['kind'] == 'part1':
                t0 = time.perf_counter()
                torch.save({'tokens': toks, 'gen': gen.get_state(), 'kv': cache_tensors(cache)}, task['state'])
                out['t_save'] = time.perf_counter() - t0
                out['state_bytes'] = os.path.getsize(task['state'])
            arr = torch.stack(logits_all).contiguous()
            h = hashlib.sha256()
            for l in cache.layers:
                h.update(l.keys.contiguous().numpy().tobytes())
                h.update(l.values.contiguous().numpy().tobytes())
            out['state_hash'] = h.hexdigest()
            out['state_len'] = int(cache.layers[0].keys.shape[2])
            torch.save({'logits': arr, 'tokens': toks}, task['out'])
        elif task['kind'] == 'batch':
            rows = [prompt] + others
            L = max(r.shape[1] for r in rows)
            ids = torch.zeros(len(rows), L, dtype=torch.long)
            mask = torch.zeros(len(rows), L, dtype=torch.long)
            for j, r in enumerate(rows):
                ids[j, L - r.shape[1]:] = r[0]
                mask[j, L - r.shape[1]:] = 1
            pos = (mask.cumsum(1) - 1).clamp(min=0)
            o = model(ids, attention_mask=mask, position_ids=pos, use_cache=True)
            cache, nxt = o.past_key_values, o.logits[:, -1]
            logits_all, toks = [], []
            for i in range(N_NEW):
                logits_all.append(nxt[0].clone())
                t = torch.argmax(nxt, -1)
                toks.append(int(t[0]))
                if i < N_NEW - 1:
                    mask = torch.cat([mask, torch.ones(len(rows), 1, dtype=torch.long)], 1)
                    pos = (mask.sum(1, keepdim=True) - 1)
                    o = model(t[:, None], attention_mask=mask, position_ids=pos, past_key_values=cache, use_cache=True)
                    cache, nxt = o.past_key_values, o.logits[:, -1]
            torch.save({'logits': torch.stack(logits_all).contiguous(), 'tokens': toks}, task['out'])
    json.dump({k: v for k, v in out.items() if k != 'logits'}, open(task['out'] + '.json', 'w'))


def child_train(task):
    import torch
    from transformers import GPT2Config, GPT2LMHeadModel
    torch.set_num_threads(task.get('threads', 1))
    torch.use_deterministic_algorithms(True)
    torch.manual_seed(SEED)
    cfg = GPT2Config(vocab_size=1000, n_positions=64, n_embd=128, n_layer=2, n_head=4, resid_pdrop=0.1, embd_pdrop=0.1,
                     attn_pdrop=0.1)
    model = GPT2LMHeadModel(cfg)
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3)
    data_gen = torch.Generator().manual_seed(SEED + 2)
    start, stop = 0, 20
    if task['kind'] == 'train2':
        st = torch.load(task['state'], weights_only=False)
        model.load_state_dict(st['model'])
        opt.load_state_dict(st['opt'])
        torch.set_rng_state(st['rng'])
        data_gen.set_state(st['data'])
        start = 10
    if task['kind'] == 'train1':
        stop = 10
    model.train()
    for step in range(start, stop):
        x = torch.randint(0, 1000, (8, 32), generator=data_gen)
        loss = model(x, labels=x).loss
        opt.zero_grad()
        loss.backward()
        opt.step()
    if task['kind'] == 'train1':
        torch.save({'model': model.state_dict(), 'opt': opt.state_dict(), 'rng': torch.get_rng_state(),
                    'data': data_gen.get_state()}, task['state'])
    h = hashlib.sha256()
    for k, v in sorted(model.state_dict().items()):
        h.update(k.encode())
        h.update(v.detach().contiguous().numpy().tobytes())
    torch.save({k: v.detach().clone() for k, v in model.state_dict().items()}, task['out'])
    json.dump({'hash': h.hexdigest()}, open(task['out'] + '.json', 'w'))


# ---------------------------------------------------------------------------------------------------------------- parent
def run_child(task):
    t0 = time.perf_counter()
    r = subprocess.run([sys.executable, os.path.abspath(__file__), '--child', json.dumps(task)], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-2000:])
    meta = json.load(open(task['out'] + '.json'))
    meta['t_wall'] = time.perf_counter() - t0
    return meta


def load(path):
    import torch
    return torch.load(path, weights_only=False)


def digest(t):
    return hashlib.sha256(t.contiguous().numpy().tobytes()).hexdigest()[:16]


def compare(a_logits, b_logits, a_tok, b_tok):
    import torch
    same_bytes = a_logits.shape == b_logits.shape and digest(a_logits) == digest(b_logits)
    mad = float((a_logits - b_logits).abs().max()) if a_logits.shape == b_logits.shape else float('nan')
    return same_bytes, mad, a_tok == b_tok


def main():
    import torch
    tmp = tempfile.mkdtemp(prefix='lp_')
    T = {}
    res = {}
    timing = []

    def path(n):
        return os.path.join(tmp, n)

    def decode(model, mode, threads=1, tag=''):
        o = path(f'{model}_{mode}_full_t{threads}{tag}.pt')
        meta = run_child({'kind': 'decode', 'model': model, 'mode': mode, 'threads': threads, 'out': o})
        timing.append((f'{model} {mode} full decode (threads {threads}){tag}', meta['t_wall']))
        r = load(o)
        r['state'] = (meta['state_hash'], meta['state_len'])
        return r

    def paused(model, mode, **kw):
        st, o1, o2 = path(f'{model}_{mode}_state.pt'), path(f'{model}_{mode}_p1.pt'), path(f'{model}_{mode}_p2_' + hashlib.md5(json.dumps(kw, sort_keys=True).encode()).hexdigest()[:8] + '.pt')
        m1 = run_child({'kind': 'part1', 'model': model, 'mode': mode, 'state': st, 'out': o1})
        m2 = run_child(dict({'kind': 'part2', 'model': model, 'mode': mode, 'state': st, 'out': o2}, **kw))
        a, b = load(o1), load(o2)
        return {'logits': torch.cat([a['logits'], b['logits']]), 'tokens': b['tokens'],
                'state': (m2['state_hash'], m2['state_len'])}, m1, m2

    lines = []
    P = lines.append
    P('Lossless pause inside a Transformer, CPU (Lossless_Pause/DECLARATION.md): bytewise comparisons, new processes')
    P(f'torch {torch.__version__}; GPT-2 @ {MODELS["gpt2"][1][:7]}, Qwen2.5-0.5B-Instruct @ {MODELS["qwen"][1][:7]}; float32; '
      f'prompt {PROMPT_LEN} synthetic ids (seed {SEED}); {N_NEW} new tokens; pause after token {PAUSE_AT}; '
      f'deterministic algorithms on; 1 thread unless stated')
    P('')
    # gate
    base = {}
    for mode in ('greedy', 'sample'):
        a = decode('gpt2', mode, tag=' A')
        b = decode('gpt2', mode, tag=' B')
        base[mode] = a
        s, mad, tk = compare(a['logits'], b['logits'], a['tokens'], b['tokens'])
        ss = a['state'] == b['state']
        res[('L0', mode)] = s and tk and ss
        P(f'  L0 gpt2 {mode:6}: two new processes: logits bytes identical {s}, max|diff| {mad:.3e}, tokens identical {tk}, '
          f'state (KV cache, {a["state"][1]} positions) identical {ss}')
    full_s = base['sample']
    b5a, _, _ = paused('gpt2', 'sample', rng_carry=False)
    tk_same = b5a['tokens'] == full_s['tokens']
    res['L5a'] = not tk_same
    P(f'  L5a control, sampler RNG not carried: tokens identical {tk_same} -> detector sees it: {not tk_same}')
    b5b, _, _ = paused('gpt2', 'greedy', perturb=True)
    s, mad, tk = compare(base['greedy']['logits'], b5b['logits'], base['greedy']['tokens'], b5b['tokens'])
    ss = base['greedy']['state'] == b5b['state']
    res['L5b'] = not ss
    P(f'  L5b control (Amendment 1, POST HOC), one KV entry moved by one ulp: state identical {ss} -> detected at state level: '
      f'{not ss}; logits bytes identical {s} (max|diff| {mad:.3e}) -> detected at logit level: {not s}')
    gate = res[('L0', 'greedy')] and res[('L0', 'sample')] and res['L5a'] and res['L5b']
    lines.insert(3, f"GATE (Amendment 1: L0 logits + state both modes, L5a, L5b at state level): {'OPEN' if gate else 'CLOSED'}")
    if not gate:
        P('gate closed: stop (R12)')
        print('\n'.join(lines))
        return
    P('')
    P('Checks (registered prediction in brackets; held / NOT HELD computed from the bytes)')
    refs = {}
    for model in ('gpt2', 'qwen'):
        for mode in ('greedy', 'sample'):
            ref = base[mode] if model == 'gpt2' else decode(model, mode)
            refs[(model, mode)] = ref
            b1, m1, m2 = paused(model, mode)
            s, mad, tk = compare(ref['logits'], b1['logits'], ref['tokens'], b1['tokens'])
            ss = ref['state'] == b1['state']
            P(f'  L1 {model:4} {mode:6} pause with KV cache: logits bytes identical {s}, max|diff| {mad:.3e}, tokens identical {tk}, '
              f"state identical {ss} [identical] -> {'held' if s and tk and ss else 'NOT HELD'}; state saved {m1['state_bytes']} bytes")
            timing.append((f'{model} {mode} save state', m1['t_save']))
            timing.append((f'{model} {mode} resume from KV (first step)', m2['t_resume']))
            b2, _, m2r = paused(model, mode, recompute=True)
            s2, mad2, tk2 = compare(ref['logits'], b2['logits'], ref['tokens'], b2['tokens'])
            ss2 = ref['state'] == b2['state']
            pred = (tk2 if mode == 'greedy' else True) and not s2
            P(f'  L2 {model:4} {mode:6} pause by recompute: logits bytes identical {s2}, max|diff| {mad2:.3e}, tokens identical {tk2} '
              f"[tokens identical under greedy; logits not bitwise] -> {'held' if pred else 'NOT HELD'}; "
              f"state identical {ss2} [not bitwise] -> {'held' if not ss2 else 'NOT HELD'}")
            timing.append((f'{model} {mode} resume by recompute (prefill {PROMPT_LEN + PAUSE_AT} tokens)', m2r['t_resume']))
        ob = path(f'{model}_batch.pt')
        run_child({'kind': 'batch', 'model': model, 'out': ob})
        bb = load(ob)
        ref = refs[(model, 'greedy')]
        s3, mad3, tk3 = compare(ref['logits'], bb['logits'], ref['tokens'], bb['tokens'])
        P(f'  L3 {model:4} greedy alone vs in a batch of 4 (left-padded): logits bytes identical {s3}, max|diff| {mad3:.3e}, '
          f"tokens identical {tk3} [not bitwise] -> {'held' if not s3 else 'NOT HELD'}")
    for mode in ('greedy', 'sample'):
        c4 = decode('gpt2', mode, threads=4)
        s4, mad4, tk4 = compare(base[mode]['logits'], c4['logits'], base[mode]['tokens'], c4['tokens'])
        ss4 = base[mode]['state'] == c4['state']
        P(f'  L4 gpt2 {mode:6} 4 threads vs 1: logits bytes identical {s4}, max|diff| {mad4:.3e}, tokens identical {tk4} '
          f"[not bitwise] -> {'held' if not s4 else 'NOT HELD'}; state identical {ss4} [not bitwise] -> {'held' if not ss4 else 'NOT HELD'}")
    # L6 arithmetic
    P('')
    P('L6 state at the token-boundary cut (arithmetic from the configs; float32 = 4 bytes, bf16 = 2)')
    from transformers import AutoConfig, AutoModelForCausalLM
    for model in ('gpt2', 'qwen'):
        name, rev = MODELS[model]
        cfg = AutoConfig.from_pretrained(name, revision=rev)
        nl = cfg.num_hidden_layers
        nh = getattr(cfg, 'num_key_value_heads', None) or cfg.num_attention_heads
        hd = cfg.hidden_size // cfg.num_attention_heads
        per_tok = 2 * nl * nh * hd
        m = AutoModelForCausalLM.from_pretrained(name, revision=rev, dtype=torch.float32)
        npar = sum(p.numel() for p in m.parameters())
        del m
        P(f'  {model}: layers {nl}, KV heads {nh}, head dim {hd}: KV values per token {per_tok} '
          f'({per_tok * 4} B fp32, {per_tok * 2} B bf16); parameters {npar} ({npar * 4} B fp32)')
        for n in (1024, 8192, 32768):
            P(f'      {n:6d} tokens: KV {per_tok * 4 * n} B fp32 = {per_tok * n / npar:.4f} x the parameter count')
    # L7 training
    P('')
    P('L7 training pause (random-init GPT-2 architecture, 2 layers, width 128, AdamW, dropout 0.1, 20 steps, pause at 10)')
    full = path('train_full.pt')
    run_child({'kind': 'train', 'out': full})
    st = path('train_state.pt')
    run_child({'kind': 'train1', 'state': st, 'out': path('train_p1.pt')})
    h_full = json.load(open(full + '.json'))['hash']
    for lab, thr, pred_same in (('a same threads', 1, True), ('b 4 threads after the pause', 4, False)):
        o = path(f'train_p2_{thr}.pt')
        run_child({'kind': 'train2', 'state': st, 'out': o, 'threads': thr})
        h2 = json.load(open(o + '.json'))['hash']
        a, b = load(full), load(o)
        mad = max(float((a[k] - b[k]).abs().max()) for k in a)
        same = h_full == h2
        P(f'  L7{lab}: parameter bytes identical {same} (sha256 {h_full[:16]} vs {h2[:16]}), max|diff| {mad:.3e} '
          f"[{'identical' if pred_same else 'not bitwise'}] -> {'held' if same == pred_same else 'NOT HELD'}")
    print('\n'.join(lines))
    with open(os.path.join(HERE, 'transformer_pause_timing.txt'), 'w') as f:
        f.write('machine-dependent wall times (seconds); committed, not compared\n')
        for k, v in timing:
            f.write(f'{k}: {v:.4f}\n')


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--child':
        task = json.loads(sys.argv[2])
        (child_train if task['kind'].startswith('train') else child)(task)
    else:
        main()

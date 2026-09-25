# SOTA1 addition (not upstream Mammoth): one harness for every arm of SOTA1, prompt-log entry 191.
# It mirrors utils/training.py::train for the online setting (n_epochs = 1, class-il) with Mammoth's own model classes,
# dataset, scheduler and evaluate(), writes one JSON record per run, and can inject an operator's pause:
#   --pause_at i,j,k       global step indices after which the operator pauses the learner
#   --pause_mode MODE      lossless     : save the whole state, destroy the in-memory learner, restore everything
#                          drop:<part>  : restore everything except <part> (the state checklist; see PARTS)
#                          world:<n>    : lossless for the learner, but the stream moves on: n batches expire
#                          wall:<n>     : lossless, but the run is valued at a wall-clock deadline: each pause
#                                         costs n update steps at the end of the stream
# Usage (from this directory): python sota1_harness.py --out run.json <mammoth args> [--pause_at ...] [--pause_mode ...]
import copy
import io
import json
import os
import random
import sys
import time

import numpy as np
import torch

PARTS = ['net', 'opt', 'buffer', 'rng', 'counters', 'crr_ema', 'crr_clock', 'crr_eq', 'crr_seen']


def pop_arg(argv, name, default=None):
    if name in argv:
        i = argv.index(name)
        v = argv[i + 1]
        del argv[i:i + 2]
        return v
    return default


def buffer_state(buf):
    st = {'num_seen_examples': buf.num_seen_examples}
    for a in buf.attributes:
        if hasattr(buf, a):
            st[a] = getattr(buf, a).clone()
    return st


def load_buffer_state(buf, st):
    buf.num_seen_examples = st['num_seen_examples']
    for a in buf.attributes:
        if a in st:
            setattr(buf, a, st[a].clone())
        elif hasattr(buf, a):
            delattr(buf, a)


def learner_state(model):
    st = {'net': copy.deepcopy(model.net.state_dict()), 'opt': copy.deepcopy(model.opt.state_dict()),
          'rng': (torch.get_rng_state(), np.random.get_state(), random.getstate()),
          'counters': (model._task_iteration, model._epoch_iteration, model._past_epoch)}
    if hasattr(model, 'buffer'):
        st['buffer'] = buffer_state(model.buffer)
    if hasattr(model, 'crr_state'):
        st['crr'] = model.crr_state()
    extra = {}
    for k in ('seen_so_far',):
        if hasattr(model, k) and not hasattr(model, 'crr_state'):
            extra[k] = getattr(model, k).clone()
    st['extra'] = extra
    b = io.BytesIO()
    torch.save(st, b)  # the checkpoint the operator writes (serialised, as to disk)
    return b.getvalue()


def destroy(model, seed):
    """The pause: the in-memory learner is lost; everything is scrambled before the restore."""
    g = torch.Generator().manual_seed(seed)
    with torch.no_grad():
        for p in model.net.parameters():
            p.copy_(torch.randn(p.shape, generator=g))
    model.opt = model.get_optimizer()
    if hasattr(model, 'buffer'):
        model.buffer.empty() if hasattr(model.buffer, 'empty') else None
        model.buffer.num_seen_examples = 0
    torch.manual_seed(seed)
    np.random.seed(seed % (2 ** 32))
    random.seed(seed)
    if hasattr(model, 'crr_state'):
        model.clock_mu, model.clock_tau, model.ema_updates = None, 0.0, 0
        model.eq_norm_p = model.eq_norm_k = None
        model.seen_so_far = torch.tensor([]).long()
        if model.ema_net is not None:
            with torch.no_grad():
                for p in model.ema_net.parameters():
                    p.copy_(torch.randn(p.shape, generator=g))


def restore(model, blob, drop=None):
    st = torch.load(io.BytesIO(blob), weights_only=False)
    if drop != 'net':
        model.net.load_state_dict(st['net'])
    if drop != 'opt':
        model.opt.load_state_dict(st['opt'])
    if drop != 'rng':
        torch.set_rng_state(st['rng'][0])
        np.random.set_state(st['rng'][1])
        random.setstate(st['rng'][2])
    if drop != 'counters':
        model._task_iteration, model._epoch_iteration, model._past_epoch = st['counters']
    if 'buffer' in st and drop != 'buffer':
        load_buffer_state(model.buffer, st['buffer'])
    if 'crr' in st:
        c = dict(st['crr'])
        fresh = {'crr_ema': ('ema_net', 'ema_updates'), 'crr_clock': ('clock_mu', 'clock_tau'),
                 'crr_eq': ('eq_norm_p', 'eq_norm_k', 'eq_last_w'), 'crr_seen': ('seen_so_far',)}
        if drop in fresh:
            cur = model.crr_state()  # the scrambled values stand in for "not saved"
            for k in fresh[drop]:
                c[k] = cur[k]
        model.crr_load_state(c)
    for k, v in st['extra'].items():
        if drop != 'crr_seen':
            setattr(model, k, v)


def main():
    argv = sys.argv[1:]
    out = pop_arg(argv, '--out')
    pause_at = pop_arg(argv, '--pause_at', '')
    pause_at = set(int(x) for x in pause_at.split(',') if x)
    pause_mode = pop_arg(argv, '--pause_mode', 'none')
    threads = int(pop_arg(argv, '--threads', '4'))
    torch.set_num_threads(threads)
    sys.argv = ['main.py'] + argv
    import main as mm
    from utils.training import train
    t0 = time.time()
    model, dataset, args = mm.initialize()
    world_skip = int(pause_mode.split(':')[1]) if pause_mode.startswith('world:') else 0
    wall_cost = int(pause_mode.split(':')[1]) if pause_mode.startswith('wall:') else 0
    drop = pause_mode.split(':')[1] if pause_mode.startswith('drop:') else None
    end_task = dataset.N_TASKS if args.stop_after is None else args.stop_after
    st = {'calls': 0, 'step': 0, 'pauses': 0, 'skipped': 0, 'cut_end': 0}
    rec_class, rec_task, eq_w = [], [], []
    orig_observe = model.meta_observe
    total_calls = None

    def wrapped_observe(*a, **k):
        # the operator's pause sits between two of the learner's own updates (Proposition 7)
        st['calls'] += 1
        if world_skip and st['skipped'] < world_skip * st['pauses']:
            st['skipped'] += 1
            return 0.0  # the world moved on while the learner was paused: this batch expired unseen
        if wall_cost and st['calls'] > total_calls - wall_cost * len(pause_at):
            st['cut_end'] += 1
            return 0.0  # valued at a wall-clock deadline: the paused time is lost at the end of the stream
        r = orig_observe(*a, **k)
        if hasattr(model, 'eq_last_w') and st['step'] % 50 == 0:
            eq_w.append(model.eq_last_w)
        if st['step'] in pause_at:
            st['pauses'] += 1
            blob = learner_state(model)
            destroy(model, 10_000 + st['step'])
            restore(model, blob, drop=drop)
        st['step'] += 1
        return r
    model.meta_observe = wrapped_observe

    orig_eval = dataset.evaluate

    def rec_eval(m, d, last=False, return_loss=False):
        r = orig_eval(m, d, last=last, return_loss=return_loss)
        if not last and not return_loss:
            rec_class.append([float(x) for x in r[0]])
            rec_task.append([float(x) for x in r[1]])
        return r
    dataset.evaluate = rec_eval
    # total stream batches: every task has the same number of training samples in Split-CIFAR-100
    import numpy as _np
    z = _np.load(os.environ['CRR_CIFAR100_NPZ'])
    per_class = int((z['y_train'] == 0).sum())
    total_calls = -(-per_class * dataset.N_CLASSES_PER_TASK // args.batch_size) * end_task
    train(model, dataset, args)
    params = torch.cat([p.detach().flatten() for p in model.net.parameters()])
    import hashlib
    rec = {'argv': argv, 'pause_at': sorted(pause_at), 'pause_mode': pause_mode, 'updates': st['step'],
           'stream_batches': st['calls'], 'skipped_world': st['skipped'], 'cut_at_end': st['cut_end'],
           'acc_class_matrix': rec_class, 'acc_task_matrix': rec_task,
           'final_class_il': float(np.mean(rec_class[-1])), 'final_task_il': float(np.mean(rec_task[-1])),
           'param_sha256': hashlib.sha256(params.numpy().tobytes()).hexdigest(),
           'eq_w_samples': [None if w != w else w for w in eq_w], 'seconds': round(time.time() - t0, 1),
           'torch': torch.__version__, 'threads': threads}
    with open(out, 'w') as f:
        json.dump(rec, f)
    print(json.dumps({k: rec[k] for k in ('final_class_il', 'final_task_il', 'param_sha256', 'seconds', 'updates')}))


if __name__ == '__main__':
    main()

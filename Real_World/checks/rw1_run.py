"""RW1, one process = one run (Real_World/DECLARATION_RW1.md, pushed in e0a47b5 before this file existed).
An existing stack: Hugging Face Transformers Trainer 5.17.0, a pretrained model at a pinned commit, synthetic token data.

  uv run --group realsys python Real_World/checks/rw1_run.py '<config json>' <out dir>
config: model ('gpt2' | 'qwen'), phase ('full' | 'first' | 'second'), ckpt (checkpoint dir for 'second'),
        delete (list of checkpoint files removed before resuming), ignore_data_skip (bool), sleep (seconds of real pause)
"""
import os

os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")          # the orchestrator sets HF_HUB_OFFLINE=1 for every run
import hashlib  # noqa: E402
import json  # noqa: E402
import shutil  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402

import numpy as np  # noqa: E402
import torch  # noqa: E402
from transformers import AutoModelForCausalLM, Trainer, TrainerCallback, TrainingArguments  # noqa: E402

MODELS = {"gpt2": ("openai-community/gpt2", "607a30d783dfa663caf39e06633721c8d4cfcd7e"),
          "qwen": ("Qwen/Qwen2.5-0.5B-Instruct", "7ae557604adf67be50417f59c2c2f167def9a775")}
SETTINGS = {"gpt2": dict(bs=8, max_steps=48, pause=24, n_probe=8), "qwen": dict(bs=2, max_steps=8, pause=4, n_probe=2)}
N_TRAIN, SEQ, ID_MAX, ACCUM, LR, WARMUP, SEED = 512, 64, 5000, 2, 5e-5, 10, 0


class Tokens(torch.utils.data.Dataset):
    def __init__(self, n, seed):
        self.x = torch.tensor(np.random.default_rng(seed).integers(0, ID_MAX, size=(n, SEQ)), dtype=torch.long)

    def __len__(self):
        return len(self.x)

    def __getitem__(self, i):
        return {"input_ids": self.x[i], "labels": self.x[i]}


class StopAfterSave(TrainerCallback):
    def __init__(self, step):
        self.step = step

    def on_save(self, args, state, control, **kw):
        if state.global_step == self.step:
            control.should_training_stop = True
        return control


def sha_state(model):
    h = hashlib.sha256()
    for k, v in sorted(model.state_dict().items()):
        h.update(k.encode()); h.update(v.detach().float().contiguous().numpy().tobytes())
    return h.hexdigest()


def main(cfg, out):
    torch.set_num_threads(1)
    name, rev = MODELS[cfg["model"]]; st = SETTINGS[cfg["model"]]
    model = AutoModelForCausalLM.from_pretrained(name, revision=rev, dtype=torch.float32)
    args = TrainingArguments(output_dir=os.path.join(out, "trainer"), per_device_train_batch_size=st["bs"],
                             gradient_accumulation_steps=ACCUM, learning_rate=LR, warmup_steps=WARMUP, lr_scheduler_type="linear",
                             max_steps=st["max_steps"], save_strategy="steps", save_steps=st["pause"], logging_steps=1000,
                             report_to="none", seed=SEED, use_cpu=True, dataloader_num_workers=0, disable_tqdm=True,
                             ignore_data_skip=bool(cfg.get("ignore_data_skip", False)))
    cbs = [StopAfterSave(st["pause"])] if cfg["phase"] == "first" else []
    tr = Trainer(model=model, args=args, train_dataset=Tokens(N_TRAIN, 11), callbacks=cbs)
    res = {}
    t0 = time.perf_counter()
    if cfg["phase"] == "second":
        ck = os.path.join(out, "ckpt")
        shutil.copytree(cfg["ckpt"], ck, copy_function=os.link)        # hard links: deleting a link leaves the original
        for f in cfg.get("delete", []):
            os.remove(os.path.join(ck, f))
        time.sleep(float(cfg.get("sleep", 0)))                        # the real wall-clock pause
        t0 = time.perf_counter()
        tr.train(resume_from_checkpoint=ck)
    else:
        tr.train()
    dt = time.perf_counter() - t0
    res["global_step"] = int(tr.state.global_step)
    if cfg["phase"] == "first":
        ck = os.path.join(out, "trainer", f"checkpoint-{st['pause']}")
        res["ckpt"] = ck; res["files"] = {f: os.path.getsize(os.path.join(ck, f)) for f in sorted(os.listdir(ck))}
    else:
        model.eval()
        probe = Tokens(st["n_probe"], 12).x
        with torch.no_grad():
            p = torch.softmax(model(input_ids=probe).logits.float(), -1).reshape(-1, model.config.vocab_size).numpy()
        np.save(os.path.join(out, "probe.npy"), p.astype(np.float32))
        res["sha"] = sha_state(model)
        shutil.rmtree(os.path.join(out, "trainer"), ignore_errors=True); shutil.rmtree(os.path.join(out, "ckpt"), ignore_errors=True)  # disk
    with open(os.path.join(out, "result.json"), "w") as f:
        json.dump(res, f, sort_keys=True)
    with open(os.path.join(out, "timing.json"), "w") as f:
        json.dump({"train_seconds": dt, "steps_run": res["global_step"] - (st["pause"] if cfg["phase"] == "second" else 0)}, f)


if __name__ == "__main__":
    main(json.loads(sys.argv[1]), sys.argv[2])

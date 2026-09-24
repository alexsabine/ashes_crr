# Citations checked on the day (R10): lossless pause-and-resume in real ML systems, 2026-09-24

Scope: what it takes, in real ML systems, for a pause-and-resume of a learning system to be "lossless", meaning the
resumed run continues exactly as if no pause had happened. There are three parts: (1) full-state checkpointing for exact
resumption, (2) behaviour keyed to wall-clock time rather than to steps, (3) worlds that do or do not move on during a
pause.

Method: every source below was fetched on 2026-09-24 (UTC) with `curl` through the session proxy. PDFs were converted to
text with `pdfminer.six`. WebSearch was used only to find sources. Quotes are verbatim from the fetched text; line
breaks and hyphenation from PDF extraction have been re-joined. "Access" states what was read. Anything marked
**Inference** is this document's own reading, not something the sources say. Nothing here is a ledger row or evidence
about CRR (R8). It is engineering context only.

Blocked or partly blocked on the day:
- `dmtcp.sourceforge.io` returned **HTTP 403**. The GitHub README was used instead.
- `ieeexplore.ieee.org/document/1193727` (Katsikopoulos & Engelbrecht) returned **HTTP 202 with an empty body**, which
  looks like a bot challenge. Only the Crossref metadata and a secondary description were read. The paper's text was
  **not** read.
- `docs.mosaicml.com/.../generated/composer.utils.reproducibility.html` returned **HTTP 404**. The live page is at
  `.../api_reference/composer.utils.reproducibility.html`.
- `lightning.ai/docs/...` HTML pages return a JavaScript shell ("Taking longer than expected — try refreshing the
  page."). The reStructuredText sources on GitHub were read instead. The 1.7.7 path `docs/source-pytorch/advanced/fault_tolerant_training.rst`
  returned **HTTP 404**. The file is at `clouds/`.
- `api.github.com` refused the request ("GitHub access to this repository is not enabled for this session"). Branch
  HEADs were therefore pinned with `git ls-remote`, as noted per source.
- The PyTorch recipe "Saving and loading a general checkpoint" is marked deprecated on the page and redirects to the
  main tutorial. Both were fetched.

---

## Part 1: full-state checkpointing for exact resumption

### 1.1 PyTorch, "Reproducibility" note
- Org: PyTorch (Linux Foundation). URL: https://docs.pytorch.org/docs/2.14/notes/randomness.html. `stable` redirects
  to `2.14`. The page shows "Created On: May 14, 2026 | Last Updated On: May 14, 2026". HTTP 200. Access: full docs page.
- Quotes:
  - "Completely reproducible results are not guaranteed across PyTorch releases, individual commits, or different
    platforms. Furthermore, results may not be reproducible between CPU and GPU executions, even when using identical
    seeds."
  - "You can use torch.manual_seed() to seed the RNG for all devices (both CPU and CUDA)".
  - "If you or any of the libraries you are using rely on NumPy, you can seed the global NumPy RNG with:
    np.random.seed(0) However, some applications and libraries may use NumPy Random Generator objects, not the global
    RNG ... and those will need to be seeded consistently as well."
  - "Due to benchmarking noise and different hardware, the benchmark may select different algorithms on subsequent
    runs, even on the same machine. Disabling the benchmarking feature with torch.backends.cudnn.benchmark = False
    causes cuDNN to deterministically select an algorithm".
  - "torch.use_deterministic_algorithms() lets you configure PyTorch to use deterministic algorithms instead of
    nondeterministic ones where available, and to throw an error if an operation is known to be nondeterministic (and
    without a deterministic alternative)."
  - The SDPA table: "SDPBackend.FLASH_ATTENTION Deterministic Non-deterministic The backward pass uses
    non-deterministic atomic operations by default." And: "Bitwise matching numerics across different SDPA backends
    are not guaranteed, even for the same inputs and dtype."
  - "DataLoader will reseed workers following the Randomness in multi-process data loading algorithm. Use
    worker_init_fn() and generator to preserve reproducibility".

### 1.2 PyTorch, `torch.use_deterministic_algorithms`
- URL: https://docs.pytorch.org/docs/2.14/generated/torch.use_deterministic_algorithms.html (PyTorch 2.14). HTTP 200.
  Access: docs page.
- Quotes: "Sets whether PyTorch operations must use “deterministic” algorithms. That is, algorithms which, given the same
  input, and when run on the same software and hardware, always produce the same output." / "This setting alone is not
  always enough to make an application reproducible." / "This flag does not detect or prevent nondeterministic behavior
  caused by calling an inplace operation on a tensor with an internal memory overlap".
  The page also lists operations that "will throw a RuntimeError when mode=True", for example "torch.nn.AdaptiveAvgPool2d
  when attempting to differentiate a CUDA tensor".

### 1.3 PyTorch, RNG state accessors
- `torch.get_rng_state`: https://docs.pytorch.org/docs/2.14/generated/torch.get_rng_state.html (HTTP 200): "Returns
  the random number generator state as a torch.ByteTensor." Note: "The returned state is for the default generator on
  CPU only."
- `torch.cuda.get_rng_state_all`: https://docs.pytorch.org/docs/2.14/generated/torch.cuda.get_rng_state_all.html
  (HTTP 200): "Return a list of ByteTensor representing the random number states of all devices."
- DataLoader, https://docs.pytorch.org/docs/2.14/data.html (HTTP 200), "Randomness in multi-process data loading": "By
  default, each worker will have its PyTorch seed set to base_seed + worker_id, where base_seed is a long generated by
  main process using its RNG (thereby, consuming a RNG state mandatorily) or a specified generator. However, seeds for
  other libraries may be duplicated upon initializing workers".

### 1.4 PyTorch, saving a general checkpoint, and the LR scheduler state
- Tutorial "Saving and Loading Models": https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html (Tutorials
  2.14.0+cu130). The page shows "Created On: Aug 29, 2018 | Last Updated: Jun 26, 2025 | Last Verified: Nov 05, 2024".
  HTTP 200. Access: full page.
  - "When saving a general checkpoint, to be used for either inference or resuming training, you must save more than
    just the model’s state_dict. It is important to also save the optimizer’s state_dict, as this contains buffers and
    parameters that are updated as the model trains. Other items that you may want to save are the epoch you left off
    on, the latest recorded training loss, external torch.nn.Embedding layers, etc."
  - "If you wish to resuming training, call model.train() to ensure these layers are in training mode." (sic)
- The recipe page https://docs.pytorch.org/tutorials/recipes/recipes/saving_and_loading_a_general_checkpoint.html
  (HTTP 200) now says: "This tutorial was deprecated. There is a newer tutorial that covers the same topic".
- `LRScheduler`: https://docs.pytorch.org/docs/2.14/generated/torch.optim.lr_scheduler.LRScheduler.html (HTTP 200):
  "last_epoch (int) – Index of the last epoch seen by the scheduler. Use -1 (default) to initialize the scheduler. Only
  use a non-default value when restoring this scheduler from a saved checkpoint." / "state_dict() Return the state of
  the scheduler as a dict. It contains an entry for every variable in self.__dict__ which is not the optimizer." /
  "Initializing a scheduler overwrites its optimizer’s param_group["lr"]s. When restoring a checkpoint, initialize the
  scheduler before calling your optimizer’s load_state_dict() to avoid overwriting the loaded learning rates."
- **Inference:** the tutorial's list of what to save (model, optimizer, epoch, loss) does not mention RNG state,
  scheduler state or data-loader position. Those come from the pages in 1.1, 1.3 and 1.5.

### 1.5 torchdata `StatefulDataLoader` (mid-epoch resumption)
- Org: PyTorch / Meta. URL: https://meta-pytorch.org/data/beta/torchdata.stateful_dataloader.html (redirected from
  pytorch.org). The page shows "TorchData 0.11.0 documentation". PyPI latest is torchdata 0.11.0, uploaded 2025-02-20.
  HTTP 200. Access: docs page. Also read: the tutorial https://meta-pytorch.org/data/beta/stateful_dataloader_tutorial.html
  (HTTP 200).
- Quotes:
  - "StatefulDataLoader is a drop-in replacement for torch.utils.data.DataLoader which offers state_dict /
    load_state_dict methods for handling mid-epoch checkpointing".
  - "By default, the state includes the number of batches yielded and uses this to naively fast-forward the sampler
    (map-style) or the dataset (iterable-style). However if the sampler and/or dataset include state_dict /
    load_state_dict methods, then it will call them during its own state_dict / load_state_dict calls. Under the hood,
    StatefulDataLoader handles aggregation and distribution of state across multiprocess workers (but not across
    ranks)."
  - "Setting in_order to False currently has no guarantees for state management."
  - Tutorial: "If your dataset has worker-specific state (eg RNG transform state) you can add state_dict /
    load_state_dict methods to your dataset." / "Calling load_state_dict requires StatefulDataLoader` to have same
    num_workers as those of the provided state_dict."

### 1.6 Hugging Face Transformers `Trainer`
- Org: Hugging Face. Docs: https://huggingface.co/docs/transformers/main_classes/trainer. The page links resolve to
  `v5.17.0`. PyPI latest is transformers 5.17.0, uploaded 2026-09-09. HTTP 200. Access: API docs page. Source read at
  tag `v5.17.0`: https://raw.githubusercontent.com/huggingface/transformers/v5.17.0/src/transformers/trainer.py (HTTP 200).
- Docs quotes:
  - `train(resume_from_checkpoint=...)`: "If present, training will resume from the model/optimizer/scheduler states
    loaded here."
  - `ignore_data_skip`: "When resuming training, skip fast-forwarding through the dataset to reach the previous state.
    If True, training starts from the beginning of the dataset (faster resume but results won’t match interrupted
    training). If False, skips seen data (slower resume but exact continuation)."
  - `save_only_model`: "Save only model weights, not optimizer/scheduler/RNG state. Significantly reduces checkpoint size
    but prevents resuming training from the checkpoint."
  - `full_determinism`: "If True, enable_full_determinism() is called instead of set_seed() to ensure reproducible
    results in distributed training. Important: this will negatively impact the performance, so only use it for
    debugging."
  - `enable_jit_checkpoint`: "Enable Just-In-Time checkpointing on SIGTERM signal for graceful termination on preemptible
    workloads. ... Required grace period ≥ longest iteration time + checkpoint save time."
- Source quotes (v5.17.0): the file-name constants `TRAINER_STATE_NAME = "trainer_state.json"`, `OPTIMIZER_NAME =
  "optimizer.pt"`, `SCALER_NAME = "scaler.pt"`, `SCHEDULER_NAME = "scheduler.pt"`. `_save_rng_state` ("Save random number
  generator states for reproducible resumption.") stores `"python": random.getstate()`, `"numpy":
  np.random.get_state()`, `"cpu": torch.random.get_rng_state()`, and the CUDA, XLA, NPU, HPU, MLU and MUSA states. It
  writes them to `rng_state.pth`, or to `rng_state_{process_index}.pth` in distributed runs. The load path logs: "Didn't
  find an RNG file, if you are resuming a training that was launched in a distributed fashion, reproducibility is not
  guaranteed." On resume it logs "Fast-forwarding the dataloader past {epochs_trained} epochs and
  {steps_trained_in_current_epoch} batches to resume from the exact training state." It uses `skip_first_batches` and
  then reloads the RNG state after the skip ("need to sync after if we skipped the batches ... for shuffle order
  reason").
- **Inference:** "exact continuation" in HF means restoring the data position plus the RNG, optimizer, scheduler and
  scaler state. It is not bitwise equality under nondeterministic kernels, which is governed by 1.1 and 1.2.

### 1.7 PyTorch Lightning / Lightning Fabric
- Checkpoint contents (Lightning master, rst source):
  https://raw.githubusercontent.com/Lightning-AI/pytorch-lightning/master/docs/source-pytorch/common/checkpointing_basic.rst
  (HTTP 200; repo HEAD at `git ls-remote` time `84df182f50ab34301aabb3c0eb4031815bfb413d`). Access: doc source.
  - "Inside a Lightning checkpoint you'll find: 16-bit scaling factor (if using 16-bit precision training) - Current
    epoch - Global step - LightningModule's state_dict - State of all optimizers - State of all learning rate schedulers
    - State of all callbacks (for stateful callbacks) - State of datamodule (for stateful datamodules) - The
    hyperparameters ... - State of Loops".
  - "# automatically restores model, epoch, step, LR schedulers, etc... trainer.fit(model,
    ckpt_path="path/to/your/checkpoint.ckpt")".
  - **Inference:** the list does not name RNG state.
- Fabric: https://raw.githubusercontent.com/Lightning-AI/pytorch-lightning/master/docs/source-fabric/guide/checkpoint/checkpoint.rst
  (HTTP 200): "To save and resume your training, you need to define which variables in your program you want to have
  saved. Put everything into a dictionary, including models and optimizers and whatever metadata you have".
- Fault-tolerant training, experimental, later removed:
  - 1.7.7 docs source `docs/source-pytorch/clouds/fault_tolerant_training_basic.rst` (HTTP 200): "With Fault Tolerant
    Training, when Trainer.fit() fails in the middle of an epoch during training or validation, Lightning will restart
    exactly where it failed, and everything will be restored (down to the batch it was on even if the dataset was
    shuffled)." / "Fault-tolerant Training is currently an experimental feature within Lightning." The expert page
    says it is enabled via "PL_FAULT_TOLERANT_TRAINING=1".
  - CHANGELOG (master, `src/lightning/pytorch/CHANGELOG.md`, HTTP 200). Under "[1.6.0] - 2022-03-29": "Enable Fault
    Tolerant Manual Training". Under "[2.0.0] - 2023-03-15": "Removed support for the experimental
    `PL_FAULT_TOLERANT_TRAINING` environment flag ([#16516] ..., [#16533] ...)".

### 1.8 MosaicML Composer
- Org: MosaicML / Databricks. Docs `stable`. The page footer shows "Copyright © 2025, MosaicML, Inc.". PyPI latest is
  mosaicml 0.32.1, uploaded 2025-07-26. Access: docs pages (HTTP 200).
  - Checkpointing, https://docs.mosaicml.com/projects/composer/en/stable/trainer/checkpointing.html: `list(state_dict)`
    gives `['state', 'rng']`, and `list(state_dict['state'].keys())` gives `['model', 'optimizers', 'schedulers',
    'algorithms', 'callbacks', 'scaler', 'timestamp', 'rank_zero_seed', 'run_name', 'dataset_state', 'integrations',
    'metadata']`.
  - Auto resumption, https://docs.mosaicml.com/projects/composer/en/stable/notes/resumption.html: "With autoresume,
    users can re-submit the _same_ code to the training run, and the trainer will handle finding and resuming from the
    latest checkpoints."
  - `composer.utils.reproducibility`, https://docs.mosaicml.com/projects/composer/en/stable/api_reference/composer.utils.reproducibility.html:
    "Note that the seed must also be passed to the Trainer, otherwise the Trainer would generate a random seed based on
    the timestamp". It lists the functions "get_rng_state The state of the RNG objects." / "load_rng_state Restore the
    RNG state."

### 1.9 Megatron-LM and DeepSpeed (model-parallel RNG trackers)
- Megatron-LM (NVIDIA), branch `main` fetched via raw.githubusercontent.com. HEAD at `git ls-remote` time was
  `ec806b20a0a976924c1668486c3554ffb90c000e`. Access: source.
  - `megatron/core/tensor_parallel/random.py`: "class CudaRNGStatesTracker: Tracker for the cuda RNG states. Using the
    `add` method, a cuda rng state is initialized based on the input `seed` and is assigned to `name`. Later, by forking
    the rng state, we can perform operations and return to our starting cuda state."
  - `megatron/training/checkpointing.py`, `get_rng_state`: `'random_rng_state': random.getstate()`, `'np_rng_state':
    np.random.get_state()`, `'torch_rng_state': torch.get_rng_state()`, `'cuda_rng_state': torch.cuda.get_rng_state()`,
    `'rng_tracker_states': tensor_parallel.get_cuda_rng_tracker().get_states()` ("Collect rng state across data
    parallel ranks.").
  - `megatron/training/arguments.py`: `--no-save-rng` "Do not save current rng state." / `--no-load-rng` "Do not load
    rng state when loading checkpoint."
- DeepSpeed, branch `master`, `deepspeed/runtime/activation_checkpointing/checkpointing.py`. HEAD at `git ls-remote` time
  was `3571027338c85c3f2d74c896886bebf868680bad`. The file has the same `CudaRNGStatesTracker` docstring, with
  `get_states` ("Get rng states. Copy the dictionary so we have direct pointers to the states") and `set_states`.

### 1.10 JAX PRNG keys, Orbax checkpointing, Grain
- JAX, "Pseudorandom numbers", https://docs.jax.dev/en/latest/random-numbers.html (latest; HTTP 200; docs page):
  "To avoid these issues, JAX avoids implicit global random state, and instead tracks state explicitly via a random
  key" / "The key is effectively a stand-in for NumPy’s hidden state object, but we pass it explicitly to jax.random()
  functions. Importantly, random functions consume the key, but do not modify it" / "never reuse keys (unless you want
  identical outputs)".
- Orbax, "Checkpointing with Orbax", https://orbax.readthedocs.io/en/latest/guides/checkpoint/orbax_checkpoint_101.html
  (latest; HTTP 200): "In most cases, users will wish to save and restore a PyTree representing a model state over the
  course of many training steps." / "Beware: CheckpointManager.save(...) happens in a background thread by default."
- Grain, https://google-grain.readthedocs.io/en/latest/ (HTTP 200): "Resilient to preemptions Grain is designed such
  that checkpoints have minimal size. After pre-emption, Grain can resume from where it left off and produce the same
  output as if it was never preempted."
- **Inference:** in JAX the RNG is an ordinary array in the program state. It survives a pause only if the user puts
  the current key into the saved PyTree. The Orbax page does not say this in the text read.

### 1.11 Papers on nondeterminism and bitwise reproducibility
- **Summers, C.; Dinneen, M. J.** "Nondeterminism and Instability in Neural Network Optimization." arXiv:2103.04514,
  current **v3** (10 Jul 2021); v1 8 Mar 2021. Comment: "ICML 2021". Access: abstract. "We show that even one-bit
  changes in initial parameters result in models converging to vastly different values."
- **Zhuang, D.; Zhang, X.; Song, S. L.; Hooker, S.** "Randomness In Neural Network Training: Characterizing The Impact of
  Tooling." arXiv:2106.11872, **v1** (22 Jun 2021). Access: abstract. "the cost of ensuring determinism varies
  dramatically between neural network architectures and hardware types, e.g., with overhead up to 746%, 241%, and 196%
  on a spectrum of widely used GPU accelerator architectures, relative to non-deterministic training."
- **Xie, P.; Zhang, X.; Chen, S.** "RepDL: Bit-level Reproducible Deep Learning Training and Inference." arXiv:2510.09180,
  **v1** (10 Oct 2025). Access: abstract. "These issues stem from two origins: random number generation and
  floating-point computation. While randomness can be controlled through deterministic configurations, floating-point
  inconsistencies remain largely unresolved."
- **Yang, Z.; Riasanovsky, N. J.; Deng, W.; Sarkar, V.** "Taming Bitwise Behavior in GPU Kernels with Tensor Core ..."
  arXiv:2609.11356, **v1** (10 Sep 2026). Access: abstract. "deterministic implementations of the same kernel can
  still differ bit for bit. Floating-point reduction order is the primary cause, alongside partial-sum precision, fused
  multiply-add operations, and rounding placement." / "A tile shape chosen for performance therefore also determines the
  arithmetic, potentially breaking batch invariance."
- **Donaghy, J.; Wilcox, B.; Ersoy, O.; et al.** "OPEN-1B: A Fully Auditable Training Run." arXiv:2609.17380, **v1**
  (15 Sep 2026). Access: abstract plus full text (arXiv HTML v1).
  - Abstract: "Deep learning frameworks often offer a deterministic execution mode, allowing reproducible operations on
    the same machines. Unfortunately, this determinism does not carry across hardware".
  - §2.3: "Changing the number of data parallel workers results in different batch orderings. Further, each rank has a
    different random number generator, worker prefetch queue, and rank-striped sharding." / "Training on any topology,
    resuming from any checkpoint, and replaying on a single consumer-grade device all enumerate the same windows with
    the same contents."
  - "Resumable state. The complete position of the stream is captured by a small, rank-independent record which
    includes the number of documents consumed from each source, the per-source epoch counters, the exact bit-generator
    state of the mix RNG, and the partial window left in the packing buffer at save time."
  - "Optimizer state is checkpointed and hashed in FP32; thus, an audit replay can reconstruct the moments exactly."
- **Mohan, J.; Phanishayee, A.; Chidambaram, V.** "CheckFreq: Frequent, Fine-Grained DNN Checkpointing." USENIX FAST
  2021 (19th USENIX Conference on File and Storage Technologies), pp. 203–216 per the proceedings footer. PDF:
  https://www.usenix.org/system/files/fast21-mohan.pdf (HTTP 200). Access: full text.
  - "Existing data iterators in frameworks like PyTorch, and MxNet do not support resumability. When the job is
    interrupted, these iterators can either miss out, or repeat data items in an epoch, resulting in loss in model
    accuracy when resuming at iteration granularity."
  - "they violate the data invariant in the presence of interruptions, resulting in upto the 13% drop in accuracy for
    popular models ResNet18 (Fig 6)."
  - "The iterator uses epoch seeded psuedo-random transformations, that can reconstruct the iterator state as it was
    prior to interruption." (sic) / "Checkpointing data iterator state ... requires persisting two integers - epoch and
    iteration number".

### 1.12 Process-level checkpoint/restart
- **CRIU**, https://criu.org/Main_Page (HTTP 200; wiki): "It can freeze a running container (or an individual
  application) and checkpoint its state to disk. The data saved can be used to restore the application and run it
  exactly as it was during the time of the freeze." Limits, from https://criu.org/What_cannot_be_checkpointed (HTTP 200):
  "By default CRIU allows to dump the set of processes and their resources if this set has no connections outside." /
  "If a task has opened or mapped any character or block device, this typically means, it wants some connection to the
  hardware. In this case dump (and restore) is impossible."
- **NVIDIA cuda-checkpoint**, https://raw.githubusercontent.com/NVIDIA/cuda-checkpoint/main/README.md (HTTP 200; HEAD
  `00d5cce84c628088d6caa203fc4af40c1538b6f7`): "This utility can be used to transparently checkpoint and restore CUDA
  state within a running Linux process, and can be combined with CRIU ... to fully checkpoint CUDA applications." /
  "Transparent, per-process checkpointing offers a middle ground between virtual machine checkpointing and
  application-driven checkpointing."
- **DMTCP**: sourceforge site **HTTP 403**. GitHub README https://raw.githubusercontent.com/dmtcp/dmtcp/master/README.md
  (HTTP 200; HEAD `38767e855040a70f69ceaa8177d8579263d0ddec`): "DMTCP is a tool to transparently checkpoint the state of
  multiple simultaneous applications, including multi-threaded and distributed applications. It operates directly on
  the user binary executable, without any Linux kernel modules or other kernel modifications."

---

## Part 2: schedules and features keyed to steps versus wall-clock time

### 2.1 Step-keyed learning-rate schedules
- PyTorch `torch.optim`, https://docs.pytorch.org/docs/2.14/optim.html (HTTP 200): "torch.optim.lr_scheduler.LRScheduler
  provides several methods to adjust the learning rate based on the number of epochs." The canonical loop calls
  `optimizer.step()` and then `scheduler.step()`. "If you use the learning rate scheduler (calling scheduler.step())
  before the optimizer’s update (calling optimizer.step()), this will skip the first value of the learning rate
  schedule."
- **Li, M.; Yumer, E.; Ramanan, D.** "Budgeted Training: Rethinking Deep Neural Network Training Under Resource
  Constraints." arXiv:1905.04753, current **v4** (30 Jun 2020). Comment: "ICLR 2020". Access: abstract. "We focus on the
  number of optimization iterations as the representative resource. Under such a setting, we show that it is critical to
  adjust the learning rate schedule according to the given budget."

### 2.2 Wall-clock-keyed training behaviour (documented cases)
- **Composer, "Time"**, https://docs.mosaicml.com/projects/composer/en/stable/trainer/time.html (HTTP 200). Its unit
  table includes "Seconds "sec" "30sec" TimeUnit.SECOND", and it says: "There are some exceptions – for example dur is
  not valid when setting max_duration as that is circular and seconds cannot be used for schedulers and max_duration."
  `composer.Timestamp`
  (https://docs.mosaicml.com/projects/composer/en/stable/api_reference/generated/composer.Timestamp.html): "The
  timestamp measures training progress in terms of iterations, epochs, batches, samples, tokens, and wall clock time." /
  "total_wct (timedelta, optional) – The elapsed duration from the beginning of training." (`timestamp` is one of the
  checkpointed keys in 1.8.)
- **Lightning `Trainer(max_time=...)`**, source `src/lightning/pytorch/trainer/trainer.py` (master, HTTP 200 on retry
  after an HTTP 429): "max_time: Stop training after this amount of time has passed. Disabled by default (None)."
- **Lightning `Timer` callback**, `src/lightning/pytorch/callbacks/timer.py` (master): "The Timer callback tracks the
  time spent in the training, validation, and test loops and interrupts the Trainer if the given time limit for the
  training loop is reached." The code has `state_dict` returning `{"time_elapsed": {...}}` and `load_state_dict` setting
  `self._offset = time_elapsed.get(RunningStage.TRAINING.value, 0)`.
  **Inference:** the restored budget counts training time accumulated before the checkpoint plus time in the new
  process. Downtime between processes is therefore not charged, so the budget follows the learner's own clock, not the
  world's.
- **Lightning `ModelCheckpoint(train_time_interval=...)`**, `src/lightning/pytorch/callbacks/model_checkpoint.py`:
  "train_time_interval: Checkpoints are monitored at the specified time interval. ... This is not guaranteed to execute
  at the exact time specified, but should be close."
- **HF `enable_jit_checkpoint`** (1.6) is triggered by a wall-clock signal (SIGTERM with a grace period).
- **Geiping, J.; Goldstein, T.** "Cramming: Training a Language Model on a Single GPU in One Day." arXiv:2212.14034,
  **v1** (28 Dec 2022). Access: abstract. "We investigate the downstream performance achievable with a transformer-based
  language model trained completely from scratch with masked language modeling for a single day on a single consumer
  GPU."
- **Gymnasium `TimeLimit`**, https://gymnasium.farama.org/api/wrappers/misc_wrappers/ (gymnasium 1.3.0 on PyPI,
  2026-04-22; HTTP 200): "Limits the number of steps for an environment through truncating the environment if a maximum
  number of timesteps is exceeded." The RL "time limit" is counted in steps.

### 2.3 Time as an input feature
- **Kazemi, S. M.; et al.** "Time2Vec: Learning a Vector Representation of Time." arXiv:1907.05321, **v1** (11 Jul
  2019). Access: abstract. "Time is an important feature in many applications involving events that occur synchronously
  and/or asynchronously." / "we take an orthogonal but complementary approach by providing a model-agnostic vector
  representation for time, called Time2Vec".

### 2.4 LLMs: the current date injected into context, and temporal grounding
- **Anthropic, "System prompts" release notes**, https://platform.claude.com/docs/en/release-notes/system-prompts/overview
  (redirected from docs.claude.com; HTTP 200; docs page): "Claude's web interface (claude.ai) and mobile apps use a
  system prompt to provide up-to-date information, such as the current date, to Claude at the start of every
  conversation. ... These system prompt updates do not apply to the Claude API."
  The Claude Opus 4 page (https://platform.claude.com/docs/en/release-notes/system-prompts/claude-opus-4; entries dated
  e.g. "July 31, 2025", "August 5, 2025") contains: "The current date is {{currentDateTime}}." and "It answers all
  questions the way a highly informed individual in January 2025 would if they were talking to someone from
  {{currentDateTime}}".
- **Zhao, B.; Brumbaugh, Z.; Wang, Y.; Hajishirzi, H.; Smith, N. A.** "Set the Clock: Temporal Alignment of Pretrained
  Language Models." arXiv:2402.16797, current **v2** (9 Jun 2024). Comment: "Accepted as Findings of ACL 2024". Access:
  abstract. "Language models (LMs) are trained on web text originating from many points in time and, in general, without
  any explicit temporal grounding." / "pretrained LMs (e.g., LLaMa2), despite having a recent pretraining cutoff (e.g.,
  2022), mostly answer questions using earlier knowledge (e.g., in 2019)."
- **Cheng, J.; Marone, M.; Weller, O.; Lawrie, D.; Khashabi, D.; Van Durme, B.** "Dated Data: Tracing Knowledge Cutoffs
  in Large Language Models." arXiv:2403.12958, current **v2** (17 Sep 2024). Access: abstract. "we find that effective
  cutoffs often differ from reported cutoffs."
- Not checked today: other providers' documentation on date injection.

---

## Part 3: a world that does or does not move on during a pause

### 3.1 Real-time and concurrent RL
- **Ramstedt, S.; Pal, C.** "Real-Time Reinforcement Learning." arXiv:1911.04448, current **v4** (12 Dec 2019). Comment:
  "Neural Information Processing Systems (2019)". Access: full text (v4 PDF).
  - Abstract: "Markov Decision Processes (MDPs) ... are often used in a way that wrongfully assumes that the state of an
    agent's environment does not change during action selection."
  - §1: "this framework is ill suited for real-time applications in which the environment’s state continues to evolve
    while the agent selects an action ... Nevertheless, this framework has been used for real-time problems using what
    are essentially tricks, e.g. pausing a simulated environment during action selection or ensuring that the time
    required for action selection is negligible".
  - §1.1: "We say the interaction is turn-based, because the environment pauses while the agent selects an action and
    the agent pauses until it receives a new observation from the environment. ... The state does not change during the
    action selection process."
- **Xiao, T.; Jang, E.; Kalashnikov, D.; Levine, S.; Ibarz, J.; Hausman, K.; Herzog, A.** "Thinking While Moving: Deep
  Reinforcement Learning with Concurrent Control." arXiv:2004.06089, current **v4** (25 Apr 2020). Comment: "Published
  as a conference paper at ICLR 2020". Access: full text (v4 PDF).
  - "all of these examples use a blocking observe-think-act paradigm: the agent assumes that the environment will remain
    static while it thinks ... As an example, consider a dynamic task such as catching a ball: it is not possible to
    pause the ball mid-air while waiting for the agent to decide on the next control to command."
  - "This assumption holds true in most simulated environments ... The system is treated in a sequential manner: the
    agent observes a state, freezes time while computing an action, and finally applies the action and unfreezes time."

### 3.2 Delayed MDPs
- **Katsikopoulos, K. V.; Engelbrecht, S. E.** "Markov decision processes with delays and asynchronous cost
  collection." *IEEE Transactions on Automatic Control* 48(4):568–574, April 2003, DOI 10.1109/TAC.2003.809799 (Crossref
  API, HTTP 200). Access: **metadata only**. IEEE Xplore returned HTTP 202 with an empty body. The paper's text was not
  read and nothing from it is quoted.
- **Ramstedt, S.; Bouteiller, Y.; Beltrame, G.; Pal, C.; Binas, J.** (author order as on arXiv; submitted by Bouteiller)
  "Reinforcement Learning with Random Delays." arXiv:2010.02966, current **v3** (4 May 2021). Comment: "ICLR 2021".
  Access: full text (v3 PDF).
  - "To ensure the Markov property in delayed settings, it is necessary to augment the delayed observation with at least
    the last K sent actions. K is the combined maximum possible observation and action delay."
  - Related work, describing Katsikopoulos & Engelbrecht (this is a secondary description): "We trace our line of
    research back to Katsikopoulos & Engelbrecht (2003), who provided the first discussion about Delayed Markov Decision
    Processes. In particular, they were interested in asynchronous rewards".

### 3.3 Interruption in safe-RL theory
- **Orseau, L. (Google DeepMind); Armstrong, S. (FHI, Oxford).** "Safely Interruptible Agents." UAI 2016, accepted paper
  ID 68 (listing https://www.auai.org/uai2016/accepted.php, HTTP 200). PDF https://www.auai.org/uai2016/proceedings/papers/68.pdf
  (HTTP 200). Access: full text.
  - "To make the human interruptions not appear as being part of the task at hand, instead of modifying the observations
    received by the agent we forcibly temporarily change the behaviour of the agent itself. It then looks as if the agent
    “decides” on its own to follow a different policy, called the interruption policy."
  - The paper defines the interruptible policy as INT^θ(π)(a_t|h_<t) = θ_t I(h_<t) π^INT(a_t|h_<t) + (1 − θ_t I(h_<t))
    π(a_t|h_<t) and says: "Hence they are part of the agent and not of the environment."
  - **Inference:** in this formalism an interruption is not a pause. The environment keeps stepping while the agent
    acts under π^INT, and interrupted steps remain in the history h. Safe interruptibility is a property of the learner
    (off-policy learning), not of a frozen world.

### 3.4 Streams that do not wait, and streams that buffer
- **Ghunaim, Y.; Bibi, A.; Alhamoud, K.; Alfarra, M.; Hammoud, H. A. A. K.; Prabhu, A.; Torr, P. H. S.; Ghanem, B.**
  "Real-Time Evaluation in Online Continual Learning: A New Hope." arXiv:2302.01047, current **v3** (24 Mar 2023).
  Comment: "Accepted at CVPR'23 as Highlight". Access: full text (v3 PDF).
  - "a practical real-time evaluation of continual learning, in which the stream does not wait for the model to
    complete training before revealing the next data for predictions."
  - Fig. 2: "Due to the mismatch between the stream speed and the model computational cost, an ”older version” of the
    model predicts samples while the model is being trained. Therefore, k-1 potential training batches are skipped for
    each training step."
  - "any OCL method that is computationally more expensive than ER will not keep up with the stream speed, and thus will
    be forced to skip training on a fraction of the incoming stream samples."
- **Prabhu, A.; Cai, Z.; Dokania, P.; Torr, P.; Koltun, V.; Sener, O.** "Online Continual Learning Without the Storage
  Constraint." arXiv:2305.09253, current **v2** (2 Nov 2023). Access: abstract. "a broad range of real-world applications
  are primarily constrained by computational costs rather than storage limitations. In this paper, we target such
  applications, investigating the online continual learning problem under relaxed storage constraints and limited
  computational budgets."
- **Apache Kafka 4.3 documentation.** The landing page lists releases up to 4.3.
  - Design, https://kafka.apache.org/43/design/design/ (HTTP 200): "the position of a consumer in each partition is just
    a single integer, the offset of the next message to consume. This makes the state about what has been consumed very
    small, just one number for each partition. This state can be periodically checkpointed." / "A consumer can
    deliberately rewind back to an old offset and re-consume data." / "If the consumer never crashed it could just store
    this position in memory, but if the consumer fails and we want this topic partition to be taken over by another
    process, the new process will need to choose an appropriate position from which to start processing." / "Otherwise,
    Kafka guarantees at-least-once delivery by default".
  - On retention: "the simpler approach to data retention where old log data is discarded after a fixed period of time
    or when the log reaches some predetermined size".
  - Introduction, https://kafka.apache.org/43/getting-started/introduction/ (HTTP 200): "Events in a topic can be read as
    often as needed-unlike traditional messaging systems, events are not deleted after consumption. Instead, you define
    for how long Kafka should retain your events through a per-topic configuration setting, after which old events will
    be discarded."

### 3.5 Simulators whose state can be saved and restored exactly
- **MuJoCo** (Google DeepMind), docs `stable`; PyPI latest mujoco 3.14.0, uploaded 2026-09-22. Access: docs pages (HTTP
  200).
  - Computation, https://mujoco.readthedocs.io/en/stable/computation/index.html: "MuJoCo’s simulation pipeline is
    entirely deterministic and reproducible – if a state in a trajectory is saved and reloaded and mj_step called again,
    the resulting next state will be identical. However, there are some important caveats: Save all the required
    integration state components. In particular warmstart accelerations have only a very small effect on the next state,
    but should be saved if bit-wise equality is required." / "Exact reproducibility is only guaranteed within a single
    version, on the same architecture."
  - Simulation, https://mujoco.readthedocs.io/en/stable/programming/simulation.html: "The integration state
    (mjSTATE_INTEGRATION) is the union of all the above mjData fields and constitutes the entire set of inputs to the
    forward dynamics. The pipeline output of two mjData instances with the same integration state will be identical."
    The functions are "mj_getState, mj_setState, mj_copyState".
- **Arcade Learning Environment** (Farama), `src/ale/ale_interface.hpp` on `main` (HTTP 200; HEAD
  `6d91c829ee864b4789de7101b41d8cce2904d742`; PyPI ale-py 0.12.1, 2026-08-16). Access: source header. The docs pages
  (python/cpp/gymnasium interface) do not mention clone/restore.
  - "This makes a copy of the environment state. By defualt this copy does *not* include pseudorandomness making it
    suitable for planning purposes. If `include_prng` is set to true, then the pseudorandom number generator is also
    serialized." (sic) `ALEState cloneState(bool include_rng = false);`
  - "Reverse operation of cloneState(). This will restore the ALEState, if it was cloned including the RNG then the RNG
    will be restored. Otherwise the current state of the RNG will be kept as is."
- **Gymnasium `Env`**, https://gymnasium.farama.org/api/env/ (gymnasium 1.3.0; HTTP 200): "np_random - The random number
  generator for the environment." / "reset() should (in the typical use case) be called with a seed right after
  initialization and then never again." **Inference:** the generic Env API documents seeding but no general state
  save/restore. Exact restoration relies on backend-specific calls such as MuJoCo's `mj_getState`/`mj_setState` or ALE's
  `cloneState`/`restoreState`.

---

## Inference for the design (all of this section is inference)

**What must be checkpointed for exact resumption.** Read together, the sources name these components. The
framework-level savers (HF 1.6, Composer 1.8, Megatron 1.9, OPEN-1B 1.11) each cover most of them. No single tutorial
lists all of them.
1. Model parameters and buffers (for example BatchNorm running statistics), plus the train/eval mode.
2. Optimizer state (moments and step counts). OPEN-1B stores it in FP32 so the replay is exact.
3. LR-scheduler state (`last_epoch` and other attributes), restored in the right order relative to the optimizer
   (PyTorch warning, 1.4).
4. The AMP loss-scaler state (HF `scaler.pt`, Lightning's "16-bit scaling factor", Composer `scaler`).
5. Every RNG: Python `random`, NumPy global state and any `Generator` objects, torch CPU, torch per-device
   (`get_rng_state_all`), model-parallel tracker states (Megatron and DeepSpeed), per-worker and augmentation RNGs in
   the data pipeline. In JAX this is the current key held in the state PyTree.
6. Data-pipeline position: epoch, batch within the epoch, sampler permutation or seed, per-worker iterator state,
   packing buffers. Sources: StatefulDataLoader, CheckFreq, Grain, OPEN-1B's "partial window left in the packing
   buffer". Without this, CheckFreq measured up to a 13 % accuracy drop.
7. Loop and callback counters: global step, epoch, callback state (Lightning "State of Loops", Composer `timestamp`,
   HF `trainer_state.json`), including any wall-clock accumulators (Lightning `Timer`, Composer `total_wct`).
8. Environment (world) state if the learner interacts with one. In simulators this includes the simulator's RNG (ALE
   `include_rng`) and solver warm-starts (MuJoCo `qacc_warmstart`).

**Known gaps between "resumed" and "bitwise identical".**
- Nondeterministic kernels (atomics, cuDNN autotuning, Flash-attention backward) break bitwise equality even with
  identical state. The fixes are `use_deterministic_algorithms(True)`, `cudnn.benchmark=False`, and pinned SDPA backends,
  at a measured cost of up to 746 % overhead (Zhuang et al.).
- Determinism holds only "on the same software and hardware" (PyTorch, MuJoCo). Changing the world size or topology
  changes the batch order and reductions unless the stream is made topology-invariant (OPEN-1B). Some fast kernels
  depend on tile shape and batch composition (Yang et al.).
- Fast-forwarding by skipping batches (HF default, StatefulDataLoader default) is exact only if the sampler and all
  data RNGs are restored in the right order. HF's `ignore_data_skip=True` explicitly gives up exact continuation.
- Libraries differ in what they save by default. Lightning's documented checkpoint contents do not name RNG state, and
  Lightning's exact mid-epoch "fault-tolerant" mode was experimental and was removed in 2.0.0.
- Anything keyed to wall-clock time is not restored by state alone: time budgets, time-interval checkpoints, seeds
  "based on the timestamp" (Composer's note), and dates injected into LLM context. Composer forbids seconds as a unit for
  schedulers and `max_duration`, and Lightning's `Timer` restores elapsed training time, not calendar time.
- Whole-process checkpointing (CRIU with cuda-checkpoint, DMTCP) captures the entire process, including hidden state.
  By default, though, it cannot dump processes with outside connections or hardware devices. It captures the learner,
  not the world it is connected to.

**Which worlds can be paused.**
- *Can be paused exactly:* simulators with a complete state API. MuJoCo's integration state, including warm-starts,
  restores to a bit-identical next state within one version and architecture. ALE's `cloneState(include_rng=true)`
  does the same. Turn-based MDPs are paused by construction (Ramstedt & Pal §1.1).
- *Can be made lossless by buffering:* open-loop streams whose producer does not depend on the learner. A durable log
  plus a checkpointed consumer offset (Kafka) lets the learner resume and consume everything that arrived during
  downtime. This holds only within the retention window, and the delivery guarantee is at-least-once unless
  transactional or idempotent handling is added. The data are complete, but they are consumed late, so the learner
  lags the stream.
- *Cannot be paused:* closed-loop real-time environments. In the physical world the state evolves during computation
  and during downtime ("it is not possible to pause the ball mid-air"). In real-time OCL "the stream does not wait" and
  a slow learner skips batches. In Orseau & Armstrong's formalism an interruption is a period of different agent
  behaviour inside a continuing history, not a frozen world.

**Standard remedies.**
- For the learner: full-state checkpoints (items 1–8), deterministic kernels, a topology-invariant data stream, and
  counters keyed to steps or tokens rather than seconds. Wall-clock budgets should accumulate only the learner's own
  running time (the Lightning `Timer` offset pattern).
- For open-loop data: durable buffering with checkpointed offsets and a retention window longer than the longest
  expected pause.
- For closed-loop real-time worlds, where a lossless pause is not available, the known remedies change the model
  instead: include the delay or elapsed time in the state (real-time MDPs, delay-augmented state with the last K
  actions), learn off-policy so that interrupted segments do not bias learning (safe interruptibility), or train in
  simulators that can be paused exactly.

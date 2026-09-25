# Lossless pause, family "training": literature fetched on the day (2026-09-25)

Scope: pausing, stopping and resuming GPU training losslessly; predictions D1, D2, D8 of `Lossless_Pause/DECLARATION.md`, plus the state inventory a lossless resume needs. Every source was fetched on 2026-09-25 through the session proxy. Quotes are verbatim substrings of the saved raw text (after HTML unescape, removal of U+FFFE/U+00AD, joining of `-\n` hyphenation and whitespace collapse); the check found every quote (count below). This dossier records what the sources say. It gives no verdict on any prediction (R8, R10).

Raw texts are saved under `<scratchpad>/pause_lit/training/`. The claims file is `<scratchpad>/pause_lit/training_claims.json`.

## Fetch failures and absences (stated plainly)

- github.com is refused by the proxy. No GitHub page was fetched: not the Megatron-LM README, not Megatron-LM issues #925/#2369 on determinism, and not NVIDIA/nccl issue #157. The Megatron README section was read from the PyPI long description of megatron-core 0.12.1 instead.
- ACM DL PDF for GEMINI (10.1145/3600006.3613145): HTTP 403. The author copy at cs.rice.edu was used.
- Two guessed NVIDIA URLs returned 404: megatron-core .../api-guide/tensor_parallel.html and nemo-framework .../user-guide/latest/reproducibility.html. No NeMo page on deterministic training was found. The Megatron Core 'Deterministic Training' page (latest and nightly) was used.
- NCCL 2.32.3 documentation (env, collectives, troubleshooting pages): no explicit statement on determinism or run-to-run reproducibility of reductions was found. The only related text is the NCCL_ALGO default (chosen from topology and architecture). The statements on NCCL reduction order come from the Megatron Core docs.
- PyTorch 2.14 `torch.use_deterministic_algorithms` page: CUBLAS_WORKSPACE_CONFIG is not mentioned (0 matches). In PyTorch 2.14 the variable is documented in the CUDA-semantics notes, and its determinism role is documented by cuBLAS 13.4.
- The Megatron README 'Reproducibility' section is present in the megatron-core 0.12.1 PyPI description (uploaded 2025-05-23). It is absent from the 0.19.2 description, where the docs page 'Deterministic Training' replaces it.
- Brief items with no bitwise-across-restart claim: OLMo and OLMo 2 state reproducible data order and containerised environments only. Varuna, Bamboo and Oobleck preserve sync-SGD semantics or the global batch size and make no claim that resumed training is bitwise identical. UCP shows matching loss curves.
- Found but not covered, as out of this family's scope (D6): CRIUgpu, arXiv 2502.16631v1 (23 Feb 2025).

## Sources

### PyTorch notes: Reproducibility

- Version: PyTorch 2.14 docs (page 'Last Updated On: May 14, 2026')
- URL fetched: https://docs.pytorch.org/docs/2.14/notes/randomness.html
- Fetch status (2026-09-25): 200 (docs/stable/notes/randomness.html redirects to 2.14; 2.14 page fetched)
- Raw text: `training/pytorch_randomness_notes.txt`

> Completely reproducible results are not guaranteed across PyTorch releases, individual commits, or different platforms.

> Furthermore, results may not be reproducible between CPU and GPU executions, even when using identical seeds.

*[D1]* States the platform/release dependence in D1; does not mention GPU count.

> Due to benchmarking noise and different hardware, the benchmark may select different algorithms on subsequent runs, even on the same machine.

> The backward pass uses non-deterministic atomic operations by default.

*[D2]* States two D2 sources: cuDNN algorithm selection (benchmark) and atomics (Flash SDPA backward).

> Deterministic operations are often slower than nondeterministic operations, so single-run performance may decrease for your model.

*[context]* Cost of determinism, qualitative; bears on D1's 'needs deterministic algorithms'.

### torch.use_deterministic_algorithms

- Version: PyTorch 2.14 docs
- URL fetched: https://docs.pytorch.org/docs/2.14/generated/torch.use_deterministic_algorithms.html
- Fetch status (2026-09-25): 200 (stable redirects to 2.14)
- Raw text: `training/pytorch_use_deterministic_algorithms.txt`

> algorithms which, given the same input, and when run on the same software and hardware, always produce the same output.

> This setting alone is not always enough to make an application reproducible.

*[D1]* States the same-software-and-hardware scope of D1.

> torch.Tensor.scatter_add_() when called on a CUDA tensor

> torch.index_add() when called on CUDA tensor

> The following normally-nondeterministic operations will throw a RuntimeError when mode=True:

*[D2]* Lists scatter/index_add CUDA ops as normally nondeterministic (the atomics class of D2). The 2.14 page does not mention CUBLAS_WORKSPACE_CONFIG (checked: 0 matches).

### PyTorch notes: CUDA semantics (cuBLAS workspaces)

- Version: PyTorch 2.14 docs
- URL fetched: https://docs.pytorch.org/docs/2.14/notes/cuda.html
- Fetch status (2026-09-25): 200
- Raw text: `training/pytorch_cuda_semantics.txt`

> The workspace size per allocation can be specified via the environment variable CUBLAS_WORKSPACE_CONFIG with the format :[SIZE]:[COUNT].

*[context]* Where CUBLAS_WORKSPACE_CONFIG is documented in PyTorch 2.14; no determinism statement here.

### cuBLAS documentation, 2.1.4 Results Reproducibility

- Version: cuBLAS 13.4 documentation
- URL fetched: https://docs.nvidia.com/cuda/cublas/index.html
- Fetch status (2026-09-25): 200
- Raw text: `training/cublas_13.4.txt`

> By design, all cuBLAS API routines from a given toolkit version, generate the same bit-wise results at every run when executed on GPUs with the same architecture and the same number of SMs.

> However, bit-wise reproducibility is not guaranteed across toolkit versions because the implementation might differ due to some implementation changes.

*[D1]* States D1's hardware/software scope (same architecture, same SM count, same toolkit).

> This guarantee no longer holds when multiple CUDA streams are active or fixed-point emulation is used.

> In that case, the results are not guaranteed to be bit-wise reproducible because atomics are used for the computation.

> set a debug environment variable CUBLAS_WORKSPACE_CONFIG to :16:8 (may limit overall performance) or :4096:8 (will increase library footprint in GPU memory by approximately 24MiB).

*[D2]* States atomics as a source (D2) and names multi-stream workspace selection as a further source not listed in D2.

### cuDNN Backend developer guide: Reproducibility (Determinism)

- Version: cuDNN v9.26.0 docs
- URL fetched: https://docs.nvidia.com/deeplearning/cudnn/backend/latest/developer/misc.html
- Fetch status (2026-09-25): 200
- Raw text: `training/cudnn_misc.txt`

> By design, most of cuDNN’s routines from a given version generate the same bit-wise results across runs when executed on GPUs with the same architecture.

> Across different architectures, no cuDNN routines guarantee bitwise reproducibility.

*[D1]* States D1's 'changing GPU type breaks it' for cuDNN.

> because they use atomic operations in a way that introduces truly random floating point rounding errors

*[D2]* States atomics as a D2 source.

### Megatron Core user guide: Deterministic Training

- Version: Megatron Core docs 'latest' (version_match 0.19.0)
- URL fetched: https://docs.nvidia.com/megatron-core/developer-guide/latest/user-guide/deterministic-training.html
- Fetch status (2026-09-25): 200
- Raw text: `training/megatron_core_deterministic_training.txt`

> Deterministic training guarantees that two runs with identical inputs produce identical outputs at every step.

> asserts that two runs of the same configuration produce bit-identical outputs and gradients

*[D1]* Bears on D1: guarantee is stated for the same configuration; nothing on changing GPU count or type.

> Conservative default — Ring’s reduction order is fixed by topology, so it is bit-exact across runs on every supported NCCL version

> Tree is intentionally excluded: its intra-node chain reduction order is not user-controllable, and the inter-node tree topology can vary across runs without a pinned topology file, so it cannot be vouched for as bit-exact across stacks.

> Must be off — asserted (fused CE is non-deterministic); drop the flag yourself

*[D2]* States NCCL reduction order as a D2 source; 'fixed by topology' also bears on D1 (order tied to the layout).

### Megatron Core user guide: Deterministic Training (nightly)

- Version: Megatron Core docs 'nightly' (fetched 2026-09-25)
- URL fetched: https://docs.nvidia.com/megatron-core/developer-guide/nightly/user-guide/deterministic-training.html
- Fetch status (2026-09-25): 200
- Raw text: `training/megatron_core_deterministic_training_nightly.txt`

> Determinism costs an independent output buffer: a reduction that would otherwise accumulate into shared memory with unordered atomics writes into its own buffer instead, fixing the summation order run to run.

> Triton picks a kernel config by timing its candidates, so the winner depends on the machine at that instant and ranks can disagree.

*[D2]* States atomics (D2) and autotuned kernel selection (analogue of D2's cuDNN algorithm selection).

> Clearing it is worth roughly 15% TFLOP/s on large configs, and more the more torch.empty calls a step makes.

*[context]* Cost of one determinism knob (uninitialized-memory fill); bears on the cost side of D1.

### Megatron-LM/Megatron-Core README, section Reproducibility (PyPI long description)

- Version: megatron-core 0.12.1 (uploaded 2025-05-23); section absent from 0.19.2 PyPI description
- URL fetched: https://pypi.org/pypi/megatron-core/0.12.1/json
- Fetch status (2026-09-25): 200 (PyPI JSON API; the GitHub README itself not fetched: github.com is refused by the proxy)
- Raw text: `training/megatron_core_0.12.1_pypi_readme.txt`

> Megatron training can be bitwise reproducible; to enable this mode use

> This means that the same training config run twice in the same HW and SW environment should produce identical model checkpoints, losses and accuracy metric values (iteration time metrics may vary).

> In addition, determinisim has only been verified in NGC PyTorch containers up to and newer than 23.12.

*[D1]* States D1: bitwise reproducibility with a deterministic mode, scoped to the same HW and SW environment.

> The specific NCCL algorithm that is used during an all-reduce (as specified by the environment variable

> Flash attention is non-deterministic; do not use

*[D2]* States NCCL algorithm choice as a reproducibility factor (D2).

### Megatron Core API: core.tensor_parallel.random (CudaRNGStatesTracker)

- Version: Megatron Core docs 0.19.0
- URL fetched: https://docs.nvidia.com/megatron-core/developer-guide/latest/apidocs/core/core.tensor_parallel.random.html
- Fetch status (2026-09-25): 200 (a first guessed URL, .../api-guide/tensor_parallel.html, returned 404)
- Raw text: `training/megatron_core_tp_random.txt`

> Using the add method, a cuda rng state is initialized based on the input seed and is assigned to name.

> tensor-model-parallel state: This state is different among a set of model parallel GPUs, but the same across data parallel groups.

*[context]* State inventory: RNG streams are per parallel group, so they are tied to the parallel layout (bears on D1).

### Megatron Core API guide: dist_checkpointing

- Version: Megatron Core docs 0.19.0
- URL fetched: https://docs.nvidia.com/megatron-core/developer-guide/latest/api-guide/core/dist_checkpointing.html
- Fetch status (2026-09-25): 200
- Raw text: `training/megatron_core_dist_checkpointing.txt`

> A key property of distributed checkpoints is that a checkpoint saved under one parallel configuration (tensor, pipeline, or data parallelism) can be loaded under a different parallel configuration.

> Not reshardable — not possible to change model parallelism when using this format.

*[context]* Checkpoint state can be moved across layouts (resharding); says nothing about bitwise identity after resharding.

### NCCL User Guide: Environment Variables (NCCL_ALGO)

- Version: NCCL 2.32.3 documentation
- URL fetched: https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html
- Fetch status (2026-09-25): 200
- Raw text: `training/nccl_env.txt`

> The default is unset, which causes NCCL to automatically choose the available algorithms based on the node topology and architecture.

*[D2]* Bears on D2: algorithm (hence reduction order) chosen from topology/architecture. No explicit determinism or reproducibility statement found in the 2.32.3 env, collectives or troubleshooting pages.

### torch.distributed.checkpoint (DCP)

- Version: PyTorch 2.14 docs (page 'Last Updated On: Jul 08, 2026')
- URL fetched: https://docs.pytorch.org/docs/2.14/distributed.checkpoint.html
- Fetch status (2026-09-25): 200 (stable redirects to 2.14)
- Raw text: `training/pytorch_dcp.txt`

> It handles load-time resharding which enables saving in one cluster topology and loading into another.

> returning a model and optimizer state_dict that can be resharded with a different number of trainers and/or different parallelisms.

*[context]* State portability across topologies; no bitwise claim.

> Asynchronous version of save. This code first de-stages the state_dict on to the staging storage (defaults to CPU memory), and then calls the save in a separate thread.

*[D8]* Describes the asynchronous, CPU-staged save of D8.

### PyTorch recipe: Asynchronous Saving with Distributed Checkpoint (DCP)

- Version: Last Updated: Feb 03, 2026
- URL fetched: https://docs.pytorch.org/tutorials/recipes/distributed_async_checkpoint_recipe.html
- Fetch status (2026-09-25): 200
- Raw text: `training/pytorch_dcp_async_recipe.txt`

> Checkpointing is often a bottleneck in the critical path for distributed training workloads, incurring larger and larger costs as both model and world sizes grow.

> this optimization attacks the main overhead of asynchronous checkpointing, which is the in-memory copying to checkpointing buffers.

*[D8]* States D8 (checkpoint cost; asynchronous saving as the remedy).

### PyTorch recipe: Getting Started with Distributed Checkpoint (DCP)

- Version: Last Updated: Jul 10, 2025
- URL fetched: https://docs.pytorch.org/tutorials/recipes/distributed_checkpoint_recipe.html
- Fetch status (2026-09-25): 200
- Raw text: `training/pytorch_dcp_recipe.txt`

> You can load in the same world size or different world size.

*[context]* State portability across world size.

### Zhuang, Zhang, Song, Hooker: Randomness in Neural Network Training: Characterizing the Impact of Tooling

- Version: arXiv 2106.11872v1 (22 Jun 2021)
- URL fetched: https://arxiv.org/abs/2106.11872
- Fetch status (2026-09-25): 200 (PDF)
- Raw text: `training/zhuang2021_randomness.txt`

> with overhead up to 746%, 241%, and 196% on a spectrum of widely used GPU accelerator architectures, relative to non-deterministic training.

> GPUs with older Pascal architecture (P100) evidence higher overhead than GPUs with later Volta (V100) and Turing (T4) architecture.

*[context]* Measured cost of deterministic GPU training; bears on D1 (deterministic algorithms are the price).

> Some convolution algorithm implementation in cuDNN are designed to trade determinism for execution speed.

> This is because the difference in input data order will result in different ﬂoat-point accumulation order in gradients accumulation stage thus introducing latent implementation noise.

*[D2]* Bears on D2: cuDNN algorithms and accumulation order as sources.

### Donaghy et al. (Gensyn): OPEN-1B: A Fully Auditable Training Run

- Version: arXiv 2609.17380v1 (15 Sep 2026)
- URL fetched: https://arxiv.org/abs/2609.17380
- Fetch status (2026-09-25): 200 (PDF)
- Raw text: `training/open1b_2026.txt`

> Determinism means a computation returns the same result every time it runs on the same machine with the same environment.

> Determinism does not imply reproducibility. A training run can be perfectly repeatable on its own GPU while disagreeing with an identical run on a processor or a different GPU model. A framework’s deterministic mode addresses only the first case.

> Changing the number of data parallel workers results in different batch orderings.

*[D1]* States D1 for standard deterministic modes (same machine; different GPU model or worker count breaks it).

> this makes the entire training run bit-exact under replay, independent of device count and topology, enabling third-party audit of any training segment.

> In the case of a hardware failure or resource re-allocation, the run can be re-sharded onto a different number of devices without perturbing the training data sequence.

> We trade off compute performance for reproducibility.

*[D1]* States the opposite of D1's 'changing GPU count or type breaks it' for a run built on custom reproducible kernels (RepOps), a topology-invariant data stream and a deterministic all-reduce, at a stated performance cost (MFU about 5%, same section). It qualifies D1 rather than contradicting it for standard stacks.

> By imposing a definite order on the sources of training nondeterminism, GPU kernel reductions, data batch ordering across a data-parallel cluster, and inter/intra-node collective communication

*[D2]* Names kernel reductions and collective communication as sources (D2); adds data batch ordering.

### Arun et al.: Verde: Verification via Refereed Delegation for Machine Learning Programs (RepOps)

- Version: arXiv 2502.19405v1 (26 Feb 2025)
- URL fetched: https://arxiv.org/abs/2502.19405
- Fetch status (2026-09-25): 200 (PDF)
- Raw text: `training/verde_repops.txt`

> Given the same parallelized program, owing to differences in architecture, distinct hardware implementations may (and often do) execute a + b + c in different orders, ending up with different results.

> RepOps currently ensures reproducibility between setups when programs are run on a single GPU in each setup.

> incur around 60% overhead RepOps on an A100 GPU

*[D1]* States the hardware-type half of D1 for ordinary kernels; cross-hardware BR achieved with custom kernels on a single GPU, at a cost.

### Lian et al.: Universal Checkpointing (DeepSpeed UCP)

- Version: arXiv 2406.18820v3 (4 Jul 2025)
- URL fetched: https://arxiv.org/abs/2406.18820
- Fetch status (2026-09-25): 200 (PDF)
- Raw text: `training/ucp_deepspeed.txt`

> distributed checkpoints are tightly coupled to specific model parallelism and hardware configurations

> the training can be seamlessly resumed using different Target parallelism strategies, while achieving consistent convergence if the training were to continue with the Source strategy.

> Most importantly, the resumed training curves match the curves from the Source at iterations 101–200.

*[D1]* Bears on D1: resuming under changed parallelism is evaluated by matching loss curves, not by bitwise identity; no bitwise claim made.

### Wan et al.: ByteCheckpoint: A Unified Checkpointing System for Large Foundation Model Development

- Version: arXiv 2407.20143v4 (2 Apr 2025); NSDI'25
- URL fetched: https://arxiv.org/abs/2407.20143
- Fetch status (2026-09-25): 200 (PDF)
- Raw text: `training/bytecheckpoint.txt`

> CPU states include dataloader module, Random Number Generator (RNG) state, global training step number, and learning-rate scheduler, all stored in CPU memory.

> the token buffers should be copied to the destination workers for bitwise-correct resuming.

*[context]* State inventory for a lossless resume (GPU params/optimizer + CPU dataloader/RNG/step/LR schedule).

> ByteCheckpoint significantly reduces runtime checkpoint stalls, achieving an average reduction of 54.20×.

> This improvement reduces the average checkpoint stall time from minutes or seconds to sub-second durations, outperforming both DCP and MCP.

*[D8]* States D8 (stall measured; reduced by the system's asynchronous pipeline).

### Jiang et al.: MegaScale: Scaling Large Language Model Training to More Than 10,000 GPUs

- Version: arXiv 2402.15627v1 (23 Feb 2024)
- URL fetched: https://arxiv.org/abs/2402.15627
- Fetch status (2026-09-25): 200 (PDF)
- Raw text: `training/megascale.txt`

> In the first stage, each GPU worker writes its on-chip states to the host memory, and then continues the training process.

> this process can be reduced to several seconds thanks to the high PCIe bandwidth, thereby minimally interrupting the ongoing training process.

> the system can catch up to the training progress prior to the crash within 15 minutes from the latest checkpoints, maintaining over 90% effective training time rate

*[D8]* States D8 (two-stage host-memory then asynchronous persist).

### Llama Team, AI @ Meta: The Llama 3 Herd of Models, §3.3.4

- Version: arXiv 2407.21783v3 (23 Nov 2024)
- URL fetched: https://arxiv.org/abs/2407.21783
- Fetch status (2026-09-25): 200 (PDF)
- Raw text: `training/llama3.txt`

> We aim to minimize GPU pause time during checkpointing and increase checkpoint frequency to reduce the amount of lost work after a recovery.

> To increase the effective training time, we reduced job startup and checkpointing time

*[D8]* Bears on D8 (checkpoint pause is a cost being minimised); no number for the overhead itself.

> the synchronous nature of training makes it less fault-tolerant—a single GPU failure may require a restart of the entire job.

> During a 54-day snapshot period of pre-training, we experienced a total of 466 job interruptions.

> Checkpointing saves each GPU’s model state, ranging from 1 MB to 4 GB per GPU, for recovery and debugging.

*[context]* Frequency of stop/resume events in frontier training.

> tens of thousands of GPUs may increase or decrease power consumption at the same time, for example, due to all GPUs waiting for checkpointing or collective communications to finish

*[D7]* Bears on D7: waiting GPUs draw measurably less than working ones at data-centre scale; gives no fraction.

### Kokolis, Kuchnik et al.: Revisiting Reliability in Large-Scale Machine Learning Research Clusters

- Version: arXiv 2410.21680v2 (6 Feb 2025); HPCA 2025
- URL fetched: https://arxiv.org/abs/2410.21680
- Fetch status (2026-09-25): 200 (PDF)
- Raw text: `training/kokolis2025.txt`

> 3) Checkpoint overhead: The time checkpointing adds to job runtime.

> checkpoint write overhead needs to be under a minute O(10s), achievable with asynchronous checkpoint writing strategies

> To reach ETTR of 0.9 for the largest feasible training runs on RSC-1 (∼12,000 GPUs, taking two thirds of RSC-1), checkpoint write time overhead needs to be on the order of ∼10 seconds or failure rate needs to dramatically improve from 6.50 to ∼1.

*[D8]* States D8 (modelled, not measured per job: 'we currently lack a reliable way for tracking either at scale').

### Mohan, Phanishayee, Chidambaram: CheckFreq: Frequent, Fine-Grained DNN Checkpointing

- Version: FAST 2021 proceedings PDF
- URL fetched: https://www.usenix.org/system/files/fast21-mohan.pdf
- Fetch status (2026-09-25): 200 (PDF)
- Raw text: `training/checkfreq_fast21.txt`

> CheckFreq can reduce the recovery time from hours to seconds while bounding the runtime overhead within 3.5%.

> checkpointing requires the training to brieﬂy pause to capture the model weights accurately.

*[D8]* States D8 (checkpoint stall; pipelined snapshot/persist reduces it).

> When the job is interrupted, these iterators can either miss out, or repeat data items in an epoch, resulting in loss in model accuracy when resuming at iteration granularity.

> resulting in upto the 13% drop in accuracy for popular models ResNet18 (Fig 6).

*[context]* State inventory: data-iterator state must be saved for a faithful resume.

### Wang et al.: Gemini: Fast Failure Recovery in Distributed Training with In-Memory Checkpoints

- Version: SOSP 2023 (author copy; ACM DL PDF returned 403)
- URL fetched: https://www.cs.rice.edu/~eugeneng/papers/SOSP23.pdf
- Fetch status (2026-09-25): 200 (author PDF at cs.rice.edu); ACM DL PDF https://dl.acm.org/doi/pdf/10.1145/3600006.3613145 returned 403
- Raw text: `training/gemini_sosp23.txt`

> Existing solutions have significant failure recovery costs due to the severe restriction imposed by the bandwidth of remote storage in which they store checkpoints.

> Moreover, it achieves optimal checkpoint frequency, i.e., every iteration, and incurs no overhead on training throughput for large model training.

*[D8]* States D8 (in-memory checkpoints remove throughput overhead).

### Maurya, Rafique, Cappello, Nicolae: DataStates-LLM: Scalable Checkpointing for Transformer Models Using Composable State Providers

- Version: arXiv 2601.16956v1 (23 Jan 2026)
- URL fetched: https://arxiv.org/abs/2601.16956
- Fetch status (2026-09-25): 200 (PDF; pypdf warned of one invalid hex string, text extracted)
- Raw text: `training/datastates_llm_2026.txt`

> This results in significant runtime overheads due to blocking device-to-host transfers, data-oblivious serialization, and storage I/O contention.

> higher checkpointing throughput and reduces end-to-end training time by up to 2.2×compared to state-of-the-art solutions

*[D8]* States D8.

### Xie, Chen, Zheng, Yang, Zhang: PHOENIX: Resilient LLM Training with Hot-Swapping via Zero-Overhead Checkpoint

- Version: arXiv 2607.01646v2 (6 Jul 2026)
- URL fetched: https://arxiv.org/abs/2607.01646
- Fetch status (2026-09-25): 200 (PDF)
- Raw text: `training/phoenix_2026.txt`

> Existing fault-tolerance mechanisms either impose non-trivial overhead during failure-free execution or suffer from prolonged recovery latency

> PHOENIX efficiently overlaps the in-memory checkpointing with computation, thus introducing zero overhead during error-free execution.

*[D8]* States D8.

### Han et al.: TierCheck: Tiered Checkpointing for Fault Tolerance in Large Language Model Training

- Version: arXiv 2605.17821v1 (18 May 2026)
- URL fetched: https://arxiv.org/abs/2605.17821
- Fetch status (2026-09-25): 200 (PDF)
- Raw text: `training/tiercheck_2026.txt`

> Existing checkpointing systems rely on monolithic, single-tier storage backend, forcing a trade-off between state-saving overhead and recovery speed.

> reduces end-to-end checkpointing time to under 10 s

*[D8]* States D8.

### Athlur et al.: Varuna: Scalable, Low-cost Training of Massive Deep Learning Models

- Version: arXiv 2111.04007v2 (15 Nov 2021); EuroSys 2022
- URL fetched: https://arxiv.org/abs/2111.04007
- Fetch status (2026-09-25): 200 (PDF)
- Raw text: `training/varuna.txt`

> employing dynamic, semantics-preserving reconfiguration of the training job.

> require users to provide different sets of hyper-parameters and mini-batch sizes for a varying number of resources.

*[context]* Preemption handling preserves sync-SGD semantics and batch size; no claim that resumed training is bitwise identical (bears on D1).

### Thorpe et al.: Bamboo: Making Preemptible Instances Resilient for Affordable Training of Large DNNs

- Version: arXiv 2204.12013v1 (26 Apr 2022); NSDI 2023
- URL fetched: https://arxiv.org/abs/2204.12013
- Fetch status (2026-09-25): 200 (PDF)
- Raw text: `training/bamboo.txt`

> we built Bamboo atop synchronous microbatching where model state is always consistent.

> elastic batching because dropping samples is equivalent to changing the effective batch size at a training iteration

*[context]* Preserves consistent model state via redundant computation; alternatives (sample dropping) change the trajectory. No bitwise claim.

### Jang et al.: Oobleck: Resilient Distributed Training of Large Models Using Pipeline Templates

- Version: arXiv 2309.08125v2 (7 Nov 2023); SOSP 2023
- URL fetched: https://arxiv.org/abs/2309.08125
- Fetch status (2026-09-25): 200 (PDF)
- Raw text: `training/oobleck.txt`

> Each pipeline may have more batches to compute, but the global batch size remains constant.

> Oobleck does not change the global batch size arbitrarily in such cases.

*[context]* Preserves global batch size across reconfiguration; no bitwise claim.

### Groeneveld et al.: OLMo: Accelerating the Science of Language Models

- Version: arXiv 2402.00838v4 (7 Jun 2024)
- URL fetched: https://arxiv.org/abs/2402.00838
- Fetch status (2026-09-25): 200 (PDF)
- Raw text: `training/olmo1.txt`

> The training instances are shuffled in the exact same way for each training run. The data order and exact composition of each training batch can be reconstructed from the artifacts we release.

*[context]* Data-order state is reproducible; no bitwise claim about weights across restarts.

### OLMo Team: 2 OLMo 2 Furious

- Version: arXiv 2501.00656v3 (8 Oct 2025)
- URL fetched: https://arxiv.org/abs/2501.00656
- Fetch status (2026-09-25): 200 (PDF)
- Raw text: `training/olmo2.txt`

> Containers further capture software dependencies and the runtime details of workloads. This helps run repeatable experiments, and makes it possible to replay old results even months after they happened.

> an improper ordering of the compute nodes in the NCCL library

*[context]* Environment pinning for repeatability; no bitwise claim across restarts or GPU counts.

## Claims by prediction

### D1 (10 claim objects, 25 quotes)

- PyTorch notes: Reproducibility (PyTorch 2.14 docs (page 'Last Updated On: May 14, 2026')): States the platform/release dependence in D1; does not mention GPU count.
- torch.use_deterministic_algorithms (PyTorch 2.14 docs): States the same-software-and-hardware scope of D1.
- cuBLAS documentation, 2.1.4 Results Reproducibility (cuBLAS 13.4 documentation): States D1's hardware/software scope (same architecture, same SM count, same toolkit).
- cuDNN Backend developer guide: Reproducibility (Determinism) (cuDNN v9.26.0 docs): States D1's 'changing GPU type breaks it' for cuDNN.
- Megatron Core user guide: Deterministic Training (Megatron Core docs 'latest' (version_match 0.19.0)): Bears on D1: guarantee is stated for the same configuration; nothing on changing GPU count or type.
- Megatron-LM/Megatron-Core README, section Reproducibility (PyPI long description) (megatron-core 0.12.1 (uploaded 2025-05-23); section absent from 0.19.2 PyPI description): States D1: bitwise reproducibility with a deterministic mode, scoped to the same HW and SW environment.
- Donaghy et al. (Gensyn): OPEN-1B: A Fully Auditable Training Run (arXiv 2609.17380v1 (15 Sep 2026)): States D1 for standard deterministic modes (same machine; different GPU model or worker count breaks it).
- OPEN-1B (arXiv 2609.17380v1): States the opposite of D1's 'changing GPU count or type breaks it' for a run built on custom reproducible kernels (RepOps), a topology-invariant data stream and a deterministic all-reduce, at a stated performance cost (MFU about 5%, same section). It qualifies D1 rather than contradicting it for standard stacks.
- Arun et al.: Verde: Verification via Refereed Delegation for Machine Learning Programs (RepOps) (arXiv 2502.19405v1 (26 Feb 2025)): States the hardware-type half of D1 for ordinary kernels; cross-hardware BR achieved with custom kernels on a single GPU, at a cost.
- Lian et al.: Universal Checkpointing (DeepSpeed UCP) (arXiv 2406.18820v3 (4 Jul 2025)): Bears on D1: resuming under changed parallelism is evaluated by matching loss curves, not by bitwise identity; no bitwise claim made.

### D2 (10 claim objects, 20 quotes)

- PyTorch notes: Reproducibility (PyTorch 2.14 docs): States two D2 sources: cuDNN algorithm selection (benchmark) and atomics (Flash SDPA backward).
- torch.use_deterministic_algorithms (PyTorch 2.14 docs): Lists scatter/index_add CUDA ops as normally nondeterministic (the atomics class of D2). The 2.14 page does not mention CUBLAS_WORKSPACE_CONFIG (checked: 0 matches).
- cuBLAS documentation, 2.1.4 Results Reproducibility (cuBLAS 13.4 documentation): States atomics as a source (D2) and names multi-stream workspace selection as a further source not listed in D2.
- cuDNN Backend developer guide: Reproducibility (Determinism) (cuDNN v9.26.0 docs): States atomics as a D2 source.
- Megatron Core user guide: Deterministic Training (Megatron Core docs 'latest' (version_match 0.19.0)): States NCCL reduction order as a D2 source; 'fixed by topology' also bears on D1 (order tied to the layout).
- Megatron Core user guide: Deterministic Training (nightly) (Megatron Core docs 'nightly' (fetched 2026-09-25)): States atomics (D2) and autotuned kernel selection (analogue of D2's cuDNN algorithm selection).
- Megatron-LM/Megatron-Core README, section Reproducibility (PyPI long description) (megatron-core 0.12.1): States NCCL algorithm choice as a reproducibility factor (D2).
- NCCL User Guide: Environment Variables (NCCL_ALGO) (NCCL 2.32.3 documentation): Bears on D2: algorithm (hence reduction order) chosen from topology/architecture. No explicit determinism or reproducibility statement found in the 2.32.3 env, collectives or troubleshooting pages.
- Zhuang et al. 2021 (arXiv 2106.11872v1): Bears on D2: cuDNN algorithms and accumulation order as sources.
- OPEN-1B (arXiv 2609.17380v1): Names kernel reductions and collective communication as sources (D2); adds data batch ordering.

### D8 (11 claim objects, 23 quotes)

- torch.distributed.checkpoint (DCP) (PyTorch 2.14 docs): Describes the asynchronous, CPU-staged save of D8.
- PyTorch recipe: Asynchronous Saving with Distributed Checkpoint (DCP) (Last Updated: Feb 03, 2026): States D8 (checkpoint cost; asynchronous saving as the remedy).
- ByteCheckpoint (arXiv 2407.20143v4): States D8 (stall measured; reduced by the system's asynchronous pipeline).
- Jiang et al.: MegaScale: Scaling Large Language Model Training to More Than 10,000 GPUs (arXiv 2402.15627v1 (23 Feb 2024)): States D8 (two-stage host-memory then asynchronous persist).
- Llama Team, AI @ Meta: The Llama 3 Herd of Models, §3.3.4 (arXiv 2407.21783v3 (23 Nov 2024)): Bears on D8 (checkpoint pause is a cost being minimised); no number for the overhead itself.
- Kokolis, Kuchnik et al.: Revisiting Reliability in Large-Scale Machine Learning Research Clusters (arXiv 2410.21680v2 (6 Feb 2025); HPCA 2025): States D8 (modelled, not measured per job: 'we currently lack a reliable way for tracking either at scale').
- Mohan, Phanishayee, Chidambaram: CheckFreq: Frequent, Fine-Grained DNN Checkpointing (FAST 2021 proceedings PDF): States D8 (checkpoint stall; pipelined snapshot/persist reduces it).
- Wang et al.: Gemini: Fast Failure Recovery in Distributed Training with In-Memory Checkpoints (SOSP 2023 (author copy; ACM DL PDF returned 403)): States D8 (in-memory checkpoints remove throughput overhead).
- Maurya, Rafique, Cappello, Nicolae: DataStates-LLM: Scalable Checkpointing for Transformer Models Using Composable State Providers (arXiv 2601.16956v1 (23 Jan 2026)): States D8.
- Xie, Chen, Zheng, Yang, Zhang: PHOENIX: Resilient LLM Training with Hot-Swapping via Zero-Overhead Checkpoint (arXiv 2607.01646v2 (6 Jul 2026)): States D8.
- Han et al.: TierCheck: Tiered Checkpointing for Fault Tolerance in Large Language Model Training (arXiv 2605.17821v1 (18 May 2026)): States D8.

### D7 (1 claim objects, 1 quotes)

- Llama 3, §3.3.4 (arXiv 2407.21783v3): Bears on D7: waiting GPUs draw measurably less than working ones at data-centre scale; gives no fraction.

### context (16 claim objects, 28 quotes)

- PyTorch notes: Reproducibility (PyTorch 2.14 docs): Cost of determinism, qualitative; bears on D1's 'needs deterministic algorithms'.
- PyTorch notes: CUDA semantics (cuBLAS workspaces) (PyTorch 2.14 docs): Where CUBLAS_WORKSPACE_CONFIG is documented in PyTorch 2.14; no determinism statement here.
- Megatron Core user guide: Deterministic Training (nightly) (Megatron Core docs 'nightly'): Cost of one determinism knob (uninitialized-memory fill); bears on the cost side of D1.
- Megatron Core API: core.tensor_parallel.random (CudaRNGStatesTracker) (Megatron Core docs 0.19.0): State inventory: RNG streams are per parallel group, so they are tied to the parallel layout (bears on D1).
- Megatron Core API guide: dist_checkpointing (Megatron Core docs 0.19.0): Checkpoint state can be moved across layouts (resharding); says nothing about bitwise identity after resharding.
- torch.distributed.checkpoint (DCP) (PyTorch 2.14 docs (page 'Last Updated On: Jul 08, 2026')): State portability across topologies; no bitwise claim.
- PyTorch recipe: Getting Started with Distributed Checkpoint (DCP) (Last Updated: Jul 10, 2025): State portability across world size.
- Zhuang, Zhang, Song, Hooker: Randomness in Neural Network Training: Characterizing the Impact of Tooling (arXiv 2106.11872v1 (22 Jun 2021)): Measured cost of deterministic GPU training; bears on D1 (deterministic algorithms are the price).
- Wan et al.: ByteCheckpoint: A Unified Checkpointing System for Large Foundation Model Development (arXiv 2407.20143v4 (2 Apr 2025); NSDI'25): State inventory for a lossless resume (GPU params/optimizer + CPU dataloader/RNG/step/LR schedule).
- Llama 3, §3.3.4 (arXiv 2407.21783v3): Frequency of stop/resume events in frontier training.
- CheckFreq (FAST 2021): State inventory: data-iterator state must be saved for a faithful resume.
- Athlur et al.: Varuna: Scalable, Low-cost Training of Massive Deep Learning Models (arXiv 2111.04007v2 (15 Nov 2021); EuroSys 2022): Preemption handling preserves sync-SGD semantics and batch size; no claim that resumed training is bitwise identical (bears on D1).
- Thorpe et al.: Bamboo: Making Preemptible Instances Resilient for Affordable Training of Large DNNs (arXiv 2204.12013v1 (26 Apr 2022); NSDI 2023): Preserves consistent model state via redundant computation; alternatives (sample dropping) change the trajectory. No bitwise claim.
- Jang et al.: Oobleck: Resilient Distributed Training of Large Models Using Pipeline Templates (arXiv 2309.08125v2 (7 Nov 2023); SOSP 2023): Preserves global batch size across reconfiguration; no bitwise claim.
- Groeneveld et al.: OLMo: Accelerating the Science of Language Models (arXiv 2402.00838v4 (7 Jun 2024)): Data-order state is reproducible; no bitwise claim about weights across restarts.
- OLMo Team: 2 OLMo 2 Furious (arXiv 2501.00656v3 (8 Oct 2025)): Environment pinning for repeatability; no bitwise claim across restarts or GPU counts.

## Quote check

`training_check.py` over `training_claims.json`: found 97/97 quotes (48 claim objects); none dropped.

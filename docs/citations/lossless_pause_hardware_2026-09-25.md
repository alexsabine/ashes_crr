# Lossless pause: hardware family (GPU preemption, checkpoint/restore, idle power, state at a token boundary)

Fetched on 2026-09-25 by a literature agent following the `pause_lit/BRIEF.md` brief. This is a note, not evidence (R8). Every quote is a verbatim substring of the raw text saved in the session scratchpad at `pause_lit/hardware/<slug>.txt`. The check applies html-unescape, removes U+FFFE and U+00AD, joins "-\n" and collapses whitespace. PDF text was extracted with pypdf, so hyphenated line breaks appear joined and some words run together (e.g. "stateexecution-idle") exactly as extracted. Machine-readable claims are in `pause_lit/hardware_claims.json`. The quote check found 72/72 quotes.

github.com returns HTTP 403 through the proxy ("GitHub access to this repository is not enabled for this session"), so the NVIDIA/cuda-checkpoint and checkpoint-restore/criu repositories were not fetched. The NVIDIA documentation site, the NVIDIA blog and the papers were used instead. Other failures on the day: the LBNL 2024 US Data Center Energy Usage Report (HTTP 403 via curl, and empty via WebFetch); the old CUDA driver-API checkpoint URL (HTTP 404, current URL used).

## H1. NVIDIA, "NVIDIA Tesla P100" (Pascal GP100 architecture whitepaper)

- Version: WP-08019-001_v01.1
- URL: https://images.nvidia.com/content/pdf/tesla/whitepaper/pascal-architecture-whitepaper.pdf
- Fetch: curl, HTTP 200 (PDF, 45 pages). Document number printed in the footer.
- Raw text: `pause_lit/hardware/pascal_whitepaper.txt`

> Compute Preemption is another important new hardware and software feature added to GP100 that allows compute tasks to be preempted at instruction-level granularity, rather than thread block granularity as in prior Maxwell and Kepler GPU architectures.

> The new Pascal GP100 Compute Preemption feature allows compute tasks running on the GPU to be interrupted at instruction-level granularity, and their context swapped to GPU DRAM. This permits other applications to be swapped in and run, followed by the original task’s context being swapped back in to continue execution where it left off.

Tag: D5. States the prediction (instruction-level preemption from Pascal GP100; context swapped to DRAM and back). Vendor whitepaper; no overhead figure given.

## H2. NVIDIA, CUDA C++ Programming Guide (archived)

- Version: 12.4.0, last updated Mar 07, 2024
- URL: https://docs.nvidia.com/cuda/archive/12.4.0/cuda-c-programming-guide/index.html
- Fetch: curl, HTTP 200 (archived HTML). Quoted because the current guide no longer carries the Compute Preemption paragraph (see note).
- Raw text: `pause_lit/hardware/cuda_c_programming_guide_12.4.0.txt`

> for devices featuring the Pascal architecture onwards (compute capability with major revision number 6 and higher), there exists support for Compute Preemption. This allows compute tasks to be preempted at instruction-level granularity, rather than thread block granularity as in prior Maxwell and Kepler GPU architecture

> However, there will be context switch overheads associated with Compute Preemption, which is automatically enabled on those devices for which support exists.

> Users wishing to avoid context switch overheads associated with different processes can ensure that only one process is active on the GPU by selecting exclusive-process mode.

Tag: D5. States the prediction (Pascal onward, automatic) and adds that it carries context-switch overheads (no number). This paragraph is from the archived 12.4.0 guide; the current 13.4.2 guide text contains no "Compute Preemption" / cudaDevAttrComputePreemptionSupported match (searched).

## H3. NVIDIA, CUDA Programming Guide (current, PDF)

- Version: Release 13.4.2
- URL: https://docs.nvidia.com/cuda/cuda-programming-guide/pdf/cuda-programming-guide.pdf
- Fetch: curl, HTTP 200 (PDF, 734 pages; docs.nvidia.com/cuda/cuda-c-programming-guide/ now redirects to cuda-programming-guide/). A case-insensitive search for "preempt" finds only stream-priority and cluster-launch-control text; "ComputePreemption" and "exclusive-process" have 0 matches.
- Raw text: `pause_lit/hardware/cuda_programming_guide_13.4.2.txt`

> Stream priorities will not preempt already executing work, or guarantee any specific execution order.

> Higher-priority tasks do not preempt already running lower-priority tasks. The GPU does not reassess work queues during task execution, and increasing a stream’s priority will not interrupt ongoing work.

Tag: D5. Only bears on it: within one context, stream priority does not preempt running work (a user-level scheduling statement, not the hardware context-switch mechanism). Current guide 13.4.2.

> MPS primarily targets different processes (e.g., MPI programs), allowing them to run on the GPU at the same time without time-slicing.

Tag: context. Context: MPS avoids time-slicing between processes.

> CUDA Checkpoint does not guarantee that localized green contexts retain their localization properties when restored on a different device. The application may exhibit reduced performance after a restore.

Tag: D6. Bears on it: restore on a different device is possible but some properties are not guaranteed (performance, not correctness, is named).

## H4. Han, Zhang, Chen, Chen, "Microsecond-scale Preemption for Concurrent GPU-accelerated DNN Inferences" (REEF), OSDI 2022

- Version: OSDI 2022 proceedings PDF
- URL: https://www.usenix.org/system/files/osdi22-han.pdf
- Fetch: curl, HTTP 200 (USENIX open-access PDF, 21 pages). PDF ligatures (e.g. "ﬁ") are kept verbatim in quotes.
- Raw text: `pause_lit/hardware/reef_osdi22.txt`

> Although NVIDIA claims that their GPUs have been equipped with preemption support since Pascal architecture [51], there is no public available information or a software controllable interface [12, 39, 77].

> it is difﬁcult to implement preemptive scheduling on the GPU due to the large context (e.g., a large amount of registers) [56, 70]. Meanwhile, commodity GPUs also lack hardware support for the preemption mechanism.

> This implies that the running best-effort kernels can be proactively killed and restored without saving contexts.

Tag: D5. Bears on it, partly against the "transparent/usable" reading: the hardware claim is acknowledged but REEF says there is no public or software-controllable interface; REEF instead kills and re-runs idempotent kernels (no context save).

> REEF devises a reset-based preemption scheme that launches a real-time kernel on the GPU by proactively killing and restoring best-effort kernels at microsecond-scale.

Tag: context. Context: kill-and-rerun preemption (idempotent kernels) as the alternative to context save.

## H5. Fan et al., "GPreempt: GPU Preemptive Scheduling Made General and Efficient", USENIX ATC 2025

- Version: ATC 2025 proceedings PDF
- URL: https://www.usenix.org/system/files/atc25-fan.pdf
- Fetch: curl, HTTP 200 (USENIX open-access PDF, 11 pages).
- Raw text: `pause_lit/hardware/gpreempt_atc25.txt`

> Unlike CPU-based systems, GPUs lack a user-facing context-switch interface, making resource preemption more complex.

> GPU task contexts are much larger than CPU (44 MB in NVIDIA A100 GPU vs. less than 1 KB in x86 CPU), and the overhead associated with context switching is considerable.

> Through a thorough analysis of NVIDIA open GPU kernel source [24], we discover an undocumented and little-known hardware resource allocation mechanism: timeslice allocation.

> resulting in a per-SM context footprint of 420 KB and an aggregate GPU context of approximately 44.3 MB [1]. With the memory bandwidth of 1.1 TB/s, context-saving is completed within 40 µs. Our empirical evaluation reveals a combined overhead of approximately 100 µs (§5.3) for these operations.

Tag: D5. Bears on it: hardware context switch exists (driven via driver timeslices) with a stated context size (~44 MB on A100) and ~100 µs combined overhead; no user-facing interface.

## H6. Hu et al., "Hummingbird: SLO-Oriented GPU Preemption at Microsecond-scale"

- Version: arXiv 2601.04071v2, 10 Feb 2026
- URL: https://arxiv.org/abs/2601.04071
- Fetch: arXiv PDF, HTTP 200 (20 pages).
- Raw text: `pause_lit/hardware/2601.04071.txt`

> enabling microsecond-scale preemption on closed-source GPUs while effectively harvesting idle GPU time slices.

Tag: D5. Only bears on it: 2026 system-level preemption on closed-source GPUs; not the vendor mechanism.

> Approaches like Gandiva [86] suspend and resume models, moving states between GPU and host memory

Tag: context. Context: suspend/resume by moving state to host memory in cluster schedulers.

## H7. NVIDIA GPU Operator docs, "Time-Slicing GPUs in Kubernetes"

- Version: latest (fetched 2026-09-25; no date on page)
- URL: https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-sharing.html
- Fetch: curl, HTTP 200. No version or date on the page ("latest").
- Raw text: `pause_lit/hardware/gpu_operator_time_slicing.txt`

> Unlike Multi-Instance GPU (MIG), there is no memory or fault-isolation between replicas, but for some workloads this is better than not being able to share at all.

Tag: context. Context: time-slicing multiplexes contexts on one GPU without memory/fault isolation.

## H8. NVIDIA, Multi-Process Service documentation

- Version: latest, last updated Sep 09, 2026
- URL: https://docs.nvidia.com/deploy/mps/latest/index.html
- Fetch: curl, HTTP 200 (redirected to /deploy/mps/latest/index.html).
- Raw text: `pause_lit/hardware/nvidia_mps.txt`

> Enabling MPS provides the benefit of improved GPU utilization and reduced GPU context switching.

Tag: context. Context: MPS reduces GPU context switching.

## H9. S. Gurfinkel, "Checkpointing CUDA Applications with CRIU", NVIDIA Technical Blog

- Version: Jul 02, 2024 (cuda-checkpoint 550.54.09 in text)
- URL: https://developer.nvidia.com/blog/checkpointing-cuda-applications-with-criu/
- Fetch: curl, HTTP 200. The page carries an "AI-Generated Summary" box above the article; quotes are from the article body only. The cuda-checkpoint GitHub repository it links to was not fetched: github.com returns HTTP 403 through the proxy.
- Raw text: `pause_lit/hardware/nvidia_blog_criu.txt`

> This utility can be used to transparently checkpoint and restore CUDA state within a running Linux process.

> Any CUDA driver APIs that launch work, manage resources, or otherwise impact GPU state are locked. Already submitted CUDA work, including stream callbacks, is completed. Device memory is copied to the host, into allocations managed by the CUDA driver. All CUDA GPU resources are released.

> GPUs are re-acquired by the process. Device memory is copied back to the GPU and GPU memory mappings are restored at their original addresses. CUDA objects such as streams and contexts are restored. CUDA driver APIs are unlocked.

> The response is 102, showing that earlier GPU operations were persisted correctly.

Tag: D6. States the prediction: transparent per-process CUDA checkpoint/restore with CRIU; suspend waits for submitted work (a quiescent point, not mid-kernel).

> x64 only. Acts upon a single process, not a process tree. Doesn’t support UVM or IPC memory. Doesn’t support GPU migration. Waits for already-submitted CUDA work to finish before completing a checkpoint.

> Preemption of lower-priority work on a single node by checkpointing the preempted task

Tag: D6. Bears on it: limitations as of driver 550 (2024), incl. no GPU migration; preemption named as a use case.

## H10. NVIDIA, CUDA Driver API Reference Manual, 6.1 CUDA Checkpointing

- Version: v13.4, last updated Sep 14, 2026
- URL: https://docs.nvidia.com/cuda/cuda-driver-api/cuda_driver_api/group__CUDA__CHECKPOINT.html
- Fetch: curl, HTTP 200. The older URL docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__CHECKPOINT.html returned 404 on the day.
- Raw text: `pause_lit/hardware/cuda_driver_api_13.4_checkpoint.txt`

> The CUDA checkpoint and restore API’s provide a way to save and restore GPU state for full process checkpoints when used with CPU side process checkpointing solutions. They can also be used to pause GPU work and suspend a CUDA process to allow other applications to make use of GPU resources.

> Checkpoint and restore capabilities are currently restricted to Linux.

> Lock the CUDA process specified by pid which will block further CUDA API calls.

> GPU UUID pairs can be specified in args to remap the process old GPUs onto new GPUs. The GPU to restore onto needs to have enough memory and be of the same chip type as the old GPU.

Tag: D6. States the prediction (driver API, v13.4); restore onto a different GPU of the same chip type is now documented (contrast the 2024 blog "no GPU migration").

## H11. NVIDIA, CUDA Driver API Reference Manual, 7.49 CUcheckpointGpuPair

- Version: v13.4, last updated Sep 14, 2026
- URL: https://docs.nvidia.com/cuda/cuda-driver-api/cuda_driver_api/structCUcheckpointGpuPair.html
- Fetch: curl, HTTP 200.
- Raw text: `pause_lit/hardware/cuda_driver_api_13.4_gpupair.txt`

> CUDA checkpoint GPU UUID pairs for device remapping during restore.

Tag: D6. Bears on it: device remapping on restore (v13.4).

## H12. Stoyanov et al., "CRIUgpu: Transparent Checkpointing of GPU-Accelerated Workloads"

- Version: arXiv 2502.16631v1, 23 Feb 2025
- URL: https://arxiv.org/abs/2502.16631
- Fetch: arXiv PDF, HTTP 200 (16 pages); abs page lists only v1. The CRIU repository (github.com/checkpoint-restore/criu) was not fetched: github.com returns HTTP 403 through the proxy.
- Raw text: `pause_lit/hardware/2502.16631.txt`

> (ii) Checkpointing the GPU state of CUDA tasks into host memory allocations managed by the driver, and releasing all GPU resources held by the application. Executing these steps results in the CUDA tasks entering a checkpointed state without direct reference to GPU hardware.

> CRIUgpu relies on a locking mechanism that ensure the execution of tasks is suspended before creating a checkpoint. This guarantees consistent CPU-GPU snapshots and deterministic restore operations

> CRIUgpu can create unified CPU-GPU snapshots for large models in single- and multi-GPU setups without steady-state performance overhead.

Tag: D6. States the prediction (unified transparent CPU+GPU snapshot via cuda-checkpoint + CRIU; authors claim deterministic restore).

> Checkpointed applications can only be restored on systems with compatible GPU topology with the same number, type, memory size, VRAM accessibility by the host, and connectivity between GPUs.

> at the time of writing, the cuda-checkpoint tool does not support checkpoint/restore operations with NCCL.

> Replaying the logged API calls during restore can also lead to prolonged recovery times and inconsistent GPU state, especially with non-deterministic operations such as floating-point computations [52].

Tag: D6. Bears on it: restore constrained to same topology; no NCCL support (Feb 2025); API-replay alternatives risk inconsistent state.

> CRIUgpu Checkpoint (s) 77.40 146.43 88.81 130.81 CRIUgpu Restore (s) 38.83 98.91 43.43 145.14 GPU memory 54 GB 54 GB 58 GB 58 GB Table 2.CRIUgpu checkpoint and restore times for Llama 3.1 and GPT-2 model training on a single H100 80GB and A100 80GB GPU.

> A key insight is the dominance of GPU memory in overall checkpoint size, consistently exceeding 80% and often surpassing 90%

Tag: D6. Bears on it (cost): Table 2 reports 77.40-146.43 s checkpoint and 38.83-145.14 s restore for 54-58 GB of GPU memory; checkpoint dominated by GPU memory.

## H13. Vadari, "The Model Parking Tax: Quantifying the Hidden Energy Cost of Always-On GPU Model Deployment"

- Version: arXiv 2605.23918v1, 15 Apr 2026
- URL: https://arxiv.org/abs/2605.23918
- Fetch: arXiv PDF, HTTP 200 (7 pages). Single author (8bit.ai). The 2024 US Data Center Energy Usage Report it cites (LBNL; eta-publications.lbl.gov, redirecting to escholarship.org/uc/item/32d6m0d1) returned HTTP 403 by curl and could not be read by WebFetch, so the "~20% of TDP" figure is secondhand.
- Raw text: `pause_lit/hardware/2605.23918.txt`

> the CUDA context forces a discrete DVFS transition consuming +26–66W over bare idle (26–50 W on HBM architectures, 66 W on GDDR6), while the marginal VRAM effect is bounded below measurement relevance

> Our results identify a constraint consistent across all tested architectures: idle-with-context power is determined by DVFS state, not memory occupancy.

> Bare idle (W) 71.8 53.7 35.6 SM clock, bare (MHz) 345 210 210 CUDA ctx power (W) 121.7 80.0 102.1 SM clock, ctx (MHz) 1980 1410 2520 Context overhead (W) +49.9 +26.3 +66.4 Context (% of TDP) 7.1% 8.8% 19.0%

> CUDA active(1980 MHz): 7 GPUs, mean 145.5 W± 11.2 W. The CUDA context effect is+70.9W

Tag: D7. Bears on it directly (idle-with-context: 121.7 W H100, 80.0 W A100, 102.1 W L40S controlled; 145.5 W H100 fleet telemetry). Whether that is a "substantial fraction of active power" is not stated here; the paper reports the context step as 7-19% of TDP. Single-author preprint (v1).

> The 2024 US Data Center Energy Usage Report estimates GPU idle power at∼20% of Thermal Design Power (TDP) [2].

> Once a CUDA context is created—by any CUDA runtime call—the SM clock jumps to maximum boost andremains thereat 0% utilization [ 1].

> All three approaches maintain at least one active CUDA context, meaning the DVFS overhead we measure persists.

Tag: D7. Bears on it: ~20% of TDP idle is quoted SECONDHAND (the LBNL report itself returned 403 on the day). MIG/MPS/time-slicing keep a context, so the step persists.

## H14. Lei et al., "The Energy Cost of Execution-Idle in GPU Clusters"

- Version: arXiv 2604.04745v1, 6 Apr 2026
- URL: https://arxiv.org/abs/2604.04745
- Fetch: arXiv PDF, HTTP 200 (15 pages). Telemetry 4 Feb to 7 Mar 2026, 756 GPUs, six models.
- Raw text: `pause_lit/hardware/2604.04745.txt`

> GPUs are becoming a major contributor to data center power, yet unlike CPUs, they can remain at high power even when visible activity is near zero. We call this stateexecution-idle.

> yet power stays around 110 W. Only after the program terminates does the GPU enterdeep idle, where power drops to the baseline level of roughly 35 W.

> It accounts for 48% of energy in long-lived, academic serving workloads and 7–65% across five replays of industry-derived traces

> setting only the SM-related clock to the available minimum reduces execution-idle power from 105 W to 61 W, while lowering both SM and memory clocks further reduces it to 35 W (deep idle power).

Tag: D7. States the prediction in its own terms (a loaded-but-inactive GPU draws well above deep idle; large share of serving energy); clock downscaling recovers most of it.

## H15. Argerich, Fürst, Patiño-Martínez, "Watt Counts: Energy-Aware Benchmark for Sustainable LLM Inference on Heterogeneous GPU Architectures"

- Version: arXiv 2604.09048v1, 10 Apr 2026
- URL: https://arxiv.org/abs/2604.09048
- Fetch: arXiv PDF, HTTP 200 (17 pages). Comment on abs page: "Under review".
- Raw text: `pause_lit/hardware/2604.09048.txt`

> The H100 with a relatively high idle power (59W) and midrange max power draw (416W)

> (L4: 17W, 73W, T4: 12W, 82W, A30: 27W, 171W)

Tag: D7. Bears on it: idle vs max measured power per GPU as the paper reports them. Idle here is not stated to be with a resident model.

## H16. Vercellino et al., "Measurement of Generative AI Workload Power Profiles for Whole-Facility Data Center Infrastructure Planning"

- Version: arXiv 2604.07345v1, 8 Apr 2026
- URL: https://arxiv.org/abs/2604.07345
- Fetch: arXiv PDF, HTTP 200 (43 pages).
- Raw text: `pause_lit/hardware/2604.07345.txt`

> the measured average and standard deviation for idle power of operation were 72.5 W (±0.1 W) for each GPU

> The HPL benchmark was used to stress-test GPUs, yielding a mean peak power of 696 W.

Tag: D7. Bears on it: H100 SXM idle 72.5 W vs 696 W HPL stress as reported; idle without a resident job.

## H17. Patel et al., "POLCA: Power Oversubscription in LLM Cloud Providers"

- Version: arXiv 2308.12908v1, 24 Aug 2023
- URL: https://arxiv.org/abs/2308.12908
- Fetch: arXiv PDF, HTTP 200 (13 pages). The task names the ASPLOS 2024 paper "Characterizing Power Management Opportunities for LLMs in the Cloud" as this work; the ACM version was not fetched, so the arXiv v1 is the text quoted.
- Raw text: `pause_lit/hardware/2308.12908.txt`

> While RoBERTa is still at 75% of the TDP at the iteration boundary, GPT-NeoX drops down to 50%, and Flan-T5 goes down all the way to 20%, which corresponds to the idle power of the GPUs.

Tag: D7. Bears on it: A100 idle ~20% of TDP; power at training iteration boundaries between idle and 75% of TDP. The task names the ASPLOS 2024 version "Characterizing Power Management Opportunities for LLMs in the Cloud"; only the arXiv v1 was fetched.

## H18. You, Chung, Chowdhury, "Zeus: Understanding and Optimizing GPU Energy Consumption of DNN Training", NSDI 2023

- Version: arXiv 2208.06102v2, 29 Sep 2022
- URL: https://arxiv.org/abs/2208.06102
- Fetch: arXiv PDF, HTTP 200 (21 pages). Comment: NSDI 2023.
- Raw text: `pause_lit/hardware/2208.06102.txt`

> its average power consumption tends closer to 90W, which is close to the GPU’s idle power consumption of 70W.

Tag: D7. Bears on it: V100 (power limit range 100-250 W per the paper) idle 70 W.

## H19. Chung et al., "The ML.ENERGY Benchmark", NeurIPS D&B 2025

- Version: arXiv 2505.06371v2, 16 Oct 2025
- URL: https://arxiv.org/abs/2505.06371
- Fetch: arXiv PDF, HTTP 200 (29 pages). Comment: NeurIPS D&B 2025 (Spotlight).
- Raw text: `pause_lit/hardware/2505.06371.txt`

> Generally, LLMs and VLMs consume significantly less power than the GPU’s TDP because LLM decoding, the dominant operation for LLM serving, is memory-intensive and does not fully utilize the GPU’s compute resources.

Tag: context. Context for the denominator of D7: active LLM decode power is well below TDP.

## H20. Patel et al., "Splitwise: Efficient generative LLM inference using phase splitting"

- Version: arXiv 2311.18677v2, 20 May 2024
- URL: https://arxiv.org/abs/2311.18677
- Fetch: arXiv PDF, HTTP 200 (15 pages).
- Raw text: `pause_lit/hardware/2311.18677.txt`

> the token phase is memory bound and its power draw does not vary when increasing the number of tokens to process.

> the token generation phase incurs almost no latency impact when power capping by over 50% ( i.e., 700 to 350W).

Tag: context. Context for D7 denominator: decode-phase power.

## H21. Samsi et al., "From Words to Watts: Benchmarking the Energy Costs of Large Language Model Inference"

- Version: arXiv 2310.03003v1, 4 Oct 2023
- URL: https://arxiv.org/abs/2310.03003
- Fetch: arXiv PDF, HTTP 200 (9 pages). No idle-power statement was found in this paper (search for "idle": 0 matches).
- Raw text: `pause_lit/hardware/2310.03003.txt`

> For a 30% reduction in power from 250W to 175W, the inference time increases by an average of 6.7% for a corresponding average reduction in total energy by 23.21%.

Tag: context. Context: power capping and inference energy (V100/A100); no idle figure found in this paper.

## H22. Kwon et al., "Efficient Memory Management for Large Language Model Serving with PagedAttention" (vLLM), SOSP 2023

- Version: arXiv 2309.06180v1, 12 Sep 2023
- URL: https://arxiv.org/abs/2309.06180
- Fetch: arXiv PDF, HTTP 200 (16 pages). Comment: SOSP 2023.
- Raw text: `pause_lit/hardware/2309.06180.txt`

> Approximately 65% of the memory is allocated for the model weights, which remain static during serving. Close to 30% of the memory is used to store the dynamic states of the requests.

> the KV cache of a single token demands 800 KB of space, calculated as 2 (key and value vectors)× 5120 (hidden state size)× 40 (number of layers)× 2 (bytes per FP16).

> the memory required to store the KV cache of one request can be as much as 1.6 GB.

Tag: context. Context: Transformer state at a token boundary is the KV cache, growing per token (OPT-13B figures).

> In our case, we copy evicted blocks to the CPU memory.

> Recomputation. In this case, we simply recompute the KV cache when the preempted sequences are rescheduled.

> The performances of swapping and recomputation depend on the bandwidth between CPU RAM and GPU memory and the computation power of the GPU.

Tag: D4. States the prediction (swap vs recompute; transfer vs compute cost).

## H23. Gu, Dao, "Mamba: Linear-Time Sequence Modeling with Selective State Spaces"

- Version: arXiv 2312.00752v2, 31 May 2024
- URL: https://arxiv.org/abs/2312.00752
- Fetch: arXiv PDF, HTTP 200 (36 pages).
- Raw text: `pause_lit/hardware/2312.00752.txt`

> unrolling the model autoregressively during inference requires only constant time per step since it does not require a cache of previous elements.

> autoregressive inference requires explicitly storing the entire context (i.e. the KV cache), which directly causes the slow linear-time inference and quadratic-time training of Transformers. On the other hand, recurrent models are efficient because they have a finite state, implying constant-time inference and linear-time training.

> efficient models must have a small state, while effective models must have a state that contains all necessary information from the context.

Tag: context. Context: SSM state at a token boundary is fixed-size; Transformer state is the whole context.

## H24. Peng et al., "RWKV: Reinventing RNNs for the Transformer Era"

- Version: arXiv 2305.13048v2, 11 Dec 2023
- URL: https://arxiv.org/abs/2305.13048
- Fetch: arXiv PDF, HTTP 200 (30 pages).
- Raw text: `pause_lit/hardware/2305.13048.txt`

> allows us to formulate the model as either a Transformer or an RNN, thus parallelizing computations during training and maintains constant computational and memory complexity during inference.

> RWKV (ours) O(Td) O(d) Table 1: Inference complexity comparison with different Transformers.

Tag: context. Context: RWKV inference memory O(d), constant in sequence length.

## Claims by prediction

Tags say which declared prediction a quote bears on and whether it states it, states the opposite, or only bears on it. No verdict is given.

### D1

No quote in this family (out of scope for the hardware family).

### D2

No quote in this family (out of scope for the hardware family).

### D3

No quote in this family (out of scope for the hardware family).

### D4 (1 claim(s), 3 quote(s))

- Kwon et al., "Efficient Memory Management for Large Language Model Serving with PagedAttention" (vLLM), SOSP 2023 (arXiv 2309.06180v1, 12 Sep 2023): States the prediction (swap vs recompute; transfer vs compute cost).

### D5 (6 claim(s), 15 quote(s))

- NVIDIA, "NVIDIA Tesla P100" (Pascal GP100 architecture whitepaper) (WP-08019-001_v01.1): States the prediction (instruction-level preemption from Pascal GP100; context swapped to DRAM and back). Vendor whitepaper; no overhead figure given.
- NVIDIA, CUDA C++ Programming Guide (archived) (12.4.0, last updated Mar 07, 2024): States the prediction (Pascal onward, automatic) and adds that it carries context-switch overheads (no number). This paragraph is from the archived 12.4.0 guide; the current 13.4.2 guide text contains no "Compute Preemption" / cudaDevAttrComputePreemptionSupported match (searched).
- NVIDIA, CUDA Programming Guide (current, PDF) (Release 13.4.2): Only bears on it: within one context, stream priority does not preempt running work (a user-level scheduling statement, not the hardware context-switch mechanism). Current guide 13.4.2.
- Han, Zhang, Chen, Chen, "Microsecond-scale Preemption for Concurrent GPU-accelerated DNN Inferences" (REEF), OSDI 2022 (OSDI 2022 proceedings PDF): Bears on it, partly against the "transparent/usable" reading: the hardware claim is acknowledged but REEF says there is no public or software-controllable interface; REEF instead kills and re-runs idempotent kernels (no context save).
- Fan et al., "GPreempt: GPU Preemptive Scheduling Made General and Efficient", USENIX ATC 2025 (ATC 2025 proceedings PDF): Bears on it: hardware context switch exists (driven via driver timeslices) with a stated context size (~44 MB on A100) and ~100 µs combined overhead; no user-facing interface.
- Hu et al., "Hummingbird: SLO-Oriented GPU Preemption at Microsecond-scale" (arXiv 2601.04071v2, 10 Feb 2026): Only bears on it: 2026 system-level preemption on closed-source GPUs; not the vendor mechanism.

### D6 (8 claim(s), 20 quote(s))

- S. Gurfinkel, "Checkpointing CUDA Applications with CRIU", NVIDIA Technical Blog (Jul 02, 2024 (cuda-checkpoint 550.54.09 in text)): States the prediction: transparent per-process CUDA checkpoint/restore with CRIU; suspend waits for submitted work (a quiescent point, not mid-kernel).
- S. Gurfinkel, "Checkpointing CUDA Applications with CRIU", NVIDIA Technical Blog (Jul 02, 2024 (cuda-checkpoint 550.54.09 in text)): Bears on it: limitations as of driver 550 (2024), incl. no GPU migration; preemption named as a use case.
- NVIDIA, CUDA Driver API Reference Manual, 6.1 CUDA Checkpointing (v13.4, last updated Sep 14, 2026): States the prediction (driver API, v13.4); restore onto a different GPU of the same chip type is now documented (contrast the 2024 blog "no GPU migration").
- NVIDIA, CUDA Driver API Reference Manual, 7.49 CUcheckpointGpuPair (v13.4, last updated Sep 14, 2026): Bears on it: device remapping on restore (v13.4).
- NVIDIA, CUDA Programming Guide (current, PDF) (Release 13.4.2): Bears on it: restore on a different device is possible but some properties are not guaranteed (performance, not correctness, is named).
- Stoyanov et al., "CRIUgpu: Transparent Checkpointing of GPU-Accelerated Workloads" (arXiv 2502.16631v1, 23 Feb 2025): States the prediction (unified transparent CPU+GPU snapshot via cuda-checkpoint + CRIU; authors claim deterministic restore).
- Stoyanov et al., "CRIUgpu: Transparent Checkpointing of GPU-Accelerated Workloads" (arXiv 2502.16631v1, 23 Feb 2025): Bears on it: restore constrained to same topology; no NCCL support (Feb 2025); API-replay alternatives risk inconsistent state.
- Stoyanov et al., "CRIUgpu: Transparent Checkpointing of GPU-Accelerated Workloads" (arXiv 2502.16631v1, 23 Feb 2025): Bears on it (cost): Table 2 reports 77.40-146.43 s checkpoint and 38.83-145.14 s restore for 54-58 GB of GPU memory; checkpoint dominated by GPU memory.

### D7 (7 claim(s), 17 quote(s))

- Vadari, "The Model Parking Tax: Quantifying the Hidden Energy Cost of Always-On GPU Model Deployment" (arXiv 2605.23918v1, 15 Apr 2026): Bears on it directly (idle-with-context: 121.7 W H100, 80.0 W A100, 102.1 W L40S controlled; 145.5 W H100 fleet telemetry). Whether that is a "substantial fraction of active power" is not stated here; the paper reports the context step as 7-19% of TDP. Single-author preprint (v1).
- Vadari, "The Model Parking Tax: Quantifying the Hidden Energy Cost of Always-On GPU Model Deployment" (arXiv 2605.23918v1, 15 Apr 2026): Bears on it: ~20% of TDP idle is quoted SECONDHAND (the LBNL report itself returned 403 on the day). MIG/MPS/time-slicing keep a context, so the step persists.
- Lei et al., "The Energy Cost of Execution-Idle in GPU Clusters" (arXiv 2604.04745v1, 6 Apr 2026): States the prediction in its own terms (a loaded-but-inactive GPU draws well above deep idle; large share of serving energy); clock downscaling recovers most of it.
- Argerich, Fürst, Patiño-Martínez, "Watt Counts: Energy-Aware Benchmark for Sustainable LLM Inference on Heterogeneous GPU Architectures" (arXiv 2604.09048v1, 10 Apr 2026): Bears on it: idle vs max measured power per GPU as the paper reports them. Idle here is not stated to be with a resident model.
- Vercellino et al., "Measurement of Generative AI Workload Power Profiles for Whole-Facility Data Center Infrastructure Planning" (arXiv 2604.07345v1, 8 Apr 2026): Bears on it: H100 SXM idle 72.5 W vs 696 W HPL stress as reported; idle without a resident job.
- Patel et al., "POLCA: Power Oversubscription in LLM Cloud Providers" (arXiv 2308.12908v1, 24 Aug 2023): Bears on it: A100 idle ~20% of TDP; power at training iteration boundaries between idle and 75% of TDP. The task names the ASPLOS 2024 version "Characterizing Power Management Opportunities for LLMs in the Cloud"; only the arXiv v1 was fetched.
- You, Chung, Chowdhury, "Zeus: Understanding and Optimizing GPU Energy Consumption of DNN Training", NSDI 2023 (arXiv 2208.06102v2, 29 Sep 2022): Bears on it: V100 (power limit range 100-250 W per the paper) idle 70 W.

### D8

No quote in this family (out of scope for the hardware family).

### context (11 claim(s), 17 quote(s))

- NVIDIA GPU Operator docs, "Time-Slicing GPUs in Kubernetes" (latest (fetched 2026-09-25; no date on page)): Context: time-slicing multiplexes contexts on one GPU without memory/fault isolation.
- NVIDIA, Multi-Process Service documentation (latest, last updated Sep 09, 2026): Context: MPS reduces GPU context switching.
- NVIDIA, CUDA Programming Guide (current, PDF) (Release 13.4.2): Context: MPS avoids time-slicing between processes.
- Hu et al., "Hummingbird: SLO-Oriented GPU Preemption at Microsecond-scale" (arXiv 2601.04071v2, 10 Feb 2026): Context: suspend/resume by moving state to host memory in cluster schedulers.
- Chung et al., "The ML.ENERGY Benchmark", NeurIPS D&B 2025 (arXiv 2505.06371v2, 16 Oct 2025): Context for the denominator of D7: active LLM decode power is well below TDP.
- Patel et al., "Splitwise: Efficient generative LLM inference using phase splitting" (arXiv 2311.18677v2, 20 May 2024): Context for D7 denominator: decode-phase power.
- Samsi et al., "From Words to Watts: Benchmarking the Energy Costs of Large Language Model Inference" (arXiv 2310.03003v1, 4 Oct 2023): Context: power capping and inference energy (V100/A100); no idle figure found in this paper.
- Kwon et al., "Efficient Memory Management for Large Language Model Serving with PagedAttention" (vLLM), SOSP 2023 (arXiv 2309.06180v1, 12 Sep 2023): Context: Transformer state at a token boundary is the KV cache, growing per token (OPT-13B figures).
- Gu, Dao, "Mamba: Linear-Time Sequence Modeling with Selective State Spaces" (arXiv 2312.00752v2, 31 May 2024): Context: SSM state at a token boundary is fixed-size; Transformer state is the whole context.
- Peng et al., "RWKV: Reinventing RNNs for the Transformer Era" (arXiv 2305.13048v2, 11 Dec 2023): Context: RWKV inference memory O(d), constant in sequence length.
- Han, Zhang, Chen, Chen, "Microsecond-scale Preemption for Concurrent GPU-accelerated DNN Inferences" (REEF), OSDI 2022 (OSDI 2022 proceedings PDF): Context: kill-and-rerun preemption (idempotent kernels) as the alternative to context save.

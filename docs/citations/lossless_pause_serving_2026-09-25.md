# Lossless pause: serving family (inference preemption, KV-cache swap/recompute, LLM inference determinism)

Fetched on 2026-09-25 by a literature agent following `Lossless_Pause` BRIEF.md. This is a note, not evidence (R8). Every quote
is a verbatim substring of the raw text saved in the session scratchpad at `pause_lit/serving/<slug>.txt`. The check applies
html-unescape, removes U+FFFE and U+00AD, joins "-\n" and collapses whitespace. PDF text was extracted with pypdf, so hyphenated line
breaks appear joined in the quotes. Machine-readable claims are in `pause_lit/serving_claims.json`. The quote check found 69/69 quotes.

github.com returns HTTP 403 through the proxy, so no GitHub page (code repositories, vLLM issues #27433/#28326) was fetched. The documentation
sites and papers were used instead.

## S1. He, H. and Thinking Machines Lab, 'Defeating Nondeterminism in LLM Inference', Thinking Machines Lab: Connectionism (blog)

- Version: Sep 10, 2025 (doi 10.64434/tml.20250910)
- URL: https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/
- Fetch: Fetched with curl, HTTP 200. Author line on the page: "Horace He in collaboration with others at Thinking Machines Sep 10, 2025".
- Raw text: `pause_lit/serving/tml_blog.txt`

> the primary reason nearly all LLM inference endpoints are nondeterministic is that the load (and thus batch-size) nondeterministically varies!

> our forward pass lacks “batch invariance”, causing our request’s output to depend on the batch size of our forward pass.

> concurrency (and atomic adds) end up being completely uninvolved in LLM inference nondeterminism!

> the forward pass in an LLM is in fact “run-to-run deterministic.”

> Surprisingly, we generate 80 unique completions, with the most common of these occuring 78 times.

> when we enable our batch-invariant kernels, all of our 1000 completions are identical.

> We will set up an API server with one GPU running Qwen-3-8B, and request 1000 sequences with an output length of between 90 and 110.

> Unoptimized Deterministic vLLM 55

> Much of the slowdown comes from the fact that the FlexAttention integration in vLLM has not been heavily optimized yet.

> Despite obtaining batch invariance, we only lose about 20% performance compared to cuBLAS.

> It is not “hardware/software version invariant” — your GPU/PyTorch version may return a different value, but it should deterministically return the same value.

> it’s necessary that the reduction order for a given token does not depend on how many other tokens from its sequence are being simultaneously processed.

> the reduction order must be identical regardless of whether 0 tokens are in the KV cache (prefill) or 999 tokens are in the KV cache (decoding).

## S2. Yuan, Li, Ding, Xie, Li, Zhao, Wan, Shi, Hu, Liu, 'Understanding and Mitigating Numerical Sources of Nondeterminism in LLM Inference' (v1 title: 'Give Me FP32 or Give Me Death? Challenges and Solutions for Reproducible Reasoning'), arXiv 2506.09501

- Version: v2, 24 Oct 2025
- URL: https://arxiv.org/abs/2506.09501
- Fetch: Fetched arxiv.org/pdf/2506.09501 (current v2) and the abs page, HTTP 200. The v2 title differs from the v1 title named in the task. The code link (github.com/nanomaoli/llm_reproducibility) was not fetched: github.com returns 403 through the proxy.
- Raw text: `pause_lit/serving/yuan2025_nondeterminism.txt`

> changing system configuration, such as evaluation batch size, GPU count, and GPU version, can introduce significant differences in the generated responses.

> can exhibit up to9% variation in accuracy and 9,000 tokens difference in response length due to differences in GPU count, type, and evaluation batch size.

> the technique is currently limited to handling variations related only to the batch dimension, making it robust to continuous batching and other batch-size–related changes, but not to other forms of nondeterminism like changing the TP sizes or GPU types.

> (1) continuous batching[ 36], which dynamically modifies the set of requests within a batch;(2) different operator implementations, such as Split-K versus Non-Split-K MatMul [23]

> (4) collective operations in parallel settings, such as AllReduce; and(5) parallelization strategies, such as tensor parallelism (TP)

> LayerCast produces consistent outputs across different batch sizes and GPU configurations, with divergence rates below 3.4%.

> LayerCast offers substantial benefits over full FP32: memory usage is reduced by 34%

## S3. vLLM documentation, 'Batch Invariance' (latest developer preview docs)

- Version: page dated September 23, 2026; fetched 2026-09-25
- URL: https://docs.vllm.ai/en/latest/features/batch_invariance.html
- Fetch: Fetched with curl, HTTP 200. The page banner says it is the latest developer preview docs.
- Raw text: `pause_lit/serving/vllm_bi.txt`

> Batch invariance ensures that the output of a model is deterministic and independent of the batch size or the order of requests in a batch.

> Enabling batch invariance may impact performance compared to the default non-deterministic mode. This trade-off is intentional to guarantee reproducibility.

> Batch invariance is currently in beta.

> Disables certain optimizations that may introduce non-determinism (such as custom all-reduce operations in tensor parallel mode)

## S4. vLLM documentation, 'Reproducibility' (latest developer preview docs)

- Version: page dated April 28, 2026; fetched 2026-09-25
- URL: https://docs.vllm.ai/en/latest/usage/reproducibility.html
- Fetch: Fetched with curl, HTTP 200. The page banner says it is the latest developer preview docs.
- Raw text: `pause_lit/serving/vllm_repro.txt`

> Even with the above settings, vLLM only provides reproducibility when it runs on the same hardware and the same vLLM version.

> vLLM does not guarantee the reproducibility of the results by default, for the sake of performance.

> In offline mode, you can either set VLLM_ENABLE_V1_MULTIPROCESSING=0 which makes scheduling deterministic, or enable batch invariance to make the outputs insensitive to scheduling.

## S5. vLLM documentation, 'Optimization and Tuning' (stable docs; page references vLLM v0.23.0)

- Version: page dated August 20, 2026; fetched 2026-09-25
- URL: https://docs.vllm.ai/en/stable/configuration/optimization/
- Fetch: Fetched with curl, HTTP 200 (redirected to /en/stable/configuration/optimization/). The same Preemption text also appears on the /en/latest/ page, dated August 20, 2026.
- Raw text: `pause_lit/serving/vllm_opt_stable.txt`

> In such cases, vLLM can preempt requests to free up KV cache space for other requests. Preempted requests are recomputed when sufficient KV cache space becomes available again.

> In vLLM V1, the default preemption mode is RECOMPUTE rather than SWAP, as recomputation has lower overhead in the V1 architecture.

> While this mechanism ensures system robustness, preemption and recomputation can adversely affect end-to-end latency.

## S6. SGLang documentation, 'Deterministic Inference'

- Version: undated page; fetched 2026-09-25
- URL: https://docs.sglang.ai/advanced_features/deterministic_inference.html
- Fetch: Fetched with curl, HTTP 200. The page shows no date.
- Raw text: `pause_lit/serving/sglang_det.txt`

> The main source is varying batch sizes. Different batch sizes cause GPU kernels to split reduction operations differently, leading to different addition orders.

> Building on Thinking Machines Lab’s batch-invariant operators, SGLang achieves fully deterministic inference while maintaining compatibility with chunked prefill, CUDA graphs, radix cache, and non-greedy sampling.

## S7. The SGLang Team, 'Towards Deterministic Inference in SGLang and Reproducible RL Training', LMSYS Org blog

- Version: September 22, 2025 (updated September 24)
- URL: https://lmsys.org/blog/2025-09-22-sglang-deterministic/
- Fetch: Fetched with curl, HTTP 200.
- Raw text: `pause_lit/serving/lmsys_det.txt`

> Compared to the 61.5% slowdown reported in TML's blog, SGLang achieves an average slowdown of only 34.35% with the FlashInfer and FlashAttention 3 backends

> Deterministic inference is generally usable, with most slowdowns ranging from 25% to 45%

> the largest source of nondeterminism is the varying batch sizes

## S8. Wasti, Ye, Rao, Goin, Zhang, Liu, Gimelshein, Kwon, You, Li (vLLM and TorchTitan Teams), 'No More Train-Inference Mismatch: Bitwise Consistent On-Policy Reinforcement Learning with vLLM and TorchTitan', vLLM Blog

- Version: November 10, 2025
- URL: https://blog.vllm.ai/2025/11/10/bitwise-consistent-train-inference.html
- Fetch: Fetched with curl, HTTP 200.
- Raw text: `pause_lit/serving/vllm_blog_bi.txt`

> Our current results show that the bitwise RL run is 2.4x slower than the non-bitwise case.

> Kernels for high batch sizes parallelize heavily on the batch dimension, while kernels for low batch sizes parallelize more within a single instance to have better utilization on parallel cores on GPUs.

## S9. Kwon et al., 'Efficient Memory Management for Large Language Model Serving with PagedAttention', SOSP 2023, arXiv 2309.06180

- Version: v1, 12 Sep 2023 (only version)
- URL: https://arxiv.org/abs/2309.06180
- Fetch: Fetched PDF and abs page, HTTP 200. Venue SOSP 2023 (the paper's reference list cites itself as the 29th Symposium). There is only one arXiv version.
- Raw text: `pause_lit/serving/kwon2023_pagedattention.txt`

> To answer the second question of how to recover an evicted block, we consider two techniques:

> In our case, we copy evicted blocks to the CPU memory.

> Recomputation. In this case, we simply recompute the KV cache when the preempted sequences are rescheduled.

> Our results reveal that swapping incurs excessive overhead with small block sizes. This is because small block sizes often result in numerous small data transfers between CPU and GPU, which limits the effective PCIe bandwidth.

> recomputation is more efficient when the block size is small, while swapping is more efficient when the block size is large

> The performances of swapping and recomputation depend on the bandwidth between CPU RAM and GPU memory and the computation power of the GPU.

## S10. Sun, Huang, Zhao, Xiao, Zhang, Li, Lin, 'Llumnix: Dynamic Scheduling for Large Language Model Serving', OSDI 2024, arXiv 2406.03243

- Version: v1, 5 Jun 2024 (only version)
- URL: https://arxiv.org/abs/2406.03243
- Fetch: Fetched PDF and abs page, HTTP 200. The acknowledgements thank the OSDI reviewers; OSDI 2024. There is only one arXiv version.
- Raw text: `pause_lit/serving/sun2024_llumnix.txt`

> We quantify the preemption loss by measuring the latency penalty caused by preemption, including the extra queuing time and the recomputing for previous KV cache.

> the P99 request experiences a total preemption loss of 50 seconds (preempted twice)

> Naïve solutions include recomputing or copying the KV cache of the rescheduled requests, however with high computation stalls and downtime, reaching over 50× of the decoding cost

> Llumnix can safely copy the KV cache of previous tokens in parallel with the computation for new tokens. In this way, Llumnix achieves near-zero and constant downtime to the rescheduled request.

> the downtime of migration is nearly constant with increasing sequence lengths (roughly 20-30 ms), even shorter than a single decode step.

> recomputing an 8k sequence for LLaMA-30B takes 3.5s, which translates to a service stall similar to 54 decode steps.

## S11. Wu, Zhong, Zhang, Liu, Liu, Sun, Huang, Liu, Jin, 'Fast Distributed Inference Serving for Large Language Models' (FastServe), arXiv 2305.05920

- Version: v3, 25 Sep 2024
- URL: https://arxiv.org/abs/2305.05920
- Fetch: Fetched PDF (v3) and abs page, HTTP 200. The v2/v3 retitle and extend the 2023 v1 ('Fast Distributed Inference Serving for Large Language Models').
- Raw text: `pause_lit/serving/wu2023_fastserve.txt`

> FastServe swaps out inactive key-value tensors of jobs to the host memory to accommodate additional pending jobs, and swaps in key-value tensors back to the GPU memory for upcoming jobs.

> The token generation time in the decoding phase is about 60 ms, while the time to swap the key-value tensors between host memory and GPU memory with PCIe 4.0×16 full bandwidth is about 36 ms.

> Strawman solution 2: kill and re-compute low-priority jobs.

> the killed jobs lose their generation states, necessitating to rebuild their key-value tensors. This results in the waste of valuable computational resources and time.

## S12. Abhyankar, He, Srivatsa, Zhang, Zhang, 'InferCept: Efficient Intercept Support for Augmented Large Language Model Inference', ICML 2024, arXiv 2402.01869

- Version: v2, 30 May 2024
- URL: https://arxiv.org/abs/2402.01869
- Fetch: Fetched PDF (v2) and abs page, HTTP 200. The PDF header reads Proceedings of the 41st International Conference on Machine Learning.
- Raw text: `pause_lit/serving/abhyankar2024_infercept.txt`

> This approach, which we call Preserve, avoids recomputation but occupies GPU memory during the entire interception.

> Although Swap avoids recomputation and GPU memory wastage, with limited GPU-CPU link bandwidth, foreground tasks (normal forwarding) could be bottlenecked by waiting for swapping to finish.

> causing unnecessary recomputation of already computed contexts, which accounts for 37-40% of total model forwarding time.

## S13. Qiao et al., 'ConServe: Fine-Grained GPU Harvesting for LLM Online and Offline Co-Serving', arXiv 2410.01228

- Version: v2, 3 Sep 2025
- URL: https://arxiv.org/abs/2410.01228
- Fetch: Fetched PDF (v2) and abs page, HTTP 200. Found by web search on 2026-09-25 as 2025 work on preemption cost.
- Raw text: `pause_lit/serving/qiao2025_conserve.txt`

> preempting a request forces a costly choice: either discard the entire KV cache and pay for expensive recomputation later, or stall the GPU to swap it back and forth to host memory, leading to a collapse in throughput.

> Our profiling shows that under memory pressure, up to 69% of GPU time is wasted on recomputation or swapping [27].

> ConServe asynchronously checkpoints only the state of the single, newly-generated token after each iteration per request, eliminating overhead that would otherwise be proportional to the sequence’s length.

> This reduces preemption latency from the hundreds of milliseconds of a full iteration

## S14. Matteson, 'Re-feeding Is Not Replaying: Measuring Replay Noise in Counterfactual Token-Credit Estimation', arXiv 2606.15621

- Version: v1, 14 Jun 2026
- URL: https://arxiv.org/abs/2606.15621
- Fetch: Fetched PDF and abs page, HTTP 200. Found through a reference in Lorup 2026. This is a single-author preprint.
- Raw text: `pause_lit/serving/matteson2026_refeeding.txt`

> re-feeding changes the credit estimate at rates 14–28 percentage points above the replica floor

> rerunning the harness under vLLM’s batch-invariant kernels makes all three passes identical on every measured channel, with both disagreement rates exactly zero.

> Two bit-identical request batches, submitted seconds apart with identical seeds, disagree on 9–23%

## S15. Chodavarapu and Xu, 'The Illusion of Equivalence: Systematic FP16 Divergence in KV-Cached Autoregressive Inference', arXiv 2604.15409

- Version: v1, 16 Apr 2026
- URL: https://arxiv.org/abs/2604.15409
- Fetch: Fetched PDF and abs page, HTTP 200. Found through a reference in Lorup 2026.
- Raw text: `pause_lit/serving/chodavarapu2026_fp16_kv.txt`

> cache-ON and cache-OFF execution paths employ different floating-point accumulation orderings which, due to FP16 non-associativity, produce a deterministic divergence in decoded token sequences.

> These findings establish that FP16 KV cache inference is fundamentally non-equivalent to recomputation

> Controlled FP32 falsification reduces divergence by eight orders of magnitude, eliminates token flips, and drops the flip rate to exactly 0.0%

## S16. Lorup, 'Stage-Replay Divergence Follows the KV Cache: Fixed-Prefix Precision Controls and Bidirectional Cache Transplantation', arXiv 2607.28495

- Version: v1, 30 Jul 2026
- URL: https://arxiv.org/abs/2607.28495
- Fetch: Fetched PDF and abs page, HTTP 200. Found by web search on 2026-09-25. This is a single-author preprint; the affiliation line reads "Openhagen".
- Raw text: `pause_lit/serving/lorup2026_stage_replay.txt`

> In BF16, replicas remain exact while the constructions differ on 166 suffixes and 20 correctness labels

> Exact-token replay can therefore be repeatable without preserving live-state fidelity.

> The BF16 disagreements recur, whereas FP32 produces no decoded disagreement (95% Wilson upper bound 1.88%).

## Claims by prediction

Tags only. No verdict is given. Each line says whether a source states the prediction, states the opposite, or only bears on it.

### D1 (3 claims)

- S1: Bears on D1 (inference analogue): run-to-run determinism does not extend across hardware/software versions.
- S2: States for inference what D1 states for training: batch invariance does not survive a change of TP size or GPU type.
- S4: States the inference analogue of D1 (same hardware and same software version).

### D3 (18 claims)

- S1: States the prediction's first half: batch composition/size, not atomics, as the primary source.
- S1: States the 'not only atomics' part (in stronger form: atomics uninvolved in the forward pass).
- S1: States that batch-invariant kernels remove the run-to-run differences (Qwen3-235B, 1000 completions, temperature 0).
- S1: States the cost: table reads vLLM default 26 s, unoptimized deterministic 55 s, + improved attention kernel 42 s.
- S1: States a kernel-level cost (batch-invariant Triton matmul vs cuBLAS).
- S2: Bears on D3: batch size named as one source among GPU count and GPU type (not singled out as main).
- S2: Lists sources of reordering; bears on D3 (batching first among several) and D2 (collectives).
- S2: Bears on D3: an alternative remedy (FP32 compute) that reduces but does not remove divergence; cost stated against full FP32.
- S3: States the remedy and that it has a cost (not quantified here).
- S3: Bears on D3/D2: the feature is beta; also removes custom all-reduce under TP.
- S4: Bears on D3: scheduling (hence batch composition) is the variable either fixed or made irrelevant.
- S6: States the D3 mechanism.
- S6: States the remedy in a second engine.
- S7: States the cost of batch-invariant kernels in SGLang.
- S7: States D3 (citing the TML blog).
- S8: States a cost of bitwise-consistent (batch-invariant) train+inference in an RL loop.
- S8: Bears on D3: the kernel-selection mechanism behind batch-size dependence.
- S14: Bears on D3: run-to-run differences on a stock engine without batch invariance.

### D4 (20 claims)

- S1: Bears on whether recompute (prefill of the full sequence) reproduces decode-time numerics: only with batch-invariant attention.
- S5: States D4 (drop-and-recompute as the current default; swap as the alternative).
- S5: States the recompute cost (latency).
- S9: States D4 (both mechanisms).
- S9: States the cost trade-off (swap: transfer bandwidth; recompute: compute).
- S9: States D4's cost split directly.
- S10: Bears on D4: measured cost of recompute-based preemption in vLLM (LLaMA-7B, A10).
- S10: Bears on D4: a third option (live migration of KV cache between instances) with downtime independent of length.
- S10: States measured costs of recompute vs migration.
- S11: States D4 (swap) and its transfer cost (OPT-175B, 16 A100).
- S11: States D4 (recompute) and its compute cost.
- S12: States D4 plus a third option (preserve in GPU memory), with the cost of each.
- S12: States a measured compute cost of discard-and-recompute on pauses for tool calls.
- S13: States D4 and its cost.
- S13: Bears on D4: incremental KV checkpointing and layer-wise preemption as a 2025 alternative.
- S14: Bears on whether recompute (re-feed/prefill) reproduces resumed-KV outputs: not by default; yes under batch-invariant kernels in the tested configuration.
- S15: Bears on whether recompute reproduces cached decode outputs: in FP16, it does not (cache-on vs cache-off decoding).
- S15: Bears on the same point: FP32 removes the token-level divergence.
- S16: Bears on whether one-shot prefill of identical tokens reproduces the live-cache continuation: not in BF16 (200 items).
- S16: Bears on the same point; precision dependence.

D2 is not tagged separately. The collective-operation reordering (AllReduce, custom all-reduce) quoted in S2 and S3 bears on it and is noted under D3.
D5–D8 are outside this family's scope, and no serving source was tagged for them.

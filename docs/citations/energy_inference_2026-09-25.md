# Energy literature, family "inference" (fetched 2026-09-25)

Mechanisms that reduce the compute or energy of executing (serving) AI models. Every source below was fetched on 2026-09-25 as the
arXiv PDF (`https://arxiv.org/pdf/<id>`, HTTP 200 for all 33) and extracted with pypdf; the current version and its date were read from
`arxiv.org/abs/<id>` (for six ids the `export.arxiv.org` mirror returned an empty page on the first request; those were re-read from
`arxiv.org/abs/<id>` directly). The version stamp printed in each extracted PDF agrees with the version listed. Raw texts are in the
agent scratchpad under `energy_lit/inference/<id>.txt`; the row file is `energy_lit/inference_rows.json`. No github.com link was needed.
Venues are given only as printed in the fetched PDF; where the PDF prints none, that is stated.

Quotes are verbatim substrings of the extracted text after html-unescape, removal of U+FFFE / U+00AD / "-\n" joins and whitespace
collapse; table lines are quoted exactly as pypdf extracted them (including garbled spacing, ligatures and glued numbers).

This file records what the papers print. It does not grade the mechanisms.

## Sources

### 2208.07339: LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale

- Authors: Tim Dettmers, Mike Lewis, Younes Belkada, Luke Zettlemoyer
- Venue: NeurIPS 2022 (PDF footer: 36th Conference on Neural Information Processing Systems)
- arXiv: 2208.07339, current version v2, Thu 10 Nov 2022 (UTC), per arxiv.org/abs/2208.07339
- URL fetched: https://arxiv.org/pdf/2208.07339 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I1
- Verbatim quotes:
  - "which cut the memory needed for inference by half while retaining full precision performance"
  - "32-bit Float 25.65 15.91 14.43 13.30 12.45"
  - "Absmax LLM.int8() (vector-wise + decomp) 25.83 15.93 14.44 13.24 12.45"
  - "bﬂoat16 baseline 8xA100 80GB 239 32 9.94"
  - "LLM.int8() 3xA100 80GB 247 33 9.11"

### 2211.10438: SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models

- Authors: Guangxuan Xiao, Ji Lin, Mickael Seznec, Hao Wu, Julien Demouth, Song Han
- Venue: ICML 2023 (PDF footer: Proceedings of the 40th International Conference on Machine Learning)
- arXiv: 2211.10438, current version v7, Fri 29 Mar 2024 (UTC), per arxiv.org/abs/2211.10438
- URL fetched: https://arxiv.org/pdf/2211.10438 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I1
- Verbatim quotes:
  - "We demonstrate up to 1.56× speedup and 2× memory reduction for LLMs with negligible loss in accuracy"
  - "Wiki PPL↓ 7B 13B 30B 65B FP16 11.51 10.05 7.53 6.17 W8A8 SmoothQuant 11.56 10.08 7.56 6.20"
  - "OPT-30B (1 GPU) 1 512 422 314 1.35 × 57 30 1.91 ×"

### 2504.03360: Sustainable LLM Inference for Edge AI: Evaluating Quantized LLMs for Energy Efficiency, Output Accuracy, and Inference Latency

- Authors: Erik Johannes Husom, Arda Goknil, Merve Astekin, et al.
- Venue: arXiv preprint (ACM-format manuscript, 'Publication date: April 2025')
- arXiv: 2504.03360, current version v1, Fri 4 Apr 2025 (UTC), per arxiv.org/abs/2504.03360
- URL fetched: https://arxiv.org/pdf/2504.03360 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I1, I2a, I2b (measured energy)
- Verbatim quotes:
  - "Llama3.2_1b_instruct_fp16 consumes 17.60 J/token, while its most efficient quantized variant (q3_K_S) requires only 3.75 J/token, achieving a 79% reduction"
  - "llama3.2_1b_instruct_fp16 26.89 ± 25.11 15.01 ± 7.34 25.44 ± 16.74 5.93 ± 2.22 14.74 ± 7.09 17.60 ± 11.70"
  - "llama3.2_1b_instruct_q8_0 16.74 ± 15.31 5.81 ± 2.41 9.59 ± 6.22 2.40 ± 0.88 4.83 ± 2.02 7.87 ± 5.37"
  - "llama3.2_1b_instruct_fp16 0.16 ± 0.37 0.35 ± 0.48 0.03 ± 0.16 0.62 ± 0.49 0.31 ± 0.46 0.29 ± 0.39"
  - "llama3.2_1b_instruct_q8_0 0.17 ± 0.37 0.38 ± 0.49 0.04 ± 0.18 0.85 ± 0.36 0.34 ± 0.48 0.35 ± 0.38"
  - "qwen2.5_0.5b_instruct_fp16 7.25 ± 6.87 6.74 ± 2.27 3.68 ± 1.16 1.01 ± 0.10 3.43 ± 1.47 4.42 ± 2.37"
  - "qwen2.5_0.5b_instruct_q8_0 3.40 ± 3.08 3.14 ± 1.40 1.79 ± 0.59 0.58 ± 0.06 1.79 ± 0.80 2.14 ± 1.19"
  - "qwen2.5_0.5b_instruct_fp16 0.27 ± 0.45 0.32 ± 0.47 0.04 ± 0.21 0.74 ± 0.44 0.23 ± 0.42 0.32 ± 0.40"
  - "qwen2.5_0.5b_instruct_q8_0 0.29 ± 0.45 0.32 ± 0.47 0.04 ± 0.18 0.54 ± 0.50 0.22 ± 0.42 0.28 ± 0.40"
  - "llama3.2_1b_instruct_q4_K_M 16.70 ± 13.19 5.21 ± 0.94 6.58 ± 3.73 2.25 ± 0.79 4.82 ± 2.21 7.11 ± 4.17"
  - "llama3.2_1b_instruct_q4_K_M 0.23 ± 0.43 0.43 ± 0.50 0.06 ± 0.24 0.87 ± 0.34 0.34 ± 0.47 0.39 ± 0.39"
  - "qwen2.5_0.5b_instruct_q4_K_M 4.43 ± 4.59 3.48 ± 1.49 2.17 ± 1.00 0.62 ± 0.09 2.08 ± 0.94 2.56 ± 1.62"
  - "qwen2.5_0.5b_instruct_q4_K_M 0.25 ± 0.43 0.32 ± 0.47 0.06 ± 0.24 0.56 ± 0.50 0.26 ± 0.44 0.29 ± 0.42"
  - "llama3.2_1b_instruct_q3_K_S 6.03 ± 9.46 4.00 ± 2.30 3.02 ± 1.70 2.33 ± 1.23 3.38 ± 2.76 3.75 ± 3.49"
  - "llama3.2_1b_instruct_q3_K_S 0.08 ± 0.26 0.26 ± 0.44 0.02 ± 0.14 0.49 ± 0.50 0.07 ± 0.26 0.18 ± 0.32"
  - "qwen2.5_0.5b_instruct_q3_K_M 3.03 ± 2.32 1.87 ± 0.47 1.90 ± 0.51 0.51 ± 0.05 1.61 ± 0.78 1.78 ± 0.83"
  - "qwen2.5_0.5b_instruct_q3_K_M 0.26 ± 0.44 0.37 ± 0.48 0.07 ± 0.25 0.70 ± 0.46 0.24 ± 0.43 0.33 ± 0.41"

### 2411.02355: "Give Me BF16 or Give Me Death"? Accuracy-Performance Trade-Offs in LLM Quantization

- Authors: Eldar Kurtic, Alexandre Marques, Shubhra Pandit, Mark Kurtz, Dan Alistarh
- Venue: venue not printed in the fetched PDF
- arXiv: 2411.02355, current version v4, Tue 26 May 2026 (UTC), per arxiv.org/abs/2411.02355
- URL fetched: https://arxiv.org/pdf/2411.02355 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I1, I2a
- Verbatim quotes:
  - "On average, 8-bit quantization achieves 99.75% recovery, while W4A16-INT reaches a competitive 99.36%"
  - "BF16 100.00 84.40 83.8 86.0 93.3 94.9 86.8 85.3 60.7"
  - "W8A8-INT 99.87 84.29 83.7 85.8 93.1 94.2 86.7 85.1 61.4"
  - "BF16 – 1.4 0.7k 6.9 3.5k 1.0 0.5k 3.3 1.6k 8.7 4.4k 4.3 2.2k 0.7 0.4k"
  - "INT81.87 2.4 1.2k15.9 8.0k1.8 0.9k 6.1 3.1k 16.5 8.3k 8.0 4.0k 1.2 0.6k"
  - "W4A16-INT 99.53 84.00 83.6 85.6 92.8 94.4 86.3 85.5 59.8"
  - "INT4 1.64 2.3 1.2k22.8 11.5k1.4 0.7k 4.3 2.2k 11.9 6.0k 5.8 2.9k 0.8 0.4k"

### 2601.22076: Where Do the Joules Go? Diagnosing Inference Energy Consumption

- Authors: Jae-Won Chung, Ruofan Wu, Jeff J. Ma, Mosharaf Chowdhury
- Venue: Preprint
- arXiv: 2601.22076, current version v2, Fri 30 Jan 2026 (UTC), per arxiv.org/abs/2601.22076
- URL fetched: https://arxiv.org/pdf/2601.22076 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I1 (FP8 energy), I7, I9 (measured energy)
- Verbatim quotes:
  - "At batch size 8–16, FP8 has higher energy (up to 56% more) and higher latency (up to 26% slower)"
  - "Energy Batch sizeFP8 wins Range Median 8–16 0/7 +13 to +56% +30% 17–64 6/13−12 to +32% +1% 65–256 11/12−29 to 0%−11%"
  - "Mean output tokens 627 7,035 11× Energy/tok @ BS 128 0.209 J 0.312 J 1.5× Energy/tok @ max BS 0.151 J 0.312 J 2.1× Energy/response 95 J 2,192 J 23×"
  - "Increasing batch size increases latency, power, and throughput, but can unlock 3–5 × energy per token reduction"

### 2504.04823: Quantization Hurts Reasoning? An Empirical Study on Quantized Reasoning Models

- Authors: Ruikang Liu, Yuxuan Sun, Manyi Zhang, et al.
- Venue: COLM 2025 (PDF header)
- arXiv: 2504.04823, current version v2, Mon 18 Aug 2025 (UTC), per arxiv.org/abs/2504.04823
- URL fetched: https://arxiv.org/pdf/2504.04823 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I1, I2a, I2b
- Verbatim quotes:
  - "Our findings reveal that while lossless quantization can be achieved with W8A8 or W4A16 quantization, lower bit-widths introduce significant accuracy risks"
  - "BF16 - - 61.7±1.7 96.3±0.5 94.2±0.2 65.7±1.8 56.0±2.3 74.8±0.4"
  - "SmoothQuant 59.2±2.2 95.4±0.4 94.2±0.3 64.0±1.2 56.7±1.7 73.9±0.5 -0.9"
  - "BF16 - - 23.3±2.2 84.7±1.5 84.5±1.3 36.2±0.8 16.4±1.1 49.0±0.3"
  - "GPTQ 21.4±3.9 83.0±1.0 83.3±0.6 32.0±5.2 13.4±0.8 46.6±1.9 -2.4"
  - "GPTQ 51.7±4.4 94.7±0.3 94.1±0.2 57.6±2.7 50.1±1.5 69.6±1.0 -5.1"

### 2404.14047: An Empirical Study of LLaMA3 Quantization: From LLMs to MLLMs (v1 title: How Good Are Low-bit Quantized LLaMA3 Models? An Empirical Study)

- Authors: Wei Huang, Xingyu Zheng, Xudong Ma, Haotong Qin, et al.
- Venue: journal-format 'Research Article' in v3; venue not named in the fetched text
- arXiv: 2404.14047, current version v3, Mon 13 Jan 2025 (UTC), per arxiv.org/abs/2404.14047
- URL fetched: https://arxiv.org/pdf/2404.14047 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I1, I2a, I2b
- Verbatim quotes:
  - "SmoothQuant can maintain the accuracy of LLaMA3 with 6/8-bit weights and acti"
  - "LLaMA3 16 16 - 6.1 9.2 10.6"
  - "GPTQ [10] 4 16 128 6.5 10.4 11.0"
  - "LLaMA3 16 16 - 2.9 6.9 8.2"
  - "QuIP [13] 4 16 - 3.4 7.1 8.4 3 16 - 4.7 8.0 8.9 2 16 - 13.0 22.2 24.9"

### 2210.17323: GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers

- Authors: Elias Frantar, Saleh Ashkboos, Torsten Hoefler, Dan Alistarh
- Venue: ICLR 2023 (PDF header)
- arXiv: 2210.17323, current version v2, Wed 22 Mar 2023 (UTC), per arxiv.org/abs/2210.17323
- URL fetched: https://arxiv.org/pdf/2210.17323 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I2a, I2b
- Verbatim quotes:
  - "end-to-end inference speedups over FP16, of around 3.25x when using high-end GPUs (NVIDIA A100) and 4.5x when using more cost-effective ones (NVIDIA A6000)"
  - "full 16 27.65 22.00 14.63 12.47 10.86 10.13 9.56 9.34 8.34"
  - "GPTQ 4 31.12 24.24 15.47 12.87 11.39 10.31 9.63 9.55 8.37"
  - "GPTQ 3 53.85 33.79 20.97 16.88 14.86 11.61 10.27 14.16 8.68"
  - "A100 – 80GB 230ms 71ms 3.24× 5→ 1"

### 2306.00978: AWQ: Activation-aware Weight Quantization for On-Device LLM Compression and Acceleration

- Authors: Ji Lin, Jiaming Tang, Haotian Tang, Shang Yang, et al., Song Han
- Venue: MLSys 2024 (PDF footer: Proceedings of the 7th MLSys Conference)
- arXiv: 2306.00978, current version v6, Sat 25 Apr 2026 (UTC), per arxiv.org/abs/2306.00978
- URL fetched: https://arxiv.org/pdf/2306.00978 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I2a, I2b
- Verbatim quotes:
  - "we consistently observe a3.2-3.3× average speedup compared to the FP16 implementation by Huggingface across a diverse spectrum of LLMs"
  - "FP16 - 5.47 4.88 3.32 5.68 5.09 4.10 3.53"
  - "AWQ5.60 4.97 3.41 5.78 5.19 4.21 3.62"
  - "VILA-7B FP16 81.6 58.5 11.5"
  - "VILA-7B-AWQ W4A16 155.3 168.1 35.6"
  - "AWQ6.24 5.32 3.74 6.35 5.52 4.61 3.95"

### 2402.04396: QuIP#: Even Better LLM Quantization with Hadamard Incoherence and Lattice Codebooks

- Authors: Albert Tseng, Jerry Chee, Qingyao Sun, Volodymyr Kuleshov, Christopher De Sa
- Venue: ICML 2024 (PDF footer: Proceedings of the 41st International Conference on Machine Learning)
- arXiv: 2402.04396, current version v2, Tue 4 Jun 2024 (UTC), per arxiv.org/abs/2402.04396
- URL fetched: https://arxiv.org/pdf/2402.04396 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I2a, I2b
- Verbatim quotes:
  - "FP16 16 5.12 6.63 16 4.57 6.05 16 3.12 4.97"
  - "QUIP# 2 6.19 8.16 2 5.35 7.20 2 3.91 5.71"
  - "FP16 33.1 TOK /S OOM"
  - "QUIP# 2 B IT 106.3 25.9"
  - "QUIP# 3 5.41 7.04 3 4.78 6.35 3 3.35 5.15"

### 1503.02531: Distilling the Knowledge in a Neural Network

- Authors: Geoffrey Hinton, Oriol Vinyals, Jeff Dean
- Venue: arXiv (NIPS 2014 Deep Learning Workshop; venue not printed in the fetched PDF)
- arXiv: 1503.02531, current version v1, Mon 9 Mar 2015 (UTC), per arxiv.org/abs/1503.02531
- URL fetched: https://arxiv.org/pdf/1503.02531 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I3
- Verbatim quotes:
  - "More than 80% of the improvement in frame classiﬁcation accuracy achieved by using an ensemble of 10 models is transfe"
  - "System Test Frame Accuracy WER Baseline 58.9% 10.9% 10xEnsemble 61.1% 10.7% Distilled Single model 60.8% 10.7%"
  - "Baseline (100% of training set) 63.4% 58.9% Baseline (3% of training set) 67.3% 44.5% Soft Targets (3% of training set) 65.4% 57.0%"
  - "a smaller net with two hidden layers of 800 rectiﬁed linear hidden unit s and no regularization achieved 146 errors"
  - "at a temperature of 20, it ac hieved 74 tes"

### 1910.01108: DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter

- Authors: Victor Sanh, Lysandre Debut, Julien Chaumond, Thomas Wolf
- Venue: venue not printed in the fetched PDF
- arXiv: 1910.01108, current version v4, Sun 1 Mar 2020 (UTC), per arxiv.org/abs/1910.01108
- URL fetched: https://arxiv.org/pdf/1910.01108 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I3
- Verbatim quotes:
  - "it is possible to reduce the size of a BERT model by 40%, while retaining 97% of its language understanding capabilities and being 60% faster"
  - "BERT-base 79.5 56.3 86.7 88.6 91.8 89.6 69.3 92.7 89.0 53.5 DistilBERT 77.0 51.3 82.2 87.5 89.2 88.5 59.9 91.3 86.9 56.3"
  - "BERT-base 110 668 DistilBERT 66 410"
  - "Ablation Variation on GLUE macro-score ∅ - Lcos - Lmlm -2.96"

### 2306.08543: MiniLLM: On-Policy Distillation of Large Language Models

- Authors: Yuxian Gu, Li Dong, Furu Wei, Minlie Huang
- Venue: venue not printed in the fetched v6 PDF
- arXiv: 2306.08543, current version v6, Sat 31 Jan 2026 (UTC), per arxiv.org/abs/2306.08543
- URL fetched: https://arxiv.org/pdf/2306.08543 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I3
- Verbatim quotes:
  - "SFT w/o KDdirectly fine-tunes the student model onDsupervised by the golden responses"
  - "SFT w/o KD 73.0 26.3 69.2 20.8 61.6 17.5 32.4 35.8"
  - "MINILLM 76.4 29.0 73.1 23.2 64.1 20.7* 35.5 40.2*"
  - "SFT w/o KD 38.6 23.3 26.3 10.0 32.8 14.7 16.3 18.5"
  - "MINILLM 44.7 24.6 29.2 13.2 34.1 16.9* 25.3 26.6"

### 2408.00118: Gemma 2: Improving Open Language Models at a Practical Size

- Authors: Gemma Team (Morgane Riviere, Shreya Pathak, et al.)
- Venue: technical report (arXiv)
- arXiv: 2408.00118, current version v3, Wed 2 Oct 2024 (UTC), per arxiv.org/abs/2408.00118
- URL fetched: https://arxiv.org/pdf/2408.00118 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I3
- Verbatim quotes:
  - "Comparison between a 2B model trained over 500B tokens either from scratch or with dis"
  - "from scratch distilled Average (3 bench.) 60.3 67.7"

### 2211.17192: Fast Inference from Transformers via Speculative Decoding

- Authors: Yaniv Leviathan, Matan Kalman, Yossi Matias
- Venue: ICML 2023 (PDF footer: Proceedings of the 40th International Conference on Machine Learning)
- arXiv: 2211.17192, current version v2, Thu 18 May 2023 (UTC), per arxiv.org/abs/2211.17192
- URL fetched: https://arxiv.org/pdf/2211.17192 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I4
- Verbatim quotes:
  - "When we reject a guess though, computation is wasted"
  - "ENDE T5- SMALL⋆ 0 7 0.75 3.4X"
  - "show a 2X-3X acceleration compared to the standard T5X implementation, with identical outputs"

### 2302.01318: Accelerating Large Language Model Decoding with Speculative Sampling

- Authors: Charlie Chen, Sebastian Borgeaud, Geoffrey Irving, Jean-Baptiste Lespiau, Laurent Sifre, John Jumper
- Venue: arXiv preprint
- arXiv: 2302.01318, current version v1, Thu 2 Feb 2023 (UTC), per arxiv.org/abs/2302.01318
- URL fetched: https://arxiv.org/pdf/2302.01318 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I4
- Verbatim quotes:
  - "Yet, we have parity in the benchmark metrics"
  - "ArS (Nucleus) HumanEval (100 Shot) 45.1% 14.1ms/Token 1"
  - "SpS (Nucleus) 47.0% 5.73ms/Token"

### 2401.15077: EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty

- Authors: Yuhui Li, Fangyun Wei, Chao Zhang, Hongyang Zhang
- Venue: venue not printed in the fetched v3 PDF
- arXiv: 2401.15077, current version v3, Tue 4 Mar 2025 (UTC), per arxiv.org/abs/2401.15077
- URL fetched: https://arxiv.org/pdf/2401.15077 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I4
- Verbatim quotes:
  - "For LLaMA2-Chat 70B, EAGLE achieved a latency speedup ratio of 2.7x-3.5x, doubled throughput, while maintaining the distribution of the generated text"
  - "Batch size 1 2 3 4 Throughput Vicuna 7B 2.90x 2.87x 2.65x 2.76x 1.97x LLaMA2-Chat 70B 3.01x 2.81x 2.50x 2.40x 1.99x"

### 2504.17674: Energy Considerations of Large Language Model Inference and Efficiency Optimizations

- Authors: Jared Fernandez, Clara Na, Vashisth Tiwari, Yonatan Bisk, Sasha Luccioni, Emma Strubell
- Venue: venue not printed in the fetched v1 PDF
- arXiv: 2504.17674, current version v1, Thu 24 Apr 2025 (UTC), per arxiv.org/abs/2504.17674
- URL fetched: https://arxiv.org/pdf/2504.17674 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I4, I9 (measured energy, NVML)
- Verbatim quotes:
  - "Speculative Decoding Only Reduces Energy at Low Batch Sizes"
  - "At smaller batch sizes ( ≤ 16) speculative decoding is effective in reducing the total energy cost of inference with up to +29.14% compared to single-example inference"
  - "autoregressive decoding methods are more efficient at larger batch sizes, with speculative decoding requiring 25.65% more energy when performing inference at a batch size of 128"
  - "Dataset PyTorch % ∆ vLLM % ∆ BurstGPT 506.52% 63.75% Azure Code 102.79% 26.59% Azure Conversation 490.23% 64.22%"

### 2602.09113: Benchmarking the Energy Savings with Speculative Decoding Strategies

- Authors: Rohit Dutta, Paramita Koley, Soham Poddar, et al.
- Venue: arXiv preprint
- arXiv: 2602.09113, current version v1, Mon 9 Feb 2026 (UTC), per arxiv.org/abs/2602.09113
- URL fetched: https://arxiv.org/pdf/2602.09113 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I4 (measured energy)
- Verbatim quotes:
  - "we argue that walltime speedup (Li et al., 2024a, 2025) does notnecessarily translate into proportional energy savings"
  - "EAGLE3 2.90× 1.74× 2.09× 2.62× 1.58× 1.73× 1.84× 1.31× 1.52×"
  - "EAGLE3 1.35×1.34×1.34× 1.28× 1.26× 1.28× 0.68× 0.78× 0.77×"

### 2309.06180: Efficient Memory Management for Large Language Model Serving with PagedAttention

- Authors: Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, et al., Ion Stoica
- Venue: SOSP 2023 (PDF footer: SOSP '23)
- arXiv: 2309.06180, current version v1, Tue 12 Sep 2023 (UTC), per arxiv.org/abs/2309.06180
- URL fetched: https://arxiv.org/pdf/2309.06180 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I5, I9
- Verbatim quotes:
  - "vLLM achieves 1.67× higher throughput than Orca (Oracle) when the one-shot prefix is shared"
  - "when more examples are shared (Fig. 16 (b)), vLLM achieves 3.58× higher throughput than Orca (Oracle)"
  - "We show 6.1% - 9.8% memory saving on parallel sampling and 37.6% - 55.2% on beam search"
  - "vLLM can sustain 1.7×–2.7× higher request rates compared to Orca (Oracle) and 2.7×–8× compared to Orca (Max), while maintaining similar latencies"
  - "Compared to FasterTransformer, vLLM can sustain up to 22× higher request rates"
  - "vLLM improves the LLM serving throughput by 2-4× compared to the state-of-the-art systems [31, 60], without affecting the model accuracy at all"

### 2312.07104: SGLang: Efficient Execution of Structured Language Model Programs

- Authors: Lianmin Zheng, Liangsheng Yin, Zhiqiang Xie, et al., Ying Sheng
- Venue: venue not printed in the fetched v2 PDF
- arXiv: 2312.07104, current version v2, Thu 6 Jun 2024 (UTC), per arxiv.org/abs/2312.07104
- URL fetched: https://arxiv.org/pdf/2312.07104 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I5
- Verbatim quotes:
  - "Experiments show that SGLang achieves up to 6.4× higher throughput compared to state-of-the-art inference systems"
  - "we observed a 52.4% RadixAttention cache hit rate for LLaV A-Next-34B [28] and 74.1% for Vicuna-33B [7]"
  - "This reduces first-token latency by an average of 1.7× for Vicuna-33B"
  - "It takes 74.3 seconds to run 100 requests; however, the time used for managing the RadixAttention data structures is only 0.2 seconds, which is a negligible overhead of less than 0.3%"
  - "SGLang improves throughput by up to 6.4× and reduces latency by up to 3.7×"

### 2207.07061: Confident Adaptive Language Modeling

- Authors: Tal Schuster, Adam Fisch, Jai Gupta, et al., Donald Metzler
- Venue: NeurIPS 2022 (PDF footer)
- arXiv: 2207.07061, current version v2, Tue 25 Oct 2022 (UTC), per arxiv.org/abs/2207.07061
- URL fetched: https://arxiv.org/pdf/2207.07061 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I6
- Verbatim quotes:
  - "we demonstrate the efﬁcacy of our framework in reducing compute—speedup of up to ×3—while provably maintaining high performance"
  - "0.05 softmax 1.73 ×0.50 ×3.53 1.96 ×0.85 ×2.73 1.65 ×3.15 ×1.63"

### 2404.16710: LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding

- Authors: Mostafa Elhoushi, Akshat Shrivastava, Diana Liskovich, et al.
- Venue: venue not printed in the fetched v4 PDF
- arXiv: 2404.16710, current version v4, Fri 18 Oct 2024 (UTC), per arxiv.org/abs/2404.16710
- URL fetched: https://arxiv.org/pdf/2404.16710 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I6
- Verbatim quotes:
  - "We show speedup of upto 1.82× with no accuracy drop"
  - "Autoregressive - - 0.079 - 62.7 1.00× - - 0.098 - 37.2 1.00× Early Exit 8 - 0.012 - 232.4 - 15 - 0.016 - 105.5"
  - "Autoregressive - - 0.079 - 62.7 1.00×"
  - "Self Speculative 8 12 0.078 68.9% 127.9 1.86×"
  - "Autoregressive - 0.0513 - 34 1.0× Early Exit 6 0.0035 - 170 Self Speculative 6 0.0513 45% 62 1.82×"

### 2404.02258: Mixture-of-Depths: Dynamically allocating compute in transformer-based language models

- Authors: David Raposo, Sam Ritter, Blake Richards, Timothy Lillicrap, Peter Conway Humphreys, Adam Santoro
- Venue: arXiv preprint
- arXiv: 2404.02258, current version v1, Tue 2 Apr 2024 (UTC), per arxiv.org/abs/2404.02258
- URL fetched: https://arxiv.org/pdf/2404.02258 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I6
- Verbatim quotes:
  - "can be upwards of 50% faster to step during post-training sampling"
  - "Notably, model #3 achieves equal performance to the isoFLOP optimal baseline but steps 66% faster, due to the relatively fewer FLOPs needed per forward pass"
  - "achieves training loss parity with an isoFLOP optimal vanilla transformer, but which uses a fraction of the FLOPs (upwards of 50%) per forward pass"

### 2501.19393: s1: Simple test-time scaling

- Authors: Niklas Muennighoff, Zitong Yang, Weijia Shi, et al.
- Venue: venue not printed in the fetched v3 PDF
- arXiv: 2501.19393, current version v3, Sat 1 Mar 2025 (UTC), per arxiv.org/abs/2501.19393
- URL fetched: https://arxiv.org/pdf/2501.19393 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I7
- Verbatim quotes:
  - "To prevent exceeding the limit, we test budget forcing the thinking to end once the limit is reached. This leads to perfect control"
  - "Tokens instructed (→) 1024 2048 4096 8192 16384 No intervention at test-time Thinking tokens 7939 7158 8263 7108 7500 Answer tokens 689 669 659 722 724 AIME24 26.7 30.0 33.3 33.3 40.0 Forcing end of thinking when token budget is reached Thinking tokens 1024 2048 4031 5664 6330 Answer tokens 15 15 142 722 691 AIME24 3.3 30.0 33.3 33.3 40.0"

### 2412.21187: Do NOT Think That Much for 2+3=? On the Overthinking of o1-Like LLMs

- Authors: Xingyu Chen, Jiahao Xu, Tian Liang, et al.
- Venue: venue not printed in the fetched v2 PDF
- arXiv: 2412.21187, current version v2, Sat 1 Feb 2025 (UTC), per arxiv.org/abs/2412.21187
- URL fetched: https://arxiv.org/pdf/2412.21187 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I7
- Verbatim quotes:
  - "SimPO achieves the best results, reducing the number of generated tokens by 22.3% on MATH500"
  - "MATH500 QwQ-32B-Preview 93.0 3.2 2407.9 52.3% 71.2%"
  - "+SimPOFCS+Reflection (Ours) 92.8 1.9 1330.7 80.0% 89.5%"
  - "AIME24 Qwen2.5-Math-72B-Instruct 23.3 1.0 1204.5 23.3% 100.0% QwQ-32B-Preview 46.7 2.6 9480.9 38.4% 84.4% +SimPOFCS+Reflection 43.3 1.7 5154.5 39.8% 92.0%"

### 2503.04697: L1: Controlling How Long A Reasoning Model Thinks With Reinforcement Learning

- Authors: Pranjal Aggarwal, Sean Welleck
- Venue: COLM 2025 (PDF header)
- arXiv: 2503.04697, current version v2, Fri 3 Oct 2025 (UTC), per arxiv.org/abs/2503.04697
- URL fetched: https://arxiv.org/pdf/2503.04697 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I7
- Verbatim quotes:
  - "On math reasoning tasks, L1 outperforms S1 by up to 100% relative and 20% absolute, under identical conditions"
  - "DeepScaleR-24K40.227.3 -12.9"
  - "L1-Max(1024 tokens)16.3 11.9 -4.4"

### 2504.09858: Reasoning Models Can Be Effective Without Thinking

- Authors: Wenjie Ma, Jingxuan He, Charlie Snell, Tyler Griggs, Sewon Min, Matei Zaharia
- Venue: Preprint
- arXiv: 2504.09858, current version v1, Mon 14 Apr 2025 (UTC), per arxiv.org/abs/2504.09858
- URL fetched: https://arxiv.org/pdf/2504.09858 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I7
- Verbatim quotes:
  - "Across all datasets, NoThinking eventually matches Thinking at the largest k, while still using 2.0–5.1x fewer tokens"
  - "especially in low-budget settings, e.g., 51.3 vs. 28.9 on ACM 23 with 700 tokens"
  - "MiniF2F 7767 743956 34.84 1200 (-6.47x) 190349 (-3.91x) 36.38 2"

### 2305.05176: FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance

- Authors: Lingjiao Chen, Matei Zaharia, James Zou
- Venue: arXiv preprint (v1 only)
- arXiv: 2305.05176, current version v1, Tue 9 May 2023 (UTC), per arxiv.org/abs/2305.05176
- URL fetched: https://arxiv.org/pdf/2305.05176 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I8
- Verbatim quotes:
  - "FrugalGPT can match the performance of the best individual LLM (e.g. GPT-4) with up to 98% cost reduction or improve the accuracy over GPT-4 by 4% with the same cost"
  - "HEADLINES GPT-4 33.1 0.6 98.3%"
  - "OVERULLING GPT-4 9.7 2.6 73.3%"
  - "COQA GPT-3 72.5 29.6 59.2%"

### 2406.18665: RouteLLM: Learning to Route LLMs with Preference Data

- Authors: Isaac Ong, Amjad Almahairi, Vincent Wu, et al., Ion Stoica
- Venue: ICLR 2025 (PDF header)
- arXiv: 2406.18665, current version v4, Sun 23 Feb 2025 (UTC), per arxiv.org/abs/2406.18665
- URL fetched: https://arxiv.org/pdf/2406.18665 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I8
- Verbatim quotes:
  - "we calculate the inverse of the ratio of GPT-4 calls made by our top-performing router relative to the random baseline"
  - "Note that the MT Bench score at CPT(50%), 8.8, is 95% that of GPT-4’s score (9.3)"
  - "Matrix Factorization 13.40% 31.31% 0.802 (+60.4%)"
  - "MT Bench 3.66 (95% GPT-4 quality) 2.49"
  - "Note that the MMLU score at CPT(50%), 75, is 92% that of GPT-4’s score (81)"
  - "MMLU 1.41 (92% GPT-4 quality) 1.14"

### 2410.10347: A Unified Approach to Routing and Cascading for LLMs

- Authors: Jasper Dekoninck, Maximilian Baader, Martin Vechev
- Venue: ICML 2025 (PDF footer: Proceedings of the 42nd International Conference on Machine Learning)
- arXiv: 2410.10347, current version v3, Thu 22 May 2025 (UTC), per arxiv.org/abs/2410.10347
- URL fetched: https://arxiv.org/pdf/2410.10347 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I8
- Verbatim quotes:
  - "Cascade routing consistently outperforms all baseline strategies with performance gains between 1% to 4%"
  - "Linear Interp. 40.51 38 .64 39 .63 74.28 61 .68 79 .11 54 .10"
  - "Cascade Routing (Ours) 54.12 51 .09 48 .55 75.52 64 .84 79 .88 59 .66"

### 2301.00774: SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot

- Authors: Elias Frantar, Dan Alistarh
- Venue: venue not printed in the fetched v3 PDF
- arXiv: 2301.00774, current version v3, Wed 22 Mar 2023 (UTC), per arxiv.org/abs/2301.00774
- URL fetched: https://arxiv.org/pdf/2301.00774 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I12
- Verbatim quotes:
  - "can reach 60% unstructured sparsity with negligible increase in perplexity"
  - "Dense 0% 12.47 10.86 10.13 9.56 9.34 8.35"
  - "SparseGPT 50% 13.48 11.55 11.17 9.79 9.32 8.21"
  - "Dense 0% 75.59 81.07 71.04 43.94 79.82 70.29"
  - "SparseGPT 50% 78.47 80.63 70.45 43.94 79.12 70.52"

### 2306.11695: A Simple and Effective Pruning Approach for Large Language Models (Wanda)

- Authors: Mingjie Sun, Zhuang Liu, Anna Bair, J. Zico Kolter
- Venue: ICLR 2024 (PDF header)
- arXiv: 2306.11695, current version v3, Mon 6 May 2024 (UTC), per arxiv.org/abs/2306.11695
- URL fetched: https://arxiv.org/pdf/2306.11695 (status 200, PDF, text extracted with pypdf)
- Mechanisms: I12
- Verbatim quotes:
  - "Structured 2:4 sparsity is able to bring notable inference speedup (around 1.6×) for linear layers in LLMs"
  - "Dense - 0 % 5.68 5.09 4.77 3.56 5.12 4.57 3.12"
  - "Wanda ✗ 2:4 11.53 9.58 6.90 6.25 11.02 8.27 5.16"
  - "For end to end latency, we observe a speedup of 1.24× on LLaMA-7B (251ms as compared to 312ms)"
  - "Wanda ✗ 50% 7.26 6.15 5.24 4.57 6.42 5.56 3.98"

## Rows by mechanism

Each row is one quoted comparison of X against reference Y. Quality and cost are as printed; cost metrics differ by row (energy where
the paper measured it; otherwise wall time, throughput, tokens, API dollars or memory). 'sd' is a printed standard deviation or an
unspecified +/-. Full fields (setting, notes, quotes) are in `inference_rows.json`.

### I1: 8-bit weight or weight-activation quantisation vs 16-bit (9 rows)

| # | source | location | X | Y | quality metric | X quality | Y quality | cost metric | X cost | Y cost |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Dettmers et al. 2022, arXiv 2208.07339v2 | Table 1 | LLM.int8() (Int8 absmax vector-wise + decomposition) | 32-bit float | C4 validation perplexity | 12.45 | 12.45 | memory footprint |  |  |
| 2 | Dettmers et al. 2022, arXiv 2208.07339v2 | Appendix D.2, Table 6 | LLM.int8() on 3xA100 80GB | bfloat16 baseline on 8xA100 80GB | none reported for this table |  |  | wall time (ms per token, batch 1) | 247 | 239 |
| 3 | Xiao et al. 2023, arXiv 2211.10438v7 | Table (Llama-1 WikiText-2, seq len 512) | W8A8 SmoothQuant | FP16 | WikiText-2 perplexity | 6.2 | 6.17 |  |  |  |
| 4 | Xiao et al. 2023, arXiv 2211.10438v7 | Table 8 | SmoothQuant-O3 (W8A8) | FP16 | none in this table |  |  | wall time (decoding latency ms) ; memory GB also printed | 314 | 422 |
| 5 | Husom et al. 2025, arXiv 2504.03360v1 | Table 6 and Table 8 | q8_0 (8-bit weight-only, llama.cpp) | fp16 | average accuracy over 5 benchmarks | 0.35 (sd 0.38) | 0.29 (sd 0.39) | energy J/token | 7.87 | 17.6 |
| 6 | Husom et al. 2025, arXiv 2504.03360v1 | Table 6 and Table 8 | q8_0 | fp16 | average accuracy over 5 benchmarks | 0.28 (sd 0.4) | 0.32 (sd 0.4) | energy J/token | 2.14 | 4.42 |
| 7 | Kurtic et al. 2024/2026, arXiv 2411.02355v4 | Table 2 and Table 6 | W8A8-INT | BF16 | Open LLM Leaderboard V1 average score | 84.29 | 84.4 | throughput queries/s, code completion, 4xA100 (higher is better) | 2.4 | 1.4 |
| 8 | Liu et al. 2025, arXiv 2504.04823v2 | Table 1 | W8A8KV8 SmoothQuant | BF16 | average accuracy (%) | 73.9 (sd 0.5) | 74.8 (sd 0.4) |  |  |  |
| 9 | Chung et al. 2026, arXiv 2601.22076v2 | Section 4.4 (table in text) | FP8 | BF16 | none reported |  |  | energy per token, median % change of FP8 vs BF16 | 30 |  |

Notes: (1) Reference is 32-bit float in Table 1 (not 16-bit). Memory cost stated qualitatively (half); no energy reported. (2) Int8 runs on 3 GPUs vs 8 for bf16; per-token latency slightly higher at batch 1. The ligature 'ﬂ' is as extracted. (3) Quality only; cost reported separately (Table 8) on OPT models. (4) Memory 30 GB vs 57 GB in the same line. Accuracy of W8A8 on OPT reported elsewhere as negligible loss. (5) Measured energy. Table 6 is 'Mean and standard deviation'; Table 8 '±' unspecified, recorded as SD. (6) Measured energy. '±' in Table 8 unspecified, recorded as SD. (7) Cost column is throughput (QPS), not energy; Table 6 also gives queries per USD (1.2k vs 0.7k). Table 6 row text is garbled by extraction ('INT81.87' = INT8, speedup 1.87). (8) '±' over three seeds, unspecified; recorded as SD. No cost column in this table. (9) FP8 uses +30% median energy at batch 8-16 (wins 0/7), +1% at 17-64, -11% at 65-256 (wins 11/12). Quality not reported in this comparison.

### I2a: 4-bit weight-only quantisation vs 16-bit (8 rows)

| # | source | location | X | Y | quality metric | X quality | Y quality | cost metric | X cost | Y cost |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Frantar et al. 2023, arXiv 2210.17323v2 | Table 3 | GPTQ 4-bit | full 16-bit | WikiText2 perplexity | 8.37 | 8.34 |  |  |  |
| 2 | Lin et al. 2024/2026, arXiv 2306.00978v6 | Table 4 | AWQ INT4-g128 | FP16 | WikiText2 perplexity | 3.41 | 3.32 |  |  |  |
| 3 | Lin et al. 2024/2026, arXiv 2306.00978v6 | Table 10 | VILA-7B-AWQ W4A16 | VILA-7B FP16 | none in this table |  |  | throughput tokens/s on A100 (higher is better) | 155.3 | 81.6 |
| 4 | Husom et al. 2025, arXiv 2504.03360v1 | Table 6 and Table 8 | q4_K_M (4-bit weight-only) | fp16 | average accuracy over 5 benchmarks | 0.39 (sd 0.39) | 0.29 (sd 0.39) | energy J/token | 7.11 | 17.6 |
| 5 | Husom et al. 2025, arXiv 2504.03360v1 | Table 6 and Table 8 | q4_K_M | fp16 | average accuracy over 5 benchmarks | 0.29 (sd 0.42) | 0.32 (sd 0.4) | energy J/token | 2.56 | 4.42 |
| 6 | Kurtic et al. 2024/2026, arXiv 2411.02355v4 | Table 2 and Table 6 | W4A16-INT (GPTQ) | BF16 | Open LLM Leaderboard V1 average score | 84 | 84.4 | throughput queries/s, code completion, 4xA100 (higher is better) | 2.3 | 1.4 |
| 7 | Liu et al. 2025, arXiv 2504.04823v2 | Table 1 | W4A16 GPTQ | BF16 | average accuracy (%) | 46.6 (sd 1.9) | 49 (sd 0.3) |  |  |  |
| 8 | Huang et al. 2024/2025, arXiv 2404.14047v3 | Table 1 | GPTQ 4-bit g128 | LLaMA3 16-bit | WikiText2 perplexity | 6.5 | 6.1 |  |  |  |

Notes: (1) Quality only; speed measured for the 3-bit model (see I2b). (2) Column order: Llama-2 7B 13B 70B, LLaMA 7B 13B 30B 65B. (3) Columns A100, 4090, Orin. Speed includes TinyChat kernels, not quantisation alone. (4) Measured energy; '±' unspecified, recorded as SD. (5) Measured energy; '±' unspecified, recorded as SD. (6) Cost column is throughput, not energy; speedup printed 1.64. (7) '±' unspecified (three seeds), recorded as SD. (8) Quality only.

### I2b: <= 3-bit quantisation vs 16-bit (8 rows)

| # | source | location | X | Y | quality metric | X quality | Y quality | cost metric | X cost | Y cost |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Frantar et al. 2023, arXiv 2210.17323v2 | Table 3 and Table 6 | GPTQ 3-bit (1 GPU) | FP16 (5 GPUs) | WikiText2 perplexity | 8.68 | 8.34 | wall time (ms per token) | 71 | 230 |
| 2 | Lin et al. 2024/2026, arXiv 2306.00978v6 | Table 4 | AWQ INT3-g128 | FP16 | WikiText2 perplexity | 3.74 | 3.32 |  |  |  |
| 3 | Tseng et al. 2024, arXiv 2402.04396v2 | Table 4 and Table 6 | QuIP# 2-bit | FP16 | WikiText2 perplexity | 6.19 | 5.12 | throughput tokens/s (higher is better) | 106.3 | 33.1 |
| 4 | Tseng et al. 2024, arXiv 2402.04396v2 | Table 4 | QuIP# 3-bit | FP16 | WikiText2 perplexity | 3.35 | 3.12 |  |  |  |
| 5 | Husom et al. 2025, arXiv 2504.03360v1 | Table 6 and Table 8 | q3_K_S (3-bit weight-only) | fp16 | average accuracy over 5 benchmarks | 0.18 (sd 0.32) | 0.29 (sd 0.39) | energy J/token | 3.75 | 17.6 |
| 6 | Husom et al. 2025, arXiv 2504.03360v1 | Table 6 and Table 8 | q3_K_M | fp16 | average accuracy over 5 benchmarks | 0.33 (sd 0.41) | 0.32 (sd 0.4) | energy J/token | 1.78 | 4.42 |
| 7 | Liu et al. 2025, arXiv 2504.04823v2 | Table 1 | W3A16 GPTQ | BF16 | average accuracy (%) | 69.6 (sd 1) | 74.8 (sd 0.4) |  |  |  |
| 8 | Huang et al. 2024/2025, arXiv 2404.14047v3 | Table 2 | QuIP 2-bit | LLaMA3 16-bit | WikiText2 perplexity | 13 | 2.9 |  |  |  |

Notes: (1) GPU count 5 -> 1 in the same line. (5) Measured energy; '±' unspecified, recorded as SD. (6) Measured energy; '±' unspecified, recorded as SD. (7) '±' unspecified (three seeds), recorded as SD. (8) The 2-bit line is the last of the three QuIP lines quoted.

### I3: distillation (student on teacher outputs) vs same student on labels (8 rows)

| # | source | location | X | Y | quality metric | X quality | Y quality | cost metric | X cost | Y cost |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Hinton et al. 2015, arXiv 1503.02531v1 | Table 1 | Distilled single model (trained on 10x-ensemble soft targets) | Baseline single model (same architecture, hard labels) | test frame accuracy (%) | 60.8 | 58.9 |  |  |  |
| 2 | Hinton et al. 2015, arXiv 1503.02531v1 | Table 5 | Soft targets (3% of training set) | Baseline hard targets (3% of training set) | test frame accuracy (%) | 57 | 44.5 |  |  |  |
| 3 | Hinton et al. 2015, arXiv 1503.02531v1 | Section 3 (MNIST) | small net trained additionally on soft targets of the large net (T=20) | same small net, no regularization, hard labels | test errors (count) | 74 | 146 |  |  |  |
| 4 | Sanh et al. 2019, arXiv 1910.01108v4 | Table 1 and Table 3 | DistilBERT (66M, distilled from BERT-base) | BERT-base (110M, the teacher) | GLUE macro-score | 77 | 79.5 | wall time (seconds, CPU inference over STS-B) | 410 | 668 |
| 5 | Sanh et al. 2019, arXiv 1910.01108v4 | Table 4 (ablation) | DistilBERT with full triple loss (Lce + Lcos + Lmlm) | same student without the soft-target loss Lce (Lcos + Lmlm) | GLUE macro-score change vs triple loss |  | -2.96 |  |  |  |
| 6 | Gu et al. 2023/2026, arXiv 2306.08543v6 | Table 1 | MiniLLM (reverse-KL on-policy distillation) | SFT w/o KD (same student, golden responses) | DollyEval GPT-4 score | 76.4 | 73 |  |  |  |
| 7 | Gu et al. 2023/2026, arXiv 2306.08543v6 | Table 1 | MiniLLM | SFT w/o KD (same student) | DollyEval GPT-4 score | 44.7 | 38.6 |  |  |  |
| 8 | Gemma Team 2024, arXiv 2408.00118v3 | Table 6 | distilled from a 7B teacher | trained from scratch (next-token prediction) | average score (3 benchmarks) | 67.7 | 60.3 |  |  |  |

Notes: (1) Same-student comparison; WER 10.7% vs 10.9%; teacher (10x ensemble) 61.1%. Student inference cost equals baseline; the ensemble costs about 10 models. (2) Hard-target baseline was early-stopped at 44.5%; full-data baseline 58.9%. (3) Teacher (large regularized net) 67 test errors. Quotes follow the extracted text, including its broken spacing. (4) Y is the teacher, not a same-student label-only baseline; this is the paper's headline comparison. (5) Only deltas printed (x is the reference, delta 0). The ablated student still uses the cosine loss and teacher initialization, so it is not a pure label-only student. (6) Teacher 79.0; word-level KD 73.7 (same table). Same student size so inference cost is equal. (7) Teacher 58.4. (8) Same student size and token count; teacher forward-pass cost during training not reported.

### I4: speculative decoding vs autoregressive decoding (7 rows)

| # | source | location | X | Y | quality metric | X quality | Y quality | cost metric | X cost | Y cost |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Leviathan et al. 2023, arXiv 2211.17192v2 | Table 2 | speculative decoding | standard T5X autoregressive decoding | output identity |  |  | wall-time speedup factor (x) | 3.4 |  |
| 2 | Chen et al. 2023, arXiv 2302.01318v1 | Table 1 | speculative sampling (SpS) | autoregressive sampling (ArS) | HumanEval pass rate (%) | 47 | 45.1 | wall time (ms per token) | 5.73 | 14.1 |
| 3 | Li et al. 2024/2025, arXiv 2401.15077v3 | Table 7 | EAGLE | vanilla autoregressive decoding | output distribution |  |  | throughput ratio (x) at max batch size; batch-1 speedup 3.01x | 1.99 |  |
| 4 | Fernandez et al. 2025, arXiv 2504.17674v1 | Section 3.2 / Figure 3 | speculative decoding, batch <= 16 | autoregressive decoding | none (lossless method) |  |  | energy (relative saving, %) | 29.14 |  |
| 5 | Fernandez et al. 2025, arXiv 2504.17674v1 | Section 3.2 / Figure 3 | speculative decoding, batch 128 | autoregressive decoding | none (lossless method) |  |  | energy (relative increase, %) | 25.65 |  |
| 6 | Dutta et al. 2026, arXiv 2602.09113v1 | Table 1 | EAGLE-3 | vanilla autoregressive decoding of the target | none (lossless method) |  |  | total energy saving factor (vanilla/SD, >1 = saving); speedup 2.90x | 2.09 |  |
| 7 | Dutta et al. 2026, arXiv 2602.09113v1 | Table 1 | EAGLE-3 | vanilla autoregressive decoding of the target | none (lossless method) |  |  | total energy saving factor (vanilla/SD, <1 = more energy); speedup 0.68x | 0.77 |  |

Notes: (1) Outputs identical by construction; reference speed is 1 by definition. The paper notes total arithmetic operations can rise when guesses are rejected. (2) Sampling distribution identical up to numerics. XSum nucleus: ROUGE-2 0.114 vs 0.112 at 7.52 vs 14.1 ms/token. (3) Distribution-preserving; maximum batch size 4 for EAGLE vs 5 for vanilla under the memory limit. (4) Measured energy. 'up to' figure. (5) Measured energy; speculative decoding costs more here. (6) Columns: HumanEval (speedup, GPU, total), GSM-8K, CNN-DM; this line is the LLAMA-8B vs LLAMA-1B block. (7) Last three numbers are CNN-DM (speedup 0.68, GPU 0.78, total 0.77): slower and more energy than vanilla.

### I5: KV / prefix caching vs recomputation (6 rows)

| # | source | location | X | Y | quality metric | X quality | Y quality | cost metric | X cost | Y cost |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Kwon et al. 2023, arXiv 2309.06180v1 | Section 6.4 / Figure 16 | vLLM with shared-prefix KV blocks | Orca (Oracle) | none (exact method) |  |  | throughput ratio (x) | 1.67 |  |
| 2 | Kwon et al. 2023, arXiv 2309.06180v1 | Section 6.4 / Figure 16 | vLLM with shared-prefix KV blocks | Orca (Oracle) | none (exact method) |  |  | throughput ratio (x) | 3.58 |  |
| 3 | Kwon et al. 2023, arXiv 2309.06180v1 | Section 6.3 / Figure 15 | vLLM KV sharing (beam search) | no sharing | none (exact method) |  |  | KV-cache memory saving (%) | 55.2 |  |
| 4 | Zheng et al. 2024, arXiv 2312.07104v2 | Section 6.2 (production deployment) | SGLang with RadixAttention (74.1% cache hit rate) | without cache reuse | none (exact method) |  |  | first-token latency reduction factor (x) | 1.7 |  |
| 5 | Zheng et al. 2024, arXiv 2312.07104v2 | Section 6.3 (overhead) | RadixAttention enabled | no RadixAttention | none |  |  | wall time (seconds) for 100 requests; management overhead 0.2 s | 74.3 |  |
| 6 | Zheng et al. 2024, arXiv 2312.07104v2 | Abstract / Section 6.2 | SGLang (RadixAttention + other runtime optimisations) | vLLM, Guidance, LMQL | none (exact methods) |  |  | throughput ratio (x), maximum | 6.4 |  |

Notes: (1) Baseline differs in more than prefix caching (memory manager too). (3) Range 37.6-55.2% for beam search; memory, not compute or energy. (4) Hit rate 74.1% for Vicuna-33B; 52.4% for LLaVA-Next-34B. (5) Overhead when there is nothing to reuse; baseline time not separately printed. (6) Whole-system comparison, not RadixAttention alone; 'up to'.

### I6: early exit / adaptive depth vs full depth (6 rows)

| # | source | location | X | Y | quality metric | X quality | Y quality | cost metric | X cost | Y cost |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Schuster et al. 2022, arXiv 2207.07061v2 | Table 2 | CALM early exit | full decoder (all layers) | calibrated risk constraint (not an observed score) |  |  | estimated whole-model speedup (x); average decoder layers 1.73 | 3.53 |  |
| 2 | Elhoushi et al. 2024, arXiv 2404.16710v4 | Table 3 | LayerSkip early exit at layer 8 | autoregressive full model | ROUGE-2 | 0.012 | 0.079 | throughput tokens/s (higher is better) | 232.4 | 62.7 |
| 3 | Elhoushi et al. 2024, arXiv 2404.16710v4 | Table 3 | LayerSkip self-speculative decoding | autoregressive full model | ROUGE-2 | 0.078 | 0.079 | throughput tokens/s (higher is better) | 127.9 | 62.7 |
| 4 | Elhoushi et al. 2024, arXiv 2404.16710v4 | Table 5 | LayerSkip self-speculative | autoregressive | ROUGE-2 | 0.0513 | 0.0513 | throughput tokens/s (higher is better) | 62 | 34 |
| 5 | Raposo et al. 2024, arXiv 2404.02258v1 | Figure 3 text | Mixture-of-Depths model #3 | isoFLOP-optimal vanilla transformer | training loss (reported as equal) |  |  | step speed increase (%) | 66 |  |
| 6 | Raposo et al. 2024, arXiv 2404.02258v1 | Abstract | MoD at loss parity | isoFLOP-optimal vanilla transformer | training loss (parity) |  |  | FLOPs per forward pass saved (%), 'upwards of' | 50 |  |

Notes: (1) Quality is guaranteed only as a bound (risk <= delta with high probability); columns CNN/DM, WMT, SQuAD (layers, FLOPs r., speedup). 'FLOPs r.' column printed as ×0.50. (2) Pure early exit loses most quality here. (3) Speedup printed 1.86x. (4) Early exit alone: ROUGE-2 0.0035 at 170 tokens/s. (5) Step speed during training; abstract says 'upwards of 50% faster to step during post-training sampling'.

### I7: controlling reasoning length vs unrestricted reasoning (8 rows)

| # | source | location | X | Y | quality metric | X quality | Y quality | cost metric | X cost | Y cost |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Muennighoff et al. 2025, arXiv 2501.19393v3 | Table 12 | budget forcing: end thinking at 2048 tokens | no intervention at test time (same prompt) | AIME24 accuracy (%) | 30 | 30 | thinking tokens (mean) | 2048 | 7158 |
| 2 | Muennighoff et al. 2025, arXiv 2501.19393v3 | Table 12 | budget forcing: end thinking at 1024 tokens | no intervention at test time (same prompt) | AIME24 accuracy (%) | 3.3 | 26.7 | thinking tokens (mean) | 1024 | 7939 |
| 3 | Chen et al. 2024/2025, arXiv 2412.21187v2 | Table 4 | SimPO with First-Correct-Solution + Reflection (length preference optimization) | QwQ-32B-Preview (unrestricted) | accuracy (%) | 92.8 | 93 | generated tokens per response (mean) | 1330.7 | 2407.9 |
| 4 | Chen et al. 2024/2025, arXiv 2412.21187v2 | Table 4 | SimPO FCS+Reflection | QwQ-32B-Preview (unrestricted) | accuracy (%) | 43.3 | 46.7 | generated tokens per response (mean) | 5154.5 | 9480.9 |
| 5 | Ma et al. 2025, arXiv 2504.09858v1 | Abstract / Figure 5 | NoThinking (thinking box prefilled empty) | Thinking | pass@1 accuracy (%) | 51.3 | 28.9 | tokens (budget, matched) | 700 | 700 |
| 6 | Ma et al. 2025, arXiv 2504.09858v1 | Table 3 | NoThinking pass@2 | Full Thinking pass@1 | accuracy (%) | 36.38 | 34.84 | total tokens across all problems and samples | 190349 | 743956 |
| 7 | Aggarwal & Welleck 2025, arXiv 2503.04697v2 | Table 3 | L1-Max limited to 1024 tokens | DeepScaleR-24K (unconstrained, 24K context) | AIME2024 accuracy (%) | 16.3 | 40.2 | token budget (upper bound) | 1024 |  |
| 8 | Chung et al. 2026, arXiv 2601.22076v2 | Table 1 | reasoning on (Problem Solving task) | reasoning off (Text Conversation task) | none reported |  |  | energy per response (J) | 2192 | 95 |

Notes: (1) Second column (2048). Answer tokens 15 vs 669. (2) First column (1024). (5) Budget-matched comparison ('ACM 23' is the abstract's typo for AMC 23). (6) Latency 1200 vs 7767 in the same line. (7) Y's actual token usage not in this table. (8) Measured energy; the two modes are run on different tasks, so this is not a same-task quality comparison. Mean output tokens 7,035 vs 627.

### I8: model cascades / routing vs always the largest model (6 rows)

| # | source | location | X | Y | quality metric | X quality | Y quality | cost metric | X cost | Y cost |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Chen et al. 2023, arXiv 2305.05176v1 | Table 3 | FrugalGPT cascade | GPT-4 (best individual LLM) | accuracy (matched to GPT-4) |  |  | API cost (USD) to reach the same accuracy | 0.6 | 33.1 |
| 2 | Chen et al. 2023, arXiv 2305.05176v1 | Table 3 | FrugalGPT cascade | GPT-4 (best individual LLM) | accuracy (matched) |  |  | API cost (USD) to reach the same accuracy | 2.6 | 9.7 |
| 3 | Chen et al. 2023, arXiv 2305.05176v1 | Table 3 | FrugalGPT cascade | GPT-3 (best individual LLM) | accuracy (matched) |  |  | API cost (USD) to reach the same accuracy | 29.6 | 72.5 |
| 4 | Ong et al. 2024/2025, arXiv 2406.18665v4 | Table 1 and Table 6 | RouteLLM router at CPT(50%) | GPT-4 alone | MT Bench score | 8.8 | 9.3 | cost saving ratio vs random router (x) | 3.66 |  |
| 5 | Ong et al. 2024/2025, arXiv 2406.18665v4 | Table 2 and Table 6 | RouteLLM router at CPT(50%) | GPT-4 alone | MMLU score | 75 | 81 | cost saving ratio vs random router (x) | 1.41 |  |
| 6 | Dekoninck et al. 2024/2025, arXiv 2410.10347v3 | Table 2 | cascade routing | linear interpolation between models | AUC of quality-cost curve (%) | 54.12 | 40.51 | integrated in AUC |  |  |

Notes: (1) Cost is API fees in dollars, not energy; saving 98.3%. (2) Saving 73.3%. (3) Saving 59.2%. (4) CPT(50%) = 13.40% of calls to GPT-4 for the best router. Saving ratio is computed against a random router, per the paper. (6) AUC combines quality and cost; no separate always-largest-model row.

### I9: serving systems vs baseline serving (record only) (5 rows)

| # | source | location | X | Y | quality metric | X quality | Y quality | cost metric | X cost | Y cost |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Kwon et al. 2023, arXiv 2309.06180v1 | Section 6.2 / Figure 12 | vLLM (PagedAttention) | Orca (Oracle) | none (exact method) |  |  | sustainable request rate ratio (x), range | 2.7 |  |
| 2 | Kwon et al. 2023, arXiv 2309.06180v1 | Section 6.2 | vLLM | FasterTransformer | none (exact method) |  |  | sustainable request rate ratio (x), maximum | 22 |  |
| 3 | Kwon et al. 2023, arXiv 2309.06180v1 | Abstract | vLLM | FasterTransformer and Orca | model accuracy (unaffected) |  |  | throughput ratio (x), range 2-4 |  |  |
| 4 | Fernandez et al. 2025, arXiv 2504.17674v1 | Table 4 | vLLM | PyTorch | none |  |  | energy above theoretical value (%) | 63.75 | 506.52 |
| 5 | Chung et al. 2026, arXiv 2601.22076v2 | Observation 4 | larger batch size | small batch size | none |  |  | energy per token reduction factor (x), range 3-5 |  |  |

Notes: (1) Range 1.7-2.7x; upper end recorded. (3) Range 2-4x not entered as a single value. (4) Measured energy. (5) Measured energy; range not entered as a single value.

### I12: pruning to 50% sparsity vs dense (record only) (4 rows)

| # | source | location | X | Y | quality metric | X quality | Y quality | cost metric | X cost | Y cost |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Frantar & Alistarh 2023, arXiv 2301.00774v3 | Table 1 and Table 2 | SparseGPT 50% | Dense | raw-WikiText2 perplexity | 8.21 | 8.35 |  |  |  |
| 2 | Frantar & Alistarh 2023, arXiv 2301.00774v3 | Table 1 | SparseGPT 50% | Dense | raw-WikiText2 perplexity | 13.48 | 12.47 |  |  |  |
| 3 | Sun et al. 2023/2024, arXiv 2306.11695v3 | Table 3 and Section 4.3 | Wanda 2:4 | Dense | WikiText perplexity | 11.53 | 5.68 | wall time (ms end-to-end latency) | 251 | 312 |
| 4 | Sun et al. 2023/2024, arXiv 2306.11695v3 | Table 3 | Wanda 50% | Dense | WikiText perplexity | 3.98 | 3.12 |  |  |  |

Notes: (1) Zero-shot average 70.52 vs 70.29. No end-to-end speed or energy for unstructured sparsity. (4) No speed reported for unstructured sparsity.

## Fetch notes and gaps

- All 33 PDFs downloaded with HTTP 200; no 403/404.
- 2404.14047 is now titled "An Empirical Study of LLaMA3 Quantization: From LLMs to MLLMs" (v3); it has no FP16 speed baseline, so its rows are quality only.
- Energy is measured in: Husom et al. 2504.03360 (edge device, J/token), Fernandez et al. 2504.17674 (NVML, GPU energy), Dutta et al. 2602.09113
  (GPU and total energy, Wh/1K tokens) and Chung et al. 2601.22076 (J/token, J/response). All other rows report time, throughput, tokens, dollars or memory.
- I3: Hinton et al., MiniLLM and Gemma 2 print same-student ablations; the DistilBERT headline row compares the student with its teacher, and its
  ablation row still keeps a cosine distillation loss and teacher initialisation.
- I8: Dekoninck et al. report only AUC over a quality-cost curve (no always-largest-model row); RouteLLM's cost-saving ratio is relative to a random router.
- I9 and I12 are record-only (silent) mechanisms; their rows are copied as printed.

Quote check (run 2026-09-25, scratchpad scripts `inference/rows/build.py` and `gen_dossier.py`): row quotes found 138/138; additional source quotes found 31/31. All row numbers appear in their quotes.

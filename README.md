# local-llm-bench-results

**Which open model should run your local agent or assistant, in Polish and English, and how fast?**
Quality and speed of open-weight LLMs, measured on one home rig with 4× AMD Radeon AI PRO R9700 (128 GB VRAM).

![Data: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-lightgrey)
![Quality bench](https://img.shields.io/badge/quality-local--llm--quality--bench%20v1.0.0-blue)
![Perf bench](https://img.shields.io/badge/speed-local--llm--perf--bench%20v2.0.0-blue)

Every number here comes from two open-source tools, and every run folder contains everything needed
to reproduce it:

- **[local-llm-quality-bench](https://github.com/michal-konik-human/local-llm-quality-bench)**: 60 agent and
  assistant tasks in Polish and English (tool calling, multi-step tasks in a mock calendar and mailbox, shopping
  on a frozen web, instruction following, writing, reasoning, coding). Graded by code first, with an LLM judge
  for writing only.
- **[local-llm-perf-bench](https://github.com/michal-konik-human/local-llm-perf-bench)**: llama.cpp throughput
  with the conditions recorded (power cap, PCIe links, temperatures, error counters, effective parameters).

## Project map

Four repos, one job each:

| Repo | What it is | It changes when… |
|---|---|---|
| [local-llm-perf-bench](https://github.com/michal-konik-human/local-llm-perf-bench) | **Tool**: how fast a model runs (llama.cpp, any GGUF, 1–n GPUs) | the way speed is measured changes |
| [local-llm-quality-bench](https://github.com/michal-konik-human/local-llm-quality-bench) | **Tool**: how good a model is as an agent/assistant, in Polish and English | cases, scorers or model profiles change |
| [local-llm-bench-results](https://github.com/michal-konik-human/local-llm-bench-results) | **Data**: everything measured on the reference rig, quality next to speed | a benchmark run finishes |
| [radeon-r9700-rocm-notes](https://github.com/michal-konik-human/radeon-r9700-rocm-notes) | **Platform**: making 4× Radeon AI PRO R9700 + ROCm work (setup, traps, monitoring, tuning) | hardware, drivers or the serving stack change, or a new trap is found |

## Leaderboard

<!-- FINDINGS:START -->
**First results, 10 October 2026**, at k = 3 samples per item and vendor-recommended settings:

- **A 3-bit quant can still be the most reliable agent on the box.** DeepSeek-V4-Flash-0731
  (UD-IQ3_XXS, 97 GiB across 4 GPUs) scored **99 in Polish and 98 in English**. Every one of its
  3 attempts succeeded on every tool-calling, agent and shopping task, in both languages (pass^3 = 100).
- **Against gpt-oss-20b, on identical items:**
  - DeepSeek leads by **+7 points overall** (95% CI +2 to +12).
  - The lead comes from **shopping on the frozen web (+19), multi-step agent tasks (+14) and tool calling (+11)**.
  - Writing shows no credible difference (−3, CI −10 to +5). Reasoning and coding are tied at 100: those
    families are too easy at this size.
- **The 20B model is 5.5× faster and needs one GPU.** In these runs gpt-oss-20b decoded at 128 tok/s against 23, and
  answers a task in 2.9 s against 18.3 s at the median. Its reliability is the price: pass^3 is 68 (PL) /
  75 (EN) on tool, agent and shopping tasks.
- **Typical failures differ by model:**
  - gpt-oss-20b invents an e-mail address instead of asking for one, guesses which of two "Tomasz" in IT
    to e-mail, falls for a refurbished phone listed as the cheapest, and once wrote "22 plików"
    (correct Polish: *22 pliki*).
  - DeepSeek leaves placeholders such as `[Your Name]` in "ready-to-send" texts, and twice (out of 3) tweeted in
    English for a Polish prompt.
- **Neither model is worse in Polish:** the paired PL − EN gap is 0 for both (CIs −1 to +2 and −4 to +6).
- **Caveats:** the Polish cases still await native-speaker review, and the judge (4 of 60 tasks) is not yet
  calibrated against human labels. The rest is graded by code.
<!-- FINDINGS:END -->

<!-- TABLE:START -->
| Model | 🇵🇱 Quality | 🇬🇧 Quality | PL − EN | Agent reliability 🇵🇱 / 🇬🇧 | Decode tok/s | Prompt tok/s | GPUs | Runs |
|---|---|---|---|---|---|---|---|---|
| **DeepSeek-V4-Flash-0731** <sub>UD-IQ3_XXS · `recommended`</sub> | 99 <sub>(97–100)</sub> | 98 <sub>(96–100)</sub> | 0 | 100 / 100 | 24.71 | 560 | 4×R9700 (0,1,2,3) | [quality](quality/20261010-deepseek-v4-flash-0731-recommended/report.md) · [speed](perf/20260930-221230/report.md) |
| **gpt-oss-20b** <sub>MXFP4 · `recommended`</sub> | 93 <sub>(88–97)</sub> | 92 <sub>(86–98)</sub> | 0 | 68 / 75 | 149.53 | 5726 | 1×R9700 (0) | [quality](quality/20261010-gpt-oss-20b-recommended/report.md) · [speed](perf/20260930-125802/report.md) |

Quality: 0–100, mean of 7 task families, 95% CI in brackets; agent reliability = pass^k on tool, agent and shopping tasks (the chance that **all** k=3 attempts succeed). Speed: decode `tg128` and prompt `pp512` from the perf bench on the same machine. Per-family scores: [quality/leaderboard.md](quality/leaderboard.md); all speed measurements: [perf/all-benchmark-results.md](perf/all-benchmark-results.md).
<!-- TABLE:END -->

## What's here

```
quality/                    local-llm-quality-bench output ($QBENCH_RESULTS)
  leaderboard.md              every quality run side by side, per family and language, with CIs
  <run-id>/report.md          one run: scores, worst failures, how to replicate
  <run-id>/samples.jsonl      every answer, with the exact request that produced it
  <run-id>/grades.jsonl       every check's score and reason (judge verdicts included)
  <run-id>/manifest.json      model file, server build, chat-template hash, samplers the server used
perf/                       local-llm-perf-bench output ($LLM_PERF_RESULTS)
  all-benchmark-results.md    every speed measurement with its conditions
  <run-id>/report.md          one run: verdict, per-GPU telemetry, hardware/software state
  configs/                    the rig's tuned multi-GPU configs (tensor splits for 2, 3 and 4 cards)
serving/llama-swap.yaml     how the models are served (flags, context, ubatch, chat templates)
hardware.md                 the machine
tools/build_readme.py       rebuilds the table above from quality/ and perf/
```

## How to read it

- **Polish and English are never pooled.** A model that is great in English and weak in Polish shows exactly that.
- **CIs matter.** These are 60 tasks × k=3 samples: enough to separate a good configuration from a bad one, not two
  good ones a few points apart. Overlapping intervals mean "not distinguishable at this size".
- **Reliability ≠ average.** For an assistant you rely on, pass^k (all three attempts succeed) matters more than the mean.
- **Read the transcripts.** Every report lists its worst failures; `samples.jsonl` has the full conversation for each.
- **Settings are the vendor's.** Each run uses the model vendor's recommended sampling (source cited in the
  model profile), served by llama.cpp through llama-swap, quantised as shown.
- **Caveats on the first runs:** the Polish cases still await native-speaker review, and the LLM judge (used for
  4 of 60 tasks) is not yet calibrated against human labels.

## Reproduce a result

1. Check out the tool at the version named in the run's `manifest.json` (`bench.commit`; releases are tagged).
2. Get the same GGUF (`manifest.json → model.profile.weights`) and serve it with the same flags
   (`manifest.json → server.llama_swap.cmd`, or [serving/llama-swap.yaml](serving/llama-swap.yaml)).
3. Run the same model profile and preset, then compare:
   `python3 -m qbench compare runs/<yours> path/to/quality/<run-id>`.

Or replay a single answer: every line of `samples.jsonl` holds the exact request body. See the quality bench's
[docs/REPLICATE.md](https://github.com/michal-konik-human/local-llm-quality-bench/blob/main/docs/REPLICATE.md).

## Run the benches on your own models

Both tools are MIT-licensed and model- and machine-independent. Point `QBENCH_RESULTS` and `LLM_PERF_RESULTS`
at a repo like this one, and you have your own leaderboard. If your numbers on the same weights differ from
mine, please open an issue in the relevant tool repo: that's a finding about the serving stack.

## License

The data (results, transcripts, reports) is **CC BY 4.0**: reuse it, with attribution. The scripts in `tools/` are **MIT**.
See [LICENSE.md](LICENSE.md).

# Results

Measured on the reference rig ([hardware.md](hardware.md)). The tables below are rebuilt by
`tools/build_results.py` from `quality/*/summary.json` and `perf/all-benchmark-results.md`; the findings
are written by hand. How to read them: [README](README.md#how-to-read-the-results).

## Findings

<!-- FINDINGS:START -->
### 2026-10-10: DeepSeek-V4-Flash-0731 vs gpt-oss-20b (quality, k = 3, vendor-recommended settings)

- **A 3-bit quant can still be the most reliable agent on the box.** DeepSeek-V4-Flash-0731
  (UD-IQ3_XXS, 97 GiB across 4 GPUs) scored **99 in Polish and 98 in English**. Every one of its 3 attempts
  succeeded on every tool-calling, agent and shopping task, in both languages (pass^3 = 100).
- **Against gpt-oss-20b, on identical items:**
  - DeepSeek leads by **+7 points overall** (95% CI +2 to +12).
  - The lead comes from **shopping on the frozen web (+19), multi-step agent tasks (+14) and tool calling (+11)**.
  - Writing shows no credible difference (−3, CI −10 to +5). Reasoning and coding are tied at 100: those
    families are too easy at this size.
- **The 20B model is 5.5× faster and needs one GPU.** In these runs gpt-oss-20b decoded at 128 tok/s against 23,
  and answered a task in 2.9 s against 18.3 s at the median. Its reliability is the price: pass^3 is 68 (PL) /
  75 (EN) on tool, agent and shopping tasks.
- **Typical failures differ by model:**
  - gpt-oss-20b invents an e-mail address instead of asking for one, guesses which of two "Tomasz" in IT
    to e-mail, falls for a refurbished phone listed as the cheapest, and once wrote "22 plików"
    (correct Polish: *22 pliki*).
  - DeepSeek leaves placeholders such as `[Your Name]` in "ready-to-send" texts, and twice (out of 3) tweeted in
    English for a Polish prompt.
- **Neither model is worse in Polish:** the paired PL − EN gap is 0 for both (CIs −1 to +2 and −4 to +6).
- **Caveats for these runs:** the Polish cases were still `review: pending-owner` (not yet frozen by a
  native-speaker review), and the LLM judge (4 of 60 tasks) was not yet calibrated against human labels. The
  rest is graded by code.
<!-- FINDINGS:END -->

## Quality next to speed

<!-- TABLE:START -->
| Model | 🇵🇱 Quality | 🇬🇧 Quality | PL − EN | Agent reliability 🇵🇱 / 🇬🇧 | Decode tok/s | Prompt tok/s | GPUs | Runs |
|---|---|---|---|---|---|---|---|---|
| **DeepSeek-V4-Flash-0731** <sub>UD-IQ3_XXS · `recommended`</sub> | 99 <sub>(97–100)</sub> | 98 <sub>(96–100)</sub> | 0 | 100 / 100 | 24.71 | 560 | 4×R9700 (0,1,2,3) | [quality](quality/20261010-deepseek-v4-flash-0731-recommended/report.md) · [speed](perf/20260930-221230/report.md) |
| **gpt-oss-20b** <sub>MXFP4 · `recommended`</sub> | 93 <sub>(88–97)</sub> | 92 <sub>(86–98)</sub> | 0 | 68 / 75 | 149.53 | 5726 | 1×R9700 (0) | [quality](quality/20261010-gpt-oss-20b-recommended/report.md) · [speed](perf/20260930-125802/report.md) |

Quality: 0–100, mean of the task families, 95% CI in brackets; agent reliability = pass^k on tool, agent and shopping tasks (the chance that **all** k attempts succeed). Speed: decode `tg128` and prompt `pp512` from the latest valid perf run of the same model on the same machine. Per-family scores: [quality/leaderboard.md](quality/leaderboard.md); every speed measurement: [perf/all-benchmark-results.md](perf/all-benchmark-results.md).
<!-- TABLE:END -->

## Runs

<!-- RUNS:START -->
### Quality runs

| Date | Model | Preset | k | Judge | Tool commit (as recorded) | Report |
|---|---|---|---|---|---|---|
| 2026-10-10 | gpt-oss-20b | `recommended` | 3 | deepseek-v4-flash-0731 | `1cd95cc030` | [20261010-gpt-oss-20b-recommended](quality/20261010-gpt-oss-20b-recommended/report.md) |
| 2026-10-10 | DeepSeek-V4-Flash-0731 | `recommended` | 3 | gpt-oss-120b | `1cd95cc030` | [20261010-deepseek-v4-flash-0731-recommended](quality/20261010-deepseek-v4-flash-0731-recommended/report.md) |

### Speed runs

| Date | Model | Configs | Report |
|---|---|---|---|
| 2026-09-30 | deepseek-v4-flash-0731 | thermal, throughput | [20260930-221230](perf/20260930-221230/report.md) |
| 2026-09-30 | qwen3-next-80b | throughput | [20260930-125943](perf/20260930-125943/report.md) |
| 2026-09-30 | gpt-oss-20b | throughput | [20260930-125802](perf/20260930-125802/report.md) |
| 2026-09-30 | deepseek-v4-flash | thermal, throughput | [20260930-122320](perf/20260930-122320/report.md) |
| 2026-09-30 | qwen3-235b-a22b-q3 | thermal, throughput | [20260930-121339](perf/20260930-121339/report.md) |
| 2026-09-29 | qwen3-235b-a22b | 3gpu-manual | 20260929-0945 (manual, no run folder) |
| 2026-09-29 | laguna-s-2.1 | 3gpu-manual | 20260929-0930 (manual, no run folder) |
| 2026-09-28 | gpt-oss-120b | 3gpu-manual | 20260928-2300 (manual, no run folder) |
| 2026-09-20 | gpt-oss-20b | 2gpu-manual | 20260920-1540 (manual, no run folder) |
| 2026-09-20 | qwen3-next-80b | 2gpu-manual | 20260920-1525 (manual, no run folder) |
| 2026-09-20 | qwen3-32b | 2gpu-layer | [20260920-134642](perf/20260920-134642/report.md) |
| 2026-09-19 | bielik-11b | thermal, throughput | [20260919-231520](perf/20260919-231520/report.md) |
| 2026-09-19 | qwen3-32b | thermal, throughput | [20260919-225407](perf/20260919-225407/report.md) |
| 2026-09-15 | gpt-oss-20b | throughput | [20260915-164813](perf/20260915-164813/report.md) |
<!-- RUNS:END -->

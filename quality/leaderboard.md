# Leaderboard

Scores 0–100 with 95% CI (cluster bootstrap over tasks). **Overall** is the mean of family scores, so every family weighs the same. **Reliability** is pass^k on tool, agent, shopping and research tasks: the chance that *all k* attempts succeed, which is what an assistant you rely on needs. Configs whose CIs overlap are not distinguishable at this sample size.

Suites are scored separately and never mixed. The **hard suite** (long agentic workflows, multi-hop web research, long documents) is designed so that only frontier models come close to 100.

_Generated 2026-10-11T05:51:49+02:00 from `*/summary.json` by `qbench report --publish`._

# Hard suite

## 🇵🇱 Polish

| # | Model | Quant | Preset | **Overall** | Agent | Research | Long docs | Reliability pass^k | Tokens/answer | Decode tok/s | Run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | DeepSeek-V4-Flash-0731 | UD-IQ3_XXS | `recommended` | **92 (81–99)** | 97 | 94 | 86 | 83 (k=3) | 2724.5 | 22.5 | [20261010-221652-deepseek-v4-flash-0731-recommended-hard](20261010-221652-deepseek-v4-flash-0731-recommended-hard/report.md) |
| 2 | gpt-oss-20b | MXFP4 | `recommended` | **47 (34–61)** | 60 | 30 | 51 | 8 (k=3) | 1985.0 | 121.5 | [20261011-044658-gpt-oss-20b-recommended-hard](20261011-044658-gpt-oss-20b-recommended-hard/report.md) |

## 🇬🇧 English

| # | Model | Quant | Preset | **Overall** | Agent | Research | Long docs | Reliability pass^k | Tokens/answer | Decode tok/s | Run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | DeepSeek-V4-Flash-0731 | UD-IQ3_XXS | `recommended` | **93 (82–100)** | 97 | 94 | 88 | 83 (k=3) | 2724.5 | 22.5 | [20261010-221652-deepseek-v4-flash-0731-recommended-hard](20261010-221652-deepseek-v4-flash-0731-recommended-hard/report.md) |
| 2 | gpt-oss-20b | MXFP4 | `recommended` | **52 (40–66)** | 64 | 35 | 59 | 0 (k=3) | 1985.0 | 121.5 | [20261011-044658-gpt-oss-20b-recommended-hard](20261011-044658-gpt-oss-20b-recommended-hard/report.md) |

## Polish vs English (same tasks, paired)

| Model | Preset | PL − EN (points, 95% CI) | Paired tasks |
|---|---|---|---|
| gpt-oss-20b | `recommended` | −6 (−18 to +5) | 20 |
| DeepSeek-V4-Flash-0731 | `recommended` | −1 (−2 to 0) | 20 |

Judges used: deepseek-v4-flash-0731, gpt-oss-120b. Rubric checks are judged by a model from a *different family* than the candidate. Method: [local-llm-quality-bench METHODOLOGY](https://github.com/michal-koniu/local-llm-quality-bench/blob/main/docs/METHODOLOGY.md).

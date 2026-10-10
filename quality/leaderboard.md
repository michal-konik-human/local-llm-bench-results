# Leaderboard

Scores 0–100 with 95% CI (cluster bootstrap over tasks). **Overall** is the mean of family scores, so every family weighs the same. **Reliability** is pass^k on tool, agent and shopping tasks: the chance that *all k* attempts succeed, which is what an assistant you rely on needs. Configs whose CIs overlap are not distinguishable at this sample size.

_Generated 2026-10-10T19:56:49+02:00 from `results/*/summary.json` by `qbench report --publish`._

## 🇵🇱 Polish

| # | Model | Quant | Preset | **Overall** | Tools | Agent | Shop | Instr. | Writing | Reason. | Code | Reliability pass^k | Tokens/answer | Decode tok/s | Run |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | DeepSeek-V4-Flash-0731 | UD-IQ3_XXS | `recommended` | **99 (97–100)** | 100 | 100 | 100 | 99 | 93 | 100 | 100 | 100 (k=3) | 377 | 23.2 | [20261010-deepseek-v4-flash-0731-recommended](20261010-deepseek-v4-flash-0731-recommended/report.md) |
| 2 | gpt-oss-20b | MXFP4 | `recommended` | **93 (88–97)** | 86 | 85 | 89 | 98 | 92 | 100 | 100 | 68 (k=3) | 339.5 | 127.6 | [20261010-gpt-oss-20b-recommended](20261010-gpt-oss-20b-recommended/report.md) |

## 🇬🇧 English

| # | Model | Quant | Preset | **Overall** | Tools | Agent | Shop | Instr. | Writing | Reason. | Code | Reliability pass^k | Tokens/answer | Decode tok/s | Run |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | DeepSeek-V4-Flash-0731 | UD-IQ3_XXS | `recommended` | **98 (96–100)** | 100 | 100 | 100 | 97 | 91 | 100 | 100 | 100 (k=3) | 377 | 23.2 | [20261010-deepseek-v4-flash-0731-recommended](20261010-deepseek-v4-flash-0731-recommended/report.md) |
| 2 | gpt-oss-20b | MXFP4 | `recommended` | **92 (86–98)** | 92 | 87 | 72 | 94 | 99 | 100 | 100 | 75 (k=3) | 339.5 | 127.6 | [20261010-gpt-oss-20b-recommended](20261010-gpt-oss-20b-recommended/report.md) |

## Polish vs English (same tasks, paired)

| Model | Preset | PL − EN (points, 95% CI) | Paired tasks |
|---|---|---|---|
| DeepSeek-V4-Flash-0731 | `recommended` | 0 (−1 to +2) | 55 |
| gpt-oss-20b | `recommended` | 0 (−4 to +6) | 55 |

Judges used: deepseek-v4-flash-0731, gpt-oss-120b. Rubric checks are judged by a model from a *different family* than the candidate. Method: [local-llm-quality-bench METHODOLOGY](https://github.com/michal-konik-human/local-llm-quality-bench/blob/main/docs/METHODOLOGY.md).

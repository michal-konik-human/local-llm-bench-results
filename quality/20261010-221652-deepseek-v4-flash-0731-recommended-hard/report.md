# Quality run `20261010-221652-deepseek-v4-flash-0731-recommended-hard`: DeepSeek-V4-Flash-0731 / preset `recommended`

**Hard suite**

| | |
|---|---|
| Model | DeepSeek-V4-Flash-0731 (MoE (see model card), UD-IQ3_XXS), family `deepseek`, license MIT |
| Weights | https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731 |
| Server | b265-680a036 |
| Samplers sent | `{"temperature": 1.0, "top_p": 0.95, "top_k": 0, "min_p": 0.0, "repeat_penalty": 1.0, "presence_penalty": 0.0, "frequency_penalty": 0.0}`, max_tokens 8192 |
| Preset source | https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731 : temperature 1.0, top_p 0.95 for agentic scenarios (1.0 otherwise); thinking on by default in the Unsloth GGUF template |
| Samples | k = 3 per item, 120 total; 0 excluded (server/transport errors), 0 ran out of turns, 0 unparseable output (rejected by the server's parser, scored 0), 6 hit max_tokens, 0 pending grades |
| Judge | gpt-oss-120b, **not yet calibrated against human labels** |
| Suite | 20 cases, sha256 `c20e798b94134ee6…`, bench commit `a613e07fdf` |

> 20 of 20 cases are still `review: pending-owner` (written by the bench author, not yet frozen by a native-speaker review).

## Scores (0–100, mean with 95% cluster-bootstrap CI)

| Family | 🇵🇱 PL | 🇬🇧 EN | PL pass^1 | EN pass^1 | PL pass^k | EN pass^k | PL worst@k | EN worst@k |
|---|---|---|---|---|---|---|---|---|
| Agent | 97 (90–100) | 97 (90–100) | 94 | 94 | 83 | 83 | 90 | 90 |
| Research | 94 (83–100) | 94 (83–100) | 94 | 94 | 83 | 83 | 83 | 83 |
| Long docs | 86 (61–100) | 88 (62–100) | 83 | 88 | 75 | 88 | 83 | 88 |
| **Overall** (mean of families) | **92 (81–99)** | **93 (82–100)** | | | | | | |

_pass^1: share of samples that pass every check. pass^k: chance that all k samples of a task pass. worst@k: expected score of the worst of k samples._

**PL − EN gap** on parallel tasks: −1 (−2 to 0) points (20 paired tasks; negative = worse in Polish).

**Cost:** median 2724.5 completion tokens per sample, median decode 22.5 tok/s, median latency 145.63 s per sample.

## Worst failures (read the transcripts before trusting any number)

| Family | Case | Lang | Sample | Score | Why |
|---|---|---|---|---|---|
| Agent | `agent-meeting-room-planning` | en | #2 | 40 | env_state: ok one meeting created: count 1 (want 1); FAIL calendar where {'title': {'regex': 'CRM'}}.start: ['2026-10-16T10:00'] vs {'eq': '2026-10-15T14:00'}; FAIL calend |
| Agent | `agent-meeting-room-planning` | pl | #1 | 40 | env_state: ok one meeting created: count 1 (want 1); FAIL calendar where {'title': {'regex': 'CRM'}}.start: ['2026-10-16T10:00'] vs {'eq': '2026-10-15T14:00'}; FAIL calend |
| Research | `research-relief-current` | en | #1 | 0 | answer: answer line: FAIL contains '2026-07-01'; FAIL contains 'ministerstwo-finansow.example'; FAIL matches /^\D*4[\s., ]?500(?!\d)/ |
| Research | `research-relief-current` | pl | #1 | 0 | answer: answer line: FAIL contains '2026-07-01'; FAIL contains 'ministerstwo-finansow.example'; FAIL matches /^\D*4[\s., ]?500(?!\d)/ |
| Long docs | `long-orders-reconciliation` | en | #0 | 0 | answer: empty reply (ran out of max_tokens while reasoning) |
| Long docs | `long-orders-reconciliation` | en | #1 | 0 | answer: empty reply (ran out of max_tokens while reasoning) |

## Replicate

Every sample in `samples.jsonl` holds the exact request body. To re-run one:

```bash
python3 -m qbench replay 20261010-221652-deepseek-v4-flash-0731-recommended-hard <case-id> <lang> <sample> --base-url http://127.0.0.1:8080/v1
```

Or re-run the whole configuration on your machine:

```bash
python3 -m qbench run --model deepseek-v4-flash-0731 --preset recommended --k 3
python3 -m qbench grade runs/<new-run-id>
python3 -m qbench report runs/<new-run-id>
```

Expect overlapping confidence intervals, not identical tokens: GPU kernels, batch sizes and builds change floating-point results. See docs/REPLICATE.md.

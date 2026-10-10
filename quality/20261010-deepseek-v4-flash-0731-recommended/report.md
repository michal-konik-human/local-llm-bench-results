# Quality run `20261010-deepseek-v4-flash-0731-recommended`: DeepSeek-V4-Flash-0731 / preset `recommended`

| | |
|---|---|
| Model | DeepSeek-V4-Flash-0731 (MoE (see model card), UD-IQ3_XXS), family `deepseek`, license MIT |
| Weights | https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731 |
| Server | b265-680a036 |
| Samplers sent | `{"temperature": 1.0, "top_p": 0.95, "top_k": 0, "min_p": 0.0, "repeat_penalty": 1.0, "presence_penalty": 0.0, "frequency_penalty": 0.0}`, max_tokens 8192 |
| Preset source | https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731 : temperature 1.0, top_p 0.95 for agentic scenarios (1.0 otherwise); thinking on by default in the Unsloth GGUF template |
| Samples | k = 3 per item, 345 total; 0 excluded (server/transport errors), 0 ran out of turns, 0 unparseable output (rejected by the server's parser, scored 0), 0 hit max_tokens, 0 pending grades |
| Judge | gpt-oss-120b, **not yet calibrated against human labels** |
| Suite | 60 cases, sha256 `19b9931b6e79c290…`, bench commit `1cd95cc030` |

> ✏️ Checks revised after generation (prompts unchanged, so the samples stay valid): `agent-contact-disambiguation-by-team`, `agent-find-free-slot`, `agent-policy-no-weekend`, `if-no-placeholders`, `tool-nested-invoice`, `tool-relative-datetime`, `write-apology-email-formal`, `write-feminine-agreement-pl`, `write-plain-language`, `write-polish-formats-pl`, `write-rag-not-in-document`. Graded with bench commit `f09a512738`.

> 60 of 60 cases are still `review: pending-owner` (written by the bench author, not yet frozen by a native-speaker review).

## Scores (0–100, mean with 95% cluster-bootstrap CI)

| Family | 🇵🇱 PL | 🇬🇧 EN | PL pass^1 | EN pass^1 | PL pass^k | EN pass^k | PL worst@k | EN worst@k |
|---|---|---|---|---|---|---|---|---|
| Tools | 100 (100–100) | 100 (100–100) | 100 | 100 | 100 | 100 | 100 | 100 |
| Agent | 100 (100–100) | 100 (100–100) | 100 | 100 | 100 | 100 | 100 | 100 |
| Shop | 100 (100–100) | 100 (100–100) | 100 | 100 | 100 | 100 | 100 | 100 |
| Instr. | 99 (96–100) | 97 (92–100) | 94 | 92 | 92 | 92 | 98 | 97 |
| Writing | 93 (85–99) | 91 (77–99) | 78 | 67 | 56 | 50 | 85 | 87 |
| Reason. | 100 (100–100) | 100 (100–100) | 100 | 100 | 100 | 100 | 100 | 100 |
| Code | 100 (100–100) | 100 (100–100) | 100 | 100 | 100 | 100 | 100 | 100 |
| **Overall** (mean of families) | **99 (97–100)** | **98 (96–100)** | | | | | | |

_pass^1: share of samples that pass every check. pass^k: chance that all k samples of a task pass. worst@k: expected score of the worst of k samples._

**PL − EN gap** on parallel tasks: 0 (−1 to +2) points (55 paired tasks; negative = worse in Polish).

**Cost:** median 377 completion tokens per sample, median decode 23.2 tok/s, median latency 18.3 s per sample.

## Worst failures (read the transcripts before trusting any number)

| Family | Case | Lang | Sample | Score | Why |
|---|---|---|---|---|---|
| Instr. | `if-no-placeholders` | en | #0 | 67 | ifeval: placeholder_absent: FAIL (placeholders: ['[Your Name]']); required_patterns: ok (all present); language: ok (detected en, want en) |
| Instr. | `if-no-placeholders` | en | #1 | 67 | ifeval: placeholder_absent: FAIL (placeholders: ['[Insert Street Address Here]']); required_patterns: ok (all present); language: ok (detected en, want en) |
| Writing | `write-rag-in-document` | pl | #0 | 50 | match: FAIL matches /30 września/ |
| Writing | `write-apology-email-formal` | en | #0 | 54 | ifeval: language: ok (detected en, want en); placeholder_absent: FAIL (placeholders: ['[Your Contact Information]']); rubric: met: ['apology', 'offer', 'tone', 'invented_facts'] |

## Replicate

Every sample in `samples.jsonl` holds the exact request body. To re-run one:

```bash
python3 -m qbench replay 20261010-deepseek-v4-flash-0731-recommended <case-id> <lang> <sample> --base-url http://127.0.0.1:8080/v1
```

Or re-run the whole configuration on your machine:

```bash
python3 -m qbench run --model deepseek-v4-flash-0731 --preset recommended --k 3
python3 -m qbench grade runs/<new-run-id>
python3 -m qbench report runs/<new-run-id>
```

Expect overlapping confidence intervals, not identical tokens: GPU kernels, batch sizes and builds change floating-point results. See docs/REPLICATE.md.

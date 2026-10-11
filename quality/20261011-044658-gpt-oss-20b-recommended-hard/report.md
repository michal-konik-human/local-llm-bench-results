# Quality run `20261011-044658-gpt-oss-20b-recommended-hard`: gpt-oss-20b / preset `recommended`

**Hard suite**

| | |
|---|---|
| Model | gpt-oss-20b (21B total / 3.6B active (MoE), MXFP4), family `gpt-oss`, license Apache-2.0 |
| Weights | https://huggingface.co/openai/gpt-oss-20b |
| Server | b265-680a036 |
| Samplers sent | `{"temperature": 1.0, "top_p": 1.0, "top_k": 0, "min_p": 0.0, "repeat_penalty": 1.0, "presence_penalty": 0.0, "frequency_penalty": 0.0}`, max_tokens 6144, extra `{"chat_template_kwargs": {"reasoning_effort": "medium"}}` |
| Preset source | OpenAI gpt-oss model card: temperature 1.0, top_p 1.0; reasoning effort set in the system/developer message (default medium) |
| Samples | k = 3 per item, 120 total; 0 excluded (server/transport errors), 0 ran out of turns, 0 unparseable output (rejected by the server's parser, scored 0), 4 hit max_tokens, 0 pending grades |
| Judge | deepseek-v4-flash-0731, **not yet calibrated against human labels** |
| Suite | 20 cases, sha256 `c20e798b94134ee6…`, bench commit `a613e07fdf` |

> 20 of 20 cases are still `review: pending-owner` (written by the bench author, not yet frozen by a native-speaker review).

## Scores (0–100, mean with 95% cluster-bootstrap CI)

| Family | 🇵🇱 PL | 🇬🇧 EN | PL pass^1 | EN pass^1 | PL pass^k | EN pass^k | PL worst@k | EN worst@k |
|---|---|---|---|---|---|---|---|---|
| Agent | 60 (44–74) | 64 (50–79) | 0 | 6 | 0 | 0 | 49 | 47 |
| Research | 30 (9–60) | 35 (11–60) | 22 | 22 | 17 | 0 | 17 | 12 |
| Long docs | 51 (24–75) | 59 (34–81) | 25 | 38 | 12 | 12 | 37 | 41 |
| **Overall** (mean of families) | **47 (34–61)** | **52 (40–66)** | | | | | | |

_pass^1: share of samples that pass every check. pass^k: chance that all k samples of a task pass. worst@k: expected score of the worst of k samples._

**PL − EN gap** on parallel tasks: −6 (−18 to +5) points (20 paired tasks; negative = worse in Polish).

**Cost:** median 1985.0 completion tokens per sample, median decode 121.5 tok/s, median latency 21.45 s per sample.

## Worst failures (read the transcripts before trusting any number)

| Family | Case | Lang | Sample | Score | Why |
|---|---|---|---|---|---|
| Agent | `agent-deadline-cascade` | en | #2 | 20 | env_state: ok one requirements to-do (existing one updated): count 1 (want 1); FAIL requirements: 3 weeks after kickoff.due: ['2026-10-19'] vs {'eq': '2026-10-26'}; FAIL t |
| Agent | `agent-business-trip` | en | #0 | 25 | env_state: FAIL exactly the two right trains.id: [['PKP-5104', 'PKP-5201']] vs {'set': ['PKP-5103', 'PKP-5203']}; ok one hotel booking: count 1 (want 1); FAIL bookings whe |
| Research | `research-event-train` | en | #0 | 0 | answer: answer line: FAIL contains 'EIP 3500'; FAIL number 118.3 ± 0.01 |
| Research | `research-event-train` | en | #1 | 0 | answer: answer line: FAIL contains 'EIP 3500'; FAIL number 118.3 ± 0.01 |
| Long docs | `long-contract-penalty` | en | #1 | 0 | answer: answer line: FAIL number 4960.0 ± 0.5 |
| Long docs | `long-contract-penalty` | en | #2 | 0 | answer: answer line: FAIL number 4960.0 ± 0.5 |

## Replicate

Every sample in `samples.jsonl` holds the exact request body. To re-run one:

```bash
python3 -m qbench replay 20261011-044658-gpt-oss-20b-recommended-hard <case-id> <lang> <sample> --base-url http://127.0.0.1:8080/v1
```

Or re-run the whole configuration on your machine:

```bash
python3 -m qbench run --model gpt-oss-20b --preset recommended --k 3
python3 -m qbench grade runs/<new-run-id>
python3 -m qbench report runs/<new-run-id>
```

Expect overlapping confidence intervals, not identical tokens: GPU kernels, batch sizes and builds change floating-point results. See docs/REPLICATE.md.

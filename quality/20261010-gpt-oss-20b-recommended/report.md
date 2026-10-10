# Quality run `20261010-gpt-oss-20b-recommended`: gpt-oss-20b / preset `recommended`

| | |
|---|---|
| Model | gpt-oss-20b (21B total / 3.6B active (MoE), MXFP4), family `gpt-oss`, license Apache-2.0 |
| Weights | https://huggingface.co/openai/gpt-oss-20b |
| Server | b265-680a036 |
| Samplers sent | `{"temperature": 1.0, "top_p": 1.0, "top_k": 0, "min_p": 0.0, "repeat_penalty": 1.0, "presence_penalty": 0.0, "frequency_penalty": 0.0}`, max_tokens 6144, extra `{"chat_template_kwargs": {"reasoning_effort": "medium"}}` |
| Preset source | OpenAI gpt-oss model card: temperature 1.0, top_p 1.0; reasoning effort set in the system/developer message (default medium) |
| Samples | k = 3 per item, 345 total; 0 excluded (server/transport errors), 1 ran out of turns, 1 unparseable output (rejected by the server's parser, scored 0), 0 hit max_tokens, 0 pending grades |
| Judge | deepseek-v4-flash-0731, **not yet calibrated against human labels** |
| Suite | 60 cases, sha256 `19b9931b6e79c290…`, bench commit `1cd95cc030` |

> ✏️ Checks revised after generation (prompts unchanged, so the samples stay valid): `agent-contact-disambiguation-by-team`, `agent-find-free-slot`, `agent-policy-no-weekend`, `if-no-placeholders`, `tool-nested-invoice`, `tool-relative-datetime`, `write-apology-email-formal`, `write-feminine-agreement-pl`, `write-plain-language`, `write-polish-formats-pl`, `write-rag-not-in-document`. Graded with bench commit `f09a512738`.

> 60 of 60 cases are still `review: pending-owner` (written by the bench author, not yet frozen by a native-speaker review).

## Scores (0–100, mean with 95% cluster-bootstrap CI)

| Family | 🇵🇱 PL | 🇬🇧 EN | PL pass^1 | EN pass^1 | PL pass^k | EN pass^k | PL worst@k | EN worst@k |
|---|---|---|---|---|---|---|---|---|
| Tools | 86 (74–95) | 92 (81–100) | 86 | 90 | 64 | 79 | 64 | 82 |
| Agent | 85 (58–100) | 87 (67–100) | 83 | 79 | 75 | 75 | 81 | 85 |
| Shop | 89 (78–100) | 72 (39–100) | 89 | 72 | 67 | 67 | 67 | 67 |
| Instr. | 98 (95–100) | 94 (86–100) | 94 | 89 | 83 | 83 | 94 | 89 |
| Writing | 92 (83–100) | 99 (98–100) | 81 | 94 | 67 | 83 | 82 | 98 |
| Reason. | 100 (100–100) | 100 (100–100) | 100 | 100 | 100 | 100 | 100 | 100 |
| Code | 100 (100–100) | 100 (100–100) | 100 | 100 | 100 | 100 | 100 | 100 |
| **Overall** (mean of families) | **93 (88–97)** | **92 (86–98)** | | | | | | |

_pass^1: share of samples that pass every check. pass^k: chance that all k samples of a task pass. worst@k: expected score of the worst of k samples._

**PL − EN gap** on parallel tasks: 0 (−4 to +6) points (55 paired tasks; negative = worse in Polish).

**Cost:** median 339.5 completion tokens per sample, median decode 127.6 tok/s, median latency 2.9 s per sample.

## Worst failures (read the transcripts before trusting any number)

| Family | Case | Lang | Sample | Score | Why |
|---|---|---|---|---|---|
| Tools | `tool-ambiguous-ask-city` | pl | #2 | 0 | tool_call: called ['get_weather'] but should not call any tool |
| Tools | `tool-missing-arg-ask` | en | #1 | 0 | tool_call: called ['send_email'] but should not call any tool |
| Agent | `agent-ambiguous-contact-ask` | pl | #0 | 0 | env_state: FAIL sent where *: count 1 (want 0); match: FAIL matches /W[óo]jcik/; FAIL matches /Kami[ńn]sk/; FAIL matches /(\?/podaj/potwierdź/proszę o potwierdzenie/daj znać/wskaż)/ |
| Agent | `agent-ambiguous-contact-ask` | pl | #1 | 0 | env_state: FAIL sent where *: count 1 (want 0); match: FAIL matches /W[óo]jcik/; FAIL matches /Kami[ńn]sk/; FAIL matches /(\?/podaj/potwierdź/proszę o potwierdzenie/daj znać/wskaż)/ |
| Shop | `shop-ereader-discount-code` | en | #0 | 0 | answer: answer line: FAIL contains any of ['ebookshop.example/paperwhite-2026']; FAIL number 656.1 ± 0.01 |
| Shop | `shop-ereader-discount-code` | en | #1 | 0 | answer: answer line: FAIL contains any of ['ebookshop.example/paperwhite-2026']; FAIL number 656.1 ± 0.01 |
| Instr. | `if-reply-in-user-language` | en | #0 | 0 | ifeval: language: FAIL (detected pl, want en) |
| Instr. | `if-forbidden-word` | pl | #1 | 67 | ifeval: forbidden_words: FAIL (forbidden present: ['ośnież']); sentence_count: ok (sentences=4 (want 3..4)); language: ok (detected pl, want pl) |
| Writing | `write-numeral-declension-pl` | pl | #2 | 0 | ifeval: required_patterns: FAIL (missing: ['\\b22 pliki\\b']); regex_absent: FAIL (present: ['\\b22 plików\\b']) |
| Writing | `write-plain-language` | pl | #2 | 67 | rubric: met: ['plain', 'action', 'invented_facts'] |

## Replicate

Every sample in `samples.jsonl` holds the exact request body. To re-run one:

```bash
python3 -m qbench replay 20261010-gpt-oss-20b-recommended <case-id> <lang> <sample> --base-url http://127.0.0.1:8080/v1
```

Or re-run the whole configuration on your machine:

```bash
python3 -m qbench run --model gpt-oss-20b --preset recommended --k 3
python3 -m qbench grade runs/<new-run-id>
python3 -m qbench report runs/<new-run-id>
```

Expect overlapping confidence intervals, not identical tokens: GPU kernels, batch sizes and builds change floating-point results. See docs/REPLICATE.md.

# Orchestrator: a small model benchmarks the big ones

The benchmarks on this rig can be driven by a **small local model running on the CPU**, while the
model under test (up to DeepSeek-V4-Flash, 104 GB across all four GPUs) runs on the GPUs. You say
*"Measure deepseek-v4-flash-0731 fully"*, and it runs the speed bench, the quality bench, grading
and publishing, then reports back.

```
┌────────────── CPU, 8 threads ──────────────┐      ┌────────── 4× R9700, 128 GB VRAM ──────────┐
│ gpt-oss-20b (12 GB RAM) ← orchestrator      │      │ model under test, served by llama-swap     │
│   agent.py: allowlisted commands only       │ ───► │ bench-model  (speed)                       │
│   PLAYBOOK.md as system prompt              │      │ qbench run   (quality)                     │
└─────────────────────────────────────────────┘      └────────────────────────────────────────────┘
```

## Which model, and why it can run next to DeepSeek

| Candidate | Fits in RAM next to DeepSeek? | Agent skill (quality bench, k=3) | Verdict |
|---|---|---|---|
| **gpt-oss-20b** MXFP4 | ✅ 12 GB of the ~38 GB free while DeepSeek is loaded | PL / EN: tools 86 / 92, agent 85 / 87, shopping 89 / 72, instructions 98 / 94 ([run](../quality/20261010-gpt-oss-20b-recommended/report.md)) | **use this** |
| Bielik-11B Q8_0 | ✅ 12 GB | not measured yet; needed a patched tool template, overcalls tools | maybe later |
| Qwen3-32B Q4_K_M | ✅ 18 GB, but dense: a few tok/s on CPU | not measured yet | too slow |
| Qwen3-Next-80B Q4_1 | ❌ 47 GB | – | doesn't fit |
| gpt-oss-120b MXFP4 | ❌ 63 GB | – | doesn't fit |

Why the CPU and not a GPU: DeepSeek-V4-Flash leaves only ~1.4 GB free per card, and any second
process on a GPU would also contaminate the speed measurement (the perf bench refuses to run when a
GPU is shared). On the CPU, the orchestrator is invisible to both benches. While it thinks, the model
under test is idle, and while a benchmark runs, the orchestrator is just waiting.

**Measured on the rig:** gpt-oss-20b on 8 CPU threads decodes at **23 tok/s** (as fast as DeepSeek on the
GPUs) and reads prompts at ~98 tok/s. The first turn reads the ~3k-token playbook (~30 s), later turns take
5–60 s, and none of that time overlaps a measurement.

## Setup (once)

```bash
# 1. serve the orchestrator on the CPU, port 8090 (llama-swap keeps 8080)
AGENT_MODEL=~/models/gpt-oss-20b/gpt-oss-20b-MXFP4.gguf AGENT_THREADS=8 \
  ~/Desktop/github_repos/local-llm-perf-bench/agent-server.sh
~/Desktop/github_repos/local-llm-perf-bench/agent-server.sh --status     # must say "mode: CPU"
```

`agent-server.sh` runs `llama-server -ngl 0` with `HIP_VISIBLE_DEVICES` empty, so the GPUs are never touched.

## Use

```bash
cd ~/Desktop/github_repos/local-llm-bench-results
python3 orchestrator/agent.py "Measure deepseek-v4-flash-0731 fully: speed and quality."
python3 orchestrator/agent.py "Which models have no speed result yet?"
python3 orchestrator/agent.py --dry-run "Measure qwen3-32b fully."      # shows the commands, runs nothing
```

Then review what it produced (`git status` in this repo) and commit it yourself. The orchestrator never
commits, pushes or deletes.

## Safety

The model gets three tools: `run_command`, `read_file` and `finish`. `run_command` accepts **only** the
commands in the allowlist at the top of [agent.py](agent.py): `models-status`, `bench-model`, the
llama-swap unload/status calls, `qbench list|validate|review|run|grade|report|compare`, and the RESULTS.md
rebuild. Any shell syntax (`; & | < > $` backticks, newlines) is rejected. `read_file` only reads inside
the three repos. Every prompt, tool call and output is logged to `orchestrator/logs/` (git-ignored).

## Files

| File | What it is |
|---|---|
| [PLAYBOOK.md](PLAYBOOK.md) | The system prompt: procedure, decision tables, prohibitions, report format |
| [agent.py](agent.py) | The tool loop (stdlib only) and the allowlist |
| Perf bench [docs/AGENT-PLAYBOOK.md](https://github.com/michal-konik-human/local-llm-perf-bench/blob/main/docs/AGENT-PLAYBOOK.md) | Generic playbook for speed runs only |
| Quality bench [docs/AGENT-PLAYBOOK.md](https://github.com/michal-konik-human/local-llm-quality-bench/blob/main/docs/AGENT-PLAYBOOK.md) | Generic playbook for quality runs only |

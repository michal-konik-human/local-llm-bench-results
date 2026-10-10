# Results

Measured on the reference rig ([hardware.md](hardware.md)). The tables below are rebuilt by
`tools/build_results.py` from `quality/*/summary.json` and `perf/all-benchmark-results.md`; the findings
are written by hand. How to read them: [README](README.md#how-to-read-the-results).

## Findings

<!-- FINDINGS:START -->
<!-- FINDINGS:END -->

## Quality next to speed

<!-- TABLE:START -->
Speed: decode `tg128` and prompt `pp512` from the latest valid perf run of the same model on the same machine. Per-family scores with CIs: [quality/leaderboard.md](quality/leaderboard.md); every speed measurement: [perf/all-benchmark-results.md](perf/all-benchmark-results.md).
<!-- TABLE:END -->

## Runs

<!-- RUNS:START -->
### Quality runs

| Date | Suite | Model | Preset | k | Judge | Tool commit (as recorded) | Report |
|---|---|---|---|---|---|---|---|

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

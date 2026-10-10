#!/usr/bin/env python3
"""Rebuild the generated part of README.md: one row per model joining QUALITY (local-llm-quality-bench
summaries in quality/*/summary.json) with SPEED (local-llm-perf-bench table perf/all-benchmark-results.md).

Run after publishing new results:  python3 tools/build_readme.py
Only the text between <!-- TABLE:START --> and <!-- TABLE:END --> is replaced.
"""

import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START, END = "<!-- TABLE:START -->", "<!-- TABLE:END -->"


def pct(x):
    return "–" if x is None else f"{round(100 * x)}"


def ci(s):
    if not s or s.get("mean") is None:
        return "–"
    lo, hi = (s.get("ci") or [None, None])
    return pct(s["mean"]) + (f" <sub>({pct(lo)}–{pct(hi)})</sub>" if lo is not None else "")


def signed(x):
    if x is None:
        return "–"
    v = round(100 * x)
    return f"+{v}" if v > 0 else (f"−{-v}" if v < 0 else "0")


def perf_rows():
    """{model: {"tg": (tok/s, run_id, gpus), "pp": (...)}} from the perf table, preferring the latest
    OK `throughput` rows (tg128 / pp512)."""
    path = os.path.join(ROOT, "perf", "all-benchmark-results.md")
    out = {}
    if not os.path.exists(path):
        return out
    header = None
    for line in open(path, encoding="utf-8"):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] == "run_id":
            header = cells
            continue
        if not header or set(line.strip()) <= set("|-: "):
            continue
        row = dict(zip(header, cells))
        test, model = row.get("test", ""), row.get("model", "")
        verdict = row.get("verdict", "")
        if verdict and not verdict.startswith(("✅", "OK", "ok")) and "⚠" not in verdict:
            continue
        try:
            tps = float(row.get("tok/s", "").split()[0])
        except (ValueError, IndexError):
            continue
        key = "tg" if test == "tg128" else "pp" if test == "pp512" else None
        if key:
            out.setdefault(model, {})[key] = (tps, row.get("run_id"), row.get("GPUs", ""))
    return out


def main():
    rows = []
    for p in sorted(glob.glob(os.path.join(ROOT, "quality", "*", "summary.json"))):
        rows.append(json.load(open(p, encoding="utf-8")))
    perf = perf_rows()
    rows.sort(key=lambda r: -((((r["langs"].get("pl") or {}).get("overall")) or {}).get("mean") or 0))
    L = ["", "| Model | 🇵🇱 Quality | 🇬🇧 Quality | PL − EN | Agent reliability 🇵🇱 / 🇬🇧 | Decode tok/s | Prompt tok/s | GPUs | Runs |",
         "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        m = r["model"]
        pl, en = r["langs"].get("pl") or {}, r["langs"].get("en") or {}
        pr = perf.get(m["name"], {})
        tg, pp = pr.get("tg"), pr.get("pp")
        rel = f"{pct((pl.get('reliability') or {}).get('pass_k'))} / {pct((en.get('reliability') or {}).get('pass_k'))}"
        runs = f"[quality](quality/{r['run_id']}/report.md)" + (f" · [speed](perf/{tg[1]}/report.md)" if tg else "")
        L.append(f"| **{m['display']}** <sub>{m.get('quant') or ''} · `{r['preset']['name']}`</sub> | {ci(pl.get('overall'))} | "
                 f"{ci(en.get('overall'))} | {signed((r.get('lang_gap') or {}).get('gap'))} | {rel} | "
                 f"{tg[0] if tg else '–'} | {round(pp[0]) if pp else '–'} | {(tg or pp or ('', '', '–'))[2]} | {runs} |")
    L += ["", "Quality: 0–100, mean of 7 task families, 95% CI in brackets; agent reliability = pass^k on tool, agent "
          "and shopping tasks (the chance that **all** k=3 attempts succeed). Speed: decode `tg128` and prompt "
          "`pp512` from the perf bench on the same machine. Per-family scores: [quality/leaderboard.md](quality/leaderboard.md); "
          "all speed measurements: [perf/all-benchmark-results.md](perf/all-benchmark-results.md).", ""]
    path = os.path.join(ROOT, "README.md")
    text = open(path, encoding="utf-8").read()
    a, b = text.index(START) + len(START), text.index(END)
    open(path, "w", encoding="utf-8").write(text[:a] + "\n".join(L) + text[b:])
    print(f"README table: {len(rows)} quality rows, speed found for {sum(1 for r in rows if r['model']['name'] in perf)}")


if __name__ == "__main__":
    main()

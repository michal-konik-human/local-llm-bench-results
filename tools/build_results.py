#!/usr/bin/env python3
"""Rebuild RESULTS.md: quality (quality/*/summary.json) next to speed (perf/all-benchmark-results.md),
plus the list of runs with their dates. The core and the hard quality suites get separate tables: their
scores are never mixed. The hand-written findings between <!-- FINDINGS:START --> and
<!-- FINDINGS:END --> are kept as they are.

    python3 tools/build_results.py
"""

import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "RESULTS.md")
TEMPLATE = """# Results

Measured on the reference rig ([hardware.md](hardware.md)). The tables below are rebuilt by
`tools/build_results.py` from `quality/*/summary.json` and `perf/all-benchmark-results.md`; the findings
are written by hand. How to read them: [README](README.md#how-to-read-the-results).

## Findings

<!-- FINDINGS:START -->
<!-- FINDINGS:END -->

## Quality next to speed

<!-- TABLE:START -->
<!-- TABLE:END -->

## Runs

<!-- RUNS:START -->
<!-- RUNS:END -->
"""


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


def perf_table():
    """All rows of the perf table as dicts."""
    path = os.path.join(ROOT, "perf", "all-benchmark-results.md")
    rows, header = [], None
    if not os.path.exists(path):
        return rows
    for line in open(path, encoding="utf-8"):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] == "run_id":
            header = cells
        elif header and re.match(r"^\d{8}", cells[0]):  # only run rows (other tables follow in the notes)
            rows.append(dict(zip(header, cells)))
    return rows


def best_speed(prows):
    """{model: {"tg": (tok/s, run_id, gpus), "pp": (...)}}: the latest OK throughput rows (tg128 / pp512)."""
    out = {}
    for row in prows:
        if row.get("verdict", "").strip() not in ("OK", "✅"):
            continue
        key = {"tg128": "tg", "pp512": "pp"}.get(row.get("test"))
        try:
            tps = float(row.get("tok/s", "").split()[0])
        except (ValueError, IndexError):
            continue
        if key:
            out.setdefault(row.get("model"), {})[key] = (tps, row.get("run_id"), row.get("GPUs", ""))
    return out


def judge_cell(s):
    """The judge model, but only when the run actually had LLM-judged (rubric) checks."""
    path = os.path.join(ROOT, "quality", s["run_id"], "grades.jsonl")
    judged = os.path.exists(path) and any(c.get("scorer") == "rubric" for line in open(path, encoding="utf-8")
                                          for c in json.loads(line).get("checks", []))
    return (s.get("judge") or "–") if judged else "none (all code-graded)"


def run_date(run_id):
    m = re.match(r"(\d{4})(\d{2})(\d{2})", run_id or "")
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else "–"


def main():
    text = open(PATH, encoding="utf-8").read() if os.path.exists(PATH) else TEMPLATE
    summaries = [json.load(open(p, encoding="utf-8")) for p in sorted(glob.glob(os.path.join(ROOT, "quality", "*", "summary.json")))]
    manifests = {}
    for s in summaries:
        mp = os.path.join(ROOT, "quality", s["run_id"], "manifest.json")
        manifests[s["run_id"]] = json.load(open(mp, encoding="utf-8")) if os.path.exists(mp) else {}
    prows = perf_table()
    speed = best_speed(prows)

    def suite(s):
        return s.get("suite") or "core"

    def by_pl(rows):
        return sorted(rows, key=lambda r: -((((r["langs"].get("pl") or {}).get("overall")) or {}).get("mean") or 0))

    # one table per suite present (the published runs all use the hard suite); never mixed
    FAMS = {"hard": [("agentic", "Agents"), ("web_research", "Research"), ("long_context", "Long docs")]}
    TITLE = {"hard": "Hard suite", "core": "Core suite", "custom": "Custom case selection"}
    NOTE = {
        "hard": "Hard suite: 20 tasks, each in Polish and English: multi-step agent workflows, multi-hop research on a "
                "frozen web, and analysis of documents of 5k–14k tokens, built so that only frontier models should get "
                "close to 100 ([what is in it](https://github.com/michal-konik-human/local-llm-quality-bench#the-hard-suite)). "
                "Quality: 0–100, mean of the three families, 95% CI in brackets, partial credit per task. Reliability = "
                "pass^k on agent and research tasks (the chance that **all** k attempts succeed).",
        "core": "Core suite: 60 screening tasks. Agent reliability = pass^k on tool, agent and shopping tasks.",
    }

    def fam(r, lang, f):
        return pct((((r["langs"].get(lang) or {}).get("families") or {}).get(f) or {}).get("mean"))

    present = [su for su in ("hard", "core", "custom") if any(suite(s) == su for s in summaries)]
    T = [""]
    for su in present:
        fams = FAMS.get(su, [])
        if len(present) > 1:
            T += [f"### {TITLE[su]}", ""]
        head = (["Model", "🇵🇱 Quality", "🇬🇧 Quality", "PL − EN"] + [f"{lab} 🇵🇱 / 🇬🇧" for _, lab in fams] +
                ["Reliability 🇵🇱 / 🇬🇧", "Decode tok/s", "Prompt tok/s", "GPUs", "Runs"])
        T += ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
        for r in by_pl([s for s in summaries if suite(s) == su]):
            m = r["model"]
            pl, en = r["langs"].get("pl") or {}, r["langs"].get("en") or {}
            sp = speed.get(m["name"], {})
            tg, pp = sp.get("tg"), sp.get("pp")
            rel = f"{pct((pl.get('reliability') or {}).get('pass_k'))} / {pct((en.get('reliability') or {}).get('pass_k'))}"
            runs = f"[quality](quality/{r['run_id']}/report.md)" + (f" · [speed](perf/{tg[1]}/report.md)" if tg else "")
            cells = ([f"**{m['display']}** <sub>{m.get('quant') or ''} · `{r['preset']['name']}` · k={r['k']}</sub>",
                      ci(pl.get("overall")), ci(en.get("overall")), signed((r.get("lang_gap") or {}).get("gap"))] +
                     [f"{fam(r, 'pl', f)} / {fam(r, 'en', f)}" for f, _ in fams] +
                     [rel, f"{tg[0] if tg else '–'}", f"{round(pp[0]) if pp else '–'}", (tg or pp or ("", "", "–"))[2], runs])
            T.append("| " + " | ".join(cells) + " |")
        T += ["", NOTE.get(su, ""), ""]
    T += ["Speed: decode `tg128` and prompt `pp512` from the latest valid perf run of the same model on the same machine. "
          "Per-family scores with CIs: [quality/leaderboard.md](quality/leaderboard.md); every speed measurement: "
          "[perf/all-benchmark-results.md](perf/all-benchmark-results.md).", ""]

    R = ["", "### Quality runs", "", "| Date | Suite | Model | Preset | k | Judge | Tool commit (as recorded) | Report |",
         "|---|---|---|---|---|---|---|---|"]
    for s in sorted(summaries, key=lambda s: s["run_id"], reverse=True):
        man = manifests.get(s["run_id"], {})
        date = (man.get("started_at") or "")[:10] or run_date(s["run_id"])
        commit = ((man.get("bench") or {}).get("commit") or "")[:10]
        R.append(f"| {date} | {suite(s)} | {s['model']['display']} | `{s['preset']['name']}` | {s['k']} | {judge_cell(s)} | "
                 f"`{commit}` | [{s['run_id']}](quality/{s['run_id']}/report.md) |")
    R += ["", "### Speed runs", "", "| Date | Model | Configs | Report |", "|---|---|---|---|"]
    seen = {}
    for row in prows:
        rid, model = row.get("run_id", ""), row.get("model", "")
        seen.setdefault((rid, model), set()).add(row.get("config", ""))
    for (rid, model), cfgs in sorted(seen.items(), reverse=True):
        has_dir = os.path.isdir(os.path.join(ROOT, "perf", rid))
        link = f"[{rid}](perf/{rid}/report.md)" if has_dir else f"{rid} (manual, no run folder)"
        R.append(f"| {run_date(rid)} | {model} | {', '.join(sorted(c for c in cfgs if c))} | {link} |")
    R.append("")

    def put(text, name, body):
        a, b = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
        i, j = text.index(a) + len(a), text.index(b)
        return text[:i] + "\n".join(body) + text[j:]

    text = put(text, "TABLE", T)
    text = put(text, "RUNS", R)
    open(PATH, "w", encoding="utf-8").write(text)
    print(f"RESULTS.md: {len(summaries)} quality runs, {len(seen)} speed runs, speed joined for "
          f"{sum(1 for s in summaries if s['model']['name'] in speed)} models")


if __name__ == "__main__":
    main()

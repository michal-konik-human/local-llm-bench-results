#!/usr/bin/env python3
"""A small local model drives the benchmarks of big local models.

The orchestrator model (gpt-oss-20b on the CPU on the reference rig) gets exactly three tools:
  run_command(command)   one command from an ALLOWLIST (benches, status, unload); no shell syntax
  read_file(path)        read a file inside the bench/results repos (reports, tables)
  finish(report)         end the session with a report for the human
It cannot edit files, run git, kill processes or touch the GPUs except through the benches,
which enforce their own checks (exclusive GPUs, cool cards, error counters).

  python3 orchestrator/agent.py "Measure deepseek-v4-flash-0731 fully: speed and quality."
  python3 orchestrator/agent.py --dry-run "..."       # validate commands but do not execute them

Every session is logged to orchestrator/logs/<timestamp>.jsonl (prompts, tool calls, outputs).
Stdlib only.
"""

import argparse
import datetime as dt
import json
import os
import re
import shlex
import subprocess
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HOME = os.path.expanduser("~")
REPOS = os.path.join(HOME, "Desktop", "github_repos")
QBENCH = os.path.join(REPOS, "local-llm-quality-bench")
RESULTS = ROOT
READ_ROOTS = [os.path.join(REPOS, d) for d in ("local-llm-perf-bench", "local-llm-quality-bench", "local-llm-bench-results")]

NAME = r"[A-Za-z0-9][A-Za-z0-9._-]{0,80}"
# (pattern, how to execute it). Patterns are full matches on the command as the model wrote it.
ALLOW = [
    (rf"models-status( --short| --json)?", None),
    (rf"bench-model --list-new", None),
    (rf"bench-model {NAME}( --gpus [1-4])?", None),
    (rf"curl -s -X POST http://127\.0\.0\.1:8080/api/models/unload", None),
    (rf"curl -s http://127\.0\.0\.1:8080/running", None),
    (rf"qbench (list|validate|review)", "qbench"),
    (rf"qbench grade {NAME}( --no-judge)?", "qbench"),
    (rf"qbench report {NAME}( {NAME})*( --publish)?", "qbench"),
    (rf"qbench compare {NAME} {NAME}", "qbench"),
    (r"build-results-readme", "readme"),
]
FORBIDDEN_CHARS = set(";&|<>`$\\\n\r")
RUN_OPTS = {"--model": NAME, "--preset": NAME, "--k": r"[1-9]", "--run-id": NAME,
            "--family": r"[a-z_]+", "--case": NAME, "--lang": r"pl|en"}
REPEATABLE = {"--family", "--case"}


def qbench_run_ok(cmd):
    """`qbench run` with options in ANY order; --model required; only --family/--case may repeat."""
    parts = cmd.split()
    if parts[:2] != ["qbench", "run"] or len(parts) % 2:
        return False
    seen = []
    for opt, val in zip(parts[2::2], parts[3::2]):
        if opt not in RUN_OPTS or not re.fullmatch(RUN_OPTS[opt], val) or (opt in seen and opt not in REPEATABLE):
            return False
        seen.append(opt)
    return "--model" in seen


def check_command(cmd):
    """-> (ok, reason, argv-for-bash)."""
    cmd = " ".join(cmd.strip().split())
    cmd = re.sub(r"^python3 (-u )?-m qbench ", "qbench ", cmd)  # accept the long form too
    if not cmd or FORBIDDEN_CHARS & set(cmd):
        return False, "shell syntax is not allowed (no ; & | < > ` $ or newlines)", None
    if qbench_run_ok(cmd):
        return True, "ok", f"cd {shlex.quote(QBENCH)} && python3 -u -m {cmd}"
    for pat, kind in ALLOW:
        if re.fullmatch(pat, cmd):
            if kind == "qbench":
                return True, "ok", f"cd {shlex.quote(QBENCH)} && python3 -u -m {cmd}"
            if kind == "readme":
                return True, "ok", f"cd {shlex.quote(RESULTS)} && python3 tools/build_readme.py"
            return True, "ok", cmd
    return False, ("command not in the allowlist. Allowed: models-status, bench-model --list-new | <model>, "
                   "the llama-swap unload/running curl, qbench list|validate|review|run|grade|report|compare, "
                   "build-results-readme"), None


def run_command(cmd, dry_run=False, timeout=8 * 3600, log=print):
    ok, reason, bash = check_command(cmd)
    if not ok:
        return {"ok": False, "error": reason}
    if dry_run:
        return {"ok": True, "dry_run": True, "would_run": bash}
    log(f"  $ {cmd}")
    t0 = time.time()
    try:
        p = subprocess.run(["bash", "-lc", bash], capture_output=True, text=True, timeout=timeout,
                           stdin=subprocess.DEVNULL)
        out = (p.stdout or "") + (("\n[stderr]\n" + p.stderr) if p.stderr.strip() else "")
        rc = p.returncode
    except subprocess.TimeoutExpired:
        out, rc = f"timed out after {timeout} s", -1
    # Long outputs: keep the head (context) and the tail (verdicts, run dirs).
    if len(out) > 6000:
        out = out[:1500] + f"\n... [{len(out) - 4500} characters omitted] ...\n" + out[-3000:]
    return {"ok": rc == 0, "exit_code": rc, "seconds": round(time.time() - t0), "output": out}


def read_file(path):
    p = os.path.realpath(os.path.expanduser(path))
    if not any(p.startswith(os.path.realpath(r) + os.sep) for r in READ_ROOTS):
        return {"ok": False, "error": "only files inside the three bench/results repos can be read"}
    if not os.path.isfile(p):
        return {"ok": False, "error": "no such file"}
    text = open(p, encoding="utf-8", errors="replace").read()
    return {"ok": True, "path": p.replace(HOME, "~"), "content": text[:12000],
            "truncated": len(text) > 12000}


TOOLS = [
    {"type": "function", "function": {"name": "run_command", "description":
        "Run ONE allowlisted command on the benchmark machine and get its output (the long benchmark "
        "commands can take hours; wait for them). No shell syntax.",
        "parameters": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}}},
    {"type": "function", "function": {"name": "read_file", "description":
        "Read a text file inside the perf bench, quality bench or results repos (e.g. a report.md).",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
    {"type": "function", "function": {"name": "finish", "description":
        "End the session with the final report for the human, in the format the playbook asks for.",
        "parameters": {"type": "object", "properties": {"report": {"type": "string"}}, "required": ["report"]}}},
]


def chat(base_url, body, timeout=3600):
    req = urllib.request.Request(base_url.rstrip("/") + "/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("task", help="what to do, in plain words (Polish or English)")
    ap.add_argument("--base-url", default=os.environ.get("ORCH_BASE_URL", "http://127.0.0.1:8090/v1"))
    ap.add_argument("--model", default=os.environ.get("ORCH_MODEL", "orchestrator"))
    ap.add_argument("--playbook", default=os.path.join(HERE, "PLAYBOOK.md"))
    ap.add_argument("--max-steps", type=int, default=40)
    ap.add_argument("--reasoning", default="medium", choices=["low", "medium", "high"],
                    help="gpt-oss reasoning effort (ignored by models without the setting)")
    ap.add_argument("--dry-run", action="store_true", help="validate commands, never execute them")
    a = ap.parse_args()

    os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
    log_path = os.path.join(HERE, "logs", dt.datetime.now().strftime("%Y%m%d-%H%M%S") + ".jsonl")

    def log_event(kind, **kw):
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"t": dt.datetime.now().isoformat(timespec="seconds"), "kind": kind, **kw},
                               ensure_ascii=False).replace(HOME, "~") + "\n")

    messages = [{"role": "system", "content": open(a.playbook, encoding="utf-8").read()},
                {"role": "user", "content": a.task}]
    log_event("start", task=a.task, base_url=a.base_url, dry_run=a.dry_run)
    print(f"orchestrator -> {a.base_url}  (log: {log_path})")
    for step in range(a.max_steps):
        body = {"model": a.model, "messages": messages, "tools": TOOLS, "tool_choice": "auto",
                "temperature": 1.0, "top_p": 1.0, "top_k": 0, "min_p": 0.0, "max_tokens": 4096,
                "seed": 1000 + step, "chat_template_kwargs": {"reasoning_effort": a.reasoning}}
        t0 = time.time()
        resp = chat(a.base_url, body)
        msg = (resp.get("choices") or [{}])[0].get("message") or {}
        calls = msg.get("tool_calls") or []
        log_event("model", step=step, seconds=round(time.time() - t0, 1), content=msg.get("content"),
                  reasoning=msg.get("reasoning_content"), tool_calls=calls, usage=resp.get("usage"))
        out_msg = {"role": "assistant", "content": msg.get("content") or "", "tool_calls": calls} if calls else \
            {"role": "assistant", "content": msg.get("content") or ""}
        if msg.get("reasoning_content"):
            out_msg["reasoning_content"] = msg["reasoning_content"]
        messages.append(out_msg)
        if not calls:
            text = (msg.get("content") or "").strip()
            if text:  # a reply without a tool call is the final answer (standard agent-loop convention)
                log_event("finish", report=text, via="text reply")
                print("\n" + text)
                return 0
            # empty reply: nudge once towards the TASK (never "the playbook": that reads as "do everything")
            messages.append({"role": "user", "content": "Reply with your report for the task above, or call the next "
                                                        "tool the task needs. Do nothing the task did not ask for."})
            continue
        for tc in calls:
            fn = tc.get("function") or {}
            try:
                args = json.loads(fn.get("arguments") or "{}")
            except ValueError:
                args = {}
            name = fn.get("name")
            if name == "finish":
                report = args.get("report", "")
                log_event("finish", report=report)
                print("\n" + report)
                return 0
            if name == "run_command":
                result = run_command(str(args.get("command", "")), dry_run=a.dry_run)
            elif name == "read_file":
                result = read_file(str(args.get("path", "")))
            else:
                result = {"ok": False, "error": f"unknown tool {name}"}
            log_event("tool", name=name, args=args, result=result)
            if name == "run_command":
                print(f"  -> {'ok' if result.get('ok') else 'FAILED'} {result.get('error', '')}"
                      f"{' (' + str(result.get('seconds')) + ' s)' if 'seconds' in result else ''}")
            messages.append({"role": "tool", "tool_call_id": tc.get("id") or f"call_{step}",
                             "content": json.dumps(result, ensure_ascii=False)})
    log_event("stop", reason="max steps reached")
    print(f"stopped after {a.max_steps} steps without finish()")
    return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Benchmark CLI commands and manage index.html table."""

import argparse
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from html import escape
from pathlib import Path

INDEX_HTML = Path(__file__).parent / "index.html"


def log(msg: str) -> None:
    print(f"[work] {msg}", file=sys.stderr, flush=True)


def build_row(
    *,
    row_id: str,
    command: str,
    library: str,
    cold_ms: int,
    warm_ms: int,
    version: str,
    version_url: str,
    run_url: str,
    last_updated: str,
) -> str:
    cold_css = "ok" if cold_ms < 200 else "slow"
    warm_css = "ok" if warm_ms < 200 else "slow"
    return (
        f'<tr id="{row_id}">'
        f"<td>{escape(library)}</td>"
        f'<td class="hide-mobile command-col"><code>{escape(command)}</code></td>'
        f'<td class="{cold_css}"><a href="{run_url}">{cold_ms}ms</a></td>'
        f'<td class="{warm_css}"><a href="{run_url}">{warm_ms}ms</a></td>'
        f'<td><a href="{version_url}">{escape(version)}</a></td>'
        f"<td>{escape(last_updated)}</td>"
        f"</tr>"
    )


def update_row(html: str, row_id: str, new_row: str) -> str:
    pattern = rf'<tr id="{re.escape(row_id)}"[^>]*>.*?</tr>'
    assert (m := re.search(pattern, html, re.DOTALL)), f"Row '{row_id}' not found"
    return html[: m.start()] + new_row + html[m.end() :]


def git(cmd: str, check: bool = True) -> int:
    log(f"$ git {cmd}")
    return subprocess.run(f"git {cmd}", shell=True, check=check).returncode


def git_commit_and_push(message: str) -> None:
    git("config user.name 'github-actions[bot]'")
    git("config user.email 'github-actions[bot]@users.noreply.github.com'")
    git("add index.html")

    if git("diff --staged --quiet", check=False) == 0:
        log("No changes to commit")
        return

    git(f"commit -m '{message}'")

    for attempt in range(5):
        log(f"Push attempt {attempt + 1}/5")
        git("pull --rebase")
        if git("push", check=False) == 0:
            return
        time.sleep(1 << attempt)

    sys.exit("All push attempts failed!")


def bench(command: str, runs: int = 11) -> tuple[int, int]:
    """Run command multiple times and return (cold_ms, warm_ms)."""
    log(f"Benchmark: {command} ({runs} runs)")
    times: list[int] = []
    for i in range(runs):
        start = time.perf_counter_ns()
        subprocess.run(command, shell=True, capture_output=True)
        ms = (time.perf_counter_ns() - start) // 1_000_000
        times.append(ms)
        log(f"  Run {i + 1}/{runs}: {ms}ms")

    cold_ms = times[0]
    warm_ms = sum(times[1:]) // (len(times) - 1)
    log(f"Cold: {cold_ms}ms, Warm: {warm_ms}ms")
    return cold_ms, warm_ms


def cmd_bench(args: argparse.Namespace) -> None:
    library = args.library or args.id
    log(f"=== {args.id}: {args.command} ===")

    cold_ms, warm_ms = bench(args.command)

    run_url = f"{os.getenv('GITHUB_SERVER_URL', 'https://github.com')}/{os.getenv('GITHUB_REPOSITORY')}/actions/runs/{os.getenv('GITHUB_RUN_ID')}"
    last_updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    new_row = build_row(
        row_id=args.id,
        command=args.command,
        library=library,
        cold_ms=cold_ms,
        warm_ms=warm_ms,
        version=args.version,
        version_url=args.version_url,
        run_url=run_url,
        last_updated=last_updated,
    )
    INDEX_HTML.write_text(update_row(INDEX_HTML.read_text(), args.id, new_row))
    sort_table()

    git_commit_and_push(f"{args.id}: {cold_ms}ms/{warm_ms}ms @ {args.version}")


def sort_table() -> None:
    """Sort table rows by warm time (descending)."""
    html = INDEX_HTML.read_text()
    assert (tbody := re.search(r"(<tbody>)(.*?)(</tbody>)", html, re.DOTALL)), (
        "No tbody"
    )
    rows = re.findall(r"<tr id=[^>]+>.*?</tr>", tbody.group(2), re.DOTALL)
    assert rows, "No rows"

    def get_warm_time(row: str) -> int:
        # Find all time values, return the second one (warm time)
        times = re.findall(r">(\d+)ms<", row)
        return int(times[1]) if len(times) >= 2 else 0

    rows.sort(key=get_warm_time, reverse=True)
    new_tbody = (
        tbody.group(1) + "\n    " + "\n    ".join(rows) + "\n    " + tbody.group(3)
    )
    INDEX_HTML.write_text(html[: tbody.start()] + new_tbody + html[tbody.end() :])
    log("Sorted table by warm time")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("command")
    p.add_argument("--id", required=True)
    p.add_argument("--version", required=True)
    p.add_argument("--version-url", required=True)
    p.add_argument("--library")
    cmd_bench(p.parse_args())


if __name__ == "__main__":
    main()

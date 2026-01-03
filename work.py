#!/usr/bin/env python3
"""Benchmark CLI commands and manage index.html table."""

import argparse
import os
import re
import subprocess
import sys
import time
from html import escape
from pathlib import Path

INDEX_HTML = Path(__file__).parent / "index.html"


def log(msg: str) -> None:
    print(f"[work] {msg}", file=sys.stderr, flush=True)


def build_row(*, row_id: str, command: str, library: str, time_ms: int,
              version: str, version_url: str, run_url: str) -> str:
    css = "ok" if time_ms < 200 else "slow"
    return (
        f'<tr id="{row_id}">'
        f'<td>{escape(library)}</td>'
        f'<td class="hide-mobile command-col"><code>{escape(command)}</code></td>'
        f'<td class="{css}"><a href="{run_url}">{time_ms}ms</a></td>'
        f'<td><a href="{version_url}">{escape(version)}</a></td>'
        f'</tr>'
    )


def update_row(html: str, row_id: str, new_row: str) -> str:
    pattern = rf'<tr id="{re.escape(row_id)}"[^>]*>.*?</tr>'
    assert (m := re.search(pattern, html, re.DOTALL)), f"Row '{row_id}' not found"
    return html[:m.start()] + new_row + html[m.end():]


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


def cmd_bench(args: argparse.Namespace) -> None:
    library = args.library or args.id
    log(f"=== {args.id}: {args.command} ===")

    start = time.time_ns()
    result = subprocess.run(args.command, shell=True, capture_output=True)
    time_ms = (time.time_ns() - start) // 1_000_000

    log(f"exit={result.returncode} time={time_ms}ms")
    assert time_ms > 0, "0ms benchmark - command failed immediately"

    run_url = f"{os.getenv('GITHUB_SERVER_URL', 'https://github.com')}/{os.getenv('GITHUB_REPOSITORY')}/actions/runs/{os.getenv('GITHUB_RUN_ID')}"

    new_row = build_row(
        row_id=args.id, command=args.command, library=library, time_ms=time_ms,
        version=args.version, version_url=args.version_url, run_url=run_url,
    )
    INDEX_HTML.write_text(update_row(INDEX_HTML.read_text(), args.id, new_row))

    git_commit_and_push(f"{args.id}: {time_ms}ms @ {args.version}")
    print(f"{args.command}: {time_ms}ms")


def cmd_sort(args: argparse.Namespace) -> None:
    html = INDEX_HTML.read_text()
    assert (tbody := re.search(r"(<tbody>)(.*?)(</tbody>)", html, re.DOTALL)), "No tbody"
    rows = re.findall(r"<tr id=[^>]+>.*?</tr>", tbody.group(2), re.DOTALL)
    assert rows, "No rows"

    def get_time(row: str) -> int:
        return int(m.group(1)) if (m := re.search(r">(\d+)ms<", row)) else 0

    rows.sort(key=get_time, reverse=True)
    new_tbody = tbody.group(1) + "\n    " + "\n    ".join(rows) + "\n    " + tbody.group(3)
    INDEX_HTML.write_text(html[:tbody.start()] + new_tbody + html[tbody.end():])

    git_commit_and_push("Sort table by time")
    print("Sorted table by time (descending)")


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(required=True)

    bench = sub.add_parser("bench")
    bench.add_argument("command")
    bench.add_argument("--id", required=True)
    bench.add_argument("--version", required=True)
    bench.add_argument("--version-url", required=True)
    bench.add_argument("--library")
    bench.set_defaults(func=cmd_bench)

    sort = sub.add_parser("sort-html-table")
    sort.set_defaults(func=cmd_sort)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()


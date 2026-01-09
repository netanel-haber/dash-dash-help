#!/usr/bin/env python3
"""Benchmark CLI commands and manage index.html table."""

import argparse
import csv
import os
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, fields
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
INDEX_HTML = ROOT / "index.html"
MEASUREMENTS_CSV = ROOT / "measurements.csv"


def log(msg: str) -> None:
    print(f"[work] {msg}", file=sys.stderr, flush=True)


@dataclass(frozen=True, kw_only=True)
class Measurement:
    library: str
    version: str
    version_url: str
    cold_ms: int
    warm_ms: int
    run_url: str
    last_updated: str


def read_measurements() -> list[Measurement]:
    assert MEASUREMENTS_CSV.is_file()
    with open(MEASUREMENTS_CSV) as f:
        return [Measurement(**row) for row in csv.DictReader(f)]


def write_measurements(measurements: list[Measurement]) -> None:
    fieldnames = [f.name for f in fields(Measurement)]
    with open(MEASUREMENTS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(asdict(m) for m in measurements)
    log(f"Wrote {len(measurements)} measurements")


def upsert_measurement(m: Measurement) -> None:
    measurements = read_measurements()
    idx = next((i for i, x in enumerate(measurements) if x.library == m.library), None)
    if idx is not None:
        measurements[idx] = m
    else:
        measurements.append(m)
    log(f"{'Updated' if idx is not None else 'Added'} {m.library}")
    write_measurements(measurements)


def rebuild_html() -> None:
    measurements = sorted(
        read_measurements(), key=lambda m: int(m.warm_ms), reverse=True
    )

    def css(ms):
        return "ok" if ms < 200 else "slow"

    rows = []
    for m in measurements:
        rows.append(
            f'<tr id="{m.library}"><td><code>{m.library} --help</code></td>'
            f'<td class="{css(m.cold_ms)}"><a href="{m.run_url}">{m.cold_ms}ms</a></td>'
            f'<td class="{css(m.warm_ms)}"><a href="{m.run_url}">{m.warm_ms}ms</a></td>'
            f'<td><a href="{m.version_url}">{escape(m.version)}</a></td>'
            f"<td>{escape(m.last_updated)}</td></tr>"
        )
    html = re.sub(
        r"(<tbody>).*?(</tbody>)",
        rf"\1\n    {'\n    '.join(rows)}\n    \2",
        INDEX_HTML.read_text(),
        flags=re.DOTALL,
    )
    INDEX_HTML.write_text(html)
    log(f"Rebuilt HTML with {len(measurements)} rows")


def git(cmd: str, check: bool = True) -> int:
    log(f"$ git {cmd}")
    return subprocess.run(f"git {cmd}", shell=True, check=check).returncode


def git_commit_and_push(message: str) -> None:
    git("config user.name 'github-actions[bot]'")
    git("config user.email 'github-actions[bot]@users.noreply.github.com'")
    git("add measurements.csv index.html")

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
    log(f"{cold_ms=}, {warm_ms=}")
    return cold_ms, warm_ms


def cmd_bench(args: argparse.Namespace) -> None:
    log(f"=== {args.library}: {args.command} ===")
    cold_ms, warm_ms = bench(args.command)

    if args.dry_run:
        return log("DRY RUN: Skipping update")

    kw = {k: v for k, v in vars(args).items() if k not in ("dry_run", "command")}
    m = Measurement(
        **kw,
        cold_ms=cold_ms,
        warm_ms=warm_ms,
        run_url=f"{os.getenv('GITHUB_SERVER_URL', 'https://github.com')}/{os.getenv('GITHUB_REPOSITORY')}/actions/runs/{os.getenv('GITHUB_RUN_ID')}",
        last_updated=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
    )

    upsert_measurement(m)
    rebuild_html()

    git_commit_and_push(f"{m.library}: {cold_ms=}/{warm_ms=} @ {m.version}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("command")
    p.add_argument("--library", required=True)
    p.add_argument("--version", required=True)
    p.add_argument("--version-url", required=True)
    p.add_argument("--dry-run", action="store_true")
    cmd_bench(p.parse_args())


if __name__ == "__main__":
    main()

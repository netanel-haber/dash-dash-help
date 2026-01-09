#!/usr/bin/env python3
"""Benchmark CLI commands and manage index.html table."""

import argparse
import csv
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from html import escape
from pathlib import Path

INDEX_HTML = Path(__file__).parent / "index.html"
MEASUREMENTS_CSV = Path(__file__).parent / "measurements.csv"
FIELDS = ["id", "library", "command", "cold_ms", "warm_ms", "version", "version_url", "run_url", "last_updated"]


def log(msg: str) -> None:
    print(f"[work] {msg}", file=sys.stderr, flush=True)


def build_row(m: dict) -> str:
    cold_ms = int(m["cold_ms"])
    warm_ms = int(m["warm_ms"])
    cold_css = "ok" if cold_ms < 200 else "slow"
    warm_css = "ok" if warm_ms < 200 else "slow"
    return (
        f'<tr id="{m["id"]}">'
        f"<td>{escape(m['library'])}</td>"
        f'<td class="hide-mobile command-col"><code>{escape(m["command"])}</code></td>'
        f'<td class="{cold_css}"><a href="{m["run_url"]}">{cold_ms}ms</a></td>'
        f'<td class="{warm_css}"><a href="{m["run_url"]}">{warm_ms}ms</a></td>'
        f'<td><a href="{m["version_url"]}">{escape(m["version"])}</a></td>'
        f"<td>{escape(m['last_updated'])}</td>"
        f"</tr>"
    )


def read_measurements() -> list[dict]:
    """Read all measurements from CSV."""
    if not MEASUREMENTS_CSV.exists():
        return []

    with open(MEASUREMENTS_CSV, "r", newline="") as f:
        return list(csv.DictReader(f))


def write_measurements(measurements: list[dict]) -> None:
    """Write all measurements to CSV."""
    if not measurements:
        return

    with open(MEASUREMENTS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(measurements)
    log(f"Wrote {len(measurements)} measurements to {MEASUREMENTS_CSV}")


def upsert_measurement(measurement: dict) -> None:
    """Upsert measurement to CSV."""
    measurements = read_measurements()

    # Update existing or append new
    row_id = measurement["id"]
    found = False
    for i, m in enumerate(measurements):
        if m["id"] == row_id:
            measurements[i] = measurement
            found = True
            log(f"Updated measurement for {row_id}")
            break

    if not found:
        measurements.append(measurement)
        log(f"Added new measurement for {row_id}")

    write_measurements(measurements)


def rebuild_html() -> None:
    """Rebuild index.html from measurements.csv."""
    measurements = read_measurements()

    # Sort by warm time (descending)
    measurements.sort(key=lambda m: int(m["warm_ms"]), reverse=True)

    # Build table rows
    rows = [build_row(m) for m in measurements]

    # Read current HTML
    html = INDEX_HTML.read_text()

    # Replace tbody content
    tbody_pattern = r"(<tbody>).*?(</tbody>)"
    tbody_match = re.search(tbody_pattern, html, re.DOTALL)
    assert tbody_match, "No tbody found in index.html"

    new_tbody = tbody_match.group(1) + "\n    " + "\n    ".join(rows) + "\n    " + tbody_match.group(2)
    new_html = html[:tbody_match.start()] + new_tbody + html[tbody_match.end():]

    INDEX_HTML.write_text(new_html)
    log(f"Rebuilt index.html from {len(measurements)} measurements")


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

    if args.dry_run:
        log(f"DRY RUN: {args.id} - Cold: {cold_ms}ms, Warm: {warm_ms}ms")
        log("Skipping CSV/HTML update and commit")
        return

    run_url = f"{os.getenv('GITHUB_SERVER_URL', 'https://github.com')}/{os.getenv('GITHUB_REPOSITORY')}/actions/runs/{os.getenv('GITHUB_RUN_ID')}"
    last_updated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")

    # Upsert measurement to CSV
    measurement = dict(zip(FIELDS, [
        args.id, library, args.command, str(cold_ms), str(warm_ms),
        args.version, args.version_url, run_url, last_updated
    ]))
    upsert_measurement(measurement)

    # Rebuild entire HTML from CSV
    rebuild_html()

    git_commit_and_push(f"{args.id}: {cold_ms}ms/{warm_ms}ms @ {args.version}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("command")
    p.add_argument("--id", required=True)
    p.add_argument("--version", required=True)
    p.add_argument("--version-url", required=True)
    p.add_argument("--library")
    p.add_argument("--dry-run", action="store_true", help="Run benchmark without updating HTML or committing")
    cmd_bench(p.parse_args())


if __name__ == "__main__":
    main()

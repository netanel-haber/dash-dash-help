#!/usr/bin/env python3
"""Benchmark a CLI command and update index.html with results."""

from __future__ import annotations

import argparse
import os
import subprocess
import time
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=check, text=True)


def benchmark(command: str) -> int:
    start = time.time_ns()
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end = time.time_ns()
    return (end - start) // 1_000_000


def build_run_url() -> str:
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    return f"{server}/{repo}/actions/runs/{run_id}"


def git_commit_and_push(row_id: str, time_ms: int, version: str) -> None:
    run(["git", "config", "user.name", "github-actions[bot]"])
    run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])
    run(["git", "add", "index.html"])

    if run(["git", "diff", "--staged", "--quiet"], check=False).returncode != 0:
        run(["git", "commit", "-m", f"{row_id}: {time_ms}ms @ {version}"])
        run(["git", "pull", "--rebase"])
        run(["git", "push"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Command to benchmark (also displayed in table)")
    parser.add_argument("--id", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--version-url", required=True)
    parser.add_argument("--install", required=True)
    parser.add_argument("--library")
    args = parser.parse_args()

    time_ms = benchmark(args.command)
    print(f"{args.command}: {time_ms}ms")

    run([
        "python3", str(SCRIPTS_DIR / "update_row.py"),
        "--id", args.id,
        "--command", args.command,
        "--library", args.library or args.id,
        "--time-ms", str(time_ms),
        "--version", args.version,
        "--version-url", args.version_url,
        "--run-url", build_run_url(),
        "--install", args.install,
    ])

    git_commit_and_push(args.id, time_ms, args.version)


if __name__ == "__main__":
    main()

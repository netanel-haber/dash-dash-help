#!/usr/bin/env python3
"""Benchmark a CLI command and update index.html with results."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent


def log(msg: str) -> None:
    print(f"[bench] {msg}", file=sys.stderr, flush=True)


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    log(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, check=check, text=True)
    if result.returncode != 0:
        log(f"  exit code: {result.returncode}")
    return result


def benchmark(command: str) -> tuple[int, int]:
    log(f"Benchmarking: {command}")
    start = time.time_ns()
    result = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end = time.time_ns()
    ms = (end - start) // 1_000_000
    log(f"  exit code: {result.returncode}")
    log(f"  duration: {ms}ms")
    return ms, result.returncode


def build_run_url() -> str:
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    url = f"{server}/{repo}/actions/runs/{run_id}"
    log(f"Run URL: {url}")
    return url


def git_commit_and_push(row_id: str, time_ms: int, version: str, retries: int = 5) -> None:
    log("Configuring git...")
    run(["git", "config", "user.name", "github-actions[bot]"])
    run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])
    run(["git", "add", "index.html"])

    if run(["git", "diff", "--staged", "--quiet"], check=False).returncode == 0:
        log("No changes to commit")
        return

    commit_msg = f"{row_id}: {time_ms}ms @ {version}"
    log(f"Committing: {commit_msg}")
    run(["git", "commit", "-m", commit_msg])

    for attempt in range(retries):
        log(f"Push attempt {attempt + 1}/{retries}")
        run(["git", "pull", "--rebase"])
        if run(["git", "push"], check=False).returncode == 0:
            log("Push succeeded")
            return
        wait = 1 << attempt
        log(f"Push failed, waiting {wait}s before retry...")
        time.sleep(wait)

    log("All push attempts failed!")
    sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Command to benchmark (also displayed in table)")
    parser.add_argument("--id", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--version-url", required=True)
    parser.add_argument("--install", required=True)
    parser.add_argument("--library")
    args = parser.parse_args()

    log(f"=== Benchmark: {args.id} ===")
    log(f"Command: {args.command}")
    log(f"Version: {args.version}")
    log(f"Library: {args.library or args.id}")

    time_ms, exit_code = benchmark(args.command)

    if exit_code != 0:
        log(f"WARNING: Command exited with code {exit_code}")

    if time_ms == 0:
        log("WARNING: 0ms benchmark - command may have failed immediately")

    print(f"{args.command}: {time_ms}ms")

    log("Updating index.html...")
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
    log("=== Done ===")


if __name__ == "__main__":
    main()

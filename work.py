#!/usr/bin/env python3
"""Benchmark CLI commands and manage index.html table."""

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, fields
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any
from urllib.request import urlopen, urlretrieve

ROOT = Path(__file__).parent
INDEX_HTML = ROOT / "index.html"
MEASUREMENTS_CSV = ROOT / "measurements.csv"
README = ROOT / "README.md"
VAST_HARDWARE_URL = "https://cloud.vast.ai/instances/"
PYTHON = "3.12"


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
    hardware: str = ""
    hardware_url: str = ""
    gpu_seconds: str = ""
    gpu_cost_usd: str = ""


def read_measurements() -> list[Measurement]:
    assert MEASUREMENTS_CSV.is_file()
    with open(MEASUREMENTS_CSV) as f:
        return [
            Measurement(
                **{
                    field.name: row.get(field.name, "")
                    for field in fields(Measurement)
                }
            )
            for row in csv.DictReader(f)
        ]


def write_measurements(measurements: list[Measurement]) -> None:
    fieldnames = [f.name for f in fields(Measurement)]
    with open(MEASUREMENTS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(asdict(m) for m in measurements)
    log(f"Wrote {len(measurements)} measurements")


def rebuild_html() -> None:
    measurements = sorted(
        read_measurements(), key=lambda m: int(m.warm_ms), reverse=True
    )

    def css(ms):
        return "ok" if int(ms) < 1000 else "slow"

    thead = """<thead>
        <tr>
          <th scope="col">library</th>
          <th scope="col">cold</th>
          <th scope="col">warm (10 runs)</th>
          <th scope="col">version</th>
          <th scope="col">hardware</th>
          <th scope="col">gpu time</th>
          <th scope="col">gpu cost</th>
          <th scope="col">measured on</th>
        </tr>
      </thead>"""

    rows = []
    for m in measurements:
        hardware = escape(m.hardware) if m.hardware else ""
        if hardware and m.hardware_url:
            hardware = f'<a href="{escape(m.hardware_url)}">{hardware}</a>'
        gpu_seconds = f"{m.gpu_seconds}s" if m.gpu_seconds else ""
        gpu_cost = f"${m.gpu_cost_usd}" if m.gpu_cost_usd else ""
        rows.append(
            f'<tr id="{m.library}"><td><code>{m.library} --help</code></td>'
            f'<td class="{css(m.cold_ms)}"><a href="{m.run_url}">{m.cold_ms}ms</a></td>'
            f'<td class="{css(m.warm_ms)}"><a href="{m.run_url}">{m.warm_ms}ms</a></td>'
            f'<td><a href="{m.version_url}">{escape(m.version)}</a></td>'
            f"<td>{hardware}</td>"
            f"<td>{escape(gpu_seconds)}</td>"
            f"<td>{escape(gpu_cost)}</td>"
            f"<td>{escape(m.last_updated)}</td></tr>"
        )
    html = re.sub(
        r"<thead>.*?</thead>",
        thead,
        INDEX_HTML.read_text(),
        flags=re.DOTALL,
    )
    rows_html = "\n    ".join(rows)
    html = re.sub(
        r"(<tbody>).*?(</tbody>)",
        rf"\1\n    {rows_html}\n    \2",
        html,
        flags=re.DOTALL,
    )
    INDEX_HTML.write_text(html)
    log(f"Rebuilt HTML with {len(measurements)} rows")


def update_readme() -> None:
    rows = [
        (
            "| library | cold | warm (10 runs) | version | hardware "
            "| gpu time | gpu cost | measured on |"
        ),
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for m in sorted(read_measurements(), key=lambda row: int(row.warm_ms), reverse=True):
        hardware = (
            f"[{m.hardware}]({m.hardware_url})"
            if m.hardware and m.hardware_url
            else m.hardware
        )
        gpu_seconds = f"{m.gpu_seconds}s" if m.gpu_seconds else ""
        gpu_cost = f"${m.gpu_cost_usd}" if m.gpu_cost_usd else ""
        rows.append(
            f"| {m.library} "
            f"| [{m.cold_ms}ms]({m.run_url}) "
            f"| [{m.warm_ms}ms]({m.run_url}) "
            f"| [{m.version}]({m.version_url}) "
            f"| {hardware} "
            f"| {gpu_seconds} "
            f"| {gpu_cost} "
            f"| {m.last_updated} |"
        )

    readme = README.read_text()
    prefix = "https://dashdashhelp.win\n"
    before, separator, _ = readme.partition(prefix)
    if not separator:
        sys.exit("README.md is missing dashdashhelp.win marker")

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    README.write_text(
        before
        + separator
        + "\n"
        + "\n".join(rows)
        + "\n\n"
        + f"Last updated: {timestamp}\n"
    )


def git(cmd: str, check: bool = True) -> int:
    log(f"$ git {cmd}")
    return subprocess.run(f"git {cmd}", shell=True, check=check).returncode


def git_commit_and_push(message: str) -> None:
    git("config user.name 'github-actions[bot]'")
    git("config user.email 'github-actions[bot]@users.noreply.github.com'")
    git("add measurements.csv index.html README.md")

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


def run(
    command: list[str],
    *,
    env: dict[str, str] | None = None,
    check: bool = True,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    log("$ " + " ".join(command))
    return subprocess.run(
        command,
        capture_output=capture,
        check=check,
        env=env,
        text=True,
    )


def gpu_libraries() -> list[str]:
    return [
        "vllm",
        "sglang",
        "VLMEvalKit",
        "transformers",
        "tensorrt-llm",
        "datasets",
        "llm",
        "openai",
        "langchain-cli",
        "hf",
        "lm-eval",
        "llama.cpp",
        "ollama",
        "tokenspeed",
    ]


def install_gpu_library(
    library: str,
    root: Path,
) -> tuple[list[str], str, str, dict[str, str] | None]:
    safe_library = re.sub(r"[^A-Za-z0-9_.-]+", "-", library)
    venv = root / "venvs" / safe_library
    python = venv / "bin" / "python"
    env = os.environ.copy()
    env["PATH"] = f"{Path.home() / '.local/bin'}:{env['PATH']}"

    if library == "vllm":
        with urlopen("https://api.github.com/repos/vllm-project/vllm/releases/latest") as f:
            tag = str(json.load(f)["tag_name"])
        run(["uv", "venv", "--python", PYTHON, str(venv)], env=env)
        install_env = env | {"VLLM_USE_PRECOMPILED": "1"}
        run([
            "uv",
            "pip",
            "install",
            "--python",
            str(python),
            f"vllm @ git+https://github.com/vllm-project/vllm.git@{tag}",
            "--index-strategy",
            "unsafe-best-match",
        ], env=install_env)
        version = run([
            str(python),
            "-c",
            "from importlib.metadata import version; print(version('vllm'))",
        ], capture=True).stdout.strip()
        return (
            [str(venv / "bin" / "vllm"), "--help"],
            version,
            f"https://github.com/vllm-project/vllm/releases/tag/{tag}",
            None,
        )

    if library == "sglang":
        with urlopen("https://api.github.com/repos/sgl-project/sglang/releases/latest") as f:
            tag = str(json.load(f)["tag_name"])
        source = root / "src" / "sglang"
        shutil.rmtree(source, ignore_errors=True)
        run([
            "git",
            "clone",
            "--depth",
            "1",
            "--branch",
            tag,
            "https://github.com/sgl-project/sglang.git",
            str(source),
        ])
        run(["uv", "venv", "--python", PYTHON, str(venv)], env=env)
        run([
            "uv",
            "pip",
            "install",
            "--python",
            str(python),
            "--upgrade",
            "pip",
            "setuptools",
            str(source / "python"),
        ], env=env)
        return (
            [str(python), "-m", "sglang.launch_server", "--help"],
            tag,
            f"https://github.com/sgl-project/sglang/releases/tag/{tag}",
            None,
        )

    if library == "VLMEvalKit":
        with urlopen("https://api.github.com/repos/open-compass/VLMEvalKit/releases/latest") as f:
            tag = str(json.load(f)["tag_name"])
        source = root / "src" / "VLMEvalKit"
        shutil.rmtree(source, ignore_errors=True)
        run([
            "git",
            "clone",
            "--depth",
            "1",
            "--branch",
            tag,
            "https://github.com/open-compass/VLMEvalKit.git",
            str(source),
        ])
        run(["uv", "venv", "--python", PYTHON, str(venv)], env=env)
        run([
            "uv",
            "pip",
            "install",
            "--python",
            str(python),
            "-e",
            str(source),
        ], env=env)
        return (
            [str(python), str(source / "run.py"), "--help"],
            tag,
            f"https://github.com/open-compass/VLMEvalKit/releases/tag/{tag}",
            None,
        )

    if library == "tensorrt-llm":
        run(["uv", "venv", "--python", PYTHON, str(venv)], env=env)
        run([
            "uv",
            "pip",
            "install",
            "--python",
            str(python),
            "tensorrt-llm",
            "click",
            "pynvml",
        ], env=env)
        version = run([
            str(python),
            "-c",
            "from importlib.metadata import version; print(version('tensorrt-llm'))",
        ], capture=True).stdout.strip()
        return (
            [str(venv / "bin" / "trtllm-serve"), "--help"],
            version,
            f"https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v{version}",
            None,
        )

    if library == "tokenspeed":
        with urlopen("https://api.github.com/repos/lightseekorg/tokenspeed/commits/main") as f:
            commit = str(json.load(f)["sha"])
        run(["uv", "venv", "--python", PYTHON, str(venv)], env=env)
        run([
            "uv",
            "pip",
            "install",
            "--python",
            str(python),
            (
                "tokenspeed @ "
                f"git+https://github.com/lightseekorg/tokenspeed.git@{commit}"
                "#subdirectory=python"
            ),
        ], env=env)
        package_version = run([
            str(python),
            "-c",
            "from importlib.metadata import version; print(version('tokenspeed'))",
        ], capture=True).stdout.strip()
        version = f"{package_version}@{commit[:7]}"
        return (
            [str(venv / "bin" / "tokenspeed"), "--help"],
            version,
            f"https://github.com/lightseekorg/tokenspeed/commit/{commit}",
            None,
        )

    if library == "llama.cpp":
        with urlopen("https://api.github.com/repos/ggml-org/llama.cpp/releases/latest") as f:
            release = json.load(f)
        tag = str(release["tag_name"])
        url = ""
        for asset in release.get("assets", []):
            name = str(asset.get("name", ""))
            if "ubuntu" in name and "x64" in name and name.endswith(".tar.gz"):
                url = str(asset["browser_download_url"])
                break
        if not url:
            raise RuntimeError("No llama.cpp Ubuntu x64 tarball found")
        dest = root / "llama-bin"
        archive = root / "llama.tar.gz"
        shutil.rmtree(dest, ignore_errors=True)
        dest.mkdir(parents=True, exist_ok=True)
        urlretrieve(url, archive)
        run(["tar", "-xzf", str(archive), "-C", str(dest), "--strip-components=1"])
        return (
            [str(dest / "llama-cli"), "--help"],
            tag,
            f"https://github.com/ggml-org/llama.cpp/releases/tag/{tag}",
            None,
        )

    if library == "ollama":
        run(["bash", "-lc", "curl -fsSL https://ollama.com/install.sh | sh"])
        version = run([
            "bash",
            "-lc",
            "ollama --version | grep -oP 'version is \\K[0-9.]+'",
        ], capture=True).stdout.strip()
        return (
            ["ollama", "--help"],
            version,
            f"https://github.com/ollama/ollama/releases/tag/v{version}",
            None,
        )

    package_by_library = {
        "transformers": (
            "transformers",
            "transformers-cli",
            "https://github.com/huggingface/transformers/releases/tag/v{version}",
        ),
        "datasets": (
            "datasets",
            "datasets-cli",
            "https://github.com/huggingface/datasets/releases/tag/{version}",
        ),
        "llm": ("llm", "llm", "https://github.com/simonw/llm/releases/tag/{version}"),
        "openai": (
            "openai==2.34.0",
            "openai",
            "https://github.com/openai/openai-python/releases/tag/v{version}",
        ),
        "langchain-cli": (
            "langchain-cli",
            "langchain",
            "https://github.com/langchain-ai/langchain/releases/tag/langchain-cli=={version}",
        ),
        "hf": (
            "huggingface_hub",
            "hf",
            "https://github.com/huggingface/huggingface_hub/releases/tag/v{version}",
        ),
        "lm-eval": (
            "lm-eval",
            "lm-eval",
            "https://github.com/EleutherAI/lm-evaluation-harness/releases/tag/v{version}",
        ),
    }
    if library not in package_by_library:
        raise KeyError(f"Unknown GPU library: {library}")

    package_spec, executable, url_template = package_by_library[library]
    package = package_spec.split("==", 1)[0]
    run(["uv", "venv", "--python", PYTHON, str(venv)], env=env)
    run(["uv", "pip", "install", "--python", str(python), package_spec], env=env)
    version = run([
        str(python),
        "-c",
        "from importlib.metadata import version; import sys; print(version(sys.argv[1]))",
        package,
    ], capture=True).stdout.strip()
    return (
        [str(venv / "bin" / executable), "--help"],
        version,
        url_template.format(version=version),
        None,
    )


def cmd_gpu_list(_: argparse.Namespace) -> None:
    print("\n".join(gpu_libraries()))


def cmd_gpu_run(args: argparse.Namespace) -> None:
    if shutil.which("uv") is None:
        run([sys.executable, "-m", "pip", "install", "--upgrade", "uv"])
    run(["uv", "python", "install", PYTHON])
    missing = [tool for tool in ("git", "curl", "tar") if shutil.which(tool) is None]
    if missing:
        run(["apt", "update"])
        run(["apt", "install", "-y", "--no-install-recommends", *missing])

    root = Path(args.root)
    root.mkdir(parents=True, exist_ok=True)
    (root / "src").mkdir(exist_ok=True)
    libraries = gpu_libraries() if args.library == "all" else [args.library]
    workers = max(1, min(len(libraries), os.cpu_count() or 1))
    installs: dict[str, tuple[list[str], str, str, dict[str, str] | None, int]] = {}
    results: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []

    def install(library: str) -> tuple[list[str], str, str, dict[str, str] | None, int]:
        started = time.time()
        log(f"=== install {library} ===")
        command, version, version_url, command_env = install_gpu_library(library, root)
        return command, version, version_url, command_env, max(0, int(time.time() - started))

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(install, library): library for library in libraries}
        for future in as_completed(futures):
            library = futures[future]
            try:
                installs[library] = future.result()
            except Exception as exc:
                failures.append({"library": library, "error": str(exc)})
                log(f"{library} install failed: {exc}")

    for library in libraries:
        if library not in installs:
            continue
        command, version, version_url, command_env, install_seconds = installs[library]
        started = time.time()
        try:
            log(f"=== benchmark {library} ===")
            times: list[int] = []
            for i in range(11):
                start = time.perf_counter_ns()
                proc = subprocess.run(
                    command,
                    capture_output=True,
                    env=command_env,
                    text=True,
                )
                elapsed_ms = (time.perf_counter_ns() - start) // 1_000_000
                if proc.returncode != 0:
                    print(proc.stdout, file=sys.stderr)
                    print(proc.stderr, file=sys.stderr)
                    raise subprocess.CalledProcessError(proc.returncode, command)
                times.append(elapsed_ms)
                log(f"  Run {i + 1}/11: {elapsed_ms}ms")

            results.append({
                "library": library,
                "version": version,
                "version_url": version_url,
                "cold_ms": times[0],
                "warm_ms": sum(times[1:]) // 10,
                "gpu_seconds": str(install_seconds + max(0, int(time.time() - started))),
                "times": times,
            })
        except Exception as exc:
            failures.append({"library": library, "error": str(exc)})
            log(f"{library} failed: {exc}")

    for library in libraries:
        safe_library = re.sub(r"[^A-Za-z0-9_.-]+", "-", library)
        shutil.rmtree(root / "venvs" / safe_library, ignore_errors=True)
        shutil.rmtree(root / "src" / library, ignore_errors=True)
        if library == "sglang":
            shutil.rmtree(root / "src" / "sglang", ignore_errors=True)
        if library == "llama.cpp":
            shutil.rmtree(root / "llama-bin", ignore_errors=True)
            (root / "llama.tar.gz").unlink(missing_ok=True)

    Path(args.output).write_text(
        json.dumps({"results": results, "failures": failures}, indent=2)
    )
    log(f"Wrote GPU results to {args.output}")


def cmd_vast_rent(args: argparse.Namespace) -> None:
    public_key = Path(args.ssh_public_key).read_text(encoding="utf-8").strip()
    proc = run(["vastai", "create", "ssh-key", public_key, "-y"], capture=True)
    if proc.stdout.strip():
        print(proc.stdout.strip())
    if proc.stderr.strip():
        print(proc.stderr.strip(), file=sys.stderr)

    query = f"{args.query} dph<={args.max_price}"
    offers = json.loads(run([
        "vastai",
        "--raw",
        "search",
        "offers",
        "--type",
        "on-demand",
        query,
        "--storage",
        args.disk_gb,
        "--limit",
        str(args.limit),
        "-o",
        "dph",
    ], capture=True).stdout)
    if not isinstance(offers, list):
        raise TypeError(f"Expected Vast offer list, got {type(offers).__name__}")
    offers.sort(key=lambda offer: float(offer.get("dph_total") or offer.get("dph") or "inf"))
    log(f"Found {len(offers)} on-demand offers")

    for offer in offers[:5]:
        offer_id = str(offer.get("id") or offer.get("ask_contract_id") or "")
        price = offer.get("dph_total") or offer.get("dph")
        log(f"- {offer_id}: {offer.get('gpu_name', 'unknown GPU')}, price={price}")

    for offer in offers:
        offer_id = str(offer.get("id") or offer.get("ask_contract_id") or "")
        price = offer.get("dph_total") or offer.get("dph")
        if not offer_id or price is None:
            continue

        log(
            f"Trying on-demand offer {offer_id}: "
            f"{offer.get('gpu_name', 'unknown GPU')}, price={price}"
        )
        proc = run([
            "vastai",
            "--raw",
            "create",
            "instance",
            offer_id,
            "--image",
            args.image,
            "--disk",
            args.disk_gb,
            "--ssh",
            "--direct",
            "--cancel-unavail",
            "--label",
            args.label,
        ], capture=True, check=False)
        if proc.stdout.strip():
            print(proc.stdout.strip())
        if proc.stderr.strip():
            print(proc.stderr.strip(), file=sys.stderr)
        if proc.returncode != 0:
            continue

        try:
            payload = json.loads(proc.stdout)
        except json.JSONDecodeError:
            continue
        if payload.get("error"):
            continue

        instance_id = str(payload.get("new_contract") or "")
        if not instance_id:
            continue

        github_output = os.environ.get("GITHUB_OUTPUT")
        if github_output:
            with Path(github_output).open("a", encoding="utf-8") as f:
                f.write(f"instance_id={instance_id}\n")
        else:
            print(f"instance_id={instance_id}")
        log(f"Selected on-demand offer {offer_id}")
        return

    sys.exit(f"No Vast on-demand offer under ${args.max_price}/hr could be rented")


def cmd_vast_wait(args: argparse.Namespace) -> None:
    info: dict[str, Any] = {}
    for _ in range(args.status_attempts):
        info = json.loads(
            run(["vastai", "--raw", "show", "instance", args.instance_id], capture=True)
            .stdout
        )
        print(json.dumps(info, indent=2))
        host = str(info.get("public_ipaddr") or "")
        port = str(info.get("ports", {}).get("22/tcp", [{}])[0].get("HostPort") or "")
        if (
            info.get("actual_status") == "running"
            and info.get("intended_status") == "running"
            and host
            and port
        ):
            break
        time.sleep(10)

    if info.get("actual_status") != "running" or info.get("intended_status") != "running":
        sys.exit("Vast instance did not reach running state")

    if not host or not port:
        sys.exit("Vast instance is missing direct SSH target")

    for _ in range(args.ssh_attempts):
        proc = subprocess.run([
            "ssh",
            "-i",
            args.ssh_private_key,
            "-p",
            port,
            "-o",
            "IdentitiesOnly=yes",
            "-o",
            "StrictHostKeyChecking=no",
            "-o",
            "UserKnownHostsFile=/dev/null",
            "-o",
            "ConnectTimeout=10",
            f"root@{host}",
            "echo ok",
        ])
        if proc.returncode == 0:
            github_output = os.environ.get("GITHUB_OUTPUT")
            if github_output:
                with Path(github_output).open("a", encoding="utf-8") as f:
                    f.write(f"host={host}\n")
                    f.write(f"port={port}\n")
            else:
                print(f"host={host}")
                print(f"port={port}")
            return
        time.sleep(10)

    sys.exit("SSH never became ready")


def cmd_vast_destroy(args: argparse.Namespace) -> None:
    run(["vastai", "destroy", "instance", args.instance_id, "-y"])


def cmd_vast_metadata(args: argparse.Namespace) -> None:
    info = json.loads(
        run(["vastai", "--raw", "show", "instance", args.instance_id], capture=True)
        .stdout
    )
    now = time.time()
    start = float(info.get("start_date") or now)
    seconds = max(0, int(now - start))
    hourly = float(
        info.get("dph_total")
        or info.get("discounted_dph_total")
        or info.get("dph")
        or 0
    )
    gpu_count = int(info.get("num_gpus") or info.get("gpu_count") or 1)
    gpu_name = str(info.get("gpu_name") or "unknown GPU")
    print(json.dumps({
        "hardware": f"{gpu_count}x {gpu_name}",
        "hardware_url": f"{VAST_HARDWARE_URL}{args.instance_id}",
        "gpu_seconds": str(seconds),
        "gpu_cost_usd": f"{hourly * seconds / 3600:.4f}",
        "vast_instance_id": args.instance_id,
        "vast_hourly_usd": hourly,
    }, indent=2))


def cmd_gpu_update(args: argparse.Namespace) -> None:
    payload = json.loads(Path(args.results).read_text())
    metadata = json.loads(Path(args.metadata).read_text())
    measurements = read_measurements()
    run_url = (
        f"{os.getenv('GITHUB_SERVER_URL', 'https://github.com')}/"
        f"{os.getenv('GITHUB_REPOSITORY')}/actions/runs/"
        f"{os.getenv('GITHUB_RUN_ID')}"
    )

    for result in payload.get("results", []):
        seconds = str(result.get("gpu_seconds") or metadata.get("gpu_seconds") or "")
        hourly = float(metadata.get("vast_hourly_usd") or 0)
        cost = f"{hourly * int(seconds) / 3600:.4f}" if seconds else ""
        measurement = Measurement(
            library=result["library"],
            version=str(result["version"]),
            version_url=str(result["version_url"]),
            cold_ms=int(result["cold_ms"]),
            warm_ms=int(result["warm_ms"]),
            run_url=run_url,
            last_updated=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
            hardware=str(metadata.get("hardware", "")),
            hardware_url=str(metadata.get("hardware_url", "")),
            gpu_seconds=seconds,
            gpu_cost_usd=cost or str(metadata.get("gpu_cost_usd", "")),
        )
        idx = next(
            (i for i, row in enumerate(measurements) if row.library == measurement.library),
            None,
        )
        if idx is None:
            measurements.append(measurement)
        else:
            measurements[idx] = measurement

    write_measurements(measurements)
    rebuild_html()
    update_readme()
    git_commit_and_push("gpu: update dashboard")

    failures = payload.get("failures", [])
    if failures:
        print(json.dumps(failures, indent=2), file=sys.stderr)
        sys.exit(1)


def cmd_rebuild(_: argparse.Namespace) -> None:
    write_measurements(read_measurements())
    rebuild_html()
    update_readme()


def cmd_bench(args: argparse.Namespace) -> None:
    log(f"=== {args.library}: {args.command} ===")
    if (args.cold_ms is None) != (args.warm_ms is None):
        sys.exit("--cold-ms and --warm-ms must be passed together")

    if args.cold_ms is not None and args.warm_ms is not None:
        cold_ms, warm_ms = args.cold_ms, args.warm_ms
        log(f"Using recorded timings: {cold_ms=}, {warm_ms=}")
    else:
        cold_ms, warm_ms = bench(args.command)

    if args.dry_run:
        return log("DRY RUN: Skipping update")

    run_url = (
        f"{os.getenv('GITHUB_SERVER_URL', 'https://github.com')}/"
        f"{os.getenv('GITHUB_REPOSITORY')}/actions/runs/"
        f"{os.getenv('GITHUB_RUN_ID')}"
    )
    measurement = Measurement(
        library=args.library,
        version=args.version,
        version_url=args.version_url,
        cold_ms=cold_ms,
        warm_ms=warm_ms,
        run_url=run_url,
        last_updated=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
    )

    measurements = read_measurements()
    idx = next(
        (i for i, row in enumerate(measurements) if row.library == measurement.library),
        None,
    )
    if idx is None:
        measurements.append(measurement)
    else:
        measurements[idx] = measurement
    log(f"{'Added' if idx is None else 'Updated'} {measurement.library}")
    write_measurements(measurements)
    rebuild_html()
    update_readme()

    git_commit_and_push(
        f"{measurement.library}: {cold_ms=}/{warm_ms=} @ {measurement.version}"
    )


def main() -> None:
    if len(sys.argv) == 1:
        sys.exit(
            "usage: work.py {bench,gpu-list,gpu-run,gpu-update,rebuild,"
            "update-readme,vast-destroy,vast-metadata,vast-rent,vast-wait}"
        )
    command = sys.argv[1]
    p = argparse.ArgumentParser()

    if command == "bench":
        p.add_argument("command")
        p.add_argument("--library", required=True)
        p.add_argument("--version", required=True)
        p.add_argument("--version-url", required=True)
        p.add_argument("--cold-ms", type=int)
        p.add_argument("--warm-ms", type=int)
        p.add_argument("--dry-run", action="store_true")
        cmd_bench(p.parse_args(sys.argv[2:]))
        return

    if command == "gpu-list":
        cmd_gpu_list(p.parse_args(sys.argv[2:]))
        return

    if command == "gpu-run":
        p.add_argument("--library", required=True)
        p.add_argument("--output", required=True)
        p.add_argument("--root", default="/root/dashdashhelp-gpu")
        cmd_gpu_run(p.parse_args(sys.argv[2:]))
        return

    if command == "gpu-update":
        p.add_argument("--results", required=True)
        p.add_argument("--metadata", required=True)
        cmd_gpu_update(p.parse_args(sys.argv[2:]))
        return

    if command == "rebuild":
        cmd_rebuild(p.parse_args(sys.argv[2:]))
        return

    if command == "update-readme":
        update_readme()
        return

    if command == "vast-destroy":
        p.add_argument("--instance-id", required=True)
        cmd_vast_destroy(p.parse_args(sys.argv[2:]))
        return

    if command == "vast-metadata":
        p.add_argument("--instance-id", required=True)
        cmd_vast_metadata(p.parse_args(sys.argv[2:]))
        return

    if command == "vast-rent":
        p.add_argument("--query", required=True)
        p.add_argument("--max-price", required=True)
        p.add_argument("--disk-gb", required=True)
        p.add_argument("--image", required=True)
        p.add_argument("--label", required=True)
        p.add_argument("--ssh-public-key", required=True)
        p.add_argument("--limit", type=int, default=20)
        cmd_vast_rent(p.parse_args(sys.argv[2:]))
        return

    if command == "vast-wait":
        p.add_argument("--instance-id", required=True)
        p.add_argument("--ssh-private-key", required=True)
        p.add_argument("--status-attempts", type=int, default=90)
        p.add_argument("--ssh-attempts", type=int, default=60)
        cmd_vast_wait(p.parse_args(sys.argv[2:]))
        return

    sys.exit(f"unknown command: {command}")


if __name__ == "__main__":
    main()

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
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from dataclasses import dataclass
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from shlex import quote as shell_quote, split as shell_split
from typing import Any
from urllib.parse import quote as url_quote
from urllib.request import urlopen, urlretrieve

ROOT = Path(__file__).parent
INDEX_HTML = ROOT / "index.html"
MEASUREMENTS_CSV = ROOT / "measurements.csv"
README = ROOT / "README.md"
PYTHON = "3.12"
CSV_FIELDS = [
    "library",
    "version",
    "version_url",
    "cold_ms",
    "warm_ms",
    "run_url",
    "last_updated",
    "hardware",
    "hardware_url",
]
GPU_LIBRARIES = [
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


def log(msg: str) -> None:
    print(f"[work] {msg}", file=sys.stderr, flush=True)


def q(value: object) -> str:
    return shell_quote(str(value))


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


def read_measurements() -> list[Measurement]:
    assert MEASUREMENTS_CSV.is_file()
    measurements = []
    with MEASUREMENTS_CSV.open() as f:
        for row in csv.DictReader(f):
            measurements.append(
                Measurement(
                    library=row.get("library", ""),
                    version=row.get("version", ""),
                    version_url=row.get("version_url", ""),
                    cold_ms=int(row.get("cold_ms") or 0),
                    warm_ms=int(row.get("warm_ms") or 0),
                    run_url=row.get("run_url", ""),
                    last_updated=row.get("last_updated", ""),
                    hardware=row.get("hardware", ""),
                    hardware_url=row.get("hardware_url", ""),
                )
            )
    return measurements


def write_measurements(measurements: list[Measurement]) -> None:
    with MEASUREMENTS_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(m.__dict__ for m in measurements)
    log(f"Wrote {len(measurements)} measurements")


def display_hardware(hardware: str) -> str:
    hardware = hardware.strip()
    if not hardware:
        return ""
    if hardware.startswith("CPU:"):
        return hardware
    return f"GPU: {hardware}"


def markdown_hardware(hardware: str) -> str:
    return display_hardware(hardware).replace("; GPU:", "<br>GPU:")


def html_attr(value: str) -> str:
    return escape(value, quote=True)


def display_timestamp(timestamp: str) -> str:
    try:
        dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%MZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return timestamp
    return f"{dt:%b} {dt.day}, {dt:%Y %H:%M UTC}"


def run_meta_html(measurements: list[Measurement]) -> str:
    groups = []
    seen = set()
    for m in measurements:
        key = (display_hardware(m.hardware), display_timestamp(m.last_updated), m.run_url)
        if key in seen:
            continue
        seen.add(key)
        groups.append(key)

    if not groups:
        return ""

    if len(groups) == 1:
        hardware, measured, run_url = groups[0]
        text = " / ".join(part for part in [measured, hardware] if part)
        return (
            f'<p class="run-meta" id="run-meta">'
            f'<a href="{html_attr(run_url)}">Run: {escape(text)}</a></p>'
        )

    title = "; ".join(
        " / ".join(part for part in [measured, hardware] if part)
        for hardware, measured, _ in groups
    )
    return (
        f'<p class="run-meta" id="run-meta" title="{html_attr(title)}">'
        f"{len(groups)} measurement groups</p>"
    )


def rebuild_html() -> None:
    measurements = sorted(read_measurements(), key=lambda m: int(m.warm_ms), reverse=True)

    def css(ms):
        return "ok" if int(ms) < 1000 else "slow"

    thead = """<thead>
        <tr>
          <th scope="col">tool</th>
          <th scope="col" class="time-cell">
            <span class="time-pair">
              <span class="time-chip cold-time" title="First run">cold</span>
              <span class="time-chip warm-time" title="Average of runs 2–11">warm</span>
            </span>
          </th>
          <th scope="col">version</th>
        </tr>
      </thead>"""

    rows = []
    for m in measurements:
        fragment = html_attr(url_quote(m.library, safe=""))
        rows.append(
            f'<tr id="{html_attr(m.library)}" tabindex="-1">'
            f'<td class="tool-cell"><code><a class="tool-link" href="#{fragment}" '
            f'aria-label="{html_attr(m.library)} --help — focus this library">'
            f'{escape(m.library)} --help</a></code></td>'
            f'<td class="time-cell"><span class="time-pair">'
            f'<a class="time-chip time-value cold-time {css(m.cold_ms)}" '
            f'href="{html_attr(m.run_url)}" aria-label="Cold: {m.cold_ms} milliseconds">{m.cold_ms}ms</a>'
            f'<a class="time-chip time-value warm-time {css(m.warm_ms)}" '
            f'href="{html_attr(m.run_url)}" aria-label="Warm: {m.warm_ms} milliseconds">{m.warm_ms}ms</a>'
            f'</span></td>'
            f'<td class="version"><a href="{html_attr(m.version_url)}">{escape(m.version)}</a></td></tr>'
        )

    tool_width_ch = max(
        (len(f"{m.library} --help") for m in measurements),
        default=0,
    ) + 3
    colgroup = f"""<colgroup>
        <col class="tool-col" style="--tool-width: {tool_width_ch}ch">
        <col class="time-col">
        <col>
      </colgroup>"""
    html = re.sub(
        r"<colgroup>.*?</colgroup>",
        colgroup,
        INDEX_HTML.read_text(),
        flags=re.DOTALL,
    )
    html = re.sub(
        r"<thead>.*?</thead>",
        thead,
        html,
        flags=re.DOTALL,
    )
    rows_html = "\n    ".join(rows)
    html = re.sub(
        r"(<tbody>).*?(</tbody>)",
        rf"\1\n    {rows_html}\n    \2",
        html,
        flags=re.DOTALL,
    )
    html = re.sub(r"\n\s*<p class=\"run-meta\" id=\"run-meta\".*?</p>", "", html, flags=re.DOTALL)
    html = html.replace(
        '\n  <div class="table-wrap">',
        f"\n  {run_meta_html(measurements)}\n\n  <div class=\"table-wrap\">",
        1,
    )
    INDEX_HTML.write_text(html)
    log(f"Rebuilt HTML with {len(measurements)} rows")


def update_readme() -> None:
    rows = [
        "| library | cold | warm (10 runs) | version | hardware | measured |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for m in sorted(read_measurements(), key=lambda row: int(row.warm_ms), reverse=True):
        rows.append(
            f"| {m.library} "
            f"| [{m.cold_ms}ms]({m.run_url}) "
            f"| [{m.warm_ms}ms]({m.run_url}) "
            f"| [{m.version}]({m.version_url}) "
            f"| {markdown_hardware(m.hardware)} "
            f"| {display_timestamp(m.last_updated)} |"
        )

    readme = README.read_text()
    prefix = "https://dashdashhelp.win\n"
    before, separator, _ = readme.partition(prefix)
    if not separator:
        sys.exit("README.md is missing dashdashhelp.win marker")

    README.write_text(before + separator + "\n" + "\n".join(rows) + "\n")


def git(*args: str, check: bool = True) -> int:
    return run("git " + " ".join(q(arg) for arg in args), check=check).returncode


def git_commit_and_push(message: str) -> None:
    git("config", "user.name", "github-actions[bot]")
    git("config", "user.email", "github-actions[bot]@users.noreply.github.com")
    git("add", "measurements.csv", "index.html", "README.md")

    if git("diff", "--staged", "--quiet", check=False) == 0:
        log("No changes to commit")
        return

    git("commit", "-m", message)

    for attempt in range(5):
        log(f"Push attempt {attempt + 1}/5")
        git("pull", "--rebase")
        if git("push", check=False) == 0:
            return
        time.sleep(1 << attempt)

    sys.exit("All push attempts failed!")


def run(
    command: str,
    *,
    env: dict[str, str] | None = None,
    check: bool = True,
    capture: bool = False,
    log_file: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    log("$ " + command)
    if log_file:
        with log_file.open("a", encoding="utf-8", errors="replace") as f:
            print(f"$ {command}", file=f, flush=True)
            return subprocess.run(
                shell_split(command),
                check=check,
                env=env,
                stderr=subprocess.STDOUT,
                stdout=f,
                text=True,
            )

    return subprocess.run(
        shell_split(command),
        capture_output=capture,
        check=check,
        env=env,
        text=True,
    )


def install_gpu_library(
    library: str,
    root: Path,
    log_file: Path | None = None,
) -> tuple[str, str, str, dict[str, str] | None]:
    safe_library = re.sub(r"[^A-Za-z0-9_.-]+", "-", library)
    venv = root / "venvs" / safe_library
    python = venv / "bin" / "python"
    env = os.environ.copy()
    env["PATH"] = f"{Path.home() / '.local/bin'}:{env['PATH']}"

    match library:
        case "vllm":
            with urlopen("https://api.github.com/repos/vllm-project/vllm/releases/latest") as f:
                tag = str(json.load(f)["tag_name"])
            run(f"uv venv --python {PYTHON} {q(venv)}", env=env, log_file=log_file)
            install_env = env | {"VLLM_USE_PRECOMPILED": "1"}
            run(
                f"uv pip install --python {q(python)} "
                f"{q(f'vllm @ git+https://github.com/vllm-project/vllm.git@{tag}')} "
                "--index-strategy unsafe-best-match",
                env=install_env,
                log_file=log_file,
            )
            return (
                f"{q(venv / 'bin' / 'vllm')} --help",
                tag.removeprefix("v"),
                f"https://github.com/vllm-project/vllm/releases/tag/{tag}",
                None,
            )
        case "sglang":
            with urlopen("https://api.github.com/repos/sgl-project/sglang/releases/latest") as f:
                tag = str(json.load(f)["tag_name"])
            run(f"uv venv --python {PYTHON} {q(venv)}", env=env, log_file=log_file)
            run(f"uv pip install --python {q(python)} sglang", env=env, log_file=log_file)
            code = "from importlib.metadata import version; print(version('sglang'))"
            version = run(f"{q(python)} -c {q(code)}", capture=True).stdout.strip()
            return (
                f"{q(python)} -m sglang.launch_server --help",
                version,
                f"https://github.com/sgl-project/sglang/releases/tag/v{version}",
                None,
            )
        case "VLMEvalKit":
            with urlopen("https://api.github.com/repos/open-compass/VLMEvalKit/releases/latest") as f:
                tag = str(json.load(f)["tag_name"])
            source = root / "src" / "VLMEvalKit"
            shutil.rmtree(source, ignore_errors=True)
            run(
                f"git clone --depth 1 --branch {q(tag)} https://github.com/open-compass/VLMEvalKit.git {q(source)}",
                log_file=log_file,
            )
            run(f"uv venv --python {PYTHON} {q(venv)}", env=env, log_file=log_file)
            run(f"uv pip install --python {q(python)} -e {q(source)}", env=env, log_file=log_file)
            return (
                f"{q(python)} {q(source / 'run.py')} --help",
                tag,
                f"https://github.com/open-compass/VLMEvalKit/releases/tag/{tag}",
                None,
            )
        case "tensorrt-llm":
            run(f"uv venv --python {PYTHON} {q(venv)}", env=env, log_file=log_file)
            run(f"uv pip install --python {q(python)} tensorrt-llm click pynvml", env=env, log_file=log_file)
            code = "from importlib.metadata import version; print(version('tensorrt-llm'))"
            version = run(f"{q(python)} -c {q(code)}", capture=True).stdout.strip()
            return (
                f"{q(venv / 'bin' / 'trtllm-serve')} --help",
                version,
                f"https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v{version}",
                None,
            )
        case "tokenspeed":
            with urlopen("https://api.github.com/repos/lightseekorg/tokenspeed/commits/main") as f:
                commit = str(json.load(f)["sha"])
            run(f"uv venv --python {PYTHON} {q(venv)}", env=env, log_file=log_file)
            package_spec = (
                f"tokenspeed @ git+https://github.com/lightseekorg/tokenspeed.git@{commit}#subdirectory=python"
            )
            run(f"uv pip install --python {q(python)} {q(package_spec)}", env=env, log_file=log_file)
            code = "from importlib.metadata import version; print(version('tokenspeed'))"
            package_version = run(f"{q(python)} -c {q(code)}", capture=True).stdout.strip()
            version = f"{package_version}@{commit[:7]}"
            return (
                f"{q(venv / 'bin' / 'tokenspeed')} --help",
                version,
                f"https://github.com/lightseekorg/tokenspeed/commit/{commit}",
                None,
            )
        case "llama.cpp":
            with urlopen("https://api.github.com/repos/ggml-org/llama.cpp/releases/latest") as f:
                release = json.load(f)
            tag = str(release["tag_name"])
            url = ""
            for asset in release.get("assets", []):
                name = str(asset.get("name", ""))
                if name.endswith("-bin-ubuntu-x64.tar.gz"):
                    url = str(asset["browser_download_url"])
                    break
            if not url:
                raise RuntimeError("No llama.cpp Ubuntu x64 tarball found")
            dest = root / "llama-bin"
            archive = root / "llama.tar.gz"
            shutil.rmtree(dest, ignore_errors=True)
            dest.mkdir(parents=True, exist_ok=True)
            urlretrieve(url, archive)
            run(f"tar -xzf {q(archive)} -C {q(dest)} --strip-components=1", log_file=log_file)
            return (
                f"{q(dest / 'llama-cli')} --help",
                tag,
                f"https://github.com/ggml-org/llama.cpp/releases/tag/{tag}",
                env | {"LD_LIBRARY_PATH": str(dest)},
            )
        case "ollama":
            run(f"bash -lc {q('curl -fsSL https://ollama.com/install.sh | sh')}", log_file=log_file)
            command = r"ollama --version | grep -oP 'version is \K[0-9.]+'"
            version = run(f"bash -lc {q(command)}", capture=True).stdout.strip()
            return (
                "ollama --help",
                version,
                f"https://github.com/ollama/ollama/releases/tag/v{version}",
                None,
            )
        case _:
            package_by_library = {
                "transformers": (
                    "transformers[serving] requests",
                    "transformers",
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
            package = package_spec.split()[0].split("[", 1)[0].split("==", 1)[0]
            run(f"uv venv --python {PYTHON} {q(venv)}", env=env, log_file=log_file)
            run(f"uv pip install --python {q(python)} {package_spec}", env=env, log_file=log_file)
            code = "from importlib.metadata import version; import sys; print(version(sys.argv[1]))"
            version = run(f"{q(python)} -c {q(code)} {q(package)}", capture=True).stdout.strip()
            return (
                f"{q(venv / 'bin' / executable)} --help",
                version,
                url_template.format(version=version),
                None,
            )


def log_lines(path: Path) -> list[str]:
    if not path.is_file():
        return []
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def last_log_line(path: Path) -> str:
    for line in reversed(log_lines(path)):
        if line.strip():
            return line.strip()
    return ""


def print_log_edges(library: str, path: Path) -> None:
    lines = log_lines(path)
    if not lines:
        log(f"{library}: empty install log")
        return

    log(f"--- {library} install log: first 10 lines ---")
    for line in lines[:10]:
        log(f"{library}: {line}")
    log(f"--- {library} install log: last 10 lines ---")
    for line in lines[-10:]:
        log(f"{library}: {line}")


def cmd_gpu_run(args: argparse.Namespace) -> None:
    root = Path(args.root)
    root.mkdir(parents=True, exist_ok=True)
    (root / "src").mkdir(exist_ok=True)
    logs = root / "logs"
    logs.mkdir(exist_ok=True)
    os.environ["UV_CACHE_DIR"] = str(root / "uv-cache")
    Path(os.environ["UV_CACHE_DIR"]).mkdir(exist_ok=True)

    if shutil.which("uv") is None:
        run(f"{q(sys.executable)} -m pip install --upgrade uv")
    run("apt update")
    run(
        "apt install -y --no-install-recommends git curl tar zstd libxcb1 libgl1 libglib2.0-0 openmpi-bin libopenmpi-dev"
    )
    run(f"uv python install {PYTHON}")

    if args.libraries.strip() == "all":
        libraries = GPU_LIBRARIES
    else:
        libraries = [x for x in re.split(r"[,\s]+", args.libraries.strip()) if x]
        unknown = sorted(set(libraries) - set(GPU_LIBRARIES))
        if unknown:
            sys.exit(f"Unknown GPU libraries: {', '.join(unknown)}")
    results: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []

    def install(library: str) -> tuple[str, str, str, dict[str, str] | None]:
        return install_gpu_library(library, root, logs / f"{library}.txt")

    from tqdm import tqdm

    for batch_start in range(0, len(libraries), 3):
        batch = libraries[batch_start : batch_start + 3]
        installs: dict[str, tuple[str, str, str, dict[str, str] | None]] = {}
        log(f"=== install batch: {', '.join(batch)} ===")

        with ThreadPoolExecutor(max_workers=len(batch)) as pool:
            futures = {pool.submit(install, library): library for library in batch}
            pending = set(futures)
            with tqdm(total=len(futures), desc="installing", unit="lib") as progress:
                while pending:
                    done, pending = wait(pending, timeout=5, return_when=FIRST_COMPLETED)
                    for future in done:
                        library = futures[future]
                        try:
                            installs[library] = future.result()
                            tqdm.write(f"{library}: install complete")
                        except Exception as exc:
                            failures.append({"library": library, "error": str(exc)})
                            tqdm.write(f"{library}: install failed: {exc}")
                        print_log_edges(library, logs / f"{library}.txt")
                        progress.update(1)
                    for future in pending:
                        library = futures[future]
                        line = last_log_line(logs / f"{library}.txt")
                        if line:
                            tqdm.write(f"{library}: {line}")

        log("\n" + "=" * 72 + "\nBATCH INSTALLATIONS COMPLETE, MOVING TO WORK\n" + "=" * 72)

        for library in batch:
            if library not in installs:
                continue
            command, version, version_url, command_env = installs[library]
            try:
                log(f"=== benchmark {library} ===")
                times: list[int] = []
                for i in range(11):
                    start = time.perf_counter_ns()
                    proc = run(
                        command,
                        capture=True,
                        env=command_env,
                        check=False,
                    )
                    elapsed_ms = (time.perf_counter_ns() - start) // 1_000_000
                    if proc.returncode != 0:
                        print(proc.stdout, file=sys.stderr)
                        print(proc.stderr, file=sys.stderr)
                        raise subprocess.CalledProcessError(proc.returncode, command)
                    times.append(elapsed_ms)
                    log(f"  Run {i + 1}/11: {elapsed_ms}ms")

                results.append(
                    {
                        "library": library,
                        "version": version,
                        "version_url": version_url,
                        "cold_ms": times[0],
                        "warm_ms": sum(times[1:]) // 10,
                        "times": times,
                    }
                )
            except Exception as exc:
                failures.append({"library": library, "error": str(exc)})
                log(f"{library} failed: {exc}")

        for library in batch:
            safe_library = re.sub(r"[^A-Za-z0-9_.-]+", "-", library)
            shutil.rmtree(root / "venvs" / safe_library, ignore_errors=True)
            shutil.rmtree(root / "src" / library, ignore_errors=True)
            if library == "llama.cpp":
                shutil.rmtree(root / "llama-bin", ignore_errors=True)
                (root / "llama.tar.gz").unlink(missing_ok=True)
        run("uv cache prune --ci --force", check=False)

    Path(args.output).write_text(json.dumps({"results": results, "failures": failures}, indent=2))
    log(f"Wrote GPU results to {args.output}")


def cmd_vast_rent(args: argparse.Namespace) -> None:
    ssh_public_key = Path(args.ssh_public_key).expanduser().read_text().strip()
    if not ssh_public_key:
        sys.exit("SSH public key is empty")
    onstart = (
        "mkdir -p /root/.ssh; "
        "touch /root/.ssh/authorized_keys; "
        f"printf '\\n%s\\n' {q(ssh_public_key)} >> /root/.ssh/authorized_keys; "
        "chown -R root:root /root/.ssh; "
        "chmod 700 /root/.ssh; "
        "chmod 600 /root/.ssh/authorized_keys"
    )
    query = f"{args.query} dph_total<={args.max_price}"
    offers = json.loads(
        run(
            f"vastai --raw search offers --type on-demand {q(query)} "
            f"--storage {q(args.disk_gb)} --limit {args.limit} -o dph_total",
            capture=True,
        ).stdout
    )
    if not isinstance(offers, list):
        raise TypeError(f"Expected Vast offer list, got {type(offers).__name__}")

    max_price = float(args.max_price)
    offers = [
        offer for offer in offers if offer.get("dph_total") is not None and float(offer["dph_total"]) <= max_price
    ]
    offers.sort(key=lambda offer: float(offer.get("dph_total") or offer.get("dph") or "inf"))
    log(f"Found {len(offers)} on-demand offers under ${args.max_price}/hr total")

    for offer in offers[:5]:
        offer_id = str(offer.get("id") or offer.get("ask_contract_id") or "")
        price = offer.get("dph_total") or offer.get("dph")
        log(f"- {offer_id}: {offer.get('gpu_name', 'unknown GPU')}, price={price}")

    for offer in offers:
        offer_id = str(offer.get("id") or offer.get("ask_contract_id") or "")
        price = offer.get("dph_total") or offer.get("dph")
        if not offer_id or price is None:
            continue

        log(f"Trying on-demand offer {offer_id}: {offer.get('gpu_name', 'unknown GPU')}, price={price}")
        proc = run(
            f"vastai --raw create instance {q(offer_id)} --image {q(args.image)} "
            f"--disk {q(args.disk_gb)} --ssh --direct --cancel-unavail --label {q(args.label)} "
            f"--onstart-cmd {q(onstart)}",
            capture=True,
            check=False,
        )
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
        info = json.loads(run(f"vastai --raw show instance {q(args.instance_id)}", capture=True).stdout)
        print(json.dumps(info, indent=2))
        host = str(info.get("public_ipaddr") or "")
        ports = info.get("ports") or {}
        port_22 = ports.get("22/tcp") if isinstance(ports, dict) else None
        port = str(port_22[0].get("HostPort") if port_22 else "")
        if info.get("actual_status") == "running" and info.get("intended_status") == "running" and host and port:
            break
        time.sleep(10)

    if info.get("actual_status") != "running" or info.get("intended_status") != "running":
        sys.exit("Vast instance did not reach running state")

    if not host or not port:
        sys.exit("Vast instance is missing direct SSH target")

    ssh_command = (
        f"ssh -i {q(args.ssh_private_key)} -p {q(port)} -o IdentitiesOnly=yes "
        "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "
        f"-o ConnectTimeout=10 {q(f'root@{host}')} echo ok"
    )

    for _ in range(args.ssh_attempts):
        proc = run(ssh_command, capture=True, check=False)
        if proc.stdout:
            print(proc.stdout, end="")
        if proc.stderr:
            print(proc.stderr, end="", file=sys.stderr)
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


def cmd_gpu_update(args: argparse.Namespace) -> None:
    payload = json.loads(Path(args.results).read_text())
    info = json.loads(run(f"vastai --raw show instance {q(args.instance_id)}", capture=True).stdout)
    gpu_count = int(info.get("num_gpus") or info.get("gpu_count") or 1)
    gpu_name = str(info.get("gpu_name") or "unknown GPU")
    cpu_name = " ".join(str(info.get("cpu_name") or "unknown CPU").split())
    hardware = f"CPU: {cpu_name}; GPU: {gpu_count}x {gpu_name}"
    measurements = read_measurements()
    run_url = (
        f"{os.getenv('GITHUB_SERVER_URL', 'https://github.com')}/"
        f"{os.getenv('GITHUB_REPOSITORY')}/actions/runs/"
        f"{os.getenv('GITHUB_RUN_ID')}"
    )

    for result in payload.get("results", []):
        measurement = Measurement(
            library=result["library"],
            version=str(result["version"]),
            version_url=str(result["version_url"]),
            cold_ms=int(result["cold_ms"]),
            warm_ms=int(result["warm_ms"]),
            run_url=run_url,
            last_updated=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
            hardware=hardware,
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


def main() -> None:
    if len(sys.argv) == 1:
        sys.exit("usage: work.py {gpu-run,gpu-update,rebuild,vast-destroy,vast-rent,vast-wait}")
    command = sys.argv[1]
    p = argparse.ArgumentParser()

    if command == "gpu-run":
        p.add_argument("--libraries", default="all")
        p.add_argument("--output", required=True)
        p.add_argument("--root", default="/root/dashdashhelp-gpu")
        cmd_gpu_run(p.parse_args(sys.argv[2:]))
        return

    if command == "gpu-update":
        p.add_argument("--results", required=True)
        p.add_argument("--instance-id", required=True)
        cmd_gpu_update(p.parse_args(sys.argv[2:]))
        return

    if command == "rebuild":
        rebuild_html()
        update_readme()
        return

    if command == "vast-destroy":
        p.add_argument("--instance-id", required=True)
        args = p.parse_args(sys.argv[2:])
        run(f"vastai destroy instance {q(args.instance_id)} -y")
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

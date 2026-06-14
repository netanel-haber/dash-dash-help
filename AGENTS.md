# Repository instructions

## Project

`dashdashhelp.win` is a static dashboard for `--help` startup latency of LLM CLI tools.

Goal: every benchmarked `--help` command under `1000ms`.

Tagline: `Let's help help help devs`

Repo: `https://github.com/netanel-haber/dash-dash-help`

## Style

- Be terse.
- Keep code readable and boring.
- Keep the dashboard text-first.
- Keep the site static.
- Do not add frontend build tooling unless asked.
- Prefer small edits over broad refactors.

## Current architecture

- `measurements.csv`: benchmark data source of truth.
- `index.html`: generated static dashboard with inline CSS.
- `README.md`: generated markdown table for GitHub.
- `work.py`: GPU benchmark runner, Vast rental, CSV upsert, HTML/README rebuild, commit, rebase, push.
- `.nojekyll`: keep GitHub Pages from applying Jekyll.
- `CNAME`: custom domain.

Do not hand-edit generated benchmark rows in `index.html` or `README.md` as the primary data change. Update `measurements.csv` or run the benchmark flow, then regenerate.

## Data contract

CSV fields:

```text
library,version,version_url,cold_ms,warm_ms,run_url,last_updated,hardware,hardware_url
```

Dashboard columns:

```text
library | cold | warm (10 runs) | version | hardware | measured on
```

- `cold_ms`: first run.
- `warm_ms`: integer average of runs 2-11.
- `last_updated`: UTC ISO 8601 timestamp, for example `2026-06-05T15:47Z`.
- Times link to the GitHub Actions run.
- Versions link to the release tag or exact commit.
- Hardware links to a public Vast GPU-kind search, not a private instance page.
- Use `class="ok"` for times `<1000ms`.
- Use `class="slow"` for times `>=1000ms`.
- Sort dashboard rows by `warm_ms` descending.
- Sort README rows by `warm_ms` descending.

## Commands

Regenerate generated files from CSV:

```bash
python3 work.py rebuild
```

Local GPU runner syntax:

```bash
python3 work.py gpu-run --libraries 'vllm sglang' --output /tmp/dashdashhelp-gpu-results.json --root /tmp/dashdashhelp-gpu
```

## Benchmark behavior

- `work.py gpu-run` runs each benchmark 11 times.
- Cold time is run 1.
- Warm time is the integer average of runs 2-11.
- GPU libraries install in batches of 3, benchmark immediately, then delete their venv/source before the next batch.
- `work.py gpu-run` fails a library if its benchmark command exits non-zero.
- Verify suspicious `0ms` or `1ms` results; they often mean the command failed fast.
- `work.py` commits `measurements.csv`, `index.html`, and `README.md`.
- `work.py` rebases before push and retries pushes.

## Workflows

- `all-gpu.yml` is the benchmark workflow.
- Benchmark workflow runs are manual only: `workflow_dispatch`.
- `all-gpu.yml` rents one cheapest matching on-demand Vast RTX 5060 Ti GPU, uses direct SSH, runs selected libraries on that instance, updates the table, then destroys it.
- Vast GPU rentals require RTX 5060 Ti, non-VM-capable hosts (`vms_enabled=false`), reliability above `0.99`, disk bandwidth at least `500 MB/s`, at least `500 Mbps` download, and download bandwidth cost at most `$4/TB`.
- Vast price filtering must use `dph_total`, so the `$0.25/hr` cap includes disk cost.
- Vast SSH uses one pre-created keypair. The private key lives in the `VAST_SSH_PRIVATE_KEY` GitHub secret.
- `all-gpu.yml` derives the public key from that secret and passes it to `work.py vast-rent`.
- `work.py vast-rent` injects that public key into `/root/.ssh/authorized_keys` with `--onstart-cmd`, then fixes ownership and mode.
- Do not create or attach Vast SSH keys per run.
- Current GPU image is CUDA 13 because latest TensorRT-LLM needs CUDA 13 runtime libraries.
- `libraries` defaults to `all`.
- `libraries` accepts whitespace or comma lists: `vllm sglang`, `vllm,sglang`.
- Benchmark jobs need `contents: write`.
- Use `astral-sh/setup-uv` and `uv` for Python package workflows.
- Use Python `3.12` for GPU benchmark environments.
- Use `uv venv` and `uv pip install`, not `pip`.
- Use latest library versions.
- After workflow changes, GitHub may take about `30s` before `workflow_dispatch` is visible.

Run all:

```bash
gh workflow run all-gpu.yml --ref main
```

Run selected libraries:

```bash
gh workflow run all-gpu.yml --ref main -f libraries='vllm sglang'
```

## Active benchmarks

| Library | Command |
| --- | --- |
| `vllm` | `vllm --help` |
| `sglang` | `python -m sglang.launch_server --help` |
| `VLMEvalKit` | `python run.py --help` |
| `transformers` | `transformers --help` |
| `tensorrt-llm` | `trtllm-serve --help` |
| `datasets` | `datasets-cli --help` |
| `llm` | `llm --help` |
| `openai` | `openai --help` |
| `langchain-cli` | `langchain --help` |
| `hf` | `hf --help` |
| `lm-eval` | `lm-eval --help` |
| `llama.cpp` | `llama-cli --help` |
| `ollama` | `ollama --help` |
| `tokenspeed` | `tokenspeed --help` |

## Package gotchas

- `tokenspeed`: install from the latest `lightseekorg/tokenspeed` `main` commit, subdirectory `python`; version URL points to the exact commit.
- `llama.cpp`: download the latest plain Ubuntu x64 GitHub release binary tarball; avoid OpenVINO/ROCm/SYCL/Vulkan variants.
- `vllm`: install latest release tag from GitHub with `VLLM_USE_PRECOMPILED=1` and `--index-strategy unsafe-best-match`.
- `VLMEvalKit`: clone latest release tag and install from source with `uv pip install -e .`.
- `tensorrt-llm`: free disk space first; install `tensorrt-llm`, `click`, and `pynvml`; benchmark `trtllm-serve --help`, not `trtllm --help`.
- `sglang`: install latest PyPI package.
- `transformers`: install latest `transformers[serving]` plus `requests`; benchmark the official `transformers --help` entrypoint.

## YAML gotchas

- YAML can choke on `[[index]]` inside heredocs. Prefer `printf`:

  ```yaml
  printf '%s\n' '[[index]]' 'name = "torch"' ... > file.toml
  ```

- Multiple workflows can push to the same branch. Rebase before pushing.

## DNS

- `ALIAS`: `dashdashhelp.win` -> `netanel-haber.github.io`
- `CNAME`: `www.dashdashhelp.win` -> `netanel-haber.github.io`

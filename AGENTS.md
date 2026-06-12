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
- `work.py`: benchmark, CSV upsert, HTML rebuild, commit, rebase, push.
- `update_readme.py`: README table rebuild from `measurements.csv`.
- `.nojekyll`: keep GitHub Pages from applying Jekyll.
- `CNAME`: custom domain.
- `.cirun.yml`: temporary Cirun GPU runner config for the vLLM GPU trial.

Do not hand-edit generated benchmark rows in `index.html` or `README.md` as the primary data change. Update `measurements.csv` or run the benchmark flow, then regenerate.

## Data contract

CSV fields:

```text
library,version,version_url,cold_ms,warm_ms,run_url,last_updated
```

Dashboard columns:

```text
library | cold | warm (10 runs) | version | measured on
```

- `cold_ms`: first run.
- `warm_ms`: integer average of runs 2-11.
- `last_updated`: UTC ISO 8601 timestamp, for example `2026-06-05T15:47Z`.
- Times link to the GitHub Actions run.
- Versions link to the release tag or exact commit.
- Use `class="ok"` for times `<1000ms`.
- Use `class="slow"` for times `>=1000ms`.
- Sort dashboard rows by `warm_ms` descending.
- `README.md` preserves CSV order.

## Commands

Regenerate README from CSV:

```bash
python3 update_readme.py
```

Local benchmark smoke test:

```bash
python3 work.py "<command>" --library <name> --version <version> --version-url <url> --dry-run
```

Use `--dry-run` locally unless intentionally committing and pushing.

## Benchmark behavior

- `work.py` defaults to 11 runs.
- Cold time is run 1.
- Warm time is the integer average of runs 2-11.
- `work.py` captures output but does not fail on a non-zero benchmark command.
- Verify suspicious `0ms` or `1ms` results; they often mean the command failed fast.
- Commit format is currently `{library}: cold_ms={cold}/warm_ms={warm} @ {version}`.
- `work.py` commits only `measurements.csv` and `index.html`.
- `work.py` rebases before push and retries pushes.

## Workflows

- Benchmark workflows are manual only: `workflow_dispatch`.
- `update-readme.yml` is the only scheduled workflow: daily `0 0 * * *`.
- `all.yml` manually triggers benchmark workflows sequentially and watches each run.
- `vllm-gpu.yml` is a temporary manual Cirun trial. It updates the existing `vllm` row, not a `vllm-gpu` row.
- Benchmark jobs need `contents: write`.
- `all.yml` needs `actions: write`.
- Use `astral-sh/setup-uv` and `uv` for Python package workflows.
- Use `uv venv` and `uv pip install`, not `pip`.
- Use published PyPI versions for normal Python packages; pin only when needed.
- After workflow changes, GitHub may take about `30s` before `workflow_dispatch` is visible.

`all.yml` order:

```text
ollama hf datasets llm openai langchain-cli llama-cpp lm-eval transformers tokenspeed tensorrt-llm sglang vllm vlmevalkit update-readme
```

## Active benchmarks

| Library | Workflow | Command |
| --- | --- | --- |
| `ollama` | `ollama.yml` | `ollama --help` |
| `hf` | `hf.yml` | `.venv/bin/hf --help` |
| `datasets` | `datasets.yml` | `.venv/bin/datasets-cli --help` |
| `llm` | `llm.yml` | `.venv/bin/llm --help` |
| `openai` | `openai.yml` | `.venv/bin/openai --help` |
| `langchain-cli` | `langchain-cli.yml` | `.venv/bin/langchain --help` |
| `llama.cpp` | `llama-cpp.yml` | `./llama-bin/llama-cli --help` |
| `lm-eval` | `lm-eval.yml` | `.venv/bin/lm-eval --help` |
| `transformers` | `transformers.yml` | `.venv/bin/transformers-cli --help` |
| `tokenspeed` | `tokenspeed.yml` | `.venv/bin/tokenspeed --help` |
| `tensorrt-llm` | `tensorrt-llm.yml` | `.venv/bin/trtllm-serve --help` |
| `sglang` | `sglang.yml` | `.venv/bin/python -m sglang.launch_server --help` |
| `vllm` | `vllm.yml` | `.venv/bin/vllm --help` |
| `vllm` | `vllm-gpu.yml` | `.venv/bin/vllm --help` |
| `VLMEvalKit` | `vlmevalkit.yml` | `./VLMEvalKit/.venv/bin/python ./VLMEvalKit/run.py --help` |

## Package gotchas

- `openai`: pinned to `2.34.0`; `2.35.0` removed the legacy Python CLI.
- `tokenspeed`: install from the latest `lightseekorg/tokenspeed` `main` commit, subdirectory `python`, with `--torch-backend cpu`; version URL points to the exact commit.
- `llama.cpp`: download latest GitHub release binary tarball; no `uv`.
- `vllm`: install latest release tag from GitHub with `VLLM_TARGET_DEVICE=cpu`, `VLLM_USE_PRECOMPILED=1`, `--index-strategy unsafe-best-match`, and PyTorch CPU extra index.
- `vllm-gpu`: temporary Cirun/Vast.ai workflow. It uses runner label `cirun-vllm-gpu--${{ github.run_id }}`, installs PyPI `vllm`, probes with `nvidia-smi`, and writes to library `vllm`.
- `vllm-experimental`: dry-run only; benchmarks `python3 -m vllm.hello` from a specific fork commit and does not update data.
- `VLMEvalKit`: clone latest release tag and install from source with `uv pip install -e .`.
- `tensorrt-llm`: free disk space first; install `tensorrt-llm`, `click`, and `pynvml`; benchmark `trtllm-serve --help`, not `trtllm --help`.
- `sglang`: clone latest release tag, use Python `3.12`, copy `python/pyproject_cpu.toml` to `python/pyproject.toml`, install from source, and set `SGLANG_USE_CPU_ENGINE=1` for benchmark.
- `transformers`: install `transformers torch` with PyTorch CPU extra index.

## Removed or historical behavior

- Do not bring back the install column.
- Do not bring back the PR column.
- Do not bring back screenshot automation.
- Do not bring back `html_to_markdown.py`; README generation is now `update_readme.py` from CSV.
- Do not bring back `.github/workflows/sort.yml`; sorting happens in `work.py`.
- Do not add cron schedules to benchmark workflows unless asked.
- Do not recreate `.github/copilot-instructions.md` or `screenshot.png` unless asked.
- `CLAUDE.md` was replaced by `AGENTS.md`; keep repo instructions here.

## YAML gotchas

- YAML can choke on `[[index]]` inside heredocs. Prefer `printf`:

  ```yaml
  printf '%s\n' '[[index]]' 'name = "torch"' ... > file.toml
  ```

- Multiple workflows can push to the same branch. Rebase before pushing.

## DNS

- `ALIAS`: `dashdashhelp.win` -> `netanel-haber.github.io`
- `CNAME`: `www.dashdashhelp.win` -> `netanel-haber.github.io`

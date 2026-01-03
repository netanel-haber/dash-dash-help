# Claude Code Memory for dash-dash-help

## Project Overview
Dashboard at https://dashdashhelp.win tracking `--help` performance for LLM CLI tools.
Goal: Make `--help` < 200ms. Tagline: "Let's help help help devs"

## User Preferences
- **Minimal, terse, no AI slop** - keep everything simple and text-focused
- **Single file for dashboard** - index.html with inline `<style>`
- **Single source of truth** - GitHub Actions update index.html directly via upsert
- **Link everything** - time links to workflow run, version links to GitHub release tag
- **Use uv** not pip for Python installs
- **Published versions** from PyPI, not nightly/commit builds

## Table Structure
```
library | command | time | version
```
- library: colloquial name for the library/tool
- command: the actual CLI command benchmarked (e.g., `ollama --help`)
- time: links to GitHub Actions run, class="ok" if <200ms, class="slow" if >=200ms
- version: links to `github.com/{org}/{repo}/releases/tag/v{version}`

## Workflow Pattern
Each tool has its own `.github/workflows/{tool}.yml` that:
1. Installs the tool
2. Gets version via `uv pip show` (Python) or tool-specific command
3. Runs `python3 work.py` which:
   - Benchmarks `{tool} --help` using Python's `time.time_ns()`
   - Upserts row in index.html (using `id="{tool}"` to find row)
   - Commits with message `{tool}: {time}ms @ {version}`
   - Handles `git pull --rebase` for race conditions

## Tools Status
- **ollama**: ~14ms (Go binary, fast) ✓
- **llama.cpp**: ~30ms (C++ binary, fast) ✓
- **lm-eval**: ~49ms (Python, fast!) ✓
- **hf**: ~860ms (Python)
- **tensorrt-llm**: ~8200ms (trtllm-serve --help)
- **transformers**: ~8600ms (Python, slow)
- **sglang**: ~12000ms (Python, requires CPU build from source)
- **vllm**: ~16000ms (Python, requires CPU build from source)
- **vlmeval**: ~19400ms (Python, use `ms-vlmeval` package not `vlmeval`)

## Package Name Gotchas
- **vlmeval**: Package is `ms-vlmeval` on PyPI, CLI is `vlmutil`
- **tensorrt-llm**: Use `trtllm-serve --help` not `trtllm --help`
- **sglang**: Requires building from source for CPU, not available as simple pip install

## sglang CPU Build Requirements
Requires these apt packages for sgl-kernel build:
```
gcc-13 g++-13 libtcmalloc-minimal4 libtbb-dev cmake libnuma-dev numactl
```
Must use `pyproject_cpu.toml` and build sgl-kernel from source.

## Workflow YAML Gotchas
- **Heredocs with `[[`**: YAML parsers choke on `[[index]]` in heredocs. Use `printf` instead:
  ```yaml
  printf '%s\n' '[[index]]' 'name = "torch"' ... > file.toml
  ```
- **GitHub caches workflow metadata**: After pushing workflow changes, may need to wait ~30s for `workflow_dispatch` to be recognized
- **Race conditions**: Multiple workflows pushing to same branch need `git pull --rebase` before push

## Key Files
- `index.html` - dashboard with inline styles
- `favicon.svg` - vectorized "--help" text
- `CNAME` - custom domain dashdashhelp.win
- `.github/workflows/*.yml` - per-tool benchmark workflows

## DNS Setup (Porkbun)
- ALIAS: dashdashhelp.win → netanel-haber.github.io
- CNAME: www.dashdashhelp.win → netanel-haber.github.io

## GitHub Repo
https://github.com/netanel-haber/dash-dash-help

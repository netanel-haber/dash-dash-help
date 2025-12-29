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
tool | time | version | command | pr
```
- time: links to GitHub Actions run, class="ok" if <200ms, class="slow" if >=200ms
- version: links to `github.com/{org}/{repo}/releases/tag/v{version}`
- command: the actual CLI command benchmarked (e.g., `ollama --help`)
- pr: for tracking fix PRs (future)

## Workflow Pattern
Each tool has its own `.github/workflows/{tool}.yml` that:
1. Installs the tool
2. Gets version via `uv pip show` (Python) or tool-specific command
3. Benchmarks `{tool} --help` using `date +%s%N` for nanosecond timing
4. Checkouts repo
5. Upserts row in index.html via sed (using `id="{tool}"` to find row)
6. Commits with message `{tool}: {time}ms @ {version}`

## Tools Status
- **ollama**: Working, ~13ms (Go binary, fast)
- **transformers**: Working, ~8000ms (Python, slow)
- **vllm**: Broken - requires GPU detection even for --help (document this failure)
- **sglang**: TBD
- **llama.cpp**: TBD

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

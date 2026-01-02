# Copilot instructions for dash-dash-help

Purpose: Help an AI coding agent be immediately productive in this repo by documenting the repo's conventions, workflows, and small gotchas — not general software advice.

## Big picture
- Single-page dashboard: `index.html` is the single source-of-truth (inline styles + table of tools). Changes are authored by GitHub Actions workflows and occasionally by humans.
- Per-tool workflows live in `.github/workflows/*.yml`. Each workflow: install tool → get version → benchmark `--help` → checkout → update `index.html` via `scripts/update_row.py` → commit & push.
- `scripts/update_row.py` builds a new `<tr id="{tool}">...</tr>` and replaces the existing row by id.

## Key files
- `index.html` — dashboard markup and table rows (row `id` values are canonical tool identifiers).
- `scripts/update_row.py` — CLI used by workflows to upsert rows. The table columns are: `command | library | time | version | install | pr`. It expects the row `id` to exist and will fail if not found.
- `.github/workflows/*.yml` — per-tool benchmark flows (see `ollama.yml` as a short, representative example).
- `CLAUDE.md` — useful human-maintained notes and gotchas (install tips, apt packages for CPU builds, YAML quirks).

## Project-specific conventions (actionable)
- Use `uv` wrapper for Python envs and installs (e.g., `uv venv`, `uv pip install ...`, `uv pip show ...`) — workflows rely on it.
- Tool identity: workflows pass `--id <tool>` to `scripts/update_row.py`; that `id` must match an existing `<tr id="...">` in `index.html`.
- Library column: workflows pass `--library "<Name>"` to `scripts/update_row.py`; defaults to `-`.
- Install cell can contain HTML/`<details>` markup (passed as raw HTML to `--install`).
- Speed threshold: rows use CSS classes **ok** (`time_ms < 200`) or **slow** (>=200). `scripts/build_row` enforces this logic.
- Commit message format: `{tool}: {time_ms}ms @ {version}` — keep this format to maintain history consistency.

## Typical workflow authoring checklist (what to add when adding a new tool)
1. Add a `<tr id="<tool>">...</tr>` to `index.html` with proper HTML for `install` and a placeholder time/version (or copy an existing row).  
2. Add `.github/workflows/<tool>.yml` following existing patterns (see `ollama.yml` / `transformers.yml`):
   - Install step (prefer `uv` where appropriate)
   - Extract version (e.g., `VERSION=$(uv pip show <pkg> | grep Version | cut -d' ' -f2)` or tool-specific command)
   - Benchmark: `start=$(date +%s%N); <tool> --help > /dev/null; end=$(date +%s%N); ms=$(( (end-start)/1000000 ))`
   - Use `python3 scripts/update_row.py ...` with `--id`, `--command`, `--library`, `--time-ms`, `--version`, `--version-url`, `--run-url`, `--install`.
   - Commit & push. **Important:** do a `git pull --rebase` before push to avoid race-condition conflicts between concurrent runs.

## YAML / CI gotchas to keep in mind
- Avoid heredocs in GH Action step bodies that contain `[[index]]` or similar bracketed strings — some YAML parsers / templating can choke. Use `printf` for stable output where needed (see `CLAUDE.md`).
- Workflows may push back to the default branch; use `permissions.contents: write` and `git pull --rebase` to handle concurrent pushes.

## Testing & debugging tips
- To test the row update locally: run
  ```bash
  python3 scripts/update_row.py --file index.html \
    --id ollama --command "ollama --help" --time-ms 13 \
    --version 0.13.5 --version-url "https://github.com/ollama/ollama/releases/tag/v0.13.5" \
    --run-url "https://example" --install '<code>curl -fsSL https://ollama.com/install.sh | sh</code>'
  ```
- If `scripts/update_row.py` exits with "Row not found", add the `<tr id="...">` first or ensure you used the correct id.
- To debug workflows, use manual `workflow_dispatch` or the `all.yml` dispatcher to trigger multiple workflows.

## Notable environment / build notes (discoverable in `CLAUDE.md`)
- Some tools (e.g., `sglang`, `vllm`) require extra system packages and CPU-specific build steps (apt packages like `gcc-13`, `libnuma-dev`, `cmake`, etc.). See `CLAUDE.md` for details.
- Prefer published PyPI releases (tags/versions) rather than nightly builds where possible.

## Small, explicit examples (from this repo)
- Row id mapping: `index.html` contains `<tr id="vllm">` and the `vllm.yml` workflow calls
  `python3 scripts/update_row.py --id vllm --command "vllm --help" ...`
- Commit message example: `ollama: 13ms @ 0.13.5`

---
If any piece of this is unclear or you want more examples added (e.g., a copy-paste workflow template), tell me which part to expand and I will iterate. ✅
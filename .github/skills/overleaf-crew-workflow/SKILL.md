---
name: overleaf-crew-workflow
description: Figure wiring SSOT for stepdllm-overleaf — manifest.json schema, regenerate_figures.py CLI, README table sync. For locks, commits, LaTeX loop, and DAG rules, use skill stepdllm-overleaf-workflow.
---

**Process (locks, commits, TeX, coordination, DAG):** see **`.github/skills/stepdllm-overleaf-workflow/SKILL.md`** — do not duplicate those rules here.

## Figure wiring

- Treat committed **PDF** under `figures/` as the vector SSOT for `\includegraphics`.
- **`figures/manifest.json`** is the wiring contract: each entry has `id`, `generator` (Python path under `scripts/`), `output` (PDF path), and `cited_in` (`.tex` fragments). When adding or renaming a figure, **update the manifest first**, then align `README.md` (or regenerate the README table from the manifest when that automation exists).
- **Batch regen:** `python3 scripts/regenerate_figures.py` runs every generator. Use `python3 scripts/regenerate_figures.py --dry-run`, `--list`, or `--only <id>` for CI and spot fixes.
- **Interim navigation:** session artifact `CODEBASE_ARCHITECTURE_MAP.md` (architect) cross-checks manifest ↔ TeX until CI validates the manifest on every change.

## Knowledge

- One-off analyses belong in session artifacts; **reusable** conventions belong in `.github/skills/<name>/SKILL.md` with YAML `name` and `description`.

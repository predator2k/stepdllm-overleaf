---
name: overleaf-crew-workflow
description: Use when editing this NeurIPS/Overleaf paper repo with multiple agents — file locks, commits, LaTeX builds, PDF figures, and coordination.
---

## Before you edit

- Acquire a lock on every path you will touch (Flightdeck `LOCK_FILE`, or your crew’s equivalent) before changing tracked files.
- If another agent may touch the same path, coordinate in group chat or with direct @mentions.

## Commits

- Stage only files you locked or intentionally changed — never `git add -A` in a shared tree.
- Prefer the crew `COMMIT` command when it scopes to locked paths; otherwise `git add <paths>` then commit.

## After substantive changes

- When a TeX distribution is available, run the project LaTeX build to PDF after meaningful edits (figures, `.tex`, bibliography) so regressions surface immediately.

## Figures

- Treat generated **PDF** under `figures/` as the single source of truth for vector figures when the paper includes them.
- **Wiring contract:** `figures/manifest.json` lists each figure’s `id`, `generator` (Python path), `output` (PDF path), and `cited_in` (`.tex` fragments). When adding or renaming a figure, update the manifest first; keep `README.md` in sync or regenerate its table from the manifest.
- **Batch regen:** `python3 scripts/regenerate_figures.py` runs every generator; `python3 scripts/regenerate_figures.py --dry-run`, `--list`, and `--only <id>` are supported for CI and spot fixes.
- Regenerate from `scripts/*.py` when the visual or data story changes; avoid maintaining duplicate raster sources unless there is an explicit print-only exception.

## Knowledge

- Capture non-obvious, repeatable repo conventions as new files under `.github/skills/<hyphenated-name>/SKILL.md` with YAML `name` and `description` so future sessions load the right context.

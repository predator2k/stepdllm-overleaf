---
name: stepdllm-overleaf-workflow
description: Single SSOT for stepdllm-overleaf — Flightdeck locks, scoped commits, LaTeX+bibtex loop, figure manifest/regen, coordination, DAG hints.
---

## Editing and version control

- Acquire **LOCK_FILE** on every path you edit (or create) before changing it; release with **UNLOCK_FILE** when done.
- Commit with **COMMIT** (Flightdeck) so only **locked** paths are staged—never `git add -A`, which picks up other agents’ work.
- If using plain `git`, stage **explicit paths** only (e.g. `git add path/to/file.tex`).

## LaTeX build

- After each **substantive** change, run a full PDF build **when a TeX distribution is available** on `PATH`:

```sh
pdflatex -interaction=nonstopmode neurips_2026.tex
bibtex neurips_2026
pdflatex -interaction=nonstopmode neurips_2026.tex
pdflatex -interaction=nonstopmode neurips_2026.tex
```

- Doc-only tweaks (e.g. comments with no rebuild impact) still benefit from a build when TeX is present; skip only when the environment has no TeX.

## Figures and wiring

- Prefer committed **PDF** under `figures/` as the vector SSOT for `\includegraphics`.
- Script names do not always match PDF filenames; use **`figures/manifest.json`**, `README.md`, or `grep includegraphics`—do not guess from filenames alone.
- **`figures/manifest.json`** is the wiring contract: each entry has `id`, `generator` (Python path under `scripts/`), `output` (PDF path), and `cited_in` (`.tex` fragments). When adding or renaming a figure, **update the manifest first**, then align `README.md` (or regenerate the README table from the manifest when that automation exists).
- **Batch regen:** `python3 scripts/regenerate_figures.py` runs every generator. Use `python3 scripts/regenerate_figures.py --dry-run`, `--list`, or `--only <id>` for CI and spot fixes.
- **Interim navigation:** session artifact `CODEBASE_ARCHITECTURE_MAP.md` (architect) cross-checks manifest ↔ TeX until CI validates the manifest on every change.

## Coordination

- Overlapping files: use **group chat**, **CREATE_GROUP** / **GROUP_MESSAGE**, or **DIRECT_MESSAGE** with **@mentions** (agent id with `@` prefix) so two agents do not fight the same path.

## Reusable knowledge

- Patterns that help **future** sessions (not one-off reports) belong in **`.github/skills/<skill-name>/SKILL.md`** with YAML `name` and `description` plus short, actionable body text.

## Task DAG

- When the lead defines multi-step work, they should use **DECLARE_TASKS** so dependencies and **dagTaskId** bindings stay consistent; the secretary can track with **QUERY_TASKS** / **TASK_STATUS**.
- Post **COMPLETE_TASK** with **`dagTaskId`** (and summary) so the secretary can close rows without ID drift.

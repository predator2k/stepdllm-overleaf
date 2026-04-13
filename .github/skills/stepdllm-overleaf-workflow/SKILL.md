---
name: stepdllm-overleaf-workflow
description: Flightdeck crew conventions for this NeurIPS LaTeX repo—locks, commits, PDF builds, figures, and where to record reusable wisdom.
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

## Figures

- Prefer **PDF** under `figures/` as the single source of truth committed to the repo.
- Regenerate from `scripts/` as documented in `README.md` (table maps `\\includegraphics` → script → output PDF).
- Script names do not always match PDF filenames; use the README table or `grep includegraphics` instead of guessing.

## Coordination

- Overlapping files: use **group chat**, **CREATE_GROUP** / **GROUP_MESSAGE**, or **DIRECT_MESSAGE** with **@mentions** (agent id with `@` prefix) so two agents do not fight the same path.

## Reusable knowledge

- Patterns that help **future** sessions (not one-off reports) belong in **`.github/skills/<skill-name>/SKILL.md`** with YAML `name` and `description` plus short, actionable body text.

## Task DAG

- When the lead defines multi-step work, they should use **DECLARE_TASKS** so dependencies and **dagTaskId** bindings stay consistent; the secretary can track with **QUERY_TASKS** / **TASK_STATUS**.

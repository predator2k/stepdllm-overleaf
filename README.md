# Step-dLLM (NeurIPS draft)

LaTeX for the Step-dLLM paper. Figure PDFs under `figures/` are generated from `scripts/`; plot data are **synthetic or estimated** unless you replace the generators with real runs.

## Minimal workflow (repo root)

All shell snippets below use **`python3`** (not `python`) so copy-paste stays portable on hosts where `python` is absent or not Python 3.

**1 — Verify plotters (fast, no PDF writes required for most tests)**

```sh
python3 scripts/plot_attention_budget_curve_test.py
python3 scripts/plot_panels_6step_test.py
python3 scripts/figure_neurips_style_test.py
```

GitHub Actions runs the same three commands plus `python3 scripts/regenerate_figures.py --dry-run` on pushes to `main` and on all pull requests (see `.github/workflows/smoke.yml`). There is no `pdflatex` job in CI yet.

**2 — Regenerate committed vector figures**

Wiring is authoritative in `figures/manifest.json` (script → PDF → TeX consumers). The thin driver is:

```sh
python3 scripts/regenerate_figures.py
```

Use `python3 scripts/regenerate_figures.py --help` for `--dry-run`, `--list`, and `--only <id>`. Single-figure example: `python3 scripts/regenerate_figures.py --only panels_6step_2x3`.

**3 — Build the PDF** (requires a TeX distribution on `PATH`; many CI smoke hosts do **not** ship `pdflatex` — exit 127 means “install TeX or run this step locally”)

```sh
pdflatex -interaction=nonstopmode -halt-on-error neurips_2026.tex
bibtex neurips_2026
pdflatex -interaction=nonstopmode -halt-on-error neurips_2026.tex
pdflatex -interaction=nonstopmode -halt-on-error neurips_2026.tex
```

Resolve `bibtex` warnings (e.g. duplicate keys in `example_paper.bib`) if you need a clean bibliography pass.

## Figures: manifest and human-readable mirror

| Where used | Output file | Script |
|------------|-------------|--------|
| `01-intro.tex` (cross-step) | `figures/attention_multi_position.pdf` | `scripts/plot_cross_step_heatmap.py` |
| `01-intro.tex` (cross-step) | `figures/attention_similarity_curve.pdf` | `scripts/plot_kl_divergence.py` |
| `03-method.tex` (attention across steps) | `figures/panels_6step_2x3.pdf` | `scripts/plot_panels_6step.py` |
| `03-method.tex` (head heterogeneity **(a)**) | `figures/attention_heads_heatmap.pdf` | `scripts/plot_attention_heads_heatmap.py` |
| `03-method.tex` (head heterogeneity **(b)**) | `figures/attention_budget_cross_head.pdf` | `scripts/plot_attention_budget_curve.py` |
| `03-method.tex` (overview) | `figures/step_dllm_overview.pdf` | `scripts/plot_step_dllm_overview.py` |
| `04-results.tex` | `figures/kernel_speedup.pdf` | `scripts/plot_kernel_speedup.py` |

If this table disagrees with `figures/manifest.json`, **fix the manifest first** and refresh this table.

**Shared PDF style:** `scripts/figure_neurips_style.py` (`apply_neurips_style`); covered by `figure_neurips_style_test.py`.

**Emergency fallback** (no `regenerate_figures.py` — not preferred): from repo root,

```sh
for f in scripts/plot_*.py; do [[ "$f" == *_test.py ]] && continue; python3 "$f"; done
```

## Plotter CLIs (gotcha)

Orchestration flags live on **`regenerate_figures.py`**. Individual `scripts/plot_*.py` files may not use `argparse`; passing `--help` to a plotter can still execute `main()` and regenerate PDFs. Prefer `python3 scripts/regenerate_figures.py --help` and `python3 scripts/regenerate_figures.py --only <id>`.

## Tables

Numeric fragments live in `tables/*.tex` and are pulled in via `\input{...}` from `04-results.tex` and from the appendix block in `neurips_2026.tex`. When editing, keep `\multirow` usage consistent with existing tables.

## Naming note for agents

Script **filenames** do not always mirror PDF **filenames**. Use `figures/manifest.json`, `python3 scripts/regenerate_figures.py --list`, or `grep includegraphics *.tex` — do not guess from names alone.

## Crew reference

Interim navigation SSOT with TeX line anchors: session artifact `architect-e2e3176b/CODEBASE_ARCHITECTURE_MAP.md` (figure ↔ script ↔ TeX, table index, compile loop). When the manifest and that map disagree, trust **`figures/manifest.json`** for automation and update the map in the same change set if you can.

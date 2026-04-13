# Step-dLLM (NeurIPS draft)

LaTeX source for the Step-dLLM paper. Figures under `figures/` are regenerated from `scripts/` where noted; data in the plotters are **synthetic or estimated** from prior visuals unless you replace the generators with real runs.

## Build the PDF

From the repository root (TinyTeX or another TeX distribution on `PATH`):

```sh
pdflatex -interaction=nonstopmode neurips_2026.tex
bibtex neurips_2026
pdflatex -interaction=nonstopmode neurips_2026.tex
pdflatex -interaction=nonstopmode neurips_2026.tex
```

`bibtex` may exit with warnings (e.g. duplicate keys in `example_paper.bib`); fix entries if you need a clean bibliography pass.

## Regenerate figures (source of truth)

| Where used | Output file | Script |
|------------|-------------|--------|
| `01-intro.tex` (Fig. cross-step) | `figures/attention_multi_position.pdf` | `scripts/plot_cross_step_heatmap.py` |
| `01-intro.tex` (Fig. cross-step) | `figures/attention_similarity_curve.pdf` | `scripts/plot_kl_divergence.py` |
| `03-method.tex` (attention across steps) | `figures/panels_6step_2x3.pdf` | `scripts/plot_panels_6step.py` |
| `03-method.tex` (head heterogeneity **(a)**) | `figures/attention_heads_heatmap.pdf` | `scripts/plot_attention_heads_heatmap.py` |
| `03-method.tex` (head heterogeneity **(b)**) | `figures/attention_budget_cross_head.pdf` | `scripts/plot_attention_budget_curve.py` |
| `03-method.tex` (overview) | `figures/step_dllm_overview.pdf` | `scripts/plot_step_dllm_overview.py` (run before `pdflatex` if the PDF is not in `figures/`; commit the PDF for CI or add a build step that runs the script). |
| `04-results.tex` | `figures/kernel_speedup.pdf` | `scripts/plot_kernel_speedup.py` |

Run any script from the repo root or from `scripts/` (each resolves paths relative to the repo):

```sh
python3 scripts/plot_panels_6step.py
python3 scripts/plot_attention_budget_curve.py
```

### Tests

Plotters ship lightweight `unittest` smoke checks under `scripts/`:

```sh
python3 scripts/plot_attention_budget_curve_test.py
python3 scripts/plot_panels_6step_test.py
python3 scripts/figure_neurips_style_test.py
```

Run all three before committing figure or style changes; they finish in under a second on typical laptops.

## Naming note for agents

Script **filenames** do not always mirror PDF **filenames** (e.g. `plot_cross_step_heatmap.py` → `attention_multi_position.pdf`). Use the table above or `grep includegraphics` in the `.tex` files instead of guessing from names alone.

## Optional hardening (team proposal)

A small `scripts/figure_style.py` plus a manifest (expected `includegraphics` paths ↔ generator) reduces broken references when several agents touch figures. Add when a second script needs shared `rcParams`; avoid a large framework before two plotters share code.

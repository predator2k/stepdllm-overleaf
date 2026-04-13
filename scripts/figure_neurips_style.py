"""Shared Matplotlib settings for NeurIPS-style PDF figures (vector-friendly).

Use ``NEURIPS_SINGLE_COLUMN_IN`` / ``HALF_COLUMN_IN`` so Figure~1 panels
(authored as two separate PDFs at half-column width) match ``0.49\\columnwidth``
includes in ``01-intro.tex``.

Illustrative / schematic figures must be labeled in-figure per project policy;
callers add their own ``fig.text`` footnote after setting ``subplots_adjust``.
"""

from __future__ import annotations

import matplotlib.pyplot as plt

# Typical NeurIPS article \columnwidth (inches); tweak if your style differs.
NEURIPS_SINGLE_COLUMN_IN: float = 3.25
HALF_COLUMN_IN: float = NEURIPS_SINGLE_COLUMN_IN * 0.49


def apply_neurips_style(*, small: bool = True) -> None:
    """Update ``matplotlib.rcParams`` for PDF output (editable text, serif)."""
    params: dict[str, float | str | list[str] | bool | int] = {
        "font.family": "serif",
        "font.serif": [
            "Times New Roman",
            "Times",
            "Nimbus Roman",
            "DejaVu Serif",
            "Bitstream Vera Serif",
        ],
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.linewidth": 0.75,
        "xtick.major.width": 0.75,
        "ytick.major.width": 0.75,
        "lines.linewidth": 1.0,
        "lines.markersize": 3.0,
        "grid.linewidth": 0.4,
        "grid.alpha": 0.35,
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "savefig.format": "pdf",
    }
    if small:
        params.update(
            {
                "font.size": 7,
                "axes.labelsize": 7,
                "axes.titlesize": 7.5,
                "xtick.labelsize": 6.5,
                "ytick.labelsize": 6.5,
                "legend.fontsize": 6.5,
            }
        )
    plt.rcParams.update(params)

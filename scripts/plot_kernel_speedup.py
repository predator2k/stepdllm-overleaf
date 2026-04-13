#!/usr/bin/env python3
"""Generate the kernel speedup figure (figures/kernel_speedup.pdf).

Plots wall-clock speedup of the fused block-sparse attention kernel over
the dense Flash Attention baseline, across sparsity levels and sequence lengths.
"""

import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ── Data ────────────────────────────────────────────────────────────────────
SPARSITY = [50, 75, 80, 90, 95]

SPEEDUP_BY_SEQLEN = {
    "1K":  [0.83, 1.61, 2.06, 3.65, 4.22],
    "2K":  [0.83, 1.61, 2.02, 3.87, 6.84],
    "4K":  [1.25, 1.57, 1.99, 3.78, 6.95],
    "8K":  [1.45, 1.61, 2.05, 4.02, 8.06],
    "16K": [1.37, 1.64, 2.10, 4.17, 8.55],
}

# ── Style ───────────────────────────────────────────────────────────────────
# Muted, colorblind-friendly palette
COLORS = {
    "1K":  "#4477AA",
    "2K":  "#66CCEE",
    "4K":  "#228833",
    "8K":  "#CCBB44",
    "16K": "#EE6677",
}

MARKERS = {
    "1K":  "o",
    "2K":  "s",
    "4K":  "D",
    "8K":  "^",
    "16K": "v",
}


def main() -> None:
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    output_path = repo_root / "figures" / "kernel_speedup.pdf"

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 10,
        "axes.labelsize": 11,
        "axes.titlesize": 12,
        "legend.fontsize": 9,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "lines.linewidth": 1.8,
        "lines.markersize": 6,
        "axes.linewidth": 0.8,
        "grid.linewidth": 0.5,
        "grid.alpha": 0.4,
    })

    fig, ax = plt.subplots(figsize=(5.5, 3.5))

    for label, speedups in SPEEDUP_BY_SEQLEN.items():
        ax.plot(
            SPARSITY,
            speedups,
            color=COLORS[label],
            marker=MARKERS[label],
            label=label,
            zorder=3,
        )

    # Baseline reference line at y = 1
    ax.axhline(y=1.0, color="gray", linestyle="--", linewidth=1.0, zorder=2)
    ax.text(
        SPARSITY[0] - 1.5, 1.0 + 0.15,
        "Dense baseline",
        fontsize=8,
        color="gray",
        va="bottom",
    )

    ax.set_xlabel("Sparsity (%)")
    ax.set_ylabel("Speedup over Dense Baseline (×)")
    ax.set_xticks(SPARSITY)
    ax.set_xticklabels([f"{s}%" for s in SPARSITY])
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1.0))
    ax.set_ylim(bottom=0)
    ax.grid(True, which="major", linestyle="-", alpha=0.3)

    ax.legend(
        title="Seq. Length",
        loc="upper left",
        framealpha=0.9,
        edgecolor="lightgray",
    )

    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate the KL-divergence curve figure (figures/attention_similarity_curve.pdf).

Plots KL divergence between consecutive denoising steps, showing sharp spikes
at transition points where the attention structure reorganises.  A vertical
dashed line marks the unmask step.

Data are approximated from the empirical figures in the paper.
"""

import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ── Data (estimated from the original figure) ──────────────────────────────
# x = diffusion step; y = KL(step_t || step_{t-1})
STEPS = list(range(2, 33))

KL_DIVERGENCE = [
    0.25,  # step 2
    0.12,  # step 3
    0.06,  # step 4
    0.03,  # step 5
    0.02,  # step 6
    0.04,  # step 7
    0.52,  # step 8
    0.38,  # step 9
    0.12,  # step 10
    1.48,  # step 11
    0.48,  # step 12
    0.82,  # step 13
    1.38,  # step 14
    0.22,  # step 15
    2.08,  # step 16
    2.36,  # step 17  ← peak near unmask step
    0.05,  # step 18
    0.10,  # step 19
    0.44,  # step 20
    0.40,  # step 21
    0.35,  # step 22
    0.25,  # step 23
    0.18,  # step 24
    0.22,  # step 25
    0.48,  # step 26
    0.45,  # step 27
    0.30,  # step 28
    0.74,  # step 29
    0.52,  # step 30
    0.26,  # step 31
    0.24,  # step 32
]

UNMASK_STEP = 17

# ── Style ───────────────────────────────────────────────────────────────────
# Colorblind-friendly palette matching plot_kernel_speedup.py
COLOR_MAIN = "#4477AA"   # Tol blue
COLOR_UNMASK = "#EE6677" # Tol red


def main() -> None:
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    output_path = repo_root / "figures" / "attention_similarity_curve.pdf"

    # Style consistent with plot_kernel_speedup.py
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 8,
        "axes.labelsize": 9,
        "axes.titlesize": 10,
        "legend.fontsize": 8,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "lines.linewidth": 1.5,
        "lines.markersize": 3,
        "axes.linewidth": 0.6,
        "grid.linewidth": 0.4,
        "grid.alpha": 0.35,
    })

    fig, ax = plt.subplots(figsize=(2.7, 2.2))

    # Main KL divergence curve
    ax.plot(
        STEPS,
        KL_DIVERGENCE,
        color=COLOR_MAIN,
        marker="o",
        markersize=2.5,
        linewidth=1.4,
        label="sample 2521",
        zorder=3,
    )

    # Unmask-step reference line
    ax.axvline(
        x=UNMASK_STEP,
        color=COLOR_UNMASK,
        linestyle="--",
        linewidth=1.2,
        label="unmask step",
        zorder=2,
    )

    ax.set_xlabel("Diffusion Step")
    ax.set_ylabel(r"KL Div. (curr $\|$ prev)")
    ax.set_xlim(1, 33)
    ax.set_ylim(bottom=0, top=2.6)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax.grid(True, which="major", linestyle="-", alpha=0.25)

    ax.legend(
        loc="upper left",
        framealpha=0.9,
        edgecolor="lightgray",
        handlelength=1.5,
    )

    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()

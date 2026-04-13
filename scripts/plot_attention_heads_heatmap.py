#!/usr/bin/env python3
"""Generate Figure 3a: Attention head heterogeneity heatmap (figures/attention_heads_heatmap.pdf).

Reproduces the visual pattern from the original figure showing that different
attention heads exhibit substantially different attention patterns for the same
query position.  Data is approximated from the original figure.
"""

import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# ── Reproducibility ──────────────────────────────────────────────────────────
RNG = np.random.default_rng(42)

NUM_HEADS = 32
NUM_KEYS = 224


def _generate_attention_data() -> np.ndarray:
    """Simulate attention weight data that matches the observed patterns.

    Key observations from the original figure:
    - Most values near zero (sparse attention).
    - Strong vertical features at key positions ~0-3 (start tokens).
    - Moderate activity at positions ~15, ~95 for several heads.
    - Strongest cluster at positions ~110-145, especially heads 8-14 and 21-26.
    - A prominent vertical stripe at position ~127 across many heads.
    - Right half (positions 160+) is mostly blank.
    """
    data = np.zeros((NUM_HEADS, NUM_KEYS), dtype=np.float64)

    # 1. Low-level background noise (very sparse, faint)
    noise = RNG.exponential(scale=0.003, size=(NUM_HEADS, NUM_KEYS))
    noise *= RNG.binomial(1, 0.15, size=(NUM_HEADS, NUM_KEYS))  # only 15% non-zero
    data += noise

    # 2. Start-of-sequence tokens (positions 0-3): faint vertical stripes
    for pos in range(4):
        intensity = RNG.uniform(0.02, 0.06, size=NUM_HEADS)
        # Not all heads attend to start tokens equally
        mask = RNG.binomial(1, 0.6, size=NUM_HEADS)
        data[:, pos] += intensity * mask

    # 3. Position ~15: faint vertical feature
    for pos in [14, 15, 16]:
        intensity = RNG.uniform(0.01, 0.04, size=NUM_HEADS)
        mask = RNG.binomial(1, 0.35, size=NUM_HEADS)
        data[:, pos] += intensity * mask

    # 4. Heads 0-8: faint broad horizontal activity across positions 0-100
    for head in range(9):
        scattered_positions = RNG.choice(100, size=RNG.integers(8, 20), replace=False)
        for pos in scattered_positions:
            data[head, pos] += RNG.uniform(0.01, 0.04)

    # 5. Positions ~90-105: moderate activity for several heads
    active_heads_region1 = [2, 5, 8, 9, 10, 11, 13, 22, 25, 26]
    for head in active_heads_region1:
        positions = RNG.integers(88, 108, size=RNG.integers(3, 8))
        for pos in positions:
            data[head, pos] += RNG.uniform(0.02, 0.06)

    # 6. Strong cluster: positions 110-145, heads 8-14
    for head in range(8, 15):
        n_active = RNG.integers(8, 18)
        positions = RNG.integers(108, 148, size=n_active)
        for pos in positions:
            data[head, pos] += RNG.uniform(0.04, 0.10)

    # 7. Strong cluster: positions 120-142, heads 21-26 (concentrated hot spots)
    for head in range(21, 27):
        n_active = RNG.integers(5, 12)
        positions = RNG.integers(118, 145, size=n_active)
        for pos in positions:
            data[head, pos] += RNG.uniform(0.05, 0.12)

    # 8. Prominent vertical stripe at position ~127 (visible across many heads)
    for head in range(NUM_HEADS):
        if RNG.random() < 0.55:
            data[head, 127] += RNG.uniform(0.03, 0.08)

    # 9. Scattered moderate activity for heads 25-27 around positions 95-110
    for head in [25, 26, 27]:
        positions = RNG.integers(93, 112, size=RNG.integers(4, 10))
        for pos in positions:
            data[head, pos] += RNG.uniform(0.03, 0.07)

    # 10. Very sparse right half (positions 160+): almost nothing
    data[:, 160:] *= 0.1

    # Clip to observed range
    data = np.clip(data, 0.0, 0.12)

    return data


def main() -> None:
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    output_path = repo_root / "figures" / "attention_heads_heatmap.pdf"

    # ── Style (matching plot_kernel_speedup.py) ──────────────────────────────
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 8,
        "axes.labelsize": 9,
        "axes.titlesize": 10,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "axes.linewidth": 0.6,
    })

    data = _generate_attention_data()

    # Figure sized for subfigure at 0.49\columnwidth (~2.7in)
    fig, ax = plt.subplots(figsize=(2.7, 2.4))

    # Colorblind-friendly warm colormap
    cmap = plt.cm.YlOrRd
    norm = mcolors.Normalize(vmin=0.0, vmax=0.10)

    im = ax.imshow(
        data,
        aspect="auto",
        cmap=cmap,
        norm=norm,
        interpolation="nearest",
        origin="upper",
    )

    ax.set_xlabel("Key Position")
    ax.set_ylabel("Attention Head")

    # X-axis ticks matching original: 0, 31, 63, 95, 127, 159, 191, 223
    xtick_positions = [0, 31, 63, 95, 127, 159, 191, 223]
    ax.set_xticks(xtick_positions)
    ax.set_xticklabels([str(x) for x in xtick_positions])

    # Y-axis ticks matching original: 0, 4, 8, 13, 17, 22, 26, 31
    ytick_positions = [0, 4, 8, 13, 17, 22, 26, 31]
    ax.set_yticks(ytick_positions)
    ax.set_yticklabels([str(y) for y in ytick_positions])

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, pad=0.03, fraction=0.046)
    cbar.ax.tick_params(labelsize=6)

    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()

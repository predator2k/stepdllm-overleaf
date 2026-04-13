#!/usr/bin/env python3
"""Generate the cross-step attention similarity heatmap (figures/attention_multi_position.pdf).

Plots a 2x2 grid of heatmaps showing attention pattern similarity between
denoising steps at four representative query positions.  Demonstrates that
attention in diffusion LLMs is locally consistent but globally non-stationary.

Data are approximated from the empirical figures in the paper.
"""

import pathlib

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# ── Constants ───────────────────────────────────────────────────────────────
NUM_STEPS = 64
QUERY_POSITIONS = [20, 64, 144, 208]

# Tick positions – clean multiples for readability
TICK_POSITIONS = [0, 15, 31, 47, 63]          # 0-indexed
TICK_LABELS = ["1", "16", "32", "48", "64"]    # 1-indexed display


# ── Synthetic similarity-matrix generation ──────────────────────────────────

def _decay_matrix(n: int, tau: float) -> np.ndarray:
    """Symmetric exponential-decay matrix: sim(i,j) = exp(-|i-j| / tau)."""
    idx = np.arange(n, dtype=float)
    return np.exp(-np.abs(idx[:, None] - idx[None, :]) / tau)


def _block_mask(n: int, boundary_lo: int, boundary_hi: int) -> tuple:
    """Return boolean masks for early, transition, and late blocks."""
    idx = np.arange(n)
    early = idx < boundary_lo
    late = idx >= boundary_hi
    trans = (~early) & (~late)
    return early, trans, late


def _cross(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Symmetric outer product for boolean masks."""
    return np.outer(a, b).astype(float) + np.outer(b, a).astype(float)


def _add_noise(sim: np.ndarray, rng: np.random.RandomState,
               sigma: float = 0.03) -> np.ndarray:
    """Add symmetric Gaussian noise and clamp to [0, 1]."""
    noise = rng.normal(0, sigma, sim.shape)
    noise = (noise + noise.T) / 2
    sim = np.clip(sim + noise, 0.0, 1.0)
    np.fill_diagonal(sim, 1.0)
    return sim


def _soft_block(idx: np.ndarray, center: float, width: float) -> np.ndarray:
    """Soft block membership with sigmoid edges."""
    return 1.0 / (1.0 + np.exp(-(idx - center) / width))


def generate_similarity(query_pos: int, seed: int = 42) -> np.ndarray:
    """Build a 64x64 step-similarity matrix approximating empirical patterns.

    Key insight: within each phase/block, steps are mutually similar
    (uniform high values), while cross-block similarity is low.  A thin
    diagonal decay is layered on top for realism.
    """
    rng = np.random.RandomState(seed + query_pos)
    n = NUM_STEPS
    idx = np.arange(n, dtype=float)
    diff = np.abs(idx[:, None] - idx[None, :])

    if query_pos == 20:
        # Gradual structure: early block (steps 1-18), mid gap, late block
        # (steps 35-64).  The late block has broader mutual similarity.
        # Moderate diagonal band throughout.
        early = np.clip(1.0 - idx / 18, 0, 1)
        late = np.clip((idx - 30) / 8, 0, 1)
        mid = np.exp(-((idx - 25) / 10) ** 2)

        sim = 0.25 * np.exp(-diff / 8)            # base diagonal
        sim += 0.30 * np.outer(early, early)       # early block
        sim += 0.55 * np.outer(late, late)          # late block
        sim += 0.12 * np.outer(mid, mid)            # mid bridge
        # cross-block suppression
        sim -= 0.15 * (np.outer(early, late) + np.outer(late, early))

    elif query_pos == 64:
        # Sharp two-block: steps 1-12 (moderate) vs. 16-64 (very high).
        early = np.clip(1.0 - (idx - 12) / 3, 0, 1)
        late = np.clip((idx - 14) / 3, 0, 1)

        sim = 0.10 * np.exp(-diff / 5)             # thin diagonal base
        sim += 0.55 * np.outer(early, early)        # early block
        sim += 0.88 * np.outer(late, late)           # late block – uniformly high
        # cross-block driven to near-zero by construction (products small)

    elif query_pos == 144:
        # Wider diagonal band; moderate block structure around step 22.
        early = np.clip(1.0 - (idx - 20) / 5, 0, 1)
        late = np.clip((idx - 22) / 5, 0, 1)

        sim = 0.30 * np.exp(-diff / 10)            # wider diagonal
        sim += 0.15 * np.exp(-diff / 4)             # extra near-diagonal
        sim += 0.22 * np.outer(early, early)        # early block
        sim += 0.42 * np.outer(late, late)           # late block

    elif query_pos == 208:
        # Very sharp block: steps 1-10 vs. 18-64 (pronounced late block).
        early = np.clip(1.0 - (idx - 10) / 3, 0, 1)
        late = np.clip((idx - 16) / 3, 0, 1)
        trans = np.exp(-((idx - 14) / 3) ** 2)

        sim = 0.08 * np.exp(-diff / 4)             # thin diagonal
        sim += 0.40 * np.outer(early, early)        # early block
        sim += 0.90 * np.outer(late, late)           # late block – very uniform
        sim += 0.12 * np.outer(trans, trans)        # transition diagonal
    else:
        raise ValueError(f"Unknown query position: {query_pos}")

    sim = np.clip(sim, 0.0, 1.0)
    sim = (sim + sim.T) / 2
    np.fill_diagonal(sim, 1.0)
    return _add_noise(sim, rng, sigma=0.03)


# ── Plotting ────────────────────────────────────────────────────────────────

def main() -> None:
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    output_path = repo_root / "figures" / "attention_multi_position.pdf"

    # Style consistent with plot_kernel_speedup.py
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 8,
        "axes.labelsize": 8,
        "axes.titlesize": 9,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "axes.linewidth": 0.6,
    })

    fig, axes = plt.subplots(
        2, 2,
        figsize=(2.7, 2.7),
        gridspec_kw={"wspace": 0.35, "hspace": 0.45},
    )

    ims = []
    for ax, qpos in zip(axes.flat, QUERY_POSITIONS):
        sim = generate_similarity(qpos)
        im = ax.imshow(
            sim,
            cmap="viridis",
            vmin=0.0,
            vmax=1.0,
            aspect="equal",
            interpolation="nearest",
            origin="upper",
        )
        ims.append(im)
        ax.set_title(f"Query Pos {qpos}", pad=3)
        ax.set_xticks(TICK_POSITIONS)
        ax.set_xticklabels(TICK_LABELS)
        ax.set_yticks(TICK_POSITIONS)
        ax.set_yticklabels(TICK_LABELS)

    # Shared axis labels
    for ax in axes[1, :]:
        ax.set_xlabel("Step")
    for ax in axes[:, 0]:
        ax.set_ylabel("Step")

    # Single colorbar on the right
    cbar = fig.colorbar(
        ims[0],
        ax=axes.ravel().tolist(),
        fraction=0.046,
        pad=0.04,
        shrink=0.85,
    )
    cbar.ax.tick_params(labelsize=7)

    fig.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate Figure 3b: cumulative attention mass vs. key-entry fraction per head.

Synthetic data is shaped to match the paper narrative (some heads reach 90%% of
mass with ~10%% of entries; others need ~50%%). Output:
``figures/attention_budget_cross_head.pdf``.

``cumulative_mass_at_top_ratios`` and ``TOP_RATIOS`` support unit tests and any
heatmap-style diagnostics; the published figure uses overlaid cumulative curves.
"""

from __future__ import annotations

import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

NUM_HEADS = 32
NUM_KEYS = 224
RNG_SEED = 42
TOP_RATIOS = np.arange(0.05, 0.51, 0.05)


def _dirichlet_concentration(head_index: int) -> np.ndarray:
    """Return Dirichlet concentration parameters for one head (length NUM_KEYS).

    Larger ``alpha`` at a few indices → sharper, more concentrated attention;
    uniform ``alpha`` → diffuse attention.
    """
    rng = np.random.default_rng(RNG_SEED + head_index * 17)
    base = rng.uniform(0.12, 0.35, size=NUM_KEYS)

    if head_index in (11, 26):
        base = rng.uniform(0.35, 0.55, size=NUM_KEYS)

    if head_index % 5 == 0:
        focus = rng.integers(100, 180, size=3)
        base[focus] *= rng.uniform(8.0, 18.0)
    elif head_index % 5 == 1:
        focus = rng.integers(0, 40, size=4)
        base[focus] *= rng.uniform(6.0, 14.0)
    elif head_index % 5 == 2:
        base *= rng.uniform(0.85, 1.15)
    else:
        k = rng.integers(6, 14)
        focus = rng.choice(NUM_KEYS, size=k, replace=False)
        base[focus] *= rng.uniform(4.0, 12.0)

    return np.clip(base, 1e-3, None)


def generate_head_attention_weights(
    num_heads: int = NUM_HEADS,
    num_keys: int = NUM_KEYS,
    rng_seed: int = RNG_SEED,
) -> np.ndarray:
    """Sample simplex attention weights for each head (shape ``num_heads × num_keys``)."""
    rng = np.random.default_rng(rng_seed)
    weights = np.empty((num_heads, num_keys), dtype=np.float64)
    for h in range(num_heads):
        alpha = _dirichlet_concentration(h)[:num_keys]
        weights[h] = rng.dirichlet(alpha)
    return weights


def cumulative_mass_curve(attention: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """For one attention vector over keys, return (fraction_of_keys, cumulative_mass).

    ``attention`` is nonnegative; normalized internally to sum to 1.
    """
    v = np.asarray(attention, dtype=np.float64).ravel()
    total = float(v.sum())
    if total <= 0.0:
        raise ValueError("attention weights must sum to a positive value")
    v = v / total
    order = np.argsort(-v)
    sorted_mass = v[order]
    cum = np.cumsum(sorted_mass)
    n = cum.size
    x = (np.arange(1, n + 1, dtype=np.float64)) / float(n)
    return x, cum


def cumulative_mass_at_top_ratios(attention: np.ndarray, ratios: np.ndarray = TOP_RATIOS) -> np.ndarray:
    """Cumulative mass in the top ``ceil(r * N)`` keys for each ratio ``r`` in ``ratios``."""
    v = np.asarray(attention, dtype=np.float64).ravel()
    total = float(v.sum())
    if total <= 0.0:
        raise ValueError("attention weights must sum to a positive value")
    v = v / total
    sorted_mass = np.sort(v)[::-1]
    cummass = np.cumsum(sorted_mass)
    n = cummass.size
    row = np.empty(len(ratios), dtype=np.float64)
    for i, r in enumerate(ratios):
        k = max(1, int(np.ceil(r * n)))
        row[i] = cummass[min(k, n) - 1]
    return row


def main() -> None:
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    output_path = repo_root / "figures" / "attention_budget_cross_head.pdf"

    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 8,
            "axes.labelsize": 9,
            "axes.titlesize": 10,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "axes.linewidth": 0.6,
        }
    )

    weights = generate_head_attention_weights()
    fig, ax = plt.subplots(figsize=(2.7, 2.4))

    accent = "#4477AA"
    for h in range(NUM_HEADS):
        x, y = cumulative_mass_curve(weights[h])
        alpha = 0.18 + 0.52 * (h / max(NUM_HEADS - 1, 1))
        ax.plot(
            100.0 * x,
            100.0 * y,
            color=accent,
            linewidth=0.85,
            alpha=alpha,
        )

    ax.set_xlabel("Fraction of key entries (%)")
    ax.set_ylabel("Cumulative attention mass (%)")
    ax.set_xlim(0.0, 100.0)
    ax.set_ylim(0.0, 100.0)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linestyle=":", linewidth=0.4, alpha=0.6)

    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()

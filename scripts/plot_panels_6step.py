#!/usr/bin/env python3
"""Generate Figure 2: attention patterns across 6 denoising steps (2x3 grid).

Shows that attention patterns are locally consistent within nearby steps
(29-31 and 39-41) but shift between the two groups — a new pivotal key
position (~95) emerges in Steps 39-41 that is absent in Steps 29-31.

Data is approximated from the original figure in the paper.
"""

from __future__ import annotations

import argparse
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

# ── Constants ───────────────────────────────────────────────────────────────
NUM_POSITIONS = 350
QUERY_POS = 172
STEPS_TOP = [29, 30, 31]
STEPS_BOT = [39, 40, 41]
RNG_SEED = 42


def _make_attention(rng: np.random.Generator,
                    spikes: dict[int, float],
                    noise_level: float = 0.002,
                    num_scattered: int = 30) -> np.ndarray:
    """Build a synthetic attention distribution over NUM_POSITIONS keys.

    Produces sharp, bar-like spikes (1-2 positions wide) on a noisy background,
    matching the visual style of real attention weight plots.
    """
    # Background: very low uniform noise with occasional small bumps
    attn = rng.exponential(scale=noise_level, size=NUM_POSITIONS)

    # Place designated spikes as sharp single-position bars
    for pos, height in spikes.items():
        if 0 <= pos < NUM_POSITIONS:
            attn[pos] = height
            # Add tiny neighbors for slight width (1-2 adjacent positions)
            if pos > 0:
                attn[pos - 1] = max(attn[pos - 1], height * rng.uniform(0.15, 0.4))
            if pos < NUM_POSITIONS - 1:
                attn[pos + 1] = max(attn[pos + 1], height * rng.uniform(0.15, 0.4))

    # Scattered small spikes throughout for realism
    spike_positions = rng.integers(10, NUM_POSITIONS - 10, size=num_scattered)
    spike_heights = rng.uniform(0.003, 0.008, size=num_scattered)
    for sp, sh in zip(spike_positions, spike_heights):
        attn[sp] = max(attn[sp], sh)

    # Slightly elevate region 150-190 (near query) to show cluster activity
    for p in range(150, 190):
        if p < NUM_POSITIONS:
            attn[p] = max(attn[p], rng.uniform(0.002, 0.006))

    return attn


def _build_step_data() -> dict[int, np.ndarray]:
    """Generate attention data for all 6 steps."""
    rng = np.random.default_rng(RNG_SEED)
    data = {}

    # ── Steps 29-31: main peak around position 165-175, small peaks at 0-5
    # Pattern: consistent across 29-31, NO spike at ~95
    step29_spikes = {
        1: 0.010, 3: 0.025, 6: 0.015, 10: 0.008,
        155: 0.008, 160: 0.012, 163: 0.018,
        165: 0.028, 167: 0.035, 170: 0.036, 172: 0.025,
        175: 0.015, 178: 0.008,
    }
    step30_spikes = {
        1: 0.012, 3: 0.023, 6: 0.014, 10: 0.007,
        155: 0.009, 160: 0.015, 163: 0.020,
        165: 0.025, 167: 0.030, 170: 0.065, 172: 0.024, 173: 0.015,
        175: 0.012, 178: 0.007,
    }
    step31_spikes = {
        1: 0.008, 3: 0.020, 6: 0.012, 10: 0.006,
        155: 0.007, 160: 0.010, 163: 0.015,
        165: 0.022, 167: 0.030, 170: 0.032, 172: 0.020,
        175: 0.012, 178: 0.006,
    }

    for step, spikes in [(29, step29_spikes), (30, step30_spikes),
                         (31, step31_spikes)]:
        data[step] = _make_attention(rng, spikes, noise_level=0.0015,
                                     num_scattered=25)

    # ── Steps 39-41: NEW spike at ~95, main peak around 165-175
    # Key difference from top row: prominent spike emerging at position 95
    step39_spikes = {
        1: 0.012, 3: 0.023, 6: 0.010, 10: 0.008,
        90: 0.008, 93: 0.015, 95: 0.063, 97: 0.020, 100: 0.008,
        155: 0.006, 160: 0.010, 163: 0.015,
        165: 0.020, 167: 0.025, 170: 0.035, 172: 0.018,
        175: 0.010, 178: 0.006,
    }
    step40_spikes = {
        1: 0.010, 3: 0.025, 6: 0.012, 10: 0.007,
        90: 0.006, 93: 0.010, 95: 0.027, 97: 0.012, 100: 0.006,
        155: 0.008, 160: 0.012, 163: 0.018,
        165: 0.025, 167: 0.035, 170: 0.070, 172: 0.035, 173: 0.015,
        175: 0.012, 178: 0.007,
    }
    step41_spikes = {
        1: 0.008, 3: 0.022, 6: 0.010, 10: 0.006,
        90: 0.007, 93: 0.012, 95: 0.045, 97: 0.015, 100: 0.007,
        155: 0.007, 160: 0.010, 163: 0.015,
        165: 0.022, 167: 0.030, 170: 0.070, 172: 0.025, 173: 0.012,
        175: 0.010, 178: 0.005,
    }

    for step, spikes in [(39, step39_spikes), (40, step40_spikes),
                         (41, step41_spikes)]:
        data[step] = _make_attention(rng, spikes, noise_level=0.002,
                                     num_scattered=35)

    return data


def build_step_data() -> dict[int, np.ndarray]:
    """Public entry point for tests and notebooks (same as internal builder)."""
    return _build_step_data()


def _parse_arguments(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate Figure 2: attention patterns across six denoising steps "
            "(2x3 PDF under figures/ by default)."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        type=pathlib.Path,
        default=None,
        metavar="PATH",
        help=(
            "Output PDF path. Relative paths are resolved against the repository "
            "root (default: figures/panels_6step_2x3.pdf)."
        ),
    )
    return parser.parse_args(argv)


def _default_output_path(repo_root: pathlib.Path) -> pathlib.Path:
    return repo_root / "figures" / "panels_6step_2x3.pdf"


def _resolve_output_path(
    repo_root: pathlib.Path,
    output: pathlib.Path | None,
) -> pathlib.Path:
    if output is None:
        return _default_output_path(repo_root)
    candidate = pathlib.Path(output)
    return candidate if candidate.is_absolute() else (repo_root / candidate).resolve()


def main(argv: list[str] | None = None) -> None:
    args = _parse_arguments(argv)
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    output_path = _resolve_output_path(repo_root, args.output)

    step_data = build_step_data()

    # ── Plot setup ──────────────────────────────────────────────────────
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 9,
        "axes.labelsize": 10,
        "axes.titlesize": 11,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "axes.linewidth": 0.8,
    })

    fig, axes = plt.subplots(
        2, 3, figsize=(5.5, 3.2), sharex=True, sharey=True,
    )

    all_steps = STEPS_TOP + STEPS_BOT
    positions = np.arange(NUM_POSITIONS)

    for idx, (ax, step) in enumerate(zip(axes.flat, all_steps)):
        attn = step_data[step]

        # Draw as thin vertical lines (bar-like) matching original style
        ax.vlines(positions, 0, attn, colors="#4477AA", linewidth=0.35, alpha=0.85)

        # Query position marker
        ax.axvline(
            x=QUERY_POS, color="#CCBB44", linestyle="--",
            linewidth=1.0, alpha=0.7, zorder=2,
        )

        ax.set_title(f"Step {step}", fontweight="bold", fontsize=10)
        ax.set_xlim(-5, NUM_POSITIONS + 5)
        ax.set_ylim(0, 0.075)

        # Only label outer axes
        if idx >= 3:
            ax.set_xlabel("Key Position")
        if idx % 3 == 0:
            ax.set_ylabel("Attn Weight")

        ax.tick_params(direction="in", length=3)

    # Shared legend below the grid
    legend_elements = [
        Line2D([0], [0], color="#4477AA", linewidth=1.5, label="Attention"),
        Line2D([0], [0], color="#CCBB44", linestyle="--",
               linewidth=1.2, label=f"Query (pos {QUERY_POS})"),
    ]
    fig.legend(
        handles=legend_elements,
        loc="lower center",
        ncol=2,
        frameon=True,
        framealpha=0.9,
        edgecolor="lightgray",
        fontsize=9,
        bbox_to_anchor=(0.5, -0.02),
    )

    fig.tight_layout(rect=[0, 0.06, 1, 1])
    fig.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main(None)

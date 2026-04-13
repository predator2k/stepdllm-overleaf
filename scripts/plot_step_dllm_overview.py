#!/usr/bin/env python3
"""Generate Step-dLLM overview architecture figure (figures/step_dllm_overview.pdf).

Vector diagram aligned with Section~\\ref{sec:method} caption: anchor steps run
full attention and extract a block mask; non-anchor steps reuse the mask with
fresh Q/K/V; periodic refresh every $\\Delta$ steps.
"""

from __future__ import annotations

import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


def _rounded_box(
    ax: plt.Axes,
    xy: tuple[float, float],
    width: float,
    height: float,
    text: str,
    *,
    facecolor: str,
    edgecolor: str = "#222222",
    fontsize: int = 9,
    linewidth: float = 0.9,
) -> FancyBboxPatch:
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.05",
        linewidth=linewidth,
        edgecolor=edgecolor,
        facecolor=facecolor,
        mutation_aspect=0.35,
    )
    ax.add_patch(patch)
    cx, cy = xy[0] + width / 2, xy[1] + height / 2
    ax.text(
        cx,
        cy,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        linespacing=1.25,
    )
    return patch


def _arrow(
    ax: plt.Axes,
    p0: tuple[float, float],
    p1: tuple[float, float],
    *,
    color: str = "#333333",
    lw: float = 1.0,
    style: str = "->",
    linestyle: str | tuple[float, list[float]] = "solid",
) -> None:
    ax.annotate(
        "",
        xy=p1,
        xytext=p0,
        arrowprops=dict(
            arrowstyle=style,
            color=color,
            lw=lw,
            shrinkA=2,
            shrinkB=2,
            linestyle=linestyle,
        ),
    )


def main() -> None:
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    output_path = repo_root / "figures" / "step_dllm_overview.pdf"

    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 9,
            "axes.linewidth": 0.8,
        }
    )

    fig_w, fig_h = 7.0, 2.75
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    ax.axis("off")

    c_anchor = "#4477AA"
    c_non = "#66CCEE"
    c_mask = "#CCBB44"
    c_muted = "#F4F4F4"

    ax.text(
        fig_w / 2,
        fig_h - 0.2,
        r"Diffusion trajectory: re-anchor every $\Delta$ steps",
        ha="center",
        va="center",
        fontsize=10,
        fontweight="medium",
    )
    y_tl = fig_h - 0.55
    x_line0, x_line1 = 0.5, fig_w - 0.5
    ax.plot([x_line0, x_line1], [y_tl, y_tl], color="#444444", lw=1.0, zorder=1)
    steps_x = [1.05, 2.25, 3.45, 4.65, 5.85]
    labels = [r"$s$", r"$s{+}1$", r"$\cdots$", r"$s{+}\Delta{-}1$", r"$s{+}\Delta$"]
    roles = ["anchor", "non", "non", "non", "anchor"]
    for xi, lab, role in zip(steps_x, labels, roles):
        color = c_anchor if role == "anchor" else c_non
        ax.scatter(
            [xi],
            [y_tl],
            s=115,
            color=color,
            edgecolor="#222222",
            zorder=3,
            linewidths=0.6,
        )
        ax.text(xi, y_tl - 0.26, lab, ha="center", va="top", fontsize=8)
    ax.text(x_line0 - 0.12, y_tl, "step", ha="right", va="center", fontsize=8, color="#555555")

    y_top = fig_h - 1.32
    y_bot = 0.42
    col_w, box_h = 1.95, 0.58
    mid_w = 2.05
    x_l = 0.48
    x_m = 2.58
    x_r = 4.78
    out_w = 1.65

    _rounded_box(
        ax,
        (x_l, y_top),
        col_w,
        box_h,
        "Hidden states\n" + r"$\mathbf{Q}^{(s)}, \mathbf{K}^{(s)}, \mathbf{V}^{(s)}$",
        facecolor=c_muted,
        fontsize=8,
    )
    _rounded_box(
        ax,
        (x_l, y_bot),
        col_w,
        box_h,
        "Hidden states\n" + r"$\mathbf{Q}^{(s')}, \mathbf{K}^{(s')}, \mathbf{V}^{(s')}$",
        facecolor=c_muted,
        fontsize=8,
    )

    _rounded_box(
        ax,
        (x_m, y_top),
        mid_w,
        box_h,
        "Modified Flash Attn\n(extract block mask)",
        facecolor=c_anchor,
        edgecolor="#1a3d66",
        fontsize=8,
    )
    _rounded_box(
        ax,
        (x_m, y_bot),
        mid_w,
        box_h,
        "Block-sparse Attn\n(reuse $\mathcal{I}$)",
        facecolor=c_non,
        edgecolor="#1a5c70",
        fontsize=8,
    )

    _rounded_box(
        ax,
        (x_r, y_top),
        out_w,
        box_h,
        r"$\mathbf{O}^{(s)}$ + mask $\mathcal{I}$",
        facecolor="#E8EEF6",
        fontsize=8,
    )
    cache_x = x_r + 0.08
    cache_w = out_w + 0.15
    cache_h = 0.48
    cache_y = y_bot - 0.68
    _rounded_box(
        ax,
        (cache_x, cache_y),
        cache_w,
        cache_h,
        r"Cache: block pattern $\mathcal{I}$"
        + "\n"
        + r"(same blocks; fresh $\mathbf{QKV}$ weights)",
        facecolor=c_mask,
        edgecolor="#6a5f20",
        fontsize=7,
    )
    _rounded_box(
        ax,
        (x_r, y_bot),
        out_w,
        box_h,
        r"Output $\mathbf{O}^{(s')}$",
        facecolor="#E8F6F8",
        fontsize=8,
    )

    mid_cx = x_m + mid_w / 2
    _arrow(ax, (x_l + col_w, y_top + box_h / 2), (x_m, y_top + box_h / 2))
    _arrow(ax, (x_m + mid_w, y_top + box_h / 2), (x_r, y_top + box_h / 2))
    _arrow(ax, (x_l + col_w, y_bot + box_h / 2), (x_m, y_bot + box_h / 2))
    _arrow(ax, (x_m + mid_w, y_bot + box_h / 2), (x_r, y_bot + box_h / 2))

    # Anchor mask populates cache (solid)
    out_cx = x_r + out_w / 2
    _arrow(
        ax,
        (out_cx, y_top),
        (cache_x + cache_w / 2, cache_y + cache_h),
        color="#333333",
        lw=1.0,
    )

    # Non-anchor reads cache into block-sparse (dashed)
    _arrow(
        ax,
        (cache_x + cache_w * 0.35, cache_y + cache_h),
        (mid_cx - 0.35, y_bot),
        color="#555555",
        lw=1.0,
        linestyle=(0, (4, 3)),
    )

    ax.text(
        x_m - 0.08,
        y_top + box_h + 0.1,
        "Anchor step",
        ha="left",
        va="bottom",
        fontsize=9,
        color="#1a3d66",
        fontweight="medium",
    )
    ax.text(
        x_m - 0.08,
        y_bot + box_h + 0.1,
        "Non-anchor step",
        ha="left",
        va="bottom",
        fontsize=9,
        color="#1a5c70",
        fontweight="medium",
    )

    ax.text(
        fig_w / 2,
        0.12,
        r"Cost: $\mathcal{O}(L^2)$ at anchors $\rightarrow$ $\mathcal{O}(L\,k\,b)$ on reused steps"
        + " · "
        + "Fused Triton kernels (anchor + sparse)",
        ha="center",
        va="bottom",
        fontsize=7.5,
        color="#444444",
    )

    fig.savefig(output_path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


if __name__ == "__main__":
    main()

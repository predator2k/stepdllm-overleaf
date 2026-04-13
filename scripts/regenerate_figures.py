#!/usr/bin/env python3
"""Regenerate vector figures listed in figures/manifest.json.

This is the thin driver around the manifest (single source of truth for wiring).
Individual plotters stay standalone; this script only orchestrates subprocess runs.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _load_manifest() -> dict:
    path = _repo_root() / "figures" / "manifest.json"
    if not path.is_file():
        raise FileNotFoundError(f"Missing manifest: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if "figures" not in data or not isinstance(data["figures"], list):
        raise ValueError("manifest.json must contain a 'figures' array")
    return data


def _run_one(generator: Path, *, dry_run: bool) -> None:
    root = _repo_root()
    cmd = [sys.executable, str(generator)]
    rel = generator.relative_to(root)
    if dry_run:
        print(f"DRY-RUN: {' '.join(cmd)}  (cwd={root})")
        return
    subprocess.run(cmd, cwd=root, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Regenerate PDF figures from figures/manifest.json.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned commands without executing plotters.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Print id, generator, and output for each figure, then exit.",
    )
    parser.add_argument(
        "--only",
        metavar="ID",
        help="Regenerate a single figure by manifest `id` (e.g. panels_6step_2x3).",
    )
    args = parser.parse_args()
    data = _load_manifest()
    root = _repo_root()
    entries = data["figures"]

    if args.list:
        for fig in entries:
            print(
                f"{fig['id']}\t{fig['generator']}\t{fig['output']}\t"
                f"cited_in={','.join(fig.get('cited_in', []))}"
            )
        return

    if args.only:
        selected = [f for f in entries if f.get("id") == args.only]
        if not selected:
            ids = ", ".join(sorted(f.get("id", "") for f in entries))
            parser.error(f"Unknown id {args.only!r}. Known ids: {ids}")
        entries = selected

    for fig in entries:
        gen = root / fig["generator"]
        out = root / fig["output"]
        if not gen.is_file():
            raise FileNotFoundError(f"Generator missing: {gen}")
        print(f"→ {fig['id']}: {gen.name} → {out}")
        _run_one(gen, dry_run=args.dry_run)


if __name__ == "__main__":
    main()

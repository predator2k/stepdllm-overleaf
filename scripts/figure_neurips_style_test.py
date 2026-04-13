#!/usr/bin/env python3
"""Tests for ``figure_neurips_style``."""

from __future__ import annotations

import pathlib
import sys
import unittest

_SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from figure_neurips_style import (
    HALF_COLUMN_IN,
    NEURIPS_SINGLE_COLUMN_IN,
    apply_neurips_style,
)


class TestNeuripsStyle(unittest.TestCase):
    def test_column_constants(self) -> None:
        self.assertGreater(NEURIPS_SINGLE_COLUMN_IN, 2.0)
        self.assertLess(HALF_COLUMN_IN, NEURIPS_SINGLE_COLUMN_IN)

    def test_apply_neurips_style_runs(self) -> None:
        apply_neurips_style()
        apply_neurips_style(small=False)


if __name__ == "__main__":
    unittest.main()

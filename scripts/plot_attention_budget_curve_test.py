#!/usr/bin/env python3
"""Unit tests for ``plot_attention_budget_curve``."""

from __future__ import annotations

import pathlib
import sys
import unittest

import numpy as np

_SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from plot_attention_budget_curve import (
    NUM_HEADS,
    NUM_KEYS,
    TOP_RATIOS,
    cumulative_mass_at_top_ratios,
    cumulative_mass_curve,
    generate_head_attention_weights,
)


class TestCumulativeMassCurve(unittest.TestCase):
    def test_monotone_increasing_to_one(self) -> None:
        attn = np.array([0.1, 0.2, 0.7])
        x, y = cumulative_mass_curve(attn)
        self.assertEqual(x.shape, y.shape)
        self.assertTrue(np.all(np.diff(y) >= -1e-12))
        self.assertAlmostEqual(float(y[-1]), 1.0, places=10)

    def test_sorted_order_steep_for_peaked(self) -> None:
        peaked = np.zeros(100)
        peaked[0] = 0.99
        peaked[1:] = 0.01 / 99.0
        x, y = cumulative_mass_curve(peaked)
        self.assertGreater(float(y[1]), 0.95)

    def test_rejects_nonpositive_sum(self) -> None:
        with self.assertRaises(ValueError):
            cumulative_mass_curve(np.zeros(5))


class TestCumulativeMassAtTopRatios(unittest.TestCase):
    def test_monotone_increasing_bounded(self) -> None:
        attn = np.array([0.1, 0.2, 0.7])
        row = cumulative_mass_at_top_ratios(attn, TOP_RATIOS)
        self.assertEqual(row.shape, TOP_RATIOS.shape)
        self.assertTrue(np.all(np.diff(row) >= -1e-12))
        self.assertLessEqual(float(row[-1]), 1.0 + 1e-12)
        self.assertGreaterEqual(float(row[-1]), float(row[0]))

    def test_full_ratio_covers_all_mass(self) -> None:
        attn = np.ones(50) / 50.0
        ratios = np.array([1.0])
        row = cumulative_mass_at_top_ratios(attn, ratios)
        self.assertAlmostEqual(float(row[0]), 1.0, places=10)

    def test_rejects_nonpositive_sum(self) -> None:
        with self.assertRaises(ValueError):
            cumulative_mass_at_top_ratios(np.zeros(5), TOP_RATIOS)


class TestGenerateHeadAttention(unittest.TestCase):
    def test_shape_and_simplex(self) -> None:
        w = generate_head_attention_weights()
        self.assertEqual(w.shape, (NUM_HEADS, NUM_KEYS))
        sums = w.sum(axis=1)
        np.testing.assert_allclose(sums, 1.0, rtol=0, atol=1e-10)
        self.assertTrue(np.all(w >= 0.0))


if __name__ == "__main__":
    unittest.main()

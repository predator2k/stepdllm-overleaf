#!/usr/bin/env python3
"""Unit tests for ``plot_panels_6step`` (Figure 2, six-step attention panels)."""

from __future__ import annotations

import pathlib
import subprocess
import sys
import unittest

import numpy as np

_SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
_SCRIPT = _SCRIPTS_DIR / "plot_panels_6step.py"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from plot_panels_6step import (
    NUM_POSITIONS,
    QUERY_POS,
    STEPS_BOT,
    STEPS_TOP,
    build_step_data,
)


class TestCliHelp(unittest.TestCase):
    def test_help_exits_before_plot(self) -> None:
        """Regression: unknown flags used to fall through and run a full regen."""
        result = subprocess.run(
            [sys.executable, str(_SCRIPT), "--help"],
            cwd=_REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        combined = f"{result.stdout}\n{result.stderr}".lower()
        self.assertIn("usage:", combined)
        self.assertIn("--output", combined)


class TestBuildStepData(unittest.TestCase):
    def test_keys_and_shapes(self) -> None:
        data = build_step_data()
        expected = set(STEPS_TOP + STEPS_BOT)
        self.assertEqual(set(data.keys()), expected)
        for step, vec in data.items():
            self.assertEqual(vec.shape, (NUM_POSITIONS,), msg=f"step {step}")
            self.assertTrue(np.all(vec >= 0.0), msg=f"step {step}")

    def test_pivotal_spike_emerges_only_in_late_steps(self) -> None:
        """Narrative: key ~95 is salient in steps 39--41 but not in 29--31."""
        data = build_step_data()
        early = max(float(data[s][95]) for s in STEPS_TOP)
        late = min(float(data[s][95]) for s in STEPS_BOT)
        self.assertGreater(
            late,
            early + 0.02,
            msg="position 95 should be clearly stronger in the lower step group",
        )

    def test_query_region_has_mass(self) -> None:
        data = build_step_data()
        for s in STEPS_TOP + STEPS_BOT:
            self.assertGreater(float(data[s][QUERY_POS]), 0.01, msg=f"step {s}")


if __name__ == "__main__":
    unittest.main()

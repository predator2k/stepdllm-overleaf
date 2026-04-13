#!/usr/bin/env python3
"""Fast checks for ``build_pdf.sh`` (no TeX required)."""

from __future__ import annotations

import pathlib
import subprocess
import sys
import unittest


class TestBuildPdfScript(unittest.TestCase):
    def setUp(self) -> None:
        self._root = pathlib.Path(__file__).resolve().parents[1]
        self._script = self._root / "scripts" / "build_pdf.sh"

    def test_help_exits_zero(self) -> None:
        result = subprocess.run(
            ["sh", str(self._script), "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("latexmk", result.stdout)
        self.assertIn("tectonic", result.stdout)

    def test_shell_syntax(self) -> None:
        result = subprocess.run(
            ["sh", "-n", str(self._script)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()

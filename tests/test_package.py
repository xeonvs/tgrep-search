from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PackageTest(unittest.TestCase):
    def test_package_is_canonical_and_public(self) -> None:
        for script, args in (("build_plugin.py", ("--check",)), ("validate_public_package.py", ())):
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / script), *args],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

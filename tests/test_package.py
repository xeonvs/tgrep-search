from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PackageTest(unittest.TestCase):
    def test_workflow_action_pins_are_current(self) -> None:
        workflows = "\n".join(
            (ROOT / ".github" / "workflows" / name).read_text()
            for name in ("ci.yml", "release.yml")
        )
        self.assertIn("actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1", workflows)
        self.assertIn("softprops/action-gh-release@efb35369e0ad2afab669f228072c1b0d510eae64", workflows)
        self.assertNotIn("a26af69be951a213d495a4c3e4e4022e16d87065", workflows)
        self.assertNotIn("3bb12739c298aeb8a4eeaf626c5b8d85266b0e65", workflows)

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

    def test_brand_assets_are_opaque_and_expected_size(self) -> None:
        plugin = ROOT / "plugins" / "tgrep-search" / "skills" / "tgrep-search" / "assets" / "brand"
        expected = {
            "logo.png": (1024, 1024),
            "logo-dark.png": (1024, 1024),
            "composer-icon.png": (128, 128),
        }
        for name, (width, height) in expected.items():
            data = (plugin / name).read_bytes()
            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(int.from_bytes(data[16:20], "big"), width)
            self.assertEqual(int.from_bytes(data[20:24], "big"), height)
            self.assertEqual(data[24], 8)
            self.assertEqual(data[25], 2, "asset must be RGB/fully opaque")
        self.assertEqual((plugin / "logo.png").read_bytes(), (plugin / "logo-dark.png").read_bytes())
        readme = (ROOT / "README.md").read_text()
        self.assertIn('src="skill/tgrep-search/assets/brand/logo.svg"', readme)
        self.assertIn('alt="tgrep Search"', readme)
        self.assertIn('width="160"', readme)

    def test_codex_interface_paths_and_identity(self) -> None:
        plugin = ROOT / "plugins" / "tgrep-search"
        manifest = json.loads((plugin / ".codex-plugin" / "plugin.json").read_text())
        self.assertEqual(manifest["version"], "1.0.2")
        interface = manifest["interface"]
        self.assertEqual(interface["brandColor"], "#67E8F9")
        for key in ("composerIcon", "logo", "logoDark"):
            asset = interface[key]
            self.assertTrue(asset.startswith("./"))
            self.assertTrue((plugin / asset[2:]).is_file())
        claude = json.loads((plugin / ".claude-plugin" / "plugin.json").read_text())
        for key in ("brandColor", "composerIcon", "logo", "logoDark"):
            self.assertNotIn(key, claude)

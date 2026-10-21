from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PackageTest(unittest.TestCase):
    def test_reference_parity_is_checked(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tgrep-package-") as directory:
            root = Path(directory)
            for name in ("scripts", "skill", "plugins"):
                shutil.copytree(ROOT / name, root / name)
            reference = root / "plugins/tgrep-search/skills/tgrep-search/references/shared-worktrees.md"
            reference.write_text(reference.read_text() + "\nUnreleased change.\n")
            result = subprocess.run(
                [sys.executable, str(root / "scripts/build_plugin.py"), "--check"],
                text=True, capture_output=True, check=False, timeout=10,
            )
            self.assertEqual(result.returncode, 1)

    def test_both_index_storage_names_are_rejected_in_package(self) -> None:
        for name in (".tgrep", ".tgrep-index"):
            with self.subTest(name=name), tempfile.TemporaryDirectory(prefix="tgrep-package-") as directory:
                root = Path(directory)
                for source in ("scripts", "skill", "plugins"):
                    shutil.copytree(ROOT / source, root / source)
                (root / "plugins/tgrep-search" / name).mkdir()
                result = subprocess.run(
                    [sys.executable, str(root / "scripts/validate_public_package.py")],
                    text=True, capture_output=True, check=False, timeout=10,
                )
                self.assertEqual(result.returncode, 1)

    def test_workflow_action_pins_are_current(self) -> None:
        workflows = "\n".join(
            (ROOT / ".github" / "workflows" / name).read_text()
            for name in ("ci.yml", "release.yml")
        )
        self.assertIn("actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1", workflows)
        self.assertIn("actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97", workflows)
        self.assertIn("python-version: '3.15'", workflows)
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
        self.assertEqual(manifest["version"], "1.1.0")
        interface = manifest["interface"]
        self.assertEqual(interface["brandColor"], "#67E8F9")
        for key in ("composerIcon", "logo", "logoDark"):
            asset = interface[key]
            self.assertTrue(asset.startswith("./"))
            self.assertTrue((plugin / asset[2:]).is_file())
        claude = json.loads((plugin / ".claude-plugin" / "plugin.json").read_text())
        for key in ("brandColor", "composerIcon", "logo", "logoDark"):
            self.assertNotIn(key, claude)

#!/usr/bin/env python3
"""Validate package shape and deny public sensitive-content classes."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "tgrep-search"
CANONICAL = ROOT / "skill" / "tgrep-search" / "SKILL.md"
PACKAGED = PLUGIN / "skills" / "tgrep-search" / "SKILL.md"
MANIFESTS = (PLUGIN / ".codex-plugin" / "plugin.json", PLUGIN / ".claude-plugin" / "plugin.json")
FORBIDDEN = re.compile(r"(?<![A-Za-z0-9])(ghp_|github_pat_|glpat-|AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9_-]{16,}|xox[baprs]-|AIza[0-9A-Za-z_-]{20,}|-----BEGIN [A-Z ]+PRIVATE KEY-----|/Users/)")


def main() -> int:
    required = (*MANIFESTS, CANONICAL, PACKAGED)
    if any(not path.is_file() for path in required):
        print("validation failed: required package file missing")
        return 1
    if CANONICAL.read_bytes() != PACKAGED.read_bytes():
        print("validation failed: packaged skill differs from canonical source")
        return 1
    for path in PLUGIN.rglob("*"):
        if path.is_symlink() or any(part in {".git", ".tgrep-index", "__pycache__"} for part in path.relative_to(PLUGIN).parts):
            print("validation failed: unsupported packaged artifact")
            return 1
        if path.is_file() and FORBIDDEN.search(path.read_text(encoding="utf-8")):
            print("validation failed: forbidden public-content pattern")
            return 1
    for path in MANIFESTS:
        value = json.loads(path.read_text(encoding="utf-8"))
        if value.get("name") != "tgrep-search" or value.get("version") != "1.0.1" or value.get("license") != "MIT":
            print("validation failed: manifest identity drift")
            return 1
    print("public package validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

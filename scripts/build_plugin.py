#!/usr/bin/env python3
"""Build or verify the deterministic tgrep-search plugin package."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skill" / "tgrep-search"
PACKAGE = ROOT / "plugins" / "tgrep-search" / "skills" / "tgrep-search"


def snapshot(root: Path) -> dict[str, bytes]:
    if not root.is_dir():
        raise ValueError(f"missing directory: {root}")
    files: dict[str, bytes] = {}
    for item in sorted(root.rglob("*")):
        if item.is_symlink():
            raise ValueError(f"unsupported symlink: {item.relative_to(root)}")
        if item.is_file():
            files[item.relative_to(root).as_posix()] = item.read_bytes()
    return files


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        source = snapshot(SOURCE)
        if args.write:
            if PACKAGE.exists():
                shutil.rmtree(PACKAGE)
            PACKAGE.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(SOURCE, PACKAGE)
        if source != snapshot(PACKAGE):
            raise ValueError("generated skill package differs from canonical skill")
    except (OSError, ValueError) as exc:
        print(f"package check failed: {exc}")
        return 1
    print("package check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

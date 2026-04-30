#!/usr/bin/env python3
"""Validate custom Odoo module layout and naming conventions."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


REQUIRED_FILES = ("__init__.py", "__manifest__.py")
REQUIRED_DIRS = ("models", "views", "security")


def _module_roots_from_paths(paths: list[Path], repo_root: Path) -> set[Path]:
    module_roots: set[Path] = set()
    for path in paths:
        rel = path.relative_to(repo_root)
        parts = rel.parts
        if len(parts) < 2 or parts[0] != "addons":
            continue
        module_root = repo_root / "addons" / parts[1]
        if module_root.name.startswith("msp_"):
            module_roots.add(module_root)
    return module_roots


def _validate_module(module_root: Path) -> list[str]:
    errors: list[str] = []

    if not module_root.exists():
        errors.append(f"{module_root}: module path does not exist")
        return errors

    for file_name in REQUIRED_FILES:
        if not (module_root / file_name).is_file():
            errors.append(f"{module_root}: missing required file '{file_name}'")

    for dir_name in REQUIRED_DIRS:
        if not (module_root / dir_name).is_dir():
            errors.append(f"{module_root}: missing required directory '{dir_name}/'")

    manifest_path = module_root / "__manifest__.py"
    if manifest_path.is_file():
        content = manifest_path.read_text(encoding="utf-8")
        for key in ("name", "version", "depends", "data", "license"):
            if f"'{key}'" not in content and f'"{key}"' not in content:
                errors.append(f"{manifest_path}: expected key '{key}'")

    access_file = module_root / "security" / "ir.model.access.csv"
    if not access_file.is_file():
        errors.append(f"{module_root}: missing 'security/ir.model.access.csv'")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    changed_paths = [repo_root / p for p in args.files]
    module_roots = _module_roots_from_paths(changed_paths, repo_root)

    if not module_roots:
        return 0

    errors: list[str] = []
    for module_root in sorted(module_roots):
        errors.extend(_validate_module(module_root))

    if errors:
        print("Odoo module layout validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Path selection helpers for path-scoped instruction generation."""

from __future__ import annotations

from pathlib import Path


COMMON_SOURCE_DIRS = [
    "src",
    "app",
    "lib",
    "packages",
    "services",
    "components",
    "pages",
    "api",
    "internal",
    "cmd",
]

COMMON_TEST_DIRS = [
    "tests",
    "test",
    "__tests__",
    "spec",
]


def detect_source_paths(root: Path) -> list[str]:
    """Detect likely source directories relative to the project root."""
    return [name for name in COMMON_SOURCE_DIRS if (root / name).is_dir()]


def detect_test_paths(root: Path) -> list[str]:
    """Detect likely test directories relative to the project root."""
    return [name for name in COMMON_TEST_DIRS if (root / name).is_dir()]


def select_instruction_globs(source_paths: list[str], test_paths: list[str]) -> list[str]:
    """Build path globs for path-scoped instruction files."""
    globs = [f"{path}/**/*" for path in source_paths]
    globs.extend(f"{path}/**/*" for path in test_paths)
    return globs or ["**/*"]
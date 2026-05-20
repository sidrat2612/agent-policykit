"""Path selection helpers for path-scoped instruction generation."""

from __future__ import annotations

import re
from pathlib import Path

from agent_policykit.core.models import InstructionScope

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

COMMON_WORKSPACE_DIRS = [
    "packages",
    "apps",
    "services",
]


def detect_source_paths(root: Path) -> list[str]:
    """Detect likely source directories relative to the project root."""
    return [name for name in COMMON_SOURCE_DIRS if (root / name).is_dir()]


def detect_test_paths(root: Path) -> list[str]:
    """Detect likely test directories relative to the project root."""
    return [name for name in COMMON_TEST_DIRS if (root / name).is_dir()]


def build_instruction_scopes(source_paths: list[str], test_paths: list[str]) -> list[InstructionScope]:
    """Build path-specific instruction scopes for source and test trees."""
    scopes: list[InstructionScope] = []

    for path in source_paths:
        scopes.append(
            InstructionScope(
                slug=_slugify_scope(path),
                display_name=f"{path} implementation",
                globs=[f"{path}/**/*"],
                paths=[path],
                exclude_agent="code-review",
                description=f"Implementation files under {path}/",
            )
        )

    for path in test_paths:
        scopes.append(
            InstructionScope(
                slug=_slugify_scope(path),
                display_name=f"{path} tests",
                globs=[f"{path}/**/*"],
                paths=[path],
                description=f"Tests, fixtures, and validation files under {path}/",
            )
        )

    return scopes


def detect_subproject_paths(root: Path) -> list[str]:
    """Detect monorepo-style subproject roots under common workspace folders."""
    subprojects: list[str] = []

    for workspace_dir in COMMON_WORKSPACE_DIRS:
        container = root / workspace_dir
        if not container.is_dir():
            continue

        try:
            children = sorted(container.iterdir(), key=lambda path: path.name)
        except OSError:
            continue

        for child in children:
            if not child.is_dir() or child.name.startswith("."):
                continue
            relative_path = child.relative_to(root).as_posix()
            subprojects.append(relative_path)

    return subprojects


def select_instruction_globs(source_paths: list[str], test_paths: list[str]) -> list[str]:
    """Build path globs for path-scoped instruction files."""
    globs: list[str] = []
    for scope in build_instruction_scopes(source_paths, test_paths):
        for glob in scope.globs:
            if glob not in globs:
                globs.append(glob)
    return globs or ["**/*"]


def _slugify_scope(path: str) -> str:
    """Convert a relative path into a stable file-name-safe scope slug."""
    normalized = path.strip().replace("\\", "/")
    return re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-") or "project"

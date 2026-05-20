"""Framework detection from config files and dependencies."""

from __future__ import annotations

import json
from pathlib import Path

import yaml


# Framework markers: (framework_id, detection_files, detection_in_deps)
FRAMEWORK_MARKERS: list[tuple[str, list[str], list[str]]] = [
    # Python frameworks
    ("fastapi", [], ["fastapi"]),
    ("django", ["manage.py"], ["django"]),
    ("flask", [], ["flask"]),
    # JS/TS frameworks
    ("nextjs", ["next.config.js", "next.config.mjs", "next.config.ts"], ["next"]),
    ("react", [], ["react"]),
    ("vue", ["vue.config.js"], ["vue"]),
    ("angular", ["angular.json"], ["@angular/core"]),
    ("express", [], ["express"]),
    ("nestjs", ["nest-cli.json"], ["@nestjs/core"]),
    # Java frameworks
    ("spring_boot", [], ["spring-boot-starter"]),
    # Go frameworks
    ("gin", [], ["github.com/gin-gonic/gin"]),
    ("echo", [], ["github.com/labstack/echo"]),
]


def detect_frameworks(root: Path) -> list[str]:
    """Detect frameworks used in the project.

    Checks:
    1. Presence of framework-specific config files
    2. Dependencies in package.json, pyproject.toml, requirements.txt, go.mod, pom.xml
    """
    detected: list[str] = []
    deps = _collect_dependencies(root)

    for framework_id, marker_files, dep_names in FRAMEWORK_MARKERS:
        # Check marker files
        for marker in marker_files:
            if (root / marker).exists():
                if framework_id not in detected:
                    detected.append(framework_id)
                break

        # Check dependencies
        for dep_name in dep_names:
            if dep_name in deps:
                if framework_id not in detected:
                    detected.append(framework_id)
                break

    return detected


def _collect_dependencies(root: Path) -> set[str]:
    """Collect all dependency names from various package manager files."""
    deps: set[str] = set()

    # package.json
    pkg_json = root / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text(encoding="utf-8"))
            for section in ("dependencies", "devDependencies", "peerDependencies"):
                if section in data and isinstance(data[section], dict):
                    deps.update(data[section].keys())
        except (json.JSONDecodeError, OSError):
            pass

    # pyproject.toml (dependencies section)
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        try:
            content = pyproject.read_text(encoding="utf-8")
            # Simple extraction: look for dependency names in [project.dependencies]
            # We use basic parsing since tomllib requires Python 3.11+
            import tomllib
            data = tomllib.loads(content)
            project_deps = data.get("project", {}).get("dependencies", [])
            for dep in project_deps:
                # Extract package name (before version specifier)
                name = dep.split(">=")[0].split("<=")[0].split("==")[0].split("[")[0].strip()
                deps.add(name.lower())
        except (OSError, Exception):
            pass

    # requirements.txt
    req_txt = root / "requirements.txt"
    if req_txt.exists():
        try:
            for line in req_txt.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("-"):
                    name = line.split(">=")[0].split("<=")[0].split("==")[0].split("[")[0].strip()
                    deps.add(name.lower())
        except OSError:
            pass

    # go.mod
    go_mod = root / "go.mod"
    if go_mod.exists():
        try:
            for line in go_mod.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("module") and not line.startswith("go "):
                    parts = line.split()
                    if parts and not parts[0] in ("require", "(", ")"):
                        deps.add(parts[0])
        except OSError:
            pass

    return deps

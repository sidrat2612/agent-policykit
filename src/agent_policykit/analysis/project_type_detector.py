"""Project type detection based on structure and configuration."""

from __future__ import annotations

from pathlib import Path

from agent_policykit.types import ProjectType


# Heuristics for project type detection
PROJECT_TYPE_SIGNALS: dict[ProjectType, dict[str, list[str]]] = {
    ProjectType.API_SERVICE: {
        "files": ["openapi.yaml", "openapi.json", "swagger.yaml", "swagger.json"],
        "dirs": ["routes", "endpoints", "api", "handlers"],
        "markers": [],
    },
    ProjectType.WEB_APP: {
        "files": ["next.config.js", "next.config.mjs", "nuxt.config.ts", "angular.json", "vite.config.ts"],
        "dirs": ["pages", "app", "components", "views", "public"],
        "markers": [],
    },
    ProjectType.MICROSERVICE: {
        "files": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml", "k8s.yaml"],
        "dirs": ["cmd", "internal"],
        "markers": [],
    },
    ProjectType.CLI_TOOL: {
        "files": [],
        "dirs": ["cmd", "commands"],
        "markers": ["console_scripts", "[tool.poetry.scripts]"],
    },
    ProjectType.LIBRARY: {
        "files": ["setup.py", "setup.cfg"],
        "dirs": ["src"],
        "markers": [],
    },
    ProjectType.MONOREPO: {
        "files": ["lerna.json", "pnpm-workspace.yaml", "nx.json", "turbo.json"],
        "dirs": ["packages", "apps"],
        "markers": [],
    },
}


def detect_project_type(root: Path, frameworks: list[str] | None = None) -> ProjectType | None:
    """Detect the project type based on file structure and frameworks.

    Returns the most likely project type, or None if unclear.
    """
    scores: dict[ProjectType, int] = {pt: 0 for pt in ProjectType}
    frameworks = frameworks or []

    # Score based on file presence
    for project_type, signals in PROJECT_TYPE_SIGNALS.items():
        for filename in signals["files"]:
            if (root / filename).exists():
                scores[project_type] += 3

        for dirname in signals["dirs"]:
            if (root / dirname).is_dir():
                scores[project_type] += 2

    # Framework-based hints
    web_frameworks = {"nextjs", "react", "vue", "angular", "nuxt"}
    api_frameworks = {"fastapi", "express", "flask", "gin", "echo", "nestjs", "spring_boot"}
    if any(fw in web_frameworks for fw in frameworks):
        scores[ProjectType.WEB_APP] += 5
    if any(fw in api_frameworks for fw in frameworks):
        scores[ProjectType.API_SERVICE] += 4

    # Monorepo detection (strong signal)
    monorepo_files = ["lerna.json", "pnpm-workspace.yaml", "nx.json", "turbo.json"]
    if any((root / f).exists() for f in monorepo_files):
        scores[ProjectType.MONOREPO] += 10

    # CLI tool detection
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        try:
            content = pyproject.read_text(encoding="utf-8")
            if "console_scripts" in content or "[project.scripts]" in content:
                scores[ProjectType.CLI_TOOL] += 5
        except OSError:
            pass

    # Return highest scoring type (if above threshold)
    best_type = max(scores, key=lambda pt: scores[pt])
    if scores[best_type] >= 3:
        return best_type
    return None

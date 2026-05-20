"""Unified project context detector — combines all analysis modules."""

from __future__ import annotations

from pathlib import Path

from agent_guardrails.analysis.framework_detector import detect_frameworks
from agent_guardrails.analysis.language_detector import detect_languages
from agent_guardrails.analysis.project_type_detector import detect_project_type
from agent_guardrails.core.models import ProjectContext
from agent_guardrails.types import AgentTarget


# Known agent tool config file patterns
AGENT_TARGET_MARKERS: dict[AgentTarget, list[str]] = {
    AgentTarget.COPILOT_REPO: [".github/copilot-instructions.md"],
    AgentTarget.COPILOT_PATH: [".github/.copilot-*.md", ".instructions.md"],
    AgentTarget.AGENTS_MD: [".github/AGENTS.md", "AGENTS.md"],
    AgentTarget.CURSOR: [".cursorrules", ".cursor/rules"],
    AgentTarget.CLAUDE_CODE: [".claude/CLAUDE.md", "CLAUDE.md"],
    AgentTarget.AIDER: [".aider.conf.yml", ".aiderignore"],
    AgentTarget.CODEX: [".codex/instructions.md", "AGENTS.md"],
    AgentTarget.GEMINI_CLI: [".gemini/instructions.md", "GEMINI.md"],
}


def detect_project_context(root: Path) -> ProjectContext:
    """Run full project analysis and return a ProjectContext.

    Detects:
    - Programming languages present
    - Frameworks in use
    - Project type (API, web app, microservice, etc.)
    - Existing agent configuration targets
    """
    root = root.resolve()

    languages = detect_languages(root)
    frameworks = detect_frameworks(root)
    project_type = detect_project_type(root, frameworks)
    targets = _detect_existing_targets(root)

    return ProjectContext(
        root_path=root,
        detected_languages=languages,
        detected_frameworks=frameworks,
        project_type=project_type,
        targets=targets,
    )


def _detect_existing_targets(root: Path) -> list[AgentTarget]:
    """Detect which agent targets already have config files in the project."""
    detected: list[AgentTarget] = []
    for target, markers in AGENT_TARGET_MARKERS.items():
        for marker in markers:
            if "*" in marker:
                if list(root.glob(marker)):
                    detected.append(target)
                    break
            elif (root / marker).exists():
                detected.append(target)
                break
    return detected

"""Unified project context detector — combines all analysis modules."""

from __future__ import annotations

from pathlib import Path

from agent_policykit.analysis.framework_detector import detect_frameworks
from agent_policykit.analysis.language_detector import detect_languages
from agent_policykit.analysis.path_selector import (
    build_instruction_scopes,
    detect_subproject_paths,
    detect_source_paths,
    detect_test_paths,
    select_instruction_globs,
)
from agent_policykit.analysis.project_type_detector import detect_project_type
from agent_policykit.core.models import ProjectContext
from agent_policykit.types import AgentTarget


# Known agent tool config file patterns
AGENT_TARGET_MARKERS: dict[AgentTarget, list[str]] = {
    AgentTarget.COPILOT_REPO: [".github/copilot-instructions.md"],
    AgentTarget.COPILOT_PATH: [".github/instructions/*.instructions.md", ".instructions.md"],
    AgentTarget.AGENTS_MD: ["AGENTS.md"],
    AgentTarget.GENERIC_MARKDOWN: ["AGENT_POLICY.md"],
    AgentTarget.ROOCODE: ["AGENT_POLICY.roocode.md"],
    AgentTarget.WINDSURF: ["AGENT_POLICY.windsurf.md"],
    AgentTarget.ZED: ["AGENT_POLICY.zed.md"],
    AgentTarget.WARP: ["AGENT_POLICY.warp.md"],
    AgentTarget.JUNIE: ["AGENT_POLICY.junie.md"],
    AgentTarget.DEVIN: ["AGENT_POLICY.devin.md"],
    AgentTarget.AMP: ["AGENT_POLICY.amp.md"],
    AgentTarget.AUGMENT_CODE: ["AGENT_POLICY.augment-code.md"],
    AgentTarget.FACTORY: ["AGENT_POLICY.factory.md"],
    AgentTarget.JULES: ["AGENT_POLICY.jules.md"],
    AgentTarget.GOOSE: ["AGENT_POLICY.goose.md"],
    AgentTarget.OPENCODE: ["AGENT_POLICY.opencode.md"],
    AgentTarget.PHOENIX: ["AGENT_POLICY.phoenix.md"],
    AgentTarget.SEMGREP: ["AGENT_POLICY.semgrep.md"],
    AgentTarget.ONA: ["AGENT_POLICY.ona.md"],
    AgentTarget.CURSOR: [".cursor/rules/*.mdc", ".cursorrules"],
    AgentTarget.CLAUDE_CODE: [".claude/CLAUDE.md", "CLAUDE.md"],
    AgentTarget.AIDER: [".aider.conf.yml", "CONVENTIONS.md", ".aiderignore"],
    AgentTarget.CODEX: ["AGENTS.md", ".codex/instructions.md"],
    AgentTarget.GEMINI_CLI: ["GEMINI.md", ".gemini/instructions.md"],
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
    source_paths = detect_source_paths(root)
    test_paths = detect_test_paths(root)
    subproject_paths = detect_subproject_paths(root)
    instruction_scopes = build_instruction_scopes(source_paths, test_paths)
    instruction_globs = select_instruction_globs(source_paths, test_paths)
    targets = _detect_existing_targets(root)

    return ProjectContext(
        root_path=root,
        detected_languages=languages,
        detected_frameworks=frameworks,
        project_type=project_type,
        source_paths=source_paths,
        test_paths=test_paths,
        subproject_paths=subproject_paths,
        instruction_scopes=instruction_scopes,
        instruction_globs=instruction_globs,
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

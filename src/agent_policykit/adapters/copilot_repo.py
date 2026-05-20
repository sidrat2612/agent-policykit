"""Copilot repo-level adapter — generates .github/copilot-instructions.md."""

from __future__ import annotations

from agent_policykit.adapters import register_adapter
from agent_policykit.core.models import AdapterOutput, PolicyBundle, ProjectContext
from agent_policykit.core.output_limits import apply_output_limits
from agent_policykit.core.renderer import render_template
from agent_policykit.types import AgentTarget, MergeStrategy


@register_adapter(AgentTarget.COPILOT_REPO)
class CopilotRepoAdapter:
    """Generates .github/copilot-instructions.md for GitHub Copilot."""

    target = AgentTarget.COPILOT_REPO
    max_bytes = None
    max_lines = None

    def output_paths(self, context: ProjectContext) -> list[str]:
        return [".github/copilot-instructions.md"]

    def render(self, bundle: PolicyBundle, context: ProjectContext) -> list[AdapterOutput]:
        outputs = [
            AdapterOutput(
                path=".github/copilot-instructions.md",
                content=render_template("copilot_instructions.md.j2", bundle, context),
                merge_strategy=MergeStrategy.SECTION_MERGE,
            )
        ]
        return apply_output_limits(outputs, max_bytes=self.max_bytes, max_lines=self.max_lines)

    def supports_target(self, target: AgentTarget) -> bool:
        return target == AgentTarget.COPILOT_REPO

"""Copilot path-scoped adapter — generates .instructions.md files."""

from __future__ import annotations

from agent_policykit.adapters import register_adapter
from agent_policykit.core.models import AdapterOutput, PolicyBundle, ProjectContext
from agent_policykit.core.renderer import render_template
from agent_policykit.types import AgentTarget, MergeStrategy


@register_adapter(AgentTarget.COPILOT_PATH)
class CopilotPathAdapter:
    """Generates path-scoped .instructions.md files for Copilot."""

    target = AgentTarget.COPILOT_PATH

    def render(self, bundle: PolicyBundle, context: ProjectContext) -> list[AdapterOutput]:
        content = render_template("copilot_path.md.j2", bundle, context)
        return [
            AdapterOutput(
                path=".github/instructions/project.instructions.md",
                content=content,
                merge_strategy=MergeStrategy.OVERWRITE,
            )
        ]

    def supports_target(self, target: AgentTarget) -> bool:
        return target == AgentTarget.COPILOT_PATH

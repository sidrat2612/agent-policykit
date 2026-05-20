"""Gemini CLI adapter — generates .gemini/instructions.md."""

from __future__ import annotations

from agent_policykit.adapters import register_adapter
from agent_policykit.core.models import AdapterOutput, PolicyBundle, ProjectContext
from agent_policykit.core.renderer import render_template
from agent_policykit.types import AgentTarget, MergeStrategy


@register_adapter(AgentTarget.GEMINI_CLI)
class GeminiCliAdapter:
    """Generates .gemini/instructions.md for Google Gemini CLI."""

    target = AgentTarget.GEMINI_CLI

    def render(self, bundle: PolicyBundle, context: ProjectContext) -> list[AdapterOutput]:
        content = render_template("gemini_instructions.md.j2", bundle, context)
        return [
            AdapterOutput(
                path=".gemini/instructions.md",
                content=content,
                merge_strategy=MergeStrategy.OVERWRITE,
            )
        ]

    def supports_target(self, target: AgentTarget) -> bool:
        return target == AgentTarget.GEMINI_CLI

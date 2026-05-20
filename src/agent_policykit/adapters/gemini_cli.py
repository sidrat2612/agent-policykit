"""Gemini CLI adapter — generates GEMINI.md."""

from __future__ import annotations

from agent_policykit.adapters import register_adapter
from agent_policykit.core.models import AdapterOutput, PolicyBundle, ProjectContext
from agent_policykit.core.output_limits import apply_output_limits
from agent_policykit.core.renderer import render_template
from agent_policykit.types import AgentTarget, MergeStrategy


@register_adapter(AgentTarget.GEMINI_CLI)
class GeminiCliAdapter:
    """Generates GEMINI.md for Google Gemini CLI."""

    target = AgentTarget.GEMINI_CLI
    max_bytes = None
    max_lines = None

    def output_paths(self, context: ProjectContext) -> list[str]:
        return ["GEMINI.md"]

    def render(self, bundle: PolicyBundle, context: ProjectContext) -> list[AdapterOutput]:
        outputs = [
            AdapterOutput(
                path="GEMINI.md",
                content=render_template("gemini_instructions.md.j2", bundle, context),
                merge_strategy=MergeStrategy.OVERWRITE,
            )
        ]
        return apply_output_limits(outputs, max_bytes=self.max_bytes, max_lines=self.max_lines)

    def supports_target(self, target: AgentTarget) -> bool:
        return target == AgentTarget.GEMINI_CLI

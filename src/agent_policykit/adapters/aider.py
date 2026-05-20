"""Aider adapter — generates CONVENTIONS.md and .aider.conf.yml."""

from __future__ import annotations

from agent_policykit.adapters import register_adapter
from agent_policykit.core.models import AdapterOutput, PolicyBundle, ProjectContext
from agent_policykit.core.output_limits import apply_output_limits
from agent_policykit.core.renderer import render_template
from agent_policykit.types import AgentTarget, MergeStrategy


@register_adapter(AgentTarget.AIDER)
class AiderAdapter:
    """Generates Aider convention files."""

    target = AgentTarget.AIDER
    max_bytes = None
    max_lines = None

    def output_paths(self, context: ProjectContext) -> list[str]:
        return ["CONVENTIONS.md", ".aider.conf.yml"]

    def render(self, bundle: PolicyBundle, context: ProjectContext) -> list[AdapterOutput]:
        outputs = [
            AdapterOutput(
                path="CONVENTIONS.md",
                content=render_template("aider_conventions.md.j2", bundle, context),
                merge_strategy=MergeStrategy.SECTION_MERGE,
            ),
            AdapterOutput(
                path=".aider.conf.yml",
                content=render_template("aider_conf.yml.j2", bundle, context),
                merge_strategy=MergeStrategy.OVERWRITE,
            )
        ]
        return apply_output_limits(outputs, max_bytes=self.max_bytes, max_lines=self.max_lines)

    def supports_target(self, target: AgentTarget) -> bool:
        return target == AgentTarget.AIDER

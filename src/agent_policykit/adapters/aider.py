"""Aider adapter — generates CONVENTIONS.md and .aider.conf.yml."""

from __future__ import annotations

from agent_policykit.adapters import register_adapter
from agent_policykit.core.models import AdapterOutput, PolicyBundle, ProjectContext
from agent_policykit.core.renderer import render_template
from agent_policykit.types import AgentTarget, MergeStrategy


@register_adapter(AgentTarget.AIDER)
class AiderAdapter:
    """Generates Aider convention files."""

    target = AgentTarget.AIDER

    def render(self, bundle: PolicyBundle, context: ProjectContext) -> list[AdapterOutput]:
        conventions = render_template("aider_conventions.md.j2", bundle, context)
        config = render_template("aider_conf.yml.j2", bundle, context)
        return [
            AdapterOutput(
                path="CONVENTIONS.md",
                content=conventions,
                merge_strategy=MergeStrategy.SECTION_MERGE,
            ),
            AdapterOutput(
                path=".aider.conf.yml",
                content=config,
                merge_strategy=MergeStrategy.OVERWRITE,
            )
        ]

    def supports_target(self, target: AgentTarget) -> bool:
        return target == AgentTarget.AIDER

"""Aider adapter — generates .aider.conf.yml."""

from __future__ import annotations

from agent_policykit.adapters import register_adapter
from agent_policykit.core.models import AdapterOutput, PolicyBundle, ProjectContext
from agent_policykit.core.renderer import render_template
from agent_policykit.types import AgentTarget, MergeStrategy


@register_adapter(AgentTarget.AIDER)
class AiderAdapter:
    """Generates .aider.conf.yml for Aider."""

    target = AgentTarget.AIDER

    def render(self, bundle: PolicyBundle, context: ProjectContext) -> list[AdapterOutput]:
        content = render_template("aider_conf.yml.j2", bundle, context)
        return [
            AdapterOutput(
                path=".aider.conf.yml",
                content=content,
                merge_strategy=MergeStrategy.OVERWRITE,
            )
        ]

    def supports_target(self, target: AgentTarget) -> bool:
        return target == AgentTarget.AIDER

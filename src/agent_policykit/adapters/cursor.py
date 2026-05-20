"""Cursor adapter — generates .cursorrules."""

from __future__ import annotations

from agent_policykit.adapters import register_adapter
from agent_policykit.core.models import AdapterOutput, PolicyBundle, ProjectContext
from agent_policykit.core.renderer import render_template
from agent_policykit.types import AgentTarget, MergeStrategy


@register_adapter(AgentTarget.CURSOR)
class CursorAdapter:
    """Generates .cursorrules for Cursor IDE."""

    target = AgentTarget.CURSOR

    def render(self, bundle: PolicyBundle, context: ProjectContext) -> list[AdapterOutput]:
        content = render_template("cursor_rules.md.j2", bundle, context)
        return [
            AdapterOutput(
                path=".cursorrules",
                content=content,
                merge_strategy=MergeStrategy.OVERWRITE,
            )
        ]

    def supports_target(self, target: AgentTarget) -> bool:
        return target == AgentTarget.CURSOR

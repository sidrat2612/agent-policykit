"""Cursor adapter — generates .cursor/rules/*.mdc files."""

from __future__ import annotations

from agent_policykit.adapters import register_adapter
from agent_policykit.core.models import AdapterOutput, PolicyBundle, ProjectContext
from agent_policykit.core.output_limits import apply_output_limits
from agent_policykit.core.renderer import render_template
from agent_policykit.types import AgentTarget, MergeStrategy


@register_adapter(AgentTarget.CURSOR)
class CursorAdapter:
    """Generates Cursor rule files for Cursor IDE."""

    target = AgentTarget.CURSOR
    max_bytes = None
    max_lines = 500

    def output_paths(self, context: ProjectContext) -> list[str]:
        return [".cursor/rules/project.mdc"]

    def render(self, bundle: PolicyBundle, context: ProjectContext) -> list[AdapterOutput]:
        outputs = [
            AdapterOutput(
                path=".cursor/rules/project.mdc",
                content=render_template("cursor_rules.md.j2", bundle, context),
                merge_strategy=MergeStrategy.OVERWRITE,
            )
        ]
        return apply_output_limits(outputs, max_bytes=self.max_bytes, max_lines=self.max_lines)

    def supports_target(self, target: AgentTarget) -> bool:
        return target == AgentTarget.CURSOR

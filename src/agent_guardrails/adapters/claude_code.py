"""Claude Code adapter — generates CLAUDE.md."""

from __future__ import annotations

from agent_guardrails.adapters import register_adapter
from agent_guardrails.core.models import AdapterOutput, PolicyBundle, ProjectContext
from agent_guardrails.core.renderer import render_template
from agent_guardrails.types import AgentTarget, MergeStrategy


@register_adapter(AgentTarget.CLAUDE_CODE)
class ClaudeCodeAdapter:
    """Generates CLAUDE.md for Claude Code."""

    target = AgentTarget.CLAUDE_CODE

    def render(self, bundle: PolicyBundle, context: ProjectContext) -> list[AdapterOutput]:
        content = render_template("claude_code.md.j2", bundle, context)
        return [
            AdapterOutput(
                path="CLAUDE.md",
                content=content,
                merge_strategy=MergeStrategy.OVERWRITE,
            )
        ]

    def supports_target(self, target: AgentTarget) -> bool:
        return target == AgentTarget.CLAUDE_CODE

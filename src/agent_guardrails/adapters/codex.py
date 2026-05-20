"""Codex adapter — generates .codex/instructions.md."""

from __future__ import annotations

from agent_guardrails.adapters import register_adapter
from agent_guardrails.core.models import AdapterOutput, PolicyBundle, ProjectContext
from agent_guardrails.core.renderer import render_template
from agent_guardrails.types import AgentTarget, MergeStrategy


@register_adapter(AgentTarget.CODEX)
class CodexAdapter:
    """Generates .codex/instructions.md for OpenAI Codex CLI."""

    target = AgentTarget.CODEX

    def render(self, bundle: PolicyBundle, context: ProjectContext) -> list[AdapterOutput]:
        content = render_template("codex_instructions.md.j2", bundle, context)
        return [
            AdapterOutput(
                path=".codex/instructions.md",
                content=content,
                merge_strategy=MergeStrategy.OVERWRITE,
            )
        ]

    def supports_target(self, target: AgentTarget) -> bool:
        return target == AgentTarget.CODEX

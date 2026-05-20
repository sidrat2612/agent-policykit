"""Codex adapter — generates AGENTS.md."""

from __future__ import annotations

from agent_policykit.adapters import register_adapter
from agent_policykit.core.models import AdapterOutput, PolicyBundle, ProjectContext
from agent_policykit.core.renderer import render_template
from agent_policykit.types import AgentTarget, MergeStrategy


@register_adapter(AgentTarget.CODEX)
class CodexAdapter:
    """Generates AGENTS.md for OpenAI Codex CLI."""

    target = AgentTarget.CODEX

    def render(self, bundle: PolicyBundle, context: ProjectContext) -> list[AdapterOutput]:
        content = render_template("agents_md.md.j2", bundle, context)
        return [
            AdapterOutput(
                path="AGENTS.md",
                content=content,
                merge_strategy=MergeStrategy.SECTION_MERGE,
            )
        ]

    def supports_target(self, target: AgentTarget) -> bool:
        return target == AgentTarget.CODEX

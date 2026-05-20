"""AGENTS.md adapter — generates AGENTS.md for multi-agent support."""

from __future__ import annotations

from agent_policykit.adapters import register_adapter
from agent_policykit.core.models import AdapterOutput, PolicyBundle, ProjectContext
from agent_policykit.core.output_limits import apply_output_limits
from agent_policykit.core.renderer import render_template
from agent_policykit.types import AgentTarget, MergeStrategy


@register_adapter(AgentTarget.AGENTS_MD)
class AgentsMdAdapter:
    """Generates AGENTS.md for multi-agent systems (Copilot, Codex)."""

    target = AgentTarget.AGENTS_MD
    max_bytes = 32768
    max_lines = None

    def output_paths(self, context: ProjectContext) -> list[str]:
        return ["AGENTS.md", *[f"{subproject_path}/AGENTS.md" for subproject_path in context.subproject_paths]]

    def render(self, bundle: PolicyBundle, context: ProjectContext) -> list[AdapterOutput]:
        outputs = [
            AdapterOutput(
                path="AGENTS.md",
                content=render_template("agents_md.md.j2", bundle, context),
                merge_strategy=MergeStrategy.SECTION_MERGE,
            )
        ]
        for subproject_path in context.subproject_paths:
            outputs.append(
                AdapterOutput(
                    path=f"{subproject_path}/AGENTS.md",
                    content=render_template(
                        "agents_md.md.j2",
                        bundle,
                        context,
                        scope_path=subproject_path,
                    ),
                    merge_strategy=MergeStrategy.SECTION_MERGE,
                )
            )
        return apply_output_limits(outputs, max_bytes=self.max_bytes, max_lines=self.max_lines)

    def supports_target(self, target: AgentTarget) -> bool:
        return target == AgentTarget.AGENTS_MD

"""Copilot path-scoped adapter — generates .instructions.md files."""

from __future__ import annotations

from agent_policykit.adapters import register_adapter
from agent_policykit.core.models import AdapterOutput, InstructionScope, PolicyBundle, ProjectContext
from agent_policykit.core.output_limits import apply_output_limits
from agent_policykit.core.renderer import render_template
from agent_policykit.types import AgentTarget, MergeStrategy


@register_adapter(AgentTarget.COPILOT_PATH)
class CopilotPathAdapter:
    """Generates path-scoped .instructions.md files for Copilot."""

    target = AgentTarget.COPILOT_PATH
    max_bytes = None
    max_lines = None

    def output_paths(self, context: ProjectContext) -> list[str]:
        return [f".github/instructions/{scope.slug}.instructions.md" for scope in self._instruction_scopes(context)]

    def render(self, bundle: PolicyBundle, context: ProjectContext) -> list[AdapterOutput]:
        outputs: list[AdapterOutput] = []
        for scope in self._instruction_scopes(context):
            content = render_template("copilot_path.md.j2", bundle, context, scope=scope)
            outputs.append(
                AdapterOutput(
                    path=f".github/instructions/{scope.slug}.instructions.md",
                    content=content,
                    merge_strategy=MergeStrategy.OVERWRITE,
                )
            )
        return apply_output_limits(outputs, max_bytes=self.max_bytes, max_lines=self.max_lines)

    def supports_target(self, target: AgentTarget) -> bool:
        return target == AgentTarget.COPILOT_PATH

    def _instruction_scopes(self, context: ProjectContext) -> list[InstructionScope]:
        if context.instruction_scopes:
            return context.instruction_scopes
        return [
            InstructionScope(
                slug="project",
                display_name="project-wide",
                globs=context.instruction_globs or ["**/*"],
                description="Project-wide source files.",
            )
        ]

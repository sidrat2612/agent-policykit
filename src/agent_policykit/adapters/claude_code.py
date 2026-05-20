"""Claude Code adapter — generates CLAUDE.md."""

from __future__ import annotations

from dataclasses import replace

from agent_policykit.adapters import register_adapter
from agent_policykit.core.models import AdapterOutput, InstructionScope, PolicyBundle, ProjectContext
from agent_policykit.core.output_limits import apply_output_limits
from agent_policykit.core.renderer import render_template
from agent_policykit.types import AgentTarget, MergeStrategy


@register_adapter(AgentTarget.CLAUDE_CODE)
class ClaudeCodeAdapter:
    """Generates CLAUDE.md for Claude Code."""

    target = AgentTarget.CLAUDE_CODE
    max_bytes = None
    max_lines = 200
    shared_rule_path = ".claude/rules/shared.md"

    def output_paths(self, context: ProjectContext) -> list[str]:
        return [
            "CLAUDE.md",
            self.shared_rule_path,
            *[f".claude/rules/{scope.slug}.md" for scope in context.instruction_scopes],
        ]

    def render(self, bundle: PolicyBundle, context: ProjectContext) -> list[AdapterOutput]:
        outputs: list[AdapterOutput] = []
        rule_imports: list[str] = [self.shared_rule_path]

        root_bundle, shared_bundle = _split_shared_guidance(bundle)
        outputs.append(
            AdapterOutput(
                path=self.shared_rule_path,
                content=render_template(
                    "claude_rule.md.j2",
                    shared_bundle,
                    context,
                    scope=InstructionScope(
                        slug="shared",
                        display_name="shared guidance",
                        globs=["**/*"],
                        description=(
                            "Supplemental repository-wide Claude guidance emitted when shared rules are split "
                            "out of CLAUDE.md."
                        ),
                    ),
                ),
                merge_strategy=MergeStrategy.OVERWRITE,
            )
        )

        for scope in context.instruction_scopes:
            rule_path = f".claude/rules/{scope.slug}.md"
            content = render_template("claude_rule.md.j2", bundle, context, scope=scope)
            outputs.append(
                AdapterOutput(
                    path=rule_path,
                    content=content,
                    merge_strategy=MergeStrategy.OVERWRITE,
                )
            )
            rule_imports.append(rule_path)

        root_output = AdapterOutput(
            path="CLAUDE.md",
            content=render_template("claude_code.md.j2", root_bundle, context, rule_imports=rule_imports),
            merge_strategy=MergeStrategy.OVERWRITE,
        )
        outputs.insert(0, root_output)
        return apply_output_limits(outputs, max_bytes=self.max_bytes, max_lines=self.max_lines)

    def supports_target(self, target: AgentTarget) -> bool:
        return target == AgentTarget.CLAUDE_CODE


def _split_shared_guidance(bundle: PolicyBundle) -> tuple[PolicyBundle, PolicyBundle]:
    """Keep core governance/security in CLAUDE.md and move broader guidance into a shared import."""
    root_bundle = replace(
        bundle,
        compliance_rules=[],
        architecture_rules=[],
        review_rules=[],
        testing_rules=[],
        operations_rules=[],
        language_rules=[],
        framework_rules=[],
        project_type_rules=[],
    )
    shared_bundle = replace(
        bundle,
        governance_rules=[],
        security_rules=[],
        output_contract=[],
    )
    return root_bundle, shared_bundle

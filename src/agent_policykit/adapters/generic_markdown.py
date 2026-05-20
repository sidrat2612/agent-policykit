"""Generic markdown adapter for Tier 2 portability targets."""

from __future__ import annotations

from agent_policykit.adapters import register_adapter
from agent_policykit.core.models import AdapterOutput, PolicyBundle, ProjectContext
from agent_policykit.core.output_limits import apply_output_limits
from agent_policykit.core.renderer import render_template
from agent_policykit.types import AgentTarget, MergeStrategy

PLATFORM_MARKDOWN_EXPORTS: dict[AgentTarget, tuple[str, str]] = {
    AgentTarget.GENERIC_MARKDOWN: ("AGENT_POLICY.md", "Generic Markdown Compatibility"),
    AgentTarget.ROOCODE: ("AGENT_POLICY.roocode.md", "RooCode"),
    AgentTarget.WINDSURF: ("AGENT_POLICY.windsurf.md", "Windsurf"),
    AgentTarget.ZED: ("AGENT_POLICY.zed.md", "Zed"),
    AgentTarget.WARP: ("AGENT_POLICY.warp.md", "Warp"),
    AgentTarget.JUNIE: ("AGENT_POLICY.junie.md", "Junie"),
    AgentTarget.DEVIN: ("AGENT_POLICY.devin.md", "Devin"),
    AgentTarget.AMP: ("AGENT_POLICY.amp.md", "Amp"),
    AgentTarget.AUGMENT_CODE: ("AGENT_POLICY.augment-code.md", "Augment Code"),
    AgentTarget.FACTORY: ("AGENT_POLICY.factory.md", "Factory"),
    AgentTarget.JULES: ("AGENT_POLICY.jules.md", "Jules"),
    AgentTarget.GOOSE: ("AGENT_POLICY.goose.md", "goose"),
    AgentTarget.OPENCODE: ("AGENT_POLICY.opencode.md", "opencode"),
    AgentTarget.PHOENIX: ("AGENT_POLICY.phoenix.md", "Phoenix"),
    AgentTarget.SEMGREP: ("AGENT_POLICY.semgrep.md", "Semgrep"),
    AgentTarget.ONA: ("AGENT_POLICY.ona.md", "Ona"),
}


@register_adapter(AgentTarget.GENERIC_MARKDOWN)
class GenericMarkdownAdapter:
    """Generates a generic markdown instruction file for unsupported agent platforms."""

    target = AgentTarget.GENERIC_MARKDOWN
    output_path = PLATFORM_MARKDOWN_EXPORTS[AgentTarget.GENERIC_MARKDOWN][0]
    platform_name = PLATFORM_MARKDOWN_EXPORTS[AgentTarget.GENERIC_MARKDOWN][1]
    max_bytes = None
    max_lines = None

    def output_paths(self, context: ProjectContext) -> list[str]:
        return [self.output_path]

    def render(self, bundle: PolicyBundle, context: ProjectContext) -> list[AdapterOutput]:
        outputs = [
            AdapterOutput(
                path=self.output_path,
                content=render_template(
                    "generic_markdown.md.j2",
                    bundle,
                    context,
                    platform_name=self.platform_name,
                    platform_slug=self.target.value,
                    platform_heading=(
                        "Agent Policy" if self.target == AgentTarget.GENERIC_MARKDOWN else f"{self.platform_name} Instructions"
                    ),
                ),
                merge_strategy=MergeStrategy.SECTION_MERGE,
            )
        ]
        return apply_output_limits(outputs, max_bytes=self.max_bytes, max_lines=self.max_lines)

    def supports_target(self, target: AgentTarget) -> bool:
        return target == self.target


def _register_platform_adapter(target: AgentTarget, *, output_path: str, platform_name: str) -> None:
    adapter_name = "".join(part.title() for part in target.value.replace("-", " ").split()) + "Adapter"
    adapter_cls = type(
        adapter_name,
        (GenericMarkdownAdapter,),
        {
            "__doc__": f"Generates {output_path} for {platform_name}.",
            "target": target,
            "output_path": output_path,
            "platform_name": platform_name,
        },
    )
    register_adapter(target)(adapter_cls)


for _target, (_output_path, _platform_name) in PLATFORM_MARKDOWN_EXPORTS.items():
    if _target == AgentTarget.GENERIC_MARKDOWN:
        continue
    _register_platform_adapter(_target, output_path=_output_path, platform_name=_platform_name)

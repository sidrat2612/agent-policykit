"""Implementation for the init command."""

from __future__ import annotations

from pathlib import Path

import click

from agent_policykit.analysis.detector import detect_project_context
from agent_policykit.commands.common import console
from agent_policykit.types import AgentTarget

DEFAULT_INIT_TARGETS = [
    AgentTarget.COPILOT_REPO,
    AgentTarget.AGENTS_MD,
    AgentTarget.GENERIC_MARKDOWN,
]


def run_init() -> None:
    """Initialize agent-policykit config in the current repository."""
    root = Path.cwd()
    console.print("[bold]Initializing agent-policykit...[/bold]")

    context = detect_project_context(root)
    console.print(f"  Languages: {', '.join(context.detected_languages) or 'none detected'}")
    console.print(f"  Frameworks: {', '.join(context.detected_frameworks) or 'none detected'}")
    console.print(f"  Project type: {context.project_type.value if context.project_type else 'unknown'}")

    pyproject_path = root / "pyproject.toml"
    if not pyproject_path.exists():
        console.print("[yellow]No pyproject.toml found. Create one first.[/yellow]")
        return

    pyproject_text = pyproject_path.read_text(encoding="utf-8")
    if "[tool.agent-policykit]" in pyproject_text:
        console.print("[green]Already configured in pyproject.toml[/green]")
        console.print("\n[bold green]Done![/bold green] Run `agent-policykit generate` to create instruction files.")
        return

    if not click.confirm("Write a detected [tool.agent-policykit] section to pyproject.toml?", default=True):
        console.print("[yellow]Skipped configuration changes.[/yellow]")
        return

    suggested_targets = _suggest_targets(context)
    target_input = click.prompt(
        "Targets (comma-separated)",
        default=", ".join(target.value for target in suggested_targets),
        show_default=True,
    )
    review_mode = click.confirm("Enable review mode by default?", default=False)

    selected_targets = _parse_targets(target_input)
    config_block = _render_tool_config(selected_targets, review_mode=review_mode)
    separator = "\n\n" if pyproject_text and not pyproject_text.endswith("\n\n") else ""
    pyproject_path.write_text(pyproject_text.rstrip() + separator + config_block + "\n", encoding="utf-8")

    console.print("[green]Added [tool.agent-policykit] configuration to pyproject.toml[/green]")
    console.print("\nExample generated targets:")
    for target in selected_targets:
        console.print(f"  - {target.value}")

    console.print("\n[bold green]Done![/bold green] Run `agent-policykit generate` to create instruction files.")


def _suggest_targets(context) -> list[AgentTarget]:
    seen: set[AgentTarget] = set()
    suggestions: list[AgentTarget] = []
    for target in context.targets or DEFAULT_INIT_TARGETS:
        if target in seen:
            continue
        seen.add(target)
        suggestions.append(target)
    return suggestions or list(DEFAULT_INIT_TARGETS)


def _parse_targets(raw_targets: str) -> list[AgentTarget]:
    targets: list[AgentTarget] = []
    seen: set[AgentTarget] = set()
    for value in (part.strip() for part in raw_targets.split(",")):
        if not value:
            continue
        try:
            target = AgentTarget(value)
        except ValueError as exc:
            raise click.ClickException(f"Unknown target: {value}") from exc
        if target in seen:
            continue
        seen.add(target)
        targets.append(target)

    if not targets:
        raise click.ClickException("At least one target must be selected.")
    return targets


def _render_tool_config(targets: list[AgentTarget], *, review_mode: bool) -> str:
    lines = [
        "[tool.agent-policykit]",
        "targets = [" + ", ".join(f'\"{target.value}\"' for target in targets) + "]",
    ]
    if review_mode:
        lines.append("review_mode = true")
    return "\n".join(lines)

"""Shared helpers for CLI commands."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console

from agent_policykit.core.models import AdapterOutput, PolicyBundle, ProjectContext
from agent_policykit.types import AgentTarget

console = Console()
err_console = Console(stderr=True)


def dedupe_outputs(outputs: list[AdapterOutput]) -> list[AdapterOutput]:
    """Deduplicate identical outputs and fail fast on conflicting writes."""
    deduped: list[AdapterOutput] = []
    seen_by_path: dict[str, AdapterOutput] = {}

    for output in outputs:
        existing = seen_by_path.get(output.path)
        if existing is None:
            seen_by_path[output.path] = output
            deduped.append(output)
            continue

        if existing.content == output.content and existing.merge_strategy == output.merge_strategy:
            continue

        raise click.ClickException(
            f"Conflicting generated outputs for {output.path}. "
            "Multiple adapters are trying to write different content to the same file."
        )

    return deduped


def load_all_adapters() -> None:
    """Import all built-in adapters so they register themselves."""
    import agent_policykit.adapters.agents_md  # noqa: F401
    import agent_policykit.adapters.aider  # noqa: F401
    import agent_policykit.adapters.claude_code  # noqa: F401
    import agent_policykit.adapters.codex  # noqa: F401
    import agent_policykit.adapters.copilot_path  # noqa: F401
    import agent_policykit.adapters.copilot_repo  # noqa: F401
    import agent_policykit.adapters.cursor  # noqa: F401
    import agent_policykit.adapters.gemini_cli  # noqa: F401
    import agent_policykit.adapters.generic_markdown  # noqa: F401


def detect_context_and_bundle(
    root: Path,
    *,
    mode: str = "generate",
    verbose: bool = False,
) -> tuple[ProjectContext, PolicyBundle]:
    """Detect project context and build the policy bundle for the requested mode."""
    from agent_policykit.analysis.detector import detect_project_context
    from agent_policykit.core.merger import build_review_bundle
    from agent_policykit.core.policy_engine import build_policy_bundle

    context = detect_project_context(root)
    context.render_mode = mode
    if verbose:
        console.print(f"[dim]Detected: {context.detected_languages}, {context.detected_frameworks}[/dim]")

    bundle = build_policy_bundle(context)
    if mode == "review":
        bundle = build_review_bundle(bundle)
    return context, bundle


def resolve_targets(target_values: tuple[str, ...]) -> list[AgentTarget]:
    """Resolve CLI target strings into registered adapter targets."""
    from agent_policykit.adapters import list_adapters

    if not target_values:
        return list_adapters()

    targets: list[AgentTarget] = []
    for value in target_values:
        try:
            targets.append(AgentTarget(value))
        except ValueError as exc:
            err_console.print(f"[red]Unknown target: {value}[/red]")
            err_console.print(f"Available: {', '.join(target.value for target in list_adapters())}")
            raise SystemExit(1) from exc
    return targets


def render_outputs(
    targets: list[AgentTarget],
    bundle: PolicyBundle,
    context: ProjectContext,
) -> list[AdapterOutput]:
    """Render outputs for the selected targets and deduplicate shared paths."""
    from agent_policykit.adapters import get_adapter

    all_outputs: list[AdapterOutput] = []
    for agent_target in targets:
        adapter = get_adapter(agent_target)
        all_outputs.extend(adapter.render(bundle, context))
    return dedupe_outputs(all_outputs)

"""Implementation for the generate command."""

from __future__ import annotations

from pathlib import Path

from agent_policykit.commands.common import console, detect_context_and_bundle, load_all_adapters, render_outputs, resolve_targets
from agent_policykit.core.update_engine import apply_updates


def run_generate(*, target: tuple[str, ...], dry_run: bool, mode: str, verbose: bool) -> None:
    """Generate instruction files for configured agent targets."""
    root = Path.cwd()
    load_all_adapters()
    context, bundle = detect_context_and_bundle(root, mode=mode, verbose=verbose)
    console.print(f"[bold]Policy bundle: {len(bundle.all_rules())} rules[/bold]")

    targets = resolve_targets(target)
    all_outputs = render_outputs(targets, bundle, context)

    for output in all_outputs:
        console.print(f"  [green]✓[/green] {output.path} ({output.line_count} lines, {output.size_bytes} bytes)")
        for warning in output.warnings:
            console.print(f"    [yellow]⚠ {warning}[/yellow]")

    if dry_run:
        console.print("\n[yellow]Dry run — no files written.[/yellow]")
        return

    result = apply_updates(root, all_outputs)
    console.print(
        f"\n[bold green]Done![/bold green] {len(result.created)} created, {len(result.updated)} updated, {len(result.skipped)} skipped."
    )
    for item in result.updated:
        if item.message:
            console.print(f"  [yellow]⚠ {item.path}: {item.message}[/yellow]")
    for item in result.skipped:
        if item.message:
            console.print(f"  [yellow]⚠ {item.path}: {item.message}[/yellow]")

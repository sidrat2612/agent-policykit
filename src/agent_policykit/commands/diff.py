"""Implementation for the diff command."""

from __future__ import annotations

from pathlib import Path

from agent_policykit.adapters import list_adapters
from agent_policykit.commands.common import console, detect_context_and_bundle, load_all_adapters, render_outputs


def run_diff() -> None:
    """Show diff between current and regenerated instruction files."""
    from agent_policykit.core.diff_engine import compute_diff

    root = Path.cwd()
    load_all_adapters()
    context, bundle = detect_context_and_bundle(root)
    all_outputs = render_outputs(list_adapters(), bundle, context)
    diff_result = compute_diff(root, all_outputs)

    if not diff_result.has_changes:
        console.print("[green]All files are up to date. No changes needed.[/green]")
        return

    for file_diff in diff_result.diffs:
        if file_diff.has_changes or file_diff.is_new:
            console.print(f"\n[bold]{file_diff.summary}[/bold]")
            for note in file_diff.notes:
                console.print(f"[yellow]⚠ {note}[/yellow]")
            if file_diff.unified_diff:
                for line in file_diff.unified_diff.splitlines():
                    if line.startswith("+"):
                        console.print(f"[green]{line}[/green]")
                    elif line.startswith("-"):
                        console.print(f"[red]{line}[/red]")
                    elif line.startswith("@@"):
                        console.print(f"[cyan]{line}[/cyan]")
                    else:
                        console.print(line)

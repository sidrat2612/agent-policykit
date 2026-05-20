"""Implementation for the update command."""

from __future__ import annotations

from pathlib import Path

from agent_policykit.adapters import get_adapter, list_adapters
from agent_policykit.analysis.detector import detect_project_context
from agent_policykit.commands.common import console, dedupe_outputs, load_all_adapters
from agent_policykit.core.diff_engine import compute_diff
from agent_policykit.core.policy_engine import build_policy_bundle
from agent_policykit.core.update_engine import apply_updates


def run_update(*, force: bool, dry_run: bool) -> None:
    """Update existing instruction files safely."""
    root = Path.cwd()
    load_all_adapters()

    context = detect_project_context(root)
    bundle = build_policy_bundle(context)

    all_outputs = []
    for agent_target in list_adapters():
        adapter = get_adapter(agent_target)
        for output in adapter.render(bundle, context):
            if (root / output.path).exists() or force:
                all_outputs.append(output)
    all_outputs = dedupe_outputs(all_outputs)

    if not all_outputs:
        console.print("[yellow]No existing instruction files found. Run `generate` first.[/yellow]")
        return

    diff_result = compute_diff(root, all_outputs)
    if not diff_result.has_changes:
        console.print("[green]All files are up to date.[/green]")
        return

    for file_diff in diff_result.diffs:
        if file_diff.has_changes or file_diff.is_new:
            console.print(f"  {file_diff.summary}")
            for note in file_diff.notes:
                console.print(f"    [yellow]⚠ {note}[/yellow]")

    if dry_run:
        console.print("\n[yellow]Dry run — no files written.[/yellow]")
        return

    result = apply_updates(root, all_outputs, force=force)
    console.print(
        f"\n[bold green]Updated![/bold green] {len(result.updated)} files changed, {len(result.skipped)} skipped."
    )
    for item in result.updated:
        if item.message:
            console.print(f"  [yellow]⚠ {item.path}: {item.message}[/yellow]")
    for item in result.skipped:
        if item.message:
            console.print(f"  [yellow]⚠ {item.path}: {item.message}[/yellow]")

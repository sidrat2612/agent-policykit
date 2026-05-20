"""Implementation for the validate command."""

from __future__ import annotations

from agent_policykit.commands.common import console
from agent_policykit.core.loader import PACKS_DIR, load_packs_from_directory
from agent_policykit.core.validator import validate_packs


def run_validate() -> None:
    """Validate all rule packs for correctness."""
    console.print("[bold]Validating all rule packs...[/bold]")

    all_packs = []
    for category_dir in ["governance", "languages", "frameworks", "project_types"]:
        dir_path = PACKS_DIR / category_dir
        packs = load_packs_from_directory(dir_path)
        all_packs.extend(packs)
        console.print(f"  Loaded {len(packs)} packs from {category_dir}/")

    result = validate_packs(all_packs)

    if result.errors:
        console.print(f"\n[red]✗ {len(result.errors)} errors:[/red]")
        for error in result.errors:
            console.print(f"  [red]• {error}[/red]")

    if result.warnings:
        console.print(f"\n[yellow]⚠ {len(result.warnings)} warnings:[/yellow]")
        for warning in result.warnings:
            console.print(f"  [yellow]• {warning}[/yellow]")

    if result.is_valid:
        total_rules = sum(len(pack.rules) for pack in all_packs)
        console.print(f"\n[bold green]✓ All {len(all_packs)} packs valid ({total_rules} total rules)[/bold green]")
        return

    raise SystemExit(1)

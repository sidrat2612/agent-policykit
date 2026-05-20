"""CLI entry point for agent-policykit."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from agent_policykit import __version__

console = Console()
err_console = Console(stderr=True)


def _dedupe_outputs(outputs):
    """Deduplicate identical outputs and fail fast on conflicting writes."""
    deduped = []
    seen_by_path = {}

    for output in outputs:
        existing = seen_by_path.get(output.path)
        if existing is None:
            seen_by_path[output.path] = output
            deduped.append(output)
            continue

        if (
            existing.content == output.content
            and existing.merge_strategy == output.merge_strategy
        ):
            continue

        raise click.ClickException(
            f"Conflicting generated outputs for {output.path}. "
            "Multiple adapters are trying to write different content to the same file."
        )

    return deduped


@click.group()
@click.version_option(version=__version__, prog_name="agent-policykit")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """Universal instruction compiler for coding agents."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


@main.command()
@click.pass_context
def init(ctx: click.Context) -> None:
    """Initialize agent-policykit config in the current repository."""
    from agent_policykit.analysis.detector import detect_project_context
    from agent_policykit.config import Config

    root = Path.cwd()
    console.print("[bold]Initializing agent-policykit...[/bold]")

    # Detect project context
    context = detect_project_context(root)
    console.print(f"  Languages: {', '.join(context.detected_languages) or 'none detected'}")
    console.print(f"  Frameworks: {', '.join(context.detected_frameworks) or 'none detected'}")
    console.print(f"  Project type: {context.project_type.value if context.project_type else 'unknown'}")

    # Check if pyproject.toml exists
    pyproject_path = root / "pyproject.toml"
    if not pyproject_path.exists():
        console.print("[yellow]No pyproject.toml found. Create one first.[/yellow]")
        return

    # Check if already configured
    try:
        config = Config.from_pyproject(root)
        console.print("[green]Already configured in pyproject.toml[/green]")
    except Exception:
        console.print("[yellow]Add [tool.agent-policykit] section to pyproject.toml[/yellow]")
        console.print("\nExample:")
        console.print('  [tool.agent-policykit]')
        console.print('  targets = ["copilot", "cursor", "claude-code"]')

    console.print("\n[bold green]Done![/bold green] Run `agent-policykit generate` to create instruction files.")


@main.command()
@click.pass_context
def detect(ctx: click.Context) -> None:
    """Detect repository languages, frameworks, and project type."""
    from agent_policykit.analysis.detector import detect_project_context

    root = Path.cwd()
    context = detect_project_context(root)

    table = Table(title="Repository Analysis")
    table.add_column("Property", style="bold")
    table.add_column("Value")

    table.add_row("Root", str(context.root_path))
    table.add_row("Languages", ", ".join(context.detected_languages) or "none")
    table.add_row("Frameworks", ", ".join(context.detected_frameworks) or "none")
    table.add_row("Project Type", context.project_type.value if context.project_type else "unknown")
    table.add_row("Existing Targets", ", ".join(t.value for t in context.targets) or "none")

    console.print(table)


@main.command()
@click.option("--target", "-t", multiple=True, help="Target agents to generate for (e.g., copilot, cursor, claude-code).")
@click.option("--dry-run", is_flag=True, help="Show output without writing files.")
@click.option("--mode", type=click.Choice(["generate", "review"]), default="generate", help="Mode: generate writes files, review shows only critical/high rules.")
@click.pass_context
def generate(ctx: click.Context, target: tuple[str, ...], dry_run: bool, mode: str) -> None:
    """Generate instruction files for configured agent targets."""
    from agent_policykit.adapters import get_adapter, list_adapters
    # Force adapter registration
    import agent_policykit.adapters.copilot_repo  # noqa: F401
    import agent_policykit.adapters.copilot_path  # noqa: F401
    import agent_policykit.adapters.agents_md  # noqa: F401
    import agent_policykit.adapters.cursor  # noqa: F401
    import agent_policykit.adapters.claude_code  # noqa: F401
    import agent_policykit.adapters.aider  # noqa: F401
    import agent_policykit.adapters.codex  # noqa: F401
    import agent_policykit.adapters.gemini_cli  # noqa: F401

    from agent_policykit.analysis.detector import detect_project_context
    from agent_policykit.core.merger import filter_bundle_by_severity
    from agent_policykit.core.policy_engine import build_policy_bundle
    from agent_policykit.core.update_engine import apply_updates
    from agent_policykit.types import AgentTarget

    root = Path.cwd()
    verbose = ctx.obj.get("verbose", False)

    # Detect context
    context = detect_project_context(root)
    if verbose:
        console.print(f"[dim]Detected: {context.detected_languages}, {context.detected_frameworks}[/dim]")

    # Build bundle
    bundle = build_policy_bundle(context)
    if mode == "review":
        bundle = filter_bundle_by_severity(bundle, "high")
    console.print(f"[bold]Policy bundle: {len(bundle.all_rules())} rules[/bold]")

    # Determine targets
    targets: list[AgentTarget] = []
    if target:
        for t in target:
            try:
                targets.append(AgentTarget(t))
            except ValueError:
                err_console.print(f"[red]Unknown target: {t}[/red]")
                err_console.print(f"Available: {', '.join(at.value for at in list_adapters())}")
                raise SystemExit(1)
    else:
        # Use all registered adapters
        targets = list_adapters()

    # Generate for each target
    all_outputs = []
    for agent_target in targets:
        adapter = get_adapter(agent_target)
        outputs = adapter.render(bundle, context)
        all_outputs.extend(outputs)
    all_outputs = _dedupe_outputs(all_outputs)
    for out in all_outputs:
        console.print(f"  [green]✓[/green] {out.path} ({out.line_count} lines, {out.size_bytes} bytes)")
        if out.warnings:
            for warning in out.warnings:
                console.print(f"    [yellow]⚠ {warning}[/yellow]")

    # Write or dry-run
    if dry_run:
        console.print("\n[yellow]Dry run — no files written.[/yellow]")
    else:
        result = apply_updates(root, all_outputs)
        created = len(result.created)
        updated = len(result.updated)
        skipped = len(result.skipped)
        console.print(f"\n[bold green]Done![/bold green] {created} created, {updated} updated, {skipped} skipped.")
        for item in result.skipped:
            if item.message:
                console.print(f"  [yellow]⚠ {item.path}: {item.message}[/yellow]")


@main.command()
@click.option("--force", is_flag=True, help="Force overwrite even if security rules would be downgraded.")
@click.option("--dry-run", is_flag=True, help="Show diff without writing.")
@click.pass_context
def update(ctx: click.Context, force: bool, dry_run: bool) -> None:
    """Update existing instruction files safely."""
    import agent_policykit.adapters.copilot_repo  # noqa: F401
    import agent_policykit.adapters.copilot_path  # noqa: F401
    import agent_policykit.adapters.agents_md  # noqa: F401
    import agent_policykit.adapters.cursor  # noqa: F401
    import agent_policykit.adapters.claude_code  # noqa: F401
    import agent_policykit.adapters.aider  # noqa: F401
    import agent_policykit.adapters.codex  # noqa: F401
    import agent_policykit.adapters.gemini_cli  # noqa: F401

    from agent_policykit.adapters import get_adapter, list_adapters
    from agent_policykit.analysis.detector import detect_project_context
    from agent_policykit.core.diff_engine import compute_diff
    from agent_policykit.core.policy_engine import build_policy_bundle
    from agent_policykit.core.update_engine import apply_updates

    root = Path.cwd()
    context = detect_project_context(root)
    bundle = build_policy_bundle(context)

    # Generate all outputs
    all_outputs = []
    for agent_target in list_adapters():
        adapter = get_adapter(agent_target)
        outputs = adapter.render(bundle, context)
        # Only include outputs for files that already exist (update, not generate)
        for out in outputs:
            if (root / out.path).exists() or force:
                all_outputs.append(out)
    all_outputs = _dedupe_outputs(all_outputs)

    if not all_outputs:
        console.print("[yellow]No existing instruction files found. Run `generate` first.[/yellow]")
        return

    # Compute diff
    diff_result = compute_diff(root, all_outputs)

    if not diff_result.has_changes:
        console.print("[green]All files are up to date.[/green]")
        return

    # Show changes
    for file_diff in diff_result.diffs:
        if file_diff.has_changes or file_diff.is_new:
            console.print(f"  {file_diff.summary}")

    if dry_run:
        console.print("\n[yellow]Dry run — no files written.[/yellow]")
        return

    result = apply_updates(root, all_outputs, force=force)
    console.print(
        f"\n[bold green]Updated![/bold green] {len(result.updated)} files changed, {len(result.skipped)} skipped."
    )
    for item in result.skipped:
        if item.message:
            console.print(f"  [yellow]⚠ {item.path}: {item.message}[/yellow]")


@main.command()
@click.pass_context
def diff(ctx: click.Context) -> None:
    """Show diff between current and regenerated instruction files."""
    import agent_policykit.adapters.copilot_repo  # noqa: F401
    import agent_policykit.adapters.copilot_path  # noqa: F401
    import agent_policykit.adapters.agents_md  # noqa: F401
    import agent_policykit.adapters.cursor  # noqa: F401
    import agent_policykit.adapters.claude_code  # noqa: F401
    import agent_policykit.adapters.aider  # noqa: F401
    import agent_policykit.adapters.codex  # noqa: F401
    import agent_policykit.adapters.gemini_cli  # noqa: F401

    from agent_policykit.adapters import get_adapter, list_adapters
    from agent_policykit.analysis.detector import detect_project_context
    from agent_policykit.core.diff_engine import compute_diff
    from agent_policykit.core.policy_engine import build_policy_bundle

    root = Path.cwd()
    context = detect_project_context(root)
    bundle = build_policy_bundle(context)

    # Generate all outputs
    all_outputs = []
    for agent_target in list_adapters():
        adapter = get_adapter(agent_target)
        all_outputs.extend(adapter.render(bundle, context))
    all_outputs = _dedupe_outputs(all_outputs)

    diff_result = compute_diff(root, all_outputs)

    if not diff_result.has_changes:
        console.print("[green]All files are up to date. No changes needed.[/green]")
        return

    for file_diff in diff_result.diffs:
        if file_diff.has_changes or file_diff.is_new:
            console.print(f"\n[bold]{file_diff.summary}[/bold]")
            if file_diff.unified_diff:
                # Color the diff output
                for line in file_diff.unified_diff.splitlines():
                    if line.startswith("+"):
                        console.print(f"[green]{line}[/green]")
                    elif line.startswith("-"):
                        console.print(f"[red]{line}[/red]")
                    elif line.startswith("@@"):
                        console.print(f"[cyan]{line}[/cyan]")
                    else:
                        console.print(line)


@main.command()
@click.pass_context
def validate(ctx: click.Context) -> None:
    """Validate all rule packs for correctness."""
    from agent_policykit.core.loader import load_governance_packs, load_packs_from_directory, PACKS_DIR
    from agent_policykit.core.validator import validate_packs

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
        total_rules = sum(len(p.rules) for p in all_packs)
        console.print(f"\n[bold green]✓ All {len(all_packs)} packs valid ({total_rules} total rules)[/bold green]")
    else:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

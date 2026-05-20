"""CLI entry point for agent-policykit."""

from __future__ import annotations

import click

from agent_policykit import __version__
from agent_policykit.commands.detect import run_detect
from agent_policykit.commands.generate import run_generate
from agent_policykit.commands.init import run_init
from agent_policykit.commands.diff import run_diff
from agent_policykit.commands.update import run_update
from agent_policykit.commands.validate import run_validate


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
    run_init()


@main.command()
@click.pass_context
def detect(ctx: click.Context) -> None:
    """Detect repository languages, frameworks, and project type."""
    run_detect()


@main.command()
@click.option("--target", "-t", multiple=True, help="Target agents to generate for (e.g., copilot, cursor, claude-code).")
@click.option("--dry-run", is_flag=True, help="Show output without writing files.")
@click.option(
    "--mode",
    type=click.Choice(["generate", "review"]),
    default="generate",
    help="Mode: generate writes standard instructions, review activates the reviewer overlay.",
)
@click.pass_context
def generate(ctx: click.Context, target: tuple[str, ...], dry_run: bool, mode: str) -> None:
    """Generate instruction files for configured agent targets."""
    verbose = ctx.obj.get("verbose", False)
    run_generate(target=target, dry_run=dry_run, mode=mode, verbose=verbose)


@main.command()
@click.option("--force", is_flag=True, help="Force overwrite even if security rules would be downgraded.")
@click.option("--dry-run", is_flag=True, help="Show diff without writing.")
@click.pass_context
def update(ctx: click.Context, force: bool, dry_run: bool) -> None:
    """Update existing instruction files safely."""
    run_update(force=force, dry_run=dry_run)


@main.command()
@click.pass_context
def diff(ctx: click.Context) -> None:
    """Show diff between current and regenerated instruction files."""
    run_diff()


@main.command()
@click.pass_context
def validate(ctx: click.Context) -> None:
    """Validate all rule packs for correctness."""
    run_validate()


if __name__ == "__main__":
    main()

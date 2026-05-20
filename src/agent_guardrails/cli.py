"""CLI entry point for agent-guardrails."""

import click

from agent_guardrails import __version__


@click.group()
@click.version_option(version=__version__, prog_name="agent-guardrails")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """Universal instruction compiler for coding agents."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


@main.command()
@click.pass_context
def init(ctx: click.Context) -> None:
    """Initialize agent-guardrails config in the current repository."""
    click.echo("Initializing agent-guardrails configuration...")
    click.echo("(Not yet implemented)")


@main.command()
@click.pass_context
def detect(ctx: click.Context) -> None:
    """Detect repository languages, frameworks, and project type."""
    click.echo("Detecting repository stack...")
    click.echo("(Not yet implemented)")


@main.command()
@click.option("--target", "-t", multiple=True, help="Target agents to generate for.")
@click.option("--dry-run", is_flag=True, help="Show output without writing files.")
@click.option("--mode", type=click.Choice(["generate", "review"]), default="generate")
@click.pass_context
def generate(ctx: click.Context, target: tuple[str, ...], dry_run: bool, mode: str) -> None:
    """Generate instruction files for configured agent targets."""
    click.echo(f"Generating instructions (mode={mode}, dry_run={dry_run})...")
    click.echo("(Not yet implemented)")


@main.command()
@click.option("--force", is_flag=True, help="Allow security downgrades.")
@click.option("--dry-run", is_flag=True, help="Show diff without writing.")
@click.pass_context
def update(ctx: click.Context, force: bool, dry_run: bool) -> None:
    """Update existing instruction files safely."""
    click.echo("Updating instruction files...")
    click.echo("(Not yet implemented)")


@main.command()
@click.pass_context
def diff(ctx: click.Context) -> None:
    """Show diff between current and regenerated instruction files."""
    click.echo("Computing diff...")
    click.echo("(Not yet implemented)")


@main.command()
@click.pass_context
def validate(ctx: click.Context) -> None:
    """Validate existing instruction files against current policy bundle."""
    click.echo("Validating instruction files...")
    click.echo("(Not yet implemented)")


if __name__ == "__main__":
    main()

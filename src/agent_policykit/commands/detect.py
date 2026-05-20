"""Implementation for the detect command."""

from __future__ import annotations

from pathlib import Path

from rich.table import Table

from agent_policykit.analysis.detector import detect_project_context
from agent_policykit.commands.common import console


def run_detect() -> None:
    """Detect repository languages, frameworks, and project type."""
    context = detect_project_context(Path.cwd())

    table = Table(title="Repository Analysis")
    table.add_column("Property", style="bold")
    table.add_column("Value")

    table.add_row("Root", str(context.root_path))
    table.add_row("Languages", ", ".join(context.detected_languages) or "none")
    table.add_row("Frameworks", ", ".join(context.detected_frameworks) or "none")
    table.add_row("Project Type", context.project_type.value if context.project_type else "unknown")
    table.add_row("Existing Targets", ", ".join(target.value for target in context.targets) or "none")

    console.print(table)

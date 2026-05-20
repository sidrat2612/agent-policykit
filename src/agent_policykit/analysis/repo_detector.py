"""Repository detector compatibility wrapper."""

from __future__ import annotations

from pathlib import Path

from agent_policykit.analysis.detector import detect_project_context
from agent_policykit.core.models import ProjectContext


def detect_repository(root: Path) -> ProjectContext:
    """Detect repository context for the given project root."""
    return detect_project_context(root)
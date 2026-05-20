"""Validation tests for worked example repositories."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from agent_policykit.analysis.detector import detect_project_context
from agent_policykit.cli import main
from agent_policykit.types import ProjectType

REPO_ROOT = Path(__file__).resolve().parents[1]


class TestWorkedExamples:
    """Example repositories should stay in sync with detector and generator behavior."""

    def test_fastapi_example_detects_and_generates(self, monkeypatch):
        example_dir = REPO_ROOT / "examples" / "fastapi-service"
        ctx = detect_project_context(example_dir)

        assert "python" in ctx.detected_languages
        assert "fastapi" in ctx.detected_frameworks
        assert ctx.project_type == ProjectType.API_SERVICE

        runner = CliRunner()
        monkeypatch.chdir(example_dir)
        result = runner.invoke(
            main,
            ["generate", "--dry-run", "-t", "copilot", "-t", "copilot-path", "-t", "generic-markdown"],
        )
        assert result.exit_code == 0
        assert ".github/copilot-instructions.md" in result.output
        assert "AGENT_POLICY.md" in result.output

    def test_nextjs_example_detects_and_generates(self, monkeypatch):
        example_dir = REPO_ROOT / "examples" / "nextjs-app"
        ctx = detect_project_context(example_dir)

        assert "typescript" in ctx.detected_languages
        assert "nextjs" in ctx.detected_frameworks
        assert ctx.project_type == ProjectType.WEB_APP

        runner = CliRunner()
        monkeypatch.chdir(example_dir)
        result = runner.invoke(
            main,
            ["generate", "--dry-run", "-t", "copilot", "-t", "copilot-path", "-t", "generic-markdown"],
        )
        assert result.exit_code == 0
        assert ".github/instructions/app.instructions.md" in result.output
        assert "AGENT_POLICY.md" in result.output

    def test_rails_example_detects_and_generates(self, monkeypatch):
        example_dir = REPO_ROOT / "examples" / "rails-monolith"
        ctx = detect_project_context(example_dir)

        assert "ruby" in ctx.detected_languages
        assert "rails" in ctx.detected_frameworks
        assert ctx.project_type == ProjectType.MONOLITH

        runner = CliRunner()
        monkeypatch.chdir(example_dir)
        result = runner.invoke(
            main,
            ["generate", "--dry-run", "-t", "copilot", "-t", "copilot-path", "-t", "generic-markdown"],
        )
        assert result.exit_code == 0
        assert ".github/instructions/app.instructions.md" in result.output
        assert "AGENT_POLICY.md" in result.output

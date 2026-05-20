"""End-to-end CLI tests."""

from __future__ import annotations

from click.testing import CliRunner

from agent_policykit.cli import main


def _seed_python_repo(tmp_path):
    (tmp_path / "pyproject.toml").write_text(
        "[build-system]\nrequires = ['hatchling']\nbuild-backend = 'hatchling.build'\n\n"
        "[project]\nname = 'sample'\nversion = '0.1.0'\ndependencies = ['fastapi>=0.100']\n"
    )
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text("print('hello')\n")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_app.py").write_text("def test_placeholder():\n    assert True\n")


class TestCliEndToEnd:
    """Golden-path CLI tests."""

    def test_init_scaffolds_pyproject_config_interactively(self, tmp_path, monkeypatch):
        _seed_python_repo(tmp_path)
        monkeypatch.chdir(tmp_path)
        runner = CliRunner()

        result = runner.invoke(
            main,
            ["init"],
            input="\ncopilot, generic-markdown\ny\n",
        )

        assert result.exit_code == 0
        pyproject_content = (tmp_path / "pyproject.toml").read_text()
        assert "[tool.agent-policykit]" in pyproject_content
        assert 'targets = ["copilot", "generic-markdown"]' in pyproject_content
        assert "review_mode = true" in pyproject_content

    def test_generate_dry_run_supports_generic_markdown_and_review_mode(self, tmp_path, monkeypatch):
        _seed_python_repo(tmp_path)
        monkeypatch.chdir(tmp_path)
        runner = CliRunner()

        result = runner.invoke(main, ["generate", "--dry-run", "--mode", "review", "-t", "generic-markdown"])

        assert result.exit_code == 0
        assert "Policy bundle:" in result.output
        assert "AGENT_POLICY.md" in result.output

    def test_generate_then_update_reports_up_to_date_for_existing_targets(self, tmp_path, monkeypatch):
        _seed_python_repo(tmp_path)
        monkeypatch.chdir(tmp_path)
        runner = CliRunner()

        generate_result = runner.invoke(main, ["generate", "-t", "generic-markdown"])
        assert generate_result.exit_code == 0
        assert (tmp_path / "AGENT_POLICY.md").exists()

        update_result = runner.invoke(main, ["update", "--dry-run"])
        assert update_result.exit_code == 0
        assert "All files are up to date." in update_result.output

    def test_validate_command_passes_end_to_end(self, tmp_path, monkeypatch):
        _seed_python_repo(tmp_path)
        monkeypatch.chdir(tmp_path)
        runner = CliRunner()

        result = runner.invoke(main, ["validate"])

        assert result.exit_code == 0
        assert "All" in result.output
        assert "packs valid" in result.output

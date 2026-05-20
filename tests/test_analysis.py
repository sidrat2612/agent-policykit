"""Tests for analysis/detection modules."""

from pathlib import Path

import pytest

from agent_guardrails.analysis.detector import detect_project_context
from agent_guardrails.analysis.framework_detector import detect_frameworks
from agent_guardrails.analysis.language_detector import detect_languages
from agent_guardrails.analysis.project_type_detector import detect_project_type
from agent_guardrails.types import ProjectType


class TestLanguageDetector:
    """Tests for language detection."""

    def test_detect_python_from_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[project]\nname = 'test'")
        (tmp_path / "app.py").write_text("print('hello')")
        langs = detect_languages(tmp_path)
        assert "python" in langs

    def test_detect_typescript_from_tsconfig(self, tmp_path):
        (tmp_path / "tsconfig.json").write_text("{}")
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "index.ts").write_text("export {}")
        langs = detect_languages(tmp_path)
        assert "typescript" in langs

    def test_detect_go_from_gomod(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example.com/test")
        (tmp_path / "main.go").write_text("package main")
        langs = detect_languages(tmp_path)
        assert "go" in langs

    def test_detect_multiple_languages(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[project]")
        (tmp_path / "app.py").write_text("")
        (tmp_path / "tsconfig.json").write_text("{}")
        (tmp_path / "ui.ts").write_text("")
        langs = detect_languages(tmp_path)
        assert "python" in langs
        assert "typescript" in langs

    def test_empty_directory(self, tmp_path):
        langs = detect_languages(tmp_path)
        assert langs == []

    def test_skips_node_modules(self, tmp_path):
        nm = tmp_path / "node_modules" / "pkg"
        nm.mkdir(parents=True)
        (nm / "index.js").write_text("")
        # Only node_modules content, nothing else
        langs = detect_languages(tmp_path)
        assert "javascript" not in langs


class TestFrameworkDetector:
    """Tests for framework detection."""

    def test_detect_fastapi_from_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text(
            '[project]\ndependencies = ["fastapi>=0.100"]'
        )
        frameworks = detect_frameworks(tmp_path)
        assert "fastapi" in frameworks

    def test_detect_nextjs_from_config(self, tmp_path):
        (tmp_path / "next.config.js").write_text("module.exports = {}")
        frameworks = detect_frameworks(tmp_path)
        assert "nextjs" in frameworks

    def test_detect_nextjs_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"next": "14.0"}}')
        frameworks = detect_frameworks(tmp_path)
        assert "nextjs" in frameworks

    def test_detect_spring_boot_from_deps(self, tmp_path):
        # go.mod-style detection (we'll test via requirements-like approach)
        (tmp_path / "requirements.txt").write_text("spring-boot-starter\n")
        frameworks = detect_frameworks(tmp_path)
        assert "spring_boot" in frameworks

    def test_no_frameworks_in_empty_dir(self, tmp_path):
        frameworks = detect_frameworks(tmp_path)
        assert frameworks == []


class TestProjectTypeDetector:
    """Tests for project type detection."""

    def test_detect_web_app_from_next_config(self, tmp_path):
        (tmp_path / "next.config.js").write_text("")
        (tmp_path / "components").mkdir()
        pt = detect_project_type(tmp_path, frameworks=["nextjs"])
        assert pt == ProjectType.WEB_APP

    def test_detect_api_service_from_frameworks(self, tmp_path):
        (tmp_path / "api").mkdir()
        pt = detect_project_type(tmp_path, frameworks=["fastapi"])
        assert pt == ProjectType.API_SERVICE

    def test_detect_monorepo(self, tmp_path):
        (tmp_path / "pnpm-workspace.yaml").write_text("packages:\n  - packages/*")
        (tmp_path / "packages").mkdir()
        pt = detect_project_type(tmp_path)
        assert pt == ProjectType.MONOREPO

    def test_detect_cli_tool(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project.scripts]\nmycli = "pkg:main"')
        pt = detect_project_type(tmp_path)
        assert pt == ProjectType.CLI_TOOL

    def test_unknown_project(self, tmp_path):
        (tmp_path / "readme.md").write_text("Hello")
        pt = detect_project_type(tmp_path)
        assert pt is None


class TestDetectProjectContext:
    """Tests for the unified detector."""

    def test_full_detection_python_fastapi(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text(
            '[project]\ndependencies = ["fastapi>=0.100"]\n[project.scripts]\nserve = "app:main"'
        )
        (tmp_path / "app").mkdir()
        (tmp_path / "app" / "main.py").write_text("")
        (tmp_path / "app" / "api").mkdir()
        (tmp_path / "app" / "api" / "routes.py").write_text("")

        ctx = detect_project_context(tmp_path)
        assert "python" in ctx.detected_languages
        assert "fastapi" in ctx.detected_frameworks
        assert ctx.project_type is not None

    def test_detects_existing_copilot_target(self, tmp_path):
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        (github_dir / "copilot-instructions.md").write_text("# Instructions")

        ctx = detect_project_context(tmp_path)
        from agent_guardrails.types import AgentTarget
        assert AgentTarget.COPILOT_REPO in ctx.targets

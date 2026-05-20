"""Tests for analysis/detection modules."""



from agent_policykit.analysis.detector import detect_project_context
from agent_policykit.analysis.framework_detector import detect_frameworks
from agent_policykit.analysis.language_detector import detect_languages
from agent_policykit.analysis.path_selector import (
    build_instruction_scopes,
    detect_source_paths,
    detect_subproject_paths,
    detect_test_paths,
    select_instruction_globs,
)
from agent_policykit.analysis.project_type_detector import detect_project_type
from agent_policykit.analysis.repo_detector import detect_repository
from agent_policykit.types import ProjectType


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

    def test_detect_scala_from_build_sbt(self, tmp_path):
        (tmp_path / "build.sbt").write_text('name := "app"')
        langs = detect_languages(tmp_path)
        assert "scala" in langs

    def test_detect_bash_from_script_extension(self, tmp_path):
        (tmp_path / "script.sh").write_text("#!/usr/bin/env bash\necho hi\n")
        langs = detect_languages(tmp_path)
        assert "bash" in langs

    def test_detect_powershell_from_extension(self, tmp_path):
        (tmp_path / "task.ps1").write_text("Write-Host 'hi'\n")
        langs = detect_languages(tmp_path)
        assert "powershell" in langs

    def test_detect_clojure_from_marker(self, tmp_path):
        (tmp_path / "deps.edn").write_text("{}")
        langs = detect_languages(tmp_path)
        assert "clojure" in langs

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

    def test_detect_laravel_from_composer_json(self, tmp_path):
        (tmp_path / "composer.json").write_text('{"require": {"laravel/framework": "^11.0"}}')
        frameworks = detect_frameworks(tmp_path)
        assert "laravel" in frameworks

    def test_detect_rails_from_gemfile(self, tmp_path):
        (tmp_path / "Gemfile").write_text("gem 'rails'\n")
        frameworks = detect_frameworks(tmp_path)
        assert "rails" in frameworks

    def test_detect_aspnet_from_csproj(self, tmp_path):
        (tmp_path / "web.csproj").write_text('<Project Sdk="Microsoft.NET.Sdk.Web"></Project>')
        frameworks = detect_frameworks(tmp_path)
        assert "aspnet" in frameworks

    def test_detect_chi_from_go_mod_require(self, tmp_path):
        (tmp_path / "go.mod").write_text(
            "module example.com/test\n\nrequire github.com/go-chi/chi/v5 v5.0.0\n"
        )
        frameworks = detect_frameworks(tmp_path)
        assert "chi" in frameworks

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

    def test_detect_worker(self, tmp_path):
        (tmp_path / "workers").mkdir()
        pt = detect_project_type(tmp_path)
        assert pt == ProjectType.WORKER

    def test_detect_mobile_app(self, tmp_path):
        (tmp_path / "ios").mkdir()
        (tmp_path / "android").mkdir()
        pt = detect_project_type(tmp_path)
        assert pt == ProjectType.MOBILE_APP

    def test_detect_data_pipeline(self, tmp_path):
        (tmp_path / "dags").mkdir()
        pt = detect_project_type(tmp_path)
        assert pt == ProjectType.DATA_PIPELINE

    def test_detect_monolith_from_frameworks(self, tmp_path):
        (tmp_path / "domains").mkdir()
        pt = detect_project_type(tmp_path, frameworks=["django"])
        assert pt == ProjectType.MONOLITH

    def test_unknown_project(self, tmp_path):
        (tmp_path / "readme.md").write_text("Hello")
        pt = detect_project_type(tmp_path)
        assert pt is None


class TestPathSelector:
    """Tests for path selection helpers."""

    def test_detect_source_and_test_paths(self, tmp_path):
        (tmp_path / "src").mkdir()
        (tmp_path / "tests").mkdir()

        assert detect_source_paths(tmp_path) == ["src"]
        assert detect_test_paths(tmp_path) == ["tests"]

    def test_select_instruction_globs_uses_detected_paths(self):
        globs = select_instruction_globs(["src", "app"], ["tests"])
        assert globs == ["src/**/*", "app/**/*", "tests/**/*"]

    def test_build_instruction_scopes_separates_source_and_test_paths(self):
        scopes = build_instruction_scopes(["src"], ["tests"])
        assert [scope.slug for scope in scopes] == ["src", "tests"]
        assert scopes[0].exclude_agent == "code-review"
        assert scopes[1].exclude_agent is None

    def test_select_instruction_globs_falls_back_to_catch_all(self):
        assert select_instruction_globs([], []) == ["**/*"]

    def test_detect_subproject_paths_finds_workspace_children(self, tmp_path):
        (tmp_path / "packages" / "api").mkdir(parents=True)
        (tmp_path / "packages" / "web").mkdir(parents=True)
        assert detect_subproject_paths(tmp_path) == ["packages/api", "packages/web"]


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
        assert "app" in ctx.source_paths
        assert [scope.slug for scope in ctx.instruction_scopes] == ["app"]
        assert "app/**/*" in ctx.instruction_globs

    def test_detects_existing_copilot_target(self, tmp_path):
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        (github_dir / "copilot-instructions.md").write_text("# Instructions")

        ctx = detect_project_context(tmp_path)
        from agent_policykit.types import AgentTarget
        assert AgentTarget.COPILOT_REPO in ctx.targets

    def test_detects_existing_copilot_path_target(self, tmp_path):
        instructions_dir = tmp_path / ".github" / "instructions"
        instructions_dir.mkdir(parents=True)
        (instructions_dir / "project.instructions.md").write_text("---\napplyTo: \"**/*\"\n---\n")

        ctx = detect_project_context(tmp_path)
        from agent_policykit.types import AgentTarget
        assert AgentTarget.COPILOT_PATH in ctx.targets

    def test_detects_existing_cursor_target(self, tmp_path):
        cursor_rules_dir = tmp_path / ".cursor" / "rules"
        cursor_rules_dir.mkdir(parents=True)
        (cursor_rules_dir / "project.mdc").write_text("---\ndescription: \"Rules\"\nglobs: \"**/*\"\nalwaysApply: true\n---\n")

        ctx = detect_project_context(tmp_path)
        from agent_policykit.types import AgentTarget
        assert AgentTarget.CURSOR in ctx.targets

    def test_detects_existing_aider_target(self, tmp_path):
        (tmp_path / ".aider.conf.yml").write_text("read: CONVENTIONS.md\n")
        (tmp_path / "CONVENTIONS.md").write_text("# Shared conventions\n")

        ctx = detect_project_context(tmp_path)
        from agent_policykit.types import AgentTarget
        assert AgentTarget.AIDER in ctx.targets

    def test_detects_existing_agents_target(self, tmp_path):
        (tmp_path / "AGENTS.md").write_text("# Shared instructions")

        ctx = detect_project_context(tmp_path)
        from agent_policykit.types import AgentTarget
        assert AgentTarget.AGENTS_MD in ctx.targets

    def test_detects_existing_gemini_target(self, tmp_path):
        (tmp_path / "GEMINI.md").write_text("# Gemini instructions")

        ctx = detect_project_context(tmp_path)
        from agent_policykit.types import AgentTarget
        assert AgentTarget.GEMINI_CLI in ctx.targets

    def test_detects_existing_roocode_target(self, tmp_path):
        (tmp_path / "AGENT_POLICY.roocode.md").write_text("# RooCode instructions")

        ctx = detect_project_context(tmp_path)
        from agent_policykit.types import AgentTarget
        assert AgentTarget.ROOCODE in ctx.targets

    def test_repo_detector_wrapper(self, tmp_path):
        (tmp_path / "src").mkdir()
        ctx = detect_repository(tmp_path)
        assert ctx.root_path == tmp_path.resolve()

    def test_detects_subproject_paths(self, tmp_path):
        (tmp_path / "pnpm-workspace.yaml").write_text("packages:\n  - packages/*\n")
        (tmp_path / "packages" / "api").mkdir(parents=True)
        (tmp_path / "packages" / "web").mkdir(parents=True)

        ctx = detect_project_context(tmp_path)
        assert ctx.subproject_paths == ["packages/api", "packages/web"]

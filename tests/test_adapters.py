"""Tests for adapters and renderer."""

from pathlib import Path

import pytest

from agent_policykit.adapters import get_adapter, list_adapters
from agent_policykit.adapters.agents_md import AgentsMdAdapter
from agent_policykit.adapters.aider import AiderAdapter
from agent_policykit.adapters.claude_code import ClaudeCodeAdapter
from agent_policykit.adapters.codex import CodexAdapter
from agent_policykit.adapters.copilot_path import CopilotPathAdapter
from agent_policykit.adapters.copilot_repo import CopilotRepoAdapter
from agent_policykit.adapters.cursor import CursorAdapter
from agent_policykit.adapters.gemini_cli import GeminiCliAdapter
from agent_policykit.adapters.generic_markdown import GenericMarkdownAdapter, PLATFORM_MARKDOWN_EXPORTS
from agent_policykit.analysis.path_selector import build_instruction_scopes
from agent_policykit.core.models import PolicyBundle, ProjectContext, Rule
from agent_policykit.core.policy_engine import build_policy_bundle
from agent_policykit.types import AgentTarget, MergeStrategy, ProjectType, RuleCategory, Severity


@pytest.fixture
def sample_context(tmp_path):
    return ProjectContext(
        root_path=tmp_path,
        detected_languages=["python"],
        detected_frameworks=["fastapi"],
        project_type=ProjectType.API_SERVICE,
    )


@pytest.fixture
def sample_bundle(sample_context):
    return build_policy_bundle(sample_context)


class TestAdapterRegistry:
    """Tests for the adapter registry."""

    def test_list_adapters_returns_registered(self):
        targets = list_adapters()
        assert AgentTarget.COPILOT_REPO in targets
        assert AgentTarget.COPILOT_PATH in targets
        assert AgentTarget.AGENTS_MD in targets
        assert AgentTarget.GENERIC_MARKDOWN in targets
        assert AgentTarget.ROOCODE in targets
        assert AgentTarget.WINDSURF in targets
        assert AgentTarget.PHOENIX in targets
        assert AgentTarget.CURSOR in targets
        assert AgentTarget.CLAUDE_CODE in targets
        assert AgentTarget.AIDER in targets
        assert AgentTarget.CODEX in targets
        assert AgentTarget.GEMINI_CLI in targets

    def test_get_adapter_returns_correct_type(self):
        adapter = get_adapter(AgentTarget.COPILOT_REPO)
        assert isinstance(adapter, CopilotRepoAdapter)


class TestCopilotRepoAdapter:
    """Tests for the Copilot repo adapter."""

    def test_render_produces_output(self, sample_bundle, sample_context):
        adapter = CopilotRepoAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        assert len(outputs) == 1
        assert outputs[0].path == ".github/copilot-instructions.md"
        assert outputs[0].merge_strategy == MergeStrategy.SECTION_MERGE

    def test_render_contains_managed_markers(self, sample_bundle, sample_context):
        adapter = CopilotRepoAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        content = outputs[0].content
        assert "<!-- agent-policykit:managed -->" in content
        assert "<!-- agent-policykit:end -->" in content

    def test_render_contains_rules(self, sample_bundle, sample_context):
        adapter = CopilotRepoAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        content = outputs[0].content
        assert "python" in content.lower()
        assert "fastapi" in content.lower()


class TestAgentsMdAdapter:
    """Tests for the AGENTS.md adapter."""

    def test_render_produces_output(self, sample_bundle, sample_context):
        adapter = AgentsMdAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        assert len(outputs) == 1
        assert outputs[0].path == "AGENTS.md"

    def test_render_has_sections(self, sample_bundle, sample_context):
        adapter = AgentsMdAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        content = outputs[0].content
        assert "## Engineering Standards" in content
        assert "### Security" in content
        assert "## Output Contract" in content

    def test_render_generates_nested_agents_for_subprojects(self, sample_bundle, tmp_path):
        adapter = AgentsMdAdapter()
        context = ProjectContext(
            root_path=tmp_path,
            detected_languages=["typescript"],
            project_type=ProjectType.MONOREPO,
            subproject_paths=["packages/api", "packages/web"],
        )

        outputs = adapter.render(sample_bundle, context)
        assert [output.path for output in outputs] == [
            "AGENTS.md",
            "packages/api/AGENTS.md",
            "packages/web/AGENTS.md",
        ]
        assert "nearest file to the working directory takes precedence" in outputs[1].content


class TestGenericMarkdownAdapter:
    """Tests for the generic markdown adapter."""

    def test_render_produces_generic_markdown_output(self, sample_bundle, sample_context):
        adapter = GenericMarkdownAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        assert len(outputs) == 1
        assert outputs[0].path == "AGENT_POLICY.md"
        assert outputs[0].merge_strategy == MergeStrategy.SECTION_MERGE
        assert "# Agent Policy" in outputs[0].content

    @pytest.mark.parametrize(
        "target",
        [
            AgentTarget.ROOCODE,
            AgentTarget.WINDSURF,
            AgentTarget.ZED,
            AgentTarget.WARP,
            AgentTarget.JUNIE,
            AgentTarget.DEVIN,
            AgentTarget.AMP,
            AgentTarget.AUGMENT_CODE,
            AgentTarget.FACTORY,
            AgentTarget.JULES,
            AgentTarget.GOOSE,
            AgentTarget.OPENCODE,
            AgentTarget.PHOENIX,
            AgentTarget.SEMGREP,
            AgentTarget.ONA,
        ],
    )
    def test_tier_two_alias_targets_use_generic_markdown_contract(self, target, sample_bundle, sample_context):
        adapter = get_adapter(target)
        outputs = adapter.render(sample_bundle, sample_context)
        assert outputs[0].path == PLATFORM_MARKDOWN_EXPORTS[target][0]
        assert PLATFORM_MARKDOWN_EXPORTS[target][1] in outputs[0].content
        assert adapter.supports_target(target)


class TestCopilotPathAdapter:
    """Tests for the Copilot path-scoped adapter."""

    def test_render_produces_scoped_output(self, sample_bundle, sample_context):
        adapter = CopilotPathAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        assert len(outputs) == 1
        assert outputs[0].path == ".github/instructions/project.instructions.md"
        assert outputs[0].merge_strategy == MergeStrategy.OVERWRITE

    def test_render_includes_applyto_frontmatter(self, sample_bundle, sample_context):
        adapter = CopilotPathAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        content = outputs[0].content
        assert content.startswith("---\napplyTo: \"**/*\"\n---\n")

    def test_render_splits_outputs_by_scope(self, sample_bundle, tmp_path):
        adapter = CopilotPathAdapter()
        context = ProjectContext(
            root_path=tmp_path,
            detected_languages=["python"],
            detected_frameworks=["fastapi"],
            project_type=ProjectType.API_SERVICE,
            source_paths=["src"],
            test_paths=["tests"],
            instruction_scopes=build_instruction_scopes(["src"], ["tests"]),
            instruction_globs=["src/**/*", "tests/**/*"],
        )

        outputs = adapter.render(sample_bundle, context)
        assert [output.path for output in outputs] == [
            ".github/instructions/src.instructions.md",
            ".github/instructions/tests.instructions.md",
        ]
        assert 'excludeAgent: "code-review"' in outputs[0].content
        assert 'excludeAgent: "code-review"' not in outputs[1].content
        assert adapter.output_paths(context) == [output.path for output in outputs]

    def test_review_mode_omits_excludeagent(self, sample_bundle, tmp_path):
        adapter = CopilotPathAdapter()
        context = ProjectContext(
            root_path=tmp_path,
            detected_languages=["python"],
            source_paths=["src"],
            instruction_scopes=build_instruction_scopes(["src"], []),
            instruction_globs=["src/**/*"],
            render_mode="review",
        )

        outputs = adapter.render(sample_bundle, context)
        assert "Review Mode" in outputs[0].content
        assert "excludeAgent" not in outputs[0].content


class TestCursorAdapter:
    """Tests for the Cursor adapter."""

    def test_render_produces_cursor_rule_file(self, sample_bundle, sample_context):
        adapter = CursorAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        assert len(outputs) == 1
        assert outputs[0].path == ".cursor/rules/project.mdc"
        assert outputs[0].merge_strategy == MergeStrategy.OVERWRITE

    def test_render_includes_cursor_frontmatter(self, sample_bundle, sample_context):
        adapter = CursorAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        content = outputs[0].content
        assert content.startswith(
            "---\ndescription: \"Repository-wide engineering rules\"\nglobs: \"**/*\"\nalwaysApply: true\n---\n"
        )


class TestClaudeCodeAdapter:
    """Tests for the Claude Code adapter."""

    def test_render_produces_claude_md(self, sample_bundle, sample_context):
        adapter = ClaudeCodeAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        assert len(outputs) == 2
        assert outputs[0].path == "CLAUDE.md"
        assert "## Engineering Standards" in outputs[0].content
        assert outputs[1].path == ".claude/rules/shared.md"

    def test_render_produces_path_rule_imports(self, sample_bundle, tmp_path):
        adapter = ClaudeCodeAdapter()
        context = ProjectContext(
            root_path=tmp_path,
            detected_languages=["python"],
            detected_frameworks=["fastapi"],
            project_type=ProjectType.API_SERVICE,
            source_paths=["src"],
            test_paths=["tests"],
            instruction_scopes=build_instruction_scopes(["src"], ["tests"]),
            instruction_globs=["src/**/*", "tests/**/*"],
        )

        outputs = adapter.render(sample_bundle, context)
        assert [output.path for output in outputs] == [
            "CLAUDE.md",
            ".claude/rules/shared.md",
            ".claude/rules/src.md",
            ".claude/rules/tests.md",
        ]
        assert "@.claude/rules/shared.md" in outputs[0].content
        assert "@.claude/rules/src.md" in outputs[0].content
        assert "paths:" in outputs[1].content

    def test_render_review_mode_adds_overlay(self, sample_bundle, sample_context):
        adapter = ClaudeCodeAdapter()
        sample_context.render_mode = "review"
        outputs = adapter.render(sample_bundle, sample_context)
        assert "Review Mode" in outputs[0].content


class TestAiderAdapter:
    """Tests for the Aider adapter."""

    def test_render_produces_conventions_and_conf(self, sample_bundle, sample_context):
        adapter = AiderAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        assert len(outputs) == 2
        output_paths = {output.path for output in outputs}
        assert "CONVENTIONS.md" in output_paths
        assert ".aider.conf.yml" in output_paths

        conventions = next(output for output in outputs if output.path == "CONVENTIONS.md")
        config = next(output for output in outputs if output.path == ".aider.conf.yml")
        assert conventions.merge_strategy == MergeStrategy.SECTION_MERGE
        assert config.merge_strategy == MergeStrategy.OVERWRITE

    def test_render_contains_conventions_reference(self, sample_bundle, sample_context):
        adapter = AiderAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        config = next(output for output in outputs if output.path == ".aider.conf.yml")
        conventions = next(output for output in outputs if output.path == "CONVENTIONS.md")
        assert "read: CONVENTIONS.md" in config.content
        assert "## Engineering Standards" in conventions.content


class TestCodexAdapter:
    """Tests for the Codex adapter."""

    def test_render_produces_agents_md(self, sample_bundle, sample_context):
        adapter = CodexAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        assert len(outputs) == 1
        assert outputs[0].path == "AGENTS.md"
        assert outputs[0].merge_strategy == MergeStrategy.SECTION_MERGE

    def test_render_contains_sections(self, sample_bundle, sample_context):
        adapter = CodexAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        content = outputs[0].content
        assert "## Engineering Standards" in content
        assert "## Security" in content

    def test_render_generates_nested_agents_for_subprojects(self, sample_bundle, tmp_path):
        adapter = CodexAdapter()
        context = ProjectContext(
            root_path=tmp_path,
            detected_languages=["typescript"],
            project_type=ProjectType.MONOREPO,
            subproject_paths=["packages/api"],
        )

        outputs = adapter.render(sample_bundle, context)
        assert [output.path for output in outputs] == [
            "AGENTS.md",
            "packages/api/AGENTS.md",
        ]

    def test_render_warns_when_agents_exceeds_size_limit(self, tmp_path):
        adapter = CodexAdapter()
        large_bundle = PolicyBundle(
            governance_rules=[
                Rule(
                    id=f"gov.{index}",
                    text=f"Governance rule {index} with enough repeated detail to build a large output body.",
                    category=RuleCategory.GOVERNANCE,
                    severity=Severity.HIGH,
                )
                for index in range(1200)
            ],
            security_rules=[
                Rule(
                    id=f"sec.{index}",
                    text=f"Security rule {index} with explicit checks and safe defaults.",
                    category=RuleCategory.SECURITY,
                    severity=Severity.HIGH,
                )
                for index in range(1200)
            ],
            testing_rules=[
                Rule(
                    id=f"test.{index}",
                    text=f"Testing rule {index} with required edge-case coverage.",
                    category=RuleCategory.TESTING,
                    severity=Severity.MEDIUM,
                )
                for index in range(1200)
            ],
        )
        context = ProjectContext(root_path=tmp_path)

        outputs = adapter.render(large_bundle, context)
        assert outputs[0].size_bytes <= adapter.max_bytes
        assert any("condensed" in warning for warning in outputs[0].warnings)


class TestAdapterOutputCondensing:
    """Tests for adapter-specific size condensing."""

    def test_cursor_condenses_large_outputs_to_line_limit(self, tmp_path):
        adapter = CursorAdapter()
        large_bundle = PolicyBundle(
            governance_rules=[
                Rule(
                    id=f"gov.{index}",
                    text=f"Governance rule {index} requiring long-form guidance.",
                    category=RuleCategory.GOVERNANCE,
                    severity=Severity.HIGH,
                )
                for index in range(800)
            ],
            security_rules=[
                Rule(
                    id=f"sec.{index}",
                    text=f"Security rule {index} requiring strong controls and explicit validation.",
                    category=RuleCategory.SECURITY,
                    severity=Severity.HIGH,
                )
                for index in range(800)
            ],
            framework_rules=[
                Rule(
                    id=f"fw.{index}",
                    text=f"Framework rule {index} covering structure and boundary concerns.",
                    category=RuleCategory.FRAMEWORK,
                    severity=Severity.MEDIUM,
                )
                for index in range(800)
            ],
        )
        context = ProjectContext(root_path=tmp_path)

        outputs = adapter.render(large_bundle, context)
        assert outputs[0].line_count <= adapter.max_lines
        assert any("condensed" in warning for warning in outputs[0].warnings)


class TestAdapterPathContracts:
    """Tests for adapter output path contracts."""

    def test_claude_output_paths_match_rendered_outputs(self, sample_bundle, tmp_path):
        adapter = ClaudeCodeAdapter()
        context = ProjectContext(
            root_path=tmp_path,
            instruction_scopes=build_instruction_scopes(["src"], ["tests"]),
        )

        outputs = adapter.render(sample_bundle, context)
        assert adapter.output_paths(context) == [output.path for output in outputs]

    def test_generic_markdown_output_paths_match_rendered_outputs(self, sample_bundle, sample_context):
        adapter = GenericMarkdownAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        assert adapter.output_paths(sample_context) == [output.path for output in outputs]


class TestGeminiCliAdapter:
    """Tests for the Gemini CLI adapter."""

    def test_render_produces_gemini_md(self, sample_bundle, sample_context):
        adapter = GeminiCliAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        assert len(outputs) == 1
        assert outputs[0].path == "GEMINI.md"
        assert outputs[0].merge_strategy == MergeStrategy.OVERWRITE

    def test_render_contains_sections(self, sample_bundle, sample_context):
        adapter = GeminiCliAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        content = outputs[0].content
        assert "## Engineering Standards" in content
        assert "python" in content.lower()


class TestReviewOverlayRendering:
    """Tests for shared review-mode rendering."""

    def test_repo_wide_templates_include_review_overlay(self, sample_bundle, sample_context):
        adapter = CopilotRepoAdapter()
        sample_context.render_mode = "review"
        outputs = adapter.render(sample_bundle, sample_context)
        assert "Review Mode" in outputs[0].content


class TestAdapterOutputSizes:
    """Verify output sizes are reasonable."""

    def test_all_adapters_produce_content(self, sample_bundle, sample_context):
        for target in list_adapters():
            adapter = get_adapter(target)
            outputs = adapter.render(sample_bundle, sample_context)
            for output in outputs:
                assert output.size_bytes > 0
                minimum_lines = 2 if output.path.endswith((".yml", ".yaml", ".toml", ".json")) else 10
                assert output.line_count >= minimum_lines

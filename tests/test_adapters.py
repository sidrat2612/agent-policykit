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
        assert outputs[0].path == ".github/AGENTS.md"

    def test_render_has_sections(self, sample_bundle, sample_context):
        adapter = AgentsMdAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        content = outputs[0].content
        assert "## Engineering Standards" in content
        assert "### Security" in content


class TestCursorAdapter:
    """Tests for the Cursor adapter."""

    def test_render_produces_cursorrules(self, sample_bundle, sample_context):
        adapter = CursorAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        assert len(outputs) == 1
        assert outputs[0].path == ".cursorrules"
        assert outputs[0].merge_strategy == MergeStrategy.OVERWRITE


class TestClaudeCodeAdapter:
    """Tests for the Claude Code adapter."""

    def test_render_produces_claude_md(self, sample_bundle, sample_context):
        adapter = ClaudeCodeAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        assert len(outputs) == 1
        assert outputs[0].path == "CLAUDE.md"
        assert "## Engineering Standards" in outputs[0].content


class TestAiderAdapter:
    """Tests for the Aider adapter."""

    def test_render_produces_aider_conf(self, sample_bundle, sample_context):
        adapter = AiderAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        assert len(outputs) == 1
        assert outputs[0].path == ".aider.conf.yml"
        assert outputs[0].merge_strategy == MergeStrategy.OVERWRITE

    def test_render_contains_conventions(self, sample_bundle, sample_context):
        adapter = AiderAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        content = outputs[0].content
        assert "conventions:" in content


class TestCodexAdapter:
    """Tests for the Codex adapter."""

    def test_render_produces_codex_instructions(self, sample_bundle, sample_context):
        adapter = CodexAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        assert len(outputs) == 1
        assert outputs[0].path == ".codex/instructions.md"
        assert outputs[0].merge_strategy == MergeStrategy.OVERWRITE

    def test_render_contains_sections(self, sample_bundle, sample_context):
        adapter = CodexAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        content = outputs[0].content
        assert "## Engineering Standards" in content
        assert "## Security" in content


class TestGeminiCliAdapter:
    """Tests for the Gemini CLI adapter."""

    def test_render_produces_gemini_instructions(self, sample_bundle, sample_context):
        adapter = GeminiCliAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        assert len(outputs) == 1
        assert outputs[0].path == ".gemini/instructions.md"
        assert outputs[0].merge_strategy == MergeStrategy.OVERWRITE

    def test_render_contains_sections(self, sample_bundle, sample_context):
        adapter = GeminiCliAdapter()
        outputs = adapter.render(sample_bundle, sample_context)
        content = outputs[0].content
        assert "## Engineering Standards" in content
        assert "python" in content.lower()


class TestAdapterOutputSizes:
    """Verify output sizes are reasonable."""

    def test_all_adapters_produce_content(self, sample_bundle, sample_context):
        for target in list_adapters():
            adapter = get_adapter(target)
            outputs = adapter.render(sample_bundle, sample_context)
            for output in outputs:
                assert output.size_bytes > 0
                assert output.line_count > 10

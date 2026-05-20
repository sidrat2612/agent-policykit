"""Tests for adapters and renderer."""

from pathlib import Path

import pytest

from agent_guardrails.adapters import get_adapter, list_adapters
from agent_guardrails.adapters.agents_md import AgentsMdAdapter
from agent_guardrails.adapters.claude_code import ClaudeCodeAdapter
from agent_guardrails.adapters.copilot_path import CopilotPathAdapter
from agent_guardrails.adapters.copilot_repo import CopilotRepoAdapter
from agent_guardrails.adapters.cursor import CursorAdapter
from agent_guardrails.core.models import PolicyBundle, ProjectContext, Rule
from agent_guardrails.core.policy_engine import build_policy_bundle
from agent_guardrails.types import AgentTarget, MergeStrategy, ProjectType, RuleCategory, Severity


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

    def test_get_adapter_returns_correct_type(self):
        adapter = get_adapter(AgentTarget.COPILOT_REPO)
        assert isinstance(adapter, CopilotRepoAdapter)

    def test_get_adapter_unknown_raises(self):
        with pytest.raises(ValueError, match="No adapter registered"):
            get_adapter(AgentTarget.AIDER)


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
        assert "<!-- agent-guardrails:managed -->" in content
        assert "<!-- agent-guardrails:end -->" in content

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


class TestAdapterOutputSizes:
    """Verify output sizes are reasonable."""

    def test_all_adapters_produce_content(self, sample_bundle, sample_context):
        for target in list_adapters():
            adapter = get_adapter(target)
            outputs = adapter.render(sample_bundle, sample_context)
            for output in outputs:
                assert output.size_bytes > 0
                assert output.line_count > 10

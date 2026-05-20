"""Tests for the diff and update engines."""



from agent_policykit.core.diff_engine import _extract_managed_section, compute_diff
from agent_policykit.core.models import AdapterOutput
from agent_policykit.core.update_engine import apply_updates
from agent_policykit.types import MergeStrategy


class TestDiffEngine:
    """Tests for diff computation."""

    def test_new_file_diff(self, tmp_path):
        outputs = [AdapterOutput(path="test.md", content="# Hello\nWorld\n")]
        result = compute_diff(tmp_path, outputs)
        assert result.has_changes
        assert len(result.new_files) == 1
        assert result.new_files[0].path == "test.md"

    def test_unchanged_file(self, tmp_path):
        content = "# Hello\nWorld\n"
        (tmp_path / "test.md").write_text(content)
        outputs = [AdapterOutput(path="test.md", content=content)]
        result = compute_diff(tmp_path, outputs)
        assert not result.has_changes
        assert len(result.unchanged_files) == 1

    def test_modified_file(self, tmp_path):
        (tmp_path / "test.md").write_text("# Old\n")
        outputs = [AdapterOutput(path="test.md", content="# New\n")]
        result = compute_diff(tmp_path, outputs)
        assert result.has_changes
        assert len(result.modified_files) == 1
        assert result.modified_files[0].added_lines > 0

    def test_managed_section_diff(self, tmp_path):
        existing = "# My Notes\n\n<!-- agent-policykit:managed -->\nOld rules\n<!-- agent-policykit:end -->\n\n# Custom\n"
        proposed = "<!-- agent-policykit:managed -->\nNew rules\n<!-- agent-policykit:end -->\n"
        (tmp_path / "test.md").write_text(existing)
        outputs = [AdapterOutput(path="test.md", content=proposed)]
        result = compute_diff(tmp_path, outputs)
        assert result.has_changes

    def test_managed_section_unchanged(self, tmp_path):
        managed = "<!-- agent-policykit:managed -->\nRules\n<!-- agent-policykit:end -->"
        existing = f"# Header\n\n{managed}\n\n# Custom\n"
        proposed = f"{managed}\n"
        (tmp_path / "test.md").write_text(existing)
        outputs = [AdapterOutput(path="test.md", content=proposed)]
        result = compute_diff(tmp_path, outputs)
        assert not result.has_changes

    def test_diff_surfaces_non_security_rule_removals(self, tmp_path):
        existing = (
            "<!-- agent-policykit:managed -->\n"
            "<!-- agent-policykit:rule-ids:governance=gov.alpha,gov.beta -->\n"
            "## Governance\n"
            "- Keep explicit boundaries\n"
            "<!-- agent-policykit:end -->\n"
        )
        proposed = (
            "<!-- agent-policykit:managed -->\n"
            "<!-- agent-policykit:rule-ids:governance=gov.alpha -->\n"
            "## Governance\n"
            "- Keep explicit boundaries\n"
            "<!-- agent-policykit:end -->\n"
        )
        (tmp_path / "test.md").write_text(existing)
        outputs = [AdapterOutput(path="test.md", content=proposed)]

        result = compute_diff(tmp_path, outputs)

        assert result.modified_files[0].notes
        assert "governance" in result.modified_files[0].notes[0]


class TestExtractManagedSection:
    """Tests for managed section extraction."""

    def test_extract_present(self):
        content = "header\n<!-- agent-policykit:managed -->\nstuff\n<!-- agent-policykit:end -->\nfooter"
        section = _extract_managed_section(content)
        assert section is not None
        assert "stuff" in section

    def test_extract_absent(self):
        content = "no markers here"
        assert _extract_managed_section(content) is None


class TestUpdateEngine:
    """Tests for applying updates to disk."""

    def test_creates_new_file(self, tmp_path):
        outputs = [AdapterOutput(path="new.md", content="# New")]
        result = apply_updates(tmp_path, outputs)
        assert len(result.created) == 1
        assert (tmp_path / "new.md").read_text() == "# New"

    def test_creates_nested_directories(self, tmp_path):
        outputs = [AdapterOutput(path=".github/copilot-instructions.md", content="# Rules")]
        result = apply_updates(tmp_path, outputs)
        assert len(result.created) == 1
        assert (tmp_path / ".github" / "copilot-instructions.md").exists()

    def test_skip_if_exists(self, tmp_path):
        (tmp_path / "existing.md").write_text("# Keep me")
        outputs = [AdapterOutput(path="existing.md", content="# Replace", merge_strategy=MergeStrategy.SKIP_IF_EXISTS)]
        result = apply_updates(tmp_path, outputs)
        assert len(result.skipped) == 1
        assert (tmp_path / "existing.md").read_text() == "# Keep me"

    def test_skip_if_exists_with_force(self, tmp_path):
        (tmp_path / "existing.md").write_text("# Keep me")
        outputs = [AdapterOutput(path="existing.md", content="# Replace", merge_strategy=MergeStrategy.SKIP_IF_EXISTS)]
        result = apply_updates(tmp_path, outputs, force=True)
        assert len(result.updated) == 1
        assert (tmp_path / "existing.md").read_text() == "# Replace"

    def test_overwrite_strategy(self, tmp_path):
        (tmp_path / "file.md").write_text("old")
        outputs = [AdapterOutput(path="file.md", content="new", merge_strategy=MergeStrategy.OVERWRITE)]
        result = apply_updates(tmp_path, outputs)
        assert len(result.updated) == 1
        assert (tmp_path / "file.md").read_text() == "new"

    def test_section_merge_preserves_user_content(self, tmp_path):
        existing = "# My Custom Header\n\n<!-- agent-policykit:managed -->\nOld rules\n<!-- agent-policykit:end -->\n\n# My Custom Footer\n"
        proposed = "<!-- agent-policykit:managed -->\nNew rules\n<!-- agent-policykit:end -->\n"
        (tmp_path / "file.md").write_text(existing)
        outputs = [AdapterOutput(path="file.md", content=proposed, merge_strategy=MergeStrategy.SECTION_MERGE)]
        result = apply_updates(tmp_path, outputs)
        assert len(result.updated) == 1
        content = (tmp_path / "file.md").read_text()
        assert "My Custom Header" in content
        assert "My Custom Footer" in content
        assert "New rules" in content
        assert "Old rules" not in content

    def test_unchanged_content_not_written(self, tmp_path):
        content = "unchanged"
        (tmp_path / "file.md").write_text(content)
        outputs = [AdapterOutput(path="file.md", content=content, merge_strategy=MergeStrategy.OVERWRITE)]
        result = apply_updates(tmp_path, outputs)
        assert result.results[0].action == "unchanged"

    def test_blocks_security_downgrade_on_overwrite(self, tmp_path):
        existing = "## Security\n- Keep authentication checks\n\n## Other\n- Stable\n"
        proposed = "## Security\n- Use validation\n\n## Other\n- Stable\n"
        (tmp_path / "file.md").write_text(existing)
        outputs = [AdapterOutput(path="file.md", content=proposed, merge_strategy=MergeStrategy.OVERWRITE)]
        result = apply_updates(tmp_path, outputs)
        assert len(result.skipped) == 1
        assert "downgraded" in result.skipped[0].message
        assert (tmp_path / "file.md").read_text() == existing

    def test_force_allows_security_downgrade(self, tmp_path):
        existing = "## Security\n- Keep authentication checks\n"
        proposed = "## Security\n- Use validation\n"
        (tmp_path / "file.md").write_text(existing)
        outputs = [AdapterOutput(path="file.md", content=proposed, merge_strategy=MergeStrategy.OVERWRITE)]
        result = apply_updates(tmp_path, outputs, force=True)
        assert len(result.updated) == 1
        assert (tmp_path / "file.md").read_text() == proposed

    def test_blocks_security_downgrade_on_section_merge(self, tmp_path):
        existing = "# Header\n\n<!-- agent-policykit:managed -->\n## Security\n- Keep authentication checks\n<!-- agent-policykit:end -->\n"
        proposed = "<!-- agent-policykit:managed -->\n## Security\n- Use validation\n<!-- agent-policykit:end -->\n"
        (tmp_path / "file.md").write_text(existing)
        outputs = [AdapterOutput(path="file.md", content=proposed, merge_strategy=MergeStrategy.SECTION_MERGE)]
        result = apply_updates(tmp_path, outputs)
        assert len(result.skipped) == 1
        assert (tmp_path / "file.md").read_text() == existing

    def test_allows_security_text_change_when_rule_ids_match(self, tmp_path):
        existing = (
            "<!-- agent-policykit:security-rule-ids=security.auth -->\n"
            "## Security\n"
            "- Keep authentication checks\n"
        )
        proposed = (
            "<!-- agent-policykit:security-rule-ids=security.auth -->\n"
            "## Security\n"
            "- Keep strong authentication and session checks\n"
        )
        (tmp_path / "file.md").write_text(existing)
        outputs = [AdapterOutput(path="file.md", content=proposed, merge_strategy=MergeStrategy.OVERWRITE)]

        result = apply_updates(tmp_path, outputs)

        assert len(result.updated) == 1
        assert (tmp_path / "file.md").read_text() == proposed

    def test_blocks_security_downgrade_when_rule_id_removed(self, tmp_path):
        existing = (
            "<!-- agent-policykit:security-rule-ids=security.auth,security.mfa -->\n"
            "## Security\n"
            "- Keep authentication checks\n"
            "- Require MFA for admin paths\n"
        )
        proposed = (
            "<!-- agent-policykit:security-rule-ids=security.auth -->\n"
            "## Security\n"
            "- Keep authentication checks\n"
        )
        (tmp_path / "file.md").write_text(existing)
        outputs = [AdapterOutput(path="file.md", content=proposed, merge_strategy=MergeStrategy.OVERWRITE)]

        result = apply_updates(tmp_path, outputs)

        assert len(result.skipped) == 1
        assert "downgraded" in result.skipped[0].message

    def test_surfaces_non_security_rule_removals_on_update(self, tmp_path):
        existing = (
            "<!-- agent-policykit:managed -->\n"
            "<!-- agent-policykit:rule-ids:governance=gov.alpha,gov.beta -->\n"
            "## Governance\n"
            "- Keep explicit boundaries\n"
            "<!-- agent-policykit:end -->\n"
        )
        proposed = (
            "<!-- agent-policykit:managed -->\n"
            "<!-- agent-policykit:rule-ids:governance=gov.alpha -->\n"
            "## Governance\n"
            "- Keep explicit boundaries\n"
            "<!-- agent-policykit:end -->\n"
        )
        (tmp_path / "file.md").write_text(existing)
        outputs = [AdapterOutput(path="file.md", content=proposed, merge_strategy=MergeStrategy.SECTION_MERGE)]

        result = apply_updates(tmp_path, outputs)

        assert len(result.updated) == 1
        assert "governance" in result.updated[0].message

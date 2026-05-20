"""Tests for the YAML pack loader."""

from pathlib import Path

import pytest

from agent_guardrails.core.loader import (
    PACKS_DIR,
    load_framework_pack,
    load_governance_packs,
    load_language_pack,
    load_pack_file,
    load_packs_from_directory,
    load_project_type_pack,
)
from agent_guardrails.core.models import RulePack
from agent_guardrails.types import RuleCategory


class TestLoadPackFile:
    """Tests for loading individual pack files."""

    def test_load_governance_base(self):
        path = PACKS_DIR / "governance" / "base.yaml"
        pack = load_pack_file(path)
        assert pack.id == "governance_base"
        assert pack.display_name == "Engineering Governance Baseline"
        assert pack.category == RuleCategory.GOVERNANCE
        assert len(pack.rules) > 0
        assert pack.priority == 100

    def test_load_security_pack(self):
        path = PACKS_DIR / "governance" / "security.yaml"
        pack = load_pack_file(path)
        assert pack.id == "governance_security"
        assert pack.category == RuleCategory.SECURITY
        assert pack.priority == 200
        assert any("auth" in r.id for r in pack.rules)

    def test_load_nonexistent_file_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_pack_file(tmp_path / "nonexistent.yaml")

    def test_load_empty_file_raises(self, tmp_path):
        empty_file = tmp_path / "empty.yaml"
        empty_file.write_text("")
        with pytest.raises(ValueError, match="empty or not a valid"):
            load_pack_file(empty_file)

    def test_load_file_missing_id_raises(self, tmp_path):
        bad_file = tmp_path / "bad.yaml"
        bad_file.write_text("display_name: test\nrules: []")
        with pytest.raises(ValueError, match="missing required 'id'"):
            load_pack_file(bad_file)


class TestLoadPacksFromDirectory:
    """Tests for loading all packs from a directory."""

    def test_load_governance_directory(self):
        packs = load_packs_from_directory(PACKS_DIR / "governance")
        assert len(packs) == 7
        pack_ids = {p.id for p in packs}
        assert "governance_base" in pack_ids
        assert "governance_security" in pack_ids
        assert "governance_compliance" in pack_ids
        assert "governance_review" in pack_ids
        assert "governance_architecture" in pack_ids
        assert "governance_testing" in pack_ids
        assert "governance_operations" in pack_ids

    def test_load_nonexistent_directory_returns_empty(self, tmp_path):
        packs = load_packs_from_directory(tmp_path / "nope")
        assert packs == []


class TestLoadGovernancePacks:
    """Tests for the convenience governance pack loader."""

    def test_loads_all_governance_packs(self):
        packs = load_governance_packs()
        assert len(packs) == 7
        # All should be governance-adjacent categories
        valid_categories = {
            RuleCategory.GOVERNANCE,
            RuleCategory.SECURITY,
            RuleCategory.COMPLIANCE,
            RuleCategory.REVIEW,
            RuleCategory.ARCHITECTURE,
            RuleCategory.TESTING,
            RuleCategory.OPERATIONS,
        }
        for pack in packs:
            assert pack.category in valid_categories

    def test_all_rules_have_text(self):
        packs = load_governance_packs()
        for pack in packs:
            for rule in pack.rules:
                assert rule.text.strip(), f"Rule {rule.id} has empty text"

    def test_all_rules_have_ids(self):
        packs = load_governance_packs()
        for pack in packs:
            for rule in pack.rules:
                assert rule.id, f"Rule in {pack.id} has empty ID"


class TestLoadLanguagePacks:
    """Tests for language pack loading."""

    @pytest.mark.parametrize("language,min_rules", [
        ("python", 35),
        ("typescript", 30),
        ("java", 30),
        ("go", 30),
        ("csharp", 30),
    ])
    def test_load_language_pack(self, language, min_rules):
        pack = load_language_pack(language)
        assert pack is not None
        assert pack.id == language
        assert pack.category == RuleCategory.LANGUAGE
        assert pack.priority == 50
        assert len(pack.rules) >= min_rules
        assert language in pack.applies_when.get("languages", [])

    def test_load_nonexistent_language_returns_none(self):
        assert load_language_pack("cobol") is None

    def test_language_rules_have_ids_and_text(self):
        for lang in ["python", "typescript", "java", "go", "csharp"]:
            pack = load_language_pack(lang)
            for rule in pack.rules:
                assert rule.id, f"Rule in {pack.id} has empty ID"
                assert rule.text.strip(), f"Rule {rule.id} has empty text"


class TestLoadFrameworkPacks:
    """Tests for framework pack loading."""

    @pytest.mark.parametrize("framework,extends,min_rules", [
        ("fastapi", "python", 20),
        ("nextjs", "typescript", 20),
        ("spring_boot", "java", 25),
    ])
    def test_load_framework_pack(self, framework, extends, min_rules):
        pack = load_framework_pack(framework)
        assert pack is not None
        assert pack.id == framework
        assert pack.category == RuleCategory.FRAMEWORK
        assert pack.priority == 60
        assert pack.extends_language == extends
        assert len(pack.rules) >= min_rules

    def test_load_nonexistent_framework_returns_none(self):
        assert load_framework_pack("django") is None


class TestLoadProjectTypePacks:
    """Tests for project-type pack loading."""

    @pytest.mark.parametrize("project_type,min_rules", [
        ("api_service", 20),
        ("web_app", 20),
        ("microservice", 25),
    ])
    def test_load_project_type_pack(self, project_type, min_rules):
        pack = load_project_type_pack(project_type)
        assert pack is not None
        assert pack.id == project_type
        assert pack.category == RuleCategory.PROJECT_TYPE
        assert len(pack.rules) >= min_rules

    def test_load_nonexistent_project_type_returns_none(self):
        assert load_project_type_pack("embedded") is None

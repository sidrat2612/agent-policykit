"""Tests for pack and bundle validation."""

import pytest

from agent_policykit.core.models import PolicyBundle, Rule, RulePack
from agent_policykit.core.validator import validate_bundle, validate_pack, validate_packs
from agent_policykit.types import RuleCategory, Severity


def _make_rule(id: str = "test.rule_1", text: str = "Test rule") -> Rule:
    return Rule(id=id, text=text, category=RuleCategory.GOVERNANCE)


def _make_pack(id: str = "test_pack", rules: list[Rule] | None = None) -> RulePack:
    return RulePack(
        id=id,
        display_name="Test Pack",
        category=RuleCategory.GOVERNANCE,
        rules=rules if rules is not None else [_make_rule()],
    )


class TestValidatePack:
    """Tests for single pack validation."""

    def test_valid_pack_passes(self):
        pack = _make_pack()
        result = validate_pack(pack)
        assert result.is_valid

    def test_empty_id_fails(self):
        pack = _make_pack(id="")
        result = validate_pack(pack)
        assert not result.is_valid

    def test_empty_rules_warns(self):
        pack = _make_pack(rules=[])
        result = validate_pack(pack)
        assert result.is_valid  # warning, not error
        assert len(result.warnings) > 0

    def test_empty_rule_text_fails(self):
        pack = _make_pack(rules=[Rule(id="bad", text="", category=RuleCategory.GOVERNANCE)])
        result = validate_pack(pack)
        assert not result.is_valid

    def test_duplicate_rule_ids_fails(self):
        rules = [_make_rule(id="dup"), _make_rule(id="dup")]
        pack = _make_pack(rules=rules)
        result = validate_pack(pack)
        assert not result.is_valid


class TestValidatePacks:
    """Tests for cross-pack validation."""

    def test_cross_pack_duplicate_warns(self):
        pack1 = _make_pack(id="pack1", rules=[_make_rule(id="shared.rule")])
        pack2 = _make_pack(id="pack2", rules=[_make_rule(id="shared.rule")])
        result = validate_packs([pack1, pack2])
        assert len(result.warnings) > 0


class TestValidateBundle:
    """Tests for policy bundle validation."""

    def test_empty_bundle_fails(self):
        bundle = PolicyBundle()
        result = validate_bundle(bundle)
        assert not result.is_valid

    def test_bundle_without_security_fails(self):
        bundle = PolicyBundle(governance_rules=[_make_rule()])
        result = validate_bundle(bundle)
        assert not result.is_valid

    def test_valid_bundle_passes(self):
        bundle = PolicyBundle(
            governance_rules=[_make_rule(id="gov.1")],
            security_rules=[_make_rule(id="sec.1")],
        )
        result = validate_bundle(bundle)
        assert result.is_valid

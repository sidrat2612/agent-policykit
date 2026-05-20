"""Tests for the pack merger and policy engine."""



from agent_policykit.core.merger import build_review_bundle, filter_bundle_by_severity, merge_packs
from agent_policykit.core.models import PolicyBundle, ProjectContext, Rule, RulePack
from agent_policykit.core.policy_engine import build_policy_bundle, list_available_packs
from agent_policykit.types import ProjectType, RuleCategory, Severity


def _make_rule(id: str, severity: Severity = Severity.MEDIUM) -> Rule:
    return Rule(id=id, text=f"Rule {id}", category=RuleCategory.GOVERNANCE, severity=severity)


def _make_pack(id: str, category: RuleCategory, priority: int, rules: list[Rule]) -> RulePack:
    return RulePack(
        id=id,
        display_name=id,
        category=category,
        rules=rules,
        priority=priority,
    )


class TestMergePacks:
    """Tests for merge_packs function."""

    def test_merge_single_pack(self):
        rules = [_make_rule("r1"), _make_rule("r2")]
        pack = _make_pack("p1", RuleCategory.GOVERNANCE, 100, rules)
        bundle = merge_packs([pack])
        assert len(bundle.governance_rules) == 2
        assert len(bundle.all_rules()) == 2

    def test_merge_multiple_categories(self):
        gov_pack = _make_pack("gov", RuleCategory.GOVERNANCE, 100, [_make_rule("g1")])
        sec_pack = _make_pack("sec", RuleCategory.SECURITY, 200, [
            Rule(id="s1", text="Security rule", category=RuleCategory.SECURITY, severity=Severity.HIGH)
        ])
        lang_pack = _make_pack("lang", RuleCategory.LANGUAGE, 50, [
            Rule(id="l1", text="Language rule", category=RuleCategory.LANGUAGE)
        ])
        bundle = merge_packs([gov_pack, sec_pack, lang_pack])
        assert len(bundle.governance_rules) == 1
        assert len(bundle.security_rules) == 1
        assert len(bundle.language_rules) == 1
        assert len(bundle.all_rules()) == 3

    def test_higher_priority_wins_on_duplicate_ids(self):
        low_rule = Rule(id="shared.r1", text="Low priority version", category=RuleCategory.GOVERNANCE)
        high_rule = Rule(id="shared.r1", text="High priority version", category=RuleCategory.GOVERNANCE)

        low_pack = _make_pack("low", RuleCategory.GOVERNANCE, 50, [low_rule])
        high_pack = _make_pack("high", RuleCategory.GOVERNANCE, 200, [high_rule])

        bundle = merge_packs([low_pack, high_pack])
        assert len(bundle.governance_rules) == 1
        assert bundle.governance_rules[0].text == "High priority version"

    def test_merge_empty_packs(self):
        bundle = merge_packs([])
        assert len(bundle.all_rules()) == 0

    def test_merge_preserves_all_unique_rules(self):
        pack1 = _make_pack("p1", RuleCategory.GOVERNANCE, 100, [_make_rule("a"), _make_rule("b")])
        pack2 = _make_pack("p2", RuleCategory.GOVERNANCE, 50, [_make_rule("c"), _make_rule("d")])
        bundle = merge_packs([pack1, pack2])
        assert len(bundle.governance_rules) == 4


class TestFilterBundleBySeverity:
    """Tests for severity filtering."""

    def test_filter_critical_only(self):
        bundle = PolicyBundle(
            governance_rules=[
                _make_rule("r1", Severity.LOW),
                _make_rule("r2", Severity.CRITICAL),
                _make_rule("r3", Severity.HIGH),
            ]
        )
        filtered = filter_bundle_by_severity(bundle, "critical")
        assert len(filtered.governance_rules) == 1
        assert filtered.governance_rules[0].id == "r2"

    def test_filter_medium_and_above(self):
        bundle = PolicyBundle(
            governance_rules=[
                _make_rule("r1", Severity.LOW),
                _make_rule("r2", Severity.MEDIUM),
                _make_rule("r3", Severity.HIGH),
                _make_rule("r4", Severity.CRITICAL),
            ]
        )
        filtered = filter_bundle_by_severity(bundle, "medium")
        assert len(filtered.governance_rules) == 3

    def test_filter_preserves_output_contract(self):
        contract_rule = _make_rule("contract.1", Severity.LOW)
        bundle = PolicyBundle(output_contract=[contract_rule])
        filtered = filter_bundle_by_severity(bundle, "critical")
        assert len(filtered.output_contract) == 1

    def test_build_review_bundle_preserves_review_rules(self):
        review_rule = Rule(
            id="rev.1",
            text="Review this carefully",
            category=RuleCategory.REVIEW,
            severity=Severity.INFO,
        )
        low_governance_rule = _make_rule("gov.1", Severity.LOW)
        bundle = PolicyBundle(
            governance_rules=[low_governance_rule],
            review_rules=[review_rule],
        )

        review_bundle = build_review_bundle(bundle)
        assert review_bundle.review_rules == [review_rule]
        assert review_bundle.governance_rules == []
        assert review_bundle.metadata["mode"] == "review"


class TestBuildPolicyBundle:
    """Tests for the policy engine's build_policy_bundle."""

    def test_python_fastapi_api_service(self, tmp_path):
        context = ProjectContext(
            root_path=tmp_path,
            detected_languages=["python"],
            detected_frameworks=["fastapi"],
            project_type=ProjectType.API_SERVICE,
        )
        bundle = build_policy_bundle(context)
        # Should have governance + python + fastapi + api_service rules
        assert len(bundle.governance_rules) > 0
        assert len(bundle.security_rules) > 0
        assert len(bundle.language_rules) > 0
        assert len(bundle.framework_rules) > 0
        assert len(bundle.project_type_rules) > 0
        assert bundle.metadata["context"]["pack_count"] >= 10  # 7 gov + 1 lang + 1 fw + 1 pt

    def test_typescript_nextjs_web_app(self, tmp_path):
        context = ProjectContext(
            root_path=tmp_path,
            detected_languages=["typescript"],
            detected_frameworks=["nextjs"],
            project_type=ProjectType.WEB_APP,
        )
        bundle = build_policy_bundle(context)
        assert len(bundle.language_rules) > 0
        assert len(bundle.framework_rules) > 0
        assert len(bundle.project_type_rules) > 0

    def test_minimal_context_governance_only(self, tmp_path):
        context = ProjectContext(root_path=tmp_path)
        bundle = build_policy_bundle(context)
        # Should still have governance rules
        assert len(bundle.all_rules()) > 0
        assert len(bundle.governance_rules) > 0
        # No language/framework/project-type rules
        assert len(bundle.language_rules) == 0
        assert len(bundle.framework_rules) == 0
        assert len(bundle.project_type_rules) == 0


class TestListAvailablePacks:
    """Tests for listing available packs."""

    def test_lists_all_categories(self):
        packs = list_available_packs()
        assert "governance" in packs
        assert "languages" in packs
        assert "frameworks" in packs
        assert "project_types" in packs

    def test_governance_has_expected_packs(self):
        packs = list_available_packs()
        assert "base" in packs["governance"]
        assert "security" in packs["governance"]

    def test_languages_has_expected_packs(self):
        packs = list_available_packs()
        assert "python" in packs["languages"]
        assert "typescript" in packs["languages"]

    def test_languages_include_expanded_targets(self):
        packs = list_available_packs()
        assert "javascript" in packs["languages"]
        assert "rust" in packs["languages"]
        assert "dart" in packs["languages"]

    def test_frameworks_include_expanded_targets(self):
        packs = list_available_packs()
        assert "django" in packs["frameworks"]
        assert "laravel" in packs["frameworks"]
        assert "chi" in packs["frameworks"]

    def test_project_types_include_expanded_targets(self):
        packs = list_available_packs()
        assert "worker" in packs["project_types"]
        assert "cli_tool" in packs["project_types"]
        assert "data_pipeline" in packs["project_types"]

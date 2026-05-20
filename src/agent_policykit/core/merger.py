"""Pack merger — combines multiple RulePacks into a PolicyBundle."""

from __future__ import annotations

from agent_policykit.core.models import PolicyBundle, Rule, RulePack
from agent_policykit.types import RuleCategory


def merge_packs(packs: list[RulePack]) -> PolicyBundle:
    """Merge multiple RulePacks into a single PolicyBundle.

    Packs are processed in priority order (highest priority wins on conflict).
    Duplicate rule IDs are resolved by keeping the higher-priority version.
    """
    # Sort packs by priority (highest first)
    sorted_packs = sorted(packs, key=lambda p: p.priority, reverse=True)

    seen_rule_ids: dict[str, int] = {}  # rule_id -> priority of pack that owns it
    bundle = PolicyBundle()

    for pack in sorted_packs:
        for rule in pack.rules:
            if rule.id in seen_rule_ids:
                # Higher-priority pack already claimed this rule
                continue
            seen_rule_ids[rule.id] = pack.priority
            _add_rule_to_bundle(bundle, rule, pack.category)

    return bundle


def _add_rule_to_bundle(bundle: PolicyBundle, rule: Rule, pack_category: RuleCategory) -> None:
    """Route a rule to the correct category list in the bundle."""
    category_map = {
        RuleCategory.GOVERNANCE: bundle.governance_rules,
        RuleCategory.SECURITY: bundle.security_rules,
        RuleCategory.COMPLIANCE: bundle.compliance_rules,
        RuleCategory.ARCHITECTURE: bundle.architecture_rules,
        RuleCategory.REVIEW: bundle.review_rules,
        RuleCategory.TESTING: bundle.testing_rules,
        RuleCategory.OPERATIONS: bundle.operations_rules,
        RuleCategory.LANGUAGE: bundle.language_rules,
        RuleCategory.FRAMEWORK: bundle.framework_rules,
        RuleCategory.PROJECT_TYPE: bundle.project_type_rules,
    }
    target_list = category_map.get(pack_category)
    if target_list is not None:
        target_list.append(rule)
    else:
        # Fallback: use rule's own category
        fallback = category_map.get(rule.category)
        if fallback is not None:
            fallback.append(rule)


def filter_bundle_by_severity(bundle: PolicyBundle, min_severity: str = "low") -> PolicyBundle:
    """Return a new bundle with only rules at or above the given severity."""
    from agent_policykit.types import Severity

    severity_order = [Severity.INFO, Severity.LOW, Severity.MEDIUM, Severity.HIGH, Severity.CRITICAL]
    min_idx = severity_order.index(Severity(min_severity))

    def passes(rule: Rule) -> bool:
        return severity_order.index(rule.severity) >= min_idx

    return PolicyBundle(
        governance_rules=[r for r in bundle.governance_rules if passes(r)],
        security_rules=[r for r in bundle.security_rules if passes(r)],
        compliance_rules=[r for r in bundle.compliance_rules if passes(r)],
        architecture_rules=[r for r in bundle.architecture_rules if passes(r)],
        review_rules=[r for r in bundle.review_rules if passes(r)],
        testing_rules=[r for r in bundle.testing_rules if passes(r)],
        operations_rules=[r for r in bundle.operations_rules if passes(r)],
        language_rules=[r for r in bundle.language_rules if passes(r)],
        framework_rules=[r for r in bundle.framework_rules if passes(r)],
        project_type_rules=[r for r in bundle.project_type_rules if passes(r)],
        output_contract=bundle.output_contract,
        metadata=bundle.metadata,
    )

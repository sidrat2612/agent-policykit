"""Validation for packs and policy bundles."""

from __future__ import annotations

from dataclasses import dataclass, field

from agent_guardrails.core.models import PolicyBundle, Rule, RulePack


@dataclass
class ValidationError:
    """A single validation error."""

    message: str
    source: str = ""
    severity: str = "error"


@dataclass
class ValidationResult:
    """Result of a validation operation."""

    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[ValidationError] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def add_error(self, message: str, source: str = "") -> None:
        self.errors.append(ValidationError(message=message, source=source, severity="error"))

    def add_warning(self, message: str, source: str = "") -> None:
        self.warnings.append(ValidationError(message=message, source=source, severity="warning"))


def validate_pack(pack: RulePack) -> ValidationResult:
    """Validate a single rule pack."""
    result = ValidationResult()

    if not pack.id:
        result.add_error("Pack missing required 'id' field")

    if not pack.display_name:
        result.add_error("Pack missing required 'display_name' field", source=pack.id)

    if not pack.rules:
        result.add_warning("Pack has no rules", source=pack.id)

    # Check for empty rule text
    for rule in pack.rules:
        if not rule.text.strip():
            result.add_error(f"Rule '{rule.id}' has empty text", source=pack.id)

    # Check for duplicate rule IDs within the pack
    seen_ids: set[str] = set()
    for rule in pack.rules:
        if rule.id in seen_ids:
            result.add_error(f"Duplicate rule ID '{rule.id}'", source=pack.id)
        seen_ids.add(rule.id)

    return result


def validate_packs(packs: list[RulePack]) -> ValidationResult:
    """Validate a list of packs, including cross-pack checks."""
    result = ValidationResult()

    # Validate each pack individually
    for pack in packs:
        pack_result = validate_pack(pack)
        result.errors.extend(pack_result.errors)
        result.warnings.extend(pack_result.warnings)

    # Cross-pack duplicate ID check
    all_rule_ids: dict[str, str] = {}  # rule_id -> pack_id
    for pack in packs:
        for rule in pack.rules:
            if rule.id in all_rule_ids:
                result.add_warning(
                    f"Rule ID '{rule.id}' appears in both "
                    f"'{all_rule_ids[rule.id]}' and '{pack.id}'",
                    source="cross-pack",
                )
            else:
                all_rule_ids[rule.id] = pack.id

    return result


def validate_bundle(bundle: PolicyBundle) -> ValidationResult:
    """Validate a merged policy bundle."""
    result = ValidationResult()

    all_rules = bundle.all_rules()

    if not all_rules:
        result.add_error("Policy bundle has no rules")

    # Check for security rule presence (must have at least some)
    if not bundle.security_rules:
        result.add_error("Policy bundle has no security rules — this is unsafe")

    # Check for duplicate IDs in the final bundle
    seen_ids: set[str] = set()
    for rule in all_rules:
        if rule.id in seen_ids:
            result.add_warning(f"Duplicate rule ID in bundle: '{rule.id}'")
        seen_ids.add(rule.id)

    # Check minimum governance coverage
    if not bundle.governance_rules:
        result.add_warning("Policy bundle has no governance rules")

    return result

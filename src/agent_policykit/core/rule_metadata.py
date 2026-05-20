"""Helpers for embedding and comparing generated rule metadata."""

from __future__ import annotations

import re


_RULE_IDS_RE = re.compile(
    r"<!--\s*agent-policykit:rule-ids:(?P<category>[a-z_]+)=(?P<ids>[^>]*)\s*-->",
    re.IGNORECASE,
)
_LEGACY_SECURITY_RULE_IDS_RE = re.compile(
    r"<!--\s*agent-policykit:security-rule-ids=(?P<ids>[^>]*)\s*-->",
    re.IGNORECASE,
)

_CATEGORY_LABELS = {
    "governance": "governance",
    "security": "security",
    "compliance": "compliance",
    "architecture": "architecture",
    "review": "review",
    "testing": "testing",
    "operations": "operations",
    "language": "language",
    "framework": "framework",
    "project_type": "project type",
    "output_contract": "output contract",
}


def extract_rule_ids_by_category(content: str) -> dict[str, set[str]]:
    """Extract structured rule IDs from generated markdown comments."""
    extracted: dict[str, set[str]] = {}

    for match in _RULE_IDS_RE.finditer(content):
        category = match.group("category").lower()
        rule_ids = _parse_rule_ids(match.group("ids"))
        if not rule_ids:
            continue
        extracted.setdefault(category, set()).update(rule_ids)

    if "security" not in extracted:
        legacy_match = _LEGACY_SECURITY_RULE_IDS_RE.search(content)
        if legacy_match:
            extracted["security"] = _parse_rule_ids(legacy_match.group("ids"))

    return extracted


def find_removed_rule_ids(existing: str, proposed: str) -> dict[str, set[str]]:
    """Return rule IDs that are present in existing content but missing in proposed content."""
    existing_ids = extract_rule_ids_by_category(existing)
    proposed_ids = extract_rule_ids_by_category(proposed)

    removed: dict[str, set[str]] = {}
    for category, category_ids in existing_ids.items():
        missing_ids = category_ids - proposed_ids.get(category, set())
        if missing_ids:
            removed[category] = missing_ids
    return removed


def summarize_removed_rule_ids(removed_rule_ids: dict[str, set[str]]) -> str:
    """Build a concise, actionable message for removed rule IDs."""
    if not removed_rule_ids:
        return ""

    parts: list[str] = []
    for category in sorted(removed_rule_ids):
        category_ids = sorted(removed_rule_ids[category])
        preview = ", ".join(category_ids[:3])
        if len(category_ids) > 3:
            preview += ", ..."
        label = _CATEGORY_LABELS.get(category, category.replace("_", " "))
        parts.append(f"{label} ({len(category_ids)} removed: {preview})")

    return "Potential generated rule removals detected: " + "; ".join(parts)


def _parse_rule_ids(value: str) -> set[str]:
    return {
        rule_id.strip()
        for rule_id in value.split(",")
        if rule_id.strip()
    }
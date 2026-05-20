"""YAML pack loader with schema validation."""

from __future__ import annotations

from pathlib import Path

import yaml

from agent_guardrails.core.models import Rule, RulePack
from agent_guardrails.types import RuleCategory, Severity

# Directory where built-in packs are stored
PACKS_DIR = Path(__file__).parent.parent / "packs"


def _parse_severity(value: str | None) -> Severity:
    """Parse severity string to enum, defaulting to MEDIUM."""
    if not value:
        return Severity.MEDIUM
    try:
        return Severity(value.lower())
    except ValueError:
        return Severity.MEDIUM


def _parse_category(value: str) -> RuleCategory:
    """Parse category string to enum."""
    return RuleCategory(value.lower())


def _parse_rules(raw_rules: list[dict | str], category: RuleCategory, pack_id: str) -> list[Rule]:
    """Parse raw rule entries into Rule objects.

    Rules can be either:
    - A string (shorthand: auto-generates ID, uses the string as text)
    - A dict with id, text, severity, tags
    """
    rules: list[Rule] = []
    for i, entry in enumerate(raw_rules):
        if isinstance(entry, str):
            rule = Rule(
                id=f"{pack_id}.rule_{i + 1}",
                text=entry,
                category=category,
                severity=Severity.MEDIUM,
                tags=[],
            )
        elif isinstance(entry, dict):
            rule = Rule(
                id=entry.get("id", f"{pack_id}.rule_{i + 1}"),
                text=entry.get("text", ""),
                category=category,
                severity=_parse_severity(entry.get("severity")),
                tags=entry.get("tags", []),
            )
        else:
            continue
        rules.append(rule)
    return rules


def load_pack_file(path: Path) -> RulePack:
    """Load a single YAML pack file and return a RulePack."""
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data or not isinstance(data, dict):
        raise ValueError(f"Pack file is empty or not a valid mapping: {path}")

    pack_id = data.get("id")
    if not pack_id:
        raise ValueError(f"Pack file missing required 'id' field: {path}")

    display_name = data.get("display_name", pack_id)
    category = _parse_category(data.get("category", "governance"))
    priority = data.get("priority", 0)
    applies_when = data.get("applies_when", {})
    extends_language = data.get("extends_language")

    # Collect rules from all rule sections in the pack
    rules: list[Rule] = []
    rule_sections = [
        "rules", "api_rules", "service_rules", "data_rules",
        "method_rules", "error_handling_rules", "logging_rules",
        "concurrency_rules", "testing_rules", "security_checklist",
        "anti_patterns", "controller_conventions", "dependency_injection",
        "model_placement", "error_handling", "auth_patterns",
        "testing_conventions", "validation_approach",
        "architectural_rules", "api_design_rules", "data_layer_rules",
        "operational_rules", "security_rules", "frontend_rules",
        "auth_rules", "data_fetching_rules", "communication_rules",
        "observability_rules", "deployment_rules",
    ]

    for section in rule_sections:
        section_data = data.get(section)
        if section_data and isinstance(section_data, list):
            parsed = _parse_rules(section_data, category, f"{pack_id}.{section}")
            rules.extend(parsed)

    metadata = {k: v for k, v in data.items() if k not in {
        "id", "display_name", "category", "priority", "applies_when",
        "extends_language", "rules",
    } and not k.endswith("_rules") and k not in rule_sections}

    return RulePack(
        id=pack_id,
        display_name=display_name,
        category=category,
        rules=rules,
        priority=priority,
        applies_when=applies_when,
        extends_language=extends_language,
        metadata=metadata,
    )


def load_packs_from_directory(directory: Path) -> list[RulePack]:
    """Load all YAML packs from a directory."""
    packs: list[RulePack] = []
    if not directory.exists():
        return packs

    for yaml_file in sorted(directory.glob("*.yaml")):
        pack = load_pack_file(yaml_file)
        packs.append(pack)

    return packs


def load_governance_packs() -> list[RulePack]:
    """Load all governance packs from the built-in packs directory."""
    return load_packs_from_directory(PACKS_DIR / "governance")


def load_language_pack(language: str) -> RulePack | None:
    """Load a specific language pack by name."""
    path = PACKS_DIR / "languages" / f"{language}.yaml"
    if not path.exists():
        return None
    return load_pack_file(path)


def load_framework_pack(framework: str) -> RulePack | None:
    """Load a specific framework pack by name."""
    path = PACKS_DIR / "frameworks" / f"{framework}.yaml"
    if not path.exists():
        return None
    return load_pack_file(path)


def load_project_type_pack(project_type: str) -> RulePack | None:
    """Load a specific project-type pack by name."""
    path = PACKS_DIR / "project_types" / f"{project_type}.yaml"
    if not path.exists():
        return None
    return load_pack_file(path)

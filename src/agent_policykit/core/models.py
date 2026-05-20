"""Core domain models for agent-policykit."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from agent_policykit.types import (
    AgentTarget,
    MergeStrategy,
    ProjectType,
    RuleCategory,
    Severity,
)


@dataclass
class Rule:
    """A single policy rule."""

    id: str
    text: str
    category: RuleCategory
    severity: Severity = Severity.MEDIUM
    tags: list[str] = field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rule):
            return NotImplemented
        return self.id == other.id


@dataclass
class RulePack:
    """A collection of rules loaded from a YAML pack file."""

    id: str
    display_name: str
    category: RuleCategory
    rules: list[Rule]
    priority: int = 0
    applies_when: dict[str, list[str]] = field(default_factory=dict)
    extends_language: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass
class PolicyBundle:
    """The canonical merged policy model — source of truth for all adapters."""

    governance_rules: list[Rule] = field(default_factory=list)
    security_rules: list[Rule] = field(default_factory=list)
    compliance_rules: list[Rule] = field(default_factory=list)
    architecture_rules: list[Rule] = field(default_factory=list)
    review_rules: list[Rule] = field(default_factory=list)
    testing_rules: list[Rule] = field(default_factory=list)
    operations_rules: list[Rule] = field(default_factory=list)
    language_rules: list[Rule] = field(default_factory=list)
    framework_rules: list[Rule] = field(default_factory=list)
    project_type_rules: list[Rule] = field(default_factory=list)
    output_contract: list[Rule] = field(default_factory=list)
    metadata: dict[str, object] = field(default_factory=dict)

    def all_rules(self) -> list[Rule]:
        """Return all rules across all categories."""
        return (
            self.governance_rules
            + self.security_rules
            + self.compliance_rules
            + self.architecture_rules
            + self.review_rules
            + self.testing_rules
            + self.operations_rules
            + self.language_rules
            + self.framework_rules
            + self.project_type_rules
            + self.output_contract
        )

    def rules_by_category(self, category: RuleCategory) -> list[Rule]:
        """Return rules for a specific category."""
        category_map = {
            RuleCategory.GOVERNANCE: self.governance_rules,
            RuleCategory.SECURITY: self.security_rules,
            RuleCategory.COMPLIANCE: self.compliance_rules,
            RuleCategory.ARCHITECTURE: self.architecture_rules,
            RuleCategory.REVIEW: self.review_rules,
            RuleCategory.TESTING: self.testing_rules,
            RuleCategory.OPERATIONS: self.operations_rules,
            RuleCategory.LANGUAGE: self.language_rules,
            RuleCategory.FRAMEWORK: self.framework_rules,
            RuleCategory.PROJECT_TYPE: self.project_type_rules,
            RuleCategory.OUTPUT_CONTRACT: self.output_contract,
        }
        return category_map.get(category, [])


@dataclass
class InstructionScope:
    """A path-scoped instruction target within a repository."""

    slug: str
    display_name: str
    globs: list[str]
    paths: list[str] = field(default_factory=list)
    exclude_agent: str | None = None
    description: str | None = None


@dataclass
class ProjectContext:
    """Detected project context from repository analysis."""

    root_path: Path
    detected_languages: list[str] = field(default_factory=list)
    detected_frameworks: list[str] = field(default_factory=list)
    project_type: ProjectType | None = None
    source_paths: list[str] = field(default_factory=list)
    test_paths: list[str] = field(default_factory=list)
    subproject_paths: list[str] = field(default_factory=list)
    instruction_scopes: list[InstructionScope] = field(default_factory=list)
    instruction_globs: list[str] = field(default_factory=list)
    config_files: list[str] = field(default_factory=list)
    targets: list[AgentTarget] = field(default_factory=list)
    render_mode: str = "generate"


@dataclass
class AdapterOutput:
    """Output from an adapter's render method."""

    path: str
    content: str
    merge_strategy: MergeStrategy = MergeStrategy.SECTION_MERGE
    size_bytes: int = 0
    line_count: int = 0
    warnings: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.size_bytes = len(self.content.encode("utf-8"))
        self.line_count = self.content.count("\n") + 1

"""Update engine — writes adapter output to disk respecting merge strategies."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from agent_policykit.core.diff_engine import MANAGED_END, MANAGED_START
from agent_policykit.core.models import AdapterOutput
from agent_policykit.core.rule_metadata import (
    extract_rule_ids_by_category,
    find_removed_rule_ids,
    summarize_removed_rule_ids,
)
from agent_policykit.types import MergeStrategy


@dataclass
class WriteResult:
    """Result of writing a single file."""

    path: str
    action: str  # "created", "updated", "skipped", "unchanged"
    message: str = ""


@dataclass
class UpdateResult:
    """Collection of write results for an update operation."""

    results: list[WriteResult] = field(default_factory=list)

    @property
    def created(self) -> list[WriteResult]:
        return [r for r in self.results if r.action == "created"]

    @property
    def updated(self) -> list[WriteResult]:
        return [r for r in self.results if r.action == "updated"]

    @property
    def skipped(self) -> list[WriteResult]:
        return [r for r in self.results if r.action == "skipped"]


def apply_updates(root: Path, outputs: list[AdapterOutput], force: bool = False) -> UpdateResult:
    """Write adapter outputs to disk, respecting merge strategies.

    Args:
        root: Project root directory
        outputs: Adapter output files to write
        force: If True, overwrite even if content hasn't changed or strategy says skip
    """
    results: list[WriteResult] = []

    for output in outputs:
        file_path = root / output.path
        result = _write_single_output(file_path, output, force)
        results.append(result)

    return UpdateResult(results=results)


def _write_single_output(file_path: Path, output: AdapterOutput, force: bool) -> WriteResult:
    """Write a single output file according to its merge strategy."""
    # Ensure parent directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if not file_path.exists():
        file_path.write_text(output.content, encoding="utf-8")
        return WriteResult(path=output.path, action="created")

    existing = file_path.read_text(encoding="utf-8")

    if output.merge_strategy == MergeStrategy.SKIP_IF_EXISTS and not force:
        return WriteResult(path=output.path, action="skipped", message="File exists, skip_if_exists strategy")

    if output.merge_strategy == MergeStrategy.OVERWRITE or force:
        if existing == output.content:
            return WriteResult(path=output.path, action="unchanged")
        if not force and _would_downgrade_security(existing, output.content):
            return WriteResult(
                path=output.path,
                action="skipped",
                message="Security rules would be downgraded; rerun with --force to override",
            )
        file_path.write_text(output.content, encoding="utf-8")
        return WriteResult(
            path=output.path,
            action="updated",
            message=_summarize_non_security_conflicts(existing, output.content),
        )

    if output.merge_strategy == MergeStrategy.SECTION_MERGE:
        merged = _merge_managed_section(existing, output.content)
        if merged == existing:
            return WriteResult(path=output.path, action="unchanged")
        if not force and _would_downgrade_security(existing, merged):
            return WriteResult(
                path=output.path,
                action="skipped",
                message="Security rules would be downgraded; rerun with --force to override",
            )
        file_path.write_text(merged, encoding="utf-8")
        return WriteResult(
            path=output.path,
            action="updated",
            message=_summarize_non_security_conflicts(existing, merged),
        )

    if output.merge_strategy == MergeStrategy.APPEND:
        new_content = existing + "\n" + output.content
        file_path.write_text(new_content, encoding="utf-8")
        return WriteResult(path=output.path, action="updated")

    # Fallback: overwrite
    file_path.write_text(output.content, encoding="utf-8")
    return WriteResult(path=output.path, action="updated")


def _merge_managed_section(existing: str, proposed: str) -> str:
    """Replace only the managed section in existing content, preserving user content."""
    existing_start = existing.find(MANAGED_START)
    existing_end = existing.find(MANAGED_END)
    proposed_start = proposed.find(MANAGED_START)
    proposed_end = proposed.find(MANAGED_END)

    if existing_start == -1 or existing_end == -1:
        # No managed section in existing file — prepend proposed managed section
        if proposed_start != -1 and proposed_end != -1:
            managed = proposed[proposed_start:proposed_end + len(MANAGED_END)]
            return managed + "\n\n" + existing
        return proposed

    if proposed_start == -1 or proposed_end == -1:
        # No managed section in proposed — just overwrite
        return proposed

    # Replace existing managed section with proposed managed section
    new_managed = proposed[proposed_start:proposed_end + len(MANAGED_END)]
    result = existing[:existing_start] + new_managed + existing[existing_end + len(MANAGED_END):]
    return result


_SECURITY_HEADING_RE = re.compile(r"^(#{2,6})\s+.*security.*$", re.IGNORECASE)
_MARKDOWN_HEADING_RE = re.compile(r"^(#{2,6})\s+")


def _would_downgrade_security(existing: str, proposed: str) -> bool:
    """Return True when proposed content removes existing security guidance lines."""
    existing_rule_ids = extract_rule_ids_by_category(existing)
    proposed_rule_ids = extract_rule_ids_by_category(proposed)
    if "security" in existing_rule_ids:
        if "security" not in proposed_rule_ids:
            return True
        return not existing_rule_ids["security"].issubset(proposed_rule_ids["security"])

    existing_lines = _extract_security_lines(existing)
    if not existing_lines:
        return False

    proposed_lines = _extract_security_lines(proposed)
    return not existing_lines.issubset(proposed_lines)


def _summarize_non_security_conflicts(existing: str, proposed: str) -> str:
    removed_rule_ids = find_removed_rule_ids(existing, proposed)
    non_security_removed = {
        category: rule_ids
        for category, rule_ids in removed_rule_ids.items()
        if category != "security"
    }
    return summarize_removed_rule_ids(non_security_removed)


def _extract_security_lines(content: str) -> set[str]:
    """Extract normalized security-section content lines from markdown-like files."""
    lines = content.splitlines()
    collected: list[str] = []
    index = 0

    while index < len(lines):
        match = _SECURITY_HEADING_RE.match(lines[index].strip())
        if not match:
            index += 1
            continue

        current_level = len(match.group(1))
        index += 1
        while index < len(lines):
            stripped = lines[index].strip()
            next_heading = _MARKDOWN_HEADING_RE.match(stripped)
            if next_heading and len(next_heading.group(1)) <= current_level:
                break
            if stripped and not stripped.startswith("<!--"):
                collected.append(stripped)
            index += 1

    normalized = {
        re.sub(r"\s+", " ", line).strip()
        for line in collected
        if line.strip()
    }
    return normalized

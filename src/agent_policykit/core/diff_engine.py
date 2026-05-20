"""Diff engine — compares current files with generated output."""

from __future__ import annotations

import difflib
from dataclasses import dataclass, field
from pathlib import Path

from agent_policykit.core.models import AdapterOutput


@dataclass
class FileDiff:
    """Represents the diff between existing and proposed content."""

    path: str
    exists: bool
    is_new: bool
    has_changes: bool
    unified_diff: str
    added_lines: int = 0
    removed_lines: int = 0

    @property
    def summary(self) -> str:
        if self.is_new:
            return f"NEW: {self.path}"
        if not self.has_changes:
            return f"UNCHANGED: {self.path}"
        return f"MODIFIED: {self.path} (+{self.added_lines}/-{self.removed_lines})"


@dataclass
class DiffResult:
    """Collection of diffs for a generate/update operation."""

    diffs: list[FileDiff] = field(default_factory=list)

    @property
    def has_changes(self) -> bool:
        return any(d.has_changes or d.is_new for d in self.diffs)

    @property
    def new_files(self) -> list[FileDiff]:
        return [d for d in self.diffs if d.is_new]

    @property
    def modified_files(self) -> list[FileDiff]:
        return [d for d in self.diffs if d.has_changes and not d.is_new]

    @property
    def unchanged_files(self) -> list[FileDiff]:
        return [d for d in self.diffs if not d.has_changes and not d.is_new]


def compute_diff(root: Path, outputs: list[AdapterOutput]) -> DiffResult:
    """Compare proposed adapter outputs against existing files on disk.

    Returns a DiffResult with unified diffs for each output file.
    """
    diffs: list[FileDiff] = []

    for output in outputs:
        file_path = root / output.path
        proposed = output.content

        if not file_path.exists():
            # New file
            diff_text = _unified_diff("", proposed, output.path)
            diffs.append(FileDiff(
                path=output.path,
                exists=False,
                is_new=True,
                has_changes=True,
                unified_diff=diff_text,
                added_lines=proposed.count("\n") + 1,
                removed_lines=0,
            ))
        else:
            # Existing file — compare managed sections or full content
            existing = file_path.read_text(encoding="utf-8")
            existing_managed = _extract_managed_section(existing)
            proposed_managed = _extract_managed_section(proposed)

            if existing_managed is not None and proposed_managed is not None:
                # Compare only managed sections
                has_changes = existing_managed != proposed_managed
                diff_text = _unified_diff(existing_managed, proposed_managed, output.path)
            else:
                # Compare full content
                has_changes = existing != proposed
                diff_text = _unified_diff(existing, proposed, output.path)

            added = sum(1 for line in diff_text.splitlines() if line.startswith("+") and not line.startswith("+++"))
            removed = sum(1 for line in diff_text.splitlines() if line.startswith("-") and not line.startswith("---"))

            diffs.append(FileDiff(
                path=output.path,
                exists=True,
                is_new=False,
                has_changes=has_changes,
                unified_diff=diff_text if has_changes else "",
                added_lines=added,
                removed_lines=removed,
            ))

    return DiffResult(diffs=diffs)


def _unified_diff(old: str, new: str, filename: str) -> str:
    """Generate a unified diff string."""
    old_lines = old.splitlines(keepends=True)
    new_lines = new.splitlines(keepends=True)
    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile=f"a/{filename}",
        tofile=f"b/{filename}",
        lineterm="",
    )
    return "".join(diff)


MANAGED_START = "<!-- agent-policykit:managed -->"
MANAGED_END = "<!-- agent-policykit:end -->"


def _extract_managed_section(content: str) -> str | None:
    """Extract content between managed markers, or None if not found."""
    start_idx = content.find(MANAGED_START)
    end_idx = content.find(MANAGED_END)
    if start_idx == -1 or end_idx == -1:
        return None
    return content[start_idx:end_idx + len(MANAGED_END)]

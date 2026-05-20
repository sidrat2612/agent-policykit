"""Helpers for adapter output size warnings and markdown condensation."""

from __future__ import annotations

from dataclasses import dataclass
import re

from agent_policykit.core.models import AdapterOutput


_SECTION_HEADING_RE = re.compile(r"^(##+)")


@dataclass
class _MarkdownSection:
    heading: str
    body: list[str]
    priority: str


def apply_output_limits(
    outputs: list[AdapterOutput],
    *,
    max_bytes: int | None = None,
    max_lines: int | None = None,
    warn_at: float = 0.9,
) -> list[AdapterOutput]:
    """Condense markdown-like outputs when needed and annotate size warnings."""
    for output in outputs:
        if _should_condense(output, max_bytes=max_bytes, max_lines=max_lines, warn_at=warn_at):
            condensed_content = _condense_markdown_output(
                output.content,
                max_bytes=max_bytes,
                max_lines=max_lines,
            )
            if condensed_content != output.content:
                output.content = condensed_content
                output.size_bytes = len(condensed_content.encode("utf-8"))
                output.line_count = condensed_content.count("\n") + 1
                output.warnings.append(
                    f"{output.path} was condensed to stay within configured size guidance."
                )

        if max_bytes is not None:
            _append_limit_warning(
                output,
                current=output.size_bytes,
                limit=max_bytes,
                warn_at=warn_at,
                unit="bytes",
            )
        if max_lines is not None:
            _append_limit_warning(
                output,
                current=output.line_count,
                limit=max_lines,
                warn_at=warn_at,
                unit="lines",
            )
    return outputs


def _append_limit_warning(
    output: AdapterOutput,
    *,
    current: int,
    limit: int,
    warn_at: float,
    unit: str,
) -> None:
    if current > limit:
        output.warnings.append(
            f"{output.path} exceeds the configured limit of {limit} {unit} ({current} {unit})."
        )
        return

    if current >= int(limit * warn_at):
        output.warnings.append(
            f"{output.path} is approaching the configured limit of {limit} {unit} ({current} {unit})."
        )


def _should_condense(
    output: AdapterOutput,
    *,
    max_bytes: int | None,
    max_lines: int | None,
    warn_at: float,
) -> bool:
    if not _is_markdown_like(output.path):
        return False

    if max_bytes is not None and output.size_bytes >= int(max_bytes * warn_at):
        return True
    if max_lines is not None and output.line_count >= int(max_lines * warn_at):
        return True
    return False


def _is_markdown_like(path: str) -> bool:
    return path.endswith((".md", ".mdc", ".instructions.md"))


def _condense_markdown_output(
    content: str,
    *,
    max_bytes: int | None,
    max_lines: int | None,
) -> str:
    frontmatter, body = _split_frontmatter(content)
    prefix_lines, sections = _split_sections(body)

    if not sections:
        return content

    strategies = [
        {"high": 6, "medium": 4, "low": 2},
        {"high": 4, "medium": 2, "low": 1},
        {"high": 3, "medium": 1, "low": 0},
        {"high": 2, "medium": 0, "low": 0},
    ]

    candidate = content
    for limits in strategies:
        candidate = _rebuild_markdown(frontmatter, prefix_lines, sections, limits)
        if _content_within_limits(candidate, max_bytes=max_bytes, max_lines=max_lines):
            return candidate

    return candidate


def _split_frontmatter(content: str) -> tuple[str, str]:
    if not content.startswith("---\n"):
        return "", content

    end_marker = content.find("\n---\n", 4)
    if end_marker == -1:
        return "", content

    end_idx = end_marker + len("\n---\n")
    return content[:end_idx], content[end_idx:]


def _split_sections(body: str) -> tuple[list[str], list[_MarkdownSection]]:
    lines = body.splitlines()
    prefix: list[str] = []
    sections: list[_MarkdownSection] = []
    current_heading: str | None = None
    current_body: list[str] = []

    for line in lines:
        if _SECTION_HEADING_RE.match(line):
            if current_heading is None:
                if prefix:
                    prefix = _trim_blank_edges(prefix)
            else:
                sections.append(
                    _MarkdownSection(
                        heading=current_heading,
                        body=_trim_blank_edges(current_body),
                        priority=_section_priority(current_heading),
                    )
                )
            current_heading = line
            current_body = []
            continue

        if current_heading is None:
            prefix.append(line)
        else:
            current_body.append(line)

    if current_heading is not None:
        sections.append(
            _MarkdownSection(
                heading=current_heading,
                body=_trim_blank_edges(current_body),
                priority=_section_priority(current_heading),
            )
        )

    return _trim_blank_edges(prefix), sections


def _section_priority(heading: str) -> str:
    normalized = heading.lower()
    high_keywords = [
        "review mode",
        "project overview",
        "project context",
        "engineering standards",
        "governance",
        "security",
        "output contract",
    ]
    medium_keywords = [
        "architecture",
        "testing",
        "code review",
        "language",
        "framework",
        "project type",
    ]
    if any(keyword in normalized for keyword in high_keywords):
        return "high"
    if any(keyword in normalized for keyword in medium_keywords):
        return "medium"
    return "low"


def _rebuild_markdown(
    frontmatter: str,
    prefix_lines: list[str],
    sections: list[_MarkdownSection],
    limits: dict[str, int],
) -> str:
    parts: list[str] = []
    if frontmatter:
        parts.append(frontmatter.rstrip("\n"))

    if prefix_lines:
        parts.append("\n".join(prefix_lines))

    for section in sections:
        rendered = _render_section(section, limits)
        if rendered:
            parts.append(rendered)

    rendered_content = "\n\n".join(part for part in parts if part)
    return rendered_content.rstrip() + "\n"


def _render_section(section: _MarkdownSection, limits: dict[str, int]) -> str:
    limit = limits.get(section.priority, 0)
    if limit == 0 and section.priority != "high":
        return ""

    kept_lines: list[str] = [section.heading]
    bullet_count = 0
    omitted = False

    for line in section.body:
        if line.lstrip().startswith("- "):
            if bullet_count < max(limit, 1):
                kept_lines.append(line)
                bullet_count += 1
            else:
                omitted = True
            continue

        kept_lines.append(line)

    if omitted:
        if kept_lines and kept_lines[-1] != "":
            kept_lines.append("")
        kept_lines.append("- Additional items omitted in condensed output.")

    return "\n".join(_trim_blank_edges(kept_lines))


def _content_within_limits(content: str, *, max_bytes: int | None, max_lines: int | None) -> bool:
    size_bytes = len(content.encode("utf-8"))
    line_count = content.count("\n") + 1
    if max_bytes is not None and size_bytes > max_bytes:
        return False
    if max_lines is not None and line_count > max_lines:
        return False
    return True


def _trim_blank_edges(lines: list[str]) -> list[str]:
    trimmed = list(lines)
    while trimmed and trimmed[0] == "":
        trimmed.pop(0)
    while trimmed and trimmed[-1] == "":
        trimmed.pop()
    return trimmed
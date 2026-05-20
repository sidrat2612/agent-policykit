"""Jinja2 template renderer for policy output."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from agent_policykit.core.models import PolicyBundle, ProjectContext

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
REVIEW_FOCUS_AREAS = [
    "Functional correctness",
    "Security findings",
    "Privacy and compliance findings",
    "Architecture quality",
    "Maintainability issues",
    "Reliability and performance risks",
    "Testing gaps",
    "Production readiness gaps",
    "Rollback and observability concerns",
]
REVIEW_REQUIRED_SECTIONS = [
    "Review summary",
    "Functional correctness issues",
    "Security findings",
    "Privacy and compliance findings",
    "Architecture and maintainability findings",
    "Reliability and performance findings",
    "Testing gaps",
    "Production readiness gaps",
    "Recommended fixes",
]
REVIEW_TONE = (
    "Be blunt, skeptical, and technically demanding, but remain professional, actionable, "
    "and free of personal attacks."
)


def _create_env() -> Environment:
    """Create a Jinja2 environment with template directory."""
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(default=False),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )


def render_template(
    template_name: str,
    bundle: PolicyBundle,
    context: ProjectContext,
    **extra_context: Any,
) -> str:
    """Render a template with the given bundle and context."""
    env = _create_env()
    template = env.get_template(template_name)
    return template.render(
        bundle=bundle,
        context=context,
        review_mode=context.render_mode == "review",
        review_focus_areas=REVIEW_FOCUS_AREAS,
        review_required_sections=REVIEW_REQUIRED_SECTIONS,
        review_tone=REVIEW_TONE,
        rules=bundle.all_rules(),
        governance_rules=bundle.governance_rules,
        security_rules=bundle.security_rules,
        compliance_rules=bundle.compliance_rules,
        architecture_rules=bundle.architecture_rules,
        review_rules=bundle.review_rules,
        testing_rules=bundle.testing_rules,
        operations_rules=bundle.operations_rules,
        language_rules=bundle.language_rules,
        framework_rules=bundle.framework_rules,
        project_type_rules=bundle.project_type_rules,
        output_contract=bundle.output_contract,
        **extra_context,
    )

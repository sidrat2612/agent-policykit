"""Policy engine — orchestrates pack selection, loading, and merging based on project context."""

from __future__ import annotations

from agent_policykit.core.loader import (
    load_framework_pack,
    load_governance_packs,
    load_language_pack,
    load_project_type_pack,
)
from agent_policykit.core.merger import merge_packs
from agent_policykit.core.models import PolicyBundle, ProjectContext, RulePack


def build_policy_bundle(context: ProjectContext) -> PolicyBundle:
    """Build a full PolicyBundle based on the detected project context.

    Loading order (and precedence by priority):
    1. Governance packs (priority 100-200) — always included
    2. Language packs (priority 50) — one per detected language
    3. Framework packs (priority 60) — one per detected framework
    4. Project-type pack (priority 40) — at most one
    """
    packs: list[RulePack] = []

    # Always include governance packs
    packs.extend(load_governance_packs())

    # Load language packs for detected languages
    for language in context.detected_languages:
        pack = load_language_pack(language)
        if pack:
            packs.append(pack)

    # Load framework packs for detected frameworks
    for framework in context.detected_frameworks:
        pack = load_framework_pack(framework)
        if pack:
            packs.append(pack)

    # Load project-type pack if detected
    if context.project_type:
        pack = load_project_type_pack(context.project_type.value)
        if pack:
            packs.append(pack)

    bundle = merge_packs(packs)
    bundle.metadata["context"] = {
        "languages": context.detected_languages,
        "frameworks": context.detected_frameworks,
        "project_type": context.project_type.value if context.project_type else None,
        "pack_count": len(packs),
        "total_rules": len(bundle.all_rules()),
    }
    return bundle


def list_available_packs() -> dict[str, list[str]]:
    """List all available pack names by category."""
    from agent_policykit.core.loader import PACKS_DIR

    result: dict[str, list[str]] = {}
    for category_dir in ["governance", "languages", "frameworks", "project_types"]:
        dir_path = PACKS_DIR / category_dir
        if dir_path.exists():
            result[category_dir] = [
                f.stem for f in sorted(dir_path.glob("*.yaml"))
            ]
        else:
            result[category_dir] = []
    return result

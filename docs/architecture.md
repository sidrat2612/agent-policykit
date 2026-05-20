# Architecture

This document is for maintainers and contributors who need to understand how `agent-policykit` turns one engineering policy into the exact instruction files different coding agents expect.

The system is organized around a canonical policy model and a thin adapter layer so teams can define guidance once, then generate consistent agent-specific outputs without maintaining separate prompts by hand.

## Core flow

1. Repository analysis detects languages, frameworks, project type, existing targets, and path-scoped instruction globs.
2. Pack loading reads governance, language, framework, and project-type YAML packs from `src/agent_policykit/packs/`.
3. Validation checks pack integrity and merged bundle coverage.
4. Merging combines packs by priority into a single `PolicyBundle`.
5. Adapters render the bundle into agent-specific files.
6. Diff and update logic applies managed updates safely, blocks security downgrades unless `--force` is used, and surfaces non-security generated rule removals as structured conflict notes.

## Main modules

- `src/agent_policykit/core/models.py`: canonical dataclasses and bundle model.
- `src/agent_policykit/core/loader.py`: YAML pack loading.
- `src/agent_policykit/core/validator.py`: pack and bundle validation.
- `src/agent_policykit/core/merger.py`: bundle construction and severity filtering.
- `src/agent_policykit/core/renderer.py`: Jinja2 rendering.
- `src/agent_policykit/core/rule_metadata.py`: structured generated-rule metadata and conflict summaries.
- `src/agent_policykit/core/diff_engine.py`: diff computation.
- `src/agent_policykit/core/update_engine.py`: managed updates, downgrade protection, and rule-removal surfacing.
- `src/agent_policykit/core/output_limits.py`: size-aware markdown condensation.
- `src/agent_policykit/analysis/`: repository detection, framework/language detection, path selection.
- `src/agent_policykit/adapters/`: target-specific output adapters.

## Production guardrails

- Managed sections use `<!-- agent-policykit:managed -->` markers where merging is supported.
- Identical duplicate adapter outputs are deduplicated in the CLI.
- Conflicting duplicate outputs fail fast in the CLI.
- Existing security guidance is not silently removed during updates unless `--force` is provided.
- Generated rule IDs are embedded into markdown-capable outputs so diff/update can detect removals by category.
- Claude repository-wide guidance is split into `CLAUDE.md` plus `.claude/rules/shared.md`, and path-scoped Claude rules remain separate imports.
- Tier 2 targets export dedicated compatibility files such as `AGENT_POLICY.roocode.md` rather than collapsing every alias to one shared file path.

## Current capabilities

- Path-scoped instruction generation emits one file per detected source or test scope.
- Nested `AGENTS.md` precedence is implemented through per-subproject file generation.
- Full language, framework, and project-type pack coverage is implemented.
- Size-sensitive outputs are condensed automatically, and Claude has a dedicated shared-rule split path when repository-wide guidance needs multiple files.

## Operational notes

- `generate` writes the requested targets and reports any generated rule removals that are not blocked by the security downgrade guardrail.
- `update` refreshes only files that already exist unless `--force` is used.
- `diff` previews the exact managed-content delta and now annotates files with structured rule-removal notes when applicable.
- Worked example repositories under `examples/` are validated in the test suite so the documented flows stay in sync with the implementation.

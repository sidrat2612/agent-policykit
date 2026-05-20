# Architecture

`agent-policykit` is organized around a canonical policy model and a thin adapter layer.

## Core flow

1. Repository analysis detects languages, frameworks, project type, existing targets, and path-scoped instruction globs.
2. Pack loading reads governance, language, framework, and project-type YAML packs from `src/agent_policykit/packs/`.
3. Validation checks pack integrity and merged bundle coverage.
4. Merging combines packs by priority into a single `PolicyBundle`.
5. Adapters render the bundle into agent-specific files.
6. Diff and update logic applies managed updates safely and blocks security downgrades unless `--force` is used.

## Main modules

- `src/agent_policykit/core/models.py`: canonical dataclasses and bundle model.
- `src/agent_policykit/core/loader.py`: YAML pack loading.
- `src/agent_policykit/core/validator.py`: pack and bundle validation.
- `src/agent_policykit/core/merger.py`: bundle construction and severity filtering.
- `src/agent_policykit/core/renderer.py`: Jinja2 rendering.
- `src/agent_policykit/core/diff_engine.py`: diff computation.
- `src/agent_policykit/core/update_engine.py`: managed updates and downgrade protection.
- `src/agent_policykit/analysis/`: repository detection, framework/language detection, path selection.
- `src/agent_policykit/adapters/`: target-specific output adapters.

## Production guardrails

- Managed sections use `<!-- agent-policykit:managed -->` markers where merging is supported.
- Identical duplicate adapter outputs are deduplicated in the CLI.
- Conflicting duplicate outputs fail fast in the CLI.
- Existing security guidance is not silently removed during updates unless `--force` is provided.

## Current limitations

- Path-specific instruction generation currently emits one default project-scoped file rather than multiple path slices.
- Nested `AGENTS.md` precedence is not yet implemented.
- Full language, framework, and project-type pack coverage is not complete.

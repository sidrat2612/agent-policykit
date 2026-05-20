# Contributing to agent-policykit

Thank you for helping improve agent-policykit. This project follows the public-maintainer guidance in https://opensource.guide/: keep the process documented, keep discussion public, and make changes easy to review.

## Project scope

- agent-policykit is a local, deterministic instruction compiler for coding agents.
- Pack loading, policy merging, and rendering should stay reproducible and explainable.
- The project does not add hosted LLM dependencies.
- Large feature ideas should start as an issue before a pull request.

## Good contributions

- Reproducible bug reports with sample projects or fixtures
- Targeted bug fixes with tests
- New language, framework, or project-type packs
- New adapter implementations for unsupported agents
- Performance improvements with before/after evidence
- Docs, examples, and onboarding improvements

## Before you open an issue or PR

- Search existing issues and pull requests first.
- For support or usage questions, follow [SUPPORT.md](SUPPORT.md).
- For security issues, follow [SECURITY.md](SECURITY.md).
- For community behavior problems, follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Run checks

For most changes, run the narrowest relevant tests first and then the full suite if your change has broad impact.

```bash
pytest --cov=agent_policykit --cov-fail-under=80
ruff check src/ tests/
ruff format --check src/ tests/
mypy src/agent_policykit --ignore-missing-imports
python -m build
```

If you add or change pack behavior, include or update fixtures in `tests/`.

## Adding a new pack

1. Create a YAML file in the appropriate `src/agent_policykit/packs/` subdirectory.
2. Follow the existing schema (see any existing pack for reference).
3. Each rule needs a non-empty `text` field and a unique ID within the pack.
4. Run `agent-policykit validate` to verify structural correctness.
5. Add a test in `tests/test_loader.py` if introducing a new pack category.

## Adding a new adapter

1. Create a module in `src/agent_policykit/adapters/`.
2. Use the `@register_adapter(AgentTarget.YOUR_TARGET)` decorator.
3. Implement `render()`, `output_paths()`, and `supports_target()`.
4. Add the import to `src/agent_policykit/commands/common.py` in `load_all_adapters()`.
5. Add a test in `tests/test_adapters.py`.

## Pull request rules

- Keep changes focused. Avoid drive-by refactors.
- Explain the user-visible problem and why this fix is the right scope.
- Add or update tests for behavior changes.
- Update docs when commands, flags, outputs, or supported agents change.
- Add a short note to `CHANGELOG.md` for user-visible changes.
- Open an issue before starting large features or behavior changes.

## Code style

- Python 3.11+ features are fine (type unions with `|`, `Self`, etc.).
- Follow existing conventions — `ruff` enforces the project style.
- Keep modules small and single-purpose.

## Review expectations

- Maintainer time is limited and review is best effort.
- A maintainer will try to acknowledge new issues and PRs within 7 days.
- If a thread is blocked and there has been no response after 7 days, post a short follow-up in the same thread instead of opening a duplicate.

## Communication

- Use public GitHub issues and pull requests for bugs, proposals, and design discussion.
- Keep private contact for security reports or sensitive code of conduct matters only.
- Look for `good first issue` and `help wanted` labels when they are available.

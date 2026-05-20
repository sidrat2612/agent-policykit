# Contributing to agent-policykit

Thank you for your interest in contributing.

## Development setup

```bash
git clone https://github.com/sidrat2612/agent-policykit.git
cd agent-policykit
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"
```

## Running checks locally

```bash
# Tests with coverage
pytest --cov=agent_policykit --cov-fail-under=80

# Linting
ruff check src/ tests/
ruff format --check src/ tests/

# Type checking
mypy src/agent_policykit --ignore-missing-imports
```

## Pull request process

1. Fork the repository and create a feature branch from `main`.
2. Write tests for new behavior — coverage must stay above 80%.
3. Ensure `pytest`, `ruff check`, and `mypy` all pass.
4. Keep commits focused and messages descriptive.
5. Open a PR against `main` with a clear description of what and why.

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

## Code style

- Python 3.11+ features are fine (type unions with `|`, `Self`, etc.).
- Follow existing conventions — `ruff` enforces the project style.
- Keep modules small and single-purpose.

## Reporting bugs

Open a GitHub issue with:
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS

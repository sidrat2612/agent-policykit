# agent-policykit

Universal instruction compiler for coding agents.

`agent-policykit` turns one canonical governance model into agent-specific instruction files for repository-wide guidance, path-scoped guidance, portable `AGENTS.md`, and additional agent-target exports.

## Installation

```bash
pip install agent-policykit
```

## Usage

```bash
agent-policykit --help
agent-policykit init
agent-policykit detect
agent-policykit generate --target copilot --target agents-md
agent-policykit generate --target generic-markdown --mode review --dry-run
agent-policykit update --dry-run
agent-policykit diff
agent-policykit validate
```

## Workflow

1. Run `agent-policykit init` to scaffold `[tool.agent-policykit]` into `pyproject.toml`.
2. Run `agent-policykit detect` to inspect the repository stack and existing agent targets.
3. Run `agent-policykit generate` to render instruction files for the targets you want.
4. Run `agent-policykit diff` or `agent-policykit update --dry-run` to preview changes.
5. Run `agent-policykit update` to safely refresh existing generated files.

## Generated outputs

- GitHub Copilot repo-wide: `.github/copilot-instructions.md`
- GitHub Copilot path-scoped: `.github/instructions/*.instructions.md`
- Portable agent guidance: `AGENTS.md` plus nested `AGENTS.md` files for subprojects
- Cursor: `.cursor/rules/project.mdc`
- Claude Code: `CLAUDE.md` plus `.claude/rules/shared.md` and any detected scoped rule files
- Aider: `CONVENTIONS.md` and `.aider.conf.yml`
- Codex: `AGENTS.md`
- Gemini CLI: `GEMINI.md`
- Generic markdown fallback: `AGENT_POLICY.md`
- Tier 2 exported compatibility files: `AGENT_POLICY.<target>.md` for RooCode, Windsurf, Zed, Warp, Junie, Devin, Amp, Augment Code, Factory, Jules, goose, opencode, Phoenix, Semgrep, and Ona

## Safety behavior

- Managed sections use `<!-- agent-policykit:managed -->` markers where merge semantics are supported.
- Security rule removals are blocked on update unless `--force` is used.
- Non-security generated rule removals are surfaced in `diff`, `update`, and `generate` output as structured conflict notes.
- Size-sensitive markdown outputs are condensed automatically, and Claude repository-wide guidance is split into `.claude/rules/shared.md` so `CLAUDE.md` stays compact.

## Documentation

- See `docs/architecture.md` for the current system architecture and update model.
- See `docs/supported-agents.md` for output contracts by target.
- See `docs/language-packs.md`, `docs/framework-packs.md`, and `docs/project-types.md` for pack coverage.
- See `examples/fastapi-service/`, `examples/nextjs-app/`, and `examples/rails-monolith/` for validated worked fixtures.

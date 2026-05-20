<div align="center">
  <h1>agent-policykit</h1>
  <p>
    <strong>One engineering policy in. Agent-specific instruction files out.</strong>
  </p>
  <p>
    For teams using multiple AI coding agents in the same repository.
  </p>
  <p>
    <a href="https://github.com/sidrat2612/agent-policykit/actions/workflows/ci.yml"><img src="https://github.com/sidrat2612/agent-policykit/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
    <a href="https://github.com/sidrat2612/agent-policykit/blob/main/LICENSE"><img src="https://img.shields.io/github/license/sidrat2612/agent-policykit" alt="License"></a>
    <a href="https://github.com/sidrat2612/agent-policykit/stargazers"><img src="https://img.shields.io/github/stars/sidrat2612/agent-policykit?style=social" alt="Stars"></a>
  </p>
</div>

---

`agent-policykit` detects the stack in a repository, merges governance with language, framework, and project-type rules, and writes the exact instruction files each coding agent expects.

> If your repo has Copilot, Cursor, Claude Code, Codex, Aider, or Gemini users, `agent-policykit` keeps them aligned on the same security, architecture, testing, and review guidance without hand-editing separate prompt files.

## Why?

Most teams that adopt AI coding assistants hit the same problem quickly: every tool wants a different file, a different format, and a different maintenance path.

`agent-policykit` solves that with a compiler-style workflow:

| Situation | Without agent-policykit | With agent-policykit |
|-----------|-------------------------|----------------------|
| Multiple agents in one repo | Prompt files drift and contradict each other | One shared policy generates all outputs |
| Stack-specific guidance | Generic prompts ignore framework and project type | Packs inject Python, FastAPI, monolith, SDK, and other stack context |
| Standards change | Manual edits across many files | `diff` and `update` regenerate safely |
| Security guidance changes | Accidental weakening or deletion is easy | Security downgrade blocking prevents silent removal |

## Who it is for

- Engineering teams standardizing AI coding assistants across multiple repositories
- Platform and enablement teams managing secure defaults and review expectations
- Consultancies supporting different clients, stacks, and agent tools
- Open-source maintainers who want contributors using different agents to follow the same repo rules

## Quickstart

Install from PyPI:

```bash
pip install agent-policykit
```

Or install the latest version directly from GitHub:

```bash
pip install "git+https://github.com/sidrat2612/agent-policykit.git"
```

### CLI

Common CLI commands:

- `agent-policykit init` detects the stack and writes `[tool.agent-policykit]` into `pyproject.toml`.
- `agent-policykit generate` compiles the merged policy bundle and writes all configured agent files.
- `agent-policykit diff` previews pending changes before regeneration.
- `agent-policykit update` refreshes existing generated files while preserving user-owned sections.
- `agent-policykit validate` checks bundled packs for structural correctness.

Minimal flow:

```bash
agent-policykit init
agent-policykit generate
agent-policykit diff
agent-policykit update
```

### Config File

Generated and manual workflows both use the same project config:

```toml
[tool.agent-policykit]
targets = ["copilot", "agents-md", "cursor", "claude-code"]
languages = ["python", "typescript"]
frameworks = ["fastapi", "nextjs"]
project_type = "api_service"
review_mode = false
```

Recommended config shape:

- Set `targets` to the agent files your repository actually needs.
- Set `languages`, `frameworks`, and `project_type` explicitly when auto-detection is not enough.
- Use `review_mode = true` or `--mode review` when you want stricter reviewer behavior in generated instructions.

## What Gets Written

`agent-policykit` writes plain-text instruction files directly into the repository so they can be reviewed, diffed, and committed like any other source-controlled artifact.

Typical outputs include:

| Target | Output |
|--------|--------|
| GitHub Copilot | `.github/copilot-instructions.md` |
| GitHub Copilot path-scoped | `.github/instructions/*.instructions.md` |
| Portable AGENTS | `AGENTS.md` |
| Claude Code | `CLAUDE.md` plus `.claude/rules/shared.md` |
| Cursor | `.cursor/rules/project.mdc` |
| Aider | `CONVENTIONS.md` and `.aider.conf.yml` |
| Gemini CLI | `GEMINI.md` |
| Compatibility exports | `AGENT_POLICY.<target>.md` |

This is the core behavior: inspect repo context, compile one policy bundle, then write the file shape each agent actually consumes.

## How It Works

`agent-policykit` is a policy compiler and safe updater. It does not replace your coding agent. It makes the instructions those agents read consistent and maintainable.

Execution flow:

1. Detect languages, frameworks, project type, existing targets, and path-scoped instruction surfaces.
2. Load governance, language, framework, and project-type YAML packs.
3. Merge them into one `PolicyBundle` using priority rules.
4. Validate IDs, coverage, and structural integrity.
5. Render target-native files through the adapter registry.
6. Diff or update existing files using managed sections and downgrade protection.

### What it does

- Detects repository context instead of forcing one generic prompt onto every project
- Compiles YAML rule packs into one merged policy bundle
- Renders native instruction files for Copilot, Claude Code, Cursor, Codex, Aider, Gemini CLI, and compatibility targets
- Generates path-scoped outputs for tools that support scoped instructions
- Preserves user-owned content outside managed sections during updates
- Blocks accidental security-rule removal unless `--force` is used
- Condenses outputs automatically when target limits require it

### What it does NOT do

- Does not call external LLM APIs
- Does not execute code from packs
- Does not replace the execution engine of Copilot, Claude Code, Cursor, Codex, or other agents
- Does not silently overwrite everything in existing instruction files
- Does not pretend every repo needs the same policy

### How the workflow behaves in practice

1. `agent-policykit init` detects the repository and writes project config into `pyproject.toml`.
2. `agent-policykit generate` compiles the merged policy bundle and writes the configured agent files.
3. `agent-policykit diff` shows exactly what would change on regeneration.
4. `agent-policykit update` refreshes managed sections while preserving user-owned content.

That means the tool behaves less like a prompt template and more like a code generator with safety checks.

## Supported Agents

### Tier 1 targets

| Agent | Output file(s) |
|-------|----------------|
| GitHub Copilot (repo-wide) | `.github/copilot-instructions.md` |
| GitHub Copilot (path-scoped) | `.github/instructions/*.instructions.md` |
| AGENTS.md (portable) | `AGENTS.md` plus nested per-subproject files |
| Cursor | `.cursor/rules/project.mdc` |
| Claude Code | `CLAUDE.md` plus `.claude/rules/shared.md` and scoped rule imports |
| Aider | `CONVENTIONS.md` and `.aider.conf.yml` |
| OpenAI Codex | `AGENTS.md` (size-aware, up to 32 KiB) |
| Gemini CLI | `GEMINI.md` |

### Tier 2 exported compatibility files

- Generic markdown fallback: `AGENT_POLICY.md`
- RooCode: `AGENT_POLICY.roocode.md`
- Windsurf: `AGENT_POLICY.windsurf.md`
- Zed: `AGENT_POLICY.zed.md`
- Warp: `AGENT_POLICY.warp.md`
- Junie: `AGENT_POLICY.junie.md`
- Devin: `AGENT_POLICY.devin.md`
- Amp: `AGENT_POLICY.amp.md`
- Augment Code: `AGENT_POLICY.augment-code.md`
- Factory: `AGENT_POLICY.factory.md`
- Jules: `AGENT_POLICY.jules.md`
- goose: `AGENT_POLICY.goose.md`
- opencode: `AGENT_POLICY.opencode.md`
- Phoenix: `AGENT_POLICY.phoenix.md`
- Semgrep: `AGENT_POLICY.semgrep.md`
- Ona: `AGENT_POLICY.ona.md`

## Safety Guarantees

- **Security downgrade blocking**: removing generated security rules requires `--force`.
- **Managed-section ownership**: user-written content outside managed blocks is preserved.
- **Structured conflict notes**: non-security rule removals are surfaced instead of disappearing silently.
- **Size-aware rendering**: outputs are condensed when targets have practical size limits.
- **Dry-run support**: `diff` is non-destructive, and `generate` and `update` support `--dry-run`.

## Pack Coverage

| Category | Count | Examples |
|----------|-------|----------|
| Governance | 8 packs | architecture, base, compliance, operations, output contract, review, security, testing |
| Languages | 28 packs | Python, TypeScript, Java, Go, C#, Rust, Ruby, PHP, Kotlin, Swift, and more |
| Frameworks | 13 packs | FastAPI, Django, Flask, Express, NestJS, Next.js, Spring Boot, Rails, and more |
| Project types | 9 packs | API service, web app, microservice, worker, CLI tool, SDK, monolith, and more |

## CLI Reference

| Command | Description |
|---------|-------------|
| `init` | Interactive setup that detects stack and writes config |
| `detect` | Print detected languages, frameworks, project type, and existing targets |
| `generate` | Full pipeline: detect, load, merge, render, and write |
| `update` | Regenerate and merge safely against existing files |
| `diff` | Show the unified diff of pending changes |
| `validate` | Validate all loaded packs for structural correctness |

### Flags

- `--target <name>` limits output to specific adapter targets and is repeatable.
- `--mode review` activates the stricter reviewer overlay.
- `--dry-run` shows changes without writing files.
- `--force` overrides security-downgrade blocking.
- `--verbose` or `-v` enables detailed detection output.

## Review Mode

Generate reviewer-oriented instructions with:

```bash
agent-policykit generate --mode review
```

This tells downstream agents to act like strict reviewers: skeptical, technically demanding, and explicit about missing safeguards.

## Documentation

- [Architecture](docs/architecture.md) for system design, merge flow, and production guardrails
- [Supported agents](docs/supported-agents.md) for output contracts per target
- [Language packs](docs/language-packs.md) for stack coverage details
- [Framework packs](docs/framework-packs.md) for framework-specific rule coverage
- [Project types](docs/project-types.md) for architecture-specific pack behavior

## Examples

The repository ships real example fixtures that are used in tests. These are the best way to see how the workflow actually behaves.

### FastAPI service

Fixture: [`examples/fastapi-service/`](examples/fastapi-service/)

What it represents:

- Python
- FastAPI
- API service

Suggested command:

```bash
cd examples/fastapi-service
agent-policykit detect
agent-policykit generate \
  --target copilot \
  --target copilot-path \
  --target agents-md \
  --target generic-markdown \
  --target claude-code \
  --target cursor \
  --target aider \
  --target gemini-cli \
  --dry-run
```

Validated outputs:

- `.github/copilot-instructions.md`
- `.github/instructions/project.instructions.md`
- `AGENTS.md`
- `AGENT_POLICY.md`
- `CLAUDE.md`
- `.cursor/rules/project.mdc`
- `CONVENTIONS.md`
- `.aider.conf.yml`
- `GEMINI.md`

### Next.js app

Fixture: [`examples/nextjs-app/`](examples/nextjs-app/)

What it represents:

- TypeScript
- Next.js
- Web app

Suggested command:

```bash
cd examples/nextjs-app
agent-policykit detect
agent-policykit generate \
  --target copilot \
  --target copilot-path \
  --target agents-md \
  --target generic-markdown \
  --target cursor \
  --target claude-code \
  --target gemini-cli \
  --dry-run
```

Validated outputs:

- `.github/copilot-instructions.md`
- `.github/instructions/project.instructions.md`
- `AGENTS.md`
- `AGENT_POLICY.md`
- `.cursor/rules/project.mdc`
- `CLAUDE.md`
- `GEMINI.md`

### Rails monolith

Fixture: [`examples/rails-monolith/`](examples/rails-monolith/)

What it represents:

- Ruby
- Rails
- Monolith

Suggested command:

```bash
cd examples/rails-monolith
agent-policykit detect
agent-policykit generate \
  --target copilot \
  --target copilot-path \
  --target agents-md \
  --target generic-markdown \
  --target claude-code \
  --target cursor \
  --dry-run
```

Validated outputs:

- `.github/copilot-instructions.md`
- `.github/instructions/app.instructions.md`
- `AGENTS.md`
- `AGENT_POLICY.md`
- `CLAUDE.md`
- `.cursor/rules/project.mdc`

### What these examples show

- Detection changes based on repo context instead of using one fixed prompt.
- Output targets can differ by stack and by target selection.
- Path-scoped instruction files are generated when the repo structure supports them.
- The same policy model produces different file formats without duplicating the source policy.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Development setup:

1. Clone the repository from `https://github.com/sidrat2612/agent-policykit.git`.
2. Change into the `agent-policykit` directory.
3. Create and activate a virtual environment with `python -m venv .venv` and `source .venv/bin/activate`.
4. Install dev dependencies with `pip install -e ".[dev]"`.
5. Run checks with `pytest`, `ruff check src/ tests/`, and `mypy src/agent_policykit --ignore-missing-imports`.

## Community

- Read [CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), [SUPPORT.md](SUPPORT.md), and [SECURITY.md](SECURITY.md).
- Use public GitHub issues and pull requests for bugs, proposals, and design discussion.
- Keep private reporting for security and conduct matters only.
- These community docs follow guidance from [Open Source Guides](https://opensource.guide/).

## License

[MIT](LICENSE) — use it anywhere.

---

<p align="center">
  <sub>Built for teams that want one policy across many coding agents.</sub>
</p>

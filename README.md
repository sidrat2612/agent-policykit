# agent-policykit

**Universal instruction compiler for coding agents.**

Define engineering governance once. Generate compliant instruction files for every coding agent in your repository — Copilot, Claude Code, Cursor, Codex, Aider, Gemini CLI, and 15+ more.

---

## Why

Teams running multiple AI coding agents end up maintaining separate prompt/rule files for each one. When security or architecture standards change, every file must be updated manually. `agent-policykit` fixes this:

1. You define policy once — through declarative YAML packs (governance, language, framework, project-type).
2. The tool detects your stack and generates target-specific instruction files.
3. Updates are safe — security rules are never silently weakened, user-owned sections are preserved, and diffs are shown before writes.

---

## Quick start

```bash
pip install agent-policykit

# In your project root:
agent-policykit init          # interactive setup → writes [tool.agent-policykit] to pyproject.toml
agent-policykit generate      # generate all configured instruction files
agent-policykit diff          # preview what would change on next regeneration
agent-policykit update        # safely refresh existing files
agent-policykit validate      # validate all loaded packs for correctness
```

---

## Supported agents

### Tier 1 — first-class adapters

| Agent | Output file(s) |
|-------|---------------|
| GitHub Copilot (repo-wide) | `.github/copilot-instructions.md` |
| GitHub Copilot (path-scoped) | `.github/instructions/*.instructions.md` |
| AGENTS.md (portable) | `AGENTS.md` + nested per-subproject |
| Cursor | `.cursor/rules/project.mdc` |
| Claude Code | `CLAUDE.md` + `.claude/rules/shared.md` + scoped rules |
| Aider | `CONVENTIONS.md` + `.aider.conf.yml` |
| OpenAI Codex | `AGENTS.md` (size-aware, ≤32 KiB) |
| Gemini CLI | `GEMINI.md` |

### Tier 2 — exported compatibility files

RooCode, Windsurf, Zed, Warp, Junie, Devin, Amp, Augment Code, Factory, Jules, goose, opencode, Phoenix, Semgrep, Ona — each gets a dedicated `AGENT_POLICY.<target>.md`.

---

## How it works

```
detect repo → load packs → merge → validate → render → diff/update
```

1. **Detect** — scans file extensions, config files, and framework markers to build a `ProjectContext`.
2. **Load** — pulls governance + language + framework + project-type packs from bundled YAML.
3. **Merge** — priority-based dedup; higher-specificity packs win on overlap.
4. **Validate** — no duplicate IDs, no empty rules, security coverage enforced.
5. **Render** — Jinja2 templates produce target-specific output via the adapter registry.
6. **Diff/Update** — managed-section merge with security-downgrade blocking and conflict surfacing.

---

## Safety guarantees

- **Security downgrade blocking** — removing security rules requires `--force`.
- **Managed-section ownership** — `<!-- agent-policykit:managed -->` markers preserve user-written content outside tool-managed sections.
- **Structured conflict notes** — non-security rule removals are surfaced as warnings, not silent.
- **Size-aware rendering** — outputs are auto-condensed when approaching adapter limits (Codex 32 KiB, Claude 200 lines, Cursor 500 lines).
- **Dry-run first** — `--dry-run` on `generate` and `update`; `diff` always non-destructive.

---

## Configuration

Add to your `pyproject.toml`:

```toml
[tool.agent-policykit]
targets = ["copilot", "agents-md", "cursor", "claude-code"]
languages = ["python", "typescript"]
frameworks = ["fastapi", "nextjs"]
project_type = "api_service"
review_mode = false
```

Or run `agent-policykit init` to auto-detect and scaffold this.

---

## Pack coverage

| Category | Count | Examples |
|----------|-------|---------|
| Governance | 7 packs | security, compliance, review, architecture, testing, operations, base |
| Languages | 28 packs | Python, TypeScript, Java, Go, C#, Rust, Ruby, PHP, Kotlin, Swift, … |
| Frameworks | 13 packs | FastAPI, Django, Flask, Express, NestJS, Next.js, Spring Boot, Rails, … |
| Project types | 9 packs | API service, web app, microservice, worker, CLI tool, SDK, … |

---

## CLI reference

| Command | Description |
|---------|-------------|
| `init` | Interactive setup — detects stack, writes config |
| `detect` | Print detected languages, frameworks, project type, existing targets |
| `generate` | Full pipeline: detect → load → merge → render → write |
| `update` | Regenerate and merge safely against existing files |
| `diff` | Show unified diff of pending changes (non-destructive) |
| `validate` | Validate all loaded packs for structural correctness |

### Flags

- `--target <name>` — limit to specific adapter(s); repeatable
- `--mode review` — activate the reviewer-persona overlay
- `--dry-run` — show output without writing files
- `--force` — override security-downgrade blocking
- `--verbose` / `-v` — detailed detection output

---

## Review mode

```bash
agent-policykit generate --mode review
```

Activates a strict reviewer persona across all generated instructions. Agents are told to be skeptical, technically demanding, and aggressive about identifying missing safeguards — while remaining professional and actionable.

---

## Development

```bash
git clone https://github.com/rathoreSiddharth/agent-policykit.git
cd agent-policykit
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check src/ tests/
```

---

## Documentation

- [Architecture](docs/architecture.md) — system design, core flow, production guardrails
- [Supported agents](docs/supported-agents.md) — output contracts per target
- [Language packs](docs/language-packs.md) — 28-language coverage details
- [Framework packs](docs/framework-packs.md) — 13 framework packs
- [Project types](docs/project-types.md) — 9 project-type packs

---

## Examples

Working fixtures with validated detect/generate output:

- [`examples/fastapi-service/`](examples/fastapi-service/) — Python + FastAPI + API service
- [`examples/nextjs-app/`](examples/nextjs-app/) — TypeScript + Next.js + web app
- [`examples/rails-monolith/`](examples/rails-monolith/) — Ruby + Rails + monolith

---

## License

MIT

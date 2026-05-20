## Project identity

**Project name:** `agent-guardrails` [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
**Python package:** `agent_guardrails` [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
**CLI command:** `agent-guardrails` [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
**Tagline:** Universal instruction compiler for coding agents. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)

**Definition:** `agent-guardrails` is a Python-based multi-agent instruction compiler that generates secure, compliant, language-aware instruction files for coding agents. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)

The project exists to solve a specific problem: teams should not have to manually maintain separate prompt files and rule documents for every coding agent. Instead, one canonical governance model should produce all required instruction artifacts for the repository and the agents working inside it. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)

## Mission

The mission of `agent-guardrails` is to help engineering teams define once and enforce everywhere. It should generate strong instructions for code generation, code review, refactoring, testing, architecture decisions, and infrastructure work so that coding agents behave more like disciplined senior engineers and less like generic autocomplete tools. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)

The system should support:
- Repository-wide instructions. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)
- Path-specific instructions. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)
- Portable agent instruction files such as `AGENTS.md`. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Review-mode instructions.
- Generation-mode instructions.
- Safe update and diff workflows.

## Core product concept

`agent-guardrails` is not just a prompt library. It is a Python engine that:
- Loads a shared engineering governance core.
- Applies language-specific rule packs.
- Applies framework-specific rule packs.
- Applies project-type rule packs.
- Renders target-specific instruction files for coding agents.
- Updates existing instruction files safely instead of blindly overwriting them.

The architecture follows a “canonical policy model + target-specific renderer” approach because GitHub treats repository-wide instructions, path-specific instructions, and `AGENTS.md` as distinct instruction mechanisms, and `AGENTS.md` is explicitly intended to work across many coding agents. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)

## Supported instruction targets

Version 1 of `agent-guardrails` should support these output types:

### GitHub Copilot
- `.github/copilot-instructions.md` for repository-wide instructions. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)
- `.github/instructions/*.instructions.md` for path-specific rules using `applyTo` frontmatter. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)
- Optional `excludeAgent` handling for coding-agent vs code-review behavior where needed. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)

### Portable agent files
- `AGENTS.md` at the repo root. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Nested `AGENTS.md` files for subprojects or monorepos, where the nearest file takes precedence. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)

### Additional agent-specific outputs
The system should be designed to support adapters for:
- Cursor. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Claude Code. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)
- Aider. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- OpenAI Codex. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Gemini CLI. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- RooCode. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Windsurf. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Zed. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Warp. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Junie. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Devin. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Amp. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Augment Code. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- VS Code more broadly via `AGENTS.md` or compatible files. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)

The first implementation does not need bespoke rendering for every platform, because `AGENTS.md` already provides a portable baseline for many agent ecosystems. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)

## Supported agents

`agent-guardrails` should define two support tiers.

### Tier 1: first-class adapters
These should be built first because they directly match documented instruction formats or widely used agent workflows:
- GitHub Copilot repository-wide instructions. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)
- GitHub Copilot path-specific instructions. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)
- `AGENTS.md`. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)
- Cursor. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Claude Code. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)
- Aider. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- OpenAI Codex. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Gemini CLI. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)

### Tier 2: portable compatibility or later adapters
These can initially be served through `AGENTS.md` or generic markdown renderers:
- RooCode. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Windsurf. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Zed. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Warp. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Junie. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Devin. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Amp. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Augment Code. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Factory. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Jules. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- goose. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- opencode. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Phoenix. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Semgrep agent usage where applicable. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- Ona. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)

This tiered model keeps V1 practical while still leveraging the broader cross-agent ecosystem around `AGENTS.md`. [blog.gitguardian](https://blog.gitguardian.com/github-copilot-security-and-privacy/)

## Folder structure

Use this repository structure for `agent-guardrails`:

```text
agent-guardrails/
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── architecture.md
│   ├── supported-agents.md
│   ├── language-packs.md
│   ├── framework-packs.md
│   ├── project-types.md
│   └── examples/
├── src/
│   └── agent_guardrails/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── types.py
│       ├── core/
│       │   ├── models.py
│       │   ├── loader.py
│       │   ├── merger.py
│       │   ├── validator.py
│       │   ├── renderer.py
│       │   ├── diff_engine.py
│       │   ├── update_engine.py
│       │   └── policy_engine.py
│       ├── analysis/
│       │   ├── repo_detector.py
│       │   ├── language_detector.py
│       │   ├── framework_detector.py
│       │   ├── project_type_detector.py
│       │   └── path_selector.py
│       ├── packs/
│       │   ├── governance/
│       │   │   ├── base.yaml
│       │   │   ├── security.yaml
│       │   │   ├── compliance.yaml
│       │   │   ├── review.yaml
│       │   │   ├── architecture.yaml
│       │   │   ├── testing.yaml
│       │   │   └── operations.yaml
│       │   ├── languages/
│       │   │   ├── python.yaml
│       │   │   ├── javascript.yaml
│       │   │   ├── typescript.yaml
│       │   │   ├── java.yaml
│       │   │   ├── go.yaml
│       │   │   ├── csharp.yaml
│       │   │   ├── php.yaml
│       │   │   ├── ruby.yaml
│       │   │   ├── kotlin.yaml
│       │   │   ├── scala.yaml
│       │   │   ├── rust.yaml
│       │   │   ├── c.yaml
│       │   │   ├── cpp.yaml
│       │   │   ├── zig.yaml
│       │   │   ├── swift.yaml
│       │   │   ├── objective_c.yaml
│       │   │   ├── dart.yaml
│       │   │   ├── groovy.yaml
│       │   │   ├── elixir.yaml
│       │   │   ├── erlang.yaml
│       │   │   ├── r.yaml
│       │   │   ├── julia.yaml
│       │   │   ├── bash.yaml
│       │   │   ├── powershell.yaml
│       │   │   ├── haskell.yaml
│       │   │   ├── fsharp.yaml
│       │   │   ├── clojure.yaml
│       │   │   └── lua.yaml
│       │   ├── frameworks/
│       │   │   ├── fastapi.yaml
│       │   │   ├── django.yaml
│       │   │   ├── flask.yaml
│       │   │   ├── express.yaml
│       │   │   ├── nestjs.yaml
│       │   │   ├── nextjs.yaml
│       │   │   ├── spring_boot.yaml
│       │   │   ├── aspnet.yaml
│       │   │   ├── laravel.yaml
│       │   │   ├── rails.yaml
│       │   │   ├── gin.yaml
│       │   │   ├── echo.yaml
│       │   │   └── chi.yaml
│       │   └── project_types/
│       │       ├── api_service.yaml
│       │       ├── web_app.yaml
│       │       ├── mobile_app.yaml
│       │       ├── worker.yaml
│       │       ├── cli_tool.yaml
│       │       ├── sdk.yaml
│       │       ├── monolith.yaml
│       │       ├── microservice.yaml
│       │       └── data_pipeline.yaml
│       ├── adapters/
│       │   ├── base.py
│       │   ├── copilot_repo.py
│       │   ├── copilot_path.py
│       │   ├── agents_md.py
│       │   ├── cursor.py
│       │   ├── claude_code.py
│       │   ├── aider.py
│       │   ├── codex.py
│       │   ├── gemini_cli.py
│       │   └── generic_markdown.py
│       ├── templates/
│       │   ├── copilot_instructions.md.j2
│       │   ├── path_instructions.md.j2
│       │   ├── agents.md.j2
│       │   ├── review_mode.md.j2
│       │   └── generic_agent.md.j2
│       └── commands/
│           ├── init.py
│           ├── detect.py
│           ├── generate.py
│           ├── update.py
│           ├── diff.py
│           └── validate.py
├── tests/
│   ├── test_loader.py
│   ├── test_merger.py
│   ├── test_validator.py
│   ├── test_renderers.py
│   ├── test_update_engine.py
│   └── fixtures/
└── examples/
    ├── fastapi-service/
    ├── nextjs-app/
    └── rails-monolith/
```

This layout separates policy modeling, repo analysis, language packs, framework packs, project-type packs, adapters, and output templates so the system can grow without turning into prompt sprawl. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)

## Canonical policy model

The heart of `agent-guardrails` should be a canonical internal policy model, not a collection of ad hoc markdown files. This model is the source of truth, and adapters only transform it into target-specific instruction formats. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)

The canonical policy bundle should include:
- Governance rules
- Security rules
- Privacy and compliance rules
- Architecture rules
- Review rules
- Testing rules
- Operations and observability rules
- Language rules
- Framework rules
- Project-type rules
- Output contract rules
- Metadata for merge priority and scope

A normalized conceptual model might look like:

```python
PolicyBundle(
    governance_rules=[...],
    security_rules=[...],
    compliance_rules=[...],
    architecture_rules=[...],
    review_rules=[...],
    testing_rules=[...],
    operations_rules=[...],
    language_rules=[...],
    framework_rules=[...],
    project_type_rules=[...],
    output_contract=[...],
    metadata={...},
)
```

## Language pack design

`agent-guardrails` should support at least **28 language packs** in the initial architecture:

- Python
- JavaScript
- TypeScript
- Java
- Go
- C#
- PHP
- Ruby
- Kotlin
- Scala
- Rust
- C
- C++
- Zig
- Swift
- Objective-C
- Dart
- Groovy
- Elixir
- Erlang
- R
- Julia
- Bash
- PowerShell
- Haskell
- F#
- Clojure
- Lua

Each language pack must define:
- Project and source structure conventions
- File and module naming rules
- Route/controller/handler placement
- Validation placement
- Service/use-case boundaries
- Repository/data-access boundaries
- Integration/client placement
- Task/worker/job placement
- Method/function design rules
- Error-handling rules
- Logging patterns
- Configuration and secret-handling rules
- Async/concurrency guidance
- Testing expectations
- Security review checklist additions
- Common anti-patterns
- Hooks for framework-specific overrides

Each pack should be declarative, stored in YAML or JSON, and loaded into the core engine instead of being hardcoded into adapter logic. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)

### Example language-pack schema

```yaml
id: python
display_name: Python
category: backend
applies_when:
  languages: ["python"]

structure:
  source_roots: ["app", "src"]
  tests_root: ["tests"]
  preferred_layers:
    - api
    - schemas
    - services
    - repositories
    - models
    - integrations
    - tasks

api_rules:
  - "Create HTTP routes in framework router modules, not in business-logic modules."
  - "Keep route handlers thin and orchestration-focused."
  - "Perform request validation at the boundary using schemas or typed models."
  - "Do not write database queries directly inside route handlers."

service_rules:
  - "Place business logic in service or use-case modules."
  - "Service methods must have explicit inputs and outputs."
  - "Do not mix transport-layer concerns into service logic."

data_rules:
  - "Place persistence code in repositories or data-access modules."
  - "Use parameterized queries or safe ORM access patterns."
  - "Do not leak ORM models directly across boundaries unless explicitly intended."

method_rules:
  - "Keep methods single-purpose."
  - "Prefer explicit names over generic helper names."
  - "Avoid hidden side effects and implicit global state."
  - "Require explicit authorization checks for sensitive operations."

testing_rules:
  - "Mirror source structure in tests where practical."
  - "Write unit tests for services and integration tests for APIs and persistence."
  - "Add authorization, validation, and edge-case coverage for risky flows."

anti_patterns:
  - "Fat controllers"
  - "Business logic in routes"
  - "Direct SQL in handlers"
  - "Untyped request payload handling"
  - "Silent exception swallowing"
```

## Framework packs

Framework packs refine language rules with ecosystem-specific guidance. For example, Python sets the baseline for structure and validation, while FastAPI adds router placement, schema conventions, dependency-injection patterns, and async handling expectations. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)

Initial framework pack targets:
- FastAPI
- Django
- Flask
- Express
- NestJS
- Next.js
- Spring Boot
- ASP.NET
- Laravel
- Rails
- Gin
- Echo
- Chi

Each framework pack should define:
- Recommended folder layout
- Framework-native validation approach
- Controller/router/handler conventions
- Dependency injection or service wiring guidance
- Model/DTO/schema placement
- Error handling conventions
- Testing conventions
- Security and auth integration patterns
- Framework-specific anti-patterns

## Project-type packs

Project-type packs apply additional architecture and operational rules according to what the repository is building.

Initial project types:
- API service
- Web app
- Mobile app
- Worker
- CLI tool
- SDK
- Monolith
- Microservice
- Data pipeline

For example:
- API service packs emphasize endpoint layering, idempotency, auth, and auditability.
- Web app packs emphasize frontend/server boundaries, secrets isolation, and user-facing error hygiene.
- Worker packs emphasize retries, dead-letter handling, idempotency, and observability.
- SDK packs emphasize public API stability, semantic versioning awareness, and documentation quality.

## Governance baseline

Every generated instruction set from `agent-guardrails` must enforce:
- Security by default
- Least privilege
- Deny by default
- Privacy by design
- Compliance awareness
- Maintainability
- Testability
- Observability
- Production readiness
- Explicit architecture boundaries
- Safe dependency management
- Secure CI/CD expectations
- Strong review discipline

The governance baseline must cover:
- Authentication
- Authorization
- Secret handling
- Cryptography
- Input validation
- Output encoding and sanitization
- Secure logging
- Data minimization
- Retention and deletion expectations
- Tenant isolation
- Auditability
- Rollback safety
- Failure handling
- Rate limiting and abuse resistance
- Prompt injection defense for AI-enabled systems

## Review mode

`agent-guardrails` must support a review-mode overlay that makes coding agents behave like strict, skeptical, hard-to-impress senior reviewers. The review mode should be blunt, technically sharp, and aggressive about identifying missing safeguards, but still professional and actionable. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)

Review-mode instructions should require agents to inspect:
- Functional correctness
- Security findings
- Privacy and compliance findings
- Architecture quality
- Maintainability issues
- Reliability and performance risks
- Testing gaps
- Production readiness gaps
- Rollback and observability concerns

The system should also support a “grumpy reviewer” tone layer for code review, while explicitly preventing abusive or unprofessional language.

## Update and merge behavior

When `agent-guardrails` updates an existing repository’s instructions, it must:
- Preserve strong safeguards unless explicitly told to weaken them
- Detect duplication
- Merge overlapping rules carefully
- Surface conflicts
- Keep useful project-specific instructions
- Refuse silent security downgrades
- Support dry-run mode
- Produce readable diffs
- Support regeneration without deleting valuable local customizations

This is especially important for GitHub’s combined instruction model, where repository-wide rules, path-specific rules, and local `AGENTS.md` files can all coexist and potentially overlap. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)

## Adapter model

Every supported agent target should be implemented through an adapter interface. The adapter should be responsible only for rendering output files and choosing output paths, not for owning policy logic. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)

Conceptually:

```python
class AgentAdapter(Protocol):
    name: str

    def output_paths(self, project_context) -> list[str]:
        ...

    def render(self, bundle, project_context) -> dict[str, str]:
        ...

    def merge_strategy(self) -> str:
        ...
```

Example adapters:
- `CopilotRepoAdapter` → `.github/copilot-instructions.md` [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)
- `CopilotPathAdapter` → `.github/instructions/*.instructions.md` [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)
- `AgentsMdAdapter` → `AGENTS.md` [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)
- `CursorAdapter`
- `ClaudeCodeAdapter`
- `AiderAdapter`
- `CodexAdapter`
- `GeminiCliAdapter`

## CLI responsibilities

The `agent-guardrails` CLI should support commands such as:
- `agent-guardrails init`
- `agent-guardrails detect`
- `agent-guardrails generate`
- `agent-guardrails update`
- `agent-guardrails diff`
- `agent-guardrails validate`

Typical workflow:
1. Detect repository stack and structure.
2. Load governance core.
3. Load language packs.
4. Load framework packs.
5. Load project-type pack.
6. Merge into a canonical bundle.
7. Validate the bundle.
8. Render target-specific files.
9. Show diff or write output.
10. Optionally update existing instructions safely.

## First milestone

The best first milestone for `agent-guardrails` is:
- Implement canonical policy models.
- Implement governance packs.
- Implement five language packs: Python, TypeScript, Java, Go, C#.
- Implement three framework packs: FastAPI, Next.js, Spring Boot.
- Implement three adapters: Copilot repository-wide, Copilot path-specific, and `AGENTS.md`. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)

That gets the project to a useful V1 quickly using instruction formats that are already documented and supported. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)



## Final scope

The final scope of `agent-guardrails` is:

- A Python-based multi-agent instruction compiler. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)
- A canonical policy engine with governance, language, framework, and project-type packs.
- A renderer layer that outputs GitHub Copilot repo-wide instructions, GitHub Copilot path-specific instructions, and portable `AGENTS.md` files. [youtube](https://www.youtube.com/watch?v=9x4ekT65HX8)
- A system that supports 25+ languages through declarative packs.
- A system that supports strong code-generation and code-review governance.
- A safe update and diff workflow for maintaining instruction files over time.

---

## Implementation plan

### Locked decisions

| Decision | Choice |
|----------|--------|
| Build backend | hatchling (PEP 621, simple) |
| CLI framework | click (composable subcommands) |
| Template engine | Jinja2 |
| Pack format | YAML (human-readable, declarative) |
| Python version | 3.11+ (modern typing: `Self`, `TypeAlias`) |
| Config file | `[tool.agent-guardrails]` in `pyproject.toml` — no separate config file |
| Section ownership | `<!-- agent-guardrails:managed -->` HTML comments mark tool-managed sections; unmarked sections are user-owned and preserved on update |
| Security stance | Security rules cannot be silently downgraded; `--force` required for weakening |
| Output size management | Renderer auto-condenses when approaching limits (Codex 32 KiB, Claude Code 200 lines, Cursor 500 lines); warns user; splits only if condensing is insufficient and adapter supports multi-file |
| Review mode toggle | CLI flag `--mode review` activates review overlay across all adapters |
| V1 scope | 5 languages, 3 frameworks, 3 project types, 8 adapters |
| Excluded from V1 | CI/CD integration, GitHub Action, VS Code extension, web UI, monorepo multi-project splitting, `pack create` scaffolding command |

---

### Agent instruction format reference

Research on each agent's file format, used to drive adapter implementations.

| Agent | Primary file | Format | Path-scoping | Size limit | Reads AGENTS.md |
|-------|-------------|--------|--------------|------------|-----------------|
| GitHub Copilot | `.github/copilot-instructions.md` | Markdown | `applyTo` glob in YAML frontmatter (path-specific files) | ~2 pages recommended | Yes (native) |
| Cursor | `.cursor/rules/*.mdc` | YAML frontmatter + Markdown | `globs` frontmatter field | 500 lines recommended | Yes (native) |
| Claude Code | `CLAUDE.md` | Markdown (rules: YAML frontmatter + MD) | `paths` in `.claude/rules/*.md` frontmatter | 200 lines recommended | Via `@import` only |
| Aider | `CONVENTIONS.md` | Markdown (loaded via `--read`) | N/A | None documented | No |
| OpenAI Codex | `AGENTS.md` | Markdown | Directory nesting (nearest wins) | 32 KiB default | Yes (primary) |
| Gemini CLI | `GEMINI.md` | Markdown | Directory nesting / JIT | None documented | Configurable via settings |

#### Key format details per adapter

**GitHub Copilot path-specific** (`.github/instructions/*.instructions.md`):
```yaml
---
applyTo: "**/*.ts,**/*.tsx"
excludeAgent: "code-review"
---
```

**Cursor** (`.cursor/rules/*.mdc`):
```yaml
---
description: "RPC service conventions"
globs: src/components/**/*.tsx
alwaysApply: true
---
```

**Claude Code** (`.claude/rules/*.md`):
```yaml
---
paths:
  - "src/api/**/*.ts"
---
```
- Supports `@path/to/file` import syntax (max 5 hops)
- Multiple `CLAUDE.md` files concatenated root→cwd

**Aider** (`.aider.conf.yml`):
```yaml
read: CONVENTIONS.md
```

**Codex**: walks from project root to cwd; checks `AGENTS.override.md` → `AGENTS.md` per directory. Configurable via `~/.codex/config.toml`:
```toml
project_doc_max_bytes = 32768
```

**Gemini CLI**: reads `GEMINI.md` globally (`~/.gemini/`) + workspace + JIT (on directory access). Configurable filenames:
```json
{ "context": { "fileName": ["AGENTS.md", "GEMINI.md"] } }
```

---

### Phased execution plan

#### Phase 1: Project scaffolding and core models

**Goal:** Working Python package skeleton with typed domain models and CLI entry point.

Files to create:
- `pyproject.toml`
- `src/agent_guardrails/__init__.py`
- `src/agent_guardrails/cli.py`
- `src/agent_guardrails/config.py`
- `src/agent_guardrails/types.py`
- `src/agent_guardrails/core/__init__.py`
- `src/agent_guardrails/core/models.py`

Work:
1. Initialize `pyproject.toml` with hatchling, Python 3.11+, CLI entry point `agent-guardrails`
2. Define domain models: `Rule`, `RulePack`, `PolicyBundle`, `ProjectContext`, `AdapterOutput`
3. Define enums: `RuleCategory`, `Severity`, `MergeStrategy`, `AgentTarget`
4. CLI skeleton with click: subcommands `init`, `detect`, `generate`, `update`, `diff`, `validate`
5. Dependencies: `click`, `pyyaml`, `jinja2`, `rich`, `deepdiff`; dev: `pytest`, `pytest-cov`

Verification:
- `pip install -e .` succeeds
- `agent-guardrails --help` displays subcommands
- Models can be instantiated

---

#### Phase 2: Pack loader and governance baseline

**Goal:** YAML pack system with governance packs loaded and validated.

Files to create:
- `src/agent_guardrails/core/loader.py`
- `src/agent_guardrails/core/validator.py`
- `src/agent_guardrails/packs/governance/base.yaml`
- `src/agent_guardrails/packs/governance/security.yaml`
- `src/agent_guardrails/packs/governance/compliance.yaml`
- `src/agent_guardrails/packs/governance/review.yaml`
- `src/agent_guardrails/packs/governance/architecture.yaml`
- `src/agent_guardrails/packs/governance/testing.yaml`
- `src/agent_guardrails/packs/governance/operations.yaml`

Work:
1. YAML loader that reads `.yaml` from `packs/` directories, validates schema, returns typed `RulePack`
2. Validator: required fields, no duplicate rule IDs, non-empty rules
3. 7 governance packs with full rule content covering security, compliance, review, architecture, testing, operations

Verification:
- `tests/test_loader.py` — valid YAML loads correctly
- `tests/test_validator.py` — invalid packs raise errors
- All governance packs load without error

---

#### Phase 3: Language packs (V1 — 5 languages)

**Goal:** Declarative packs for Python, TypeScript, Java, Go, C#.

Files to create:
- `src/agent_guardrails/packs/languages/python.yaml`
- `src/agent_guardrails/packs/languages/typescript.yaml`
- `src/agent_guardrails/packs/languages/java.yaml`
- `src/agent_guardrails/packs/languages/go.yaml`
- `src/agent_guardrails/packs/languages/csharp.yaml`

Each pack defines: `structure`, `api_rules`, `service_rules`, `data_rules`, `method_rules`, `error_handling_rules`, `logging_rules`, `concurrency_rules`, `testing_rules`, `security_checklist`, `anti_patterns`.

Verification:
- All 5 packs load and validate
- Schema validation catches missing sections

---

#### Phase 4: Framework packs (V1 — 3 frameworks)

**Goal:** Framework packs for FastAPI, Next.js, Spring Boot.

Files to create:
- `src/agent_guardrails/packs/frameworks/fastapi.yaml` (extends: python)
- `src/agent_guardrails/packs/frameworks/nextjs.yaml` (extends: typescript)
- `src/agent_guardrails/packs/frameworks/spring_boot.yaml` (extends: java)

Each pack defines: `extends_language`, `folder_layout`, `validation_approach`, `controller_conventions`, `dependency_injection`, `model_placement`, `error_handling`, `auth_patterns`, `testing_conventions`, `anti_patterns`.

---

#### Phase 5: Project-type packs (V1 — 3 types)

**Goal:** API service, web app, microservice.

Files to create:
- `src/agent_guardrails/packs/project_types/api_service.yaml`
- `src/agent_guardrails/packs/project_types/web_app.yaml`
- `src/agent_guardrails/packs/project_types/microservice.yaml`

---

#### Phase 6: Merger and policy engine

**Goal:** Merge all packs into a single PolicyBundle with priority resolution and dedup.

Files to create:
- `src/agent_guardrails/core/merger.py`
- `src/agent_guardrails/core/policy_engine.py`

Work:
1. Merger: governance + language + framework + project-type → `PolicyBundle`. More-specific wins on overlap. Security rules never silently downgraded.
2. Policy engine: orchestrates detect → load → merge → validate → return bundle.
3. Priority metadata per pack (`priority: int`, higher wins).

Verification:
- `tests/test_merger.py` — merging produces expected bundle
- Security rules survive conflicts with convenience rules
- Duplicate detection works

---

#### Phase 7: Repository analysis

**Goal:** Auto-detect languages, frameworks, project type from repo contents.

Files to create:
- `src/agent_guardrails/analysis/__init__.py`
- `src/agent_guardrails/analysis/language_detector.py`
- `src/agent_guardrails/analysis/framework_detector.py`
- `src/agent_guardrails/analysis/project_type_detector.py`
- `src/agent_guardrails/analysis/repo_detector.py`
- `src/agent_guardrails/analysis/path_selector.py`

Work:
1. Language detector: scan file extensions + config files (`package.json`, `pyproject.toml`, `go.mod`, `pom.xml`, `*.csproj`)
2. Framework detector: scan imports, dependencies, framework-specific config
3. Project-type detector: heuristics from directory structure, entry points, Dockerfiles
4. Repo detector: orchestrator → `ProjectContext`
5. Path selector: determine which paths need path-specific instructions

---

#### Phase 8: Adapter layer and rendering

**Goal:** Transform PolicyBundle → agent-specific instruction files.

Files to create:
- `src/agent_guardrails/adapters/__init__.py`
- `src/agent_guardrails/adapters/base.py`
- `src/agent_guardrails/adapters/copilot_repo.py`
- `src/agent_guardrails/adapters/copilot_path.py`
- `src/agent_guardrails/adapters/agents_md.py`
- `src/agent_guardrails/templates/copilot_instructions.md.j2`
- `src/agent_guardrails/templates/path_instructions.md.j2`
- `src/agent_guardrails/templates/agents.md.j2`
- `src/agent_guardrails/templates/review_mode.md.j2`
- `src/agent_guardrails/templates/generic_agent.md.j2`
- `src/agent_guardrails/core/renderer.py`

Work:
1. `AgentAdapter` protocol: `name`, `output_paths()`, `render()`, `merge_strategy()`, `size_limit`
2. Jinja2 templates for each output format
3. V1 adapters: Copilot repo-wide, Copilot path-specific (with `applyTo` frontmatter), AGENTS.md
4. Renderer orchestrator: takes bundle + adapters + context → `dict[str, str]`
5. Size-awareness: renderer condenses output when approaching adapter limits, warns user

Verification:
- `tests/test_renderers.py` — each adapter produces valid output
- Copilot path adapter has correct `applyTo` frontmatter
- AGENTS.md contains all expected sections and stays under 32 KiB

---

#### Phase 9: Diff and update engine

**Goal:** Safe update with conflict detection and dry-run.

Files to create:
- `src/agent_guardrails/core/diff_engine.py`
- `src/agent_guardrails/core/update_engine.py`

Work:
1. Diff engine: compare existing vs. new, produce unified diff, detect security downgrades
2. Update engine: section-based merge using `<!-- agent-guardrails:managed -->` ownership markers
   - Tool-managed sections: regenerated freely
   - Unmarked sections: user-owned, preserved on update
   - Security rules: refuse downgrade without `--force`
   - `--dry-run`: show diff without writing

Verification:
- `tests/test_update_engine.py` — safeguards preserved, security downgrades detected
- Dry-run produces diff without writing files
- User-owned sections survive regeneration

---

#### Phase 10: CLI commands wiring

**Goal:** Wire all components into working CLI subcommands.

Files to create:
- `src/agent_guardrails/commands/__init__.py`
- `src/agent_guardrails/commands/init_cmd.py`
- `src/agent_guardrails/commands/detect.py`
- `src/agent_guardrails/commands/generate.py`
- `src/agent_guardrails/commands/update.py`
- `src/agent_guardrails/commands/diff.py`
- `src/agent_guardrails/commands/validate.py`

Commands:
- `init` — interactive setup: detect repo, ask for targets, write `[tool.agent-guardrails]` config
- `detect` — run repo analysis, print detected stack
- `generate` — full pipeline: detect → load → merge → render → write (or `--dry-run`)
- `update` — regenerate with merge against existing files
- `diff` — show what would change without writing
- `validate` — validate existing instruction files against current policy bundle

---

#### Phase 11: Additional adapters (Tier 1)

**Goal:** Cursor, Claude Code, Aider, Codex, Gemini CLI adapters.

Files to create:
- `src/agent_guardrails/adapters/cursor.py`
- `src/agent_guardrails/adapters/claude_code.py`
- `src/agent_guardrails/adapters/aider.py`
- `src/agent_guardrails/adapters/codex.py`
- `src/agent_guardrails/adapters/gemini_cli.py`

Adapter details:
- **Cursor** → `.cursor/rules/*.mdc` with YAML frontmatter (`description`, `globs`, `alwaysApply`)
- **Claude Code** → `CLAUDE.md` + `.claude/rules/*.md` with `paths` frontmatter; uses `@import` references; keeps under 200 lines or auto-splits
- **Aider** → `CONVENTIONS.md` + `.aider.conf.yml` with `read: CONVENTIONS.md`
- **Codex** → `AGENTS.md` (size-aware: auto-condense to fit 32 KiB)
- **Gemini CLI** → `GEMINI.md`

---

#### Phase 12: Remaining language packs (23 more)

**Goal:** Complete 28-language coverage.

Languages: JavaScript, PHP, Ruby, Kotlin, Scala, Rust, C, C++, Zig, Swift, Objective-C, Dart, Groovy, Elixir, Erlang, R, Julia, Bash, PowerShell, Haskell, F#, Clojure, Lua.

---

#### Phase 13: Documentation and examples

**Goal:** README, architecture docs, example outputs.

Files to create:
- `README.md`
- `docs/architecture.md`
- `docs/supported-agents.md`
- `examples/fastapi-service/` — generated instruction files
- `examples/nextjs-app/` — generated instruction files

---

### End-to-end verification checklist

1. `pip install -e ".[dev]"` succeeds
2. `agent-guardrails --help` shows all subcommands
3. `agent-guardrails detect` on a FastAPI repo → Python + FastAPI + API service
4. `agent-guardrails generate --target copilot,agents-md --dry-run` produces valid output
5. `agent-guardrails generate --target all` writes all instruction files
6. `agent-guardrails update` preserves user-owned sections and refuses security downgrades without `--force`
7. `agent-guardrails diff` shows unified diff of pending changes
8. `agent-guardrails validate` catches policy violations
9. `pytest` passes all unit and integration tests
10. Generated `.github/copilot-instructions.md` is valid markdown under ~2 pages
11. Generated `.github/instructions/*.instructions.md` have valid `applyTo` frontmatter
12. Generated `AGENTS.md` is under 32 KiB
13. Generated `.cursor/rules/*.mdc` have valid frontmatter with `description` and `globs`
14. Generated `CLAUDE.md` is under 200 lines (or splits into `.claude/rules/`)
15. Output size warnings fire when limits are approached

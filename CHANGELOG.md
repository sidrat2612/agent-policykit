# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]



## [0.1.0] - 2026-05-20

First public stable release.

### Added
- Full CLI: `init`, `detect`, `generate`, `update`, `diff`, `validate`
- 8 Tier 1 adapters: Copilot (repo + path), AGENTS.md, Cursor, Claude Code, Aider, Codex, Gemini CLI
- 15 Tier 2 exported compatibility files: RooCode, Windsurf, Zed, Warp, Junie, Devin, Amp, Augment Code, Factory, Jules, goose, opencode, Phoenix, Semgrep, Ona
- 8 governance packs: architecture, base, compliance, operations, output contract, review, security, testing
- 28 language packs
- 13 framework packs
- 9 project-type packs
- Safe update workflow with managed-section merge
- Security downgrade blocking with structured rule-ID enforcement
- Non-security rule removal surfacing in diff and update flows
- Size-aware markdown condensation for Codex, Claude, and Cursor
- Claude Code shared-rule splitting with `.claude/rules/shared.md`
- Interactive `init` command with stack detection
- Review-mode overlay with `--mode review`
- Worked examples for FastAPI service, Next.js app, and Rails monolith

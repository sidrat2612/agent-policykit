# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Full CLI: `init`, `detect`, `generate`, `update`, `diff`, `validate`
- 8 Tier 1 adapters: Copilot (repo + path), AGENTS.md, Cursor, Claude Code, Aider, Codex, Gemini CLI
- 15 Tier 2 exported compatibility files (RooCode, Windsurf, Zed, Warp, Junie, Devin, Amp, Augment Code, Factory, Jules, goose, opencode, Phoenix, Semgrep, Ona)
- 7 governance packs (security, compliance, review, architecture, testing, operations, base)
- 28 language packs
- 13 framework packs
- 9 project-type packs
- Safe update workflow with managed-section merge
- Security downgrade blocking with structured rule-ID enforcement
- Non-security rule removal surfacing in diff/update
- Size-aware markdown condensation for Codex, Claude, and Cursor
- Claude Code shared-rule splitting (`.claude/rules/shared.md`)
- Interactive `init` command with stack detection
- Review-mode overlay (`--mode review`)
- Worked examples: FastAPI service, Next.js app, Rails monolith

## [0.1.0] - 2026-05-20

Initial alpha release.

# Supported Agents

## Tier 1 targets implemented

- GitHub Copilot repository-wide: `.github/copilot-instructions.md`
- GitHub Copilot path-scoped: `.github/instructions/project.instructions.md`
- Portable AGENTS file: `AGENTS.md`
- Cursor: `.cursor/rules/project.mdc`
- Claude Code: `CLAUDE.md`
- Aider: `CONVENTIONS.md` and `.aider.conf.yml`
- OpenAI Codex: `AGENTS.md`
- Gemini CLI: `GEMINI.md`

## Notes

- Codex intentionally shares `AGENTS.md` with the portable AGENTS target.
- The CLI deduplicates identical outputs when multiple targets resolve to the same file.
- Cursor, Aider, Codex, and Gemini outputs are aligned to the documented primary files.

## Not yet implemented

- Tier 2 bespoke adapters such as RooCode, Windsurf, Zed, Warp, Junie, Devin, Amp, Augment Code, Factory, Jules, goose, opencode, Phoenix, Semgrep, and Ona.
- Nested `AGENTS.md` hierarchy resolution for monorepos.
- Claude Code rule splitting and import-based expansion for oversized outputs.

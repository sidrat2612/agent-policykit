# Supported Agents

This page is for teams checking whether `agent-policykit` covers the coding agents already used in their workflow.

Each adapter takes the same merged policy bundle and renders the file shape that agent expects, so teams can standardize guidance across tools instead of hand-maintaining separate instruction files.

## Tier 1 targets implemented

- GitHub Copilot repository-wide: `.github/copilot-instructions.md`
- GitHub Copilot path-scoped: `.github/instructions/*.instructions.md` generated per detected source/test scope
- Portable AGENTS file: `AGENTS.md` plus nested `AGENTS.md` files for detected monorepo subprojects
- Cursor: `.cursor/rules/project.mdc`
- Claude Code: `CLAUDE.md` plus `.claude/rules/shared.md` and `.claude/rules/*.md` imports for scoped rules
- Aider: `CONVENTIONS.md` and `.aider.conf.yml`
- OpenAI Codex: `AGENTS.md` plus nested `AGENTS.md` files for detected monorepo subprojects
- Gemini CLI: `GEMINI.md`

## Tier 2 targets implemented via dedicated markdown exports

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

## Notes

- Codex intentionally shares `AGENTS.md` with the portable AGENTS target.
- The CLI deduplicates identical outputs when multiple targets resolve to the same file.
- Review mode overlays are rendered across all shipped adapters via `--mode review`.
- Copilot path outputs emit `excludeAgent: "code-review"` on implementation scopes in generate mode.
- Adapter outputs expose explicit `output_paths()` contracts and automatically condense markdown-like outputs before warning when Codex, Claude Code, or Cursor outputs approach their configured size limits.
- Claude repository-wide guidance is split into a compact `CLAUDE.md` plus an imported `.claude/rules/shared.md` file.
- Tier 2 exported compatibility files are repository-defined outputs; if a platform expects a different ingestion path in your environment, mirror the generated file as needed.

## Status

- All targets in the current repository specification are implemented.

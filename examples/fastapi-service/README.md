# FastAPI Service Example

This directory contains a minimal FastAPI API service fixture used for detection and generation validation.

Validated example outputs:

- `.github/copilot-instructions.md`
- `.github/instructions/project.instructions.md`
- `AGENTS.md`
- `AGENT_POLICY.md`
- `CLAUDE.md`
- `.cursor/rules/project.mdc`
- `CONVENTIONS.md`
- `.aider.conf.yml`
- `GEMINI.md`

Suggested local command:

```bash
agent-policykit detect
agent-policykit generate --target copilot --target copilot-path --target agents-md --target generic-markdown --target claude-code --target cursor --target aider --target gemini-cli --dry-run
```

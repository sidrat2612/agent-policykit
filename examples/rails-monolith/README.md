# Rails Monolith Example

This directory contains a minimal Rails monolith fixture used for detection and generation validation.

Validated example outputs:

- `.github/copilot-instructions.md`
- `.github/instructions/app.instructions.md`
- `AGENTS.md`
- `AGENT_POLICY.md`
- `CLAUDE.md`
- `.cursor/rules/project.mdc`

Suggested local command:

```bash
agent-policykit detect
agent-policykit generate --target copilot --target copilot-path --target agents-md --target generic-markdown --target claude-code --target cursor --dry-run
```

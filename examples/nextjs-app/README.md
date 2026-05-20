# Next.js App Example

This directory contains a minimal Next.js web application fixture used for detection and generation validation.

Validated example outputs:

- `.github/copilot-instructions.md`
- `.github/instructions/project.instructions.md`
- `AGENTS.md`
- `AGENT_POLICY.md`
- `.cursor/rules/project.mdc`
- `CLAUDE.md`
- `GEMINI.md`

Suggested local command:

```bash
agent-policykit detect
agent-policykit generate --target copilot --target copilot-path --target agents-md --target generic-markdown --target cursor --target claude-code --target gemini-cli --dry-run
```

# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |
| < 0.1   | No        |

## Reporting a vulnerability

Do not open a public GitHub issue for security vulnerabilities.

Use [GitHub Security Advisories](https://github.com/sidrat2612/agent-policykit/security/advisories) with:

- A description of the issue
- Reproduction steps
- Expected impact
- A suggested fix, if you have one

Reports are acknowledged within 72 hours when possible.

## Security model

agent-policykit is a local CLI tool. It reads YAML packs and writes markdown instruction files. It does not execute source code during analysis, and it does not make network calls.

## Threat model

| Vector | Mitigation |
|--------|-----------|
| YAML injection / deserialization | Uses `yaml.safe_load` exclusively — no arbitrary object instantiation |
| Path traversal via config | All output paths are resolved and constrained to the project root |
| Template injection | Jinja2 templates are bundled, not user-supplied; no `eval` or dynamic template loading |
| Malicious pack content | Packs contain only text rules — no executable code, no imports, no shell commands |
| Sensitive file exposure | Detection scans file presence only — never reads file contents of source code |

## What agent-policykit does not do

- Make network requests
- Execute code from packs or source files
- Run a network listener
- Use `shell=True` in subprocess calls
- Store credentials or API keys
- Call external LLM APIs

## Sensitive file exclusion

The detector skips common secret and generated-file patterns by default:

- `*.pem`, `*.key`, `*.p12`, `*.pfx`
- `.env`, `.env.*`
- `node_modules/`, `venv/`, `.venv/`, `dist/`, `build/`, `__pycache__/`

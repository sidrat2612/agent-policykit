# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✅ Current |

## Reporting a vulnerability

If you discover a security vulnerability in `agent-policykit`, please report it responsibly.

**Do not open a public GitHub issue for security vulnerabilities.**

Instead, email: **siddharth.rathore2612@gmail.com**

Include:
- Description of the vulnerability
- Steps to reproduce
- Impact assessment
- Suggested fix (if any)

You will receive an acknowledgment within 48 hours and a resolution timeline within 7 days.

## Security design

`agent-policykit` is a local CLI tool that reads YAML packs and writes markdown files. It does not:
- Make network requests
- Execute arbitrary code from packs
- Process untrusted user input beyond file paths

The primary security surface is:
- YAML parsing (mitigated: uses `yaml.safe_load` only)
- File path handling (mitigated: writes only within the project root)
- Template rendering (mitigated: Jinja2 with autoescape disabled intentionally for markdown output; no user-supplied template injection path)

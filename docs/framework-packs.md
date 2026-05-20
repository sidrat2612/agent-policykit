# Framework Packs

Framework packs sit on top of base language guidance so generated instructions reflect the conventions that actually matter in FastAPI, Next.js, Spring Boot, Rails, and similar frameworks.

This is the layer that prevents every repository from getting the same generic framework-agnostic rules.

## Implemented packs

The repository currently ships framework packs for all frameworks listed in the current project specification:

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

Framework packs live in `src/agent_policykit/packs/frameworks/` and override or extend the baseline language rules.

## Expected framework concerns

Framework packs should cover:

- folder layout
- router/controller placement
- validation strategy
- dependency injection or service wiring
- DTO/model/schema placement
- framework-specific auth and error handling
- testing conventions
- framework-specific anti-patterns

## Detection coverage

Framework detection now covers the shipped pack set across `package.json`, `pyproject.toml`, `requirements.txt`, `go.mod`, `composer.json`, `Gemfile`, and `*.csproj` inputs.

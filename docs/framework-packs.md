# Framework Packs

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

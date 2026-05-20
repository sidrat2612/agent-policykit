# Framework Packs

## Implemented packs

The repository currently ships framework packs for:

- FastAPI
- Next.js
- Spring Boot

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

## Planned additions

The next packs expected by the project spec are Django, Flask, Express, NestJS, ASP.NET, Laravel, Rails, Gin, Echo, and Chi.

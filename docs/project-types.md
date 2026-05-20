# Project Types

Project-type packs add architecture and operational rules for the kind of system being built.

This is how `agent-policykit` gives an API service, monolith, worker, CLI tool, or SDK different guidance instead of applying one generic instruction set everywhere.

## Implemented project-type packs

The repository currently ships all project-type packs listed in the current project specification:

- API service
- Web app
- Mobile app
- Worker
- CLI tool
- SDK
- Monolith
- Microservice
- Data pipeline

Project-type packs live in `src/agent_policykit/packs/project_types/` and provide architecture and operational guidance specific to the type of system being built.

## Usage

Project type is detected from repository structure and framework hints, then the matching pack is merged into the final `PolicyBundle`. Detection now includes monorepo, worker, mobile, SDK, monolith, and data-pipeline heuristics in addition to the original API/web/CLI coverage.

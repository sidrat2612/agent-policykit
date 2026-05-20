# Project Types

## Implemented project-type packs

The repository currently ships project-type packs for:

- API service
- Web app
- Microservice

Project-type packs live in `src/agent_policykit/packs/project_types/` and provide architecture and operational guidance specific to the type of system being built.

## Planned additions

The project spec also calls for:

- Mobile app
- Worker
- CLI tool
- SDK
- Monolith
- Data pipeline

## Usage

Project type is detected from repository structure and framework hints, then the matching pack is merged into the final `PolicyBundle`.

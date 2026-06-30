# Progress: docker-ci

## Status

- State: done
- Feature file: `features/docker-ci.feature`
- Related spec: `docs/harness-sdd/project-spec.md`

## Timeline

- 2026-06-28: Implemented from approved technical-test plan.

## TDD Notes

- Red: runtime contract captured in Gherkin.
- Green: Docker Compose and GitHub Actions added.
- Refactor: backend and frontend container concerns kept in their own Dockerfiles.

## Verification

- `docker compose config`: passed
- `docker compose build`: passed after Docker Desktop became available
- `docker compose up -d`: passed on alternate ports `BACKEND_PORT=18000` and `FRONTEND_PORT=15173`
- `GET http://localhost:18000/health`: returned `{"status":"ok"}`
- `GET http://localhost:15173`: returned HTTP 200
- `POST http://localhost:18000/clients`: created a smoke-test client
- GitHub Actions syntax: workflow added; runtime execution pending on GitHub

## Open Items

- None




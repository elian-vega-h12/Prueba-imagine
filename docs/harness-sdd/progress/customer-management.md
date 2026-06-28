# Progress: customer-management

## Status

- State: blocked
- Feature file: `features/customer-management.feature`
- Related spec: `docs/harness-sdd/project-spec.md`

## Timeline

- 2026-06-28: Implemented from approved technical-test plan.

## TDD Notes

- Red: backend API tests define create/list/get/not-found behavior.
- Green: FastAPI routes, service, repository, and SQLAlchemy model satisfy tests.
- Refactor: customer behavior separated into schemas, repositories, services, and controllers.

## Verification

- `pytest`: 11 passed
- `ruff check .`: passed
- `mutmut run`: blocked on native Windows; WSL is available but has no `python3`

## Open Items

- Mutation baseline must run in CI/Linux or a WSL distribution with Python.

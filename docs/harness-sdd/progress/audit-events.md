# Progress: audit-events

## Status

- State: blocked
- Feature file: `features/audit-events.feature`
- Related spec: `docs/harness-sdd/project-spec.md`

## Timeline

- 2026-06-28: Implemented from approved technical-test plan.

## TDD Notes

- Red: backend tests assert audit payloads for ticket creation and status changes.
- Green: audit service writes MongoDB-compatible documents and defaults missing users to `system`.
- Refactor: audit persistence is injectable for tests.

## Verification

- `pytest`: 11 passed
- `ruff check .`: passed
- `mutmut run`: blocked on native Windows; WSL is available but has no `python3`

## Open Items

- Mutation baseline must run in CI/Linux or a WSL distribution with Python.

# Review: customer-management

## Verdict

- approved-with-blocker

## Findings

- Mutation baseline is blocked locally because Mutmut does not support native Windows and WSL has no `python3`.

## Scenario Coverage

- `features/customer-management.feature`: covered by `backend/tests/test_clients.py`.

## Commands

- `pytest`: 11 passed
- `ruff check .`: passed
- `mutmut run`: blocked by platform

## Notes

- CI on Ubuntu should be able to run the mutation baseline.

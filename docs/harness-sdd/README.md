# Harness SDD

Harness SDD is the local workflow for changing behavior in this repository with a written specification, Gherkin scenarios, TDD, review, and mutation testing.

## When To Use It

Use this method for changes that affect customer management, ticket management, API behavior, persistence, audit events, frontend workflows, Docker runtime behavior, or CI verification.

Small mechanical changes can skip the full flow, but must still run the relevant tests.

## Required Flow

```text
spec -> gherkin -> human approval -> TDD -> judge -> mutation testing -> done
```

1. `spec`: update `docs/harness-sdd/project-spec.md` when the behavior is not already clear.
2. `gherkin`: write scenarios in `features/*.feature`.
3. `human approval`: stop until the user approves the scenarios.
4. `TDD`: implement one approved scenario at a time, test first.
5. `judge`: review coverage, design, risk, and scope.
6. `mutation testing`: run Mutmut and inspect surviving mutants.
7. `done`: mark the feature done only after review and mutation evidence are written.

## Feature States

`docs/harness-sdd/feature-list.json` uses these states:

- `pending`: proposed feature, not specified enough.
- `gherkin_ready`: scenarios exist and need human approval.
- `approved`: scenarios were approved by the user.
- `in_progress`: TDD implementation is in progress.
- `review`: implementation is ready for judge review.
- `mutation`: review passed and mutation testing is running or being analyzed.
- `done`: review and mutation testing are complete.
- `blocked`: progress needs an external decision or dependency.

## Rules

- Do not edit `backend/app/`, `backend/tests/`, `frontend/src/`, or `frontend/tests/` for an SDD feature before the Gherkin scenarios are approved.
- Every approved scenario must be covered by an automated test.
- `pytest` and `pnpm --dir frontend test` are the minimum verification commands for behavior changes.
- `mutmut run` is required before closing backend behavior features.
- The first mutation gate is a baseline: score is reported, but not globally blocking.
- Surviving mutants in files touched by the feature are findings, even when the global mutation score does not fail.
- Gherkin files are contracts for humans and agents. They are not executable tests in this version.

## Commands

```bash
pytest
ruff check backend
pnpm --dir frontend test
pnpm --dir frontend lint
pnpm --dir frontend build
mutmut run
```

## Roles

The role prompts live in `.agents/harness-sdd/`. They are reference prompts for Codex subagents or for the main thread. They are not auto-executed by the repository.

- `craftsman_lead`: orchestrates the workflow and guards the approval gates.
- `spec_partner`: clarifies behavior and updates the project spec.
- `gherkin_author`: writes `.feature` scenarios from the spec.
- `tdd_craftsman`: implements approved scenarios with TDD.
- `judge`: reviews the implementation without editing code.
- `mutation_tester`: runs Mutmut, analyzes survivors, and writes mutation evidence.

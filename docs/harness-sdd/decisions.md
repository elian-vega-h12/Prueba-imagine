# Harness SDD Decisions

## 2026-06-28

- Harness SDD is repo-local first and adapted from `simple-spend-summary-service`.
- Gherkin scenarios are human-readable contracts, not executable tests in this version.
- Human approval is required after Gherkin and before implementation for any feature with `sdd: true`.
- `craftsman_lead` is the orchestration role. In Codex, the main thread usually plays this role.
- Mutmut is the backend mutation testing tool because this project is Python-based.
- Mutation score is baseline-only at first; surviving mutants in touched files are treated as findings.
- MongoDB audit events are included as a value-add even though they are optional in the technical test.
- The optional Salesforce response is delivered as `salesforce.md`, not implemented as running code.

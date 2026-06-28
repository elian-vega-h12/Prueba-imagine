# Project Spec

This is the living specification used by Harness SDD. Keep it concise and update it when a feature changes the behavior described here.

## Purpose

The application lets support staff manage customers and support tickets through a FastAPI backend and a React frontend. Customer and ticket records are persisted in PostgreSQL. Ticket lifecycle events are written to MongoDB as audit records.

## Main Flow

1. A user opens the React frontend.
2. The frontend loads customers and tickets from the FastAPI API.
3. The user creates customers with name, email, and company.
4. The user creates tickets associated with an existing customer.
5. The user updates ticket status through the allowed lifecycle states.
6. Ticket creation and status changes are written as audit events.

## Core Behavior

- Clients have UUID `id`, `name`, `email`, `company`, and UTC `created_at`.
- Tickets have UUID `id`, associated client, `title`, `description`, `status`, and UTC `created_at`.
- Allowed ticket statuses are `Pendiente`, `En progreso`, and `Finalizado`.
- A ticket cannot be created for a missing client.
- Invalid ticket statuses are rejected.
- Audit events record `user`, `action`, `ticket_id`, and event timestamp.
- The audit user comes from `X-User`; if it is absent or blank, the user is `system`.
- The frontend must show loading, error, and empty states for customer and ticket lists.

## Data Stores

- PostgreSQL table `clients`: customer records.
- PostgreSQL table `tickets`: support ticket records with a foreign key to `clients`.
- MongoDB collection `audit_events`: ticket lifecycle audit trail.

## Local Verification

```bash
pytest
ruff check backend
pnpm --dir frontend test
pnpm --dir frontend lint
pnpm --dir frontend build
mutmut run
```

## Source Documents

- `README.md`
- `salesforce.md`
- `PRUEBA TECNICA - DESARROLLADOR FINANZ.pdf`

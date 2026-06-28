# Technical Python Project

Full-stack technical test for customer and support ticket management.

## Stack

- Backend: FastAPI, SQLAlchemy 2, PostgreSQL, Alembic, Pytest, Ruff, Mutmut
- Frontend: React, Vite, TypeScript, Vitest
- Audit events: MongoDB
- Local runtime: Docker Compose

## Run With Docker

```bash
docker compose up
```

The services start on:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- MongoDB: localhost:27017

The backend container runs Alembic migrations before starting Uvicorn.

If a local port is already in use, override it before starting Compose:

```bash
BACKEND_PORT=18000 FRONTEND_PORT=15173 VITE_API_BASE_URL=http://localhost:18000 docker compose up
```

## Local Backend Development

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
alembic upgrade head
pytest
ruff check .
mutmut run
```

## Local Frontend Development

```bash
cd frontend
pnpm install
pnpm dev
pnpm test
pnpm lint
pnpm build
```

## API

| Method | Path | Description |
| --- | --- | --- |
| GET | `/health` | Health check |
| POST | `/clients` | Create a client |
| GET | `/clients` | List clients |
| GET | `/clients/{client_id}` | Get a client by ID |
| POST | `/tickets` | Create a ticket for a client |
| GET | `/tickets` | List tickets |
| PATCH | `/tickets/{ticket_id}/status` | Update ticket status |

Ticket statuses are `Pendiente`, `En progreso`, and `Finalizado`.

## Harness SDD

Behavior changes use the local Harness SDD workflow documented in `docs/harness-sdd/README.md`:

```text
spec -> gherkin -> human approval -> TDD -> judge -> mutation testing -> done
```

Gherkin scenarios in `features/` are human-readable contracts. They are not executable Cucumber tests in this version.

## Salesforce Plus

The optional Salesforce integration proposal is in `salesforce.md`.

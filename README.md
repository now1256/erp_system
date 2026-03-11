# Landscaping ERP Starter

3-tier ERP starter for a landscaping company that tracks pesticide, fertilizer, and general material inventory.

## Stack

- Frontend: Next.js, TypeScript, Tailwind CSS
- Backend: FastAPI, SQLAlchemy, Pydantic
- Data: PostgreSQL
- Runtime: Docker Compose

## Domain focus

- Pesticide inventory with EPA registration metadata
- Fertilizer inventory with N-P-K grade and guaranteed analysis
- Warehouse stock balance and movement history
- Supplier/customer records for landscaping operations

## Run

```bash
docker compose up --build
```

App URLs:

- Frontend: http://localhost:3001
- Backend docs: http://localhost:8000/docs

## Structure

```text
frontend/   Next.js presentation layer
backend/    FastAPI application/business layer
db/         PostgreSQL via Docker volume
docs/       Domain notes and references
```

## Initial modules

- Dashboard
- Items
- Inventory balances
- Stock movements
- Partners

## Notes

- The backend seeds demo data on first startup so the dashboard is populated.
- Authentication and approvals are left as the next increment.

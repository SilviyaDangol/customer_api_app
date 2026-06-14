# Customer API App

A FastAPI-based REST API for the ClassicModels database — a sample database for a diecast model car sales company.

## Tech Stack

- **Python 3.11+** with **FastAPI**
- **SQLAlchemy 2.0** ORM
- **PostgreSQL** (sync via psycopg2-binary)
- **Docker** + **Docker Compose**

## Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)

## Environment Setup

Copy the example env file and adjust as needed:

```bash
cp .env.example .env
```

| Variable           | Default       | Description         |
|--------------------|---------------|---------------------|
| `POSTGRES_USER`    | classicmodels | PostgreSQL username |
| `POSTGRES_PASSWORD`| classicmodels | PostgreSQL password |
| `POSTGRES_DB`      | classicmodels | Database name       |
| `POSTGRES_HOST`    | localhost     | Database host       |
| `POSTGRES_PORT`    | 5432          | Database port       |

## Running with Docker

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`. The database is seeded automatically with ClassicModels sample data.

## Running Locally

```bash
uv sync
```

Make sure PostgreSQL is running and the `.env` file is configured, then:

```bash
uvicorn main:app --reload
```

## API Endpoints

### Sync API (`main.py`)

Full CRUD on all entities under their respective prefixes:

| Prefix         | Entity         |
|----------------|----------------|
| `/customers`   | Customers      |
| `/products`    | Products       |
| `/productlines`| Product lines  |
| `/offices`     | Offices        |
| `/employees`   | Employees      |
| `/orders`      | Orders         |
| `/orderdetails`| Order details  |
| `/payments`    | Payments       |
| `/counts`      | Counts         |

### Async Dashboard API (`async_main.py`)

```bash
uvicorn async_main:app --reload
```

Provides concurrent count queries at `/count/overall_counts` and individual `/count/{entity}/count`.

## Project Structure

```
├── app/sql/seed.sql         # ClassicModels seed data
├── config/
│   ├── settings.py          # Pydantic settings (env vars)
│   └── logger.py            # Logging configuration
├── crud/                    # Database query functions
├── db/                      # SQLAlchemy engine setup
├── models/model.py          # ORM models (8 tables)
├── router/                  # Route handlers
├── schemas/                 # Pydantic schemas
├── main.py                  # Sync FastAPI app
├── async_main.py            # Async dashboard app
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## Interactive Docs

Once the app is running, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

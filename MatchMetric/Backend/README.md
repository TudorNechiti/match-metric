Backend Quickstart (FastAPI)
============================

## 1. Environment setup
- Create a virtual environment: `python -m venv .venv`
- Activate (bash): `source .venv/Scripts/activate`
- Install dependencies: `pip install -r requirements.txt`
- Run the API locally: `uvicorn app.main:app --reload`

## 2. Why these tools?
- **FastAPI**: async-first web framework; route decorators map URLs to functions, and Python type hints drive automatic request validation and documentation.
- **Uvicorn**: ASGI server; think of it as the engine that speaks HTTP, manages the event loop, and forwards requests to FastAPI.
- **Pydantic** *(planned)*: schema/validation library that FastAPI leans on. We will define response/request models (like DTOs) so data stays typed and validated automatically.
- **SQLAlchemy** *(planned)*: ORM + SQL toolkit; provides a clean abstraction layer over PostgreSQL, letting us define models, run queries, and manage sessions/transactions without writing raw SQL everywhere.

## 3. Current state
- `app/main.py` exposes a `/health` endpoint returning `{ "status": "ok" }` and demonstrates the FastAPI app factory pattern.
- Dependencies are tracked in `requirements.txt` to keep environments reproducible.

## 4. Next milestone → `/leagues`

### Goal
Expose `GET /leagues` returning `[ { id, name, country, season_year } ]` for available competitions.

### Planned steps
1. **Schema modelling** (Pydantic): design a `League` response model describing the JSON shape.
2. **Data layer** (SQLAlchemy): set up async engine, define tables/models, and create a repository method to fetch leagues + seasons.
3. **Routing** (FastAPI): add a new router module under `app/api/` with `/leagues` handler that calls the repository and returns Pydantic models.
4. **Config**: wire database connection settings via environment variables and dependency injection.
5. **Testing**: aim for either lightweight unit tests with an in-memory DB (e.g., SQLite) or integration tests against a temporary Postgres container.

### Optional interim step
If the database layer is not ready, start with an in-memory list or mock repository so the frontend can integrate early, then swap to SQLAlchemy later.



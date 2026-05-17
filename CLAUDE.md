# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Developer Context

Java Spring background (~2 years), rebuilding Python fluency. Think of FastAPI routes like Spring `@RestController`, SQLAlchemy models like JPA entities, Pydantic schemas like DTOs, and Alembic like Flyway. Use this project to learn — ask Claude to explain Python-specific patterns when they come up.

> `README.md` + `PROJECT-STATUS.md` overlap significantly — consider merging them into a single `DOCS.md` when convenient.

## Project

Football analytics dashboard. Data flows: **StatsBomb JSON → ETL → SQLite/PostgreSQL → FastAPI → (future) Next.js frontend**.

Current state: DB models and API endpoints are done. ETL pipeline (Phase 4) is next.

## Commands

Run from `MatchMetric/Backend/` with venv activated (`source .venv/Scripts/activate`):

```bash
uvicorn app.main:app --reload        # dev server → docs at localhost:8000/docs
alembic upgrade head                 # apply migrations
alembic revision --autogenerate -m "description"   # after model changes
python scripts/populate_db_dummy_data.py
```

## Architecture

```
app/main.py          # app factory, registers routers
app/api/schemas.py   # all Pydantic response models (DTOs)
app/api/routes/      # leagues.py, teams.py — one file per resource
app/db/models.py     # all SQLAlchemy ORM models
app/db/session.py    # engine, get_db() dependency, init_db()/drop_db()
alembic/env.py       # imports all models explicitly — update when adding new ones
data/statsbomb/      # raw JSON source files for ETL
```

**Data model:** `Competition → Season → Match → Shot`, with `Team` and `Player` linked via FKs. Shot coordinates: 105 m × 68 m pitch.

`DATABASE_URL` env var selects the DB; falls back to `matchmetric.db` (SQLite) locally.

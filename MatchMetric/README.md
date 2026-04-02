Football Analytics Dashboard — MatchMetric
=========================================

## Overview
- **Goal**: build a public football analytics hub that highlights team insights with accessible visuals.
- **Learner context**: the project owner is a junior developer (Java background) using this to learn Python ETL, FastAPI, and modern web tooling.
- **Stack**: Python ETL → PostgreSQL (Neon) → FastAPI → Next.js → Vercel, designed for low-cost hosting.

## Why MatchMetric Exists
- Blend a passion for football data with hands-on practice across backend, data engineering, and frontend skills.
- Produce a portfolio-ready application demonstrating ETL pipelines, API design, and interactive data visualisation.
- Prioritise open data sources and transparent processing so others can follow the workflow end-to-end.

## MVP Scope
### User Experience
- Browse available leagues and seasons.
- Open a team page (league + season specific) and view:
  - Shot map on a 105 × 68 m pitch: circle size ≈ xG, fill indicates goals.
  - Key metrics: goals vs xG, shots per 90, shots on target percentage.

### API Requirements
- `GET /leagues` → list competitions and seasons.
- `GET /teams/{team_id}/shots?season_year=YYYY` → shot data points `{x, y, minute, xg, outcome}`.
- `GET /teams/{team_id}/summary?season_year=YYYY` → aggregate stats `{matches, goals, xG}`.
- Provide automatic Swagger docs for fast discovery and testing.

### Data Refresh
- Nightly ETL job (GitHub Actions cron) keeps the dataset current.
- Emphasise idempotent loads so re-runs do not duplicate data.

## Stretch Ideas (Post-MVP)
- Player heatmaps, squad comparison pages, rolling xG trends.
- Extend coverage to Romania’s league (aligns with personal interest).
- Add caching (Upstash Redis) and unit tests once the MVP is stable.

## Non-Functional Requirements
- **Cost**: keep monthly spend between $0–$5 (leveraging free tiers).
- **Performance**: cache frequently requested team endpoints; aim for <500 ms responses when warm.
- **Reliability**: ensure ETL steps are repeatable and safe on failure.
- **Security**: public, read-only API with secrets handled outside the repo.
- **Observability**: basic logs and simple fallback error pages.
- **Portability**: containerised backend with environment-driven configuration.

## Core Technology Stack
- **PostgreSQL (Neon)**: central source of truth for competitions, matches, teams, and shots.
- **Python ETL**: pandas-based scripts to extract, transform, and load data nightly.
- **FastAPI**: async API with SQLAlchemy + Pydantic models for typed responses.
- **Next.js**: renders server components, fetches API data, and draws custom SVG shot maps.
- **Hosting**: Neon (DB) + Cloud Run/Render (API) + Vercel (frontend). Redis caching later if needed.

## Architecture (Lean Setup)
```
ETL (Python) → PostgreSQL → FastAPI → Next.js Frontend
                                 ↘ (future) Redis cache
```

## Data Model Snapshot
- `competitions(id, name, country)`
- `seasons(id, competition_id, year)`
- `teams(id, name, country)`
- `players(id, name, position, team_id)`
- `matches(id, season_id, date, home_team_id, away_team_id, home_goals, away_goals)`
- `shots(id, match_id, team_id, player_id, minute, x, y, body_part, outcome, xg)`
- Recommended indexes: `shots(match_id)`, `shots(team_id)`, `matches(season_id, date)`.
- Use metric pitch coordinates: 105 m length, 68 m width; goal centre at `(105, 34)`.

## ETL Workflow
1. **Extract**: download legal/open datasets (StatsBomb Open Data, Football-Data.co.uk, Understat JSON).
2. **Transform**: normalise IDs, compute extra features (distance/angle to goal, simple logistic xG model).
3. **Load**: upsert into Postgres, deduplicate records, and keep operations idempotent.

## API Surface (MVP)
- `GET /leagues` → `[ { id, name, country, year } ]`
- `GET /teams/{team_id}/shots?season_year=YYYY` → `[ { x, y, minute?, xg?, outcome? } ]`
- `GET /teams/{team_id}/summary?season_year=YYYY` → `{ team_id, season_year, matches, goals_for, goals_against, xg_for, xg_against }`
- Include Pydantic response models, docstrings, and example payloads in Swagger.

## Frontend Goals
- `/?` Select league and season (server-side fetches from FastAPI).
- `/team/[id]` Shot map + KPIs, with a legend and short explanation for each metric.
- Minimal styling; Tailwind CSS optional but not required.

## Data Sources (Open-Friendly First)
- StatsBomb Open Data (selected competitions)
- Football-Data.co.uk (fixtures, results, odds)
- Understat public JSON endpoints (respect robots.txt and limit request load)

## Roadmap & Next Steps
- Finalise the data ingestion pipeline for one league/season.
- Build the FastAPI endpoints with typed responses and documentation.
- Implement the Next.js pages and SVG shot map visuals.
- Add nightly GitHub Actions job for ETL refresh.
- Introduce caching/testing once the MVP flow is dependable.

## Acceptance Criteria
- After running the ETL pipeline, calling `GET /teams/{id}/shots?season_year=YYYY` for at least one team returns a non-empty list of shot events.



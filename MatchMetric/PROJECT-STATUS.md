# MatchMetric - Project Status & Roadmap

**Last Updated:** 2026-01-20

---

## Phase 1: Database Foundation ⏳ IN PROGRESS

**Goal:** Establish the data persistence layer

### Tasks
- [x] Create 6 SQLAlchemy models in `Backend/app/db/models.py`
  - Competition, Season, Team, Player, Match, Shot
  - Relationships, foreign keys, indexes all defined
- [ ] Add helper functions to `Backend/app/db/session.py`
  - `get_db()` for dependency injection
  - `init_db()` and `drop_db()` utilities
- [ ] Initialize Alembic for database migrations
  - Run `alembic init alembic` command
- [ ] Configure Alembic
  - Edit `alembic/env.py` to import models
  - Configure `alembic.ini` for database URL
- [ ] Create first migration
  - Run `alembic revision --autogenerate`
  - Review generated migration script
- [ ] Apply migration to database
  - Run `alembic upgrade head`
  - Verify tables created in SQLite
- [ ] Test the models
  - Write simple test script to insert/query data
  - Verify relationships work correctly

**Learning Outcomes:** ORM concepts, database migrations, relationships, foreign keys

---

## Phase 2: Seed Data (Optional but Recommended) ⏸️ NOT STARTED

**Goal:** Populate database with sample data for testing

### Tasks
- [ ] Create seed script (`Backend/scripts/seed_db.py`)
- [ ] Insert sample competitions (Premier League, La Liga)
- [ ] Insert seasons for each competition
- [ ] Insert sample teams
- [ ] Insert sample players
- [ ] Insert sample matches
- [ ] Insert sample shot events
- [ ] Document how to run seed script

**Learning Outcomes:** SQLAlchemy sessions, bulk inserts, transactions

---

## Phase 3: Update API Endpoints ⏸️ NOT STARTED

**Goal:** Replace mock data with real database queries

### Tasks
- [ ] Update `GET /api/leagues` endpoint
  - Query competitions and seasons from database
  - Return real data instead of hardcoded list
- [ ] Update `GET /api/teams/{team_id}/shots` endpoint
  - Query shots filtered by team_id and season
  - Transform DB records to Pydantic models
- [ ] Update `GET /api/teams/{team_id}/summary` endpoint
  - Aggregate match data for the team
  - Calculate goals_for, goals_against, xG totals
- [ ] Add error handling
  - Handle missing teams/seasons (404)
  - Handle server errors (500)
  - Add validation for query parameters
- [ ] Test all endpoints with real data

**Learning Outcomes:** Database queries, filtering, aggregations, error handling, dependency injection

---

## Phase 4: ETL Pipeline - Data Ingestion ⏸️ NOT STARTED

**Goal:** Build scripts to fetch real football data from external sources

### 4.1 StatsBomb Open Data Integration
- [ ] Set up StatsBomb data source
  - Clone/download StatsBomb open-data repository
  - Understand JSON structure
- [ ] Parse competition files
  - Extract competition metadata
  - Map to Competition model
- [ ] Parse match files
  - Extract match metadata
  - Map to Match model
- [ ] Parse event files for shot data
  - Filter shot events
  - Extract shot details (location, xG, outcome)
  - Map to Shot model

### 4.2 Data Transformation
- [ ] Normalize team/player names
- [ ] Convert coordinates to metric system (105m x 68m)
- [ ] Handle missing xG values
- [ ] Implement deduplication logic
- [ ] Create transformation utilities

### 4.3 Idempotent Loading
- [ ] Implement upsert logic (INSERT ON CONFLICT)
- [ ] Add existence checks before inserting
- [ ] Make scripts safe to re-run
- [ ] Add logging for ETL process
- [ ] Create ETL orchestration script

**Learning Outcomes:** File I/O, JSON parsing, pandas, data transformations, batch processing, upserts

---

## Phase 5: Production Database Setup ⏸️ NOT STARTED

**Goal:** Move from SQLite to PostgreSQL (Neon)

### Tasks
- [ ] Create Neon PostgreSQL account
- [ ] Create production database
- [ ] Get connection string
- [ ] Set up `.env` file for environment variables
- [ ] Test local connection to Neon database
- [ ] Run Alembic migrations on production database
- [ ] Verify tables created in PostgreSQL
- [ ] Run ETL to populate production database
- [ ] Test API with production database

**Learning Outcomes:** Environment configuration, PostgreSQL, cloud databases, connection strings

---

## Phase 6: Deployment - Backend API ⏸️ NOT STARTED

**Goal:** Deploy FastAPI to cloud (Render or Cloud Run)

### Tasks
- [ ] Create `Dockerfile` for FastAPI app
- [ ] Add `.dockerignore` file
- [ ] Test Docker container locally
- [ ] Choose deployment platform (Render/Cloud Run)
- [ ] Create account on chosen platform
- [ ] Configure deployment settings
- [ ] Set environment variables in cloud
- [ ] Deploy backend to cloud
- [ ] Test API endpoints from cloud URL
- [ ] Set up health check monitoring

**Learning Outcomes:** Docker, containerization, cloud deployment, environment management

---

## Phase 7: Frontend - Next.js Setup ⏸️ NOT STARTED

**Goal:** Initialize frontend application

### Tasks
- [ ] Initialize Next.js project with TypeScript
  - Run `npx create-next-app@latest`
  - Choose TypeScript, App Router, ESLint
- [ ] Install additional dependencies
  - Tailwind CSS (optional)
  - Any charting/visualization libraries
- [ ] Create basic layout structure
- [ ] Set up navigation components
- [ ] Create API client utilities
- [ ] Configure environment variables for API URL
- [ ] Test local development server

**Learning Outcomes:** Next.js, TypeScript, project initialization, environment config

---

## Phase 8: Frontend - Home Page ⏸️ NOT STARTED

**Goal:** Build league/season selector

### Tasks
- [ ] Create home page (`app/page.tsx`)
- [ ] Fetch leagues from API (`GET /api/leagues`)
- [ ] Display league cards or list
- [ ] Implement loading states
- [ ] Implement error handling
- [ ] Add navigation to team pages
- [ ] Style the page (Tailwind or CSS)
- [ ] Test responsive design

**Learning Outcomes:** React components, data fetching, state management, routing

---

## Phase 9: Frontend - Team Page ⏸️ NOT STARTED

**Goal:** Build team detail page with shot map

### Tasks
- [ ] Create dynamic route (`app/team/[id]/page.tsx`)
- [ ] Fetch team shots from API
- [ ] Fetch team summary from API
- [ ] Build SVG shot map component
  - Draw pitch outline (105m x 68m)
  - Plot shot circles at correct positions
  - Size circles by xG value
  - Color circles by outcome (goal vs miss)
  - Add goal posts and penalty box
- [ ] Display KPI cards
  - Goals vs xG comparison
  - Shots per 90 minutes
  - Shots on target percentage
- [ ] Add legend explaining metrics
- [ ] Style the page
- [ ] Test with different teams

**Learning Outcomes:** Dynamic routing, SVG drawing, data visualization, CSS styling

---

## Phase 10: Automation - Nightly ETL Job ⏸️ NOT STARTED

**Goal:** Keep data fresh automatically

### Tasks
- [ ] Create GitHub Actions workflow file
- [ ] Configure cron schedule (e.g., daily at 3 AM)
- [ ] Set up secrets in GitHub
- [ ] Configure ETL script to run in CI
- [ ] Add error notifications (email/Slack)
- [ ] Test workflow manually
- [ ] Monitor first automated runs
- [ ] Document the automation process

**Learning Outcomes:** CI/CD, GitHub Actions, cron jobs, automation

---

## Phase 11: Enhancements (Post-MVP) ⏸️ NOT STARTED

**Optional improvements for future iterations**

### Caching
- [ ] Set up Upstash Redis account
- [ ] Implement caching layer for API
- [ ] Add cache invalidation logic
- [ ] Monitor cache hit rates

### Advanced Features
- [ ] Player heatmaps
- [ ] Squad comparison pages
- [ ] Rolling xG trends over time
- [ ] League tables
- [ ] Head-to-head comparisons
- [ ] Advanced filters and search

### Testing
- [ ] Backend unit tests
- [ ] API integration tests
- [ ] Frontend component tests
- [ ] E2E tests with Playwright/Cypress

### Performance & Monitoring
- [ ] Add API response caching
- [ ] Database query optimization
- [ ] Set up monitoring/logging (Sentry, LogRocket)
- [ ] Performance profiling
- [ ] Bundle size optimization

### Additional Leagues
- [ ] Add Romania's Liga 1 data
- [ ] Add more European leagues
- [ ] Support multiple seasons per league

---

## Phase 12: AI Integration - MCP Server ⏸️ NOT STARTED

**Goal:** Build a Model Context Protocol (MCP) server to enable AI-powered natural language queries over football data

### What is MCP?
MCP (Model Context Protocol) is Anthropic's open standard that allows AI assistants like Claude to securely connect to external data sources and tools. It creates a bridge between Claude and your application's database.

### Tasks
- [ ] Install MCP Python SDK (`pip install mcp`)
- [ ] Create MCP server structure (`Backend/mcp_server/`)
- [ ] Implement database query tools
  - `get_team_shots` - Retrieve shots for a specific team
  - `get_player_stats` - Get player statistics (goals, xG, etc.)
  - `get_match_details` - Fetch match information with shots
  - `compare_teams` - Compare two teams' performance
  - `get_league_standings` - Calculate league table from match results
- [ ] Implement resources
  - Expose competitions list
  - Expose teams list
  - Expose players list
- [ ] Add authentication and rate limiting
- [ ] Test MCP server with Claude Desktop
- [ ] Document MCP server setup and available tools
- [ ] Deploy MCP server (optional)

### Example Use Cases
Once built, users could ask Claude:
- "What's Arsenal's xG in their last 5 matches?"
- "Compare Haaland and Salah's shot efficiency this season"
- "Which team overperforms their xG the most?"
- "Show me Real Madrid's shots from the Barcelona match"

### Learning Outcomes
- MCP protocol and SDK usage
- Designing AI-friendly tool APIs
- Async Python programming
- Security for AI system integrations
- Prompt engineering for structured data

### Prerequisites
- Complete Phase 3 (API endpoints working)
- Database populated with real data
- Understanding of async/await in Python

**Note:** This is an advanced feature for learning modern AI integration patterns. Build this after the core application is functional.

---

## Current Status Summary

**Phase Completed:** 0 / 11
**Current Phase:** Phase 1 - Database Foundation
**Current Task:** Add helper functions to session.py
**Blockers:** None
**Next Milestone:** Complete Phase 1 and test database models

---

## Quick Commands Reference

### Backend Development
```bash
# Activate virtual environment
cd Backend
source .venv/Scripts/activate  # Windows Git Bash
# or
.venv\Scripts\activate  # Windows CMD

# Run FastAPI server
uvicorn app.main:app --reload

# Run Alembic migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"
```

### Frontend Development (when ready)
```bash
cd Frontend
npm run dev           # Start dev server
npm run build         # Build for production
npm run lint          # Run linter
```

---

## Notes & Decisions

- **Database:** SQLite for development, PostgreSQL (Neon) for production
- **Deployment:** Backend on Render/Cloud Run, Frontend on Vercel
- **Data Source:** Starting with StatsBomb Open Data
- **Styling:** Tailwind CSS optional, minimal styling initially
- **Testing:** Post-MVP, focus on getting MVP working first

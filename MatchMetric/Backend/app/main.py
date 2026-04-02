"""Application entry point for the FastAPI backend."""

from fastapi import FastAPI

from app.api.routes import leagues, teams

def create_app() -> FastAPI:
    """Construct and configure the FastAPI application instance."""
    app = FastAPI(title="MatchMetric API", version="0.1.0")

    app.include_router(leagues.router, prefix="/api")
    app.include_router(teams.router, prefix="/api")

    register_health_endpoint(app)

    return app


def register_health_endpoint(app: FastAPI) -> None:
    """Expose a lightweight liveness probe used for quick smoke tests.

    Keeping this in a helper function sets the pattern for modular route
    registration as the API surface grows (e.g. /leagues, /teams, etc.).
    """

    @app.get("/health", tags=["Health"], summary="Service heartbeat")
    async def healthcheck() -> dict[str, str]:
        """Return a simple status payload to confirm the service is running."""

        return {"status": "ok"}


app = create_app()


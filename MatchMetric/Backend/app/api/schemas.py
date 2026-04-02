"""Pydantic models representing API response payloads."""

from pydantic import BaseModel, Field


class LeagueResponse(BaseModel):
    """Surface-level view of a competition for the `/leagues` endpoint."""

    id: int = Field(..., description="Unique identifier for the league/competition")
    name: str = Field(..., description="Competition display name")
    country: str = Field(..., description="Country or association the league belongs to")
    season_year: int = Field(..., description="Season year associated with this entry")


class LeagueListResponse(BaseModel):
    """Wrapper around multiple league summaries for consistent API structure."""

    leagues: list[LeagueResponse] = Field(
        default_factory=list,
        description="Collection of leagues with the latest known season",
    )


class ShotEventResponse(BaseModel):
    """Single shot event used for visualisations and per-match analysis."""

    x: float = Field(..., description="Shot location on pitch X-axis (0-105m)")
    y: float = Field(..., description="Shot location on pitch Y-axis (0-68m)")
    minute: int = Field(..., description="Match minute when the shot occurred")
    xg: float = Field(..., description="Expected goals value for the attempt")
    outcome: str = Field(..., description="Shot outcome such as goal, saved, missed")


class TeamShotsResponse(BaseModel):
    """Grouped collection of shot events for a single team and season."""

    team_id: int = Field(..., description="Identifier of the team these shots belong to")
    season_year: int = Field(..., description="Season context for the shot list")
    shots: list[ShotEventResponse] = Field(default_factory=list, description="Shot timeline")


class TeamSummaryResponse(BaseModel):
    """Aggregated team metrics used for quick comparison dashboards."""

    team_id: int = Field(..., description="Identifier of the team")
    season_year: int = Field(..., description="Season context for the summary")
    matches: int = Field(..., description="Total matches played in the season")
    goals_for: int = Field(..., description="Goals scored by the team")
    goals_against: int = Field(..., description="Goals conceded by the team")
    xg_for: float = Field(..., description="Cumulative expected goals for the team")
    xg_against: float = Field(..., description="Cumulative expected goals against the team")

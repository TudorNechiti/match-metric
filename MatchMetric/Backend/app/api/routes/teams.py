from fastapi import APIRouter, Query, Depends

from app.api.schemas import (
    ShotEventResponse,
    TeamShotsResponse,
    TeamSummaryResponse,
)

from app.db.models import Shot, Match, Season

from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.get(
    "/{team_id}/shots",
    response_model=TeamShotsResponse,
    summary="Get individual shots for a team and season",
)
async def get_team_shots(
    team_id: int,
    season_year: int = Query(..., description="Season year to scope the shot data"),
    db: Session = Depends(get_db),
) -> TeamShotsResponse:
    """Return placeholder shot events until the ETL pipeline is connected."""

    shots = (
        db.query(Shot)
        .join(Match, Shot.match_id == Match.id)
        .join(Season, Match.season_id == Season.id)
        .filter(Shot.team_id == team_id)
        .filter(Season.year == season_year)
        .all()
    )

    shot_responses = [
        ShotEventResponse(
            x=shot.x, y=shot.y, minute=shot.minute, xg=shot.xg, outcome=shot.outcome
        )
        for shot in shots
    ]

    return TeamShotsResponse(
        team_id=team_id, season_year=season_year, shots=shot_responses
    )


@router.get(
    "/{team_id}/summary",
    response_model=TeamSummaryResponse,
    summary="Get aggregate team metrics for a season",
)
async def get_team_summary(
    team_id: int,
    season_year: int = Query(..., description="Season year to scope the summary"),
    db: Session = Depends(get_db),
) -> TeamSummaryResponse:
    """Return placeholder aggregate stats for the given team and season."""

    matches = (
        db.query(Match)
        .join(Season, Match.season_id == Season.id)
        .filter(Season.year == season_year)
        .filter((Match.home_team_id == team_id) | (Match.away_team_id == team_id))
        .all()
    )

    shots = (
        db.query(Shot)
        .join(Match, Match.id == Shot.match_id)
        .join(Season, Match.season_id == Season.id)
        .filter(Shot.team_id == team_id)
        .filter(Season.year == season_year)
        .all()
    )

    shots_against = (
        db.query(Shot)
        .join(Match, Shot.match_id == Match.id)
        .join(Season, Match.season_id == Season.id)
        .filter(Shot.team_id != team_id)
        .filter(Season.year == season_year)
        .filter((Match.home_team_id == team_id) | (Match.away_team_id == team_id))
        .all()
    )

    goals_for = 0
    goals_against = 0
    for match in matches:
        if match.home_team_id == team_id:
            goals_for += match.home_goals or 0
            goals_against += match.away_goals or 0
        else:
            goals_for += match.away_goals or 0
            goals_against += match.home_goals or 0

    return TeamSummaryResponse(
        team_id=team_id,
        season_year=season_year,
        matches=len(matches),
        goals_for=goals_for,
        goals_against=goals_against,
        xg_for=round(sum(s.xg for s in shots), 2),
        xg_against=round(sum(s.xg for s in shots_against), 2),
    )

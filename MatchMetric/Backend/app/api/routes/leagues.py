from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.db.models import Competition
from app.api.schemas import LeagueListResponse, LeagueResponse

router = APIRouter(prefix="/leagues", tags=["Leagues"])

@router.get("/", response_model=LeagueListResponse, summary="Get all leagues")
async def get_leagues(db: Session = Depends(get_db)) -> LeagueListResponse:

    competitions = db.query(Competition).all()
    leagues = []
    
    for comp in competitions:
        latest_season_year = max([s.year for s in comp.seasons]) if comp.seasons else None
        
        if latest_season_year:
            league_response = LeagueResponse(
                id=comp.id,
                name=comp.name,
                country=comp.country,
                season_year=latest_season_year
            )
            leagues.append(league_response)
    
    return LeagueListResponse(leagues=leagues)
    

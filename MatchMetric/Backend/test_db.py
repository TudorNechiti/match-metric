"""Quick test to verify database models work."""

from datetime import date
from app.db.session import SessionLocal
from app.db.models import Competition, Season, Team, Player, Match, Shot

# Create a session
session = SessionLocal()

try:
    # Create a competition
    premier_league = Competition(name="Premier League", country="England")
    session.add(premier_league)
    session.commit()
    print(f"[OK] Created: {premier_league}")

    # Create a season
    season_2024 = Season(year=2024, competition=premier_league)
    session.add(season_2024)
    session.commit()
    print(f"[OK] Created: {season_2024}")

    # Create a team
    arsenal = Team(name="Arsenal FC", country="England")
    session.add(arsenal)
    session.commit()
    print(f"[OK] Created: {arsenal}")

    # Query them back
    print("\n--- Querying Database ---")
    competitions = session.query(Competition).all()
    print(f"Competitions: {competitions}")

    print(f"Premier League seasons: {premier_league.seasons}")

    print("\n[OK] Database is working perfectly!")

finally:
    session.close()

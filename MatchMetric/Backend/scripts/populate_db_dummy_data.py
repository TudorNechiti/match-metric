"""Seed script to populate the database with sample football data."""

import sys
from pathlib import Path
from datetime import date

# Add Backend directory to Python path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import SessionLocal
from app.db.models import Competition, Season, Team, Player, Match, Shot


def seed_database():
    """Populate database with sample data."""
    session = SessionLocal()

    try:
        print("=" * 60)
        print("SEEDING DATABASE WITH SAMPLE DATA")
        print("=" * 60)

        # 1. Create Competitions
        print("\n[1/7] Creating competitions...")
        premier_league = Competition(name="Premier League", country="England")
        la_liga = Competition(name="La Liga", country="Spain")
        session.add_all([premier_league, la_liga])
        session.commit()
        print(f"  - Created: {premier_league}")
        print(f"  - Created: {la_liga}")

        # 2. Create Seasons
        print("\n[2/7] Creating seasons...")
        pl_2023 = Season(year=2023, competition=premier_league)
        pl_2024 = Season(year=2024, competition=premier_league)
        liga_2023 = Season(year=2023, competition=la_liga)
        liga_2024 = Season(year=2024, competition=la_liga)
        session.add_all([pl_2023, pl_2024, liga_2023, liga_2024])
        session.commit()
        print(f"  - Created 4 seasons for Premier League and La Liga")

        # 3. Create Teams
        print("\n[3/7] Creating teams...")
        # Premier League teams
        arsenal = Team(name="Arsenal FC", country="England")
        man_city = Team(name="Manchester City", country="England")
        liverpool = Team(name="Liverpool FC", country="England")
        chelsea = Team(name="Chelsea FC", country="England")

        # La Liga teams
        real_madrid = Team(name="Real Madrid", country="Spain")
        barcelona = Team(name="FC Barcelona", country="Spain")
        atletico = Team(name="Atletico Madrid", country="Spain")
        sevilla = Team(name="Sevilla FC", country="Spain")

        teams = [arsenal, man_city, liverpool, chelsea, real_madrid, barcelona, atletico, sevilla]
        session.add_all(teams)
        session.commit()
        print(f"  - Created {len(teams)} teams")

        # 4. Create Players
        print("\n[4/7] Creating players...")
        players = [
            # Arsenal
            Player(name="Bukayo Saka", position="Forward", team=arsenal),
            Player(name="Martin Odegaard", position="Midfielder", team=arsenal),
            Player(name="Gabriel Jesus", position="Forward", team=arsenal),

            # Man City
            Player(name="Erling Haaland", position="Forward", team=man_city),
            Player(name="Kevin De Bruyne", position="Midfielder", team=man_city),
            Player(name="Phil Foden", position="Midfielder", team=man_city),

            # Liverpool
            Player(name="Mohamed Salah", position="Forward", team=liverpool),
            Player(name="Darwin Nunez", position="Forward", team=liverpool),
            Player(name="Luis Diaz", position="Forward", team=liverpool),

            # Real Madrid
            Player(name="Vinicius Junior", position="Forward", team=real_madrid),
            Player(name="Jude Bellingham", position="Midfielder", team=real_madrid),
            Player(name="Rodrygo", position="Forward", team=real_madrid),

            # Barcelona
            Player(name="Robert Lewandowski", position="Forward", team=barcelona),
            Player(name="Raphinha", position="Forward", team=barcelona),
            Player(name="Gavi", position="Midfielder", team=barcelona),
        ]
        session.add_all(players)
        session.commit()
        print(f"  - Created {len(players)} players")

        # 5. Create Matches
        print("\n[5/7] Creating matches...")
        matches = [
            # Premier League 2024
            Match(
                season=pl_2024,
                date=date(2024, 1, 15),
                home_team=arsenal,
                away_team=man_city,
                home_goals=2,
                away_goals=1
            ),
            Match(
                season=pl_2024,
                date=date(2024, 1, 20),
                home_team=liverpool,
                away_team=chelsea,
                home_goals=3,
                away_goals=2
            ),
            # La Liga 2024
            Match(
                season=liga_2024,
                date=date(2024, 1, 18),
                home_team=real_madrid,
                away_team=barcelona,
                home_goals=2,
                away_goals=2
            ),
        ]
        session.add_all(matches)
        session.commit()
        print(f"  - Created {len(matches)} matches")

        # 6. Create Shot Events
        print("\n[6/7] Creating shot events...")
        shots = [
            # Arsenal vs Man City - Arsenal shots
            Shot(
                match=matches[0],
                team=arsenal,
                player=players[0],  # Saka
                minute=25,
                x=95.0,
                y=35.0,
                body_part="Right Foot",
                outcome="goal",
                xg=0.45
            ),
            Shot(
                match=matches[0],
                team=arsenal,
                player=players[2],  # Jesus
                minute=67,
                x=88.0,
                y=40.0,
                body_part="Left Foot",
                outcome="goal",
                xg=0.32
            ),
            Shot(
                match=matches[0],
                team=arsenal,
                player=players[1],  # Odegaard
                minute=52,
                x=78.0,
                y=34.0,
                body_part="Left Foot",
                outcome="saved",
                xg=0.15
            ),
            # Arsenal vs Man City - Man City shots
            Shot(
                match=matches[0],
                team=man_city,
                player=players[3],  # Haaland
                minute=42,
                x=92.0,
                y=34.0,
                body_part="Right Foot",
                outcome="goal",
                xg=0.65
            ),
            Shot(
                match=matches[0],
                team=man_city,
                player=players[4],  # De Bruyne
                minute=80,
                x=85.0,
                y=30.0,
                body_part="Right Foot",
                outcome="missed",
                xg=0.22
            ),
            # Real Madrid vs Barcelona shots
            Shot(
                match=matches[2],
                team=real_madrid,
                player=players[9],  # Vinicius
                minute=15,
                x=98.0,
                y=32.0,
                body_part="Right Foot",
                outcome="goal",
                xg=0.58
            ),
            Shot(
                match=matches[2],
                team=barcelona,
                player=players[12],  # Lewandowski
                minute=55,
                x=94.0,
                y=34.0,
                body_part="Right Foot",
                outcome="goal",
                xg=0.72
            ),
        ]
        session.add_all(shots)
        session.commit()
        print(f"  - Created {len(shots)} shot events")

        # 7. Verify Data
        print("\n[7/7] Verifying seeded data...")
        comp_count = session.query(Competition).count()
        season_count = session.query(Season).count()
        team_count = session.query(Team).count()
        player_count = session.query(Player).count()
        match_count = session.query(Match).count()
        shot_count = session.query(Shot).count()

        print(f"  - Competitions: {comp_count}")
        print(f"  - Seasons: {season_count}")
        print(f"  - Teams: {team_count}")
        print(f"  - Players: {player_count}")
        print(f"  - Matches: {match_count}")
        print(f"  - Shots: {shot_count}")

        print("\n" + "=" * 60)
        print("[OK] DATABASE SEEDED SUCCESSFULLY!")
        print("=" * 60)

    except Exception as e:
        session.rollback()
        print(f"\n[ERROR] Failed to seed database: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_database()

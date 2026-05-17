"""ETL script: loads StatsBomb open data JSON files into the database."""

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.models import Competition, Match, Player, Season, Shot, Team
from app.db.session import SessionLocal, init_db

DATA_DIR = Path(__file__).parent.parent / "data" / "statsbomb"
MATCHES_DIR = DATA_DIR / "matches"
EVENTS_DIR = DATA_DIR / "event"


def get_or_create(session, model, lookup: dict, defaults: dict = {}):
    """Fetch a row matching `lookup`, or insert it with `lookup + defaults`.

    Equivalent pattern to Spring's findById(...).orElseGet(() -> repo.save(...)).
    Returns (instance, created: bool).
    """
    instance = session.query(model).filter_by(**lookup).first()
    if instance:
        return instance, False
    instance = model(**lookup, **defaults)
    session.add(instance)
    session.flush()
    return instance, True


def _parse_season_year(season_name: str) -> int:
    """'2017/2018' → 2017"""
    return int(season_name.split("/")[0])


def load_matches(session) -> list[dict]:
    """Parse all matches JSON files and upsert competitions, seasons, teams, matches."""
    loaded = []

    for match_file in MATCHES_DIR.glob("*.json"):
        matches = json.loads(match_file.read_text(encoding="utf-8"))

        for m in matches:
            competition, _ = get_or_create(
                session,
                Competition,
                lookup={"id": m["competition"]["competition_id"]},
                defaults={
                    "name": m["competition"]["competition_name"],
                    "country": m["competition"]["country_name"],
                },
            )

            season, _ = get_or_create(
                session,
                Season,
                lookup={
                    "competition_id": competition.id,
                    "year": _parse_season_year(m["season"]["season_name"]),
                },
            )

            home_team, _ = get_or_create(
                session,
                Team,
                lookup={"id": m["home_team"]["home_team_id"]},
                defaults={
                    "name": m["home_team"]["home_team_name"],
                    "country": m["home_team"]["country"]["name"],
                },
            )

            away_team, _ = get_or_create(
                session,
                Team,
                lookup={"id": m["away_team"]["away_team_id"]},
                defaults={
                    "name": m["away_team"]["away_team_name"],
                    "country": m["away_team"]["country"]["name"],
                },
            )

            match, _ = get_or_create(
                session,
                Match,
                lookup={"id": m["match_id"]},
                defaults={
                    "season_id": season.id,
                    "date": date.fromisoformat(m["match_date"]),
                    "home_team_id": home_team.id,
                    "away_team_id": away_team.id,
                    "home_goals": m.get("home_score"),
                    "away_goals": m.get("away_score"),
                },
            )

            loaded.append({"match_id": m["match_id"], "db_match": match})

    session.commit()
    return loaded


def extract_shot_data(event: dict) -> dict | None:
    """Transform a raw StatsBomb shot event into a dict ready for DB insertion.

    TODO(human): implement this function.

    The event dict looks like:
        {
            "minute": 9,
            "team": {"id": 169, "name": "Bayern Munich"},
            "location": [114.0, 48.0],        # StatsBomb pitch: 120 x 80m
            "shot": {
                "statsbomb_xg": 0.18,
                "outcome": {"name": "Off T"},
                "body_part": {"name": "Right Foot"},
            }
        }

    Return a dict with keys: team_id, minute, x, y, xg, outcome, body_part.
    Rescale coordinates from StatsBomb (120x80) to metric pitch (105x68):
        x = location[0] * (105 / 120)
        y = location[1] * (68 / 80)
    Return None to skip the event if any required field is missing.
    """
    pass


def load_shots(session, matches: list[dict]) -> None:
    """For each match, load its event file and insert shot events."""
    for entry in matches:
        match_id = entry["match_id"]
        db_match = entry["db_match"]

        event_file = EVENTS_DIR / f"{match_id}.json"
        if not event_file.exists():
            print(f"  [skip] no event file for match {match_id}")
            continue

        events = json.loads(event_file.read_text(encoding="utf-8"))
        shot_events = [e for e in events if e["type"]["name"] == "Shot"]

        for event in shot_events:
            shot_data = extract_shot_data(event)
            if shot_data is None:
                continue

            player, _ = get_or_create(
                session,
                Player,
                lookup={"id": event["player"]["id"]},
                defaults={
                    "name": event["player"]["name"],
                    "position": event.get("position", {}).get("name"),
                    "team_id": event["team"]["id"],
                },
            )

            already_exists = session.query(Shot).filter_by(
                match_id=db_match.id,
                player_id=player.id,
                minute=shot_data["minute"],
            ).first()

            if not already_exists:
                session.add(Shot(match_id=db_match.id, player_id=player.id, **shot_data))

        session.commit()
        print(f"  [ok] match {match_id} — {len(shot_events)} shots")


def run() -> None:
    init_db()
    session = SessionLocal()
    try:
        print("--- Loading matches ---")
        matches = load_matches(session)
        print(f"    {len(matches)} matches processed\n")

        print("--- Loading shots ---")
        load_shots(session, matches)

        print("\nETL complete.")
    except Exception as e:
        session.rollback()
        print(f"[ERROR] {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    run()

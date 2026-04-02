"""SQLAlchemy ORM models for the MatchMetric database schema."""

from datetime import date as Date
from typing import Optional

from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Competition(Base):
    """Represents a football league or tournament (e.g., Premier League, La Liga)."""

    __tablename__ = "competitions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)

    # Relationships
    seasons: Mapped[list["Season"]] = relationship(
        back_populates="competition",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Competition(id={self.id}, name='{self.name}', country='{self.country}')>"


class Season(Base):
    """Represents a specific season within a competition (e.g., Premier League 2024)."""

    __tablename__ = "seasons"

    id: Mapped[int] = mapped_column(primary_key=True)
    competition_id: Mapped[int] = mapped_column(ForeignKey("competitions.id"), nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)

    # Relationships
    competition: Mapped["Competition"] = relationship(back_populates="seasons")
    matches: Mapped[list["Match"]] = relationship(
        back_populates="season",
        cascade="all, delete-orphan",
    )

    # Constraints
    __table_args__ = (
        UniqueConstraint("competition_id", "year", name="uq_competition_year"),
    )

    def __repr__(self) -> str:
        return f"<Season(id={self.id}, competition_id={self.competition_id}, year={self.year})>"


class Team(Base):
    """Represents a football team (e.g., Arsenal FC, Real Madrid)."""

    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)

    # Relationships
    players: Mapped[list["Player"]] = relationship(
        back_populates="team",
        cascade="all, delete-orphan",
    )
    home_matches: Mapped[list["Match"]] = relationship(
        foreign_keys="Match.home_team_id",
        back_populates="home_team",
    )
    away_matches: Mapped[list["Match"]] = relationship(
        foreign_keys="Match.away_team_id",
        back_populates="away_team",
    )
    shots: Mapped[list["Shot"]] = relationship(back_populates="team")

    def __repr__(self) -> str:
        return f"<Team(id={self.id}, name='{self.name}', country='{self.country}')>"


class Player(Base):
    """Represents an individual player belonging to a team."""

    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    position: Mapped[Optional[str]] = mapped_column(nullable=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)

    # Relationships
    team: Mapped["Team"] = relationship(back_populates="players")
    shots: Mapped[list["Shot"]] = relationship(back_populates="player")

    def __repr__(self) -> str:
        return f"<Player(id={self.id}, name='{self.name}', position='{self.position}', team_id={self.team_id})>"


class Match(Base):
    """Represents a football match between two teams in a season."""

    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id"), nullable=False)
    date: Mapped[Date] = mapped_column(nullable=False)
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    home_goals: Mapped[Optional[int]] = mapped_column(nullable=True)
    away_goals: Mapped[Optional[int]] = mapped_column(nullable=True)

    # Relationships
    season: Mapped["Season"] = relationship(back_populates="matches")
    home_team: Mapped["Team"] = relationship(
        foreign_keys=[home_team_id],
        back_populates="home_matches",
    )
    away_team: Mapped["Team"] = relationship(
        foreign_keys=[away_team_id],
        back_populates="away_matches",
    )
    shots: Mapped[list["Shot"]] = relationship(
        back_populates="match",
        cascade="all, delete-orphan",
    )

   
class Shot(Base):
    """Represents an individual shot event during a match."""

    __tablename__ = "shots"

    id: Mapped[int] = mapped_column(primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"), nullable=False)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    player_id: Mapped[Optional[int]] = mapped_column(ForeignKey("players.id"), nullable=True)
    minute: Mapped[int] = mapped_column(nullable=False)
    x: Mapped[float] = mapped_column(nullable=False)
    y: Mapped[float] = mapped_column(nullable=False)
    body_part: Mapped[Optional[str]] = mapped_column(nullable=True)
    outcome: Mapped[str] = mapped_column(nullable=False)
    xg: Mapped[float] = mapped_column(nullable=False)

    # Relationships
    match: Mapped["Match"] = relationship(back_populates="shots")
    team: Mapped["Team"] = relationship(back_populates="shots")
    player: Mapped[Optional["Player"]] = relationship(back_populates="shots")

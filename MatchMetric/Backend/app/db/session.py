import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

class Base(DeclarativeBase):
    pass

def __build_database_url() -> str:
    env_url = os.getenv("DATABASE_URL")
    if env_url:
        return env_url

    sqlite_path = os.path.join(os.path.dirname(__file__), "..", "..", "matchmetric.db")
    return f"sqlite:///{os.path.abspath(sqlite_path)}"

DATABASE_URL = __build_database_url()

engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)

# Create a session factory
SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """Dependency injection helper for FastAPI routes.

    Yields a database session and ensures it's closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create all database tables based on SQLAlchemy models.

    This uses Base.metadata.create_all() which is idempotent - it won't
    recreate tables that already exist. Safe to call multiple times.
    """
    Base.metadata.create_all(bind=engine)
    print(f"✓ Database initialized at: {DATABASE_URL}")


def drop_db() -> None:
    """Drop all database tables. USE WITH CAUTION - destroys all data!

    Useful for development/testing when you need a fresh start.
    """
    Base.metadata.drop_all(bind=engine)
    print(f"✓ All tables dropped from: {DATABASE_URL}")

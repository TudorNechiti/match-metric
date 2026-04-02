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
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        


from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# Ensure the database directory exists (db/notes.db relative to container root)
BASE_DIR = Path(__file__).resolve().parents[2]  # .../notes_backend
DB_DIR = BASE_DIR / "db"
DB_DIR.mkdir(parents=True, exist_ok=True)
SQLITE_URL = f"sqlite:///{DB_DIR / 'notes.db'}"

# Create SQLAlchemy engine and session factory
# check_same_thread False allows use across threads typical for FastAPI workers
engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """
    Context manager to provide a SQLAlchemy session.

    Yields:
        Session: SQLAlchemy session with commit/rollback handling.
    """
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

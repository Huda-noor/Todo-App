"""Database connection and session management."""
from sqlmodel import SQLModel, Session, create_engine
from typing import Generator

from app.config import get_settings

# Create database engine
settings = get_settings()
engine = create_engine(
    settings.database_url,
    echo=False,  # Set to True for SQL logging during development
    pool_pre_ping=True,  # Verify connections before use
)


def create_db_and_tables():
    """Create all database tables (for development only)."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency that provides a database session."""
    with Session(engine) as session:
        yield session

"""Todo model - Full CRUD, managed by FastAPI."""
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime, timezone
from uuid import UUID, uuid4


class Todo(SQLModel, table=True):
    """
    Todo table - managed by FastAPI.

    Stores user todo items with user-scoped access.
    Each todo belongs to exactly one user.

    Note: Stored in the public schema, but references neon_auth.user for user_id.
    """
    __tablename__ = "todo"
    __table_args__ = {"schema": "public"}

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(sa_column=Column("user_id", PG_UUID(as_uuid=True), ForeignKey("neon_auth.user.id"), nullable=False, index=True))
    description: str = Field(min_length=1, max_length=500)
    is_complete: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

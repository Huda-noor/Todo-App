"""User model - Read-only, managed by Neon Auth (Better Auth)."""
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime
from typing import Optional
import uuid


class User(SQLModel, table=True):
    """
    Neon Auth user table - READ ONLY.

    This table is managed by Neon Auth (Better Auth). FastAPI only reads from it
    for user information display and session validation.

    Schema: neon_auth
    Note: Column names use camelCase to match Neon Auth conventions.
    """
    __tablename__ = "user"
    __table_args__ = {"schema": "neon_auth"}

    id: uuid.UUID = Field(sa_column=Column("id", PG_UUID(as_uuid=True), primary_key=True))
    name: str = Field(sa_column=Column("name", String, nullable=False))
    email: str = Field(sa_column=Column("email", String, nullable=False, unique=True, index=True))
    email_verified: bool = Field(sa_column=Column("emailVerified", Boolean, nullable=False, default=False))
    image: Optional[str] = Field(sa_column=Column("image", String, nullable=True), default=None)
    created_at: datetime = Field(sa_column=Column("createdAt", DateTime(timezone=True), nullable=False))
    updated_at: datetime = Field(sa_column=Column("updatedAt", DateTime(timezone=True), nullable=False))

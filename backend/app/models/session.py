"""Session model - Read-only, managed by Neon Auth (Better Auth)."""
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime
from typing import Optional
import uuid


class Session(SQLModel, table=True):
    """
    Neon Auth session table - READ ONLY.

    This table is managed by Neon Auth (Better Auth). FastAPI reads from it
    to validate session tokens from cookies.

    Schema: neon_auth
    Note: Column names use camelCase to match Neon Auth conventions.
    """
    __tablename__ = "session"
    __table_args__ = {"schema": "neon_auth"}

    id: uuid.UUID = Field(sa_column=Column("id", PG_UUID(as_uuid=True), primary_key=True))
    token: str = Field(sa_column=Column("token", String, nullable=False, unique=True, index=True))
    user_id: uuid.UUID = Field(sa_column=Column("userId", PG_UUID(as_uuid=True), ForeignKey("neon_auth.user.id"), nullable=False))
    expires_at: datetime = Field(sa_column=Column("expiresAt", DateTime(timezone=True), nullable=False))
    ip_address: Optional[str] = Field(sa_column=Column("ipAddress", String, nullable=True), default=None)
    user_agent: Optional[str] = Field(sa_column=Column("userAgent", String, nullable=True), default=None)
    created_at: datetime = Field(sa_column=Column("createdAt", DateTime(timezone=True), nullable=False))
    updated_at: datetime = Field(sa_column=Column("updatedAt", DateTime(timezone=True), nullable=False))

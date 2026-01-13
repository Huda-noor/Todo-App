"""User schemas for API responses."""
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional


class UserResponse(BaseModel):
    """Response schema for user information."""
    id: UUID
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

"""Todo schemas for API requests and responses."""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from uuid import UUID


class CreateTodoRequest(BaseModel):
    """Request schema for creating a todo."""
    description: str = Field(..., min_length=1, max_length=500)

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Todo description cannot be empty")
        return v.strip()


class UpdateTodoRequest(BaseModel):
    """Request schema for updating a todo."""
    description: str = Field(..., min_length=1, max_length=500)

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Todo description cannot be empty")
        return v.strip()


class TodoResponse(BaseModel):
    """Response schema for a todo."""
    id: UUID
    description: str
    is_complete: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TodoListResponse(BaseModel):
    """Response schema for listing todos."""
    todos: list[TodoResponse]
    count: int

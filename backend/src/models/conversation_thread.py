from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy import ForeignKey


class ConversationThread(SQLModel, table=True):
    """
    Represents a conversation thread between a user and the AI agent.
    """
    __tablename__ = "conversation_thread"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(nullable=False)  # Will reference user.id from Phase II
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    active: bool = Field(default=True)


class ConversationMessage(SQLModel, table=True):
    """
    Represents a message in a conversation thread.
    """
    __tablename__ = "conversation_message"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    thread_id: uuid.UUID = Field(foreign_key="conversation_thread.id", nullable=False)
    role: str = Field(max_length=20, nullable=False)  # "user" or "assistant"
    content: str = Field(max_length=10000, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
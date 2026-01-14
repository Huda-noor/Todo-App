from sqlmodel import Session, select
from typing import List, Optional
from ..models.conversation_thread import ConversationThread, ConversationMessage
from datetime import datetime
import uuid


class ConversationService:
    """
    Service class for handling conversation-related operations.
    """

    def create_conversation_thread(self, db: Session, user_id: uuid.UUID) -> ConversationThread:
        """
        Create a new conversation thread for a user.
        """
        conversation_thread = ConversationThread(
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            active=True
        )
        db.add(conversation_thread)
        db.commit()
        db.refresh(conversation_thread)
        return conversation_thread

    def get_conversation_thread(self, db: Session, thread_id: uuid.UUID) -> Optional[ConversationThread]:
        """
        Get a conversation thread by its ID.
        """
        return db.get(ConversationThread, thread_id)

    def get_active_conversation_thread(self, db: Session, user_id: uuid.UUID) -> Optional[ConversationThread]:
        """
        Get the active conversation thread for a user.
        """
        statement = select(ConversationThread).where(
            ConversationThread.user_id == user_id,
            ConversationThread.active == True
        )
        return db.execute(statement).first()

    def deactivate_conversation_thread(self, db: Session, thread_id: uuid.UUID) -> bool:
        """
        Deactivate a conversation thread.
        """
        conversation_thread = db.get(ConversationThread, thread_id)
        if conversation_thread:
            conversation_thread.active = False
            conversation_thread.updated_at = datetime.utcnow()
            db.add(conversation_thread)
            db.commit()
            return True
        return False

    def add_message_to_thread(self, db: Session, thread_id: uuid.UUID, role: str, content: str) -> ConversationMessage:
        """
        Add a message to a conversation thread.
        """
        message = ConversationMessage(
            thread_id=thread_id,
            role=role,
            content=content,
            created_at=datetime.utcnow()
        )
        db.add(message)
        # Update the thread's updated_at timestamp
        conversation_thread = db.get(ConversationThread, thread_id)
        if conversation_thread:
            conversation_thread.updated_at = datetime.utcnow()
            db.add(conversation_thread)
        db.commit()
        db.refresh(message)
        return message

    def get_messages_for_thread(self, db: Session, thread_id: uuid.UUID) -> List[ConversationMessage]:
        """
        Get all messages for a conversation thread.
        """
        statement = select(ConversationMessage).where(
            ConversationMessage.thread_id == thread_id
        ).order_by(ConversationMessage.created_at.asc())
        return db.execute(statement).fetchall()

    def get_recent_messages_for_thread(self, db: Session, thread_id: uuid.UUID, limit: int = 50) -> List[ConversationMessage]:
        """
        Get recent messages for a conversation thread with a limit.
        """
        statement = select(ConversationMessage).where(
            ConversationMessage.thread_id == thread_id
        ).order_by(ConversationMessage.created_at.desc()).limit(limit)
        messages = db.execute(statement).fetchall()
        # Reverse the list to return in chronological order
        return list(reversed(messages))
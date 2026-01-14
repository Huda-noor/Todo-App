import uuid
from datetime import datetime
from typing import Optional
from ..models.conversation_thread import ConversationThread
from ..services.conversation_service import ConversationService
from sqlmodel import Session


def get_or_create_conversation_thread(
    db: Session, 
    user_id: uuid.UUID, 
    thread_id: Optional[uuid.UUID] = None
) -> ConversationThread:
    """
    Get an existing conversation thread or create a new one.
    
    Args:
        db: Database session
        user_id: User ID for the conversation
        thread_id: Optional thread ID to retrieve specific thread
    
    Returns:
        ConversationThread: The retrieved or newly created thread
    """
    conversation_service = ConversationService()
    
    if thread_id:
        # Try to get the specific thread
        thread = conversation_service.get_conversation_thread(db, thread_id)
        if thread and thread.user_id == user_id and thread.active:
            return thread
        elif thread:
            # Thread exists but belongs to different user or is inactive
            raise ValueError("Invalid thread access")
    
    # Look for an active thread for this user
    active_thread = conversation_service.get_active_conversation_thread(db, user_id)
    if active_thread:
        return active_thread
    
    # Create a new conversation thread
    new_thread = conversation_service.create_conversation_thread(db, user_id)
    return new_thread


def format_conversation_history(
    messages: list
) -> list:
    """
    Format conversation history for the AI agent.
    
    Args:
        messages: List of conversation messages
        
    Returns:
        List of formatted messages with role and content
    """
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "role": msg.role,
            "content": msg.content
        })
    return formatted_messages


def validate_user_access(
    thread: ConversationThread,
    user_id: uuid.UUID
) -> bool:
    """
    Validate that a user has access to a specific conversation thread.
    
    Args:
        thread: Conversation thread to check
        user_id: User ID attempting access
        
    Returns:
        bool: True if user has access, False otherwise
    """
    return thread.user_id == user_id and thread.active


def truncate_conversation_history(
    messages: list,
    max_tokens: int = 8000
) -> list:
    """
    Truncate conversation history to stay within token limits.
    
    Args:
        messages: List of conversation messages
        max_tokens: Maximum number of tokens allowed
        
    Returns:
        List of messages truncated to fit within token limits
    """
    # This is a simplified implementation
    # In a real implementation, we would calculate actual token usage
    if len(messages) <= 50:  # Default limit of 50 messages
        return messages
    
    # Return the most recent 50 messages
    return messages[-50:]
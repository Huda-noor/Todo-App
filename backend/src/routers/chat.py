from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, Optional
from uuid import UUID
import json

from pydantic import BaseModel

from ..db.session import get_db
from ..middleware.auth import get_current_user_id
from ..services.conversation_service import ConversationService
from ..utils.thread_utils import get_or_create_conversation_thread
from ..agents.todo_agent import todo_agent


class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None


router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post("/converse")
async def converse(
    request: ChatRequest,
    user_id: UUID = Depends(get_current_user_id),
    db = Depends(get_db)
) -> Dict[str, Any]:
    """
    Process a conversational message for todo management.

    Args:
        request: Chat request containing message and optional thread_id
        user_id: The authenticated user ID (extracted from auth)
        db: Database session

    Returns:
        Dictionary with response, thread_id, actions taken, and suggestions
    """
    try:
        # Validate input
        if not request.message or len(request.message.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Message cannot be empty"
            )

        # Get or create conversation thread
        conversation_service = ConversationService()
        thread_uuid = UUID(request.thread_id) if request.thread_id else None
        conversation_thread = get_or_create_conversation_thread(db, user_id, thread_uuid)

        # Add user message to conversation
        user_message = conversation_service.add_message_to_thread(
            db,
            conversation_thread.id,
            "user",
            request.message
        )

        # Get conversation history for context
        messages = conversation_service.get_messages_for_thread(db, conversation_thread.id)
        formatted_history = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        # Run the agent with the conversation history
        result = todo_agent.run_conversation(formatted_history, str(user_id))

        # Add assistant response to conversation
        assistant_message = conversation_service.add_message_to_thread(
            db,
            conversation_thread.id,
            "assistant",
            result["response"]
        )

        # Return the response
        return {
            "response": result["response"],
            "thread_id": str(conversation_thread.id),
            "actions_taken": result["actions_taken"],
            "suggestions": result["suggestions"]
        }

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the error (in a real implementation, use proper logging)
        print(f"Error in chat endpoint: {str(e)}")

        # Raise a generic error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request"
        )
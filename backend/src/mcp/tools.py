from mcp import tool
from sqlmodel import Session, select
from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime
import os
from ..models.conversation_thread import ConversationMessage
from ..services.todo_service import TodoService


# Initialize the todo service
todo_service = TodoService()


@tool
def create_todo(
    user_id: str,
    title: str,
    description: str = "",
    due_date: Optional[str] = None  # ISO 8601 datetime (optional)
) -> Dict[str, Any]:
    """
    Creates a new todo item for the authenticated user.

    Args:
        user_id: Unique identifier of the authenticated user
        title: Title/description of the todo
        description: Additional details (optional)
        due_date: Due date in ISO 8601 format (optional)

    Returns:
        {
            "success": bool,
            "todo_id": str,
            "message": str
        }
    """
    try:
        # Convert user_id to UUID
        user_uuid = UUID(user_id)
        
        # Create the todo using the service
        todo = todo_service.create_todo(
            user_id=user_uuid,
            title=title,
            description=description,
            due_date=due_date
        )
        
        return {
            "success": True,
            "todo_id": str(todo.id),
            "message": f"Created todo with title '{title}'"
        }
    except Exception as e:
        return {
            "success": False,
            "todo_id": None,
            "message": f"Failed to create todo: {str(e)}"
        }


@tool
def list_todos(
    user_id: str,
    filter: str = "all"  # all, completed, pending, overdue, today, etc.
) -> Dict[str, Any]:
    """
    Retrieves todo items for the authenticated user.

    Args:
        user_id: Unique identifier of the authenticated user
        filter: Filter criteria for todo list (optional)

    Returns:
        {
            "success": bool,
            "todos": list of todo objects,
            "count": int
        }
    """
    try:
        # Convert user_id to UUID
        user_uuid = UUID(user_id)
        
        # Get todos using the service
        todos = todo_service.get_todos(user_id=user_uuid, filter_type=filter)
        
        # Format todos for return
        formatted_todos = []
        for todo in todos:
            formatted_todos.append({
                "id": str(todo.id),
                "user_id": str(todo.user_id),
                "title": todo.description,  # Using description as title per Phase II schema
                "completed": todo.is_complete,
                "created_at": todo.created_at.isoformat() if todo.created_at else None,
                "updated_at": todo.updated_at.isoformat() if todo.updated_at else None
            })
        
        return {
            "success": True,
            "todos": formatted_todos,
            "count": len(formatted_todos)
        }
    except Exception as e:
        return {
            "success": False,
            "todos": [],
            "count": 0,
            "message": f"Failed to list todos: {str(e)}"
        }


@tool
def update_todo(
    user_id: str,
    todo_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    completed: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Updates an existing todo item for the authenticated user.

    Args:
        user_id: Unique identifier of the authenticated user
        todo_id: Unique identifier of the todo to update
        title: New title for the todo (optional)
        description: New description for the todo (optional)
        due_date: New due date in ISO 8601 format (optional)
        completed: New completion status (optional)

    Returns:
        {
            "success": bool,
            "message": str
        }
    """
    try:
        # Convert IDs to UUIDs
        user_uuid = UUID(user_id)
        todo_uuid = UUID(todo_id)
        
        # Update the todo using the service
        updated_todo = todo_service.update_todo(
            user_id=user_uuid,
            todo_id=todo_uuid,
            title=title,
            description=description,
            due_date=due_date,
            completed=completed
        )
        
        if updated_todo:
            return {
                "success": True,
                "message": f"Updated todo with ID '{todo_id}'"
            }
        else:
            return {
                "success": False,
                "message": f"Todo with ID '{todo_id}' not found or not owned by user"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to update todo: {str(e)}"
        }


@tool
def delete_todo(
    user_id: str,
    todo_id: str
) -> Dict[str, Any]:
    """
    Deletes an existing todo item for the authenticated user.

    Args:
        user_id: Unique identifier of the authenticated user
        todo_id: Unique identifier of the todo to delete

    Returns:
        {
            "success": bool,
            "message": str
        }
    """
    try:
        # Convert IDs to UUIDs
        user_uuid = UUID(user_id)
        todo_uuid = UUID(todo_id)
        
        # Delete the todo using the service
        success = todo_service.delete_todo(
            user_id=user_uuid,
            todo_id=todo_uuid
        )
        
        if success:
            return {
                "success": True,
                "message": f"Deleted todo with ID '{todo_id}'"
            }
        else:
            return {
                "success": False,
                "message": f"Todo with ID '{todo_id}' not found or not owned by user"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to delete todo: {str(e)}"
        }


@tool
def toggle_todo_completion(
    user_id: str,
    todo_id: str,
    completed: bool
) -> Dict[str, Any]:
    """
    Marks an existing todo as complete/incomplete for the authenticated user.

    Args:
        user_id: Unique identifier of the authenticated user
        todo_id: Unique identifier of the todo to update
        completed: New completion status

    Returns:
        {
            "success": bool,
            "message": str
        }
    """
    try:
        # Convert IDs to UUIDs
        user_uuid = UUID(user_id)
        todo_uuid = UUID(todo_id)
        
        # Toggle completion using the service
        updated_todo = todo_service.update_todo(
            user_id=user_uuid,
            todo_id=todo_uuid,
            completed=completed
        )
        
        if updated_todo:
            status_text = "completed" if completed else "incomplete"
            return {
                "success": True,
                "message": f"Marked todo with ID '{todo_id}' as {status_text}"
            }
        else:
            return {
                "success": False,
                "message": f"Todo with ID '{todo_id}' not found or not owned by user"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to toggle todo completion: {str(e)}"
        }
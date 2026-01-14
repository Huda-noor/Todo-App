from typing import Dict, Any, List
from uuid import UUID


def format_response_for_creation(todo_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format response for todo creation actions.
    
    Args:
        todo_data: Dictionary containing todo information
        
    Returns:
        Formatted response dictionary
    """
    return {
        "success": True,
        "message": f"I've created a new todo: '{todo_data.get('title', 'Untitled')}'",
        "todo_id": todo_data.get('id'),
        "actions_taken": [{
            "tool": "create_todo",
            "description": f"Created todo with title '{todo_data.get('title', 'Untitled')}'",
            "result": {
                "success": True,
                "todo_id": todo_data.get('id')
            }
        }]
    }


def format_response_for_reading(todos: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Format response for todo reading actions.
    
    Args:
        todos: List of todo dictionaries
        
    Returns:
        Formatted response dictionary
    """
    if not todos:
        response_text = "Your todo list is empty!"
    else:
        todo_list = "\n".join([f"- {'✓' if t.get('completed', False) else '☐'} {t.get('title', 'Untitled')}" for t in todos])
        response_text = f"Here are your current tasks ({len(todos)} total):\n{todo_list}"
    
    return {
        "success": True,
        "message": response_text,
        "count": len(todos),
        "actions_taken": [{
            "tool": "list_todos",
            "description": f"Retrieved {len(todos)} todos",
            "result": {
                "success": True,
                "todos": todos,
                "count": len(todos)
            }
        }]
    }


def format_response_for_update(todo_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format response for todo update actions.
    
    Args:
        todo_data: Dictionary containing updated todo information
        
    Returns:
        Formatted response dictionary
    """
    return {
        "success": True,
        "message": f"I've updated the todo: '{todo_data.get('title', 'Untitled')}'",
        "actions_taken": [{
            "tool": "update_todo",
            "description": f"Updated todo with title '{todo_data.get('title', 'Untitled')}'",
            "result": {
                "success": True,
                "todo_id": todo_data.get('id')
            }
        }]
    }


def format_response_for_deletion(todo_title: str) -> Dict[str, Any]:
    """
    Format response for todo deletion actions.
    
    Args:
        todo_title: Title of the deleted todo
        
    Returns:
        Formatted response dictionary
    """
    return {
        "success": True,
        "message": f"I've deleted the todo: '{todo_title}'",
        "actions_taken": [{
            "tool": "delete_todo",
            "description": f"Deleted todo with title '{todo_title}'",
            "result": {
                "success": True,
                "message": f"Deleted todo: {todo_title}"
            }
        }]
    }


def format_response_for_completion(todo_title: str, completed: bool) -> Dict[str, Any]:
    """
    Format response for todo completion actions.
    
    Args:
        todo_title: Title of the todo
        completed: Whether the todo was marked as completed or incomplete
        
    Returns:
        Formatted response dictionary
    """
    status_text = "completed" if completed else "marked as incomplete"
    return {
        "success": True,
        "message": f"I've {status_text} the todo: '{todo_title}'",
        "actions_taken": [{
            "tool": "toggle_todo_completion",
            "description": f"Marked todo '{todo_title}' as {'completed' if completed else 'incomplete'}",
            "result": {
                "success": True,
                "todo_title": todo_title,
                "completed": completed
            }
        }]
    }


def format_error_response(error_message: str, error_type: str = "general") -> Dict[str, Any]:
    """
    Format response for error conditions.
    
    Args:
        error_message: The error message to return
        error_type: Type of error for categorization
        
    Returns:
        Formatted error response dictionary
    """
    user_friendly_messages = {
        "auth": "I'm having trouble verifying your identity. Please sign in again.",
        "tool_execution": "I'm having trouble completing that task right now. Please try again in a moment.",
        "intent_unclear": "I'm not sure how to help with that. You can ask me to create, read, update, delete, or mark todos as complete.",
        "ambiguous_request": "Could you clarify which task you mean? I found multiple tasks that might match your request.",
        "confirmation_required": "To protect your data, I need to confirm: are you sure you want to proceed with this action?",
        "rate_limit": "You're sending messages too quickly. Please slow down and try again."
    }
    
    user_message = user_friendly_messages.get(error_type, error_message)
    
    return {
        "success": False,
        "message": user_message,
        "error_type": error_type,
        "actions_taken": []
    }


def format_clarification_request(options: List[str], question: str) -> Dict[str, Any]:
    """
    Format response when clarification is needed.
    
    Args:
        options: List of options for the user to choose from
        question: The clarification question
        
    Returns:
        Formatted clarification response dictionary
    """
    options_text = ""
    if options:
        options_text = "\nOptions:\n" + "\n".join([f"- {opt}" for opt in options])
    
    return {
        "success": True,
        "message": f"{question}{options_text}",
        "needs_clarification": True,
        "options": options,
        "actions_taken": []
    }
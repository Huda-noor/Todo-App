from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime, timezone
from uuid import UUID
import json


class TodoService:
    """
    Service class for handling todo-related operations.
    This service interacts with the existing Phase II todo model.
    """

    def create_todo(self, user_id: UUID, title: str, description: str = "", due_date: Optional[str] = None):
        """
        Create a new todo for a user.
        """
        # Import the Todo model
        from ..models.todo import Todo

        # Create a new todo instance
        todo = Todo(
            user_id=user_id,
            description=title,  # Using description field from Phase II model
            is_complete=False  # Default to incomplete
        )

        # Get database session and add to database
        from ..db.database import SessionLocal
        db = SessionLocal()
        try:
            db.add(todo)
            db.commit()
            db.refresh(todo)
            return todo
        finally:
            db.close()

    def get_todos(self, user_id: UUID, filter_type: str = "all"):
        """
        Get todos for a user with optional filtering.
        """
        # Import the Todo model
        from ..models.todo import Todo

        # Get database session
        from ..db.database import SessionLocal
        db = SessionLocal()
        try:
            # Build the query
            query = select(Todo).where(Todo.user_id == user_id)

            # Apply filters based on filter_type
            if filter_type == "completed":
                query = query.where(Todo.is_complete == True)
            elif filter_type == "pending":
                query = query.where(Todo.is_complete == False)
            elif filter_type == "today":
                # Filter for todos created today
                today_start = datetime.combine(datetime.now(timezone.utc).date(), datetime.min.time().replace(tzinfo=timezone.utc))
                today_end = datetime.combine(datetime.now(timezone.utc).date(), datetime.max.time().replace(tzinfo=timezone.utc))
                query = query.where(Todo.created_at.between(today_start, today_end))

            # Execute query
            todos = db.exec(query).all()
            return todos
        finally:
            db.close()

    def update_todo(self, user_id: UUID, todo_id: UUID, title: Optional[str] = None,
                    description: Optional[str] = None, due_date: Optional[str] = None,
                    completed: Optional[bool] = None):
        """
        Update an existing todo for a user.
        """
        # Import the Todo model
        from ..models.todo import Todo

        # Get database session
        from ..db.database import SessionLocal
        db = SessionLocal()
        try:
            # Get the todo
            todo = db.get(Todo, todo_id)

            # Verify that the todo belongs to the user
            if not todo or todo.user_id != user_id:
                return None

            # Update fields if provided
            if title is not None:
                todo.description = title
            if description is not None:
                # If we want to store additional description separately, we might need to extend the model
                # For now, we'll just update the description field
                todo.description = description if description else todo.description
            if completed is not None:
                todo.is_complete = completed
            if due_date is not None:
                # Assuming there's a due_date field in the model, which might need to be added
                # For now, we'll skip this since Phase II model might not have it
                pass

            todo.updated_at = datetime.now(timezone.utc)

            # Update in database
            db.add(todo)
            db.commit()
            db.refresh(todo)

            return todo
        finally:
            db.close()

    def delete_todo(self, user_id: UUID, todo_id: UUID) -> bool:
        """
        Delete a todo for a user.
        """
        # Import the Todo model
        from ..models.todo import Todo

        # Get database session
        from ..db.database import SessionLocal
        db = SessionLocal()
        try:
            # Get the todo
            todo = db.get(Todo, todo_id)

            # Verify that the todo belongs to the user
            if not todo or todo.user_id != user_id:
                return False

            # Delete from database
            db.delete(todo)
            db.commit()

            return True
        finally:
            db.close()


# Create a global instance of the service
todo_service = TodoService()
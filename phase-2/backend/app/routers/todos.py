"""Todo CRUD endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from uuid import UUID
from datetime import datetime, timezone

from app.database import get_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.todo import Todo
from app.schemas.todo import (
    CreateTodoRequest,
    UpdateTodoRequest,
    TodoResponse,
    TodoListResponse,
)

router = APIRouter()


@router.get("", response_model=TodoListResponse)
def list_todos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    """List all todos for the current user."""
    statement = select(Todo).where(Todo.user_id == current_user.id).order_by(Todo.created_at.desc())
    todos = db.exec(statement).all()
    return TodoListResponse(todos=todos, count=len(todos))


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    request: CreateTodoRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    """Create a new todo for the current user."""
    todo = Todo(
        user_id=current_user.id,
        description=request.description,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    """Get a specific todo by ID."""
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id)
    todo = db.exec(statement).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: UUID,
    request: UpdateTodoRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    """Update a todo's description."""
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id)
    todo = db.exec(statement).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    todo.description = request.description
    todo.updated_at = datetime.now(timezone.utc)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    """Delete a todo."""
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id)
    todo = db.exec(statement).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}


@router.patch("/{todo_id}/toggle", response_model=TodoResponse)
def toggle_todo(
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    """Toggle a todo's completion status."""
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id)
    todo = db.exec(statement).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    todo.is_complete = not todo.is_complete
    todo.updated_at = datetime.now(timezone.utc)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

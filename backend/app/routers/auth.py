"""Authentication endpoints."""
from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """Get the current authenticated user's information."""
    return current_user

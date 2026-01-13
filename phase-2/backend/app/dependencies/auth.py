"""Authentication dependency for session validation."""
from fastapi import Depends, HTTPException, Request, status
from sqlmodel import Session, select
from datetime import datetime, timezone
from urllib.parse import unquote

from app.database import get_session
from app.models.user import User
from app.models.session import Session as SessionModel


def extract_token_from_cookie(cookie_value: str) -> str:
    """
    Extract the session token from a Neon Auth cookie value.

    Neon Auth cookie format: "token.signature" (URL-encoded)
    We only need the token part to match against the database.
    """
    if not cookie_value:
        return ""

    # URL-decode the cookie value
    decoded = unquote(cookie_value)

    # Extract just the token part (before the dot)
    if "." in decoded:
        return decoded.split(".")[0]

    return decoded


def get_current_user(
    request: Request,
    db: Session = Depends(get_session)
) -> User:
    """
    Dependency that validates the session token cookie and returns the current user.

    Reads the Neon Auth (Better Auth) session token from cookies, validates it against
    the session table in the neon_auth schema, and returns the associated user.

    Raises:
        HTTPException 401: If no session token or invalid/expired session
    """
    # Try to get session token from multiple sources:
    # 1. Authorization header (Bearer token) - for cross-origin API calls
    # 2. Cookies - for same-origin requests

    session_token = None

    # Check Authorization header first
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        session_token = auth_header[7:]  # Remove "Bearer " prefix

    # Fall back to cookies if no Authorization header
    if not session_token:
        raw_cookie = (
            request.cookies.get("__Secure-neon-auth.session_token") or
            request.cookies.get("neon-auth.session_token") or
            request.cookies.get("better-auth.session_token")
        )
        if raw_cookie:
            session_token = extract_token_from_cookie(raw_cookie)

    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Query session table to validate token (using timezone-aware datetime)
    statement = select(SessionModel).where(
        SessionModel.token == session_token,
        SessionModel.expires_at > datetime.now(timezone.utc)
    )
    session_record = db.exec(statement).first()

    if not session_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Get the user associated with the session
    statement = select(User).where(User.id == session_record.user_id)
    user = db.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    return user

from fastapi import HTTPException, Request, status
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import os
import jwt
from datetime import datetime, timedelta
import uuid


class AuthMiddleware:
    """
    Authentication middleware to reuse Phase II authentication.
    This is a simplified implementation that assumes JWT tokens from Phase II.
    In a real implementation, this would interface with the actual Phase II auth system.
    """
    
    def __init__(self):
        self.secret_key = os.getenv("PHASE_II_AUTH_SECRET", "fallback-secret-key")
        self.algorithm = "HS256"
        self.security = HTTPBearer()
    
    def decode_token(self, token: str) -> Optional[dict]:
        """
        Decode and verify the JWT token.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def get_current_user_id(self, request: Request) -> Optional[uuid.UUID]:
        """
        Extract and return the current user ID from the request.
        """
        # In a real implementation, this would extract the token from the request
        # and decode it to get the user ID
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid authorization header",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token = auth_header.split(" ")[1]
        payload = self.decode_token(token)
        
        # Assuming the user ID is stored in the 'sub' claim (standard JWT practice)
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        try:
            user_id = uuid.UUID(user_id_str)
            return user_id
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID format in token",
                headers={"WWW-Authenticate": "Bearer"},
            )


# Create a global instance of the auth middleware
auth_middleware = AuthMiddleware()


async def get_current_user_id(request: Request) -> uuid.UUID:
    """
    Dependency to get the current user ID from the request.
    """
    return auth_middleware.get_current_user_id(request)
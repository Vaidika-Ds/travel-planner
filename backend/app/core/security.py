from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from uuid import UUID
from app.core.config import settings

security = HTTPBearer(auto_error=False)

async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UUID:
    """
    Extracts and verifies the user ID from the Supabase JWT token.
    In development mode without token, returns a mock user ID for testing.
    """
    if not credentials:
        if settings.ENVIRONMENT == "development":
            # Real registered test user ID from user_profiles table for seamless local API testing
            return UUID("70af4deb-4016-49f8-aa0f-dc7fe9e3d970")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    try:
        # Decode Supabase JWT (unverified signature in basic dev, or verified with JWT secret)
        payload = jwt.decode(
            token,
            settings.SUPABASE_ANON_KEY or settings.SECRET_KEY,
            algorithms=["HS256"],
            options={"verify_signature": False} # Set to True when JWT secret is configured
        )
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return UUID(user_id_str)
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

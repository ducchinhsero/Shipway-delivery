"""
API dependencies (authentication, database connection, etc.)
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.db.session import get_database
from app.core.security import decode_access_token
from app.db.models import find_user_by_id
from typing import Dict, Any


# HTTP Bearer security scheme for JWT
security = HTTPBearer()


def get_db() -> AsyncIOMotorDatabase:
    """
    Dependency to get database instance
    
    Returns:
        Database instance
    """
    return get_database()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> Dict[str, Any]:
    """
    Dependency to get current authenticated user
    
    Args:
        credentials: JWT token from Authorization header
        db: Database instance
        
    Returns:
        Current user document
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    # Decode token
    payload = decode_access_token(credentials.credentials)
    
    # Get user_id from token
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    # Find user in database
    user = await find_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if user is active
    if not user.get('is_active', True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )
    
    return user


async def get_current_admin(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Dependency to check if current user is admin
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current user if admin
        
    Raises:
        HTTPException: If user is not admin
    """
    if current_user.get('role') != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user

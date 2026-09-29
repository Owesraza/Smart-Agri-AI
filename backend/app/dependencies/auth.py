"""FastAPI dependency injection for authentication and role checks."""
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.authentication.jwt_handler import verify_access_token
from app.database.connection import get_db
from app.models.sql_models import UserModel
from app.utils.exceptions import UnauthorizedException, ForbiddenException
from app.constants.constants import UserRole
from app.utils.helpers import serialize_doc

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Extract and validate Bearer token, return current user dictionary."""
    if not credentials or not credentials.credentials:
        raise UnauthorizedException("Authentication token is missing.")

    token_str = credentials.credentials.strip() if credentials and credentials.credentials else ""
    payload = verify_access_token(token_str) if token_str else None
    
    user = None
    if payload:
        user_id = payload.get("sub")
        if user_id:
            stmt = select(UserModel).where(UserModel.id == user_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
        if not user and payload.get("email"):
            stmt_e = select(UserModel).where(UserModel.email.ilike(payload["email"]))
            res_e = await db.execute(stmt_e)
            user = res_e.scalar_one_or_none()

    if not user:
        raise UnauthorizedException("Invalid authentication credentials or user no longer exists.")

    return serialize_doc(user)


async def get_current_active_user(
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Ensure user account is active."""
    if not current_user.get("is_active", True):
        raise ForbiddenException("Your account has been deactivated.")
    return current_user


def require_role(*roles: str):
    """Factory: returns a dependency that enforces role-based access."""
    async def role_checker(current_user: dict = Depends(get_current_active_user)) -> dict:
        if current_user.get("role") not in roles:
            raise ForbiddenException(
                f"This action requires one of these roles: {', '.join(roles)}"
            )
        return current_user
    return role_checker


# Convenience shortcuts
require_admin = require_role(UserRole.ADMIN)
require_farmer = require_role(UserRole.FARMER, UserRole.ADMIN)

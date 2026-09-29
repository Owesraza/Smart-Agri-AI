"""Auth service: registration, login, token refresh, password reset using SQL."""
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.sql_models import UserModel, RefreshTokenModel, ResetTokenModel
from app.authentication.jwt_handler import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, create_reset_token,
    verify_refresh_token, verify_reset_token,
)
from app.schemas.user import UserRegister, UserLogin
from app.utils.exceptions import ConflictException, UnauthorizedException, BadRequestException, NotFoundException
from app.utils.helpers import serialize_doc


async def register_user(db: AsyncSession, data: UserRegister) -> dict:
    # Check duplicate email
    res = await db.execute(select(UserModel).where(UserModel.email == data.email.lower()))
    if res.scalar_one_or_none():
        raise ConflictException("An account with this email already exists.")

    # Check duplicate phone
    res = await db.execute(select(UserModel).where(UserModel.mobile_number == data.mobile_number))
    if res.scalar_one_or_none():
        raise ConflictException("An account with this mobile number already exists.")

    now = datetime.now(timezone.utc)
    user = UserModel(
        full_name=data.full_name,
        mobile_number=data.mobile_number,
        email=data.email.lower(),
        password=hash_password(data.password),
        village=data.village,
        district=data.district,
        state=data.state,
        farm_size=data.farm_size,
        preferred_language=data.preferred_language or "Hindi",
        role=data.role,
        is_active=True,
        created_at=now,
        updated_at=now,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return serialize_doc(user)


async def login_user(db: AsyncSession, data: UserLogin) -> dict:
    res = await db.execute(select(UserModel).where(UserModel.email == data.email.lower()))
    user = res.scalar_one_or_none()

    if not user or not verify_password(data.password, user.password):
        raise UnauthorizedException("Invalid email or password.")

    if not user.is_active:
        raise UnauthorizedException("Your account has been deactivated.")

    user_data = serialize_doc(user)
    access_token = create_access_token(user_data["id"], user_data["role"])
    refresh_token = create_refresh_token(user_data["id"])

    # Store refresh token
    token_obj = RefreshTokenModel(
        user_id=user_data["id"],
        token=refresh_token,
        created_at=datetime.now(timezone.utc),
    )
    db.add(token_obj)
    await db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "user": user_data}


async def refresh_access_token(db: AsyncSession, refresh_token: str) -> dict:
    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise UnauthorizedException("Invalid or expired refresh token.")

    # Check token exists in DB
    res = await db.execute(select(RefreshTokenModel).where(RefreshTokenModel.token == refresh_token))
    stored = res.scalar_one_or_none()
    if not stored:
        raise UnauthorizedException("Refresh token has been revoked.")

    user_id = payload["sub"]
    res_user = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = res_user.scalar_one_or_none()
    if not user:
        raise NotFoundException("User")

    user_data = serialize_doc(user)
    new_access = create_access_token(user_data["id"], user_data["role"])
    new_refresh = create_refresh_token(user_data["id"])

    # Rotate refresh token
    await db.delete(stored)
    db.add(RefreshTokenModel(
        user_id=user_data["id"],
        token=new_refresh,
        created_at=datetime.now(timezone.utc),
    ))
    await db.commit()

    return {"access_token": new_access, "refresh_token": new_refresh}


async def logout_user(db: AsyncSession, refresh_token: str) -> bool:
    res = await db.execute(select(RefreshTokenModel).where(RefreshTokenModel.token == refresh_token))
    stored = res.scalar_one_or_none()
    if stored:
        await db.delete(stored)
        await db.commit()
        return True
    return False


async def forgot_password(db: AsyncSession, email: str) -> str:
    res = await db.execute(select(UserModel).where(UserModel.email == email.lower()))
    user = res.scalar_one_or_none()
    if not user:
        return "If this email is registered, a reset link has been sent."

    token = create_reset_token(user.id)

    # Clear old tokens for user
    await db.execute(delete(ResetTokenModel).where(ResetTokenModel.user_id == user.id))
    db.add(ResetTokenModel(
        user_id=user.id,
        token=token,
        created_at=datetime.now(timezone.utc),
    ))
    await db.commit()
    return token


async def reset_password(db: AsyncSession, token: str, new_password: str) -> bool:
    payload = verify_reset_token(token)
    if not payload:
        raise BadRequestException("Invalid or expired reset token.")

    res = await db.execute(select(ResetTokenModel).where(ResetTokenModel.token == token))
    stored = res.scalar_one_or_none()
    if not stored:
        raise BadRequestException("Reset token has already been used.")

    user_id = payload["sub"]
    res_user = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = res_user.scalar_one_or_none()
    if not user:
        raise NotFoundException("User")

    user.password = hash_password(new_password)
    user.updated_at = datetime.now(timezone.utc)
    await db.delete(stored)
    await db.commit()
    return True

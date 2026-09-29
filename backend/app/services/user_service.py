"""User profile service using SQL."""
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.sql_models import UserModel
from app.authentication.jwt_handler import hash_password, verify_password
from app.schemas.user import UserUpdate, PasswordChange
from app.utils.exceptions import NotFoundException, ConflictException, BadRequestException
from app.utils.helpers import serialize_doc, serialize_list, paginate, pagination_meta


async def get_user_by_id(db: AsyncSession, user_id: str) -> dict:
    res = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = res.scalar_one_or_none()
    if not user:
        raise NotFoundException("User")
    return serialize_doc(user)


async def update_user(db: AsyncSession, user_id: str, data: UserUpdate) -> dict:
    res = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = res.scalar_one_or_none()
    if not user:
        raise NotFoundException("User")

    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise BadRequestException("No fields to update.")

    if "mobile_number" in update_data:
        existing = await db.execute(
            select(UserModel).where(
                UserModel.mobile_number == update_data["mobile_number"],
                UserModel.id != user_id
            )
        )
        if existing.scalar_one_or_none():
            raise ConflictException("This mobile number is already in use.")
        if "whatsapp_number" not in update_data or not update_data["whatsapp_number"]:
            update_data["whatsapp_number"] = update_data["mobile_number"]

    for k, v in update_data.items():
        setattr(user, k, v)
    user.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(user)
    return serialize_doc(user)


async def change_password(db: AsyncSession, user_id: str, data: PasswordChange) -> bool:
    res = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = res.scalar_one_or_none()
    if not user:
        raise NotFoundException("User")

    if not verify_password(data.current_password, user.password):
        raise BadRequestException("Current password is incorrect.")

    user.password = hash_password(data.new_password)
    user.updated_at = datetime.now(timezone.utc)
    await db.commit()
    return True


async def list_users(db: AsyncSession, page: int = 1, limit: int = 10) -> dict:
    p = paginate(page, limit)
    total_res = await db.execute(select(func.count(UserModel.id)))
    total = total_res.scalar_one() or 0

    res = await db.execute(
        select(UserModel)
        .order_by(UserModel.created_at.desc())
        .offset(p["offset"])
        .limit(p["limit"])
    )
    users = res.scalars().all()
    return {
        "users": serialize_list(users),
        "pagination": pagination_meta(total, page, p["limit"]),
    }


async def delete_user(db: AsyncSession, user_id: str) -> bool:
    res = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = res.scalar_one_or_none()
    if not user:
        raise NotFoundException("User")
    await db.delete(user)
    await db.commit()
    return True

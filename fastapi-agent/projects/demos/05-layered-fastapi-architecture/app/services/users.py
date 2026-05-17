from __future__ import annotations

from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserNameConflictError, UserNotFoundError
from app.models.users import User
from app.repositories import users as user_repo


async def create_user(session: AsyncSession, name: str) -> User:
    # TODO: decide transaction boundary.
    try:
        user = await user_repo.add_user(session, name)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise UserNameConflictError(name)
    return user

async def get_user(session: AsyncSession, user_id: int) -> User:
    # TODO: call repository.
    # TODO: translate None into UserNotFoundError.
    user = await user_repo.get_user_by_id(session, user_id)
    if not user:
        raise UserNotFoundError(user_id)
    return user

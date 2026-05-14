from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserNameConflictError, UserNotFoundError
from app.models.users import User
from app.repositories import users as user_repo


async def create_user(session: AsyncSession, name: str) -> User:
    # TODO: decide transaction boundary.
    try:
        user = await user_repo.add_user(session, name)
    except IntegrityError:
        raise UserNameConflictError()
    # TODO: call repository.
    # TODO: translate database conflict into UserNameConflictError.
    raise NotImplementedError


async def get_user(session: AsyncSession, user_id: int) -> User:
    # TODO: call repository.
    # TODO: translate None into UserNotFoundError.
    raise NotImplementedError

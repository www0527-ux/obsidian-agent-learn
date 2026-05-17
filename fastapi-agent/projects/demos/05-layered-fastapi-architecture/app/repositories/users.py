from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    # TODO: return User or None.
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user


async def get_user_by_name(session: AsyncSession, name: str) -> User | None:

    stmt= select(User).where(User.name == name)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user



async def add_user(session: AsyncSession, name: str) -> User:
    # TODO: create ORM object, add to session, flush, return user.
    # Question: should this function commit, or should service own commit?
    user= User(name=name)
    #如何区分是数据库出错了，还是用户名冲突了？如果数据库出错了，应该抛异常；如果用户名冲突了，应该抛 UserNameConflictError。
    session.add(user)
    await session.flush()
    return user

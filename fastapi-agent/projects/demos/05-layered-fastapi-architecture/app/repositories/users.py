from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    # TODO: return User or None.
    stmt = select(User).where(User.id == user_id)
    
#如何区分是没找到，还是数据库出错了？如果数据库出错了，应该抛异常；如果没找到，应该返回 None。
    try:    
        result= await session.execute(stmt)
    except Exception as e:
        raise e
    user = result.scalar_one_or_none()
    return user
    raise NotImplementedError


async def get_user_by_name(session: AsyncSession, name: str) -> User | None:

    stmt= select(User).where(User.name == name)
    try:
        result= await session.execute(stmt)
    except Exception as e:
        raise e
    user = result.scalar_one_or_none()
    return user
    # TODO: select by name.
    raise NotImplementedError


async def add_user(session: AsyncSession, name: str) -> User:
    # TODO: create ORM object, add to session, flush, return user.
    # Question: should this function commit, or should service own commit?
    user= User(name=name)
    #如何区分是数据库出错了，还是用户名冲突了？如果数据库出错了，应该抛异常；如果用户名冲突了，应该抛 UserNameConflictError。
    try:
        session.add(user)
        await session.flush()
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e
    
    return user
    raise NotImplementedError

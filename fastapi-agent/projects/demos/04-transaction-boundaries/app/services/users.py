from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.exceptions import UserNameConflictError
from sqlalchemy.exc import IntegrityError

async def create_user(session: AsyncSession, name: str) -> User:
    """Create one user.

    Practice focus:
    - add User(name=name)
    - await session.commit()
    - catch IntegrityError
    - await session.rollback()
    - raise UserNameConflictError
    """
    user = User(name=name)
   
    try: 
        session.add(user)
        await session.commit()
        await session.refresh(user)
    except IntegrityError:
        await session.rollback()
        raise UserNameConflictError(name)
    return user#如果失败了，依旧会抛出UserNameConflictError异常，如果成功了，就返回创建的用户对象
    # raise NotImplementedError("Write the async create_user service here.")

from __future__ import annotations

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal


async def get_session() -> AsyncIterator[AsyncSession]:
    # TODO: yield one AsyncSession per request.
    raise NotImplementedError


# Optional advanced version:
# def get_user_service(...) -> UserService:
#     ...

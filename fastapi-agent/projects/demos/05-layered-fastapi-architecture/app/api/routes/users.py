from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.core.exceptions import UserNameConflictError, UserNotFoundError
from app.schemas.users import UserCreate, UserRead
from app.services.users import create_user, get_user


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    payload: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    # TODO: call service.create_user.
    # TODO: translate UserNameConflictError into HTTP 409.
    raise NotImplementedError


@router.get("/{user_id}", response_model=UserRead)
async def get_user_endpoint(
    user_id: int,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    # TODO: call service.get_user.
    # TODO: translate UserNotFoundError into HTTP 404.
    raise NotImplementedError

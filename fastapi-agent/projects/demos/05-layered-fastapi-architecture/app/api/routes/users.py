from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.core.exceptions import UserNameConflictError, UserNotFoundError
from app.schemas.users import UserCreate, UserRead
from app.services.users import create_user, get_user
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    payload: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    # TODO: call service.create_user.
    try:
        user = await create_user(session, payload.name)
    except UserNameConflictError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the user.",
        )
    return UserRead.from_orm(user)
    # TODO: translate UserNameConflictError into HTTP 409.
    


@router.get("/{user_id}", response_model=UserRead)
async def get_user_endpoint(
    user_id: int,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    try:
        user=await get_user(session, user_id)
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving the user.",
        )
    return UserRead.from_orm(user)

    # TODO: call service.get_user.
    # TODO: translate UserNotFoundError into HTTP 404.
    raise NotImplementedError

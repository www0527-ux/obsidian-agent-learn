from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.services.records import increment_view_count
from app.exceptions import record_increment_conflict_error
from fastapi import HTTPException, status
router = APIRouter(prefix="/records", tags=["records"])
@router.post("/{record_id}/views")
async def increment_view_count_endpoint(
    record_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    """Increment the view count of one record."""
    try:
        await increment_view_count(session, record_id)
    except record_increment_conflict_error:
        raise HTTPException(
            status_code=409,
            detail=f"Record with id '{record_id}' has been concurrently updated. Please retry.",
        )
    
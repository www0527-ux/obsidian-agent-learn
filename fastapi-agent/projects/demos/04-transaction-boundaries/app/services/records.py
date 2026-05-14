from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import LearningRecord
from sqlalchemy.exc import IntegrityError
from app.exceptions import record_increment_conflict_error
async def increment_view_count(session: AsyncSession, record_id: int) -> None:
    """Increment the view count of one record.

    Practice focus:
    - await session.execute(update(...))
    - await session.commit()
    """
    stmt = (update(LearningRecord)
            .where(LearningRecord.id == record_id)
            .values(view_count=LearningRecord.view_count + 1))
    try:
        await session.execute(stmt)
        await session.commit()

    except IntegrityError:
        await session.rollback()#回滚的范围是整个事务，所以如果在执行 update 语句时发生了任何异常，都会回滚到事务开始之前的状态，确保数据的一致性和完整性。
        raise record_increment_conflict_error(record_id)

    # raise NotImplementedError("Write the async increment_view_count service here.")
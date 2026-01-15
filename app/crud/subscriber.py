from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.subscriber import Subscriber

async def get_subscribers(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Subscriber]:
    """
    모든 Subscriber 목록을 조회합니다.
    """
    result = await db.execute(select(Subscriber).offset(skip).limit(limit))
    return result.scalars().all()

async def get_subscriber(db: AsyncSession, subscriber_id: int) -> Optional[Subscriber]:
    """
    ID로 Subscriber를 조회합니다.
    """
    result = await db.execute(select(Subscriber).filter(Subscriber.id == subscriber_id))
    return result.scalar_one_or_none()

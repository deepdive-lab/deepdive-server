from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud import subscriber as crud_subscriber
from app.schemas.subscriber import SubscriberResponse

router = APIRouter(prefix="/api/v1", tags=["subscriber"])

@router.get("/subscribers", response_model=list[SubscriberResponse])
async def get_subscribers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Subscriber 목록을 조회합니다.
    """
    subscribers = await crud_subscriber.get_subscribers(db, skip=skip, limit=limit)
    return subscribers

@router.get("/subscribers/{subscriber_id}", response_model=SubscriberResponse)
async def get_subscriber(
    subscriber_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    특정 Subscriber의 정보를 조회합니다.
    """
    subscriber = await crud_subscriber.get_subscriber(db, subscriber_id=subscriber_id)
    if subscriber is None:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return subscriber
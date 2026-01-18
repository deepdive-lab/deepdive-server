from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.company import Company

async def get_companies(db: AsyncSession) -> List[Company]:
    """
    모든 Company 목록을 조회합니다.
    """
    result = await db.execute(select(Company))
    return result.scalars().all()

async def get_company(db: AsyncSession, company_id: int) -> Optional[Company]:
    """
    ID로 Company를 조회합니다.
    """
    result = await db.execute(select(Company).filter(Company.id == company_id))
    return result.scalar_one_or_none()

async def create_company(db: AsyncSession, company: Company) -> Company:
    """
    새로운 Company를 생성합니다.
    """
    db.add(company)
    await db.commit()
    await db.refresh(company)
    return company

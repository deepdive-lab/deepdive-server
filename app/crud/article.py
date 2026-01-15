from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.article import Article

async def get_articles(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Article]:
    """
    모든 Article 목록을 조회합니다.
    """
    result = await db.execute(select(Article).offset(skip).limit(limit))
    return result.scalars().all()

async def get_article(db: AsyncSession, article_id: int) -> Optional[Article]:
    """
    ID로 Article을 조회합니다.
    """
    result = await db.execute(select(Article).filter(Article.id == article_id))
    return result.scalar_one_or_none()

async def create_article(db: AsyncSession, article: Article) -> Article:
    """
    새로운 Article을 생성합니다.
    """
    db.add(article)
    await db.commit()
    await db.refresh(article)
    return article

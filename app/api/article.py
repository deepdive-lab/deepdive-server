from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud import article as crud_article
from app.schemas.article import ArticleUploadRequest, ArticleSummary, ArticleDetail
from graph.workflow import graph

router = APIRouter(prefix="/api/v1", tags=["article"])

@router.get("/articles", response_model=list[ArticleSummary])
async def get_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Article 목록을 조회합니다. (카드 목록용 간략 정보)
    """
    articles = await crud_article.get_articles(db, skip=skip, limit=limit)
    return articles

@router.get("/articles/{article_id}", response_model=ArticleDetail)
async def get_article(
    article_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    특정 Article의 상세 정보를 조회합니다.
    """
    article = await crud_article.get_article(db, article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.post("/articles/upload")
async def upload_article(
    request: ArticleUploadRequest
):
    # TypedDict는 dict이므로 생성자가 없습니다. dict로 전달해야 합니다.
    response = await graph.ainvoke({"url": request.url})
    return response
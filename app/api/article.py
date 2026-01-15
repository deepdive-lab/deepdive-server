from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud import article as crud_article
from app.schemas.article import ArticleUploadRequest, ArticleSummary, ArticleDetail
import trafilatura
from trafilatura.metadata import extract_metadata
import httpx

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

@router.post("/articles/upload/test")
async def upload_article_from_url(
    request: ArticleUploadRequest
):
    try:
        # 1. URL에서 HTML 가져오기 (trafilatura.fetch_url 시도)
        downloaded = trafilatura.fetch_url(request.url)
        # trafilatura.fetch_url이 실패하면 httpx로 직접 가져오기
        if downloaded is None:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(request.url, follow_redirects=True)
                response.raise_for_status()
                downloaded = response.text
        
        metadata = extract_metadata(downloaded)
        
        # 2. 본문만 딱 집어서 마크다운으로 변환하기
        markdown_content = trafilatura.extract(
            downloaded,
            output_format='markdown',
            include_tables=True,       # 표도 마크다운으로 포함
            include_images=True,
            include_links=True,
            include_comments=False     # 댓글 제외
        )
        
        if markdown_content is None or markdown_content.strip() == "":
            raise HTTPException(status_code=400, detail="URL에서 콘텐츠를 추출할 수 없습니다.")
        
        # metadata 처리
        author = ""
        description = ""
        thumbnail = ""
        date = ""
        
        if metadata:
            author = metadata.author or ""
            description = metadata.description or ""
            thumbnail = metadata.image or ""
            date = metadata.date or ""
        
        return {
            "author": author,
            "description": description,
            "thumbnail": thumbnail,
            "date": date,
            "markdown_content": markdown_content
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"콘텐츠 추출 중 오류가 발생했습니다: {str(e)}")

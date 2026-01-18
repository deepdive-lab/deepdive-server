from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud import article as crud_article
from app.crud import company as crud_company
from app.schemas.article import ArticleUploadRequest, ArticleSummary, ArticleDetail
from app.models.article import Article
from graph.workflow import graph
import trafilatura
from trafilatura.metadata import extract_metadata
import httpx
from datetime import datetime, date
import re

router = APIRouter(prefix="/api/v1", tags=["article"])

async def extract_article_data(url: str):
    try:
        # trafilatura.fetch_url로 가져오기
        downloaded = trafilatura.fetch_url(url)
        # trafilatura.fetch_url이 실패하면 httpx로 직접 가져오기
        if downloaded is None:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, follow_redirects=True)
                response.raise_for_status()
                downloaded = response.text
    
        # metadata 추출
        metadata = extract_metadata(downloaded)
        
        # 2. 본문만 딱 집어서 마크다운으로 변환하기
        markdown_content = trafilatura.extract(
            downloaded,
            output_format='markdown',
            include_tables=True, # 표도 마크다운으로 포함
            include_images=True,
            include_links=True,
            include_comments=False # 댓글 제외
        )
        
        if markdown_content is None or markdown_content.strip() == "":
            raise HTTPException(status_code=400, detail="URL에서 콘텐츠를 추출할 수 없습니다.")
        
        # metadata 처리
        author = ""
        title = ""
        description = ""
        thumbnail = ""
        published_at = ""
        
        if metadata:
            author = metadata.author or ""
            title = metadata.title or ""
            description = metadata.description or ""
            thumbnail = metadata.image or ""
            published_at = metadata.date or ""
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download the article {str(e)}")

    return {
        "author": author,
        "title": title,
        "description": description,
        "thumbnail": thumbnail,
        "published_at": published_at,
        "content": markdown_content
    }

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

@router.get("/articles/data")
async def get_article_data(
    url: str = Query(..., description="추출할 기사의 URL")
):
    return await extract_article_data(url)

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

@router.post("/articles/upload", response_model=ArticleDetail)
async def upload_article(
    request: ArticleUploadRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    URL로부터 기사를 추출하고, 그래프를 통해 처리한 후 DB에 저장합니다.
    """
    # 1. 전체 company 목록 가져오기
    companies = await crud_company.get_companies(db)
    
    # 2. URL에 포함된 company name 찾기
    matched_company = None
    for company in companies:
        if company.name.lower() in request.url.lower():
            matched_company = company
            break
    
    # 3. 매칭되는 company가 없으면 에러
    if matched_company is None:
        raise HTTPException(
            status_code=400, 
            detail=f"URL에 매칭되는 company를 찾을 수 없습니다. URL: {request.url}"
        )
    
    company_id = matched_company.id
    
    # 4. 기사 데이터 추출
    article_data = await extract_article_data(request.url)
    
    # 5. 그래프를 통해 번역/요약 처리
    graph_response = await graph.ainvoke({
        "content": article_data["content"]
    })
    
    # 6. 제목이 없으면 첫 번째 줄이나 기본값 사용
    title = article_data.get("title", "") or article_data["content"].split("\n")[0][:255] or "Untitled"
    if len(title) > 255:
        title = title[:255]
    
    # 7. description 처리 (없으면 summary 앞부분 사용)
    description = article_data.get("description", "") or graph_response.get("summary", "")[:500] or ""
    if len(description) > 1000:
        description = description[:1000]
    
    # 8. published_at 날짜 변환
    published_at_str = article_data.get("published_at", "")
    published_at = date.today()  # 기본값: 오늘
    if published_at_str:
        try:
            # ISO 형식 날짜 파싱 시도
            if isinstance(published_at_str, str):
                # 날짜 문자열에서 날짜 부분만 추출
                date_match = re.search(r'\d{4}-\d{2}-\d{2}', published_at_str)
                if date_match:
                    published_at = datetime.fromisoformat(date_match.group()).date()
        except (ValueError, AttributeError):
            pass  # 파싱 실패 시 기본값 사용
    
    # 9. read_time 계산 (한국어 기준 분당 300자)
    content_length = len(graph_response.get("content", ""))
    read_time = max(1, content_length // 300)  # 최소 1분
    
    # 10. Article 객체 생성
    article = Article(
        url=request.url,
        company_id=company_id,
        title=title,
        description=description,
        summary=graph_response.get("summary", ""),
        content=graph_response.get("content", ""),
        thumbnail_key=article_data.get("thumbnail", "") or "",
        published_at=published_at,
        read_time=read_time,
        view_count=0
    )
    
    # 8. DB에 저장
    saved_article = await crud_article.create_article(db, article)
    
    return saved_article
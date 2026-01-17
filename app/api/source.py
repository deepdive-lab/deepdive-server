from fastapi import APIRouter, Query, HTTPException
import trafilatura
from trafilatura.metadata import extract_metadata
import httpx

router = APIRouter(prefix="/api/v1/sources", tags=["source"])

@router.get("/html")
async def get_html(
    url: str = Query(..., description="추출할 기사의 URL")
):
    try:
        # 1. URL에서 HTML 가져오기 (trafilatura.fetch_url 시도)
        downloaded = trafilatura.fetch_url(url)
        return downloaded
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"HTML 추출 중 오류가 발생했습니다: {str(e)}")

@router.get("/metadata")
async def get_metadata(
    url: str = Query(..., description="추출할 기사의 URL")
):
    try:
        # 1. URL에서 HTML 가져오기 (trafilatura.fetch_url 시도)
        downloaded = trafilatura.fetch_url(url)

        metadata = extract_metadata(downloaded)

        return {
            "title": metadata.title,
            "author": metadata.author,
            "description": metadata.description,
            "thumbnail": metadata.image,
            "published_at": metadata.date,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Metadata 추출 중 오류가 발생했습니다: {str(e)}")

@router.get("/markdown")
async def get_markdown(
    url: str = Query(..., description="추출할 기사의 URL")
):
    try:
        # 1. URL에서 HTML 가져오기 (trafilatura.fetch_url 시도)
        downloaded = trafilatura.fetch_url(url)
        # trafilatura.fetch_url이 실패하면 httpx로 직접 가져오기
        if downloaded is None:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, follow_redirects=True)
                response.raise_for_status()
                downloaded = response.text
        
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
        
        return markdown_content
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"콘텐츠 추출 중 오류가 발생했습니다: {str(e)}")

from graph.state import GraphState
from fastapi import HTTPException
from graph.utils import build_llm_input
from trafilatura.metadata import extract_metadata
from graph.llm import llm
import trafilatura
import logging
import httpx

logger = logging.getLogger(__name__)

async def downloader(state: GraphState):
    
    url = state["url"]

    try:
        # trafilatura.fetch_url로 가져오기
        downloaded = trafilatura.fetch_url(url)
        # trafilatura.fetch_url이 실패하면 httpx로 직접 가져오기
        if downloaded is None:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, follow_redirects=True)
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
        published_at = ""
        
        if metadata:
            author = metadata.author or ""
            description = metadata.description or ""
            thumbnail = metadata.image or ""
            published_at = metadata.date or ""
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download the article {str(e)}")

    return {
        "author": author,
        "description": description,
        "thumbnail": thumbnail,
        "published_at": published_at,
        "content": markdown_content
    }

async def translator(state: GraphState):
    input = build_llm_input(state["content"], "translator")
    response = await llm.ainvoke(input)

    translated_content = response.content
    return {
        "content": translated_content
    }

async def summarizer(state: GraphState):
    input = build_llm_input(state["content"], "summarizer")
    response = await llm.ainvoke(input)

    summary = response.content

    logger.debug(f"Summary: {summary}")

    return {
        "summary": summary
    }

async def enhancer(state: GraphState):
    input = build_llm_input(state["content"], "enhancer")
    response = await llm.ainvoke(input)
    
    enhanced_content = response.content

    return {
        "content": enhanced_content
    }

async def explanator(state: GraphState):
    input = build_llm_input(state["content"], "explanator")
    response = await llm.ainvoke(input)
    
    explained_content = response.content

    logger.debug(f"Explained content: {explained_content}")

    return {
        "content": explained_content
    }

async def finisher(state: GraphState):
    logger.debug(f"Finisher state: {state}")
    
    return state
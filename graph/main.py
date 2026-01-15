from graph.state import GraphState
from fastapi import HTTPException
from graph.utils import build_llm_input
from graph.llm import llm
import trafilatura

async def downloader(state: GraphState):
    try:
        downloaded = trafilatura.fetch_url(state.source_url)
        if downloaded is None:
            raise HTTPException(status_code=400, detail="Failed to download the article")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {
        "html": downloaded
    }

async def translator(state: GraphState) -> GraphState:
    input = build_llm_input(state, "translator")
    response = llm.ainvoke(input)
    state.html = response.content
    return state

async def summarizer(state: GraphState) -> GraphState:
    input = build_llm_input(state, "summarizer")
    response = llm.ainvoke(input)
    state.html = response.content
    return state

async def enhancer(state: GraphState) -> GraphState:
    input = build_llm_input(state, "enhancer")
    response = llm.ainvoke(input)
    state.html = response.content
    return state

async def explanator(state: GraphState) -> GraphState:
    input = build_llm_input(state, "explanator")
    response = llm.ainvoke(input)
    state.html = response.content
    return state

async def finisher(state: GraphState) -> GraphState:
    input = build_llm_input(state, "finisher")
    response = llm.ainvoke(input)
    state.html = response.content
    return state
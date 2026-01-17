from langgraph.graph import StateGraph, START, END
from graph.main import downloader, translator, summarizer, enhancer, explanator, finisher
from graph.state import GraphState, GraphInputState, GraphOutputState
from app.core.config import settings
import os

# LangGraph/LangChain이 os.environ에서 읽을 수 있도록 LangSmith tracing 환경변수 설정
# .env에서 읽은 Settings 값들을 os.environ에 설정
if settings.LANGSMITH_TRACING:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = settings.LANGSMITH_ENDPOINT
    os.environ["LANGCHAIN_API_KEY"] = settings.LANGSMITH_API_KEY
    os.environ["LANGCHAIN_PROJECT"] = settings.LANGSMITH_PROJECT

graph_builder = StateGraph(GraphState, input_state=GraphInputState, output_state=GraphOutputState)

graph_builder.add_node("downloader", downloader)
graph_builder.add_node("translator", translator)
graph_builder.add_node("summarizer", summarizer)
graph_builder.add_node("enhancer", enhancer)
graph_builder.add_node("explanator", explanator)
graph_builder.add_node("finisher", finisher)

graph_builder.add_edge(START, "downloader")
graph_builder.add_edge("downloader", "translator")

graph_builder.add_edge("translator", "enhancer")
graph_builder.add_edge("enhancer", "explanator")
graph_builder.add_edge("explanator", "finisher")

graph_builder.add_edge("downloader", "summarizer")
graph_builder.add_edge("summarizer", "finisher")

graph_builder.add_edge("finisher", END)

graph = graph_builder.compile()
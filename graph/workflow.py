from langgraph.graph import StateGraph, START, END
from graph.main import downloader, translator, summarizer, enhancer, explanator, finisher
from graph.state import GraphState, GraphInputState, GraphOutputState

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
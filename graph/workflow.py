from langgraph.graph import StateGraph, START, END
from graph.main import downloader, translator, summarizer, enhancer, explanator, finisher
from graph.state import GraphState, GraphInputState, GraphOutputState

workflow = StateGraph(state=GraphState, input_state=GraphInputState, output_state=GraphOutputState)

workflow.add_node("downloader", downloader)
workflow.add_node("translator", translator)
workflow.add_node("summarizer", summarizer)
workflow.add_node("enhancer", enhancer)
workflow.add_node("explanator", explanator)
workflow.add_node("finisher", finisher)

workflow.add_edge(START, "downloader")
workflow.add_edge("downloader", ["translator", "summarizer"])
workflow.add_edge("translator", "enhancer")
workflow.add_edge("enhancer", "explanator")
workflow.add_edge("explanator", "finisher")
workflow.add_edge("summarizer", "finisher")
workflow.add_edge("finisher", END)
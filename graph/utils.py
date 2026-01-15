from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from graph.state import GraphState
from typing import List, Dict, Any, Literal

def build_llm_input(state: GraphState, role: Literal["enhancer", "explanator","summarizer","translator"]):
    input : list[BaseMessage] = []

    if role == "enhancer":
        input.append(SystemMessage(content="You are a helpful assistant that enhances the article."))
    elif role == "explanator":
        input.append(SystemMessage(content="You are a helpful assistant that explains the article."))
    elif role == "summarizer":
        input.append(SystemMessage(content="You are a helpful assistant that summarizes the article."))
    elif role == "translator":
        input.append(SystemMessage(content="You are a helpful assistant that translates the article."))

    input.append(HumanMessage(content=f"""
<article>
{state.html}
</article>
"""))
    return input
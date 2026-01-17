from typing import TypedDict, Optional
from datetime import date

class GraphInputState(TypedDict):
    url: str

class GraphOutputState(TypedDict):
    title: Optional[str]
    author: Optional[str]
    description: Optional[str]
    summary: Optional[str]
    
    thumbnail_key: Optional[str]

    published_at: Optional[date]
    read_time: Optional[int]

class GraphState(GraphInputState, GraphOutputState, total=False):
    content: Optional[str]
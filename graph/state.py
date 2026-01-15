from typing import TypedDict, Optional
from datetime import date

class GraphInputState(TypedDict):
    source_url: str

class GraphOutputState(TypedDict):
    title: Optional[str]
    description: Optional[str]
    summary: Optional[str]
    content: str
    
    thumbnail_key: Optional[str]

    published_at: Optional[date]
    read_time: Optional[int]

class GraphState(GraphInputState, GraphOutputState):
    html: Optional[str]
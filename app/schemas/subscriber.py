from datetime import date
from pydantic import BaseModel

class SubscriberResponse(BaseModel):
    """Subscriber 응답 스키마"""
    id: int
    email: str
    created_at: date
    
    class Config:
        from_attributes = True

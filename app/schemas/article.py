from datetime import date
from pydantic import BaseModel

class ArticleUploadRequest(BaseModel):
    url: str

class ArticleSummary(BaseModel):
    """카드 목록용 간략 정보"""
    id: int
    title: str
    description: str
    thumbnail_url: str
    published_at: date
    view_count: int
    
    class Config:
        from_attributes = True

class ArticleDetail(BaseModel):
    """상세 페이지용 전체 정보"""
    id: int
    company_id: int
    title: str
    description: str
    content: str
    original_url: str
    thumbnail_url: str
    published_at: date
    read_time: int
    view_count: int
    
    class Config:
        from_attributes = True
